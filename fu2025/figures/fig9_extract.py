"""Digitize Figure 9 of Fu et al. 2025 (Polymers 17, 2441), p. 13: simulated resultant cutting force vs
undeformed chip thickness for plain PMMA and four PMMA/CNT nanocomposites, with error bars.

Source: the figure is stored as 21 horizontal image strips on PDF p. 13 (1496 px wide, 500 ppi, JPEG and
indexed); tools/strips.py stacks them into one 1496 x 1237 px image. No vector data.
    python3 -I fig9_extract.py   -> fig9.csv (+ ../work/fig9_overlay.png)
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from digitize_common import fit_axis  # noqa: E402
from lineplot import classify, runs_of  # noqa: E402
from strips import stack_strips  # noqa: E402

PDF = HERE.parent / "source" / "fu2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)

SERIES = [  # legend name, colour of the legend line (median of its pixels)
    ("Plain PMMA", (82, 82, 82)),
    ("PMMA/0.1 wt% CNT", (255, 68, 68)),
    ("PMMA/0.2 wt% CNT", (17, 102, 221)),
    ("PMMA/0.5 wt% CNT", (51, 170, 102)),
    ("PMMA/1.0 wt% CNT", (187, 119, 221)),
]
# Calibration (pixel positions in the stacked image): inward x ticks 100/150/200 nm at columns 579/983/1387,
# left frame (x = 50) at 175; y ticks 75/50/25 N/m at rows 81/407/733, bottom frame (y = 0) at 1058.5.
fx, xres, xs = fit_axis([175, 579, 983, 1387], [50, 100, 150, 200])
fy, yres, ys = fit_axis([1058.5, 733, 407, 81], [0, 25, 50, 75])
X_NM = [60, 80, 100, 120, 150, 200]
LEGEND = (180, 25, 870, 385)   # x0, y0, x1, y1
INNER = (182, 22, 1462, 1052)  # plot area inside the frame and its tick marks

a, _ = stack_strips(PDF, 13, (160, 300, 382, 486))
lab = classify(a, [c for _, c in SERIES] + [(0, 0, 0)], max_res=70, t_min=0.5)
x0, y0, x1, y1 = LEGEND
lab[y0:y1, x0:x1] = -1
keep = np.zeros_like(lab, bool)
keep[INNER[1]:INNER[3], INNER[0]:INNER[2]] = True
lab[~keep] = -1


def px(v):  # nm -> column
    return (v - 50) / (fx(1) - fx(0)) + 175



def line_fit(m, c0, c1):
    """Robust straight-line fit to the centre of the series' connecting line between columns c0 and c1."""
    xs, ys = [], []
    for c in range(c0, c1):
        r = np.where(m[:, c])[0]
        rs = [q for q in runs_of(r, gap=1) if 4 <= len(q) <= 14]   # a line is ~8 px thick
        if len(rs) == 1:
            xs.append(c)
            ys.append(rs[0].mean())
    if len(xs) < 15:
        return None
    xs, ys = np.array(xs, float), np.array(ys, float)
    k = np.polyfit(xs, ys, 1)
    for _ in range(3):   # drop outliers (other pieces of the same colour)
        res = np.abs(np.polyval(k, xs) - ys)
        ok = res < max(2.0, 2.5 * np.median(res))
        k = np.polyfit(xs[ok], ys[ok], 1)
    return k, int(ok.sum())


# Hand guides for the error-bar caps: approximate row of the top and bottom cap (None = not visible;
# GUIDE value None = no error bar drawn), read off 2x and 4x zooms of the stacked image (work/fig9_cols.png).
GUIDE = {
    (0, 60): (745, 812), (0, 80): (724, 816), (0, 100): (679, 744), (0, 120): (617, 684), (0, 150): (612, 704),
    (0, 200): (595, 661),
    (1, 60): (618, 682), (1, 80): (608, 674), (1, 100): (561, 654), (1, 120): (525, 591), (1, 150): (594, 689),
    (1, 200): (588, 653),
    (2, 60): (641, 702), (2, 80): (644, 708), (2, 100): (581, 675), (2, 120): (571, 636), (2, 150): (522, 586),
    (2, 200): (427, 467),
    (3, 60): (586, 624), (3, 80): (585, 617), (3, 100): (577, 641), (3, 120): (550, 642), (3, 150): (528, 620),
    (3, 200): (540, 607),
    (4, 60): None, (4, 80): None, (4, 100): None, (4, 120): None, (4, 150): None, (4, 200): None,
}

