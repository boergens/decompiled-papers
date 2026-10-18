"""Fig. 5a-c: digitize the tensile stress, total energy and density curves of the bulk epoxy system.

Tier 3 (digitized). Source: the embedded 300 ppi JPEG of Fig. 5 on PDF page 8 (xref 129, 1854 x 1016 px).
Origin plots with inward tick marks; calibration = linear fit on the labelled major ticks found in the image.
 5a: open markers (x black squares, y red circles, z magenta triangles) found by template matching
     (templates = the legend's own markers, OpenCV TM_CCOEFF_NORMED on the colour mask); the dashed fit
     curves are also traced (centre per pixel column of the thick strokes) and compared with the printed
     equations.
 5b, 5c: line + small marker series; the centre of each colour's line per pixel column (largest run
     nearest the previous column), with the run's upper/lower ends.
Writes figures/fig5a.csv, fig5b.csv, fig5c.csv and overlays work/fig5{a,b,c}_overlay.png.
"""
import csv
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import digitize_common as dc  # noqa: E402
import f1_origin as fo  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PDF = ROOT / "source" / "wei2024.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)

NAMES = {"x": "x", "y": "y", "z": "z"}
# grid steps (strain = 0.005 * i) whose best match was judged wrong on the zoomed tile sheet
# (work/f1_tiles5a_unc.png): the cross sat on a dash or on another series' marker, not on this series' marker
REJECT = {"x": {2, 17, 33, 52}, "y": {1, 13, 19}, "z": {1, 5, 41}}
FITS = {"x": (-158.95, 0.045, 151.39), "y": (-152.11, 0.041, 139.91), "z": (-139.06, 0.040, 143.88)}


def write(path, hdr, cols, rows):
    with open(path, "w", newline="") as f:
        for h in hdr:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)


def calib(dark, L, R, T, B, xvals, yvals, xmajor_every=1, ymajor_every=1):
    xt = dc.tick_positions(dark, B, -1, 4, L[1] + 2, R[0] - 1)
    yt = dc.tick_positions_v(dark, L, +1, 4, T[1] + 2, B[0] - 1)
    return xt, yt


