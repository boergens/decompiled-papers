"""Digitize Figure 2C of Tegethoff & Briggman 2024 (PDF p.5): EMbed 812 MH hardness vs BDMA concentration.

Source: the embedded JPEG of Figure 2 (994 x 1914 px, ~349 ppi), panel C in its lower part.
    python3 -I fig2c_extract.py   -> fig2c.csv (+ ../work/fig2c_overlay.png)

The y tick LABELS of this panel do not sit on its tick marks (see README): the labels 12, 11, 10, 9 are
~120 px apart, the tick marks/grid lines ~52 px. Primary calibration: the ticks, taken as 0.5 HV apart (as in
panel B, which has the same plot height), with the tick under the label "10" (the only label centred on a
tick, within 1 px) = 10 HV. Alternative: a fit on the four label centres; given as hardness_HV_labelfit.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(5)
YT = [1334.5, 1387.0, 1439.0, 1491.0, 1543.0, 1596.0, 1648.0, 1700.0, 1752.0, 1804.0]
YV = [12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8]
fy, ry, sy = fit_axis(YT, YV)
LBL_ROWS = [1354.5, 1476.0, 1594.5, 1715.5]   # vertical centres of the printed labels 12, 11, 10, 9
fy2, ry2, sy2 = fit_axis(LBL_ROWS, [12, 11, 10, 9])
XT = [260.0, 414.0, 567.0, 720.0, 873.5]
fx, rx, sx = fit_axis(XT, [1.0, 2.0, 3.0, 4.0, 5.0])
BOX = (110, 1320, 990, 1800)
m = gray(a) < 100
rows, pts = dot_rows({"EMbed 812 MH": m}, BOX, fx, fy, single_area=24, min_area=10)
out = [(r[1], r[2], float(fy2(r[4])), r[5]) for r in sorted(rows, key=lambda r: (r[1], r[2]))]
save(mark(a, pts), "fig2c_overlay.png")
write_csv(os.path.join(HERE, "fig2c.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 2C: hardness of EMbed 812 MH cured with different",
    "  concentrations of the accelerator BDMA (black dots).",
    "Columns: bdma_percent = x position (numeric axis, ticks 1.0-5.0; one group of dots lies between 2.0 and 3.0, at ~2.3,",
    "  without a tick); hardness_HV = Vickers hardness from the tick-mark calibration (primary, see below);",
    "  hardness_HV_labelfit = the same dot read with the alternative calibration on the printed tick labels;",
    "  n_in_blob = markers in the merged blob this point was split from (1 = isolated; >1 = split with k-means).",
    "CALIBRATION PROBLEM IN THE SOURCE: the y labels 12, 11, 10, 9 are ~120 px apart but the tick marks and grid lines",
    "  are ~52 px apart, so labels and ticks disagree. Primary: ticks taken as 0.5 HV apart (as in panel B of the same",
    "  height), the tick under the label '10' (the only label centred on a tick) = 10 HV; axis 8 to 12.5 HV.",
    "  Support for the primary: with it, 48 of the 50 dots fall within +-0.02 HV of a multiple of 0.1 HV (the other two, at",
    "  1.0 %, sit diagonally beside a third dot at ~9.0 HV and are within 0.05); the dots of panel B, calibrated on its own",
    "  consistent ticks and labels, are on the same 0.1 HV grid; with the label fit the panel-C dots are not.",
    f"  Alternative (label centres fitted, max residual {ry2:.3f} HV) differs from the primary by up to ~0.3 HV.",
    "Provenance: tier 3, digitized from the embedded ~349 ppi JPEG (no vector data in the PDF) by fig2c_extract.py.",
    f"Uncertainty: +-{2 * abs(sy):.2f} HV (2 px) for isolated markers, plus the calibration ambiguity above;",
    f"  x +-{2 * abs(sx):.3f} %. Fully overlapping markers cannot be seen; counts are lower limits.",
], ["bdma_percent", "hardness_HV", "hardness_HV_labelfit", "n_in_blob"], out)
print(len(out), "points; residuals", ry, ry2, "x", rx)
