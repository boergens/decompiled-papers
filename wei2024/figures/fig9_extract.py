"""Digitize Fig. 9a (main plot and inset) and Fig. 9b of wei2024 (tier 3, raster).

Source: the embedded 2034 x 579 px, 300 ppi JPEG at the top of PDF page 15 (source/wei2024.pdf).
Writes figures/fig9a.csv, figures/fig9a_inset.csv, figures/fig9b.csv and overlays in work/.
Run: python3 -I -B figures/fig9_extract.py (any working directory).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import numpy as np  # noqa: E402
import digitize_common as dc  # noqa: E402
import f2_common as fc  # noqa: E402

WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)
a = dc.embedded_image(str(ROOT / "source" / "wei2024.pdf"), 15, bbox_near=(54, 59, 542, 198))
g = dc.gray(a)
dark = g < 120


def runs_1d(b, offset):
    """Centres of runs of True in a 1-D bool array."""
    out, i = [], 0
    while i < len(b):
        if b[i]:
            e = i
            while e + 1 < len(b) and b[e + 1]:
                e += 1
            out.append(offset + (i + e) / 2)
            i = e + 1
        else:
            i += 1
    return out


# ------------------------------------------------------------------ Fig. 9a main
SER_A = ["x-direction", "y-direction", "z-direction", "overall"]
SHAPE = {"x-direction": "open square", "y-direction": "open circle", "z-direction": "open triangle (up)",
         "overall": "open triangle (down)"}
PAL_A = [(0, 0, 0), (250, 0, 0), (245, 0, 245), (255, 128, 0)]
OVC = [(0, 255, 255), (0, 200, 0), (0, 128, 255), (128, 0, 255)]
lab, tt = fc.classify(a, PAL_A)
core = tt <= 0.55            # shaded marker interiors (t > 0.55) are left out, so hollow markers keep a hole

xt = dc.tick_positions(dark, (447, 449), -1, 8, 728, 1314)     # inward majors 0..45
yt = dc.tick_positions_v(dark, (725, 727), 1, 8, 15, 445)      # inward majors 12..-3
xv = list(range(0, 50, 5))
yv = [12, 9, 6, 3, 0, -3]
assert len(xt) == 10 and len(yt) == 6, (xt, yt)
fx, rx, sx = fc.fit_ticks(xt, xv)
fy, ry, sy = fc.fit_ticks(yt + [12.5], yv + [15])
cal_a = (f"x: major ticks at px {', '.join(f'{t:.1f}' for t in xt)} = 0..45 Å, max residual {rx:.3f} Å; "
         f"y: major ticks at px {', '.join(f'{t:.1f}' for t in yt)} = 12..-3 nN plus top frame row 12.5 = 15 nN, "
         f"max residual {ry:.3f} nN; 1 px = {abs(sx):.3f} Å in x and {abs(sy):.4f} nN in y")
roi = np.zeros(lab.shape, bool)
roi[15:437, 729:1314] = True     # rows below 437 hold the inward tick marks
roi[20:250, 735:960] = False     # legend
roi[20:80, 735:1170] = False     # "Loading rate of 1.0 Å/ps" title
roi[85:238, 930:1185] = False    # inset with its tick labels
gx = np.polyval(np.polyfit(xv, xt, 1), np.arange(0, 46))
rows, ov = [], []
for k, s in enumerate(SER_A):
    m = (lab == k) & roi & core
    ms = sorted(fc.hollow_markers(m, gx), key=lambda q: q["x"])
    for q in ms:
        rows.append([s, "marker", float(fx(q["x"])), float(fy(q["y"])), ""])
    ov.append(([(q["x"], q["y"]) for q in ms], OVC[k], "ring"))
    # smooth curve: follow the line column by column (top/bottom of the line in steep parts)
    x_start = gx[15] if k < 3 else gx[0] + 2      # below h_z ~ 15 Å only the orange curve is visible
    env = dc.trace_envelope(m, int(x_start), int(gx[45]) + 1, 15, 446, half_width=1.5)
    env = env[~np.isnan(env[:, 1])]
    for c, ymid, ytop, ybot in env[::2]:
        rows.append([s, "curve", float(fx(c)), float(fy(ymid)), f"band {float(fy(ybot)):.3f} to {float(fy(ytop)):.3f}"
                     if ybot - ytop > 2 else ""])
    ov.append((list(zip(env[:, 0], env[:, 1])), OVC[k], "dot"))
fc.save_overlay(a, ov, str(WORK / "fig9a_overlay.png"), r=0)
csv_a = rows

# ------------------------------------------------------------------ Fig. 9a inset
# axes: x axis rows 208-209 (ticks below, at row 211), y axis cols 990-991 (ticks left, at col 988)
xti = runs_1d(g[211, 1000:1180] < 150, 1000)        # ticks at 17.5, 20, 22.5, 25 Å
yti = runs_1d(g[85:205, 988] < 150, 85)             # ticks at 0.6, 0.4, 0.2, 0.0 nN
assert len(xti) == 4 and len(yti) == 4, (xti, yti)
fxi, rxi, sxi = fc.fit_ticks([990.5] + xti, [15, 17.5, 20, 22.5, 25])
fyi, ryi, syi = fc.fit_ticks(yti + [208.5], [0.6, 0.4, 0.2, 0.0, -0.2])
cal_i = (f"x: y-axis col 990.5 = 15 Å and outward ticks at px {', '.join(f'{t:.1f}' for t in xti)} = 17.5, 20, 22.5, 25 Å "
         f"(labels on 15, 20, 25), max residual {rxi:.3f} Å; y: outward ticks at px {', '.join(f'{t:.1f}' for t in yti)} "
         f"= 0.6, 0.4, 0.2, 0.0 nN plus x-axis row 208.5 = -0.2 nN, max residual {ryi:.4f} nN; "
         f"1 px = {abs(sxi):.3f} Å in x and {abs(syi):.4f} nN in y")
roi_i = np.zeros(lab.shape, bool)
roi_i[84:207, 993:1185] = True
gxi = (np.arange(15, 26) - fxi(0)) / sxi
rows, ov = [], []
for k, s in enumerate(SER_A):
    m = (lab == k) & roi_i & core
    env = dc.trace_envelope(m, 994, int(gxi[-1]) + 1, 84, 207, half_width=1.0)
    env = env[~np.isnan(env[:, 1])]
    # the ~5 px symbols rarely keep a hole, so: (1) blobs of this colour away from its own line,
    # (2) symbols sitting on the line, seen as a local thickening of the line at a grid column
    zone = fc.curve_zone(lab.shape, env[:, 0], env[:, 1], 2.5)
    from scipy import ndimage as ndi
    offl, nb = ndi.label(m & ~zone)
    ms = []
    for i, sl in enumerate(ndi.find_objects(offl), start=1):
        ys_, xs_ = np.where(offl[sl] == i)
        if len(ys_) < 6:
            continue
        cx, cy = xs_.mean() + sl[1].start, ys_.mean() + sl[0].start
        if np.min(np.abs(gxi - cx)) <= 3:
            ms.append(dict(x=cx, y=cy, flag="off-line"))
    env_y = dict(zip(env[:, 0].astype(int), env[:, 1]))

    def run_len(c):
        if c not in env_y:
            return None
        y = env_y[c]
        r = np.where(m[:, c])[0]
        seg = [q for q in np.split(r, np.where(np.diff(r) > 1)[0] + 1) if len(q) and q[0] - 1 <= y <= q[-1] + 1]
        return (seg[0][0], seg[0][-1]) if seg else None
    for xc in gxi:
        c = int(round(xc))
        r0, r1, r2 = run_len(c), run_len(c - 5), run_len(c + 5)
        if None in (r0, r1, r2):
            continue
        L0, L1, L2 = r0[1] - r0[0] + 1, r1[1] - r1[0] + 1, r2[1] - r2[0] + 1
        if L0 >= 5 and L0 >= max(L1, L2) + 2 and all((q["x"] - c) ** 2 > 9 for q in ms):
            ms.append(dict(x=float(c), y=(r0[0] + r0[1]) / 2, flag="on-line"))
    ms = sorted(ms, key=lambda q: q["x"])
    for q in ms:
        rows.append([s, "marker", float(fxi(q["x"])), float(fyi(q["y"])), q["flag"]])
    ov.append(([(q["x"], q["y"]) for q in ms], OVC[k], "ring"))
    for c, ymid, ytop, ybot in env[::2]:
        rows.append([s, "curve", float(fxi(c)), float(fyi(ymid)), f"band {float(fyi(ybot)):.3f} to {float(fyi(ytop)):.3f}"
                     if ybot - ytop > 2 else ""])
    ov.append((list(zip(env[:, 0], env[:, 1])), OVC[k], "dot"))
fc.save_overlay(a, ov, str(WORK / "fig9a_inset_overlay.png"), r=0)
csv_i = rows

# ------------------------------------------------------------------ Fig. 9b
PAL_B = [(0, 0, 250), (250, 0, 0)]
SER_B = ["average: h_z of 40 ∼ 45 Å", "average: h_z of 20 ∼ 45 Å"]
EQ_B = [(-3.87, 0.99, 7.89, 0.82), (-1.75, 1.12, 3.67, 0.86)]
labb, _ = fc.classify(a, PAL_B)
xtb = dc.tick_positions(dark, (448, 450), -1, 8, 1476, 2030)      # 0.0 .. 2.0
ytb = dc.tick_positions_v(dark, (1473, 1474), 1, 8, 15, 445)      # 8 .. 2
xvb = [0.0, 0.5, 1.0, 1.5, 2.0]
yvb = [8, 7, 6, 5, 4, 3, 2]
assert len(xtb) == 5 and len(ytb) == 7, (xtb, ytb)
fxb, rxb, sxb = fc.fit_ticks(xtb, xvb)
fyb, ryb, syb = fc.fit_ticks(ytb + [13], yvb + [9])
cal_b = (f"x: major ticks at px {', '.join(f'{t:.1f}' for t in xtb)} = 0.0..2.0 Å/ps, max residual {rxb:.4f}; "
         f"y: major ticks at px {', '.join(f'{t:.1f}' for t in ytb)} = 8..2 nN plus top frame row 13 = 9 nN, "
         f"max residual {ryb:.4f} nN; 1 px = {abs(sxb):.4f} Å/ps in x and {abs(syb):.4f} nN in y")
roi_b = np.zeros(lab.shape, bool)
roi_b[15:446, 1477:2030] = True
roi_b[15:95, 1477:2030] = False      # legend rows
roi_b[230:320, 1600:2030] = False    # equations
rows, ov = [], []
inv_x = lambda v: (np.asarray(v) - fxb(0)) / sxb  # noqa: E731
inv_y = lambda v: (np.asarray(v) - fyb(0)) / syb  # noqa: E731
for k, s in enumerate(SER_B):
    ms = [q for q in fc.markers_dt((labb == k) & roi_b, 3.0, 5) if q["r"] >= 3.5 and q["cov"] >= 0.8]
    ms = sorted(ms, key=lambda q: q["x"])
    for q in ms:
        rows.append([s, "marker", float(fxb(q["x"])), float(fyb(q["y"])), ""])
    ov.append(([(q["x"], q["y"]) for q in ms], OVC[k], "ring"))
    A, b, c, _ = EQ_B[k]
    xs = np.linspace(0.1, 2.0, 39)
    for x in xs:
        rows.append([s, "fit_equation", float(x), float(A * np.exp(-x / b) + c), ""])
    ov.append((list(zip(inv_x(xs), inv_y(A * np.exp(-xs / b) + c))), (255, 160, 0), "dot"))
fc.save_overlay(a, ov, str(WORK / "fig9b_overlay.png"), r=1)
csv_b = rows

# ------------------------------------------------------------------ write
PROV = ("Provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF page 15, top image 2034 x 579 px) by "
        "figures/fig9_extract.py with tools/f2_common.py.")
H_A = ["Fig. 9a (main plot): pairwise interaction force (nN) between the quartz and epoxy groups vs displacement of",
       "indenter h_z (Å), loading rate 1.0 Å/ps. Series (legend): x-direction (black, open squares), y-direction (red,",
       "open circles), z-direction (magenta, open up-triangles), overall (orange, open down-triangles), each with a",
       "smooth line of the same colour.",
       "Columns: series; kind = marker (one plotted point) or curve (the smooth line, centre per pixel column, every",
       "2nd column; in steep parts flag gives the band the line covers in that column); x_hz_A; y_force_nN; flag.",
       PROV,
       "Markers: pixels assigned to the legend colour along its white-mixing line (tools/f2_common.classify), only",
       "the saturated part (white fraction <= 0.55) kept, so each hollow marker leaves a hole; holes within",
       "+-4 px of the integer-h_z grid columns (all points sit at integer h_z) give the marker centre (midpoint of",
       "the hole rows, so a line crossing the marker does not move it).",
       "INCOMPLETE: below h_z ~ 18 Å all four series are at ~0 nN and only the orange 'overall' markers and line are",
       "visible on top; markers of the other series hidden under other colours are missing. Curves of x, y and z are",
       "traced from h_z = 15 Å; where two lines cross, the trace of the hidden one has a gap or may jump.",
       "Uncertainty: about ±0.1 Å in x and ±0.05 nN in y (one source pixel = 0.085 Å, 0.043 nN)."]
H_I = ["Fig. 9a inset: zoom of the dashed box (h_z 15-25 Å, force -0.2 to 0.6 nN), same four series and symbols.",
       "Columns: series; kind = marker or curve (centre per pixel column, every 2nd column; band in steep parts);",
       "x_hz_A; y_force_nN; flag.", PROV,
       "Markers: the ~5 px hollow symbols rarely keep a visible hole, so they are found (1) as blobs of the series",
       "colour more than 2.5 px from its own traced line, centroid within +-3 px of an integer h_z column",
       "(flag off-line), or (2) as a local thickening of the line at an integer h_z column (vertical run >= 5 px and",
       ">= 2 px longer than 5 px to either side; centre = run midpoint; flag on-line). Symbols hidden by other",
       "colours, or on a steep part of their line, are missing.",
       "Uncertainty: about ±0.06 Å in x and ±0.01 nN in y (one source pixel = 0.055 Å, 0.007 nN)."]
H_B = ["Fig. 9b: average overall pairwise interaction force (nN) between the two groups vs loading rate (Å/ps), for",
       "two h_z intervals: 'average: h_z of 40 ∼ 45 Å' (blue balls, blue dashed fit) and 'average: h_z of 20 ∼ 45 Å'",
       "(red balls, red dashed fit).",
       "Columns: series; kind = marker (digitized) or fit_equation (computed from the equation printed in the panel,",
       "39 points from 0.1 to 2.0 Å/ps; not digitized); x_rate_A_per_ps; y_force_nN; flag.",
       "Printed equations: blue y = -3.87e^(-x/0.99) + 7.89, R^2 = 0.82; red y = -1.75e^(-x/1.12) + 3.67, R^2 = 0.86.",
       "The equation curves drawn over the source image (work/fig9b_overlay.png) lie on the printed dashed lines.",
       PROV, "Markers: distance-transform maxima of each colour mask (inscribed radius >= 3.5 px, >= 80 % fill).",
       "Uncertainty: about ±0.005 Å/ps in x and ±0.02 nN in y (one source pixel = 0.0045 Å/ps, 0.017 nN)."]
for name, head, rows, cal, xcol in (("fig9a", H_A, csv_a, cal_a, "x_hz_A"), ("fig9a_inset", H_I, csv_i, cal_i, "x_hz_A"),
                                    ("fig9b", H_B, csv_b, cal_b, "x_rate_A_per_ps")):
    dc.write_csv(str(HERE / f"{name}.csv"), head + ["Calibration (linear least squares on tick marks): " + cal],
                 ["series", "kind", xcol, "y_force_nN", "flag"], rows, fmt=["{}", "{}", "{:.4f}", "{:.4f}", "{}"])
    print(name, len(rows), "rows;", cal)
    for s in SER_A + SER_B:
        n = sum(1 for r in rows if r[0] == s and r[1] == "marker")
        if n:
            print("   ", s, n, "markers")
