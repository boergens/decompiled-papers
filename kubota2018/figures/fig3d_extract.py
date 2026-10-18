#!/usr/bin/env python3
"""Fig. 3d (3D laser SCM surface profile, colour-coded depth) -> fig3d.csv (grid, nm).

Tier 3 (digitized colour map). The panel is part of the embedded RGB JPEG (842 x 1599 px, 300 ppi)
that holds Fig. 3a-d on p. 5 of the article. The colour bar (black-blue-cyan-green-yellow-orange)
is inside the image (rows 272-282 of the panel crop, columns 42-290); its labels "-550 -400 -200 0 nm"
are PDF text. The bar has no tick marks, so the value scale is a piecewise-linear map through the
label centres (PDF x converted to image columns). Every map pixel is mapped to the nearest bar colour
by hue; pixels with low saturation/brightness (grey/brown shading,
dark outlines) are left empty (NaN). The SCM rendering is shaded (3D lighting), so values are
approximate; see the header of fig3d.csv for the check against the printed depths.
"""
import csv, os, sys
import numpy as np
import cv2
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from digitize_common import embedded_image
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "../source/s41467-017-02768-7.pdf")
IMG_BBOX = (56.6, 65.7, 258.7, 449.5)   # placement of the embedded image on p. 5 (PDF pt)
ROW0 = 1267                              # first image row of panel d crop
SMIN, VMIN = 90, 60                      # minimum saturation / brightness (0-255) to accept a pixel

a = embedded_image(PDF, 5, bbox_near=IMG_BBOX)
sx = a.shape[1] / (IMG_BBOX[2] - IMG_BBOX[0])
d = a[ROW0:].copy()
H, W = d.shape[:2]

# colour-bar samples: median over bar rows 273-281, columns 42..290
bar_cols = np.arange(42, 291)
bar = np.median(d[273:282, 42:291].astype(float), axis=0)          # (n,3) RGB

# label centres -> columns (PDF text bboxes on p. 5)
doc = pymupdf.open(PDF)
labels = {}
for b in doc[4].get_text("dict", clip=pymupdf.Rect(56, 436, 150, 450))["blocks"]:
    for l in b["lines"]:
        for s in l["spans"]:
            t = s["text"].replace("–", "-").replace("nm", "").strip()
            x0, _, x1, _ = s["bbox"]
            if t == "0":
                # "0 nm" span: centre of the digit "0" = left edge + half a digit width
                xc = x0 + (x1 - x0) * 0.13
            else:
                xc = (x0 + x1) / 2
            labels[float(t)] = (xc - IMG_BBOX[0]) * sx
lab_v = np.array(sorted(labels))
lab_c = np.array([labels[v] for v in lab_v])
order = np.argsort(lab_c)
bar_val = np.interp(bar_cols, lab_c[order], lab_v[order])  # extrapolates flat beyond end labels

# Map by hue: the rendering's lighting changes brightness and saturation, but keeps the hue roughly.
# Bar hue (OpenCV HSV_FULL, 0-255) falls monotonically from ~162 (dark blue, column 74) to ~18 (orange, column 290);
# the black start of the bar (columns 42-73, about -550 to -480 nm by the label scale) has no hue and cannot be mapped.
bar_hsv = cv2.cvtColor(bar.reshape(1, -1, 3).astype(np.uint8), cv2.COLOR_RGB2HSV_FULL).reshape(-1, 3).astype(float)
use = bar_cols >= 74
bh, bv = bar_hsv[use, 0], bar_val[use]
img_hsv = cv2.cvtColor(d, cv2.COLOR_RGB2HSV_FULL).astype(float)
hue, sat, vv = img_hsv[..., 0], img_hsv[..., 1], img_hsv[..., 2]
# nearest bar hue (bh is monotonic decreasing): interpolate value on hue
o = np.argsort(bh)
val = np.interp(hue, bh[o], bv[o], left=np.nan, right=np.nan)
val[(sat < SMIN) | (vv < VMIN)] = np.nan
val[(hue < bh.min() - 3) | (hue > bh.max() + 3)] = np.nan
val[268:286, 36:296] = np.nan     # the colour bar itself

# check against the printed depths: median inside the inner part of each square
squares = {"-223 nm": (75, 100, 195, 200), "-337 nm": (260, 100, 385, 200),
           "-371nm": (450, 100, 580, 210), "-383 nm": (635, 100, 770, 220)}
# (x0, y0, x1, y1) in panel-crop pixels, inner areas chosen by eye on work/fig3d_native.png
checks = []
for k, (x0, y0, x1, y1) in squares.items():
    v = val[y0:y1, x0:x1]
    checks.append((k, np.nanmedian(v), np.nanpercentile(v, 25), np.nanpercentile(v, 75), np.isfinite(v).mean()))

out = os.path.join(HERE, "fig3d.csv")
with open(out, "w", newline="") as f:
    f.write("# Fig. 3d | 3D laser SCM surface profile of the CNT tape after repeated imaging (colour = depth, nm)\n")
    f.write("# Provenance: tier 3 (digitized colour map) from the embedded 300 ppi JPEG on p. 5, by fig3d_extract.py.\n")
    f.write("# Grid: one CSV row per image row of the panel crop (row 0 = top), one column per image column (col 0 = left);\n")
    f.write(f"#   {H} rows x {W} columns, 1 px = {1/sx:.4f} pt = {25.4/72/sx*1000:.1f} um on the printed page (no lateral scale bar in panel d).\n")
    f.write("# Value: depth in nm from the colour bar (labels -550, -400, -200, 0 nm; no tick marks, so the scale is piecewise linear\n")
    f.write(f"#   through the label centres at image columns {', '.join(f'{v:g}->{c:.1f}' for v, c in zip(lab_v, lab_c))}; label-position uncertainty ~ +-5 px ~ +-15 nm).\n")
    f.write(f"# Each pixel -> bar position with the same hue (OpenCV HSV); empty = saturation < {SMIN} or brightness < {VMIN} (grey/brown shading,\n")
    f.write("#   dark outlines), hue outside the bar's hue range, or the bar itself. The black start of the bar (about -550 to -480 nm) has no hue\n")
    f.write("#   and cannot be mapped, so the deepest values are missing.\n")
    f.write("# The map is a shaded 3D rendering (lighting changes the colours), and JPEG compression adds noise: values are APPROXIMATE,\n")
    f.write("#   typically +-30 nm or worse; the colour scale is only resolved to ~2 nm per bar pixel.\n")
    f.write("# Check against the depths printed above the squares (median [IQR] of mapped values in the inner square area, fraction mapped):\n")
    for k, med, q1, q3, fr in checks:
        f.write(f"#   printed {k}: mapped {med:.0f} [{q1:.0f}, {q3:.0f}] nm, {fr:.0%} of pixels mapped\n")
    w = csv.writer(f)
    w.writerow([f"c{j}" for j in range(W)])
    for row in val:
        w.writerow(["" if np.isnan(v) else f"{v:.0f}" for v in row])
print(out)
for c in checks: print(c)
