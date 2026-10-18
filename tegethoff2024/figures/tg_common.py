"""Shared helpers for the tegethoff2024 extraction scripts (figN?_extract.py).

All figures of this paper are JPEG raster images embedded in the PDF (no vector plot data:
the only vector paths on the figure pages are the grey figure frames), so every plotted panel
is tier 3, digitized. This module adds to ../tools/digitize_common.py:

  img(page)            the embedded figure image of a PDF page (RGB, native resolution)
  axis_line()          locate a dark axis line (row or column) inside a box
  ticks()              tick marks attached to an axis line (MATLAB style, pointing into the plot)
  classify()           assign each pixel to the nearest colour of a palette (MATLAB default colours)
  dots()               marker centres of a sparse dot/strip plot from a colour mask
  swarm_profile()      per-pixel-row profile of a dense beeswarm (pixel count, extent, est. points)
  colourbar()/lookup() map a colour to a value through a colour bar sampled in the image

Scripts put this folder on sys.path themselves, so they run with `python3 -I`.
"""
import os
import sys

import numpy as np
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "../tools"))
sys.path.insert(0, TOOLS)
from digitize_common import embedded_image, fit_axis, write_csv, overlay, trace_envelope  # noqa: E402,F401

PDF = os.path.normpath(os.path.join(HERE, "../source/fnins-18-1286991.pdf"))
WORK = os.path.normpath(os.path.join(HERE, "../work"))
os.makedirs(WORK, exist_ok=True)

# placement bbox (PDF points) of the figure image on each page
BBOX = {4: (77, 89, 261, 443), 5: (66, 89, 272, 484), 51: (322, 89, 527, 341), 6: (74, 89, 519, 379),
        7: (74, 89, 519, 612), 8: (74, 335, 519, 674), 10: (122, 89, 471, 677), 11: (147, 89, 446, 483)}

# MATLAB default line colours, as used for the resins in Figs 2, 5, 6, 7
MATLAB = {
    "blue": (0, 114, 189), "orange": (217, 83, 25), "yellow": (237, 177, 32), "purple": (126, 47, 142),
    "green": (119, 172, 48), "lightblue": (77, 190, 238), "darkred": (162, 20, 47),
}


def img(key):
    """Embedded figure image; key = page number (5 for Fig 2, 51 for Fig 3 on the same page)."""
    page = key if key < 50 else key // 10
    return embedded_image(PDF, page, bbox_near=BBOX[key])


def gray(a):
    return a.astype(float).mean(2)


def sat(a):
    a = a.astype(int)
    return a.max(2) - a.min(2)


def dark(a, thr=140, maxsat=40):
    return (gray(a) < thr) & (sat(a) < maxsat)


def axis_line(mask, box, orient):
    """Return (first, last) index of the longest straight dark line in box=(x0,y0,x1,y1).

    orient 'v': a column (y axis); 'h': a row (x axis). Lines thicker than 1 px give a group."""
    x0, y0, x1, y1 = box
    sub = mask[y0:y1, x0:x1]
    s = sub.sum(0) if orient == "v" else sub.sum(1)
    m = s.max()
    idx = np.where(s >= 0.7 * m)[0]
    # keep the group containing the maximum
    k = int(np.argmax(s))
    lo = hi = k
    while lo - 1 in idx:
        lo -= 1
    while hi + 1 in idx:
        hi += 1
    off = x0 if orient == "v" else y0
    return off + lo, off + hi


def ticks(mask, line, orient, side, lo, hi, gap=1, length=4, frac=0.75):
    """Centres of tick marks on an axis line.

    line = (first,last) index of the axis line; orient 'v' (ticks are rows along a column line)
    or 'h' (ticks are columns along a row line); side +1 = right of / below the line, -1 = left / above;
    lo..hi = range along the line to search; the band gap..gap+length px off the line must be dark."""
    if orient == "v":
        c = line[1] + 1 + gap if side > 0 else line[0] - gap - length
        band = mask[lo:hi, c:c + length]
        full = band.mean(1) >= frac
    else:
        r = line[1] + 1 + gap if side > 0 else line[0] - gap - length
        band = mask[r:r + length, lo:hi]
        full = band.mean(0) >= frac
    idx = np.where(full)[0]
    groups = []
    for i in idx:
        if groups and i <= groups[-1][-1] + 1:
            groups[-1].append(i)
        else:
            groups.append([i])
    return [lo + float(np.mean(g)) for g in groups]


