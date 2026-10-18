"""Digitize the line profiles of Figure 16(a) and 16(b) of Xu et al. 2017 (PDF p. 27): electron counts along a line.

Source: the embedded raster image of Figure 16 (2466 x 1677 px, ~345 ppi); the two profile plots are its bottom strip.
    python3 -I -B figures/fig16ab_extract.py  -> figures/fig16a.csv, figures/fig16b.csv (+ work/fig16ab_overlay.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import write_csv, overlay  # noqa: E402
from xu_helpers import load, lin, work_path  # noqa: E402

a = load(27).astype(int)
dark = a.mean(2) < 170
ROW_TEXT = 1430      # the printed annotations ("478 electrons/pixel ...") start below this row (< ~390 counts)

PANELS = {
    # a: frame cols 98.5 / 1255.5, rows 1189.5 (top) / 1661.5 (bottom); 17 left-axis ticks every 29.5 px = 50 counts,
    #    labels 0, 200, 400, 600, 800 -> the frame spans 0-800.
    "a": dict(xl=98.5, xr=1255.5, fy=lin(1661.5, 0, 1189.5, 800), top=1189.5, bot=1661.5, drops=[],
              cal="y calibrated on the left-axis ticks (0 at row 1661.5, 800 at row 1189.5; 17 ticks every 50 counts, max deviation < 1 px)"),
    # b: frame cols 1353.5 / 2427.5, rows 1186 / 1663; grey grid lines 600, 400, 200 at rows 1298, 1419.5, 1541 (labels at left).
    "b": dict(xl=1353.5, xr=2427.5, fy=lin(1541, 200, 1298, 600), top=1186, bot=1663, drops=[(1543, 1548), (1717, 1722)],
              cal="y calibrated on the grey grid lines 200 and 600 (rows 1541, 1298); the 400 line (1419.5) and the bottom frame (0, row 1662.5) agree within 0.5 px"),
}
from scipy import ndimage  # noqa: E402
pts = []
for key, P in PANELS.items():
    fx = lin(P["xl"], 0.0, P["xr"], 1.0)
    # keep only the profile: large connected pieces of dark pixels inside the frame (frame tick marks are small pieces)
    win = np.zeros_like(dark)
    win[int(P["top"]) + 3:ROW_TEXT, int(P["xl"]) + 3:int(P["xr"]) - 2] = True
    lab, n = ndimage.label(dark & win, structure=np.ones((3, 3)))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    curve = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz > 80])
    rows = []
    for c in range(int(P["xl"]) + 4, int(P["xr"]) - 3):
        r = np.nonzero(curve[int(P["top"]) + 7:ROW_TEXT, c])[0]
        flag = ""
        if any(lo <= c <= hi for lo, hi in P["drops"]):
            flag = "vertical drop to 0 (line continues below the plotted range shown)"
        if len(r) == 0:
            col = dark[ROW_TEXT:int(P["bot"]) - 2, c]
            rows.append((c, float(fx(c)), np.nan, np.nan, np.nan, "curve at ~0 counts, on the bottom frame (not separable)" if key == "b" else "no line pixels"))
            continue
        top, bot = int(P["top"]) + 7 + r.min(), int(P["top"]) + 7 + r.max()
        mid = (top + bot) / 2
        rows.append((c, float(fx(c)), float(P["fy"](mid)), float(P["fy"](top)), float(P["fy"](bot)), flag))
        pts += [(c, top), (c, bot)]
    write_csv(str(HERE / f"fig16{key}.csv"), [
        f"Xu et al. 2017 eLife 6:e25916, Figure 16({key}): line profile 'Electron Counts' along the line drawn in the image above it.",
        "x has no scale in the figure: x_frac = position as a fraction of the plot-frame width (0 = left frame, 1 = right frame);",
        "  x_px = column of the source image. One row per pixel column.",
        "counts_mid / counts_max / counts_min = middle, top and bottom of the plotted (noisy) line within that pixel column, in electron counts.",
        f"Provenance: tier 3, digitized from the embedded raster image (~345 ppi, no vector data in the PDF) by fig16ab_extract.py; {P['cal']}.",
        "  Dark-pixel mask (grey < 170), connected pieces > 80 px only (drops the frame tick marks); rows below the printed annotations' top edge are not searched, so the profile is",
        "  only extracted above ~390 counts" + (" (it never goes lower in panel a)." if key == "a" else "; between the two vertical drops (black region of the image, x_frac ~0.18-0.34) the line lies on the bottom frame at ~0 counts and is flagged."),
        f"Uncertainty: +-{abs(P['fy'](0) - P['fy'](1)):.1f} counts per pixel row; the line is ~2 px wide.",
        "Annotations printed in the panel: " + ("'478 electrons/pixel On Epoxy 5.5% detected', '634 electrons/pixel On Pt[(C6H5)3P]4 7.3% detected', '8650 primary 1.2 KeV electrons per pixel'."
                                                 if key == "a" else "'468 electrons/pixel On Epoxy 5.3% detected', '500-700 electrons/pixel On Neuropil 5.6%-7.9% detected', '8830 primary 1.2 KeV electrons per pixel'; unlabelled vertical grey grid lines at x_frac 0.18, 0.36, 0.54, 0.72, 0.91."),
    ], ["x_px", "x_frac", "counts_mid", "counts_max", "counts_min", "flag"], rows,
        fmt=["{}", "{:.4f}", "{:.1f}", "{:.1f}", "{:.1f}", "{}"])
    v = np.array([r[2] for r in rows if r[2] == r[2]])
    print(key, len(rows), "rows; median counts", np.median(v))
overlay(a.astype(np.uint8), pts, work_path("fig16ab_overlay.png"))
