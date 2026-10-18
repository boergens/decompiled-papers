"""Digitize Figure 1b of Nguyen et al. 2016 (Sci Rep 6:23721, PDF p.3): resistance vs Ketjen black concentration.

Source: the embedded JPEG of Figure 1 (917 x 1309 px, about 220 ppi); panel b is in its upper right.
The plot is raster only (vector_dump.py finds no paths in the figure area), so this is tier 3.
    python3 -I fig1b_extract.py   -> fig1b.csv (+ ../work/fig1b_overlay.png for checking)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))   # tools/digitize_common.py
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from digitize_common import (embedded_image, gray, tick_positions, tick_positions_v, fit_axis,  # noqa: E402
                             write_csv, overlay)

PDF = os.path.join(HERE, "../source/srep23721.pdf")
a = embedded_image(PDF, 3)
g = gray(a)
dark = g < 110

YAXIS = (595, 599)     # columns of the left axis line (found as the long dark vertical line)
XAXIS = (215, 219)     # rows of the bottom axis line
# ticks point outward: left of the y axis, below the x axis
yt = tick_positions_v(dark, YAXIS, -1, 5, 25, 225)
xt = tick_positions(dark, XAXIS, 1, 5, YAXIS[1] + 1, 917)
ylab = [1e4, 1e3, 1e2, 1e1, 1e0]          # printed 10^4 ... 10^0, top to bottom
xlab = [5, 10, 15, 20]
assert len(yt) == 5 and len(xt) == 4, (yt, xt)
fy, res_y, _ = fit_axis(yt, ylab, log=True)
fx, res_x, sx = fit_axis(xt, xlab)
px_per_decade = (yt[-1] - yt[0]) / 4

# the four data dots: solid black discs (~13 px across) inside the axes, away from the inset photo
m = (g < 90).astype(np.uint8)
m[:, :YAXIS[1] + 3] = 0
m[XAXIS[0] - 2:, :] = 0
n, lab, st, cen = cv2.connectedComponentsWithStats(m)
dots = []
for i in range(1, n):
    x, y, w, h, area = st[i]
    if 10 <= w <= 16 and 10 <= h <= 16 and area >= 100:      # disc-sized blobs only (not the inset, not text)
        dots.append(cen[i])
dots.sort(key=lambda c: c[0])
assert len(dots) == 4, dots

rows = []
for cx, cy in dots:
    rows.append(("Conductive Plain resin", float(fx(cx)), float(fy(cy)), float(np.log10(fy(cy)))))
overlay(a, [(cx + dx, cy + dy) for cx, cy in dots for dx, dy in ((0, 0), (-2, 0), (2, 0), (0, -2), (0, 2))]
        + [(c, 217) for c in xt] + [(597, r) for r in yt],
        os.path.join(HERE, "../work/fig1b_overlay.png"))

write_csv(os.path.join(HERE, "fig1b.csv"), [
    "Nguyen et al. 2016 Sci Rep 6:23721, Figure 1b: scatter plot of the resistance of the conductive resin block",
    "  versus the filler (Ketjen black) concentration. Axis titles as printed: 'Concentration (wt%)' (x, linear,",
    "  ticks 5-20) and 'Resistance (Ohm/cm)' (y, log10, ticks 10^0-10^4). The main text (p.2) calls the quantity the",
    "  'surface resistance of cured conductive Plain resin'; the series name below is taken from that sentence.",
    "Columns: series; concentration_wt_pct (x as plotted); resistance_ohm_per_cm (y as plotted, unit as printed on the",
    "  axis); log10_resistance.",
    "Provenance: tier 3, digitized from the embedded ~220 ppi JPEG of Figure 1 (no vector data in the PDF) by",
    "  fig1b_extract.py: dot centres = centroids of the four black discs (connected components); x calibrated on the",
    f"  4 labelled x ticks (max residual {res_x:.3f} wt%), y on the 5 labelled log ticks (max residual {res_y:.4f} decades).",
    f"Uncertainty: about +-{abs(sx):.2f} wt% in x and +-{1 / px_per_decade:.3f} decades (+-{(10 ** (1 / px_per_decade) - 1) * 100:.0f} %) in y",
    "  (1 px of the source image; the dots are ~13 px across, so their centroids are good to well below that).",
    "No error bars are drawn; n is not stated.",
], ["series", "concentration_wt_pct", "resistance_ohm_per_cm", "log10_resistance"], rows)
print("wrote fig1b.csv; x ticks", xt, "y ticks", yt, "residuals", res_x, res_y)
for r in rows:
    print(r)
