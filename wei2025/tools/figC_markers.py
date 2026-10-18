"""Helpers for digitizing the Origin line+marker panels of wei2025 Figs. 11 and 13 (fork C).

Each panel: a black axis frame, outward tick marks on the bottom and left axes, three series
(Fx black open squares, Fy red filled circles, Fz magenta open triangles) joined by dashed lines.
The markers are the data samples. They are located by normalized cross-correlation of a colour
mask with a template cut from the panel's own legend marker, plus non-maximum suppression.
All coordinates are pixels of the 300 ppi embedded image (x = column, y = row).
"""
import numpy as np


def colour_masks(a):
    """Boolean masks (black, red, magenta) of an RGB uint8 image."""
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    black = (mx < 120) & (mx - mn < 45)
    red = (r > 150) & (g < 120) & (b < 120) & (r - g > 90)
    magenta = (r > 150) & (b > 150) & (g < 140) & (r - g > 70) & (b - g > 70)
    return black, red, magenta


def runs(v):
    """(start, end_exclusive) of True runs in a 1-D bool array."""
    d = np.diff(np.r_[0, v.astype(int), 0])
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def find_frame(dark, x0, x1, y0, y1, min_len=0.8):
    """Axis box inside the search window: returns (top, bottom, left, right) as centre rows/cols
    of the frame lines, and their (first,last) index pairs."""
    sub = dark[y0:y1, x0:x1]
    W, H = x1 - x0, y1 - y0
    rows = np.where(sub.sum(1) >= min_len * W * 0.75)[0]
    cols = np.where(sub.sum(0) >= min_len * H * 0.75)[0]

    def groups(idx):
        gs = []
        for i in idx:
            if gs and i <= gs[-1][1] + 1:
                gs[-1][1] = i
            else:
                gs.append([i, i])
        return gs
    gr, gc = groups(rows), groups(cols)
    top, bot = gr[0], gr[-1]
    left, right = gc[0], gc[-1]
    tb = (y0 + top[0], y0 + top[1]), (y0 + bot[0], y0 + bot[1])
    lr = (x0 + left[0], x0 + left[1]), (x0 + right[0], x0 + right[1])
    return tb, lr


def ticks_bottom(dark, bot, left, right, length=4, frac=0.99):
    """Inward tick marks on the bottom frame line (bot = (first,last) rows): list of
    (centre column, tick length in px). Ticks point up into the plot."""
    out = []
    band = dark[bot[0] - length:bot[0], left[1] + 1:right[0]]
    full = band.mean(0) >= frac
    for s, e in runs(full):
        c = left[1] + 1 + (s + e - 1) / 2
        n = 0
        while dark[bot[0] - 1 - n, int(round(c))]:
            n += 1
        out.append((c, n))
    return out


def ticks_left(dark, left, top, bot, length=4, frac=0.99):
    """Inward tick marks on the left frame line (left = (first,last) cols): list of
    (centre row, tick length in px). Ticks point right into the plot."""
    out = []
    band = dark[top[1] + 1:bot[0], left[1] + 1:left[1] + 1 + length]
    full = band.mean(1) >= frac
    for s, e in runs(full):
        r = top[1] + 1 + (s + e - 1) / 2
        n = 0
        while dark[int(round(r)), left[1] + 1 + n]:
            n += 1
        out.append((r, n))
    return out


