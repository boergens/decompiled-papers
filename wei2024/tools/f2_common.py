"""Helpers for the wei2024 Fig. 6, 9 and 10 digitizations (fork F2).

The plots are Origin-style 300 ppi JPEGs: coloured scatter markers drawn as shaded balls (pure
colour in the lower right, a white highlight towards the upper left) and dashed fit lines of the
same colour. A shaded pixel is modelled as a mix of a palette colour c and white:
p = (1 - t) c + t (255, 255, 255). classify() assigns each pixel the palette colour with the
smallest distance to that mixing line (t limited to [0, tmax]), which keeps highlights with their
marker and keeps the pale pink background (red at t ~ 0.95) out of every class.
"""
import numpy as np
from scipy import ndimage as ndi


def classify(a, palette, tmax=0.7, resid_max=45.0):
    """Return (label, t): label[i, j] = index into palette (or -1), t = white fraction."""
    p = a.astype(float)
    best = np.full(p.shape[:2], np.inf)
    lab = np.full(p.shape[:2], -1, int)
    tt = np.zeros(p.shape[:2])
    w = np.array([255.0, 255.0, 255.0])
    for k, c in enumerate(palette):
        c = np.asarray(c, float)
        d = w - c
        dd = float(d @ d)
        t = np.clip(((p - c) @ d) / dd, 0, tmax) if dd > 0 else np.zeros(p.shape[:2])
        r = np.linalg.norm(p - c - t[..., None] * d, axis=2)
        m = r < best
        best[m] = r[m]
        lab[m] = k
        tt[m] = t[m]
    lab[best > resid_max] = -1
    return lab, tt


