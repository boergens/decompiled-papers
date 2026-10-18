"""Shared driver for figures/fig12_extract.py, fig13_extract.py, fig14_extract.py (PEEQ contour maps, sun2019).
Writes figures/fig<N><panel>.csv and work/fig<N><panel>_classified.png (source strip | classified map)."""
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / "figures"
import numpy as np  # noqa: E402
from fe_contour import page_image, classify, write_grid, render, header  # noqa: E402

PDF = str(HERE.parent / "source" / "sun2019.pdf")
# annotation boxes inside each panel strip (col0, row0, col1, row1): colour key, panel label box, axis triad
ANNOT = [(0, 0, 345, 300), (0, 655, 340, 730), (95, 590, 190, 668)]


def run(fig, page, bbox, panels, caption, thickness):
    a = page_image(PDF, page, bbox)
    for panel, r0, speed, key_values in panels:
        strip = a[r0:r0 + 730]
        top = float(key_values.split(",")[0])
        codes = classify(strip, ANNOT)
        cnt = sorted(Counter(codes.ravel().tolist()).items())
        write_grid(str(HERE / f"fig{fig}{panel}.csv"),
                   header(fig, panel, caption, speed, thickness, top, key_values, page, cnt), codes)
        from PIL import Image
        Image.fromarray(np.concatenate([strip, render(codes)], 1)).save(
            str(HERE.parent / "work" / f"fig{fig}{panel}_classified.png"))
        print(f"fig{fig}{panel}: rows {r0}-{r0 + 729}", cnt)
