"""Digitize Figure 1 of Gabričević, Lente & Fábián 2020 (poc.4045.pdf p. 3): UV-vis spectra after 24 h (TCE-OsO4
stoichiometry series) and the inset (A at 320 nm vs [TCE]/[Os(VIII)]).

Source: the embedded raster image of Figure 1 (1003 x 721 px).
Main panel: 11 spectra, one colour each, no legend (the caption gives only the [TCE] range). Names used here are the
line colours as they appear in the image. Five lie well apart (red, blue, teal, magenta, olive from top to bottom at
300 nm); six run in a tight bundle (navy, wine, pink, royal blue, black, green), within about 10 px of each other
between 280 and 400 nm.
Inset: 11 grey diamonds, a red dotted straight line and an orange dashed horizontal line.
    python3 -I fig1_extract.py   -> fig1main.csv, fig1inset.csv (+ ../work/fig1_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from gab_common import (load, gray, tick_positions, tick_positions_v, fit_axis, scatter, write_csv, overlay,  # noqa: E402
                        cross_overlay, WORK)
from spectra_common import trace_spectra, straight_line, OVERLAP_PX  # noqa: E402

a = load("fig1")
dark = gray(a) < 120
# ---- main panel: frame left col 106-107, right 979-980, top rows 4-6, bottom row 622
BOT, LEFT, TOP = (622, 622), (106, 107), 6
xt = tick_positions(dark, BOT, 1, 8, 108, 978)            # 300, 350, 400, 450, 500 nm (350/450 unlabelled)
yt = tick_positions_v(dark, LEFT, -1, 4, 7, 620)          # 2.5, 2, 1.5, 1, 0.5 (2 and 1 labelled; 0 = frame)
assert len(xt) == 5 and len(yt) == 5, (xt, yt)
fx, rx, sx = fit_axis([xt[0], xt[2], xt[4]], [300, 400, 500])          # labelled ticks
fx_all, rx_all, _ = fit_axis(xt, [300, 350, 400, 450, 500])
fy, ry, sy = fit_axis([yt[1], yt[3], 622.0], [2.0, 1.0, 0.0])          # labelled: 2, 1, 0 (bottom frame)
_, ry_all, _ = fit_axis(yt + [622.0], [2.5, 2.0, 1.5, 1.0, 0.5, 0.0])
INSET = (532, 0, 985, 342)                                             # inset box incl. its frame and labels
box = (109, TOP + 1, 978, 621)
specs = [
    dict(name="red", rgb=(255, 0, 0), seed=(330, 167), extra_seeds=[(120, 135, 109, 150)]),
    dict(name="blue", rgb=(0, 0, 255), seed=(330, 235)),
    dict(name="teal", rgb=(0, 128, 128), seed=(330, 249)),
    dict(name="magenta", rgb=(255, 0, 255), seed=(330, 263)),
    dict(name="olive", rgb=(128, 128, 0), seed=(330, 336)),
    dict(name="navy", rgb=(0, 0, 115), seed=(380, 458), tol=30),
    dict(name="wine", rgb=(140, 0, 0), seed=(420, 481), tol=40),
    dict(name="pink", rgb=(255, 0, 140), seed=(380, 470), tol=45),
    dict(name="royal blue", rgb=(0, 0, 170), seed=(380, 473), tol=30),
    dict(name="black", rgb=(0, 0, 0), seed=(600, 577), tol=35, alpha_min=0.8),
    dict(name="green", rgb=(0, 128, 0), seed=(380, 482)),
]
traces, rows = trace_spectra(a, specs, box, exclude=[INSET], fx=fx, fy=fy, top_frame=TOP)
pts = []
for name, tr in traces.items():
    for c, (t, b) in tr.items():
        pts += [(c, (t + b) / 2)]
rows.sort(key=lambda r: ([s["name"] for s in specs].index(r[0]), r[1]))
cover = {n: (fx(min(tr)), fx(max(tr)), len(tr)) for n, tr in traces.items()}
write_csv(os.path.join(HERE, "fig1main.csv"), [
    "Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 1 (main panel): UV-vis spectra of TCE-OsO4",
    "  mixtures measured after completion of the reaction (24 h); [Os(VIII)] = 1.00 mmol/dm3, [TCE] = 0.050-5.0 mmol/dm3.",
    "  The figure has no legend: which spectrum belongs to which [TCE] is not given. 'series' is the line colour as",
    "  it appears in the image (11 spectra).",
    "Columns: series; wavelength_nm = lambda (nm); A = absorbance at the line centre in this pixel column; A_upper/A_lower",
    "  = top and bottom of the line in the column (they differ on steep parts); flags: 'overlap' = another traced",
    f"  spectrum passes within {OVERLAP_PX} px (about {OVERLAP_PX * abs(sy):.3f} A) in this column, so the colour assignment and value",
    "  are uncertain there; 'clipped' = the curve runs into the top frame. One row per pixel column where the line's",
    "  colour is visible; columns where it is hidden under other lines are missing.",
    "Provenance: tier 3, digitized from the embedded raster image (1003 x 721 px; no vector data in the PDF) by",
    f"  fig1_extract.py. x calibrated on the labelled ticks 300, 400, 500 nm, max residual {rx:.2g} nm (all 5 ticks incl.",
    f"  350/450: {rx_all:.2g} nm); left frame = {float(fx(106.5)):.1f} nm, right frame = {float(fx(979.5)):.1f} nm. y on the labelled",
    f"  ticks 2 and 1 and the bottom frame (0), max residual {ry:.2g} (with the unlabelled 0.5/1.5/2.5 ticks: {ry_all:.2g});",
    f"  top frame = {float(fy(5)):.2f}. Lines followed column by column through colour masks from a seed where each is clear.",
    f"Uncertainty: about +-{2 * abs(sx):.1f} nm and +-{2 * abs(sy):.3f} A (2 px) where a line is isolated. Inside the bundle of six",
    "  (navy, wine, pink, royal blue, black, green, 280-400 nm) the lines overlap and partly hide each other in the",
    "  JPEG-compressed image; values flagged 'overlap' may belong to a neighbouring line (error up to ~0.05 A).",
    "Coverage (nm from-to, columns): " + "; ".join(f"{n} {v[0]:.0f}-{v[1]:.0f} ({v[2]})" for n, v in cover.items()),
], ["series", "wavelength_nm", "A", "A_upper", "A_lower", "flags"], rows, fmt="{:.5g}")

# ---- inset: frame left col 537, bottom rows 334-335; top/right = main frame
IL, IB = (537, 537), (334, 335)
ixt = tick_positions(dark, IB, 1, 4, 540, 977)            # 1..5 (2 and 4 labelled)
iyt = tick_positions_v(dark, IL, -1, 8, 8, 332)            # 2.0, 1.5, 1.0 (labelled)
assert len(ixt) == 5 and len(iyt) == 3, (ixt, iyt)
ifx, irx, isx = fit_axis([537.0, ixt[1], ixt[3]], [0, 2, 4])      # 0 (frame, labelled), 2, 4
_, irx_all, _ = fit_axis([537.0] + ixt, [0, 1, 2, 3, 4, 5])
ify, iry, isy = fit_axis(iyt + [334.5], [2.0, 1.5, 1.0, 0.5])     # bottom frame = 0.5 (labelled)
ibox = (539, 7, 978, 333)
found = scatter(a, [("data", (128, 128, 128))], ibox, alpha_min=0.6, min_area=40, split=True)
irows = [("data", "marker", float(ifx(x)), float(ify(y)), w, h, f) for n, x, y, w, h, f in found]
irows.sort(key=lambda r: r[2])
from gab_common import colour_mask  # noqa: E402
grey = colour_mask(a, (128, 128, 128), alpha_min=0.3)
lines = {}
from spectra_common import hue_mask  # noqa: E402
ora = hue_mask(a, "orange")
sl, ic, (xa, xb), (xs, ys), rms = straight_line(a, ora, ibox, ifx, ify, exclude_mask=grey)
lines["orange dashed line"] = (sl, ic, xa, xb, rms, len(xs))
orow = np.median(ys)
red = hue_mask(a, "red") & ~ora
red[int(orow) - 4:int(orow) + 5, :] = False       # the dashes of the orange line have red-looking cores
sl2, ic2, (xa2, xb2), (xs2, ys2), rms2 = straight_line(a, red, ibox, ifx, ify, exclude_mask=grey)
lines["red dotted line"] = (sl2, ic2, xa2, xb2, rms2, len(xs2))
for lname, (sl_, ic_, xa_, xb_, _, _) in lines.items():
    for xv in (xa_, xb_):
        irows.append((lname, "line end", float(xv), float(sl_ * xv + ic_), "", "", ""))
pts += list(zip(xs, ys)) + list(zip(xs2, ys2))
write_csv(os.path.join(HERE, "fig1inset.csv"), [
    "Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 1 inset: absorbance change at 320 nm vs",
    "  TCE/OsO4 ratio (x axis title '[TCE]/[Os(VIII)]', y axis title 'A (320 nm)').",
    "Columns: series ('data' = grey diamonds; the two straight lines); kind = marker or 'line end' (the two ends of a",
    "  straight line fitted to that line's pixels); ratio = [TCE]/[Os(VIII)]; A_320 = A (320 nm); marker size; note.",
    "Provenance: tier 3, digitized from the embedded raster image by fig1_extract.py. x calibrated on the inset's left",
    f"  frame (0) and the labelled ticks 2 and 4, max residual {irx:.2g} (with the unlabelled 1, 3, 5: {irx_all:.2g}); y on 2.0, 1.5,",
    f"  1.0 and the bottom frame (0.5), max residual {iry:.2g}. Markers: bounding-box centre of the grey blob (overlapping",
    "  diamonds flagged). Lines: least-squares straight line through the pixels of the dotted/dashed line (grey marker",
    "  pixels excluded; the red dotted line's pixels in the 9 rows around the orange line are also excluded);\n#   " + "; ".join(f"{k}: A = {v[0]:.4g} x ratio + {v[1]:.4g}, rms {v[4]:.3f}, {v[5]} px" for k, v in lines.items()) + ".",
    f"Uncertainty: about +-{2 * abs(isx):.3f} in ratio and +-{2 * abs(isy):.3f} in A (2 px).",
], ["series", "kind", "ratio", "A_320", "marker_w_px", "marker_h_px", "note"], irows, fmt="{:.4g}")
overlay(a, pts, os.path.join(WORK, "fig1_overlay.png"))
from PIL import Image  # noqa: E402
cross_overlay(np.array(Image.open(os.path.join(WORK, "fig1_overlay.png"))), [(x, y) for n, x, y, w, h, f in found],
              os.path.join(WORK, "fig1_overlay.png"), colour=(0, 255, 255))
print("main", cover)
print("x res", rx, rx_all, "y res", ry, ry_all)
print("inset", irx, irx_all, iry, lines)
for r in irows:
    print(r)
