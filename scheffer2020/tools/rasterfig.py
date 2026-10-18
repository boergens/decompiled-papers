"""Small shared helpers for the raster figures of scheffer2020 (written by fork B for Figs 10-18).

load(page) -> RGB numpy array (H, W, 3) of the largest embedded image on a 1-based page of
source/elife-57443-v4.pdf, at its native resolution; bbox(page) -> its placement on the page (PDF points).
read_csv(path) -> list of dicts, skipping '#' comment lines.
"""
import csv
from pathlib import Path

import numpy as np
import pymupdf

PDF = Path(__file__).resolve().parent.parent / "source" / "elife-57443-v4.pdf"


def _info(page):
    doc = pymupdf.open(PDF)
    p = doc[page - 1]
    infos = p.get_image_info(xrefs=True)
    i = max(infos, key=lambda i: pymupdf.Rect(i["bbox"]).width * pymupdf.Rect(i["bbox"]).height)
    return doc, i


def load(page):
    doc, i = _info(page)
    pix = pymupdf.Pixmap(doc, i["xref"])
    if pix.alpha:
        pix = pymupdf.Pixmap(pix, 0)
    if pix.n != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3).copy()


def bbox(page):
    return pymupdf.Rect(_info(page)[1]["bbox"])


def read_csv(path):
    with open(path, newline="") as f:
        rows = [r for r in f if not r.startswith("#")]
    return list(csv.DictReader(rows))
