"""Small helpers for reading vector plots out of zhao2025's PDF with PyMuPDF (written for this paper).

Coordinates are PDF points, origin top left, y down (PyMuPDF's frame).

    import vecplot as vp
    page = vp.page(PDF, 3)
    ds = vp.drawings_in(page, (x0, y0, x1, y1))     # paths whose bbox lies inside the box
    pts = vp.vertices(d)                             # ordered vertex list of one path
    ax = vp.Axis([(142.1, 0), (194.27, 10), (246.5, 20)])   # page coordinate -> data, least squares
"""
import csv

import numpy as np
import pymupdf


def page(pdf, pno):
    return pymupdf.open(pdf)[pno - 1]


def hexcol(c):
    return None if c is None else "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c[:3])


def drawings_in(pg, box, tol=0.5):
    """All drawings whose bounding box lies inside box (x0, y0, x1, y1).

    Bounds are compared directly (Rect.contains() is False for zero-width/height rects)."""
    x0, y0, x1, y1 = box
    out = []
    for i, d in enumerate(pg.get_drawings()):
        r = d["rect"]
        if r.x0 >= x0 - tol and r.x1 <= x1 + tol and r.y0 >= y0 - tol and r.y1 <= y1 + tol:
            d = dict(d)
            d["index"] = i
            d["stroke"] = hexcol(d.get("color"))
            d["fillc"] = hexcol(d.get("fill"))
            out.append(d)
    return out


def vertices(d):
    """Ordered vertices of a path: line ends, Bezier end points, rect / quad corners.

    Consecutive duplicates are merged. Bezier control points are not data and are skipped."""
    pts = []

    def add(p):
        p = (float(p.x), float(p.y))
        if not pts or abs(pts[-1][0] - p[0]) > 1e-6 or abs(pts[-1][1] - p[1]) > 1e-6:
            pts.append(p)

    for it in d["items"]:
        k = it[0]
        if k == "l":
            add(it[1]); add(it[2])
        elif k == "c":
            add(it[1]); add(it[4])
        elif k == "re":
            r = it[1]
            for p in (r.tl, r.tr, r.br, r.bl):
                add(p)
        elif k == "qu":
            q = it[1]
            for p in (q.ul, q.ur, q.lr, q.ll):
                add(p)
    return pts


def bbox_centre(d):
    r = d["rect"]
    return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)


class Axis:
    """Linear (or log10) map page coordinate -> data value, least-squares fit through (coord, value) ticks."""

    def __init__(self, ticks, log=False):
        c = np.array([t[0] for t in ticks], float)
        v = np.array([t[1] for t in ticks], float)
        self.log = log
        if log:
            v = np.log10(v)
        self.a, self.b = np.polyfit(c, v, 1)
        self.resid = (self.a * c + self.b) - v
        self.ticks = ticks

    def __call__(self, c):
        v = self.a * np.asarray(c, float) + self.b
        return 10 ** v if self.log else v

    def per_point(self):
        """Data units per PDF point."""
        return abs(self.a)

    def describe(self, name):
        return (f"{name}: linear fit through {len(self.ticks)} ticks " +
                ", ".join(f"{v:g}@{c:.3f}pt" for c, v in self.ticks) +
                f"; max residual {np.max(np.abs(self.resid)):.2g} data units")


def write_csv(path, comments, header, rows):
    with open(path, "w", newline="") as f:
        for c in comments:
            for line in c.split("\n"):
                f.write("# " + line + "\n")
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def subpaths(d, tol=1e-3):
    """Split a path's 'l' items into connected vertex chains (a new chain starts where a segment does not
    continue from the previous end point)."""
    subs, cur = [], []
    for it in d["items"]:
        if it[0] != "l":
            continue
        a, b = it[1], it[2]
        if cur and (abs(cur[-1][0] - a.x) > tol or abs(cur[-1][1] - a.y) > tol):
            subs.append(cur)
            cur = []
        if not cur:
            cur.append((a.x, a.y))
        cur.append((b.x, b.y))
    if cur:
        subs.append(cur)
    return subs


def _proj(p, poly):
    """Nearest point on polyline poly to p, and its distance."""
    best, bd = None, 1e9
    for (x0, y0), (x1, y1) in zip(poly[:-1], poly[1:]):
        dx, dy = x1 - x0, y1 - y0
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - x0) * dx + (p[1] - y0) * dy) / L2))
        q = (x0 + t * dx, y0 + t * dy)
        dd = ((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2) ** 0.5
        if dd < bd:
            best, bd = q, dd
    return best, bd


def outline_centreline(outline, width, tol=0.35):
    """Centre line of a dash drawn as the filled outline of a stroked polyline (one side out, the other back).

    The outline is split at its two most distant vertices (the dash ends) into side A and side B; every vertex of
    either side is projected onto the other side and the midpoint is kept when the two sides are about one line
    width apart (|d - width| < tol*width), which drops cap and join artefacts. Returns points sorted along the dash.
    """
    P = np.array(outline[:-1] if outline[0] == outline[-1] else outline, float)
    n = len(P)
    if n < 4:
        return []
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    i, j = np.unravel_index(np.argmax(D), D.shape)
    i, j = min(i, j), max(i, j)
    A = [tuple(p) for p in P[i:j + 1]]
    B = [tuple(p) for p in np.r_[P[j:], P[:i + 1]]]
    out = []
    for S, T in ((A, B), (B, A)):
        for p in S:
            q, dd = _proj(p, T)
            if abs(dd - width) < tol * width:
                out.append(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2))
    if not out:
        return []
    out = np.array(out)
    e = P[i]
    order = np.argsort(np.linalg.norm(out - e, axis=1))
    return [tuple(map(float, p)) for p in out[order]]


