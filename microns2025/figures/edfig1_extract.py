#!/usr/bin/env python3
"""Extended Data Fig. 1 (p. 23): locations of the synapse test volumes in subvolume 65, coloured by F1 score. The whole
figure (two plotly scatter plots with colour bars) is one embedded raster (3989 x 5433 px, 600 ppi). -> edfig1a.csv
(top plot: y vs x, the caption's coronal view (a)) and edfig1b.csv (bottom plot: z vs x, the top view (b)).
The panels carry no printed letters; the mapping top = (a), bottom = (b) follows the caption's description of the axes.

Axes: white plotly grid lines found in the image: x 200 ... 1600 um at columns 407.5 ... 3203.5 (both plots);
top y 1200 ... 200 um at rows 374 ... 2280.5; bottom z 1100 ... 600 um at rows 3163.5 ... 5077.5.
Markers: square markers (~31 x 31 px) found as connected components of saturated pixels inside each plot frame;
centre = component centroid. Components larger than 1.5 marker areas are flagged 'overlap' (two or more touching
markers; centroid of the union). F1 from the marker colour: nearest colour on the plot's colour bar (rows 276-2242 /
3181-5146, value 1 at the top end, 0.5 at the bottom end, the printed end labels)."""
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(mc.PDF), 23).astype(float)
sat = a.max(2) - a.min(2)
XG = [407.5, 807.5, 1206.5, 1606, 2005, 2405, 2804.5, 3203.5]
X = mc.LinAxis(list(zip(XG, range(200, 1601, 200))))
PLOTS = {
    "a": dict(rows=(215, 2273), Y=mc.LinAxis(list(zip([374, 755.5, 1136, 1518.5, 1899.5, 2280.5], [1200, 1000, 800, 600, 400, 200]))),
              cbar=(276, 2242), yname="y_um", title="top plot, y (um) vs x (um)"),
    "b": dict(rows=(3118, 5091), Y=mc.LinAxis(list(zip([3163.5, 3547, 3929.5, 4311.5, 4694.5, 5077.5], [1100, 1000, 900, 800, 700, 600]))),
              cbar=(3181, 5146), yname="z_um", title="bottom plot, z (um) vs x (um)"),
}
qa = a.copy()
for p, d in PLOTS.items():
    r0, r1 = d["rows"]
    c0, c1 = d["cbar"]
    lut = a[c0 + 3:c1 - 2, 3740:3865].mean(1)
    lv = 1 - 0.5 * (np.arange(c0 + 3, c1 - 2) - c0) / (c1 - c0)
    m = np.zeros(sat.shape, bool)
    m[r0:r1, 420:3600] = sat[r0:r1, 420:3600] > 40
    lab, n = ndimage.label(m)
    idx = range(1, n + 1)
    sizes = ndimage.sum(m, lab, idx)
    cms = ndimage.center_of_mass(m, lab, idx)
    single = np.median([s for s in sizes if s > 300])
    BG = np.array([243, 241, 244])
    cand = [(s_, k) for s_, k in zip(sizes, idx) if s_ >= 300]
    meds = np.array([np.median(a[lab == k], 0) for s_, k in cand])
    best = None
    for alpha in np.arange(0.30, 1.001, 0.01):
        bl = alpha * lut + (1 - alpha) * BG
        dd = np.sqrt(((meds[:, None, :] - bl[None]) ** 2).sum(2)).min(1)
        if best is None or np.median(dd) < best[0]:
            best = (np.median(dd), alpha)
    alpha = best[1]
    lutb = alpha * lut + (1 - alpha) * BG
    rows = []
    for s, (cy, cx), k in zip(sizes, cms, idx):
        if s < 300:
            continue
        pix = a[lab == k]
        col = np.median(pix, 0)
        dist = np.sqrt(((lutb - col) ** 2).sum(1))
        i = int(dist.argmin())
        flag = "overlap" if s > 1.5 * single else ""
        rows.append([f"{X(cx + 0.5):.1f}", f"{d['Y'](cy + 0.5):.1f}", f"{lv[i]:.3f}", f"{dist[i]:.1f}", int(s), flag,
                     "%02x%02x%02x" % tuple(int(v) for v in col)])
        qa[int(cy) - 3:int(cy) + 4, int(cx) - 3:int(cx) + 4] = (0, 255, 0)
    rows.sort(key=lambda r: float(r[0]))
    mc.write_csv(Path(__file__).with_name(f"edfig1{p}.csv"), [
        f"Extended Data Fig. 1{p} (p. 23 of microns2025.pdf): {d['title']}; title 'Location of Synapse Test Volumes';",
        "black rectangle 'Minnie65 Volume Bounds'; colour bar 'F1' 0.5-1.",
        "Provenance: tier 3, digitized from the embedded raster (1 px = 0.5 um in x; marker centres +-1 px = +-0.5 um).",
        f"F1 from colour: resolution ~0.0003 per colour-bar row, but neighbouring F1 values have similar colours: +-0.01.",
        f"Columns: x_um; {d['yname']}; F1; colour_dist (RGB distance to the colour bar); area_px (component area, single marker ~{single:.0f});",
        "flag (overlap = touching markers merged); rgb (median marker colour).",
        f"The markers are drawn semi-transparent over the grey plot background (243,241,244); the marker opacity was fitted",
        f"as {alpha:.2f} (median colour distance {best[0]:.1f}) and the colour bar blended accordingly before matching.",
        X.describe("x (px)"), d["Y"].describe("y (px)"),
    ], ["x_um", d["yname"], "F1", "colour_dist", "area_px", "flag", "rgb"], rows)
from PIL import Image  # noqa: E402
Image.fromarray(qa.astype(np.uint8)).resize((997, 1358)).save(mc.K / "work" / "overlay_edfig1.png")
