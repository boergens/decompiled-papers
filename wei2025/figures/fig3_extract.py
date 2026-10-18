"""Digitize Figure 3 (a, b) of Wei et al. 2025 (PDF p. 4): equilibration of the pyramid-0° system.

Source: the embedded 300 ppi raster of Figure 3 (1500 x 608 px, lossless); no vector data in the PDF.
    python3 -I -B figures/fig3_extract.py  -> figures/fig3a.csv, fig3b.csv, work/fig3?_overlay.png

(a) total energy vs time, one red line+symbol series (shaded spheres with a white highlight, ~11 px across,
    overlapping). (b) temperature vs time, Thermostat layer (black, small filled symbols) and Newtonian layer
    (red, open diamonds).
Each series is traced per pixel column (centre and top/bottom of the line+symbol band). Symbols are added where
they can be located: (a) from the white highlight of each sphere (shifted to the sphere centre by the offset
measured on the isolated t = 0 symbol), (b, Newtonian) from the white interior of each open diamond.
"""
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from digitize_common import embedded_image, write_csv, trace_envelope  # noqa: E402
from figA_axes import refine_frame, ticks, fit  # noqa: E402
from figA_markers import draw_cross  # noqa: E402

PDF = HERE.parent / "source" / "wei2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)

a = embedded_image(str(PDF), 4, bbox_near=(117.5, 375.8, 477.5, 521.7))
ai = a.astype(int)
dark = ai.mean(2) < 110
R_, G_, B_ = ai[..., 0], ai[..., 1], ai[..., 2]
red = (R_ - np.maximum(G_, B_)) > 90
black = (ai.max(2) < 110)

XLAB = [0, 200, 400, 600, 800, 1000]


def calib(box, ylab):
    fr = refine_frame(dark, box)
    bx = [t for t, n in ticks(dark, fr, "bottom") if n >= 7]
    ly = [t for t, n in ticks(dark, fr, "left") if n >= 8]
    assert len(bx) == len(XLAB), bx
    assert len(ly) == len(ylab), ly
    return fr, fit(bx, XLAB), fit(ly, ylab)


def env_rows(mask, fr, X, Y, name, half=4):
    L, R, T, B = [int(v) for v in fr]
    env = trace_envelope(mask, L + 12, R - 3, T + 3, B - 3, half_width=half, min_px=2)
    rows = []
    for c, ym, yu, yl in env:
        if ym == ym:
            rows.append([name, "trace", float(X(c)), float(Y(ym)), float(Y(yu)), float(Y(yl))])
    return rows, env


def hole_centres(mask, region, max_area=40):
    """Centroids of small enclosed non-mask holes (white interiors) inside region (c0,c1,r0,r1)."""
    c0, c1, r0, r1 = region
    inv = (~mask[r0:r1, c0:c1]).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(inv, 4)
    out = []
    for i in range(1, n):
        x, y, w, h, ar = st[i]
        if ar <= max_area and x > 0 and y > 0 and x + w < c1 - c0 and y + h < r1 - r0:
            out.append((c0 + cen[i][0], r0 + cen[i][1]))
    return out


# ---------------- panel (a)
fr, (mx, bx_, rx), (my, by_, ry) = calib((144, 760, 14, 466), [-20000, -40000, -60000, -80000, -100000])
L, R, T, B = fr
X = lambda c: mx * np.asarray(c) + bx_  # noqa: E731
Y = lambda r: my * np.asarray(r) + by_  # noqa: E731
rows_a, env_a = env_rows(red, fr, X, Y, "Total energy", half=5)
# symbols: white highlights (min channel > 170, <= 25 px) enclosed by red on >= 3 of 4 sides within 6 px
bright = ai.min(2) > 170
n, lab, st, cen = cv2.connectedComponentsWithStats(bright.astype(np.uint8), 8)
hl = []
for i in range(1, n):
    x, y, w, h, ar = st[i]
    if ar <= 25 and w <= 6 and h <= 6 and L + 5 < x < R - 5 and T + 5 < y < B - 5:
        cx, cy = cen[i]
        xi, yi = int(round(cx)), int(round(cy))
        sides = [red[yi, xi - 6:xi].any(), red[yi, xi + 1:xi + 7].any(), red[yi - 6:yi, xi].any(), red[yi + 1:yi + 7, xi].any()]
        if sum(sides) >= 3:
            hl.append((cx, cy))
