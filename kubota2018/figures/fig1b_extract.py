"""Digitize Fig. 1b of Kubota et al. 2018 (main PDF p. 3): surface resistance of the CNT tape vs length.

Source: the embedded 300 ppi raster of panel b (421 x 296 px); tick labels are PDF text.
    python3 -I fig1b_extract.py  -> fig1b.csv (+ ../work/fig1b_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from kubota_main_common import Img, calib, blobs, opened, WORK  # noqa: E402
from digitize_common import tick_positions, tick_positions_v, write_csv, overlay  # noqa: E402

im = Img(3, (231.2, 66.3, 332.3, 137.4))
d = im.g < 128
XAX, YAX = (282, 284), (12, 14)          # axis lines (rows / columns), found with frame_lines()
xt = tick_positions(d, XAX, +1, 5, YAX[1] + 1, d.shape[1])
yt = tick_positions_v(d, YAX, -1, 5, 0, XAX[0])
labs = im.labels((205, 55, 340, 150))
xl = [l for l in labs if l[2] > XAX[1]]                      # below the x axis
yl = [l for l in labs if l[1] < YAX[0] and l[0] >= 220]       # 220-320 (above the axis break)
fx, rx, sx, xp, xv = calib(xt, xl, 1)
fy, ry, sy, yp, yv = calib(yt, yl, 2)

m = d.copy()
m[XAX[0] - 3:, :] = False
m[:, :YAX[1] + 2] = False
m = opened(m, 3)                         # keep the ~11 px filled markers, drop the 3 px line
pts = []
for cx, cy, area, box in blobs(m, 20):
    if area > 140:                        # two touching markers: split with k-means
        ys, xs = np.where(m[box[1]:box[3], box[0]:box[2]])
        Z = np.float32(np.c_[xs + box[0], ys + box[1]])
        _, lab, cen = cv2.kmeans(Z, 2, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.01), 10,
                                 cv2.KMEANS_PP_CENTERS)
        pts += [(c[0], c[1]) for c in cen]
    else:
        pts.append((cx, cy))
pts.sort()
overlay(im.a, pts, os.path.join(WORK, "fig1b_overlay.png"))
rows = [(float(fx(x)), float(fy(y))) for x, y in pts]
write_csv(os.path.join(HERE, "fig1b.csv"), [
    "Kubota et al. 2018 Nat Commun 9:437, Fig. 1b: surface resistance of the CNT tape along the tape (main PDF p. 3).",
    "Columns: length_m = position along the tape (x axis 'Length (meter)'); surface_resistance_ohm_per_sq = y axis",
    "  'Surface resistance', unit printed as 'Ω □-1' (ohms per square). One row per plotted marker (filled circle).",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector plot paths in the PDF) by",
    "  fig1b_extract.py: marker centres by morphological opening + connected components (3 pairs of touching",
    "  markers split by k-means). Axes calibrated on the tick marks in the image, paired with the PDF-text tick labels:",
    f"  x on {len(xp)} labelled ticks (0-10 m), max residual {rx:.3f} m; y on {len(yp)} labelled ticks (220-320), max residual {ry:.2f}.",
    f"Uncertainty: about +-{2 * abs(sx):.2f} m in x and +-{2 * abs(sy):.1f} ohm/sq in y (2 source pixels).",
    "The y axis is broken: a '0' label sits at the x-axis line below a break mark; all data lie above the break,",
    "  in the linear 220-320 part, which is what the calibration uses.",
], ["length_m", "surface_resistance_ohm_per_sq"], rows, fmt=["{:.3f}", "{:.1f}"])
print(len(rows), "points; x ticks", xp, xv, "res", rx, "; y", yp, yv, "res", ry)
