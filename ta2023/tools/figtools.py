"""Helpers for digitizing the raster line+marker plots of Ta, Tran & Righi 2023 (Langmuir).

All plots in this paper are 300 ppi RGB images (no vector paths). They are drawn in an Igor-Pro-like style:
a detached left (and sometimes right) axis line with outward major/minor ticks, a detached bottom axis
line with outward ticks, coloured filled markers (squares, triangles, circles) joined by smooth curves,
and structure insets in coloured boxes on top of the plot.

Functions:
  load(page, xref)                -> RGB uint8 array of the embedded image (soft mask applied)
  dark_mask(a, thr)               -> unsaturated dark pixels (axes, ticks, black series)
  vaxis(dark, x0, x1, y0, y1)     -> column range of the longest vertical dark line in the window
  haxis(dark, x0, x1, y0, y1)     -> row range of the longest horizontal dark line in the window
  ticks_v(dark, cols, side, ...)  -> tick rows (with their lengths) on a vertical axis line
  ticks_h(dark, rows, side, ...)  -> tick columns (with their lengths) on a horizontal axis line
  fit(pix, val)                   -> linear map pixel -> value, max residual, slope
  hue_mask(a, name)               -> colour mask for 'green', 'red', 'blue', 'black', ...
  markers(mask, k, amin, amax)    -> centroids of blobs that survive a k x k elliptic opening
  save_overlay(a, groups, path)   -> draw points (per-series colours) over the image
"""
from pathlib import Path

import cv2
import numpy as np
import pymupdf

KEY = Path(__file__).resolve().parent.parent
PDF = KEY / "source" / "ta2023.pdf"


def load(page, xref):
    doc = pymupdf.open(PDF)
    pix = pymupdf.Pixmap(doc, xref)
    if pix.n - pix.alpha != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()
    smask = doc.xref_get_key(xref, "SMask")
    if smask[0] == "xref":
        m = pymupdf.Pixmap(doc, int(smask[1].split()[0]))
        al = np.frombuffer(m.samples, np.uint8).reshape(m.height, m.width).astype(float) / 255
        a = (a * al[:, :, None] + 255 * (1 - al[:, :, None])).astype(np.uint8)
    assert any(i["xref"] == xref for i in doc[page - 1].get_image_info(xrefs=True))
    return a


def dark_mask(a, thr=120, maxsat=60):
    a = a.astype(int)
    return (a.mean(2) < thr) & ((a.max(2) - a.min(2)) < maxsat)


def _runs(idx):
    groups = []
    for i in idx:
        if groups and i <= groups[-1][-1] + 1:
            groups[-1].append(i)
        else:
            groups.append([i])
    return groups


