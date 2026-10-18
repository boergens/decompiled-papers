"""Digitize Figure 4B of Denk & Horstmann 2004 (PLoS Biol 2: e329) -> fig4b.csv (tier 3).

Source: the embedded 500 x 852 px JPEG (150 ppi) on PDF page 6; panel B is the lower part of it.
Calibration from the tick marks on the two axis lines (they cross at the origin):
  x: ticks below the horizontal axis (row 649) at columns 62.0 (-200), 160.0 (-100), 355.0 (100), 453.0 (200);
  y: ticks right of the vertical axis (cols 257-258) at rows 452.5 (200), 551.0 (100), 747.0 (-100), 845.4 (-200).
Dots are ~3-4 px black discs. Each dark connected component (grey < 110) inside the data area,
outside the tick labels and axis titles, is one row:
  * kind 'dot': a single isolated marker (its ink centroid);
  * kind 'group_k': k touching markers (k = round(area / median single-dot area) <= 6), split into k
    centres by k-means on the component's pixels;
  * kind 'cluster': the dense central cluster, which cannot be split; given as one row with its ink
    centroid, bounding box and estimated marker count (area / single-dot area; an underestimate,
    since markers overlap).
"""
import csv
import sys
from pathlib import Path

import numpy as np
import cv2
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import digitize_common as dc  # noqa: E402

PDF = HERE.parent / "source" / "denk2004.pdf"
a = dc.embedded_image(str(PDF), 6, bbox_near=(45, 52, 285, 461))
g = a.astype(float).mean(2)


def centroids(w, thr, off):
    lab, n = ndimage.label(w > thr)
    out = []
    for i in range(1, n + 1):
        idx = np.where(lab == i)[0]
        out.append(off + float((w[idx] * idx).sum() / w[idx].sum()))
    return out


# tick marks (short grey strokes on the far side of the axes from the data cluster)
xt = [c for c in centroids((235 - g[650:654, :]).clip(0).sum(0), 40, 0)
      if min(abs(c - v) for v in (62, 160, 355, 453)) < 3]
yt = [r for r in centroids((235 - g[430:852, 259:263]).clip(0).sum(1), 40, 430)
      if min(abs(r - v) for v in (452.5, 551, 747, 845.4)) < 3]
assert len(xt) == 4 and len(yt) == 4, (xt, yt)
fx, rx, _ = dc.fit_axis(xt, [-200, -100, 100, 200])
fy, ry, _ = dc.fit_axis(yt, [200, 100, -100, -200])

# data area and label boxes to exclude (native pixel coordinates: col0, row0, col1, row1)
AREA = (180, 470, 440, 700)
LABELS = [(310, 470, 340, 572),   # "shift_y (nm)" title (rotated)
          (262, 538, 305, 562),   # "100" y tick label
          (140, 655, 185, 672), (335, 655, 380, 672), (430, 655, 470, 672),  # x tick labels
          (360, 690, 470, 715)]   # "shift_x (nm)" title
dark = g < 110
dark[:, 255:261] &= g[:, 255:261] < 90       # axis line is light grey; keep only dots on it
mask = np.zeros_like(dark)
c0, r0, c1, r1 = AREA
mask[r0:r1, c0:c1] = dark[r0:r1, c0:c1]
for c0, r0, c1, r1 in LABELS:
    mask[r0:r1, c0:c1] = False
lab, n = ndimage.label(mask)
comps = []
for i in range(1, n + 1):
    rr, cc = np.where(lab == i)
    w = (110 - g[rr, cc]).clip(1)
    comps.append(dict(rr=rr, cc=cc, w=w, area=len(rr), h=np.ptp(rr) + 1, wd=np.ptp(cc) + 1))
single = [c["area"] for c in comps if c["h"] <= 5 and c["wd"] <= 5 and c["area"] >= 4]
dot_area = float(np.median(single))

