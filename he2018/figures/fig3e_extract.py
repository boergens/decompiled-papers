"""Digitize Figure 3e of He et al. 2018 (Sci Rep 8:12985), main PDF p.6: six voxel-value histograms.

Source: the embedded raster image of Figure 3 (1650 x 2205 px, ~300 ppi), panel e in its lower half.
Each of the six sub-plots has its own light-grey frame and gridlines (x: -10, -5, 0, 5, 10; y: 0, 50, ...,
200), found with row/column sums of light-grey pixels and listed in SUB below. Markers (filled dots,
~9 px across) are found as maxima of the distance transform of each colour mask (the 3 px connecting
lines have a distance of at most ~1.5 px, the dots ~4.5 px), so touching dots are still separated.
    python3 -I fig3e_extract.py   -> fig3e.csv (+ ../work/fig3e_overlay.png for checking)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/admin/ephemeral/oct_17_papers/he2018/tools")
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, write_csv, overlay  # noqa: E402

PDF = os.path.join(HERE, "../source/he2018.pdf")
a = embedded_image(PDF, 6)
assert a.shape == (2205, 1650, 3), a.shape
ai = a.astype(int)
R, G, B = ai[:, :, 0], ai[:, :, 1], ai[:, :, 2]
red = ((R > 150) & (G < 110) & (B < 110) & (R - G > 80)).astype(np.uint8)
green = ((G - R > 45) & (G - B > 20) & (G < 220)).astype(np.uint8)

# sub-plot: (title, x gridline columns for -10,-5,0,5,10, y gridline rows for 200,150,100,50,0)
SUB = [
    ("cuboid 1 top sub-slice", [224, 340.5, 455, 571.5, 686.5], [1047.5, 1082.5, 1115.5, 1150.5, 1183.5]),
    ("cuboid 1 bottom sub-slice", [880, 996.5, 1112.5, 1228.5, 1344], [1047.5, 1083.5, 1119.5, 1155.5, 1192]),
    ("cuboid 2 top sub-slice", [213.5, 332.5, 451.5, 569.5, 689.5], [1457.5, 1493.5, 1529.5, 1566, 1602.5]),
    ("cuboid 2 bottom sub-slice", [869.5, 988.5, 1106.5, 1225.5, 1344], [1457.5, 1493.5, 1529.5, 1566, 1602.5]),
    ("cuboid 3 top sub-slice", [213.5, 332.5, 451.5, 569.5, 689.5], [1866.5, 1903, 1939.5, 1976.5, 2012.5]),
    ("cuboid 3 bottom sub-slice", [869.5, 988.5, 1106.5, 1225.5, 1344], [1866.5, 1903, 1939.5, 1976.5, 2012.5]),
]
XV = [-10, -5, 0, 5, 10]
YV = [200, 150, 100, 50, 0]
MIN_DIST = 3.0     # distance-transform value that only dot interiors reach
NMS = 3            # half-size of the local-maximum window (px); dot centres are >= ~6 px apart


DISK_R = 5          # dot radius in px (distance-transform maximum at dot centres is ~5)


def peaks(mask, x0, x1, y0, y1):
    """(x, y, d) of distance-transform maxima >= MIN_DIST: dot centres (d ~5 for a fully visible dot)."""
    m = np.zeros_like(mask)
    m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))   # fill JPEG speckle
    d = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    mx = cv2.dilate(d, np.ones((2 * NMS + 1, 2 * NMS + 1), np.uint8))
    pk = (d >= MIN_DIST) & (d >= mx - 1e-6)
    n, lab, st, cen = cv2.connectedComponentsWithStats(pk.astype(np.uint8))
    return [(cen[i][0], cen[i][1], float(d[int(round(cen[i][1])), int(round(cen[i][0]))])) for i in range(1, n)]


def fit_grid(xs):
    """Regular bin spacing: every clean series in this figure has equally spaced dots (Excel histogram
    bins). Find the LARGEST spacing dx (and offset x0) for which the most dot centres lie within 1.5 px of
    x0 + k*dx (any integer fraction of the true spacing fits as well, so the largest one is taken), then
    refine x0, dx by least squares on the dots that fit."""
    xs = np.sort(np.asarray(xs, float))
    cands = []
    for dx in np.arange(6.0, 30.0, 0.02):
        k = np.round((xs - xs[0]) / dx)
        if len(set(k)) < len(k):          # two dots in one bin: spacing too large
            continue
        x0 = np.median(xs - k * dx)
        n = int((np.abs(xs - (x0 + k * dx)) < 1.5).sum())
        cands.append((n, dx, x0))
    nmax = max(c[0] for c in cands)
    n, dx, x0 = max((c for c in cands if c[0] == nmax), key=lambda c: c[1])
    k = np.round((xs - x0) / dx)
    ok = np.abs(xs - (x0 + k * dx)) < 1.5
    dx, x0 = np.polyfit(k[ok], xs[ok], 1)
    return x0, dx


yy, xx = np.mgrid[-DISK_R:DISK_R + 1, -DISK_R:DISK_R + 1]
DISK = (xx ** 2 + yy ** 2) <= DISK_R ** 2


def recover(mask, other, cx, y0, y1):
    """A dot partly hidden under the other series: at column cx (+-1 px), the disk position that holds the
    most pixels of this colour while being covered by coloured pixels (this or the other series) for >= 70 %
    (the colour masks miss the anti-aliased rim of each dot, so a fully covered disk scores ~0.8-0.95)."""
    best = (0, None, None)
    for x in (cx - 1, cx, cx + 1):
        for y in range(y0, y1):
            win = (slice(y - DISK_R, y + DISK_R + 1), slice(x - DISK_R, x + DISK_R + 1))
            own = mask[win][DISK].sum()
            cov = (mask[win] | other[win])[DISK].mean()
            if cov >= 0.7 and own > best[0]:
                best = (own, x, y)
    return best


rows, ov = [], a.copy()
summary = []
for title, xs, ys in SUB:
    fx, rx, sx = fit_axis(xs, XV)
    fy, ry, sy = fit_axis(ys, YV)
    x0, x1 = int(xs[0]) - 12, int(xs[-1]) + 12
    y0, y1 = int(ys[0]) - 20, int(ys[-1]) + 12
    for series, mask, other, col in (("red", red, green, (0, 0, 255)), ("green", green, red, (255, 0, 255))):
        pk = peaks(mask, x0, x1, y0, y1)
        strong = [p for p in pk if p[2] >= 4.5]
        gx0, gdx = fit_grid([p[0] for p in strong] if len(strong) >= 4 else [p[0] for p in pk])
        # extent of the series: leftmost/rightmost pixel of its colour inside the plot box
        cols = np.where(mask[y0:y1, x0:x1].any(0))[0] + x0
        # the end dots are the extremes of the series; their centres lie one dot radius inside its extent
        first, last = cols.min() + DISK_R - 0.5, cols.max() - DISK_R + 0.5
        nd = int(round((last - first) / gdx)) + 1
        grid = np.linspace(first, last, nd)
        gdx = (last - first) / (nd - 1)
        dev = [min(abs(p[0] - grid)) for p in strong]
        if dev and max(dev) > 2:
            print("  WARNING", title, series, "strong dot off the grid by", round(max(dev), 1), "px")
        n_vis = n_part = n_hid = 0
        for gxk in grid:
            near = [p for p in pk if abs(p[0] - gxk) < 2.5]
            if near:
                p = max(near, key=lambda q: q[2])
                cx, cy = p[0], p[1]
                flag = "visible" if p[2] >= 4.5 else "partly hidden"
            else:
                own, bx, by = recover(mask.astype(bool), other.astype(bool), int(round(gxk)), y0 + DISK_R, y1 - DISK_R)
                if own >= 6:
                    cx, cy, flag = bx, by, "partly hidden"
                else:
                    cx, cy, flag = gxk, float("nan"), "hidden"
            n_vis += flag == "visible"
            n_part += flag == "partly hidden"
            n_hid += flag == "hidden"
            rows.append((title, series, float(fx(cx)), float(fy(cy)) if cy == cy else float("nan"), flag, rx, ry))
            if cy == cy:
                cv2.circle(ov, (int(round(cx)), int(round(cy))), 2, col if flag == "visible" else ((0, 255, 255) if series == "red" else (255, 255, 0)), -1)
        dropped = [round(p[0]) for p in pk if min(abs(p[0] - grid)) >= 2.5]
        summary.append(f"{title}, {series}: {nd} dots ({n_vis} visible, {n_part} partly hidden, {n_hid} hidden);"
                       f" bin spacing {gdx * abs(sx):.3f}")
        print(summary[-1], "dropped off-grid peaks at px", dropped)
overlay(ov[1000:2060, 150:1400], [], os.path.join(HERE, "../work/fig3e_overlay.png"))

write_csv(os.path.join(HERE, "fig3e.csv"), [
    "He et al. 2018 Sci Rep 8:12985, Figure 3e: histograms of the computed number of lead atoms per voxel for",
    "  cuboids 1 to 3 and their backgrounds in the top and bottom sub-slice (fluence 1000 e/pixel). Six sub-plots,",
    "  named by their printed titles (column 'subplot'). Each has two series, drawn as dots joined by lines:",
    "  'red' and 'green'. The legend above each sub-plot shows the red series next to a thumbnail with a red box",
    "  on a cuboid and the green series next to a thumbnail with a green box on the background (caption: 'cuboids",
    "  1 to 3 and their corresponding backgrounds'); the series have no other names in the figure.",
    "Columns: x_1e3_atoms_per_voxel = Number of lead atoms (10^3 /voxel), the shared x-axis title; frequency = the",
    "  shared y-axis title 'Frequency' (counts of voxels); one row per plotted dot (marker centre).",
    "  x_fit_residual / y_fit_residual = max residual of the axis fit on the gridlines of that sub-plot.",
    "Provenance: tier 3, digitized from the embedded raster image (no vector data in the PDF) by fig3e_extract.py:",
    "  axes calibrated on the 5 vertical (-10..10) and 5 horizontal (0..200) gridlines of each sub-plot; dot centres",
    "  from maxima of the distance transform of red/green colour masks.",
    "Uncertainty: about +-0.1 (10^3 atoms/voxel) in x and +-2 in frequency (1 px is ~0.043 in x and ~1.4 in y;",
    "  the gridlines in the source are unevenly spaced by up to 2 px). Dots hidden under a dot of the other colour",
    "  can be missing (see README); the overlay ../work/fig3e_overlay.png was checked dot by dot.",
], ["subplot", "series", "x_1e3_atoms_per_voxel", "frequency", "flag", "x_fit_residual", "y_fit_residual"], rows)
print("wrote fig3e.csv", len(rows), "rows")
