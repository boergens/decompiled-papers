"""Shared helpers for raster digitizing scripts (figN_extract.py). First written for li2024.

All plots in this paper are raster images embedded in the PDFs (no vector paths), so every
extraction is tier 3 ("digitized"): load the embedded image (pdfimages -png, extracted by
the scripts themselves with PyMuPDF), find the axis frame and the tick marks, fit a linear
pixel->data map per axis on the tick marks whose labels are printed in the figure, then
trace each series with a colour mask (centre of the mask pixels in each pixel column).
"""
import numpy as np
import pymupdf


def embedded_image(pdf, page, xref_index=None, bbox_near=None):
    """Return the embedded raster image on <page> (1-based) as an RGB uint8 array.

    The SMask (alpha) of the image is composited over white, as in the PDF rendering.
    Pick the image whose placement bbox is closest to bbox_near (PDF points), or the
    largest one.
    """
    doc = pymupdf.open(pdf)
    p = doc[page - 1]
    infos = p.get_image_info(xrefs=True)
    if bbox_near is not None:
        def dist(i):
            return sum(abs(a - b) for a, b in zip(i["bbox"], bbox_near))
        info = min(infos, key=dist)
    else:
        info = max(infos, key=lambda i: i["width"] * i["height"])
    xref = info["xref"]
    pix = pymupdf.Pixmap(doc, xref)
    smask = doc.xref_get_key(xref, "SMask")
    rgb = pymupdf.Pixmap(pymupdf.csRGB, pix) if pix.n - pix.alpha != 3 else pix
    a = np.frombuffer(rgb.samples, np.uint8).reshape(rgb.height, rgb.width, rgb.n)[:, :, :3].astype(float)
    if smask[0] == "xref":
        m = pymupdf.Pixmap(doc, int(smask[1].split()[0]))
        al = np.frombuffer(m.samples, np.uint8).reshape(m.height, m.width).astype(float) / 255
        a = a * al[:, :, None] + 255 * (1 - al[:, :, None])
    return a.astype(np.uint8)


def gray(a):
    return a.astype(float).mean(2)


def frame_lines(dark, axis, min_frac=0.6):
    """Indices (rows if axis=1, columns if axis=0) where the dark mask forms a long line.

    Returns groups of consecutive indices as (first, last) pairs.
    """
    s = dark.sum(axis=axis)
    n = dark.shape[axis]
    idx = np.where(s >= min_frac * n)[0]
    groups = []
    for i in idx:
        if groups and i == groups[-1][1] + 1:
            groups[-1][1] = i
        else:
            groups.append([i, i])
    return [tuple(g) for g in groups]


def tick_positions(dark, line_rows, side, length, x0, x1, frac=0.8):
    """Columns of tick marks attached to a horizontal axis line.

    dark: bool mask; line_rows: (first,last) rows of the axis line; side: -1 to look
    above the line (ticks pointing up/inward on a bottom axis), +1 below; length: how many
    rows next to the line to examine (all must be dark in >= frac of them). Returns the centre column of each tick.
    """
    r0, r1 = line_rows
    if side < 0:
        band = dark[r0 - length:r0, x0:x1]
    else:
        band = dark[r1 + 1:r1 + 1 + length, x0:x1]
    full = band.mean(0) >= frac
    cols = np.where(full)[0]
    groups = []
    for c in cols:
        if groups and c == groups[-1][-1] + 1:
            groups[-1].append(c)
        else:
            groups.append([c])
    return [x0 + float(np.mean(g)) for g in groups]


def tick_positions_v(dark, line_cols, side, length, y0, y1, frac=0.8):
    """Rows of tick marks attached to a vertical axis line (side +1: to the right)."""
    c0, c1 = line_cols
    if side > 0:
        band = dark[y0:y1, c1 + 1:c1 + 1 + length]
    else:
        band = dark[y0:y1, c0 - length:c0]
    full = band.mean(1) >= frac
    rows = np.where(full)[0]
    groups = []
    for r in rows:
        if groups and r == groups[-1][-1] + 1:
            groups[-1].append(r)
        else:
            groups.append([r])
    return [y0 + float(np.mean(g)) for g in groups]


