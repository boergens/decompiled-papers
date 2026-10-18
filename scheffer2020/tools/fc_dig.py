"""Small raster-digitizing helpers for scheffer2020 Figs 20-26 and Appendix 1-figures 1-3 (written for this paper).

All plots in these figures are raster images embedded in the PDF; scripts load the embedded image at its native
resolution with PyMuPDF, calibrate the axes on gridlines / tick marks located in the image (pixel positions found by
code, never read off a displayed image), and trace each series with a colour mask.
"""
import csv
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "source" / "elife-57443-v4.pdf"


def embedded(page):
    """Largest embedded image on a 1-based page, as an RGB uint8 array (native resolution)."""
    doc = pymupdf.open(PDF)
    pg = doc[page - 1]
    info = max(pg.get_image_info(xrefs=True), key=lambda i: pymupdf.Rect(i["bbox"]).get_area())
    pix = pymupdf.Pixmap(doc, info["xref"])
    if pix.n - pix.alpha != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return a[:, :, :3].copy()


def colour_mask(a, rgb, tol=40):
    d = np.abs(a.astype(int) - np.array(rgb)[None, None, :]).max(axis=2)
    return d <= tol


def dark_mask(a, thr=90):
    return a.astype(int).max(axis=2) <= thr


def white_lines(a, x0, x1, y0, y1, axis, thr=250, frac=0.5):
    """Centres of runs of near-white rows (axis='h') or columns (axis='v') inside a box: gridlines on a grey background."""
    g = a[y0:y1, x0:x1].astype(int).min(axis=2)
    f = (g >= thr).mean(axis=1 if axis == "h" else 0)
    idx = np.where(f > frac)[0]
    runs, cur = [], []
    for i in idx:
        if cur and i != cur[-1] + 1:
            runs.append(cur); cur = []
        cur.append(i)
    if cur:
        runs.append(cur)
    off = y0 if axis == "h" else x0
    return [off + float(np.mean(r)) for r in runs]


def fit(pix, val, log=False):
    """Least-squares pixel -> value map; returns (function, max residual in value units)."""
    pix = np.asarray(pix, float)
    v = np.log10(val) if log else np.asarray(val, float)
    k, c = np.polyfit(pix, v, 1)
    res = float(np.max(np.abs(k * pix + c - v)))
    if log:
        return (lambda p: 10 ** (k * np.asarray(p, float) + c)), res
    return (lambda p: k * np.asarray(p, float) + c), res


def inverse(f, lo, hi):
    """Pixel position for a value (numeric inverse of a monotone map over pixel range lo..hi)."""
    xs = np.linspace(lo, hi, 20001)
    vs = f(xs)
    def g(v):
        if vs[0] > vs[-1]:
            return float(np.interp(v, vs[::-1], xs[::-1]))
        return float(np.interp(v, vs, xs))
    return g


def runs(ys, gap=1):
    """Split sorted indices into contiguous runs (allowing gaps of up to `gap` - 1 missing pixels)."""
    out, cur = [], []
    for y in ys:
        if cur and y - cur[-1] > gap:
            out.append(cur); cur = []
        cur.append(y)
    if cur:
        out.append(cur)
    return out


def trace(mask, x0, x1, y0, y1, min_px=1, longest=True, gap=2):
    """Per column x in [x0, x1): (x, mean row, top row, bottom row) of mask pixels in rows [y0, y1).
    longest=True keeps only the longest contiguous run in the column (drops stray anti-aliasing pixels)."""
    out = []
    for x in range(x0, x1):
        ys = np.where(mask[y0:y1, x])[0]
        if longest and len(ys):
            ys = np.array(max(runs(list(ys), gap), key=len))
        if len(ys) >= min_px:
            out.append((x, y0 + ys.mean(), y0 + ys.min(), y0 + ys.max()))
    return out


def blank(mask, boxes):
    m = mask.copy()
    for (x0, y0, x1, y1) in boxes:
        m[y0:y1, x0:x1] = False
    return m


def write_csv(path, header_lines, columns, rows):
    path = Path(path)
    with open(path, "w", newline="") as f:
        for h in header_lines:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(columns)
        for r in rows:
            w.writerow([(f"{v:.6g}" if isinstance(v, (float, np.floating)) else v) for v in r])
    return path


def read_csv(path):
    with open(path) as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines))


def overlay(a, pts, out, colours=None, r=2):
    """Draw points (pixel x, y in the source image) over the source; pts is {series: [(x, y), ...]}."""
    im = Image.fromarray(np.ascontiguousarray(a)).convert("RGB")
    d = ImageDraw.Draw(im)
    pal = [(255, 0, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0), (0, 160, 0), (120, 0, 200), (255, 128, 0)]
    for i, (k, v) in enumerate(pts.items()):
        c = (colours or {}).get(k, pal[i % len(pal)])
        for x, y in v:
            d.ellipse([x - r, y - r, x + r, y + r], outline=c)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    im.save(out)


def blobs(mask, x0, y0, x1, y1, amin=3, amax=400):
    """Connected components of mask inside a box: list of (cx, cy, area, w, h) in source pixels."""
    from scipy import ndimage
    sub = mask[y0:y1, x0:x1]
    lab, n = ndimage.label(sub, structure=np.ones((3, 3)))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        ys, xs = np.where(lab[sl] == i)
        if amin <= len(ys) <= amax:
            out.append((x0 + sl[1].start + xs.mean(), y0 + sl[0].start + ys.mean(), len(ys),
                        sl[1].stop - sl[1].start, sl[0].stop - sl[0].start))
    return out
