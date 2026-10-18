"""Classify the von Mises contour maps of Figures 10 and 11 of Fu et al. 2025 (Polymers 17, 2441), p. 14, into the
bands of their colour keys -> fig10left.csv, fig10right.csv, fig11a.csv ... fig11f.csv (grid CSVs, one row per pixel
row) and work/<panel>_classified.png (source | classified map) for checking.

Sources: the embedded images on PDF p. 14: Fig. 10 = 1479 x 524 px lossless (Flate) image, Fig. 11 = 1579 x 1307 px
JPEG, both 300 ppi. Method: tools/fe_mises.py.
    python3 -I fig11_extract.py
"""
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from digitize_common import embedded_image  # noqa: E402
from fe_mises import classify, render, write_grid, band_text  # noqa: E402

PDF = HERE.parent / "source" / "fu2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)

K10 = ["+3.485×10^4", "+3.195×10^4", "+2.906×10^4", "+2.616×10^4", "+2.327×10^4", "+2.038×10^4", "+1.748×10^4",
       "+1.459×10^4", "+1.169×10^4", "+8.799×10^3", "+5.904×10^3", "+3.010×10^3", "+1.158×10^2"]


def k(s):
    return s.split()


FIGS = {
    10: dict(bbox=(168.1, 75.8, 523.0, 201.5), jpeg=False, cap="stress distribution of plain PMMA and PMMA/1.0 wt% "
             "CNTs at 100 nm cutting thickness (caption)", panels=[
        ("left", "Plain PMMA (title box above the panel)", (262, 0, 860, 524), [(262, 0, 860, 92)], K10,
         "the key at the left of the figure, shared by both panels"),
        ("right", "PMMA/ 1.0 wt% CNT (title box above the panel)", (860, 0, 1479, 524), [(860, 0, 1479, 92)], K10,
         "the key at the left of the figure, shared by both panels"),
    ]),
    11: dict(bbox=(170.1, 233.3, 549.1, 547.2), jpeg=True, cap="stress distribution (S, Mises) at 60 nm cutting "
             "thickness (caption)", panels=[
        ("a", "plain PMMA, shear-zone propagation", (135, 0, 860, 415), [(668, 22, 852, 308), (600, 18, 662, 68)],
         k("+3.499e+04 +3.208e+04 +2.917e+04 +2.626e+04 +2.335e+04 +2.045e+04 +1.754e+04 +1.463e+04 +1.172e+04 "
           "+8.810e+03 +5.901e+03 +2.992e+03 +8.297e+01"), "the key printed beside the panel"),
        ("b", "plain PMMA, edge stress localization", (860, 0, 1579, 415), [(1390, 20, 1572, 305), (1308, 18, 1376, 68)],
         k("+3.495e+04 +3.204e+04 +2.913e+04 +2.622e+04 +2.331e+04 +2.040e+04 +1.749e+04 +1.459e+04 +1.168e+04 "
           "+8.766e+03 +5.857e+03 +2.948e+03 +3.832e+01"), "the key printed beside the panel"),
        ("c", "PMMA/0.5 wt% CNTs, primary shear band growth", (135, 420, 860, 860),
         [(668, 472, 852, 762), (600, 448, 664, 498)],
         k("+3.444e+04 +3.157e+04 +2.870e+04 +2.583e+04 +2.296e+04 +2.009e+04 +1.722e+04 +1.435e+04 +1.148e+04 "
           "+8.611e+03 +5.741e+03 +2.870e+03 +0.000e+00"), "the key printed beside the panel"),
        ("d", "PMMA/0.5 wt% CNTs, CNT protrusion at the interface", (845, 420, 1579, 860),
         [(1383, 472, 1567, 762), (1308, 452, 1376, 502)],
         k("+3.480e+04 +3.190e+04 +2.900e+04 +2.610e+04 +2.320e+04 +2.030e+04 +1.740e+04 +1.450e+04 +1.160e+04 "
           "+8.700e+03 +5.800e+03 +2.900e+03 +0.000e+00"), "the key printed beside the panel"),
        ("e", "PMMA/1.0 wt% CNTs, inhibited stress propagation", (135, 860, 860, 1307),
         [(676, 922, 857, 1203), (603, 898, 662, 948)],
         k("+3.448e+04 +3.161e+04 +2.874e+04 +2.586e+04 +2.299e+04 +2.012e+04 +1.724e+04 +1.437e+04 +1.149e+04 "
           "+8.621e+03 +5.747e+03 +2.874e+03 +0.000e+00"), "the key printed beside the panel"),
        ("f", "PMMA/1.0 wt% CNTs, stress redistribution during chip flow", (860, 860, 1579, 1307),
         [(1386, 922, 1567, 1203), (1308, 898, 1376, 948)],
         k("+3.488e+04 +3.197e+04 +2.906e+04 +2.616e+04 +2.325e+04 +2.034e+04 +1.744e+04 +1.453e+04 +1.163e+04 "
           "+8.719e+03 +5.813e+03 +2.906e+03 +0.000e+00"), "the key printed beside the panel"),
    ]),
}

