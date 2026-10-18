"""Digitize Fig. 9a and 9b of Bouwer et al. 2016 (PDF p. 11): envelopes of the BSE (blue) and SE (green)
trajectory fans, height vs lateral distance.

Source: the embedded raster image of Fig. 9 (1955 x 804 px, 300 ppi, RGB) in source/bouwer2016.pdf.
No vector plot paths in the PDF, so tier 3 (digitized). The panels show thousands of trajectories drawn as
dots; single trajectories cannot be separated, so the CSV gives, for every pixel row (height), the leftmost
and rightmost blue and green pixel: the outer edges of the BSE and SE fans.
    python3 -I -B figures/fig9_extract.py   -> figures/fig9a.csv, figures/fig9b.csv (+ work/fig9*_overlay.png)
Axis calibration: tick marks on the x axis (-10..10 mm, every 2 mm; the 0 tick is hidden under the fans) and
on the y axis (1..6 mm) plus the x axis line (0 mm), fitted per panel.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, write_csv, overlay  # noqa: E402

PDF = HERE.parent / "source" / "bouwer2016.pdf"
a = embedded_image(str(PDF), 11, bbox_near=(63.4, 95.0, 532.6, 287.9))
ai = a.astype(int)
R, G, B = ai[:, :, 0], ai[:, :, 1], ai[:, :, 2]
k = ai.max(2) < 100
blue = (B > 180) & (R < 190) & (G < 190) & (B - R > 60)
green = (G > 180) & (G - R > 40) & (G - B > 40)

# x axis line rows and y axis line columns
axis_row = float(np.mean([r for r in range(a.shape[0]) if k[r].sum() > 1000]))
ycols = [c for c in range(a.shape[1]) if k[60:722, c].sum() > 400]
ycols = np.split(np.array(ycols), np.where(np.diff(ycols) > 1)[0] + 1)
panels = {"a": (int(ycols[0][-1]) + 1, 1000), "b": (int(ycols[1][-1]) + 1, a.shape[1])}


def groups(idx):
    idx = np.asarray(idx)
    if len(idx) == 0:
        return []
    return [float(np.mean(g)) for g in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)]


for name, (x0, x1) in panels.items():
    yaxis = x0 - 1
    # x ticks: short vertical dark marks just above the axis line (rows axis-8 .. axis-2)
    band = k[int(axis_row) - 8:int(axis_row) - 2, yaxis - 3:x1].mean(0) >= 0.8
    xt = [yaxis - 3 + c for c in groups(np.where(band)[0])]
    # the y axis line itself is the -10 tick
    xt = [c for c in xt if c > yaxis + 3]
    xvals = [-10] + [v for v in (-8, -6, -4, -2, 2, 4, 6, 8, 10)]
    assert len(xt) == 9, (name, xt)
    fx, xres, xs = fit_axis([yaxis - 0.5] + xt, xvals)
    yband = k[60:int(axis_row) - 3, yaxis + 1:yaxis + 6].mean(1) >= 0.8
    yt = [60 + r for r in groups(np.where(yband)[0])]
    assert len(yt) == 6, (name, yt)
    fy, yres, ysl = fit_axis(yt[::-1] + [axis_row], [1, 2, 3, 4, 5, 6, 0])
    rows, pts = [], []
    W = 2   # the outer trajectories are dotted: take the extreme pixel over rows r-W..r+W
    for r in range(0, int(axis_row) - 1):
        if not (blue[r, x0 + 2:x1].any() or green[r, x0 + 2:x1].any()):
            continue
        lo, hi = max(0, r - W), min(int(axis_row) - 1, r + W + 1)
        bl = np.where(blue[lo:hi, x0 + 2:x1].any(0))[0] + x0 + 2
        gr = np.where(green[lo:hi, x0 + 2:x1].any(0))[0] + x0 + 2
        if len(bl) == 0 and len(gr) == 0:
            continue
        row = [float(fy(r))]
        for m in (bl, gr):
            if len(m):
                row += [float(fx(m.min())), float(fx(m.max()))]
                pts += [(m.min(), r), (m.max(), r)]
            else:
                row += [np.nan, np.nan]
        rows.append(row)
    rows.sort()
    overlay(a, pts, str(HERE.parent / "work" / f"fig9{name}_overlay.png"))
    desc = {"a": "3-keV gun-accelerating voltage, -1.5-keV decelerating potential, 1.5-keV landing energy",
            "b": "4.5-keV gun-accelerating voltage, -3-keV decelerating potential, 1.5-keV landing energy"}[name]
    write_csv(str(HERE / f"fig9{name}.csv"), [
        f"Bouwer et al. 2016 Adv Struct Chem Imag 2:11, Fig. 9{name}: 'Electron Trajectories with Applied Deceleration'",
        f"  ({desc}, per the caption). BSE trajectories blue, SE trajectories green.",
        "Columns: height_mm = Height (mm), y axis, one row per source pixel row; bse_left_mm/bse_right_mm = Distance (mm)",
        "  of the leftmost/rightmost blue pixel within +-2 pixel rows of that row (the outermost trajectories are drawn",
        "  as dots with gaps, so a single row can miss them); this is the outer edge of the BSE fan; se_left_mm/se_right_mm = the",
        "  same for the green pixels (SE fan). Where green is drawn over blue the blue fan's inner edge is hidden, so only",
        "  the outer edges are given. Empty = no pixel of that colour in the row.",
        "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig9_extract.py.",
        f"  x fitted on the y-axis line (-10 mm) and 9 tick marks (-8..10 mm), max residual {xres:.3f} mm; y fitted on",
        f"  the x-axis line (0 mm) and 6 tick marks (1..6 mm), max residual {yres:.3f} mm.",
        f"Uncertainty: about +-{abs(xs):.3f} mm in x and +-{abs(ysl):.3f} mm in y (1 source pixel); the outer blue",
        "  trajectories are drawn as sparse dots, so near the top of the fan the edge can be off by a few pixels more.",
    ], ["height_mm", "bse_left_mm", "bse_right_mm", "se_left_mm", "se_right_mm"], rows, fmt="{:.3f}")
    top = rows[-1]
    print(name, len(rows), "rows; residuals", xres, yres, "top row", [round(v, 2) for v in top],
          "row at 1 mm", [round(v, 2) for v in min(rows, key=lambda q: abs(q[0] - 1))])
