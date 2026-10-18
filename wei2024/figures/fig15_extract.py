"""Digitize Fig. 15 a-e of wei2024 (tier 3): marker centres of Fx, Fy, Fz per sliding velocity.

Writes figures/fig15a.csv ... fig15e.csv (panel f: figures/fig15f_extract.py) and work/fig15_overlay*.png,
work/fig15_weak_sheet.png, work/fig15_legend_check.txt. Same method as fig12_extract.py (tools/f3_panels.py,
tools/f3_markers.py). Marker spacing (found by free template-peak detection, see README): a, b, e every 0.5 A (60 per series),
c every 1 A (30), d every 0.375 A (80).
Run: python3 -I -B figures/fig15_extract.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
from f3_panels import LEGEND_LOG, run_panel, sheet, write  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)
SRC = "the embedded 300 ppi JPEG (PDF page 19, xref 264) by figures/fig15_extract.py"

FORCE_SERIES = [("Fx", "black", "open square"), ("Fy", "red", "filled circle"), ("Fz", "magenta", "open up-triangle")]
FORCE_Y = [5, 0, -5, -10]  # 10 and -15 sit on the top and bottom frame lines (no visible tick)
SIZES = {"open square": (6, 6), "filled circle": (6, 6), "open up-triangle": (6, 7)}
HALF = np.arange(0.5, 30.01, 0.5)
ONE = np.arange(1, 31)
STEP375 = np.arange(1, 81) * 0.375

PANELS = {
    "a": dict(frame=((71, 72), (660, 662), (11, 12), (445, 446)), title="hc = 20 A, 0.1 A/ps", grid=HALF,
              legend=(100, 295, 225, 420), blank=[(100, 295, 225, 420), (115, 28, 350, 68)]),
    "b": dict(frame=((748, 749), (1340, 1342), (11, 12), (447, 448)), title="hc = 20 A, 0.5 A/ps", grid=HALF,
              legend=(790, 300, 900, 420), blank=[(790, 300, 900, 420), (948, 368, 1172, 410)]),
    "c": dict(frame=((1443, 1444), (2020, 2022), (16, 18), (443, 444)), title="hc = 20 A, 1.0 A/ps", grid=ONE,
              legend=(1484, 290, 1592, 410), blank=[(1484, 290, 1592, 410), (1483, 30, 1712, 72)]),
    "d": dict(frame=((82, 83), (660, 662), (606, 608), (1033, 1034)), title="hc = 20 A, 1.5 A/ps", grid=STEP375,
              legend=(100, 880, 210, 1015), blank=[(100, 880, 210, 1015), (100, 620, 330, 665)]),
    "e": dict(frame=((759, 760), (1346, 1347), (603, 604), (1034, 1036)), title="hc = 20 A, 2.0 A/ps", grid=HALF,
              legend=(785, 900, 893, 1020), blank=[(785, 900, 893, 1020), (785, 620, 1015, 662)]),
}
ZOOMS = {"a": (68, 0, 665, 450), "b": (745, 0, 1345, 452), "c": (1440, 5, 2025, 448),
         "d": (79, 595, 665, 1038), "e": (756, 592, 1350, 1040)}


def main():
    a = dc.embedded_image(str(PDF), 19, bbox_near=(54, 59, 542, 338))
    allpts = []
    for key, cfg in PANELS.items():
        cfg["sizes"] = SIZES
        cfg["ring"] = ("filled circle",)
        cfg["others"] = True
        cfg["close"] = 0  # the open markers of this figure have intact outlines; closing would merge dashes into blobs
        header, rows, pts = run_panel(a, "15", key, cfg, FORCE_SERIES, FORCE_Y, "Force", "nN", cfg["title"], SRC)
        header[1] = header[1].replace("Force (nN)", "force (nN); series Fx black open squares, Fy red filled circles, Fz magenta open triangles")
        write(HERE / f"fig15{key}.csv", header, rows)
        allpts += pts
    sheet(a, allpts, WORK / "fig15_weak_sheet.png")
    (WORK / "fig15_legend_check.txt").write_text("\n".join(LEGEND_LOG) + "\n")
    from PIL import Image
    ov = a.copy()
    for x, y, c, lab, sc in allpts:
        xi, yi = int(round(x)), int(round(y))
        ov[yi, max(0, xi - 3):xi + 4] = (0, 200, 255)
        ov[max(0, yi - 3):yi + 4, xi] = (0, 200, 255)
    Image.fromarray(ov).save(WORK / "fig15_overlay.png")


if __name__ == "__main__":
    main()
