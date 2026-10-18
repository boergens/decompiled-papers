"""Digitize Figure 13 of Xie & Fang 2019 (Nanoscale Res Lett 14:370, PDF p. 12): cutting forces Ft and Fn
versus cutting depth at edge radius 2 nm.

Source: the embedded 300 ppi JPEG of Fig. 13 (896 x 534 px), an Excel line chart with light-grey gridlines.
    python3 -I -B fig13_extract.py   -> fig13.csv (+ ../work/fig13_overlay.png for checking)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, overlay, write_csv  # noqa: E402
from excel_markers import EXCEL_BLUE, EXCEL_ORANGE, gridlines, markers  # noqa: E402

PDF = HERE.parent / "source" / "xie2019.pdf"
a = embedded_image(str(PDF), 12, bbox_near=(66.2, 94.8, 281.1, 222.8))
assert a.shape[:2] == (534, 896), a.shape

# gridlines: vertical ones at x = 0, 0.2, ..., 2.4 A; horizontal ones at y = 80, 70, ..., -10 nN
vx = gridlines(a, 1, 100, 890, 10, 430)
hy = gridlines(a, 0, 5, 440, 115, 875)
assert len(vx) == 13 and len(hy) == 10, (vx, hy)
fx, rx, sx = fit_axis(vx, np.round(np.arange(13) * 0.2, 1))
fy, ry, sy = fit_axis(hy, np.arange(80, -11, -10))

LEGEND = [(720, 315, 750, 395)]   # legend markers (Ft, Fn)
rows, pts = [], []
for name, col in (("Ft", EXCEL_BLUE), ("Fn", EXCEL_ORANGE)):
    for x, y, r, k in markers(a, col, LEGEND):
        rows.append((name, float(fx(x)), float(fy(y)), float(x), float(y)))
        pts.append((x, y))
(HERE.parent / "work").mkdir(exist_ok=True)
overlay(a, pts, str(HERE.parent / "work" / "fig13_overlay.png"))

write_csv(str(HERE / "fig13.csv"), [
    "Xie & Fang 2019, Nanoscale Research Letters 14:370, Fig. 13: cutting forces versus cutting depth at edge radius of 2 nm.",
    "Columns: series (Ft = tangential, Fn = normal cutting force, the legend names); cutting_depth_A = x (Angstrom);",
    "  cutting_force_nN = y (nN); px_x, px_y = marker centre in the embedded image (896 x 534 px), for checking.",
    "One row per plotted marker (19 per series). The smoothed lines between markers are Excel's drawing, not data.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster (no vector data in the PDF) by fig13_extract.py.",
    f"  x calibrated on the 13 vertical gridlines (0 to 2.4 A), max residual {rx:.4f} A; y on the 10 horizontal",
    f"  gridlines (-10 to 80 nN), max residual {ry:.3f} nN. Marker centre = circle fit to the marker rim.",
    f"Uncertainty: about +-{abs(sx):.4f} A in x and +-{abs(sy):.2f} nN in y (1 px).",
    "Note: the markers sit at x = 0, 0.18, 0.38, ... (0.2 A steps from 0.18) and at 0.1 A steps from 0.98 to 2.38 A,",
    "  with no marker near 1.98 A; read as plotted.",
], ["series", "cutting_depth_A", "cutting_force_nN", "px_x", "px_y"], rows,
    fmt=["{}", "{:.3f}", "{:.2f}", "{:.2f}", "{:.2f}"])
print("wrote fig13.csv", len(rows), "rows; residuals", rx, ry)
