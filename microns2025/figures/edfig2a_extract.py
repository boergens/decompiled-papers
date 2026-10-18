#!/usr/bin/env python3
"""Extended Data Fig. 2A (p. 25): histogram of number of edits, log-log. Vector paths -> edfig2a.csv.

Tick labels are glyph outlines (no text); the decades were read off the render and paired with the long
(major) tick marks: x 10^0..10^3 at 83.96, 140.70, 197.43, 254.17 pt; y 10^0..10^4 at 275.62 ... 93.54 pt.
"All Cells" = 76 grey filled rectangles (matplotlib bars); "Dendrite Proofreading Complete" (blue #0073b1)
and "Cleaned Axons" (orange #ee7e31) = step outlines. Bins are equal in log space (2.0059 pt wide).
"""
import sys
from pathlib import Path

import numpy as np
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import pdfplot as pp  # noqa: E402

page = pymupdf.open(mc.PDF)[24]
dr = pp.drawings(page, pp.R(74, 58, 293, 276))

maj = lambda o: [t["pos"] for t in pp.tick_marks(dr, o, max_len=3, min_len=2.4)]
xt = sorted(set(round(p, 2) for p in maj("x")))
yt = sorted(set(round(p, 2) for p in maj("y")), reverse=True)
assert len(xt) == 4 and len(yt) == 5, (xt, yt)
X = mc.LinAxis(list(zip(xt, [1, 10, 100, 1000])), log=True)
Y = mc.LinAxis(list(zip(yt, [1, 10, 100, 1000, 10000])), log=True)
BASE = yt[0]

grey = sorted(d["rects"][0] for d in dr if pp.hexcolor(d["fill"]) == "#c6c8ca" and d["rects"][0][2] - d["rects"][0][0] < 3)
x0s = np.array([r[0] for r in grey])
k = np.round((x0s - x0s[0]) / 2.0059)
W, X0 = np.polyfit(k, x0s, 1)  # bin width and first edge in pt
rows = []
qa = []
for r in grey:
    kb = int(round((r[0] - X0) / W))
    l, rr = X0 + kb * W, X0 + (kb + 1) * W
    qa.append(((r[0] + r[2]) / 2, r[1]))
    rows.append(["All Cells", kb, f"{X(l):.5g}", f"{X(rr):.5g}", f"{Y(r[1]):.4g}", "bar"])

for name, col in [("Dendrite Proofreading Complete", "#0073b1"), ("Cleaned Axons", "#ee7e31")]:
    d = max((d for d in dr if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == col), key=lambda d: d["n_items"])
    pts = d["points"]
    level = {}
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        if abs(ya - yb) < 1e-3 and xb > xa:  # horizontal step top
            for kb in range(int(round((xa - X0) / W)), int(round((xb - X0) / W))):
                level[kb] = ya
    for kb in sorted(level):
        l, rr = X0 + kb * W, X0 + (kb + 1) * W
        y = level[kb]
        flag = "at_floor(<=1)" if abs(y - BASE) < 0.05 else "step"
        qa.append(((l + rr) / 2, y))
        rows.append([name, kb, f"{X(l):.5g}", f"{X(rr):.5g}", f"{Y(y):.4g}", flag])

mc.write_csv(Path(__file__).with_name("edfig2a.csv"), [
    "Extended Data Fig. 2A (p. 25 of microns2025.pdf): histogram of number of edits per object associated with a nucleus.",
    "Provenance: tier 2, vector paths in the PDF (exact up to PDF precision, ~0.01 pt).",
    "Columns: series (legend name); bin (bin index, 0 = first bin at 10^0); bin_left, bin_right (number of edits, bin edges;",
    "  bins are equal-width in log10, width %.5f decades); count (number of cells = bar/step height); kind:" % (W * X.a),
    "  bar = grey filled bar; step = step outline; at_floor(<=1) = the step runs along the bottom axis (10^0), i.e. count 0 or 1.",
    "Bars of height 1 or 0 are not drawn on the log axis, so bins missing for All Cells have count <= 1.",
    "Counts are 10^(height); values come out as integers to within ~0.5 % (log-scale rounding).",
    mc.LinAxis.describe(X, "x (log10 edits)"), mc.LinAxis.describe(Y, "y (log10 count)"),
    "Tick labels are outlined glyphs; decades read from the rendered figure.",
], ["series", "bin", "bin_left", "bin_right", "count", "kind"], rows)
mc.overlay_pts(24, (37, 47, 300, 305), qa, "overlay_edfig2a.png", r=2)
