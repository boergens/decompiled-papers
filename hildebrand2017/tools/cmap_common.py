"""Colour-key helpers for the calibrated colour maps of hildebrand2017 (Fig. 4b,e,g,h,j; Extended Data Fig. 9f,h,j,k).

A colour bar is sampled in the figure image itself (mean RGB across its width, one entry per pixel row),
and each map pixel or cell colour is assigned the value of the nearest colour-bar entry (Euclidean RGB).
The distance to that entry is kept as a quality measure (JPEG noise gives ~5-15; > 40 means the colour is
not on the key, e.g. black = no data, white separators, labels).
"""
import numpy as np


def bar_lut(a, c0, c1, r_top, r_bot, v_top, v_bot):
    """LUT from a vertical colour bar occupying columns c0..c1 (inclusive) and rows r_top..r_bot (inclusive),
    linear from v_top (top row edge) to v_bot (bottom row edge). Returns (rgb[N,3], values[N])."""
    rows = np.arange(r_top, r_bot + 1)
    rgb = a[r_top:r_bot + 1, c0:c1 + 1].astype(float).mean(1)
    # value at the row centre; bar edges = outer edges of the first/last rows
    frac = (rows + 0.5 - r_top) / (r_bot + 1 - r_top)
    vals = v_top + (v_bot - v_top) * frac
    return rgb, vals


def lookup(rgb_pixels, lut):
    """Nearest-LUT value and RGB distance for an array of RGB pixels (..., 3)."""
    lrgb, lval = lut
    p = np.asarray(rgb_pixels, float)
    flat = p.reshape(-1, 3)
    d = np.sqrt(((flat[:, None, :] - lrgb[None, :, :]) ** 2).sum(2))
    i = d.argmin(1)
    return lval[i].reshape(p.shape[:-1]), d[np.arange(len(i)), i].reshape(p.shape[:-1]), i.reshape(p.shape[:-1])


def first_last(mask):
    idx = np.where(mask)[0]
    return int(idx[0]), int(idx[-1])


def sample_cells(a, lefts, tops, w, h, lut, inset=3):
    """Median colour of the inner part of each cell (cells given by their left/top pixel and size) mapped
    through the LUT. Returns dict (i, j) -> (value, rgb_dist, (cx, cy))."""
    out = {}
    for i, t in enumerate(tops):
        for j, l in enumerate(lefts):
            blk = a[t + inset:t + h - inset, l + inset:l + w - inset].reshape(-1, 3).astype(float)
            rgb = np.median(blk, 0)
            v, d, _ = lookup(rgb[None], lut)
            out[(i, j)] = (float(v[0]), float(d[0]), (l + w / 2, t + h / 2))
    return out
