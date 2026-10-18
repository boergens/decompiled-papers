"""Digitize Figure 3A of Tegethoff & Briggman 2024 (PDF p.5): hardness vs days post cure, three cure times.

Source: the embedded JPEG of Figure 3 (1061 x 1305 px, ~372 ppi), panel A in its top half.
    python3 -I fig3a_extract.py   -> fig3a.csv (+ ../work/fig3a_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(51)
YT = [34.0, 107.0, 180.0, 253.0, 326.0, 399.0, 472.0]
fy, ry, sy = fit_axis(YT, [15, 14, 13, 12, 11, 10, 9])
# broken x axis ("//" at ~679 px): two linear pieces
fxl, rxl, sxl = fit_axis([179.0, 290.5, 402.0, 513.0], [0, 1, 2, 3])
fxr, rxr, sxr = fit_axis([847.0, 884.5, 921.5], [30, 31, 32])   # 31 = the unlabelled middle tick


def fx(p):
    p = np.asarray(p, float)
    return np.where(p < 679, fxl(p), fxr(p))


BOX = (107, 20, 1050, 505)
g, s = gray(a), sat(a)
pal = [MATLAB["blue"], MATLAB["orange"]]
lab = classify(a, pal, max_dist=45, min_sat=40)
grey = (s < 25) & (g > 90) & (g < 185)
legend = np.zeros(g.shape, bool)
legend[40:160, 130:360] = True          # the coloured legend text at upper left
masks = {"24 hr cure": (lab == 0) & ~legend, "48 hr cure": (lab == 1) & ~legend,
         "72 hr cure": grey & ~legend}
masks["72 hr cure"][495:, :] = False   # x-axis tick marks
rows, pts = dot_rows(masks, BOX, fx, fy, single_area=26, min_area=10)
out = []
for r in sorted(rows, key=lambda r: (r[0], r[1], r[2])):
    x = r[1]
    day = int(round(x)) if x < 10 else int(round(x))
    out.append((r[0], day, x, r[2], r[5]))
save(mark(a, pts), "fig3a_overlay.png")
write_csv(os.path.join(HERE, "fig3a.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 3A: hardness of EMbed 812 blocks cured for 24 (blue),",
    "  48 (red/orange) or 72 (grey) hours at 70 C, measured at different days post cure.",
    "Columns: series = legend entry without its ', 70C' (all three legend entries end in ', 70C'); day = nearest x tick (0-3, or 30/31/32 on the right of the axis break);",
    "  x_days = horizontal position in axis units (the three series are drawn side by side around each tick 0-3, blue left,",
    "  grey right, so x_days - day there is a plotting offset, not data; right of the break blue sits on tick 30, orange on",
    "  the unlabelled middle tick (31), grey on 32); hardness_HV = Vickers hardness; n_in_blob = markers in the merged",
    "  blob this point was split from (1 = isolated; >1 = split with k-means, positions approximate).",
    "The x axis is broken ('//'): left piece calibrated on ticks 0,1,2,3, right piece on ticks 30, 31 (unlabelled), 32.",
    "Provenance: tier 3, digitized from the embedded ~372 ppi JPEG (no vector data in the PDF) by fig3a_extract.py.",
    f"  y calibrated on the 7 ticks 9-15 HV, max residual {ry:.3f} HV.",
    f"Uncertainty: +-{2 * abs(sy):.2f} HV (2 px); fully overlapping markers cannot be seen, so counts are lower limits.",
], ["series", "day", "x_days", "hardness_HV", "n_in_blob"], out)
for k in masks:
    print(k, [sum(1 for o in out if o[0] == k and o[1] == d) for d in (0, 1, 2, 3, 30, 31, 32)])
print("residuals", ry, rxl, rxr)
