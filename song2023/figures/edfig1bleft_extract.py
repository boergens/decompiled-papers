"""Extended Data Fig. 1b, left plot (Os intensity profiles across a 2-mm sample: uCT, SEM, EDS) -> edfig1bleft.csv

Tier 1 for y: Edmond data/Extended Data Fig.1/Extended Data Fig. 1a-b/EDX/Suppl_Fig1b.mat.mat, as plotted by the
authors' supp_fig1_EDS.m: plot(uct(:,1), uct2n); plot(sem(:,1), sem2n); plot(439*x2/max(x2), y3n).
uct2n and sem2n are z-scored grey-value profiles (index 0..411 and 0..446); y3n is the EDS line scan that the
authors traced from an image (mask 'bw' -> x2, column positions) and normalized.
The x values in the .mat are sample indices (pixels), not um; the printed axis is 'Location (um)'. The conversion
(um per index, offset) is not in the source data, so it is fitted here for each series to the printed traces
(raster, 300 ppi, embedded image of PDF p. 12; x axis calibrated on the 200-um tick marks, y on the unit ticks).
The printed y values are then checked against the source values (same axis calibration, no free parameter).
Also digitized: the x positions of the four dashed vertical lines (tier 3).
Run: python3 -I edfig1bleft_extract.py
"""
import os
import sys

import cv2
import numpy as np
import scipy.io as sio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, SRC, WORK, fit, hue_mask, overlay, page_image, write_csv

a = page_image(12)
# axes (embedded-image pixels): y axis line col 1064-1067, x axis row 342-344
XT = [1108.0, 1151.5, 1195.0, 1239.0, 1282.0, 1326.0, 1370.0, 1414.0]   # ticks 200..1600 um (below the axis line)
YT = [74.0, 120.0, 166.0, 212.0, 257.5, 304.0]                           # ticks 3, 2, 1, 0, -1, -2 (labels 2, 0, -2)
px2x, x2px, rx = fit(XT, np.arange(200, 1601, 200))
py2y, y2py, ry = fit(YT, [3, 2, 1, 0, -1, -2])
X0, X1, Y0, Y1 = 1068, 1460, 40, 341

m = sio.loadmat(os.path.join(SRC, "Extended Data Fig.1/Extended Data Fig. 1a-b/EDX/Suppl_Fig1b.mat.mat"), squeeze_me=True)
# NB: the printed red curve (legend 'uCT') is the .mat variable sem2n, and the printed blue curve (legend 'SEM') is
# uct2n: the shapes match only this way round (MATLAB drew uct2n first in default blue; see README).
series = {
    "uCT (red; .mat sem2n)": (m["sem"][:, 0], m["sem2n"], (170, 8)),
    "SEM (blue; .mat uct2n)": (m["uct"][:, 0], m["uct2n"], (95, 115)),
    "EDS (green; .mat y3n)": (439 * m["x2"] / m["x2"].max(), m["y3n"], (55, 85)),
}
sub = a[Y0:Y1, X0:X1]
rows, ov, notes = [], [], []
for name, (xi, yv, (h0, h1)) in series.items():
    mask = hue_mask(sub, h0, h1, smin=90, vmin=80)
    # distance (px) from every pixel to the nearest pixel of this series' colour
    dist = cv2.distanceTransform((~mask).astype(np.uint8), cv2.DIST_L2, 3)
    ys = np.clip(np.round(y2py(yv) - Y0).astype(int), 0, sub.shape[0] - 1)
    best = None
    for k in np.arange(3.4, 5.0, 0.005):            # um per index
        for off in np.arange(-250, 101, 1.0):
            xs = np.round(x2px(k * xi + off) - X0).astype(int)
            ok = (xs >= 0) & (xs < sub.shape[1])
            if ok.sum() < 0.8 * len(xs):
                continue
            # score: fraction of all source points that land within 2 px of the printed trace of the same colour
            score = np.sum(dist[ys[ok], xs[ok]] <= 2) / len(xs)
            if best is None or score > best[0]:
                best = (score, k, off)
    score, k, off = best
    x_um = k * xi + off
    notes.append(f"{name}: x_um = {k:.3f} * index {off:+.0f} um (fit), {100 * score:.0f}% of points within 2 px of the printed trace")
    for i, (x, y, idx) in enumerate(zip(x_um, yv, xi)):
        rows.append([name, f"{idx:g}", f"{x:.1f}", f"{y:.5f}"])
        ov.append((x2px(x), y2py(y)))
# dashed vertical lines: columns in the plot where dark pixels form a dashed vertical pattern
dark = (sub.max(2) < 110) & ((sub.max(2) - sub.min(2)) < 40)
colsum = dark.sum(0)
cand = [c for c in range(5, sub.shape[1] - 5) if colsum[c] > 0.25 * sub.shape[0] and colsum[c] < 0.8 * sub.shape[0]]
groups = []
for c in cand:
    if groups and c - groups[-1][-1] <= 2:
        groups[-1].append(c)
    else:
        groups.append([c])
dash_x = [px2x(np.mean(g) + X0) for g in groups]
for x in dash_x:
    rows.append(["dashed_line", "", f"{x:.0f}", ""])
write_csv(os.path.join(HERE, "edfig1bleft.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 1b (left plot): Os intensity (a.u.) along a line across a 2-mm",
    "  sample stained with the 1-mm (Hua) protocol, from uCT (red), SEM (blue) and EDS (green); x = Location (um).",
    "Provenance: y = tier 1, source data (Edmond 10.17617/3.RG58DU, Extended Data Fig. 1a-b/EDX/Suppl_Fig1b.mat.mat:",
    "  uct2n, sem2n, y3n; z-scored profiles, unitless). x: the .mat holds only sample indices (uct(:,1), sem(:,1),",
    "  439*x2/max(x2) as in the authors' supp_fig1_EDS.m); x_um is a scale+offset fitted per series to the printed",
    "  traces (tier 3 calibration, raster p. 12, x axis fitted on 8 ticks 200..1600 um, max residual %.1f um;" % rx,
    "  y on 6 ticks, max residual %.3f). Uncertainty of x_um about +-10 um (+-2 px)." % ry,
] + notes + [
    "The first point of the red and blue series (index 0: sem2n = 4.01, uct2n = 2.11) is not visible in the printed",
    "  figure (the printed traces start at about x = 40 um); everything else is.",
    "dashed_line rows: x of the four dashed vertical lines in the plot (tier 3, digitized, +-5 um).",
    "Columns: series; index = x value stored in the .mat; x_um; y = Os intensity (a.u.) from the .mat.",
], ["series", "index", "x_um", "y"], rows)
overlay(a, ov, os.path.join(WORK, "edfig1bleft_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig1bleft_overlay_full.png")).crop((1000, 30, 1470, 400)).save(
    os.path.join(WORK, "edfig1bleft_overlay.png"))
print(notes, dash_x)