def panel_a(a, masks, dark, report):
    L, R, T, B = (78, 79), (600, 600), (10, 11), (394, 395)
    xt = dc.tick_positions(dark, B, -1, 4, L[1] + 2, R[0] - 1)
    yt = dc.tick_positions_v(dark, L, +1, 4, T[1] + 2, B[0] - 1)
    assert len(xt) == 7 and len(yt) == 5, (xt, yt)
    fx, rx, _ = dc.fit_axis(xt, [0, .05, .1, .15, .2, .25, .3])
    fy, ry, _ = dc.fit_axis(yt, [200, 150, 100, 50, 0])
    gx = np.polyfit([0, .05, .1, .15, .2, .25, .3], xt, 1)
    gy = np.polyfit([200, 150, 100, 50, 0], yt, 1)
    inner = np.zeros(dark.shape, bool)
    inner[T[1] + 3:B[0] - 2, L[1] + 3:R[0] - 2] = True
    legend = np.zeros(dark.shape, bool)
    legend[256:286, 330:482] = True       # 'Tensile direction'
    legend[286:376, 222:600] = True       # three legend entries with equations
    tmpl_boxes = {"x": (299, 305, 229, 235), "y": (329, 335, 229, 235), "z": (358, 365, 228, 236)}
    rows, ov = [], []
    stats = {}
    for k, m in masks.items():
        y0, y1, x0, x1 = tmpl_boxes[k]
        tmpl = np.pad(m[y0:y1, x0:x1], 1)      # legend marker with a 1 px empty margin
        mm = m & inner & ~legend
        import cv2
        t = tmpl.astype(np.float32)
        res = cv2.matchTemplate(mm.astype(np.float32), t, cv2.TM_CCOEFF_NORMED)
        ty, tx = np.where(tmpl)
        cy, cx = (ty.min() + ty.max()) / 2, (tx.min() + tx.max()) / 2
        pts = []
        # the markers sit on a grid of strain steps of 0.005 (seen in a first free search: all clear markers
        # fall within 1 px of it); search each grid column (+-2 px) for the best match of this series
        for i in range(61):
            xp = np.polyval(gx, 0.005 * i)
            c0 = int(round(xp - cx)) - 2
            band = res[:, c0:c0 + 5]
            yy, xx = np.unravel_index(np.argmax(band), band.shape)
            sc = float(band[yy, xx])
            X, Y = c0 + xx + cx, yy + cy
            if sc >= 0.45:
                pts.append((float(fx(X)), float(fy(Y)), sc))
            else:
                pts.append((0.005 * i, float("nan"), sc))
        A, tau, C = FITS[k]
        for i, (X, Y, sc) in enumerate(pts):
            near_fit = Y == Y and abs(np.polyval(gy, Y) - np.polyval(gy, A * np.exp(-X / tau) + C)) <= 3
            if Y != Y:
                flag = "not_found"
            elif i in REJECT[k]:
                flag = "rejected_by_eye"
            elif sc < 0.7 or near_fit:
                flag = "uncertain"
            else:
                flag = ""
            if flag == "rejected_by_eye":
                Y = float("nan")
            if Y == Y:
                ov.append((np.polyval(gx, X), np.polyval(gy, Y)))
            rows.append([NAMES[k], "marker", round(X, 5), "" if Y != Y else round(Y, 2), round(sc, 2), flag])
        # dashed fit curve: centre of thick strokes per column (excluding legend sample line)
        thick, _ = fo.split_thick(mm)
        tr = []
        for c in range(L[1] + 3, R[0] - 2):
            rr = np.where(thick[:, c])[0]
            if len(rr) == 0:
                continue
            runs = np.split(rr, np.where(np.diff(rr) > 1)[0] + 1)
            A, tau, C = FITS[k]
            ypred = np.polyval(gy, A * np.exp(-float(fx(c)) / tau) + C)
            run = min(runs, key=lambda q: abs(q.mean() - ypred))
            if abs(run.mean() - ypred) < 8 and len(run) <= 8:
                tr.append((c, run.mean()))
        for c, y in tr:
            rows.append([NAMES[k], "fit_curve_digitized", round(float(fx(c)), 5), round(float(fy(y)), 2), "", ""])
            ov.append((c, y))
        A, tau, C = FITS[k]
        res = [float(fy(y)) - (A * np.exp(-float(fx(c)) / tau) + C) for c, y in tr]
        fl = [r[5] for r in rows if r[0] == NAMES[k] and r[1] == "marker"]
        stats[k] = (fl.count(""), fl.count("uncertain"), fl.count("rejected_by_eye") + fl.count("not_found"), len(tr), float(np.mean(res)), float(np.max(np.abs(res))))
    hdr = [
        "Fig. 5a: tensile stress vs tensile strain of the bulk epoxy system, tensile directions x, y, z (legend 'Tensile direction')",
        "columns: series (x, y, z), kind (marker = one plotted data point; fit_curve_digitized = centre of the dashed fit curve, per pixel column),",
        "  tensile_strain (dimensionless), tensile_stress_MPa, score (template-match score of the marker, 0-1), flag",
        "markers: one per series per strain step of 0.005 (0 to 0.30, 61 steps; the step is seen in the figure: clear markers sit within 1 px of this grid); each grid column (+-2 px) is searched for the best match of the series' legend marker",
        "flag: '' = clear match (score >= 0.7, not on its own dashed curve); uncertain = score 0.45-0.7 or within 3 px of its own dashed fit curve (may be a dash or a partly hidden marker); rejected_by_eye = best match judged wrong on a zoomed check (stress left empty); not_found = no match >= 0.45 (stress empty, strain = grid value). Below a strain of about 0.03 the three dashed curves overlap the markers and most points there are uncertain",
        "printed fits (legend, as read): x: y = -158.95e^(-x/0.045) + 151.39, R^2 = 0.66; y: y = -152.11e^(-x/0.041) + 139.91, R^2 = 0.63; z: y = -139.06e^(-x/0.040) + 143.88, R^2 = 0.51 (exponent text is tiny; '(-x/0.045)' etc. read at zoom)",
        f"dashed curves vs printed equations (digitized minus equation, MPa): " + "; ".join(f"{k}: mean {v[4]:+.2f}, max |{v[5]:.2f}|" for k, v in stats.items()),
        "provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF p. 8, xref 129); figures/fig5_extract.py (normalized template matching, TM_CCOEFF_NORMED, of each series' colour mask with its own legend marker)",
        f"calibration: inward major ticks, x 0.00..0.30 (7 ticks, max residual {rx:.2g}), y 0..200 MPa (5 ticks, max residual {ry:.2g} MPa)",
        f"uncertainty: +-1 px = +-{abs(float(fx(1)-fx(0))):.4f} strain, +-{abs(float(fy(1)-fy(0))):.2f} MPa for markers; weak/hidden markers are flagged",
    ]
    write(HERE / "fig5a.csv", hdr, ["series", "kind", "tensile_strain", "tensile_stress_MPa", "score", "flag"], rows)
    dc.overlay(a[:470, :610].copy(), ov, str(WORK / "fig5a_overlay.png"), colour=(0, 200, 0))
    report["a"] = (stats, rx, ry)