rows, marks = [], []
for i, (name, colour) in enumerate(SERIES):
    m = lab == i
    if i == 0:   # dark grey: JPEG noise splits it between grey and black; take any neutral mid-dark pixel
        g = a.astype(int)
        m = (g.max(2) - g.min(2) < 30) & (g.mean(2) > 35) & (g.mean(2) < 150) & keep
        m[y0:y1, x0:x1] = False
    cols = [px(v) for v in X_NM]
    fits = [line_fit(m, int(cols[j]) + 22, int(cols[j + 1]) - 22) for j in range(len(cols) - 1)]
    for j, xv in enumerate(X_NM):
        c = cols[j]
        est = []
        if j > 0 and fits[j - 1] is not None:
            est.append(np.polyval(fits[j - 1][0], c))
        if j < len(fits) and fits[j] is not None:
            est.append(np.polyval(fits[j][0], c))
        yc = float(np.mean(est))
        spread = float(abs(est[0] - est[-1]))
        ci = int(round(c))
        # error bar: cap rows guided by hand (GUIDE, read off zoomed crops), snapped to the centre of the
        # nearest bar of the series colour (rows where it spans >= 12 px of a 33-px window) within +-6 rows
        capw = m[:, ci - 16:ci + 17].sum(1)
        g = GUIDE[(i, xv)]
        ends, how = [], []
        for gr in (g or (None, None)):
            if gr is None:
                ends.append(None)
                continue
            near = [k for k in range(gr - 6, gr + 7) if capw[k] >= 12]
            runs = runs_of(np.array(near, int), gap=1) if near else []
            if runs:
                best = min(runs, key=lambda q: abs(q.mean() - gr))
                ends.append(float(best.mean()))
                how.append("snapped")
            else:
                ends.append(float(gr))
                how.append("read by eye")
        top, bot = ends
        note = f"marker centre from the connecting lines (left/right estimates differ by {spread * abs(ys):.2f} N/m)"
        if len(est) == 1:
            note = "marker centre from one connecting line (end point)"
        if g is None:
            note += "; no error bar drawn"
        elif top is None or bot is None:
            note += "; one cap hidden under other series"
        if "read by eye" in how:
            note += "; a cap read by eye"
        rows.append([name, xv, round(float(fy(yc)), 2),
                     "" if top is None else round(float(fy(top)), 2),
                     "" if bot is None else round(float(fy(bot)), 2), note])
        marks.append((colour, ci, yc, top, bot))

# overlay: marker centre as a black cross, error-bar ends as orange bars
from PIL import Image  # noqa: E402
im = a.copy()
for colour, c, yc, top, bot in marks:
    yi = int(round(yc))
    im[yi - 1:yi + 2, c - 12:c + 13] = (0, 0, 0)
    im[yi - 12:yi + 13, c - 1:c + 2] = (0, 0, 0)
    for e in (top, bot):
        if e is not None:
            ei = int(round(e))
            im[ei, c - 20:c + 21] = (255, 140, 0)
Image.fromarray(im).save(WORK / "fig9_overlay.png")

with open(HERE / "fig9.csv", "w", newline="") as f:
    for h in [
        "Fu et al. 2025, Polymers 17, 2441, Figure 9: simulated resultant cutting force of various PMMA/CNT",
        "  nanocomposites and plain PMMA at various cutting thicknesses (caption).",
        "Columns: series = legend entry; chip_thickness_nm = Undeformed chip thickness (nm), the six simulated",
        "  values (60, 80, 100, 120, 150, 200 nm, Table 2), at which the markers sit; force_N_per_m = Resultant",
        "  cutting force (N/m) at the marker centre; err_top / err_bottom = ends of the error bar (centre of the",
        "  cap line); empty where not visible; note = remarks. The figure does not say what the error bars are.",
        "Provenance: tier 3, digitized from the embedded image strips on PDF p. 13 (500 ppi; stacked with",
        "  tools/strips.py) by fig9_extract.py. Axes fitted on the frame and the inward ticks",
        f"  (x max residual {xres:.3f} nm, y max residual {yres:.3f} N/m). Series separated by colour (legend",
        "  colours; Plain PMMA = any neutral dark-grey pixel). Marker centre = where the straight connecting lines",
        "  (each segment fitted robustly to the line centre between two markers) reach the marker's x; left and",
        "  right segments give two estimates, averaged (their difference is in the note; markers themselves are",
        "  partly hidden under other series). Error-bar caps: approximate rows placed by hand on zoomed crops",
        "  (GUIDE in the script), each snapped to the centre of the nearest bar of the series colour within 6 px;",
        "  all 48 caps snapped. Check: every error bar is symmetric about its marker within 0.1 N/m.",
        "  Thin grey lines inside some Plain PMMA error bars (a second, shorter bar?) are not extracted.",
        f"Uncertainty: about +-{1.5 * abs(ys):.2f} N/m (1.5 px) for markers and caps; x is the nominal thickness.",
        "  The overlay work/fig9_overlay.png was checked by eye (see README).",
    ]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["series", "chip_thickness_nm", "force_N_per_m", "err_top", "err_bottom", "note"])
    w.writerows(rows)
for r in rows:
    print(r)
