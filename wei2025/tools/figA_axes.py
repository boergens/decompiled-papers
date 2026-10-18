"""Axis helpers for wei2025 Figs. 3 and 6 (Origin plots embedded as 300 ppi rasters). Fork A.

Frame lines are 2-3 px wide; major ticks (~10 px) and minor ticks (~5 px) point inward.
"""
import numpy as np


def _groups(idx):
    out = []
    for i in idx:
        if out and i <= out[-1][-1] + 1:
            out[-1].append(i)
        else:
            out.append([i])
    return out


def refine_frame(dark, box, search=6, min_frac=0.85):
    """box = approximate (left, right, top, bottom) frame-line pixel positions.
    Returns the centre of each frame line, found as the rows/cols near the guess whose
    dark fraction over the box span is >= min_frac."""
    L, R, T, B = box
    res = []
    for pos, axis in ((L, "v"), (R, "v"), (T, "h"), (B, "h")):
        cand = []
        n = dark.shape[1] if axis == "v" else dark.shape[0]
        for p in range(max(0, pos - search), min(n, pos + search + 1)):
            if axis == "v":
                frac = dark[T + 10:B - 10, p].mean()
            else:
                frac = dark[p, L + 10:R - 10].mean()
            if frac >= min_frac:
                cand.append(p)
        if not cand:
            raise ValueError(f'no frame line near {pos}')
        g = max(_groups(cand), key=len)
        res.append(float(np.mean(g)))
    return tuple(res)


def ticks(dark, frame, which, lo=3, hi=14, frac=0.8):
    """Inward ticks on one frame side. which: 'bottom' or 'left'.
    Returns list of (centre_position, length_px). A tick is a column (row) where the
    pixels from the frame line inward are dark for >= lo px."""
    L, R, T, B = [int(round(v)) for v in frame]
    out = []
    if which == 'bottom':
        start = B - 2
        cols = range(L + 4, R - 3)
        lens = []
        for c in cols:
            n = 0
            while n < hi + 5 and dark[start - n, c]:
                n += 1
            lens.append(n)
        lens = np.array(lens)
        idx = [c for c, n in zip(cols, lens) if lo <= n <= hi]
        for g in _groups(idx):
            if len(g) > 6:
                continue
            ln = max(lens[i - (L + 4)] for i in g)
            out.append((float(np.mean(g)), int(ln)))
    else:
        start = L + 2
        rows = range(T + 4, B - 3)
        lens = []
        for r in rows:
            n = 0
            while n < hi + 5 and dark[r, start + n]:
                n += 1
            lens.append(n)
        lens = np.array(lens)
        idx = [r for r, n in zip(rows, lens) if lo <= n <= hi]
        for g in _groups(idx):
            if len(g) > 6:
                continue
            ln = max(lens[i - (T + 4)] for i in g)
            out.append((float(np.mean(g)), int(ln)))
    return out


def fit(pix, val):
    pix = np.asarray(pix, float)
    val = np.asarray(val, float)
    A = np.vstack([pix, np.ones_like(pix)]).T
    (m, b), *_ = np.linalg.lstsq(A, val, rcond=None)
    res = float(np.max(np.abs(A @ [m, b] - val)))
    return m, b, res
