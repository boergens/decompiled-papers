"""Convert the six CSP-coloured side views of Figure 8 of Xie & Fang 2019 (Nanoscale Res Lett 14:370, PDF p. 8) to
centro-symmetry parameter values through the printed colour key (10 at the top, 3 at the bottom).

Source: the embedded 300 ppi image of Fig. 8 (1949 x 1671 px).
    python3 -I -B fig8_extract.py   -> fig8a.csv.gz ... (+ ../work/fig8_map_check.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import extract_figure  # noqa: E402

PANELS = {'a': (6, 8, 920, 550), 'b': (939, 8, 1854, 550), 'c': (6, 559, 920, 1103), 'd': (939, 559, 1854, 1103), 'e': (6, 1118, 920, 1664), 'f': (939, 1118, 1854, 1664)}
cfg = dict(
    pdf=str(HERE.parent / "source" / "xie2019.pdf"), page=8, bbox=(63.8, 312.2, 531.5, 713.1), shape=(1671, 1949),
    bar=(1913, 1928, 615, 965, 10.0, 3.0), panels=PANELS, decimals=2, stem="fig8",
    header=[
        "Xie & Fang 2019, Nanoscale Research Letters 14:370, Fig. 8({panel}): side view of the workpiece during cutting, atoms coloured by centro-symmetry parameter (CSP);",
        "  colour key 'CSP': 10 dark red at the top, 3 dark blue at the bottom. Per the text, atoms with CSP smaller than 3 (perfect FCC) are omitted.",
        "Grid: one row per pixel row, one column per pixel column of the embedded 300 ppi image, cropped to the panel",
        "  ({box} of the 1949 x 1671 px image); c0 = left edge. Pixel coordinates only: the figure has no length scale.",
        "Values: in CSP (dimensionless), read through the printed colour key. Provenance: tier 3, colour key conversion by fig8_extract.py",
        "  (tools/colourkey_map.py): the key is sampled down its centre between its ends, which are taken as the printed end",
        "  values; pixels and key rows are matched on hue (the atoms are shaded, highlighted spheres, so brightness varies;",
        "  hue does not) and each pixel gets the median value of the key rows matching its hue.",
        "Empty cells: not an atom colour (white background, grey tool atoms, black labels and frames, unsaturated sphere",
        "  edges, anti-aliasing).",
        "Limits: the key's dark ends differ from their neighbours only in brightness, not hue, so values in {ends} CSP (dimensionless)",
        "  (the dark-blue/blue and red/dark-red runs) cannot be told apart and are given as the middle of the run; values",
        "  beyond the key's end values (if the rendering clamps them) are indistinguishable from the end colours. Elsewhere",
        "  about +-0.2 (JPEG colour noise; coarser in the green part of the key, where hue changes fast). Use local medians",
        "  (per atom), not single pixels.",
    ])
ends, stats = extract_figure(cfg, HERE)
print("ends", ends)
for k, v in stats.items():
    print(k, v)
