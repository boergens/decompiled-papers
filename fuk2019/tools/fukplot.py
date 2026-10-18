"""Helpers shared by the fuk2019 figure-extraction scripts (figures/*_extract.py).

Written for fuk2019 (all plots are Origin raster exports, 220-300 ppi, anti-aliased lines on
white). Builds on digitize_common.py (copied from the osmium decompile tools, unchanged).

- load(page, bbox): the embedded image nearest to bbox (PDF points) on that page, RGB uint8.
- classify(img, palette): per pixel, the palette colour it is a blend of (with white), or -1.
  An anti-aliased pixel p = a*c + (1-a)*white; for each colour c the best a in [0,1] is fitted
  and the residual taken; the pixel goes to the colour with the smallest residual when a is
  large enough. Separates e.g. navy (0,0,128) from blue (0,0,255) and black.
- inward_ticks_x / inward_ticks_y: centres of tick marks that point into the frame from an
  axis line (Origin's default); returns the columns/rows whose tick is at least `length` px.
- fit(pix, val): least-squares linear map, returns (f, max residual, slope).
"""
from pathlib import Path

import numpy as np

import digitize_common as dc

PDF = Path(__file__).resolve().parent.parent / "source" / "fuk2019.pdf"


def load(page, bbox):
    return dc.embedded_image(str(PDF), page, bbox_near=bbox)


def classify(img, palette, amin=0.45, maxres=60.0):
    """Label each pixel with the index of the palette colour it is a white-blend of, else -1."""
    p = img.astype(float)
    w = np.array([255.0, 255.0, 255.0])
    best = np.full(p.shape[:2], np.inf)
    lab = np.full(p.shape[:2], -1, int)
    alpha = np.zeros(p.shape[:2])
    for k, c in enumerate(palette):
        d = np.asarray(c, float) - w           # p - w = a * (c - w)
        nn = (d * d).sum()
        a = ((p - w) * d).sum(2) / nn
        a = np.clip(a, 0, 1)
        res = np.sqrt((((p - w) - a[..., None] * d) ** 2).sum(2))
        upd = (res < best) & (a >= amin)
        best[upd] = res[upd]
        lab[upd] = k
        alpha[upd] = a[upd]
    lab[best > maxres] = -1
    return lab, alpha


def _groups(idx):
    out = []
    for i in idx:
        if out and i == out[-1][-1] + 1:
            out[-1].append(i)
        else:
            out.append([i])
    return [float(np.mean(g)) for g in out]


def inward_ticks_x(dark, axis_row, direction, length, c0, c1, frac=0.99):
    """Columns in [c0,c1) where `length` px next to the axis row (direction -1: above) are dark."""
    if direction < 0:
        band = dark[axis_row - length:axis_row, c0:c1]
    else:
        band = dark[axis_row + 1:axis_row + 1 + length, c0:c1]
    return [c0 + g for g in _groups(np.where(band.mean(0) >= frac)[0])]


def inward_ticks_y(dark, axis_col, direction, length, r0, r1, frac=0.99):
    """Rows in [r0,r1) where `length` px next to the axis column (direction +1: right) are dark."""
    if direction > 0:
        band = dark[r0:r1, axis_col + 1:axis_col + 1 + length]
    else:
        band = dark[r0:r1, axis_col - length:axis_col]
    return [r0 + g for g in _groups(np.where(band.mean(1) >= frac)[0])]


def fit(pix, val):
    return dc.fit_axis(pix, val)


def components(mask, min_size=1):
    """Connected components (8-connectivity) of a bool mask: list of (rows, cols) arrays."""
    import cv2
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    out = []
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            r, c = np.where(lab == i)
            out.append((r, c))
    return out
