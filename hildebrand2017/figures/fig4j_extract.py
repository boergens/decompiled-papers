"""Fig. 4j: 6 x 6 pair matrix, colour-coded with a key; digitized from the 150 ppi raster on PDF page 29 (tier 3).
Each cell's median inner colour is matched to the nearest colour of the printed key. Writes fig4j.csv + overlay."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, overlay  # noqa: E402
from pairs_matrix import run  # noqa: E402

a = embedded_image(str(ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"), 29)
hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Fig. 4j: variance per pair across z: upper triangle = variance in a (key 0-22.5 deg), lower triangle = variance in d (key 0-1 um).",
    "Rows/columns: the 6 left-right pairs in the order of the printed colour dots (MeMv, MeMd, MeLr, MeLm, MeLc, Mauthner;",
    "colour code of Fig. 4f). Diagonal cells are empty (white) in the figure.",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 29 (figures/fig4j_extract.py): median colour",
    "of the inner 7x7 px of each 13x13 px cell matched to the nearest colour of the printed key (a blue-to-green map, linear from",
    "0 at the bottom edge to the top label at the top edge; the key is only ~86 px tall). Uncertainty about +-3 % of the key",
    "range for blue cells; colours between blue and green are less certain. rgb_dist = RGB distance to the matched key colour.",
]
rows, pts = run(a, [21, 36, 50, 65, 80, 95], [696, 711, 725, 740, 754, 769], 13, 13, (145, 149, 701, 786),
                ("variance in a across z", "deg", 22.5), ("variance in d across z", "um", 1.0), HERE / "fig4j.csv", hdr)
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts, str(ROOT / "work" / "fig4j_overlay.png"))
for r in rows:
    print(r)
