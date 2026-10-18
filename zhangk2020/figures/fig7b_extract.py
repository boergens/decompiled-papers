"""Fig. 7b (p. 8): profile of section C-C' of the reverse cutting edge (raw data + reversed fitted arc).
Digitized -> fig7b.csv.

Source: the embedded 300-ppi JPEG of Figure 7 (1767 x 657 px, xref 480); panel b is its right part.
Run: python3 -I -B figures/fig7b_extract.py  (from any directory) -> fig7b.csv, ../work/fig7b_overlay.png
"""
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import (embedded_image, gray, frame_lines, tick_positions, tick_positions_v,  # noqa: E402
                             fit_axis, trace_envelope, write_csv, overlay)

PDF = str(ROOT / "source" / "zhangk2020.pdf")
a = embedded_image(PDF, 8, bbox_near=(86.7, 553.4, 510.7, 711.3))
g = gray(a)
dark = g < 80
X0 = 850
rows_ = frame_lines(dark[:, X0:], 1, 0.5)
TOP, BOT = rows_[0], rows_[-1]
cols_ = [c for c in frame_lines(dark, 0, 0.5) if c[0] > X0]
LEFT, RIGHT = cols_[0], cols_[-1]
xl, xr = (LEFT[0] + LEFT[1]) / 2, (RIGHT[0] + RIGHT[1]) / 2
yt, yb = (TOP[0] + TOP[1]) / 2, (BOT[0] + BOT[1]) / 2
xt = tick_positions(dark, BOT, -1, 8, LEFT[1] + 3, RIGHT[0] - 3)
yt_r = tick_positions_v(dark, RIGHT, -1, 8, TOP[1] + 3, BOT[0] - 3)
assert len(xt) == 4 and len(yt_r) == 3, (xt, yt_r)
# "X-position 20 nm/div.", "Z-position 20 nm/div."; no numbers -> origin at the frame's lower left corner
fx, rx, _ = fit_axis([xl] + xt + [xr], [0, 20, 40, 60, 80, 100])
fz, rz, _ = fit_axis([yb] + yt_r[::-1] + [yt], [0, 20, 40, 60, 80])

A = a.astype(int)
red = ((A[:, :, 0] > 170) & (A[:, :, 1] < 120) & (A[:, :, 2] < 120)).astype(np.uint8)
red[:, :LEFT[1] + 1] = 0
red[:, RIGHT[0]:] = 0
red[:TOP[1] + 1] = 0
red[BOT[0]:] = 0
# the red line is ~6 px thick, the circle outlines ~1-2 px: an opening keeps only the line
line = cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))
ring = red.copy()
ring[cv2.dilate(line, np.ones((3, 3), np.uint8)) > 0] = 0
hc = cv2.HoughCircles((ring * 255).astype(np.uint8), cv2.HOUGH_GRADIENT, dp=1, minDist=12, param1=50, param2=8,
                      minRadius=8, maxRadius=13)[0]
ys, xs = np.nonzero(ring)
circles = []
for cx, cy, r in sorted(hc.tolist()):
    d = np.hypot(xs - cx, ys - cy)
    m = (d > r - 3) & (d < r + 3)
    if m.sum() < 15:
        continue
    X, Y = xs[m].astype(float), ys[m].astype(float)
    M = np.c_[2 * X, 2 * Y, np.ones_like(X)]
    sx_, sy_, c = np.linalg.lstsq(M, X ** 2 + Y ** 2, rcond=None)[0]
    circles.append((sx_, sy_, np.sqrt(c + sx_ ** 2 + sy_ ** 2), int(m.sum())))

env = trace_envelope(line.astype(bool), LEFT[1] + 1, RIGHT[0], TOP[1] + 1, BOT[0], half_width=3, min_px=3)

