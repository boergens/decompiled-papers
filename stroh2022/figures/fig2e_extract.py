"""Digitize Figure 2e of Ströh et al. 2022 (PDF p.7): density vs time at depths 200, 600 and 1000 μm (n=13, mean ±
s.d.) and the three dashed model curves.  Source: embedded raster of Figure 2 (~322 ppi).  python3 -I fig2e_extract.py

Mean lines: colour masks of the (semi-transparent) line colours. Model curves: dark grey dashes (darker where they
cross a line), followed from a seed point on each curve, read on the dash runs of one column, by linear
extrapolation across the dash gaps (main_common.track_extrap). The 600 μm and
1000 μm model curves come close at the right end, where the tracking may swap them. The callout lines and labels
(200μm, 600μm, 1000μm) inside the plot have other colours and are not traced.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import fig_image, dark_mask, vspine, hspine, ticks_below, fit_axis, write_csv, save_overlay, \
    save_crop, lineband, track_extrap  # noqa: E402

a = fig_image(2)
d = dark_mask(a)
W = (670, 1110, 720, 1080)
vc, va, vb = vspine(d, *W)
hr, ha, hb = hspine(d, *W)
xt = ticks_below(d, hr, ha - 5, hb + 5)
xt = [vc] + xt               # the 0 tick coincides with the y axis line
assert len(xt) == 3, xt
yt = [681.0, 1038.5]          # tick rows of the labels 186 (top) and 93, found by inspecting the pixels (as in d)
fy, yres, ys = fit_axis(yt, [186, 93])
fx, xres, xs = fit_axis(xt, [0, 500, 1000])
LINES = {"200μm": (124, 180, 220), "600μm": (250, 124, 124), "1000μm": (250, 180, 124)}
BANDS = {"200μm": (226, 234, 242), "600μm": (250, 232, 232), "1000μm": (250, 240, 232)}
P = (672, int(hr) - 2, int(vc) + 3, int(hb))
rows, ov = lineband(a, P, fx, fy, LINES, BANDS, alpha=0.2, band_tol=14, line_tol=40, maxjump=20)
ai = a.astype(int)
model = (ai.sum(2) < 420) & ~d & ((ai.max(2) - ai.min(2)) < 100)   # grey dashes; not black axes, not callouts/labels
model[:, :int(vc) + 3] = False
# The dashed model curves cross each other (200/600 μm near 250 min) and the 600/1000 μm curves nearly coincide at the
# right, so each curve is followed from two seeds, each within its own column range (seed rows read on the dash runs)
SEEDS = {"model 200μm": [(805, 866, 757, 850), (1030, 801.5, 900, 1060)],
         "model 600μm": [(805, 853, 757, 900), (950, 775, 900, 1060)],
         "model 1000μm": [(805, 958, 757, 900), (950, 784, 900, 1060)]}
for name, seeds in SEEDS.items():
    for sc, sr, ca, cb in seeds:
        tr = track_extrap(model, sc, sr, max(ca, int(vc) + 3), min(cb, int(hb)), 672, int(hr) - 2)
        rows += [(name, float(fx(c)), float(fy(m)), "", "") for c, m, t, b in tr if m == m]
        ov.append(((0, 255, 0) if "200" in name else (0, 200, 255) if "600" in name else (255, 255, 0), [(c, m) for c, m, t, b in tr]))
write_csv(os.path.join(HERE, "fig2e.csv"), [
    "Ströh et al. 2022 eLife, Figure 2d: density profiles (nmol/mm3) of the spatial accumulation of osmium (n=13, mean ±",
    "  s.d.) after 1 hr (orange), 2 hrs (red) and 10 hr (blue) in 2% buffered OsO4, and the diffusion-reaction-advection",
    "  model (dashed). Series names as printed next to the curves; 'model ...' = the dashed curve of that time.",
    "Columns: series; depth_um = Depth (μm); density = Density (nmol/mm3) of the line centre in that pixel column;",
    "  sd_low / sd_high = edges of the shaded s.d. band (very light; mean series only).",
    "Provenance: tier 3, digitized from the embedded ~322 ppi raster (no vector data) by fig2e_extract.py. x fitted on 3",
    f"  ticks (0 = y-axis line, 500, 1000), max residual {xres:.2f} min; y on the 2 labelled ticks (93 at row 1038.5, 186 at row 681),",
    "  linear (as in d).",
    f"Uncertainty: about ±{2 * abs(xs):.0f} min and ±{2 * abs(ys):.1f} nmol/mm3 (2 px); lines ~8 px wide. The bands are very",
    "  faint and overlap; their edges are less certain (±3 px). Mean lines have gaps where a model dash covers them.",
    "  Model curves: each followed in two column ranges from its own seeds (no values in between, e.g. 200 μm model",
    "  at about 370-570 min); the 600 μm / 1000 μm model curves nearly coincide at the right end. The steep early part",
    "  of the 1000 μm model (before about 250 min, lower right of the 600 μm data) is NOT followed correctly: values",
    "  of 'model 1000μm' below 250 min are unreliable (the tracker stays on neighbouring dashes).",
], ["series", "time_min", "density", "sd_low", "sd_high"], rows)
save_overlay(a, ov, "fig2e_overlay.png", crop=(670, 1095, 745, 1080))
save_crop(a, (670, 1095, 745, 1080), os.path.join(HERE, "../work/fig2e_src.png"))
print(len(rows), xres)
