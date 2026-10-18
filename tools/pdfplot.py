"""pdfplot.py -- helpers for recovering figure content from a vector PDF page with PyMuPDF.

Typical use for one plot panel:

    import pdfplot as pp
    page = pp.open_page(PDF, 36)                 # 1-based page number
    clip = pp.R(380, 15, 520, 105)               # panel bounding box in PDF points (origin top-left, y down)
    pp.render(page, clip, 300, "fig2c_orig.png") # crop of the original, for side-by-side QA
    spans = pp.text_spans(page, clip)            # tick labels, axis labels, legend text ...
    draws = pp.drawings(page, clip)              # strokes / fills, with flattened point lists
    xax = pp.axis_from_labels(spans, draws, "x") # pixel -> data mapping from numeric tick labels (+ tick marks)
    yax = pp.axis_from_labels(spans, draws, "y")
    for d in draws:
        if d["kind"] == "stroke" and len(d["points"]) > 20:
            xy = [(xax(x), yax(y)) for x, y in d["points"]]

Everything is in PDF points (1/72 inch), origin at the top-left of the page, y increasing downwards.
Colors are (r, g, b) floats in 0..1, or None.
"""
import csv
import math
import re

import fitz  # PyMuPDF

R = fitz.Rect


def open_page(pdf, pno):
    """Return page `pno` (1-based) of `pdf`."""
    doc = fitz.open(pdf)
    return doc[pno - 1]


# ---------------------------------------------------------------- text

