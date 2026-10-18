"""Digitize Fig. 4b of Kubota et al. 2018 (main PDF p. 6): 'Absorption spectra (coated side)' of the three tapes.

Source: the embedded 300 ppi raster image of the panel; tick labels are PDF text.
    python3 -I fig4b_extract.py  -> fig4b.csv (+ ../work/fig4b_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from kubota_main_common import Img, calib, trace_three_series, WORK  # noqa: E402
from digitize_common import tick_positions, tick_positions_v, write_csv, overlay  # noqa: E402

BB = (107.5, 182.9, 225.3, 264.5)
im = Img(6, BB)
k = (im.g < 110) & (np.ptp(im.a.astype(int), axis=2) < 60)
XAX, YAX = (331, 332), (8, 9)
xt = tick_positions(k, XAX, +1, 4, YAX[1] + 2, k.shape[1])
yt = tick_positions_v(k, YAX, -1, 4, 0, XAX[0]) + [(XAX[0] + XAX[1]) / 2]     # 0 = the axis line
labs = im.labels((BB[0] - 30, BB[1] - 5, BB[2] + 5, BB[3] + 12))
fx, rx, sx, xp, xv = calib(xt, [l for l in labs if l[2] > XAX[1]], 1)
fy, ry, sy, yp, yv = calib(yt, [l for l in labs if l[1] < 0], 2)
EXCLUDE = ()           # legend box (pixels), blanked before tracing
series, pts = trace_three_series(im, YAX[1] + 3, k.shape[1], XAX, exclude=EXCLUDE)
overlay(im.a, pts, os.path.join(WORK, "fig4b_overlay.png"), colour=(0, 255, 0))
rows = [(s, float(fx(c)), float(fy(ym)), float(fy(yu)), float(fy(yl)), fl)
        for s, r in series.items() for c, ym, yu, yl, fl in r]
write_csv(os.path.join(HERE, "fig4b.csv"), [
    "Kubota et al. 2018 Nat Commun 9:437, Fig. 4b: 'Absorption spectra (coated side)' (main PDF p. 6). Series per the colour key",
    "  of Fig. 4c: red = CNT-PET, blue = Kapton, black = cc-Kapton.",
    "Columns: series; wavelength_nm (x axis 'Wavelength (nm)'); reflection_pct_mid = y axis 'Reflection (%)'; _upper/_lower = top and",
    "  bottom of the plotted line within this pixel column. One row per pixel column where the series' colour is",
    "  visible; columns where another series is drawn on top are missing.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector plot paths in the PDF) by",
    "  fig4b_extract.py: colour masks, per-column envelope of the ~5 px line (half width 2 px). Axes calibrated on",
    f"  the image's tick marks paired with the PDF-text labels: x on {len(xp)} ticks ({min(xv):g}-{max(xv):g} nm), max",
    f"  residual {rx:.2f} nm; y on {len(yp)} ticks ({min(yv):g}-{max(yv):g}; 0 = the axis line), max residual {ry:.2f}.",
    f"Uncertainty: about +-{2 * abs(sy):.2f} percentage points in y and +-{2 * abs(sx):.1f} nm in x (2 px). Where the",
    "  black line runs along the x-axis line its centre is taken as its top edge + 2 px, or, where it only thickens",
    "  the axis line (value ~0), as the axis line itself (flags).",
], ["series", "wavelength_nm", "reflection_pct_mid", "reflection_pct_upper", "reflection_pct_lower", "flag"], rows,
    fmt=["{}", "{:.1f}", "{:.2f}", "{:.2f}", "{:.2f}", "{}"])
print(len(rows), "rows; x", xp, xv, rx, "; y", yp, yv, ry)
for s, r in series.items():
    v = [float(fy(q[1])) for q in r]
    print(s, len(r), "x", round(float(fx(r[0][0])), 1), round(float(fx(r[-1][0])), 1), "y first/last", round(v[0], 2), round(v[-1], 2), "min/max", round(min(v), 2), round(max(v), 2))
