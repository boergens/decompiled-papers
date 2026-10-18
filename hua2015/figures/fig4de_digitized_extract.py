"""Digitize Fig. 4d (Meas.) and 4e (Fit) of Hua et al. 2015 (main PDF p.6) -> fig4d_digitized.csv, fig4e_digitized.csv

The two vote-histogram heat maps and their shared colour bar ('# edges', log scale, ticks 1, 10, 100, 1,000)
are one embedded JPEG (304 x 122 px, xref 846, placed at x 138.768-238.107, y 178.810-218.794 pt). The axis
frames, tick marks and tick labels around them are vector paths/text, which give the cell grid exactly:
  d: frame x 138.938-178.691, y 178.840-218.592 pt; e: frame x 185.396-225.186, same y; 8 x 8 cells each.
  Tick labels 0, 3, 6 sit under/next to cells 0, 3 and 6 (cell index = number of votes); the small tick marks
  sit at the centres of cells 1, 3, 5 and 7.
  Colour bar: frame x 231.975-237.950, y 178.838 (top) - 218.629 (bottom); tick marks at y=218.629 (1),
  208.340 (10), 198.053 (100), 187.765 (1,000): log10, 10.288 pt per decade, so the top of the bar is 10^3.87.
Method: median RGB of the central 7 x 7 px of each cell; median RGB of the central columns of the colour bar in
each pixel row gives a lookup table row -> log10(value); each cell gets the value of the nearest colour-bar
colour (Euclidean RGB). The bar is MATLAB 'jet' (dark blue -> dark red).

    python3 -I fig4de_digitized_extract.py   -> fig4d_digitized.csv, fig4e_digitized.csv (+ ../work/fig4de_overlay.png)
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))   # tools/digitize_common.py
import numpy as np  # noqa: E402
from digitize_common import embedded_image  # noqa: E402

PDF = os.path.join(HERE, "../source/hua2015.pdf")
IMG_BBOX = (138.768, 178.810, 238.107, 218.794)
a = embedded_image(PDF, 6, bbox_near=IMG_BBOX).astype(float)
H, W = a.shape[:2]
assert (W, H) == (304, 122)
sx = W / (IMG_BBOX[2] - IMG_BBOX[0])
sy = H / (IMG_BBOX[3] - IMG_BBOX[1])
px = lambda X: (X - IMG_BBOX[0]) * sx
py = lambda Y: (Y - IMG_BBOX[1]) * sy

# colour bar lookup
CB = (231.975, 178.838, 237.950, 218.629)
cb_c0, cb_c1 = int(round(px(CB[0]))) + 3, int(round(px(CB[2]))) - 3
rows = np.arange(int(np.ceil(py(CB[1]))) + 1, int(np.floor(py(CB[3]))) - 1)
lut_rgb = np.array([np.median(a[r, cb_c0:cb_c1 + 1], axis=0) for r in rows])
Y_of_row = IMG_BBOX[1] + (rows + 0.5) / sy
lut_log = (218.629 - Y_of_row) / 10.288
print("colour bar columns", cb_c0, cb_c1, "rows", rows[0], rows[-1], "log10 range", lut_log.min(), lut_log.max())
bottom_rgb = lut_rgb[-1]


def lookup(rgb):
    dist = np.sqrt(((lut_rgb - rgb) ** 2).sum(1))
    k = int(np.argmin(dist))
    return lut_log[k], dist[k], k


pts = []
for panel, x0, x1 in (("d", 138.938, 178.691), ("e", 185.396, 225.186)):
    y0, y1 = 178.840, 218.592
    cw, ch = (x1 - x0) / 8, (y1 - y0) / 8
    out = []
    for T in range(8):
        for N in range(8):
            cx, cy = px(x0 + (N + 0.5) * cw), py(y0 + (T + 0.5) * ch)
            ci, ri = int(round(cx)), int(round(cy))
            rgb = np.median(a[ri - 3:ri + 4, ci - 3:ci + 4].reshape(-1, 3), axis=0)
            lg, dist, k = lookup(rgb)
            flag = ""
            if k >= len(rows) - 3 or np.sqrt(((rgb - bottom_rgb) ** 2).sum()) < 25:
                flag = "bottom_colour"   # darkest blue: <= ~1 edge on the colour scale (0 is drawn the same way)
            elif k <= 2:
                flag = "top_colour"      # darkest red at the top of the bar: >= ~6,000, may be clipped
            out.append((N, T, 10 ** lg, lg, dist, "%d %d %d" % tuple(rgb), flag))
            pts.append((cx, cy))
    name = {"d": "Meas. (measured vote histogram)", "e": "Fit (fitted vote histogram)"}[panel]
    path = os.path.join(HERE, f"fig4{panel}_digitized.csv")
    with open(path, "w", newline="") as f:
        for h in [
            f"Hua, Laserstein & Helmstaedter 2015 Nat Commun 6:7923, Fig. 4{panel}: {name}, heat map of the number of",
            "  skeleton edges ('# edges', colour, log scale) for each combination of total votes N and agreeing votes T.",
            "Columns: N = 'Total votes for an edge (N)' (x, cells 0..7, left to right); T = 'Agreeing votes for an edge (T)'",
            "  (y, cells 0..7, top to bottom); n_edges = '# edges' read from the colour bar; log10_n_edges; rgb_dist = RGB",
            "  distance between the cell colour and the nearest colour-bar colour (JPEG noise; < ~15 is a clean match);",
            "  cell_rgb = median colour of the cell; flag bottom_colour = the darkest blue at the bottom of the colour bar",
            "  (1 edge or fewer; empty cells are drawn the same way, so 0 cannot be told apart); top_colour = the darkest",
            "  red at the top of the bar (the lookup stops 2 px below the top, at 10^3.79; the true value may be higher).",
            "Provenance: tier 3, digitized from the embedded 304 x 122 px JPEG (heat maps and colour bar; ~3.06 px per pt,",
            "  ~15 px per cell) by fig4de_digitized_extract.py. Cell grid from the vector axis frames; colour bar calibrated on its",
            "  vector tick marks at 1, 10, 100, 1,000 (log10, 10.288 pt per decade; bar top = 10^3.87).",
            "Uncertainty: about +-0.06 in log10 (+-15 %): the colour map has discrete steps of ~0.06 decades (64-colour",
            "  'jet' over 3.87 decades) and the JPEG shifts colours slightly. Values below ~1.15 cannot be resolved.",
        ]:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(["N", "T", "n_edges", "log10_n_edges", "rgb_dist", "cell_rgb", "flag"])
        for r in out:
            w.writerow([r[0], r[1], f"{r[2]:.3g}", f"{r[3]:.3f}", f"{r[4]:.1f}", r[5], r[6]])
    print(path, "max rgb_dist", max(r[4] for r in out),
          "non-bottom cells", sum(1 for r in out if not r[6]))

from PIL import Image  # noqa: E402
z = 4
im = Image.fromarray(a.astype(np.uint8)).resize((W * z, H * z), Image.NEAREST)
arr = np.array(im)
for cx, cy in pts:
    u, v = int(round(cx * z)), int(round(cy * z))
    arr[v - 14:v + 15, u - 14:u - 12] = (255, 0, 255)
    arr[v - 14:v + 15, u + 13:u + 15] = (255, 0, 255)
    arr[v - 14:v - 12, u - 14:u + 15] = (255, 0, 255)
    arr[v + 13:v + 15, u - 14:u + 15] = (255, 0, 255)
arr[int(rows[0] * z):int(rows[-1] * z), cb_c0 * z:cb_c0 * z + 2] = (255, 0, 255)
arr[int(rows[0] * z):int(rows[-1] * z), (cb_c1 + 1) * z - 2:(cb_c1 + 1) * z] = (255, 0, 255)
Image.fromarray(arr).save(os.path.join(HERE, "../work/fig4de_overlay.png"))
