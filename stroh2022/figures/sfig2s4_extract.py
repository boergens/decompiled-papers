"""Digitize Figure 2—figure supplement 4 of Ströh et al. 2022 (eLife JPEG fig2-figsupp4.jpg, 2081 x 652 px).

Seven fitted parameters, each shown as grey dots (individual samples, n=13 per the legend) and a black bar with an
upward error bar (mean and, by the main text's convention, + s.d.; the legend does not say what the error bar is).
Values are in the units printed under each bar (e.g. D^e in 10^4 μm^2 min^-1).
y axis: tick marks at rows 12.3 (label 10), 220.2 (5) and 438.9 (0) - their spacing is not uniform (208 vs 219 px),
so a straight-line fit through all three has a residual of ~0.13 units; values are from that fit.
Dots: Hough circles on the light-grey mask; overlapping dots merge, so fewer than 13 dots per parameter are found.
    python3 -I sfig2s4_extract.py -> sfig2s4.csv (+ ../work/sfig2s4_overlay.png)
"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import supp_image, dark_mask, fit_axis, write_csv, save_overlay, save_crop, runs  # noqa: E402

a = supp_image("fig2-figsupp4.jpg")
ai = a.astype(int)
d = dark_mask(a, thr=110, sat=50)
fy, yres, ys = fit_axis([12.3, 220.2, 438.9], [10, 5, 0])
X_AXIS = 439
PARAMS = [("D^e", "10^4 μm^2 min^-1"), ("k^unmask", "10^-5 mm^3 nmol^-1 min^-1"), ("k^on", "10^-4 mm^3 nmol^-1 min^-1"),
          ("C^0", "10^2 nmol mm^-3"), ("S^0", "10^2 nmol mm^-3"), ("M^0", "10^2 nmol mm^-3"), ("H", "10^2 μm")]
cols = [c for c in range(60, a.shape[1]) if d[X_AXIS - 25:X_AXIS - 3, c].all()]
bars = [(g[0], g[-1]) for g in runs(cols) if g[-1] - g[0] > 20]
assert len(bars) == 7, bars
rows, pts = [], []
grey = ((ai.max(2) - ai.min(2)) < 15) & (ai.mean(2) > 175) & (ai.mean(2) < 235)
for (c0, c1), (name, unit) in zip(bars, PARAMS):
    full = [r for r in range(0, X_AXIS) if d[r, c0 + 3:c1 - 2].mean() > 0.9]
    top = min(full)
    mid = (c0 + c1) // 2
    centre = [r for r in range(0, X_AXIS) if d[r, mid - 2:mid + 3].any()]
    cap = min(centre)
    rows.append((name, unit, "bar (mean)", float(fy(top)), ""))
    rows.append((name, unit, "error bar top", float(fy(cap)), ""))
    pts += [(c, top) for c in range(c0, c1)] + [(mid, cap)]
    # dots: to the left of the bar, within ~130 px
    w0, w1 = c0 - 140, c0 - 2
    sub = (grey[0:X_AXIS, w0:w1] * 255).astype(np.uint8)
    cs = cv2.HoughCircles(cv2.GaussianBlur(sub, (5, 5), 1), cv2.HOUGH_GRADIENT, dp=1, minDist=7, param1=60, param2=9,
                          minRadius=7, maxRadius=11)
    found = []
    if cs is not None:
        for x, y, r in cs[0]:
            if sub[int(y), int(x)] and all(np.hypot(x - p, y - q) > 7 for p, q in found):
                found.append((x, y))
    for x, y in sorted(found, key=lambda q: q[1]):
        rows.append((name, unit, "dot", float(fy(y)), f"{x + w0:.0f}"))
        pts.append((x + w0, y))
write_csv(os.path.join(HERE, "sfig2s4.csv"), [
    "Ströh et al. 2022 eLife, Figure 2—figure supplement 4: fitted parameters of n=13 samples (grey dots) and their",
    "  mean (black bar) with error bar (upward only).",
    "Columns: parameter (as printed under the bar); unit (as printed); kind (bar (mean) | error bar top | dot);",
    "  value in the printed unit; x_px = horizontal position of a dot in the image (dots are jittered sideways).",
    "Provenance: tier 3, digitized from the eLife figure-supplement JPEG by sfig2s4_extract.py; y calibrated on the 3",
    f"  tick marks (0, 5, 10; labels read by eye), max residual {yres:.3f} (the ticks are not evenly spaced).",
    "  Bar top = highest row where the whole bar width is black; error bar top = highest dark pixel in the bar centre.",
    "  Dots: Hough circles on the grey mask; overlapping dots merge (C^0 dots overlap almost completely), so the dot",
    "  count per parameter is below 13.",
    f"Uncertainty: ±{abs(ys) * 2 + yres:.2f} units (2 px plus the tick-spacing residual).",
], ["parameter", "unit", "kind", "value", "x_px"], rows)
save_overlay(a, [((255, 0, 255), pts)], "sfig2s4_overlay.png")
save_crop(a, (0, 460, 0, a.shape[1]), os.path.join(HERE, "../work/sfig2s4_src.png"))
for r in rows:
    if r[2] != "dot":
        print(r)
print(sum(1 for r in rows if r[2] == "dot"), "dots", yres)
