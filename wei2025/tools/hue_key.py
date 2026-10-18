"""Map rendered atom colours to values through a rainbow colour key (shared by fig9a_extract.py, fig15_extract.py).

The MD snapshots are OVITO renderings with shaded spheres, so brightness varies across each atom; the key runs
blue -> cyan -> green -> yellow -> red with monotonically falling hue. A pixel's value is therefore read from its
hue alone (nearest hue on the key's centre row, ends trimmed by 4 px against JPEG blending), and only for pixels
that are saturated enough to carry a hue (white background, grey surface mesh and dark outlines are left empty).
"""
import colorsys

import numpy as np


def hue_deg(rgb):
    a = np.asarray(rgb, float) / 255.0
    mx, mn = a.max(-1), a.min(-1)
    d = np.where(mx - mn == 0, 1e-9, mx - mn)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60.0
    return h, mx - mn, mx


def key_profile(a, row0, row1, col0, col1, v0, v1, trim=4):
    """Hue along the key (median over its rows), with the value of each column (linear v0 at col0 .. v1 at col1)."""
    cols = np.arange(col0 + trim, col1 - trim + 1)
    h, _, _ = hue_deg(a[row0 + 3:row1 - 2, col0 + trim:col1 - trim + 1])
    h = np.median(h, axis=0)
    vals = v0 + (cols - col0) / (col1 - col0) * (v1 - v0)
    return h, vals


def map_values(rgb, key_h, key_v, min_sat=0.35, min_v=0.25, max_dh=12.0):
    """Value per pixel from its hue (NaN where the pixel carries no usable hue or no key hue is within max_dh)."""
    h, s, v = hue_deg(rgb)
    sat = s / np.maximum(v, 1e-9)
    # red hues near 360 wrap to the red end of the key (hue ~0-10)
    h = np.where(h > 300, h - 360, h)
    kh = np.where(key_h > 300, key_h - 360, key_h)
    d = np.abs(h[..., None] - kh[None, None, :])
    i = d.argmin(-1)
    out = key_v[i].astype(float)
    bad = (sat < min_sat) | (v < min_v) | (d.min(-1) > max_dh)
    out[bad] = np.nan
    return out


_ = colorsys
