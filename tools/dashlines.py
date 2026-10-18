"""dashlines.py -- recover dashed data series from vector PDF figures whose dashed lines were exported as
FILLED DASH POLYGONS (one closed outline per dash; MATLAB -> Illustrator -> PDF does this), plus band
slicing and the band-symmetry validation.  Builds on tools/pdfplot.py; needs only numpy and PyMuPDF.

Usage: from a page + panel clip + tick values to a CSV of one dashed series
--------------------------------------------------------------------------
    import pdfplot as pp, dashlines as dl
    page  = pp.open_page(PDF, 36)                              # 1-based page number
    clip  = pp.R(260, 183, 392, 330)                           # panel bbox in PDF points (y down)
    draws = pp.drawings(page, clip, how="inside")
    xax   = pp.axis_from_ticks(draws, "x", [10, 20, 30, 40, 50], region=pp.R(285, 307, 392, 313))
    yax   = pp.axis_from_ticks(draws, "y", [-100, -50, 0, 50, 100], region=pp.R(280, 190, 290, 312))
    polys = dl.dash_polygons(draws, color="#fcae34", width=1.0)      # the dash fills of one series
    rows  = dl.dashed_series(polys, xax, yax, range(1, 51), width=1.0, y_limits=(-100, 100))
    pp.write_csv("series.csv", ["feature", "value_pct", "se_pct", "method", "flags"],
                 [[r["x"], r["value"], r["se"], r["method"], "+".join(r["flags"])] for r in rows],
                 comments=["dashed line recovered from dash polygons with tools/dashlines.py", ...])
    # bands (filled, usually translucent polygons around a line):
    band  = [d for d in draws if d["kind"] == "fill" and d["raw"].get("fill_opacity", 1) < 0.5][0]
    lo, hi = dl.band_extent(band["subpaths"][0], xax, yax, range(1, 51))
    print(dl.check_band_symmetry([r["value"] for r in rows], lo, hi))  # (max |mid-line|, mean, n)
    dl.overlay_png(page, clip, [([(r["x_pt"], r["y_pt"]) for r in rows if r["value"] is not None], (1, 0, 0))],
                   "qa.png")                                        # QA: recovered polyline on the 300-dpi crop

You need: the x positions of the polyline's vertices in DATA units (`x_grid`, e.g. 1..50 features, or the
x of a solid stroke's vertices mapped through xax), the stroke width of the dashed line in pt (`width`,
1.0 in the Hesse 2026 figures; measure it as the length of a dash's end cap if unknown), and the axis
limits (`y_limits`, data units) so that polygons cut by the axes box are handled.

How the dashes look (see the figure notes in hesse2026/README.md):
  * Each dash polygon is a chain of per-segment rectangles: two long sides offset +-width/2 from the centre
    line, butt caps of length `width` at both ends (perpendicular to the line).  Where a dash spans a
    polyline vertex V, a sharp join puts V itself into the outline (offset -> V -> offset, two edges of
    exactly width/2) with the antipodal offsets present; a shallow join is a plain miter, whose two miter
    points are point-symmetric about V.  Polygons are clipped to the axes box where the line leaves it.
  * Pitfalls handled (documented by the figure agents): width/2 'foot' edges and butt caps must not be
    paired with long sides; a single outline point sitting on a grid x is NOT a vertex read (cap corners
    and miter points of near-horizontal lines land there too); on near-vertical spikes two offsets of
    DIFFERENT segments can be point-symmetric about a point 0.03 pt off V (so vertex-point reads take
    priority and symmetric pairs are median-combined and checked against the segment fits).

Recovery per grid vertex (method / se):
  'vertex'       exact read: V in the outline, or the midpoint of a symmetric pair, or a cap sitting on the
                 vertex; se = coordinate precision (`prec`, 0.005 pt default, 0.01 % here).
  'segment_fit'  vertex inside a dash gap (or at a dash end): centre lines of the adjacent segments, fitted
                 to the antiparallel-side midlines + exact points, evaluated at x_k and combined by inverse
                 variance; if the gap contains exactly one unknown vertex the dash-pattern constraint (path
                 length end-cap -> V -> start-cap = pattern gap, constant along the line) is added
                 (flag 'pattern').  se = max(formal error, half the spread of the estimates).
  'gap_interp'   both adjacent segments lie inside one dash gap: linear interpolation between the
                 neighbours; se = geometric bound (the two segments fit into one pattern gap).
  None           nothing usable (flag 'gap'), or the line is outside the axes there (flag 'clipped').
Flags: 'gap' (vertex not covered by a dash), 'pattern' (dash-pattern constraint used), 'ambiguous' (two
pattern roots, nothing to choose between them: value is their mean, se their half distance), 'clipped'
(value outside y_limits: the exported line is cut there; the value is an extrapolation of the visible
straight segments, keep or blank as you see fit), 'anchor' (vertex read from a symmetric pair / cap
rather than the vertex point itself), 'offgrid' (exact read whose x is > 0.01 pt from the grid x).

Known limitations:
  * The line must be a polyline with KNOWN vertex x positions, monotone in x (a function of x); curves
    (bezier dashes, round caps) are rejected by dash_polygons (has_curves).  Butt caps are assumed.
  * Vertices whose two adjacent segments both lie inside one dash gap (flat line, pattern gap longer than
    two grid steps) are only interpolated ('gap_interp'); use the band midpoint (band_extent) if there is one.
  * `se` is a formal 1-sigma estimate from the coordinate precision and the extrapolation geometry (plus the
    spread between independent estimates); on near-vertical segments extrapolated far beyond the axes box
    it can be optimistic by a factor 2-3.  It is not a bound.
  * The dash-pattern constraint is skipped where dashes overlap in x (steep spikes) and next to polygons cut
    by the axes box; values flagged 'clipped' are extrapolations of the visible straight pieces.
  * dash_polygons filters by colour only: dashed reference lines of the same colour (zero lines, identity
    lines) must be removed by the caller (position / n_items).

Self-test:  python3 -I tools/dashlines.py [--overlay DIR]   (compares against the published hesse2026 CSVs)
"""
import math
import os
import sys

import numpy as np