def to_lab(rgb):
    import cv2
    a = np.asarray(rgb, np.uint8).reshape(-1, 1, 3)
    return cv2.cvtColor(a, cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(float)


def classify(a, palette, max_dist=40, min_sat=50):
    """Label image: index into palette (list of RGB) of the nearest colour in Lab, or -1.

    Pixels with saturation < min_sat (white, grey, black) or farther than max_dist (Lab units)
    from every palette colour are -1."""
    import cv2
    lab = cv2.cvtColor(a, cv2.COLOR_RGB2LAB).astype(float)
    pal = to_lab(palette)
    d = np.stack([np.sqrt(((lab - p) ** 2).sum(2)) for p in pal], 0)
    k = d.argmin(0)
    ok = (d.min(0) <= max_dist) & (sat(a) >= min_sat)
    return np.where(ok, k, -1)


def dots(mask, single_area=None, min_area=4):
    """Marker centres from a boolean mask of one series (sparse strip/dot plots).

    Connected components; the area of an isolated marker (single_area, or the median area of
    the components if not given) sets how many markers a merged blob holds (n = round(area/single)).
    A blob of n > 1 markers is split with k-means on its pixel coordinates.
    Returns a list of (x, y, n_in_blob, blob_id)."""
    import cv2
    m = mask.astype(np.uint8)
    nlab, lab, stats, cent = cv2.connectedComponentsWithStats(m, connectivity=8)
    areas = stats[1:, cv2.CC_STAT_AREA]
    keep = [i + 1 for i, ar in enumerate(areas) if ar >= min_area]
    if not keep:
        return [], 0
    if single_area is None:
        single_area = float(np.median([stats[i, cv2.CC_STAT_AREA] for i in keep]))
    out = []
    for i in keep:
        ar = stats[i, cv2.CC_STAT_AREA]
        n = max(1, int(round(ar / single_area)))
        if n == 1:
            out.append((cent[i][0], cent[i][1], 1, i))
            continue
        ys, xs = np.where(lab == i)
        pts = np.column_stack([xs, ys]).astype(np.float32)
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
        cv2.setRNGSeed(1)
        _, _, centres = cv2.kmeans(pts, n, None, crit, 10, cv2.KMEANS_PP_CENTERS)
        for cx, cy in sorted(centres.tolist(), key=lambda c: (c[1], c[0])):
            out.append((cx, cy, n, i))
    return out, single_area


def swarm_profile(mask, x0, x1, y0, y1, dot_area):
    """Per pixel row of a beeswarm group inside columns x0..x1: (row, n_px, left, right, est_points).

    est_points = n_px / dot_area: the number of markers whose area falls in that row if markers do
    not overlap (a beeswarm spreads them sideways); summed over rows it estimates the group size."""
    rows = []
    for r in range(y0, y1):
        c = np.where(mask[r, x0:x1])[0]
        if len(c):
            rows.append((r, len(c), x0 + c.min(), x0 + c.max(), len(c) / dot_area))
    return rows


def colourbar(a, col0, col1, row_top, row_bot):
    """Sample a vertical colour bar: mean colour of columns col0..col1 for each row (top to bottom)."""
    strip = a[row_top:row_bot + 1, col0:col1 + 1].astype(float).mean(1)
    return np.arange(row_top, row_bot + 1), strip


def lookup(rgb, bar_rows, bar_rgb, row_to_value):
    """Value of colour rgb through the colour bar (nearest bar colour in Lab). Returns (value, dist,
    value range of bar entries within dist+3 Lab units, a measure of how well the colour pins the value)."""
    lab = to_lab(np.clip(np.asarray([rgb]), 0, 255))[0]
    bl = to_lab(np.clip(bar_rgb, 0, 255))
    d = np.sqrt(((bl - lab) ** 2).sum(1))
    k = int(d.argmin())
    near = np.where(d <= d[k] + 3)[0]
    vals = row_to_value(bar_rows[near])
    return float(row_to_value(bar_rows[k])), float(d[k]), (float(vals.min()), float(vals.max()))


def save(a, name):
    from PIL import Image
    Image.fromarray(a).save(os.path.join(WORK, name))


def read_csv(path):
    import csv
    with open(path) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def box_mask(shape, box):
    m = np.zeros(shape[:2], bool)
    x0, y0, x1, y1 = box
    m[y0:y1, x0:x1] = True
    return m


def dot_rows(masks, box, fx, fy, single_area, min_area=8):
    """Marker centres of several series. masks: {series: bool mask}; box limits the search
    (x0,y0,x1,y1, inside the axis frame). Returns rows (series, x, y, x_px, y_px, n_in_blob, blob)
    sorted by series then x then y, and the pixel points for overlay()."""
    rows, pts = [], []
    bm = box_mask(next(iter(masks.values())).shape, box)
    for name, m in masks.items():
        d, _ = dots(m & bm, single_area, min_area)
        for x, y, n, b in d:
            rows.append((name, float(fx(x)), float(fy(y)), x, y, n, f"{name}:{b}"))
            pts.append((x, y))
    return rows, pts


def mark(a, pts, colour=(255, 0, 255), r=1):
    """Copy of a with small crosses at pts (for overlays of sparse markers)."""
    im = a.copy()
    for x, y in pts:
        xi, yi = int(round(x)), int(round(y))
        for dx in range(-r - 1, r + 2):
            if 0 <= yi < im.shape[0] and 0 <= xi + dx < im.shape[1]:
                im[yi, xi + dx] = colour
            if 0 <= yi + dx < im.shape[0] and 0 <= xi < im.shape[1]:
                im[yi + dx, xi] = colour
    return im


def image_box(a, region, white=245):
    """Bounding box (x0,y0,x1,y1) of the non-white pixels (a micrograph) inside region."""
    x0, y0, x1, y1 = region
    m = gray(a[y0:y1, x0:x1]) < white
    cols = np.where(m.mean(0) > 0.5)[0]
    rows = np.where(m.mean(1) > 0.5)[0]
    return x0 + cols.min(), y0 + rows.min(), x0 + cols.max(), y0 + rows.max()


def dotmap(a, box, bar_cols, bar_rows, label_rows, label_vals, min_sat=70, min_area=20, core=2.5):
    """Coloured measurement dots on a micrograph, mapped through a colour bar.

    box: region of the micrograph; bar_cols/bar_rows: (first,last) of the colour bar; label_rows: vertical
    centres of the colour-bar labels, label_vals their values. Returns (dots, fit residual, slope):
    dots = list of (x_px, y_px, value, lab_dist, value_lo, value_hi, rgb)."""
    import cv2
    fv, res, slope = fit_axis(label_rows, label_vals)
    c0, c1 = bar_cols
    brows, brgb = colourbar(a, c0 + 3, c1 - 3, bar_rows[0] + 2, bar_rows[1] - 2)
    x0, y0, x1, y1 = box
    m = (sat(a) >= min_sat)
    m[:y0], m[y1:], m[:, :x0], m[:, x1:] = False, False, False, False
    n, lab, st, cen = cv2.connectedComponentsWithStats(m.astype(np.uint8))
    out = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < min_area:
            continue
        cx, cy = cen[i]
        ys, xs = np.where(lab == i)
        sel = (xs - cx) ** 2 + (ys - cy) ** 2 <= core ** 2
        rgb = np.median(a[ys[sel], xs[sel]].astype(float), 0)
        v, d, (lo, hi) = lookup(rgb, brows, brgb, fv)
        out.append((cx, cy, v, d, lo, hi, tuple(int(c) for c in rgb)))
    return out, res, slope


def traces(masks, x0, x1, y0, y1, fx, fy, min_px=1):
    """Per pixel column and series: (series, x, y_mid, y_top, y_bottom) in data units, following the run of mask
    pixels nearest the previous column (trace_envelope with half_width 0: top/bottom are the drawn band's edges,
    i.e. line width plus the noise of the trace within one pixel column). Columns where the series is hidden
    are skipped. Returns rows and overlay points."""
    rows, pts = [], []
    for name, m in masks.items():
        env = trace_envelope(m, x0, x1, y0, y1, half_width=0, min_px=min_px)
        for c, ym, yt, yb in env:
            if ym != ym:
                continue
            rows.append((name, float(fx(c)), float(fy(ym)), float(fy(yt)), float(fy(yb))))
            pts += [(c, yt), (c, yb)]
    return rows, pts


RESINS = ["LX 112", "M Epon", "MH Epon", "H Epon", "VH Epon", "Durcupan", "Spurr's"]
RESIN_RGB = [MATLAB[k] for k in ["yellow", "darkred", "blue", "orange", "lightblue", "purple", "green"]]


def fill_holes(m):
    import cv2
    m8 = m.astype(np.uint8) * 255
    h, w = m8.shape
    ff = m8.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, mask, (0, 0), 255)
    return (m8 | cv2.bitwise_not(ff)) > 0


