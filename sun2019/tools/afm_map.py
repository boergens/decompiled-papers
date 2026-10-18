"""Convert a printed AFM height map (sun2019 Figs. 4 and 7) to heights through its printed colour bar.

Written for sun2019. The colour bar is sampled down its centre (mean over a band of columns) between the
centres of its top and bottom frame lines, which are the printed end values (e.g. 25.0 nm and -25.0 nm); each
bar row then has a colour and a height (linear in row). A map pixel gets the median height of the bar rows whose
colour is within TOL of its nearest bar colour (so a colour that the bar repeats, e.g. saturated black at the
low end, gets the middle of that run and is flagged by the caller as clipped). Pixels farther than MAX_DIST from
every bar colour, and masked annotation pixels, are left empty.
"""
import numpy as np
import pymupdf

TOL = 6.0
MAX_DIST = 45.0


def embedded(pdf, page, bbox_near):
    doc = pymupdf.open(pdf)
    p = doc[page - 1]
    info = min(p.get_image_info(xrefs=True), key=lambda i: sum(abs(a - b) for a, b in zip(i["bbox"], bbox_near)))
    pix = pymupdf.Pixmap(doc, info["xref"])
    if pix.n - pix.alpha != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()


def bar_lut(a, cols, row_top, row_bot, v_top, v_bot):
    """LUT from the bar: rows strictly inside the frame centres row_top..row_bot (2 px margin)."""
    rows = np.arange(int(np.ceil(row_top)) + 2, int(np.floor(row_bot)) - 1)
    col = a[rows][:, cols[0]:cols[1]].astype(float).mean(1)
    vals = v_top + (v_bot - v_top) * (rows - row_top) / (row_bot - row_top)
    return col, vals


def to_height(img, lut_rgb, lut_val, mask):
    h, w, _ = img.shape
    f = img.reshape(-1, 3).astype(float)
    out = np.full(h * w, np.nan)
    for s in range(0, h * w, 20000):
        d = np.sqrt(((f[s:s + 20000, None, :] - lut_rgb[None, :, :]) ** 2).sum(2))
        dmin = d.min(1)
        near = d <= (dmin[:, None] + TOL)
        v = np.where(near, lut_val[None, :], np.nan)
        med = np.nanmedian(v, axis=1)
        med[dmin > MAX_DIST] = np.nan
        out[s:s + 20000] = med
    out = out.reshape(h, w)
    out[mask] = np.nan
    return out


def white_mask(img, boxes_full, boxes_white, thr=200, grow=2):
    """Annotation mask: whole boxes (labels) plus near-white pixels (arrows) in other boxes, grown by `grow` px."""
    from scipy.ndimage import binary_dilation
    m = np.zeros(img.shape[:2], bool)
    for c0, r0, c1, r1 in boxes_full:
        m[r0:r1, c0:c1] = True
    wm = np.zeros_like(m)
    for c0, r0, c1, r1 in boxes_white:
        wm[r0:r1, c0:c1] = img[r0:r1, c0:c1].min(2) > thr
    return m | binary_dilation(wm, iterations=grow)


def write_grid(path, header_lines, z, decimals):
    fmt = f"{{:.{decimals}f}}"
    with open(path, "w", newline="") as f:
        for hl in header_lines:
            f.write("# " + hl + "\n")
        f.write("row," + ",".join(f"c{j}" for j in range(z.shape[1])) + "\n")
        for i, row in enumerate(z):
            f.write(str(i) + "," + ",".join("" if v != v else fmt.format(v) for v in row) + "\n")