PREC = 0.005          # assumed PDF coordinate precision (pt); coordinates in these figures are 0.001-0.01 pt
_TINY = 1e-9


# ---------------------------------------------------------------- small helpers

def _hex(c):
    if c is None:
        return None
    if isinstance(c, str):
        return c.lower()
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c[:3])


def _pts(poly):
    """Polygon -> (n,2) array without the repeated closing point."""
    p = np.asarray(poly, float)
    if len(p) > 1 and np.allclose(p[0], p[-1], atol=1e-9):
        p = p[:-1]
    return p


def _edges(pts):
    """Closed polygon points -> list of dict(p0, p1, L, u, mid) for every edge (including the closing one)."""
    n = len(pts)
    E = []
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        d = p1 - p0
        L = float(np.hypot(*d))
        E.append(dict(p0=p0, p1=p1, L=L, u=(d / L if L > _TINY else np.zeros(2)), mid=(p0 + p1) / 2))
    return E


def _pt_seg_dist(q, a, b):
    d = b - a
    L2 = float(d @ d)
    if L2 < 1e-12:
        return float(np.hypot(*(q - a)))
    t = min(1.0, max(0.0, float(((q - a) @ d) / L2)))
    return float(np.hypot(*(q - (a + t * d))))


def _antiparallel_pairs(E, width, skip, prec, min_edge, min_overlap, par_tol):
    """Pairs of antiparallel edges one `width` apart with the same offset at both ends (really parallel,
    not just nearly: the two sides of one straight piece of the stroke).  Yields dict(p0, p1, u) = the
    midline piece (p0.x <= p1.x)."""
    tol_w = max(0.06 * width, 4 * prec)
    out = []
    idx = [i for i, e in enumerate(E) if not skip[i] and e["L"] >= min_edge]
    for ii, i in enumerate(idx):
        a = E[i]
        nrm = np.array([-a["u"][1], a["u"][0]])
        for j in idx[ii + 1:]:
            b = E[j]
            if float(a["u"] @ b["u"]) > -0.99:
                continue
            off0 = float((b["p0"] - a["p0"]) @ nrm)
            off1 = float((b["p1"] - a["p0"]) @ nrm)
            if abs(off0 - off1) > par_tol:
                continue
            off = (off0 + off1) / 2
            if abs(abs(off) - width) > tol_w:
                continue
            s0 = float((b["p0"] - a["p0"]) @ a["u"])
            s1 = float((b["p1"] - a["p0"]) @ a["u"])
            lo, hi = max(0.0, min(s0, s1)), min(a["L"], max(s0, s1))
            if hi - lo < min_overlap:
                continue
            base = a["p0"] + nrm * (off / 2)
            # direction: length-weighted mean of the two (antiparallel) edges
            u = a["u"] * a["L"] - b["u"] * b["L"]
            u = u / np.hypot(*u)
            q0, q1 = base + a["u"] * lo, base + a["u"] * hi
            if q0[0] > q1[0]:
                q0, q1 = q1, q0
            if u[0] < 0:
                u = -u
            out.append(dict(p0=q0, p1=q1, u=u, L=hi - lo))
    return out


# ---------------------------------------------------------------- 1. find the dash polygons

def dash_polygons(draws, color=None, width=1.0, min_points=4):
    """The drawing paths (from pdfplot.drawings) that are dash polygons of a dashed series: opaque fills
    without curves whose fill colour is `color` ('#rrggbb' or (r,g,b); None = any colour) and that contain
    at least one closed subpath with two antiparallel edges exactly `width` apart (a straight piece of a
    stroke of that width).  Translucent band polygons, markers and glyph outlines are rejected.
    Returns the matching draw dicts (each may hold many dashes as subpaths)."""
    want = _hex(color)
    out = []
    for d in draws:
        if d.get("kind") not in ("fill", "fillstroke") or d.get("has_curves"):
            continue
        if want is not None and _hex(d.get("fill")) != want:
            continue
        raw = d.get("raw") or {}
        op = raw.get("fill_opacity")
        if op is not None and op < 0.99:
            continue
        polys = [sp for sp in d["subpaths"] if len(sp) >= min_points]
        if polys and any(_looks_like_dash(sp, width) for sp in polys):
            out.append(d)
    return out


def _looks_like_dash(sp, width, prec=PREC):
    pts = _pts(sp)
    if len(pts) < 3:
        return False
    E = _edges(pts)
    skip = [e["L"] < 0.1 * width for e in E]
    return bool(_antiparallel_pairs(E, width, skip, prec, min_edge=0.1 * width, min_overlap=0.05 * width, par_tol=0.02))


# ---------------------------------------------------------------- 2. parse one dash polygon

