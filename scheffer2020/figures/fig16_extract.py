"""Fig. 16 (p. 34): scatter of synapse counts per connection (path) in the ellipsoid body, at 50 % vs 30 % proofreading
completeness (~40,000 '+' markers), with two reference lines ('Five synapses': orange above, grey below the diagonal).
Tier 3, digitized from the embedded raster (2207 x 1486 px) at native resolution.

The markers are too dense to separate inside the main band, and they do not sit on an integer grid (fractional
parts of the isolated markers are spread evenly), so the CSV gives:
  kind=marker          every '+' marker that can be seen whole: the cross template (13 x 13 px, arms 3 px) is
                       >= 80 % blue, not counting pixels of the reference lines drawn over it, and its four 4 x 4 px corners are < 15 % blue (i.e. no neighbouring ink), centre;
  kind=envelope_upper  per pixel column, the topmost blue ink pixel of the whole point cloud (data units);
  kind=envelope_lower  per pixel column, the lowest blue ink pixel;
  kind=line_orange / line_grey  the two reference lines, least-squares fits to their pixels, given at x = 0 and 100.
Calibration: the six labelled tick marks on each axis (0, 20, ..., 100), linear fits.
"""
import csv
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import rasterfig as rf  # noqa: E402

a = rf.load(34).astype(float)
g = a.mean(2)
H, W = g.shape

# --- calibration
ax_col = [c for c in range(W) if (g[:, c] < 60).sum() > 900][0]
ax_row = [r for r in range(H) if (g[r, :] < 60).sum() > 1500][-1]
yt = [r for r in range(H) if (g[r, ax_col - 17:ax_col - 1] < 100).sum() >= 14]
xt = [c for c in range(W) if (g[ax_row + 2:ax_row + 20, c] < 100).sum() >= 16]
grp = lambda v: [x.mean() for x in np.split(np.array(v), np.where(np.diff(v) > 1)[0] + 1)]
ytp, xtp = grp(yt), grp(xt)
vals = [0, 20, 40, 60, 80, 100]
assert len(ytp) == 6 and len(xtp) == 6, (ytp, xtp)
ky, by = np.polyfit(ytp, vals[::-1], 1)
kx, bx = np.polyfit(xtp, vals, 1)
yres = np.array(vals[::-1]) - (ky * np.array(ytp) + by)
xres = np.array(vals) - (kx * np.array(xtp) + bx)
X = lambda px: kx * px + bx
Y = lambda py: ky * py + by

# --- markers
blue = (((a[:, :, 2] - a[:, :, 0]) > 60) & (a[:, :, 2] > 120)).astype(np.float32)
blue[:, :ax_col + 3] = 0
blue[ax_row - 2:, :] = 0
T = np.zeros((13, 13), np.float32); T[5:8, :] = 1; T[:, 5:8] = 1
C = np.zeros((13, 13), np.float32); C[:4, :4] = 1; C[:4, 9:] = 1; C[9:, :4] = 1; C[9:, 9:] = 1
# pixels of the two reference lines are 'unknown' (the lines are drawn over the markers)
lines_px = ((np.abs(a - 153).max(2) < 30) | ((a[:, :, 0] > 200) & (a[:, :, 2] < 120))).astype(np.float32)
unk = cv2.matchTemplate(lines_px, T, cv2.TM_CCORR)
res = cv2.matchTemplate(blue, T, cv2.TM_CCORR) / np.maximum(T.sum() - unk, 1)
cor = cv2.matchTemplate(blue, C, cv2.TM_CCORR) / C.sum()
good = ((res > 0.8) & (cor < 0.15) & (unk < 0.5 * T.sum())).astype(np.uint8)
n, lab, st, cen = cv2.connectedComponentsWithStats(good, 8)
markers = []
for i in range(1, n):
    m = lab == i
    ys, xs = np.where(m)
    wts = res[ys, xs]
    cx = (xs * wts).sum() / wts.sum() + 6.0          # template origin -> centre of the 13x13 cross
    cy = (ys * wts).sum() / wts.sum() + 6.0
    markers.append((X(cx), Y(cy), cx, cy))

# --- envelopes (whole point cloud)
env = []
for c in range(ax_col + 3, W):
    rows = np.where(blue[:, c] > 0)[0]
    if len(rows):
        env.append((X(c), Y(rows.min()), Y(rows.max())))

