"""Helpers shared by the figure extraction scripts of xu2017 (written for this paper).

All plots in Xu et al. 2017 are raster images embedded in the PDF; every script loads the
embedded image with digitize_common.embedded_image() and works in its pixel coordinates.
"""
from pathlib import Path

import numpy as np
from scipy import ndimage

from digitize_common import embedded_image

KEY = Path(__file__).resolve().parent.parent          # the xu2017/ folder
PDF = KEY / "source" / "elife-25916-v3.pdf"
WORK = KEY / "work"


def load(page):
    """Embedded image of the figure on <page> (the largest image there), RGB uint8."""
    return embedded_image(str(PDF), page)


def work_path(name):
    WORK.mkdir(exist_ok=True)
    return str(WORK / name)


def blobs(mask, min_area=20, max_area=None):
    """Connected components of a bool mask: list of (x_centroid, y_centroid, area, bbox)."""
    lab, n = ndimage.label(mask)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None:
            continue
        m = lab[sl] == i
        area = int(m.sum())
        if area < min_area or (max_area and area > max_area):
            continue
        ys, xs = np.nonzero(m)
        out.append((sl[1].start + xs.mean(), sl[0].start + ys.mean(), area,
                    (sl[1].start, sl[0].start, sl[1].stop, sl[0].stop)))
    return out


def lin(p0, v0, p1, v1):
    """Linear pixel -> value map through two reference points."""
    m = (v1 - v0) / (p1 - p0)
    return lambda p: v0 + m * (np.asarray(p, float) - p0)


def logmap(p0, v0, p1, v1):
    """Log10 pixel -> value map through two reference points."""
    f = lin(p0, np.log10(v0), p1, np.log10(v1))
    return lambda p: 10 ** f(p)


def column_centres(mask, x0, x1, y0, y1, min_px=1):
    """For each column in [x0,x1): (x, mean row, top row, bottom row) of mask pixels in rows [y0,y1); NaN if none."""
    out = []
    for c in range(x0, x1):
        r = np.nonzero(mask[y0:y1, c])[0]
        if len(r) < min_px:
            out.append((c, np.nan, np.nan, np.nan))
        else:
            out.append((c, y0 + r.mean(), y0 + r.min(), y0 + r.max()))
    return np.array(out, float)


def split_disks(blob_mask, r, kmax=8):
    """Split a blob of overlapping equal filled circles of radius r into circle centres.

    For k = 1..kmax circles, starts with centres spread along the blob's principal axis and
    minimises the number of mismatched pixels between the union of k discs and the blob
    (Powell); returns the centres (x, y in the blob mask's coordinates) of the best k, where an
    extra circle must reduce the mismatch by more than 15 % of one disc's area.
    """
    from scipy.optimize import minimize
    ys, xs = np.nonzero(blob_mask)
    H, W = blob_mask.shape
    yy, xx = np.mgrid[0:H, 0:W]
    target = blob_mask.astype(float)

    def render(c):
        img = np.zeros((H, W))
        for i in range(0, len(c), 2):
            d = np.hypot(xx - c[i], yy - c[i + 1])
            img = np.maximum(img, np.clip(r + 0.5 - d, 0, 1))
        return img

    def cost(c):
        return float(np.abs(render(c) - target).sum())

    cx, cy = xs.mean(), ys.mean()
    cov = np.cov(np.vstack([xs - cx, ys - cy]))
    w, v = np.linalg.eigh(cov)
    ax = v[:, -1]
    half = max(0.0, np.sqrt(w[-1]) * np.sqrt(3) - r * 0.5)
    best, area1 = None, np.pi * r * r
    for k in range(1, kmax + 1):
        ts = np.linspace(-half, half, k) if k > 1 else [0.0]
        c0 = np.ravel([[cx + t * ax[0], cy + t * ax[1]] for t in ts])
        res = minimize(cost, c0, method="Powell", options={"xtol": 0.05, "ftol": 0.5, "maxfev": 20000})
        if best is None or res.fun < best[0] - 0.15 * area1:
            best = (res.fun, res.x)
        else:
            break
    c = best[1]
    return [(c[i], c[i + 1]) for i in range(0, len(c), 2)], best[0]
