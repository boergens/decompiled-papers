"""Helpers for the fork-B digitizations of wei2025 (Figs. 7, 10, 14a, 17): axis frame and tick finding
inside one panel region of an embedded raster image, and colour classification of plot pixels.

All coordinates are pixel (column, row) of the embedded image; regions are (x0, y0, x1, y1).
"""
import numpy as np


def groups(idx):
    """Consecutive integer runs -> list of (first, last)."""
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(g) for g in out]


def frame(dark, region, frac=0.6):
    """Axis-box lines inside region: returns dict with 'top','bottom' (row runs) and 'left','right' (column runs).

    Picks the first and last long horizontal runs and the first and last long vertical runs.
    """
    x0, y0, x1, y1 = region
    sub = dark[y0:y1, x0:x1]
    rs = sub.sum(1)
    cs = sub.sum(0)
    hr = groups(np.where(rs >= frac * rs.max())[0])
    vc = groups(np.where(cs >= frac * cs.max())[0])
    return {"top": (y0 + hr[0][0], y0 + hr[0][1]), "bottom": (y0 + hr[-1][0], y0 + hr[-1][1]),
            "left": (x0 + vc[0][0], x0 + vc[0][1]), "right": (x0 + vc[-1][0], x0 + vc[-1][1])}


def ticks_h(dark, line, side, length, c0, c1, frac=0.8):
    """Tick columns on a horizontal axis line (row run `line`); side -1 above, +1 below."""
    r0, r1 = line
    band = dark[r0 - length:r0, c0:c1] if side < 0 else dark[r1 + 1:r1 + 1 + length, c0:c1]
    g = groups(np.where(band.mean(0) >= frac)[0])
    return [c0 + (a + b) / 2 for a, b in g]


def ticks_v(dark, line, side, length, r0, r1, frac=0.8):
    """Tick rows on a vertical axis line (column run `line`); side -1 left, +1 right."""
    c0, c1 = line
    band = dark[r0:r1, c0 - length:c0] if side < 0 else dark[r0:r1, c1 + 1:c1 + 1 + length]
    g = groups(np.where(band.mean(1) >= frac)[0])
    return [r0 + (a + b) / 2 for a, b in g]


def mid(run):
    return (run[0] + run[1]) / 2


def linfit(pix, val):
    """Linear map pixel -> value; returns (f, max residual, slope)."""
    pix = np.asarray(pix, float)
    val = np.asarray(val, float)
    A = np.vstack([pix, np.ones_like(pix)]).T
    (m, b), *_ = np.linalg.lstsq(A, val, rcond=None)
    res = float(np.max(np.abs(A @ [m, b] - val))) if len(pix) > 2 else 0.0
    return (lambda p: m * np.asarray(p, float) + b), res, m


def classify(a, refs, max_dist=60, min_sat=0):
    """Label each pixel with the index of the nearest reference colour (RGB) or -1.

    refs: list of RGB triples. A pixel is labelled only if its distance to the nearest ref is
    <= max_dist and its saturation (max-min channel) >= min_sat.
    """
    a = a.astype(float)
    d = np.stack([np.sqrt(((a - np.array(r, float)) ** 2).sum(2)) for r in refs], 0)
    lab = d.argmin(0)
    dm = d.min(0)
    sat = a.max(2) - a.min(2)
    lab[(dm > max_dist) | (sat < min_sat)] = -1
    return lab


def runs_in_column(col_mask, gap=2):
    """Runs of True in a 1-D mask (indices), split where gaps > gap."""
    r = np.where(col_mask)[0]
    if len(r) == 0:
        return []
    return np.split(r, np.where(np.diff(r) > gap)[0] + 1)


def overlay_series(a, series_pts, out_png, crop=None, scale=1):
    """Check image: the source in light grey, each series' extracted points drawn in its own colour.

    series_pts: list of (rgb, [(x, y), ...], size) ; size 1 draws 1-px dots, size >1 draws a cross of that half-size.
    """
    from PIL import Image
    g = a.astype(float).mean(2)
    im = np.stack([155 + 0.39 * g] * 3, 2).astype(np.uint8)
    for rgb, pts, size in series_pts:
        for x, y in pts:
            if x != x or y != y:
                continue
            xi, yi = int(round(x)), int(round(y))
            if size <= 1:
                if 0 <= yi < im.shape[0] and 0 <= xi < im.shape[1]:
                    im[yi, xi] = rgb
            else:
                for d in range(-size, size + 1):
                    for yy, xx in ((yi + d, xi), (yi, xi + d)):
                        if 0 <= yy < im.shape[0] and 0 <= xx < im.shape[1]:
                            im[yy, xx] = rgb
    out = Image.fromarray(im)
    if crop:
        out = out.crop(crop)
    if scale != 1:
        out = out.resize((out.width * scale, out.height * scale), Image.NEAREST)
    out.save(out_png)