def _parse_polygon(sp, width, clip_y, prec, min_overlap):
    """-> dict(pts, V=[(x,y)] vertex points in the outline, caps=[dict(mid, u)] butt caps (u = direction of
    the adjacent sides, pointing into the dash is not needed), pieces=[dict(p0,p1,u,L)] centre-line pieces,
    anchors=[(mx,my,d)] midpoints of point-symmetric outline pairs, clipped=bool, xmin, xmax)."""
    pts = _pts(sp)
    E = _edges(pts)
    n = len(E)
    onclip = np.zeros(n, bool)
    if clip_y:
        for c in clip_y:
            onclip |= np.array([abs(e["p0"][1] - c) < 0.05 and abs(e["p1"][1] - c) < 0.05 for e in E])
    w2 = width / 2
    foot_tol = max(0.06 * width, 2 * prec)
    # vertex points: both adjacent edges of length width/2 and the antipodes of both neighbours in the outline
    V = []
    for i in range(n):
        ep, e = E[(i - 1) % n], E[i]
        if abs(ep["L"] - w2) < foot_tol and abs(e["L"] - w2) < foot_tol:
            v = pts[i]
            A, B = ep["p0"], e["p1"]
            ok = True
            for q in (2 * v - A, 2 * v - B):
                if not np.any(np.hypot(pts[:, 0] - q[0], pts[:, 1] - q[1]) < max(0.05 * width, 3 * prec)):
                    ok = False
            if ok:
                V.append((float(v[0]), float(v[1])))
    # butt caps: length = width, perpendicular to its two neighbours, which are (anti)parallel to each other
    caps = []
    cap_idx = set()
    for i, e in enumerate(E):
        if abs(e["L"] - width) > max(0.04 * width, 4 * prec) or onclip[i]:
            continue
        ep, en = E[(i - 1) % n], E[(i + 1) % n]
        if ep["L"] < _TINY or en["L"] < _TINY:
            continue
        if abs(float(ep["u"] @ en["u"])) < 0.97 or abs(float(e["u"] @ ep["u"])) > 0.1:
            continue
        # a real cap has no other outline point on it (the bevel edge of a hairpin spike has V on it)
        others = [p for j, p in enumerate(pts) if j not in (i, (i + 1) % n)]
        if any(_pt_seg_dist(p, e["p0"], e["p1"]) < max(0.08 * width, 2 * prec) for p in others):
            continue
        if any(np.hypot(*(e["p0"] - v)) < 0.52 * width and np.hypot(*(e["p1"] - v)) < 0.52 * width for v in map(np.array, V)):
            continue
        u = ep["u"] if ep["L"] >= en["L"] else en["u"]
        if u[0] < 0:
            u = -u
        caps.append(dict(mid=e["mid"], u=u))
        cap_idx.add(i)
    # centre-line pieces from antiparallel side pairs (caps, feet, clip edges, tiny edges excluded)
    skip = [onclip[i] or i in cap_idx or abs(e["L"] - w2) < min(0.03, foot_tol) or e["L"] < max(0.1 * width, 2 * prec)
            for i, e in enumerate(E)]
    pieces = _antiparallel_pairs(E, width, skip, prec, min_edge=max(0.1 * width, 2 * prec), min_overlap=min_overlap,
                                 par_tol=max(0.006, 1.5 * prec))
    # point-symmetric pairs (miter points of a join, cap corners, rectangle corners at a vertex)
    anchors = []
    m = len(pts)
    for i in range(m):
        for j in range(i + 1, m):
            d = float(np.hypot(*(pts[i] - pts[j])))
            if width - max(0.02, 2 * prec) <= d <= 1.6 * width:
                mid = (pts[i] + pts[j]) / 2
                anchors.append((float(mid[0]), float(mid[1]), d))
    return dict(pts=pts, V=V, caps=sorted(caps, key=lambda c: c["mid"][0]), pieces=pieces, anchors=anchors,
                clipped=bool(onclip.any()), xmin=float(pts[:, 0].min()), xmax=float(pts[:, 0].max()))


# ---------------------------------------------------------------- 3. the series

def _line_fit(P, W):
    """Weighted total-least-squares line through points P (n,2) with weights W.  -> (c, u, t, resid) with
    centre c, unit direction u (u.x >= 0), positions t along the line and perpendicular residuals; None if
    the points do not define a line."""
    if len(P) < 2:
        return None
    W = np.asarray(W, float)
    c = (P * W[:, None]).sum(0) / W.sum()
    Q = (P - c) * np.sqrt(W)[:, None]
    if np.ptp(P[:, 0]) + np.ptp(P[:, 1]) < 1e-6:
        return None
    _, S, Vt = np.linalg.svd(Q, full_matrices=False)
    u = Vt[0]
    if u[0] < 0:
        u = -u
    nrm = np.array([-u[1], u[0]])
    t = (P - c) @ u
    r = (P - c) @ nrm
    if np.ptp(t) < 1e-6:
        return None
    return c, u, t, r


def _eval_line(fit, x, prec):
    """y of the fitted line at x and its 1-sigma error (pt), regression-style: perpendicular precision p,
    n points spread s along the line, extrapolated a distance D from their centre, projected to vertical."""
    c, u, t, r = fit
    if abs(u[0]) < 1e-6:
        return None
    m = u[1] / u[0]
    y = c[1] + (x - c[0]) * m
    n = len(t)
    p = max(prec, float(np.sqrt(np.mean(r ** 2))) if n > 2 else prec)
    s2 = float(np.mean((t - t.mean()) ** 2))
    D = (x - c[0]) / u[0]
    var_perp = p * p * (1.0 / n + (D * D) / (n * s2) if s2 > 1e-12 else np.inf)
    return float(y), float(math.sqrt(var_perp) * math.sqrt(1 + m * m)), m


