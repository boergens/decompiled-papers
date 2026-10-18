"""Digitize Figure 1—figure supplement 1 of Ströh et al. 2022 (eLife JPEG fig1-figsupp1.jpg, 1176 x 2329 px).

Line plots a, g, m: standardized intensity profiles, SEM (blue) and μCT (orange), traced per pixel column (top and
bottom of the thick, noisy line kept). Scatter plots d, j, p: small black dots that overlap heavily; every dark pixel
of the cloud is reported in data units (single dots cannot be separated).
Tick marks are found in the image; the tick labels were read by eye (listed below per panel). Legends are blanked.
    python3 -I sfig1s1_extract.py -> sfig1s1a.csv, sfig1s1d.csv, sfig1s1g.csv, sfig1s1j.csv, sfig1s1m.csv, sfig1s1p.csv
"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import supp_image, dark_mask, fit_axis, write_csv, save_overlay, save_crop, column_trace, \
    colour_mask  # noqa: E402

a = supp_image("fig1-figsupp1.jpg")
d = dark_mask(a, thr=120, sat=50)
# panel: plot area (r0, r1, c0, c1), y ticks (rows, labels), x ticks (cols, labels), legend box to blank, axis names
P = {
    "a": ((16, 304, 73, 438), ([42.5, 101.5, 160.5, 219.0], [1, 0, -1, -2]), ([70.0, 175.5, 281.5, 387.5], [0, 400, 800, 1200]),
          (225, 295, 270, 390), "distance_um", "Distance (μm)", "standardized_au", "Standardized (a.u.)"),
    "g": ((797, 1082, 72, 434), ([794.0, 842.5, 891.0, 939.5, 988.5], [3, 2, 1, 0, -1]), ([69.0, 191.5, 314.0, 436.0], [0, 400, 800, 1200]),
          (980, 1050, 292, 410), "distance_um", "Distance (μm)", "standardized_au", "Standardized (a.u.)"),
    "m": ((1578, 1869, 75, 435), ([1706.5, 1748.0, 1789.5, 1830.5, 1872.0], [-1, -2, -3, -4, -5]),
          ([72.5, 164.0, 255.0, 346.0, 437.0], [0, 400, 800, 1200, 1600]),
          (1762, 1842, 292, 410), "depth_um", "Depth (μm)", "standardized_au", "Standardized (a.u.)"),
    "d": ((388, 676, 138, 440), ([422.0, 496.0, 569.0, 642.0], [220, 210, 200, 190]),
          ([183.0, 230.5, 278.5, 326.0, 373.5, 421.5], [50, 60, 70, 80, 90, 100]), None,
          "mean_uCT_au", "mean μCT intensity (a.u.)", "mean_SEM_au", "mean SEM intensity (a.u.)"),
    "j": ((1176, 1464, 138, 440), ([1174.0, 1291.0, 1408.5], [170, 160, 150]),
          ([135.0, 211.5, 287.5, 363.5, 439.5], [100, 120, 140, 160, 180]), None,
          "mean_uCT_au", "mean μCT intensity (a.u.)", "mean_SEM_au", "mean SEM intensity (a.u.)"),
    "p": ((1958, 2245, 138, 440), ([1955.0, 2039.0, 2123.0, 2207.0], [120, 100, 80, 60]),
          ([134.5, 195.0, 256.0, 317.0, 378.0, 439.0], [50, 60, 70, 80, 90, 100]), None,
          "mean_Xray_au", "mean X-ray intensity (a.u.)", "mean_SEM_au", "mean SEM intensity (a.u.)"),
}
SEM, UCT = (0, 114, 189), (217, 83, 25)
for p, (W, (yr, yl), (xc, xl), leg, xn, xlab, yn, ylab) in P.items():
    fy, yres, ys = fit_axis(yr, yl)
    fx, xres, xs = fit_axis(xc, xl)
    b = a.copy()
    if leg:
        r0, r1, c0, c1 = leg
        b[r0:r1, c0:c1] = 255
    r0, r1, c0, c1 = W
    rows, ov = [], []
    if p in "agm":
        for name, rgb in (("SEM", SEM), ("μCT", UCT)):
            m = colour_mask(b, rgb, 70)
            tr = column_trace(m, c0, c1, r0, r1, maxjump=40)
            rows += [(name, float(fx(c)), float(fy(mid)), float(fy(bot)), float(fy(top))) for c, mid, top, bot in tr if mid == mid]
            ov.append(((255, 0, 255) if name == "SEM" else (0, 255, 0), [(c, t) for c, mid, t, bb in tr] + [(c, bb) for c, mid, t, bb in tr]))
        cols = ["series", xn, yn, "line_bottom", "line_top"]
        what = ("SEM (blue) and μCT (orange) as in the legend; value = centre of the line in that pixel column;"
                " line_bottom / line_top = lower / upper edge of the line there (the SEM trace is noisy, so this range"
                " is the spread of the plotted data in that column)")
    else:
        m = dark_mask(b, thr=140, sat=60)[r0:r1, c0:c1]
        yy, xx = np.nonzero(m)
        for y, x in zip(yy, xx):
            rows.append(("dark_pixel", float(fx(x + c0)), float(fy(y + r0))))
        ov.append(((255, 0, 255), [(x + c0, y + r0) for y, x in zip(yy[::7], xx[::7])]))
        cols = ["series", xn, yn]
        what = ("every dark pixel of the dot cloud (the dots are ~3-5 px across and overlap heavily, so single samples"
                " cannot be separated; the pixel cloud gives the shape and extent of the scatter), in data units")
    write_csv(os.path.join(HERE, f"sfig1s1{p}.csv"), [
        f"Ströh et al. 2022 eLife, Figure 1—figure supplement 1{p}: x = {xlab}, y = {ylab}.",
        f"Rows: {what}.",
        "Provenance: tier 3, digitized from the eLife figure-supplement JPEG by sfig1s1_extract.py; tick marks found in",
        f"  the image, labels read by eye: x {xl} (max residual {xres:.3g}), y {yl} (max residual {yres:.3g}).",
        f"Uncertainty: about ±{2 * abs(xs):.3g} in x and ±{2 * abs(ys):.3g} in y (2 px) plus JPEG blur.",
    ], cols, rows)
    save_overlay(b, ov, f"sfig1s1{p}_overlay.png", crop=(W[0] - 15, W[1] + 40, W[2] - 50, W[3] + 10))
    save_crop(a, (W[0] - 15, W[1] + 40, W[2] - 50, W[3] + 10), os.path.join(HERE, f"../work/sfig1s1{p}_src.png"))
    print(p, len(rows), xres, yres)
