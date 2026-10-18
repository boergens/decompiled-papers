"""Digitize Fig 4 of Lee et al. 2018 (PLoS ONE 13:e0206172) -> fig4.csv (tier 3).

Fig 4 is a MATLAB 3D surface plot (orthographic view) of predicted yield [%] over m (substrates per batch) and
c (sections per substrate), embedded as a 300 ppi raster (p. 9, xref 131). A single 2D image cannot give the whole
surface, but its outer boundary can be read exactly: each boundary curve of the surface lies in a known plane
(c = c_max, m = m_max, c = c_min, m = m_min), and in an orthographic view a point in a known plane maps to the
image by an affine map, which is inverted here.
  1. axis lines: least-squares lines through the dark grey pixels of the m axis (front left) and c axis (front right);
     the z axis is the vertical line at column ~253;
  2. tick marks: each tick is a short slanted line; its crossing with the axis line (intercept of a linear fit of
     the tick pixels) gives the axis position of m = 0, 20; c = 0, 20, ..., 80; z = 0, 20, ..., 100;
  3. affine projection screen = O + m*A + c*B + z*C built from the tick spacings; the box corners give the axis
     limits (c_min, m_min) of the plotted grid;
  4. surface outline: outer contour of the coloured (saturated) pixels after closing the black mesh lines; split
     at the apex, the right corner, the bottom corner and the corner nearest the box corner (m_min, c_min, 0);
  5. each piece is mapped into its plane.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
import pymupdf  # noqa: E402
import digitize_common as dc  # noqa: E402

doc = pymupdf.open(str(ROOT / "source/lee2018_lasso.pdf"))
pix = pymupdf.Pixmap(doc, 131)
a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(int)
g = a.mean(2); sat = a.max(2) - a.min(2)
dark = (g < 170) & (sat < 40)
yy, xx = np.nonzero(dark)


def fitline(p0, p1, w):
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    for _ in range(4):
        d = (p1 - p0) / np.linalg.norm(p1 - p0); n = np.array([-d[1], d[0]])
        rel = np.stack([xx - p0[0], yy - p0[1]], 1)
        t = rel @ d; s = rel @ n
        sel = (np.abs(s) < w) & (t > -50) & (t < np.linalg.norm(p1 - p0) + 50)
        k, b = np.polyfit(xx[sel], yy[sel], 1)
        p0 = np.array([p0[0], k * p0[0] + b]); p1 = np.array([p1[0], k * p1[0] + b]); w = max(2.5, w / 2)
    return k, b


ZCOL = 253.5                                   # z axis: columns 253-254 are dark over rows 608-1462
km, bm = fitline((253, 1461), (1120, 2065), 12)    # starting guesses read off the page render
kc, bc = fitline((1120, 2065), (1970, 1465), 12)
L = np.array([ZCOL, km * ZCOL + bm])               # m axis meets z axis
xF = (bc - bm) / (km - kc); F = np.array([xF, km * xF + bm])   # m axis meets c axis
xR = max(x for x in range(1500, 2100) if dark[int(round(kc * x + bc)) - 2:int(round(kc * x + bc)) + 3, x].any())
R = np.array([xR, kc * xR + bc])                 # right end of the c axis line
dk2 = (g < 190) & (sat < 60); yy2, xx2 = np.nonzero(dk2)


def intercepts(p0, p1, side, t_list, win):
    """Crossing points (axis parameter t from p0) of the slanted tick marks with the axis line."""
    Lh = np.linalg.norm(p1 - p0); d = (p1 - p0) / Lh; n = np.array([-d[1], d[0]]) * side
    rel = np.stack([xx2 - p0[0], yy2 - p0[1]], 1); t = rel @ d; s = rel @ n
    out = []
    for t0 in t_list:
        sel = (s > 4) & (s < 16) & (np.abs(t - t0) < win)
        k, b0 = np.polyfit(s[sel], t[sel], 1)
        out.append(b0)
    return np.array(out), d


tm, dm = intercepts(L, F, +1, [0, 211], 30)              # m = 0, 20 (the other m ticks are crowded by labels)
tcs, dcv = intercepts(F, R, +1, [-12, 250, 513, 775, 1037], 15)    # c = 0..80
tz, dz = intercepts(L, np.array([ZCOL, 600.0]), -1, [0, 170, 341, 511, 682, 852], 15)   # z = 0..100
sm = (tm[1] - tm[0]) / 20
fc, rc, sc = dc.fit_axis(tcs, [0, 20, 40, 60, 80])
fz, rz, sz = dc.fit_axis(tz, [0, 20, 40, 60, 80, 100])
A = dm * sm; B = dcv / sc; C = dz / sz
# screen = O + m*A + c*B + z*C. On the m axis (c = c_min): screen(m) = L + dm*(tm[0] + m*sm);
# on the c axis (m = m_F): screen(c) = F + dcv*(c - c0)/sc with c0 = fc(0) (c at F)
m_L = -tm[0] / sm                 # m at the corner L
m_F = (np.linalg.norm(F - L) - tm[0]) / sm   # m at the corner F
c_F = float(fc(0.0))              # c at F (= c_min of the box)
c_R = float(fc(np.linalg.norm(R - F)))
O = F - m_F * A - c_F * B
z_L = float(fz(0.0))
M = np.stack([A, B, C], 1)        # 2x3


def to_plane(p, fixed, val):
    """Invert screen = O + M @ (m, c, z) for a point in the plane 'fixed' = val ('m' or 'c')."""
    if fixed == "c":
        Msub = M[:, [0, 2]]; rhs = p - O - val * B
        m, z = np.linalg.solve(Msub, rhs); return m, val, z
    Msub = M[:, [1, 2]]; rhs = p - O - val * A
    c, z = np.linalg.solve(Msub, rhs); return val, c, z


# 4. surface outline
mask = cv2.morphologyEx((sat > 40).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
i = 1 + int(np.argmax(st[1:, 4]))
cs, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cont = max(cs, key=len)[:, 0, :].astype(float) + 0.5
iT = int(np.argmin(cont[:, 1])); iR = int(np.argmax(cont[:, 0])); iB = int(np.argmax(cont[:, 1]))
iL = int(np.argmin(np.linalg.norm(cont - L, axis=1)))


def arc(i0, i1):
    """Contour points from index i0 to i1 going forward (wrapping)."""
    if i1 >= i0:
        return cont[i0:i1 + 1]
    return np.vstack([cont[i0:], cont[:i1 + 1]])


# OpenCV external contours run counter-clockwise in image coordinates (y down): check orientation
order = [iT, iR, iB, iL]
fwd = arc(iT, iR); ccw = len(fwd) < len(cont) / 2 and fwd[len(fwd) // 2, 0] > cont[iT, 0]
if not ccw:
    cont = cont[::-1]
    iT, iR, iB, iL = [len(cont) - 1 - k for k in (iT, iR, iB, iL)]
pieces = [
    ("edge c=c_max (back right, upper right outline)", arc(iT, iR), "c", c_R),
    ("edge m=m_max (front right, lower right outline)", arc(iR, iB), "m", m_F),
    ("edge c=c_min (front left, lower left outline)", arc(iB, iL), "c", c_F),
    # the box starts at m ~ 0.24 (~0), but the plotted grid evidently starts at m = 2 (caption: 'we mandate at least two
    # substrates per batch'): the left outline is read in the plane m = 2 (an assumption, flagged in the CSV header)
    ("left outline, read as edge m=2 (assumed plane)", arc(iL, iT), "m", 2.0),
]
rows, over = [], []
for name, pts, fixed, val in pieces:
    pts = pts[::3]                      # every 3rd outline pixel
    for p in pts:
        m, c, z = to_plane(p, fixed, val)
        rows.append([name, float(m), float(c), float(z), float(p[0]), float(p[1])])
        over.append(tuple(p))
hdr = [
    "Lee et al. 2018, PLoS ONE 13(10):e0206172, Fig 4: predicted experiment yield (z axis 'Predicted yield', 0-100) over",
    "  m (# of substrates per batch, axis 0-100) and c (# of sections per substrate, axis 0-80); MATLAB 3D surface plot.",
    "Columns: boundary = which outline piece; m, c, yield = data coordinates of the outline point; px_x, px_y = its position",
    "  in the embedded image (xref 131, 2100 x 2253 px), for checking.",
    "Provenance: tier 3, digitized by fig4_extract.py. Only the OUTLINE of the surface is given (the interior cannot be read",
    "  from one view without the colour scale, which the figure does not show). Each outline piece lies in a plane of",
    "  the plot box, and the orthographic projection is affine, so each outline pixel maps to exactly one (m or c, yield).",
    f"  Projection from the tick marks: m axis {sm:.3f} px per unit, c axis {1 / sc:.3f} px per unit (fit residual {rc:.3f}),",
    f"  z axis {1 / sz:.3f} px per % (fit residual {rz:.3f}). Box corners in data units: m_min = {m_L:.2f}, m_max = {m_F:.2f},",
    f"  c_min = {c_F:.2f}, c_max = {c_R:.2f} (the box spans the plotted grid; c_min ~ 1 and m_max ~ 100 fit the caption's bounds).",
    "  The upper right outline (c = c_max) shows the step-like jumps described in the text.",
    "Uncertainty: +-3 px along the outline (mesh edge line, contour of closed mask), i.e. about +-0.4 % in yield and",
    "  +-0.3 in m or c; more where the outline runs nearly parallel to the z direction (steep parts), where m or c is poorly",
    "  defined. Left outline: read in the plane m = 2 (ASSUMED: the box itself starts at m ~ 0, but the caption mandates at",
    "  least two substrates per batch; reading it at the box edge m ~ 0.24 instead would lower its yields by ~2.5 and raise c",
    "  by ~1.4). Its lowest part (near the corner, yield < ~25) runs into a thin black line drawn along the m = 2, c ~ 1 corner",
    "  and is not reliable there.",
]
dc.write_csv(str(HERE / "fig4.csv"), hdr, ["boundary", "m", "c", "yield", "px_x", "px_y"], rows,
             fmt=["{}", "{:.3f}", "{:.3f}", "{:.3f}", "{:.1f}", "{:.1f}"])
(ROOT / "work").mkdir(exist_ok=True)
# overlay also the axis ticks predicted by the projection
for mt in range(0, 101, 20):
    over.append(tuple(O + mt * A + c_F * B))
for ct in range(0, 81, 20):
    over.append(tuple(O + m_F * A + ct * B))
for zt in range(0, 101, 20):
    over.append(tuple(O + m_L * A + c_F * B + zt * C))
dc.overlay(a.astype(np.uint8), over, str(ROOT / "work/fig4_overlay.png"))
print("m_L", m_L, "m_F", m_F, "c_F", c_F, "c_R", c_R, "z at L", z_L, "rc", rc, "rz", rz, "n", len(rows))
