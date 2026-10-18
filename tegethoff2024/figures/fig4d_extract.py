"""Digitize Figure 4D (main plot) of Tegethoff & Briggman 2024 (PDF p.6): sectional force over a 15 min session.

Source: the embedded JPEG of Figure 4 (1917 x 1248 px, ~310 ppi), panel D at lower left.
The trace (~250 cuts in 900 s) is far denser than the pixel grid, so per pixel column (~1.45 s) only the range of the
drawn trace can be recovered: its maximum (top of the blue in the column) and minimum (bottom).
    python3 -I fig4d_extract.py   -> fig4d.csv (+ ../work/fig4d_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

a = img(6)
fy, ry, sy = fit_axis([707.5, 1056.5, 1126.5], [60, -40, -60])
fx, rx, sx = fit_axis([88.5, 157.5, 226.5, 295.5, 364.0, 432.5, 501.5, 570.5, 639.5],
                      [0, 100, 200, 300, 400, 500, 600, 700, 800])
blue = classify(a, [(30, 105, 175), (110, 160, 205)], max_dist=60, min_sat=40) >= 0
blue[:, :91] = False
blue[1122:, :] = False
rows, pts = [], []
for c in range(91, 708):
    r = np.where(blue[600:1122, c])[0]
    if len(r) == 0:
        continue
    top, bot = 600 + r.min(), 600 + r.max()
    rows.append((float(fx(c)), float(fy(top)), float(fy(bot)), len(r)))
    pts += [(c, top), (c, bot)]
overlay(a, pts, os.path.join(WORK, "fig4d_overlay.png"))
write_csv(os.path.join(HERE, "fig4d.csv"), [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 4D (main plot): sectional forces from a 15 min long",
    "  sectioning session (blue trace).",
    "Columns: time_s = x (axis 'time (sec)', centre of the pixel column, ~1.45 s wide); force_max / force_min = the highest",
    "  and lowest point of the drawn trace in the column, mN/mm (the trace has ~250 cuts and cannot be resolved into",
    "  single cuts at this resolution; this is its envelope); blue_px = number of blue pixels in the column.",
    "The grey rectangle around ~265-350 s marks the part magnified in the inset (the inset has no axes; not digitized).",
    "Provenance: tier 3, digitized from the embedded ~310 ppi JPEG (no vector data in the PDF) by fig4d_extract.py;",
    f"  y calibrated on the ticks at 60, -40 and -60 mN/mm (labels 80 to -60; the trace hides the other ticks; max residual",
    f"  {ry:.3f}), x on 9 ticks 0-800 s (max residual {rx:.3f} s); the axis ends at 900 s.",
    f"Uncertainty: +-{2 * abs(sy):.1f} mN/mm (2 px; thin isolated spikes may be lost to JPEG blur) and +-{abs(sx):.1f} s.",
], ["time_s", "force_max", "force_min", "blue_px"], rows)
print(len(rows), "columns; res", ry, rx, "max", max(r[1] for r in rows), "min", min(r[2] for r in rows))
