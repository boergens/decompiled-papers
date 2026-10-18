"""Fig. 2d (right-hand plot) of Zhao et al. 2025: crack opening profiles (circles), parabolic fits and the dashed
blunting circles, read from the PDF's vector paths (page 3). Writes fig2d.csv and work/fig2d_overlay.png.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import vecplot as vp  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
pg = vp.page(PDF, 3)
# frame: x (page) 326.45-460.23, y (page) 196.68-300.77. Horizontal axis "y (mm)", vertical axis "x (mm)".
# Tick marks (filled 1 pt rectangles): horizontal at 358.97, 392.42, 425.87, 459.31 (centres); labels -0.5, 0, 0.5
# (the 459.31 tick has no label). Vertical: ticks at 300.77 (frame), 266.08, 231.38, 196.68; labels -0.5 at
# 266.08 and -1 at 231.38 (unlabelled ends extrapolate to 0 and -1.5).
H = vp.Axis([(358.97, -0.5), (392.42, 0.0), (425.87, 0.5)])
V = vp.Axis([(266.08, -0.5), (231.38, -1.0)])
SER = {"#d95319": "lambda=1.21", "#0072bd": "lambda=1.41"}

ds = vp.drawings_in(pg, (320, 190, 470, 340))
rows, ov = [], []
# 1) profile markers: open circles drawn as filled rings (8 Bezier pieces); centre = bbox centre
for d in ds:
    if d["type"] == "f" and d["fillc"] in SER and len(d["items"]) == 8:
        cx, cy = vp.bbox_centre(d)
        rows.append([SER[d["fillc"]], "profile_point", round(float(H(cx)), 5), round(float(V(cy)), 5)])
        ov.append((cx, cy, (255, 0, 255)))
n_pts = len(rows)
# 2) parabolic fits: one cubic Bezier each (with tiny straight end pieces); sampled at 81 points
FIT = {161: "lambda=1.41", 163: "lambda=1.21"}
alld = pg.get_drawings()
fitinfo = {}
for idx, s in FIT.items():
    its = alld[idx]["items"]
    c = [its[1][k] for k in range(1, 5)]
    t = np.linspace(0, 1, 81)[:, None]
    P = np.array([[p.x, p.y] for p in c])
    B = ((1 - t) ** 3) * P[0] + 3 * ((1 - t) ** 2) * t * P[1] + 3 * (1 - t) * t ** 2 * P[2] + t ** 3 * P[3]
    pts = [(its[0][1].x, its[0][1].y)] + [tuple(b) for b in B] + [(its[2][2].x, its[2][2].y)]
    hy = H([p[0] for p in pts]); vx = V([p[1] for p in pts])
    a2, a1, a0 = np.polyfit(hy, vx, 2)
    y0 = -a1 / (2 * a2); x0 = a0 - a1 ** 2 / (4 * a2)
    fitinfo[s] = (a2, y0, x0, 1 / (2 * abs(a2)))
    for py, px in zip(hy, vx):
        rows.append([s, "parabolic_fit", round(float(py), 5), round(float(px), 5)])
    ov += [(p[0], p[1], (0, 200, 0)) for p in pts]
# 3) dashed circles (blunting radius drawn as a circle): dash polygons, circle fitted through all their vertices
CIRC = {162: "lambda=1.41", 164: "lambda=1.21"}
circinfo = {}
for idx, s in CIRC.items():
    v = np.array(vp.vertices(alld[idx]))
    hy, vx = H(v[:, 0]), V(v[:, 1])
    A = np.c_[2 * hy, 2 * vx, np.ones(len(hy))]
    sol, *_ = np.linalg.lstsq(A, hy ** 2 + vx ** 2, rcond=None)
    cy_, cx_ = sol[0], sol[1]
    r = np.sqrt(sol[2] + cy_ ** 2 + cx_ ** 2)
    circinfo[s] = (cy_, cx_, r, float(np.ptp(hy)), float(np.ptp(vx)))
    for py, px in zip(hy, vx):
        rows.append([s, "dashed_circle_vertex", round(float(py), 5), round(float(px), 5)])
    ov += [(p[0], p[1], (0, 160, 255)) for p in v]

com = [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 2d (right-hand plot): crack opening profiles near the crack tip for",
    "  lambda = 1.21 (orange-red circles, red fit and dashed circle) and lambda = 1.41 (blue), with parabolic fits.",
    "  Colour-to-lambda mapping from the panel's labels: r_b1 = 130 um (red text) / r_b2 = 260 um (blue text) and the",
    "  red/blue frames of the lambda = 1.21 / 1.41 photographs on the left of panel d.",
    "Columns: series; kind = profile_point (centre of one open-circle marker), parabolic_fit (the drawn fit line, Bezier",
    "  sampled at 81 points plus its two short straight end pieces), dashed_circle_vertex (vertices of the dash",
    "  polygons of the dashed circular arc (upper part of a circle) drawn at the tip; not data, kept to document it); y_mm = horizontal",
    "  axis 'y (mm)'; x_mm = vertical axis 'x (mm)' (0 at the bottom frame, negative upwards, as labelled).",
    "Provenance: tier 2, vector paths in the PDF (page 3); marker centres = bbox centres of the ring paths.",
    "  " + H.describe("y (horizontal)"),
    "  " + V.describe("x (vertical)") + "; only two labelled ticks (-0.5, -1); the frame/tick at 300.77 pt",
    "  (unlabelled) maps to x = %.4f mm and the top frame 196.68 pt to %.4f mm." % (V(300.77), V(196.68)),
    "  Note: the two axes have different scales on the page (%.2f pt/mm horizontal, %.2f pt/mm vertical)." % (1 / H.a, abs(1 / V.a)),
    "Uncertainty: ~0.0003 mm (PDF precision); marker diameter is ~6.6 pt = ~0.1 mm. The red fit line runs past the",
    "  bottom frame on the page (clipped in the figure); its points below x = 0 are kept here.",
]
for s, (a2, y0, x0, R) in fitinfo.items():
    com.append(f"Parabola fitted by me to the drawn {s} fit line: x = {a2:.4f}*(y - {y0:.4f})^2 + {x0:.4f} (mm);"
               f" apex radius of curvature 1/(2|a|) = {R*1000:.0f} um"
               f" (printed r_b: 130 um for 1.21, 260 um for 1.41)")
for s, (cy_, cx_, r, w, h) in circinfo.items():
    com.append(f"Dashed circle {s}: centre y = {cy_:.4f}, x = {cx_:.4f} mm, least-squares radius {r*1000:.0f} um "
               f"(extent {w*1000:.0f} x {h*1000:.0f} um in data units; dash width included)")
vp.write_csv(HERE / "fig2d.csv", com, ["series", "kind", "y_mm", "x_mm"], rows)
print(n_pts, "markers;", len(rows), "rows")
for c in com[-4:]:
    print(c)

import pymupdf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
(ROOT / "work").mkdir(exist_ok=True)
z = 5
clip = pymupdf.Rect(320, 190, 470, 318)
pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
for x, y, col in ov:
    u, v = (x - clip.x0) * z, (y - clip.y0) * z
    dr.ellipse((u - 2, v - 2, u + 2, v + 2), fill=col)
im.save(ROOT / "work" / "fig2d_overlay.png")