def dashed_series(draws_or_polys, xax, yax, x_grid, width=1.0, y_limits=None, prec=PREC, min_overlap=0.1,
                  pattern=True, interp=True, anchor_tol=0.015, verbose=False):
    """Recover the values of a dashed polyline at its vertices from the dash polygons.

    draws_or_polys: draw dicts (from dash_polygons / pdfplot.drawings) or closed polygons ([(x,y),...] in
                    PDF points) of ONE series.
    xax, yax:       pdfplot.Axis objects (PDF coordinate <-> data value).
    x_grid:         data-x positions of the polyline vertices (e.g. range(1, 51)); the line is straight
                    between consecutive grid positions.
    width:          stroke width of the dashed line in pt (the length of a dash's butt cap).
    y_limits:       (ymin, ymax) of the axes in data units: polygons are clipped there.  Values beyond the
                    limits are flagged 'clipped'; polygon edges on the clip lines are not treated as caps.
    prec:           PDF coordinate precision in pt (se floor).
    Returns one dict per grid position, in the order of x_grid:
      x, value (data units or None), se (data units or None), method ('vertex' | 'segment_fit' |
      'gap_interp' | None), flags (list of str, see module docstring), x_pt, y_pt, se_pt (PDF points),
      n_pieces (centre-line pieces in the two adjacent segments).
    """
    # ---- inputs
    polys_in = []
    for item in draws_or_polys:
        if isinstance(item, dict) and "subpaths" in item:
            polys_in += [sp for sp in item["subpaths"] if len(sp) >= 4]
        else:
            polys_in.append(item)
    xg_data = list(x_grid)
    xg_all = np.array([xax.inv(v) for v in xg_data], float)
    order = np.argsort(xg_all)
    xg = xg_all[order]
    n = len(xg)
    clip_y = [yax.inv(v) for v in y_limits] if y_limits is not None else None
    polys = [_parse_polygon(sp, width, clip_y, prec, min_overlap) for sp in polys_in]
    polys.sort(key=lambda P: P["xmin"])
    y = np.full(n, np.nan)
    se = np.full(n, np.nan)
    method = [None] * n
    flags = [[] for _ in range(n)]
    xtol = max(0.02, 4 * prec)

    def nearest(x):
        k = int(np.argmin(np.abs(xg - x)))
        return k, float(x - xg[k])

    # ---- segments: centre-line points and pieces per segment k = [xg[k], xg[k+1]]
    seg_pts = [[] for _ in range(max(n - 1, 0))]     # (x, y, weight)
    seg_pieces = [[] for _ in range(max(n - 1, 0))]  # dict(p0, p1, u, L)
    ends = []                                         # piece end points (x, y, |u_y|) for clip labelling
    for P in polys:
        for pc in P["pieces"]:
            x0, x1 = pc["p0"][0], pc["p1"][0]
            ends.append((x0, pc["p0"][1], abs(pc["u"][1])))
            ends.append((x1, pc["p1"][1], abs(pc["u"][1])))
            if x1 - x0 < 1e-9:
                continue  # vertical piece: belongs to no x interval
            # split at interior grid positions (a piece spanning several segments = collinear run)
            cuts = [x0] + [float(g) for g in xg if x0 + 1e-6 < g < x1 - 1e-6] + [x1]
            for a, b in zip(cuts[:-1], cuts[1:]):
                k = int(np.searchsorted(xg, (a + b) / 2, side="right") - 1)
                if k < 0 or k >= n - 1:
                    continue
                if xg[k] - 0.06 > a or b > xg[k + 1] + 0.06:
                    continue
                ya = pc["p0"][1] + (a - x0) * pc["u"][1] / pc["u"][0]
                yb = pc["p0"][1] + (b - x0) * pc["u"][1] / pc["u"][0]
                if b - a < min_overlap * 0.5:
                    continue
                seg_pieces[k].append(dict(p0=np.array([a, ya]), p1=np.array([b, yb]), u=pc["u"], L=math.hypot(b - a, yb - ya)))
        for c in P["caps"]:
            k = int(np.searchsorted(xg, c["mid"][0], side="right") - 1)
            if 0 <= k < n - 1 and xg[k] - xtol <= c["mid"][0] <= xg[k + 1] + xtol:
                seg_pts[k].append((c["mid"][0], c["mid"][1], 1.0))

    # ---- exact vertex reads
    exact = [[] for _ in range(n)]   # (y, se_pt, kind)
    for P in polys:
        for (vx, vy) in P["V"]:
            k, dx = nearest(vx)
            if abs(dx) <= xtol:
                exact[k].append((vy, prec, "V"))
        for c in P["caps"]:
            k, dx = nearest(c["mid"][0])
            if abs(dx) <= xtol and abs(c["u"][0]) > 1e-6:
                m = c["u"][1] / c["u"][0]
                exact[k].append((c["mid"][1] - dx * m, prec + abs(dx * m), "cap"))
    anchor_cands = [[] for _ in range(n)]
    for P in polys:
        for (mx, my, d) in P["anchors"]:
            k, dx = nearest(mx)
            if abs(dx) <= anchor_tol:
                anchor_cands[k].append(my)
    for k in range(n):
        vs = [e for e in exact[k] if e[2] == "V"]
        if vs:
            ys = np.array([e[0] for e in vs])
            y[k] = float(ys.mean())
            se[k] = prec if np.ptp(ys) < 10 * prec else float(np.ptp(ys) / 2)
            method[k] = "vertex"
            if any(abs(nearest(vx)[1]) > 0.01 for P in polys for (vx, vy) in P["V"] if nearest(vx)[0] == k):
                flags[k].append("offgrid")
    # add exact points to the segment point lists (vertex reads serve both adjacent segments)
    for k in range(n):
        if method[k] == "vertex":
            if k > 0:
                seg_pts[k - 1].append((xg[k], y[k], 1.0))
            if k < n - 1:
                seg_pts[k].append((xg[k], y[k], 1.0))

    # ---- per-segment line fits (consensus among pieces: drop pieces off the line through the longest ones)
    seg_fit = [None] * max(n - 1, 0)
    for k in range(max(n - 1, 0)):
        pcs = sorted(seg_pieces[k], key=lambda pc: -pc["L"])
        pts_x, pts_y, wts = [], [], []
        if pcs:
            keep = [pcs[0]]
            ref = _line_fit(np.array([pcs[0]["p0"], pcs[0]["p1"]]), np.ones(2))
            for pc in pcs[1:]:
                if ref is None:
                    keep.append(pc)
                    continue
                c, u, _, _ = ref
                nrm = np.array([-u[1], u[0]])
                dev = max(abs(float((pc["p0"] - c) @ nrm)), abs(float((pc["p1"] - c) @ nrm)))
                if dev < max(0.05, 10 * prec) + 2 * prec * (np.hypot(*(pc["p0"] - c)) + np.hypot(*(pc["p1"] - c))) / max(pcs[0]["L"], 0.1):
                    keep.append(pc)
                elif verbose:
                    print(f"  segment {k}: dropped a {pc['L']:.2f}-pt piece {dev:.3f} pt off the main line")
            for pc in keep:
                for p in (pc["p0"], pc["p1"]):
                    pts_x.append(p[0]); pts_y.append(p[1]); wts.append(1.0)
        for (px, py, w) in seg_pts[k]:
            pts_x.append(px); pts_y.append(py); wts.append(w)
        if len(pts_x) >= 2:
            P = np.column_stack([pts_x, pts_y])
            P, inv = np.unique(np.round(P, 5), axis=0, return_inverse=True)
            if len(P) >= 2:
                seg_fit[k] = _line_fit(P, np.ones(len(P)))

    # ---- per-vertex combination of the adjacent segment estimates
    est_of = [[] for _ in range(n)]  # (y, se, source)
    for k in range(n):
        if method[k] == "vertex":
            continue
        for s in (k - 1, k):
            if 0 <= s < n - 1 and seg_fit[s] is not None:
                r = _eval_line(seg_fit[s], xg[k], prec)
                if r is not None and np.isfinite(r[1]):
                    est_of[k].append((r[0], r[1], "seg"))
        # symmetric-pair / cap reads, checked against the segment estimates when there are any
        ex = [e for e in exact[k] if e[2] == "cap"]
        if anchor_cands[k]:
            ya = float(np.median(anchor_cands[k]))
            spread = float(np.ptp(anchor_cands[k]))
            ex.append((ya, max(prec, spread / 2), "anchor"))
        segs = [e for e in est_of[k] if e[2] == "seg"]
        good = []
        for (ya, sa, kind) in ex:
            if segs and min(abs(ya - e[0]) for e in segs) > 0.3 + 3 * max(sa, min(e[1] for e in segs)):
                if verbose:
                    print(f"  vertex {k}: {kind} read {ya:.3f} disagrees with the segment fits, ignored")
                continue
            good.append((ya, sa, kind))
        if good:
            ys = np.array([g[0] for g in good])
            ws = np.array([1 / max(g[1], 1e-4) ** 2 for g in good])
            y[k] = float((ys * ws).sum() / ws.sum())
            se[k] = float(max(1 / math.sqrt(ws.sum()), np.ptp(ys) / 2))
            method[k] = "vertex"
            flags[k].append("anchor")
            continue
        if est_of[k]:
            ys = np.array([e[0] for e in est_of[k]])
            ws = np.array([1 / max(e[1], 1e-4) ** 2 for e in est_of[k]])
            y[k] = float((ys * ws).sum() / ws.sum())
            se[k] = float(max(1 / math.sqrt(ws.sum()), np.ptp(ys) / 2))
            method[k] = "segment_fit"
            if verbose:
                print(f"  vertex {k} (x={xg[k]:.2f}): segment estimates " + ", ".join(f"{e[0]:.3f}+/-{e[1]:.3f}" for e in est_of[k])
                      + f" -> {y[k]:.3f} +/- {se[k]:.3f} pt")

    # ---- coverage: is the vertex inside a dash?  (a piece or exact read touches it)
    covered = np.zeros(n, bool)
    for k in range(n):
        if method[k] == "vertex":
            covered[k] = True
            continue
        for s in (k - 1, k):
            if 0 <= s < n - 1:
                for pc in seg_pieces[s]:
                    if pc["p0"][0] - xtol <= xg[k] <= pc["p1"][0] + xtol:
                        covered[k] = True
    for k in range(n):
        if not covered[k]:
            flags[k].append("gap")

    # ---- dash-pattern constraint for gap vertices
    # Consecutive dashes along the path: polygons sorted by x, both complete (two caps, not cut by the axes
    # box); the gap E -> S between A's end cap and B's start cap must not contain a dash-covered vertex
    # (dashes of a steep spike overlap in x and would otherwise pair up as false neighbours).
    gap_len = float("nan")
    gaps = []

    def whole(P):
        return len(P["caps"]) == 2 and not P["clipped"]

    if pattern:
        for A, B in zip(polys[:-1], polys[1:]):
            if not (whole(A) and whole(B)):
                continue
            Ec, Sc = A["caps"][-1]["mid"], B["caps"][0]["mid"]
            if Sc[0] < Ec[0] - 1e-6 or np.any((xg > Ec[0]) & (xg < Sc[0])):
                continue
            gaps.append(float(np.hypot(*(Sc - Ec))))
        if len(gaps) >= 3:
            gap_len = float(np.median(gaps))
            gspread = max(float(np.percentile(gaps, 90) - np.percentile(gaps, 10)) / 2, prec)
        elif gaps:
            gap_len = float(np.median(gaps))
            gspread = 0.05
    if pattern and np.isfinite(gap_len):
        for A, B in zip(polys[:-1], polys[1:]):
            if not (whole(A) and whole(B)):
                continue
            Ec, Sc = A["caps"][-1]["mid"], B["caps"][0]["mid"]
            if Sc[0] < Ec[0] - 1e-6:
                continue
            ids = [i for i in range(n) if Ec[0] < xg[i] < Sc[0]]
            if not ids or float(np.hypot(*(Sc - Ec))) > gap_len + 3 * gspread:
                continue
            if any(covered[i] or method[i] == "vertex" for i in ids):
                continue  # not a gap between consecutive dashes (or nothing to improve)
            weak = [i for i in ids if np.isnan(y[i]) or se[i] > 0.3]
            unknown = ids if len(ids) == 1 else weak
            if len(unknown) != 1 or any(method[i] is None for i in ids if i != unknown[0]):
                continue
            m_ = unknown[0]

            def total(yy):
                pts = [Ec] + [np.array([xg[i], yy if i == m_ else y[i]]) for i in ids] + [Sc]
                return sum(float(np.hypot(*(pts[j + 1] - pts[j]))) for j in range(len(pts) - 1)) - gap_len

            prev = Ec if m_ == ids[0] else np.array([xg[m_ - 1], y[m_ - 1]])
            nxt = Sc if m_ == ids[-1] else np.array([xg[m_ + 1], y[m_ + 1]])
            ychord = prev[1] + (xg[m_] - prev[0]) * (nxt[1] - prev[1]) / (nxt[0] - prev[0]) if nxt[0] != prev[0] else (prev[1] + nxt[1]) / 2
            roots = []
            for lo, hi in ((ychord - 300, ychord), (ychord, ychord + 300)):
                flo, fhi = total(lo), total(hi)
                if flo * fhi > 0:
                    continue
                for _ in range(80):
                    mid = (lo + hi) / 2
                    fm = total(mid)
                    if flo * fm <= 0:
                        hi, fhi = mid, fm
                    else:
                        lo, flo = mid, fm
                roots.append((lo + hi) / 2)
            if not roots:
                continue
            prior = (y[m_], se[m_]) if not np.isnan(y[m_]) else None
            root = None
            if len(roots) == 2:
                if prior is not None and abs(roots[0] - roots[1]) >= 2 * max(prior[1], 0.05):
                    root = min(roots, key=lambda r: abs(r - prior[0]))
            else:
                root = roots[0]
            if root is None:
                if prior is None:
                    y[m_] = float(np.mean(roots))
                    se[m_] = float(abs(roots[0] - roots[1]) / 2)
                    method[m_] = "segment_fit"
                    flags[m_] += ["pattern", "ambiguous"]
                continue
            # error of the root from the pattern spread and the neighbours' uncertainties
            df = (total(root + 0.01) - total(root - 0.01)) / 0.02
            if abs(df) < 1e-6:
                continue
            extra = sum((se[i] if np.isfinite(se[i]) else 0.0) ** 2 for i in ids if i != m_)
            err = math.sqrt((gspread / df) ** 2 + extra / max(df * df, 1e-6) + prec ** 2)
            if prior is not None:
                ws = np.array([1 / max(prior[1], 1e-4) ** 2, 1 / max(err, 1e-4) ** 2])
                vals = np.array([prior[0], root])
                y[m_] = float((ws * vals).sum() / ws.sum())
                se[m_] = float(max(1 / math.sqrt(ws.sum()), abs(vals[0] - vals[1]) / 2))
            else:
                y[m_], se[m_] = root, err
            method[m_] = method[m_] or "segment_fit"
            flags[m_].append("pattern")
            if verbose:
                print(f"  vertex {m_} (x={xg[m_]:.2f}): pattern roots {[round(r, 3) for r in roots]} (gap {gap_len:.3f} pt, chord {float(np.hypot(*(Sc - Ec))):.3f}), "
                      f"prior {None if prior is None else f'{prior[0]:.3f}+/-{prior[1]:.3f}'} -> {y[m_]:.3f} +/- {se[m_]:.3f} pt")

    # ---- values outside the axes box are extrapolations of the clipped line
    if clip_y is not None:
        ylo, yhi = min(clip_y), max(clip_y)
        for k in range(n):
            if not np.isnan(y[k]) and (y[k] < ylo - 0.05 or y[k] > yhi + 0.05):
                flags[k].append("clipped")

    # ---- interpolation across vertices that no dash constrains
    for k in range(1, n - 1):
        if interp and method[k] is None and method[k - 1] is not None and method[k + 1] is not None \
                and "clipped" not in flags[k - 1] and "clipped" not in flags[k + 1]:
            y[k] = (y[k - 1] + y[k + 1]) / 2
            c = float(np.hypot(xg[k + 1] - xg[k - 1], y[k + 1] - y[k - 1]))
            bound = 0.5 * math.sqrt(max(gap_len ** 2 - c ** 2, 0.0)) if np.isfinite(gap_len) else abs(y[k + 1] - y[k - 1]) / 2
            se[k] = float(max(bound, math.hypot(se[k - 1], se[k + 1]) / 2))
            method[k] = "gap_interp"

    # ---- unrecoverable vertices: did the line leave the box there?
    E = np.array(ends) if ends else np.zeros((0, 3))
    for k in range(n):
        if method[k] is not None:
            continue
        if clip_y is not None and len(E):
            left = E[E[:, 0] < xg[k]]
            right = E[E[:, 0] > xg[k]]
            near_clip = lambda p: any(abs(p[1] - c) < 0.1 for c in clip_y) and p[2] > 0.3
            far = np.isfinite(gap_len) and (not len(left) or xg[k] - left[:, 0].max() > gap_len) and (not len(right) or right[:, 0].min() - xg[k] > gap_len)
            if (len(left) and near_clip(left[np.argmax(left[:, 0])])) or (len(right) and near_clip(right[np.argmin(right[:, 0])])) or far:
                flags[k].append("clipped")
            nb_clipped = any("clipped" in flags[j] and method[j] is not None for j in (k - 1, k + 1) if 0 <= j < n)
            if nb_clipped and "clipped" not in flags[k]:
                flags[k].append("clipped")

    # ---- n_pieces diagnostic
    n_pieces = np.zeros(n, int)
    for k in range(n):
        for s in (k - 1, k):
            if 0 <= s < n - 1:
                n_pieces[k] += len(seg_pieces[s])

    if verbose:
        from collections import Counter
        print(f"  dash polygons {len(polys)}, caps {sum(len(P['caps']) for P in polys)}, vertex points {sum(len(P['V']) for P in polys)}, "
              f"pieces {sum(len(P['pieces']) for P in polys)}, pattern gap {gap_len:.3f} pt from {len(gaps)} vertex-free gaps; "
              f"methods {dict(Counter(method))}")

    # ---- to data units, back to the caller's order
    out = [None] * n
    for i, k in enumerate(order):
        yk = y[i]
        if np.isnan(yk):
            val, sev = None, None
        else:
            val = float(yax(yk))
            sev = float(abs(yax(yk + se[i]) - val)) if np.isfinite(se[i]) else None
        out[k] = dict(x=xg_data[k], value=val, se=sev, method=method[i], flags=list(flags[i]),
                      x_pt=float(xg[i]), y_pt=(None if np.isnan(yk) else float(yk)),
                      se_pt=(None if not np.isfinite(se[i]) else float(se[i])), n_pieces=int(n_pieces[i]))
    return out