def text_spans(page, clip=None):
    """All text spans in `clip` (or the whole page).

    Each span: dict(text, bbox=(x0,y0,x1,y1), cx, cy, size, color=(r,g,b), font, dir=(cos,sin)).
    dir == (1,0) is horizontal text, (0,-1) is text rotated 90 deg counter-clockwise (y axis labels).
    """
    out = []
    d = page.get_text("dict", clip=clip)
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                if not s["text"].strip():
                    continue
                x0, y0, x1, y1 = s["bbox"]
                c = s["color"]
                out.append(dict(
                    text=s["text"], bbox=(x0, y0, x1, y1),
                    cx=(x0 + x1) / 2, cy=(y0 + y1) / 2,
                    size=s["size"], font=s["font"],
                    color=((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255),
                    dir=tuple(l["dir"]),
                ))
    return out


_num_re = re.compile(r"^[-−–]?\d+(\.\d+)?$")


def parse_number(text):
    """Parse a tick label like '-1', '0.5', '10^-3', '10−3' (superscript lost), '−0.5'. Returns float or None."""
    t = text.strip().replace("−", "-").replace("–", "-").replace(",", "")
    if _num_re.match(t):
        return float(t)
    m = re.match(r"^10\^?(-?\d+)$", t)
    if m:
        return 10.0 ** int(m.group(1))
    return None


# ---------------------------------------------------------------- drawings

def _bezier(p0, p1, p2, p3, n=12):
    pts = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        x = u ** 3 * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t ** 3 * p3.x
        y = u ** 3 * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t ** 3 * p3.y
        pts.append((x, y))
    return pts


def drawings(page, clip=None, how="intersects"):
    """Vector drawings on the page, optionally restricted to `clip`.

    how="intersects": keep paths whose bbox intersects clip; how="inside": bbox fully inside clip.

    Each path: dict(kind='stroke'|'fill'|'fillstroke', color, fill, width, rect=(x0,y0,x1,y1),
                    dashes, closePath, n_items, subpaths=[[(x,y),...], ...], points=[all points],
                    rects=[(x0,y0,x1,y1), ...] for 're' items, has_curves=bool, raw=<PyMuPDF dict>)
    Bezier curves are flattened to 12 points each. Consecutive 'l' items are joined into one subpath.
    """
    out = []
    for d in page.get_drawings():
        r = d["rect"]
        if clip is not None:
            # A single horizontal or vertical segment has a zero-height/width bbox; fitz treats such a
            # Rect as empty and intersects()/contains() are False for it. Inflate degenerate rects a
            # little before testing so spike ticks and 1-pt axis strokes are not silently dropped.
            rt = fitz.Rect(r.x0 - 0.01, r.y0 - 0.01, r.x1 + 0.01, r.y1 + 0.01) if (r.width <= 0 or r.height <= 0) else r
            if how == "inside" and not clip.contains(rt):
                continue
            if how == "intersects" and not clip.intersects(rt):
                continue
        subpaths, cur, rects, has_curves = [], [], [], False
        last = None
        for it in d["items"]:
            op = it[0]
            if op == "l":
                p1, p2 = it[1], it[2]
                if last is None or (abs(p1.x - last.x) > 1e-6 or abs(p1.y - last.y) > 1e-6):
                    if cur:
                        subpaths.append(cur)
                    cur = [(p1.x, p1.y)]
                cur.append((p2.x, p2.y))
                last = p2
            elif op == "c":
                has_curves = True
                p0 = it[1]
                if last is None or (abs(p0.x - last.x) > 1e-6 or abs(p0.y - last.y) > 1e-6):
                    if cur:
                        subpaths.append(cur)
                    cur = [(p0.x, p0.y)]
                cur.extend(_bezier(it[1], it[2], it[3], it[4]))
                last = it[4]
            elif op == "re":
                rr = it[1]
                rects.append((rr.x0, rr.y0, rr.x1, rr.y1))
                if cur:
                    subpaths.append(cur)
                    cur = []
                subpaths.append([(rr.x0, rr.y0), (rr.x1, rr.y0), (rr.x1, rr.y1), (rr.x0, rr.y1), (rr.x0, rr.y0)])
                last = None
            elif op == "qu":
                q = it[1]
                if cur:
                    subpaths.append(cur)
                    cur = []
                subpaths.append([(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y), (q.ul.x, q.ul.y)])
                last = None
        if cur:
            subpaths.append(cur)
        kind = {"s": "stroke", "f": "fill", "fs": "fillstroke"}.get(d["type"], d["type"])
        out.append(dict(
            kind=kind, color=d.get("color"), fill=d.get("fill"), width=d.get("width"),
            rect=(r.x0, r.y0, r.x1, r.y1), dashes=d.get("dashes"), closePath=d.get("closePath"),
            n_items=len(d["items"]), subpaths=subpaths, points=[p for sp in subpaths for p in sp],
            rects=rects, has_curves=has_curves, raw=d,
        ))
    return out


def summarize(draws, top=40):
    """Print a histogram of path types in a drawing list (kind, colour, width, n_items) to orient yourself."""
    from collections import Counter
    c = Counter()
    for d in draws:
        key = (d["kind"], _hex(d["color"]), _hex(d["fill"]), round(d["width"] or 0, 2), d["n_items"], d["has_curves"],
               "rects" if d["rects"] else "")
        c[key] += 1
    print(f"{'n':>5}  kind        color    fill     width items curves")
    for k, v in c.most_common(top):
        print(f"{v:5d}  {k[0]:10s}  {k[1] or '-':8s} {k[2] or '-':8s} {k[3]:5}  {k[4]:5d} {k[5]} {k[6]}")


def _hex(c):
    if c is None:
        return None
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c[:3])


def hexcolor(c):
    """(r,g,b) floats -> '#rrggbb' (or None)."""
    return _hex(c)


def markers(draws, max_size=6.0):
    """Small closed paths (circles/squares/triangles) -> list of dict(cx, cy, w, h, color, fill, kind).

    Use for scatter plots and data points. `max_size` is the largest marker extent in points.
    """
    out = []
    for d in draws:
        x0, y0, x1, y1 = d["rect"]
        w, h = x1 - x0, y1 - y0
        if 0 < w <= max_size and 0 < h <= max_size and d["kind"] in ("fill", "fillstroke", "stroke"):
            out.append(dict(cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, w=w, h=h, color=d["color"], fill=d["fill"],
                            kind=d["kind"], has_curves=d["has_curves"], n_items=d["n_items"]))
    return out