def markers_errorbars(m, box, open_px=5, min_area=30, gap=3):
    """Markers (filled circles / open squares) and their vertical error bars in one series mask.

    Holes are filled and thin lines removed (opening open_px), so the remaining blobs are markers; a marker is 'filled'
    if the original mask covers its centre, else 'open'. The error bar ends are the topmost/bottommost mask pixels
    reachable from the marker along its centre columns (cx-1..cx+1), bridging gaps of up to `gap` px.
    Returns list of (cx, cy, kind, top_row, bottom_row, area)."""
    import cv2
    x0, y0, x1, y1 = box
    mm = np.zeros_like(m)
    mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    solid = cv2.morphologyEx(fill_holes(mm).astype(np.uint8), cv2.MORPH_OPEN,
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_px, open_px)))
    n, lab, st, cen = cv2.connectedComponentsWithStats(solid)
    out = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < min_area:
            continue
        cx, cy = cen[i]
        c = int(round(cx))
        r0 = st[i, cv2.CC_STAT_TOP]
        r1 = r0 + st[i, cv2.CC_STAT_HEIGHT] - 1
        col = mm[:, c - 1:c + 2].any(1)
        top = r0
        for r in range(r0 - 1, y0 - 1, -1):
            if col[r]:
                top = r
            elif top - r > gap:
                break
        bot = r1
        for r in range(r1 + 1, y1):
            if col[r]:
                bot = r
            elif r - bot > gap:
                break
        kind = "filled" if mm[int(round(cy)) - 1:int(round(cy)) + 2, c - 1:c + 2].mean() > 0.6 else "open"
        out.append((cx, cy, kind, top, bot, int(st[i, cv2.CC_STAT_AREA])))
    return out


