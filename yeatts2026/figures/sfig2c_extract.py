#!/usr/bin/env python3
"""Extract Supplemental Figure 2, panel c (two grey-scale depth-profile images, "without and with background
subtraction", each with a grey colour bar without numbers) of Yeatts et al. 2026 as grey-level grids.

Source: the one embedded raster image of the whole figure (768 x 652 px, ~121 ppi) in yeatts2026_supplement.pdf
p. 3.  The two B-scan images sit in the lower part of the figure (found as the two blocks of rows/columns that are
dark), each with a narrow grey bar (black at the bottom, white at the top) to its right.

    python3 -I sfig2c_extract.py   -> sfig2ctop.csv, sfig2cbottom.csv (+ ../work/sfig2c_boxes.png)

Output: one CSV per image, a grid at the source image's native resolution: one row per pixel row (top = shallow,
the "Depth" axis of panel b runs downwards here), one column per pixel column, values = 8-bit grey level
(mean of R, G, B; 0 = black, 255 = white).  The colour bar has no numbers, so the grey levels are NOT calibrated
in dB; the bar's own ramp (grey level vs fraction of the bar height) is sampled in the header to show that the
display map is linear.  Provenance: tier 3 (raster, uncalibrated).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break   # digitize_common.py
import numpy as np  # noqa: E402
from digitize_common import embedded_image, gray  # noqa: E402

PDF = os.path.join(HERE, "../source/yeatts2026_supplement.pdf")


def runs_of(idx, gap=0):
    groups = []
    for i in idx:
        if groups and i <= groups[-1][1] + 1 + gap:
            groups[-1][1] = i
        else:
            groups.append([i, i])
    return [tuple(g) for g in groups]


def main():
    a = embedded_image(PDF, 3)
    g = gray(a)
    nonwhite = g < 245
    lower = nonwhite[262:, :]
    # image rows: rows with >= 300 non-white pixels; two blocks (top image, bottom image)
    rows = np.where(lower.sum(1) >= 300)[0] + 262
    blocks = [b for b in runs_of(rows, gap=2) if b[1] - b[0] > 50]
    assert len(blocks) == 2, blocks
    boxes = {}
    for name, (r0, r1) in zip(("top", "bottom"), blocks):
        colmask = nonwhite[r0:r1 + 1, :].mean(0) >= 0.5
        cruns = [c for c in runs_of(np.where(colmask)[0]) if c[1] - c[0] > 5]
        img = max(cruns, key=lambda c: c[1] - c[0])           # the wide B-scan
        bar = [c for c in cruns if c[0] > img[1]]              # the narrow bar to its right
        assert bar, cruns
        bar = bar[0]
        # the bar's own vertical extent (it is shorter than the image at the top)
        brows = np.where(nonwhite[r0:r1 + 1, bar[0]:bar[1] + 1].mean(1) >= 0.5)[0] + r0
        boxes[name] = dict(img=(r0, r1, img[0], img[1]), bar=(brows[0], brows[-1], bar[0], bar[1]))
    for name, bx in boxes.items():
        r0, r1, c0, c1 = bx["img"]
        br0, br1, bc0, bc1 = bx["bar"]
        grid = g[r0:r1 + 1, c0:c1 + 1]
        ramp = g[br0 + 2:br1 - 1, (bc0 + bc1) // 2]     # the bar's interior (its outline is grey)
        nb = len(ramp)
        samples = [(1 - k / 10, float(ramp[int(round(k / 10 * (nb - 1)))])) for k in range(11)]
        out = os.path.join(HERE, "sfig2c%s.csv" % name)
        with open(out, "w") as f:
            for h in [
                "Yeatts et al. 2026 (bioRxiv 10.64898/2026.06.11.731509), Supplemental Figure 2, panel c, %s image:" % name,
                "  depth profiles (B-scan) in dB scale %s background subtraction (the caption's order: 'without and with')." % ("without" if name == "top" else "with"),
                "Grid of 8-bit grey levels at the source image's native resolution (%d rows x %d columns; the embedded figure" % grid.shape,
                "  image is 768 x 652 px at ~121 ppi): row = pixel row from the top of the image (depth increases downwards),",
                "  col = pixel column (lateral position, left to right), value = grey level 0 (black) .. 255 (white), mean of R,G,B.",
                "UNCALIBRATED: the grey colour bar to the right of the image has no numbers, so no dB values can be assigned.",
                "  The bar runs white (top) to black (bottom); its ramp (interior of the bar, its 2-px grey outline left out),",
                "  sampled at 11 points as (fraction of bar height from the bottom, grey level): %s" % ", ".join("(%.1f, %.0f)" % s for s in samples),
                "  (linear within a few grey levels, so grey level/255 = position on the bar).",
                "Source pixels: image rows %d..%d, columns %d..%d; bar rows %d..%d, columns %d..%d." % (r0, r1, c0, c1, br0, br1, bc0, bc1),
                "Provenance: tier 3, raster values copied from the embedded image by sfig2c_extract.py (no vector data,",
                "  no numbers on the bar). The grid is the published rendering, not the authors' data.",
            ]:
                f.write("# " + h + "\n")
            f.write("row," + ",".join("c%d" % k for k in range(grid.shape[1])) + "\n")
            for i, line in enumerate(grid):
                f.write("%d," % i + ",".join("%d" % v for v in np.rint(line)) + "\n")
        print(out, grid.shape, "bar", bx["bar"], "ramp", samples[0], samples[5], samples[-1])
    # QA: draw the detected boxes on the image
    from PIL import Image, ImageDraw
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    for bx in boxes.values():
        r0, r1, c0, c1 = bx["img"]
        d.rectangle([c0, r0, c1, r1], outline=(255, 0, 255))
        r0, r1, c0, c1 = bx["bar"]
        d.rectangle([c0, r0, c1, r1], outline=(0, 200, 0))
    im.save(os.path.join(HERE, "../work/sfig2c_boxes.png"))


if __name__ == "__main__":
    main()
