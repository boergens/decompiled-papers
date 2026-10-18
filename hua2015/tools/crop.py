#!/usr/bin/env python3
"""Render a region of a PDF page to PNG (for figure images and for checking a re-plot).

Usage:
    python3 -I crop.py <pdf> <page> <x0> <y0> <x1> <y1> <out.png> [dpi]

<page> is 1-based; coordinates in PDF points, origin top left. Default 200 dpi.
Use the whole page box (0 0 W H) when in doubt; vector_dump.py prints the page size.
"""
import sys

import pymupdf

if len(sys.argv) not in (8, 9):
    sys.exit(__doc__)
pdf, page, x0, y0, x1, y1, out = sys.argv[1:8]
dpi = int(sys.argv[8]) if len(sys.argv) == 9 else 200
doc = pymupdf.open(pdf)
p = doc[int(page) - 1]
clip = pymupdf.Rect(float(x0), float(y0), float(x1), float(y1))
z = dpi / 72
p.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z)).save(out)
print(out)
