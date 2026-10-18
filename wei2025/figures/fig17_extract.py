"""Digitize Figure 17 (left scatter plot) of Wei et al. 2025 (IJNAMG 49:2949), PDF p. 13.

Source: the embedded 300 ppi JPEG of Figure 17 (1500 x 670 px); the plot is its left part, the right part holds two
MD snapshots. No vector data in the PDF.
    python3 -I -B figures/fig17_extract.py  -> figures/fig17.csv, work/fig17_overlay.png
Symbols are shaded spheres (~16 px) in four colours. Mask of all non-light pixels, holes filled, opening with a
9 px disk (removes the 4 px dashed 1.0 line, the dashed circles, the arrows and the "1.0" label), one blob per symbol;
series from the blob's mean colour. The y axis is broken: the segment below the break (0.5-2.1) and the one above it
(4.05-4.3) are calibrated separately on their own ticks.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import embedded_image, write_csv, overlay  # noqa: E402
from figB_common import frame, ticks_h, ticks_v, linfit, groups  # noqa: E402

PDF = HERE.parent / "source" / "wei2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)
a = embedded_image(str(PDF), 13, bbox_near=(117.5, 364.6, 477.5, 525.2))
ai = a.astype(int)
dark = ai.mean(2) < 130
f = frame(dark, (0, 0, 900, 620))
L, R, T, B = f["left"], f["right"], f["top"], f["bottom"]

# x: major ticks (long, inward) 0.5 ... 2.5, plus the left frame at 0.0 as a check
xt = ticks_h(dark, B, -1, 8, L[1] + 1, R[0])
assert len(xt) == 5, xt
fx, rx, sx = linfit(xt, [0.5, 1.0, 1.5, 2.0, 2.5])
x_left_check = float(fx((L[0] + L[1]) / 2))

# y: the left axis line is interrupted at the break (rows of the gap)
gap = [g for g in groups(np.where(~dark[T[1]:B[0], L[0]:L[1] + 1].any(1))[0] + T[1]) if g[1] - g[0] >= 2]
assert len(gap) == 1, gap
brk = (gap[0][0] + gap[0][1]) / 2
yt_all = ticks_v(dark, L, +1, 8, T[1] + 1, B[0])
upper = [t for t in yt_all if t < brk - 8]
lower = [t for t in yt_all if t > brk + 8]
# the long (major, labelled) ticks: upper 4.2, 4.1; lower 2.0, 1.6, 1.2, 0.8. The minor tick at 1.0 also passes the
# 8 px length test (the dashed 1.0 line runs through it), so the lower majors are the ticks on the regular grid
# between the top-most (2.0) and bottom-most (0.8) long ticks.
up_major = [t for t in upper if t > T[1] + 20]
lo = sorted(ticks_v(dark, L, +1, 8, int(brk) + 8, B[0], frac=0.8))
d = (lo[-1] - lo[0]) / 3
lo_major = [t for t in lo if min(abs(t - (lo[0] + k * d)) for k in range(4)) < 3]
assert len(lo_major) == 4, lo
fyl, ryl, syl = linfit(lo_major, [2.0, 1.6, 1.2, 0.8])
assert len(up_major) == 2, upper
fyu, ryu, syu = linfit(up_major + [(T[0] + T[1]) / 2], [4.2, 4.1, 4.3])

# symbols: classify pixels by colour class first (so touching symbols of different colours, and the black symbol
# lying on the red dashed line, separate), then fill highlights and open with a 9 px disk per class
r_, g_, b_ = ai[:, :, 0], ai[:, :, 1], ai[:, :, 2]
CLS = {"R = 10 Å": (ai.max(2) < 140) & (ai.max(2) - ai.min(2) < 40),
       "R = 14.5 Å": (r_ > 190) & (g_ < 190) & (b_ < 190) & (abs(g_ - b_) < 45),
       "R = 20 Å": (b_ > 190) & (r_ < 190) & (g_ < 190) & (abs(r_ - g_) < 45),
       "R = 25 Å": (r_ > 190) & (b_ > 190) & (g_ < 190)}
RAD = {"R = 10 Å": 10.0, "R = 14.5 Å": 14.5, "R = 20 Å": 20.0, "R = 25 Å": 25.0}
LEG = (130, 25, 470, 200)  # legend box (x0, y0, x1, y1), its symbols are not data
disk = np.hypot(*np.mgrid[-4:5, -4:5]) <= 4.2
rows, pts, full_h, partial = [], [], [], []
red_line = CLS["R = 14.5 Å"][:, L[1] + 5:L[1] + 60].mean(1) > 0.5
DASH = (int(np.where(red_line)[0].min()), int(np.where(red_line)[0].max()))   # rows of the dashed 1.0 line (left end)
for s, m0 in CLS.items():
    m0 = m0.copy()
    m0[:, :L[1] + 3] = False
    m0[:, R[0] - 2:] = False
    m0[:T[1] + 3] = False
    m0[B[0] - 2:] = False
    m0[LEG[1]:LEG[3], LEG[0]:LEG[2]] = False
    op = ndimage.binary_opening(ndimage.binary_fill_holes(ndimage.binary_closing(m0, iterations=2)), structure=disk)
    lab, n = ndimage.label(op)
    found = np.zeros(op.shape, bool)
    for i in range(1, n + 1):
        m = lab == i
        area = int(m.sum())
        ys, xs = np.where(m)
        h, w = np.ptp(ys) + 1, np.ptp(xs) + 1
        if area < 80 or h > 18 or w > 18:     # not a symbol (dashed circle pieces, arrows, label "1.0")
            continue
        cy, cx = ndimage.center_of_mass(m)
        seg = "upper" if cy < brk else "lower"
        y = float(fyu(cy) if seg == "upper" else fyl(cy))
        x = float(fx(cx))
        hcs = np.array([4, 7, 10, 16, 22, 25]) / RAD[s]
        j = int(np.argmin(abs(hcs - x)))
        rows.append((s, x, y, seg, area, [4, 7, 10, 16, 22, 25][j], float(hcs[j]), x - float(hcs[j]), ""))
        pts.append((cx, cy))
        full_h.append(h)
        found |= m
    # second pass: symbols partly hidden under the red dashed 1.0 line (drawn on top of them). Their visible lower part
    # touches the line; centre column = middle of the visible part, centre row = its bottom edge minus the median
    # symbol half-height of the fully visible symbols.
    if s == "R = 14.5 Å":
        continue   # the dashed line is red itself: a red symbol under it could not be told apart (none is expected)
    op2 = ndimage.binary_opening(ndimage.binary_fill_holes(m0), structure=np.ones((3, 3))) & ~ndimage.binary_dilation(found, iterations=3)
    lab2, n2 = ndimage.label(op2)
    for i in range(1, n2 + 1):
        m = lab2 == i
        ys, xs = np.where(m)
        if m.sum() < 40 or not (DASH[0] - 2 <= ys.min() <= DASH[1] + 3) or np.ptp(xs) + 1 > 18:
            continue
        cx = (xs.min() + xs.max()) / 2
        partial.append((s, m, cx, ys.max(), int(m.sum())))
half = (np.median(full_h) - 1) / 2
for s, m, cx, ybot, area in partial:
    cy = ybot - half
    x, y = float(fx(cx)), float(fyl(cy))
    hcs = np.array([4, 7, 10, 16, 22, 25]) / RAD[s]
    j = int(np.argmin(abs(hcs - x)))
    rows.append((s, x, y, "lower", area, [4, 7, 10, 16, 22, 25][j], float(hcs[j]), x - float(hcs[j]), "partly_hidden"))
    pts.append((cx, cy))
REF = CLS
rows.sort(key=lambda r: (list(REF).index(r[0]), r[1]))
overlay(a, pts, str(WORK / "fig17_overlay.png"))
circled = []
for r in rows:
    if (r[0] == "R = 10 Å" and abs(r[1] - 2.5) < 0.05) or (r[0] == "R = 14.5 Å" and abs(r[1] - 25 / 14.5) < 0.05):
        circled.append(r)
out = [(r[0], r[1], r[2], r[3], r[5], r[6], r[7], ";".join(t for t in ("circled" if r in circled else "", r[8]) if t)) for r in rows]
write_csv(str(HERE / "fig17.csv"), [
    "Wei et al. 2025, Figure 17 (left plot): friction coefficient (F_y/F_z) vs h_c/R for the spherical quartz indenters.",
    "  (The y-axis title is printed 'Friciton coefficient'.)",
    "Columns: series (legend text, by symbol colour: R = 10 Å black, 14.5 Å red, 20 Å blue, 25 Å magenta);",
    "  hc_over_R = symbol centre on the x axis (dimensionless); friction_coefficient = symbol centre on the y axis;",
    "  y_segment = lower (below the axis break) or upper (above it);",
    "  hc_A_nearest / hc_over_R_nominal / x_minus_nominal = my check, not in the figure: the nearest of the six target",
    "  indentation depths h_c = 4, 7, 10, 16, 22, 25 Å named in the text, its h_c/R, and the difference;",
    "  flag = circled: the two points ringed by red dashed circles with arrows to the MD snapshots",
    "  (R = 10 Å, h_c = 25 Å; R = 14.5 Å, h_c = 25 Å per the snapshot labels);",
    "  flag = partly_hidden: the red dashed 1.0 line is drawn over the upper half of this symbol; its centre row is",
    "  estimated from the visible lower edge minus the median half-height of the fully visible symbols (+-0.01).",
    "Provenance: tier 3, digitized from the embedded 300 ppi JPEG of Figure 17 by fig17_extract.py; one row per symbol.",
    f"  x calibrated on the 5 major ticks 0.5-2.5 (max residual {rx:.4f}; the left frame maps to {x_left_check:.3f}, printed 0.0).",
    "  The y axis is broken (break marks between 2.0 and 4.1): the lower segment is calibrated on its 4 labelled major ticks",
    f"  0.8-2.0 (max residual {ryl:.4f}), the upper segment on the 4.1 and 4.2 ticks and the top frame (4.3) (max residual {ryu:.4f}).",
    f"Uncertainty: about +-{2*abs(sx):.3f} in x, +-{2*abs(syl):.3f} (lower) / +-{2*abs(syu):.4f} (upper) in y (2 px; symbols ~16 px).",
    "Not data: the red dashed horizontal line at friction coefficient 1.0 (labelled '1.0'), the dashed circles and the arrows.",
], ["series", "hc_over_R", "friction_coefficient", "y_segment", "hc_A_nearest", "hc_over_R_nominal", "x_minus_nominal", "flag"],
    out, fmt=["{}", "{:.4f}", "{:.4f}", "{}", "{}", "{:.4f}", "{:+.4f}", "{}"])
for r in rows:
    print(r[0], round(r[1], 3), round(r[2], 3), r[3], r[4], r[5], round(r[7], 3), r[8])
print("DASH", DASH, "half", half)
print("n", len(rows), "rx", rx, "x(left frame)", x_left_check, "ryl", ryl, "ryu", ryu, "lo_major", lo_major, "up", up_major, "brk", brk)
