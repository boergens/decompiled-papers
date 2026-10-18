"""Extraction script for Figure 6 (page 40) of Hesse et al. 2026.

Run from anywhere:  python3 fig6_extract.py [a|b|c|d|e|f|all]
Writes the CSVs, the embedded face images and the original 300-dpi crops into this folder.
Uses tools/pdfplot.py.  Everything is in PDF points (origin top-left, y down).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import math
import os
import sys
from collections import defaultdict

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "..", "tools"))
import pdfplot as pp  # noqa: E402

PDF = os.path.join(ROOT, "source", "2026.10.15.759299v1.full.pdf")
OUT = os.path.join(ROOT, "figures")
PAGE = 40
page = pp.open_page(PDF, PAGE)

COL = {"#1c0f29": "priming_average", "#fcae34": "state1", "#543379": "state2"}
SERIES_RGB = {"priming_average": "#1c0f29", "state1": "#fcae34", "state2": "#543379"}


# --------------------------------------------------------------------------- dash polygons
def _edges(sp):
    pts = list(sp)
    if len(pts) > 1 and abs(pts[0][0] - pts[-1][0]) < 1e-6 and abs(pts[0][1] - pts[-1][1]) < 1e-6:
        pts = pts[:-1]
    n = len(pts)
    out = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 0.12:
            continue
        out.append((a, b, L, ((b[0] - a[0]) / L, (b[1] - a[1]) / L)))
    return out


def dash_pieces(d, width=1.0, tol=0.1):
    """Centre-line pieces of a dashed line that was exported as filled dash polygons of stroke width
    `width`.  Each straight dash piece is a quad whose two long sides are antiparallel and `width`
    apart; the midpoints of corresponding corners lie on the centre line.  Returns a list of
    ((x0,y0),(x1,y1)) pieces (x0 <= x1)."""
    pieces = []
    for sp in d["subpaths"]:
        E = _edges(sp)
        for i, (a, b, L1, u1) in enumerate(E):
            for j, (c, dd, L2, u2) in enumerate(E):
                if j <= i:
                    continue
                if u1[0] * u2[0] + u1[1] * u2[1] > -0.995:
                    continue  # not antiparallel
                nx, ny = -u1[1], u1[0]
                dist = (c[0] - a[0]) * nx + (c[1] - a[1]) * ny
                if abs(abs(dist) - width) > tol:
                    continue
                pc = (c[0] - a[0]) * u1[0] + (c[1] - a[1]) * u1[1]
                pd = (dd[0] - a[0]) * u1[0] + (dd[1] - a[1]) * u1[1]
                # c must sit near the far end (b) and dd near the near end (a); overlap required
                if pd > pc or min(pc, L1) - max(pd, 0.0) < 0.1:
                    continue
                p0 = ((a[0] + dd[0]) / 2, (a[1] + dd[1]) / 2)
                p1 = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)
                if p0[0] > p1[0]:
                    p0, p1 = p1, p0
                pieces.append((p0, p1, min(L1, L2)))
    return pieces


def fit_polyline(pieces, grid, sigma_pt=0.005, resid_tol=0.03, min_len=0.55):
    """Global least-squares fit of the polyline vertices y_1..y_n (at grid x positions) to straight
    pieces ((x0,y0),(x1,y1),L).  Each piece is assigned to the segment [k,k+1] containing its midpoint
    and contributes two equations y = (1-t)*y_k + t*y_{k+1}.  Pieces with residual > resid_tol pt are
    rejected iteratively (spurious cap/cap pairings).  Returns dict with arrays y (pt, NaN where
    undetermined), sigma (pt; propagated from sigma_pt per coordinate), n_pieces (pieces touching the
    vertex within 0.02 pt), n_seg (pieces in the two adjacent segments) and the list of rejected pieces."""
    n = grid.n
    eqs = []  # (k0, t, y, piece_id)
    for pid, (p0, p1, L) in enumerate(pieces):
        if L < min_len:
            continue
        xm = (p0[0] + p1[0]) / 2
        k = int(math.floor(grid.inv(xm)))
        k = max(1, min(n - 1, k))
        for (x, y) in (p0, p1):
            t = (x - grid(k)) / grid.step
            eqs.append((k, t, y, pid))
    rejected = set()
    slopes = np.zeros(n)  # per segment k (index k-1): dy/dx in pt/pt, for perpendicular residuals/weights
    for _ in range(200):
        act = [e for e in eqs if e[3] not in rejected]
        A = np.zeros((len(act), n))
        b = np.zeros(len(act))
        w = np.zeros(len(act))
        for i, (k, t, y, pid) in enumerate(act):
            A[i, k - 1] = 1 - t
            A[i, k] = t
            b[i] = y
            w[i] = 1.0 / (sigma_pt * math.sqrt(1 + slopes[k - 1] ** 2))
        cols = [j for j in range(n) if np.any(A[:, j] != 0)]
        Ac = A[:, cols]
        sol, res, rank, sv = np.linalg.lstsq(Ac * w[:, None], b * w, rcond=None)
        full = np.full(n, np.nan)
        for i, j in enumerate(cols):
            full[j] = sol[i]
        new_slopes = np.zeros(n)
        for k in range(1, n):
            if not (np.isnan(full[k - 1]) or np.isnan(full[k])):
                new_slopes[k - 1] = (full[k] - full[k - 1]) / grid.step
        r = Ac @ sol - b
        worst = {}
        for (k, t, y, pid), ri in zip(act, r):
            perp = abs(ri) / math.sqrt(1 + new_slopes[k - 1] ** 2)
            worst[pid] = max(worst.get(pid, 0.0), perp)
        if np.max(np.abs(new_slopes - slopes)) > 1e-3:
            slopes = new_slopes
            continue  # re-weight and refit
        slopes = new_slopes
        if worst and max(worst.values()) > resid_tol:
            rejected.add(max(worst, key=worst.get))
            continue
        break
    # undetermined unknowns: null space of Ac
    y = np.full(n, np.nan)
    sig = np.full(n, np.nan)
    Aw = Ac * w[:, None]
    U, S, Vt = np.linalg.svd(Aw, full_matrices=True)
    null = Vt[(S > 1e-8 * S.max()).sum():]
    undet = np.zeros(len(cols), bool)
    if len(null):
        undet = (np.abs(null) > 1e-6).any(axis=0)
    cov = np.linalg.pinv(Aw.T @ Aw)
    for i, j in enumerate(cols):
        if undet[i]:
            continue
        y[j] = sol[i]
        sig[j] = math.sqrt(max(cov[i, i], 0.0))
    n_pieces = np.zeros(n, int)
    n_seg = np.zeros(n, int)
    for pid, (p0, p1, L) in enumerate(pieces):
        if pid in rejected or L < min_len:
            continue
        for k in range(1, n + 1):
            xk = grid(k)
            if p0[0] - 0.02 <= xk <= p1[0] + 0.02:
                n_pieces[k - 1] += 1
            lo = grid(k - 1) if k > 1 else xk
            hi = grid(k + 1) if k < n else xk
            if p0[0] >= lo - 0.03 and p1[0] <= hi + 0.03:
                n_seg[k - 1] += 1
    return dict(y=y, sigma=sig, n_pieces=n_pieces, n_seg=n_seg,
                rejected=[pieces[p] for p in sorted(rejected)], n_used=len(pieces) - len(rejected))


def stroke_pieces(d):
    """Straight pieces between consecutive points of a stroke polyline (possibly clipped/split)."""
    pieces = []
    for sp in d["subpaths"]:
        for (x0, y0), (x1, y1) in zip(sp[:-1], sp[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 1e-6:
                continue
            if x0 <= x1:
                pieces.append(((x0, y0), (x1, y1), L))
            else:
                pieces.append(((x1, y1), (x0, y0), L))
    return pieces


class Grid:
    """x position of data index k: x = x1 + (k-1)*step (k=1..n)."""

    def __init__(self, x1, step, n):
        self.x1, self.step, self.n = x1, step, n

    def __call__(self, k):
        return self.x1 + (k - 1) * self.step

    def inv(self, x):
        return 1 + (x - self.x1) / self.step


def series_rows(fit, grid, yax, clip_y=None):
    """Turn a fit into rows: k, y_pt, value, sigma_value, visible, n_pieces, n_seg."""
    rows = []
    for k in range(1, grid.n + 1):
        y = fit["y"][k - 1]
        if np.isnan(y):
            rows.append(dict(k=k, y_pt=np.nan, value=np.nan, sigma=np.nan, visible=0, n_pieces=0, n_seg=0))
            continue
        s = fit["sigma"][k - 1]
        visible = 1 if (clip_y is None or y <= clip_y + 0.03) else 0
        rows.append(dict(k=k, y_pt=y, value=yax(y), sigma=abs(yax(y + s) - yax(y)), visible=visible,
                         n_pieces=int(fit["n_pieces"][k - 1]), n_seg=int(fit["n_seg"][k - 1])))
    return rows


DASH_MIN_LEN = 0.2


def fit_series(draw_list, grid, yax, clip_y=None, kind="dash"):
    """Fit one series from one or more drawings (stroke fragments or dash-polygon fills)."""
    pieces = []
    for d in draw_list:
        pieces += stroke_pieces(d) if kind == "stroke" else dash_pieces(d)
    fit = fit_polyline(pieces, grid, min_len=(0.1 if kind == "stroke" else DASH_MIN_LEN))
    return series_rows(fit, grid, yax, clip_y), pieces, fit


# --------------------------------------------------------------------------- overlay QA
def overlay(clip, dpi, items, out_png):
    """Render clip and draw recovered polylines/points on top (for checking)."""
    from PIL import Image, ImageDraw
    tmp = os.path.join(OUT, "_tmp_overlay.png")
    pp.render(page, clip, dpi, tmp)
    im = Image.open(tmp).convert("RGB")
    dr = ImageDraw.Draw(im)
    s = dpi / 72.0

    def P(x, y):
        return ((x - clip.x0) * s, (y - clip.y0) * s)

    for kind, pts, color in items:
        if kind == "line":
            dr.line([P(x, y) for x, y in pts], fill=color, width=1)
        elif kind == "pts":
            for x, y in pts:
                X, Y = P(x, y)
                dr.ellipse([X - 2, Y - 2, X + 2, Y + 2], outline=color)
    im.save(out_png)
    os.remove(tmp)


# =========================================================================== panels
def fmt(v, nd=3):
    return "" if (v is None or (isinstance(v, float) and math.isnan(v))) else f"{v:.{nd}f}"


SERIES_B = [  # (group key, line style) -> column name
    ("priming_average_solid", "priming_average_pct"),
    ("state1_solid", "binocular_conscious_state1_pct"),
    ("state2_solid", "binocular_conscious_state2_pct"),
    ("state1_dashed", "binocular_suppressed_state1_pct"),
    ("state2_dashed", "binocular_suppressed_state2_pct"),
]


def group_series(draws, min_dash_items=8):
    """Group the data paths of a panel by series colour and style."""
    groups = {}
    for d in draws:
        c = pp.hexcolor(d["color"] if d["kind"] == "stroke" else d["fill"])
        if c not in COL:
            continue
        if d["kind"] == "stroke":
            name = COL[c] + "_solid"
        elif d["kind"] == "fill" and len(d["subpaths"]) >= 4 and d["n_items"] >= min_dash_items:
            name = COL[c] + "_dashed"
        else:
            continue  # bands handled separately
        groups.setdefault(name, []).append(d)
    return groups


def panel_bd(letter, clip, xreg, yreg, csv_name):
    """Explained-variance panels b and d: 50 features, 5 series."""
    draws = pp.drawings(page, clip, how="inside")
    xax = pp.axis_from_ticks(draws, "x", [10, 20, 30, 40, 50], region=xreg)
    yax = pp.axis_from_ticks(draws, "y", [-100, -50, 0, 50, 100], region=yreg)
    print(f"[{letter}] x {xax}\n[{letter}] y {yax}")
    grid = Grid(xax.inv(1), xax.inv(2) - xax.inv(1), 50)
    clip_y = yax.inv(-100)
    groups = group_series(draws)
    table = {}
    offaxis = []
    prec = {}
    for key, colname in SERIES_B:
        lst = groups[key]
        kind = "stroke" if key.endswith("solid") else "dash"
        rows, pieces, fit = fit_series(lst, grid, yax, clip_y, kind)
        table[colname] = rows
        vis = [r["sigma"] for r in rows if r["visible"] and not np.isnan(r["value"])]
        prec[colname] = (max(vis) if vis else float("nan"), sum(1 for r in rows if r["visible"]),
                         sum(1 for r in rows if not r["visible"] and not np.isnan(r["value"])),
                         sum(1 for r in rows if np.isnan(r["value"])), len(fit["rejected"]))
        for r in rows:
            if not r["visible"] and not np.isnan(r["value"]):
                offaxis.append([colname, r["k"], fmt(r["value"], 2), fmt(r["sigma"], 2),
                                "extrapolated from the straight line segment(s) entering the clipped region; not drawn in the figure"])
            if np.isnan(r["value"]):
                nb = [table[colname][j - 1] for j in (r["k"] - 1, r["k"] + 1) if 1 <= j <= 50]
                if nb and all(x["visible"] for x in nb):
                    note = "vertex falls in a gap of the dash pattern with no dash in either adjacent segment: value not recoverable (neighbours are visible; the line passes through the gap)"
                else:
                    note = "below -100 and both adjacent segments fully clipped: value not recoverable"
                offaxis.append([colname, r["k"], "", "", note])
        print(f"[{letter}] {colname}: max sigma visible {prec[colname][0]:.3f}%, visible {prec[colname][1]}, off-axis {prec[colname][2]}, unrecoverable {prec[colname][3]}, rejected pieces {prec[colname][4]}")
    header = ["feature_index", "feature_type"] + [c for _, c in SERIES_B]
    out_rows = []
    for k in range(1, 51):
        row = [k, "shape" if k <= 20 else "appearance"]
        for _, c in SERIES_B:
            r = table[c][k - 1]
            row.append(fmt(r["value"], 2) if r["visible"] else "")
        out_rows.append(row)
    comments = [
        f"Figure 6{letter} (page {PAGE}), Hesse et al. 2026: explained variance of face features (%) vs feature index (1-20 shape, 21-50 appearance).",
        "Source: vector paths. Solid series = stroke polylines (1 vertex per feature). Dashed series were exported as filled dash polygons",
        "(stroke width 1 pt); their centre lines were recovered from the dash outlines and the 50 vertices fitted by least squares",
        "(polyline is straight between consecutive features).",
        f"x axis calibrated from tick marks at features 10,20,30,40,50 (resid {xax.resid:.2g} features); feature 1 lies on the y-axis line.",
        f"y axis calibrated from tick marks at -100,-50,0,50,100 % (resid {yax.resid:.2g} %).",
        "Precision: solid series ~0.01 % (coordinate rounding); dashed series typically 0.01-0.2 %.",
        "Empty cells: the line is below -100 % there (clipped by the axes in the original); see " + csv_name.replace(".csv", "_offaxis.csv") + ".",
        "Columns: priming_average = priming stimulus features predicted from average priming activity (black solid);",
        "binocular_conscious_stateN = conscious stimulus features from state N (solid); binocular_suppressed_stateN = suppressed stimulus features from state N (dashed).",
    ]
    pp.write_csv(os.path.join(OUT, csv_name), header, out_rows, comments)
    pp.write_csv(os.path.join(OUT, csv_name.replace(".csv", "_offaxis.csv")),
                 ["series", "feature_index", "extrapolated_value_pct", "precision_pct", "note"], offaxis,
                 [f"Figure 6{letter}: feature values that lie below the -100 % axis limit (not drawn in the original; the line leaves the axes).",
                  "Values are extrapolated from the visible straight line segments that enter/leave the clipped region (least-squares fit of the polyline);",
                  "precision_pct = 1-sigma propagated from 0.005 pt coordinate rounding. Use only to redraw the excursions; they are not plotted data points.",
                  "Rows with an empty value: both adjacent segments are entirely below -100 %, so nothing constrains the vertex."])
    return dict(xax=xax, yax=yax, grid=grid, table=table, prec=prec)


def band_envelope_grid(d, grid, yax, axis_bot, axis_top, line_y):
    """Band polygon (possibly clipped at the x axis = 0 % and at the top = 100 %) -> per grid index
    (hi_pt, lo_pt, clipped) with clipped = 0 (none), 1 (lower edge cut at 0 %), 2 (upper edge cut at 100 %).
    line_y: fitted line y (pt) per index, used to tell which edge survived when only one vertex is left."""
    by_k = defaultdict(list)
    for x, y in d["points"]:
        k = int(round(grid.inv(x)))
        if 1 <= k <= grid.n and abs(x - grid(k)) < 0.03:
            by_k[k].append(y)
    out = {}
    for k in range(1, grid.n + 1):
        ys = sorted(set(round(v, 4) for v in by_k.get(k, [])))
        if not ys:
            out[k] = (np.nan, np.nan, 0)
            continue
        hi, lo = min(ys), max(ys)
        clipped = 0
        ly = line_y[k - 1]
        if len(ys) == 1:
            if not np.isnan(ly) and ys[0] > ly + 0.02:      # the surviving vertex is below the line: lower edge
                hi, clipped = axis_top, 2
            elif not np.isnan(ly) and ys[0] < ly - 0.02:    # surviving vertex above the line: upper edge
                lo, clipped = axis_bot, 1
            elif abs(ys[0] - axis_bot) < 0.03:
                hi = lo = axis_bot
            elif np.isnan(ly):
                out[k] = (np.nan, np.nan, 3)  # one edge only, cannot tell which
                continue
        # clipped edges are projected onto the clip line (just outside the axes box) by the exporter
        if lo > axis_bot - 0.03 and hi < axis_bot - 0.03:
            lo, clipped = axis_bot, 1
        if hi < axis_top + 0.03 and lo > axis_top + 0.03:
            hi, clipped = axis_top, 2
        out[k] = (hi, lo, clipped)
    return out


def panel_ce(letter, clip, xreg, yreg, csv_name):
    """Decoding-accuracy panels c and e: number of faces 1..60, 5 series with shaded bands."""
    draws = pp.drawings(page, clip, how="inside")
    xax = pp.axis_from_ticks(draws, "x", [0, 20, 40, 60], region=xreg)
    yax = pp.axis_from_ticks(draws, "y", [0, 20, 40, 60, 80, 100], region=yreg)
    print(f"[{letter}] x {xax}\n[{letter}] y {yax}")
    grid = Grid(xax.inv(1), xax.inv(2) - xax.inv(1), 60)
    axis_bot, axis_top = yax.inv(0), yax.inv(100)
    groups = group_series(draws, min_dash_items=40)
    bands = [d for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) in COL and len(d["points"]) >= 70
             and len(d["subpaths"]) <= 3]
    table = {}
    prec = {}
    lines = {}
    for key, colname in SERIES_B:
        kind = "stroke" if key.endswith("solid") else "dash"
        rows, pieces, fit = fit_series(groups[key], grid, yax, None, kind)
        table[colname] = rows
        lines[colname] = np.array([r["y_pt"] for r in rows])
        vis = [r["sigma"] for r in rows if not np.isnan(r["value"])]
        prec[colname] = (max(vis), sum(1 for r in rows if np.isnan(r["value"])), len(fit["rejected"]))
        print(f"[{letter}] {colname}: max sigma {prec[colname][0]:.3f}%, missing {prec[colname][1]}, rejected {prec[colname][2]}")
    # assign bands to series: same colour, line inside the band at most x
    band_of = {}
    for b in bands:
        c = COL[pp.hexcolor(b["fill"])]
        cands = [cn for key, cn in SERIES_B if key.startswith(c)]
        best = None
        for cn in cands:
            env = band_envelope_grid(b, grid, yax, axis_bot, axis_top, lines[cn])
            ok = 0
            tot = 0
            for k in range(1, 61):
                hi, lo, cl = env[k]
                y = lines[cn][k - 1]
                if np.isnan(hi) or np.isnan(y):
                    continue
                tot += 1
                if hi - 0.05 <= y <= lo + 0.05:
                    ok += 1
            frac = ok / max(tot, 1)
            if best is None or frac > best[0]:
                best = (frac, cn, env)
        print(f"[{letter}] band {pp.hexcolor(b['fill'])} {len(b['points'])} pts, {len(b['subpaths'])} subpaths -> {best[1]} (line inside band at {best[0]*100:.0f}% of x)")
        if best[1] in band_of:
            print("   WARNING: two bands assigned to", best[1])
        band_of[best[1]] = best[2]
    # validation + gap filling: bands are symmetric about the line (checked on the solid series)
    filled = defaultdict(list)
    symcheck = {}
    for _, c in SERIES_B:
        env = band_of.get(c)
        if env is None:
            continue
        diffs = []
        for k in range(1, 61):
            hi, lo, cl = env[k]
            r = table[c][k - 1]
            if cl or np.isnan(hi):
                continue
            mid = (hi + lo) / 2
            if np.isnan(r["y_pt"]):
                r["y_pt"], r["value"], r["sigma"] = mid, yax(mid), abs(yax(mid + 0.005) - yax(mid))
                r["source"] = "band_midpoint"
                filled[c].append(k)
            else:
                diffs.append(mid - r["y_pt"])
        symcheck[c] = (float(np.max(np.abs(diffs))) if diffs else float("nan"), len(diffs))
        print(f"[{letter}] {c}: band midpoint vs line max |diff| {symcheck[c][0]:.4f} pt over {symcheck[c][1]} x; gap vertices filled from band midpoint: {filled[c]}")
        still = [k for k in range(1, 61) if np.isnan(table[c][k - 1]["value"])]
        if still:
            print(f"[{letter}] {c}: STILL MISSING (dash gap and band clipped): {still}")
    header = ["number_of_faces"]
    for _, c in SERIES_B:
        base = c[:-4]
        header += [c, base + "_band_lo_pct", base + "_band_hi_pct"]
    out_rows = []
    nclip = defaultdict(int)
    for k in range(1, 61):
        row = [k]
        for _, c in SERIES_B:
            r = table[c][k - 1]
            row.append(fmt(r["value"], 2))
            env = band_of.get(c)
            if env is None:
                row += ["", ""]
            else:
                hi, lo, cl = env[k]
                nclip[c] += (cl == 1)
                row += [fmt(yax(lo), 2) if not np.isnan(lo) else "", fmt(yax(hi), 2) if not np.isnan(hi) else ""]
        out_rows.append(row)
    comments = [
        f"Figure 6{letter} (page {PAGE}), Hesse et al. 2026: decoding accuracy (%) vs number of faces (1-60), 5 series with shaded bands.",
        "Source: vector paths. Solid series = stroke polylines (60 vertices); dashed series = filled dash polygons (centre lines recovered, vertices fitted by least squares).",
        "Bands = filled polygons (upper edge then lower edge); *_band_lo/_hi are the band edges at each x. The legend does not say what the shading is",
        "(presumably SEM across the n = 30 stimulus pairs).",
        f"x axis calibrated from tick marks at 0,20,40,60 faces (resid {xax.resid:.2g}); y axis from ticks at 0..100 % (resid {yax.resid:.2g} %).",
        "Precision: ~0.01 % for solid lines and band edges; dashed lines typically 0.01-0.1 %.",
        "Check: the band midpoints coincide with the fitted lines (max |difference| " + ", ".join(f"{c[:-4]} {symcheck[c][0]:.3f} pt" for _, c in SERIES_B if c in symcheck) + "; 1 pt = 1.11 %).",
    ]
    for _, c in SERIES_B:
        if filled[c]:
            comments.append(f"{c}: at number_of_faces {filled[c]} the vertex fell in a gap of the dash pattern; value taken as the band midpoint (band is symmetric about the line).")
        still = [k for k in range(1, 61) if np.isnan(table[c][k - 1]["value"])]
        if still:
            comments.append(f"{c}: empty at number_of_faces {still}: vertex in a dash gap and the band is clipped there, so the value is not recoverable (line is near 0 % there).")
    ntop = {c: sum(1 for k in range(1, 61) if band_of.get(c) and band_of[c][k][2] == 2) for _, c in SERIES_B}
    for _, c in SERIES_B:
        if ntop[c]:
            comments.append(f"{c[:-4]}_band_hi_pct is 100.00 at {ntop[c]} x positions where the band's upper edge was cut off at the top of the axes.")
    for _, c in SERIES_B:
        if nclip[c]:
            comments.append(f"{c[:-4]}_band_lo_pct is 0.00 at {nclip[c]} x positions where the band's lower edge was cut off by the x axis (clipped at 0 % in the original).")
    pp.write_csv(os.path.join(OUT, csv_name), header, out_rows, comments)
    return dict(xax=xax, yax=yax, grid=grid, table=table, prec=prec, band_of=band_of, nclip=nclip, filled=filled, symcheck=symcheck)


F_PANELS = [  # (suffix, title, x range of the axes box = x of the y-axis line .. right end of the x axis)
    ("all_states", "All states", (46.1, 108.4)),
    ("state1", "State 1", (168.7, 231.0)),
    ("state2", "State 2", (291.3, 353.6)),
    ("slope_equalized", "Slope-equalized", (413.9, 476.2)),
]


def panel_f():
    clip = pp.R(0, 325, 519, 425.28)
    draws = pp.drawings(page, clip, how="inside")
    res = {}
    for suffix, title, (xa, xb) in F_PANELS:
        sub = [d for d in draws if xa - 3 <= d["rect"][0] and d["rect"][2] <= xb + 3]
        xreg = pp.R(xa - 1, 399, xb + 1, 403)
        yreg = pp.R(xa - 3, 336, xa + 1, 403)
        xax = pp.axis_from_ticks(sub, "x", [-1, 0, 1], region=xreg)
        yax = pp.axis_from_ticks(sub, "y", [-1, 0, 1], region=yreg)
        marks = [m for m in pp.markers(sub, max_size=1.0) if m["has_curves"] and abs(m["w"] - m["h"]) < 0.05]
        pts = sorted(((xax(m["cx"]), yax(m["cy"])) for m in marks))
        # identity line: the 11-dash fill
        ident = [d for d in sub if d["kind"] == "fill" and d["n_items"] == 44]
        sign = None
        if ident:
            r = ident[0]["rect"]
            p0 = ident[0]["subpaths"][0]
            p1 = ident[0]["subpaths"][-1]
            # slope sign from first dash direction
            dx = p0[1][0] - p0[0][0]
            dy = p0[1][1] - p0[0][1]
            sign = -1 if dx * dy > 0 else 1  # y down: dy>0 with dx>0 means descending in data
        x = np.array([p[0] for p in pts])
        y = np.array([p[1] for p in pts])
        rr = np.corrcoef(x, y)[0, 1] if len(x) > 2 else float("nan")
        print(f"[f {suffix}] x {xax}\n[f {suffix}] y {yax}\n[f {suffix}] n markers {len(pts)}, Pearson r = {rr:.3f}, identity line y = {'+' if sign == 1 else '-'}x, "
              f"x range {x.min():.3f}..{x.max():.3f}, y range {y.min():.3f}..{y.max():.3f}")
        comments = [
            f"Figure 6f ('{title}', page {PAGE}), Hesse et al. 2026: modulation index binocular vs modulation index unambiguous, one point per cell-stimulus pair.",
            "Source: vector marker paths (filled circles, 0.72 pt diameter) inside the axes box; centre of each marker mapped through the tick calibration.",
            f"x axis calibrated from tick marks at -1, 0, 1 (resid {xax.resid:.2g}); y axis from tick marks at -1, 0, 1 (resid {yax.resid:.2g}).",
            "Precision ~0.0002 index units (marker centre rounding); overlapping markers are all listed separately.",
            f"n = {len(pts)} markers found (legend states n = 283 cell-stimulus pairs); Pearson r of the listed points = {rr:.3f}.",
            f"Reference lines in the panel: dashed zero lines x = 0 and y = 0, and the dashed identity line y = {'+' if sign == 1 else '-'}x.",
        ]
        pp.write_csv(os.path.join(OUT, f"fig6f_{suffix}.csv"), ["modulation_index_unambiguous", "modulation_index_binocular"],
                     [[f"{a:.4f}", f"{b:.4f}"] for a, b in pts], comments)
        res[suffix] = dict(n=len(pts), r=rr, sign=sign, xax=xax, yax=yax)
    return res


def panel_a():
    ims = pp.images(page, pp.R(0, 40, 250, 315))
    colnames = ["gt_conscious", "recon_state1", "gt_suppressed", "recon_state2"]
    rows = defaultdict(list)
    for im in ims:
        rows[int(round((im["bbox"][1] - 45) / 53.6))].append(im)
    for ri in sorted(rows):
        lst = sorted(rows[ri], key=lambda i: i["bbox"][0])
        assert len(lst) == 4, lst
        for ci, im in enumerate(lst):
            out = os.path.join(OUT, f"fig6a_r{ri + 1}_{colnames[ci]}.png")
            w, h = pp.extract_image(page, im["xref"], out)
            b = im["bbox"]
            print(f"[a] row {ri + 1} col {ci + 1} {colnames[ci]}: xref {im['xref']} {w}x{h}px placed at ({b[0]:.1f},{b[1]:.1f})-({b[2]:.1f},{b[3]:.1f}) pt")


def crops():
    for name, clip in [("b", pp.R(258, 14, 388, 160)), ("c", pp.R(386, 14, 519, 160)),
                       ("d", pp.R(258, 176, 388, 323)), ("e", pp.R(386, 176, 519, 323)),
                       ("legend", pp.R(258, 158, 519, 180)),
                       ("f_all_states", pp.R(20, 326, 131, 425)), ("f_state1", pp.R(143, 326, 253, 425)),
                       ("f_state2", pp.R(266, 326, 376, 425)), ("f_slope_equalized", pp.R(388, 326, 498, 425)),
                       ("a", pp.R(5, 18, 250, 315))]:
        pp.render(page, clip, 300, os.path.join(OUT, f"fig6{name}_orig.png"))


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("a", "all"):
        panel_a()
    if what in ("b", "all"):
        panel_bd("b", pp.R(258, 14, 388, 160), pp.R(290, 139, 388, 143), pp.R(284, 27, 289, 141), "fig6b.csv")
    if what in ("d", "all"):
        panel_bd("d", pp.R(258, 176, 388, 323), pp.R(290, 301, 388, 305.5), pp.R(284, 189, 289, 303.5), "fig6d.csv")
    if what in ("c", "all"):
        panel_ce("c", pp.R(386, 14, 519, 160), pp.R(412, 139, 519, 142.5), pp.R(410, 27, 414.5, 140), "fig6c.csv")
    if what in ("e", "all"):
        panel_ce("e", pp.R(386, 176, 519, 323), pp.R(412, 301, 519, 304.5), pp.R(410, 189, 414.5, 302), "fig6e.csv")
    if what in ("f", "all"):
        panel_f()
    if what in ("crops", "all"):
        crops()
