"""Fig. 3e (plot, right) of Zhao et al. 2025: average depth profiles of bond damage phi_y, from the PDF's vector
paths (page 4). Writes fig3e.csv and work/fig3e_overlay.png.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import vecplot as vp  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
pg = vp.page(PDF, 4)
X = vp.Axis([(344.99, 0), (377.56, 50), (410.17, 100), (442.74, 150), (475.36, 200)])
Y = vp.Axis([(662.69, 0), (646.18, 0.1), (629.53, 0.2), (612.93, 0.3), (596.37, 0.4), (579.77, 0.5)])
alld = pg.get_drawings()
rows, ov = [], []
# lambda = 1.45: solid red stroke, path 30
d = alld[30]
assert vp.hexcol(d["color"]) == "#e74c3c" and d["type"] == "s"
for k, (x, y) in enumerate(vp.vertices(d)):
    rows.append(["lambda=1.45", "vertex", k, round(float(X(x)), 3), round(float(Y(y)), 5)])
    ov.append((x, y, (0, 200, 0)))
# lambda = 1.21: dashed red line, drawn as filled outlines of the dashes (path 29), line width 1.03 pt
d = alld[29]
assert vp.hexcol(d["fill"]) == "#e74c3c" and d["type"] == "f"
k = 0
for n, sub in enumerate(vp.subpaths(d)):
    for x, y in vp.outline_centreline(sub, 1.03):
        rows.append(["lambda=1.21", f"dash{n + 1}", k, round(float(X(x)), 3), round(float(Y(y)), 5)])
        ov.append((x, y, (255, 0, 255)))
        k += 1
# phi_b threshold: black dash-dot line, path 35
d = alld[35]
(x0, y0), (x1, y1) = vp.vertices(d)
for k, (x, y) in enumerate(((x0, y0), (x1, y1))):
    rows.append(["phi_b line", "end", k, round(float(X(x)), 3), round(float(Y(y)), 5)])

vp.write_csv(HERE / "fig3e.csv", [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 3e (plot at right): average depth profile of bond damage phi_y for",
    "  pre-stretch lambda = 1.21 (dashed red) and 1.45 (solid red), and the black dash-dot line labelled phi_b=0.02%.",
    "Columns: series; piece = 'vertex' (solid polyline), 'dashN' (Nth dash of the dashed line), 'end' (ends of the",
    "  phi_b line); k = running index; y_um = depth y (um), horizontal axis; phi_y_percent = phi_y in % (axis 'phi_y %').",
    "Provenance: tier 2, vector paths in the PDF (page 4). Solid line: its polyline vertices, exact. Dashed line: drawn",
    "  as filled outlines of the dashes (no stroke), so its centre line was computed (vecplot.outline_centreline: midpoints",
    "  between the two sides of each dash, about one line width = 1.03 pt apart); gaps between dashes have no data.",
    "  " + X.describe("x"),
    "  " + Y.describe("y"),
    "Uncertainty: solid line ~0.01 pt (~0.015 um, ~0.0001 %); dashed centre line ~0.2 pt (~0.3 um, ~0.0013 %).",
    "  The phi_b line is drawn at phi_y = %.4f %% (label 0.02%%), from y = %.2f to %.2f um." % (Y(y0), X(x0), X(x1)),
    "  The legend says lambda = 1.21 and 1.45; the caption says the maps are for lambda of 1.2 (i) and 1.45 (ii).",
], ["series", "piece", "k", "y_um", "phi_y_percent"], rows)
print(len(rows), "rows; phi_b at", Y(y0))

import pymupdf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
(ROOT / "work").mkdir(exist_ok=True)
z = 6
clip = pymupdf.Rect(325, 572, 482, 683)
pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
for x, y, col in ov:
    u, v = (x - clip.x0) * z, (y - clip.y0) * z
    dr.ellipse((u - 2, v - 2, u + 2, v + 2), fill=col)
im.save(ROOT / "work" / "fig3e_overlay.png")
