"""Extended Data Fig. 3d: histograms of lost, partial and adjacent sectioning events (5.5 dpf series),
digitized from the 150 ppi raster image on PDF page 35 (tier 3). Writes edfig3d.csv + overlay in work/.

Main histograms (bins of 50 sections, ~1.2 px per bin): one row per image pixel column with a bar,
giving the column's z range and the bar height there. Insets (bins of 5 sections, ~2.3 px per bin):
one row per bar, assigned to the 5-section bin under its centre, height rounded to whole sections.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, fit_axis, overlay, write_csv  # noqa: E402
from histo_common import column_heights, group_bars, tick_centres  # noqa: E402

PDF = ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"
a = embedded_image(str(PDF), 35)
g = a.astype(float).mean(2)
ink = 255 - g

# ---- shared x axis of the three main histograms: 7 ticks below the bottom axis (row 725), 0..18000
xt = tick_centres(ink[725, 465:925], 100)
xt = [465 + t for t in xt]
assert len(xt) == 7, xt
fx, resx, mx = fit_axis(xt, [0, 3000, 6000, 9000, 12000, 15000, 18000])

# ---- main panels: axis line rows, y tick column, tick values
main = {
    "lost": dict(axis=556, ticks=(480, 556), vals=list(range(12, 0, -1)), skip=0, total=244),
    "partial": dict(axis=668, ticks=(600, 668), vals=list(range(10, 0, -1)), skip=0, total=283),
    "adjacent": dict(axis=722, ticks=(712, 721), vals=[1], skip=1, total=5),
}
rows, pts, notes = [], [], []
for name, p in main.items():
    tr = tick_centres(ink[p["ticks"][0]:p["ticks"][1], 472], 100)
    tr = [p["ticks"][0] + t for t in tr]
    assert len(tr) == len(p["vals"]), (name, tr)
    fy, resy, my = fit_axis(tr + [p["axis"] + 0.5], p["vals"] + [0])
    pxu = abs(1 / my)
    h = column_heights(g, p["axis"] - 1, 478, 910, thr=215, skip=p["skip"])
    est = 0.0
    for i, hp in enumerate(h):
        if hp == 0:
            continue
        c = 478 + i
        val = hp / pxu
        z0, z1 = float(fx(c - 0.5)), float(fx(c + 0.5))
        est += val * (z1 - z0) / 50
        rows.append((name, 50, round(z0, 1), round(z1, 1), round((z0 + z1) / 2, 1), int(hp), round(val, 3), ""))
        pts.append((c, p["axis"] - hp))
    notes.append(f"{name}: {int((h > 0).sum())} columns with bars; area-based estimate of the total count = {est:.1f} "
                 f"(the panel title gives {p['total']}); y scale {pxu:.2f} px per section/bin, y-fit residual {resy:.2f}")

# ---- insets (5-section bins): lost inset 5000..5500 above axis row 495, partial inset 1250..1750 above row 602
insets = {
    "lost_inset": dict(axis=495, xr=(5000, 5500), xrow=498, yticks=(480, 494)),
    "partial_inset": dict(axis=602, xr=(1250, 1750), xrow=605, yticks=(586, 601)),
}
for name, p in insets.items():
    xti = [680 + t for t in tick_centres(ink[p["xrow"], 680:935], 100)]
    assert len(xti) == 5, (name, xti)
    lo, hi = p["xr"]
    fxi, rxi, _ = fit_axis(xti, list(np.linspace(lo, hi, 5)))
    tr = [p["yticks"][0] + t for t in tick_centres(ink[p["yticks"][0]:p["yticks"][1], 690], 100)]
    assert len(tr) == 2, (name, tr)
    fyi, ryi, myi = fit_axis(tr + [p["axis"] + 0.5], [2, 1, 0])
    pxu = abs(1 / myi)
    # one value per 5-section bin: tallest bar run among the columns whose centres fall in the bin's central half
    # start 2 columns right of the inset's y-axis line (its anti-aliased edge would read as a bar)
    c_lo, c_hi = int(round(xti[0])) + 2, int(xti[-1]) + 3
    h = column_heights(g, p["axis"] - 2, c_lo, c_hi, thr=200, skip=1)
    inv = lambda z: (z - fxi(0)) / (fxi(1) - fxi(0))  # z -> column
    n_tot = 0
    for b0 in range(lo, hi, 5):
        ca, cb = inv(b0 + 1.25), inv(b0 + 3.75)
        cols = [c for c in range(int(np.floor(ca)), int(np.ceil(cb)) + 1) if ca <= c <= cb and c_lo <= c < c_hi]
        if not cols:
            cols = [int(round(inv(b0 + 2.5)))]
        hp = max(h[c - c_lo] for c in cols)
        if hp == 0:
            continue
        cnt = int(round(hp / pxu))
        n_tot += cnt
        rows.append((name, 5, b0, b0 + 5, b0 + 2.5, int(hp), cnt, f"cols {cols[0]}-{cols[-1]}"))
        pts += [(c, p["axis"] - hp) for c in cols]
    notes.append(f"{name}: x fit residual {rxi:.2f} sections, y scale {pxu:.2f} px per section; {n_tot} sections in the inset bars")

hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Extended Data Fig. 3d: histograms of lost, partial and adjacent",
    "(lost-partial or partial-partial) events per bin of 50 sections along the 5.5dpf series (x: position in series, z);",
    "insets: 5-section bins for z 5000-5500 (lost) and 1250-1750 (partial).",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster image on PDF page 35 (figures/edfig3d_extract.py).",
    f"x calibrated on the 7 ticks 0..18000 (labels 0, 6000, 12000, 18000 printed), max residual {resx:.1f} sections; "
    f"one pixel column = {abs(mx):.1f} sections, so main-histogram bins (50 sections) are NOT resolved individually.",
    "Main histograms: one row per pixel column containing a bar: z_left/z_right = the column's z range, height_px = grey bar",
    "run above the axis, value = sections per 50-section bin at that column (uncertainty +-1 px, i.e. about +-0.17).",
    "Insets: one row per non-empty 5-section bin (bin_start, bin_end): tallest bar among the pixel columns in the central half of the bin",
    "(~2.3 px per bin, so a bin can be off by one where bars touch); value = count, rounded to whole sections.",
    "A bar in the first inset bin (z 5000-5005 / 1250-1255) would merge with the inset y-axis line and cannot be read.",
    "The dashed lines (number of lost/partial sections per bin if uniformly distributed) are not extracted.",
] + notes + [
    "columns: series; bin_size; z_left (or bin_start); z_right (or bin_end); z_centre; height_px; value; note",
]
write_csv(HERE / "edfig3d.csv", hdr, ["series", "bin_size", "z_left", "z_right", "z_centre", "height_px", "value", "note"], rows,
          fmt=["{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"])
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts, str(ROOT / "work" / "edfig3d_overlay.png"))
print("\n".join(notes))
