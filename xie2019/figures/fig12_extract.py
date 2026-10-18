"""Digitize Figure 12 (a) and (b) of Xie & Fang 2019 (Nanoscale Res Lett 14:370, PDF p. 11): cutting forces versus
tool edge radius at cutting depth of 2 A.

Source: the embedded 300 ppi JPEG of Fig. 12 (1420 x 569 px) holding both panels, Excel line charts with
light-grey gridlines.
    python3 -I -B fig12_extract.py   -> fig12a.csv, fig12b.csv (+ ../work/fig12_overlay.png for checking)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, overlay, write_csv  # noqa: E402
from excel_markers import EXCEL_BLUE, EXCEL_ORANGE, gridlines, markers  # noqa: E402

PDF = HERE.parent / "source" / "xie2019.pdf"
a = embedded_image(str(PDF), 11, bbox_near=(127.3, 576.7, 468.0, 713.1))
assert a.shape[:2] == (569, 1420), a.shape

PANELS = {  # column window of the plot area, y gridline values top to bottom
    "a": dict(cols=(110, 690), yvals=np.arange(170, 9, -20), series=(("Ft", EXCEL_BLUE), ("Fn", EXCEL_ORANGE)),
              legend=[(480, 200, 520, 290)]),
    "b": dict(cols=(820, 1415), yvals=np.arange(46, 21, -4), series=(("Ft", EXCEL_BLUE),),
              legend=[(1175, 235, 1210, 270)]),
}
pts = []
for p, cfg in PANELS.items():
    c0, c1 = cfg["cols"]
    vx = gridlines(a, 1, c0, c1, 10, 470)
    hy = gridlines(a, 0, 5, 475, c0 + 15, c1 - 15)
    assert len(vx) == 11 and len(hy) == len(cfg["yvals"]), (p, vx, hy)
    fx, rx, sx = fit_axis(vx, np.arange(11))
    fy, ry, sy = fit_axis(hy, cfg["yvals"])
    rows = []
    for name, col in cfg["series"]:
        for x, y, r, k in markers(a, col, cfg["legend"]):
            if not (c0 <= x <= c1):
                continue
            rows.append((name, float(fx(x)), float(fy(y)), float(x), float(y)))
            pts.append((x, y))
    yr = f"{cfg['yvals'][-1]} to {cfg['yvals'][0]} nN"
    write_csv(str(HERE / f"fig12{p}.csv"), [
        f"Xie & Fang 2019, Nanoscale Research Letters 14:370, Fig. 12({p}): cutting forces versus tool edge radius at cutting depth of 2 A.",
        "Columns: series (legend names: Ft, tangential" + (", and Fn, normal cutting force" if p == "a" else " cutting force; panel b shows Ft alone")
        + "); tool_edge_radius_nm = x (nm);",
        "  cutting_force_nN = y (nN); px_x, px_y = marker centre in the embedded image (1420 x 569 px, both panels), for checking.",
        "One row per plotted marker (8 per series, at R = 0, 1, 2, 3, 4, 5, 7.5, 10 nm). The smoothed lines between markers",
        "  are Excel's drawing, not data.",
        f"Provenance: tier 3, digitized from the embedded 300 ppi raster (no vector data in the PDF) by fig12_extract.py.",
        f"  x calibrated on the 11 vertical gridlines (0 to 10 nm), max residual {rx:.4f} nm; y on the {len(hy)} horizontal",
        f"  gridlines ({yr}), max residual {ry:.3f} nN. Marker centre = circle fit to the marker rim.",
        f"Uncertainty: about +-{abs(sx):.3f} nm in x and +-{abs(sy):.2f} nN in y (1 px).",
    ], ["series", "tool_edge_radius_nm", "cutting_force_nN", "px_x", "px_y"], rows,
        fmt=["{}", "{:.3f}", "{:.2f}", "{:.2f}", "{:.2f}"])
    print(f"fig12{p}.csv", len(rows), "rows; residuals", rx, ry)
(HERE.parent / "work").mkdir(exist_ok=True)
overlay(a, pts, str(HERE.parent / "work" / "fig12_overlay.png"))
