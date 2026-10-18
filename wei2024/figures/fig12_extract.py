"""Digitize Fig. 12 a-f of wei2024 (tier 3): marker centres per series from the embedded 300 ppi JPEG.

Writes figures/fig12a.csv ... fig12f.csv and overlays work/fig12_overlay.png, work/fig12_overlay_zoom_<p>.png.
Method (tools/f3_markers.py, tools/f3_panels.py): axis calibration on the inward major ticks; per series a colour
mask with legend/title boxes blanked; 3x3 closing and filling of small holes; template matching with a filled
synthetic marker of the legend's shape (centre checked on the legend marker, work/fig12_legend_check.txt); ink of
the other series counts half; for each of the 30 marker columns (sliding distance 1, 2, ..., 30 A) the best match
within +-3 px horizontally, anywhere in the plot vertically. Fig. 12d F_z at 29 A is not drawn (override).
Run: python3 -I -B figures/fig12_extract.py
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
import f3_markers as fm  # noqa: E402,F401
from f3_panels import LEGEND_LOG, run_panel, sheet, write  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)

FORCE_SERIES = [("Fx", "black", "open square"), ("Fy", "red", "filled circle"), ("Fz", "magenta", "open up-triangle")]
FORCE_Y = [10, 5, 0, -5, -10, -15]
SRC = "the embedded 300 ppi JPEG (PDF page 16, xref 249) by figures/fig12_extract.py"

PANELS = {
    # frame (L cols, R cols, T rows, B rows), legend search box, blank boxes (legend + labels, title)
    "a": dict(frame=((88, 89), (673, 674), (4, 5), (434, 436)), title="hc = 5 A, 1.0 A/ps",
              legend=(120, 260, 250, 395), blank=[(120, 255, 250, 400), (275, 35, 525, 90)]),
    "b": dict(frame=((764, 765), (1349, 1350), (4, 5), (436, 437)), title="hc = 10 A, 1.0 A/ps",
              legend=(795, 255, 925, 390), blank=[(795, 250, 925, 395), (930, 33, 1195, 85)],
              override={("Fx", 30): "covered"}),
    "c": dict(frame=((1446, 1448), (2031, 2033), (2, 3), (433, 434)), title="hc = 15 A, 1.0 A/ps",
              legend=(1475, 285, 1595, 420), blank=[(1475, 292, 1595, 425), (1610, 33, 1875, 85)]),
    "d": dict(frame=((83, 85), (668, 669), (609, 610), (1039, 1040)), title="hc = 20 A, 1.0 A/ps",
              legend=(100, 885, 220, 1015), blank=[(100, 880, 220, 1020), (240, 622, 500, 675)],
              override={("Fz", 29): "nan"}),
    "e": dict(frame=((762, 764), (1347, 1349), (606, 607), (1037, 1038)), title="hc = 25 A, 1.0 A/ps",
              legend=(775, 910, 882, 1030), blank=[(775, 905, 882, 1035), (795, 620, 1055, 672)]),
}
F_SERIES = [("5 A", "black", "open square"), ("10 A", "red", "filled circle"), ("15 A", "green", "open up-triangle"),
            ("20 A", "blue", "open down-triangle"), ("25 A", "magenta", "open diamond")]
F_PANEL = dict(frame=((1472, 1474), (2031, 2033), (610, 611), (1021, 1022)),
               legend=(1510, 665, 1610, 835), blank=[(1505, 630, 1640, 840), (1700, 630, 1800, 675)])
F_Y = [12000, 11000, 10000, 9000, 8000]  # 13000 and 7000 sit on the top and bottom frame lines (no visible tick)


def main():
    a = dc.embedded_image(str(PDF), 16)
    allpts = []
    for key, cfg in PANELS.items():
        cfg["others"] = True
        cfg["legend_blank_all"] = True
        header, rows, pts = run_panel(a, "12", key, cfg, FORCE_SERIES, FORCE_Y, "Force", "nN", cfg["title"], SRC)
        header[1] = header[1].replace("Force (nN)", "force (nN); series Fx black open squares, Fy red filled circles, Fz magenta open triangles")
        write(HERE / f"fig12{key}.csv", header, rows)
        allpts += pts
    F_PANEL["others"] = True
    F_PANEL["legend_blank_all"] = True
    header, rows, pts = run_panel(a, "12", "f", F_PANEL, F_SERIES, F_Y, "Total energy", "kcal/mol", "hc = 5-25 A, 1.0 A/ps", SRC)
    header[1] = header[1].replace("Total energy (kcal/mol)", "total energy (kcal/mol); series = hc: 5 A black squares, 10 A red circles, 15 A green up-triangles, 20 A blue down-triangles, 25 A magenta diamonds")
    write(HERE / "fig12f.csv", header, rows)
    allpts += pts
    sheet(a, allpts, WORK / "fig12_weak_sheet.png")
    (WORK / "fig12_legend_check.txt").write_text("\n".join(LEGEND_LOG) + "\n")
    ov = a.copy()
    for x, y, c, lab, sc in allpts:
        xi, yi = int(round(x)), int(round(y))
        ov[yi, max(0, xi - 4):xi + 5] = (0, 200, 255)
        ov[max(0, yi - 4):yi + 5, xi] = (0, 200, 255)
    from PIL import Image
    Image.fromarray(ov).save(WORK / "fig12_overlay.png")
    for key, (x0, y0, x1, y1) in {"a": (85, 0, 680, 440), "b": (760, 0, 1355, 440), "c": (1440, 0, 2034, 440),
                                  "d": (80, 600, 675, 1045), "e": (758, 600, 1352, 1045), "f": (1468, 605, 2034, 1028)}.items():
        Image.fromarray(ov[y0:y1, x0:x1]).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.NEAREST).save(WORK / f"fig12_overlay_zoom_{key}.png")


if __name__ == "__main__":
    main()