def disc(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r + 0.5


def markers(mask, r_open, single_area, max_n=6):
    """Find filled round markers in a bool mask (dashes thinner than 2*r_open+1 are removed).

    Returns a list of dicts: x, y (pixel centre), n (markers estimated in the blob), area,
    flag ('' | 'merged' | 'partial'). A blob of several overlapping markers of the same colour
    is split by k-means into round(area/single_area) centres.
    """
    op = ndi.binary_opening(mask, structure=disc(r_open))
    lab, n = ndi.label(op)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        area = len(ys)
        k = int(round(area / single_area))
        if k <= 1:
            flag = "partial" if area < 0.6 * single_area else ""
            out.append(dict(x=xs.mean(), y=ys.mean(), n=1, area=area, flag=flag))
            continue
        k = min(k, max_n)
        pts = np.c_[xs, ys].astype(float)
        # k-means with farthest-point initialisation
        cen = [pts[0]]
        for _ in range(k - 1):
            dmin = np.min([np.sum((pts - c) ** 2, 1) for c in cen], 0)
            cen.append(pts[np.argmax(dmin)])
        cen = np.array(cen)
        for _ in range(30):
            d = np.stack([np.sum((pts - c) ** 2, 1) for c in cen])
            asg = d.argmin(0)
            cen = np.array([pts[asg == j].mean(0) if np.any(asg == j) else cen[j] for j in range(k)])
        for c in cen:
            out.append(dict(x=c[0], y=c[1], n=k, area=area, flag="merged"))
    return out


def lin(p0, v0, p1, v1):
    """Linear map from two (pixel, value) pairs."""
    m = (v1 - v0) / (p1 - p0)
    return lambda p: v0 + m * (np.asarray(p, float) - p0)


def fit_ticks(pix, val):
    """Least-squares pixel -> value map; returns (f, max residual in value units, slope)."""
    pix = np.asarray(pix, float)
    val = np.asarray(val, float)
    A = np.c_[pix, np.ones_like(pix)]
    (m, b), *_ = np.linalg.lstsq(A, val, rcond=None)
    res = float(np.max(np.abs(A @ [m, b] - val)))
    return (lambda p: m * np.asarray(p, float) + b), res, m


def trace_class(mask, x0, x1, y0, y1, step=1, max_jump=12, seed=None):
    """Centre row of a (dashed) line of one colour class in each column, following continuity.

    Columns without pixels are skipped (dash gaps). When a column has several runs, the run
    closest to the previous accepted row is taken; runs farther than max_jump (+ gap length)
    from it are ignored. Returns arrays x, y (pixel units).
    """
    xs, ys = [], []
    prev, prev_x = seed, None
    for c in range(x0, x1, step):
        r = np.where(mask[y0:y1, c])[0]
        if len(r) == 0:
            continue
        runs = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
        cents = np.array([y0 + q.mean() for q in runs])
        if prev is None:
            j = int(np.argmax([len(q) for q in runs]))
        else:
            j = int(np.argmin(np.abs(cents - prev)))
            gap = (c - prev_x) if prev_x is not None else 0
            if abs(cents[j] - prev) > max_jump + 0.6 * gap:
                continue
        prev, prev_x = cents[j], c
        xs.append(c)
        ys.append(cents[j])
    return np.array(xs, float), np.array(ys, float)


def save_overlay(a, groups, out_png, r=2):
    """Draw marks over the source image. groups: list of (xy_px list, rgb colour, style)
    with style 'dot' (filled square of half-size r) or 'ring' (hollow box of half-size r+3)."""
    from PIL import Image
    im = a.copy()
    H, W = im.shape[:2]
    for pts, col, style in groups:
        for x, y in pts:
            if x != x or y != y:
                continue
            xi, yi = int(round(x)), int(round(y))
            if style == "ring":
                R = r + 3
                for dx in range(-R, R + 1):
                    for yy in (yi - R, yi + R):
                        if 0 <= yy < H and 0 <= xi + dx < W:
                            im[yy, xi + dx] = col
                    for xx in (xi - R, xi + R):
                        if 0 <= yi + dx < H and 0 <= xx < W:
                            im[yi + dx, xx] = col
            else:
                im[max(0, yi - r):yi + r + 1, max(0, xi - r):xi + r + 1] = col
    Image.fromarray(im).save(out_png)


def markers_dt(mask, rmin=3.0, min_sep=5.0, close=1, cov_r=4.5):
    """Marker centres as maxima of the distance transform of a class mask.

    A round filled marker of diameter D has an inscribed-circle radius ~D/2; a dash of width w only
    ~w/2. Peaks with radius >= rmin are kept, strongest first, suppressing others within min_sep px.
    Returns list of dicts x, y, r (inscribed radius in px), cov (share of a disc of radius cov_r
    around the centre that is in the mask: ~1 for a marker, lower for a dash). A small closing first fills holes.
    """
    m = ndi.binary_closing(mask, structure=np.ones((3, 3)), iterations=close) | mask if close else mask
    m = ndi.binary_fill_holes(m)
    dt = ndi.distance_transform_edt(m)
    mx = ndi.maximum_filter(dt, size=3)
    cand = np.argwhere((dt >= rmin) & (dt == mx))
    order = np.argsort(-dt[cand[:, 0], cand[:, 1]])
    kept = []
    for i in order:
        y, x = cand[i]
        if all((x - kx) ** 2 + (y - ky) ** 2 >= min_sep ** 2 for kx, ky, _ in kept):
            kept.append((x, y, dt[y, x]))
    out = []
    for x, y, r in kept:
        # refine: centroid of the mask pixels within r of the peak
        yy, xx = np.mgrid[max(0, y - 5):y + 6, max(0, x - 5):x + 6]
        sel = m[yy, xx] & ((xx - x) ** 2 + (yy - y) ** 2 <= (r + 0.5) ** 2)
        cx, cy = float(xx[sel].mean()), float(yy[sel].mean())
        yy, xx = np.mgrid[max(0, int(cy) - 6):int(cy) + 7, max(0, int(cx) - 6):int(cx) + 7]
        dsk = (xx - cx) ** 2 + (yy - cy) ** 2 <= cov_r ** 2
        cov = float(m[yy, xx][dsk].mean())
        out.append(dict(x=cx, y=cy, r=float(r), cov=cov))
    return out


def curve_zone(shape, xs, ys, half_width):
    """Bool mask of pixels within half_width of the polyline (xs, ys) (pixel units)."""
    m = np.zeros(shape, bool)
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    for i in range(len(xs) - 1):
        n = int(max(abs(xs[i + 1] - xs[i]), abs(ys[i + 1] - ys[i])) * 2) + 2
        for t in np.linspace(0, 1, n):
            x = xs[i] + t * (xs[i + 1] - xs[i])
            y = ys[i] + t * (ys[i + 1] - ys[i])
            yi, xi = int(round(y)), int(round(x))
            if 0 <= yi < shape[0] and 0 <= xi < shape[1]:
                m[yi, xi] = True
    return ndi.binary_dilation(m, structure=disc(int(np.ceil(half_width))))


def grid_markers(mask, xcols, light, half=2.5, rmin=2.0, min_area=12, min_sep=5, R=4.0, win=5):
    """Markers of one colour placed on known x grid columns (data at fixed x steps).

    mask: bool class mask (dash pixels of the same colour already removed); xcols: pixel x of the
    grid; light: bool mask of background pixels (to tell a marker's free edge from an edge hidden
    by another marker). For each grid column, candidate rows are local maxima (>= rmin) of the
    distance transform within +-half px of the column. The marker centre row is taken from its
    free edge(s): both edges free -> midpoint; only the top edge free -> top + R; only the bottom
    edge free -> bottom - R. Returns dicts x, y, area, flag ('' | 'top-edge' | 'bottom-edge' |
    'hidden-edges').
    """
    m = ndi.binary_fill_holes(mask)
    dt = ndi.distance_transform_edt(m)
    H, W = m.shape
    out = []
    for xc in xcols:
        c0, c1 = int(np.floor(xc - half)), int(np.ceil(xc + half)) + 1
        prof = dt[:, c0:c1].max(1)
        cand = [r for r in range(1, H - 1) if prof[r] >= rmin and prof[r] >= prof[r - 1] and prof[r] >= prof[r + 1]]
        cand.sort(key=lambda r: -prof[r])
        kept = []
        for r in cand:
            if all(abs(r - q) >= min_sep for q in kept):
                kept.append(r)
        for r in kept:
            y0, y1 = max(0, r - win - 2), min(H, r + win + 3)
            x0, x1 = max(0, int(xc) - win), min(W, int(xc) + win + 2)
            lab, _ = ndi.label(m[y0:y1, x0:x1])
            cc = lab[r - y0, int(round(xc)) - x0] if m[r, int(round(xc))] else 0
            if cc == 0:
                sub = lab[r - y0, :]
                ids = [v for v in sub if v]
                if not ids:
                    continue
                cc = ids[len(ids) // 2]
            ys, xs = np.where(lab == cc)
            area = len(ys)
            if area < min_area:
                continue
            xcen = x0 + xs.mean()
            # vertical run through the column nearest the centre
            col = int(round(xcen))
            run = np.where(m[y0:y1, col])[0] + y0
            if len(run) == 0:
                continue
            seg = np.split(run, np.where(np.diff(run) > 1)[0] + 1)
            seg = min(seg, key=lambda q: 0 if q[0] <= r <= q[-1] else min(abs(q[0] - r), abs(q[-1] - r)))
            t, b = seg[0], seg[-1]
            ft = t - 1 >= 0 and light[t - 1, col - 1:col + 2].all()
            fb = b + 1 < H and light[b + 1, col - 1:col + 2].all()
            if ft and fb:
                yc, flag = (t + b) / 2, ""
                if b - t > 2 * R + 3:   # two stacked markers of the same colour
                    out.append(dict(x=xcen, y=t + R, area=area, flag="same-colour-stack"))
                    yc, flag = b - R, "same-colour-stack"
            elif ft:
                yc, flag = t + R, "top-edge"
            elif fb:
                yc, flag = b - R, "bottom-edge"
            else:
                yc, flag = (t + b) / 2, "hidden-edges"
            out.append(dict(x=xcen, y=yc, area=area, flag=flag))
    # remove duplicates (same marker found from two candidate rows)
    ded = []
    for q in sorted(out, key=lambda q: -q["area"]):
        if all((q["x"] - p["x"]) ** 2 + (q["y"] - p["y"]) ** 2 >= 9 for p in ded):
            ded.append(q)
    return ded


def chain_dashes(mask, start_xy, direction, max_gap=22.0, max_angle=40.0, min_area=6, stop_x=None):
    """Follow a dashed line made of separate dash blobs.

    mask: bool mask of one colour with markers removed; start_xy: a point near the first dash;
    direction: initial unit vector (dx, dy) of travel. Each step takes the blob whose nearest pixel
    is closest to the current end point (<= max_gap px) and whose direction from the current end
    is within max_angle degrees of the current direction. Returns the chained blobs as a list of
    (N, 2) pixel arrays (x, y), in order of travel.
    """
    lab, n = ndi.label(mask, structure=np.ones((3, 3)))
    blobs = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) >= min_area:
            blobs.append(np.c_[xs, ys].astype(float))
    used = set()
    d = np.asarray(direction, float)
    d /= np.linalg.norm(d)
    end = np.asarray(start_xy, float)
    chain = []
    first = True
    while True:
        best, bd = None, None
        for j, b in enumerate(blobs):
            if j in used:
                continue
            v = b - end
            dist = np.sqrt((v ** 2).sum(1))
            i0 = int(np.argmin(dist))
            if dist[i0] > (max_gap if not first else 15):
                continue
            c = b.mean(0) - end
            if np.linalg.norm(c) < 1e-6:
                continue
            ang = np.degrees(np.arccos(np.clip((c @ d) / np.linalg.norm(c), -1, 1)))
            if ang > max_angle and not first:
                continue
            score = dist[i0] + 0.15 * ang
            if bd is None or score < bd:
                best, bd = j, score
        if best is None:
            break
        used.add(best)
        b = blobs[best]
        chain.append(b)
        # far end of the blob along the travel direction, and new direction
        proj = (b - end) @ d
        new_end = b[int(np.argmax(proj))]
        if len(chain) >= 2:
            nd = chain[-1].mean(0) - chain[-2].mean(0)
        else:
            nd = new_end - end
        if np.linalg.norm(nd) > 1e-6:
            nd = nd / np.linalg.norm(nd)
            d = 0.5 * d + 0.5 * nd
            d /= np.linalg.norm(d)
        end = new_end
        first = False
        if stop_x is not None and end[0] <= stop_x:
            break
    return chain


def blob_centreline(b, step=2.0):
    """Points along the main axis of one dash blob (centre line), every `step` px."""
    c = b.mean(0)
    u, s, vt = np.linalg.svd(b - c, full_matrices=False)
    ax = vt[0]
    t = (b - c) @ ax
    pts = []
    for tt in np.arange(t.min() + 1, t.max() - 1 + 1e-9, step):
        sel = np.abs(t - tt) <= step / 2
        if sel.any():
            pts.append(b[sel].mean(0))
    if not pts:
        pts = [c]
    return np.array(pts)


def on_curve_markers(mask, grid_px, curve_y, min_centre=8.5, min_side=6.0, side=3):
    """Markers lying on their own dashed curve (where the curve zone was blanked for grid_markers).

    For each grid column xc, take the run of mask pixels in that column that contains (or is
    within 2 px of) the curve's row curve_y(xc). A marker gives a run of ~9-10 px and runs of
    >= ~6.5 px at xc +- 3; a dash only ~4/cos(slope) px. Returns dicts x, y, flag='on-curve'.
    """
    out = []
    H = mask.shape[0]

    def run_at(c, y):
        r = np.where(mask[:, c])[0]
        if len(r) == 0:
            return None
        seg = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
        best = min(seg, key=lambda q: 0 if q[0] - 2 <= y <= q[-1] + 2 else min(abs(q[0] - y), abs(q[-1] - y)))
        if not (best[0] - 2 <= y <= best[-1] + 2):
            return None
        return best
    for xc in grid_px:
        c = int(round(xc))
        y = float(curve_y(xc))
        if not (0 <= y < H):
            continue
        r0 = run_at(c, y)
        if r0 is None or len(r0) < min_centre:
            continue
        ok = True
        for dc_ in (-side, side):
            r1 = run_at(c + dc_, y)
            if r1 is None or len(r1) < min_side:
                ok = False
        if ok:
            out.append(dict(x=float(c), y=(r0[0] + r0[-1]) / 2, flag="on-curve"))
    return out


def hollow_markers(mask, xcols, half=4, min_hole=2, max_hole=40, max_span=9):
    """Open (hollow) markers of one colour on known x grid columns, found from their holes.

    The inside of an outlined square/circle/triangle is a small hole in the colour mask; a line of
    the same colour crossing the marker splits it into two holes. For each grid column, holes
    (area min_hole..max_hole px) whose centroid is within +-half px of the column are grouped by
    rows (gap < 5 px, total span <= max_span); the marker centre is the midpoint of the group's
    top and bottom hole rows and the mean hole column. Returns dicts x, y, n_holes, span.
    """
    filled = ndi.binary_fill_holes(mask)
    holes = filled & ~mask
    lab, n = ndi.label(holes)
    info = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        if sl is None:
            continue
        ys, xs = np.where(lab[sl] == i)
        if not (min_hole <= len(ys) <= max_hole):
            continue
        info.append((xs.mean() + sl[1].start, ys.min() + sl[0].start, ys.max() + sl[0].start, len(ys)))
    info = np.array(info) if info else np.zeros((0, 4))
    out = []
    for xc in xcols:
        sel = info[np.abs(info[:, 0] - xc) <= half] if len(info) else info
        if not len(sel):
            continue
        sel = sel[np.argsort(sel[:, 1])]
        groups = [[sel[0]]]
        for h in sel[1:]:
            if h[1] - groups[-1][-1][2] < 5 and h[2] - groups[-1][0][1] <= max_span:
                groups[-1].append(h)
            else:
                groups.append([h])
        for gr in groups:
            gr = np.array(gr)
            top, bot = gr[:, 1].min(), gr[:, 2].max()
            out.append(dict(x=float(np.average(gr[:, 0], weights=gr[:, 3])), y=float((top + bot) / 2),
                            n_holes=len(gr), span=float(bot - top + 1)))
    return out
