"""Shared helper for the Supplementary-figure digitizing scripts of kubota2018.

tools/digitize_common.embedded_image() fails on this SI: the soft masks are stored at a
different resolution from the JPEG they belong to (e.g. 887x331 image, 2417x900 SMask), so
the alpha array does not broadcast. All these SMasks are fully opaque (every value 255), so
here the SMask is resized to the image size before compositing (equivalent to ignoring it).
"""
import os
import sys

import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", "tools"))
sys.path.insert(0, TOOLS)
SI_PDF = os.path.normpath(os.path.join(HERE, "..", "source", "41467_2017_2768_MOESM1_ESM.pdf"))
WORK = os.path.normpath(os.path.join(HERE, "..", "work"))


def si_image(page):
    """Embedded figure image of SI page <page> (1-based) as RGB uint8, native resolution."""
    doc = pymupdf.open(SI_PDF)
    info = max(doc[page - 1].get_image_info(xrefs=True), key=lambda i: i["width"] * i["height"])
    xref = info["xref"]
    pix = pymupdf.Pixmap(doc, xref)
    if pix.n - pix.alpha != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(float)
    sm = doc.xref_get_key(xref, "SMask")
    if sm[0] == "xref":
        m = pymupdf.Pixmap(doc, int(sm[1].split()[0]))
        al = Image.fromarray(np.frombuffer(m.samples, np.uint8).reshape(m.height, m.width))
        al = np.asarray(al.resize((pix.width, pix.height), Image.BILINEAR), float) / 255
        a = a * al[:, :, None] + 255 * (1 - al[:, :, None])
    return a.astype(np.uint8)


def read_csv(path):
    import csv
    with open(path) as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines))
