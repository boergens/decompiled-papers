"""Extended Data Fig. 9h: 'concatenation of linearized difference matrices': two heatmaps (top: angle difference a,
key 0-180 deg; bottom: distance difference d, key 0-8 um) for the 15 pairs of the 6-pair subset over slices ~4600-8250,
digitized from the 150 ppi raster on PDF page 43 (tier 3) as grids at native resolution.
Writes edfig9h_a.csv and edfig9h_d.csv."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import heatmap_grid  # noqa: E402
from digitize_common import embedded_image, fit_axis  # noqa: E402

a = embedded_image(str(ROOT / "source" / "hildebrand2017_biorxiv_134882.pdf"), 43)
# ticks under the bottom map (image row 420): 5013 (labelled, col 702), 6013, 7013, 8013 (labelled, col 919);
# a fifth mark at col 741.5 is the red slice-5560 marker and is not used.
fx, resx, mx = fit_axis([702.0, 773.5, 848.5, 919.0], [5013, 6013, 7013, 8013])
P = ["MeMv", "MeMd", "MeLr", "MeLm", "MeLc", "Mauthner"]
pairs = [f"{P[i]}-{P[j]}" for i in range(6) for j in range(i + 1, 6)]
for name, r0, r1, vmax, q, ndp in (("a", 246, 326, 180.0, "angle difference a (degrees; key 0 to 180 deg)", 1),
                                    ("d", 333, 412, 8.0, "distance difference d (um; key 0 to 8 um)", 2)):
    hdr = [
        f"Hildebrand et al. 2017 (bioRxiv 134882), Extended Data Fig. 9h ({'top' if name == 'a' else 'bottom'} map): linearized {q}",
        "for the 15 pairs of the 6 identified left-right axon pairs (same subset as Fig. 4g,h), per slice; black = no data.",
        "Provenance: tier 3, digitized from the embedded 150 ppi raster on PDF page 43 (figures/edfig9h_extract.py) at native",
        "resolution: one CSV row per image pixel row, one column per image pixel column (header = slice at the column centre,",
        f"{abs(mx):.2f} slices per pixel). x calibrated on the 4 ticks 5013, 6013, 7013, 8013 (only 5013 and 8013 labelled), max",
        f"residual {resx:.1f} slices; the map spans image columns 680-935 and rows {r0}-{r1}. pair_index/pair: the pair band",
        "(~5.3 pixel rows each) containing that pixel row, in the dot order MeMv, MeMd, MeLr, MeLm, MeLc, Mauthner (as Fig. 4g).",
        "A faint red vertical line (slice 5560 marker) crosses the maps near image column 741; pixels it tints may be empty or off.",
        "Values: nearest colour of the printed key (linear, 0 at the bottom edge to the top label at the top edge, ~80 px tall);",
        "empty = black (no data) or no match; darkened pixels matched on colour direction. Treat values as +-5 % of the key range.",
    ]
    val, md = heatmap_grid.extract(a, r0, r1, 680, 935, (942, 950, r0, r1), vmax, fx, 15, pairs,
                                   HERE / f"edfig9h_{name}.csv", hdr, ndp=ndp)
    print(name, heatmap_grid.extract.stats, val.shape, round(md, 1), resx)
