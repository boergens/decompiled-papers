"""Marker finder for the Origin-style scatter+dashed-line panels of wei2024 Figs. 12 and 15 (fork F3).

The plots are 300 ppi JPEGs. Each series is one colour; its markers (open squares, filled circles,
open triangles, open diamonds, ...; ~7 px) are joined by dashed lines ~2-3 px thick. Method:
  1. colour mask of the series inside the plot frame (legend/title boxes blanked);
  2. fill holes (open markers become solid), then a morphological opening with a k x k square,
     which removes the thin dashes and keeps the markers;
  3. connected components of the opened mask -> marker candidates; centre = bbox centre of the
     component plus a per-shape vertical offset measured on the legend marker (whose dashed line
     is horizontal, so its ink bbox centre is the true symbol centre);
  4. when a series has a known count of markers per x step, candidates are matched to the
     expected x grid (only to flag gaps/duplicates; the reported x is the measured one).
"""
import numpy as np
from scipy import ndimage as ndi

COLOURS = {
    "black": lambda a: (a.max(2) < 135) & (np.ptp(a, axis=2) < 45),
    "red": lambda a: (a[..., 0] > 170) & (a[..., 1] < 150) & (a[..., 2] < 150) & (np.abs(a[..., 1] - a[..., 2]) < 45),
    "magenta": lambda a: (a[..., 0] > 170) & (a[..., 2] > 150) & (a[..., 1] < 150),
    "green": lambda a: (a[..., 1] > 150) & (a[..., 0] < 150) & (a[..., 2] < 150),
    "blue": lambda a: (a[..., 2] > 150) & (a[..., 0] < 120) & (a[..., 1] < 150),
    "orange": lambda a: (a[..., 0] > 200) & (a[..., 1] > 90) & (a[..., 1] < 200) & (a[..., 2] < 110),
}


def fill_small(mask, max_area=80):
    """Fill only small holes (marker interiors), never large enclosed regions such as a blanked legend box."""
    filled = ndi.binary_fill_holes(mask)
    holes = filled & ~mask
    lab, n = ndi.label(holes)
    if n:
        sizes = ndi.sum(holes, lab, index=np.arange(1, n + 1))
        big = np.isin(lab, np.where(sizes > max_area)[0] + 1)
        filled &= ~big
    return filled


