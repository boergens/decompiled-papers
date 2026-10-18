"""Scratch helpers on top of tools/pdfplot.py for edfig7 / edfig10 extraction."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import fitz  # noqa: E402
import pdfplot as pp  # noqa: E402

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "2026.10.15.759299v1.full.pdf")
PROJ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def drawings_ext(page, clip=None):
    """Same output format as pdfplot.drawings, but built from page.get_drawings(extended=True),
    which (unlike the default) keeps the stroke paths that live inside the form XObjects."""
    out = []
    for d in page.get_drawings(extended=True):
        if d.get("type") not in ("s", "f", "fs"):
            continue
        r = d["rect"]
        if clip is not None:
            # single horizontal/vertical segments have a zero-width/height bbox, which fitz treats as empty
            # (intersects() is False): inflate degenerate rects before the clip test (same fix as pdfplot)
            rt = fitz.Rect(r.x0 - 0.01, r.y0 - 0.01, r.x1 + 0.01, r.y1 + 0.01) if (r.width <= 0 or r.height <= 0) else r
            if not clip.intersects(rt):
                continue
        subpaths, cur, rects, has_curves = [], [], [], False
        last = None
        for it in d["items"]:
            op = it[0]
            if op == "l":
                p1, p2 = it[1], it[2]
                if last is None or (abs(p1.x - last.x) > 1e-6 or abs(p1.y - last.y) > 1e-6):
                    if cur:
                        subpaths.append(cur)
                    cur = [(p1.x, p1.y)]
                cur.append((p2.x, p2.y))
                last = p2
            elif op == "c":
                has_curves = True
                p0 = it[1]
                if last is None or (abs(p0.x - last.x) > 1e-6 or abs(p0.y - last.y) > 1e-6):
                    if cur:
                        subpaths.append(cur)
                    cur = [(p0.x, p0.y)]
                cur.extend(pp._bezier(it[1], it[2], it[3], it[4]))
                last = it[4]
            elif op == "re":
                rr = it[1]
                rects.append((rr.x0, rr.y0, rr.x1, rr.y1))
                if cur:
                    subpaths.append(cur)
                    cur = []
                subpaths.append([(rr.x0, rr.y0), (rr.x1, rr.y0), (rr.x1, rr.y1), (rr.x0, rr.y1), (rr.x0, rr.y0)])
                last = None
            elif op == "qu":
                q = it[1]
                if cur:
                    subpaths.append(cur)
                    cur = []
                subpaths.append([(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y), (q.ul.x, q.ul.y)])
                last = None
        if cur:
            subpaths.append(cur)
        kind = {"s": "stroke", "f": "fill", "fs": "fillstroke"}[d["type"]]
        out.append(dict(
            kind=kind, color=d.get("color"), fill=d.get("fill"), width=d.get("width"),
            rect=(r.x0, r.y0, r.x1, r.y1), dashes=d.get("dashes"), closePath=d.get("closePath"),
            n_items=len(d["items"]), subpaths=subpaths, points=[p for sp in subpaths for p in sp],
            rects=rects, has_curves=has_curves, raw=d,
        ))
    return out


# ------------------------------------------------------------------ dashed lines drawn as filled dash quads

def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _norm(v):
    return math.hypot(v[0], v[1])


def cap_evidence(poly, w=1.0, tol=0.06, perp_tol=0.08):
    """For one filled dash outline (closed polygon), find its butt caps: edges of length ~w whose two
    neighbouring edges are perpendicular to them. Returns a list of (mx, my, ex, ey): the cap midpoint
    (a point on the stroke centreline) and the unit direction of the adjacent long edge, pointing from
    the cap INTO the dash body (so ex > 0 means the dash continues to the right of this cap)."""
    pts = list(poly)
    if _norm(_sub(pts[0], pts[-1])) < 1e-6:
        pts = pts[:-1]
    n = len(pts)
    out = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        L = _norm(_sub(b, a))
        if abs(L - w) > tol:
            continue
        prev, nxt = pts[i - 1], pts[(i + 2) % n]
        e = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        vp, vn = _sub(prev, a), _sub(nxt, b)  # from cap corners into the body
        Lp, Ln = _norm(vp), _norm(vn)
        if Lp < 0.2 or Ln < 0.2:
            continue
        up, un = (vp[0] / Lp, vp[1] / Lp), (vn[0] / Ln, vn[1] / Ln)
        if abs(up[0] * e[0] + up[1] * e[1]) > perp_tol or abs(un[0] * e[0] + un[1] * e[1]) > perp_tol:
            continue
        if up[0] * un[0] + up[1] * un[1] < 0.99:  # the two neighbours must be parallel (same segment)
            continue
        u = up if Lp >= Ln else un
        out.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, u[0], u[1]))
    return out


def dashed_polyline(dash_draw, xgrid, w=1.0):
    """Recover the y value (PDF coords) at each vertex x in `xgrid` (ascending PDF x of the data vertices)
    of a piecewise-linear dashed line drawn as filled dash quads (one path, many subpaths).
    Returns (ys, spread, nevid): ys[k] is the mean of all estimates for vertex k (nan if none),
    spread[k] the max-min of those estimates (a precision indicator), nevid[k] their count."""
    ev = []
    for sp in dash_draw["subpaths"]:
        ev.extend(cap_evidence(sp, w=w))
    est = [[] for _ in xgrid]
    nx = len(xgrid)
    for (mx, my, ex, ey) in ev:
        # interval containing the dash body side of this cap
        if ex >= 0:
            k = max(i for i in range(nx) if xgrid[i] <= mx + 1e-6) if mx >= xgrid[0] - 1e-6 else None
            if k is None or k >= nx - 1:
                if k == nx - 1 and abs(mx - xgrid[-1]) < 1e-3:
                    est[k].append(my)
                continue
        else:
            k = min(i for i in range(nx) if xgrid[i] >= mx - 1e-6) - 1 if mx <= xgrid[-1] + 1e-6 else None
            if k is None or k < 0:
                if k == -1 and abs(mx - xgrid[0]) < 1e-3:
                    est[0].append(my)
                continue
        if abs(ex) < 1e-9:
            continue
        slope = ey / ex
        for j in (k, k + 1):
            est[j].append(my + (xgrid[j] - mx) * slope)
    ys, spread, nev = [], [], []
    for e in est:
        if e:
            ys.append(sum(e) / len(e)); spread.append(max(e) - min(e)); nev.append(len(e))
        else:
            ys.append(float("nan")); spread.append(float("nan")); nev.append(0)
    return ys, spread, nev


def _edge_pairs(poly, w=1.0, min_len=0.6, par_tol=0.9995, dist_tol=0.08, min_overlap=0.3):
    """Straight stroke pieces of one dash outline: pairs of long polygon edges that are parallel, w apart
    and overlapping in projection (the two offset sides of one straight piece of the stroke).
    Yields (P, u, overlap): a point on the piece's centreline, its unit direction (ux > 0) and the length
    of the overlap (a weight)."""
    pts = list(poly)
    if _norm(_sub(pts[0], pts[-1])) < 1e-6:
        pts = pts[:-1]
    n = len(pts)
    E = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        L = _norm(_sub(b, a))
        if L < min_len or abs(L - w) < 0.03:  # too short, or a cap / bevel
            continue
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        if u[0] < 0:
            u = (-u[0], -u[1])
        E.append((a, b, L, u))
    for i in range(len(E)):
        a0, a1, La, ua = E[i]
        for j in range(i + 1, len(E)):
            b0, b1, Lb, ub = E[j]
            if ua[0] * ub[0] + ua[1] * ub[1] < par_tol:
                continue
            nrm = (-ua[1], ua[0])
            ma = ((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2)
            mb = ((b0[0] + b1[0]) / 2, (b0[1] + b1[1]) / 2)
            dist = (mb[0] - ma[0]) * nrm[0] + (mb[1] - ma[1]) * nrm[1]
            if abs(abs(dist) - w) > dist_tol:
                continue
            pa = [(p[0] - ma[0]) * ua[0] + (p[1] - ma[1]) * ua[1] for p in (a0, a1)]
            pb = [(p[0] - ma[0]) * ua[0] + (p[1] - ma[1]) * ua[1] for p in (b0, b1)]
            lo, hi = max(min(pa), min(pb)), min(max(pa), max(pb))
            if hi - lo < min_overlap:
                continue
            c = (lo + hi) / 2
            P = (ma[0] + ua[0] * c + nrm[0] * dist / 2, ma[1] + ua[1] * c + nrm[1] * dist / 2)
            yield P, ua, hi - lo


def dashed_polyline2(dash_draw, xgrid, w=1.0):
    """Recover the y (PDF coords) at each vertex x in `xgrid` of a piecewise-linear line drawn as filled dash
    quads. Each straight piece of a dash (pair of parallel offset edges) gives a centreline point + direction,
    assigned to the inter-vertex interval that contains the piece's centre, and extrapolated to both ends of
    that interval. Returns (ys, spread, nevid): weighted mean of the estimates (nan if none), their max-min,
    and their number."""
    nx = len(xgrid)
    est = [[] for _ in xgrid]
    for sp in dash_draw["subpaths"]:
        for P, u, wgt in _edge_pairs(sp, w=w):
            if u[0] < 1e-4:
                continue
            k = None
            for i in range(nx - 1):
                if xgrid[i] - 1e-6 <= P[0] < xgrid[i + 1] + 1e-6:
                    k = i
                    break
            if k is None:
                continue
            slope = u[1] / u[0]
            for j in (k, k + 1):
                est[j].append((P[1] + (xgrid[j] - P[0]) * slope, wgt))
    ys, spread, nev = [], [], []
    for e in est:
        if e:
            sw = sum(wg for _, wg in e)
            ys.append(sum(v * wg for v, wg in e) / sw)
            vals = [v for v, _ in e]
            spread.append(max(vals) - min(vals))
            nev.append(len(e))
        else:
            ys.append(float("nan")); spread.append(float("nan")); nev.append(0)
    return ys, spread, nev


def fill_gaps(xs, ys):
    """Linear interpolation of nan entries between their nearest non-nan neighbours (no extrapolation).
    Returns (filled, flags) with flags[i] True where a value was interpolated."""
    out, flags = list(ys), [False] * len(ys)
    idx = [i for i, v in enumerate(ys) if not math.isnan(v)]
    for i, v in enumerate(ys):
        if not math.isnan(v):
            continue
        left = max((j for j in idx if j < i), default=None)
        right = min((j for j in idx if j > i), default=None)
        if left is None or right is None:
            continue
        t = (xs[i] - xs[left]) / (xs[right] - xs[left])
        out[i] = ys[left] + t * (ys[right] - ys[left])
        flags[i] = True
    return out, flags


# ------------------------------------------------------------------ polygons

def vertical_extent(poly, x, eps=1e-6):
    """(ymin, ymax) of the intersections of the vertical line at x with the closed polygon's edges."""
    pts = list(poly)
    if _norm(_sub(pts[0], pts[-1])) > 1e-6:
        pts.append(pts[0])
    ys = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        if abs(x1 - x0) < eps:
            if abs(x - x0) < eps:
                ys.extend([y0, y1])
            continue
        if min(x0, x1) - eps <= x <= max(x0, x1) + eps:
            t = (x - x0) / (x1 - x0)
            ys.append(y0 + t * (y1 - y0))
    if not ys:
        return None
    return min(ys), max(ys)


def polyline_dict(stroke_draw, ndig=4):
    """{x: y} for a stroke polyline (one subpath)."""
    pts = stroke_draw["points"]
    return [(x, y) for x, y in pts]
