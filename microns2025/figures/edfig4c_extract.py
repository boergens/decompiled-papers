#!/usr/bin/env python3
"""Extended Data Fig. 4c (p. 27): 2D histogram of residual (um, y) vs separation score (um, x), colour = count.
Vector paths -> edfig4c.csv. Each non-empty bin is a filled rectangle (~0.73 x 0.72 pt); empty bins are not drawn
(white background). Axes (seaborn style, no tick marks; tick labels are outlined glyphs) are calibrated on the white
grid lines: x -20, -10, 0, 10, 20 at 409.84 ... 472.81 pt; y 0, 5, ..., 30 at 126.47 ... 59.98 pt.
Count from the colour: the colour bar is an embedded 33 x 624 px image (482.89..486.63 x 55.39..130.10 pt) with tick marks
0, 10, ..., 70 at 130.10 ... 56.44 pt; each bin's fill is matched to the nearest colour-bar row."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[26]
X = mc.LinAxis(list(zip([409.84, 425.58, 441.33, 457.07, 472.81], [-20, -10, 0, 10, 20])))
Y = mc.LinAxis(list(zip([126.47, 115.39, 104.31, 93.23, 82.15, 71.06, 59.98], [0, 5, 10, 15, 20, 25, 30])))
C = mc.LinAxis(list(zip([130.10, 119.57, 109.05, 98.53, 88.01, 77.48, 66.96, 56.44], range(0, 71, 10))))
cols, frac = mc.colorbar_lut(27, (483, 55, 487, 130))
ypt = 130.10 - frac * (130.10 - 55.39)
counts = C(ypt)
dr = pp.drawings(page, pp.R(401, 54, 478.5, 130), how="inside")
rows, qa, worst = [], [], 0
for d in dr:
    if not (d["kind"] == "fill" and d["rects"] and d["n_items"] == 1):
        continue
    x0, y0, x1, y1 = d["rect"]
    if x1 - x0 > 1 or y1 - y0 > 1 or pp.hexcolor(d["fill"]) == "#ffffff":
        continue
    i, dist = mc.nearest_colour([v * 255 for v in d["fill"][:3]], cols)
    worst = max(worst, dist)
    rows.append([f"{X(x0):.3f}", f"{X(x1):.3f}", f"{Y(y1):.3f}", f"{Y(y0):.3f}", f"{counts[i]:.1f}", round(counts[i]),
                 f"{dist:.1f}", pp.hexcolor(d["fill"])])
    qa.append(((x0 + x1) / 2, (y0 + y1) / 2))
rows.sort(key=lambda r: (float(r[2]), float(r[0])))
mc.write_csv(Path(__file__).with_name("edfig4c.csv"), [
    "Extended Data Fig. 4c (p. 27 of microns2025.pdf): 2D histogram of separation score (x, um) and residual (y, um)",
    "for manually matched units. One row per non-empty bin (empty bins are not drawn).",
    "Provenance: bin positions tier 2 (vector rectangles, exact); count tier 3 (bin colour matched to the raster colour bar;",
    f"count resolution ~0.1, worst RGB distance {worst:.1f}; counts should be integers, count_int is the rounded value).",
    "Columns: x_left, x_right (separation score bin edges, um); y_bottom, y_top (residual bin edges, um); count (from colour);",
    "count_int; colour_dist (RGB distance to the colour bar, 0-441); fill (bin colour as drawn).",
    X.describe("x"), Y.describe("y"), C.describe("colour bar"),
], ["x_left", "x_right", "y_bottom", "y_top", "count", "count_int", "colour_dist", "fill"], rows)
mc.overlay_pts(26, (390, 50, 510, 145), qa, "overlay_edfig4c.png", dpi=600, r=1)