def segments(draws, orientation=None, max_len=None, min_len=0.0):
    """All straight 2-point segments, as dict(x0,y0,x1,y1,len,color,width). orientation: 'h', 'v' or None."""
    out = []
    for d in draws:
        for sp in d["subpaths"]:
            if len(sp) != 2:
                continue
            (x0, y0), (x1, y1) = sp
            L = math.hypot(x1 - x0, y1 - y0)
            if L < min_len or (max_len is not None and L > max_len):
                continue
            if orientation == "h" and abs(y1 - y0) > 0.05 * L:
                continue
            if orientation == "v" and abs(x1 - x0) > 0.05 * L:
                continue
            out.append(dict(x0=x0, y0=y0, x1=x1, y1=y1, len=L, color=d["color"], width=d["width"], kind=d["kind"]))
    return out


# ---------------------------------------------------------------- axes

class Axis:
    """Linear (or log10) map from PDF coordinate to data value, fitted to (pixel, value) pairs."""

    def __init__(self, pairs, log=False):
        self.pairs = sorted(pairs)
        self.log = log
        xs = [p for p, v in self.pairs]
        vs = [math.log10(v) if log else v for p, v in self.pairs]
        n = len(xs)
        if n < 2:
            raise ValueError("need >= 2 (pixel, value) pairs")
        mx, mv = sum(xs) / n, sum(vs) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxv = sum((x - mx) * (v - mv) for x, v in zip(xs, vs))
        self.slope = sxv / sxx
        self.intercept = mv - self.slope * mx
        self.resid = max(abs((self.slope * x + self.intercept) - v) for x, v in zip(xs, vs))

    def __call__(self, pix):
        v = self.slope * pix + self.intercept
        return 10 ** v if self.log else v

    def inv(self, val):
        v = math.log10(val) if self.log else val
        return (v - self.intercept) / self.slope

    def __repr__(self):
        return f"Axis(log={self.log}, slope={self.slope:.6g}, intercept={self.intercept:.6g}, max_resid={self.resid:.3g}, pairs={self.pairs})"


def axis_from_labels(spans, draws=None, orientation="x", log=False, label_filter=None, tick_max_len=6.0,
                     tol=None):
    """Build an Axis from numeric tick labels (and, if `draws` is given, the tick marks they sit next to).

    orientation 'x': labels in one row (similar cy); the pixel coordinate is the label's cx, refined to the
    x of the nearest short vertical tick mark if `draws` is given.
    orientation 'y': labels in one column (similar cx); pixel coordinate is the label's cy, refined to the
    y of the nearest short horizontal tick mark.
    label_filter(span) -> bool restricts which spans are considered (e.g. by cy range, to pick one of
    several axes in the clip). For a y axis, horizontal text only; rotated labels are ignored.
    """
    nums = []
    for s in spans:
        if s["dir"] != (1.0, 0.0):
            continue
        if label_filter and not label_filter(s):
            continue
        v = parse_number(s["text"])
        if v is None:
            continue
        nums.append((s, v))
    if len(nums) < 2:
        raise ValueError(f"found only {len(nums)} numeric labels: {[s['text'] for s, v in nums]}")
    # group: for x axis take the most populated row (same cy); for y the most populated column (same cx1)
    if orientation == "x":
        key = lambda s: round(s["cy"] / 3)
    else:
        key = lambda s: round(s["bbox"][2] / 3)  # right edge of label
    from collections import Counter
    grp = Counter(key(s) for s, v in nums).most_common(1)[0][0]
    sel = [(s, v) for s, v in nums if abs(key(s) - grp) <= 1]
    pairs = []
    ticks = []
    if draws is not None:
        ticks = segments(draws, orientation=("v" if orientation == "x" else "h"), max_len=tick_max_len, min_len=0.5)
    for s, v in sel:
        if orientation == "x":
            pix = s["cx"]
            if ticks:
                cand = [t for t in ticks if abs((t["x0"] + t["x1"]) / 2 - pix) < (tol or 4.0) and t["y0"] < s["bbox"][1] + 2]
                if cand:
                    t = min(cand, key=lambda t: abs((t["x0"] + t["x1"]) / 2 - pix))
                    pix = (t["x0"] + t["x1"]) / 2
        else:
            pix = s["cy"]
            if ticks:
                cand = [t for t in ticks if abs((t["y0"] + t["y1"]) / 2 - pix) < (tol or 4.0) and t["x0"] > s["bbox"][0] - 2]
                if cand:
                    t = min(cand, key=lambda t: abs((t["y0"] + t["y1"]) / 2 - pix))
                    pix = (t["y0"] + t["y1"]) / 2
        pairs.append((pix, v))
    return Axis(pairs, log=log)