# offset highlight -> sphere centre, measured on the isolated t = 0 symbol (lowest red blob)
r0 = int(B) - 60
sub = red[r0:int(B), int(L):int(L) + 80]
wide = np.where(sub.sum(1) >= 6)[0]                     # rows of the disc (the line stub above is ~3 px wide)
d0, d1 = r0 + wide.min(), r0 + wide.max()
cols = np.where(red[d0:d1 + 1, int(L):int(L) + 80].any(0))[0]
c0x, c0y = int(L) + (cols.min() + cols.max()) / 2, (d0 + d1) / 2   # centre of the t = 0 sphere's bounding box
# its highlight: bright pixels inside the disc bounding box with red on >= 3 of 4 sides
hx_, hy_ = [], []
for yy in range(d0, d1 + 1):
    for xx in range(int(L) + cols.min(), int(L) + cols.max() + 1):
        if ai[yy, xx].min() > 170:
            sides = [red[yy, xx - 6:xx].any(), red[yy, xx + 1:xx + 7].any(), red[yy - 6:yy, xx].any(), red[yy + 1:yy + 7, xx].any()]
            if sum(sides) >= 3:
                hx_.append(xx)
                hy_.append(yy)
hx, hy = np.mean(hx_), np.mean(hy_)
off = (c0x - hx, c0y - hy)
sym_a = [(c0x, c0y)] + [(x + off[0], y + off[1]) for x, y in hl]
sym_a.sort()
for x, y in sym_a:
    rows_a.append(["Total energy", "symbol", float(X(x)), float(Y(y)), "", ""])
write_csv(str(HERE / "fig3a.csv"), [
    "Wei et al. 2025, Figure 3(a): total energy (kcal/mol) vs time (ps), pyramid-0° quartz indenter-epoxy system, equilibration.",
    "Columns: series; kind = trace (one row per pixel column: E_mid = centre of the line+symbol band, E_upper/E_lower = its top and",
    "  bottom moved inward by the symbol radius, so they differ only on steep parts) or symbol (centre of one plotted sphere,",
    "  found from its white highlight and shifted by the highlight-to-centre offset measured on the isolated t = 0 symbol,",
    f"  ({off[0]:+.1f}, {off[1]:+.1f}) px; E_upper/E_lower empty); time_ps; E_kcal_mol.",
    "  The symbols are ~5.1 px = 10 ps apart (measured spacing), i.e. probably one sample per 10 ps; overlapping spheres whose",
    "  highlight is hidden are missing, so the symbol list is incomplete in the dense part (t > ~300 ps).",
    "Provenance: tier 3, digitized by fig3_extract.py from the embedded 300 ppi raster (no vector data in the PDF);",
    "  series mask R - max(G, B) > 90.",
    f"Calibration: x on the 6 labelled major ticks 0-1000 ps (max residual {rx:.2f} ps); y on the 5 labelled major ticks",
    f"  -20000 to -100000 kcal/mol (max residual {ry:.1f}); the top frame line maps to {Y(T):.0f} (labelled 0).",
    f"Plot frame: time {X(L):.1f} to {X(R):.1f} ps, energy {Y(B):.0f} to {Y(T):.0f} kcal/mol (linear axes).",
    f"Uncertainty: about +-{2 * abs(mx):.1f} ps and +-{2 * abs(my):.0f} kcal/mol (2 px) for trace rows; symbols +-{3 * abs(my):.0f} kcal/mol.",
], ["series", "kind", "time_ps", "E_kcal_mol", "E_upper_kcal_mol", "E_lower_kcal_mol"], rows_a,
    fmt=["{}", "{}", "{:.2f}", "{:.0f}", "{:.0f}", "{:.0f}"])
im = a.copy()
for c, ym, yu, yl in env_a:
    if ym == ym:
        im[int(round(ym)), int(c)] = (0, 0, 0)
for x, y in sym_a:
    draw_cross(im, x, y, (0, 200, 0), size=3)