def series_mask(a, colour, box, blank=()):
    """Colour mask restricted to box (x0,y0,x1,y1, exclusive end); blank = list of boxes set False."""
    m = COLOURS[colour](a.astype(int))
    out = np.zeros_like(m)
    x0, y0, x1, y1 = box
    out[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    for bx0, by0, bx1, by1 in blank:
        out[by0:by1, bx0:bx1] = False
    return out


def markers(mask, k=4, min_area=6, fill=True):
    """Marker candidates: list of (xc, yc, area, (x0,y0,x1,y1)) from the opened, hole-filled mask."""
    m = ndi.binary_fill_holes(mask) if fill else mask
    m = ndi.binary_closing(m, np.ones((2, 2))) if fill else m
    m = ndi.binary_fill_holes(m) if fill else m
    o = ndi.binary_opening(m, np.ones((k, k)))
    lab, n = ndi.label(o)
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        area = int((lab[sl] == i).sum())
        if area < min_area:
            continue
        y0, y1 = sl[0].start, sl[0].stop - 1
        x0, x1 = sl[1].start, sl[1].stop - 1
        out.append(((x0 + x1) / 2, (y0 + y1) / 2, area, (x0, y0, x1, y1)))
    return out


def legend_offset(mask_full, box, k=4):
    """Vertical offset (true centre - opened-bbox centre) and widths from a legend marker in box.

    box should contain the legend marker and its horizontal dashed line. The true centre row is
    the middle of the ink rows in the columns of the marker (the line is horizontal through it).
    """
    x0, y0, x1, y1 = box
    sub = np.zeros_like(mask_full)
    sub[y0:y1, x0:x1] = mask_full[y0:y1, x0:x1]
    c = markers(sub, k=k)
    if not c:
        return 0.0, None
    c = max(c, key=lambda t: t[2])
    bx0, by0, bx1, by1 = c[3]
    cols = sub[:, bx0:bx1 + 1]
    rows = np.where(cols.any(1))[0]
    true_c = (rows.min() + rows.max()) / 2
    return true_c - c[1], (c, rows.min(), rows.max())


def split_wide(cands, max_w=11):
    """Components wider than max_w px (two touching markers) are split into equal parts."""
    out = []
    for xc, yc, area, (x0, y0, x1, y1) in cands:
        w = x1 - x0 + 1
        if w > max_w:
            n = int(round(w / 8.0))
            n = max(n, 2)
            for j in range(n):
                sx0 = x0 + j * w / n
                sx1 = x0 + (j + 1) * w / n - 1
                out.append(((sx0 + sx1) / 2, yc, area / n, (sx0, y0, sx1, y1), "split"))
        else:
            out.append((xc, yc, area, (x0, y0, x1, y1), ""))
    return out


def grid_markers(mask, xcols, k=3, tol=6, prev_y=None):
    """For each expected marker column in xcols, pick the marker candidate within +-tol px.

    Returns list of (xcol_expected, xc, yc, flag). Candidates come from markers(mask, k); several
    in the window -> the one with the largest area (flag 'multi'); none -> retry with k-1
    (flag 'weak'); still none -> NaN (flag 'missing').
    """
    cands = {kk: markers(mask, k=kk) for kk in (k, k - 1)}
    out = []
    for xe in xcols:
        got = None
        for kk, fl in ((k, ""), (k - 1, "weak")):
            near = [c for c in cands[kk] if abs(c[0] - xe) <= tol]
            if near:
                # prefer compact (square-ish) and large components
                def score(c):
                    x0, y0, x1, y1 = c[3]
                    w, h = x1 - x0 + 1, y1 - y0 + 1
                    return c[2] - 3 * abs(w - h) - 2 * abs(c[0] - xe)
                c = max(near, key=score)
                f = fl
                if len(near) > 1:
                    f = (f + ";multi").strip(";")
                got = (xe, c[0], c[1], f, c[3])
                break
        if got is None:
            got = (xe, np.nan, np.nan, "missing", None)
        out.append(got)
    return out


def legend_template(mask, box):
    """Template from a legend marker: hole-filled ink of the marker inside box (x0,y0,x1,y1).

    The legend's dashed line runs horizontally through the symbol centre. The marker's columns
    are the run of columns (nearest the box centre) with ink outside the line band; the template's
    true centre is (middle of those columns, middle of the line band) relative to its top-left.
    Returns (T float array, (cx, cy) centre in template coordinates, top-left in image).
    """
    x0, y0, x1, y1 = box
    m = ndi.binary_fill_holes(ndi.binary_closing(mask[y0:y1, x0:x1], np.ones((3, 3))))
    rows_all = m.sum(1)
    band = np.where(rows_all >= 0.5 * rows_all.max())[0]
    band = band[np.abs(band - np.argmax(rows_all)) <= 3]
    ly0, ly1 = band.min(), band.max()
    off = m.copy()
    off[ly0:ly1 + 1] = False
    cols = np.where(off.any(0))[0]
    runs = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
    run = min(runs, key=lambda q: abs(q.mean() - m.shape[1] / 2))
    cx0, cx1 = run.min(), run.max()
    rows = np.where(off[:, cx0:cx1 + 1].any(1))[0]
    ry0, ry1 = min(rows.min(), ly0), max(rows.max(), ly1)
    T = m[ry0:ry1 + 1, cx0:cx1 + 1].astype(np.float32)
    cx = (cx1 - cx0) / 2
    cy = (ly0 + ly1) / 2 - ry0
    return T, (cx, cy), (x0 + cx0, y0 + ry0)


_CACHE = {}


def match_grid(mask, T, centre, xcols, row_range, tol=6, min_score=0.6, track=None, close=3, ring=False, others=None):
    """Template-match the hole-filled series mask; for each expected column, best match within +-tol px.

    Returns rows (x_expected, xc, yc, score, flag). Centre of the match = top-left + centre.
    others: mask of ink of the other series (drawn on top or underneath); it counts half (0.5) in the
    coverage and is allowed to close an open marker's outline before hole filling, so a marker partly
    hidden by another series' marker still scores higher than a bare line.
    ring=True: among the local maxima whose coverage is within 0.1 of the column's best, take the one
    with the least series ink in a 2-px ring around the template (a marker is a compact blob; where
    two dashed-line arms meet they can fill the template too, but they continue through the ring).
    """
    import cv2
    key = (id(mask), id(others), T.tobytes(), T.shape, close, ring)
    if key in _CACHE:
        res, ores, rres, locmax = _CACHE[key]
    else:
        m = ndi.binary_closing(mask, np.ones((close, close))) if close else mask
        if others is not None:
            o = others & ~m
            own = fill_small(m)
            filled = fill_small(m | o)
            # own ink and holes closed by own ink count 1; other ink and holes closed only with its help count 0.5
            m = np.where(own, 1.0, np.where(o | filled, 0.5, 0.0)).astype(np.float32)
            ores = cv2.matchTemplate(o.astype(np.float32), T, cv2.TM_CCORR) / T.sum()
        else:
            ores = None
            m = fill_small(m).astype(np.float32)
        res = cv2.matchTemplate(m, T, cv2.TM_CCORR) / T.sum()
        rres = locmax = None
        if ring:
            Tp = np.pad(T, 2)
            R = (ndi.binary_dilation(Tp > 0, np.ones((5, 5))) & ~(Tp > 0)).astype(np.float32)
            rres = cv2.matchTemplate(np.pad(m, 2), R, cv2.TM_CCORR) / R.sum()
            rres = rres[:res.shape[0], :res.shape[1]]
            locmax = res >= ndi.maximum_filter(res, size=5) - 1e-6
        _CACHE[key] = (res, ores, rres, locmax)
    h, w = T.shape
    cx, cy = centre
    out = []
    r0, r1 = row_range
    for xe in xcols:
        c0 = int(round(xe - cx - tol))
        c1 = int(round(xe - cx + tol)) + 1
        rr0 = max(0, int(r0 - cy))
        rr1 = min(res.shape[0], int(r1 - cy) + 1)
        sub = res[rr0:rr1, c0:c1]
        if sub.size == 0:
            out.append((xe, np.nan, np.nan, 0.0, "missing"))
            continue
        best = sub.max()
        if ring:
            cand = np.argwhere(locmax[rr0:rr1, c0:c1] & (sub >= best - 0.1))
            rsub = rres[rr0:rr1, c0:c1]
            if len(cand) == 0:
                cand = [np.unravel_index(np.argmax(sub), sub.shape)]
            ar, ac = min(cand, key=lambda q: (round(float(rsub[q[0], q[1]]), 2), -sub[q[0], q[1]]))
            best = float(sub[ar, ac])
        else:
            ar, ac = np.unravel_index(np.argmax(sub), sub.shape)
        # plateau of the maximum, restricted to the connected patch around the chosen peak
        lab, _ = ndi.label(sub >= sub[ar, ac] - 0.03)
        rs, cs = np.where(lab == lab[ar, ac])
        r = rr0 + rs.mean()
        c = c0 + cs.mean()
        flag = "" if best >= min_score else "weak"
        if ores is not None:
            ofrac = float(ores[rr0 + ar, c0 + ac])
            if ofrac > 0.15:
                flag = (flag + f";other-series ink covers {ofrac:.0%} of the marker area").lstrip(";")
        out.append((xe, c + cx, r + cy, float(best), flag))
    return out


def find_legend_box(mask, search):
    """Locate a legend entry of one colour inside search box: (x0,y0,x1,y1) around its marker.

    The legend line is the row with most ink; the marker is the run of columns, within the line's
    horizontal extent, that has ink >= 3 px above or below the line band, nearest the line's middle.
    """
    x0, y0, x1, y1 = search
    m = mask[y0:y1, x0:x1]
    rows = m.sum(1)
    band = np.where(rows >= 0.75 * rows.max())[0]
    band = band[np.abs(band - np.argmax(rows)) <= 3]
    b0, b1 = band.min(), band.max()
    linecols = np.where(m[b0:b1 + 1].any(0))[0]
    lc0, lc1 = linecols.min(), linecols.max()
    # the line's extent: stop at the first gap > 12 px (the label text starts after a gap)
    gaps = np.where(np.diff(linecols) > 12)[0]
    if len(gaps):
        lc1 = linecols[gaps[0]]
    off = m[max(0, b0 - 6):max(0, b0 - 1)].any(0) | m[b1 + 2:b1 + 7].any(0)
    cols = np.where(off)[0]
    cols = cols[(cols >= lc0) & (cols <= lc1)]
    runs = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
    mid = (lc0 + lc1) / 2
    run = min(runs, key=lambda q: abs(q.mean() - mid))
    c = int(round(run.mean()))
    r = (b0 + b1) // 2
    return (x0 + c - 12, y0 + r - 9, x0 + c + 13, y0 + r + 10)


def calib(a, frame, xvals, yvals, tick_len=6, dark_thr=140):
    """Axis calibration from inward major ticks. frame = (L cols, R cols, T rows, B rows) as (first,last).
    Returns fx (px->x), fy (px->y), inverse for x, and a text line with tick pixels and residuals."""
    import digitize_common as dc
    d = a.astype(float).mean(2) < dark_thr
    L, R, T, B = frame
    # major ticks are longer than minor ones: raise the length until the count matches the labels
    for ln in range(tick_len, tick_len + 8):
        xt = dc.tick_positions(d, B, -1, ln, L[1] + 2, R[0] - 1)
        if len(xt) == len(xvals):
            break
    for ln in range(tick_len, tick_len + 8):
        yt = dc.tick_positions_v(d, L, +1, ln, T[1] + 2, B[0] - 1)
        if len(yt) == len(yvals):
            break
    if len(xt) != len(xvals):
        raise SystemExit(f"x ticks {xt} vs labels {xvals}")
    if len(yt) != len(yvals):
        raise SystemExit(f"y ticks {yt} vs labels {yvals}")
    fx, rx, mx = dc.fit_axis(xt, xvals)
    fy, ry, my = dc.fit_axis(yt, yvals)
    bx = fx(0.0)
    inv_x = lambda v: (np.asarray(v, float) - bx) / mx
    txt = (f"x ticks at px {[round(v, 1) for v in xt]} = {xvals}, max residual {rx:.3g}; "
           f"y ticks at px {[round(v, 1) for v in yt]} = {yvals}, max residual {ry:.3g}; "
           f"1 px = {abs(mx):.4g} (x), {abs(my):.4g} (y)")
    return fx, fy, inv_x, txt, abs(mx), abs(my)


def synth_template(shape, w=7, h=None):
    """Filled synthetic marker template and its data-point centre (cx, cy) in template coordinates.

    square/circle/diamond: centre of the box; up-triangle: centroid (2/3 of the height from the apex);
    down-triangle: centroid (1/3 from the top edge). Checked against the legend markers, whose dashed
    line passes through the symbol's data point (see work/f3_legend_check.txt).
    """
    h = h or w
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    cx0, cy0 = (w - 1) / 2, (h - 1) / 2
    if shape == "open square":
        T = np.ones((h, w), bool)
        c = (cx0, cy0)
    elif shape == "filled circle":
        T = ((xx - cx0) / (w / 2)) ** 2 + ((yy - cy0) / (h / 2)) ** 2 <= 1.0
        c = (cx0, cy0)
    elif shape == "open diamond":
        T = np.abs(xx - cx0) / (w / 2) + np.abs(yy - cy0) / (h / 2) <= 1.0
        c = (cx0, cy0)
    elif shape == "open up-triangle":
        # apex at row 0, base at row h-1
        T = np.abs(xx - cx0) <= (yy + 0.5) / h * (w / 2)
        c = (cx0, (h - 1) * 2 / 3)
    elif shape == "open down-triangle":
        T = np.abs(xx - cx0) <= (h - yy - 0.5) / h * (w / 2)
        c = (cx0, (h - 1) / 3)
    else:
        raise ValueError(shape)
    return T.astype(np.float32), c


def free_peaks(mask, T, centre, thr=0.75, r=3, close=3):
    """All local maxima of the template-match score >= thr (non-maximum suppression radius r px).
    Returns list of (xc, yc, score) in image pixels (template centre applied)."""
    import cv2
    m = ndi.binary_closing(mask, np.ones((close, close))) if close else mask
    m = ndi.binary_fill_holes(m).astype(np.float32)
    res = cv2.matchTemplate(m, T, cv2.TM_CCORR) / T.sum()
    mx = ndi.maximum_filter(res, size=2 * r + 1)
    pk = (res >= thr) & (res >= mx - 1e-6)
    lab, n = ndi.label(pk)
    out = []
    for sl in ndi.find_objects(lab):
        rs, cs = np.mgrid[sl[0], sl[1]]
        sel = pk[sl]
        r_, c_ = rs[sel].mean(), cs[sel].mean()
        out.append((c_ + centre[0], r_ + centre[1], float(res[int(round(r_)), int(round(c_))])))
    return out
