"""Fig. 4g: heatmap of the linearized angle difference a (degrees; key 0 to 180 deg) for the 15 pairs across slices, digitized from the
150 ppi raster on PDF page 29 (tier 3) as a grid at the image's native resolution. Writes fig4g.csv."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image, fit_axis  # noqa: E402
from heatmap_grid import extract  # noqa: E402
from histo_common import tick_centres  # noqa: E402

a = embedded_image(str(ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"), 29)
ink = 255 - a.astype(float).mean(2)
# shared x axis with panel i: ticks every 1000 slices (2013 ... 11013) on row 780, red marker at cols 519-521 dropped
xt = [t for t in (262 + v for v in tick_centres(ink[780, 262:940], 60)) if abs(t - 520) > 3]
fx, resx, mx = fit_axis(xt, [2013 + 1000 * k for k in range(10)])
P = ["MeMv", "MeMd", "MeLr", "MeLm", "MeLc", "Mauthner"]
pairs = [f"{P[i]}-{P[j]}" for i in range(6) for j in range(i + 1, 6)]   # order of the dot pairs left of the map
hdr = [
    "Hildebrand et al. 2017 (bioRxiv 134882), Fig. 4g: linearized angle difference a (degrees; key 0 to 180 deg) between all 15 pairs of the 6 identified",
    "left-right axon pairs, per slice (heatmap; black = no reconstruction data for that pair).",
    "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 29 (figures/fig4g_extract.py) at native",
    "resolution: one CSV row per image pixel row (px_row), one column per image pixel column; the column header is the slice",
    f"at the column centre ({abs(mx):.2f} slices per pixel; x axis shared with panel i, calibrated on its 10 ticks 2013..11013,",
    f"max residual {resx:.1f} slices; the map spans image columns 269-936). Each of the 15 pair rows is ~5.3 pixel rows tall;",
    "pair_index/pair = the pair whose band contains that pixel row (pair names from the coloured dot pairs at the left, in the",
    "order MeMv, MeMd, MeLr, MeLm, MeLc, Mauthner = Fig. 4f key; first dot = row axon, second = column axon).",
    "Pixel rows at band borders mix two pairs. Values: colour matched to the nearest colour of the printed key (linear, 0 at",
    "the bottom edge to the top label at the top edge, ~80 px tall: ~2.3 deg or ~0.1 um per key pixel); empty = black (no",
    "data) or a colour far from the key. JPEG noise: treat values as +-5 % of the key range. Pixels darkened by blending with",
    "thin black no-data stripes were matched on colour direction (chromaticity) instead; counts are in the line below.",
    "The red slice-5560 marker line (image columns 519-521) hides the map there; those columns are empty.",
]
import heatmap_grid  # noqa: E402
val, md = heatmap_grid.extract(a, 537, 616, 269, 936, (942, 949, 537, 616), 180.0, fx, 15, pairs, HERE / "fig4g.csv", hdr, ndp=1)
print(heatmap_grid.extract.stats)
print(val.shape, "mean key distance", round(md, 1), "empty", int(np.isnan(val).sum()))
