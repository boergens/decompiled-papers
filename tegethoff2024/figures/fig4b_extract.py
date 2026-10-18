"""Digitize Figure 4B of Tegethoff & Briggman 2024 (PDF p.6): raw signals of the two force sensors S1, S2.

Source: the embedded JPEG of Figure 4 (1917 x 1248 px, ~310 ppi), panel B at top centre.
    python3 -I fig4b_extract.py   -> fig4b.csv (+ ../work/fig4b_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(6)
fy, ry, sy = fit_axis([14.0, 60.0, 106.5, 153.0, 245.5, 292.0, 338.0, 384.5], [20, 15, 10, 5, -5, -10, -15, -20])
fx, rx, sx = fit_axis([642.5, 878.0, 937.0, 1113.0], [0, 0.8, 1.0, 1.6])
g, s = gray(a), sat(a)
S1 = (g < 85) & (s < 40)
S2 = (g > 110) & (g < 200) & (s < 25)
for m in (S1, S2):
    m[:, :648] = False          # y axis and its ticks
    m[378:, :] = False          # x axis and its ticks
rows, pts = traces({"S1": S1, "S2": S2}, 649, 1112, 5, 378, fx, fy)
overlay(a, pts, os.path.join(WORK, "fig4b_overlay.png"))
write_csv(os.path.join(HERE, "fig4b.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 4B: raw signals from the force sensors S1 (black) and",
    "  S2 (grey) during a section from a diamond shaped resin block.",
    "Columns: series (S1, S2); time_s = x (axis 'time (sec)'); signal_mV_mid = centre of the drawn trace in this pixel",
    "  column; signal_mV_top / signal_mV_bottom = upper and lower edge of the drawn trace in the column (line width plus",
    "  the trace's own noise). One row per pixel column (~0.0034 s); columns where a trace is hidden under the other",
    "  (where they cross, ~0.27 s and ~1.2 s) may be missing or follow the other trace briefly.",
    "Provenance: tier 3, digitized from the embedded ~310 ppi JPEG (no vector data in the PDF) by fig4b_extract.py;",
    f"  y calibrated on 8 ticks -20..20 mV (max residual {ry:.3f} mV), x on ticks 0, 0.8, 1.0, 1.6 s (max residual {rx:.4f} s).",
    f"Uncertainty: +-{2 * abs(sy):.2f} mV and +-{2 * abs(sx):.4f} s (2 px), plus the trace width.",
], ["series", "time_s", "signal_mV_mid", "signal_mV_top", "signal_mV_bottom"], rows)
print(len(rows), "rows", {k: sum(1 for r in rows if r[0] == k) for k in ("S1", "S2")}, "res", ry, rx)
