"""Extract Fig. 4g of Hua et al. 2015 (main PDF p.6) from the vector paths in the PDF -> fig4g_vector.csv

Panel g: 'Mean inter-error distance (µm)' (log y, 10^1 .. 10^7) against '# annotators' (linear), three data
sets in red ('e1088 (retina)'), green ('This protocol (cortex)') and blue ('rOTO (cortex)'); solid lines =
full neurite tracing, dashed lines = focused re-annotation (caption).

    python3 -I fig4g_vector_extract.py   -> fig4g_vector.csv (+ ../work/fig4g_overlay.png)

Axis calibration (page coordinates, points):
  x: the tick marks labelled 10 and 20 at x=314.396 and 335.923 (2.1527 pt per annotator). The left tick,
     labelled "1", sits on the frame corner at x=292.869, which this calibration puts at 0.00 annotators,
     not 1; the solid lines start one unit to the right of it (x=295.019 -> 1.00) and their vertices fall
     on whole numbers 1..23 (max deviation printed below). So the "1" label is at the wrong place
     (or the tick is meant as 0); the 10/20 calibration is used.
  y: log10; major ticks at y = 271.508 (frame bottom), 257.341, 243.202, 229.034, 214.894, 200.726, 186.559
     = 10^1 .. 10^7 (labels at 10^1, 10^3, 10^5, 10^7), least squares.
Drawing order in the PDF: the three dashed curves are first all drawn in blue, then the blue one is drawn
again, then red and green are drawn over two of the blue copies. Only the visible (last-drawn) strokes are kept.
"""
import csv
import os

import numpy as np
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "../source/hua2015.pdf")
PAGE = 6
FRAME = (292.869, 186.559, 348.051, 271.508)
NAMES = {(1.0, 0.0, 0.0): "e1088 (retina)", (0.0, 1.0, 0.0): "This protocol (cortex)",
         (0.0, 0.0, 1.0): "rOTO (cortex)"}

doc = pymupdf.open(PDF)
page = doc[PAGE - 1]


def inside(r, box, tol=0.5):
    return r.x1 >= box[0] - tol and r.x0 <= box[2] + tol and r.y1 >= box[1] - tol and r.y0 <= box[3] + tol


draw = [d for d in page.get_drawings() if inside(d["rect"], FRAME)]
xt = sorted({round(d["rect"].x0, 3) for d in draw if d.get("color") == (0.0, 0.0, 0.0)
             and d["rect"].width == 0 and abs(d["rect"].height - 1.101) < 0.01 and d["rect"].y1 > 270})
yt = sorted({round(d["rect"].y0, 3) for d in draw if d.get("color") == (0.0, 0.0, 0.0)
             and d["rect"].height == 0 and abs(d["rect"].width - 1.075) < 0.01})
print("x ticks", xt, "major y ticks", yt)
assert xt == [292.869, 314.396, 335.923], xt
XA, XB = 314.396, 335.923
fx = lambda X: 10 + 10 * (np.asarray(X, float) - XA) / (XB - XA)
ymaj = np.array([271.508, 257.341, 243.202, 229.034, 214.894, 200.726, 186.559])
assert all(any(abs(a - b) < 0.002 for b in yt) for a in ymaj[1:]), yt   # 10^1 tick = x axis line
dec = np.arange(1, 8.0)
A = np.vstack([ymaj, np.ones(7)]).T
(m, b), *_ = np.linalg.lstsq(A, dec, rcond=None)
yres = np.max(np.abs(A @ [m, b] - dec))
fy = lambda Y: 10 ** (m * np.asarray(Y, float) + b)
print("left tick ('1') ->", fx(292.869), "; y residual (decades)", yres)

series = [d for d in draw if d.get("width") == 0.75 and tuple(d.get("color") or ()) in NAMES
          and d["rect"].x1 < 349 and len(d["items"]) > 1]
# keep only the last-drawn stroke for each geometry
seen = {}
for i, d in enumerate(series):
    key = tuple((round(it[-1].x, 1), round(it[-1].y, 1)) for it in d["items"]) + (d.get("dashes"),)
    seen[key] = (i, d)
rows, pix = [], []
dev = 0
for key, (i, d) in sorted(seen.items(), key=lambda kv: kv[1][0]):
    name = NAMES[tuple(d["color"])]
    dashed = d.get("dashes") not in (None, "[] 0")
    style = "dashed (focused re-annotation)" if dashed else "solid (full neurite tracing)"
    pts = [d["items"][0][1]] + [it[-1] for it in d["items"]]
    for p in pts:
        x, y = float(fx(p.x)), float(fy(p.y))
        flag = ""
        if p.x > FRAME[2] - 0.001:
            flag = "clipped_at_right_frame"
        if not dashed:
            dev = max(dev, abs(x - round(x)))
        rows.append((name, style, x, y, flag))
        pix.append((p.x, p.y))
print("solid-line vertices: max deviation from whole numbers of annotators", dev)

with open(os.path.join(HERE, "fig4g_vector.csv"), "w", newline="") as f:
    for h in [
        "Hua, Laserstein & Helmstaedter 2015 Nat Commun 6:7923, Fig. 4g: prediction of tracing accuracy against the number",
        "  of annotators for three data sets (legend: e1088 (retina) red, This protocol (cortex) green, rOTO (cortex) blue).",
        "  Solid lines: full neurite tracings; dashed lines: focused re-annotation of the disagreeing locations (caption).",
        "Columns: series (legend text); style; n_annotators = '# annotators' (linear); mean_inter_error_distance_um =",
        "  'Mean inter-error distance (µm)' (log10 axis 10^1..10^7); flag: clipped_at_right_frame = the line is cut by the",
        "  right end of the axis box (the red dashed line ends there below 10^7).",
        "Provenance: tier 2, vector paths in the PDF (fig4g_vector_extract.py): every vertex of each visible line.",
        "  x calibrated on the ticks labelled 10 and 20; the tick labelled '1' at the left frame corner maps to",
        f"  {fx(292.869):.3f} with this calibration (the label is misplaced, see fig4g_vector_extract.py); solid-line vertices sit on",
        f"  whole numbers 1..23 within {dev:.4f}. y: 7 decade ticks, max residual {yres:.1e} decades.",
        "  The dashed lines have only 4 vertices each, at exactly 10^2, 10^3, 10^5, 10^7 µm (as drawn).",
        "  The PDF also contains blue copies of the red and green dashed lines underneath them (not visible; omitted).",
        "Uncertainty: exact up to the PDF's coordinate precision (0.001 pt = 0.0005 annotators, 7e-5 decades).",
    ]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["series", "style", "n_annotators", "mean_inter_error_distance_um", "flag"])
    for r in rows:
        w.writerow([r[0], r[1], f"{r[2]:.3f}", f"{r[3]:.5g}", r[4]])
print(len(rows), "rows")

from PIL import Image, ImageDraw  # noqa: E402
clip = pymupdf.Rect(280, 180, 352, 280)
z = 8
pm = page.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
dr = ImageDraw.Draw(im)
for x, y in pix:
    u, v = (x - clip.x0) * z, (y - clip.y0) * z
    dr.ellipse([u - 4, v - 4, u + 4, v + 4], outline=(255, 0, 255), width=2)
im.save(os.path.join(HERE, "../work/fig4g_overlay.png"))
