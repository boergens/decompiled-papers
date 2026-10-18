"""Digitize Fig. 15f of wei2024 (tier 3): Fy scatter of the five sliding velocities and the five fitted curves.

Writes figures/fig15f.csv (markers) and figures/fig15f_fits.csv (the dashed fit curves, evaluated from the
equations printed in the panel's legend, checked against the drawn dashed curves by overlay), plus
work/fig15f_overlay.png, work/fig15f_overlay_zoom.png and work/fig15f_vs_ae.csv (each marker against the Fy
value digitized at the same sliding distance in Figs. 15a-e; run figures/fig15_extract.py first).
Method for the markers: as figures/fig15_extract.py (tools/f3_markers.py): colour mask per velocity, legend
text boxes blanked, holes filled, filled synthetic template of the marker shape, ink of the other series
counts half; per series the best match within +-3 px of each marker column. The marker columns (spacing
per velocity) were found by free template-peak detection and agree with Figs. 15a-e: 0.1, 0.5 and 2.0 A/ps
every 0.5 A, 1.0 A/ps every 1 A, 1.5 A/ps every 0.375 A.
Run: python3 -I -B figures/fig15f_extract.py
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402
import f3_markers as fm  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)

FRAME = ((1455, 1457), (2031, 2033), (604, 605), (1027, 1028))
YV = [0, -4, -8, -12, -16]  # -20 sits on the bottom frame line
BLANK = [(1560, 612, 2028, 680), (1440, 921, 1900, 1022)]  # the two legend blocks (lines + text)
# name, colour, marker shape, (w, h) px, marker spacing (A), legend equation (a, b, c, R2) for y = a e^(-x/b) + c
SERIES = [
    ("0.1 A/ps", "black", "open square", (6, 6), 0.5, (6.31, 3.68, -5.22, 0.53), "15a"),
    ("0.5 A/ps", "red", "open up-triangle", (7, 7), 0.5, (6.46, 5.78, -7.26, 0.60), "15b"),
    ("1.0 A/ps", "orange", "open down-triangle", (7, 7), 1.0, (7.0, 7.51, -8.06, 0.62), "15c"),
    ("1.5 A/ps", "blue", "open diamond", (8, 8), 0.375, (8.39, 9.34, -10.01, 0.61), "15d"),
    ("2.0 A/ps", "magenta", "filled circle", (7, 7), 0.5, (6.45, 8.44, -9.36, 0.42), "15e"),
]


def load_panel(key):
    out = {}
    p = HERE / f"fig{key}.csv"
    if not p.exists():
        return out
    for r in csv.reader(line for line in open(p) if not line.startswith("#")):
        if r[0] == "Fy" and r[2] != "":
            out[float(r[1])] = float(r[2])
    return out


def main():
    a = dc.embedded_image(str(PDF), 19, bbox_near=(54, 59, 542, 338))
    fx, fy, inv_x, caltxt, sx, sy = fm.calib(a, FRAME, [0, 5, 10, 15, 20, 25, 30], YV)
    L, R, T, B = FRAME
    box = (L[1] + 2, T[1] + 2, R[0] - 1, B[0] - 1)
    rows, pts, cmp_rows = [], [], []
    masks = {}
    obox = (L[0], T[0], R[1] + 1, B[1] + 1)
    for name, colour, shape, (w, h), step, eq, key in SERIES:
        bl = list(BLANK)
        if colour == "black":
            bl += [(box[0], box[1], box[0] + 11, box[3]), (box[0], box[3] - 11, box[2], box[3])]
            masks[colour] = fm.series_mask(a, colour, box, bl)
        else:
            masks[colour] = fm.series_mask(a, colour, obox, bl)
    frame_ink = fm.series_mask(a, "black", obox, BLANK)
    for name, colour, shape, (w, h), step, eq, key in SERIES:
        others = np.zeros_like(masks[colour])
        for oc, om in masks.items():
            if oc != colour:
                others |= om
        if colour != "black":
            others |= frame_ink
        Tt, cen = fm.synth_template(shape, w, h)
        grid = np.arange(1, int(round(30 / step)) + 1) * step
        rr = (box[1], box[3]) if colour == "black" else (T[0], B[1] + 1)
        glob = fm.match_grid(masks[colour], Tt, cen, inv_x(grid), rr, tol=3, close=0, others=others)
        panel = load_panel(key)
        for g, gres in zip(grid, glob):
            near = [k for k in panel if abs(k - g) < 0.2]
            how = "global"
            res = gres
            if near:
                # guided: best match within +-10 px (about +-0.5 nN) of the Fy value read in Fig. 15a-e
                ypred = float((panel[near[0]] - fy(0.0)) / (fy(1.0) - fy(0.0)))
                loc = fm.match_grid(masks[colour], Tt, cen, [gres[0]], (ypred - 10, ypred + 10), tol=3, close=0, others=others)[0]
                if loc[3] >= 0.45:
                    res, how = loc, "guided"
            xe, xc, yc, score, rflag = res
            flag = "" if score >= 0.6 else ("partly covered" if score >= 0.45 else "hidden (marker not visible; best-fitting ink at that column)")
            if how == "global" and near:
                flag = (flag + "; " if flag else "") + "no marker within +-10 px of the Fig. " + key + " value (global best match taken)"
            if "other-series" in rflag:
                flag = (flag + "; " if flag else "") + rflag[rflag.index("other-series"):]
            x, y = float(fx(xc)), float(fy(yc))
            rows.append([name, f"{x:.3f}", f"{y:.4g}", round(score, 3), how, flag])
            pts.append((xc, yc))
            if near:
                cmp_rows.append([name, f"{g:g}", f"{y:.3f}", f"{panel[near[0]]:.3f}", f"{y - panel[near[0]]:+.3f}", how, flag])
    header = [
        "wei2024 Fig. 15f: Fy and sliding distance curve (hc = 20 A, sliding velocities 0.1-2.0 A/ps). Markers of the scatter.",
        "Columns: series (sliding velocity, legend name), x = sliding distance (A), y = force along y-direction Fy (nN),",
        "match = template-match score (1 = marker template fully covered; other series' ink counts half), flag.",
        "Markers: 0.1 A/ps black open squares, 0.5 red open up-triangles, 1.0 orange open down-triangles, 1.5 blue open",
        "diamonds, 2.0 magenta open circles (the legend shows only the dashed fit lines).",
        "Provenance: tier 3 (digitized) from the embedded 300 ppi JPEG (PDF page 19, xref 264) by figures/fig15f_extract.py;",
        "best match within +-3 px of each marker column; marker spacing 0.5 A (0.1, 0.5, 2.0 A/ps), 1 A (1.0), 0.375 A (1.5),",
        "the same as in Figs. 15a-e. The scatter shows the same points as the Fy series of Figs. 15a-e (checked: work/fig15f_vs_ae.csv),",
        "but here the markers overlap each other and the same-coloured dashed fit curves, so the search is guided: search = 'guided'",
        "means the best match within +-10 px (about +-0.5 nN) of the value read in Fig. 15a-e (taken when its score >= 0.45);",
        "'global' = best match anywhere in the column. The values of Figs. 15a-e are the better reading of the same points.",
        "Calibration (inward major ticks, linear): " + caltxt + "; the frame lines map to 2.02 (top) and -20.0 (bottom).",
        f"Uncertainty: about +-1 px = +-{sx:.2g} A in x and +-{sy:.2g} nN in y for clean markers, +-2-4 px for flagged ones.",
        "flag: 'other-series ink covers N%' = the marker overlaps markers/lines of other series; 'partly covered'/'hidden' as in fig15a.csv.",
    ]
    with open(HERE / "fig15f.csv", "w", newline="") as f:
        for hl in header:
            f.write("# " + hl + "\n")
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["series", "x_A", "Fy_nN", "match", "search", "flag"])
        wr.writerows(rows)
    # fit curves from the legend equations
    fits = []
    xs = np.round(np.arange(0.5, 30.001, 0.25), 3)
    for name, colour, shape, wh, step, (A, Bc, C, r2), key in SERIES:
        for x in xs:
            fits.append([name, f"{x:g}", f"{A * np.exp(-x / Bc) + C:.4f}", A, Bc, C, r2])
    with open(HERE / "fig15f_fits.csv", "w", newline="") as f:
        for hl in [
            "wei2024 Fig. 15f: the five dashed fit curves y = a e^(-x/b) + c (Eq. 16), evaluated from the equations printed in the",
            "panel's legend (transcribed from the image: 0.1 A/ps y = 6.31e^(-x/3.68) - 5.22, R2 = 0.53; 0.5 A/ps y = 6.46e^(-x/5.78) - 7.26,",
            "R2 = 0.60; 1.0 A/ps y = 7.0e^(-x/7.51) - 8.06, R2 = 0.62; 1.5 A/ps y = 8.39e^(-x/9.34) - 10.01, R2 = 0.61;",
            "2.0 A/ps y = 6.45e^(-x/8.44) - 9.36, R2 = 0.42). Provenance: printed equations (exact as printed), not digitized;",
            "drawn over the source image (work/fig15f_overlay.png) they lie on the dashed curves. x = sliding distance (A),",
            "y = Fy (nN); a, b, c, R2 repeated per row. The curves are drawn from x of about 0.5 A to 30 A in the panel.",
        ]:
            f.write("# " + hl + "\n")
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["series", "x_A", "Fy_fit_nN", "a", "b", "c", "R2"])
        wr.writerows(fits)
    with open(WORK / "fig15f_vs_ae.csv", "w", newline="") as f:
        f.write("# Fig. 15f markers vs the Fy markers of Figs. 15a-e at the same sliding distance (both digitized, nN)\n")
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["series", "x_A", "Fy_15f", "Fy_15a_e", "diff", "search", "flag_15f"])
        wr.writerows(cmp_rows)
    # overlay: markers (cyan crosses) and fit curves (thin cyan dots)
    from PIL import Image
    ov = a.copy()
    for x, y in pts:
        xi, yi = int(round(x)), int(round(y))
        ov[yi, max(0, xi - 3):xi + 4] = (0, 200, 255)
        ov[max(0, yi - 3):yi + 4, xi] = (0, 200, 255)
    mx = 1.0 / (inv_x(1.0) - inv_x(0.0))
    for name, colour, shape, wh, step, (A, Bc, C, r2), key in SERIES:
        for xp in np.arange(inv_x(0.5), inv_x(30.0), 1.0):
            xv = float(fx(xp))
            yv = A * np.exp(-xv / Bc) + C
            ypx = float((yv - fy(0.0)) / (fy(1.0) - fy(0.0)))
            if 0 <= ypx < ov.shape[0] and int(xp) % 3 == 0:
                ov[int(round(ypx)), int(round(xp))] = (0, 160, 0)
    Image.fromarray(ov).save(WORK / "fig15f_overlay.png")
    x0, y0, x1, y1 = 1440, 600, 2034, 1035
    Image.fromarray(ov[y0:y1, x0:x1]).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.NEAREST).save(WORK / "fig15f_overlay_zoom.png")
    _ = mx


if __name__ == "__main__":
    main()
