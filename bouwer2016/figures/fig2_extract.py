"""Digitize Fig. 2 of Bouwer et al. 2016 (PDF p. 5): measured sample surface potential vs applied potential.

Source: the embedded raster image of Fig. 2 (896 x 901 px, 300 ppi, RGB) in source/bouwer2016.pdf.
The PDF holds no vector paths for the plot (only the figure frame), so this is tier 3 (digitized).
    python3 -I -B figures/fig2_extract.py   -> figures/fig2.csv (+ work/fig2_overlay.png)
Axis calibration: the blue frame lines and the blue grid lines, which sit at the labelled ticks
(x: -1500, -1000, -500, 0 V; y: 0, -200, ..., -1400 V). Markers: open black circles; each circle's
centre is a least-squares circle fit to its ring pixels (robust for the two circles cut by the frame).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, write_csv, overlay  # noqa: E402

PDF = HERE.parent / "source" / "bouwer2016.pdf"
a = embedded_image(str(PDF), 5, bbox_near=(66.5, 95.0, 281.5, 311.2))
ai = a.astype(int)
blue = (ai[:, :, 2] - ai[:, :, 0]) > 40


def lines(mask, axis, minlen):
    s = mask.sum(axis=axis)
    idx = np.where(s > minlen)[0]
    groups = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    return [float(np.mean(g)) for g in groups if len(g)]


rows = lines(blue, 1, 600)   # frame top, 6 grid lines, frame bottom
cols = lines(blue, 0, 550)   # frame left, 2 grid lines, frame right
assert len(rows) == 8 and len(cols) == 4, (rows, cols)
fy, yres, ys = fit_axis(rows, [0, -200, -400, -600, -800, -1000, -1200, -1400])
fx, xres, xs = fit_axis(cols, [-1500, -1000, -500, 0])
top, bot, left, right = rows[0], rows[-1], cols[0], cols[-1]

dark = (ai.max(2) < 110)
# keep only the plot area (a few px outside the frame for clipped corner markers); drop the legend box
m = np.zeros_like(dark)
m[int(top) - 12:int(bot) + 7, int(left) - 12:int(right) + 12] = True  # below bot+7: tick-label glyphs
m[600:670, 360:870] = False
dark &= m
dark[:, :int(left) - 12] = False
n, lab, stats, cent = cv2.connectedComponentsWithStats(dark.astype(np.uint8), connectivity=8)


def circle_fit(x, y):
    A = np.c_[2 * x, 2 * y, np.ones_like(x)]
    sol, *_ = np.linalg.lstsq(A, x ** 2 + y ** 2, rcond=None)
    cx, cy, c = sol
    return cx, cy, np.sqrt(c + cx ** 2 + cy ** 2)


out, pts = [], []
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] < 15:
        continue
    yy, xx = np.where(lab == i)
    cx, cy, rad = circle_fit(xx.astype(float), yy.astype(float))
    if not 4.5 < rad < 7:
        continue
    pts.append((cx, cy))
    out.append([float(fx(cx)), float(fy(cy)), rad])
out.sort()
overlay(a, pts, str(HERE.parent / "work" / "fig2_overlay.png"))
write_csv(str(HERE / "fig2.csv"), [
    "Bouwer et al. 2016 Adv Struct Chem Imag 2:11, Fig. 2: 'Applied Voltage Vs. Sample Surface Voltage'.",
    "Series: 'Measured Sample Surface Potential' (open circles, the only series).",
    "Columns: applied_potential_V = Applied Potential (Volts), x axis; measured_sample_potential_V = Measured Sample",
    "  Potential (Volts), y axis; circle_radius_px = fitted marker radius in source pixels (a check only).",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig2_extract.py.",
    f"  Axes fitted on the frame and grid lines (labelled ticks), max residual x {xres:.2f} V, y {yres:.2f} V.",
    "  Marker centre = least-squares circle fit to the ring pixels of each open circle. The first (-1500 V) and last (0 V)",
    "  markers are cut by the frame corners; their centres come from the visible arcs.",
    f"Uncertainty: about +-{abs(xs):.1f} V in x and +-{abs(ys):.1f} V in y (1 source pixel); the applied voltages look like",
    "  steps of 100 V (plus one point near -50 V), but the values below are as read, not rounded.",
], ["applied_potential_V", "measured_sample_potential_V", "circle_radius_px"], out, fmt=["{:.1f}", "{:.1f}", "{:.2f}"])
print(len(out), "points; residuals", xres, yres)
for r in out:
    print(["%.1f" % v for v in r])
