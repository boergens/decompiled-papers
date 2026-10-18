"""Fig. 2c of Zhao et al. 2025: crack extension energy G and its blade (G1) and stretch (G2) contributions vs
stretch ratio lambda. The plot area is part of the 300 ppi raster image embedded on page 3 (tick labels and the
legend are PDF text), so this is a digitization (tier 3). Writes fig2c.csv and work/fig2c_overlay.png.
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
import rastermarkers as rm  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
a = dc.embedded_image(str(PDF), 3)
# tick centres (rm.tick_centres): bottom axis 1.1-1.4 ticks, left frame = 1.0 (label '1'), right frame = 1.5;
# left axis 0 (bottom frame), 400, 800, 1200 (top frame)
XT = [(0.53, 1.0), (112.39, 1.1), (226.37, 1.2), (340.32, 1.3), (454.0, 1.4), (568.0, 1.5)]
YT = [(1009.46, 0), (862.71, 400), (716.99, 800), (571.0, 1200)]
fx, rx, _ = dc.fit_axis([p for p, v in XT], [v for p, v in XT])
fy, ry, _ = dc.fit_axis([p for p, v in YT], [v for p, v in YT])
REGION = (572, 1009, 2, 568)
LEGEND = (230, 550, 590, 695)      # columns, rows of the legend box in the image (excluded)
FRAME_TOP, FRAME_BOT = 572, 1009

SER = [("Crack extension energy", [(255, 190, 122)]), ("Blade contribution", [(40, 120, 181)]),
       ("Stretch contribution", [(255, 0, 0)])]
bar_mask = rm.colour_mask(a, [(65, 158, 221), (81, 167, 224), (46, 149, 218)], tol=45)   # light-blue error bars
rows, ov = [], []
for name, cols in SER:
    mask = rm.colour_mask(a, cols, tol=40)
    mks = rm.find_markers(mask, REGION, k=5, min_area=40)
    mks = [m for m in mks if not (LEGEND[0] <= m["cx"] <= LEGEND[1] and LEGEND[2] <= m["cy"] <= LEGEND[3])]
    if name == "Blade contribution":
        mks = [m for m in mks if m["cx"] < 500]          # the blue Fracture icon at lambda 1.45 is treated below
    for mk in mks:
        flag = []
        if mk["h"] < 12:
            # partly hidden under another series' square: square is 14 px, take the visible top edge + 6.5
            cx = mk["x0"] + (mk["w"] - 1) / 2
            cy = mk["y0"] + 6.5
            flag.append("square partly hidden under the Blade-contribution square; y from its visible top edge (+-2 px)")
        else:
            cx, cy, top, bot = rm.centre(mask, mk)
        lo = hi = np.nan
        if name == "Blade contribution":
            eb = rm.error_bar(bar_mask, cx, cy, int(cy) - 7, int(cy) + 7, FRAME_TOP, FRAME_BOT, bar_half=2,
                              cap_need=6, window=45)
            up, dn = eb["upper"][0], eb["lower"][0]
            if up is not None and dn is not None:
                hi, lo = float(fy(up)), float(fy(dn))
                ov += [(cx, up), (cx, dn)]
            else:
                flag.append("no error-bar caps visible outside the square")
        if mk["y0"] + mk["h"] >= FRAME_BOT - 1:
            flag.append("square touches the bottom frame")
        rows.append([name, float(fx(cx)), float(fy(cy)), lo, hi, round(cx, 1), round(cy, 1), "; ".join(flag)])
        ov.append((cx, cy))

# 'Fracture without blade' icons at lambda ~1.45 (white zigzag on a coloured square): centre of the icon's pixels
for name, cols, box in (("Fracture without blade (Crack extension energy / Stretch contribution)", [(229, 194, 109)],
                         (500, 530, 800, 845)),
                        ("Fracture without blade (Blade contribution)", [(46, 117, 182)], (500, 530, 985, 1018))):
    m = rm.colour_mask(a, cols, tol=40)
    c0, c1, r0, r1 = box
    sub = m[r0:r1, c0:c1]
    rr = np.nonzero(sub.sum(1) >= 8)[0]                 # rows of the icon square (drops crossing lines)
    cc = np.nonzero(sub[rr].sum(0) >= 0.5 * len(rr))[0]
    x0, x1, y0, y1 = cc.min() + c0, cc.max() + c0, rr.min() + r0, rr.max() + r0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    flag = "icon %dx%d px; centre of its bounding box (+-1.5 px)" % (x1 - x0 + 1, y1 - y0 + 1)
    if y1 > FRAME_BOT:
        flag += "; the icon is drawn over the bottom frame, reaching below it"
    rows.append([name, float(fx(cx)), float(fy(cy)), np.nan, np.nan, round(cx, 1), round(cy, 1), flag])
    ov.append((cx, cy))

# lines that leave the top of the frame (series continue off-scale to the left)
for name, cols in (("Crack extension energy (line leaves the top frame)", [(255, 190, 122)]),):
    m = rm.colour_mask(a, cols, tol=40)
    r = 574
    xs = np.nonzero(m[r, 100:160])[0] + 100
    cx = float(xs.mean())
    rows.append([name, float(fx(cx)), float(fy(r)), np.nan, np.nan, round(cx, 1), r, "line from the lambda ~1.12 point"
                 " up to the top frame; its other end (lambda ~1.08) is off scale. A thin Blade-contribution line"
                 " runs alongside it, 1-2 px to the left (also off scale)."])
    ov.append((cx, r))

head = [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 2c: crack extension energy G (Eq. 4, orange squares) and its two",
    "  contributions, blade G1 (Eq. 2, blue squares) and stretch G2 (Eq. 3, red squares), vs stretch ratio lambda;",
    "  axis 'G,G1, and G2 (J m-2)'. Points are joined by lines in the figure. Only the blade contribution has",
    "  visible (light-blue) error bars; err_low/err_high = its caps (empty elsewhere or where caps are hidden).",
    "  The three shaded regions (I, II, III) are not data; their edges are at lambda %.3f and %.3f (raster colour"
    " changes)." % (fx(161.5), fx(487.0)),
    "Columns: series; lambda; G_J_m2 (J m^-2); err_low/err_high; px_x/px_y = point in the embedded image; flag.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image on page 3 (colour masks, 5x5 opening for",
    "  squares; x centre = middle of the square's columns, y centre = middle of its fully covered rows).",
    "  x: %s; max residual %.2g" % (", ".join(f"{v:g}@{p}px" for p, v in XT), rx),
    "  y: %s; max residual %.2g J m^-2" % (", ".join(f"{v:g}@{p}px" for p, v in YT), ry),
    "Uncertainty: about +-1 px = +-0.001 in lambda and +-2.7 J m^-2 (more where flagged).",
]
dc.write_csv(HERE / "fig2c.csv", head, ["series", "lambda", "G_J_m2", "err_low", "err_high", "px_x", "px_y", "flag"],
             rows, fmt=["{}", "{:.4f}", "{:.4g}", "{:.4g}", "{:.4g}", "{:.1f}", "{:.1f}", "{}"])
for r in rows:
    print([r[0][:30]] + [round(v, 4) if isinstance(v, float) else v for v in r[1:5]] + [r[7][:60]])
(ROOT / "work").mkdir(exist_ok=True)
dc.overlay(a[560:1018, 0:575].copy(), [(x, y - 560) for x, y in ov], str(ROOT / "work" / "fig2c_overlay.png"),
           colour=(255, 0, 255))
