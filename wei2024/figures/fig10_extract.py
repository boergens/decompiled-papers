"""Digitize Fig. 10a-d of wei2024 (tier 3, raster).

Source: the embedded 1777 x 1486 px, 300 ppi JPEG in the middle of PDF page 15 (source/wei2024.pdf).
Writes figures/fig10a.csv ... fig10d.csv and overlays in work/.
Run: python3 -I -B figures/fig10_extract.py (any working directory).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage as ndi  # noqa: E402
import digitize_common as dc  # noqa: E402
import f2_common as fc  # noqa: E402

WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)
a = dc.embedded_image(str(ROOT / "source" / "wei2024.pdf"), 15, bbox_near=(84, 264, 511, 620))
g = dc.gray(a)
dark = g < 120
light = g > 215
OVC = [(0, 255, 255), (0, 160, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (0, 0, 255), (128, 0, 255)]
PROV = ("Provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF page 15, middle image 1777 x 1486 px) by "
        "figures/fig10_extract.py with tools/f2_common.py.")


def hz_axis(row, col, x0, x1):
    """x calibration of the h_z axes of panels a-c: majors 0..45 Å (inward ticks), frame = -5 and 50."""
    xt = dc.tick_positions(dark, row, -1, 10, x0, x1)
    assert len(xt) == 10, xt
    xv = list(range(0, 50, 5))
    f, r, s = fc.fit_ticks(xt, xv)
    return f, r, s, xt, xv


def yaxis(col, y0, y1, values, frame_rows=(), frame_vals=()):
    yt = dc.tick_positions_v(dark, col, 1, 10, y0, y1)
    assert len(yt) == len(values), (yt, values)
    f, r, s = fc.fit_ticks(list(yt) + list(frame_rows), list(values) + list(frame_vals))
    return f, r, s, yt


def cal_text(xt, xv, rx, sx, yt, yv, ry, sy, extra=""):
    return (f"x: major ticks at px {', '.join(f'{t:.1f}' for t in xt)} = {xv[0]}..{xv[-1]} Å, max residual {rx:.3f} Å; "
            f"y: major ticks at px {', '.join(f'{t:.1f}' for t in yt)} = {yv[0]}..{yv[-1]} kcal/mol{extra}, "
            f"max residual {ry:.2f} kcal/mol; 1 px = {abs(sx):.3f} Å in x and {abs(sy):.2f} kcal/mol in y")


def trace_lines(lab, names, roi, x_from, x_to, fx, fy, half_width=1.5, start=None):
    rows, ov = [], []
    for k, s in enumerate(names):
        m = (lab == k) & roi
        m = ndi.binary_opening(m, structure=np.ones((2, 2)))
        env = dc.trace_envelope(m, int(x_from), int(x_to) + 1, 0, m.shape[0], half_width=half_width)
        env = env[~np.isnan(env[:, 1])]
        for c, ymid, ytop, ybot in env[::2]:
            rows.append([s, "line", float(fx(c)), float(fy(ymid)),
                         f"band {float(fy(ybot)):.1f} to {float(fy(ytop)):.1f}" if ybot - ytop > 2 else ""])
        ov.append((list(zip(env[:, 0], env[:, 1])), OVC[k % len(OVC)], "dot"))
    return rows, ov


out = {}

# ------------------------------------------------------------------ Fig. 10a
SER_A = ["0.10 Å/ps", "0.25 Å/ps", "0.50 Å/ps", "0.75 Å/ps", "1.00 Å/ps", "1.50 Å/ps", "2.00 Å/ps"]
SYM_A = ["filled circle", "open circle", "open triangle (up)", "open triangle (down)", "open diamond",
         "open square", "open pentagon"]
PAL_A = [(0, 0, 0), (250, 40, 25), (40, 250, 25), (30, 30, 245), (10, 255, 252), (125, 125, 10), (255, 128, 10)]
lab, tt = fc.classify(a, PAL_A)
fx, rx, sx, xt, xv = hz_axis((548, 550), (130, 131), 133, 849)
fy, ry, sy, yt = yaxis((130, 131), 22, 546, [10000, 9000, 8000, 7000, 6000], [549], [5000])
cal_a = cal_text(xt, xv, rx, sx, yt, [10000, 6000], ry, sy, " plus bottom frame row 549 = 5000 kcal/mol")
roi = np.zeros(lab.shape, bool)
roi[22:540, 146:848] = True            # cols < 146 hold the inward y tick marks
roi[22:142, 150:560] = False           # legend, two columns
roi[142:182, 150:345] = False          # legend, last entry of the left column
gx = np.polyval(np.polyfit(xv, xt, 1), np.arange(0, 46))
rows, ov = [], []
yy, xx = np.mgrid[0:lab.shape[0], 0:lab.shape[1]]
for k, s in enumerate(SER_A):
    m = (lab == k) & roi
    if k == 0:
        cand = fc.markers_dt(m, 3.0, 5, cov_r=3.5)
        best = {}
        for q in cand:
            j = int(np.argmin(np.abs(gx - q["x"])))
            if q["cov"] >= 0.85 and abs(gx[j] - q["x"]) <= 3 and (j not in best or q["r"] > best[j]["r"]):
                best[j] = q       # one point per h_z: the largest inscribed radius (dash pieces are thinner)
        ms = [dict(x=q["x"], y=q["y"]) for q in best.values()]
    else:
        ms = fc.hollow_markers(m & (tt <= 0.55), gx, half=3)
    ms = sorted(ms, key=lambda q: q["x"])
    for q in ms:
        rows.append([s, "marker", float(fx(q["x"])), float(fy(q["y"])), ""])
    ov.append(([(q["x"], q["y"]) for q in ms], OVC[k], "ring"))
    # dashed curve (only 0.10 and 0.25 Å/ps, which run clear of the other series): blank the markers,
    # start at the rightmost elongated dash and chain the dashes leftwards
    if k > 1:
        continue
    md = m & (tt <= 0.55)
    for q in ms:
        md &= (xx - q["x"]) ** 2 + (yy - q["y"]) ** 2 > 6 ** 2
    md = ndi.binary_opening(md, structure=np.ones((2, 2)))
    lb, nb = ndi.label(md, structure=np.ones((3, 3)))
    best = None
    for i in range(1, nb + 1):
        ys_, xs_ = np.where(lb == i)
        if len(ys_) < 10:
            continue
        ev = np.linalg.eigvalsh(np.cov(np.c_[xs_, ys_].T))
        if ev[1] < 3.0 * max(ev[0], 0.3):
            continue
        # the dashed curve ends near the series' last point (h_z = 45 Å): take the dash closest to it
        lx, ly = ms[-1]["x"], ms[-1]["y"]
        dmin = np.min((xs_ - lx) ** 2 + (ys_ - ly) ** 2)
        if best is None or dmin < best[0]:
            best = (dmin, xs_[np.argmax(xs_)], ys_[np.argmax(xs_)])
    if best is None:
        continue
    ch = fc.chain_dashes(md, (best[1] + 2, best[2]), (-1.0, 0.3), max_gap=30, max_angle=55)
    if ch:
        pts = np.vstack([fc.blob_centreline(b) for b in ch])
        pts = pts[np.argsort(pts[:, 0])]
        for x, y in pts:
            rows.append([s, "dashed_curve", float(fx(x)), float(fy(y)), "trace"])
        ov.append((list(map(tuple, pts)), OVC[k], "dot"))
fc.save_overlay(a, ov, str(WORK / "fig10a_overlay.png"), r=1)
out["fig10a"] = (rows, cal_a, "y_total_energy_kcal_per_mol")

# ------------------------------------------------------------------ Fig. 10b
SER_B = ["E_pe", "E_ke", "E_total"]
lab, _ = fc.classify(a, [(0, 0, 0), (250, 0, 0), (0, 0, 250)])
fx, rx, sx, xt, xv = hz_axis((550, 552), (1028, 1029), 1031, 1754)
fy, ry, sy, yt = yaxis((1028, 1029), 18, 548, [2400, 2000, 1600, 1200, 800, 400, 0], [15], [2800])
cal_b = cal_text(xt, xv, rx, sx, yt, [2400, 0], ry, sy, " plus top frame row 15 = 2800 kcal/mol")
roi = np.zeros(lab.shape, bool)
roi[18:538, 1036:1754] = True        # leave out the inward tick marks
roi[40:110, 1240:1625] = False         # title
roi[160:310, 1100:1330] = False        # legend
x1 = np.polyval(np.polyfit(xv, xt, 1), 1.0)
x45 = np.polyval(np.polyfit(xv, xt, 1), 45.2)
rows, ov = trace_lines(lab, SER_B, roi, x1, x45, fx, fy)
fc.save_overlay(a, ov, str(WORK / "fig10b_overlay.png"), r=0)
out["fig10b"] = (rows, cal_b, "y_energy_increment_kcal_per_mol")

# ------------------------------------------------------------------ Fig. 10c
SER_C = ["E_vdwl", "E_angle", "E_coul", "E_dihed", "E_bond", "E_imp"]
lab, _ = fc.classify(a, [(0, 0, 0), (0, 0, 250), (250, 0, 0), (0, 250, 250), (128, 128, 0), (250, 0, 250)])
fx, rx, sx, xt, xv = hz_axis((1307, 1309), (133, 135), 137, 861)
fy, ry, sy, yt = yaxis((133, 135), 775, 1305, [600, 500, 400, 300, 200, 100, 0, -100, -200], [772, 1308], [700, -300])
cal_c = cal_text(xt, xv, rx, sx, yt, [600, -200], ry, sy, " plus frame rows 772 = 700 and 1308 = -300 kcal/mol")
roi = np.zeros(lab.shape, bool)
roi[775:1297, 145:861] = True        # leave out the inward tick marks
roi[775:845, 300:700] = False          # title
roi[850:975, 180:612] = False          # legend
x1 = np.polyval(np.polyfit(xv, xt, 1), 1.0)
x45 = np.polyval(np.polyfit(xv, xt, 1), 45.2)
rows, ov = trace_lines(lab, SER_C, roi, x1, x45, fx, fy)
fc.save_overlay(a, ov, str(WORK / "fig10c_overlay.png"), r=0)
out["fig10c"] = (rows, cal_c, "y_energy_increment_kcal_per_mol")

# ------------------------------------------------------------------ Fig. 10d (grouped bars)
SER_D = ["pe", "ke", "total"]
CATS = ["0.1", "0.25", "0.5", "0.75", "1.0", "1.5", "2.0"]
lab, _ = fc.classify(a, [(255, 128, 0), (250, 0, 0), (0, 0, 250)], resid_max=60)
yt = dc.tick_positions_v(dark, (1039, 1041), 1, 10, 790, 1324)
yv = [4000, 3500, 3000, 2500, 2000, 1500, 1000, 500]
assert len(yt) == len(yv), yt
fy, ry, sy = fc.fit_ticks(list(yt) + [787, 1327], yv + [4500, 0])
cal_d = (f"x: category axis (groups in printed order); y: major ticks at px {', '.join(f'{t:.1f}' for t in yt)} = 4000..500 kcal/mol plus frame rows 787 = 4500 and "
         f"1327 = 0 kcal/mol, max residual {ry:.2f} kcal/mol; 1 px = {abs(sy):.2f} kcal/mol")
roi = np.zeros(lab.shape, bool)
roi[790:1325, 1043:1770] = True
roi[790:960, 1560:1770] = False        # legend
rows, ov = [], []
for k, s in enumerate(SER_D):
    m = ndi.binary_opening((lab == k) & roi, structure=np.ones((5, 5)))
    labk, n = ndi.label(m)
    bars = []
    for i, sl in enumerate(ndi.find_objects(labk), start=1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if w < 8 or h < 10:
            continue
        top = sl[0].start
        # refine the top edge: first row whose middle third of the bar is mostly bar colour
        cols = slice(sl[1].start + w // 3, sl[1].stop - w // 3)
        frac = ((lab[top - 3:top + 4, cols] == k).mean(1))
        edge = top - 3 + float(np.interp(0.5, frac, np.arange(len(frac)))) - 0.5
        bars.append(((sl[1].start + sl[1].stop - 1) / 2, edge, w))
    bars.sort()
    assert len(bars) == 7, (s, bars)
    for (xc, edge, w), cat in zip(bars, CATS):
        rows.append([s, cat, float(xc), float(fy(edge)), ""])
        ov.append(([(xc, edge)], OVC[k + 1], "ring"))
fc.save_overlay(a, ov, str(WORK / "fig10d_overlay.png"), r=1)
out["fig10d"] = (rows, cal_d, None)

# ------------------------------------------------------------------ write
HEAD = {
    "fig10a": ["Fig. 10a: total energy of the whole system (kcal/mol) vs displacement of indenter h_z (Å) at seven loading",
               "rates. Symbols (legend): 0.10 Å/ps black filled circles, 0.25 red open circles, 0.50 green open up-triangles,",
               "0.75 blue open down-triangles, 1.00 cyan open diamonds, 1.50 olive open squares, 2.00 orange open pentagons;",
               "each with a dashed line of the same colour.",
               "Columns: series; kind = marker (one plotted point) or dashed_curve (centre line of the dashes, followed dash",
               "by dash from the right end leftwards with the markers blanked out; only for 0.10 and 0.25 Å/ps, whose",
               "curves run clear of the others; the five lower dashed curves are interleaved with each other and with",
               "the symbols and were not digitized: flag 'trace'); x_hz_A;",
               "y_total_energy_kcal_per_mol; flag.", PROV,
               "Markers: points sit at integer h_z (1-45 Å). Open symbols are found from the hole inside the outline",
               "(only saturated pixels kept, white fraction <= 0.55; centre = midpoint of the hole rows), within +-3 px of",
               "an integer-h_z column; black filled circles from distance-transform maxima (radius >= 2.5 px).",
               "INCOMPLETE: symbols hidden under other symbols or lines, and open symbols whose hole is closed by a",
               "crossing line, are missing (dense overlap of the five lower series below ~6500 kcal/mol).",
               "Uncertainty: about ±0.1 Å in x and ±10 kcal/mol in y (one source pixel = 0.076 Å, 10.4 kcal/mol)."],
    "fig10b": ["Fig. 10b: energy increment (kcal/mol) of the energy terms vs displacement of indenter h_z (Å) at a loading",
               "rate of 1.0 Å/ps. Lines (legend): E_pe black, E_ke red, E_total blue (no symbols).",
               "Columns: series; kind = line (centre of the line in each pixel column, every 2nd column; in steep parts flag",
               "gives the band the line covers in that column); x_hz_A; y_energy_increment_kcal_per_mol; flag.", PROV,
               "Where lines overlap (E_pe and E_total below h_z ~ 10 Å) the hidden line is interpolated by the tracer or has a gap.",
               "Uncertainty: about ±0.1 Å in x and ±6 kcal/mol in y (one source pixel = 0.075 Å, 5.8 kcal/mol)."],
    "fig10c": ["Fig. 10c: energy increment (kcal/mol) of the energy terms vs displacement of indenter h_z (Å) at a loading",
               "rate of 1.0 Å/ps. Lines (legend): E_vdwl black, E_angle blue, E_coul red, E_dihed cyan, E_bond olive, E_imp magenta.",
               "Columns: series; kind = line (centre per pixel column, every 2nd column; band in steep parts); x_hz_A;",
               "y_energy_increment_kcal_per_mol; flag.", PROV,
               "Where lines cross, the hidden line has a gap or the tracer may follow it with a small jump; all six start at",
               "(~1 Å, 0) where they overlap.",
               "Uncertainty: about ±0.1 Å in x and ±3 kcal/mol in y (one source pixel = 0.075 Å, 1.9 kcal/mol)."],
    "fig10d": ["Fig. 10d: energy difference ΔE (kcal/mol) between the cases h_z = 45 Å and h_z = 0 Å at different loading",
               "rates, grouped bars: pe (potential energy, orange), ke (kinetic energy, red), total (total energy, blue).",
               "Columns: series; loading_rate_A_per_ps = category label printed under the group (category axis, not to",
               "scale); bar_centre_px = bar centre column in the source image; delta_E_kcal_per_mol = bar top; flag.", PROV,
               "Bar tops: edge row where the bar colour covers half of the bar's middle third (sub-pixel interpolation).",
               "Uncertainty: about ±10 kcal/mol (one source pixel = 8.3 kcal/mol)."],
}
COLS = {"fig10a": ["series", "kind", "x_hz_A", "y_total_energy_kcal_per_mol", "flag"],
        "fig10b": ["series", "kind", "x_hz_A", "y_energy_increment_kcal_per_mol", "flag"],
        "fig10c": ["series", "kind", "x_hz_A", "y_energy_increment_kcal_per_mol", "flag"],
        "fig10d": ["series", "loading_rate_A_per_ps", "bar_centre_px", "delta_E_kcal_per_mol", "flag"]}
for name, (rows, cal, _) in out.items():
    fmt = ["{}", "{}", "{:.3f}", "{:.1f}", "{}"] if name != "fig10d" else ["{}", "{}", "{:.1f}", "{:.1f}", "{}"]
    dc.write_csv(str(HERE / f"{name}.csv"), HEAD[name] + ["Calibration (linear least squares on tick marks): " + cal],
                 COLS[name], rows, fmt=fmt)
    print(name, len(rows), "rows;", cal)
    if name == "fig10a":
        for s in SER_A:
            print("   ", s, sum(1 for r in rows if r[0] == s and r[1] == "marker"), "markers,",
                  sum(1 for r in rows if r[0] == s and r[1] == "dashed_curve"), "curve points")
