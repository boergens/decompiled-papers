#!/usr/bin/env python3
"""Re-plot scheffer2020 Figure 5B from fig5b.csv (dots drawn as circles of the digitized radius in data units)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(l for l in open(HERE / "fig5b.csv") if not l.startswith("#")))
PX = 0.1 / 98.6  # data units per source pixel (mean of x and y scale, see CSV header)
fig, ax = plt.subplots(figsize=(5, 5))
color = "tab:blue"
for r in sorted(rows, key=lambda r: -float(r["r_px"])):  # large dots first (draw order in the original is unknown)
    c = "tab:purple" if r["kind"] == "human_reference" else color
    z = 3 if r["kind"] == "human_reference" else 2
    ax.add_patch(Circle((float(r["recall"]), float(r["precision"])), float(r["r_px"]) * PX, facecolor=c,
                        edgecolor="white", linewidth=0.8, zorder=z))
ax.set_xlim(0.5, 1.02)
ax.set_ylim(0.5, 1.02)
ax.set_aspect("equal")
ax.grid(True)
ax.set_xlabel("recall")
ax.set_ylabel("precision")
ax.text(0.52, 0.98, "B", fontsize=16, va="top")
fig.tight_layout()
fig.savefig(HERE / "fig5b_replot.png", dpi=150)
