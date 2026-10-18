"""Digitize Figure 1c of Ströh et al. 2022 (PDF p.3): intensity vs OsO4 concentration.

Source: the embedded raster of Figure 1 (2079 x 2867 px, ~348 ppi). Grey dots found with a Hough circle transform on
the grey mask (dots overlap, so a dot hidden behind another may be missed); the black fit line traced per column
and fitted with a straight line.     python3 -I fig1c_extract.py -> fig1c.csv
"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import fig_image, dark_mask, vspine, hspine, ticks_left, ticks_below, fit_axis, write_csv, \
    save_overlay, column_trace, save_crop  # noqa: E402

a = fig_image(1)
d = dark_mask(a)
W = (1400, 1900, 120, 520)
vc, va, vb = vspine(d, *W)
hr, ha, hb = hspine(d, *W)
yt = ticks_left(d, vc, va - 5, vb + 5)
xt = ticks_below(d, hr, ha - 5, hb + 5)
assert len(yt) == 3 and len(xt) == 5, (yt, xt)
fy, yres, ys = fit_axis(sorted(yt, reverse=True), [0, 0.5, 1])     # labels 0, 0.5, 1 (read by eye)
fx, xres, xs = fit_axis(xt, [0, 1, 2, 3, 4])                      # labels 0 ... 4

ai = a.astype(int)
grey = (abs(ai[:, :, 0] - ai[:, :, 1]) < 12) & (ai.mean(2) > 160) & (ai.mean(2) < 215)
sub = (grey[W[0]:W[1], W[2]:W[3]] * 255).astype(np.uint8)
cs = cv2.HoughCircles(cv2.GaussianBlur(sub, (5, 5), 1), cv2.HOUGH_GRADIENT, dp=1, minDist=6, param1=60, param2=10,
                      minRadius=9, maxRadius=14)
dots = []
for x, y, r in cs[0]:
    x, y = x + W[2], y + W[0]
    if sub[int(y) - W[0], int(x) - W[2]] and all(np.hypot(x - p, y - q) > 6 for p, q, _ in dots):
        dots.append((x, y, r))
dots.sort(key=lambda q: (round(float(fx(q[0]))), q[1]))
# black line: dark pixels away from the axes and the horizontal reference line at 1
blk = dark_mask(a, thr=90)
y1 = float(np.round(np.interp(1, [0, 0.5, 1], sorted(yt, reverse=True))))
env = column_trace(blk, int(vc) + 6, int(hb) - 2, va, int(hr) - 4)
ok = np.isfinite(env[:, 1]) & (abs(env[:, 1] - y1) > 6)
m, b = np.polyfit(fx(env[ok, 0]), fy(env[ok, 1]), 1)
rows = [("dot", float(fx(x)), float(fy(y)), "Hough circle centre") for x, y, r in dots]
# the middle dot of the 3-dot stacks at 1 and 3 vol% is hidden between the two outer ones: read by eye (tier 4)
rows += [("dot", 1.0, 0.22, "read by eye (tier 4, ±0.01): middle dot of the stack, mostly hidden"),
         ("dot", 3.0, 0.66, "read by eye (tier 4, ±0.01): middle dot of the stack, mostly hidden")]
xend = float(fx(env[ok, 0].max()))
rows += [("fit_line", 0.0, float(b), f"slope {m:.5f} per vol%, intercept {b:.5f}"),
         ("fit_line", xend, float(m * xend + b), "end of the drawn line")]
rows += [("reference_line", 0.0, 1.0, "thin horizontal line at intensity 1"), ("reference_line", float(fx(hb)), 1.0, "")]
write_csv(os.path.join(HERE, "fig1c.csv"), [
    "Ströh et al. 2022 eLife, Figure 1c: measured pixel intensity of X-ray projection images vs OsO4 concentration.",
    "Columns: series (dot = one measurement, grey; fit_line = the black line, ends given; reference_line = thin line at 1);",
    "  conc_vol_percent = OsO4 conc. (vol %); intensity_au = Intensity (a.u.).",
    "Provenance: tier 3, digitized from the embedded ~348 ppi raster image (no vector data) by fig1c_extract.py:",
    f"  x fitted on 5 ticks (0-4), max residual {xres:.3f}; y on 3 ticks (0, 0.5, 1), max residual {yres:.4f}.",
    f"  Dots: Hough circles on the grey mask ({len(dots)} found; the caption says n=3 per concentration; overlapping",
    "  dots hide each other: at 1 and 3 vol% only 2 of 3 dots, at 2 vol% 1 dot can be resolved; the two hidden middle dots are added as read by eye, tier 4).",
    "  Fit line: straight-line fit to the traced black line.",
    f"Uncertainty: about ±{2 * abs(xs):.3f} vol% and ±{2 * abs(ys):.4f} a.u. (2 px) for dot centres.",
], ["series", "conc_vol_percent", "intensity_au", "note"], rows)
save_overlay(a, [((255, 0, 255), [(x, y) for x, y, r in dots]), ((255, 0, 0), [(c, (m * fx(c) + b - fy(0)) / ys + sorted(yt)[-1]) for c in env[ok, 0]])],
             "fig1c_overlay.png", crop=W)
save_crop(a, W, os.path.join(HERE, "../work/fig1c_src.png"))
print(len(dots), "dots", [(round(float(fx(x)), 2), round(float(fy(y)), 3)) for x, y, r in dots], "line", m, b)