def vaxis(dark, x0, x1, y0, y1):
    """Longest vertical dark run per column in the window; returns ((c_first, c_last), (r_top, r_bot))."""
    best = []
    for c in range(x0, x1):
        col = dark[y0:y1, c]
        rs = _runs(np.where(col)[0])
        L = max((len(r) for r in rs), default=0)
        best.append((L, c, rs))
    Lmax = max(b[0] for b in best)
    cols = [b[1] for b in best if b[0] >= 0.8 * Lmax]
    g = max(_runs(cols), key=len)
    rs = max([b for b in best if b[1] == g[len(g) // 2]][0][2], key=len)
    return (g[0], g[-1]), (y0 + rs[0], y0 + rs[-1])


def haxis(dark, x0, x1, y0, y1):
    """Longest horizontal dark run per row in the window; returns ((r_first, r_last), (c_left, c_right))."""
    (r0, r1), (c0, c1) = vaxis(dark.T, y0, y1, x0, x1)
    return (r0, r1), (c0, c1)


def ticks_v(dark, cols, side, y0, y1, maxlen=30, minlen=3):
    """Ticks on a vertical axis line occupying columns cols=(c0,c1). side=-1: ticks to the left.
    Returns list of (row_centre, length_px)."""
    c0, c1 = cols
    out = []
    lens = np.zeros(y1 - y0, int)
    for i, r in enumerate(range(y0, y1)):
        n = 0
        c = c0 - 1 if side < 0 else c1 + 1
        while n < maxlen and dark[r, c]:
            n += 1
            c += side
        lens[i] = n
    for g in _runs(np.where(lens >= minlen)[0]):
        out.append((y0 + float(np.mean(g)), int(np.max(lens[g]))))
    return out


def ticks_h(dark, rows, side, x0, x1, maxlen=30, minlen=3):
    """Ticks on a horizontal axis line occupying rows=(r0,r1). side=+1: ticks below."""
    return ticks_v(dark.transpose(), rows, side, x0, x1, maxlen, minlen)


def fit(pix, val):
    pix = np.asarray(pix, float)
    val = np.asarray(val, float)
    A = np.vstack([pix, np.ones_like(pix)]).T
    (m, b), *_ = np.linalg.lstsq(A, val, rcond=None)
    res = float(np.max(np.abs(A @ [m, b] - val)))
    return (lambda p: m * np.asarray(p, float) + b), res, m, (lambda v: (np.asarray(v, float) - b) / m)


def hue_mask(a, name):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    if name == "green":
        return (g > r + 60) & (g > b + 40)
    if name == "red":
        return (r > g + 60) & (r > b + 40)
    if name == "blue":
        return (b > r + 50) & (b > g + 50)
    if name == "black":
        return (a.mean(2) < 90) & ((a.max(2) - a.min(2)) < 50)
    raise ValueError(name)


def markers(mask, k, amin, amax, roi=None):
    """Blobs of mask that survive an elliptic opening of size k (removes lines thinner than k).
    roi=(x0,y0,x1,y1) restricts the search. Returns list of (x, y, area, w, h) in image pixels."""
    m = mask.astype(np.uint8)
    if roi is not None:
        x0, y0, x1, y1 = roi
        z = np.zeros_like(m)
        z[y0:y1, x0:x1] = m[y0:y1, x0:x1]
        m = z
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    o = cv2.morphologyEx(m, cv2.MORPH_OPEN, ker)
    n, lab, st, cen = cv2.connectedComponentsWithStats(o, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if amin <= area <= amax:
            out.append((float(cen[i][0]), float(cen[i][1]), int(area), int(w), int(h)))
    return out


def save_overlay(a, groups, path, r=3):
    """groups: list of (points [(x,y),...], (R,G,B)). Draws a small ring of radius r around each point."""
    im = a.copy()
    for pts, col in groups:
        for x, y in pts:
            if x == x and y == y:
                cv2.circle(im, (int(round(x)), int(round(y))), r, tuple(int(c) for c in col), 1)
                cv2.drawMarker(im, (int(round(x)), int(round(y))), tuple(int(c) for c in col),
                               cv2.MARKER_CROSS, 2 * r + 4, 1)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    Image.fromarray(im).save(path)


def blobs(mask, k, roi=None, close=0):
    """Like markers(), but returns every blob after the opening as dicts with centroid, bbox and area.
    close>0 first closes the mask with a close x close square (fills the holes that the black dotted
    guide lines punch through the semi-transparent markers)."""
    m = mask.astype(np.uint8)
    if close:
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((close, close), np.uint8))
    if roi is not None:
        x0, y0, x1, y1 = roi
        z = np.zeros_like(m)
        z[y0:y1, x0:x1] = m[y0:y1, x0:x1]
        m = z
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    o = cv2.morphologyEx(m, cv2.MORPH_OPEN, ker)
    n, lab, st, cen = cv2.connectedComponentsWithStats(o, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, area = st[i]
        out.append(dict(cx=float(cen[i][0]), cy=float(cen[i][1]), x0=int(x), y0=int(y), w=int(w), h=int(h),
                        bx=x + (w - 1) / 2, by=y + (h - 1) / 2, area=int(area)))
    return out


def legend_offset(a, mask, k, roi):
    """Offset (line row - marker bbox-centre row) of the legend entry inside roi, and the marker size.
    The legend line passes through the plotted data position of the marker; the opened marker's bbox
    centre can differ from it (triangles lose their tips in the opening)."""
    x0, y0, x1, y1 = roi
    m = mask[y0:y1, x0:x1]
    lr = np.where(m[:, :6].any(1))[0]          # the line stub at the left end of the legend entry
    line_row = y0 + (lr[0] + lr[-1]) / 2
    b = max(blobs(mask, k, roi), key=lambda d: d["area"])
    return line_row - b["by"], (b["w"], b["h"]), line_row, b


def pick(bl, cx, tol, amin, prefer_y=None):
    """Blob nearest to column cx (bbox centre within tol px) with area >= amin; if several, the one
    closest to prefer_y (if given), else the largest."""
    c = [d for d in bl if abs(d["bx"] - cx) <= tol and d["area"] >= amin]
    if not c:
        return None
    if prefer_y is not None:
        return min(c, key=lambda d: abs(d["by"] - prefer_y))
    return max(c, key=lambda d: d["area"])


def calib_axes(dark, vwin, hwin, ylow, ystep, xlow, xstep, vside=-1, hside=1, majfrac=0.75, dark_h=None,
               vrows=None, hline=None, ytop=None):
    """vrows=(r0, r1): scan ticks over these rows instead of the detected axis-line run; hline=((r0, r1), (c0, c1)):
    give the horizontal axis line instead of detecting it; ytop: value of the topmost major tick (labels then
    count down by ystep), instead of ylow for the lowest one."""
    """Find a detached axis line + outward ticks. vwin=(x0,x1,y0,y1) window holding the vertical axis,
    hwin likewise for the horizontal one. Major ticks = ticks at least majfrac of the longest tick.
    The lowest major y tick gets value ylow, then +ystep per major tick upward; the leftmost major x tick
    gets xlow, then +xstep. Returns dict with fy, fx, inverse maps, residuals and the tick lists."""
    cols, rows = vaxis(dark, *vwin)
    if vrows is not None:
        rows = vrows
    tv = ticks_v(dark, cols, vside, rows[0] - 3, rows[1] + 4)
    Lv = max(L for _, L in tv)
    majv = sorted([r for r, L in tv if L >= majfrac * Lv], reverse=True)   # bottom first
    if ytop is not None:
        yvals = [ytop - (len(majv) - 1 - i) * ystep for i in range(len(majv))]
    else:
        yvals = [ylow + i * ystep for i in range(len(majv))]
    fy, ry, my, iy = fit(majv, yvals)
    dh = dark if dark_h is None else dark_h
    hr, hc = haxis(dh, *hwin) if hline is None else hline
    th = ticks_h(dh, hr, hside, hc[0] - 3, hc[1] + 4)
    Lh = max(L for _, L in th)
    majh = sorted([c for c, L in th if L >= majfrac * Lh])
    xvals = [xlow + i * xstep for i in range(len(majh))]
    fx, rx, mx, ix = fit(majh, xvals)
    return dict(fy=fy, fx=fx, iy=iy, ix=ix, res_y=ry, res_x=rx, my=my, mx=mx, vcols=cols, vrows=rows,
                hrows=hr, hcols=hc, majv=majv, yvals=yvals, majh=majh, xvals=xvals,
                minor_v=[r for r, L in tv if L < majfrac * Lv], minor_h=[c for c, L in th if L < majfrac * Lh])


def curve_at(mask, col, y_guess, gap, span=8, win=12):
    """Row of a series' curve at column col, interpolated from the curve on both sides of an occluding
    marker: in columns col-gap-span..col-gap and col+gap..col+gap+span, the centre of the mask run nearest
    to y_guess (within win px); a straight line through those points is evaluated at col. Returns
    (row, n_points) or (nan, 0)."""
    pts = []
    for c in list(range(int(col - gap - span), int(col - gap))) + list(range(int(col + gap), int(col + gap + span))):
        if c < 0 or c >= mask.shape[1]:
            continue
        r = np.where(mask[max(0, int(y_guess - win)):int(y_guess + win), c])[0]
        if len(r) == 0:
            continue
        runs = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
        run = min(runs, key=lambda q: abs(q.mean() + y_guess - win - y_guess))
        pts.append((c, max(0, int(y_guess - win)) + run.mean()))
    if len(pts) < 3:
        return float("nan"), 0
    pts = np.array(pts)
    m, b = np.polyfit(pts[:, 0], pts[:, 1], 1)
    return float(m * col + b), len(pts)


def square_edges(mask, x_guess, y_guess, win=14):
    """Centre of a filled square marker that other markers or lines partly cover, from its visible edges.
    Rows: the outermost mask rows within y_guess +- win in the 4 px bands at the square's left and right
    edges (found first as the outermost mask columns within x_guess +- win on rows y_guess +- 3 that are
    not on the horizontal line). Returns (cx, cy, w, h)."""
    y0, y1 = int(y_guess - win), int(y_guess + win + 1)
    x0, x1 = int(x_guess - win), int(x_guess + win + 1)
    sub = mask[y0:y1, x0:x1]
    # columns: use the rows just inside the top and bottom of the square (lines through the centre are avoided)
    rows_any = np.where(sub.any(1))[0]
    top, bot = rows_any.min(), rows_any.max()
    band = sub[[min(top + 2, bot), max(bot - 2, top)], :].any(0)
    cols = np.where(band)[0]
    left, right = cols.min(), cols.max()
    eb = np.zeros(sub.shape[1], bool)
    eb[left:left + 4] = True
    eb[right - 3:right + 1] = True
    rows = np.where(sub[:, eb].any(1))[0]
    return x0 + (left + right) / 2, y0 + (rows.min() + rows.max()) / 2, right - left + 1, rows.max() - rows.min() + 1
