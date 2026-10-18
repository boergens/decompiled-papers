"""Digitize Figure 6C of Tegethoff & Briggman 2024 (PDF p.8): section compression vs block hardness, per resin.
    python3 -I fig6c_extract.py -> fig6c.csv (+ ../work/fig6c_overlay.png)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig6_common import *  # noqa: E402,F403

a = img(8)
fy, ry, sy = fit_axis([628.0, 552.5, 476.5, 401.0, 325.5, 250.0, 174.5, 99.0], [0, 5, 10, 15, 20, 25, 30, 35])
fx, rx, sx = fit_axis([1041.5, 1097.5, 1153.0, 1209.0, 1265.0, 1321.0, 1377.0, 1433.0, 1489.0, 1544.5, 1600.5, 1656.5,
                       1712.5], [12 + 0.5 * i for i in range(13)])
masks = resin_masks(a)
rows, pts = dot_rows(masks, (1045, 95, 1730, 625), fx, fy, SINGLE, min_area=20)
out = [(r[0], r[1], r[2], r[5]) for r in sorted(rows, key=lambda r: (RESINS.index(r[0]), r[2]))]
save(mark(a, pts, r=2), "fig6c_overlay.png")
write_csv(os.path.join(HERE, "fig6c.csv"), header(
    "Figure 6C: percentage of section compression relative to the length of block faces, plotted versus hardness",
    ["  Columns: series = resin (colour key next to the panel); hardness_HV = x of the marker; compression_percent = y;",
     "  n_in_blob. All 50 nm sections; the VH Epon markers (asterisk) are from ~100 nm sections (caption).",
     "  Markers of one resin share one hardness value; their sideways spread is the plot's placement, not data."],
    ry, rx, sy, sx, "%", "HV") + [
    "  (the figure title line: for different resins, colour-coded, 50 nm sections)"],
    ["series", "hardness_HV", "compression_percent", "n_in_blob"], out)
for n in RESINS:
    rs = [o for o in out if o[0] == n]
    print(n, len(rs), round(np.median([o[1] for o in rs]), 2) if rs else None)
