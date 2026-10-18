"""Digitizing an Origin 3D colour-mapped surface plot (fuk2019 Fig. 7): helpers.

1. Axis lines: given rough end points, the black pixels within `tol` px of the segment are fitted
   with a straight line (principal axis).
2. Tick marks: black pixels 2-8 px off the line on one side, projected onto the line and grouped;
   the group centres are the tick positions t (px along the line).
3. 1D projective fit per axis, t = (a v + b) / (c v + 1) (a straight 3D line seen in
   perspective), fitted on the ticks; it gives the axis value at the box corners (line crossings).
4. Camera: direct linear transform (DLT, 3x4 matrix P) fitted on all ticks as 3D points:
   phi1 ticks at (phi1_i, phi2_front, E_floor), phi2 ticks at (phi1_front, phi2_j, E_floor),
   E ticks at (phi1_left, phi2_front, E_k); the coordinates of the corners come from step 3.
   Coordinates are normalised before the fit.
5. Inversion: a surface pixel (u, v) whose energy E is known from its colour lies on the plane
   E = const; P restricted to that plane is a homography, so (phi1, phi2) follow from two
   linear equations.
6. Colour key: the key column, row by row, maps colour to energy linearly from the top label
   (top edge of the key) to the bottom label (bottom edge). A pixel gets the mean energy of all
   key rows whose colour is within `slack` of its nearest key colour (so the long run of plain
   red in the key gives a wide range, reported as E_err).
"""
import numpy as np


def refine_line(dark, p0, p1, tol=3.0):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = (p1 - p0) / np.linalg.norm(p1 - p0)
    n = np.array([-d[1], d[0]])
    ys, xs = np.nonzero(dark)
    P = np.stack([xs, ys], 1).astype(float)
    t = (P - p0) @ d
    o = (P - p0) @ n
    sel = (np.abs(o) <= tol) & (t >= -2) & (t <= np.linalg.norm(p1 - p0) + 2)
    Q = P[sel]
    c = Q.mean(0)
    u, s, vt = np.linalg.svd(Q - c)
    d2 = vt[0] if vt[0] @ d > 0 else -vt[0]
    n2 = np.array([-d2[1], d2[0]])
    tt = (Q - c) @ d2
    resid = (Q - c) @ n2
    return dict(c=c, d=d2, n=n2, tmin=float(tt.min()), tmax=float(tt.max()), rms=float(resid.std()), npx=len(Q))


def ticks_along(dark, line, side, off=(2.5, 8.0), tpad=1.0, mingap=3.0, minpix=2):
    ys, xs = np.nonzero(dark)
    P = np.stack([xs, ys], 1).astype(float)
    t = (P - line["c"]) @ line["d"]
    o = ((P - line["c"]) @ line["n"]) * side
    sel = (o >= off[0]) & (o <= off[1]) & (t >= line["tmin"] - tpad) & (t <= line["tmax"] + tpad)
    ts = np.sort(t[sel])
    groups, cur = [], [ts[0]] if len(ts) else []
    for x in ts[1:]:
        if x - cur[-1] <= mingap:
            cur.append(x)
        else:
            groups.append(cur)
            cur = [x]
    if cur:
        groups.append(cur)
    return [float(np.mean(g)) for g in groups if len(g) >= minpix]


def point(line, t):
    return line["c"] + t * line["d"]


def intersect_t(l1, l2):
    """Parameters (t1, t2) of the crossing of two fitted lines."""
    A = np.stack([l1["d"], -l2["d"]], 1)
    t1, t2 = np.linalg.solve(A, l2["c"] - l1["c"])
    return float(t1), float(t2)


def fit_proj1d(vals, ts):
    vals, ts = np.asarray(vals, float), np.asarray(ts, float)
    A = np.stack([vals, np.ones_like(vals), -vals * ts], 1)
    (a, b, c), *_ = np.linalg.lstsq(A, ts, rcond=None)
    pred = (a * vals + b) / (c * vals + 1)
    return dict(a=a, b=b, c=c, rms=float(np.sqrt(np.mean((pred - ts) ** 2))), maxres=float(np.max(np.abs(pred - ts))))


def proj1d_inv(f, t):
    return (t - f["b"]) / (f["a"] - f["c"] * t)


def fit_dlt(X, uv):
    X, uv = np.asarray(X, float), np.asarray(uv, float)
    mx, sx = X.mean(0), X.std(0)
    mu, su = uv.mean(0), uv.std(0).mean()
    Xn = (X - mx) / sx
    un = (uv - mu) / su
    rows = []
    for (x, y, z), (u, v) in zip(Xn, un):
        rows.append([x, y, z, 1, 0, 0, 0, 0, -u * x, -u * y, -u * z, -u])
        rows.append([0, 0, 0, 0, x, y, z, 1, -v * x, -v * y, -v * z, -v])
    _, _, vt = np.linalg.svd(np.asarray(rows))
    Pn = vt[-1].reshape(3, 4)
    T = np.diag([1 / sx[0], 1 / sx[1], 1 / sx[2], 1.0])
    T[:3, 3] = -mx / sx
    Tu = np.array([[su, 0, mu[0]], [0, su, mu[1]], [0, 0, 1]])
    P = Tu @ Pn @ T
    return P / P[2, 3]


def project(P, X):
    X = np.atleast_2d(np.asarray(X, float))
    h = np.hstack([X, np.ones((len(X), 1))]) @ P.T
    return h[:, :2] / h[:, 2:3]


def invert(P, u, v, E):
    """(phi1, phi2) of the points on plane E that project to pixels (u, v); arrays."""
    u, v, E = map(np.asarray, (u, v, E))
    # u*(P2.X) = P0.X, v*(P2.X) = P1.X with X = (x, y, E, 1): linear in x, y
    a11 = P[0, 0] - u * P[2, 0]
    a12 = P[0, 1] - u * P[2, 1]
    b1 = -(P[0, 2] - u * P[2, 2]) * E - (P[0, 3] - u * P[2, 3])
    a21 = P[1, 0] - v * P[2, 0]
    a22 = P[1, 1] - v * P[2, 1]
    b2 = -(P[1, 2] - v * P[2, 2]) * E - (P[1, 3] - v * P[2, 3])
    det = a11 * a22 - a12 * a21
    x = (b1 * a22 - a12 * b2) / det
    y = (a11 * b2 - b1 * a21) / det
    return x, y


def colour_key(img, cols, row0, row1, vtop, vbot):
    """Key colours (median over the key columns) for rows row0..row1 and their energies."""
    rows = np.arange(row0, row1 + 1)
    cs = np.median(img[row0:row1 + 1, cols[0]:cols[1] + 1].astype(float), axis=1)
    vals = vtop + (rows - row0) / (row1 - row0) * (vbot - vtop)
    return cs, vals


def decode(pix, key_cols, key_vals, maxdist=45.0, slack=6.0):
    """Energy, half-range and colour distance for an (N,3) array of pixel colours."""
    pix = pix.astype(float)
    d = np.sqrt(((pix[:, None, :] - key_cols[None, :, :]) ** 2).sum(2))
    dmin = d.min(1)
    near = d <= (dmin[:, None] + slack)
    vv = np.where(near, key_vals[None, :], np.nan)
    E = np.nanmean(vv, 1)
    Eerr = (np.nanmax(vv, 1) - np.nanmin(vv, 1)) / 2 + abs(key_vals[1] - key_vals[0]) / 2
    ok = dmin <= maxdist
    return E, Eerr, dmin, ok
