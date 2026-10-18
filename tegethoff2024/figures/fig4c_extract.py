"""Digitize Figure 4C of Tegethoff & Briggman 2024 (PDF p.6): sectional (F_S) and transverse (F_T) force profiles
for sections cut at 50 and 35 nm.

Source: the embedded JPEG of Figure 4 (1917 x 1248 px, ~310 ppi), panel C at top right.
    python3 -I fig4c_extract.py   -> fig4c.csv (+ ../work/fig4c_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(6)
fy, ry, sy = fit_axis([62.5, 108.5, 154.0, 200.0, 246.0, 292.0, 383.5], [60, 50, 40, 30, 20, 10, -10])
fx, rx, sx = fit_axis([1328.0, 1386.5, 1445.0, 1502.5, 1561.5, 1619.5, 1677.5, 1735.5, 1794.0],
                      [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
NAMES = ["F_S 50 nm", "F_S 35 nm", "F_T 50 nm", "F_T 35 nm"]
PAL = [(30, 105, 175), (110, 185, 220), (165, 30, 45), (210, 85, 25)]   # sampled from the legend and the traces
lab = classify(a, PAL, max_dist=40, min_sat=50)
masks = {n: lab == i for i, n in enumerate(NAMES)}
for m in masks.values():
    m[:, :1333] = False
    m[378:, :] = False
    m[:170, 1740:] = False      # legend
rows, pts = traces(masks, 1333, 1793, 5, 378, fx, fy)
overlay(a, pts, os.path.join(WORK, "fig4c_overlay.png"))
write_csv(os.path.join(HERE, "fig4c.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 4C: representative sectional (F_S) and transverse (F_T)",
    "  forces for sections cut at 35 and 50 nm. Legend: F_S 50 nm (dark blue), F_S 35 nm (light blue), F_T 50 nm (dark red),",
    "  F_T 35 nm (orange).",
    "Columns: series; time_s = x (axis 'time (sec)'); force_mN_per_mm_mid = centre of the drawn trace in the pixel column;",
    "  _top/_bottom = upper and lower edge of the drawn trace in the column (line width plus the trace's noise).",
    "  One row per pixel column (~0.0035 s). The traces overlap: the two F_T traces lie on top of each other for most of",
    "  the cut (orange drawn over dark red) and the two F_S traces share their rising and falling ramps, so where a trace",
    "  is hidden its column is missing or holds the visible edge of the band only.",
    "Provenance: tier 3, digitized from the embedded ~310 ppi JPEG (no vector data in the PDF) by fig4c_extract.py;",
    "  series separated by nearest colour (Lab) to the four colours sampled from the figure;",
    f"  y calibrated on 7 ticks -10..60 mN/mm (max residual {ry:.3f}), x on 9 ticks 0-1.6 s (max residual {rx:.4f} s).",
    f"Uncertainty: +-{2 * abs(sy):.2f} mN/mm and +-{2 * abs(sx):.4f} s (2 px), plus the trace width.",
], ["series", "time_s", "force_mN_per_mm_mid", "force_mN_per_mm_top", "force_mN_per_mm_bottom"], rows)
print({k: sum(1 for r in rows if r[0] == k) for k in NAMES}, "res", ry, rx)
