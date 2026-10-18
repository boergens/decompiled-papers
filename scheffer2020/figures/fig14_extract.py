"""Fig. 14 (p. 31): UMAP scatter of cells of nine types (dim1 vs dim2, arbitrary units). Tier 3, digitized from the
embedded JPEG (1067 x 998 px) at native resolution.

The markers are semi-transparent squares (about 16 px wide) that overlap heavily inside each cluster, so single
markers cannot be separated reliably. Each pixel is assigned to the series whose legend colour explains it best
(pixel on the ray from white through the legend colour, scale 0.85-1.6 to allow for overlapping translucent
markers, distance < 20 RGB units; pixels where two colours overlap stay unassigned). Each series mask is closed
and then opened with a 5x5 kernel (bridges the 1-2 px gaps cut by the annotation arrows; removes thin lines and
anti-aliased edges) and split into connected blobs.
One CSV row per blob ('stack'): centroid, the centres of its outermost markers (blob extent minus half a marker
on each side), area and an area-based estimate of the number of markers.
Calibration: light-grey gridlines at dim1 = -10, -5, 0, 5 and dim2 = 10, 5, 0, -5, -10; linear fits.
"""
import csv
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import rasterfig as rf  # noqa: E402

LEG = {"ER3p_a": (91, 146, 190), "ER2_c": (194, 210, 235), "ER2_d": (243, 157, 82), "ExR7": (247, 202, 155),
       "EPG": (110, 175, 95), "ER3p_b": (185, 226, 168), "ER2_a": (206, 91, 88), "ExR6": (242, 177, 173),
       "ER2_b": (162, 136, 197)}            # legend order; colours sampled from the legend squares
a = rf.load(31).astype(float)
H, W, _ = a.shape
Wt = np.array([255.0, 255, 255])

# calibration from gridlines
grey = (np.abs(a - 235).max(2) < 12)
def lines(mask_sum, lo, hi):
    idx = [i for i in range(lo, hi) if mask_sum[i] > 500]
    grp = np.split(np.array(idx), np.where(np.diff(idx) > 1)[0] + 1)
    return [g.mean() for g in grp]
vx = lines(grey.sum(0), 100, 1000)            # dim1 = -10, -5, 0, 5
hy = lines(grey.sum(1), 10, 900)              # dim2 = 10, 5, 0, -5, -10
assert len(vx) == 4 and len(hy) == 5, (vx, hy)
kx, bx = np.polyfit(vx, [-10, -5, 0, 5], 1)
ky, by = np.polyfit(hy, [10, 5, 0, -5, -10], 1)
xres = np.array([-10, -5, 0, 5]) - (kx * np.array(vx) + bx)
yres = np.array([10, 5, 0, -5, -10]) - (ky * np.array(hy) + by)
X = lambda px: kx * px + bx
Y = lambda py: ky * py + by

# pixel classification
p = a - Wt
dist = []
for name, c in LEG.items():
    d = np.array(c, float) - Wt
    t = np.clip((p @ d) / (d @ d), 0.85, 1.6)
    dist.append(np.linalg.norm(p - t[..., None] * d, axis=2))
dist = np.stack(dist)
best = dist.argmin(0)
ok = dist.min(0) < 20
ok[:300, 920:] = False                         # legend box
SIDE = 16.0                                    # marker width in px (isolated ExR6 blob: 18 x 16 px incl. edges)
AREA1 = 265.0                                  # area of one marker after the opening (isolated ExR6 blob: 268 px)

rows = []
overlay = a.astype(np.uint8).copy()
for si, name in enumerate(LEG):
    m = ((best == si) & ok).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))   # bridge the gaps cut by the annotation arrows
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    for i in range(1, n):
        x0, y0, w, h, area = st[i]
        if area < 0.4 * AREA1:
            continue
        cx, cy = cen[i]
        est = max(1, int(round(area / AREA1)))
        xc0, xc1 = x0 + SIDE / 2 - 0.5, x0 + w - SIDE / 2 - 0.5
        yc0, yc1 = y0 + SIDE / 2 - 0.5, y0 + h - SIDE / 2 - 0.5
        if xc1 < xc0: xc0 = xc1 = cx
        if yc1 < yc0: yc0 = yc1 = cy
        rows.append([name, X(cx), Y(cy), X(xc0), X(xc1), Y(yc1), Y(yc0), int(area), est,
                     "single" if est == 1 and w <= SIDE + 4 and h <= SIDE + 4 else "stack"])
        cv2.rectangle(overlay, (int(x0), int(y0)), (int(x0 + w - 1), int(y0 + h - 1)), (255, 0, 0), 1)
        cv2.drawMarker(overlay, (int(round(cx)), int(round(cy))), (0, 0, 0), cv2.MARKER_CROSS, 8, 1)

with open(HERE / "fig14.csv", "w", newline="") as f:
    f.write("# Figure 14 (p. 31 of elife-57443-v4.pdf): cells of nine types plotted by connectivity after UMAP; dim1 (AU) vs dim2 (AU).\n")
    f.write("# Provenance: tier 3, digitized from the embedded JPEG (1067 x 998 px) by fig14_extract.py. No source data named for this figure.\n")
    f.write(f"# Calibration: gridlines; dim1 {1/kx:.2f} px/AU (residuals {np.round(xres, 3).tolist()}), dim2 {-1/ky:.2f} px/AU (residuals {np.round(yres, 3).tolist()}).\n")
    f.write("# Markers are translucent squares (~16 px = ~0.38 AU wide) overlapping inside clusters: individual cells cannot be separated.\n")
    f.write("#   One row per connected blob of one colour ('stack'): x_centroid/y_centroid = blob centroid; x_min..x_max, y_min..y_max =\n")
    f.write("#   centres of the outermost markers of the blob (blob extent minus half a marker width); area_px = blob area in image px;\n")
    f.write("#   est_markers = area_px / 265 (area of one isolated marker), a LOWER bound when markers lie on top of each other;\n")
    f.write("#   status = single (one marker) or stack. Pixels where two series overlap (e.g. ER2_d/ER2_b, ER2_d/ER2_a, EPG/ExR6)\n")
    f.write("#   are not assigned, so touching clusters of different series are slightly eroded at their contact.\n")
    f.write("# Uncertainty: centroid +-0.05 AU; outer-marker centres +-0.1 AU.\n")
    w = csv.writer(f)
    w.writerow(["series", "x_centroid", "y_centroid", "x_min", "x_max", "y_min", "y_max", "area_px", "est_markers", "status"])
    for r in rows:
        w.writerow([r[0]] + [round(v, 3) for v in r[1:7]] + r[7:])
(HERE.parent / "work").mkdir(exist_ok=True)
cv2.imwrite(str(HERE.parent / "work" / "fig14_overlay.png"), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
for r in rows:
    print(r[0], [round(v, 2) for v in r[1:7]], r[7:])
