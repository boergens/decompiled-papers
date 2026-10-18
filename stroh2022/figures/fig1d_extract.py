"""Digitize Figure 1d of Ströh et al. 2022 (PDF p.3): staining-front depth vs time, mean (blue) ± s.d. band and the
dashed black sqrt(t) model.  Source: embedded raster of Figure 1 (~348 ppi).  python3 -I fig1d_extract.py -> fig1d.csv"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import fig_image, dark_mask, vspine, hspine, ticks_left, ticks_below, fit_axis, write_csv, \
    save_overlay, save_crop, lineband  # noqa: E402

a = fig_image(1)
d = dark_mask(a)
W = (1400, 1900, 600, 1000)
vc, va, vb = vspine(d, *W)
hr, ha, hb = hspine(d, *W)
yt = ticks_left(d, vc, va - 5, vb + 5)
xt = ticks_below(d, hr, ha - 5, hb + 5)
assert len(yt) == 3 and len(xt) == 3, (yt, xt)
fy, yres, ys = fit_axis(sorted(yt, reverse=True), [0, 500, 1000])   # labels read by eye
fx, xres, xs = fit_axis(xt, [0, 200, 400])
b = a.copy()
b[1725:1830, 705:985] = 255            # legend box (blue patch + "OsO4", dashed line + "√t ∝ x")
P = (1420, int(hr) - 3, int(vc) + 3, 985)
rows, ov = lineband(b, P, fx, fy, {"OsO4 mean": (0, 110, 188)}, {"OsO4 mean": (152, 170, 204)}, black="model sqrt(t)")
write_csv(os.path.join(HERE, "fig1d.csv"), [
    "Ströh et al. 2022 eLife, Figure 1d: propagation of the staining front in 4 mm brain punches in 2% buffered OsO4",
    "  (n=13, mean ± s.d.) and the quadratic model (dashed black line, 'sqrt(t) ∝ x' in the legend).",
    "Columns: series; time_min = Time t (min); depth_um = Depth x (μm) of the line centre in that pixel column;",
    "  sd_low_um / sd_high_um = lower / upper edge of the shaded s.d. band in that column (mean series only).",
    "Provenance: tier 3, digitized from the embedded ~348 ppi raster (no vector data) by fig1d_extract.py; colour masks",
    f"  per pixel column. x fitted on 3 ticks (0, 200, 400), max residual {xres:.2f} min; y on 3 ticks (0, 500, 1000),",
    f"  max residual {yres:.2f} μm. The legend area (lower right) was blanked before tracing.",
    f"Uncertainty: about ±{2 * abs(xs):.1f} min and ±{2 * abs(ys):.1f} μm (2 px); the lines are ~8 px wide. Where the dashed",
    "  model covers the blue line, the blue line has no row; the dashed line has gaps between dashes.",
], ["series", "time_min", "depth_um", "sd_low_um", "sd_high_um"], rows)
save_overlay(b, ov, "fig1d_overlay.png", crop=(1420, 1850, 630, 990))
save_crop(a, (1420, 1850, 630, 990), os.path.join(HERE, "../work/fig1d_src.png"))
print(len(rows), "rows", xres, yres)
