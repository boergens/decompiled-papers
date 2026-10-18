"""Re-plot Figure 2a of Templier 2019 (eLife 8:e45696) from fig2a.csv -> fig2a_replot.png

Four similarity matrices (1, 2: EM imagery; 3, 4: beads imagery; 1, 3 before and 2, 4 after reordering),
grey level as printed, axes in cell index with ticks every 50 (labels 0, 100, 200) on top and left.
Cells flagged 'red_line' (matrix 4) are drawn red; cells hidden by the printed panel numbers pale blue.
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig2a.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
N = 1 + max(int(r["row"]) for r in rows)
img = {m: np.ones((N, N, 3)) for m in (1, 2, 3, 4)}
for r in rows:
    m, i, j = int(r["matrix"]), int(r["row"]), int(r["col"])
    if r["flag"] == "red_line":
        img[m][i, j] = (1.0, 0.3, 0.3)
    elif r["flag"] == "panel_label":
        img[m][i, j] = (0.75, 0.85, 1.0)        # hidden under the printed panel number
    else:
        img[m][i, j] = float(r["grey"]) / 255

fig, axes = plt.subplots(2, 2, figsize=(4.6, 4.8))
for ax, m in zip(axes.ravel(), (1, 2, 3, 4)):
    ax.imshow(img[m], interpolation="nearest", extent=(-0.5, N - 0.5, N - 0.5, -0.5))
    ax.set_xticks(range(0, 201, 50))
    ax.set_yticks(range(0, 201, 50))
    ax.set_xticklabels(["0", "", "100", "", "200"] if m in (1, 2) else [])
    ax.set_yticklabels(["0", "", "100", "", "200"] if m in (1, 3) else [])
    ax.xaxis.tick_top()
    ax.text(0.95, 0.95, str(m), transform=ax.transAxes, ha="right", va="top", fontsize=14)
axes[0, 0].set_ylabel("EM", fontsize=13)
axes[1, 0].set_ylabel("Beads", fontsize=13)
fig.text(0.55, 0.02, "Similarity matrices", ha="center", fontsize=12)
fig.text(0.02, 0.95, "a", fontsize=20)
fig.subplots_adjust(left=0.17, right=0.97, top=0.92, bottom=0.07, wspace=0.08, hspace=0.06)
fig.savefig(os.path.join(HERE, "fig2a_replot.png"), dpi=200)
print("fig2a_replot.png")
