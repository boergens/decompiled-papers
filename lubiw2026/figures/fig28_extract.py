#!/usr/bin/env python3
"""Figure 28 of Lubiw & Schaefer: digitize the GeoGebra coordinate construction -> fig28.csv (tier 3, raster).

Source: figures/fig28.png, the authors' file (Treestwodisks.png, 417 x 284 px).  The integer grid lines give the axis
calibration; the dark filled discs are found as connected components of the dark mask after an erosion that removes
the lines; the two circles are fitted to their dark pixels.  Also draws work/fig28_overlay.png when work/ exists.
Run: python3 -I -B figures/fig28_extract.py
"""
import os
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(HERE, "fig28.png")).convert("RGBA")
bg = Image.new("RGBA", im.size, "white")
bg.alpha_composite(im)
rgb = np.array(bg.convert("RGB"))
g = rgb.astype(float).mean(2)
H, W = g.shape

# Grid lines: columns and rows whose median grey is clearly darker than their neighbours.  Major lines every unit.
def peaks(profile, min_dist):
    out = []
    bg_level = np.median(profile)
    for i in np.argsort(profile):
        if profile[i] > bg_level - 12:
            break
        if all(abs(i - j) >= min_dist for j in out):
            out.append(int(i))
    return sorted(out)

col = np.median(g, axis=0)
row = np.median(g, axis=1)
cols = peaks(col, 40)
rows = peaks(row, 40)
print("major columns", cols, "rows", rows)
# Printed labels: x = -2 ... 3 at the columns, y = 2, 1, 0, -1 at the rows (top to bottom).
step_x = np.median(np.diff(cols))
step_y = step_x  # GeoGebra axis ratio 1:1 (checked below by the fit); a row not on the unit spacing is the image edge
# the x = 0 column is the darkest (y axis), the y = 0 row is the darkest (x axis)
x0 = cols[int(np.argmin([col[c] for c in cols]))]
y0 = rows[int(np.argmin([row[r] for r in rows]))]
xs = np.array(cols, float)
xv = np.round((xs - x0) / step_x)
ax, bx = np.polyfit(xs, xv, 1)
rows = [r for r in rows if abs((y0 - r) / step_y - round((y0 - r) / step_y)) < 0.1]
ys = np.array(rows, float)
yv = np.round((y0 - ys) / step_y)
ay, by = np.polyfit(ys, yv, 1)
print("x ticks", list(zip(cols, xv)), "y ticks", list(zip(rows, yv)))
print("px per unit: x %.2f, y %.2f" % (1 / ax, -1 / ay))
fx = lambda c: ax * c + bx
fy = lambda r: ay * r + by

# Filled discs
dark = (g < 110).astype(np.uint8)
er = cv2.erode(dark, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
n, lab, stats, cent = cv2.connectedComponentsWithStats(er)
pts = []
for i in range(1, n):
    pts.append((cent[i][0], cent[i][1], stats[i][4]))
pts = [p for p in pts if p[2] >= 3]
print("discs", [(round(p[0], 1), round(p[1], 1), p[2]) for p in pts])
names = {}
for c, r, a in pts:
    x, y = fx(c), fy(r)
    if abs(x) < 0.2 and abs(y + 1) < 0.2:
        names["bottom point of D_u"] = (x, y, c, r)
    elif abs(x) < 0.2 and abs(y) < 0.2:
        names["centre u of D_u"] = (x, y, c, r)
    elif abs(x - 0.8) < 0.2 and abs(y - 0.6) < 0.2:
        names["contact point of D_u and D_v"] = (x, y, c, r)
    elif abs(x - 1.6) < 0.2 and abs(y - 1.2) < 0.2:
        names["centre v of D_v"] = (x, y, c, r)
    elif abs(x - 1.6) < 0.2 and abs(y - 2.2) < 0.2:
        names["top point of D_v"] = (x, y, c, r)
assert len(names) == 5, names

# Circle radii: dark pixels near the expected circle about each centre, median distance
def radius(cx, cy):
    yy, xx = np.nonzero(g < 130)
    d = np.hypot(xx - cx, yy - cy)
    sel = (d > 0.8 / ax) & (d < 1.2 / ax)
    return float(np.median(d[sel]))

ru = radius(*names["centre u of D_u"][2:]) * ax
rv = radius(*names["centre v of D_v"][2:]) * ax

# Top of the blue slope triangle: top end of the blue vertical at x = 1
blue = (rgb[:, :, 2].astype(int) - rgb[:, :, 0].astype(int) > 80)
c1 = int(round((1 - bx) / ax))
rr = np.nonzero(blue[:, c1 - 1:c1 + 2].any(axis=1))[0]
top = fy(rr.min())
base_y = fy(rr.max())

out = os.path.join(HERE, "fig28.csv")
with open(out, "w") as f:
    f.write("# Figure 28 of Lubiw & Schaefer (arXiv:2508.10136v3, p. 32): two pennies D_u and D_v with slope parameter m = m_uv.\n")
    f.write("# A geometric construction on a GeoGebra coordinate grid, not plotted data; digitized because the panel has numbered axes.\n")
    f.write("# Columns: object (decompiler's names; only u, v, 1 and m are printed in the figure); x, y in the figure's axis units; radius for circles, empty otherwise.\n")
    f.write("# Provenance: tier 3, digitized from the raster figures/fig28.png (authors' Treestwodisks.png, 417 x 284 px) by fig28_extract.py.\n")
    f.write("# Calibration: integer grid lines, %.1f px per unit. Uncertainty about 0.02 units (one to two pixels).\n" % (1 / ax))
    f.write("# Printed in the figure and not digitized: m = 2.0095100503047; the blue base of the triangle is labelled 1.\n")
    f.write("# Oddity: the top end of the blue vertical merges into the dark slope line, so its y here reads low by up to about 0.06.\n")
    f.write("object,x,y,radius\n")
    for k in ["bottom point of D_u", "centre u of D_u", "contact point of D_u and D_v", "centre v of D_v", "top point of D_v"]:
        f.write("%s,%.2f,%.2f,\n" % (k, round(names[k][0], 2) + 0.0, round(names[k][1], 2) + 0.0))
    f.write("circle D_u,%.2f,%.2f,%.2f\n" % (round(names["centre u of D_u"][0], 2) + 0.0, round(names["centre u of D_u"][1], 2) + 0.0, ru))
    f.write("circle D_v,%.2f,%.2f,%.2f\n" % (names["centre v of D_v"][0], names["centre v of D_v"][1], rv))
    f.write("slope triangle corner (base right end),1.00,%.2f,\n" % base_y)
    f.write("slope triangle corner (top),1.00,%.2f,\n" % top)
print(open(out).read())

work = os.path.join(os.path.dirname(HERE), "work")
if os.path.isdir(work):
    ov = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ov = cv2.resize(ov, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    for k, (x, y, c, r) in names.items():
        cv2.drawMarker(ov, (int(c * 3), int(r * 3)), (0, 0, 255), cv2.MARKER_CROSS, 24, 2)
    for k, rad in (("centre u of D_u", ru), ("centre v of D_v", rv)):
        x, y, c, r = names[k]
        cv2.circle(ov, (int(c * 3), int(r * 3)), int(rad / ax * 3), (0, 0, 255), 1)
    cv2.imwrite(os.path.join(work, "fig28_overlay.png"), ov)
