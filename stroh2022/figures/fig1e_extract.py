"""Digitize Figure 1e of Ströh et al. 2022 (PDF p.3): intensity profiles after t=20 hr, four solutions, mean ± s.d.
Source: embedded raster of Figure 1 (~348 ppi).  python3 -I fig1e_extract.py -> fig1e.csv

The y axis has only two labels (0.4, 1). It is linear: the blue (OsO4) and green (Ferro-redOs) means read on a linear
axis agree within 0.005 with the means of the per-sample t=1200 min profiles in the source data (see README)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import fig_image, dark_mask, vspine, hspine, ticks_left, ticks_below, fit_axis, write_csv, \
    save_overlay, save_crop, lineband  # noqa: E402

a = fig_image(1)
d = dark_mask(a)
W = (1440, 1900, 1100, 1560)
vc, va, vb = vspine(d, *W)
hr, ha, hb = hspine(d, *W)
yt = ticks_left(d, vc, va - 5, vb + 5)
xt = ticks_below(d, hr, ha - 5, hb + 5)
assert len(yt) == 2 and len(xt) == 3, (yt, xt)
fy, yres, ys = fit_axis(sorted(yt, reverse=True), [0.4, 1])       # labels read by eye; linear (see docstring)
fx, xres, xs = fit_axis(xt, [0, 500, 1000])
LINES = {"OsO4": (0, 110, 188), "Ferro-redOs": (0, 125, 98), "5.56% CH3NO + Ferro-redOs": (250, 100, 0),
         "11.25% CH3NO + Ferro-redOs": (250, 0, 0)}
BANDS = {"OsO4": (152, 170, 204), "Ferro-redOs": (168, 210, 202), "5.56% CH3NO + Ferro-redOs": (250, 202, 168),
         "11.25% CH3NO + Ferro-redOs": (250, 168, 168)}
P = (1430, int(hr) - 2, int(vc) + 2, 1515)
rows, ov = lineband(a, P, fx, fy, LINES, BANDS, maxjump=30)
top = float(fy(1440.5))   # first row with green-band pixels (flat top = clipping)
write_csv(os.path.join(HERE, "fig1e.csv"), [
    "Ströh et al. 2022 eLife, Figure 1e: intensity profiles of the spatial heavy metal accumulation after t=20 hr in",
    "  2% buffered OsO4 (blue, n=13), Ferro-redOs (green, n=6), Ferro-redOs with 5.56% (orange, n=4) and 11.25% formamide",
    "  (red, n=4) (mean ± s.d.); series names as in the legend (CH3NO = formamide).",
    "Columns: series; depth_um = Depth (μm); intensity_au = Intensity (a.u.) of the mean line centre in that pixel column;",
    "  sd_low / sd_high = lower / upper edge of that series' shaded s.d. band in that column.",
    "Provenance: tier 3, digitized from the embedded ~348 ppi raster (no vector data) by fig1e_extract.py. x fitted on 3",
    f"  ticks (0, 500, 1000), max residual {xres:.2f} μm; y on the 2 labelled ticks (0.4, 1), linear (checked against the",
    "  source data). Overlapping translucent bands are separated by a compositing model (main_common.band_masks).",
    f"Uncertainty: about ±{2 * abs(xs):.0f} μm and ±{2 * abs(ys):.3f} a.u. (2 px); lines ~8 px wide; band edges ±3 px where",
    "  bands overlap. The green band has a flat top (clipped) at about 300-750 μm, above the end of the y axis: sd_high there is the",
    f"  clip value ({top:.3f}), not the band edge. Where a line is hidden under another, it has no value in that column.",
], ["series", "depth_um", "intensity_au", "sd_low", "sd_high"], rows)
save_overlay(a, ov, "fig1e_overlay.png", crop=(1430, 1850, 1150, 1520))
save_crop(a, (1430, 1850, 1150, 1520), os.path.join(HERE, "../work/fig1e_src.png"))
print(len(rows), "rows", xres, "top clip", top)
