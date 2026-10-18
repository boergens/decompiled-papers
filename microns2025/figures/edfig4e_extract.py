#!/usr/bin/env python3
"""Extended Data Fig. 4e (p. 27): histogram of oracle scores, matched units (blue #4470ae) and control units
(orange #da8054). Vector paths -> edfig4e.csv. Bars are filled rectangles 1.2847 pt wide (bins of 0.01363 oracle-score
units); zero-height bars are degenerate 2-item paths on the baseline. Axes calibrated on the x tick marks 0.0, 0.2,
0.4, 0.6 (413.90 ... 470.46 pt) and the white y grid lines 0, 50, ..., 300 (234.45 ... 168.97 pt); tick labels are
outlined glyphs read from the render."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[26]
X = mc.LinAxis(list(zip([413.90, 432.76, 451.61, 470.46], [0.0, 0.2, 0.4, 0.6])))
Y = mc.LinAxis(list(zip([234.45, 223.53, 212.62, 201.71, 190.80, 179.89, 168.97], range(0, 301, 50))))
dr = pp.drawings(page, pp.R(404, 160, 486, 236), how="inside")
rows, qa = [], []
for name, col in [("matched units", "#4470ae"), ("control units", "#da8054")]:
    bars = sorted(d["rect"] for d in dr if pp.hexcolor(d["fill"]) == col and d["rect"][2] - d["rect"][0] < 2)
    for x0, y0, x1, y1 in bars:
        rows.append([name, f"{X(x0):.4f}", f"{X(x1):.4f}", f"{Y(y0):.2f}"])
        qa.append(((x0 + x1) / 2, y0))
mc.write_csv(Path(__file__).with_name("edfig4e.csv"), [
    "Extended Data Fig. 4e (p. 27 of microns2025.pdf): distribution of oracle scores for matched units and nearest-unit controls.",
    "Provenance: tier 2, vector paths (bar edges and tops exact to ~0.01 pt = ~0.05 count).",
    "Columns: series (legend); bin_left, bin_right (oracle score); count (bar height, y axis 'count').",
    "Bars of both series are drawn on the same bins, the matched-units bars on top of the control-units bars.",
    X.describe("x"), Y.describe("y"),
], ["series", "bin_left", "bin_right", "count"], rows)
mc.overlay_pts(26, (385, 150, 512, 252), qa, "overlay_edfig4e.png", dpi=600, r=2)