# ---------------------------------------------------------------- 4. bands

def band_extent(polygon_points, xax, yax, x_grid, tol=0.01):
    """Vertical extent of a filled band polygon at each grid x: slices the polygon with the vertical line
    x = xax.inv(g) (crossings of all edges + endpoints within `tol` pt), so bands clipped at the axis limits
    (where the clipped edge has no vertex at integer x) are read correctly.  polygon_points: [(x,y),...] in
    PDF points (one closed subpath), or a list of such polygons, or a draw dict from pdfplot.drawings (all
    its subpaths are used: a band cut into fragments by the axes box is one fill with several subpaths).
    Returns (lo, hi): lists in data units (lo <= hi), None where the band is absent at that x.
    (pdfplot.band_envelope is wrong for clipped bands; use this.)"""
    if isinstance(polygon_points, dict) and "subpaths" in polygon_points:
        polys = polygon_points["subpaths"]
    else:
        arr = np.asarray(polygon_points, dtype=object)
        polys = [polygon_points] if (arr.ndim == 2 or (arr.ndim == 1 and np.isscalar(arr[0]))) else list(polygon_points)
    polys = [_pts(p) for p in polys if len(p) >= 3]
    lo, hi = [], []
    for g in x_grid:
        x = xax.inv(g)
        ys = []
        for P in polys:
            nP = len(P)
            for i in range(nP):
                (xa, ya), (xb, yb) = P[i], P[(i + 1) % nP]
                if abs(xa - x) <= tol:
                    ys.append(ya)
                if abs(xb - x) <= tol:
                    ys.append(yb)
                if (xa - x) * (xb - x) < 0 and abs(xb - xa) > 1e-12:
                    ys.append(ya + (yb - ya) * (x - xa) / (xb - xa))
        if not ys:
            lo.append(None); hi.append(None)
            continue
        a, b = yax(min(ys)), yax(max(ys))
        lo.append(float(min(a, b))); hi.append(float(max(a, b)))
    return lo, hi


