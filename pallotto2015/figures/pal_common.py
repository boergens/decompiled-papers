"""Shared helpers for the pallotto2015 extraction scripts (tier 3 digitizing and source-data reading).

Images: main-text figures are the embedded 300-ppi JPEGs of elife-08206-v3.pdf (read with
tools/digitize_common.embedded_image); figure supplements are the full-size eLife JPEGs in
papers/pallotto2015/elife_figure_supplements/ (identical pixel size to the images embedded in
elife-08206-figures-v3.pdf). All pixel coordinates in the extraction scripts refer to these images.
"""
import os, sys, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # sep_28__osmium_chemistry
PAPER = os.path.join(ROOT, "papers", "pallotto2015")
TOOLS = os.path.join(ROOT, "decompiled", "tools")
WORK = os.path.join(HERE, "..", "work")
sys.path.insert(0, TOOLS)
from digitize_common import embedded_image, write_csv, fit_axis  # noqa: E402

MAIN_PDF = os.path.join(PAPER, "elife-08206-v3.pdf")
MAIN_PAGES = {"fig1": 3, "fig2": 5, "fig3": 7, "fig4": 9, "fig5": 10}
SUPP = os.path.join(PAPER, "elife_figure_supplements")


def load(name):
    """RGB uint8 array of a figure: 'fig1'..'fig5' (main PDF) or e.g. 'fig1-figsupp1' (eLife JPEG)."""
    if name in MAIN_PAGES:
        return embedded_image(MAIN_PDF, MAIN_PAGES[name])
    from PIL import Image
    return np.array(Image.open(os.path.join(SUPP, f"elife-08206-{name}-v3.jpg")).convert("RGB"))


class Axis:
    """Linear (or log10) pixel->value map fitted on tick marks: Axis([(pix, val), ...], log=False)."""
    def __init__(self, ticks, log=False):
        p, v = zip(*ticks)
        self.f, self.res, self.m = fit_axis(p, v, log)
        self.log = log
        self.ticks = ticks
        lv = np.log10(v) if log else np.asarray(v, float)
        self.b = np.mean(lv - self.m * np.asarray(p, float))

    def __call__(self, pix):
        return self.f(pix)

    def inv(self, val):
        lv = np.log10(val) if self.log else np.asarray(val, float)
        return (lv - self.b) / self.m

    def describe(self, name):
        t = ", ".join(f"{v:g}@{p:g}px" for p, v in self.ticks)
        return f"{name} axis ({'log10' if self.log else 'linear'}) fitted on ticks {t}; max residual {self.res:.3g} {'decades' if self.log else 'axis units'}"


def grey_ring_mask(a, lo=90, hi=225, sat=30):
    """Pixels of light-grey markers: unsaturated, between lo and hi grey level."""
    a = a.astype(int)
    g = a.mean(2)
    s = a.max(2) - a.min(2)
    return (g > lo) & (g < hi) & (s < sat)


def red_mask(a):
    a = a.astype(int)
    return (a[..., 0] > 180) & (a[..., 1] < 110) & (a[..., 2] < 110)


def ring_template(r, w=2.0, size=None):
    size = size or int(2 * r + 2 * w + 3)
    c = (size - 1) / 2
    yy, xx = np.mgrid[:size, :size]
    d = np.hypot(xx - c, yy - c)
    return (np.abs(d - r) <= w / 2 + 0.5).astype(np.float32), c


def match_peaks(img, templ, c, region, thr, nms):
    """Normalised cross-correlation peaks of templ in img (float32) within region (x0,y0,x1,y1)."""
    import cv2
    x0, y0, x1, y1 = region
    R = cv2.matchTemplate(img[y0:y1, x0:x1].astype(np.float32), templ.astype(np.float32), cv2.TM_CCOEFF_NORMED)
    out = []
    R2 = R.copy()
    while True:
        i = np.unravel_index(np.argmax(R2), R2.shape)
        if R2[i] < thr:
            break
        out.append((x0 + i[1] + c, y0 + i[0] + c, float(R2[i])))
        R2[max(0, i[0] - nms):i[0] + nms + 1, max(0, i[1] - nms):i[1] + nms + 1] = -1
    return out


def refine(img, templ, c, approx, search=4):
    """Best template position within +-search px of each approximate centre: [(x, y, score)]."""
    import cv2
    out = []
    size = templ.shape[0]
    for x, y in approx:
        x0, y0 = int(round(x - c - search)), int(round(y - c - search))
        sub = img[y0:y0 + size + 2 * search, x0:x0 + size + 2 * search].astype(np.float32)
        R = cv2.matchTemplate(sub, templ.astype(np.float32), cv2.TM_CCOEFF_NORMED)
        i = np.unravel_index(np.argmax(R), R.shape)
        out.append((x0 + i[1] + c, y0 + i[0] + c, float(R[i])))
    return out


