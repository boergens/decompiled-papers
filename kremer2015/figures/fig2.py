"""Re-plot Fig. 2's length-scale axis and pins from fig2.csv -> fig2_replot.png.

Run from anywhere: python3 -I -B figures/fig2.py
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(l for l in open(HERE / "fig2.csv") if not l.startswith("#")))
ticks = [r for r in rows if r["kind"] == "tick"]
pins = [r for r in rows if r["kind"] == "pin"]

fig, ax = plt.subplots(figsize=(8, 2.6))
ax.axhline(0, color="k", lw=1.5)
for t in ticks:
    x = float(t["log10_length_m"])
    ax.plot([x, x], [-0.08, 0.08], color="k", lw=1)
    ax.text(x, 0.14, t["label"].replace("10^", "10$^{").replace(" m", "}$m"), ha="center", fontsize=9)
for p in pins:
    x = float(p["log10_length_m"])
    depth = (float(p["pin_bottom_y_px"]) - 548) / 100.0
    ax.plot([x, x], [0, -depth], color="k", lw=1)
    ax.plot([x], [0], "ko", ms=4)
    ax.plot([x], [-depth], "ko", ms=4)
    ax.text(x, -depth - 0.12, f"pin {p['index']}\n{x:.2f}", ha="center", va="top", fontsize=7)
ax.set_xlim(-1.4, -9.7)   # decreasing to the right, as printed
ax.set_ylim(-2.4, 0.4)
ax.set_xlabel("log10(length / m)   (axis decreasing to the right, as in the figure)")
ax.set_yticks([])
for s in ("left", "right", "top"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "fig2_replot.png", dpi=150)
