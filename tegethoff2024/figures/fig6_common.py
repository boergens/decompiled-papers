"""Shared code for the dot plots of Figure 6 (C, E, F): see fig6c/e/f_extract.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

SINGLE = 52   # area (px) of one isolated marker (median of isolated components, ~8 px across)


def resin_masks(a, names=RESINS, fill=()):
    pal = [RESIN_RGB[RESINS.index(n)] for n in names]
    lab = classify(a, pal, max_dist=45, min_sat=40)
    masks = {}
    for k, n in enumerate(names):
        m = lab == k
        masks[n] = fill_holes(m) if n in fill else m
        if n in fill:
            masks[n + "#orig"] = m
    return masks


def header(title, provenance_extra, ry, rx, sy, sx, yunit, xunit):
    return [
        f"Tegethoff & Briggman 2024 Front Neurosci 18:1286991, {title}",
        "Provenance: tier 3, digitized from the embedded ~305 ppi JPEG (no vector data in the PDF); markers found as",
        "  connected components of each resin colour (Lab nearest MATLAB default colour); a blob of overlapping markers",
        f"  holds n = round(area / {SINGLE} px) markers, placed with k-means on its pixels (positions approximate, about one",
        "  marker diameter); n_in_blob gives n (1 = isolated marker).",
    ] + provenance_extra + [
        f"  Axis fits: y max residual {ry:.3g} {yunit}; x max residual {rx:.3g} {xunit}.",
        f"Uncertainty: isolated markers +-{2 * abs(sy):.2g} {yunit} (2 px); markers in blobs about +-{8 * abs(sy):.2g} {yunit};",
        "  markers hidden completely behind others cannot be seen, so counts are lower limits.",
    ]