def trace_lines(a, masks, box, legend, L, R, T, B, fx, fy, name):
    rows, ov, counts = [], [], {}
    ser_ov = {}
    inner = np.zeros(masks["x"].shape, bool)
    inner[T[1] + 12:B[0] - 12, L[1] + 12:R[0] - 12] = True     # leave out the inward tick marks
    for k, m in masks.items():
        mm = m & inner
        for (y0, y1, x0, x1) in legend:
            mm[y0:y1, x0:x1] = False
        env = dc.trace_envelope(mm, L[1] + 12, R[0] - 12, T[1] + 12, B[0] - 12, half_width=1)
        n = 0
        for c, ym, yu, yl in env:
            if ym != ym:
                continue
            ser_ov.setdefault(k, []).append((c, ym))
            rows.append([k, round(float(fx(c)), 5), round(float(fy(ym)), 5), round(float(fy(yu)), 5), round(float(fy(yl)), 5)])
            ov.append((c, ym))
            n += 1
        counts[k] = n
    # per-series check image: 3x enlargement of the panel, each series' points in a contrasting colour
    from PIL import Image, ImageDraw
    x0, x1, y0, y1 = L[0] - 5, R[1] + 5, T[0] - 5, B[1] + 5
    im = Image.fromarray(a[y0:y1, x0:x1]).resize(((x1 - x0) * 3, (y1 - y0) * 3), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    for k, col in (("x", (0, 220, 255)), ("y", (0, 200, 0)), ("z", (0, 0, 255))):
        for c, y in ser_ov.get(k, []):
            X, Y = (c - x0) * 3 + 1, (y - y0) * 3 + 1
            d.rectangle((X - 1, Y - 1, X + 1, Y + 1), fill=col)
    im.save(WORK / f"fig5{name}_series_check.png")
    return rows, ov, counts


def panel_bc(a, masks, dark, report):
    out = {}
    # 5b
    L, R, T, B = (715, 716), (1221, 1221), (10, 11), (382, 382)
    xt_all = dc.tick_positions(dark, B, -1, 4, L[1] + 2, R[0] - 1)
    # major ticks are the labelled ones at 0.00, 0.05, ...; pick those nearest a 72.2 px grid from the first
    xt = [t for t in xt_all if min(abs(t - (751.5 + 72.25 * i)) for i in range(7)) < 3]
    yt_all = dc.tick_positions_v(dark, L, +1, 4, T[1] + 2, B[0] - 1)
    yt = [t for t in yt_all if min(abs(t - (60.5 + 49.5 * i)) for i in range(7)) < 3]
    assert len(xt) == 7 and len(yt) == 7, (xt, yt)
    fx, rx, _ = dc.fit_axis(xt, [0, .05, .1, .15, .2, .25, .3])
    fy, ry, _ = dc.fit_axis(yt, [-500, -1000, -1500, -2000, -2500, -3000, -3500])
    rows, ov, counts = trace_lines(a, masks, None, [(205, 312, 990, 1155)], L, R, T, B, fx, fy, "b")
    hdr = [
        "Fig. 5b: total energy (kcal/mol) of the bulk epoxy system vs tensile strain, tensile directions x (black squares), y (red circles), z (magenta triangles); lines with small markers",
        "columns: series, tensile_strain, total_energy_kcal_per_mol = centre of the series' line in this pixel column, upper/lower = ends of the line's run in the column (the band the curve passes through)",
        "provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF p. 8, xref 129) by colour masks, figures/fig5_extract.py; one row per pixel column (markers merge with the line and are not listed separately)",
        f"calibration: labelled major ticks x 0.00..0.30 (7, max residual {rx:.2g}), y -500..-3500 (7, max residual {ry:.2g} kcal/mol); minor ticks every 0.025 / 250 not used",
        f"uncertainty: +-1 px = +-{abs(float(fx(1)-fx(0))):.4f} strain, +-{abs(float(fy(1)-fy(0))):.1f} kcal/mol; where the lines cross, a colour hidden under another one has no point (gaps), and the black mask can pick up the dark marker outlines of the other colours' crossings",
        "the y axis runs from about -3750 (bottom frame) to 0 (top frame, labelled 0)",
    ]
    write(HERE / "fig5b.csv", hdr, ["series", "tensile_strain", "total_energy_kcal_per_mol", "upper", "lower"], rows)
    dc.overlay(a[:470, 610:1240].copy(), [(x - 610, y) for x, y in ov], str(WORK / "fig5b_overlay.png"), colour=(0, 200, 0))
    out["b"] = (counts, rx, ry)
    # 5c
    L, R, T, B = (1339, 1340), (1837, 1838), (9, 10), (375, 376)
    xt = dc.tick_positions(dark, B, -1, 4, L[1] + 2, R[0] - 1)
    yt = dc.tick_positions_v(dark, L, +1, 4, T[1] + 2, B[0] - 1)
    assert len(xt) == 7 and len(yt) == 8, (xt, yt)
    fx, rx, _ = dc.fit_axis(xt, [0, .05, .1, .15, .2, .25, .3])
    fy, ry, _ = dc.fit_axis(yt, [1.130, 1.125, 1.120, 1.115, 1.110, 1.105, 1.100, 1.095])
    rows, ov, counts = trace_lines(a, masks, None, [(28, 148, 1605, 1765)], L, R, T, B, fx, fy, "c")
    hdr = [
        "Fig. 5c: density (kg/m^3, as printed on the axis) of the bulk epoxy system vs tensile strain, tensile directions x (black squares), y (red circles), z (magenta triangles); lines with small markers",
        "columns: series, tensile_strain, density = centre of the series' line in this pixel column, upper/lower = ends of the line's run in the column",
        "provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF p. 8, xref 129) by colour masks, figures/fig5_extract.py; one row per pixel column",
        f"calibration: labelled major ticks x 0.00..0.30 (7, max residual {rx:.2g}), y 1.130..1.095 (8 ticks, max residual {ry:.2g}); 1.090 is the bottom frame",
        f"uncertainty: +-1 px = +-{abs(float(fx(1)-fx(0))):.4f} strain, +-{abs(float(fy(1)-fy(0))):.5f} density units; where lines cross, a hidden colour has no point",
        "unit as printed: kg/m^3 (the values ~1.1 match g/cm^3 for epoxy; the paper writes kg/m3 in the text too)",
    ]
    write(HERE / "fig5c.csv", hdr, ["series", "tensile_strain", "density", "upper", "lower"], rows)
    dc.overlay(a[:470, 1240:].copy(), [(x - 1240, y) for x, y in ov], str(WORK / "fig5c_overlay.png"), colour=(0, 200, 0))
    out["c"] = (counts, rx, ry)
    report.update(out)


def main():
    a = dc.embedded_image(str(PDF), 8)
    masks = fo.colour_masks(a)
    dark = dc.gray(a) < 140
    report = {}
    panel_a(a, masks, dark, report)
    panel_bc(a, masks, dark, report)
    for k, v in report.items():
        print(k, v)


if __name__ == "__main__":
    main()
