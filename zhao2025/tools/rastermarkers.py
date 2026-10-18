"""Square markers with vertical error bars in a raster plot (zhao2025 Fig. 2b and 2c; written for this paper).

Markers are filled squares ~14 px wide in the 300 ppi image; error bars are ~3 px wide vertical lines with ~25 px
wide caps; markers of one series are joined by a ~3 px line of the same colour.
"""
import cv2
import numpy as np


def colour_mask(a, cols, tol=60):
    """Pixels within L1 distance tol of any of the RGB colours cols."""
    a = a.astype(int)
    m = np.zeros(a.shape[:2], bool)
    for c in cols:
        m |= np.abs(a - np.array(c)).sum(2) < tol
    return m


def find_markers(mask, region, k=7, min_area=100):
    """Connected blobs left after a k x k opening (lines and bars vanish, squares stay). region=(r0,r1,c0,c1)."""
    r0, r1, c0, c1 = region
    m = np.zeros(mask.shape, np.uint8)
    m[r0:r1, c0:c1] = mask[r0:r1, c0:c1]
    o = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(o)
    out = []
    for s, c in zip(st[1:], cen[1:]):
        if s[4] >= min_area:
            out.append(dict(x0=int(s[0]), y0=int(s[1]), w=int(s[2]), h=int(s[3]), cx=float(c[0]), cy=float(c[1])))
    return sorted(out, key=lambda d: d["cx"])


def centre(mask, mk, half=6, need=10):
    """Marker centre: x = middle of the blob's columns; y = middle of the run of rows (through the blob) in which
    >= need of the 2*half+1 pixels around x are set (square plus any caps touching it; bars are symmetric)."""
    cx = mk["x0"] + (mk["w"] - 1) / 2
    ci = int(round(cx))
    full = mask[:, ci - half:ci + half + 1].sum(1) >= need
    r = int(round(mk["cy"]))
    if not full[r]:
        return cx, mk["cy"], mk["y0"], mk["y0"] + mk["h"] - 1
    top = r
    while top > 0 and full[top - 1]:
        top -= 1
    bot = r
    while bot < len(full) - 1 and full[bot + 1]:
        bot += 1
    return cx, (top + bot) / 2, top, bot


def error_bar(mask, cx, cy, top, bot, frame_top, frame_bot, bar_half=1, cap_half=13, cap_need=18, gap=1, window=None):
    """Follow the bar column up and down from the marker centre (through the square); caps are rows where
    >= cap_need of the 2*cap_half+1 pixels around x are set (the square is narrower, ~14 px). Returns
    {'upper': (cap centre row or None, clipped), 'lower': ...}; clipped = the bar runs into the frame."""
    ci = int(round(cx))
    col = mask[:, ci - bar_half:ci + bar_half + 1].any(1)
    cap = mask[:, ci - cap_half:ci + cap_half + 1].sum(1) >= cap_need

    def walk(start, step, limit):
        r, last, miss = start, start, 0
        while 0 <= r + step < mask.shape[0] and (r + step - limit) * step <= 0:
            r += step
            if col[r]:
                last, miss = r, 0
            else:
                miss += 1
                if miss > gap:
                    break
        return last

    c = int(round(cy))
    if window is None:
        up = walk(c, -1, frame_top)
        dn = walk(c, 1, frame_bot)
    else:   # icon markers: the zigzag interrupts the bar column; search a fixed window instead
        up = max(frame_top, c - window)
        dn = min(frame_bot, c + window)
    res = {}
    for name, lo, hi in (("upper", up, c - 1), ("lower", c + 1, dn)):
        groups = []
        for r in range(lo, hi + 1):
            if cap[r]:
                if groups and r == groups[-1][-1] + 1:
                    groups[-1].append(r)
                else:
                    groups.append([r])
        end = up if name == "upper" else dn
        clipped = ((end <= frame_top + 1) if name == "upper" else (end >= frame_bot - 1)) and window is None
        if groups:
            gsel = (groups[-1] if name == "upper" else groups[0]) if window else (groups[0] if name == "upper" else groups[-1])
            res[name] = (float(np.mean(gsel)), clipped)
        else:
            res[name] = (None, clipped)
    return res


def tick_centres(g, rows, cols, axis, thr=200):
    """Darkness-weighted centres of tick marks in a band: axis='x' gives column centres (band rows x cols),
    axis='y' gives row centres."""
    band = np.clip(255 - g[rows[0]:rows[1], cols[0]:cols[1]], 0, None)
    band[band < 255 - thr] = 0
    prof = band.sum(0 if axis == "x" else 1)
    idx = np.where(prof > 0.5 * prof.max())[0]
    groups = []
    for i in idx:
        if groups and i == groups[-1][-1] + 1:
            groups[-1].append(i)
        else:
            groups.append([i])
    off = cols[0] if axis == "x" else rows[0]
    return [off + float(np.average(gr, weights=prof[gr])) for gr in groups]


def icon_centre(mask, mk, search=30, half=6, need=6, bar_need=2):
    """Centre of a square marker overprinted with a white zigzag icon (the opening keeps only part of it).

    x = the bar column: the column (within +-10 px of the blob) set most often in the `search` rows above and
    below the blob that are not cap rows; y = middle of the run of rows around the blob with >= need of the
    2*half+1 pixels around x set and that are not cap rows (>= 18 of 27)."""
    r0, r1 = mk["y0"], mk["y0"] + mk["h"] - 1
    c_lo, c_hi = int(mk["x0"]) - 10, int(mk["x0"] + mk["w"]) + 10
    rows = list(range(max(0, r0 - search), r0)) + list(range(r1 + 1, min(mask.shape[0], r1 + 1 + search)))
    best, bc = -1, None
    for c in range(c_lo, c_hi):
        n = sum(1 for r in rows if mask[r, c] and mask[r, c - 13:c + 14].sum() < 18 and mask[r, c - 4:c + 5].sum() <= bar_need + 2)
        if n > best:
            best, bc = n, c
    # the bar is ~3 px wide: centre of the set columns around bc in those rows
    cols = [c for c in range(bc - 2, bc + 3)
            if sum(1 for r in rows if mask[r, c]) >= 0.6 * best]
    cx = float(np.mean(cols))
    ci = int(round(cx))
    cov = mask[:, ci - half:ci + half + 1].sum(1)
    cap = mask[:, ci - 13:ci + 14].sum(1) >= 18
    ok = (cov >= need) & ~cap
    r = int(round(mk["cy"]))
    while not ok[r] and r < r1:
        r += 1
    top = bot = r
    while top > 0 and ok[top - 1]:
        top -= 1
    while bot < mask.shape[0] - 1 and ok[bot + 1]:
        bot += 1
    return cx, (top + bot) / 2, top, bot
