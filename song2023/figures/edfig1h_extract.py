"""Extended Data Fig. 1h (right): stacked bars, ratio (%) of 2-mm samples with no / weak / strong gradient at sampling
positions 1, 2, 3, for Pg 6 h + OsO4 3 h, Pg 17 h + OsO4 3 h, Pg 17 h + OsO4 6 h -> edfig1h.csv

Tier 3 (digitized): no source data in the Edmond set for this panel. Raster figure, PDF p. 12, embedded 300-ppi
image. y axis fitted on its 9 tick marks (0, 12.5, ..., 100 %; labels 0, 50, 100). In the centre column of each of
the 9 bars the colour of every pixel row is classified (green = no, yellow = weak, red = strong); a segment boundary
is the middle of the dark outline line between two colours. Uncertainty +-1 % (about 1 px at 0.76 %/px plus the
outline width).
Run: python3 -I edfig1h_extract.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, WORK, fit, hue_mask, overlay, page_image, write_csv  # noqa: E402

a = page_image(12)
YT = [1753.5, 1786.0, 1819.0, 1852.0, 1885.0, 1918.0, 1951.0, 1984.0, 2017.0]
py2y, y2py, ry = fit(YT, np.arange(100, -1, -12.5))
BARS = [(656, 671), (677, 693), (698, 714), (744, 759), (765, 781), (786, 801), (832, 847), (853, 868), (873, 889)]
COND = [("6", "3")] * 3 + [("17", "3")] * 3 + [("17", "6")] * 3
cls = {"no": hue_mask(a, 55, 90, 80, 60), "strong": hue_mask(a, 170, 8, 80, 80), "weak": hue_mask(a, 20, 40, 80, 120)}
rows, ov = [], []
for k, ((c0, c1), (pg, os_)) in enumerate(zip(BARS, COND)):
    xc = (c0 + c1) // 2
    lab = []
    for y in range(1750, 2022):
        win = {n: m[y, xc - 3:xc + 4].mean() for n, m in cls.items()}
        n = max(win, key=win.get)
        lab.append(n if win[n] > 0.5 else None)
    # contiguous coloured runs
    runs, cur = [], None
    for i, n in enumerate(lab):
        y = 1750 + i
        if n != (cur[0] if cur else None):
            if cur and cur[0]:
                runs.append((cur[0], cur[1], y - 1))
            cur = (n, y)
    if cur and cur[0]:
        runs.append((cur[0], cur[1], 2021))
    # boundaries: between runs use the midpoint of the gap (outline line); outer ends: bar top / axis
    bounds = []
    for j, (n, y0, y1) in enumerate(runs):
        top = YT[0] if j == 0 else (runs[j - 1][2] + y0) / 2
        bot = YT[-1] if j == len(runs) - 1 else (y1 + runs[j + 1][1]) / 2
        bounds.append((n, float(py2y(bot)), float(py2y(top))))
    for n, lo, hi in bounds:
        rows.append([k % 3 + 1, pg, os_, n, f"{lo:.1f}", f"{hi:.1f}", f"{hi - lo:.1f}"])
        ov += [(xc, y2py(lo)), (xc, y2py(hi))]
write_csv(os.path.join(HERE, "edfig1h.csv"), [
    "Song et al. 2023 Nat Methods, Extended Data Fig. 1h (right): stacked bars of the ratio (%) of samples showing no",
    "  (green), weak (yellow) or strong (red) gradient, at sampling positions 1, 2, 3 (numbers above the bars; cf. the",
    "  photo with positions 1-3), for Pg incubation 6/17/17 h and OsO4 (third Os) 3/3/6 h (labels below the bars).",
    "Provenance: tier 3, digitized from the raster figure (PDF p. 12) by edfig1h_extract.py; y fitted on 9 ticks",
    f"  (max residual {ry:.2f} %); uncertainty +-1 %. No source data for this panel in the Edmond data set.",
    "Columns: position; pg_h; oso4_h; gradient; bottom_pct; top_pct; height_pct (segment of the stacked bar).",
], ["position", "pg_h", "oso4_h", "gradient", "bottom_pct", "top_pct", "height_pct"], rows)
overlay(a, ov, os.path.join(WORK, "edfig1h_overlay_full.png"))
from PIL import Image  # noqa: E402
Image.open(os.path.join(WORK, "edfig1h_overlay_full.png")).crop((560, 1640, 1010, 2150)).save(os.path.join(WORK, "edfig1h_overlay.png"))
for r in rows:
    print(r)
