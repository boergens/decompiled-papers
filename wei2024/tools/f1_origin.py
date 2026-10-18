"""Helpers for the Origin-style plots of wei2024 Fig. 5 (fork F1): colour masks, marker matching, line tracing."""
import numpy as np
from scipy import ndimage as ndi


def colour_masks(a):
    a = a.astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    return {
        "x": (mx < 130) & (mx - mn < 40),               # black / dark grey
        "y": (R > 170) & (G < 130) & (B < 130),          # red
        "z": (R > 170) & (B > 160) & (G < 140),          # magenta
    }


def split_thick(mask):
    """Split a mask into thick strokes (survive a 3x3 opening: dashes, lines) and thin ones (2-px marker outlines)."""
    thick = ndi.binary_opening(mask, np.ones((3, 3), bool))
    thin = mask & ~ndi.binary_dilation(thick, np.ones((3, 3), bool))
    return thick, thin


def match_markers(thin, template, thr, min_dist=5):
    """Normalized cross-correlation of a binary marker template on a binary mask; peaks >= thr,
    non-maximum suppression within min_dist px. Returns [(x_centre, y_centre, score)] in mask pixels.
    The centre is the centre of the template ink's bounding box (for triangles closer to the plotted
    position than the ink centroid; see BRIEF lesson from atkins2004)."""
    import cv2
    t = template.astype(np.float32)
    res = cv2.matchTemplate(thin.astype(np.float32), t, cv2.TM_CCORR_NORMED)
    yy, xx = np.where(t > 0)
    cy, cx = (yy.min() + yy.max()) / 2, (xx.min() + xx.max()) / 2
    peaks = []
    mxf = ndi.maximum_filter(res, size=2 * min_dist + 1)
    ys, xs = np.where((res >= thr) & (res == mxf))
    for y, x in sorted(zip(ys, xs), key=lambda q: -res[q]):
        if all((x - px) ** 2 + (y - py) ** 2 > min_dist ** 2 for px, py, _ in peaks):
            peaks.append((x, y, float(res[y, x])))
    return [(x + cx, y + cy, s) for x, y, s in peaks]