def check_band_symmetry(line_values, lo, hi):
    """Bands are drawn symmetric about their line: compare (lo+hi)/2 with the line value where all three
    exist and neither edge is None.  Returns (max |mid - line|, mean |mid - line|, n) in data units
    ((None, None, 0) if nothing to compare).  Use it to validate a recovered dashed line and to decide
    which of two same-colour bands belongs to it."""
    d = [abs((l + h) / 2 - v) for v, l, h in zip(line_values, lo, hi)
         if v is not None and l is not None and h is not None and not (isinstance(v, float) and math.isnan(v))]
    if not d:
        return None, None, 0
    return float(max(d)), float(sum(d) / len(d)), len(d)


# ---------------------------------------------------------------- 5. QA overlay

def overlay_png(page, clip, polylines, out_png, dpi=300, width=0.3):
    """Render `clip` of `page` at `dpi` with polylines drawn on top (QA).  polylines: list of
    (points [(x_pt, y_pt), ...], (r, g, b)).  Draws on a fresh copy of the page so `page` is untouched."""
    import fitz
    doc = fitz.open(page.parent.name)
    pg = doc[page.number]
    shape = pg.new_shape()
    for pts, color in polylines:
        pts = [p for p in pts if p[1] is not None]
        for a, b in zip(pts[:-1], pts[1:]):
            shape.draw_line(fitz.Point(*a), fitz.Point(*b))
        for p in pts:
            shape.draw_circle(fitz.Point(*p), 0.4)
        shape.finish(color=color, width=width)
    shape.commit()
    pix = pg.get_pixmap(clip=clip, dpi=dpi)
    pix.save(out_png)
    doc.close()
    return pix.width, pix.height


