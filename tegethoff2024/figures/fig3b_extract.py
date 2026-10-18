"""Digitize Figure 3B of Tegethoff & Briggman 2024 (PDF p.5): hardness vs relative humidity.

Source: the embedded JPEG of Figure 3 (1061 x 1305 px, ~372 ppi), panel B in its bottom half.
    python3 -I fig3b_extract.py   -> fig3b.csv (+ ../work/fig3b_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(51)
fy, ry, sy = fit_axis([720.0, 788.0, 856.0, 924.0, 992.0, 1060.0, 1129.0, 1197.0], [14, 12, 10, 8, 6, 4, 2, 0])
fx, rx, sx = fit_axis([105.0, 292.0, 478.0, 665.0, 852.0, 1039.0], [0, 20, 40, 60, 80, 100])
BOX = (108, 747, 1050, 1194)          # starts below the small sequence numbers printed above the columns
m = gray(a) < 100
rows, pts = dot_rows({"EMbed 812 MH": m}, BOX, fx, fy, single_area=26, min_area=10)
SEQ = {15: 6, 25: 5, 30: 2, 37: 1, 50: 3, 70: 4}   # small numbers printed above each column (read from the figure)
out = []
for r in sorted(rows, key=lambda r: (r[1], r[2])):
    col = min(SEQ, key=lambda c: abs(c - r[1]))
    out.append((SEQ[col], r[1], r[2], r[5]))
save(mark(a, pts), "fig3b_overlay.png")
write_csv(os.path.join(HERE, "fig3b.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 3B: hardness of an EMbed 812 MH resin block measured at",
    "  different relative humidities.",
    "Columns: sequence = the small number printed above the column (order in which the measurements were made, per",
    "  the caption); humidity_percent = x position; hardness_HV = Vickers hardness; n_in_blob = markers in the merged blob",
    "  this point was split from (1 = isolated; >1 = split with k-means, positions approximate).",
    "Provenance: tier 3, digitized from the embedded ~372 ppi JPEG (no vector data in the PDF) by fig3b_extract.py.",
    f"  Calibrated on the ticks 0-14 HV (max residual {ry:.3f}) and 0-100 % (max residual {rx:.3f}).",
    f"Uncertainty: +-{2 * abs(sy):.2f} HV and +-{2 * abs(sx):.2f} % (2 px). Fully overlapping markers cannot be seen; counts",
    "  are lower limits.",
], ["sequence", "humidity_percent", "hardness_HV", "n_in_blob"], out)
for k, v in SEQ.items():
    print(k, v, sum(1 for o in out if o[0] == v))
