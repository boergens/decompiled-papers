"""Digitize Figure 7 of Fu et al. 2025 (Polymers 17, 2441), p. 11: resultant cutting force vs time,
(a) experimental and (b) simulated, plain PMMA, six undeformed chip thicknesses.

Source: the embedded raster image on PDF p. 11 (1427 x 554 px JPEG, 300 ppi; no vector data).
    python3 -I fig7_extract.py   -> fig7a.csv, fig7b.csv (+ ../work/fig7{a,b}_overlay.png)
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from digitize_common import embedded_image, fit_axis  # noqa: E402
from lineplot import classify, trace_all, overlay_series, overlay_grid  # noqa: E402

PDF = HERE.parent / "source" / "fu2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)

SERIES = [  # (name as in the legend, reference colour)
    ("60nm", (0, 0, 0)),
    ("80nm", (255, 0, 0)),
    ("100nm", (0, 0, 255)),
    ("120nm", (255, 0, 255)),
    ("150nm", (0, 128, 0)),
    ("200nm", (0, 0, 128)),
]

# Axis calibration, pixel positions of the frame lines and tick marks found in the image
# (frame_lines / tick scan on the dark mask, see README):
PANELS = {
    "a": dict(
        frame=(115, 29, 706, 468),            # inner edge of the frame: left, top, right, bottom (px)
        xt=([114, 260.5, 407, 554, 700], [0, 200, 400, 600, 800]),
        yt=([469, 322, 175, 27.5], [0, 20, 40, 60]),
        legend=[(275, 25, 705, 205)],         # x0, y0, x1, y1 boxes excluded (legend)
        title="(a) experimental cutting force of plain PMMA",
        core=None,                            # thin lines (about 2 px): no erosion test
    ),
    "b": dict(
        frame=(824, 37, 1420, 479),
        xt=([823, 969, 1115, 1261.5, 1407], [0, 200, 400, 600, 800]),
        yt=([480, 369, 258, 147, 36], [0, 20, 40, 60, 80]),
        legend=[(826, 38, 1419, 112)],
        title="(b) simulated cutting force of plain PMMA",
        core=2,
    ),
}

a = embedded_image(str(PDF), 11)
labels = classify(a, [c for _, c in SERIES], blue_split=(2, 5, 160), black_navy=(0, 5, 30))
for key, P in PANELS.items():
    fx, xres, xs = fit_axis(*P["xt"])
    fy, yres, ys = fit_axis(*P["yt"])
    L, T, R, B = P["frame"]
    lab = labels.copy()
    for (x0, y0, x1, y1) in P["legend"]:
        lab[y0:y1, x0:x1] = -1
    m = 3  # skip the frame lines and the inward tick marks next to them
    rows, traces = [], []
    for i, (name, _) in enumerate(SERIES):
        mask = lab == i
        if name == "60nm":   # black: also drop the tick marks along the frame
            mask[:, :L + 8] = False
            mask[B - 8:, :] = False
        tr = trace_all(mask, L + m, R - 8, T + 8, B - 1, core=P["core"])
        traces.append((SERIES[i][1], tr))
        for c, ym, yt, yb in tr:
            rows.append([f"undeformed chip thickness {name}", round(float(fx(c)), 2), round(float(fy(ym)), 3),
                         round(float(fy(yt)), 3), round(float(fy(yb)), 3)])
    overlay_series(a, traces, str(WORK / f"fig7{key}_overlay.png"), box=(L - 30, T - 10, R + 10, B + 10))
    overlay_grid(a, traces, str(WORK / f"fig7{key}_series.png"), box=(L - 5, T - 5, R + 5, B + 5))
    with open(HERE / f"fig7{key}.csv", "w", newline="") as f:
        for h in [
            f"Fu et al. 2025, Polymers 17, 2441, Figure 7{P['title'][:3]} {P['title'][4:]}, at 1 mm/s (caption).",
            "Columns: series = legend entry; time_us = Time (µs) of the pixel column; force_N_per_m = Resultant cutting",
            "  force (N/m) at the centre of a run of the series' pixels in that column; force_upper / force_lower = top",
            "  and bottom of the run (about half a line width from the centre on flat parts; on steep or vertical",
            "  segments a single column covers the whole rise or drop). A column can have SEVERAL rows for one series",
            "  (the line passing the column more than once, or a spike next to a flat part): rows are runs, not a",
            "  function of time. The replot draws runs as vertical strokes and does not connect them.",
            "Provenance: tier 3, digitized from the embedded 300 ppi JPEG image (PDF p. 11) by fig7_extract.py.",
            f"  Axes fitted on the tick marks (x: 0-800 µs, max residual {xres:.2f} µs; y: max residual {yres:.3f} N/m).",
            "  Pixels are assigned to a series by colour (legend colours black, red, blue, magenta, green, navy; a",
            "  pixel is matched as a blend of a series colour with white, tools/lineplot.py; saturated blue pixels are",
            "  split between blue and navy at blue channel 160; 'black' pixels with blue > max(red, green) + 30 are",
            "  navy edges); connected pieces smaller",
            "  than 12 px (panel b: or with < 10 px left after a 2x2 erosion) are dropped as specks/slivers. Where a series is hidden under another line its columns are missing",
            "  (gaps in time_us). The legend area and an 8 px band inside the frame (tick marks) are excluded. Where",
            "  lines cross or run together, the colour drawn on top wins and blue/navy/black edges are close in colour,",
            "  so a few runs may belong to a neighbouring series (see work/fig7*_series.png and the replot).",
            f"Uncertainty: about +-{1.5 * abs(xs):.1f} µs in x and +-{1.5 * abs(ys):.2f} N/m in y (1.5 px), plus the",
            "  line width (see force_upper/force_lower).",
        ]:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(["series", "time_us", "force_N_per_m", "force_upper", "force_lower"])
        w.writerows(rows)
    print(key, len(rows), "rows; residuals", xres, yres)
