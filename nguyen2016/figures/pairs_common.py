"""Helpers for digitizing the paired dot plots of Nguyen et al. 2016, Fig. 5h and 5i.

Both panels are raster (the embedded 1210 x 1229 px JPEG of Figure 5, about 220 ppi). Each panel
shows semi-transparent round markers (about 11 px across) at two category positions, "Cont" and
"Carbon", joined pairwise by thin lines of the marker's colour (blue, purple/violet, green).

Method, per marker (the seeds are approximate rows read off a colour profile; the code refines them):
  'run'    isolated marker: centre = midpoint of the run of coloured pixels down the category column,
           edges found at half the marker's ink level (sub-pixel);
  'top'    marker whose lower part is hidden by an overlapping marker: centre = top edge + radius;
  'bottom' marker whose upper part is hidden: centre = bottom edge - radius;
  'line'   marker inside a cluster of overlapping markers: centre = where the straight connecting
           line from its partner (whose centre is known) meets the category column. The line's
           direction is found by scanning end rows and counting pixels of the pair's colour on the
           segment between the two marker discs.
The radius is the mean half run length of the isolated markers of the same panel.
"""
import numpy as np

# "ink" = 255 - RGB of the pure marker fill colours, measured on isolated markers
INK = {
    "purple": np.array([40.0, 125.0, 3.0]),   # fill ~ (215,130,252)
    "blue": np.array([125.0, 125.0, 3.0]),    # fill ~ (130,130,252)
    "green": np.array([130.0, 40.0, 130.0]),  # fill ~ (125,215,125)
}


def ink(a):
    return 255.0 - a.astype(float)


def class_mask(a, colour, cos_min=0.97, mag_min=25):
    """Pixels whose ink vector points in the direction of the class colour (lines and fills)."""
    v = ink(a)
    ref = INK[colour] / np.linalg.norm(INK[colour])
    mag = np.linalg.norm(v, axis=2)
    cos = (v @ ref) / np.maximum(mag, 1e-6)
    return (cos >= cos_min) & (mag >= mag_min)


def column_profile(a, col, half=1):
    """Ink magnitude down a column (mean over col-half..col+half)."""
    v = ink(a[:, col - half:col + half + 1]).mean(1)
    return np.linalg.norm(v, axis=1)


def run_edges(profile, r0, r1, level):
    """Sub-pixel top and bottom edges of the run of profile >= level inside rows [r0, r1)."""
    p = profile
    idx = np.where(p[r0:r1] >= level)[0]
    if len(idx) == 0:
        return None
    top, bot = r0 + idx[0], r0 + idx[-1]
    # interpolate the crossing of `level` between the outer and inner pixel
    t = top - 1 + (level - p[top - 1]) / (p[top] - p[top - 1]) if p[top] != p[top - 1] else top
    b = bot + (p[bot] - level) / (p[bot] - p[bot + 1]) if p[bot] != p[bot + 1] else bot
    return float(t), float(b)


def best_line_end(a, colour, x0, y0, x1, y_lo, y_hi, r, step=0.25):
    """Row at column x1 of the straight line of `colour` that starts at (x0, y0).

    Scans candidate end rows y in [y_lo, y_hi]; for each, counts class pixels on the segment
    between the marker discs (x0 + r + 2 .. x1 - r - 2), allowing +-1 px vertically.
    Returns (best y, score = fraction of samples on class pixels, all (y, score)).
    """
    m = class_mask(a, colour, cos_min=0.93, mag_min=20)
    xs = np.arange(min(x0, x1) + r + 2, max(x0, x1) - r - 2, 0.5)
    res = []
    for y in np.arange(y_lo, y_hi + step / 2, step):
        ys = y0 + (y - y0) * (xs - x0) / (x1 - x0)
        hit = 0
        for x, yy in zip(xs, ys):
            xi, yi = int(round(x)), int(round(yy))
            if m[yi - 1:yi + 2, xi].any():
                hit += 1
        res.append((y, hit / len(xs)))
    res = np.array(res)
    best = res[:, 1].max()
    top = res[res[:, 1] >= best - 0.02]
    return float(top[:, 0].mean()), float(best), res


def fit_line(a, colour, x0, y0, x1, y1_guess, r, band=3.0):
    """Least-squares straight line through the pixels of one connecting line.

    Starts from the coarse segment (x0, y0) -> (x1, y1_guess); in each pixel column between the two
    marker discs (x0 + r + 2 .. x1 - r - 2) takes the ink-weighted centroid of the class pixels within
    +-band rows of the coarse line, then fits y = m x + b to those centroids (one robust re-fit
    dropping columns more than 1.5 px off, e.g. where another line crosses).
    Returns (y at x0, y at x1, rms residual in px, number of columns used).
    """
    m_cls = class_mask(a, colour, cos_min=0.93, mag_min=20)
    w_all = np.linalg.norm(ink(a), axis=2)
    xs, ys = [], []
    for x in range(int(np.ceil(min(x0, x1) + r + 2)), int(np.floor(max(x0, x1) - r - 2)) + 1):
        yc = y0 + (y1_guess - y0) * (x - x0) / (x1 - x0)
        rows = np.arange(int(np.floor(yc - band)), int(np.ceil(yc + band)) + 1)
        sel = m_cls[rows, x]
        if sel.sum() == 0:
            continue
        w = w_all[rows, x] * sel
        xs.append(x)
        ys.append(float((rows * w).sum() / w.sum()))
    xs, ys = np.array(xs, float), np.array(ys, float)
    keep = np.ones(len(xs), bool)
    for _ in range(2):
        m, b = np.polyfit(xs[keep], ys[keep], 1)
        res = ys - (m * xs + b)
        keep = np.abs(res) <= 1.5
    m, b = np.polyfit(xs[keep], ys[keep], 1)
    rms = float(np.sqrt(np.mean((ys[keep] - (m * xs[keep] + b)) ** 2)))
    return float(m * x0 + b), float(m * x1 + b), rms, int(keep.sum())
