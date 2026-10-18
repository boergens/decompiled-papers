"""Digitize Figure 2—figure supplement 3a,b of Ströh et al. 2022 (eLife JPEG fig2-figsupp3.jpg, 1046 x 669 px).

a: Intensity (a.u.) vs Depth (μm): blue 't = 0 hrs after in H2O', black 't = 20 hrs after in H2O' (n=1, no bands).
b: Change in sample height (%) vs Time (min): one black line (n=1).
Spines and tick marks found in the image, labels read by eye; the thin black reference lines (1 in a, 0 % in b) are
blanked before tracing.   python3 -I sfig2s3_extract.py -> sfig2s3a.csv, sfig2s3b.csv
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from main_common import supp_image, dark_mask, vspine, hspine, ticks_left, ticks_below, fit_axis, write_csv, \
    save_overlay, save_crop, column_trace, colour_mask  # noqa: E402

a = supp_image("fig2-figsupp3.jpg")
d = dark_mask(a, thr=110, sat=50)
for p, W in (("a", (40, 470, 60, 500)), ("b", (40, 470, 560, 1046))):
    vc, va, vb = vspine(d, *W)
    hr, ha, hb = hspine(d, *W)
    yt = ticks_left(d, vc, va - 5, vb + 5, L=3)
    xt = ticks_below(d, hr, ha - 5, hb + 5, L=3)
    if p == "a":
        assert len(yt) == 2 and len(xt) == 3, (yt, xt)
        fy, yres, ys = fit_axis(sorted(yt, reverse=True), [0.4, 1])
        ref = sorted(yt)[0]
        series = {"t = 0 hrs after in H2O": "blue", "t = 20 hrs after in H2O": "black"}
        xname, yname = "depth_um", "intensity_au"
        ycal = "y on the 2 labelled ticks (0.4, 1), linear as in Figure 1e"
    else:
        yt = [t for t in yt if t < 200] + [hr]           # 20, 10 and the x-axis line (-10); the 0 tick is under the curve
        fy, yres, ys = fit_axis(sorted(yt), [20, 10, -10])
        ref = float((0 - fy(0)) / ys)                     # row of 0 %
        series = {"height change": "black"}
        xname, yname = "time_min", "height_change_percent"
        ycal = f"y on the ticks 20, 10 and the x-axis line (-10), max residual {yres:.3f} %"
    fx, xres, xs = fit_axis(xt if len(xt) == 3 else [vc] + xt, [0, 500, 1000])
    b = a.copy()
    r = int(round(ref))
    thin = b[r - 2:r + 3, int(vc) + 3:]
    keep = dark_mask(b, thr=110, sat=50)
    # blank the reference line only where it is thin (the thick curves keep their pixels)
    for c in range(int(vc) + 3, b.shape[1]):
        col = keep[r - 6:r + 7, c]
        if col.sum() <= 4:
            b[r - 2:r + 3, c][keep[r - 2:r + 3, c]] = 255
    rows, ov = [], []
    for name, kind in series.items():
        m = colour_mask(b, (0, 110, 188), 60) if kind == "blue" else dark_mask(b, thr=90, sat=40)
        tr = column_trace(m, int(vc) + 6, int(hb), W[0], int(hr) - 2, maxjump=20)   # +6: skip tick marks
        rows += [(name, float(fx(c)), float(fy(mid)), float(fy(bot)), float(fy(top))) for c, mid, top, bot in tr if mid == mid]
        ov.append(((255, 0, 255) if kind == "black" else (255, 140, 0), [(c, mid) for c, mid, t, bb in tr]))
    write_csv(os.path.join(HERE, f"sfig2s3{p}.csv"), [
        f"Ströh et al. 2022 eLife, Figure 2—figure supplement 3{p} (n=1; series names from the legend).",
        f"Columns: series; {xname}; {yname} at the line centre in that pixel column; line_bottom / line_top = the",
        "  values at the lower / upper edge of the (thick, ~8 px) line in that column.",
        "Provenance: tier 3, digitized from the eLife figure-supplement JPEG by sfig2s3_extract.py; x fitted on 3 ticks",
        f"  (0, 500, 1000), max residual {xres:.2f}; {ycal}. The thin reference line was blanked before tracing.",
        f"Uncertainty: about ±{2 * abs(xs):.0f} in x and ±{2 * abs(ys):.3f} in y (2 px) plus JPEG blur.",
    ], ["series", xname, yname, "line_bottom", "line_top"], rows)
    crop = (W[0], int(hr) + 40, W[2], W[3])
    save_overlay(b, ov, f"sfig2s3{p}_overlay.png", crop=crop)
    save_crop(a, crop, os.path.join(HERE, f"../work/sfig2s3{p}_src.png"))
    print(p, len(rows), xres, yres)
