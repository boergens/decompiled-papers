"""Digitize Figure 2B of Tegethoff & Briggman 2024 (PDF p.5): EMbed 812 hardness vs NMA:DDSA ratio.

Source: the embedded JPEG of Figure 2 (994 x 1914 px, ~349 ppi), panel B in its middle part.
    python3 -I fig2b_extract.py   -> fig2b.csv (+ ../work/fig2b_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(5)
YT = [658.5, 701.0, 744.0, 787.0, 829.0, 872.0, 914.0, 957.0, 1000.0, 1042.0, 1085.0, 1128.0]
YV = [15, 14.5, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5]   # labels 10..15 at the integer ticks
fy, ry, sy = fit_axis(YT, YV)
XT = [261.0, 414.0, 567.0, 720.0, 873.0]
XL = [1.34, 1.57, 1.83, 2.11, 2.44]          # categorical: equally spaced ticks with these labels
fx, rx, sx = fit_axis(XT, [1, 2, 3, 4, 5])
BOX = (111, 640, 990, 1125)
m = gray(a) < 100
rows, pts = dot_rows({"EMbed 812": m}, BOX, fx, fy, single_area=24, min_area=10)
out = []
for r in sorted(rows, key=lambda r: (round(r[1]), r[2])):
    k = int(round(r[1]))
    out.append((XL[k - 1], round(r[1] - k, 3), r[2], r[5]))
save(mark(a, pts), "fig2b_overlay.png")
write_csv(os.path.join(HERE, "fig2b.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 2B: hardness of EMbed 812 for different ratios of the",
    "  hardeners NMA and DDSA (black dots).",
    "Columns: nma_ddsa_ratio = the x tick label the dot belongs to (the x axis is categorical: the five labels sit at",
    "  equally spaced ticks); x_offset = horizontal offset from that tick in units of the tick spacing (the plot places equal",
    "  values side by side); hardness_HV = Vickers hardness; n_in_blob = markers in the merged blob this point was split",
    "  from (1 = isolated marker; >1 = overlapping markers split with k-means, positions approximate).",
    "Provenance: tier 3, digitized from the embedded ~349 ppi JPEG (no vector data in the PDF) by fig2b_extract.py.",
    f"  y calibrated on the 12 tick marks 9.5-15 HV (labels 10-15 at the integer ticks), max residual {ry:.3f} HV.",
    f"Uncertainty: about +-{2 * abs(sy):.2f} HV (2 px). Fully overlapping markers cannot be seen; counts are lower limits.",
], ["nma_ddsa_ratio", "x_offset", "hardness_HV", "n_in_blob"], out)
for x in XL:
    print(x, sum(1 for o in out if o[0] == x))
print("y residual", ry)
