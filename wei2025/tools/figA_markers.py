"""Marker and line extraction for the Origin line+symbol plots of wei2025 Fig. 6 (fork A).

- find_markers: normalized cross-correlation (cv2.TM_CCOEFF_NORMED, RGB) with the panel's own legend
  symbol as template, local maxima >= threshold, non-maximum suppression over a 7 px window.
- line_mask: pixels whose colour lies on the white->series-colour mixing line (anti-aliased line pixels),
  minus discs around the detected markers.
- column_runs: per pixel column, the centre row of every run of mask pixels (curves can be multivalued).
"""
import numpy as np
import cv2
from scipy.ndimage import maximum_filter


def legend_template(a, box, half=9, thr=200):
    """Find the legend symbol inside box=(c0,c1,r0,r1): the column range where the dark-pixel count per
    column is > 8 (the thin legend line has ~5). Return (template RGB float32, centre (x, y))."""
    c0, c1, r0, r1 = box
    g = a[r0:r1, c0:c1].astype(float).mean(2) < thr
    cols = g.sum(0)
    idx = np.where(cols > 8)[0]
    # the first group of thick columns is the symbol
    grp = [idx[0]]
    for i in idx[1:]:
        if i <= grp[-1] + 1:
            grp.append(i)
        else:
            break
    sub = g[:, grp[0]:grp[-1] + 1]
    ys, xs = np.where(sub)
    cy, cx = r0 + ys.mean(), c0 + grp[0] + xs.mean()
    iy, ix = int(round(cy)), int(round(cx))
    T = a[iy - half:iy + half + 1, ix - half:ix + half + 1].astype(np.float32)
    return T, (cx, cy), (ix - cx, iy - cy)


def find_markers(a, T, region, thr=0.6, nms=7, exclude=()):
    """region=(c0,c1,r0,r1) in image pixels. Returns array of (x, y, score) of marker centres
    (template centre), excluding points inside any exclude box (c0,c1,r0,r1)."""
    c0, c1, r0, r1 = region
    h = T.shape[0] // 2
    I = a[r0:r1, c0:c1].astype(np.float32)
    R = cv2.matchTemplate(I, T, cv2.TM_CCOEFF_NORMED)
    mx = maximum_filter(R, size=nms)
    pk = np.argwhere((R == mx) & (R >= thr))
    out = []
    for y, x in pk:
        X, Y = c0 + x + h, r0 + y + h
        if any(e[0] <= X <= e[1] and e[2] <= Y <= e[3] for e in exclude):
            continue
        out.append((float(X), float(Y), float(R[y, x])))
    return np.array(out).reshape(-1, 3)


def line_mask(a, colour, t_min=0.55, resid_max=70):
    """Pixels P close to the mixing line W + t (C - W) between white W and series colour C, with t >= t_min."""
    P = a.astype(float)
    W = np.array([255.0, 255.0, 255.0])
    C = np.array(colour, float)
    d = C - W
    t = ((P - W) @ d) / (d @ d)
    resid = np.linalg.norm(P - (W + t[..., None] * d), axis=2)
    return (t >= t_min) & (resid <= resid_max)


def column_runs(mask, c0, c1, r0, r1, min_len=2):
    """[(x, y_centre, run_length)] for every vertical run of mask pixels in each column."""
    out = []
    for c in range(c0, c1):
        r = np.where(mask[r0:r1, c])[0]
        if len(r) == 0:
            continue
        runs = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
        for q in runs:
            if len(q) >= min_len:
                out.append((c, r0 + q.mean(), len(q)))
    return out


def series_mask(a, colour, dark_thr=150, t_min=0.5, resid_max=80):
    """Binary mask of one series (line + symbols): for a black series gray < dark_thr, otherwise the
    white->colour mixing-line test. Closed with a 5 px disc; holes smaller than 80 px (symbol highlights) filled."""
    if tuple(colour) == (0, 0, 0):
        m = a.astype(float).mean(2) < dark_thr
    else:
        m = line_mask(a, colour, t_min=t_min, resid_max=resid_max)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    inv = (1 - m).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 4)
    small = np.isin(lab, np.where(st[:, 4] < 80)[0])
    return (m.astype(bool) | small)


def dt_peaks(mask, region, thr=4.5, nms=7):
    """Local maxima of the distance transform of mask inside region=(c0,c1,r0,r1) with value >= thr
    (symbols are ~12 px discs, the line ~5 px wide, so only symbol centres reach >= 4.5)."""
    c0, c1, r0, r1 = region
    m = mask[r0:r1, c0:c1].astype(np.uint8)
    D = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    mx = maximum_filter(D, size=nms)
    pk = np.argwhere((D == mx) & (D >= thr))
    return np.array([(c0 + x, r0 + y, D[y, x]) for y, x in pk], float).reshape(-1, 3)


def ncc_peaks_gray(a, centre, region, half=9, thr=0.5, nms=7):
    """Grayscale normalized cross-correlation with the legend symbol centred at centre=(ix, iy)."""
    I = a.astype(np.float32).mean(2)
    ix, iy = centre
    T = I[iy - half:iy + half + 1, ix - half:ix + half + 1]
    c0, c1, r0, r1 = region
    R = cv2.matchTemplate(I[r0:r1, c0:c1], T, cv2.TM_CCOEFF_NORMED)
    mx = maximum_filter(R, size=nms)
    pk = np.argwhere((R == mx) & (R >= thr))
    return np.array([(c0 + x + half, r0 + y + half, R[y, x]) for y, x in pk], float).reshape(-1, 3)


def merge_points(*sets, dist=5.0):
    """Union of point sets (x, y, score), dropping points within dist px of an earlier kept point.
    Returns (x, y, source_index)."""
    kept = []
    for si, s in enumerate(sets):
        for x, y, _ in s:
            if all((x - k[0]) ** 2 + (y - k[1]) ** 2 > dist ** 2 for k in kept):
                kept.append((x, y, si))
    return np.array(kept, float).reshape(-1, 3)


def candidate_scores(a, mask, centre, pts, half=9):
    """For each candidate (x, y): (DT value of mask at the point, best gray NCC with the legend symbol
    within +-3 px)."""
    D = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
    I = a.astype(np.float32).mean(2)
    ix, iy = centre
    T = I[iy - half:iy + half + 1, ix - half:ix + half + 1]
    out = []
    for x, y in pts:
        xi, yi = int(round(x)), int(round(y))
        win = I[yi - half - 3:yi + half + 4, xi - half - 3:xi + half + 4]
        if win.shape != (T.shape[0] + 6, T.shape[1] + 6):
            out.append((float(D[yi, xi]), 0.0))
            continue
        R = cv2.matchTemplate(win, T, cv2.TM_CCOEFF_NORMED)
        out.append((float(D[yi - 1:yi + 2, xi - 1:xi + 2].max()), float(R.max())))
    return out


def draw_cross(im, x, y, colour, size=5, thick=1):
    xi, yi = int(round(x)), int(round(y))
    h, w = im.shape[:2]
    im[max(0, yi - thick):yi + thick + 1, max(0, xi - size):xi + size + 1] = colour
    im[max(0, yi - size):yi + size + 1, max(0, xi - thick):xi + thick + 1] = colour