rows = []
pts = []
for c in comps:
    if c["area"] < 3:
        continue                          # JPEG speckle
    k = max(1, int(round(c["area"] / dot_area)))
    cy = float((c["rr"] * c["w"]).sum() / c["w"].sum())
    cx = float((c["cc"] * c["w"]).sum() / c["w"].sum())
    bbox = (fx(c["cc"].min()), fx(c["cc"].max()), fy(c["rr"].max()), fy(c["rr"].min()))
    if k == 1:
        rows.append(["dot", fx(cx), fy(cy), 1, *bbox])
        pts.append((cx, cy))
    elif k <= 6:
        Z = np.float32(np.column_stack([c["cc"], c["rr"]]))
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.1)
        _, _, cen = cv2.kmeans(Z, k, None, crit, 10, cv2.KMEANS_PP_CENTERS)
        for x, y in cen:
            rows.append([f"group_{k}", fx(x), fy(y), 1, *bbox])
            pts.append((x, y))
    else:
        rows.append(["cluster", fx(cx), fy(cy), k, *bbox])
        pts.append((cx, cy))

rows.sort(key=lambda r: (r[0] == "cluster", -r[2]))
hdr = [
    "Denk & Horstmann 2004, PLoS Biol 2(11): e329, Figure 4B: x/y displacement of the 512x512 region",
    "  (scatter plot), shift_x (nm) and shift_y (nm); same dataset as Figure 4A.",
    "Provenance: tier 3, digitized from the embedded 500x852 px JPEG (150 ppi) on PDF page 6 by fig4b_extract.py.",
    f"Axis calibration: linear on 4 tick marks per axis (-200, -100, 100, 200 nm); max residual x {rx:.2f} nm,",
    f"  y {ry:.2f} nm; 1 px = {fx(1)-fx(0):.2f} nm. The axes cross at (0, 0).",
    "Columns: kind ('dot' = isolated marker; 'group_k' = one of k touching markers split by k-means;",
    "  'cluster' = the dense central cluster that cannot be split, one row), shift_x_nm, shift_y_nm (marker",
    "  centre, or ink centroid for the cluster), n_markers (1, or for the cluster the estimated count = ink",
    f"  area / single-marker area {dot_area:.0f} px, an underestimate because markers overlap), bbox_* (the",
    "  connected ink component's extent in nm, marker size included).",
    "Uncertainty: +-1.5 nm for isolated markers (JPEG, ~1.5 px); group splits +-3 nm. The caption gives the",
    "  standard deviations of the central cluster: 10.9 nm (x) and 11.8 nm (y).",
]
with open(HERE / "fig4b.csv", "w", newline="") as f:
    for h in hdr:
        f.write("# " + h + "\n")
    wr = csv.writer(f)
    wr.writerow(["kind", "shift_x_nm", "shift_y_nm", "n_markers", "bbox_x_min_nm", "bbox_x_max_nm",
                 "bbox_y_min_nm", "bbox_y_max_nm"])
    for r in rows:
        wr.writerow([r[0]] + [f"{v:.1f}" for v in r[1:3]] + [r[3]] + [f"{v:.1f}" for v in r[4:]])

big = cv2.resize(a, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
for x, y in pts:
    cv2.circle(big, (int(3 * x + 1), int(3 * y + 1)), 4, (255, 0, 255), 1)
for c0, r0, c1, r1 in LABELS + [AREA]:
    cv2.rectangle(big, (3 * c0, 3 * r0), (3 * c1, 3 * r1), (0, 160, 255), 1)
(HERE.parent / "work").mkdir(exist_ok=True)
cv2.imwrite(str(HERE.parent / "work" / "fig4b_overlay.png"),
            cv2.cvtColor(big[3 * 440:3 * 720, 3 * 170:3 * 480], cv2.COLOR_RGB2BGR))
print("ticks", xt, yt, "res", rx, ry, "dot area", dot_area, "rows", len(rows),
      "kinds", {k: sum(r[0] == k for r in rows) for k in set(r[0] for r in rows)})
