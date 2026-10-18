"""Fig. 2b of Zhao et al. 2025: plateau (cutting) force f and blunting radius r_b vs stretch ratio lambda.

The plot area of Fig. 2b (frame, ticks, markers, lines, error bars) is part of the 1333 x 1018 px (300 ppi) raster
image embedded on page 3 (tick labels and axis titles are PDF text), so this is a digitization (tier 3).
Writes fig2b.csv and work/fig2b_overlay.png.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
import rastermarkers as rm  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
a = dc.embedded_image(str(PDF), 3)
g = dc.gray(a)
# tick centres measured with rm.tick_centres (darkness-weighted): bottom axis, left axis, right axis
XT = [(765.54, 1.0), (878.54, 1.1), (991.56, 1.2), (1104.57, 1.3), (1217.59, 1.4)]
YL = [(436.0, 0.0), (327.54, 0.05), (218.45, 0.10), (109.55, 0.15), (0.62, 0.20)]
YR = [(436.0, 0.0), (300.45, 100.0), (164.43, 200.0), (28.38, 300.0)]
fx, rx, _ = dc.fit_axis([p for p, v in XT], [v for p, v in XT])
fl, rl, _ = dc.fit_axis([p for p, v in YL], [v for p, v in YL])
fr, rr, _ = dc.fit_axis([p for p, v in YR], [v for p, v in YR])
REGION = (0, 437, 767, 1331)
FRAME_TOP, FRAME_BOT = 1, 436

series = [
    # name, marker colours (the 'Fracture' marker at lambda ~1.45 has a darker blue / a white zigzag), axis
    ("Cutting force", [(51, 149, 216), (46, 117, 182)], fl, "f_N"),
    ("Blunting radius", [(255, 0, 0)], fr, "r_b_um"),
]
rows, ov = [], []
for name, cols, fy, unit in series:
    mask = rm.colour_mask(a, cols)
    mks = rm.find_markers(mask, REGION, k=5, min_area=60)
    # drop blobs in the legend box (page 413-452 pt; image columns >= 1080, rows 200-310)
    mks = [m for m in mks if not (1075 <= m["cx"] <= 1320 and 195 <= m["cy"] <= 315)]
    for n, mk in enumerate(mks):
        icon = mk["w"] < 12   # Fracture icon: the white zigzag splits the square
        if icon:
            cx, cy, top, bot = rm.icon_centre(mask, mk)
            eb = rm.error_bar(mask, cx, cy, top, bot, FRAME_TOP, FRAME_BOT, window=60)
            if eb["upper"][0] is not None and eb["lower"][0] is not None:
                cy = (eb["upper"][0] + eb["lower"][0]) / 2     # symmetric bar: centre between the caps
        else:
            cx, cy, top, bot = rm.centre(mask, mk)
            eb = rm.error_bar(mask, cx, cy, top, bot, FRAME_TOP, FRAME_BOT)
        up, upc = eb["upper"]
        lo, loc = eb["lower"]
        flag = []
        if upc:
            flag.append("upper bar clipped at frame")
        if loc:
            flag.append("lower bar clipped at frame")
        if up is None and not upc:
            flag.append("no upper cap found (bar hidden behind marker?)")
        if lo is None and not loc:
            flag.append("no lower cap found (bar hidden behind marker or frame)")
        if icon and name == "Cutting force":
            flag.append("icon square reaches the bottom frame; y centre uncertain by ~+-3 px (+-0.0015 N)")
        is_frac = n == len(mks) - 1 and fx(cx) > 1.43
        rows.append([name + (" (Fracture marker)" if is_frac else ""), float(fx(cx)), float(fy(cy)),
                     float(fy(lo)) if lo is not None else np.nan, float(fy(up)) if up is not None else np.nan,
                     unit, round(cx, 1), round(cy, 1), "; ".join(flag)])
        ov.append((cx, cy))
        for r in (up, lo):
            if r is not None:
                ov.append((cx, r))

head = [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 2b: plateau (cutting) force f (blue squares, left axis 'f (N)') and",
    "  blunting radius r_b (red squares, right axis 'r_b (um)') vs stretch ratio lambda; error bars = standard deviation",
    "  (caption). The last point of each series (lambda ~1.45) carries the 'Fracture' icon (white zigzag).",
    "Columns: series; lambda; value = f in N or r_b in um (see unit); err_low/err_high = the lower/upper error-bar cap",
    "  (same unit; empty where no cap is visible); unit; px_x/px_y = marker centre in the embedded image (pixels);",
    "  flag = notes. Points joined by straight lines in the figure (not data).",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image on page 3 (1333 x 1018 px; the figure's",
    "  plot areas of b and c are raster, its tick labels are PDF text). Squares found by colour mask + 5x5 opening;",
    "  x centre = middle of the square's columns, y centre = middle of the run of rows fully covered around x",
    "  (square plus touching caps; bars are symmetric); for the two Fracture-icon squares x = the error-bar column and",
    "  y = midway between its two caps (red) or the middle of the square's rows (blue, lower cap hidden by the frame);",
    "  the icon squares are ~17 px, larger than the others (14 px); caps = rows where >= 18 of 27 pixels around x are set,",
    "  reached along the bar column. Calibration on the tick marks (darkness-weighted centres):",
    "  x: %s; max residual %.2g" % (", ".join(f"{v:g}@{p}px" for p, v in XT), rx),
    "  y (f): %s; max residual %.2g N" % (", ".join(f"{v:g}@{p}px" for p, v in YL), rl),
    "  y (r_b): %s; max residual %.2g um" % (", ".join(f"{v:g}@{p}px" for p, v in YR), rr),
    "Uncertainty: about +-1 px: +-0.001 in lambda, +-0.0005 N in f, +-0.8 um in r_b.",
]
dc.write_csv(HERE / "fig2b.csv", head, ["series", "lambda", "value", "err_low", "err_high", "unit", "px_x", "px_y", "flag"],
             rows, fmt=["{}", "{:.4f}", "{:.5g}", "{:.5g}", "{:.5g}", "{}", "{:.1f}", "{:.1f}", "{}"])
for r in rows:
    print(r)
(ROOT / "work").mkdir(exist_ok=True)
dc.overlay(a[0:440, 760:1333].copy(), [(x - 760, y) for x, y in ov], str(ROOT / "work" / "fig2b_overlay.png"),
           colour=(0, 220, 0))
