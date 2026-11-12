"""Digitize Fig. 8 (p. 6 of the PDF, journal p. 031104-5): extinction ratio (TM/TE) vs wavelength of the etched
WGPs made with the two imprint templates, panels (a) and (b). Tier 3: one embedded Flate image (1763 x 671 px,
300 ppi); no vector paths on the page.

Calibration: x from the tick marks under each x axis ((a) 400 ... 800 nm, (b) 400 ... 700 nm), y from the grey
gridlines with their tick marks ((a) 0 ... 6000, (b) 0 ... 50000), darkness centroids. The image is not uniformly
scaled (tick spacing varies by 1-3 px), so the pixel -> value maps are piecewise linear through the ticks
(exact at every tick); the residual of a straight-line fit is reported for comparison.
Series: the single thick blue line of each panel (colour mask), per pixel column its centre and the lowest and
highest value its ink reaches (the line is noisy and about 8 px thick).
Writes figures/fig8a.csv, figures/fig8b.csv and work/fig8_overlay.png.

    python3 -I -B figures/fig8_extract.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "work"))
import digi  # noqa: E402

a = digi.image(6, (102.3, 59.8, 525.4, 220.8))
g = digi.gray(a)
hsv = digi.hsv(a)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
blue = (H >= 98) & (H <= 116) & (S > 80) & (V < 240)

PANELS = {
    "a": dict(xt=((503, 512), 150, 880), xv=[400, 500, 600, 700, 800], yt=((150, 157), 0, 505),
              yv=list(range(6000, -1, -1000)), cols=(160, 830), rows=(10, 500), plot_right="800 nm"),
    "b": dict(xt=((508, 516), 1060, 1763), xv=[400, 500, 600, 700], yt=((1064, 1071), 0, 510),
              yv=list(range(50000, -1, -5000)), cols=(1075, 1763), rows=(10, 505), plot_right="the image edge"),
}
pts = []
for key, P in PANELS.items():
    xt = digi.ticks_x(g, *P["xt"], thr=15)
    yt = digi.ticks_y(g, *P["yt"], thr=10)
    assert len(xt) == len(P["xv"]) and len(yt) == len(P["yv"]), (key, xt, yt)
    fx = digi.piecewise(xt, P["xv"])
    fy = digi.piecewise(yt, P["yv"])
    rx = digi.fit(xt, P["xv"])[2]
    ry = digi.fit(yt, P["yv"])[2]
    print(key, "linear-fit residuals: x %.2f nm, y %.0f" % (rx, ry))
    c0, c1 = P["cols"]
    r0, r1 = P["rows"]
    tr = digi.trace_line(blue, c0, c1, r0, r1, start_hint=None, max_jump=10)
    rows = []
    for c, mid, top, bot in tr:
        if mid != mid:
            continue
        rows.append([float(fx(c)), float(fy(mid)), float(fy(bot)), float(fy(top))])
        pts += [(c, top), (c, bot)]
    dx = (P["xv"][-1] - P["xv"][0]) / (xt[-1] - xt[0])
    dy = (P["yv"][0] - P["yv"][-1]) / (yt[-1] - yt[0])
    hdr = [
        "Fig. 8(%s) (ahn2013, PDF p. 6): extinction ratio (TM/TE) vs wavelength, etched WGP; (a) and (b) are the" % key,
        "polarizers patterned with the two imprint templates (caption; the text, p. 5-6, compares an older template",
        "with 50 nm half pitch and a newer one with 65 nm half pitch, Fig. 8(a) and 8(b)).",
        "Columns: wavelength_nm, extinction_ratio (centre of the blue line in that pixel column), er_min / er_max",
        "(lowest / highest value the line's ink reaches in that column; the line is about 8 px thick and noisy).",
        "Provenance: tier 3, digitized from the embedded Flate image (1763 x 671 px) with figures/fig8_extract.py;",
        "colour mask; one row per source pixel column (%.2f nm). Axes: piecewise linear through %d x ticks and %d y" %
        (dx, len(xt), len(yt)),
        "ticks / gridlines (straight-line fit residuals for comparison: %.2f nm, %.0f)." % (rx, ry),
        "Uncertainty: about 1 px: +-%.1f nm in x, +-%.0f in y, plus the line's own thickness (see er_min / er_max)." % (dx, dy),
    ]
    if key == "b":
        hdr.append("The panel is cut off at the right edge of the embedded image, at about %.0f nm: the x axis has" % fx(1762))
        hdr.append("labels 400 ... 700 only and the line runs to the image edge.")
    digi.write_csv(os.path.join(HERE, "fig8%s.csv" % key), hdr,
                   ["wavelength_nm", "extinction_ratio", "er_min", "er_max"], rows,
                   ["{:.1f}", "{:.0f}", "{:.0f}", "{:.0f}"])
    print(key, "rows", len(rows), "x range %.1f-%.1f" % (rows[0][0], rows[-1][0]))
digi.overlay(a, [((255, 0, 255), pts)], os.path.join(ROOT, "work", "fig8_overlay.png"))
