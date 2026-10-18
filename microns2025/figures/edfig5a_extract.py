#!/usr/bin/env python3
"""Extended Data Fig. 5a (p. 28): precision-recall curves across residual percentile (left) and separation percentile
(right) thresholds for three automatch methods. Vector paths -> edfig5a.csv.
Axes calibrated on the grid lines: x (recall) 0.0 ... 1.0 step 0.1, y (precision) 0.800 ... 1.000 step 0.025.
Series by stroke colour and legend: #f0af99 fiducial-based automatch, #e96852 vessel-based automatch,
#cd1d30 fiducial-vessel agreements. Each curve is a polyline; its vertices are the plotted points."""
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[27]
SER = {"#f0af99": "fiducial-based automatch", "#e96852": "vessel-based automatch", "#cd1d30": "fiducial-vessel agreements"}
Y = mc.LinAxis(list(zip([190.13, 174.98, 159.84, 144.69, 129.55, 114.40, 99.25, 84.11, 68.96],
                        [0.800, 0.825, 0.850, 0.875, 0.900, 0.925, 0.950, 0.975, 1.000])))
rows, qa = [], []
for panel, x0 in [("residual percentile", 124.08), ("separation percentile", 353.59)]:
    X = mc.LinAxis([(x0 + 14.634 * k, k / 10) for k in range(11)])
    dr = pp.drawings(page, pp.R(x0 - 2, 60, x0 + 150, 200), how="inside")
    for d in dr:
        c = pp.hexcolor(d["color"])
        if d["kind"] == "stroke" and c in SER and d["n_items"] > 3:
            for i, (px, py) in enumerate(d["points"]):
                rows.append([panel, SER[c], i, f"{X(px):.4f}", f"{Y(py):.4f}"])
                qa.append((px, py))
mc.write_csv(Path(__file__).with_name("edfig5a.csv"), [
    "Extended Data Fig. 5a (p. 28 of microns2025.pdf): precision-recall curves relative to manual matches.",
    "Provenance: tier 2, vector polylines (vertices exact to ~0.01 pt = ~0.0001 recall / 0.00002 precision).",
    "Columns: panel (plot title: 'residual percentile' left, 'seperation percentile' [sic] right); series (legend);",
    "vertex (index along the polyline as drawn); recall (x); precision (y). The threshold value of each vertex is not given in the figure.",
    Y.describe("y"), "x: recall = (page_x - x0) / 146.34 with x0 = 124.08 (left) or 353.59 (right) pt.",
], ["panel", "series", "vertex", "recall", "precision"], rows)
mc.overlay_pts(27, (48, 50, 553, 218), qa, "overlay_edfig5a.png", r=2)
