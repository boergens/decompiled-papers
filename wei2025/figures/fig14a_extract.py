"""Digitize Figure 14(a) of Wei et al. 2025 (IJNAMG 49:2949), PDF p. 12: absolute value of the average sliding force.

Source: the embedded 300 ppi image of Figure 14 (1500 x 660 px, lossless); panel (a) is its left part. No vector data.
    python3 -I -B figures/fig14a_extract.py  -> figures/fig14a.csv, work/fig14a_overlay.png
Six blue sphere symbols joined by a dashed line; symbol centre = centroid of the blue blob left after a
morphological opening that removes the thin dashed line.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import embedded_image, write_csv, overlay  # noqa: E402
from figB_common import frame, ticks_h, ticks_v, linfit  # noqa: E402

PDF = HERE.parent / "source" / "wei2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)
a = embedded_image(str(PDF), 12, bbox_near=(117.5, 353.7, 477.5, 512.1))
ai = a.astype(int)
dark = ai.mean(2) < 130
f = frame(dark, (60, 0, 700, 480))
L, R, T, B = f["left"], f["right"], f["top"], f["bottom"]
xt = ticks_h(dark, B, -1, 8, L[1] + 1, R[0])
yt = ticks_v(dark, L, +1, 8, T[1] + 1, B[0])
ylab = [4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0]
assert len(xt) == 6 and len(yt) == 7, (xt, yt)
fy, ry, sy = linfit(yt, ylab)
LABELS = ["Pyramid-0°", "Pyramid-45°", "Sphere (R = 10 Å)", "Sphere (R = 14.5 Å)", "Sphere (R = 20 Å)", "Sphere (R = 25 Å)"]

blue = (ai[:, :, 2] > 120) & (ai[:, :, 2] - ai[:, :, 0] > 40) & (ai[:, :, 2] - ai[:, :, 1] > 40)
blue[:, :L[1] + 2] = False
blue[:, R[0] - 1:] = False
blue[:T[1] + 2] = False
blue[B[0] - 1:] = False
disk = np.hypot(*np.mgrid[-3:4, -3:4]) <= 3.2
op = ndimage.binary_opening(ndimage.binary_fill_holes(blue), structure=disk)
lab, n = ndimage.label(op)
cents = sorted(ndimage.center_of_mass(op, lab, range(1, n + 1)), key=lambda t: t[1])
assert len(cents) == 6, cents
rows, pts = [], []
for (cy, cx), name in zip(cents, LABELS):
    tick = min(xt, key=lambda t: abs(t - cx))
    rows.append((name, float(cx), float(tick), float(fy(cy))))
    pts.append((cx, cy))
overlay(a, pts, str(WORK / "fig14a_overlay.png"))
write_csv(str(HERE / "fig14a.csv"), [
    "Wei et al. 2025, Figure 14(a): absolute value of the average sliding force (nN) per indenter system, h_c = 4 Å",
    "  (average over the data at sliding distances over 10 Å, per the caption).",
    "Category x axis: six evenly spaced labels (rotated, bold) on the major ticks; points joined by a blue dashed line.",
    "Columns: label = printed category label; symbol_centre_px / tick_px = symbol centre and nearest major tick, column of",
    "  the 1500 px wide embedded image; abs_avg_sliding_force_nN = symbol centre on the y axis.",
    "Provenance: tier 3, digitized from the embedded 300 ppi image of Figure 14 by fig14a_extract.py; symbol centre =",
    f"  centroid of the blue sphere symbol after filling its highlight and an opening with a 7 px disk; y calibrated on the 7 labelled major ticks 1.0-4.0 nN (max residual {ry:.4f} nN).",
    f"Uncertainty: about +-{2*abs(sy):.3f} nN (2 px; the symbols are shaded spheres ~12 px across).",
], ["label", "symbol_centre_px", "tick_px", "abs_avg_sliding_force_nN"], rows, fmt="{:.4g}")
print([(r[0], round(r[3], 3), round(r[1] - r[2], 1)) for r in rows], ry)
