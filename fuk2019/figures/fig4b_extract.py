"""Fig. 4b: bond-length distributions of the curing agents MTHPA and NA (solid lines) and of the
primary crosslinking structures DGEBA-MTHPA and DGEBA-NA (dashed lines) -> figures/fig4b.csv
(tier 3, digitized).

Run from anywhere: python3 -I figures/fig4b_extract.py. Embedded image 650 x 478 px, 220 ppi,
p. 6 of source/fuk2019.pdf. Method: tools/bondlen.py, plus the separation of solid and dashed
lines of the same colour: after removing text (hand-given boxes) and the red dotted ellipse
(components < 5 px), connected components with an extent of >= 25 px are taken as the solid
line, components of 5-24 px as dashes. Dashes that touch the solid line of the same colour merge
into it and are lost (those columns are missing for the dashed series); short visible pieces of a
solid line that is partly covered by the other colour can be mistaken for dashes, mainly on the
peak flanks where all four curves overlap (around 1.09-1.11 A) and along the zero baseline (where
all series are 0 anyway). Writes work/fig4b_overlay.png.
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bondlen as bl  # noqa: E402
import digitize_common as dc  # noqa: E402
import fukplot as fp  # noqa: E402

a = fp.load(6, (297.2, 559.8, 509.7, 716.4))
frame = (77, 635, 12, 419)        # axis box lines (frame_lines)
cal = bl.calibrate(a, frame, [1.1, 1.2, 1.3, 1.4, 1.5], [5, 10, 15, 20, 25, 30, 35])
L, R, T, B = frame
lab, _ = fp.classify(a, [(0, 0, 0), (255, 0, 0)])
TEXT = [(346, 343, 384, 359), (392, 316, 426, 331), (390, 402, 425, 417), (463, 343, 497, 358),
        (470, 170, 545, 225), (560, 25, 610, 55)]   # black labels C=C, C-O, C=C, C-O, C-C (+arrow), (b)
LEGEND = (110, 18, 290, 107)
masks = {}
for k, (solid, dashed) in enumerate([("MTHPA", "DGEBA-MTHPA"), ("NA", "DGEBA-NA")]):
    m = lab == k
    m[: T + 2, :] = False
    m[B - 1:, :] = False
    m[:, : L + 2] = False
    m[:, R - 1:] = False
    # tick marks (inward, up to ~9 px) on all four sides; the curves' zero baseline is 24 px above the bottom axis
    m[B - 11:, :] = False
    m[: T + 11, :] = False
    m[:, : L + 11] = False
    m[:, R - 11:] = False
    x0, y0, x1, y1 = LEGEND
    m[y0:y1, x0:x1] = False
    if k == 0:
        for x0, y0, x1, y1 in TEXT:
            m[y0:y1, x0:x1] = False
    ms, md = np.zeros_like(m), np.zeros_like(m)
    for r, c in fp.components(m, 1):
        ext = max(r.max() - r.min() + 1, c.max() - c.min() + 1)
        if ext >= 25:
            ms[r, c] = True
        elif ext >= 5:
            md[r, c] = True
    masks[solid], masks[dashed] = ms, md
NAMES = ["MTHPA", "NA", "DGEBA-MTHPA", "DGEBA-NA"]
rows, _ = bl.traces(a, cal, frame, [(0, 0, 0), (255, 0, 0), (0, 0, 0), (255, 0, 0)], NAMES, [],
                    min_extent=1, masks=masks)
print({k: v for k, v in cal.items() if k not in ("fx", "fy")})
hdr = [
    "Fig. 4b of Fu et al. 2019, Polymers 11, 975: bond-length distributions of MTHPA and NA (solid) and DGEBA-MTHPA and DGEBA-NA (dashed).",
    "Provenance: tier 3, digitized from the embedded 220 ppi raster image on p. 6 (Origin export); no source data published.",
    "Columns: series = legend entry (MTHPA solid black, NA solid red, DGEBA-MTHPA dashed black, DGEBA-NA dashed red); r_A = bond length in Angstrom;",
    "density_mid = line centre; density_upper / density_lower = ends of the line in that pixel column (half a line width inside the ink); use",
    "density_upper for peak heights. px_x, px_y = pixel in the embedded image. Missing columns: series hidden, or (dashed) in a gap between dashes.",
    "Solid and dashed lines of one colour were separated by connected-component size (see the extract script); dashed values exist only where",
    "a dash is visible and does not touch the solid line. Near 1.09-1.11 A and on the zero baseline some solid pieces may be listed as dashed.",
    "Axis fit on inward major ticks: x 1.1-1.5 (max residual %.4f A), y 5-35 (max residual %.3f); frame x = %.4f..%.4f A, y = %.2f..%.2f." % (
        cal["rx"], cal["ry"], cal["x_left"], cal["x_right"], cal["y_bot"], cal["y_top"]),
    "One row per pixel column: %.5f A. Uncertainty about +-1 px = +-%.2f in density." % (abs(cal["mx"]), abs(cal["my"])),
]
dc.write_csv(str(ROOT / "figures/fig4b.csv"), hdr,
             ["series", "r_A", "density_mid", "density_upper", "density_lower", "px_x", "px_y"], rows,
             fmt=["{}", "{:.5f}", "{:.3f}", "{:.3f}", "{:.3f}", "{}", "{:.1f}"])
img = a.copy()
COLS = {"MTHPA": (0, 200, 0), "NA": (255, 160, 0), "DGEBA-MTHPA": (255, 0, 255), "DGEBA-NA": (0, 200, 255)}
for n, x, y, yu, yl, c, ym in rows:
    img[int(round(ym)), c] = COLS[n]
from PIL import Image  # noqa: E402
(ROOT / "work").mkdir(exist_ok=True)
Image.fromarray(img).save(ROOT / "work/fig4b_overlay.png")
