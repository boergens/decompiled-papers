"""Supplementary Fig. 3e and 3f: digitize the marker positions (tier 3).

Source: the embedded figure image of SI page 12 (887 x 331 px JPEG, 150 ppi), read at native
resolution. Axis lines and tick marks are located in the image; the tick labels (read off the
image) are 0, -200 ... -800 nm and 0 ... 10 keV in e, 4 ... 7 ke- nm-2 and 0 ... 10 keV in f.
Markers are dark connected components; the centre is the centroid of the marker's ink (for the
open circles, of the ring). Writes sfig3e.csv, sfig3f.csv and overlays in ../work/.
"""
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfig_common import WORK, si_image  # noqa: E402
from digitize_common import fit_axis, overlay, write_csv  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
img = si_image(12)
g = img.astype(float).mean(2)
dark = g < 140


def ticks_left(col_axis, r0, r1, length=2):
    """Rows of tick marks just left of a vertical axis line (ticks are light grey-black, < 175)."""
    band = g[r0:r1, col_axis - length:col_axis] < 175
    rows = np.where(band.mean(1) >= 0.99)[0]
    groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
    return [r0 + float(np.mean(q)) for q in groups if len(q)]


def ticks_below(row_axis, c0, c1, length=3):
    band = (g[row_axis + 1:row_axis + 1 + length, c0:c1] < 175)
    cols = np.where(band.mean(0) >= 0.99)[0]
    groups = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
    return [c0 + float(np.mean(q)) for q in groups if len(q)]


# axis lines (found as the long dark row/column): y axis at column 748 in e, 747 in f; x axes at rows 137 and 301
# --- panel e
ye = ticks_left(748, 5, 136)
xe = ticks_below(137, 749, 887)
# --- panel f
yf = ticks_left(747, 170, 300)
xf = ticks_below(301, 749, 887)
print("e y ticks", np.round(ye, 2)); print("e x ticks", np.round(xe, 2))
print("f y ticks", np.round(yf, 2)); print("f x ticks", np.round(xf, 2))
# e: 11 ticks from +100 (unlabelled minor) down to -800, every 100 nm (labels on even hundreds)
assert len(ye) == 10, ye
ye_val = [100, 0, -100, -200, -300, -400, -500, -600, -700, -800]
fy_e, res_ye, _ = fit_axis(ye, ye_val)
fx_e, res_xe, _ = fit_axis(xe, [0, 2, 4, 6, 8, 10])
assert len(yf) == 4, yf
fy_f, res_yf, _ = fit_axis(yf, [7, 6, 5, 4])
fx_f, res_xf, _ = fit_axis(xf, [0, 2, 4, 6, 8, 10])

m = dark.astype(np.uint8)
m[:, :750] = 0
m[136:140, :] = 0
m[300:304, :] = 0
n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
pts = []
for i in range(1, n):
    x, y, w, h, area = st[i]
    if not (3 <= w <= 8 and 3 <= h <= 8):
        continue
    if 98 <= y <= 128 and x < 820:      # legend symbols and text
        continue
    fill = area / (w * h)
    pts.append((cen[i][0], cen[i][1], fill))

rows_e, rows_f, ov = [], [], []
for cx, cy, fill in sorted(pts):
    if cy < 136:
        series = "cc-Kapton" if fill < 0.7 else "CNT/PET"
        x, y = float(fx_e(cx)), float(fy_e(cy))
        rows_e.append((series, round(x * 2) / 2, x, y, cx, cy))
        ov.append((cx - 735, cy))
    elif 170 < cy < 300:
        x, y = float(fx_f(cx)), float(fy_f(cy))
        rows_f.append(("CNT/PET", round(x * 2) / 2, x, y, cx, cy))
        ov.append((cx - 735, cy))
rows_e.sort(key=lambda r: (r[0], r[2]))
rows_f.sort(key=lambda r: r[2])
assert len(rows_e) == 18 and len(rows_f) == 9, (len(rows_e), len(rows_f))

ue = abs(fy_e(1) - fy_e(0)); uxe = abs(fx_e(1) - fx_e(0))
uf = abs(fy_f(1) - fy_f(0)); uxf = abs(fx_f(1) - fx_f(0))
common = [
    "provenance: tier 3, digitized from the embedded raster image of SI page 12 (887 x 331 px JPEG, 150 ppi),"
    " native resolution; script sfig3ef_extract.py",
    "markers = dark connected components; centre = centroid of the marker ink (open circles: of the ring);"
    " filled vs open told apart by the ink fill fraction",
    "eht_nominal = digitized EHT rounded to the nearest 0.5 keV (the points sit at 2.5, 3, 4, ..., 10 keV)",
    "pixel_x, pixel_y = marker centre in the embedded image (for the overlay check)",
]
write_csv(os.path.join(HERE, "sfig3e.csv"), [
    "Supplementary Figure 3e (kubota2018 SI): depression depth / expansion height vs EHT",
    "columns: series (legend text), eht_nominal (keV), eht_keV (digitized), depth_height_nm"
    " (y axis 'Depth/height (nm)'; negative = depression, positive = expansion)",
] + common + [
    f"axis fit: y on 10 ticks +100 (unlabelled) ... -800 nm, max residual {res_ye:.2f} nm;"
    f" x on 6 ticks 0..10 keV, max residual {res_xe:.3f} keV",
    f"uncertainty: about 1 source pixel = {ue:.0f} nm in y, {uxe:.2f} keV in x",
    "the light-grey horizontal line at y = 0 is a reference line in the figure (not data)",
    "cross-check: panels b and d print the SCM depth/height above each imaged square (CNT -808 -708 -614 -511"
    " -419 -324 -232 -163 -140; cc-Kapton 134 113 109 85 44 54 45 21 11 for 10, 9, ..., 3, 2.5 keV);"
    " the digitized points agree with these to within about 1 pixel",
], ["series", "eht_nominal", "eht_keV", "depth_height_nm", "pixel_x", "pixel_y"], rows_e,
    fmt=["{}", "{:g}", "{:.2f}", "{:.0f}", "{:.2f}", "{:.2f}"])
write_csv(os.path.join(HERE, "sfig3f.csv"), [
    "Supplementary Figure 3f (kubota2018 SI): electron dose vs EHT (one series, filled circles, no legend)",
    "columns: series (named CNT/PET here after panel e; panel f has no legend), eht_nominal (keV),"
    " eht_keV (digitized), electron_dose_ke_per_nm2 (y axis 'Electron dose (ke- nm-2)')",
] + common + [
    f"axis fit: y on 4 ticks 4..7, max residual {res_yf:.3f}; x on 6 ticks 0..10 keV, max residual {res_xf:.3f} keV",
    f"uncertainty: about 1 source pixel = {uf:.2f} ke- nm-2 in y, {uxf:.2f} keV in x",
], ["series", "eht_nominal", "eht_keV", "electron_dose_ke_per_nm2", "pixel_x", "pixel_y"], rows_f,
    fmt=["{}", "{:g}", "{:.2f}", "{:.2f}", "{:.2f}", "{:.2f}"])
crop = img[:, 735:].copy()
overlay(crop, ov, os.path.join(WORK, "supp_sfig3ef_overlay.png"))
print("residuals", res_ye, res_xe, res_yf, res_xf)
for r in rows_e + rows_f:
    print(r[0], r[1], round(r[2], 2), round(r[3], 2))