def markers_any(a, box, min_sat=35, open_px=5, min_area=30, gap=3):
    """Like markers_errorbars(), on the mask of all saturated (coloured) pixels; each marker's colour is the median of
    the most saturated pixels of the marker (core of a filled circle, outline of an open square). Returns
    (cx, cy, kind, top, bottom, area, rgb)."""
    m = sat(a) >= min_sat
    res = markers_errorbars(m, box, open_px, min_area, gap)
    out = []
    for cx, cy, kind, top, bot, area in res:
        x, y = int(round(cx)), int(round(cy))
        patch = a[y - 7:y + 8, x - 7:x + 8].reshape(-1, 3).astype(float)
        s = patch.max(1) - patch.min(1)
        sel = patch[s >= np.percentile(s, 80)]
        out.append((cx, cy, kind, top, bot, area, tuple(np.median(sel, 0))))
    return out


def nearest_name(rgb, names=None, pal=None):
    names = names or RESINS
    pal = pal or RESIN_RGB
    lab = to_lab([np.clip(rgb, 0, 255)])[0]
    d = [np.sqrt(((to_lab([p])[0] - lab) ** 2).sum()) for p in pal]
    return names[int(np.argmin(d))], float(min(d))


def series_mask(a, rgb, tol=28, tmax=0.7):
    """Pixels whose colour lies within tol (Lab) of rgb blended with white by any fraction 0..tmax (antialiased thin
    lines of a series are lighter than its markers)."""
    import cv2
    lab = cv2.cvtColor(a, cv2.COLOR_RGB2LAB).astype(float)
    best = np.full(a.shape[:2], 1e9)
    for t in np.linspace(0, tmax, 8):
        c = np.asarray(rgb, float) * (1 - t) + 255 * t
        best = np.minimum(best, np.sqrt(((lab - to_lab([c])[0]) ** 2).sum(2)))
    return (best <= tol) & (sat(a) >= 25)


