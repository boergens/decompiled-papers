"""Exact geometric recovery of a dashed polyline from its outlined dash polygons (page-space geometry).

Outline structure observed in this PDF (MATLAB -> PDF export): each dash polygon is a chain of per-segment
rectangles of width w (the +/- w/2 offsets of the centre line). Where a dash spans a polyline vertex V,
the outline contains V itself (outer join: offset -> V -> offset, two edges of length w/2) and the four
endpoint offsets. Each dash has two butt caps (edges of length w, perpendicular to the segment) whose
midpoints S, E lie on the centre line. The dash pattern (dash/gap length along the path) is constant.

Recovery, with the vertex x positions `xverts` known:
  * vertex inside a dash   -> V read from the outline (exact; method 'vertex').
  * vertex inside a gap    -> 'ellipse': path length E -> V -> S equals the pattern gap g (median of the
                              vertex-free gaps), solved on the line x = x_i;
                              'line': each adjacent segment's centre line (fitted to exact centre-line
                              points: vertices, cap midpoints, midlines of antiparallel edge pairs)
                              evaluated at x_i.  Estimates are combined by inverse variance; se = max(formal
                              error, half the spread).
  * nothing usable         -> NaN.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import numpy as np
from scipy.optimize import brentq

PREC = 0.02   # assumed precision of PDF coordinates (pt)


def _edges(sp):
    pts = np.array(sp, float)
    if np.allclose(pts[0], pts[-1]):
        pts = pts[:-1]
    n = len(pts)
    E = []
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        d = p1 - p0; L = float(np.hypot(*d))
        E.append(dict(p0=p0, p1=p1, L=L, dir=d / L if L > 1e-9 else np.zeros(2), mid=(p0 + p1) / 2))
    return pts, E


def _pt_seg_dist(q, a, b):
    d = b - a; L2 = float(d @ d)
    if L2 < 1e-12:
        return float(np.hypot(*(q - a)))
    t = np.clip(((q - a) @ d) / L2, 0, 1)
    return float(np.hypot(*(q - (a + t * d))))


def parse_polygon(sp, w, clip_y=None):
    """-> dict(pts, V=[(x,y)...] strict vertex points, caps=[dict(mid, out)], centre=[(x,y)...] exact
    centre-line points (cap midpoints + antiparallel-pair midline endpoints), clipped=bool)"""
    pts, E = _edges(sp)
    n = len(E)
    onclip = np.zeros(n, bool)
    if clip_y is not None:
        for c in clip_y:
            onclip |= np.array([abs(e["p0"][1] - c) < 0.05 and abs(e["p1"][1] - c) < 0.05 for e in E])
    clipped = bool(onclip.any())
    # strict vertex points: both adjacent edges of length w/2
    V = []
    for i in range(n):
        ep, e = E[(i - 1) % n], E[i]
        if abs(ep["L"] - w / 2) < 0.06 * w and abs(e["L"] - w / 2) < 0.06 * w:
            # a true vertex has the antipodes of both neighbours in the outline (the other rectangle corners)
            v = pts[i]; A = ep["p0"]; B = e["p1"]
            ok = True
            for q in (2 * v - A, 2 * v - B):
                if not np.any(np.hypot(pts[:, 0] - q[0], pts[:, 1] - q[1]) < 0.05 * w):
                    ok = False
            if ok:
                V.append(tuple(v))
    # caps
    caps = []
    for i, e in enumerate(E):
        if abs(e["L"] - w) > 0.04 * w or onclip[i]:
            continue
        ep, en = E[(i - 1) % n], E[(i + 1) % n]
        if ep["L"] < 1e-6 or en["L"] < 1e-6:
            continue
        if abs(ep["dir"] @ en["dir"]) < 0.97 or abs(e["dir"] @ ep["dir"]) > 0.1:
            continue
        # a real cap has no other outline point near it (hairpin connectors do: V lies on them)
        others = [p for j, p in enumerate(pts) if j not in (i, (i + 1) % n)]
        if any(_pt_seg_dist(np.array(p), e["p0"], e["p1"]) < 0.08 * w for p in others):
            continue
        # hairpin inner connectors have both endpoints at w/2 from a vertex point
        if any(np.hypot(*(e["p0"] - np.array(v))) < 0.52 * w and np.hypot(*(e["p1"] - np.array(v))) < 0.52 * w for v in V):
            continue
        caps.append(dict(mid=e["mid"], out=ep["dir"]))   # 'out' = direction pointing out of the dash
    centre = [tuple(c["mid"]) for c in caps]
    # antiparallel edge pairs at distance w -> midline endpoints
    for i in range(n):
        for j in range(i + 1, n):
            a, b = E[i], E[j]
            if a["L"] < 0.25 or b["L"] < 0.25 or onclip[i] or onclip[j]:
                continue
            if a["dir"] @ b["dir"] > -0.995:
                continue
            nrm = np.array([-a["dir"][1], a["dir"][0]])
            dist = abs((b["mid"] - a["mid"]) @ nrm)
            if abs(dist - w) > 0.05 * w:
                continue
            # overlap of projections onto a.dir
            ta = sorted([0.0, a["L"]]); tb = sorted([(b["p0"] - a["p0"]) @ a["dir"], (b["p1"] - a["p0"]) @ a["dir"]])
            lo, hi = max(ta[0], tb[0]), min(ta[1], tb[1])
            if hi - lo < 0.2:
                continue
            base = a["p0"] + nrm * ((b["mid"] - a["p0"]) @ nrm) / 2
            centre.append(tuple(base + a["dir"] * lo)); centre.append(tuple(base + a["dir"] * hi))
    return dict(pts=pts, V=V, caps=sorted(caps, key=lambda c: c["mid"][0]), centre=centre, clipped=clipped)


def recover(subpaths, xverts, w, clip_y=None, xtol=0.03, verbose=False, gap_override=None):
    xv = np.asarray(xverts, float); n = len(xv)
    y = np.full(n, np.nan); se = np.full(n, np.nan); method = [""] * n
    polys = [parse_polygon(sp, w, clip_y) for sp in subpaths]
    polys.sort(key=lambda P: P["pts"][:, 0].min())
    # 1) vertices read directly
    allV = [v for P in polys for v in P["V"]]
    allpts = np.vstack([P["pts"] for P in polys])
    for i in range(n):
        cand = [v for v in allV if abs(v[0] - xv[i]) < xtol]
        if cand:
            ys = np.array([v[1] for v in cand])
            if ys.max() - ys.min() < 0.05:
                y[i] = ys.mean(); se[i] = PREC; method[i] = "vertex"
            else:
                y[i] = np.median(ys); se[i] = (ys.max() - ys.min()) / 2; method[i] = "vertex-ambiguous"
            continue
        # fallback: a horizontal segment's offsets at x_i, y_i +/- w/2
        m = np.abs(allpts[:, 0] - xv[i]) < xtol
        ys = np.sort(allpts[m, 1])
        pairs = [(a, b) for k, a in enumerate(ys) for b in ys[k + 1:] if abs((b - a) - w) < 0.05 * w]
        if pairs and len(ys) == 2:
            y[i] = np.mean([(a + b) / 2 for a, b in pairs]); se[i] = PREC; method[i] = "vertex-pair"
    # 2) dash pattern gap from vertex-free gaps between consecutive dashes
    gaps = []
    for A, B in zip(polys[:-1], polys[1:]):
        if not A["caps"] or not B["caps"] or A["clipped"] or B["clipped"]:
            continue
        Ec, Sc = A["caps"][-1]["mid"], B["caps"][0]["mid"]
        if Sc[0] < Ec[0] - 1e-6 or any(Ec[0] < xv[i] < Sc[0] for i in range(n)):
            continue
        gaps.append(float(np.hypot(*(Sc - Ec))))
    g = gap_override if gap_override is not None else (float(np.median(gaps)) if gaps else np.nan)
    gspread = (np.percentile(gaps, 90) - np.percentile(gaps, 10)) / 2 if len(gaps) > 2 else 0.05
    # 3) centre-line points per segment (vertices exact; cap midpoints; pair midlines)
    segpts = [[] for _ in range(max(n - 1, 0))]
    for i in range(n):
        if not np.isnan(y[i]) and method[i] != "vertex-ambiguous":
            if i > 0: segpts[i - 1].append((xv[i], y[i], PREC))
            if i < n - 1: segpts[i].append((xv[i], y[i], PREC))
    for P in polys:
        for (px, py) in P["centre"]:
            k = int(np.searchsorted(xv, px) - 1)
            if 0 <= k < n - 1 and xv[k] - 1e-6 <= px <= xv[k + 1] + 1e-6:
                segpts[k].append((px, py, PREC))

    def line_est(k, xi):
        """evaluate segment k's centre line at xi -> (y, err) or None"""
        pts = np.array(segpts[k]) if segpts[k] else np.zeros((0, 3))
        if len(pts) < 2:
            return None
        # deduplicate
        P = np.unique(np.round(pts[:, :2], 4), axis=0)
        if len(P) < 2:
            return None
        # total least squares direction
        c = P.mean(0); U, S, Vt = np.linalg.svd(P - c)
        d = Vt[0]
        if abs(d[0]) < 1e-4:
            return None
        base = (P - c) @ d
        L = base.max() - base.min()
        yi = c[1] + (xi - c[0]) * d[1] / d[0]
        dist = abs(xi - c[0]) / abs(d[0])
        err = PREC * (1 + dist / max(L, 1e-3)) / abs(d[0])   # position + angle error, projected vertically
        return yi, err

    for i in range(n):
        if not np.isnan(y[i]) and method[i] != "vertex-ambiguous":
            continue
        est = []
        if i > 0:
            r = line_est(i - 1, xv[i])
            if r: est.append((r[0], r[1], "line"))
        if i < n - 1:
            r = line_est(i, xv[i])
            if r: est.append((r[0], r[1], "line"))
        # path-length ('ellipse') constraint is applied in a second pass below
        if method[i] == "vertex-ambiguous":
            est.append((y[i], se[i], "vertex-ambiguous"))
        if est:
            wts = np.array([1 / max(e[1], 1e-3) ** 2 for e in est]); vals = np.array([e[0] for e in est])
            y[i] = float(np.sum(wts * vals) / wts.sum())
            se[i] = float(max(1 / np.sqrt(wts.sum()), (vals.max() - vals.min()) / 2 if len(vals) > 1 else 0))
            method[i] = "+".join(sorted(set(e[2] for e in est)))
            if verbose:
                print(f"  gap vertex {i+1}: " + "; ".join(f"{e[2]}={e[0]:.2f}+/-{e[1]:.2f}" for e in est) + f" -> {y[i]:.2f} se {se[i]:.2f}")
    # second pass: dash-pattern path-length constraint for gaps (E of dash A -> vertices -> S of dash B)
    if not np.isnan(g):
        for A, B in zip(polys[:-1], polys[1:]):
            if not A["caps"] or not B["caps"] or A["clipped"] or B["clipped"]:
                continue
            Ec, Sc = A["caps"][-1]["mid"], B["caps"][0]["mid"]
            if Sc[0] < Ec[0] - 1e-6:
                continue
            ids = [i for i in range(n) if Ec[0] < xv[i] < Sc[0]]
            if not ids:
                continue
            unknown = [i for i in ids if np.isnan(y[i]) or (method[i] and "vertex" not in method[i] and se[i] > 0.3)]
            # single-vertex gaps: always refine (combine with the line estimates); multi-vertex gaps: only when one vertex is open
            if len(ids) == 1:
                unknown = ids
            if len(unknown) != 1:
                continue
            m = unknown[0]
            def total(yy):
                P = [Ec] + [np.array([xv[i], yy if i == m else y[i]]) for i in ids] + [Sc]
                return sum(np.hypot(*(P[k + 1] - P[k])) for k in range(len(P) - 1)) - g
            # chord reference: the straight line between m's neighbours on the path
            prev = Ec if m == ids[0] else np.array([xv[m - 1], y[m - 1]]); nxt = Sc if m == ids[-1] else np.array([xv[m + 1], y[m + 1]])
            ychord = prev[1] + (xv[m] - prev[0]) * (nxt[1] - prev[1]) / (nxt[0] - prev[0]) if nxt[0] != prev[0] else (prev[1] + nxt[1]) / 2
            roots = []
            for lo, hi in ((ychord - 300, ychord), (ychord, ychord + 300)):
                try:
                    if total(lo) * total(hi) < 0:
                        roots.append(brentq(total, lo, hi, xtol=1e-6))
                except ValueError:
                    pass
            if not roots:
                continue
            prior = [e for e in ([(y[m], se[m])] if not np.isnan(y[m]) else [])]
            if len(roots) == 2 and prior:
                root = min(roots, key=lambda r: abs(r - prior[0][0]))
                # only trust the choice if the prior discriminates between the roots
                if abs(roots[0] - roots[1]) < 2 * max(prior[0][1], 0.05):
                    root = None
            elif len(roots) == 1:
                root = roots[0]
            else:
                root = None
            if root is not None:
                df = (total(root + 0.01) - total(root - 0.01)) / 0.02
                err = abs(max(gspread, PREC) / df) if abs(df) > 1e-6 else np.inf
                if prior:
                    wts = np.array([1 / max(prior[0][1], 1e-3) ** 2, 1 / max(err, 1e-3) ** 2]); vals = np.array([prior[0][0], root])
                    y[m] = float(np.sum(wts * vals) / wts.sum()); se[m] = float(max(1 / np.sqrt(wts.sum()), abs(vals[0] - vals[1]) / 2))
                    method[m] = method[m] + "+ellipse"
                else:
                    y[m] = root; se[m] = err; method[m] = "ellipse"
            else:
                # two symmetric roots, nothing to choose between them: report their mean with the half-difference as se
                y[m] = float(np.mean(roots)); se[m] = float(abs(roots[0] - roots[1]) / 2); method[m] = "ellipse-2roots"
            if verbose:
                print(f"  gap vertex {m+1} (gap with {len(ids)} vertices): roots {np.round(roots, 2)} -> {y[m]:.2f} se {se[m]:.2f} [{method[m]}]")
    if verbose:
        from collections import Counter
        print(f"  polygons={len(polys)} caps/poly={Counter(len(P['caps']) for P in polys)} V found={len(allV)}")
        print(f"  pattern gap g={g:.3f} from {len(gaps)} vertex-free gaps (10-90% half-range {gspread:.3f}); methods={Counter(method)}")
    return dict(y=y, se=se, method=method, gap=g, gaps=gaps, polys=polys)
