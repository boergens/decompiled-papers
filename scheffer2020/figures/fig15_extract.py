"""Fig. 15 (p. 33): grouped histogram of connection precision ('% valid connections') per cell type, upstream and
downstream partners. Tier 3, digitized from the embedded raster (plotly export, 2795 x 1333 px) at native resolution.

Calibration: y from the 8 white gridlines (50 ... 400, labelled every 50), linear fit; x from the 10 tick marks
under the axis (0 ... 90, labels every 10). Bins are 5 % wide and centred on multiples of 5; in each bin the
'upstream' bar (light green) lies left of the bin centre and 'downstream' (dark green) right of it. Bar top =
top of the contiguous run of the series colour above the zero line (median of a 16-px strip), plus the colour
fraction of the partly covered top row.
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import rasterfig as rf  # noqa: E402

a = rf.load(33).astype(float)
H, W, _ = a.shape
BG = np.array([229, 236, 246])
COL = {"upstream": np.array([133, 216, 133]), "downstream": np.array([43, 128, 43])}

# y: white gridlines in a background column
col = a[:, 400]
wr = [r for r in range(1175) if (col[r] > 250).all()]
grp = np.split(np.array(wr), np.where(np.diff(wr) > 1)[0] + 1)
gl_px = [g.mean() for g in grp]
gl_val = [400, 350, 300, 250, 200, 150, 100, 50]
assert len(gl_px) == 8, gl_px
ky, by = np.polyfit(gl_px, gl_val, 1)
yres = np.array(gl_val) - (ky * np.array(gl_px) + by)
y0 = -by / ky

# x: tick marks below the plot area
g = a.mean(2)
xs = np.where(g[1188, 200:2400] < 150)[0] + 200
runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1)
tx = [r.mean() for r in runs]
tv = [10 * i for i in range(len(tx))]
kx, bx = np.polyfit(tv, tx, 1)                   # px = kx*value + bx
xres = np.array(tx) - (kx * np.array(tv) + bx)

zero_row = int(np.floor(y0))                     # first row at/below the zero line
out = []
for c in range(0, 101, 5):
    xc = kx * c + bx
    for s, sgn in (("upstream", -1), ("downstream", +1)):
        cols = np.arange(int(xc + sgn * 12), int(xc + sgn * 28), sgn)
        strip = np.median(a[:zero_row, cols, :], axis=1)
        d_ser = np.abs(strip - COL[s]).sum(1)
        r = zero_row - 1
        while r > 0 and d_ser[r] < 60:
            r -= 1
        full = zero_row - 1 - r
        if full == 0:
            out.append((c, s, 0.0, 0)); continue
        # partial top row: fraction of the way from background to series colour
        frac = np.clip(np.dot(strip[r] - BG, COL[s] - BG) / np.dot(COL[s] - BG, COL[s] - BG), 0, 1)
        top = r + 1 - frac
        v = (y0 - top) * -ky
        out.append((c, s, v, int(round(v))))

with open(HERE / "fig15.csv", "w", newline="") as f:
    f.write("# Figure 15 (p. 33 of elife-57443-v4.pdf): connection precision of upstream and downstream partners for ~1000 cell types\n")
    f.write("#   (histogram; x '% valid connections', y 'Cell Type Count'; two series 'upstream' and 'downstream').\n")
    f.write("# Provenance: tier 3, digitized from the embedded raster image (2795 x 1333 px) by fig15_extract.py.\n")
    f.write("# Tier 1 not available: the caption names 'Figure 15-source data 1' (data on 1735 neurons, eLife online), not in papers/scheffer2020/.\n")
    f.write(f"# y calibration: 8 gridlines (50..400), {-1/ky:.3f} px per count, residuals {np.round(yres, 3).tolist()} counts;\n")
    f.write(f"#   x calibration: 10 tick marks (0..90), {kx:.3f} px per %, residuals {np.round(xres, 2).tolist()} px.\n")
    f.write("# Columns: bin_centre_pct = centre of the 5 %-wide bin (bars are drawn left (upstream) and right (downstream) of it;\n")
    f.write("#   the bin edges are not printed: centre +-2.5 assumed); series; count_read = bar height read off the image;\n")
    f.write("#   count = count_read rounded to an integer (counts are integers). Uncertainty about +-0.4 counts (1 px = 0.35 counts).\n")
    w = csv.writer(f)
    w.writerow(["bin_centre_pct", "series", "count_read", "count"])
    for c, s, v, n in out:
        w.writerow([c, s, round(v, 2), n])

from PIL import Image, ImageDraw  # noqa: E402
im = Image.fromarray(a.astype(np.uint8))
dr = ImageDraw.Draw(im)
for c, s, v, n in out:
    xc = kx * c + bx
    yy = y0 + v / ky
    x0, x1 = (xc - 40, xc - 2) if s == "upstream" else (xc + 2, xc + 40)
    dr.line([(x0, yy), (x1, yy)], fill=(255, 0, 0) if s == "upstream" else (255, 0, 255), width=3)
(HERE.parent / "work").mkdir(exist_ok=True)
im.save(HERE.parent / "work" / "fig15_overlay.png")
tot = {s: sum(n for c, ss, v, n in out if ss == s) for s in COL}
print("y0", y0, "px/count", -1 / ky, "kx", kx, "totals", tot)
print([(c, s, round(v, 2)) for c, s, v, n in out if v > 0])
