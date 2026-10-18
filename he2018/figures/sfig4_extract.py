"""Digitize Supplementary Figure 4 of He et al. 2018 (Sci Rep 8:12985), SI PDF p.6: EDS spectrum + 4 standards.

Source: the embedded raster image (549 x 344 px, placed at 468 x 293 pt, i.e. ~84 ppi: low resolution).
    python3 -I sfig4_extract.py   -> sfig4.csv (+ ../work/sfig4_overlay.png for checking)
"""
import colorsys
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/admin/ephemeral/oct_17_papers/he2018/tools")
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, trace_envelope, write_csv, overlay  # noqa: E402

PDF = os.path.join(HERE, "../source/41598_2018_31231_MOESM1_ESM.pdf")
a = embedded_image(PDF, 6, bbox_near=(72, 72, 540, 365))
assert a.shape == (344, 549, 3), a.shape
ai = a.astype(int)
g = ai.mean(2)
sat = np.ptp(ai, axis=2)

# Axes: frame columns 73 (8 keV) and 523 (20 keV); x tick marks below the frame at columns 73, 148, 222.5,
# 298, 373, 448, 523 (8..20 keV in steps of 2). y tick marks left of the frame at rows 58, 133, 208, 283
# (600, 400, 200, 0 counts). All found by scanning for dark pixels next to the frame.
fx, rx, sx = fit_axis([73, 148, 222.5, 298, 373, 448, 523], [8, 10, 12, 14, 16, 18, 20])
fy, ry, sy = fit_axis([58, 133, 208, 283], [600, 400, 200, 0])

# colour classes by hue (saturated pixels) and the black sample spectrum (dark grey, unsaturated)
hsv = np.array([colorsys.rgb_to_hsv(*(p / 255)) for p in ai.reshape(-1, 3)]).reshape(a.shape)
H, S, V = hsv[:, :, 0] * 360, hsv[:, :, 1], hsv[:, :, 2]
colourful = (S > 0.35) & (V > 0.3)
masks = {
    "Sectioned biological sample block": (g < 110) & (sat < 45),
    "Copper standard": colourful & (H > 195) & (H < 225),
    "Lead standard": colourful & (H > 245) & (H < 290),
    "Osmium standard": colourful & (H > 80) & (H < 160),
    "Uranium standard": colourful & ((H < 15) | (H > 340)),
}
# blank the legend box and the peak labels (text, not data); boxes in source pixels (x0, y0, x1, y1)
TEXT = [(285, 22, 524, 103),     # legend
        (93, 25, 152, 56),       # Cu K-M2 / Os L3-M4
        (115, 183, 175, 199),    # Os L2-M4
        (198, 160, 258, 194),    # Os L1-M3 / Pb L3-M5
        (210, 220, 270, 236),    # Pb L2-M4
        (263, 240, 317, 256)]    # U L3-M5
for m in masks.values():
    for x0, y0, x1, y1 in TEXT:
        m[y0:y1, x0:x1] = False

X0, X1, Y0, Y1 = 75, 522, 22, 283     # inside the frame; row 283 is the 0-count line, which the frame hides partly
rows, pts = [], []
ov = a.copy()
COLS = {"Sectioned biological sample block": (255, 0, 255), "Copper standard": (255, 140, 0),
        "Lead standard": (0, 255, 255), "Osmium standard": (255, 255, 0), "Uranium standard": (0, 0, 255)}
for name, m in masks.items():
    env = trace_envelope(m, X0, X1, Y0, Y1, half_width=0.5, min_px=1)
    for c, ym, yu, yl in env:
        if ym != ym:
            continue
        clipped = "clipped" if yu <= Y0 + 1 else ""
        rows.append((name, float(fx(c)), float(fy(ym)), float(fy(yl)), float(fy(yu)), clipped))
        for y in (yu, yl):
            ov[int(round(y)), int(c)] = COLS[name]
overlay(ov, [], os.path.join(HERE, "../work/sfig4_overlay.png"))

write_csv(os.path.join(HERE, "sfig4.csv"), [
    "He et al. 2018 Sci Rep 8:12985, Supplementary Figure 4: energy-dispersive x-ray spectrum from a thin section of the",
    "  tissue block (black, 'Sectioned biological sample block') and the DTSA-II reference spectra 'Copper standard' (blue),",
    "  'Lead standard' (purple), 'Osmium standard' (green), 'Uranium standard' (red); series names from the legend.",
    "Columns: series; energy_keV = X-ray Energy (keV); counts_mid = Counts, middle of the drawn line in this pixel column;",
    "  counts_low / counts_high = bottom and top of the line in the column (they differ on steep peak flanks);",
    "  flag 'clipped' where the curve leaves the top of the frame (the Copper standard rises above 700 counts below ~8.3 keV).",
    "Provenance: tier 3, digitized from the embedded raster image (549 x 344 px, ~84 ppi; no vector data in the PDF) by",
    f"  sfig4_extract.py. x calibrated on the 7 x tick marks (8-20 keV), max residual {rx:.4f} keV; y on the 4 y tick marks",
    f"  (0-600), max residual {ry:.3f} counts.",
    f"Uncertainty: low-resolution source. About +-{2 * abs(sx):.3f} keV in x and +-{2 * abs(sy):.0f} counts in y (2 px), more where",
    "  lines overlap. Near the baseline (0-20 counts) the five lines lie on top of each other; there each colour is",
    "  only where it is visible, so the coloured standards have gaps and the low-count values are uncertain.",
    "  The peak labels and the legend were blanked before tracing; the two annotation arrows end on the curves near",
    "  10.3-10.6 keV and may add a few pixels there.",
    "One row per pixel column of the source image per series.",
], ["series", "energy_keV", "counts_mid", "counts_low", "counts_high", "flag"], rows)
print("wrote sfig4.csv", len(rows), "rows; residuals", rx, ry)
for name in masks:
    print(name, sum(1 for r in rows if r[0] == name))
