"""Extract Fig. 4f of Hua et al. 2015 (main PDF p.6) from the vector paths in the PDF -> fig4f_vector.csv

Panel f: p(p_e) (log y, 10^-1 .. 10^3) against p_e (linear, 0 .. 1), one blue line (MATLAB plot,
stroke 0.5 pt) drawn as 15 separate sub-paths: narrow spikes that rise from below the bottom of
the axis box and fall back to it.

    python3 -I fig4f_vector_extract.py   -> fig4f_vector.csv (+ ../work/fig4f_overlay.png)

Axis calibration (page coordinates, points):
  x: tick marks at x=164.760 (label "0") and x=225.699 (label "1"); check: the unlabelled tick at
     x=195.251 maps to 0.5003.
  y: log10; major ticks (10^-1 = frame bottom) at y=284.422, 275.555, 266.687, 257.820, 248.954 = 10^-1 .. 10^3 (labels at
     10^-1, 10^1, 10^3), fitted by least squares.
Note: tools/vector_dump.py misses every horizontal or vertical line (Rect.intersects() is False for a
zero-area bbox), so this script selects paths with a closed-interval overlap test of its own.
"""
import csv
import os

import numpy as np
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "../source/hua2015.pdf")
PAGE = 6
FRAME = (158.688, 248.954, 231.815, 284.422)  # x0, y0 (top = 10^3), x1, y1 (bottom = 10^-1)

doc = pymupdf.open(PDF)
page = doc[PAGE - 1]


def inside(r, box, tol=0.5):
    return r.x1 >= box[0] - tol and r.x0 <= box[2] + tol and r.y1 >= box[1] - tol and r.y0 <= box[3] + tol


draw = [d for d in page.get_drawings() if inside(d["rect"], FRAME)]
# axis ticks (black, 0.5 pt) on the x axis and on the y axis
xt = sorted({round(d["rect"].x0, 3) for d in draw if d.get("color") == (0.0, 0.0, 0.0)
             and d["rect"].width == 0 and d["rect"].y0 >= FRAME[3] - 0.01 and d["rect"].height < 2})
yt = sorted({round(d["rect"].y0, 3) for d in draw if d.get("color") == (0.0, 0.0, 0.0)
             and d["rect"].height == 0 and abs(d["rect"].width - 2.628) < 0.01})
print("x ticks", xt, "major y ticks", yt)
X0, X1 = 164.760, 225.699
assert X0 in xt and X1 in xt and 195.251 in xt
fx = lambda X: (np.asarray(X, float) - X0) / (X1 - X0)
ymaj = np.array([284.422, 275.555, 266.687, 257.820, 248.954])
# the 10^-1 tick coincides with the x axis line (frame bottom, y=284.422), so only 4 long ticks are found;
# the minor ticks (2..9 x 10^-1 between 284.422 and 275.555) confirm the log pattern.
assert all(any(abs(a - b) < 0.002 for b in yt) for a in ymaj[1:]), yt
A = np.vstack([ymaj, np.ones(5)]).T
(m, b), *_ = np.linalg.lstsq(A, np.array([-1, 0, 1, 2, 3.0]), rcond=None)
yres = np.max(np.abs(A @ [m, b] - [-1, 0, 1, 2, 3]))
fy = lambda Y: 10 ** (m * np.asarray(Y, float) + b)
print("x check 195.251 ->", fx(195.251), "; y fit residual (decades)", yres, "; pt per decade", -1 / m)

blue = [d for d in draw if d.get("color") == (0.0, 0.0, 1.0) and d.get("width") == 0.5]
blue.sort(key=lambda d: d["rect"].x0)
rows, pix = [], []
for k, d in enumerate(blue, 1):
    pts = [d["items"][0][1]] + [it[-1] for it in d["items"]]
    for p in pts:
        flag = ""
        if p.y > FRAME[3] - 0.001:
            flag = "below_axis"     # line runs out of the bottom of the box (value < 10^-1, e.g. 0)
        elif p.y < FRAME[1] + 0.001:
            flag = "at_top"         # line reaches the top of the box (value >= 10^3)
        rows.append((k, float(fx(p.x)), float(fy(p.y)), flag))
        pix.append((p.x, p.y))

with open(os.path.join(HERE, "fig4f_vector.csv"), "w", newline="") as f:
    for h in [
        "Hua, Laserstein & Helmstaedter 2015 Nat Commun 6:7923, Fig. 4f: fitted distribution of skeleton-edge difficulty",
        "  (edge probability) p(p_e); one blue line on a log y axis.",
        "Columns: segment = index of the separate drawn sub-path (left to right; the line is only visible where it rises",
        "  above the bottom of the axis box); p_e = edge probability (axis 'p_e', linear, ticks labelled 0 and 1);",
        "  p_pe = p(p_e) (axis 'p(p_e)', log10, ticks labelled 10^-1, 10^1, 10^3); flag: below_axis = vertex lies on",
        "  the bottom frame of the plot (10^-1), i.e. the true value is <= 10^-1 (possibly 0) and was clipped;",
        "  at_top = vertex on the top of the axis box (10^3), true value may be larger.",
        "Provenance: tier 2, vector paths in the PDF (fig4f_vector_extract.py). Every vertex of the 15 blue (0.5 pt) sub-paths;",
        f"  x from the ticks at p_e=0 and 1 (check: middle tick -> {fx(195.251):.4f}); y from 5 decade ticks, max residual",
        f"  {yres:.1e} decades.",
        "Uncertainty: exact up to the PDF's coordinate precision (0.001 pt = 1.6e-5 in p_e, 1e-4 decades in y).",
    ]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["segment", "p_e", "p_pe", "flag"])
    for r in rows:
        w.writerow([r[0], f"{r[1]:.5f}", f"{r[2]:.5g}", r[3]])
print(len(rows), "vertices in", len(blue), "segments")

# overlay: render the panel at 8x and draw the vertices
from PIL import Image, ImageDraw  # noqa: E402
clip = pymupdf.Rect(150, 240, 240, 295)
z = 8
pm = page.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
dr = ImageDraw.Draw(im)
for x, y in pix:
    u, v = (x - clip.x0) * z, (y - clip.y0) * z
    dr.ellipse([u - 3, v - 3, u + 3, v + 3], outline=(255, 0, 255), width=2)
im.save(os.path.join(HERE, "../work/fig4f_overlay.png"))
