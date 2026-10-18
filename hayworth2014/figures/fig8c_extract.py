"""Fig. 8C of Hayworth et al. 2014: the sixteen tile quality values printed on the stage-stitched montage.

Not a plot with axes: the numbers are printed labels, read by eye from the embedded 300 ppi JPEG
(PDF p. 14, image xref 126, panel C = right part of the image) at 2-6x zoom and on a colour mask of the green/red label pixels (work/z8c_mask.png). Writes fig8c_values.csv
next to this script. The readings are typed in below; this script documents and re-creates the CSV and
writes ../work/fig8c_labels.png (the panel cut out at 2x) for re-checking.
"""
import csv
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# (row, col, value, colour, certainty) rows 1-4 top to bottom, cols 1-4 left to right
READ = [
    (1, 1, "41.27", "green", "clear"), (1, 2, "39.85", "green", "probable (39.65 possible)"),
    (1, 3, "39.45", "green", "clear"), (1, 4, "36.41", "green", "probable (38.41 possible)"),
    (2, 1, "37.98", "green", "probable (37.88 possible)"), (2, 2, "38.28", "green", "clear"),
    (2, 3, "43.91", "green", "probable (40.91 possible)"), (2, 4, "39.67", "green", "probable (38.67 possible)"),
    (3, 1, "41.51", "green", "clear"), (3, 2, "41.81", "green", "clear"),
    (3, 3, "35.48", "green", "clear"), (3, 4, "27.25", "red", "clear"),
    (4, 1, "41.05", "green", "probable (41.09 possible)"), (4, 2, "37.24", "green", "clear"),
    (4, 3, "38.91", "green", "probable (36.91 possible)"), (4, 4, "41.09", "green", "probable (41.03 possible)"),
]

doc = pymupdf.open(ROOT / "source" / "hayworth2014.pdf")
pix = pymupdf.Pixmap(doc, 126)
a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
(ROOT / "work").mkdir(exist_ok=True)
Image.fromarray(a[:, 820:]).resize(((pix.width - 820) * 2, pix.height * 2)).save(ROOT / "work" / "fig8c_labels.png")

with open(HERE / "fig8c_values.csv", "w", newline="") as f:
    for line in [
        "Hayworth et al. 2014 Front. Neural Circuits 8:68, Figure 8C: stage-stitched montage of 4 x 4 tiles with",
        "  the quality value printed on each tile (green = passing, red = below threshold, per the caption).",
        "Columns: row (1 = top), col (1 = left), quality_value (as printed, unitless; the paper gives no unit or",
        "  threshold value), label_colour, reading (how sure the reading is).",
        "Provenance: tier 4, read by eye from the embedded 300 ppi JPEG (PDF p. 14); the digits are about 12 px",
        "  high and blurred by JPEG compression, so most second-decimal digits and some others are uncertain.",
        "Not a plotted panel: there are no axes; this CSV just records the printed numbers.",
    ]:
        f.write("# " + line + "\n")
    w = csv.writer(f)
    w.writerow(["row", "col", "quality_value", "label_colour", "reading"])
    w.writerows(READ)
print("wrote", HERE / "fig8c_values.csv")
