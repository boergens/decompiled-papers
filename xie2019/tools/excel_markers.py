"""Helpers for the Excel line charts of xie2019 (Figs. 12 and 13): raster images with light-grey gridlines
and round markers joined by smoothed lines.

gridlines(): light-grey gridline positions (group centres) along one axis, inside a pixel window.
markers():   centres of the round markers of one series colour: the series colour mask is reduced to the pixels
             farther than CORE px from its edge (the ~4 px wide joining line drops out, the ~17 px markers
             keep a core), each core component is one marker. The centre is fitted as the centre of the
             circle through the marker's outer edge (least-squares circle fit on the mask boundary pixels
             within MAX_R of the core centroid), so a marker partly covered by another one is still centred.
"""
import numpy as np
from scipy import ndimage as ndi

EXCEL_BLUE = (68, 114, 196)
EXCEL_ORANGE = (237, 125, 49)
CORE = 4.5
MAX_R = 11


def gridlines(a, axis, lo, hi, win0, win1, min_frac=0.3):
    """axis=0: horizontal gridlines (rows), counted over columns win0..win1; axis=1: vertical (columns)."""
    g = a.astype(float).mean(2)
    sat = a.max(2).astype(int) - a.min(2).astype(int)
    grey = (g > 150) & (g < 245) & (sat < 20)
    if axis == 0:
        s = grey[lo:hi, win0:win1].sum(1)
        n = win1 - win0
    else:
        s = grey[win0:win1, lo:hi].sum(0)
        n = win1 - win0
    idx = np.where(s > min_frac * n)[0] + lo
    groups = []
    for i in idx:
        if groups and i <= groups[-1][-1] + 1:
            groups[-1].append(i)
        else:
            groups.append([i])
    return [float(np.mean(gp)) for gp in groups]


def colour_mask(a, rgb, tol=60):
    return np.sqrt(((a.astype(float) - np.array(rgb, float)) ** 2).sum(2)) < tol


def circle_fit(xs, ys):
    A = np.c_[2 * xs, 2 * ys, np.ones_like(xs)]
    b = xs ** 2 + ys ** 2
    (cx, cy, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    return cx, cy, np.sqrt(c + cx ** 2 + cy ** 2)


def markers(a, rgb, exclude_boxes=(), tol=60):
    """Return [(x, y, r, n_core_px)] marker centres in image pixels, sorted by x."""
    m = colour_mask(a, rgb, tol)
    dt = ndi.distance_transform_edt(m)
    core = dt >= CORE
    lab, k = ndi.label(core)
    edge = m & ~ndi.binary_erosion(m)
    ey, ex = np.where(edge)
    out = []
    for i in range(1, k + 1):
        ys, xs = np.where(lab == i)
        x0, y0 = xs.mean(), ys.mean()
        if any(c0 <= x0 <= c1 and r0 <= y0 <= r1 for c0, r0, c1, r1 in exclude_boxes):
            continue
        sel = (ex - x0) ** 2 + (ey - y0) ** 2 <= MAX_R ** 2
        # keep only boundary pixels that face away from the core (outer rim of this marker)
        d = np.sqrt((ex[sel] - x0) ** 2 + (ey[sel] - y0) ** 2)
        rim = d >= 5
        cx, cy, r = circle_fit(ex[sel][rim].astype(float), ey[sel][rim].astype(float))
        if not (abs(cx - x0) < 4 and abs(cy - y0) < 4 and 6 < r < 11):
            cx, cy, r = x0, y0, float("nan")   # fit failed (crowded rim): fall back to the core centroid
        out.append((cx, cy, r, len(xs)))
    return sorted(out)
