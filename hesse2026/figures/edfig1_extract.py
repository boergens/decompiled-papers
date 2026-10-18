"""Extraction script for Extended Data Figure 1 (PDF page 41): four MRI panels.
Saves the embedded rasters at native resolution, the colourbar image, and 300-dpi renders of
each panel clip (raster + vector annotations: scale bar, arrow, label, colourbar)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import pdfplot as pp
import numpy as np
from PIL import Image

PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "2026.10.15.759299v1.full.pdf")
page = pp.open_page(PDF, 41)
OUT = os.path.dirname(os.path.abspath(__file__))

panels = {  # letter: (xref of MRI image, clip of the whole panel incl. annotations)
    "a": (298, pp.R(17, 19, 106, 109)),
    "b": (299, pp.R(144, 19, 233, 109)),
    "c": (301, pp.R(273, 19, 363, 109)),
    "d": (300, pp.R(401, 19, 491, 109)),
}
imgs = {im["xref"]: im for im in pp.images(page) if im["xref"] != 297}
for p, (xref, clip) in panels.items():
    w, h = pp.extract_image(page, xref, f"{OUT}/edfig1{p}_mri_native.png")
    bb = imgs[xref]["bbox"]
    print(p, "native", w, "x", h, "px; placed at", [round(v, 2) for v in bb], "->", round(bb[2]-bb[0], 2), "x", round(bb[3]-bb[1], 2), "pt",
          "=> %.1f dpi" % (w / ((bb[2]-bb[0]) / 72)))
    W, H = pp.render(page, clip, 300, f"{OUT}/edfig1{p}.png")
    print("   render", W, "x", H)
# colourbar (same xref placed 4 times, mirrored horizontally: transform has negative a)
cw, ch = pp.extract_image(page, 297, f"{OUT}/edfig1_colourbar_native.png")
print("colourbar native", cw, "x", ch)
cb = np.array(Image.open(f"{OUT}/edfig1_colourbar_native.png").convert("RGB"))
print("colourbar rows (top->bottom), mean RGB over columns:")
for r in range(ch):
    print("  row", r, cb[r].mean(axis=0).round(0))
# scale bars: white filled rectangles ~2.3 pt wide
for d in pp.drawings(page):
    if d["rects"] and pp.hexcolor(d["fill"]) == "#ffffff":
        x0, y0, x1, y1 = d["rect"]
        if 1 < (x1 - x0) < 4 and (y1 - y0) > 5:
            print("scale bar at x=%.2f, y %.2f..%.2f, length %.2f pt" % ((x0+x1)/2, y0, y1, y1 - y0))
