"""Fig. 7a/7b extraction (3D surface plots of total energy vs. two torsion angles); see surf3d.py.

Per panel: axis lines and ticks -> camera matrix (DLT) -> each surface pixel: energy from its
colour via the colour key, then (phi1, phi2) by intersecting its view ray with the plane of that
energy. Output: one row per surface pixel (native resolution), and a regular (phi1, phi2) grid
(mean energy of the pixels in each cell).
"""
import itertools

import numpy as np

import fukplot as fp
import surf3d as s3


def pick_ticks(ts, vals):
    """Choose len(vals) of the detected tick positions that fit a 1D projective map best."""
    best = None
    for sub in itertools.combinations(sorted(ts), len(vals)):
        f = s3.fit_proj1d(vals, sub)
        if best is None or f["rms"] < best[0]["rms"]:
            best = (f, list(sub))
    return best


def run(page, bbox, axes, key):
    """axes: {name: (p0, p1, side, values)} for 'phi1', 'phi2', 'E'; key: (col0, col1, vtop, vbot)."""
    a = fp.load(page, bbox)
    g = a.max(2)
    lines, fits, ticks = {}, {}, {}
    for k, (p0, p1, side, vals) in axes.items():
        ln = s3.refine_line(g < 90, p0, p1, tol=2.5)
        ts = s3.ticks_along(g < 180, ln, side, off=(1.6, 4.4), mingap=2, minpix=2)
        f, sub = pick_ticks(ts, vals)
        lines[k], fits[k], ticks[k] = ln, f, (sub, vals, ts)
    # corners: front = phi1 x phi2 line crossing, left = phi1 x E line crossing
    t1f, t2f = s3.intersect_t(lines["phi1"], lines["phi2"])
    t1l, tEl = s3.intersect_t(lines["phi1"], lines["E"])
    phi1_front = s3.proj1d_inv(fits["phi1"], t1f)
    phi2_front = s3.proj1d_inv(fits["phi2"], t2f)
    phi1_left = s3.proj1d_inv(fits["phi1"], t1l)
    E_floor = s3.proj1d_inv(fits["E"], tEl)
    X, uv = [], []
    for t, v in zip(ticks["phi1"][0], ticks["phi1"][1]):
        X.append((v, phi2_front, E_floor)); uv.append(s3.point(lines["phi1"], t))
    for t, v in zip(ticks["phi2"][0], ticks["phi2"][1]):
        X.append((phi1_front, v, E_floor)); uv.append(s3.point(lines["phi2"], t))
    for t, v in zip(ticks["E"][0], ticks["E"][1]):
        X.append((phi1_left, phi2_front, v)); uv.append(s3.point(lines["E"], t))
    X, uv = np.array(X), np.array(uv)
    P = s3.fit_dlt(X, uv)
    res = np.sqrt(((s3.project(P, X) - uv) ** 2).sum(1))
    # colour key
    c0, c1, vtop, vbot = key
    sat = (a.astype(int).max(2) - a.astype(int).min(2)) > 60
    keycol = (c0 + c1) // 2
    krows = np.where(sat[:, keycol] | (g[:, keycol] < 60))[0]
    krows = krows[krows > 45]               # below the panel letter
    r0, r1 = int(krows.min()), int(krows.max())
    kc, kv = s3.colour_key(a, (c0 + 3, c1 - 3), r0, r1, vtop, vbot)
    # surface pixels: saturated colours left of the key, within the plot
    H, W = g.shape
    ys, xs = np.nonzero(sat[:, : c0 - 15])
    pix = a[ys, xs]
    E, Eerr, dmin, ok = s3.decode(pix, kc, kv)
    ys, xs, E, Eerr, dmin = ys[ok], xs[ok], E[ok], Eerr[ok], dmin[ok]
    p1, p2 = s3.invert(P, xs.astype(float), ys.astype(float), E)
    info = dict(fits=fits, ticks=ticks, lines=lines, phi1_front=phi1_front, phi2_front=phi2_front,
                phi1_left=phi1_left, E_floor=E_floor, P=P, dlt_res_max=float(res.max()), dlt_res_rms=float(np.sqrt((res ** 2).mean())),
                key_rows=(r0, r1), n_pix=len(xs), dmin_median=float(np.median(dmin)))
    return a, dict(px=xs, py=ys, E=E, Eerr=Eerr, phi1=p1, phi2=p2, dist=dmin), info


def grid(d, phi1_edges, phi2_edges, lim1, lim2):
    """Mean energy per (phi1, phi2) cell of the pixels that fall inside the axis ranges."""
    m = (d["phi1"] >= lim1[0]) & (d["phi1"] <= lim1[1]) & (d["phi2"] >= lim2[0]) & (d["phi2"] <= lim2[1])
    i = np.digitize(d["phi1"][m], phi1_edges) - 1
    j = np.digitize(d["phi2"][m], phi2_edges) - 1
    n1, n2 = len(phi1_edges) - 1, len(phi2_edges) - 1
    ok = (i >= 0) & (i < n1) & (j >= 0) & (j < n2)
    S = np.zeros((n1, n2)); N = np.zeros((n1, n2)); S2 = np.zeros((n1, n2))
    np.add.at(S, (i[ok], j[ok]), d["E"][m][ok])
    np.add.at(S2, (i[ok], j[ok]), d["E"][m][ok] ** 2)
    np.add.at(N, (i[ok], j[ok]), 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = S / N
        sd = np.sqrt(np.maximum(S2 / N - mean ** 2, 0))
    return mean, sd, N