for fig, F in FIGS.items():
    a = embedded_image(str(PDF), 14, bbox_near=F["bbox"])
    for panel, what, (c0, r0, c1, r1), boxes, key, keynote in F["panels"]:
        sub = a[r0:r1, c0:c1]
        local = [(x0 - c0, y0 - r0, x1 - c0, y1 - r0) for (x0, y0, x1, y1) in boxes]
        codes = classify(sub, local, max_dist=45)
        cnt = sorted(Counter(codes.ravel().tolist()).items())
        hdr = [
            f"Fu et al. 2025, Polymers 17, 2441, Figure {fig} ({panel}): {F['cap']}; this panel: {what}.",
            "  Quantity: S, Mises (Abaqus von Mises stress, 'Avg: 75%' averaging) as a discrete 12-band contour plot;",
            "  the figure gives no unit.",
            "Format: one CSV row per pixel row of the panel (row 0 = top), column 'codes' = one character per pixel",
            "  column (column 0 = left). Codes: '0'..'9','a','b' = band of the colour key, low to high (below);",
            "  '.' = white (background, knife interior); 'X' = annotation area (colour key, panel label, title box;",
            "  not data); '#' = not classified (black outlines and knife lines, black annotation text, arrows and",
            "  dashed circles, anti-aliased or JPEG-blurred pixels on band boundaries).",
            f"Bands (code: colour, range in the key's units), from {keynote}: " + band_text(key) + ".",
            "  Key values printed (top to bottom): " + ", ".join(key) + ".",
            f"Geometry: no scale bar or axes; positions are image pixels only. Source: embedded {'JPEG' if F['jpeg'] else 'lossless'}",
            f"  image of Fig. {fig} on PDF p. 14 (300 ppi, 1 px = 0.24 pt); this panel = columns {c0}-{c1 - 1}, rows {r0}-{r1 - 1}.",
            "Provenance: tier 3, digitized: each pixel assigned to the nearest band colour, the model colours being",
            "  the key colours times 216/255 (Abaqus shading), within an RGB distance of "
            "45 (about half the distance between neighbouring band colours); see tools/fe_mises.py.",
            "  Exact for flat band interiors; band boundaries are blurred in the source (" +
            ("JPEG" if F["jpeg"] else "the image was resampled before embedding") + "), uncertain by 1-2 px.",
            "Pixel counts: " + ", ".join(f"{c}={v}" for c, v in cnt),
        ]
        name = f"fig{fig}{panel}"
        write_grid(HERE / f"{name}.csv", hdr, codes)
        from PIL import Image
        Image.fromarray(np.concatenate([sub, np.full((sub.shape[0], 10, 3), 255, np.uint8), render(codes)], 1)).save(
            WORK / f"{name}_classified.png")
        print(name, cnt)
