"""Extraction script for Figure 5 (page 39) of Hesse et al. 2026 -- recovers the plotted data from the
vector PDF and writes the CSVs, the original crops and the raster of panel b.  Run from this folder:
    python3 fig5_extract.py
This script is provenance only; the redraw scripts fig5b.py ... fig5e.py read the CSVs, never the PDF.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import math, os, sys
import numpy as np
sys.path.insert(0, "../../tools")
import pdfplot as pp
from PIL import Image

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "2026.10.15.759299v1.full.pdf")
page = pp.open_page(PDF, 39)
ORANGE, PURPLE, BLACK = "#fcae34", "#543379", "#000000"
BLACK_E = "#1c0f29"

# ------------------------------------------------------------------ original crops for QA
crops = {
    "a": pp.R(0.5, 30.4, 157.0, 152.0),   # schematic (letter 'a' excluded, it ends at y=27.7)
    "b": pp.R(157, 25, 289, 142),
    "c": pp.R(5, 177, 150, 297),
    "d": pp.R(155, 170, 289, 297),
    "e": pp.R(5, 305, 289, 480),
}
pp.render(page, crops["a"], 300, "fig5a.png")
for k in "bcde":
    pp.render(page, crops[k], 300, f"fig5{k}_orig.png")

# ------------------------------------------------------------------ panel b: embedded raster heatmap
im_info = [i for i in pp.images(page, crops["b"])][0]
W, H = pp.extract_image(page, im_info["xref"], "fig5b_raster.png")
bx0, by0, bx1, by1 = im_info["bbox"]
img = np.asarray(Image.open("fig5b_raster.png").convert("RGB")).astype(float)
o = np.array([252, 174, 52.]); p = np.array([84, 51, 121.])
frac = ((img - p) @ (o - p)) / float((o - p) @ (o - p))      # 0 = pure purple (state 2), 1 = pure orange (state 1)
frac = np.clip(frac, 0, 1)
# residual off the orange-purple colour axis, to show every pixel is a mix of the two colours
proj = p + frac[..., None] * (o - p)
off_axis = np.sqrt(((img - proj) ** 2).sum(-1))
print("panel b raster", W, "x", H, "max off-axis colour residual (0-255 units):", off_axis.max().round(1),
      "99th pct:", np.percentile(off_axis, 99).round(1))
# axes: tick marks are thin filled rects on the frame; x ticks -1,-0.5,0,0.5,1 s (hidden outline labels read
# -1000 ... 1000, the visible text labels are -1, 0, 1); y ticks at trials 100..800 (hidden outline labels)
bd = pp.drawings(page, crops["b"])
xt = [t["pos"] for t in pp.tick_marks(bd, "x", region=pp.R(170, 121, 262, 124))]   # bottom frame ticks
yt = [t["pos"] for t in pp.tick_marks(bd, "y", region=pp.R(171, 30, 173, 120))]     # left frame ticks
print("b x ticks", xt, "y ticks", yt)
bxax = pp.Axis(list(zip(xt, [-1, -0.5, 0, 0.5, 1])))
byax = pp.Axis(list(zip(yt, [100, 200, 300, 400, 500, 600, 700, 800])))
print("b axes", bxax, byax)
col_t = [bxax(bx0 + (j + 0.5) * (bx1 - bx0) / W) for j in range(W)]
row_trial = [byax(by0 + (i + 0.5) * (by1 - by0) / H) for i in range(H)]
print("b image extent: time %.4f .. %.4f s, trial %.1f .. %.1f" % (bxax(bx0), bxax(bx1), byax(by0), byax(by1)))
hdr = ["trial_est_row_centre"] + ["%.4f" % t for t in col_t]
comments_b = [
    "Figure 5b (page 39): HMM state partition of all trials of an example session, rows = trials sorted by proportion of state 1.",
    "Source: the embedded raster image (xref %d, %d px wide x %d px high, ~200 dpi rasterisation of the plot, NOT the original trial x time-bin matrix)." % (im_info["xref"], W, H),
    "Each pixel colour was projected onto the orange(#fcae34, state 1)-purple(#543379, state 2) colour axis; value = fraction of state 1 (0..1).",
    "Intermediate values are resampling mixtures (about 3.2 trials per pixel row, about 8.2 ms per pixel column); max off-axis colour residual %.1f/255." % off_axis.max(),
    "Header row = time from flash (s) of each pixel-column centre, calibrated on the 5 x tick marks at -1,-0.5,0,0.5,1 s (resid %.1e)." % bxax.resid,
    "First column = estimated trial index of each pixel-row centre, calibrated on the 8 y tick marks assumed at trials 100..800 (hidden outline labels; resid %.1e); the image spans trials %.1f..%.1f, i.e. about 849 rows although the axis label says 800 trials." % (byax.resid, byax(by0), byax(by1)),
    "Image placement: x %.2f..%.2f pt = %.4f..%.4f s; y %.2f..%.2f pt." % (bx0, bx1, bxax(bx0), bxax(bx1), by0, by1),
]
rows = [["%.1f" % row_trial[i]] + ["%.3f" % v for v in frac[i]] for i in range(H)]
pp.write_csv("fig5b_state1_fraction.csv", hdr, rows, comments_b)
state = np.where(frac >= 0.5, 1, 2)
rows = [["%.1f" % row_trial[i]] + [str(v) for v in state[i]] for i in range(H)]
pp.write_csv("fig5b_state.csv", hdr, rows, comments_b[:2] + [
    "Thresholded version of fig5b_state1_fraction.csv: 1 = state 1 (orange) if fraction >= 0.5, else 2 = state 2 (purple).",
    "Header row = time (s) of pixel-column centre; first column = estimated trial index of pixel-row centre (see fig5b_state1_fraction.csv for calibration)."])
print("b: fraction of state-1 pixels before/after t=0: %.3f / %.3f" % (
    state[:, np.array(col_t) < 0].__eq__(1).mean(), state[:, np.array(col_t) > 0].__eq__(1).mean()))

# ------------------------------------------------------------------ helpers for line plots
def series(draws, color, kind, npts_min=3):
    return [d for d in draws if d["kind"] == kind and pp.hexcolor(d["color"] if kind == "stroke" else d["fill"]) == color
            and len(d["points"]) >= npts_min and not d["has_curves"]]

def envelope_at(points, xs, tol=0.05):
    """(lo_y, hi_y) in PDF coords of a band polygon at each x in xs (PDF coords); hi_y is the smaller y."""
    out = []
    for x in xs:
        ys = [py for px, py in points if abs(px - x) < tol]
        out.append((max(ys), min(ys)) if ys else (float("nan"), float("nan")))
    return out

# ------------------------------------------------------------------ panel c: fit accuracy & dwell time vs bin size
cd = pp.drawings(page, crops["c"])
xvals_c = [2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
xax_c = pp.axis_from_ticks(cd, "x", xvals_c, region=pp.R(40, 221, 142, 225), log=True)
yax_c1 = pp.axis_from_ticks(cd, "y", [0.6, 0.8, 1.0], region=pp.R(40, 180, 44, 225))
yax_c2 = pp.axis_from_ticks(cd, "y", [0, 100, 200], region=pp.R(40, 230, 44, 275))
print("c axes", xax_c, yax_c1, yax_c2, sep="\n  ")
top = pp.R(40, 180, 142, 222); bot = pp.R(40, 230, 142, 273)
def in_region(d, r): return r.contains(pp.R(*d["rect"]))
ln_c1 = [d for d in series(cd, BLACK, "stroke") if in_region(d, top)][0]
bd_c1 = [d for d in series(cd, BLACK, "fill", 10) if in_region(d, top)][0]
ln_o = [d for d in series(cd, ORANGE, "stroke") if in_region(d, bot)][0]
bd_o = [d for d in series(cd, ORANGE, "fill", 10) if in_region(d, bot)][0]
ln_p = [d for d in series(cd, PURPLE, "stroke") if in_region(d, bot)][0]
bd_p = [d for d in series(cd, PURPLE, "fill", 10) if in_region(d, bot)][0]
xs_c = [x for x, y in ln_c1["points"]]
assert all(abs(a - b) < 0.05 for a, b in zip(xs_c, [x for x, y in ln_o["points"]]))
bins = [xax_c(x) for x in xs_c]
print("c bin sizes (ms) from line x:", [round(b, 2) for b in bins])
bins_r = [round(b) for b in bins]
# marker cross-check (circle outlines, 8 curve items, 3 pt wide)
mk = pp.markers(cd, max_size=3.2)
for d, nm in [(ln_c1, "black"), (ln_o, "orange"), (ln_p, "purple")]:
    col = pp.hexcolor(d["color"])
    mks = [m for m in mk if pp.hexcolor(m["fill"]) == col]
    dev = max(min(math.hypot(m["cx"] - x, m["cy"] - y) for m in mks) for x, y in d["points"])
    print(f"c {nm}: {len(mks)} markers, max marker-vertex distance {dev:.3f} pt")
e1 = envelope_at(bd_c1["points"], xs_c); eo = envelope_at(bd_o["points"], xs_c); ep = envelope_at(bd_p["points"], xs_c)
rows = []
for i, x in enumerate(xs_c):
    rows.append([bins_r[i], round(bins[i], 2),
                 round(yax_c1(ln_c1["points"][i][1]), 4), round(yax_c1(e1[i][0]), 4), round(yax_c1(e1[i][1]), 4),
                 round(yax_c2(ln_o["points"][i][1]), 1), round(yax_c2(eo[i][0]), 1), round(yax_c2(eo[i][1]), 1),
                 round(yax_c2(ln_p["points"][i][1]), 1), round(yax_c2(ep[i][0]), 1), round(yax_c2(ep[i][1]), 1)])
pp.write_csv("fig5c.csv",
             ["bin_size_ms", "bin_size_ms_from_axis", "norm_cllr_mean", "norm_cllr_sem_lo", "norm_cllr_sem_hi",
              "median_dwell_state1_ms", "median_dwell_state1_sem_lo", "median_dwell_state1_sem_hi",
              "median_dwell_state2_ms", "median_dwell_state2_sem_lo", "median_dwell_state2_sem_hi"], rows, [
    "Figure 5c (page 39): fit accuracy (normalised conditional log-likelihood ratio, top) and median dwell time per state (bottom) vs HMM bin size.",
    "Source: vector stroke paths (1-pt lines, 8 vertices = data points) and the s.e.m. band polygons (upper edge then lower edge); circle markers coincide with the vertices (<0.01 pt).",
    "x axis: log10, calibrated on all 18 tick marks (2,3,...,9,10,20,...,90,100 ms), max residual %.1e in log10 units; bin_size_ms is the rounded value, bin_size_ms_from_axis the raw calibrated x." % xax_c.resid,
    "top y axis calibrated on ticks 0.6, 0.8, 1.0 (resid %.1e); bottom y axis on ticks 0, 100, 200 ms (resid %.1e)." % (yax_c1.resid, yax_c2.resid),
    "Precision: about 0.001 (top, 19.25 pt per 0.2) and 0.1 ms (bottom, 19.25 pt per 100 ms); PDF coordinates carry ~0.01 pt.",
    "CAVEAT: the bottom axis ends at 200 ms; the state-1 value at 100 ms sits exactly on the 200 ms axis limit and both s.e.m. bands are clipped there (upper edge = axis top), so state1 at 100 ms is >= 200 ms (the band polygon has an extra clipping vertex at bin 97 ms).",
    "s.e.m. band values of state 2 (purple) at 100 ms: upper edge clipped at 200 ms.",
])
print("c rows:", *rows, sep="\n  ")

# ------------------------------------------------------------------ panel d: fit accuracy vs median dwell time
dd = pp.drawings(page, crops["d"])
xax_d = pp.axis_from_ticks(dd, "x", [0, 50, 100, 150, 200, 250], region=pp.R(185, 271, 283, 275))
yax_d = pp.axis_from_ticks(dd, "y", [0.5, 0.6, 0.7, 0.8, 0.9, 1.0], region=pp.R(183, 174, 187, 273))
print("d axes", xax_d, yax_d, sep="\n  ")
ln_o = series(dd, ORANGE, "stroke")[0]; bd_o = series(dd, ORANGE, "fill", 10)[0]
ln_p = series(dd, PURPLE, "stroke")[0]; bd_p = series(dd, PURPLE, "fill", 10)[0]
xs_d = [x for x, y in ln_o["points"]]
assert all(abs(a - b) < 0.05 for a, b in zip(xs_d, [x for x, y in ln_p["points"]]))
dw = [xax_d(x) for x in xs_d]
print("d dwell bin centres (ms):", [round(v, 2) for v in dw])
mk = pp.markers(dd, max_size=3.2)
for d, nm in [(ln_o, "orange"), (ln_p, "purple")]:
    col = pp.hexcolor(d["color"]); mks = [m for m in mk if pp.hexcolor(m["fill"]) == col]
    dev = max(min(math.hypot(m["cx"] - x, m["cy"] - y) for m in mks) for x, y in d["points"])
    print(f"d {nm}: {len(mks)} markers, max marker-vertex distance {dev:.3f} pt")
eo = envelope_at(bd_o["points"], xs_d); ep = envelope_at(bd_p["points"], xs_d)
rows = []
for i, x in enumerate(xs_d):
    rows.append([round(dw[i], 1),
                 round(yax_d(ln_o["points"][i][1]), 4), round(yax_d(eo[i][0]), 4), round(yax_d(eo[i][1]), 4),
                 round(yax_d(ln_p["points"][i][1]), 4), round(yax_d(ep[i][0]), 4), round(yax_d(ep[i][1]), 4)])
pp.write_csv("fig5d.csv", ["median_dwell_ms", "state1_norm_cllr_mean", "state1_norm_cllr_sem_lo", "state1_norm_cllr_sem_hi",
                           "state2_norm_cllr_mean", "state2_norm_cllr_sem_lo", "state2_norm_cllr_sem_hi"], rows, [
    "Figure 5d (page 39): normalised conditional log-likelihood ratio vs median dwell time (binned), state 1 (orange) and state 2 (purple), mean +/- s.e.m. across sessions.",
    "Source: vector stroke paths (6 vertices each = the 6 dwell-time bins) and the s.e.m. band polygons; circle markers coincide with the vertices.",
    "x axis calibrated on tick marks 0,50,...,250 ms (resid %.1e); median_dwell_ms = x of the vertices (bin centres 15,35,60,85,150,250 ms)." % xax_d.resid,
    "y axis calibrated on tick marks 0.5,...,1.0 (resid %.1e); precision about 0.001 (19.3 pt per 0.1)." % yax_d.resid,
    "The two states have identical mean and band at the first bin (15 ms) in the PDF.",
])
print("d rows:", *rows, sep="\n  ")

# ------------------------------------------------------------------ panel e: explained variance vs feature, two plots
ed = pp.drawings(page, crops["e"])

def dashed_centreline(subpaths, xv, width=1.0, tol=0.02, sigma=0.01):
    """Reconstruct the centre line of a dashed polyline that the PDF stores as filled dash polygons.
    Each dash polygon is a chain of 1-pt-wide rectangles (one piece per polyline segment it covers), traced
    as one outline in which every junction between two pieces is an explicit point = the data vertex.
    1. pieces: pairs of antiparallel outline edges of equal length 1 pt apart; their end midpoints are
       points on the centre line.  All pieces on one segment (between consecutive vertex x) are fitted by
       one straight line (least squares), which is evaluated at the segment's two vertex x positions.
    2. junction candidates: outline points whose x equals a vertex x.  A candidate within 0.3 pt of the line
       estimate is taken as the exact vertex (this rejects cap corners of horizontal pieces, which also sit
       at a vertex x, 0.5 pt above/below it).
    Returns (y at vertices, info).  unc = least-squares prediction s.d. assuming sigma pt corner noise."""
    n = len(xv)
    seg_pts = [[] for _ in range(n - 1)]       # centre-line points per segment (proper rectangular pieces)
    seg_pts_short = [[] for _ in range(n - 1)]   # from short/trapezoidal stubs at junctions: fallback only
    cand = [[] for _ in range(n)]              # junction candidates per vertex
    for sp in subpaths:
        for x, y in sp[:-1]:
            for k in range(n):
                if abs(x - xv[k]) < 0.015:
                    cand[k].append(y)
        edges = []
        for (x0, y0), (x1, y1) in zip(sp, sp[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            if L >= 0.1:
                edges.append((x0, y0, x1, y1, L))
        for i, (ax0, ay0, ax1, ay1, La) in enumerate(edges):
            ux, uy = (ax1 - ax0) / La, (ay1 - ay0) / La
            nx, ny = -uy, ux
            for j in range(i + 1, len(edges)):
                bx0, by0, bx1, by1, Lb = edges[j]
                if abs(La - Lb) > 0.4:
                    continue
                vx, vy = (bx1 - bx0) / Lb, (by1 - by0) / Lb
                if ux * vx + uy * vy > -0.999:
                    continue                                   # not antiparallel
                dist = (bx0 - ax0) * nx + (by0 - ay0) * ny
                if abs(abs(dist) - width) > tol:
                    continue                                   # not the two long sides of a 1-pt-wide piece
                t0 = (bx1 - ax0) * ux + (by1 - ay0) * uy        # b's end should project near a's start (0)
                t1 = (bx0 - ax0) * ux + (by0 - ay0) * uy        # b's start near a's end (La)
                if max(t0, 0.0) > min(t1, La) - 0.05:
                    continue                                   # no overlap along the piece
                strict = min(La, Lb) >= 0.25 and abs(La - Lb) <= 0.05 and abs(t0) <= 0.05 and abs(t1 - La) <= 0.05
                c1 = ((ax0 + bx1) / 2, (ay0 + by1) / 2)       # centre-line points at the piece ends
                c2 = ((ax1 + bx0) / 2, (ay1 + by0) / 2)       # (midpoints between two parallel lines lie on the midline)
                xlo, xhi = sorted([c1[0], c2[0]])
                ks = [k for k in range(n - 1) if xv[k] - 0.03 <= xlo and xhi <= xv[k + 1] + 0.03]
                if len(ks) != 1:
                    continue
                (seg_pts if strict else seg_pts_short)[ks[0]].extend([c1, c2])
    # per-segment line fits -> estimates at both vertices with uncertainty
    est = [[] for _ in range(n)]
    n_fallback = 0
    for k in range(n - 1):
        P = seg_pts[k]
        if len(P) < 2:
            P = seg_pts_short[k]; n_fallback += bool(P)
        if len(P) < 2:
            continue
        X = np.array([p[0] for p in P]); Y = np.array([p[1] for p in P])
        if X.max() - X.min() < 0.02:
            continue
        A = np.vstack([np.ones_like(X), X]).T
        coef, *_ = np.linalg.lstsq(A, Y, rcond=None)
        cov = sigma ** 2 * np.linalg.inv(A.T @ A)
        for kk in (k, k + 1):
            a = np.array([1.0, xv[kk]])
            est[kk].append((float(a @ coef), float(math.sqrt(a @ cov @ a))))
    ys, unc, source = [], [], []
    for k in range(n):
        if est[k]:
            w = np.array([1 / u ** 2 for y, u in est[k]])
            y_line = float(sum(w * np.array([y for y, u in est[k]])) / w.sum()); u_line = float(1 / math.sqrt(w.sum()))
        else:
            y_line, u_line = float("nan"), float("nan")
        choice = None
        if cand[k]:
            cs = sorted(cand[k])
            pool = cs + [(a + b) / 2 for a in cs for b in cs if abs(abs(a - b) - 1.0) < 0.02]
            if est[k]:
                best = min(pool, key=lambda c: abs(c - y_line))
                if abs(best - y_line) < 0.3:
                    choice = best
            elif len(cs) == 1:
                choice = cs[0]
            elif len(cs) == 3 and abs((cs[0] + cs[2]) / 2 - cs[1]) < 0.02:
                choice = cs[1]
        if choice is not None:
            ys.append(choice); unc.append(0.005); source.append("junction")
        else:
            ys.append(y_line); unc.append(u_line); source.append("line" if est[k] else "none")
    jdev = [abs(ys[k] - float(sum(1 / u ** 2 * y for y, u in est[k]) / sum(1 / u ** 2 for y, u in est[k])))
            for k in range(n) if source[k] == "junction" and est[k]]
    info = dict(n_missing=source.count("none"), n_junction=source.count("junction"), n_line=source.count("line"),
                max_unc_pt=float(np.nanmax(unc)), n_unc_over_0p05=int(sum(u > 0.05 for u in unc)),
                max_junction_vs_line_pt=max(jdev) if jdev else 0.0, n_junction_checked=len(jdev),
                n_segments_from_short_stubs=n_fallback)
    return ys, info, unc

plots = {"ML_to_AM": (pp.R(36, 320, 142, 441), "ML -> AM"), "AM_to_ML": (pp.R(182, 320, 288, 441), "AM -> ML")}
for key, (reg, title) in plots.items():
    sub = [d for d in ed if reg.contains(pp.R(*d["rect"]))]
    xax = pp.axis_from_ticks(sub, "x", [10, 20, 30, 40, 50], region=pp.R(reg.x0, 435, reg.x1, 440))
    yax = pp.axis_from_ticks(sub, "y", [-100, -50, 0, 50, 100], region=pp.R(reg.x0, 322, reg.x0 + 6, 438))
    print(key, "axes", xax, yax, sep="\n  ")
    sol = {c: series(sub, c, "stroke", 40)[0] for c in (BLACK_E, ORANGE, PURPLE)}
    dsh = {c: [d for d in series(sub, c, "fill", 40) if len(d["subpaths"]) > 10][0] for c in (ORANGE, PURPLE)}
    pts = {c: d["points"][:50] for c, d in sol.items()}
    for c, d in sol.items():
        x50, x51 = d["points"][49][0], d["points"][50][0]
        assert len(d["points"]) == 51 and 0 < x51 - x50 < 0.02, (c, x50, x51)
        print(f"  {key} solid {c}: 51 pts, 51st is {x51 - x50:.3f} pt right of the 50th (dropped); y51-y50 = {d['points'][50][1] - d['points'][49][1]:.3f}")
    xv = [x for x, y in pts[BLACK_E]]
    feat = [xax(x) for x in xv]
    assert max(abs(f - round(f)) for f in feat) < 0.02, feat
    for c in (ORANGE, PURPLE):
        assert all(abs(a - b) < 0.01 for a, b in zip(xv, [x for x, y in pts[c]]))
    dash_y = {}
    for c, d in dsh.items():
        ys, info, unc = dashed_centreline(d["subpaths"], xv)
        print(f"  {key} dashed {c}: {len(d['subpaths'])} dash polygons; {info}")
        print("      unc per vertex (pt):", [round(u, 3) for u in unc])
        dash_y[c] = ys
    rows = []
    for i in range(50):
        rows.append([int(round(feat[i])), round(yax(pts[BLACK_E][i][1]), 2), round(yax(pts[ORANGE][i][1]), 2),
                     round(yax(pts[PURPLE][i][1]), 2), round(yax(dash_y[ORANGE][i]), 2), round(yax(dash_y[PURPLE][i]), 2)])
    pp.write_csv(f"fig5e_{key}.csv", ["feature_index", "priming_average_pct", "binocular_conscious_state1_pct",
                                      "binocular_conscious_state2_pct", "binocular_suppressed_state1_pct",
                                      "binocular_suppressed_state2_pct"], rows, [
        f"Figure 5e (page 39), {title} plot: explained variance (%) of face-feature reconstruction per feature (1..50), states inferred in one area and features reconstructed from the other.",
        "Series (legend): priming average (black, solid), binocular conscious state 1 (orange, solid), binocular conscious state 2 (purple, solid), binocular suppressed state 1 (orange, dashed), binocular suppressed state 2 (purple, dashed).",
        "Solid series: vector stroke paths with 50 vertices at feature 1..50 (a 51st vertex 0.01 pt right of the 50th was dropped).",
        "Dashed series: the PDF holds them as filled dash polygons (1 pt wide); the centre line was reconstructed from the parallel dash edges per segment and evaluated at the feature positions "
        "(each dash polygon is a chain of 1-pt-wide rectangles joined at explicit vertex points; vertices covered by a dash are those points (exact), vertices in a gap are the least-squares line through the neighbouring rectangles' end midpoints extended to the vertex x).",
        "Dashed-series uncertainty: <= 0.04 pt (<= 0.07 %) for every vertex except AM -> ML suppressed state 1 at feature 43 (both adjacent segments are gaps; estimated from two sub-0.4-pt stubs at the neighbouring junctions, s.d. 0.095 pt = 0.17 %). Junction points agree with the fitted lines to <= 0.035 pt.",
        "x axis calibrated on tick marks 10..50 (resid %.1e); y axis on tick marks -100..100 (resid %.1e); precision about 0.05 %% (27.75 pt per 50 %%)." % (xax.resid, yax.resid),
    ])
    print("  rows:", rows[:3], "...", rows[-2:])