def ncc(mask, tpl):
    """Normalized cross-correlation of a float mask with a template (same-size output, 'valid' padded)."""
    import cv2
    m = mask.astype(np.float32)
    t = tpl.astype(np.float32)
    res = cv2.matchTemplate(m, t, cv2.TM_CCOEFF_NORMED)
    out = np.full(mask.shape, -1.0, np.float32)
    th, tw = t.shape
    out[th // 2:th // 2 + res.shape[0], tw // 2:tw // 2 + res.shape[1]] = res
    return out


def peaks(score, thr, min_dist):
    """Local maxima of score above thr, greedy non-maximum suppression with radius min_dist.
    Returns list of (row, col, score)."""
    ys, xs = np.where(score >= thr)
    order = np.argsort(-score[ys, xs])
    taken = []
    for i in order:
        y, x = ys[i], xs[i]
        if all((y - ty) ** 2 + (x - tx) ** 2 >= min_dist ** 2 for ty, tx, _ in taken):
            taken.append((y, x, float(score[y, x])))
    return taken


def centroid_refine(mask, y, x, r):
    """Centroid of mask pixels in a (2r+1) box around (y, x); falls back to (y, x)."""
    sub = mask[y - r:y + r + 1, x - r:x + r + 1]
    yy, xx = np.nonzero(sub)
    if len(yy) == 0:
        return float(y), float(x)
    return float(y - r + yy.mean()), float(x - r + xx.mean())


# ---------------------------------------------------------------- templates
def template(kind):
    """Binary marker templates (1 = ink), with a 2 px empty border so that dashes score lower.
    Sizes measured on the legend markers of Fig. 11a (300 ppi): open square 6x6 px with a 2x2 hole,
    filled circle ~8x7 px, open triangle 7 px tall and 13 px wide at the base."""
    if kind == "square":
        t = np.zeros((10, 10))
        t[2:8, 2:8] = 1
        t[4:6, 4:6] = 0
    elif kind == "circle":
        yy, xx = np.mgrid[:10, :10]
        t = (((yy - 4.5) / 3.3) ** 2 + ((xx - 4.5) / 3.8) ** 2 <= 1).astype(float)
    elif kind == "triangle":
        t = np.zeros((11, 13))
        for i in range(7):
            half = 1 + i * 0.75
            t[2 + i, int(round(6 - half)):int(round(6 + half)) + 1] = 1
        t[4:8, 5:8] = 0
        t[6:8, 4:9] = 0
        t[5, 6] = 0
    else:
        raise ValueError(kind)
    return t


def calibrate(ticks, first, step, min_len=7):
    """Linear pixel->value map from the major ticks (length >= min_len px), labelled first,
    first+step, ... in pixel order. Returns (f, labels, positions, max residual, slope)."""
    from digitize_common import fit_axis
    pos = [p for p, n in ticks if n >= min_len]
    labels = [first + i * step for i in range(len(pos))]
    f, res, slope = fit_axis(pos, labels)
    return f, labels, pos, res, slope


def inv(f):
    """Inverse of a linear map p -> value (returns value -> pixel)."""
    v0, v1 = float(f(0.0)), float(f(1.0))
    return lambda v: (np.asarray(v, float) - v0) / (v1 - v0)


def subpixel(score, y, x):
    """Parabolic sub-pixel refinement of a score maximum at (y, x)."""
    def par(a, b, c):
        d = a - 2 * b + c
        return 0.0 if d >= 0 else 0.5 * (a - c) / d
    dy = par(score[y - 1, x], score[y, x], score[y + 1, x])
    dx = par(score[y, x - 1], score[y, x], score[y, x + 1])
    return y + float(np.clip(dy, -0.5, 0.5)), x + float(np.clip(dx, -0.5, 0.5))


SERIES = (("Fx", 0, "square"), ("Fy", 1, "circle"), ("Fz", 2, "triangle"))


def ink_maps(a):
    """Continuous ink strength (0-255) per series colour: (black, red, magenta)."""
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(2), a.min(2)
    black = np.where(mx - mn < 60, 255 - mx, 0).clip(0, 255)
    red = (r - np.maximum(g, b)).clip(0, 255)
    magenta = (np.minimum(r, b) - g).clip(0, 255)
    return [m.astype(np.float32) for m in (black, red, magenta)]


def hole_ring(T):
    """Boolean masks of the open centre (hole) and the ink ring of a learned open-marker template."""
    from scipy import ndimage
    ink = T > 0.5 * T.max()
    filled = ndimage.binary_fill_holes(ink)
    hole = filled & ~ink & (T < 0.35 * T.max())
    if hole.sum() == 0:      # hole not closed in the template: take the darkest pixels inside the ink bbox
        ys, xs = np.nonzero(ink)
        sub = T[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        thr = np.percentile(sub, 15)
        hole = np.zeros_like(ink)
        hole[ys.min() + 1:ys.max(), xs.min() + 1:xs.max()] = T[ys.min() + 1:ys.max(), xs.min() + 1:xs.max()] <= thr
    return hole, ink


def extract_panel(a, cfg, templates=None, thr_detect=0.55, thr_keep=0.3, win=3, H=6):
    """Digitize one panel. cfg keys: search (x0,x1,y0,y1) window holding the panel frame;
    xfirst, xstep, nx, yfirst, ystep, ny (label of the first major tick from the left / from the top,
    label step, number of major ticks); legend_lines (box of the three legend lines, excluded for all
    series); black_boxes (boxes of legend and annotation text, excluded for Fx). Boxes: (x0, y0, x1, y1) px.

    Two passes per series: (1) synthetic binary template on the colour mask, strong peaks (>= 0.6)
    give a learned template (mean ink patch, 13 x 13 px); (2) the learned template on the continuous
    ink map, searched at each integer-angstrom sample column (+-win px). The marker position is the
    score maximum (sub-pixel) shifted by the ink centroid of the learned template (spec: centre of the
    template's ink). Returns calibration info, rows (series, x_nominal, x_measured, y, score, flag)."""
    masks = colour_masks(a)
    inks = ink_maps(a)
    black = masks[0]
    x0, x1, y0, y1 = cfg["search"]
    (top, bot), (left, right) = find_frame(black, x0, x1, y0, y1)
    tb = ticks_bottom(black, bot, left, right)
    tl = ticks_left(black, left, top, bot)
    fx, xl, xp, xres, xs = calibrate(tb, cfg["xfirst"], cfg["xstep"])
    fy, yl, yp, yres, ys = calibrate(tl, cfg["yfirst"], cfg["ystep"])
    assert len(xl) == cfg["nx"] and len(yl) == cfg["ny"], (len(xl), len(yl), xp, yp)
    gx = inv(fx)
    ix0, ix1, iy0, iy1 = left[1] + 1, right[0], top[1] + 1, bot[0]

    def valid_mask(shape, name):
        v = np.zeros(shape, bool)
        v[iy0:iy1, ix0:ix1] = True
        lx0, ly0, lx1, ly1 = cfg["legend_lines"]
        v[ly0:ly1, lx0:lx1] = False
        if name == "Fx":
            for bx0, by0, bx1, by1 in cfg["black_boxes"]:
                v[by0:by1, bx0:bx1] = False
            v[iy1 - 12:iy1, :] = False          # tick marks on the bottom axis
            v[:, ix0:ix0 + 12] = False          # tick marks on the left axis
        return v

    scores, offsets, fr, xsamp, ntpl, tlist = [], [], [], [], {}, []
    for name, mi, kind in SERIES:
        vm = valid_mask(a.shape[:2], name)
        if templates is None:
            s1 = ncc(masks[mi], template(kind))
            s1[~vm] = -1
            strong = [(r, c) for r, c, v in peaks(s1, 0.6, 5)
                      if H <= r < a.shape[0] - H and H <= c < a.shape[1] - H]
            ntpl[name] = len(strong)
            if cfg.get("learn_only"):
                tlist.append([inks[mi][r - H:r + H + 1, c - H:c + H + 1] for r, c in strong])
                continue
            T = np.mean([inks[mi][r - H:r + H + 1, c - H:c + H + 1] for r, c in strong], 0)
        else:
            T = templates[name]
        s = ncc(inks[mi], T)
        s[~vm] = -1
        if kind == "circle":
            # filled circles (6-8 px) survive a morphological opening with a 4 px disk, the 4 px thick
            # dashes do not: only allow match centres on (or 1 px next to) what survives
            import cv2
            ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
            op = cv2.morphologyEx(masks[mi].astype(np.uint8), cv2.MORPH_OPEN, ker)
            op = cv2.dilate(op, np.ones((3, 3), np.uint8)).astype(bool)
            s[~op] = -1
        w = np.where(T > 0.5 * T.max(), T, 0)
        yy, xx = np.mgrid[:T.shape[0], :T.shape[1]]
        offsets.append(((yy * w).sum() / w.sum() - (T.shape[0] // 2), (xx * w).sum() / w.sum() - (T.shape[1] // 2)))
        scores.append(s)
        tlist.append(T)
        for r, c, v in peaks(s, 0.65, 4):
            x = float(fx(c + offsets[-1][1]))
            xsamp.append(round(x))
    if cfg.get("learn_only"):
        return dict(patches=dict(zip([n for n, _, _ in SERIES], tlist)))
    xmin, xmax = min(xsamp), max(xsamp)
    rows = []
    for (name, mi, kind), s, (oy, ox), T in zip(SERIES, scores, offsets, tlist):
        hole, ring = hole_ring(T) if kind != "circle" else (None, None)
        th, tw = T.shape
        for xn in range(xmin, xmax + 1):
            c = int(round(float(gx(xn))))
            sub = s[:, c - win:c + win + 1]
            r, cc = np.unravel_index(np.argmax(sub), sub.shape)
            v = float(sub[r, cc])
            cc += c - win
            if v < thr_keep:
                rows.append((name, xn, np.nan, np.nan, v, "not found (marker hidden or merged)"))
                continue
            flag = "" if v >= thr_detect else "weak match"
            if flag and hole is not None:
                P = inks[mi][r - th // 2:r - th // 2 + th, cc - tw // 2:cc - tw // 2 + tw]
                hy, hx = [int(round(v)) for v in np.argwhere(hole).mean(0)]
                if P.shape == T.shape and P[hy - 1:hy + 2, hx - 1:hx + 2].min() < 0.35 * P[ring].mean():
                    flag += " (open centre of the marker confirmed)"
                else:
                    rows.append((name, xn, np.nan, np.nan, v, "not found (weak match without an open marker centre: on a dash or hidden)"))
                    continue
            ry, rx = subpixel(s, r, cc)
            ry, rx = ry + oy, rx + ox
            if flag and abs(float(fx(rx)) - xn) > 0.2:
                rows.append((name, xn, np.nan, np.nan, v, "not found (weak match more than 0.2 A off the sample position: on a dash)"))
                continue
            if ry <= iy0 + 4:
                flag = (flag + "; " if flag else "") + "at top frame (may be clipped)"
            rows.append((name, xn, float(fx(rx)), float(fy(ry)), v, flag))
            if v >= 0.65:
                fr.append(float(fx(rx)) - xn)
    fr = np.array(fr)
    return dict(frame=(top, bot, left, right), xcal=(xl, xp, xres, xs), ycal=(yl, yp, yres, ys),
                fx=fx, fy=fy, frac=fr, xrange=(xmin, xmax), rows=rows, ntpl=ntpl, offsets=offsets)


def run_figure(pdf, page, bbox, fig, panels, captions, work, outdir, run_label):
    """Digitize all panels of one embedded image; write <outdir>/<fig><p>.csv and
    <work>/<fig><p>_overlay.png. Returns {panel: result}."""
    from digitize_common import embedded_image, write_csv, overlay
    a = embedded_image(str(pdf), page, bbox_near=bbox)
    work.mkdir(parents=True, exist_ok=True)
    pooled = {n: [] for n, _, _ in SERIES}
    for p, cfg in panels.items():
        for n, pl in extract_panel(a, dict(cfg, learn_only=True))["patches"].items():
            pooled[n] += pl
    templates = {n: np.mean(pl, 0) for n, pl in pooled.items()}
    ntpl = {n: len(pl) for n, pl in pooled.items()}
    out = {}
    for p, cfg in panels.items():
        res = extract_panel(a, cfg, templates)
        res["ntpl"] = ntpl
        top, bot, left, right = res["frame"]
        xl, xp, xres, xs = res["xcal"]
        yl, yp, yres, ys = res["ycal"]
        fx, fy = res["fx"], res["fy"]
        fr = res["frac"]
        frame_vals = (float(fx((left[0] + left[1]) / 2)), float(fx((right[0] + right[1]) / 2)),
                      float(fy((bot[0] + bot[1]) / 2)), float(fy((top[0] + top[1]) / 2)))
        n_found = {s: sum(1 for r in res["rows"] if r[0] == s and r[2] == r[2]) for s, _, _ in SERIES}
        n_tot = res["xrange"][1] - res["xrange"][0] + 1
        hdr = [
            f"wei2025 (Wei et al. 2025, Int J Numer Anal Methods Geomech 49:2949-2964), Figure {fig[3:]}({p}): {captions[p]}",
            "Columns: series = Fx, Fy or Fz (legend names; force on the indenter along x, y, z);",
            "  x_nominal_A = sliding distance of the sample in angstrom, snapped to the integer-angstrom sampling grid (see below);",
            "  x_measured_A = sliding distance of the located marker centre (angstrom); force_nN = marker centre in nN;",
            "  match_score = normalized cross-correlation of the marker template (0-1); flag = notes.",
            "Provenance: tier 3, digitized from the 300 ppi embedded raster image (PDF p. %d; no vector data) by %s_extract.py." % (page, fig),
            "  Markers (Fx open black squares, Fy filled red circles, Fz open magenta triangles) located by template matching:",
            "  a template learned from the clearly matched markers of all panels of this figure (%s) is correlated with the colour's ink map;" % ", ".join(f"{k} {v}" for k, v in res["ntpl"].items()),
            "  marker position = correlation maximum shifted to the template's ink centroid. Fy circles: only positions that survive a",
            "  morphological opening of the red mask with a 4 px disk (removes the dashes, keeps the filled circles) are allowed.",
            "  The dashed lines joining the markers are not given separately: they are straight segments through the markers or",
            "  (in some panels) smoothed curves passing near them, so they carry no extra data.",
            f"  x axis calibrated on {len(xp)} labelled major ticks ({xl[0]:g}..{xl[-1]:g}): max residual {xres:.3f} A; "
            f"frame check: left/right frame at {frame_vals[0]:.2f}/{frame_vals[1]:.2f} A.",
            f"  y axis calibrated on {len(yp)} labelled major ticks ({yl[0]:g}..{yl[-1]:g}): max residual {yres:.3f} nN; "
            f"frame check: bottom/top frame at {frame_vals[2]:.2f}/{frame_vals[3]:.2f} nN.",
            f"Sampling: the {len(fr)} confidently matched markers (score >= 0.65) sit at integer angstrom (offset from the integer: "
            f"rms {np.sqrt(np.mean(fr ** 2)):.3f} A, max {np.max(np.abs(fr)):.3f} A),",
            f"  so one sample per 1 A from {res['xrange'][0]} to {res['xrange'][1]} A ({run_label}) is assumed and each series is searched at each.",
            f"Markers found: Fx {n_found['Fx']}, Fy {n_found['Fy']}, Fz {n_found['Fz']} of {n_tot} each; rows without a value "
            "are samples whose marker is hidden by another series or merged with the dashed line (not found).",
            f"Uncertainty: about +-{1.5 * abs(ys):.2f} nN in force (1.5 px; 1 px = {abs(ys):.3f} nN) and +-{1.5 * abs(xs):.2f} A in x_measured.",
            "  'weak match' rows (score 0.30-0.55: marker partly covered by a dash or another marker; open markers kept only if their open",
            "  centre is seen and the match lies within 0.2 A of the sample position) are less certain; they are cyan on the overlay",
            "  work/%s%s_overlay.png (other markers: green Fx, blue Fy, orange Fz)." % (fig, p),
            "  'at top frame' rows: the marker touches the top of the plot frame and may be cut off there (value is a lower bound).",
        ]
        hdr += cfg.get("notes", [])
        rows = [(s, xn, xm, y, v, fl) for s, xn, xm, y, v, fl in res["rows"]]
        write_csv(str(outdir / f"{fig}{p}.csv"), hdr,
                  ["series", "x_nominal_A", "x_measured_A", "force_nN", "match_score", "flag"], rows,
                  fmt=["{}", "{}", "{:.2f}", "{:.3f}", "{:.2f}", "{}"])
        cols = {"Fx": (0, 200, 0), "Fy": (0, 120, 255), "Fz": (255, 160, 0)}
        im = a.copy()
        for (s, xn, xm, y, v, fl) in res["rows"]:
            if y == y:
                cx, cy = float(inv(fx)(xm)), float(inv(fy)(y))
                xi, yi = int(round(cx)), int(round(cy))
                im[yi - 1:yi + 2, xi - 1:xi + 2] = (0, 230, 230) if "weak" in fl else cols[s]
        x0, x1, y0, y1 = cfg["search"]
        from PIL import Image
        Image.fromarray(im[y0:y1, x0:x1]).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.NEAREST).save(
            str(work / f"{fig}{p}_overlay.png"))
        print(fig + p, "x", xl[0], xl[-1], "res %.3f" % xres, "frame", ["%.2f" % v for v in frame_vals],
              "y res %.3f" % yres, "range", res["xrange"], "found", n_found, "frac rms %.3f max %.3f" % (np.sqrt(np.mean(fr ** 2)), np.abs(fr).max()))
        out[p] = res
    return out