# --- reference lines
def fitline(mask):
    ys, xs = np.where(mask)
    p = np.polyfit(xs, ys, 1)
    keep = np.abs(ys - np.polyval(p, xs)) < 4
    p = np.polyfit(xs[keep], ys[keep], 1)
    # convert to data: y_data = s*x_data + c
    x1, x2 = 0.0, 100.0
    px1, px2 = (x1 - bx) / kx, (x2 - bx) / kx
    return Y(np.polyval(p, px1)), Y(np.polyval(p, px2)), keep.sum()

orange = (a[:, :, 0] > 200) & (a[:, :, 1] > 130) & (a[:, :, 1] < 190) & (a[:, :, 2] < 90)
orange[:300, :800] = False                               # legend sample 'Five synapses'
grey = (np.abs(a - 153).max(2) < 8)
grey[1150:, 1600:] = False                               # legend sample
grey[:, :ax_col + 3] = False
grey[ax_row - 2:, :] = False
lo = fitline(orange)
lg = fitline(grey)

with open(HERE / "fig16.csv", "w", newline="") as f:
    f.write("# Figure 16 (p. 34 of elife-57443-v4.pdf): 'Change in synapse count for paths during successive refinement';\n")
    f.write("#   x = 'Synapse count at 30% completeness', y = 'Synapse count at 50% completeness' (both 0-100, linear).\n")
    f.write("# Provenance: tier 3, digitized from the embedded raster image (2207 x 1486 px) by fig16_extract.py.\n")
    f.write("# Tier 1 not available: the caption names 'Figure 16-source data 1' (eLife online), not in papers/scheffer2020/.\n")
    f.write(f"# Calibration: tick marks 0..100; x {kx**-1:.3f} px/count (residuals {np.round(xres, 3).tolist()}), y {-ky**-1:.3f} px/count (residuals {np.round(yres, 3).tolist()}).\n")
    f.write("# The ~40,000 markers cannot be separated in the dense band; see the kinds below. Marker centres do not fall on integer\n")
    f.write("#   counts (the plotted values seem to be jittered or non-integer), so they are given as read.\n")
    f.write("# kind=marker: whole, unobstructed '+' markers only (a subset: mostly the outliers above the band and sparse points\n")
    f.write("#   at high counts); centre +-0.05 counts. kind=envelope_upper/_lower: top/bottom blue ink in each pixel column\n")
    f.write("#   (ink edge, i.e. marker centre +- half a marker: +-0.51 counts in y); x at the column centre.\n")
    f.write("# kind=line_orange ('Additional synapses: Five synapses') and kind=line_grey ('Fewer synapses: Five synapses'):\n")
    f.write("#   least-squares fits to the line pixels, given by their y at x = 0 and x = 100.\n")
    w = csv.writer(f)
    w.writerow(["kind", "x", "y"])
    for x, y, _, _ in sorted(markers):
        w.writerow(["marker", round(x, 3), round(y, 3)])
    for x, yu, yl in env:
        w.writerow(["envelope_upper", round(x, 3), round(yu, 3)])
    for x, yu, yl in env:
        w.writerow(["envelope_lower", round(x, 3), round(yl, 3)])
    w.writerow(["line_orange", 0, round(lo[0], 3)]); w.writerow(["line_orange", 100, round(lo[1], 3)])
    w.writerow(["line_grey", 0, round(lg[0], 3)]); w.writerow(["line_grey", 100, round(lg[1], 3)])

# overlay
ov = a.astype(np.uint8).copy()
for _, _, cx, cy in markers:
    cv2.circle(ov, (int(round(cx)), int(round(cy))), 9, (255, 0, 0), 2)
for x, yu, yl in env:
    px = int(round((x - bx) / kx))
    for yy in (yu, yl):
        ov[int(round((yy - by) / ky)), px] = (255, 0, 255)
(HERE.parent / "work").mkdir(exist_ok=True)
cv2.imwrite(str(HERE.parent / "work" / "fig16_overlay.png"), cv2.cvtColor(ov, cv2.COLOR_RGB2BGR))
print("markers", len(markers), "orange y(0), y(100)", lo, "grey", lg)
below = [(round(x, 2), round(y, 2)) for x, y, _, _ in markers if y < x - 5]
print("markers below y=x-5:", below)
print("markers at x<1 with y>10:", [(round(x, 2), round(y, 2)) for x, y, _, _ in markers if x < 1 and y > 10])
