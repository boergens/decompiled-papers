"""Convert the four perspective views of Figure 11 of Xie & Fang 2019 (Nanoscale Res Lett 14:370, PDF p. 10) to
x-direction atomic displacement through the printed colour key (2.2 A at the top, -10.2 A at the bottom).

Source: the embedded 300 ppi image of Fig. 11 (1949 x 1095 px).
    python3 -I -B fig11_extract.py   -> fig11a.csv.gz ... (+ ../work/fig11_map_check.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import extract_figure  # noqa: E402

ARROWS = [(541, 125, 630, 150), (1315, 153, 1403, 179), (280, 732, 368, 758), (1158, 742, 1246, 768)]  # red 'Chip' arrows
G = 4
MASKS = {p: [(c0 - G, r0 - G, c1 + G, r1 + G) for c0, r0, c1, r1 in ARROWS] for p in 'abcd'}
PANELS = {'a': (0, 3, 906, 525), 'b': (906, 3, 1812, 525), 'c': (0, 535, 906, 1093), 'd': (906, 535, 1812, 1093)}
cfg = dict(
    pdf=str(HERE.parent / "source" / "xie2019.pdf"), page=10, bbox=(63.8, 440.4, 531.5, 703.0), shape=(1095, 1949),
    mask_boxes=MASKS,
    bar=(1876, 1892, 335, 703, 2.2, -10.2), panels=PANELS, decimals=2, stem="fig11",
    header=[
        "Xie & Fang 2019, Nanoscale Research Letters 14:370, Fig. 11({panel}): perspective view of the workpiece at cutting edge radius 2 nm, atoms coloured by x-direction atomic",
        "  displacement; colour key 'x-displacement': 2.2 A dark red at the top, -10.2 A dark blue at the bottom.",
        "Grid: one row per pixel row, one column per pixel column of the embedded 300 ppi image, cropped to the panel",
        "  ({box} of the 1949 x 1095 px image); c0 = left edge. Pixel coordinates only: the figure has no length scale.",
        "Values: in Angstrom (x-direction displacement), read through the printed colour key. Provenance: tier 3, colour key conversion by fig11_extract.py",
        "  (tools/colourkey_map.py): the key is sampled down its centre between its ends, which are taken as the printed end",
        "  values; pixels and key rows are matched on hue (the atoms are shaded, highlighted spheres, so brightness varies;",
        "  hue does not) and each pixel gets the median value of the key rows matching its hue.",
        "Empty cells: not an atom colour (white background, grey tool atoms, black labels and frames, unsaturated sphere",
        "  edges, anti-aliasing).",
        "Limits: the key's dark ends differ from their neighbours only in brightness, not hue, so values in {ends} Angstrom (x-direction displacement)",
        "  (the dark-blue/blue and red/dark-red runs) cannot be told apart and are given as the middle of the run; values",
        "  beyond the key's end values (if the rendering clamps them) are indistinguishable from the end colours. Elsewhere",
        "  about +-0.4 A (JPEG colour noise; coarser in the green part of the key, where hue changes fast). Use local medians",
        "  (per atom), not single pixels.",
        "This is a perspective rendering: pixel positions are not proportional to atom positions. The red 'Chip' arrows are",
        "  blanked (boxes, grown 4 px); white label text on the blue zone is not saturated and stays empty, but its",
        "  anti-aliased edges take the blue of the surrounding atoms.",
        "Caution: the rendered colours are not exactly the key's (the slipped-zone blue has hue ~250 deg, the key's blue",
        "  240 deg), so all values may carry a bias of the order of 1-2 A; the far, undisturbed workpiece maps to about",
        "  -1.6 A. See README. Treat the values as semi-quantitative.",
    ])
ends, stats = extract_figure(cfg, HERE)
print("ends", ends)
for k, v in stats.items():
    print(k, v)
