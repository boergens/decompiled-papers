"""Helpers for the sectioning-event histograms of Extended Data Figs. 3d and 4d (hildebrand2017).

The histograms are raster images (150 ppi) with ~1 pixel column per 50-section bin, so single bins
cannot always be separated: the main histograms are read per pixel column (height of the grey bar run
above the axis line), the insets (5-section bins, ~2.3 px each) per bar.
"""
import numpy as np


def ink_rows(gcol, start, thr):
    """Number of contiguous pixels with grey value < thr going up from row `start`."""
    n, r = 0, start
    while r >= 0 and gcol[r] < thr:
        n += 1
        r -= 1
    return n


def column_heights(g, first_row_above_axis, c0, c1, thr=215, skip=0):
    """Bar height in pixels for each column c0..c1-1 (contiguous grey run from the axis upward).

    skip: rows directly above the axis that are anti-aliasing of the axis line on every column;
    they are skipped and added back to non-empty columns.
    """
    out = []
    for c in range(c0, c1):
        n = ink_rows(g[:, c], first_row_above_axis - skip, thr)
        out.append(n + skip if n > 0 else 0)
    return np.array(out)


def group_bars(h, c0):
    """Group consecutive non-zero columns into bars: list of (first_col, last_col, max_height_px)."""
    bars, cur = [], None
    for i, v in enumerate(h):
        c = c0 + i
        if v > 0:
            if cur and c == cur[1] + 1:
                cur = [cur[0], c, max(cur[2], v)]
            else:
                if cur:
                    bars.append(tuple(cur))
                cur = [c, c, v]
        elif cur:
            bars.append(tuple(cur))
            cur = None
    if cur:
        bars.append(tuple(cur))
    return bars


def tick_centres(profile, thr):
    """Centres (intensity-weighted) of runs where profile > thr."""
    idx = np.where(profile > thr)[0]
    if not len(idx):
        return []
    groups = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    return [float((gr * profile[gr]).sum() / profile[gr].sum()) for gr in groups]
