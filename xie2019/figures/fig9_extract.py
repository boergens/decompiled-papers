"""Convert the five CSP-coloured views of Figure 9 of Xie & Fang 2019 (Nanoscale Res Lett 14:370, PDF p. 9) to
centro-symmetry parameter values through the printed colour key (10 at the top, 3 at the bottom).

Source: the embedded 300 ppi image of Fig. 9 (1420 x 1140 px).
    python3 -I -B fig9_extract.py   -> fig9a.csv.gz ... (+ ../work/fig9_map_check.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import extract_figure  # noqa: E402

PANELS = {'a': (0, 0, 1331, 224), 'b': (0, 228, 1331, 450), 'c': (0, 452, 1331, 675), 'd': (0, 678, 1331, 908), 'e': (0, 911, 1331, 1140)}
cfg = dict(
    pdf=str(HERE.parent / "source" / "xie2019.pdf"), page=9, bbox=(127.3, 94.8, 468.0, 368.3), shape=(1140, 1420),
    bar=(1394, 1405, 402, 663, 10.0, 3.0), panels=PANELS, decimals=2, stem="fig9",
    header=[
        "Xie & Fang 2019, Nanoscale Research Letters 14:370, Fig. 9({panel}): subsurface defects (workpiece outline and defect atoms), atoms coloured by centro-symmetry parameter (CSP);",
        "  colour key 'CSP': 10 dark red at the top, 3 dark blue at the bottom. Per the text, atoms with CSP smaller than 3 (perfect FCC) are omitted.",
        "Grid: one row per pixel row, one column per pixel column of the embedded 300 ppi image, cropped to the panel",
        "  ({box} of the 1420 x 1140 px image); c0 = left edge. Pixel coordinates only: the figure has no length scale.",
        "Values: in CSP (dimensionless), read through the printed colour key. Provenance: tier 3, colour key conversion by fig9_extract.py",
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
