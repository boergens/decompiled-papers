"""Stack the horizontal image strips of a figure that the PDF stores as many thin images (fu2025 Figs. 2 and 9).

stack_strips(pdf, page, bbox) -> RGB uint8 array: every image on <page> (1-based) whose placement lies inside
bbox (PDF points), sorted top to bottom and concatenated; all strips must have the same pixel width.
Indexed (palette) and soft-masked strips are converted to RGB on white."""
import numpy as np
import pymupdf


def stack_strips(pdf, page, bbox):
    doc = pymupdf.open(str(pdf))
    p = doc[page - 1]
    x0, y0, x1, y1 = bbox
    infos = [i for i in p.get_image_info(xrefs=True)
             if i["bbox"][0] >= x0 - 1 and i["bbox"][1] >= y0 - 1 and i["bbox"][2] <= x1 + 1 and i["bbox"][3] <= y1 + 1]
    infos.sort(key=lambda i: i["bbox"][1])
    parts = []
    for i in infos:
        pix = pymupdf.Pixmap(doc, i["xref"])
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
        if pix.colorspace is None or pix.colorspace.n != 3:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        arr = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
        smask = doc.xref_get_key(i["xref"], "SMask")
        if smask[0] == "xref":
            m = pymupdf.Pixmap(doc, int(smask[1].split()[0]))
            al = np.frombuffer(m.samples, np.uint8).reshape(m.height, m.width).astype(float) / 255
            arr = (arr * al[:, :, None] + 255 * (1 - al[:, :, None])).astype(np.uint8)
        parts.append(arr)
    widths = {a.shape[1] for a in parts}
    assert len(widths) == 1, widths
    return np.vstack(parts), [i["bbox"] for i in infos]
