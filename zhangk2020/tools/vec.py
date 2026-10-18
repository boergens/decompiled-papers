"""Helpers for the vector-plot extraction scripts of zhangk2020 (figN_extract.py).

The plots in this PDF are vector drawings (an embedded page of the authors' manuscript,
clipped to the figure). Frame lines and tick marks are thin filled black rectangles,
tick labels are real text, markers are small stroked paths (squares from four 2-segment
lines, circles from four Beziers, diamonds as quads), curves are polylines.

Usage from a script in ../figures/:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
    import vec
"""
from pathlib import Path

import numpy as np
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "source" / "zhangk2020.pdf"


def _inflate(r, eps=0.01):
    r = pymupdf.Rect(r)
    if r.width == 0:
        r.x0 -= eps
        r.x1 += eps
    if r.height == 0:
        r.y0 -= eps
        r.y1 += eps
    return r


def drawings(page, clip):
    """All drawings of 1-based `page` whose bbox lies inside `clip` (x0, y0, x1, y1, PDF points).
    Degenerate (zero-width/height) rects are inflated first, so single strokes are kept."""
    doc = pymupdf.open(PDF)
    c = pymupdf.Rect(clip)
    out = []
    for d in doc[page - 1].get_drawings():
        r = _inflate(d["rect"])
        if r.x0 >= c.x0 and r.x1 <= c.x1 and r.y0 >= c.y0 and r.y1 <= c.y1:
            d = dict(d)
            d["rect"] = r
            out.append(d)
    return out


def texts(page, clip):
    """Text spans inside clip: list of (text, bbox)."""
    doc = pymupdf.open(PDF)
    c = pymupdf.Rect(clip)
    out = []
    for b in doc[page - 1].get_text("dict", clip=c)["blocks"]:
        for line in b.get("lines", []):
            for s in line["spans"]:
                if s["text"].strip():
                    out.append((s["text"].strip(), pymupdf.Rect(s["bbox"])))
    return out


def is_black_fill(d):
    f = d.get("fill")
    return f is not None and max(f) < 0.05 and d.get("color") is None


def colour_is(c, rgb, tol=0.08):
    return c is not None and all(abs(a - b) <= tol for a, b in zip(c, rgb))


def fit(pix, val):
    """Least-squares linear map pix -> val. Returns (slope, offset, max abs residual)."""
    pix = np.asarray(pix, float)
    val = np.asarray(val, float)
    a, b = np.polyfit(pix, val, 1)
    res = np.max(np.abs(a * pix + b - val))
    return a, b, res


def tick_rects(ds, axis, at, tol=1.0, maxlen=6.0):
    """Centres of the short black tick rectangles that touch the frame line at coordinate `at`.
    axis='x': ticks on a horizontal frame line at y=at -> returns their x centres.
    axis='y': ticks on a vertical frame line at x=at  -> returns their y centres."""
    out = []
    for d in ds:
        if not is_black_fill(d):
            continue
        r = d["rect"]
        if axis == "x" and r.width < 2.5 and r.height <= maxlen and (abs(r.y0 - at) < tol + 2 or abs(r.y1 - at) < tol + 2):
            out.append((r.x0 + r.x1) / 2)
        if axis == "y" and r.height < 2.5 and r.width <= maxlen and (abs(r.x0 - at) < tol + 2 or abs(r.x1 - at) < tol + 2):
            out.append((r.y0 + r.y1) / 2)
    return sorted(set(round(v, 3) for v in out))


def cluster(rects, gap=0.5):
    """Merge overlapping/touching rects; returns merged rects."""
    rs = [pymupdf.Rect(r) for r in rects]
    merged = True
    while merged:
        merged = False
        out = []
        for r in rs:
            for i, o in enumerate(out):
                if (r.x0 <= o.x1 + gap and o.x0 <= r.x1 + gap and r.y0 <= o.y1 + gap and o.y0 <= r.y1 + gap):
                    out[i] = o | r
                    merged = True
                    break
            else:
                out.append(r)
        rs = out
    return rs


def centre(r):
    return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)


def polyline(d):
    """Vertices of a drawing made of 'l' items, in order (joined end to start)."""
    pts = []
    for it in d["items"]:
        if it[0] != "l":
            continue
        p0, p1 = (it[1].x, it[1].y), (it[2].x, it[2].y)
        if not pts or (abs(pts[-1][0] - p0[0]) > 1e-6 or abs(pts[-1][1] - p0[1]) > 1e-6):
            pts.append(p0)
        pts.append(p1)
    return pts


def write_csv(path, header_lines, columns, rows):
    with open(path, "w") as f:
        for h in header_lines:
            f.write("# " + h + "\n")
        f.write(",".join(columns) + "\n")
        for r in rows:
            f.write(",".join(str(v) for v in r) + "\n")


def render(page, clip, out, dpi=400):
    doc = pymupdf.open(PDF)
    pix = doc[page - 1].get_pixmap(clip=pymupdf.Rect(clip), dpi=dpi)
    pix.save(str(out))
    return dpi / 72.0


def frame(ds):
    """The plot frame from the four long black frame bars: returns (left, top, right, bottom)
    as the centre lines of the bars (PDF points)."""
    bars = [d["rect"] for d in ds if is_black_fill(d)]
    horiz = [r for r in bars if r.width > 60 and r.height < 3]
    vert = [r for r in bars if r.height > 60 and r.width < 3]
    top = min(horiz, key=lambda r: r.y0)
    bot = max(horiz, key=lambda r: r.y0)
    left = min(vert, key=lambda r: r.x0)
    right = max(vert, key=lambda r: r.x0)
    return ((left.x0 + left.x1) / 2, (top.y0 + top.y1) / 2, (right.x0 + right.x1) / 2, (bot.y0 + bot.y1) / 2)


def axis_fit(ticks, labels, axis):
    """Match numeric tick labels [(text, bbox)] to the nearest tick position and fit a linear
    map. axis='x' uses the label's x centre, 'y' its y centre. Returns (slope, offset, maxres, pairs)."""
    pairs = []
    for t, r in labels:
        try:
            v = float(t)
        except ValueError:
            continue
        c = (r.x0 + r.x1) / 2 if axis == "x" else (r.y0 + r.y1) / 2
        tk = min(ticks, key=lambda p: abs(p - c))
        if abs(tk - c) < 6:
            pairs.append((tk, v))
    a, b, res = fit([p for p, _ in pairs], [v for _, v in pairs])
    return a, b, res, pairs


def stroke_markers(ds, rgb, maxsize=8.0):
    """Markers drawn as small stroked paths of colour rgb: clusters of their bboxes, as rects."""
    rs = [d["rect"] for d in ds if colour_is(d.get("color"), rgb) and d["rect"].width < maxsize and d["rect"].height < maxsize]
    return [r for r in cluster(rs) if r.width > 2 and r.height > 2]


def overlay_pts(page, clip, pts, out, dpi=300):
    """Render the clip and draw page-coordinate points (x, y) on it as magenta crosses (check image)."""
    from PIL import Image, ImageDraw
    doc = pymupdf.open(PDF)
    pix = doc[page - 1].get_pixmap(clip=pymupdf.Rect(clip), dpi=dpi)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    s = dpi / 72.0
    for x, y in pts:
        u, v = (x - clip[0]) * s, (y - clip[1]) * s
        dr.line((u - 4, v, u + 4, v), fill=(255, 0, 255), width=1)
        dr.line((u, v - 4, u, v + 4), fill=(255, 0, 255), width=1)
    im.save(str(out))