def fit_axis(pix, val, log=False):
    """Least-squares linear map pixel -> value (log10 if log). Returns (f, max residual in value units)."""
    pix = np.asarray(pix, float)
    v = np.log10(val) if log else np.asarray(val, float)
    A = np.vstack([pix, np.ones_like(pix)]).T
    (m, b), *_ = np.linalg.lstsq(A, v, rcond=None)
    res = np.max(np.abs(A @ [m, b] - v)) if len(pix) > 2 else 0.0
    if log:
        return (lambda p: 10 ** (m * np.asarray(p, float) + b)), res, m
    return (lambda p: m * np.asarray(p, float) + b), res, m


def trace(mask, x0, x1, y0, y1, min_px=1, mode="centre"):
    """For each column in [x0,x1) return the row of the series mask inside rows [y0,y1).

    mode 'centre': mean of the mask rows (line centre); 'top': smallest row (peak tops of a
    filled or very thick trace). Columns with fewer than min_px mask pixels are NaN.
    """
    xs, ys = [], []
    for c in range(x0, x1):
        r = np.where(mask[y0:y1, c])[0]
        xs.append(c)
        if len(r) < min_px:
            ys.append(np.nan)
        elif mode == "top":
            ys.append(y0 + r.min())
        else:
            # keep the largest connected run (the line), ignore stray pixels
            runs = np.split(r, np.where(np.diff(r) > 2)[0] + 1)
            run = max(runs, key=len)
            ys.append(y0 + run.mean())
    return np.array(xs, float), np.array(ys, float)


def write_csv(path, header_lines, columns, rows, fmt="{:.5g}"):
    """CSV with '#' comment lines first. fmt is one format for all numbers, or a list per column.
    Fields are quoted when needed (a series name may contain commas); ints stay ints."""
    import csv as _csv
    fmts = fmt if isinstance(fmt, (list, tuple)) else [fmt] * len(columns)
    with open(path, "w", newline="") as f:
        for h in header_lines:
            f.write("# " + h + "\n")
        w = _csv.writer(f)
        w.writerow(columns)
        for r in rows:
            out = []
            for x, fm in zip(r, fmts):
                if isinstance(x, str):
                    out.append(x)
                elif isinstance(x, (int,)) and not isinstance(x, bool):
                    out.append(str(x))
                elif x != x:
                    out.append("")
                else:
                    out.append(fm.format(x))
            w.writerow(out)


def trace_envelope(mask, x0, x1, y0, y1, half_width, min_px=1):
    """Per column: (x, y_mid, y_upper, y_lower) of a thin line trace, in pixel rows.

    For steep segments (peaks, edges) a column contains a long vertical run of line pixels;
    y_upper/y_lower are the run's ends moved inward by half the line width, so the band
    between them is where the plotted curve passes in that column. y_mid is their mean.
    Uses the run of mask pixels closest to the previous column's value, to ignore stray marks.
    """
    out, prev = [], None
    for c in range(x0, x1):
        r = np.where(mask[y0:y1, c])[0]
        if len(r) < min_px:
            out.append((c, np.nan, np.nan, np.nan))
            continue
        runs = np.split(r, np.where(np.diff(r) > 2)[0] + 1)
        if prev is None:
            run = max(runs, key=len)
        else:
            run = min(runs, key=lambda q: 0 if q[0] - 3 <= prev - y0 <= q[-1] + 3 else min(abs(q[0] - (prev - y0)), abs(q[-1] - (prev - y0))))
        top, bot = y0 + run[0] + half_width, y0 + run[-1] - half_width
        if top > bot:
            top = bot = y0 + run.mean()
        prev = (top + bot) / 2
        out.append((c, prev, top, bot))
    return np.array(out, float)


def overlay(a, xy_px, out_png, colour=(255, 0, 255)):
    """Draw extracted points (pixel coordinates in the source image) over the source image.

    This is the strictest check of a digitization: every magenta pixel must sit on the
    plotted line. Saves a PNG for viewing with the Read tool.
    """
    from PIL import Image
    im = a.copy()
    for x, y in xy_px:
        if x == x and y == y:
            xi, yi = int(round(x)), int(round(y))
            if 0 <= yi < im.shape[0] and 0 <= xi < im.shape[1]:
                im[max(0, yi - 1):yi + 2, max(0, xi - 1):xi + 2] = colour
    Image.fromarray(im).save(out_png)
