"""Digitize Figure 1—figure supplement 3 of Ströh et al. 2022 (eLife JPEG fig1-figsupp3.jpg, 1050 x 2109 px), panels a-f.

a, c, e: Intensity (a.u.) vs Depth (μm), mean lines with s.d. bands (y labels 0.4 and 1, linear as in Figure 1e).
b, d, f: Change in sample height (%) vs Time (min), mean lines with s.d. bands (y labels -10, 0, 10, 20).
Spines and tick marks are found in the image; tick labels were read by eye. Overlapping translucent bands are
separated with the compositing model of main_common.band_masks.
    python3 -I sfig1s3_extract.py -> sfig1s3a.csv ... sfig1s3f.csv (+ ../work/sfig1s3?_overlay.png, _src.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import supp_image, dark_mask, vspine, hspine, ticks_left, ticks_below, fit_axis, write_csv, \
    save_overlay, save_crop, lineband  # noqa: E402

a = supp_image("fig1-figsupp3.jpg")
d = dark_mask(a, thr=110, sat=50)
C = {"OsO4": ((0, 110, 188), (152, 170, 204)),
     "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4": ((0, 125, 98), (168, 210, 202)),
     "2.5% (Ferri) K3[Fe(CN)6] + 2% OsO4": ((250, 0, 0), (250, 200, 200)),
     "2.5% (Ferro) K4[Fe(CN)6] (after 2% OsO4)": ((0, 220, 76), (136, 240, 170)),
     "2.5% (Ferri) K3[Fe(CN)6] (after 2% OsO4)": ((250, 100, 0), (250, 202, 168))}
PANELS = {  # window (r0, r1, c0, c1), series (legend names as printed under each row)
    "a": ((30, 500, 60, 490), ["OsO4", "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4", "2.5% (Ferri) K3[Fe(CN)6] + 2% OsO4"]),
    "b": ((30, 500, 560, 1050), ["OsO4", "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4", "2.5% (Ferri) K3[Fe(CN)6] + 2% OsO4"]),
    "c": ((745, 1215, 60, 490), ["OsO4", "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4", "2.5% (Ferro) K4[Fe(CN)6] (after 2% OsO4)"]),
    "d": ((745, 1215, 560, 1050), ["OsO4", "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4", "2.5% (Ferro) K4[Fe(CN)6] (after 2% OsO4)"]),
    "e": ((1460, 1930, 60, 490), ["OsO4", "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4", "2.5% (Ferri) K3[Fe(CN)6] (after 2% OsO4)"]),
    "f": ((1460, 1930, 560, 1050), ["OsO4", "2.5% (Ferro) K4[Fe(CN)6] + 2% OsO4", "2.5% (Ferri) K3[Fe(CN)6] (after 2% OsO4)"]),
}
for p, (W, names) in PANELS.items():
    vc, va, vb = vspine(d, *W)
    hr, ha, hb = hspine(d, *W)
    yt = ticks_left(d, vc, va - 5, vb + 5, L=3)
    xt = ticks_below(d, hr, ha - 5, hb + 5, L=3)
    assert len(yt) == 2 and len(xt) == 3, (p, yt, xt)
    if p in "ace":
        fy, yres, ys = fit_axis(sorted(yt, reverse=True), [0.4, 1])
        yname, ylab = "intensity_au", "Intensity (a.u.)"
        fx, xres, xs = fit_axis(xt, [0, 500, 1000])
        xname = "depth_um"
        ycal = "y on the 2 labelled ticks (0.4, 1), linear as in Figure 1e"
    else:
        fy, yres, ys = fit_axis(sorted(yt) + [hr], [20, 10, -10])   # ticks 20, 10 and the x-axis line at -10
        yname, ylab = "height_change_percent", "Change in sample height (%)"
        fx, xres, xs = fit_axis(xt, [0, 500, 1000])
        xname = "time_min"
        ycal = f"y on the ticks 20, 10 and the x-axis line (-10), max residual {yres:.3f} %"
    b = a.copy()
    P = (W[0] + 5, int(hr) - 2, int(vc) + 2, int(hb))
    lines = {n: C[n][0] for n in names}
    bands = {n: C[n][1] for n in names}
    rows, ov = lineband(b, P, fx, fy, lines, bands, maxjump=30, line_tol=55, band_tol=35)
    write_csv(os.path.join(HERE, f"sfig1s3{p}.csv"), [
        f"Ströh et al. 2022 eLife, Figure 1—figure supplement 3{p}: mean ± s.d. of the series named in the legend",
        "  under this row of panels (names as printed; see the legend text in the supplement legend).",
        f"Columns: series; {xname}; {yname} = {ylab} at the mean-line centre in that pixel column; sd_low / sd_high =",
        "  lower / upper edge of that series' shaded s.d. band in that column.",
        "Provenance: tier 3, digitized from the eLife figure-supplement JPEG (1050 x 2109 px) by sfig1s3_extract.py:",
        f"  colour masks per pixel column; x fitted on 3 ticks (0, 500, 1000), max residual {xres:.2f}; {ycal}.",
        f"Uncertainty: about ±{2 * abs(xs):.0f} in x and ±{2 * abs(ys):.3f} in y (2 px) plus JPEG blur; band edges ±3 px",
        "  where bands overlap. Where a line is hidden under another it has no value in that column.",
    ], ["series", xname, yname, "sd_low", "sd_high"], rows)
    crop = (W[0], int(hr) + 40, W[2], W[3])
    save_overlay(b, ov, f"sfig1s3{p}_overlay.png", crop=crop)
    save_crop(a, crop, os.path.join(HERE, f"../work/sfig1s3{p}_src.png"))
    print(p, len(rows), round(xres, 3), round(float(yres), 4))
