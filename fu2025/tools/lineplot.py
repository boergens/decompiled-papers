"""Helpers for digitizing the multi-colour line plots of fu2025 (Figs. 7 and 8), written for this paper.

Pixels are classified by colour: a line pixel is a blend of its series colour c with the white
background w (anti-aliasing, JPEG blur), p = w + t (c - w) with 0 < t <= 1. For each reference colour
the best t is found by projection and the pixel goes to the reference with the smallest residual,
if that residual is below max_res and t >= t_min. Then each series is traced column by column,
following the run of mask pixels that continues the previous column's run.
"""
import numpy as np


def classify(a, refs, max_res=60.0, t_min=0.45, blue_split=None, black_navy=None):
    """a: RGB uint8 image; refs: list of RGB tuples. Returns int array: index into refs, or -1.

    blue_split = (i_blue, i_navy, b_min): JPEG darkens the edges of a pure blue line to about (0, 0, 185),
    which the blend model puts nearer navy (0, 0, 128). Pixels given to either of the two whose red and
    green are both below 60 are reassigned by their blue channel: > b_min -> blue, else navy.
    black_navy = (i_black, i_navy, d): pixels given to black whose blue channel exceeds max(red, green) by more
    than d are dark edges of a navy line (JPEG) and go to navy."""
    p = a.astype(float)
    w = np.array([255.0, 255.0, 255.0])
    best = np.full(a.shape[:2], -1, int)
    best_res = np.full(a.shape[:2], np.inf)
    for i, c in enumerate(refs):
        d = np.array(c, float) - w
        t = ((p - w) @ d) / (d @ d)
        t = np.clip(t, 0, 1)
        res = np.sqrt((((w + t[..., None] * d) - p) ** 2).sum(2))
        ok = (t >= t_min) & (res < best_res) & (res <= max_res)
        best[ok] = i
        best_res[ok] = res[ok]
    if blue_split is not None:
        ib, inv, bmin = blue_split
        sel = ((best == ib) | (best == inv)) & (a[..., 0] < 60) & (a[..., 1] < 60)
        best[sel & (a[..., 2] > bmin)] = ib
        best[sel & (a[..., 2] <= bmin)] = inv
    if black_navy is not None:
        ik, inv, dd = black_navy
        ai = a.astype(int)
        best[(best == ik) & (ai[..., 2] - np.maximum(ai[..., 0], ai[..., 1]) > dd)] = inv
    return best


def runs_of(rows, gap=2):
    if len(rows) == 0:
        return []
    return np.split(rows, np.where(np.diff(rows) > gap)[0] + 1)


def trace_follow(mask, x0, x1, y0, y1, start_hint=None, max_jump=40):
    """Follow one line through the mask, column by column.

    Returns a list of (col, y_centre, y_top, y_bottom) in pixel units for the columns where the
    series is visible; columns where it is hidden (drawn over by another series) are skipped.
    The run chosen in each column is the one closest to the previous run (interval distance);
    a run more than max_jump px away from the previous one is not accepted (a stray pixel group).
    """
    out = []
    prev = start_hint  # (top, bottom)
    misses = 0
    for c in range(x0, x1):
        rows = np.where(mask[y0:y1, c])[0] + y0
        rs = runs_of(rows)
        rs = [r for r in rs if len(r) >= 1]
        if not rs:
            misses += 1
            continue
        if prev is None:
            r = max(rs, key=len)
        else:
            def dist(r):
                lo, hi = r[0], r[-1]
                if hi < prev[0]:
                    return prev[0] - hi
                if lo > prev[1]:
                    return lo - prev[1]
                return 0
            r = min(rs, key=dist)
            if dist(r) > max_jump + 4 * misses:
                misses += 1
                continue
        misses = 0
        out.append((c, float(r.mean()), float(r[0]), float(r[-1])))
        prev = (r[0], r[-1])
    return out


def overlay_series(a, series, out_png, box=None, fade=0.75):
    """Check image: the source faded towards white, with each traced series drawn on it as 1-px dots in its
    own colour (top and bottom of the run as a vertical stroke). series: list of (colour, [(c, ym, yt, yb)]).
    box = (x0, y0, x1, y1) crops the result."""
    from PIL import Image
    im = (a.astype(float) * (1 - fade) + 255 * fade).astype(np.uint8)
    for colour, tr in series:
        for c, ym, yt, yb in tr:
            im[int(round(yt)):int(round(yb)) + 1, int(c)] = colour
    if box is not None:
        x0, y0, x1, y1 = box
        im = im[y0:y1, x0:x1]
    Image.fromarray(im).save(out_png)


def overlay_grid(a, series, out_png, box, ncols=3, mark=(255, 140, 0)):
    """One tile per series: the source (unfaded) cropped to box, with that series' traced centre points
    marked in orange (3 x 1 px each), so one can see whether every mark sits on a line of the right colour."""
    from PIL import Image
    x0, y0, x1, y1 = box
    tiles = []
    for colour, tr in series:
        im = a.copy()
        for c, ym, yt, yb in tr:
            r = int(round(ym))
            im[r - 1:r + 2, int(c)] = mark
        tiles.append(im[y0:y1, x0:x1])
    h, w = tiles[0].shape[:2]
    nrows = (len(tiles) + ncols - 1) // ncols
    out = np.full((nrows * (h + 6), ncols * (w + 6), 3), 255, np.uint8)
    for k, t in enumerate(tiles):
        r, c = divmod(k, ncols)
        out[r * (h + 6):r * (h + 6) + h, c * (w + 6):c * (w + 6) + w] = t
    Image.fromarray(out).save(out_png)


def trace_all(mask, x0, x1, y0, y1, min_area=12, core=None, min_core=10):
    """All runs of one series' mask, column by column, after dropping connected components (8-connected)
    smaller than min_area px (specks: anti-aliased edges of other colours, JPEG noise).

    Returns a list of (col, y_centre, y_top, y_bottom); a column can have several runs (the line passing
    a column more than once, steep spikes next to a flat part, or a stray piece of another series)."""
    import cv2
    sub = np.zeros_like(mask, dtype=np.uint8)
    sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    n, lab, stats, _ = cv2.connectedComponentsWithStats(sub, connectivity=8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= min_area
    if core is not None:
        er = cv2.erode(sub, np.ones((core, core), np.uint8))
        ncore = np.bincount(lab[er > 0], minlength=n)
        keep &= ncore >= min_core
    m = keep[lab]
    out = []
    for c in range(x0, x1):
        rows = np.where(m[:, c])[0]
        for r in runs_of(rows):
            out.append((c, float(r.mean()), float(r[0]), float(r[-1])))
    return out
