"""Digitize Figure 3d of He et al. 2018 (Sci Rep 8:12985), main PDF p.6: line profiles.

Source: the embedded raster image of Figure 3 (1650 x 2205 px, ~300 ppi), panel d at its upper right.
    python3 -I fig3d_extract.py   -> fig3d.csv (+ ../work/fig3d_overlay.png for checking)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/admin/ephemeral/oct_17_papers/he2018/tools")
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, trace_envelope, write_csv, overlay  # noqa: E402

PDF = os.path.join(HERE, "../source/he2018.pdf")
a = embedded_image(PDF, 6)
assert a.shape == (2205, 1650, 3), a.shape
ai = a.astype(int)
R, G, B = ai[:, :, 0], ai[:, :, 1], ai[:, :, 2]

# Frame and gridlines, located with row/column sums of dark (frame) and light-grey (grid) pixels:
#   frame top row 441 (y=6), bottom row 669.5 (y=-2); gridline rows 498 (4), 555 (2), 612 (0, under the data);
#   frame columns 1095 (x=-0.5) and 1608 (x=4.5); gridline columns 1197.5 (0.5), 1300 (1.5), 1402.5 (2.5), 1505 (3.5).
xpix = [1095, 1197.5, 1300, 1402.5, 1505, 1608]
xval = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
ypix = [441, 498, 555, 669.5]
yval = [6, 4, 2, -2]
fx, rx, sx = fit_axis(xpix, xval)
fy, ry, sy = fit_axis(ypix, yval)

red = (R > 140) & (G < 100) & (B < 100) & (R - G > 90)
green = (G - R > 45) & (G - B > 20) & (G < 210)
X0, X1, Y0, Y1 = 1097, 1607, 443, 668

rows, pts, ov = [], [], a[400:720, 1050:1650].copy()
for name, mask, col in (("top sub-slice", green, (255, 0, 255)), ("bottom sub-slice", red, (0, 0, 255))):
    env = trace_envelope(mask, X0, X1, Y0, Y1, half_width=1, min_px=2)
    for c, ym, yu, yl in env:
        if ym != ym:
            continue
        rows.append((name, float(fx(c)), float(fy(ym)), float(fy(yl)), float(fy(yu))))
        pts += [(c, yu), (c, yl)]
    # draw this series' points (magenta: top sub-slice, blue: bottom sub-slice) onto the crop
    for x, y in pts:
        xi, yi = int(round(x)) - 1050, int(round(y)) - 400
        ov[yi, xi] = col
    pts = []
overlay(ov, [], os.path.join(HERE, "../work/fig3d_overlay.png"))

write_csv(os.path.join(HERE, "fig3d.csv"), [
    "He et al. 2018 Sci Rep 8:12985, Figure 3d: line profiles of the features in the top and bottom sub-slices",
    "  (along the dashed lines in Fig. 3c). Series names as in the legend: 'top sub-slice' (green), 'bottom sub-slice' (red).",
    "Columns: series; distance_um = x, Distance (um); lead_atoms_1e3_per_voxel = y, Number of lead atoms (10^3 /voxel),",
    "  the middle of the drawn line in this pixel column; y_low / y_high = bottom and top of the drawn line in the",
    "  column (the profile is noisy, so a single pixel column often spans a vertical range of values).",
    "Provenance: tier 3, digitized from the embedded raster image (no vector data in the PDF) by fig3d_extract.py.",
    f"  x calibrated on the frame (-0.5, 4.5) and 4 vertical gridlines (0.5-3.5), max residual {rx:.4f} um;",
    f"  y on the frame (6, -2) and gridlines 4 and 2, max residual {ry:.4f}.",
    f"Uncertainty: about +-{abs(sx):.3f} um in x and +-{2 * abs(sy):.2f} (10^3/voxel) in y (1-2 px), plus the 3 px line width.",
    "One row per pixel column of the source image per series. Where the two lines cross or overlap (mostly near 0 at",
    "  0-0.5 um and 2.9-4.3 um) the line drawn on top hides the other; there the hidden series has gaps or follows the",
    "  visible edge of the other line.",
], ["series", "distance_um", "lead_atoms_1e3_per_voxel", "y_low", "y_high"], rows)
print("wrote fig3d.csv", len(rows), "rows; residuals", rx, ry)
