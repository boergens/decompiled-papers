"""Extended Data Fig. 9f: example difference matrix ('construction of difference matrix'), 6 x 6, colour-coded with a
key (upper triangle a, 0-180 deg; lower triangle d, 0-8 um); digitized from the 150 ppi raster on PDF page 43 (tier 3).
Each cell's median inner colour is matched to the nearest colour of the printed key. Writes edfig9f.csv + overlay."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, overlay  # noqa: E402
from pairs_matrix import run  # noqa: E402

a = embedded_image(str(ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"), 43)
hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Extended Data Fig. 9f: 'construction of difference matrix' for one slice:",
    "upper triangle = angle difference a (key 0-180 deg), lower triangle = distance difference d (key 0-8 um).",
    "Rows/columns: the 6 pairs in the order of the printed colour dots (MeMv, MeMd, MeLr, MeLm, MeLc, Mauthner; Fig. 4f",
    "colours). The panel does not say which slice; all 30 cells agree with Fig. 4e (slice 5560) within the reading error.",
    "Two cells are framed in magenta (row MeLr / column Mauthner, solid; row Mauthner / column MeLr, dashed); the frame",
    "pixels lie outside the sampled cell centres.",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 43 (figures/edfig9f_extract.py): median colour",
    "of the inner 7x7 px of each 13x13 px cell matched to the nearest colour of the printed key (~86 px tall, linear 0 at the",
    "bottom edge to the top label at the top edge). Uncertainty about +-3 % of the key range. rgb_dist = distance to the key colour.",
]
rows, pts = run(a, [257, 271, 286, 300, 315, 330], [288, 302, 317, 332, 347, 361], 13, 13, (380, 384, 293, 378),
                ("angle difference a", "deg", 180.0), ("distance difference d", "um", 8.0), HERE / "edfig9f.csv", hdr)
(ROOT / "work").mkdir(exist_ok=True)
overlay(a, pts, str(ROOT / "work" / "edfig9f_overlay.png"))
