"""Fig. 6b (p. 8): profile of section B-B' of the actual cutting edge (raw data + fitted arc).
Vector paths -> fig6b.csv.

Run: python3 -I -B figures/fig6b_extract.py   (from any directory)
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import vec  # noqa: E402

HERE = Path(__file__).resolve().parent
PAGE, CLIP = 8, (300, 90, 512, 256)
RED, BLACK = (0.87, 0.03, 0.02), (0, 0, 0)
DIV = 20.0  # nm per tick interval, both axes ("20 nm/div.")

ds = vec.drawings(PAGE, CLIP)
L, T, R, B = vec.frame(ds)
xt = [x for x in vec.tick_rects(ds, "x", B) if L + 3 < x < R - 3]
yt = [y for y in vec.tick_rects(ds, "y", L) if T + 3 < y < B - 3]
sx = DIV / np.mean(np.diff(xt))
sy = DIV / np.mean(np.diff(yt))


def to_nm(x, y):
    return (x - L) * sx, (B - y) * sy


rows = []
# raw data: red open circles (4 Bezier strokes each)
circ = sorted([d["rect"] for d in ds if vec.colour_is(d.get("color"), RED) and len(d["items"]) == 4
               and all(it[0] == "c" for it in d["items"])], key=lambda r: r.x0)
for r in circ:
    x, y = to_nm(*vec.centre(r))
    clipped = "partly outside frame (clipped)" if r.x1 > R else ""
    rows.append(("Raw data (circles)", round(x, 3), round(y, 3), clipped))
# red line through the raw data: thick segments as filled 5-point polygons; the segment end points are
# the midpoints of the polygon's short ends -> use the polygon's first/last vertices pairwise
red_poly = sorted([d for d in ds if vec.colour_is(d.get("fill"), RED) and len(d["items"]) >= 4], key=lambda d: d["rect"].x0)
line_pts = []
for d in red_poly:
    p = [(it[1].x, it[1].y) for it in d["items"] if it[0] == "l"] + [(d["items"][-1][2].x, d["items"][-1][2].y)]
    # the polygon's vertices form two small caps (about 1 pt square) at the segment ends;
    # group them by proximity to the first vertex and take each cap's bbox centre
    p = np.array(p)
    near = np.hypot(*(p - p[0]).T) < 2.0
    for grp in (p[near], p[~near]):
        line_pts.append(((grp[:, 0].min() + grp[:, 0].max()) / 2, (grp[:, 1].min() + grp[:, 1].max()) / 2))
verts = []
for q in sorted(line_pts):
    if not verts or abs(q[0] - verts[-1][0]) > 0.3 or abs(q[1] - verts[-1][1]) > 0.3:
        verts.append(q)
for q in verts:
    x, y = to_nm(*q)
    rows.append(("Raw data (red line vertices)", round(x, 3), round(y, 3), "outside frame (clipped)" if q[0] > R + 0.5 else ""))
cc = np.array([vec.centre(r) for r in circ])
vv = np.array(verts)
dmin = [float(np.min(np.hypot(*(vv - c).T))) for c in cc]
# fitted curve: its vertices are marked by tiny black strokes (0.16 pt wide, < 0.3 pt long)
fit_pts = sorted([vec.centre(d["rect"]) for d in ds if vec.colour_is(d.get("color"), BLACK)
                  and d["rect"].width < 0.4 and d["rect"].height < 0.4])
fit_nm = np.array([to_nm(x, y) for x, y in fit_pts])
for x, y in fit_nm:
    rows.append(("Fitted curve (vertices)", round(float(x), 3), round(float(y), 3), ""))

# circle fit (algebraic, Kasa) to the fitted-curve vertices
A = np.c_[2 * fit_nm[:, 0], 2 * fit_nm[:, 1], np.ones(len(fit_nm))]
bb = (fit_nm ** 2).sum(1)
cx, cy, c = np.linalg.lstsq(A, bb, rcond=None)[0]
rad = np.sqrt(c + cx ** 2 + cy ** 2)
# compare circles with the red line: distance of each circle centre to the nearest red polygon centre line
hdr = [
    "zhangk2020 Fig. 6b (p. 8): Profile of Section B-B' (Figure 6. Measured diamond tool cutting edge).",
    "Provenance: tier 2, vector paths in the PDF (PyMuPDF get_drawings).",
    "Axes carry no numbers: 'X-position 20 nm/div.' and 'Z-position 20 nm/div.'; origins are arbitrary:",
    f"x_nm = 0 at the left frame line ({L:.2f} pt), z_nm = 0 at the bottom frame line ({B:.2f} pt);",
    f"x ticks at {', '.join(f'{(x - L) * sx:.2f}' for x in xt)} nm ({np.mean(np.diff(xt)):.3f} pt per 20 nm), "
    f"z ticks at {', '.join(f'{(B - y) * sy:.2f}' for y in yt)} nm ({np.mean(np.diff(yt)):.3f} pt per 20 nm); frame {(R - L) * sx:.1f} nm x {(B - T) * sy:.1f} nm.",
    "series 'Raw data (circles)': centres of the red open circles; 'Raw data (red line vertices)': vertices of the red line, which",
    f"passes through every circle centre (max distance {max(dmin):.3f} pt) and runs on to the left and right frame;",
    "series 'Fitted curve (vertices)': vertices of the black thick 'Fitted curve', marked in the PDF by tiny black strokes.",
    f"Check (decompiler): least-squares circle through the fitted-curve vertices has radius {rad:.2f} nm "
    f"(centre x {cx:.2f}, z {cy:.2f} nm); the plot label says R_tool_m = 40.32 nm.",
    "Uncertainty: about 0.1 nm (PDF precision 0.01-0.1 pt; 1 pt = 0.52 nm in x, 0.59 nm in z).",
]
vec.write_csv(HERE / "fig6b.csv", hdr, ["series", "x_nm", "z_nm", "note"], rows)
print("\n".join(hdr))
print(len(circ), "circles,", len(fit_pts), "fit vertices,", len(line_pts), "red line segments")

vec.overlay_pts(PAGE, CLIP, [vec.centre(r) for r in circ] + list(fit_pts) + verts, HERE.parent / "work" / "fig6b_overlay.png")
