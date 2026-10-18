"""Digitize Figure 6F of Tegethoff & Briggman 2024 (PDF p.8): section compression vs cutting speed (LX 112, Spurr's).
    python3 -I fig6f_extract.py -> fig6f.csv (+ ../work/fig6f_overlay.png)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig6_common import *  # noqa: E402,F403

a = img(8)
fy, ry, sy = fit_axis([1340.5, 1265.0, 1189.5, 1114.0, 1038.0, 962.5, 887.0, 811.5], [0, 5, 10, 15, 20, 25, 30, 35])
TICKS = [1140.5, 1237.0, 1332.5, 1428.5, 1524.5, 1620.5]
LABELS = ["0.3", "0.6", "1.2", "0.3", "0.6", "1.2"]
fx, rx, sx = fit_axis(TICKS, [1, 2, 3, 4, 5, 6])          # x in tick-index units (categorical)
masks = resin_masks(a, names=["LX 112", "Spurr's"])
rows, pts = dot_rows(masks, (1048, 805, 1730, 1337), fx, fy, SINGLE, min_area=20)
out = []
for r in sorted(rows, key=lambda r: (r[1], r[2])):
    k = int(round(r[1]))
    out.append((r[0], LABELS[k - 1], round(r[1] - k, 3), r[2], r[5]))
save(mark(a, pts, r=2), "fig6f_overlay.png")
write_csv(os.path.join(HERE, "fig6f.csv"), header(
    "Figure 6F: percentage of section compression plotted versus cutting speed (colour-coded, 50 nm sections).",
    ["  Columns: series (LX 112 yellow, Spurr's green); speed_mm_s = the x tick label of the column (the axis is",
     "  categorical: 0.3, 0.6, 1.2 for LX 112, then 0.3, 0.6, 1.2 for Spurr's); x_offset = offset from the tick in tick",
     "  spacings (plot placement, not data); compression_percent = y; n_in_blob."],
    ry, rx, sy, sx, "%", "tick units"),
    ["series", "speed_mm_s", "x_offset", "compression_percent", "n_in_blob"], out)
for s in ["LX 112", "Spurr's"]:
    print(s, [sum(1 for o in out if o[0] == s and o[1] == l) for l in ("0.3", "0.6", "1.2")])