# ---------------------------------------------------------------- raster images

def images(page, clip=None):
    """Raster images placed on the page: list of dict(xref, bbox, width, height). Use extract_image to save."""
    out = []
    for info in page.get_image_info(xrefs=True):
        b = fitz.Rect(info["bbox"])
        if clip is not None and not clip.intersects(b):
            continue
        out.append(dict(xref=info["xref"], bbox=(b.x0, b.y0, b.x1, b.y1), width=info["width"], height=info["height"],
                        transform=info.get("transform")))
    out.sort(key=lambda i: (round(i["bbox"][1]), i["bbox"][0]))
    return out


def extract_image(page, xref, out_png):
    """Save the embedded image `xref` as PNG (full native resolution, soft mask applied if present)."""
    doc = page.parent
    pix = fitz.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4:  # CMYK
        pix = fitz.Pixmap(fitz.csRGB, pix)
    pix.save(out_png)
    return pix.width, pix.height


def render(page, clip, dpi, out_png):
    """Render `clip` of the page at `dpi` to PNG (for image panels and for QA crops)."""
    pix = page.get_pixmap(clip=clip, dpi=dpi)
    pix.save(out_png)
    return pix.width, pix.height


# ---------------------------------------------------------------- output

def write_csv(path, header, rows, comments=None):
    """Write CSV with an optional block of '# ...' comment lines at the top (provenance, units, caveats)."""
    with open(path, "w", newline="") as f:
        if comments:
            for c in comments:
                f.write("# " + c + "\n")
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def read_csv(path):
    """Read a CSV written by write_csv: returns (header, rows as list of lists of str), skipping '#' lines."""
    with open(path) as f:
        lines = [l for l in f if not l.startswith("#")]
    rd = list(csv.reader(lines))
    return rd[0], rd[1:]


# ---------------------------------------------------------------- thin lines / ticks / outlined text

def thin_segments(draws, max_thick=1.2):
    """Line-like paths as segments, including lines drawn as thin filled rectangles/polygons (common in
    MATLAB/Illustrator exports: axes and tick marks are 0.5 pt wide fills, not strokes).

    Returns dict(x0,y0,x1,y1,len,orient='h'|'v'|None,color,width,kind) with the centre line of thin fills.
    """
    out = list(segments(draws))
    for s in out:
        dx, dy = abs(s["x1"] - s["x0"]), abs(s["y1"] - s["y0"])
        s["orient"] = "h" if dy <= 0.05 * max(dx, 1e-9) else ("v" if dx <= 0.05 * max(dy, 1e-9) else None)
    for d in draws:
        if d["kind"] not in ("fill", "fillstroke"):
            continue
        x0, y0, x1, y1 = d["rect"]
        w, h = x1 - x0, y1 - y0
        if d["has_curves"] or d["n_items"] > 4:
            continue
        if h <= max_thick and w > h:
            y = (y0 + y1) / 2
            out.append(dict(x0=x0, y0=y, x1=x1, y1=y, len=w, orient="h", color=d["fill"], width=h, kind="thinfill"))
        elif w <= max_thick and h > w:
            x = (x0 + x1) / 2
            out.append(dict(x0=x, y0=y0, x1=x, y1=y1, len=h, orient="v", color=d["fill"], width=w, kind="thinfill"))
    return out


