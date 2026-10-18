"""Fig. 4e: 6 x 6 pair matrix, colour-coded with a key; digitized from the 150 ppi raster on PDF page 29 (tier 3).
Each cell's median inner colour is matched to the nearest colour of the printed key. Writes fig4e.csv + overlay."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, overlay  # noqa: E402
from pairs_matrix import run  # noqa: E402

a = embedded_image(str(ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"), 29)
hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Fig. 4e: difference matrix at z = 5560 (slice 5560): upper triangle = angle difference a (0-180 deg), lower triangle = distance difference d (0-8 um).",
    "Rows/columns: the 6 left-right pairs in the order of the printed colour dots (MeMv, MeMd, MeLr, MeLm, MeLc, Mauthner;",
    "colour code of Fig. 4f). Diagonal cells are empty (white) in the figure.",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 29 (figures/fig4e_extract.py): median colour",
    "of the inner 7x7 px of each 13x13 px cell matched to the nearest colour of the printed key (a blue-to-green map, linear from",
    "0 at the bottom edge to the top label at the top edge; the key is only ~86 px tall). Uncertainty about +-3 % of the key",
    "range for blue cells; colours between blue and green are less certain. rgb_dist = RGB distance to the matched key colour.",
]
rows, pts = run(a, [21, 36, 50, 65, 80, 95], [570, 584, 599, 614, 628, 643], 13, 13, (145, 149, 575, 660),
                ("angle difference a at z = 5560", "deg", 180.0), ("distance difference d at z = 5560", "um", 8.0), HERE / "fig4e.csv", hdr)
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts, str(ROOT / "work" / "fig4e_overlay.png"))
for r in rows:
    print(r)
