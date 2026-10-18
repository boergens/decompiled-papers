"""Fig. 12 (p. 27): histogram of the number of cell types with a given number of constituent cells.
Tier 3, digitized from the embedded raster (PNG-coded, 2413 x 1605 px) at native resolution.

Calibration: the five labelled major y ticks (0, 500, 1000, 1500, 2000), linear fit.
Bars: one per x tick (21 ticks: 1..20 and '>20'). Bar top = top of the contiguous bar-coloured run above the
axis in two 9-px strips beside the tick centre (median green channel), plus the coverage fraction of the
partially covered top row. Bar bottom = value 0 from the fit.
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import rasterfig as rf  # noqa: E402

LABELS = [str(i) for i in range(1, 21)] + [">20"]
a = rf.load(27).astype(float)
g = a.mean(2)
H, W = g.shape
yax = [c for c in range(600) if (g[:, c] < 80).sum() > 900][0]          # left edge of the y-axis line

rows = [r for r in range(H) if (g[r, yax - 20:yax - 1] < 120).sum() >= 17]  # major ticks only
groups = np.split(np.array(rows), np.where(np.diff(rows) > 1)[0] + 1)
tick_px = [grp.mean() for grp in groups]
tick_val = [2000, 1500, 1000, 500, 0]
assert len(tick_px) == 5, tick_px
k, b = np.polyfit(tick_px, tick_val, 1)
res = np.array(tick_val) - (k * np.array(tick_px) + b)
y0 = -b / k

axis_rows = [r for r in range(H) if (g[r, :] < 80).sum() > 1500]
axis_top, axis_bot = axis_rows[0], axis_rows[-1]
row = g[axis_bot + 8]
xs = np.where(row[yax + 10:] < 120)[0] + yax + 10
runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1)
ticks = [r.mean() for r in runs]
assert len(ticks) == len(LABELS), (len(ticks), ticks)

out = []
for lab, xc in zip(LABELS, ticks):
    cols = list(range(int(xc) - 22, int(xc) - 13)) + list(range(int(xc) + 14, int(xc) + 23))
    strip = np.median(a[:axis_top, cols, 1], axis=1)
    r = axis_top - 1
    while r > 0 and strip[r] < 200:
        r -= 1
    full = axis_top - 1 - r
    part = np.clip((255 - strip[r]) / (255 - 120), 0, 1) if full > 0 else 0.0
    h = (full + part + (y0 - axis_top)) if full > 0 else 0.0
    out.append((lab, xc, h * -k))

with open(HERE / "fig12.csv", "w", newline="") as f:
    f.write("# Figure 12 (p. 27 of elife-57443-v4.pdf): histogram, number of cell types (y, '#types') with a given number of\n")
    f.write("#   constituent neurons (x, '#neurons in a type'; categories 1..20 and '>20').\n")
    f.write("# Provenance: tier 3, digitized from the embedded raster image (2413 x 1605 px) by fig12_extract.py.\n")
    f.write("# Tier 1 not available: the caption names 'Figure 12-source data 1' (eLife online), not in papers/scheffer2020/.\n")
    f.write(f"# y calibration: linear fit to the 5 labelled major ticks; {-1/k:.3f} px per type; residuals {np.round(res, 2).tolist()} types.\n")
    f.write("# Columns: neurons_in_type = x category label as printed; n_types = bar height (number of cell types).\n")
    f.write("# Uncertainty: about +-2 types (1 px = 1.56 types). Bars of 1-3 types are only 1-2 px tall; category 13 shows at most a\n")
    f.write("#   hairline bar (value 0-3).\n")
    w = csv.writer(f)
    w.writerow(["neurons_in_type", "n_types"])
    for lab, xc, v in out:
        w.writerow([lab, round(v, 1)])

from PIL import Image, ImageDraw  # noqa: E402
im = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(im)
for lab, xc, v in out:
    yy = y0 + v / k
    d.line([(xc - 45, yy), (xc + 45, yy)], fill=(255, 0, 0), width=3)
(HERE.parent / "work").mkdir(exist_ok=True)
im.save(HERE.parent / "work" / "fig12_overlay.png")
print("px/type", -1 / k, "res", res, "y0", y0, "axis", axis_top, axis_bot, [round(v, 1) for _, _, v in out], "sum", sum(v for _, _, v in out))
