"""Digitize Fig. 6 of Bouwer et al. 2016 (PDF p. 8): normalized gold BS signal vs landing energy, 4 series.

Source: the embedded raster image of Fig. 6 (895 x 921 px, 300 ppi, RGB) in source/bouwer2016.pdf.
No vector plot paths in the PDF (only the figure frame), so tier 3 (digitized).
    python3 -I -B figures/fig6_extract.py   -> figures/fig6.csv (+ work/fig6_overlay.png)
Axis calibration: the blue frame and grid lines at the labelled ticks (x 0..5 keV, y 0..1).
Markers: open black circles (FEI CBS; centre = circle fit to the ring), open blue squares (Gatan BS;
centre of the square outline's bounding box), filled green diamonds and filled black down-triangles
(centre of the ink, i.e. the centroid of the filled shape; for the triangle that is 1/3 of its
height below the flat top edge, which is not the data point the plotting program placed: see below).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, write_csv, overlay  # noqa: E402

PDF = HERE.parent / "source" / "bouwer2016.pdf"
a = embedded_image(str(PDF), 8, bbox_near=(314.7, 95.0, 529.4, 315.9))
ai = a.astype(int)
R, G, B = ai[:, :, 0], ai[:, :, 1], ai[:, :, 2]
bluish = (B - R) > 40


def lines(mask, axis, minlen):
    s = mask.sum(axis=axis)
    idx = np.where(s > minlen)[0]
    groups = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    return [float(np.mean(g)) for g in groups if len(g)]


rows = lines(bluish, 1, 300)  # top frame, grid 0.8 .. 0.2 (0.2 is half hidden by the legend), bottom frame
cols = lines(bluish, 0, 500)
assert len(rows) == 6 and len(cols) == 6, (rows, cols)
fy, yres, ys = fit_axis(rows, [1, 0.8, 0.6, 0.4, 0.2, 0])
fx, xres, xs = fit_axis(cols, [0, 1, 2, 3, 4, 5])
top, bot, left, right = rows[0], rows[-1], cols[0], cols[-1]

area = np.zeros(R.shape, bool)
area[int(top) - 12:int(bot) + 4, int(left) - 4:int(right) + 12] = True
area[645:810, 405:890] = False       # legend box (with its drop shadow)

green = (G - R > 40) & (G - B > 40) & area
black = (ai.max(2) < 110) & area & ~green
pure_blue = (B - R > 150) & (B - G > 150) & area
# remove the pure-blue frame lines and their tick marks from the square mask: every row/column of the
# frame (+-2 px) and the tick marks (up to 10 px inside the frame) is cleared; squares on the frame
# (the one at 5 keV, centred on the corner) lose the pixels on the frame lines; the bounding box still spans the whole outline
for r in (rows[0], rows[-1]):
    pure_blue[int(r) - 2:int(r) + 3, :] = False
for c in (cols[0], cols[-1]):
    pure_blue[:, int(c) - 2:int(c) + 3] = False
pure_blue[:, int(cols[0]):int(cols[0]) + 12] = False

out, pts = [], []


def comps(mask, min_area):
    n, lab, stats, cent = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    return [(lab == i, stats[i]) for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= min_area]


def circle_fit(x, y):
    A = np.c_[2 * x, 2 * y, np.ones_like(x)]
    (cx, cy, c), *_ = np.linalg.lstsq(A, x ** 2 + y ** 2, rcond=None)
    return cx, cy, np.sqrt(c + cx ** 2 + cy ** 2)


for m, st in comps(black, 15):
    yy, xx = np.where(m)
    x0, y0, w, h = st[0], st[1], st[2], st[3]
    filled = m[y0 + h // 2, x0 + w // 2]
    if filled:   # filled down-triangle
        cx, cy = (xx.min() + xx.max()) / 2, (yy.min() + yy.max()) / 2
        out.append(["FEI CBS 4keV HT with Deceleration", float(fx(cx)), float(fy(cy)), float(fy(yy.mean())), "",
                    int(w), int(h)])
    else:
        cx, cy, rad = circle_fit(xx.astype(float), yy.astype(float))
        if not 4 < rad < 9:
            continue
        flag = "cut by the frame lines" if cx > right - 8 else ""
        out.append(["FEI CBS", float(fx(cx)), float(fy(cy)), np.nan, flag, int(w), int(h)])
    pts.append((cx, cy))
for m, st in comps(green, 15):
    yy, xx = np.where(m)
    cx, cy = xx.mean(), yy.mean()
    out.append(["FEI CBS 3keV HT with Deceleration", float(fx(cx)), float(fy(cy)), np.nan, "", int(st[2]), int(st[3])])
    pts.append((cx, cy))
# squares: the light grid lines cut some outlines into pieces, so merge pure-blue pieces within 8 px
bl = cv2.dilate(pure_blue.astype(np.uint8), np.ones((9, 9), np.uint8))
n, lab, stats, cent = cv2.connectedComponentsWithStats(bl, connectivity=8)
for i in range(1, n):
    yy, xx = np.where((lab == i) & pure_blue)
    if len(xx) < 15:
        continue
    w, h = xx.max() - xx.min() + 1, yy.max() - yy.min() + 1
    if w < 11 or h < 11:      # frame tick marks (2 x 10 px)
        continue
    cx, cy = (xx.min() + xx.max()) / 2, (yy.min() + yy.max()) / 2
    flag = "cut by the frame lines" if xx.max() > right - 8 else ""
    out.append(["Gatan BS", float(fx(cx)), float(fy(cy)), np.nan, flag, int(w), int(h)])
    pts.append((cx, cy))
order = {"FEI CBS": 0, "Gatan BS": 1, "FEI CBS 3keV HT with Deceleration": 2, "FEI CBS 4keV HT with Deceleration": 3}
out.sort(key=lambda r: (order[r[0]], r[1]))
overlay(a, pts, str(HERE.parent / "work" / "fig6_overlay.png"))
write_csv(str(HERE / "fig6.csv"), [
    "Bouwer et al. 2016 Adv Struct Chem Imag 2:11, Fig. 6: 'Gatan BS Detector and FEI CBS Detector / Normalized Gold BS",
    "  Signal Vs. / Electron Probe Beam Landing Energy'.",
    "Columns: series = legend entry ('FEI CBS' open black circles, 'Gatan BS' open blue squares, 'FEI CBS 3keV HT with",
    "  Deceleration' filled green diamonds, 'FEI CBS 4keV HT with Deceleration' filled black down-triangles);",
    "  landing_energy_keV = Landing Energy (keV), x axis; signal = Normalized Gold BS Signal (Arbitrary Units), y axis;",
    "  signal_ink_centroid = for the triangles only, y of the centroid of the filled triangle (signal uses the centre of",
    "  its bounding box; which point of the symbol marks the value is not known, the two differ by about 0.005).",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig6_extract.py.",
    f"  Axes fitted on the frame and grid lines at the labelled ticks, max residual x {xres:.4f} keV, y {yres:.4f}.",
    "  Circle centres: least-squares circle fit to the ring; squares: centre of the outline's bounding box; diamonds:",
    "  centroid of the filled shape. At 5 keV the circle and the square overlap at (5, 1) on the right frame line.",
    "  flag: markers cut by the frame lines; marker_w_px/marker_h_px: size of the marker's ink (a check only).",
    f"Uncertainty: about +-{abs(xs):.4f} keV in x and +-{abs(ys):.4f} in y (1 source pixel); about 3 px for flagged markers.",
], ["series", "landing_energy_keV", "signal", "signal_ink_centroid", "flag", "marker_w_px", "marker_h_px"], out,
    fmt=["{}", "{:.3f}", "{:.4f}", "{:.4f}", "{}", "{}", "{}"])
for r in out:
    print(r)
print("residuals", xres, yres)