from PIL import Image  # noqa: E402
Image.fromarray(im[:int(B) + 5, :int(R) + 5]).save(WORK / "fig3a_overlay.png")
print("a: x res", rx, "y res", ry, "top ->", Y(T), "symbols", len(sym_a), "offset", off)
print("a: E at t=0 symbol", Y(c0y), "last trace", rows_a[len(env_a) - 1] if env_a.size else None)

# ---------------- panel (b)
fr, (mx, bx_, rx), (my, by_, ry) = calib((880, 1495, 14, 466), [300, 280, 260, 240, 220, 200, 180, 160])
L, R, T, B = fr
X = lambda c: mx * np.asarray(c) + bx_  # noqa: E731
Y = lambda r: my * np.asarray(r) + by_  # noqa: E731
legend = (1070, 1350, 222, 297)
redm, blk = red.copy(), black.copy()
for m in (redm, blk):
    m[legend[2]:legend[3], legend[0]:legend[1]] = False
    m[:, :int(L) + 12] = False          # frame and inward ticks
    m[int(B) - 12:, :] = False
    m[:int(T) + 3, :] = False
    m[:, int(R) - 3:] = False
rows_b, env_t = env_rows(blk, fr, X, Y, "Thermostat layer", half=3)
rb, env_n = env_rows(redm, fr, X, Y, "Newtonian layer", half=4)
rows_b += rb
# Newtonian open diamonds: white interiors enclosed by red (area <= 40 px)
holes = hole_centres(red, (int(L) + 3, int(R) - 3, int(T) + 3, int(B) - 3), max_area=40)
holes = [h for h in holes if not (legend[0] <= h[0] <= legend[1] and legend[2] <= h[1] <= legend[3])]
holes.sort()
for x, y in holes:
    rows_b.append(["Newtonian layer", "symbol", float(X(x)), float(Y(y)), "", ""])
write_csv(str(HERE / "fig3b.csv"), [
    "Wei et al. 2025, Figure 3(b): temperature (K) vs time (ps) of the Thermostat layer and the Newtonian layer, pyramid-0° system.",
    "Columns: series; kind = trace (one row per pixel column: T_mid = centre of the line+symbol band, T_upper/T_lower = its top and",
    "  bottom moved inward by the symbol radius, so they differ only on steep parts, e.g. the jump at t ~ 0-10 ps) or symbol",
    "  (Newtonian layer only: centre of an open diamond, the centroid of its white interior); time_ps; T_K.",
    "  Thermostat-layer symbols (small filled circles on the line) cannot be separated from the line: trace only.",
    "  Where the black Thermostat curve lies over the red Newtonian curve (t > ~550 ps) the red trace has gaps or follows",
    "  the visible red edge only. Open diamonds whose interior is closed off by neighbours are missing from the symbol list.",
    "Provenance: tier 3, digitized by fig3_extract.py from the embedded 300 ppi raster (no vector data in the PDF);",
    "  masks: red R - max(G, B) > 90, black max(R, G, B) < 110; legend box masked out.",
    f"Calibration: x on the 6 labelled major ticks 0-1000 ps (max residual {rx:.2f} ps); y on the 8 labelled major ticks",
    f"  160-300 K (max residual {ry:.2f} K); top frame line maps to {Y(T):.1f} K (labelled 320), bottom to {Y(B):.1f} (labelled 140).",
    f"Plot frame: time {X(L):.1f} to {X(R):.1f} ps, temperature {Y(B):.1f} to {Y(T):.1f} K (linear axes).",
    f"Uncertainty: about +-{2 * abs(mx):.1f} ps and +-{2 * abs(my):.2f} K (2 px).",
], ["series", "kind", "time_ps", "T_K", "T_upper_K", "T_lower_K"], rows_b,
    fmt=["{}", "{}", "{:.2f}", "{:.2f}", "{:.2f}", "{:.2f}"])
im = a.copy()
for env, col in ((env_t, (0, 160, 255)), (env_n, (0, 0, 0))):
    for c, ym, yu, yl in env:
        if ym == ym:
            im[int(round(ym)), int(c)] = col
for x, y in holes:
    draw_cross(im, x, y, (0, 200, 0), size=3)
Image.fromarray(im[:int(B) + 5, int(L) - 5:]).save(WORK / "fig3b_overlay.png")
print("b: x res", rx, "y res", ry, "top", Y(T), "bottom", Y(B), "diamonds", len(holes))
