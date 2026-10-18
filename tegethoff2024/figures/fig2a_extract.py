"""Digitize Figure 2A of Tegethoff & Briggman 2024 (PDF p.5): hardness of independent blocks per resin.

Source: the embedded JPEG of Figure 2 (994 x 1914 px, ~349 ppi), panel A in its top part.
    python3 -I fig2a_extract.py   -> fig2a.csv (+ ../work/fig2a_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(5)
# axis frame and ticks (found with work/explore.py: axis_line()/ticks() on a grey<205 mask)
YT = [74.0, 121.0, 167.5, 214.5, 261.5, 308.5, 355.5, 402.5, 449.5]      # tick rows
YV = [18, 17, 16, 15, 14, 13, 12, 11, 10]                                  # labels 10..18 (odd ones unlabelled minor ticks)
fy, ry, sy = fit_axis(YT, YV)
XT = [134.0, 165.0, 195.5, 226.0, 257.0, 287.5, 318.0, 349.0, 379.5, 410.0, 441.0, 471.5, 502.0, 533.0,
      563.5, 594.0, 625.0, 655.5, 686.0, 717.0, 747.5, 778.0, 809.0, 839.5, 870.0, 901.0, 931.5, 962.0]
fx, rx, sx = fit_axis(XT, list(range(1, len(XT) + 1)))   # x in tick-index units (categorical axis)
BOX = (106, 20, 990, 494)

g, s = gray(a), sat(a)
names = ["medium hard", "hard", "LX 112", "Durcupan", "Spurr's"]
pal = [MATLAB[k] for k in ["blue", "orange", "yellow", "purple", "green"]]
lab = classify(a, pal, max_dist=45, min_sat=40)
masks = {n: lab == i for i, n in enumerate(names)}
grey = (s < 25) & (g > 90) & (g < 185)
grey[:, :450] = False
grey[:, 575:] = False
grey[480:, :] = False  # x-axis tick marks
masks = {"medium hard": masks["medium hard"], "hard": masks["hard"], "very hard": grey,
         "LX 112": masks["LX 112"], "Durcupan": masks["Durcupan"], "Spurr's": masks["Spurr's"]}
rows, pts = dot_rows(masks, BOX, fx, fy, single_area=24, min_area=10)

out = []
for name in masks:
    rs = [r for r in rows if r[0] == name]
    ticks_used = sorted({int(round(r[1])) for r in rs})
    for r in sorted(rs, key=lambda r: (r[1], r[2])):
        block = ticks_used.index(int(round(r[1]))) + 1
        out.append((name, block, r[1], r[2], r[5]))
save(mark(a, pts), "fig2a_overlay.png")
write_csv(os.path.join(HERE, "fig2a.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 2A: hardness values from independent blocks per resin.",
    "Columns: series = resin as labelled under the axis (EMbed 812 'medium hard', 'hard', 'very hard', LX 112, Durcupan,",
    "  Spurr's); block = 1..4, the block (tick position) within the resin, left to right; x_tick = horizontal position in",
    "  units of the x tick marks (tick 1 = first tick right of the y axis; the x axis has ticks but no numbers: it is",
    "  categorical, and small offsets from the integer are the plot's side-by-side placement of equal values);",
    "  hardness_HV = Vickers hardness (y axis); n_in_blob = number of markers in the merged blob this point was split from",
    "  (1 = an isolated marker; >1 = overlapping markers, split with k-means by blob area, positions approximate).",
    "Provenance: tier 3, digitized from the embedded ~349 ppi JPEG (the PDF has no vector data for this plot) by",
    f"  fig2a_extract.py. y calibrated on the 9 tick marks 10-18 HV, max residual {ry:.3f} HV.",
    f"Uncertainty: about +-{2 * abs(sy):.2f} HV for isolated markers (2 px; marker diameter ~5.5 px = {5.5 * abs(sy):.2f} HV);",
    "  markers that overlap completely cannot be seen, so the counts are lower limits (caption: n = 8-20 points per block face).",
    "Series colours: MATLAB default colours (blue, orange, grey, yellow, purple, green).",
], ["series", "block", "x_tick", "hardness_HV", "n_in_blob"], out)
for name in masks:
    rs = [o for o in out if o[0] == name]
    print(name, len(rs), "points; per block", [sum(1 for o in rs if o[1] == b) for b in range(1, 5)])
print("y residual", ry)
