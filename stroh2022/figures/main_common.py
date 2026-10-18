"""Helpers for digitizing the raster plots of Ströh et al. 2022 (Figures 1 and 2 of the PDF, figure-supplement JPEGs).

The plots have an L-shaped frame (left and bottom spines) with ticks pointing outward. Tick labels are read by eye
from the image (they are given in each *_extract.py); the pixel positions of spines and tick marks are found here.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))
from digitize_common import embedded_image, fit_axis, write_csv, overlay  # noqa: E402,F401

PDF = os.path.join(HERE, "../source/elife-72147-v2.pdf")
SUPP = os.path.join(HERE, "../source/elife_figure_supplements")
WORK = os.path.join(HERE, "../work")


def fig_image(n):
    """Embedded raster of main Figure n (page 3 / page 7)."""
    return embedded_image(PDF, {1: 3, 2: 7}[n])


def supp_image(name):
    return np.array(Image.open(os.path.join(SUPP, name)).convert("RGB"))


def dark_mask(a, thr=100, sat=40):
    ai = a.astype(int)
    return (ai.mean(2) < thr) & ((ai.max(2) - ai.min(2)) < sat)


def runs(idx):
    g = []
    for i in idx:
        if g and i <= g[-1][-1] + 1:
            g[-1].append(i)
        else:
            g.append([i])
    return g


def vspine(dark, r0, r1, c0, c1):
    """Column (centre) of the longest dark vertical line inside the window, and its row extent."""
    best = None
    for c in range(c0, c1):
        col = dark[r0:r1, c]
        rr = runs(np.where(col)[0])
        if rr:
            L = max(rr, key=len)
            if best is None or len(L) > best[1]:
                best = (c, len(L), r0 + L[0], r0 + L[-1])
    # spine may be 2-3 px thick: centre of adjacent columns with near-equal run length
    cols = [c for c in range(best[0] - 3, best[0] + 4) if dark[best[2]:best[3], c].mean() > 0.9]
    return float(np.mean(cols)), best[2], best[3]


def hspine(dark, r0, r1, c0, c1):
    """Row (centre) of the longest dark horizontal line inside the window, and its column extent."""
    c, a0, a1 = vspine(dark.T, c0, c1, r0, r1)
    return c, a0, a1


def ticks_left(dark, col, r0, r1, L=4):
    """Rows of tick marks sticking out to the left of a vertical spine centred at column col."""
    c = int(np.ceil(col))
    while dark[r0:r1, c - 1].mean() > 0.5:
        c -= 1                      # c = left edge of the spine
    band = dark[r0:r1, c - L:c]
    rows = np.where(band.mean(1) > 0.8)[0] + r0
    return [float(np.mean(g)) for g in runs(rows)]


def ticks_below(dark, row, c0, c1, L=4):
    """Columns of tick marks sticking out below a horizontal spine centred at row."""
    r = int(np.floor(row))
    while dark[r + 1, c0:c1].mean() > 0.5:
        r += 1                      # r = bottom edge of the spine
    band = dark[r + 1:r + 1 + L, c0:c1]
    cols = np.where(band.mean(0) > 0.8)[0] + c0
    return [float(np.mean(g)) for g in runs(cols)]


def colour_mask(a, rgb, tol=40):
    ai = a.astype(int)
    return np.sqrt(((ai - np.array(rgb)) ** 2).sum(2)) < tol


def column_trace(mask, c0, c1, r0, r1, prev=None, maxjump=None):
    """Per column: (col, mid, top, bottom) of the run of mask pixels (closest to the previous column's value)."""
    out = []
    since = 1
    for c in range(c0, c1):
        r = np.where(mask[r0:r1, c])[0]
        if len(r) == 0:
            out.append((c, np.nan, np.nan, np.nan))
            since += 1
            continue
        rr = [np.array(g) for g in runs(r)]
        if prev is None:
            run = max(rr, key=len)
        else:
            run = min(rr, key=lambda q: 0 if q[0] <= prev - r0 <= q[-1] else min(abs(q[0] - (prev - r0)), abs(q[-1] - (prev - r0))))
        mid = r0 + (run[0] + run[-1]) / 2
        if maxjump is not None and prev is not None and abs(mid - prev) > maxjump * since:
            out.append((c, np.nan, np.nan, np.nan))
            since += 1
            continue
        prev = mid
        since = 1
        out.append((c, mid, r0 + run[0], r0 + run[-1]))
    return np.array(out, float)


def save_overlay(a, pts_by_colour, name, crop=None):
    im = a.copy()
    for colour, pts in pts_by_colour:
        for x, y in pts:
            if x == x and y == y:
                xi, yi = int(round(x)), int(round(y))
                if 0 <= yi < im.shape[0] and 0 <= xi < im.shape[1]:
                    im[yi, xi] = colour
    if crop:
        r0, r1, c0, c1 = crop
        im = im[r0:r1, c0:c1]
    os.makedirs(WORK, exist_ok=True)
    Image.fromarray(im).save(os.path.join(WORK, name))


def save_crop(a, crop, path):
    r0, r1, c0, c1 = crop
    Image.fromarray(a[r0:r1, c0:c1]).save(path)


def band_masks(a, bands, alpha=0.4, tol=30, lines=None, line_tol=60):
    """Membership masks of translucent s.d. bands that overlap each other.

    bands: {name: RGB of that band alone over white}. A band drawn over existing colour P gives
    B + (1 - alpha) * (P - 255). All stacking orders of up to 3 bands are generated; each pixel is assigned to the
    nearest generated colour (within tol, summed |dRGB|) and so to the set of bands covering it. Pixels of the
    solid mean lines (lines: {name: RGB}) count as inside their own band (the line is drawn on top of it).
    """
    import itertools
    names = list(bands)
    combos = []
    for k in (1, 2, 3):
        for perm in itertools.permutations(names, k):
            col = np.full(3, 255.0)
            for n in perm:
                col = np.array(bands[n], float) + (1 - alpha) * (col - 255)
            combos.append((set(perm), col))
    ai = a.astype(float)
    best = np.full(a.shape[:2], np.inf)
    lab = np.full(a.shape[:2], -1)
    for i, (s, col) in enumerate(combos):
        d = np.abs(ai - col).sum(2)
        upd = d < best
        best[upd] = d[upd]
        lab[upd] = i
    out = {n: np.zeros(a.shape[:2], bool) for n in names}
    ok = best < tol
    for i, (s, col) in enumerate(combos):
        m = ok & (lab == i)
        for n in s:
            out[n] |= m
    if lines:
        for n, rgb in lines.items():
            out[n] |= np.abs(ai - np.array(rgb, float)).sum(2) < line_tol
    return out


def band_trace(mask, mid, c0, r0, r1, passable=None):
    """For each column (aligned with the mean-line trace mid[:,0]) the run of band pixels containing the mean line:
    returns arrays (top, bottom) in pixel rows (NaN where the line is missing)."""
    top, bot = [], []
    for c, m in zip(mid[:, 0].astype(int), mid[:, 1]):
        if m != m:
            top.append(np.nan); bot.append(np.nan); continue
        col = mask[r0:r1, c] | (passable[r0:r1, c] if passable is not None else False)
        i = int(round(m)) - r0
        i = min(max(i, 0), len(col) - 1)
        if not col[i]:
            top.append(np.nan); bot.append(np.nan); continue
        G = 4   # bridge gaps of up to G px (anti-aliased line edges)
        u = i
        while u > 0 and col[max(0, u - G):u].any():
            u -= 1
            while not col[u]:
                u -= 1
        d = i
        while d < len(col) - 1 and col[d + 1:d + 1 + G].any():
            d += 1
            while not col[d]:
                d += 1
        top.append(r0 + u); bot.append(r0 + d)
    return np.array(top, float), np.array(bot, float)


def lineband(a, W, fx, fy, lines, bands=None, alpha=0.4, line_tol=45, black=None, c_from=None, c_to=None,
             band_tol=30, maxjump=25):
    """Trace solid mean lines (colour masks) and, optionally, their translucent s.d. bands and a black (dashed) line.

    W = (r0, r1, c0, c1): plot area in image pixels (inside the spines). fx, fy: pixel -> data maps.
    Returns rows (series, x, y, band_low, band_high) in data units and overlay points per series.
    """
    r0, r1, c0, c1 = W
    c_from = c0 if c_from is None else c_from
    c_to = c1 if c_to is None else c_to
    bm = {}
    if bands:   # compute on the plot window only (speed), then place into full-size masks
        sub = band_masks(a[r0:r1, c0:c1], bands, alpha=alpha, tol=band_tol, lines=lines)
        for n, m in sub.items():
            full = np.zeros(a.shape[:2], bool)
            full[r0:r1, c0:c1] = m
            bm[n] = full
    rows, ov = [], []
    passable = dark_mask(a, thr=70, sat=30)
    for rgb in lines.values():
        passable |= colour_mask(a, rgb, line_tol)
    for name, rgb in lines.items():
        m = colour_mask(a, rgb, line_tol)
        tr = column_trace(m, c_from, c_to, r0, r1, maxjump=maxjump)
        if name in bm:
            ok = np.isfinite(tr[:, 1])
            ti = tr.copy()   # mean line interpolated across short gaps (hidden under other lines), for the band only
            ti[:, 1] = np.interp(tr[:, 0], tr[ok, 0], tr[ok, 1])
            ti[(tr[:, 0] < tr[ok, 0].min()) | (tr[:, 0] > tr[ok, 0].max()), 1] = np.nan
            top, bot = band_trace(bm[name], ti, c0, r0, r1, passable)
            top, bot = despike(top), despike(bot)
        else:
            top = bot = np.full(len(tr), np.nan)
        for (c, mid, t, b), bt, bb in zip(tr, top, bot):
            if mid == mid or bt == bt or bb == bb:
                # y axes point up: the bottom pixel of the band is its low value
                lo = float(fy(bb)) if bb == bb else ""
                hi = float(fy(bt)) if bt == bt else ""
                rows.append((name, float(fx(c)), float(fy(mid)) if mid == mid else "", lo, hi))
        ov.append((tuple(255 - np.array(rgb)), [(c, mid) for c, mid, t, b in tr]))
        ov.append(((255, 0, 255), [(c, t) for c, t in zip(tr[:, 0], top)] + [(c, b) for c, b in zip(tr[:, 0], bot)]))
    if black:
        name = black
        m = dark_mask(a, thr=70, sat=30)
        tr = column_trace(m, c_from, c_to, r0, r1, maxjump=maxjump)
        for c, mid, t, b in tr:
            if mid == mid:
                rows.append((name, float(fx(c)), float(fy(mid)), "", ""))
        ov.append(((0, 255, 0), [(c, mid) for c, mid, t, b in tr]))
    return rows, ov


def despike(v, half=4, tol=12):
    """Set to NaN the values that differ by more than tol px from the median of their +-half neighbours
    (single-column failures of the band-edge walk)."""
    v = np.asarray(v, float).copy()
    out = v.copy()
    for i in range(len(v)):
        w = v[max(0, i - half):i + half + 1]
        w = w[np.isfinite(w)]
        if len(w) >= 3 and np.isfinite(v[i]) and abs(v[i] - np.median(w)) > tol:
            out[i] = np.nan
    return out


def map_grid(a, box, bar, bar_ticks, out_csv, header, xlim=(0, 1200), ylim=(0, 1200), max_dist=40):
    """Read a colour map through its colour bar.

    box = (r0, r1, c0, c1) of the map image (inclusive pixel rows/cols, x left->right = xlim, y bottom->top = ylim,
    i.e. the image edges are the axis limits); bar = (r0, r1, c0, c1) of the colour-bar interior;
    bar_ticks = [(row, value), ...] (>= 2) for the colour-bar calibration. Writes a grid CSV: one row per pixel row
    (y value of the pixel centre, top first), one column per pixel column (x of the pixel centre).
    """
    r0, r1, c0, c1 = box
    br0, br1, bc0, bc1 = bar
    rows_ = np.arange(br0, br1 + 1)
    barcol = a[br0:br1 + 1, bc0:bc1 + 1].astype(float).mean(1)
    (tr, tv) = zip(*bar_ticks)
    m, b = np.polyfit(tr, tv, 1)
    barval = m * rows_ + b
    img = a[r0:r1 + 1, c0:c1 + 1].astype(float)
    val = np.empty(img.shape[:2]); dist = np.empty(img.shape[:2])
    for i in range(img.shape[0]):
        dd = ((img[i][:, None, :] - barcol[None, :, :]) ** 2).sum(2)
        val[i] = barval[dd.argmin(1)]
        dist[i] = np.sqrt(dd.min(1))
    val[dist > max_dist] = np.nan
    nx, ny = c1 - c0 + 1, r1 - r0 + 1
    xs = xlim[0] + (np.arange(nx) + 0.5) * (xlim[1] - xlim[0]) / nx
    ys = ylim[1] - (np.arange(ny) + 0.5) * (ylim[1] - ylim[0]) / ny
    with open(out_csv, "w") as f:
        for h in header:
            f.write("# " + h + "\n")
        f.write(f"# Colour bar: rows {br0}-{br1} of the source image, value = {m:.6g} * row + {b:.6g}; one bar row ="
                f" {abs(m):.4g} units (the bar is drawn in discrete bands, so values are quantized). Median colour"
                f" distance to the bar {np.nanmedian(dist):.1f} (RGB units); pixels farther than {max_dist} are empty.\n")
        f.write("y," + ",".join(f"{x:.2f}" for x in xs) + "\n")
        for y, row in zip(ys, val):
            f.write(f"{y:.2f}," + ",".join("" if v != v else f"{v:.4g}" for v in row) + "\n")
    return val, m, b


def track(mask, seed_c, seed_r, c0, c1, r0, r1, maxjump=12):
    """Follow one curve of a mask that holds several (e.g. three dashed model curves) from a seed point, to the left
    and to the right, taking in each column the run closest to the previous position. Returns column_trace rows."""
    right = column_trace(mask, int(seed_c), c1, r0, r1, prev=seed_r, maxjump=maxjump)
    left = column_trace(mask[:, ::-1], mask.shape[1] - int(seed_c), mask.shape[1] - c0, r0, r1, prev=seed_r,
                        maxjump=maxjump)
    left[:, 0] = mask.shape[1] - 1 - left[:, 0]
    out = np.vstack([left[::-1], right])
    return out[np.argsort(out[:, 0], kind="stable")]


def track_extrap(mask, seed_c, seed_r, c0, c1, r0, r1, tol=7, fit_len=25):
    """Follow a dashed curve from a seed point in both directions. In each column the predicted row is extrapolated
    linearly from the accepted points of the last fit_len columns; the mask run closest to the prediction is
    accepted if it lies within tol px (+1 px per column since the last accepted point). Returns column_trace rows."""
    out = {}
    for direction in (+1, -1):
        pts = [(seed_c, seed_r)]
        c = seed_c + direction
        while c0 <= c < c1:
            near = [p for p in pts if abs(p[0] - c) <= fit_len]
            if len(near) >= 3:
                k, b = np.polyfit([p[0] for p in near], [p[1] for p in near], 1)
                pred = k * c + b
            else:
                pred = pts[-1][1]
            gap = abs(c - pts[-1][0])
            r = np.where(mask[r0:r1, c])[0]
            if len(r):
                rr = [np.array(g) + r0 for g in runs(r)]
                best = min(rr, key=lambda q: 0 if q[0] <= pred <= q[-1] else min(abs(q[0] - pred), abs(q[-1] - pred)))
                dist = 0 if best[0] <= pred <= best[-1] else min(abs(best[0] - pred), abs(best[-1] - pred))
                if dist <= tol + gap and len(best) < 40:
                    mid = (best[0] + best[-1]) / 2
                    if best[-1] - best[0] > 12:      # a long run (steep part, or two curves touching): use the prediction
                        mid = float(np.clip(pred, best[0], best[-1]))
                    pts.append((c, mid))
                    out[c] = (c, mid, best[0], best[-1])
            if gap > 60:
                break
            c += direction
    out[seed_c] = (seed_c, seed_r, seed_r, seed_r)
    return np.array([out[c] for c in sorted(out)], float)
