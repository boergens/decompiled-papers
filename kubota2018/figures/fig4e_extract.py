"""Digitize Fig. 4e of Kubota et al. 2018 (main PDF p. 6): bar chart, Haze (%).

Source: the embedded 300 ppi raster image; tick labels and the value labels above the bars are PDF text.
    python3 -I fig4e_extract.py  -> fig4e.csv (+ ../work/fig4e_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from kubota_main_common import Img, calib, WORK  # noqa: E402
from digitize_common import tick_positions_v, write_csv, overlay  # noqa: E402

BB = (471.5, 180.6, 513.5, 262.3)
im = Img(6, BB)
k = (im.g < 110) & (np.ptp(im.a.astype(int), axis=2) < 60)
XAX, YAX = (331, 332), (8, 9)
yt = tick_positions_v(k, YAX, -1, 4, 0, XAX[0]) + [(XAX[0] + XAX[1]) / 2]     # 0 = the axis line
labs = im.labels((BB[0] - 20, BB[1] - 10, BB[2] + 5, BB[3] + 5))
fy, ry, sy, yp, yv = calib(yt, [l for l in labs if l[1] < 0], 2)
values = [l for l in labs if l[1] > 0]                # the printed values above the bars
nonwhite = im.g < 200
cols = np.where(nonwhite[XAX[0] - 3, YAX[1] + 3:])[0] + YAX[1] + 3
groups = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
rows, pts = [], []
for name, g in zip(("CNT-PET", "Kapton", "cc-Kapton"), groups):
    c = int(round(g.mean()))
    top = int(np.where(nonwhite[:XAX[0], c])[0].min())    # first row of the bar's top outline
    y_top = top + 0.5                                      # centre of the ~2 px outline
    lab = min(values, key=lambda l: abs(l[1] - c))
    rows.append((name, float(fy(y_top)), lab[3], int(g[0]), int(g[-1])))
    pts += [(x, y_top) for x in range(g[0], g[-1] + 1, 3)]
overlay(im.a, pts, os.path.join(WORK, "fig4e_overlay.png"), colour=(0, 255, 0))
write_csv(os.path.join(HERE, "fig4e.csv"), [
    "Kubota et al. 2018 Nat Commun 9:437, Fig. 4e: Haze (%) of the three tapes (main PDF p. 6).",
    "Columns: tape (category axis, labels as printed: CNT-PET red bar, Kapton blue, cc-Kapton black);",
    "  haze_pct_bar = height of the bar top, digitized; printed_value = the number printed above the bar in the",
    "  figure (PDF text), which is the authors' value; bar_px_left/right = bar edges in source-image pixels.",
    "Provenance: printed_value is printed in the figure; haze_pct_bar is tier 3, digitized from the embedded 300 ppi",
    "  raster (no vector plot paths in the PDF) by fig4e_extract.py: top of each bar's outline in its centre",
    f"  column; y calibrated on {len(yp)} tick marks ({min(yv):g}-{max(yv):g}; 0 = the axis line) paired with the PDF-text",
    f"  labels, max residual {ry:.3f}. Uncertainty of the bar height about +-{2 * abs(sy):.2f} (2 px).",
], ["tape", "haze_pct_bar", "printed_value", "bar_px_left", "bar_px_right"], rows, fmt=["{}", "{:.2f}", "{}", "{}", "{}"])
print(yp, yv, ry)
for r in rows:
    print(r)
