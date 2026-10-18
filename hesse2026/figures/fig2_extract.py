#!/usr/bin/env python3
"""Extraction script for Figure 2 (PDF page 36) of Hesse et al. 2026.  Provenance only: this script reads
the PDF with tools/pdfplot.py and writes the CSVs / PNGs in this folder.  The redraw scripts (fig2X.py)
read only the CSVs.

Run from inside figures/:  python3 fig2_extract.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os, sys, math
import numpy as np
import fitz
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "tools"))
import pdfplot as pp

PDF = os.path.join(ROOT, "source", "2026.10.15.759299v1.full.pdf")
PAGE = 36
page = pp.open_page(PDF, PAGE)
ALL = pp.drawings(page, None)          # all paths on the page (12181)

ORANGE, PURPLE, BLACK, GREY = "#fcae34", "#543379", "#1c0f29", "#808080"


def draws_in(clip, how="any"):
    """pdfplot.drawings(page, clip) drops paths whose bbox is empty (2-point vertical/horizontal strokes:
    all the spikes of the rasters), because fitz.Rect.intersects() is False for empty rects.  Filter by
    the points instead."""
    out = []
    for d in ALL:
        pts = d["points"]
        if not pts:
            continue
        ins = [clip.contains(fitz.Point(x, y)) for x, y in pts]
        if (how == "any" and any(ins)) or (how == "all" and all(ins)):
            out.append(d)
    return out


def hexfill(d):
    return pp.hexcolor(d["fill"] if d["kind"] != "stroke" else d["color"])


def prov(panel, extra):
    return [f"Figure 2 panel {panel}, PDF page {PAGE} of source/2026.10.15.759299v1.full.pdf (vector graphics)"] + extra


# ------------------------------------------------------------------ dashed-line recovery
# Dashed series are not dashed strokes in the PDF: each dash is a filled outline polygon (stroke width 1 pt,
# butt caps, mitre joins).  We know the x of every polyline vertex (integer feature #, integer n faces, 10-ms
# time grid ...), so we fit the unknown vertex y's so that all outline points lie at distance w/2 from the
# polyline (robust least squares).  Vertices whose two adjacent segments carry no outline point (i.e. fall
# entirely inside a gap between dashes) are returned as NaN.

def sample_outline(polys, step=0.05, drop_lines=()):
    pts = []
    for poly in polys:
        p = np.asarray(poly, float)
        if len(p) > 1 and np.allclose(p[0], p[-1]):
            p = p[:-1]
        n = len(p)
        if n < 2:
            continue
        for i in range(n):
            a, b = p[i], p[(i + 1) % n]
            L = np.hypot(*(b - a))
            m = max(int(L / step), 1)
            t = (np.arange(m) + 0.5) / m
            pts.append(a[None, :] + t[:, None] * (b - a)[None, :])
    pts = np.vstack(pts)
    keep = np.ones(len(pts), bool)
    for ax, v in drop_lines:                       # points lying on an axis clip boundary
        keep &= np.abs(pts[:, 0 if ax == "x" else 1] - v) > 0.06
    return pts[keep]


def _seg_dist(P, V):
    A = V[:-1][None, :, :]; B = V[1:][None, :, :]
    AB = B - A
    AP = P[:, None, :] - A
    t = np.clip((AP * AB).sum(-1) / np.maximum((AB * AB).sum(-1), 1e-12), 0, 1)
    C = A + t[..., None] * AB
    D = P[:, None, :] - C
    return np.hypot(D[..., 0], D[..., 1])


def recover_dashed(polys, xs, w, drop_lines=(), group_gap=None):
    """polys: outline polygons (page coords); xs: vertex x positions (ascending); w: stroke width (pt).
    Returns (y page coords with NaN where unconstrained, info dict).
    Every dash polygon is fitted on its own (2-25 unknowns: the vertices inside its x-range plus one on each
    side, which are fixed by the direction of the dash's end segments).  A vertex constrained by several dashes
    (gap between two dashes, or dashes overlapping in x) gets the mean of their estimates; info['spread'] is the
    largest disagreement (pt) between such estimates, a direct precision measure.  group_gap is ignored."""
    xs = np.asarray(xs, float)
    m = len(xs)
    dx = np.median(np.diff(xs)) if m > 1 else 1.0
    if group_gap is None:
        group_gap = 1.5 * dx
    # stage 1: every dash on its own -> per-vertex estimates
    est = [[] for _ in range(m)]
    infos = []
    rng = []
    for pi, poly in enumerate(polys):
        x0 = min(p[0] for p in poly); x1 = max(p[0] for p in poly)
        k0 = max(int(np.searchsorted(xs, x0 - 0.3 * dx)) - 1, 0)
        k1 = min(int(np.searchsorted(xs, x1 + 0.3 * dx)) + 1, m)
        if k1 - k0 < 2:
            continue
        yy, info = _recover_run([poly], xs[k0:k1], w, drop_lines)
        if info["n_points"] < 10:
            continue
        rng.append((x0, x1, pi))
        for v in np.where(~np.isnan(yy))[0]:
            est[k0 + v].append(yy[v])
        infos.append(info)
    y = np.array([np.median(e) if e else np.nan for e in est])
    spread = np.array([max(e) - min(e) if len(e) > 1 else 0.0 for e in est])
    if not infos:
        return y, dict(resid_rms=np.nan, n_points=0, frac_outlier=np.nan, spread=spread)
    n = np.array([i["n_points"] for i in infos], float)
    out = dict(resid_rms=float(np.sqrt(np.sum(n * np.array([i["resid_rms"] for i in infos]) ** 2) / n.sum())),
               n_points=int(n.sum()), frac_outlier=float(np.sum(n * np.array([i["frac_outlier"] for i in infos])) / n.sum()),
               n_dashes=len(infos), spread=spread)
    if group_gap < 0:
        return y, out
    # stage 2: refine jointly per run of neighbouring dashes, initialised with the stage-1 values
    runs = []
    for x0, x1, i in sorted(rng):
        if runs and x0 <= runs[-1][1] + group_gap:
            runs[-1][1] = max(runs[-1][1], x1); runs[-1][2].append(i)
        else:
            runs.append([x0, x1, [i]])
    y2 = np.full(m, np.nan)
    for x0, x1, idx in runs:
        k0 = max(int(np.searchsorted(xs, x0 - 0.3 * dx)) - 1, 0)
        k1 = min(int(np.searchsorted(xs, x1 + 0.3 * dx)) + 1, m)
        if k1 - k0 < 2:
            continue
        yy, info = _recover_run([polys[i] for i in idx], xs[k0:k1], w, drop_lines, y_init=y[k0:k1])
        sel = ~np.isnan(yy)
        y2[k0:k1][sel] = yy[sel]
    out["stage1_vs_stage2_max"] = float(np.nanmax(np.abs(y2 - y))) if np.any(~np.isnan(y2) & ~np.isnan(y)) else np.nan
    return y2, out


def _recover_run(polys, xs, w, drop_lines=(), y_init=None):
    P = sample_outline(polys, drop_lines=drop_lines)
    m = len(xs)
    dx = np.median(np.diff(xs)) if m > 1 else 1.0
    y0 = np.full(m, np.nan)
    for k in range(m):
        sel = np.abs(P[:, 0] - xs[k]) < max(0.6 * dx, 0.3)
        if sel.any():
            y0[k] = np.median(P[sel, 1])
    if y_init is not None:
        y0 = np.where(np.isnan(y_init), y0, y_init)
    ok = ~np.isnan(y0)
    if ok.sum() == 0:
        return y0, dict(resid_rms=np.nan, n_points=len(P), frac_outlier=np.nan)
    y0[~ok] = np.interp(xs[~ok], xs[ok], y0[ok])

    def resid(y):
        return _seg_dist(P, np.column_stack([xs, y])).min(1) - w / 2

    r = least_squares(resid, y0, loss="soft_l1", f_scale=0.15, max_nfev=300)
    V = np.column_stack([xs, r.x])
    d = _seg_dist(P, V)
    res = d.min(1) - w / 2
    j = d.argmin(1)
    good = np.abs(res) < 0.25
    # a segment counts as covered when the outline points projecting onto it span >= 30 % of its length
    # (a vertex is only trusted if an adjacent segment is covered: its y is then fixed by that segment's direction)
    covered = np.zeros(max(m - 1, 0), bool)
    for s in np.unique(j[good]):
        A, B = V[s], V[s + 1]
        AB = B - A
        t = ((P[good & (j == s)] - A) @ AB) / max(AB @ AB, 1e-12)
        if t.max() - t.min() >= 0.3:
            covered[s] = True
    vert_ok = np.zeros(m, bool)
    if m > 1:
        vert_ok[:-1] |= covered
        vert_ok[1:] |= covered
    y = np.where(vert_ok, r.x, np.nan)
    return y, dict(resid_rms=float(np.sqrt(np.mean(res[good] ** 2))), n_points=len(P),
                   frac_outlier=float((~good).mean()), covered=covered)


def dash_centrelines(polys, width=1.0, min_edge=0.6):
    """Geometric alternative (after figures/edfig9_extract.py, same idea as fig6/fig6_extract.py): the two
    long sides of a straight dash piece are antiparallel outline edges exactly `width` apart; the line midway
    between them is the centre line.  Returns pieces (x0, y0, x1, y1).  Edges shorter than min_edge are
    skipped (caps, notches at joints), so this needs segments longer than ~0.6 pt (fine for i, j, l; not k)."""
    pieces = []
    for sp in polys:
        pts = list(sp)
        if math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) > 1e-6:
            pts.append(pts[0])
        E0 = []
        for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
            L = math.hypot(bx - ax, by - ay)
            if L >= 1e-6:
                E0.append((ax, ay, bx, by, L, (bx - ax) / L, (by - ay) / L))
        E = []
        for i, e in enumerate(E0):
            if e[4] < min_edge:
                continue
            prv, nxt = E0[i - 1], E0[(i + 1) % len(E0)]
            is_cap = abs(e[4] - width) < 0.04 and abs(prv[5] * e[5] + prv[6] * e[6]) < 0.25 and abs(nxt[5] * e[5] + nxt[6] * e[6]) < 0.25
            if not is_cap:
                E.append(e)
        for i, e1 in enumerate(E):
            for e2 in E[i + 1:]:
                if e1[5] * e2[5] + e1[6] * e2[6] > -0.9995:      # must be antiparallel
                    continue
                nx, ny = -e1[6], e1[5]
                mx, my = (e2[0] + e2[2]) / 2, (e2[1] + e2[3]) / 2
                dist = (mx - e1[0]) * nx + (my - e1[1]) * ny
                if abs(abs(dist) - width) > 0.12:
                    continue
                ux, uy = e1[5], e1[6]
                t2 = sorted([(e2[0] - e1[0]) * ux + (e2[1] - e1[1]) * uy, (e2[2] - e1[0]) * ux + (e2[3] - e1[1]) * uy])
                lo, hi = max(0.0, t2[0]), min(e1[4], t2[1])
                if hi - lo < 0.15:
                    continue
                sx0, sy0 = e1[0] + nx * dist / 2, e1[1] + ny * dist / 2
                pieces.append((sx0 + ux * lo, sy0 + uy * lo, sx0 + ux * hi, sy0 + uy * hi))
    return pieces


def dashed_vertices(pieces, xv):
    """y (page coords) of a polyline with vertices at x positions xv from centre-line pieces: each piece is
    assigned to the segment containing its midpoint; the pieces of a segment (length-weighted) define its
    line, which is evaluated at the segment's two vertices; a vertex gets the mean of the estimates of its
    two adjacent segments (NaN if neither has a piece). Also returns the disagreement of the two estimates."""
    xv = np.asarray(xv, float)
    n = len(xv)
    seg = [[] for _ in range(n - 1)]
    for x0, y0, x1, y1 in pieces:
        if x1 < x0:
            x0, y0, x1, y1 = x1, y1, x0, y0
        if x1 - x0 < 1e-4:
            continue
        k = int(np.searchsorted(xv, (x0 + x1) / 2)) - 1
        if 0 <= k < n - 1:
            m = (y1 - y0) / (x1 - x0)
            seg[k].append((m, y0 - m * x0, math.hypot(x1 - x0, y1 - y0)))
    y, spread = np.full(n, np.nan), np.full(n, np.nan)
    for k in range(n):
        ests = []
        for s in (k - 1, k):
            if 0 <= s < n - 1 and seg[s]:
                w = np.array([l[2] for l in seg[s]])
                v = np.array([l[0] * xv[k] + l[1] for l in seg[s]])
                ests.append(float((w * v).sum() / w.sum()))
        if ests:
            y[k], spread[k] = np.mean(ests), (max(ests) - min(ests) if len(ests) > 1 else 0.0)
    return y, spread


def stroke_width_of_outline(d):
    """Stroke width of an outlined dash = length of its shortest edges (butt caps)."""
    L = []
    for sp in d["subpaths"]:
        p = np.asarray(sp)
        e = np.hypot(*(np.diff(p, axis=0)).T)
        L.extend(e[e > 0.02])
    return float(np.percentile(L, 10))


def fit_pitch(yc):
    """Row pitch of a raster from the spike y positions: scan for the pitch that puts all distinct y's on a
    grid (anchored at the lowest row), then refine by least squares. Returns (pitch, y of the lowest row)."""
    ys = np.unique(np.round(yc, 4))
    d = np.diff(ys)
    p_est = np.median(d[d < 1.3 * d.min()])
    best = None
    for p in np.linspace(0.97 * p_est, 1.03 * p_est, 3001):
        k = (ys - ys[-1]) / p
        r = np.abs(k - np.round(k)).max()
        if best is None or r < best[1]:
            best = (p, r)
    k = np.round((ys - ys[-1]) / best[0])
    A = np.column_stack([k, np.ones_like(k)])
    p, y0 = np.linalg.lstsq(A, ys, rcond=None)[0]
    return float(p), float(y0)


def fmt(v, nd=3):
    return "" if v is None or (isinstance(v, float) and math.isnan(v)) else round(float(v), nd)


# ====================================================================== panel c
def panel_c():
    clip = pp.R(395, 15, 520, 100)
    dr = draws_in(clip)
    xax = pp.axis_from_ticks(dr, "x", [-1, 0, 1], region=pp.R(420, 72, 520, 82))
    yax = pp.axis_from_ticks(dr, "y", [0, 25, 50, 75, 100], region=pp.R(420, 20, 435, 82))
    names = {ORANGE: "state1", PURPLE: "state2"}
    cols, t = {}, None
    for d in dr:
        c = hexfill(d)
        if c not in names or len(d["points"]) < 100:
            continue
        xs, ys = pp.polyline_to_xy(d["points"], xax, yax)
        if d["kind"] == "stroke":
            t = np.round(np.array(xs), 3); cols[names[c]] = np.array(ys)
        else:
            bx, lo, hi = pp.band_envelope(list(zip(np.round(xs, 3), ys)), 3)
            cols[names[c] + "_lo"] = dict(zip(bx, lo)); cols[names[c] + "_hi"] = dict(zip(bx, hi))
    # reference lines
    refs = []
    for d in dr:
        if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#a6a6a6":
            x0, y0, x1, y1 = d["rect"]
            if x1 - x0 < 1:
                refs.append(("vertical dashed line at time = %.3f s" % xax((x0 + x1) / 2)))
            else:
                refs.append(("horizontal dashed line at %.1f %%" % yax((y0 + y1) / 2)))
    hdr = ["time_s", "state1_pct", "state1_sd_lo_pct", "state1_sd_hi_pct", "state2_pct", "state2_sd_lo_pct", "state2_sd_hi_pct"]
    rows = []
    for i, tt in enumerate(t):
        rows.append([tt, fmt(cols["state1"][i]), fmt(cols["state1_lo"].get(tt)), fmt(cols["state1_hi"].get(tt)),
                     fmt(cols["state2"][i]), fmt(cols["state2_lo"].get(tt)), fmt(cols["state2_hi"].get(tt))])
    pp.write_csv("fig2c.csv", hdr, rows, prov("c", [
        "Lines: 1 stroke path per state (1799 segments, 1 point per ms); bands: filled polygons (upper edge + lower edge) = +/- SD across sessions",
        f"x axis calibrated on tick marks at -1, 0, 1 s (resid {xax.resid:.1e}); y axis on ticks 0,25,50,75,100 % (resid {yax.resid:.1e})",
        "colours: state 1 = #fcae34 (orange), state 2 = #543379 (purple); " + "; ".join(refs),
        "precision: ~0.1 % in y, 1 ms in x"]))
    print("c:", len(rows), "rows", t[0], t[-1], refs)


# ====================================================================== panel d
def panel_d():
    clip = pp.R(2, 100, 127, 187)
    dr = draws_in(clip)
    xax = pp.axis_from_ticks(dr, "x", [0, 100, 200], region=pp.R(30, 163, 127, 172))
    yax = pp.axis_from_ticks(dr, "y", [0, 0.5, 1], region=pp.R(25, 100, 36, 166))
    series = {"#000000": "data", "#808080": "shuffled"}
    cols, lag = {}, None
    for d in dr:
        c = hexfill(d)
        if c not in series or len(d["points"]) < 100:
            continue
        xs, ys = pp.polyline_to_xy(d["points"], xax, yax)
        if d["kind"] == "stroke":
            lag = np.round(np.array(xs), 3); cols[series[c]] = np.array(ys)
        else:
            bx, lo, hi = pp.band_envelope(list(zip(np.round(xs, 3), ys)), 3)
            cols[series[c] + "_lo"] = dict(zip(bx, lo)); cols[series[c] + "_hi"] = dict(zip(bx, hi))
    # the strokes have 202 points: lags 0..200 ms plus a duplicated end sample at 200.02 ms (same values); drop it
    keep = np.r_[True, np.diff(np.round(lag)) > 0]
    assert np.abs(lag - np.round(lag)).max() < 0.05
    lag_r = np.round(lag)
    for k in ("data", "shuffled"):
        cols[k] = cols[k][keep]
        for s in ("_lo", "_hi"):
            cols[k + s] = {float(np.round(x)): v for x, v in cols[k + s].items() if abs(x - np.round(x)) < 0.05}
    lag = lag_r[keep]
    ref = None
    for d in dr:
        if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#a6a6a6":
            x0, y0, x1, y1 = d["rect"]; ref = xax((x0 + x1) / 2)
    hdr = ["lag_ms", "data_autocorr", "data_sd_lo", "data_sd_hi", "shuffled_autocorr", "shuffled_sd_lo", "shuffled_sd_hi"]
    rows = [[l, fmt(cols["data"][i], 4), fmt(cols["data_lo"].get(l), 4), fmt(cols["data_hi"].get(l), 4),
             fmt(cols["shuffled"][i], 4), fmt(cols["shuffled_lo"].get(l), 4), fmt(cols["shuffled_hi"].get(l), 4)]
            for i, l in enumerate(lag)]
    pp.write_csv("fig2d.csv", hdr, rows, prov("d", [
        "Lines: stroke paths, lag 0..200 ms in 1 ms steps (201 points; a duplicated end sample 0.02 ms after 200 ms was dropped); bands: filled polygons = +/- SD across sessions",
        f"x axis calibrated on ticks 0, 100, 200 ms (resid {xax.resid:.1e}); y on ticks 0, 0.5, 1 (resid {yax.resid:.1e})",
        "colours: data = #000000 (black), time-shuffled = #808080 (grey); vertical dashed grey (#a6a6a6) reference line at lag = %.1f ms" % ref,
        "precision: ~0.002 in autocorrelation, 1 ms in lag"]))
    print("d:", len(rows), "rows; dashed line at lag", ref)
    return ref


# ====================================================================== panel i
def panel_i():
    clip = pp.R(260, 183, 392, 330)
    dr = draws_in(clip)
    xax = pp.axis_from_ticks(dr, "x", [10, 20, 30, 40, 50], region=pp.R(285, 307, 392, 313))
    yax = pp.axis_from_ticks(dr, "y", [-100, -50, 0, 50, 100], region=pp.R(280, 190, 290, 312))
    ymin_pix = yax.inv(-100)
    feats = np.arange(1, 51)
    xs = np.array([xax.inv(k) for k in feats])

    def solid(color):
        pts = []
        for d in dr:
            if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == color and d["n_items"] >= 2:
                pts += d["points"]
        pts = np.array(pts)
        y = np.full(50, np.nan); clipped = np.zeros(50, int)
        for i, x in enumerate(xs):
            sel = np.abs(pts[:, 0] - x) < 0.15
            if sel.any():
                y[i] = yax(np.median(pts[sel, 1]))
            else:
                clipped[i] = 1       # vertex outside the axes (line clipped at -100 %): value left empty
        return y, clipped

    def dashed(color):
        polys = []
        for d in dr:
            if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == color and not d["has_curves"] and d["n_items"] >= 4:
                polys += d["subpaths"]
        ypix, spread = dashed_vertices(dash_centrelines(polys, 1.0), xs)
        info = dict(resid_rms=np.nan, frac_outlier=np.nan, spread=np.nan_to_num(spread))
        y = np.array([yax(v) if not np.isnan(v) else np.nan for v in ypix])
        clipped = (y < -100).astype(int)
        # a vertex with no visible dash on either adjacent segment next to clipped vertices is itself clipped
        for i in np.where(np.isnan(y))[0]:
            nb = [j for j in (i - 1, i + 1) if 0 <= j < len(y)]
            if any(clipped[j] for j in nb):
                clipped[i] = 1
        y = np.where(clipped == 1, np.nan, y)
        print("   dashed", color, "fit rms %.3f pt, outliers %.1f%%, nan %d, max spread between dash estimates %.3f pt, stage1 vs stage2 max %.3f pt" % (info["resid_rms"], 100 * info["frac_outlier"], np.isnan(y).sum(), info["spread"].max(), info.get("stage1_vs_stage2_max", np.nan)))
        return y, clipped

    black, _ = solid(BLACK)
    o_s, _ = solid(ORANGE)
    p_s, p_s_clip = solid(PURPLE)
    o_d, o_d_clip = dashed(ORANGE)
    p_d, p_d_clip = dashed(PURPLE)
    hdr = ["feature_index", "feature_type", "priming_average_pct", "binocular_conscious_state1_pct",
           "binocular_conscious_state2_pct", "binocular_conscious_state2_clipped",
           "binocular_suppressed_state1_pct", "binocular_suppressed_state1_clipped", "binocular_suppressed_state2_pct"]
    rows = [[int(k), "shape" if k <= 20 else "appearance", fmt(black[i], 2), fmt(o_s[i], 2), fmt(p_s[i], 2), int(p_s_clip[i]),
             fmt(o_d[i], 2), int(o_d_clip[i]), fmt(p_d[i], 2)] for i, k in enumerate(feats)]
    pp.write_csv("fig2i.csv", hdr, rows, prov("i", [
        "Solid lines = stroke paths (50 vertices, one per feature); dashed lines = outlined dash polygons, recovered by fitting a",
        "  dash centre lines (midway between the two antiparallel long sides of each dash polygon, stroke width 1 pt) and extending the pieces on each segment to the vertices (feature #)",
        f"x axis calibrated on ticks 10..50 (resid {xax.resid:.1e}); y axis on ticks -100..100 % (resid {yax.resid:.1e})",
        "*_clipped = 1: the line leaves the axes below -100 % at this feature (the figure clips the line at -100 %); the value is",
        "  then left EMPTY (it is below -100 % and not shown in the figure); the redraw script draws these vertices at -100 %",
        "series: priming_average = black #1c0f29 solid; binocular_conscious_state1 = orange #fcae34 solid; binocular_conscious_state2 =",
        "  purple #543379 solid; binocular_suppressed_state1 = orange dashed; binocular_suppressed_state2 = purple dashed",
        "legend says shape features 1-20 (bracket 'Shape' over 1-20) and appearance features 21-50 (bracket 'Appearance')",
        "precision: solid ~0.1 % units; dashed ~0.5 % units (joints of steep segments less certain)"]))
    print("i: clipped purple solid at", np.where(p_s_clip)[0] + 1, "clipped orange dashed at", np.where(o_d_clip)[0] + 1)


# ====================================================================== panel j
def panel_j():
    clip = pp.R(388, 183, 519, 330)
    dr = draws_in(clip)
    xax = pp.axis_from_ticks(dr, "x", [0, 20, 40, 60], region=pp.R(410, 307, 519, 313))
    yax = pp.axis_from_ticks(dr, "y", [0, 20, 40, 60, 80, 100], region=pp.R(405, 190, 415, 312))
    n = np.arange(1, 61)
    xs = np.array([xax.inv(k) for k in n])
    y0_pix, y100_pix = yax.inv(0), yax.inv(100)

    def at_vertices(pts):
        pts = np.asarray(pts)
        return np.array([yax(np.median(pts[np.abs(pts[:, 0] - x) < 0.15, 1])) if (np.abs(pts[:, 0] - x) < 0.15).any() else np.nan for x in xs])

    def band(d):
        # polygon = upper edge (n = 1..60) then lower edge back, clipped by the axes box (edges running along 0 or 100 %
        # have no vertex at integer n): take the polygon's vertical extent at x = n from the crossings of its edges
        pts = np.array(d["points"])
        if not np.allclose(pts[0], pts[-1]):
            pts = np.vstack([pts, pts[:1]])
        xv = np.array([xax(x) for x in pts[:, 0]]); yv = np.array([yax(y) for y in pts[:, 1]])
        out_lo, out_hi = np.full(60, np.nan), np.full(60, np.nan)
        for i, k in enumerate(n):
            ys = list(yv[np.abs(xv - k) < 1e-3])                     # vertices exactly at n
            for (xa, ya), (xb, yb) in zip(zip(xv[:-1], yv[:-1]), zip(xv[1:], yv[1:])):
                if (xa < k < xb) or (xb < k < xa):                   # edge crossing x = n
                    ys.append(ya + (yb - ya) * (k - xa) / (xb - xa))
            if ys:
                out_lo[i], out_hi[i] = min(ys), max(ys)
        return out_lo, out_hi

    strokes = {c: [d for d in dr if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == c and d["n_items"] > 50] for c in (BLACK, ORANGE, PURPLE)}
    fills = {c: [d for d in dr if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == c and not d["has_curves"] and d["n_items"] >= 4] for c in (BLACK, ORANGE, PURPLE)}
    # bands are single-subpath polygons with ~2x60 points; dashed lines are multi-subpath (many dashes)
    series = {}
    series["priming_average"] = at_vertices(strokes[BLACK][0]["points"])
    series["binocular_conscious_state1"] = at_vertices(strokes[ORANGE][0]["points"])
    series["binocular_conscious_state2"] = at_vertices(strokes[PURPLE][0]["points"])
    # bands: identify by y-range (which line they surround)
    bands = {}
    bands["priming_average"] = band(fills[BLACK][0])
    o_b = [d for d in fills[ORANGE] if len(d["subpaths"]) == 1]
    p_b = [d for d in fills[PURPLE] if len(d["subpaths"]) <= 2]
    for d in o_b:
        lo, hi = band(d)
        key = "binocular_conscious_state1" if np.nanmean(hi) > 30 else "binocular_suppressed_state1"
        bands[key] = (lo, hi)
    for d in p_b:
        lo, hi = band(d)
        key = "binocular_suppressed_state2" if np.nanmean(hi) > 30 else "binocular_conscious_state2"
        bands[key] = (lo, hi)
    # validation: the band is symmetric about its line (mean +/- SD), so band midpoint == line where unclipped
    for nm in ("priming_average", "binocular_conscious_state1"):
        lo, hi = bands[nm]
        ok = (lo > 0.05) & (hi < 99.95)
        print("   j band-midpoint check", nm, "max |mid - line| = %.3f" % np.nanmax(np.abs((lo + hi) / 2 - series[nm])[ok]))
    # dashed lines: primary estimate = band midpoint where the band is not clipped; dash-outline fit elsewhere and as cross-check
    for c, nm in [(ORANGE, "binocular_suppressed_state1"), (PURPLE, "binocular_suppressed_state2")]:
        dash = [d for d in fills[c] if len(d["subpaths"]) > 5]
        polys = [sp for d in dash for sp in d["subpaths"]]
        ypix, spread = dashed_vertices(dash_centrelines(polys, 1.0), xs)
        yfit = np.clip(np.array([yax(v) if not np.isnan(v) else np.nan for v in ypix]), 0, 100)
        lo, hi = bands[nm]
        mid = (lo + hi) / 2
        ok = (lo > 0.05) & (hi < 99.95) & ~np.isnan(mid)
        y = np.where(ok, mid, yfit)
        # where the line runs along the 0 % axis (half of the stroke clipped away) the dash geometry gives nothing:
        # the value is 0 when both neighbours are at (or below) 0.5 %
        for _ in range(5):
            for i in np.where(np.isnan(y))[0]:
                nb = [y[j] for j in (i - 1, i + 1) if 0 <= j < len(y) and not np.isnan(y[j])]
                if nb and all(v <= 0.5 for v in nb):
                    y[i] = 0.0
        both = ok & ~np.isnan(yfit)
        dev = np.abs(yfit - mid)[both]
        print("   j dashed", nm, "band midpoint used at %d of 60 n; geometric fit NaN at %d n (spread max %.3f pt); |fit - midpoint| max %.2f, median %.2f (%% units) over %d n; final NaN %d"
              % (ok.sum(), np.isnan(yfit).sum(), np.nanmax(spread), dev.max() if len(dev) else np.nan, np.median(dev) if len(dev) else np.nan, len(dev), np.isnan(y).sum()))
        series[nm] = y
    order = ["priming_average", "binocular_conscious_state1", "binocular_conscious_state2", "binocular_suppressed_state1", "binocular_suppressed_state2"]
    hdr = ["n_faces"] + [f"{k}_{s}" for k in order for s in ("pct", "sd_lo_pct", "sd_hi_pct")]
    rows = []
    for i, k in enumerate(n):
        row = [int(k)]
        for nm in order:
            lo, hi = bands.get(nm, (np.full(60, np.nan), np.full(60, np.nan)))
            row += [fmt(series[nm][i], 2), fmt(lo[i], 2), fmt(hi[i], 2)]
        rows.append(row)
    pp.write_csv("fig2j.csv", hdr, rows, prov("j", [
        "Solid lines = stroke paths (60 vertices, n = 1..60 faces); bands = filled polygons (upper + lower edge) = +/- SD.",
        "Dashed lines: the band is symmetric about its line, so the dashed line = midpoint of its band wherever the band is not clipped",
        "  by the axes (checked against a direct fit of the dash outlines: agreement within ~0.5 % units); where the band is clipped",
        "  (at 0 or 100 %) the value comes from the dash centre lines (midway between the long sides of each dash polygon); where the line runs along the 0 % axis it is 0.",
        f"x axis calibrated on ticks 0,20,40,60 (resid {xax.resid:.1e}); y axis on ticks 0..100 % (resid {yax.resid:.1e})",
        "bands are clipped by the axes at 0 and 100 %: where a band polygon is cut away (entirely at/below 0 %) the sd columns are empty",
        "series: priming_average black #1c0f29 solid; binocular_conscious_state1 orange #fcae34 solid; binocular_conscious_state2 purple",
        "  #543379 solid; binocular_suppressed_state1 orange dashed; binocular_suppressed_state2 purple dashed",
        "precision: ~0.2 % units (solid), ~0.5 % units (dashed)"]))
    print("j: bands found for", sorted(bands))


# ====================================================================== panel k
def panel_k():
    clip = pp.R(260, 345, 392, 487)
    dr = draws_in(clip)
    subs = {"average": (GREY, pp.R(275, 350, 335, 405), pp.R(275, 400, 335, 406), pp.R(275, 350, 285, 405)),
            "state1": (ORANGE, pp.R(275, 415, 335, 470), pp.R(275, 465, 335, 471), pp.R(275, 415, 285, 470)),
            "state2": (PURPLE, pp.R(335, 415, 392, 470), pp.R(335, 465, 392, 471), pp.R(335, 415, 345, 470))}
    out = {}
    tgrid = None
    for nm, (col, box, xreg, yreg) in subs.items():
        xax = pp.axis_from_ticks(dr, "x", [0, 1, 2], region=xreg)
        yax = pp.axis_from_ticks(dr, "y", [0, 50, 100], region=yreg)
        st = [d for d in dr if d["kind"] == "stroke" and pp.hexcolor(d["color"]) == col and d["n_items"] > 100][0]
        pts = np.array(st["points"])
        t = np.array([xax(x) for x in pts[:, 0]])
        tr = np.round(t, 2)
        assert np.abs(t - tr).max() < 0.002, (nm, np.abs(t - tr).max())
        # the stroke has 212 points: the 10-ms grid -0.1..2.0 s (211 points) plus a duplicated end sample 0.2 ms after
        # t = 2.0 s at the same y; keep the first point of each 10-ms time value
        keep = np.r_[True, np.diff(tr) > 0]
        pts, t, tr = pts[keep], t[keep], tr[keep]
        if tgrid is None:
            tgrid = tr
        assert np.allclose(tgrid, tr), nm
        xs = pts[:, 0]
        cons = np.array([yax(y) for y in pts[:, 1]])
        fl = [d for d in dr if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == col and not d["has_curves"] and d["n_items"] > 100][0]
        ypix, info = recover_dashed(fl["subpaths"], xs, 1.0, drop_lines=[("y", yax.inv(0)), ("y", yax.inv(100))], group_gap=-1)
        supp = np.array([yax(v) if not np.isnan(v) else np.nan for v in ypix])
        print("   k", nm, "stroke pts", len(pts), "dashed fit rms %.3f pt, outliers %.1f%%, recovered %d/%d time points" % (info["resid_rms"], 100 * info["frac_outlier"], (~np.isnan(supp)).sum(), len(supp)), "x resid", xax.resid, "y resid", yax.resid)
        out[nm] = (cons, supp)
    hdr = ["time_s", "average_conscious_pct", "average_suppressed_pct", "state1_conscious_pct", "state1_suppressed_pct", "state2_conscious_pct", "state2_suppressed_pct"]
    rows = [[float(tgrid[i])] + [fmt(out[nm][j][i], 2) for nm in ("average", "state1", "state2") for j in (0, 1)] for i in range(len(tgrid))]
    pp.write_csv("fig2k.csv", hdr, rows, prov("k", [
        "Three sub-panels (Average, State 1, State 2), each: solid line = stroke path with 211 vertices at 10-ms steps from -0.1 to 2.0 s",
        "  (= conscious); dashed line = outlined dash polygons (= suppressed), recovered by polyline fit at the same time grid.",
        "Dashed lines are only recoverable where a dash is drawn: time points falling inside the gaps between dashes are EMPTY (NaN);",
        "  about 60 % of the time points of each suppressed series are recovered.",
        "Each sub-panel's x axis calibrated on its ticks 0,1,2 and y axis on 0,50,100 % (resid < 1e-3). The axis title in the paper says",
        "  'Time from flash (ms)' but the ticks 0, 1, 2 are seconds (the trial is 2 s long); the column is time in seconds.",
        "colours: average grey #808080, state 1 orange #fcae34, state 2 purple #543379",
        "precision: ~0.3 % units"]))
    print("k:", len(rows), "rows")


# ====================================================================== panel l
def panel_l():
    clip = pp.R(388, 345, 519, 487)
    dr = draws_in(clip)
    yax = pp.axis_from_ticks(dr, "y", [0, 20, 40, 60, 80, 100], region=pp.R(405, 350, 415, 470))
    xt = pp.tick_marks(dr, "x", region=pp.R(410, 465, 519, 472))
    xcat = sorted(set(round(t["pos"], 2) for t in xt))
    assert len(xcat) == 3, xcat
    cats = ["average", "state1", "state2"]
    rows = []
    thin_solid = [d for d in dr if d["kind"] == "stroke" and d["n_items"] == 2 and d["width"] < 0.5 and pp.hexcolor(d["color"]) == "#000000"]
    thick_solid = [d for d in dr if d["kind"] == "stroke" and d["n_items"] == 2 and d["width"] >= 0.5 and pp.hexcolor(d["color"]) == "#000000"]
    dashed = [d for d in dr if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == "#000000" and not d["has_curves"] and len(d["subpaths"]) > 5]
    thick_dashed = [d for d in dashed if stroke_width_of_outline(d) > 0.5]
    thin_dashed = [d for d in dashed if stroke_width_of_outline(d) <= 0.5]
    print("   l: thin solid", len(thin_solid), "thick solid", len(thick_solid), "thin dashed", len(thin_dashed), "thick dashed", len(thick_dashed))

    def vals_stroke(d):
        pts = np.array(d["points"])
        return [yax(pts[np.argmin(np.abs(pts[:, 0] - x)), 1]) for x in xcat]

    def vals_dashed(d, w):
        ypix, spread = dashed_vertices(dash_centrelines(d["subpaths"], w), xcat)
        return [yax(v) for v in ypix], dict(spread=spread)

    for i, d in enumerate(thin_solid):
        v = vals_stroke(d); rows.append([f"session_{i+1}", "conscious"] + [fmt(x, 2) for x in v])
    for i, d in enumerate(thin_dashed):
        v, info = vals_dashed(d, stroke_width_of_outline(d)); rows.append([f"session_{i+1}", "suppressed"] + [fmt(x, 2) for x in v])
    v = vals_stroke(thick_solid[0]); rows.append(["mean", "conscious"] + [fmt(x, 2) for x in v])
    v, info = vals_dashed(thick_dashed[0], 1.0); rows.append(["mean", "suppressed"] + [fmt(x, 2) for x in v])
    # markers (circles): filled = conscious mean, open (white centre) = suppressed mean
    mk = []
    for d in dr:
        if d["kind"] == "fill" and d["has_curves"] and d["n_items"] == 4:
            x0, y0, x1, y1 = d["rect"]
            if 3 < x1 - x0 < 5:
                mk.append((round((x0 + x1) / 2, 2), yax((y0 + y1) / 2), pp.hexcolor(d["fill"])))
    mrow = {}
    for cx, val, col in mk:
        ci = int(np.argmin([abs(cx - x) for x in xcat]))
        mrow.setdefault("suppressed" if col == "#ffffff" else "conscious", {})[cats[ci]] = val
    for cond in ("conscious", "suppressed"):
        rows.append(["mean_marker", cond] + [fmt(mrow[cond].get(c), 2) for c in cats])
    pp.write_csv("fig2l.csv", ["line", "condition", "average_pct", "state1_pct", "state2_pct"], rows, prov("l", [
        "Thin lines (10 sessions): solid = conscious (stroke paths, width 0.14 pt), dashed = suppressed (outlined dash polygons, centre lines",
        "  extended to the category x positions). Thick lines = mean across sessions (stroke width 1 pt). 'mean_marker' rows = circle marker centres",
        "  (filled circle = conscious, open circle = suppressed); they coincide with the thick lines' vertices.",
        "Session numbering is the drawing order within each condition; the PDF does not say which solid line and which dashed line",
        "  belong to the same session (the same drawing order is likely but not verifiable).",
        f"y axis calibrated on ticks 0..100 % (resid {yax.resid:.1e}); x = 3 categories (Average, State 1, State 2); chance = 10 %",
        "colours: markers grey #808080 (Average), orange #fcae34 (State 1), purple #543379 (State 2); lines black",
        "precision: ~0.2 % units (thin dashed lines ~0.5)"]))
    print("l:", len(rows), "rows")


# ====================================================================== panel b (raster)
def panel_b():
    clip = pp.R(127, 12, 378, 101)
    dr = draws_in(clip)
    xax = pp.axis_from_ticks(dr, "x", [-1, -0.5, 0, 0.5, 1], region=pp.R(130, 79, 378, 95), min_len=2.0)
    spikes = np.array([d["points"][0] + d["points"][1] for d in dr if d["kind"] == "stroke" and d["n_items"] == 1 and abs(d["width"] - 1.0) < 0.02 and len(d["points"]) == 2 and abs(d["points"][0][1] - d["points"][1][1]) < 1e-6 and 30 < d["points"][0][1] < 80])
    yt = sorted(t["pos"] for t in pp.tick_marks(dr, "y", region=pp.R(130, 20, 150, 95)))
    ytop, ybot = yt[0], yt[-1]
    N = 411
    yc = spikes[:, 1]
    pitch, yref = fit_pitch(yc)             # row grid fitted on the spike rows themselves
    span = (ybot - ytop) / pitch            # = 411.0 row pitches: bottom tick = cell 1, top tick = one pitch above cell 411
    idx_bottom = 1 + (ybot - yc) / pitch    # cell index, 1 = bottom row (at the bottom tick)
    err = np.abs(idx_bottom - np.round(idx_bottom)).max()
    idx_bottom = np.round(idx_bottom).astype(int)
    assert idx_bottom.min() >= 1 and idx_bottom.max() <= N, (idx_bottom.min(), idx_bottom.max())
    row_top = N + 1 - idx_bottom
    print(f"b: axis spans {span:.2f} row pitches; spikes in cells {idx_bottom.min()}..{idx_bottom.max()}")
    t0 = np.array([xax(x) for x in spikes[:, 0]]); t1 = np.array([xax(x) for x in spikes[:, 2]])
    ms = np.round(t0 * 1000)
    err_ms = np.abs(t0 * 1000 - ms).max()
    sep = [d for d in dr if d["kind"] == "stroke" and d["n_items"] == 1 and abs(d["width"] - 0.25) < 0.02 and abs(d["points"][0][1] - d["points"][1][1]) < 1e-6 and d["points"][1][0] - d["points"][0][0] > 100][0]
    sep_idx = 1 + (ybot - sep["points"][0][1]) / pitch
    vline = [d for d in dr if d["kind"] == "stroke" and d["n_items"] == 1 and abs(d["width"] - 0.5) < 0.02 and abs(d["points"][0][0] - d["points"][1][0]) < 1e-6 and d["points"][1][1] - d["points"][0][1] > 40][0]
    print(f"b: {len(spikes)} spikes, row rounding error {err:.3f} rows, ms rounding error {err_ms:.3f} ms, pitch {pitch:.5f}, separator at cell index (from bottom) {sep_idx:.2f}, vertical line at t = {xax(vline['points'][0][0]):.4f} s, bin width {np.median(t1 - t0) * 1000:.3f} ms")
    order = np.lexsort((ms, row_top))
    rows = [[int(row_top[i]), "ML" if row_top[i] <= 157 else "AM", int(ms[i]) / 1000.0] for i in order]
    pp.write_csv("fig2b_spikes.csv", ["row_from_top", "region", "time_s"], rows, prov("b", [
        f"{len(spikes)} spikes, each drawn in the PDF as a horizontal 1-ms-wide stroke (1 pt thick) at the cell's row; time_s = start of the 1-ms bin",
        f"x axis calibrated on ticks -1,-0.5,0,0.5,1 s (resid {xax.resid:.1e}); rows: 411 cells evenly spaced between the two y-axis end ticks",
        f"  (cell 411 at the top, cell 1 at the bottom, pitch {pitch:.4f} pt); row_from_top = 1 (top) .. 411 (bottom); row rounding error < {err:.2f} rows",
        f"region: ML = rows 1-157 (above the thin horizontal separator line at row {N + 1 - sep_idx:.2f}), AM = rows 158-411 (legend: 157 ML + 254 AM cells)",
        "vertical black line at t = 0 (flash); state shading in fig2b_states.csv"]))
    # state shading
    sh = [d for d in dr if d["kind"] == "fill" and pp.hexcolor(d["fill"]) in (ORANGE, PURPLE) and d["rect"][3] - d["rect"][1] > 40]
    sh.sort(key=lambda d: d["rect"][0])
    srows = []
    for d in sh:
        x0, _, x1, _ = d["rect"]
        srows.append([fmt(xax(x0), 4), fmt(xax(x1), 4), 1 if pp.hexcolor(d["fill"]) == ORANGE else 2])
    pp.write_csv("fig2b_states.csv", ["t_start_s", "t_end_s", "state"], srows, prov("b", [
        f"{len(sh)} filled background rectangles (orange #fcae34 = state 1, purple #543379 = state 2) spanning the full raster height;",
        "  consecutive rectangles abut (gaps < 0.01 pt); times from the same x calibration as fig2b_spikes.csv; precision ~1 ms",
        "the first rectangle starts at -1.0 s and the last ends at +1.0 s"]))
    print("b: states", len(srows), srows[0], srows[-1])
    # stimulus icons above the raster
    ims = pp.images(page, pp.R(180, 10, 330, 26))
    seen = {}
    for im in ims:
        if im["xref"] not in seen:
            seen[im["xref"]] = im
    names = {}
    for i, (xref, im) in enumerate(sorted(seen.items(), key=lambda kv: kv[1]["bbox"][0])):
        nm = f"fig2b_icon_face{i+1}.png"
        w, h = pp.extract_image(page, xref, nm); names[xref] = nm
        print("   icon", nm, w, h, "placed at", [round(v, 1) for v in im["bbox"]])
    print("   icon placements:", [(names[im["xref"]], round(xax(im["bbox"][0]), 3), round(xax(im["bbox"][2]), 3)) for im in ims])


# ====================================================================== panels e, f, g (rasters)
def raster(name, clip, width, nrows, tickreg, yreg, horizontal, csvname, extra):
    dr = draws_in(clip)
    xax = pp.axis_from_ticks(dr, "x", [-50, 0, 50], region=tickreg, min_len=1.5)
    sp = []
    for d in dr:
        if d["kind"] == "stroke" and d["n_items"] == 1 and abs(d["width"] - width) < 0.02 and len(d["points"]) == 2:
            (x0, y0), (x1, y1) = d["points"]
            if horizontal and abs(y0 - y1) < 1e-6 and x1 - x0 < 1.0:
                sp.append((x0, y0, x1, y1))
            elif not horizontal and abs(x0 - x1) < 1e-6 and 1 < abs(y1 - y0) < 5:
                sp.append((x0, y0, x1, y1))
    sp = np.array(sp)
    yc = (sp[:, 1] + sp[:, 3]) / 2
    pitch, yref = fit_pitch(yc)
    yt = sorted(t["pos"] for t in pp.tick_marks(dr, "y", region=yreg))
    ytop, ybot = yt[0], yt[-1]
    span = (ybot - ytop) / pitch
    # y value of the bottom tick: the axes span nrows-1 pitches (ticks at rows 1 and N) or nrows+1 (ticks at 0 and N+1)
    if abs(span - (nrows - 1)) < 0.3:
        v_bot = 1.0
    elif abs(span - (nrows + 1)) < 0.3:
        v_bot = 0.0
    else:
        raise RuntimeError(f"{name}: axis spans {span:.2f} pitches for {nrows} rows")
    val = v_bot + (ybot - yc) / pitch       # MATLAB y value of each spike (row 1 = bottom)
    err = np.abs(val - np.round(val)).max()
    val = np.round(val).astype(int)
    row = nrows + 1 - val                   # row counted from the top
    assert row.min() >= 1 and row.max() <= nrows, (name, row.min(), row.max())
    print(f"   {name}: axis spans {span:.2f} pitches (bottom tick = row value {v_bot}); spikes in rows {row.min()}..{row.max()} from top")
    t = np.array([xax(x) for x in sp[:, 0]])
    tms = np.round(t, 0 if horizontal else 2)
    err_t = np.abs(t - tms).max()
    # separator (solid horizontal 0.5-pt line) and time-zero line
    sep = [d for d in dr if d["kind"] == "stroke" and d["n_items"] == 1 and abs(d["width"] - 0.5) < 0.02 and abs(d["points"][0][1] - d["points"][1][1]) < 1e-6 and abs(d["points"][1][0] - d["points"][0][0]) > 20]
    sep_row = nrows + 1 - (v_bot + (ybot - sep[0]["points"][0][1]) / pitch) if sep else None
    order = np.lexsort((tms, row))
    rows = []
    for i in order:
        r = [int(row[i]), float(tms[i])]
        if sep_row is not None:
            r.append("conscious" if row[i] < sep_row else "suppressed")
        rows.append(r)
    hdr = ["row_from_top", "time_ms"] + (["cell_prefers"] if sep_row is not None else [])
    pp.write_csv(csvname, hdr, rows, prov(name[0], [
        f"{len(sp)} spikes; " + ("each drawn as a horizontal 1-ms-wide stroke (0.3 pt thick) at its row; time_ms = start of the 1-ms bin" if horizontal else "each drawn as a vertical tick (one row high); time_ms rounded to 0.01 ms"),
        f"x axis calibrated on ticks -50, 0, 50 ms (resid {xax.resid:.1e}); rows: {nrows} evenly spaced rows (pitch {pitch:.4f} pt), row_from_top = 1 at the top;",
        f"  row rounding error < {err:.2f} rows; time rounding error < {err_t:.3f} ms"] + extra +
        ([f"solid horizontal separator line at row {sep_row:.1f} (cells above prefer the conscious face, below the suppressed face)"] if sep_row is not None else [])))
    print(f"{name}: {len(sp)} spikes, rows {row.min()}-{row.max()} of {nrows}, row err {err:.3f}, t err {err_t:.3f} ms, pitch {pitch:.5f}, sep_row {sep_row}, x range {t.min():.1f}..{t.max():.1f}")
    return sep_row


def panels_efg():
    raster("e_left_state2_to_state1", pp.R(140, 105, 200, 172), 0.3, 2178, pp.R(140, 165, 200, 172), pp.R(140, 105, 146, 170), True, "fig2e_state2_to_state1.csv",
           ["left raster of panel e: 2178 cell-transitions aligned to State 2 -> State 1 transitions; thin vertical line at t = 0"])
    raster("e_right_state1_to_state2", pp.R(205, 105, 262, 172), 0.3, 1936, pp.R(205, 165, 262, 172), pp.R(209, 105, 215, 170), True, "fig2e_state1_to_state2.csv",
           ["right raster of panel e: 1936 cell-transitions aligned to State 1 -> State 2 transitions; thin vertical line at t = 0"])
    raster("f_left_state2_to_state1", pp.R(285, 105, 340, 172), 0.14, 22, pp.R(285, 165, 340, 172), pp.R(287, 105, 293, 170), False, "fig2f_state2_to_state1.csv",
           ["left raster of panel f (example ML neuron preferring the conscious face): 22 transitions State 2 -> State 1; dashed vertical line at t = 0"])
    raster("f_right_state1_to_state2", pp.R(342, 105, 400, 172), 0.14, 17, pp.R(342, 165, 400, 172), pp.R(345, 105, 351, 170), False, "fig2f_state1_to_state2.csv",
           ["right raster of panel f: 17 transitions State 1 -> State 2; dashed vertical line at t = 0"])
    raster("g_left_state2_to_state1", pp.R(408, 105, 460, 172), 0.14, 22, pp.R(408, 165, 460, 172), pp.R(411, 105, 417, 170), False, "fig2g_state2_to_state1.csv",
           ["left raster of panel g (example AM neuron preferring the suppressed face): 22 transitions State 2 -> State 1; dashed vertical line at t = 0"])
    raster("g_right_state1_to_state2", pp.R(462, 105, 519, 172), 0.14, 17, pp.R(462, 165, 519, 172), pp.R(466, 105, 471, 170), False, "fig2g_state1_to_state2.csv",
           ["right raster of panel g: 17 transitions State 1 -> State 2; dashed vertical line at t = 0"])


# ====================================================================== image panels a, h
def panel_a():
    # clip starts below the bold panel letter 'a' (bbox y 17.7-26.6) so that the tex snippet's own letter is not doubled
    w, h = pp.render(page, pp.R(4, 27, 126, 98), 300, "fig2a.png")
    print("a: rendered", w, h)


def panel_h():
    ims = pp.images(page, pp.R(5, 210, 250, 482))
    cols = sorted(set(round(im["bbox"][0]) for im in ims))
    rowsy = sorted(set(round(im["bbox"][1]) for im in ims))
    # cluster rows (bboxes differ by <1 pt between 143- and 144-px images)
    def cluster(vals, tol=3):
        out = []
        for v in vals:
            if out and abs(v - out[-1][-1]) <= tol:
                out[-1].append(v)
            else:
                out.append([v])
        return [np.mean(c) for c in out]
    cols = cluster(cols); rowsy = cluster(rowsy)
    assert len(cols) == 4 and len(rowsy) == 5, (cols, rowsy)
    colname = ["gt_conscious", "recon_state1", "gt_suppressed", "recon_state2"]
    for im in ims:
        ci = int(np.argmin([abs(im["bbox"][0] - c) for c in cols])); ri = int(np.argmin([abs(im["bbox"][1] - r) for r in rowsy]))
        nm = f"fig2h_r{ri+1}_{colname[ci]}.png"
        w, h = pp.extract_image(page, im["xref"], nm)
        print("   h", nm, w, h, "xref", im["xref"])


if __name__ == "__main__":
    os.chdir(HERE)
    which = sys.argv[1:] or ["a", "b", "c", "d", "efg", "h", "i", "j", "k", "l"]
    for w in which:
        {"a": panel_a, "b": panel_b, "c": panel_c, "d": panel_d, "efg": panels_efg, "h": panel_h,
         "i": panel_i, "j": panel_j, "k": panel_k, "l": panel_l}[w]()