def segments(ds, thin=1.4):
    """Straight horizontal/vertical pieces among drawings: single-line strokes and thin filled rectangles.

    Returns dicts with orient 'h' or 'v', the centre line (x0, y0, x1, y1; x0<=x1, y0<=y1), colour and path index."""
    out = []
    for d in ds:
        its = d["items"]
        col = d["stroke"] if d["type"] == "s" else d["fillc"]
        if d["type"] == "s" and len(its) == 1 and its[0][0] == "l":
            (a, b) = its[0][1], its[0][2]
            x0, x1 = sorted((a.x, b.x)); y0, y1 = sorted((a.y, b.y))
        elif d["type"] in ("f", "fs") and len(its) == 1 and its[0][0] == "re":
            r = its[0][1]
            if r.width <= thin and r.height > r.width:
                x0 = x1 = (r.x0 + r.x1) / 2; y0, y1 = r.y0, r.y1
            elif r.height <= thin and r.width > r.height:
                y0 = y1 = (r.y0 + r.y1) / 2; x0, x1 = r.x0, r.x1
            else:
                continue
        else:
            continue
        if abs(x1 - x0) < 1e-3 and y1 - y0 > 1e-3:
            o = "v"
        elif abs(y1 - y0) < 1e-3 and x1 - x0 > 1e-3:
            o = "h"
        else:
            continue
        out.append(dict(orient=o, x0=x0, y0=y0, x1=x1, y1=y1, color=col, index=d["index"]))
    return out


def error_bars(cx, cy, segs, cap_max=8.0, tol=0.5):
    """Error-bar ends around a marker centred near (cx, cy), in page coordinates.

    Vertical bar: pieces are vertical segments at x ~ cx; caps are short horizontal segments centred at x ~ cx.
    Horizontal bar: pieces are horizontal segments at y ~ cy; caps are short vertical segments centred at y ~ cy.
    Returns dict with exact centre coordinates from the bar lines where present (x_bar, y_bar) and the cap
    positions (y_caps sorted, x_caps sorted); empty lists if there is no bar."""
    vb = [s for s in segs if s["orient"] == "v" and abs(s["x0"] - cx) < tol and s["y1"] - s["y0"] > 0
          and (abs(s["y0"] - cy) < 3 or abs(s["y1"] - cy) < 3 or s["y0"] < cy < s["y1"])]
    hb = [s for s in segs if s["orient"] == "h" and abs(s["y0"] - cy) < tol
          and (abs(s["x0"] - cx) < 3 or abs(s["x1"] - cx) < 3 or s["x0"] < cx < s["x1"]) and s["x1"] - s["x0"] > cap_max]
    ycaps = [s for s in segs if s["orient"] == "h" and s["x1"] - s["x0"] <= cap_max and abs((s["x0"] + s["x1"]) / 2 - cx) < tol]
    xcaps = [s for s in segs if s["orient"] == "v" and s["y1"] - s["y0"] <= cap_max and abs((s["y0"] + s["y1"]) / 2 - cy) < tol
             and not (abs(s["x0"] - cx) < tol)]
    # caps only count where bar pieces reach them (drops pieces of neighbouring bars)
    # a bar shorter than the caps' thickness has no separate piece: accept a pair of caps straddling the centre
    # within 3 pt instead
    def _pair(caps, key, c):
        lo = [s for s in caps if c - 3 < s[key] < c]
        hi = [s for s in caps if c < s[key] < c + 3]
        return (lo[-1:] + hi[:1]) if lo and hi else []
    if vb:
        lo, hi = min(s["y0"] for s in vb) - 1, max(s["y1"] for s in vb) + 1
        ycaps = [s for s in ycaps if lo <= s["y0"] <= hi]
    else:
        ycaps = _pair(sorted(ycaps, key=lambda s: s["y0"]), "y0", cy)
    if hb:
        lo, hi = min(s["x0"] for s in hb) - 1, max(s["x1"] for s in hb) + 1
        xcaps = [s for s in xcaps if lo <= s["x0"] <= hi]
    else:
        xcaps = _pair(sorted(xcaps, key=lambda s: s["x0"]), "x0", cx)
    res = dict(x_bar=None, y_bar=None, y_caps=sorted({round(s["y0"], 3) for s in ycaps}),
               x_caps=sorted({round(s["x0"], 3) for s in xcaps}), v_pieces=vb, h_pieces=hb)
    if vb:
        res["x_bar"] = float(np.median([s["x0"] for s in vb]))
        ends = sorted(e for s in vb for e in (s["y0"], s["y1"]))
        shared = [a for a, b in zip(ends[:-1], ends[1:]) if abs(a - b) < 0.02]
        if len(vb) == 2 and len(shared) == 1:
            res["y_junction"] = shared[0]       # the two half-bars meet at the data point
    if hb:
        res["y_bar"] = float(np.median([s["y0"] for s in hb]))
        ends = sorted(e for s in hb for e in (s["x0"], s["x1"]))
        shared = [a for a, b in zip(ends[:-1], ends[1:]) if abs(a - b) < 0.02]
        if len(hb) == 2 and len(shared) == 1:
            res["x_junction"] = shared[0]
    return res


def fit_line_vertices(d):
    """Least-squares straight line y = m x + c (page coordinates) through all vertices of a path (dashed lines drawn
    as filled dash polygons), with the x extent of the vertices."""
    v = np.array(vertices(d))
    m, c = np.polyfit(v[:, 0], v[:, 1], 1)
    return m, c, float(v[:, 0].min()), float(v[:, 0].max()), float(np.max(np.abs(v[:, 1] - (m * v[:, 0] + c))))