# black thick "Reversed fitted curve" (about 8-14 px thick): black mask, closing 5x5 (bridges the thin red
# circle outlines that cross it), opening 5x5 (removes text strokes, the thin arrow and leader lines);
# the arc is the largest remaining component inside the frame. Per column: centre of its pixels.
# Columns where the component is much taller than the local arc (the arrowhead of the R_mark_m label
# touches the arc) are flagged and left out of the circle check.
blk = (A.max(2) < 90).astype(np.uint8)
blk = cv2.morphologyEx(blk, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
blk = cv2.morphologyEx(blk, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
blk[:, :LEFT[1] + 8] = 0
blk[:, RIGHT[0] - 8:] = 0
blk[:TOP[1] + 8] = 0
blk[BOT[0] - 8:] = 0
n, lab, st, _ = cv2.connectedComponentsWithStats(blk)
big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
arc = lab == big
fit_pts, ext = [], []
for c in range(st[big, 0], st[big, 0] + st[big, 2]):
    r = np.nonzero(arc[:, c])[0]
    if len(r):
        fit_pts.append((c, (r.min() + r.max()) / 2))
        ext.append(r.max() - r.min() + 1)
ext = np.array(ext, float)
loc = np.array([np.median(ext[max(0, i - 25):i + 26]) for i in range(len(ext))])
flag = ext > loc + 6
fp = np.array(fit_pts, float)
fnm = np.c_[fx(fp[:, 0]), fz(fp[:, 1])]
ok = ~flag
M = np.c_[2 * fnm[ok, 0], 2 * fnm[ok, 1], np.ones(ok.sum())]
ccx, ccz, cc = np.linalg.lstsq(M, (fnm[ok] ** 2).sum(1), rcond=None)[0]
rad = float(np.sqrt(cc + ccx ** 2 + ccz ** 2))

rows, pts = [], []
for cx, cy, r, npx in circles:
    rows.append(("Raw data (circles)", float(fx(cx)), float(fz(cy)), "", ""))
    pts.append((cx, cy))
for c, ym, yu, yl in env:
    if ym == ym:
        rows.append(("Raw data (red line)", float(fx(c)), float(fz(ym)), float(fz(yl)), float(fz(yu))))
        pts.append((c, ym))
for (c, y), (x_, z_), f in zip(fp, fnm, flag):
    rows.append(("Reversed fitted curve" + (" (arrowhead overlap)" if f else ""), float(x_), float(z_), "", ""))
overlay(a, pts, str(ROOT / "work" / "fig7b_overlay.png"))
overlay(cv2.imread(str(ROOT / "work" / "fig7b_overlay.png"))[:, :, ::-1].copy(), [tuple(p) for p in fp],
        str(ROOT / "work" / "fig7b_overlay.png"), colour=(0, 200, 255))

hdr = [
    "zhangk2020 Fig. 7b (p. 8): Profile of Section C-C' (Figure 7. Measured reverse diamond tool cutting edge).",
    "Provenance: tier 3, digitized from the embedded 300-ppi JPEG (xref 480, 1767 x 657 px).",
    "Axes carry no numbers: 'X-position 20 nm/div.', 'Z-position 20 nm/div.'. Origin arbitrary: x = 0 at the left frame line, z = 0 at the bottom frame line.",
    f"Calibration: frame columns {xl:.1f}/{xr:.1f} px, x ticks at columns {', '.join(f'{v:.1f}' for v in xt)} (= 20, 40, 60, 80 nm), max residual {rx:.2f} nm;",
    f"frame rows {yt:.1f}/{yb:.1f} px, z ticks at rows {', '.join(f'{v:.1f}' for v in yt_r)} (= 60, 40, 20 nm), max residual {rz:.2f} nm.",
    f"One source pixel = {100 / (xr - xl):.3f} nm in x and {80 / (yb - yt):.3f} nm in z.",
    "series 'Raw data (circles)': centres of the red open circles (Hough transform on the circle outlines after removing the thick line,",
    f"then a least-squares circle fit to each outline; {len(circles)} circles; uncertainty about 1 px = 0.13-0.15 nm); circles behind the black curve may be missed.",
    "series 'Raw data (red line)': the red line through the circles, per pixel column (opening 4x4 removes the circle outlines; z_low/z_high = run ends",
    "moved inward by 3 px, z_nm = their mean). Where the black curve covers it, the red line is hidden and the column is skipped or follows the visible part.",
    "series 'Reversed fitted curve': centre of the thick black arc per pixel column (black mask, closing and opening 5x5, largest component);",
    "columns where the arrowhead of the R_mark_m label touches the arc are named 'Reversed fitted curve (arrowhead overlap)' and are biased.",
    f"Check (decompiler): least-squares circle through the unflagged 'Reversed fitted curve' points has radius {rad:.2f} nm (centre x {ccx:.2f}, z {ccz:.2f} nm);",
    "the plot label says R_mark_m = 21.04 nm. Labels in the panel: '(b)', 'Raw data', 'R_mark_m=21.04 nm', 'Reversed fitted curve'.",
]
write_csv(ROOT / "figures" / "fig7b.csv", hdr, ["series", "x_nm", "z_nm", "z_low_nm", "z_high_nm"], rows,
          fmt=["{}", "{:.2f}", "{:.2f}", "{:.2f}", "{:.2f}"])
print("\n".join(hdr))
print(len(rows), "rows")