def refine_marker(m, x, y, half=9):
    """Centre of the mask pixels in a (2*half+1) window around (x, y): centroid for a filled marker, bounding-box
    centre for an outline. Returns (cx_centroid, cy_centroid, cx_bbox, cy_bbox)."""
    x, y = int(round(x)), int(round(y))
    ys, xs = np.where(m[y - half:y + half + 1, x - half:x + half + 1])
    return (x - half + xs.mean(), y - half + ys.mean(),
            x - half + (xs.min() + xs.max()) / 2, y - half + (ys.min() + ys.max()) / 2)


def bar_ends(m, cx, cy, skip=8, gap=3, y0=0, y1=None):
    """Top and bottom row of a vertical error bar through (cx, cy) in mask m (column cx only, gaps <= gap bridged);
    skip = rows next to the marker centre that are part of the marker itself."""
    c = int(round(cx))
    col = m[:, c]
    y1 = y1 or len(col)
    yc = int(round(cy))
    top = yc - skip
    for r in range(yc - skip, y0 - 1, -1):
        if col[r]:
            top = r
        elif top - r > gap:
            break
    bot = yc + skip
    for r in range(yc + skip, y1):
        if col[r]:
            bot = r
        elif r - bot > gap:
            break
    return top, bot


def column_groups(m, x0, x1, y0, y1, min_gap=4, min_px=3):
    """Split the coloured columns of a strip/swarm plot into groups separated by >= min_gap empty columns."""
    s = m[y0:y1, x0:x1].sum(0)
    on = np.where(s >= min_px)[0]
    groups = []
    for c in on:
        if groups and c - groups[-1][1] <= min_gap:
            groups[-1][1] = c
        else:
            groups.append([c, c])
    return [(x0 + g0, x0 + g1) for g0, g1 in groups]


def swarm_panel(a, box, fy, expected, names=None, pal=None, min_sat=40, dot_area=None, min_gap=4):
    """Beeswarm panel -> per-row profiles of each group.

    box = plot area inside the axes; expected = list of (series, group label) for the groups left to right.
    Groups are found as column clusters of saturated pixels; each group's series is checked against the dominant
    palette colour. dot_area: area of one isolated marker (px); if None, the median area of 1-marker components.
    Returns rows (series, group, y_value, n_px, est_points, x_left_px, x_right_px, x_centre_px), group summary, pts."""
    import cv2
    names = names or RESINS
    pal = pal or RESIN_RGB
    x0, y0, x1, y1 = box
    m = sat(a) >= min_sat
    m[:y0], m[y1:], m[:, :x0], m[:, x1:] = False, False, False, False
    groups = column_groups(m, x0, x1, y0, y1, min_gap=min_gap)
    if dot_area is None:
        n, lab, st, cen = cv2.connectedComponentsWithStats(m.astype(np.uint8))
        ar = st[1:, cv2.CC_STAT_AREA]
        ar = ar[(ar >= 6)]
        small = ar[ar <= np.percentile(ar, 50)]
        dot_area = float(np.median(small))
    lab = classify(a, pal, max_dist=60, min_sat=min_sat)
    rows, summ, pts = [], [], []
    for gi, (g0, g1) in enumerate(groups):
        sub = lab[y0:y1, g0:g1 + 1]
        counts = [(sub == k).sum() for k in range(len(pal))]
        dom = names[int(np.argmax(counts))]
        exp = expected[gi] if gi < len(expected) else ("?", "?")
        prof = swarm_profile(m, g0, g1 + 1, y0, y1, dot_area)
        xc = (g0 + g1) / 2
        for r, npx, l, rr, est in prof:
            rows.append((exp[0], exp[1], float(fy(r)), npx, est, l - xc, rr - xc, xc))
            pts += [(l, r), (rr, r)]
        tot = sum(p[4] for p in prof)
        ys = np.array([fy(p[0]) for p in prof])
        w = np.array([p[4] for p in prof])
        order = np.argsort(ys)
        cw = np.cumsum(w[order]) / w.sum()
        q = [float(ys[order][np.searchsorted(cw, f)]) for f in (0.25, 0.5, 0.75)]
        summ.append((exp[0], exp[1], dom, g0, g1, tot, q, float(ys.min()), float(ys.max())))
    return rows, summ, pts, dot_area, groups


