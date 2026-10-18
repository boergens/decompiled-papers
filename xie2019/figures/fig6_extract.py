"""Convert the six top-view height maps of Figure 6 of Xie & Fang 2019 (Nanoscale Res Lett 14:370, PDF p. 7) to
z-direction heights through the printed colour key (-200 A at the top, -232 A at the bottom).

Source: the embedded 300 ppi JPEG of Fig. 6 (1949 x 1030 px).
    python3 -I -B fig6_extract.py   -> fig6a.csv.gz ... fig6f.csv.gz (+ ../work/fig6_map_check.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from colourkey_map import extract_figure, mask_outline_colour  # noqa: E402

ROWS = [(2, 338), (344, 680), (689, 1028)]
COLS = [(1, 917), (921, 1835)]
panels = {}
for i, (r0, r1) in enumerate(ROWS):
    for j, (c0, c1) in enumerate(COLS):
        panels["abcdef"[2 * i + j]] = (c0, r0, c1, r1)

cfg = dict(
    pdf=str(HERE.parent / "source" / "xie2019.pdf"), page=7, bbox=(63.8, 94.8, 531.5, 341.8), shape=(1030, 1949),
    post=lambda name, sub, z: mask_outline_colour(sub, z, 170, 250, 190) if name in "cd" else z,
    bar=(1880, 1893, 377, 730, -200.0, -232.0), panels=panels, decimals=1, stem="fig6",
    header=[
        "Xie & Fang 2019, Nanoscale Research Letters 14:370, Fig. 6({panel}): surface topography of the processed Cu (111) surface,",
        "  atoms coloured by z-direction height (colour key: -200 A dark red at the top, -232 A dark blue at the bottom).",
        "Grid: one row per pixel row, one column per pixel column of the embedded 300 ppi image, cropped to the panel",
        "  ({box} of the 1949 x 1030 px image); c0 = left edge. Pixel coordinates only: the figure has no length scale.",
        "Values: z-direction height in Angstrom, read through the printed colour key. Provenance: tier 3, colour key",
        "  conversion by fig6_extract.py (tools/colourkey_map.py): the key is sampled down its centre between its ends,",
        "  which are taken as the printed end values; pixels and key rows are matched on hue (the atoms are shaded,",
        "  highlighted spheres, so brightness and paleness vary; hue does not) and each pixel gets the median value of the",
        "  key rows matching its hue.",
        "Empty cells: not an atom colour (white gaps, black labels, dark outlines, unsaturated sphere edges, anti-aliasing).",
        "Limits: the key's dark ends differ from their neighbours only in brightness, not hue, so values in {ends} A (dark",
        "  blue/blue and red/dark red runs) cannot be told apart and are given as the middle of the run. Uncertainty about",
        "  +-1 A elsewhere (JPEG colour noise; coarser in the green part of the key, where hue changes fast). Use local",
        "  medians (per atom), not single pixels.",
        "  The blue outline ellipses drawn by the authors in panels c and d are not data (blanked: hue 170-250 deg, max channel < 190, grown 2 px).",
    ])
ends, stats = extract_figure(cfg, HERE)
print("ends", ends)
for k, v in stats.items():
    print(k, v)
