"""Digitize Figure 6E of Tegethoff & Briggman 2024 (PDF p.8): section compression vs mean resultant force.
    python3 -I fig6e_extract.py -> fig6e.csv (+ ../work/fig6e_overlay.png)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig6_common import *  # noqa: E402,F403

a = img(8)
fy, ry, sy = fit_axis([1340.5, 1265.5, 1190.5, 1116.0, 1040.5, 966.0, 891.0, 816.0], [0, 5, 10, 15, 20, 25, 30, 35])
fx, rx, sx = fit_axis([103.0, 177.5, 252.0, 326.5, 401.0, 476.0, 550.5, 625.0, 699.5, 774.0],
                      [45, 50, 55, 60, 65, 70, 75, 80, 85, 90])
masks = resin_masks(a, fill=("LX 112",))
masks.pop("LX 112#orig")
rows, pts = dot_rows(masks, (106, 805, 790, 1337), fx, fy, SINGLE, min_area=20)
out = []
for r in sorted(rows, key=lambda r: (RESINS.index(r[0]), r[1], r[2])):
    kind = "filled"
    if r[0] == "LX 112":
        # all LX 112 markers near 55 mN/mm are open circles and all near 62 are filled (checked on the 2x zoom);
        # the centre test is unreliable for markers in merged blobs, so the column decides
        kind = "open" if r[1] < 58 else "filled"
    out.append((r[0], "35 nm" if kind == "open" else "50 nm", kind, r[1], r[2], r[5]))
save(mark(a, pts, r=2), "fig6e_overlay.png")
write_csv(os.path.join(HERE, "fig6e.csv"), header(
    "Figure 6E: percentage of section compression plotted versus mean resultant force (x axis 'F_R' with an overbar, mN/mm).",
    ["  Columns: series = resin (colour key of panel C); thickness: open circles = 35 nm LX 112 sections, closed",
     "  circles = 50 nm sections (caption); marker; mean_FR_mN_per_mm = x; compression_percent = y; n_in_blob.",
     "  Open circles were filled (hole filling) before detection; all LX 112 markers of the column at ~55 mN/mm are",
     "  open circles and all of the column at ~62 mN/mm filled (checked by eye), so the column sets the marker type.",
     "  The VH Epon markers (asterisk) are from ~100 nm sections (caption). At ~60 mN/mm the M Epon, MH Epon and",
     "  H Epon columns overlap, so colours mix at their edges and some markers there may be misassigned or missed."],
    ry, rx, sy, sx, "%", "mN/mm"),
    ["series", "thickness", "marker", "mean_FR_mN_per_mm", "compression_percent", "n_in_blob"], out)
for n in RESINS:
    rs = [o for o in out if o[0] == n]
    print(n, len(rs), sorted({o[1] for o in rs}), round(np.median([o[3] for o in rs]), 2) if rs else None)
