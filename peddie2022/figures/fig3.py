#!/usr/bin/env python3
"""Re-plot Figure 3 (region outlines, resolution vs target volume) from fig3.csv -> fig3_replot.png."""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig3.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
polys = defaultdict(list)
for r in rows:
    polys[r["region"]].append((float(r["x_log10_nm"]), float(r["y_tickpos"])))
colours = {"ET, ssET": "#6794c2", "FIB-SEM": "#6ac1b9", "SBF-SEM, AT, ssTEM": "#cbe2b5",
           "X-ray microscopy": "#fdf269", "Emerging vEM technologies": "#e48b8a"}
fig, ax = plt.subplots(figsize=(7, 5))
for reg, pts in polys.items():
    ax.add_patch(Polygon(pts, closed=True, facecolor=colours[reg], alpha=0.6, edgecolor="k", lw=0.8))
    xs, ys = zip(*pts)
    ax.text(sum(xs) / len(xs), sum(ys) / len(ys), reg, ha="center", va="center", fontsize=9)
ax.set_xlim(1.65, 7.5)
ax.set_ylim(-0.2, 5.4)
ax.set_xticks([2, 3, 4, 5, 6], ["100 nm", "1 µm", "10 µm", "100 µm", "1 mm"])
ax.set_yticks(range(6), ["1", "5", "10", "50", "100", "1000"])
ax.set_xlabel("Target volume")
ax.set_ylabel("Resolution (nm)")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "fig3_replot.png", dpi=150)
