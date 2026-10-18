"""Digitize Figure 4 of Gabričević, Lente & Fábián 2020 (poc.4045.pdf p. 4): k_obs of the fast step vs [Substrate].

Source: the embedded raster image of Figure 4 (1003 x 724 px). Scatter plot, three marker series.
    python3 -I fig4_extract.py   -> fig4.csv (+ ../work/fig4_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from gab_common import load, gray, tick_positions, tick_positions_v, fit_axis, scatter, write_csv, cross_overlay, WORK  # noqa: E402

a = load("fig4")
dark = gray(a) < 120
BOT, LEFT = (603, 603), (150, 152)            # frame lines found with frame_lines()
xt = tick_positions(dark, BOT, 1, 10, 153, 995)          # outward ticks below the x axis
yt = tick_positions_v(dark, LEFT, -1, 10, 8, 600)        # major ticks left of the y axis
assert len(xt) == 4 and len(yt) == 3, (xt, yt)
fx, rx, sx = fit_axis([151.0] + xt, [0.0, 0.005, 0.010, 0.015, 0.020])   # left frame = 0.000 (labelled)
fy, ry, sy = fit_axis(yt + [603.0], [0.6, 0.4, 0.2, 0.0])                # bottom frame = 0.0 (labelled)

LEGEND = (270, 410, 540, 545)   # x0, y0, x1, y1 of the legend (excluded)
series = [("TCE", (0, 128, 0)), ("trans-DCE", (255, 0, 0)), ("cis-DCE", (0, 0, 255))]
found = scatter(a, series, (156, 7, 995, 600), exclude=[LEGEND])
rows = [(n, float(fx(x)), float(fy(y)), w, h, f) for n, x, y, w, h, f in found]
pts = [(x, y) for n, x, y, w, h, f in found]
rows.sort(key=lambda r: (r[0], r[1]))
cross_overlay(a, pts, os.path.join(WORK, "fig4_overlay.png"))
write_csv(os.path.join(HERE, "fig4.csv"), [
    "Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 4: dependence of k_obs on the chloroethylene",
    "  concentration in the fast step of the reaction with osmium(VIII). Scatter plot, no error bars, no fit line.",
    "Columns: series (paper's legend names); substrate_mol_dm3 = [Substrate] (mol/dm3); kobs_s-1 = k_obs (s-1);",
    "  marker_w_px, marker_h_px = size of the marker blob in the source image; note.",
    "Provenance: tier 3, digitized from the embedded raster image (1003 x 724 px; the PDF has no vector data for the",
    f"  plot) by fig4_extract.py. x calibrated on the left frame (0.000) and 4 labelled ticks, max residual {rx:.2g};",
    f"  y on the bottom frame (0.0) and 3 labelled ticks (0.2-0.6), max residual {ry:.2g}. Marker centre = centre of",
    "  the bounding box of the colour-masked marker.",
    f"Uncertainty: about +-{2 * abs(sx):.5f} mol/dm3 in x and +-{2 * abs(sy):.4f} s-1 in y (2 px); more for markers",
    "  partly hidden by another marker (flagged), whose centre comes from the visible part only.",
], ["series", "substrate_mol_dm3", "kobs_s-1", "marker_w_px", "marker_h_px", "note"], rows)
print("fig4:", len(rows), "points; residuals", rx, ry)
for r in rows:
    print(r)