def swarm_panel2(a, box, fy, names=None, pal=None, min_sat=40, max_dist=45, dot_area=15.0, min_gap=6,
                 min_frac=0.04, min_col_px=2):
    """Beeswarm panel, groups found per series colour: each series' colour mask is split into column clusters;
    clusters holding < min_frac of the series' largest cluster are treated as misclassified edge pixels and dropped.
    Returns groups sorted left to right: list of dict(series, x0, x1, xc, prof=[(row, n_px, left, right, est)])."""
    names = names or RESINS
    pal = pal or RESIN_RGB
    x0, y0, x1, y1 = box
    lab = classify(a, pal, max_dist=max_dist, min_sat=min_sat)
    out = []
    for k, name in enumerate(names):
        m = lab == k
        m[:y0], m[y1:], m[:, :x0], m[:, x1:] = False, False, False, False
        gs = column_groups(m, x0, x1, y0, y1, min_gap=min_gap, min_px=min_col_px)
        tots = [m[y0:y1, g0:g1 + 1].sum() for g0, g1 in gs]
        if not tots:
            continue
        big = max(tots)
        for (g0, g1), t in zip(gs, tots):
            if t < min_frac * big or t < 3 * dot_area:
                continue
            prof = swarm_profile(m, g0, g1 + 1, y0, y1, dot_area)
            out.append(dict(series=name, x0=g0, x1=g1, xc=(g0 + g1) / 2, prof=prof, mask_px=int(t)))
    return sorted(out, key=lambda g: g["xc"])


def summarize(prof, fy):
    ys = np.array([fy(p[0]) for p in prof], float)
    w = np.array([p[4] for p in prof], float)
    o = np.argsort(ys)
    cw = np.cumsum(w[o]) / w.sum()
    q = [float(ys[o][min(len(o) - 1, np.searchsorted(cw, f))]) for f in (0.25, 0.5, 0.75)]
    return float(w.sum()), q, float(ys.min()), float(ys.max())


def swarm_groups(a, box, names=None, pal=None, min_sat=40, max_dist=45, dot_area=15.0, min_gap=6, min_frac=0.04):
    """Groups of a beeswarm panel: per-colour column clusters (swarm_panel2), clusters overlapping in x merged and
    named after the colour with the most pixels (JPEG colour bleeding puts some pixels of a swarm into a neighbouring
    colour class), then each group's profile is taken from the mask of ALL saturated pixels in its column range.
    Returns groups left to right: dict(series, x0, x1, xc, prof, share) with share = fraction of the group's classified
    pixels that have the group's colour."""
    gs = swarm_panel2(a, box, lambda r: r, names, pal, min_sat, max_dist, dot_area, 2, min_frac)
    merged = []
    for g in gs:
        for h in merged:
            ov = min(g["x1"], h["x1"]) - max(g["x0"], h["x0"])
            if ov >= 0.5 * min(g["x1"] - g["x0"], h["x1"] - h["x0"]):
                h["members"].append(g)
                h["x0"], h["x1"] = min(h["x0"], g["x0"]), max(h["x1"], g["x1"])
                break
        else:
            merged.append(dict(x0=g["x0"], x1=g["x1"], members=[g]))
    x0, y0, x1, y1 = box
    m = sat(a) >= min_sat
    m[:y0], m[y1:], m[:, :x0], m[:, x1:] = False, False, False, False
    out = []
    for h in merged:
        best = max(h["members"], key=lambda g: g["mask_px"])
        tot = sum(g["mask_px"] for g in h["members"])
        prof = swarm_profile(m, h["x0"], h["x1"] + 1, y0, y1, dot_area)
        out.append(dict(series=best["series"], x0=h["x0"], x1=h["x1"], xc=(h["x0"] + h["x1"]) / 2, prof=prof,
                        share=best["mask_px"] / tot))
    return sorted(out, key=lambda g: g["xc"])
