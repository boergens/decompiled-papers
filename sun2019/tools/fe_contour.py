"""Classify the pixels of an Abaqus PEEQ contour plot (Figs. 12-14 of sun2019) into the bands of its colour key.

Written for sun2019. The model is drawn with Abaqus' lighting, so a band's colour in the model is its key colour
times 206/255 (key blue 0,0,255 -> model 0,0,206; checked on the most frequent colours). Each pixel gets the code
of the nearest of these model colours if it is within MAX_DIST (RGB distance), else:
  '.' white background, 'K' the knife (grey 124,124,124), 'A' annotation area (colour key, panel label, axis
  triad; pixel boxes given by the caller), '#' anything else (black outlines, anti-aliased band boundaries).
Band codes: '0' = lowest band (0 to 5e-4) ... '7' = 2 to 3. The grey top band of some keys (3 to the panel's
maximum) is not classified: in the model it cannot be told apart from the anti-aliased grey edges of the knife and
of the image border (no uniform grey patch of that band is visible in any panel), so neutral greys other than the
knife are left as '#'.
"""
import numpy as np
import pymupdf

KEY = [  # key colour (as printed in the legend swatches), lower and upper band limit
    ((0, 0, 255), 0.0, 5e-4),
    ((0, 145, 255), 5e-4, 5e-3),
    ((0, 255, 218), 5e-3, 5e-2),
    ((0, 255, 72), 5e-2, 0.1),
    ((72, 255, 0), 0.1, 0.5),
    ((218, 255, 0), 0.5, 1.0),
    ((255, 145, 0), 1.0, 2.0),
    ((255, 0, 0), 2.0, 3.0),
    ((204, 204, 204), 3.0, None),   # upper limit = the panel's top key value
]
NAMES = ["blue", "light blue", "cyan", "spring green", "green", "yellow-green", "orange", "red", "grey"]
SHADE = 206 / 255
MAX_DIST = 30
KNIFE = (124, 124, 124)


def page_image(pdf, page, xref_near):
    doc = pymupdf.open(pdf)
    p = doc[page - 1]
    info = min(p.get_image_info(xrefs=True), key=lambda i: sum(abs(a - b) for a, b in zip(i["bbox"], xref_near)))
    pix = pymupdf.Pixmap(doc, info["xref"])
    if pix.n - pix.alpha != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()


def classify(a, annotation_boxes):
    """a: RGB uint8 panel image. Returns an array of single-character codes."""
    f = a.astype(float)
    ref = [np.array(c, float) * SHADE for c, _, _ in KEY[:8]]
    d = np.stack([np.sqrt(((f - r) ** 2).sum(2)) for r in ref], 0)
    best = d.argmin(0)
    out = np.full(a.shape[:2], "#", dtype="<U1")
    ok = d.min(0) <= MAX_DIST
    out[ok] = best[ok].astype(str)
    out[np.sqrt(((f - 255) ** 2).sum(2)) <= 12] = "."
    out[np.sqrt(((f - np.array(KNIFE, float)) ** 2).sum(2)) <= 8] = "K"
    for (c0, r0, c1, r1) in annotation_boxes:
        out[r0:r1, c0:c1] = "A"
    return out


def write_grid(path, header_lines, codes):
    with open(path, "w", newline="") as f:
        for h in header_lines:
            f.write("# " + h + "\n")
        f.write("row,codes\n")
        for i, row in enumerate(codes):
            f.write(f"{i},{''.join(row)}\n")


def render(codes, top_value=None):
    """Codes -> RGB image in the key colours (for re-plots and checks)."""
    pal = {str(i): c for i, (c, _, _) in enumerate(KEY)}
    pal.update({".": (255, 255, 255), "K": (124, 124, 124), "A": (235, 235, 235), "#": (0, 0, 0)})
    img = np.zeros(codes.shape + (3,), np.uint8)
    for k, c in pal.items():
        img[codes == k] = c
    return img


def header(fig, panel, caption, speed, thickness, top, key_values, page, n_counts):
    lines = [
        f"Sun & Gamstedt 2019, Nanomanuf Metrol 2:45-55, Fig. {fig}({panel}): {caption}",
        f"  Panel label: v0={speed} mm/s; cutting thickness t_u = {thickness} nm (caption). Quantity: PEEQ, the equivalent",
        "  plastic strain (Abaqus, 'Avg: 75%' averaging), as a discrete contour plot.",
        "Format: one CSV row per pixel row of the panel (row 0 = top), column 'codes' = one character per pixel column",
        "  (column 0 = left). Codes: '0'..'7' = PEEQ band of the panel's colour key (below); '.' = white background;",
        "  'K' = the knife (uniform grey); 'A' = annotation area (colour key, panel label box, axis triad; not data);",
        "  '#' = not classified (black outlines, anti-aliased pixels on band boundaries, and the grey top band of the",
        "  key, PEEQ > 3, where present: it cannot be told apart from the knife's anti-aliased grey edges).",
        "PEEQ bands (code: key colour, range): " + "; ".join(
            f"{i}: {NAMES[i]}, {lo:g}-{(hi if hi is not None else top):g}" for i, (c, lo, hi) in enumerate(KEY)
            if i < 8) + (f"; (grey band 3-{top:g} not classified)" if top > 3 else ""),
        f"  Key values printed in the panel (top to bottom): {key_values}.",
        "Geometry: the figure has no scale bar or axes, so positions are image pixels only (300 ppi placement in the",
        f"  PDF: 1 px = 0.24 pt on the page). The source image is the lossless embedded raster on PDF p. {page}",
        "  (1418 px wide); the panel is a horizontal strip of it (see the extract script for the row range).",
        "Provenance: tier 3, digitized: each pixel assigned to the nearest band colour of the key, the model colours",
        "  being the key colours times 206/255 (Abaqus shading), within an RGB distance of 30; see tools/fe_contour.py.",
        "  This is exact for the flat-shaded band interiors; band boundaries are uncertain by about 1 px.",
        "Pixel counts: " + ", ".join(f"{k}={v}" for k, v in n_counts),
    ]
    return lines