def draw(a, pts, out_png, colour=(255, 0, 255), r=2, lines=None):
    """Overlay: small squares at points (pixel coords), optional polylines [(pts, colour)]."""
    from PIL import Image, ImageDraw
    im = Image.fromarray(a.copy())
    d = ImageDraw.Draw(im)
    for x, y in pts:
        if x == x and y == y:
            d.rectangle([x - r, y - r, x + r, y + r], outline=colour)
    for pl, col in (lines or []):
        d.line([tuple(p) for p in pl], fill=col, width=1)
    im.save(out_png)


def read_csv(path):
    rows = [r for r in csv.reader(l for l in open(path, encoding="utf-8") if not l.startswith("#"))]
    head, body = rows[0], rows[1:]
    return [dict(zip(head, r)) for r in body]


# ---- colour masks for the MATLAB-default blue/orange series (Figs 3, 3-s1) ----
def blue_line(a):
    a = a.astype(int)
    return (a[..., 2] > 150) & (a[..., 0] < 70) & (a[..., 1] > 60) & (a[..., 1] < 150)


def orange_line(a):
    a = a.astype(int)
    return (a[..., 0] > 170) & (a[..., 1] < 120) & (a[..., 2] < 70)


def blue_band(a):
    a = a.astype(int)
    return (a[..., 0] > 90) & (a[..., 0] < 200) & (a[..., 1] > 165) & (a[..., 1] < 222) & (a[..., 2] > 200)


def orange_band(a):
    a = a.astype(int)
    return (a[..., 0] > 210) & (a[..., 1] > 140) & (a[..., 1] < 210) & (a[..., 2] > 110) & (a[..., 2] < 195)


def runs(col_bool, gap=2):
    idx = np.where(col_bool)[0]
    if not len(idx):
        return []
    return np.split(idx, np.where(np.diff(idx) > gap)[0] + 1)


def polyline_vertices(mask, xs, y0, y1, margin=4, min_cols=3):
    """Vertices of a polyline whose corners sit at the columns xs (category ticks).

    For each segment [xs[i], xs[i+1]] the centre of the mask run in every interior column (margin px
    away from both vertices) is fitted with a straight line; a vertex is the mean of the two adjacent
    segment fits evaluated at its column (one fit at the ends). Returns (y_vertex, n_segments_used)
    per x; NaN where the series is hidden.
    """
    fits = []
    for i in range(len(xs) - 1):
        cs, ys = [], []
        prev = None
        for c in range(int(np.ceil(xs[i] + margin)), int(np.floor(xs[i + 1] - margin)) + 1):
            rr = runs(mask[y0:y1, c])
            if not rr:
                continue
            r = max(rr, key=len) if prev is None else min(rr, key=lambda q: abs(q.mean() - prev))
            cs.append(c)
            ys.append(y0 + r.mean())
            prev = r.mean()
        fits.append(np.polyfit(cs, ys, 1) if len(cs) >= min_cols else None)
    out = []
    for i, x in enumerate(xs):
        v = [np.polyval(f, x) for f in (fits[i - 1] if i > 0 else None, fits[i] if i < len(fits) else None) if f is not None]
        out.append((np.mean(v) if v else np.nan, len(v)))
    return out


def band_extent(band, line, x, y_centre, y0, y1, reach=40):
    """Top and bottom rows of the shaded band (band tint or line colour, contiguous) in column x around y_centre."""
    col = (band[y0:y1, int(round(x))] | line[y0:y1, int(round(x))])
    for r in runs(col, gap=1):
        if y0 + r[0] - 2 <= y_centre <= y0 + r[-1] + 2:
            return y0 + r[0], y0 + r[-1]
    return np.nan, np.nan


def trace_curve(mask, x0, x1, y0, y1, seed_y, min_len=2, tol=8, tol_per_col=0.3):
    """Follow one line through the columns [x0, x1): in each column take the mask run nearest to a linear
    prediction from the last 6 accepted columns (starting at seed_y); runs further than
    tol + tol_per_col * (skipped columns) are rejected (another curve, or this one hidden).
    Returns [(column, centre row)]."""
    prev, lastc, slope = seed_y - y0, x0, 0.0
    hist = []
    for c in range(x0, x1):
        rr = runs(mask[y0:y1, c])
        if not rr:
            continue
        pred = prev + slope * (c - lastc)
        r = min(rr, key=lambda q: abs(q.mean() - pred))
        if len(r) < min_len or abs(r.mean() - pred) > tol + tol_per_col * (c - lastc):
            continue
        hist.append((c, r.mean()))
        if len(hist) >= 6:
            slope = np.polyfit(*zip(*hist[-6:]), 1)[0]
        prev, lastc = r.mean(), c
    return [(c, y0 + y) for c, y in hist]


def trace_both(mask, x0, x1, y0, y1, seed_x, seed_y, **kw):
    """trace_curve forward from (seed_x, seed_y) to x1 and backward to x0; sorted [(column, row)]."""
    fwd = trace_curve(mask, seed_x, x1, y0, y1, seed_y, **kw)
    flip = mask[:, ::-1]
    W = mask.shape[1]
    bwd = trace_curve(flip, W - 1 - seed_x, W - x0, y0, y1, seed_y, **kw)
    bwd = [(W - 1 - c, y) for c, y in bwd]
    pts = {c: y for c, y in bwd + fwd}
    return sorted(pts.items())
