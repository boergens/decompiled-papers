"""Digitize Figure 2d of Ströh et al. 2022 (PDF p.7): density profiles after 1 hr, 2 hrs and 10 hr (n=13, mean ± s.d.)
and the three dashed model curves.  Source: embedded raster of Figure 2 (~322 ppi).  python3 -I fig2d_extract.py

Mean lines: colour masks of the (semi-transparent) line colours. Model curves: dark grey dashes (darker where they
cross a line), followed from a seed point on each curve, read on the dash runs of one column, by linear
extrapolation across the dash gaps (main_common.track_extrap). The 1 hr and 2 hrs
model curves cross near 1000-1100 μm, where the tracking may swap them.
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
W = (670, 1110, 60, 420)
vc, va, vb = vspine(d, *W)
hr, ha, hb = hspine(d, *W)
xt = ticks_below(d, hr, ha - 5, hb + 5)
assert len(xt) == 3, xt
yt = [681.0, 1038.5]          # tick rows of the labels 186 (top) and 93, found by inspecting the pixels
fy, yres, ys = fit_axis(yt, [186, 93])
fx, xres, xs = fit_axis(xt, [0, 500, 1000])
LINES = {"10hrs": (124, 180, 220), "2hrs": (250, 124, 124), "1hr": (250, 180, 124)}
BANDS = {"10hrs": (226, 234, 242), "2hrs": (250, 232, 232), "1hr": (250, 240, 232)}
P = (672, int(hr) - 2, int(vc) + 3, int(hb))
rows, ov = lineband(a, P, fx, fy, LINES, BANDS, alpha=0.2, band_tol=14, line_tol=40, maxjump=20)
ai = a.astype(int)
model = (ai.sum(2) < 420) & ~d & ((ai.max(2) - ai.min(2)) < 100)   # grey dashes; not black axes, not callouts/labels
model[:, :int(vc) + 3] = False
SEEDS = {"model 10hrs": (290, 788.5), "model 2hrs": (290, 934), "model 1hr": (290, 1038)}   # read on the dash runs at 766 μm
for name, (sc, sr) in SEEDS.items():
    tr = track_extrap(model, sc, sr, int(vc) + 3, int(hb), 672, int(hr) - 2)
    rows += [(name, float(fx(c)), float(fy(m)), "", "") for c, m, t, b in tr if m == m]
    ov.append(((0, 255, 0), [(c, m) for c, m, t, b in tr]))
write_csv(os.path.join(HERE, "fig2d.csv"), [
    "Ströh et al. 2022 eLife, Figure 2d: density profiles (nmol/mm3) of the spatial accumulation of osmium (n=13, mean ±",
    "  s.d.) after 1 hr (orange), 2 hrs (red) and 10 hr (blue) in 2% buffered OsO4, and the diffusion-reaction-advection",
    "  model (dashed). Series names as printed next to the curves; 'model ...' = the dashed curve of that time.",
    "Columns: series; depth_um = Depth (μm); density = Density (nmol/mm3) of the line centre in that pixel column;",
    "  sd_low / sd_high = edges of the shaded s.d. band (very light; mean series only).",
    "Provenance: tier 3, digitized from the embedded ~322 ppi raster (no vector data) by fig2d_extract.py. x fitted on 3",
    f"  ticks (0, 500, 1000), max residual {xres:.2f} μm; y on the 2 labelled ticks (93 at row 1038.5, 186 at row 681),",
    "  linear (the 10 hrs plateau reads 159-160 and the 1 hr peak 129, as in the text).",
    f"Uncertainty: about ±{2 * abs(xs):.0f} μm and ±{2 * abs(ys):.1f} nmol/mm3 (2 px); lines ~8 px wide. The bands are very",
    "  faint and overlap; their edges are less certain (±3 px). Mean lines have gaps where a model dash covers them.",
    "  The 1 hr / 2 hrs model curves cross at the right end; the tracking there may follow the wrong one.",
], ["series", "depth_um", "density", "sd_low", "sd_high"], rows)
save_overlay(a, ov, "fig2d_overlay.png", crop=(670, 1095, 85, 420))
save_crop(a, (670, 1095, 85, 420), os.path.join(HERE, "../work/fig2d_src.png"))
print(len(rows), xres)
