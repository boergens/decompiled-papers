"""Digitize Figure 1f of Ströh et al. 2022 (PDF p.3): change in sample height vs time, four solutions, mean ± s.d.,
and the dashed black monomolecular growth model ("Model").
Source: embedded raster of Figure 1 (~348 ppi).  python3 -I fig1e_extract.py -> fig1e.csv

"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import fig_image, dark_mask, vspine, hspine, ticks_left, ticks_below, fit_axis, write_csv, \
    save_overlay, save_crop, lineband  # noqa: E402

a = fig_image(1)
d = dark_mask(a)
W = (1440, 1900, 1600, 2079)
vc, va, vb = vspine(d, *W)
hr, ha, hb = hspine(d, *W)
yt = ticks_left(d, vc, va - 5, vb + 5)
xt = ticks_below(d, hr, ha - 5, hb + 5)
assert len(yt) == 3 and len(xt) == 3, (yt, xt)
yt = sorted(yt) + [hr]                      # ticks 20, 10, 0 and the x-axis line at -10 (label -10 at the axis)
fy, yres, ys = fit_axis(yt, [20, 10, 0, -10])    # labels read by eye
fx, xres, xs = fit_axis(xt, [0, 500, 1000])
LINES = {"OsO4": (0, 110, 188), "Ferro-redOs": (0, 125, 98), "Ferro-redOs + 5.56% formamide": (250, 100, 0),
         "Ferro-redOs + 11.25% formamide": (250, 0, 0)}
BANDS = {"OsO4": (152, 170, 204), "Ferro-redOs": (168, 210, 202), "Ferro-redOs + 5.56% formamide": (250, 202, 168),
         "Ferro-redOs + 11.25% formamide": (250, 168, 168)}
b = a.copy()
b[1792:1840, 1745:1965] = 255                 # legend "Model" (dashed line + text)
ref = b[1714:1722, int(vc) + 2:2079]
thin = (ref.astype(int).mean(2) < 90)
ref[thin] = 255                               # thin black reference line at 0 % (would be taken for the dashed model)
P = (1440, int(hr) - 2, int(vc) + 2, 2079)
rows, ov = lineband(b, P, fx, fy, LINES, BANDS, black="Model", maxjump=30)
write_csv(os.path.join(HERE, "fig1f.csv"), [
    "Ströh et al. 2022 eLife, Figure 1f: tissue expansion as change in sample height of aldehyde-fixed brain punches in",
    "  OsO4 (blue, n=13), Ferro-redOs (green, n=6), Ferro-redOs with 5.56% (orange, n=4) and 11.25% formamide (red, n=4)",
    "  (mean ± s.d.), and the monomolecular growth model fitted to the OsO4 mean (black dashed, 'Model').",
    "  Series names for the coloured lines are from the caption (the shared legend of e/f names them as in fig1e.csv).",
    "Columns: series; time_min = Time (min); height_change_percent = Change in sample height (%) of the line centre in",
    "  that pixel column; sd_low / sd_high = lower / upper edge of that series' s.d. band in that column.",
    "Provenance: tier 3, digitized from the embedded ~348 ppi raster (no vector data) by fig1f_extract.py. x fitted on 3",
    f"  ticks (0, 500, 1000), max residual {xres:.2f} min; y on ticks 20, 10, 0 and the x-axis line (-10), max residual",
    f"  {yres:.3f} %. The legend and the thin reference line at 0 % were blanked before tracing.",
    f"Uncertainty: about ±{2 * abs(xs):.0f} min and ±{2 * abs(ys):.2f} % (2 px); lines ~8 px wide; band edges ±3 px where",
    "  bands overlap. The dashed model covers the blue line for most of its length (blue has gaps there).",
], ["series", "time_min", "height_change_percent", "sd_low", "sd_high"], rows)
save_overlay(b, ov, "fig1f_overlay.png", crop=(1430, 1850, 1700, 2079))
save_crop(a, (1430, 1850, 1700, 2079), os.path.join(HERE, "../work/fig1f_src.png"))
print(len(rows), "rows", xres, yres)
