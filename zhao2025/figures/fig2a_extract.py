"""Fig. 2a of Zhao et al. 2025 (Nat. Commun. 16:3203): force-displacement curves, read from the PDF's vector paths.

Writes fig2a.csv and work/fig2a_overlay.png. Run from anywhere: python3 -I -B figures/fig2a_extract.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import vecplot as vp  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
pg = vp.page(PDF, 3)
BOX = (140, 55, 300, 166)          # plot frame of panel a (frame 142.1-298.67 x 58.35-164.46 pt)

# ticks: tick marks (vector) at these page coordinates carry these printed labels
X = vp.Axis([(142.10, 0), (194.27, 10), (246.50, 20), (298.67, 30)])
Y = vp.Axis([(164.46, 0), (111.43, 0.1), (58.35, 0.2)])

SERIES = {"#234462": "lambda=1.16", "#3975a7": "lambda=1.28", "#6fa2ce": "lambda=1.41"}
rows = []
overlay = []
for d in vp.drawings_in(pg, BOX):
    if d["type"] != "s" or d["stroke"] not in SERIES:
        continue
    pts = vp.vertices(d)
    if len(pts) == 2 and abs(pts[0][1] - pts[1][1]) < 1e-3 and pts[0][0] > 230 and pts[0][1] < 95:
        continue                     # legend sample line
    for k, (x, y) in enumerate(pts):
        rows.append([SERIES[d["stroke"]], d["index"], k, round(float(X(x)), 4), round(float(Y(y)), 6)])
    overlay.append((d["stroke"], pts))

rows.sort(key=lambda r: (r[0], r[1], r[2]))
vp.write_csv(HERE / "fig2a.csv", [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 2a: force-displacement curves during cutting for three stretch ratios.",
    "Columns: series = curve as labelled in the legend (lambda = stretch ratio); path = index of the PDF drawing the",
    "  vertices come from (each curve is drawn as several separate paths: short pieces near f = 0 at the start, then one",
    "  long path); vertex = order of the vertex within that path; delta_mm = displacement delta (mm); f_N = force f (N).",
    "Provenance: tier 2, vector paths in the PDF (page 3), every polyline vertex (Bezier pieces: end points only).",
    "  " + X.describe("x"),
    "  " + Y.describe("y"),
    "Uncertainty: PDF coordinate precision ~0.01 pt = ~0.002 mm in x and ~2e-5 N in y; the curves are drawn with a",
    "  0.4 pt line. Curves stop at the right frame (delta = 30 mm), i.e. they are clipped there in the figure.",
    "  A few vertices lie a hair below f = 0 (down to ~-0.0002 N), as drawn.",
    "The red dash-dot 'Steady-state regime' box (not data) spans delta 9.51-25.93 mm, f 0.0177-0.1268 N.",
], ["series", "path", "vertex", "delta_mm", "f_N"], rows)
print(len(rows), "rows")

# overlay on a 4x render of the region
import pymupdf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
(ROOT / "work").mkdir(exist_ok=True)
z = 4
clip = pymupdf.Rect(120, 50, 305, 180)
pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
for col, pts in overlay:
    for x, y in pts[::3]:
        u, v = (x - clip.x0) * z, (y - clip.y0) * z
        dr.point((u, v), fill=(255, 0, 255))
im.save(ROOT / "work" / "fig2a_overlay.png")