# ---------------------------------------------------------------- self-test

def _selftest(overlay_dir=None):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pdfplot as pp
    ROOT = "/home/admin/ephemeral/oct_17_papers/hesse2026"
    PDF = os.path.join(ROOT, "source", "2026.10.15.759299v1.full.pdf")
    FIG = os.path.join(ROOT, "figures")

    def fnum(s):
        s = (s or "").strip()
        return float(s) if s else None

    def load_csv(path):
        hdr, rows = pp.read_csv(path)
        return {h: [r[i] for r in rows] for i, h in enumerate(hdr)}

    def compare(label, mine, csv_vals, csv_se=None, csv_tag=None):
        """Print agreement statistics of one recovered series against the published CSV column."""
        diffs, bad = [], []
        n_mine_empty = sum(1 for r in mine if r["value"] is None)
        n_csv_empty = sum(1 for v in csv_vals if v is None)
        both = 0
        by_method = {}
        for i, (r, v) in enumerate(zip(mine, csv_vals)):
            if r["value"] is None or v is None:
                continue
            both += 1
            d = abs(r["value"] - v)
            diffs.append(d)
            by_method.setdefault(r["method"], []).append(d)
            tol = 0.3 if r["method"] == "vertex" else max(0.3, (r["se"] or 0) + ((csv_se[i] or 0) if csv_se else 0) + 0.01)
            if d > tol:
                bad.append((r["x"], r["value"], v, r["method"], r["se"], "+".join(r["flags"]), csv_tag[i] if csv_tag else ""))
        print(f"  {label}: n both {both}, max |diff| {max(diffs):.3f} %, mean {np.mean(diffs):.3f} %; empty: mine {n_mine_empty}, csv {n_csv_empty}"
              + f"; by method: " + ", ".join(f"{m}: n {len(v)} max {max(v):.3f}" for m, v in sorted(by_method.items(), key=lambda t: str(t[0]))))
        from collections import Counter
        print(f"      methods {dict(Counter(r['method'] for r in mine))}, flags {dict(Counter(f for r in mine for f in r['flags']))}, "
              f"max se (vertex) {max([r['se'] for r in mine if r['method'] == 'vertex'] or [0]):.3f} %, max se (other) {max([r['se'] for r in mine if r['method'] not in ('vertex', None)] or [0]):.3f} %")
        for b in bad:
            print(f"      DISCREPANCY x={b[0]}: mine {b[1]:.2f} (se {b[4]:.2f}, {b[3]}, {b[5]}) vs csv {b[2]:.2f} {b[6]}")
        return bad

    results = {}
    # ------------------------------------------------ Figure 2 panel i (page 36)
    print("Figure 2i (page 36): explained variance, 50 features, dashed = suppressed state 1 (orange) / state 2 (purple)")
    page = pp.open_page(PDF, 36)
    clip = pp.R(260, 183, 392, 330)
    draws = pp.drawings(page, clip, how="inside")
    xax = pp.axis_from_ticks(draws, "x", [10, 20, 30, 40, 50], region=pp.R(285, 307, 392, 313))
    yax = pp.axis_from_ticks(draws, "y", [-100, -50, 0, 50, 100], region=pp.R(280, 190, 290, 312))
    csv = load_csv(os.path.join(FIG, "fig2i.csv"))
    grid = list(range(1, 51))
    for color, col in (("#fcae34", "binocular_suppressed_state1_pct"), ("#543379", "binocular_suppressed_state2_pct")):
        polys = dash_polygons(draws, color, 1.0)
        rows = dashed_series(polys, xax, yax, grid, 1.0, y_limits=(-100, 100))
        results[("fig2i", col)] = (page, clip, rows)
        compare(col, rows, [fnum(v) for v in csv[col]])
    # ------------------------------------------------ Figure 3 panel g (page 37), with bands
    print("Figure 3g (page 37): decoding accuracy vs number of faces (60), dashed with bands")
    page = pp.open_page(PDF, 37)
    clip = pp.R(398, 120, 512, 245)
    draws = pp.drawings(page, clip, how="inside")
    xax = pp.axis_from_ticks(draws, "x", [0, 20, 40, 60], region=pp.R(412, 239.5, 510, 243))
    yax = pp.axis_from_ticks(draws, "y", [0, 20, 40, 60, 80, 100], region=pp.R(410, 126, 413.75, 241))
    csv = load_csv(os.path.join(FIG, "fig3g.csv"))
    grid = list(range(1, 61))
    bands = [d for d in draws if d["kind"] == "fill" and (d["raw"].get("fill_opacity") or 1) < 0.5 and len(d["points"]) >= 50]
    solids = {_hex(d["color"]): d for d in draws if d["kind"] == "stroke" and len(d["points"]) >= 60 and _hex(d["color"]) in ("#1c0f29", "#fcae34", "#543379")}
    for color, name in (("#fcae34", "suppressed_state1"), ("#543379", "suppressed_state2")):
        polys = dash_polygons(draws, color, 1.0)
        rows = dashed_series(polys, xax, yax, grid, 1.0, y_limits=(0, 100))
        results[("fig3g", name)] = (page, clip, rows)
        bad = compare(name, rows, [fnum(v) for v in csv[name + "_pct"]], csv_tag=csv[name + "_recovery"])
        # bands of this colour: one belongs to the solid line, one to the dashed line; symmetry decides
        line = [r["value"] for r in rows]
        sol = [yax(y) for x, y in solids[color]["points"][:60]]
        for b in [b for b in bands if _hex(b["fill"]) == color]:
            lo, hi = band_extent(b, xax, yax, grid)   # whole draw: a band cut by the axes box has several subpaths
            lo_c = [min(max(v, 0.0), 100.0) if v is not None else None for v in lo]
            hi_c = [min(max(v, 0.0), 100.0) if v is not None else None for v in hi]
            uncl = [(v, l, h) if (l is not None and 0.05 < l and h < 99.95) else (v, None, None) for v, l, h in zip(line, lo_c, hi_c)]
            uncl_s = [(v, l, h) if (l is not None and 0.05 < l and h < 99.95) else (v, None, None) for v, l, h in zip(sol, lo_c, hi_c)]
            sym_d = check_band_symmetry(*zip(*uncl))
            sym_s = check_band_symmetry(*zip(*uncl_s))
            print(f"      band ({len(b['points'])} pts, {len(b['subpaths'])} subpaths): symmetry about dashed line max {sym_d[0]:.3f} mean {sym_d[1]:.3f} (n {sym_d[2]}); "
                  f"about solid line max {sym_s[0]:.3f} mean {sym_s[1]:.3f} (n {sym_s[2]})")
            if sym_d[1] < sym_s[1]:
                dlo = [abs(a - fnum(c)) for a, c in zip(lo_c, csv[name + "_lo_pct"]) if a is not None and fnum(c) is not None]
                dhi = [abs(a - fnum(c)) for a, c in zip(hi_c, csv[name + "_hi_pct"]) if a is not None and fnum(c) is not None]
                print(f"      -> dashed-line band; vs csv lo/hi (clamped to 0..100): max |diff| lo {max(dlo):.3f} hi {max(dhi):.3f} over {len(dlo)}/{len(dhi)}; "
                      f"absent at {sum(1 for v in lo if v is None)} x (csv empty lo: {sum(1 for c in csv[name + '_lo_pct'] if fnum(c) is None)})")
                # where the dash recovery is weak (gap, ambiguous, empty) the unclipped band midpoint is the better value
                weak = [(r, (l + h) / 2) for r, l, h in zip(rows, lo_c, hi_c)
                        if (r["method"] in (None, "gap_interp") or "ambiguous" in r["flags"]) and l is not None and 0.05 < l and h < 99.95]
                if weak:
                    cmp_ = [(r["x"], round(m, 2), fnum(csv[name + "_pct"][r["x"] - 1])) for r, m in weak]
                    print(f"      -> band midpoint replaces {len(weak)} weak dash values (x, midpoint, csv): {cmp_}")
    # ------------------------------------------------ Extended Data Figure 5 panel e (page 45)
    print("Extended Data Fig 5e (page 45): explained variance, 50 features")
    page = pp.open_page(PDF, 45)
    clip = pp.R(256, 320, 385, 468)
    draws = pp.drawings(page, clip, how="inside")
    xax = pp.axis_from_ticks(draws, "x", [10, 20, 30, 40, 50], region=pp.R(287, 446.5, 385, 451))
    yax = pp.axis_from_ticks(draws, "y", [-100, -50, 0, 50, 100], region=pp.R(284, 330, 288.2, 450))
    csv = load_csv(os.path.join(FIG, "edfig5e.csv"))
    grid = list(range(1, 51))
    for color, col in (("#fcae34", "binocular_suppressed_state1"), ("#543379", "binocular_suppressed_state2")):
        polys = dash_polygons(draws, color, 1.0)
        rows = dashed_series(polys, xax, yax, grid, 1.0, y_limits=(-100, 100))
        results[("edfig5e", col)] = (page, clip, rows)
        compare(col, rows, [fnum(v) for v in csv[col + "_pct"]], csv_se=[fnum(v) for v in csv[col + "_se_pct"]])
    if overlay_dir:
        os.makedirs(overlay_dir, exist_ok=True)
        done = set()
        for (fig, name), (page, clip, rows) in results.items():
            key = fig
            pls = [([(r["x_pt"], r["y_pt"]) for r in rr[2] if r["value"] is not None], (1, 0, 0) if "state1" in nm else (0, 0, 1))
                   for (fg, nm), rr in results.items() if fg == fig]
            if key not in done:
                out = os.path.join(overlay_dir, f"{fig}_overlay.png")
                overlay_png(page, clip, pls, out, dpi=300)
                print("  overlay written:", out)
                done.add(key)
    return results


if __name__ == "__main__":
    od = None
    if "--overlay" in sys.argv:
        od = sys.argv[sys.argv.index("--overlay") + 1]
    _selftest(od)
