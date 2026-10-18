"""Digitize Fig 1 of Lee et al. 2018 (PLoS ONE 13:e0206172) -> fig1.csv (tier 3).

Scatter plot, x = year of publication (linear), y = volume of neural tissue studied [mm^3] (log).
Reads the embedded 300 ppi raster image (xref 49, p. 3) of source/lee2018_lasso.pdf, finds the axis
frame and tick marks, fits pixel -> data maps on the ticks, finds the 13 filled circle markers
(connected components) and the dashed horizontal line, and labels the markers A-M.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(ROOT / "source/lee2018_lasso.pdf"), 3)
g = dc.gray(a)
d = g < 200
# frame: left col 178-180, right col 2048-2050, top row 28-30, bottom row 2009-2011 (found with frame_lines)
xt = dc.tick_positions(d, (2009, 2011), -1, 20, 175, 2055)          # 12 major ticks 1970..2025
yt = dc.tick_positions_v(d, (178, 180), +1, 20, 20, 2020)           # 8 decade ticks 10^0..10^-7
assert len(xt) == 12 and len(yt) == 8, (xt, yt)
fx, rx, _ = dc.fit_axis(xt, np.arange(1970, 2026, 5))
fy, ry, sy = dc.fit_axis(yt, [10.0 ** -k for k in range(8)], log=True)

dark = (g < 128).astype(np.uint8)
dark[:, :190] = 0; dark[:, 2040:] = 0; dark[:40] = 0; dark[2000:] = 0
n, lab, st, cen = cv2.connectedComponentsWithStats(dark, 8)
pts = []
for i in range(1, n):
    x, y, w, h, ar = st[i]
    # filled circles: ~20 x 21 px, area ~325, fill ratio ~0.77 (letters/brackets of the labels are < 0.6)
    if 250 < ar < 450 and 0.8 < w / h < 1.25 and ar / (w * h) > 0.7:
        pts.append(tuple(cen[i]))
assert len(pts) == 13, pts
# label order: by x; the three markers at the same x (2013) are I, J, K from top to bottom
pts.sort(key=lambda p: (round(p[0] / 10), p[1]))
labels = list("ABCDEFGHIJKLM")
legend = {
    "A": "Spacek, J. & Lieberman, A. R., 1974",
    "B": "White, J. G., Southgate, E., Thomson, J. N. & Brenner, S. 1986",
    "C": "Hamos, J. E., Van Horn, S. C., Raczkowski, D., Sherman, S. M., 1987",
    "D": "Hall, D. H., Russell, R. L., 1991",
    "E": "Shepherd, G. N. & Harris, K. M., 1998",
    "F": "Hoffpauir, B. K., Pope, B., & Spirou, G., 2007",
    "G": "Takemura, S., Lu, Z. & Meinerzhagen, I. A., 2008",
    "H": "Bock, D. D., et. al., 2011",
    "I": "Sommer, R. J., Bumbarger, D. J., Riebesell, M. & Ro, C., 2013",
    "J": "Takemura, S., et. al., 2013",
    "K": "Kuwajima, M., Mendenhall, J. M., Lindsey, L. F. & Harris, K. M. 2013",
    "L": "Lee, W. A., et. al., 2016",
    "M": "Zheng, Z., et al., 2017",
}
# dashed reference line: rows inside the plot where many short dark runs lie
# (search above the legend box, whose top and bottom edges are the other long dark rows at ~1475 and ~1966)
rows = [r for r in range(40, 1000) if (g[r, 190:2040] < 128).mean() > 0.4]
dash_row = float(np.mean(rows))
rows_out = []
for lab_, (px, py) in zip(labels, pts):
    rows_out.append(["point", lab_, legend[lab_], float(fx(px)), float(fy(py)), float(np.log10(fy(py)))])
rows_out.append(["dashed_line", "", "horizontal dashed line across the plot", float("nan"), float(fy(dash_row)),
                 float(np.log10(fy(dash_row)))])
dpx = abs(1 / sy)  # px per decade
dc.write_csv(str(HERE / "fig1.csv"), [
    "Lee et al. 2018, PLoS ONE 13(10):e0206172, Fig 1: volume of neural tissue in ssTEM studies versus publication year.",
    "Columns: kind (point = one study marker, dashed_line = the horizontal dashed line), label = the printed letter,",
    "  legend = the legend entry for that letter (verbatim from the figure), year = x position in years,",
    "  volume_mm3 = y position in mm^3 (log axis), log10_volume = log10 of that.",
    "Provenance: tier 3, digitized by fig1_extract.py from the embedded 300 ppi raster image (no vector data in the PDF).",
    f"  x calibrated on 12 major ticks 1970-2025 (max residual {rx:.3f} yr); y on 8 decade ticks 1e0-1e-7 (log, max residual {ry:.4f} decades).",
    "  Marker centre = centroid of the filled circle (connected component).",
    f"Uncertainty: about +-0.05 yr in x and +-0.005 decades in y ({dpx:.0f} px per decade; centroid precision ~1 px).",
    "  The years come out as whole numbers to within 0.05 yr, matching the legend years.",
], ["kind", "label", "legend", "year", "volume_mm3", "log10_volume"], rows_out,
    fmt=["{}", "{}", "{}", "{:.2f}", "{:.4g}", "{:.3f}"])
(ROOT / "work").mkdir(exist_ok=True)
dc.overlay(a, pts + [(x, dash_row) for x in range(200, 2030, 4)], str(ROOT / "work/fig1_overlay.png"))
print("done", rx, ry, dash_row)
