"""Fig. 4b: 22 x 22 matrix of 3D symmetry costs (left axon vs reflected right axon), colour-coded with a key
from 2000 to 6000. Digitized from the 150 ppi raster image on PDF page 29 (tier 3): each cell's colour (median of
its inner pixels, asterisk and outline pixels excluded) is matched to the nearest colour of the printed colour bar.
Writes fig4b.csv and work/fig4b_overlay.png (cell sample centres) and work/fig4b_check.png (re-rendered cells).
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, overlay, write_csv  # noqa: E402
from cmap_common import bar_lut, lookup  # noqa: E402

PDF = ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"
a = embedded_image(str(PDF), 29)

NAMES = ["MiD3cm", "RoM2L", "RoM1C", "MeLc", "RoM3M #1", "MeLr", "MiD3i", "Mauthner", "RoM3L", "MiD2cm", "MiD2i",
         "MiR1", "MiM1 #1", "MiR2", "RoM2M", "MiM1 #2", "MeMd", "RoM3M #2", "MeLm", "MeMv", "CaV", "RoM1R"]
# white separator lines (image pixels): columns 605 .. 926.5, rows 4.5 .. 326, 22 cells each way
X0, X1, Y0, Y1 = 605.0, 926.5, 4.5, 326.0
pw, ph = (X1 - X0) / 22, (Y1 - Y0) / 22
lut = bar_lut(a, 934, 941, 5, 326, 6000.0, 2000.0)

rows, pts = [], []
check = np.full((22, 22, 3), 255, np.uint8)
for i in range(22):          # row = left axon
    for j in range(22):      # column = right axon
        cx, cy = X0 + pw * (j + 0.5), Y0 + ph * (i + 0.5)
        yc, xc = int(round(cy)), int(round(cx))
        blk = a[yc - 4:yc + 5, xc - 4:xc + 5].reshape(-1, 3).astype(int)
        lum = blk.mean(1)
        dark = lum < 0.6 * np.median(lum)                        # black asterisk / outline (relative to the cell)
        red = (blk[:, 0] > 150) & (blk[:, 1] < 90) & (blk[:, 2] < 90)  # red asterisk
        star = "red" if red.sum() >= 3 else ("black" if dark.sum() >= 3 else "")
        good = blk[~dark & ~red]
        rgb = np.median(good, 0)
        v, d, k = lookup(rgb[None], lut)
        v, d, k = float(v[0]), float(d[0]), int(k[0])
        flag = "ok"
        if k <= 2:
            flag = ">=6000 (top of key, saturated)"
        elif v < 2150:
            flag = "near bottom of key (yellow); costs <= 2000 look the same"
        if d > 40:
            flag += "; colour far from key"
        rows.append((NAMES[i], NAMES[j], i + 1, j + 1, round(v, -1), round(d, 1), star, flag))
        pts.append((cx, cy))
        check[i, j] = rgb.astype(np.uint8)
hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Fig. 4b: pairwise 3D bilateral symmetry costs for 44 identified reticulospinal",
    "neurons (22 per side); rows = left axon (axis 'left'), columns = right axon (axis 'right'), names in the printed order.",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 29 (figures/fig4b_extract.py): median colour of",
    "the 9x9 px cell centre (asterisk and outline pixels removed) matched to the nearest colour of the printed colour bar",
    "(rows 5-326 of the image, linear 6000 at the top edge to 2000 at the bottom edge; parula-like map, dark blue = high).",
    "cost: value of the matched key colour, rounded to 10; resolution of the key ~12.5 cost units per pixel row, but",
    "JPEG noise (chroma subsampling bleeds the white separators and black asterisks into the cells) makes the uncertainty larger:",
    "checked against the costs printed in Fig. 4c and Extended Data Fig. 9a,d: MiD3cm/MiD3cm 2006 (printed 1315, below the key),",
    "MiD2cm/MiD2cm 2006 (2054), MiD2i/MiD2i 2031 (2062), MiM1 #1/MiM1 #1 2354 (2321), MiD2i/MiM1 #1 2354 (2242),",
    "MiM1 #1/MiD2i 2155 (1967), CaV/MeMv 5968 (14608, above the key): about +-50 to +-200 near the yellow end, where the key",
    "colours change slowly; take the values as about +-150 overall.",
    "Costs outside 2000-6000 are clipped by the colour scale: flag says so ('>=6000' for the dark navy cells; the paper",
    "prints 1315 for the MiD3cm pair and 14608 for MeMv right vs CaV left in Fig. 4c, both outside the key).",
    "rgb_dist: RGB distance to the matched key colour (quality). asterisk: black = globally optimal assignment;",
    "red = optimal assignment that is not the left-right homolog (Fig. 4b caption).",
    "columns: left; right; row (1-22); col (1-22); cost; rgb_dist; asterisk; flag",
]
write_csv(HERE / "fig4b.csv", hdr, ["left", "right", "row", "col", "cost", "rgb_dist", "asterisk", "flag"], rows,
          fmt=["{}", "{}", "{}", "{}", "{:.0f}", "{:.1f}", "{}", "{}"])
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts, str(ROOT / "work" / "fig4b_overlay.png"))
from PIL import Image  # noqa: E402
Image.fromarray(check).resize((220, 220), Image.NEAREST).save(ROOT / "work" / "fig4b_check.png")
print(sum(1 for r in rows if r[6]), "asterisks;", sum(1 for r in rows if "far" in r[7]), "far colours;",
      sum(1 for r in rows if ">=6000" in r[7]), "saturated high")
