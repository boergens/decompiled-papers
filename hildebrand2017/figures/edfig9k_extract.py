"""Extended Data Fig. 9k: heatmap of the linearized distance difference d (um; key 0 to 8 um) for all pairs of the 22 identified
left-right axon pairs (44 reticulospinal neurons) across slices, digitized from the 150 ppi raster on PDF page 43
(tier 3) as a grid at the image's native resolution. Writes edfig9k.csv."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import heatmap_grid  # noqa: E402
from digitize_common import embedded_image, fit_axis  # noqa: E402
from histo_common import tick_centres  # noqa: E402

a = embedded_image(str(ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"), 43)
ink = 255 - a.astype(float).mean(2)
# x axis below panel k: 10 ticks every 1000 slices (labels 2013, 5013, 8013, 11013) on image row 1317
xt = [40 + t for t in tick_centres(ink[1317, 40:940], 60)]
assert len(xt) == 10, xt
fx, resx, mx = fit_axis(xt, [2013 + 1000 * k for k in range(10)])
hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Extended Data Fig. 9k: linearized distance difference d (um; key 0 to 8 um) between pairs of",
    "identified axons for the 22 left-right pairs analysed in 2D (panel i), per slice (heatmap; black = no reconstruction data).",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 43 (figures/edfig9k_extract.py) at native",
    "resolution: one CSV row per image pixel row (px_row), one column per image pixel column; column header = slice at the",
    f"column centre ({abs(mx):.2f} slices per pixel; calibrated on the 10 ticks 2013..11013 under panel k, max residual",
    f"{resx:.1f} slices; the map spans image columns 59-929 and rows 952, 1312).",
    "The map has one band per pair of axons (22 choose 2 = 231 bands if all pairs are shown; the figure does not label them)",
    "but only ~1.56 pixel rows per band, so single pairs are NOT resolved: pair_index is only the band an equal-height split",
    "of the map would put the pixel row in (approximate; the pair names are not printed and are left empty).",
    "Values: colour matched to the nearest colour of the printed key (linear, 0 at the bottom edge to the top label at the",
    "top edge, 361 px tall); empty = black (no data) or no match. JPEG noise: treat values as +-5 % of the key range.",
    "Pixels darkened by blending with thin black no-data stripes were matched on colour direction (chromaticity) instead.",
]
val, md = heatmap_grid.extract(a, 952, 1312, 59, 929, (938, 949, 952, 1312), 8.0, fx, 231, None, HERE / "edfig9k.csv", hdr, ndp=2)
print(heatmap_grid.extract.stats, val.shape, round(md, 1))