def tick_marks(draws, orientation="x", max_len=6.0, min_len=0.8, region=None):
    """Short segments perpendicular to the axis: vertical ticks for an x axis, horizontal for a y axis.
    region: optional Rect; only ticks whose centre lies inside are returned. Sorted along the axis."""
    want = "v" if orientation == "x" else "h"
    out = []
    for s in thin_segments(draws):
        if s["orient"] != want or not (min_len <= s["len"] <= max_len):
            continue
        cx, cy = (s["x0"] + s["x1"]) / 2, (s["y0"] + s["y1"]) / 2
        if region is not None and not region.contains(fitz.Point(cx, cy)):
            continue
        out.append(dict(pos=cx if orientation == "x" else cy, cx=cx, cy=cy, len=s["len"], color=s["color"]))
    out.sort(key=lambda t: t["pos"])
    return out


def axis_from_ticks(draws, orientation, values, region=None, max_len=6.0, min_len=0.8, log=False, dedupe=0.6):
    """Axis from tick-mark positions + the tick VALUES you read off the rendered crop (ascending order).

    Use this when tick labels are outlined glyphs (no text spans). `region` (Rect) restricts which ticks are
    used, e.g. the strip just below the x axis line, so that ticks of a neighbouring panel are not picked up.
    For an x axis values are paired with ticks left->right; for a y axis bottom->top (values ascending).
    Raises if the number of ticks found differs from len(values) (print tick_marks(...) to debug).
    """
    ticks = tick_marks(draws, orientation, max_len=max_len, min_len=min_len, region=region)
    # merge duplicates (same tick drawn twice, or stroke + fill)
    merged = []
    for t in ticks:
        if merged and abs(t["pos"] - merged[-1]["pos"]) < dedupe:
            continue
        merged.append(t)
    pos = [t["pos"] for t in merged]
    if orientation == "y":
        pos = sorted(pos, reverse=True)  # bottom of plot (large y) first = smallest value
    if len(pos) != len(values):
        raise ValueError(f"found {len(pos)} tick marks at {[round(p,2) for p in pos]} but {len(values)} values given")
    return Axis(list(zip(pos, values)), log=log)


def glyph_boxes(draws, max_h=12.0):
    """Bounding boxes of small filled outline paths with curves: text converted to outlines (tick labels etc.).
    Returns list of dict(bbox, cx, cy, n_items, color). Use to see where labels sit relative to tick marks."""
    out = []
    for d in draws:
        if d["kind"] in ("fill", "fillstroke") and d["has_curves"]:
            x0, y0, x1, y1 = d["rect"]
            if (y1 - y0) <= max_h and (x1 - x0) <= 10 * max_h:
                out.append(dict(bbox=d["rect"], cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, n_items=d["n_items"], color=d["fill"]))
    out.sort(key=lambda g: (round(g["cy"]), g["cx"]))
    return out


# ---------------------------------------------------------------- bands / envelopes

def band_envelope(points, ndigits=6):
    """For a filled error-band polygon (already mapped to data coords), return (xs, lo, hi):
    for each distinct x (rounded to `ndigits`) the min and max y. Robust to where the polygon starts.

    Caveat: wrong where a band is clipped at an axis limit (the clipped edge has no vertices at the data x
    positions). Use `dashlines.band_extent`, which slices the polygon vertically at each grid x, for those."""
    from collections import defaultdict
    acc = defaultdict(list)
    for x, y in points:
        acc[round(x, ndigits)].append(y)
    xs = sorted(acc)
    return xs, [min(acc[x]) for x in xs], [max(acc[x]) for x in xs]


def polyline_to_xy(points, xax, yax):
    """Map a list of (px, py) to data coordinates with two Axis objects -> (xs, ys) lists."""
    xs = [xax(x) for x, y in points]
    ys = [yax(y) for x, y in points]
    return xs, ys
