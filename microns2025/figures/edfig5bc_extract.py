#!/usr/bin/env python3
"""Extended Data Fig. 5b, c (p. 28): heat maps over max residual percentile (rows) x min separation percentile
(columns) for the fiducial-based (left), vessel-based (middle) and fiducial-vessel agreement (right) automatches;
b colour = precision, c colour = # neurons. Vector paths -> edfig5b.csv, edfig5c.csv.

Each cell is a filled rectangle. The tick marks sit on the cell EDGES (seaborn/pcolormesh style): x ticks 0.0 ... 1.0
on the column edges (20 columns of 0.05); y ticks 0.1 ... 1.0 (b; the top edge is 0.05, 19 rows) or 0.0 ... 1.0
(c; 20 rows) on the row edges. Each cell is given with its edge values. Which threshold inside a cell the value belongs
to is not stated in the figure.
Values from colour: each colour bar is an embedded 44 x 864 px raster; its bbox and tick marks (b: 1.000 at 239.08 pt
... 0.800 at 342.68 pt; c: 40k at 389.90 ... 0 at 493.49 pt) give value per colour-bar row; each cell fill is matched
to the nearest colour-bar row."""
import sys
from pathlib import Path

import numpy as np
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[27]
f2 = lambda v: f"{round(float(v), 2) + 0.0:.2f}"
PANELS = ["fiducial-based automatch", "vessel-based automatch", "fiducial-vessel agreements"]
CB = {"b": [(183.584, 238.999, 188.864, 342.679), (349.544, 238.999, 354.944, 342.679), (515.624, 238.999, 520.904, 342.679)],
      "c": [(184.904, 389.839, 190.184, 493.519), (353.024, 389.839, 358.304, 493.519), (521.144, 389.839, 526.424, 493.519)]}
TICKS = {"b": list(zip([239.08, 252.03, 264.98, 277.93, 290.88, 303.83, 316.78, 329.73, 342.68],
                       [1.000, 0.975, 0.950, 0.925, 0.900, 0.875, 0.850, 0.825, 0.800])),
         "c": list(zip([389.90, 415.80, 441.70, 467.60, 493.49], [40000, 30000, 20000, 10000, 0]))}
YR = {"b": (240, 345), "c": (386, 496)}
for panel in "bc":
    V = mc.LinAxis(TICKS[panel])
    rows, qa, worst = [], [], 0
    for k, cb in enumerate(CB[panel]):
        cols, frac = mc.colorbar_lut(28, cb)
        val = V(cb[3] - frac * (cb[3] - cb[1]))
        xa = cb[0] - 120 if k else 60
        dr = pp.drawings(page, pp.R(xa, YR[panel][0], cb[0] - 1, YR[panel][1]), how="inside")
        cells = [d for d in dr if d["kind"] == "fill" and d["rects"] and d["n_items"] == 1
                 and d["rect"][2] - d["rect"][0] < 8 and pp.hexcolor(d["fill"]) not in ("#000000", "#252125", "#ffffff")]
        xe = sorted(mc.dedupe([d["rect"][0] for d in cells] + [d["rect"][2] for d in cells], 0.3))
        ye = sorted(mc.dedupe([d["rect"][1] for d in cells] + [d["rect"][3] for d in cells], 0.3))
        assert len(xe) == 21, len(xe)
        X = mc.LinAxis([(xe[0], 0.0), (xe[-1], 1.0)])
        Y = mc.LinAxis([(ye[0], 0.05 if panel == "b" else 0.0), (ye[-1], 1.0)])
        for d in cells:
            x0, y0, x1, y1 = d["rect"]
            i, dist = mc.nearest_colour([v * 255 for v in d["fill"][:3]], cols)
            worst = max(worst, dist)
            rows.append([PANELS[k], f2(X(x0)), f2(X(x1)), f2(Y(y0)), f2(Y(y1)),
                         f"{val[i]:.4f}" if panel == "b" else f"{val[i]:.0f}", f"{dist:.1f}", pp.hexcolor(d["fill"])])
            qa.append(((x0 + x1) / 2, (y0 + y1) / 2))
    rows.sort(key=lambda r: (PANELS.index(r[0]), float(r[3]), float(r[1])))
    what = "precision (relative to manual matches)" if panel == "b" else "# neurons remaining after the thresholds"
    res = "~0.0003 precision" if panel == "b" else "~60 neurons"
    mc.write_csv(Path(__file__).with_name(f"edfig5{panel}.csv"), [
        f"Extended Data Fig. 5{panel} (p. 28 of microns2025.pdf): heat maps of {what} over max residual percentile (rows)",
        "and min separation percentile (columns), for three automatch tables (column 'automatch', the panel titles).",
        "Provenance: cell edges tier 2 (vector rectangles, exact); value tier 3 (cell colour matched to the raster colour bar,",
        f"resolution {res}; worst RGB distance {worst:.1f} of 441).",
        "Columns: automatch; sep_lo, sep_hi (min separation percentile, cell edges); res_lo, res_hi (max residual percentile, cell edges,",
        "res_lo is the top edge of the cell in the plot); value; colour_dist; fill.",
        V.describe("colour bar"),
    ], ["automatch", "sep_lo", "sep_hi", "res_lo", "res_hi", "value", "colour_dist", "fill"], rows)
    mc.overlay_pts(27, (40, YR[panel][0] - 15, 560, YR[panel][1] + 20), qa, f"overlay_edfig5{panel}.png", r=2)
