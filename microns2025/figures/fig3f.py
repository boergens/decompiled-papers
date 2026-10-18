#!/usr/bin/env python3
"""Re-plot Fig. 3f from fig3f.csv -> fig3f_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("fig3f.csv"))
grid = {}
for a in r:
    grid.setdefault((int(a["oracle_percentile"]), int(a["clip"])), np.zeros((10, 62)))[int(a["repeat"]) - 1, int(a["time_bin"]) - 1] = float(a["darkness"])
fig, axs = plt.subplots(3, 6, figsize=(6, 3.3))
for i, p in enumerate([100, 79, 34]):
    for j in range(6):
        ax = axs[i, j]
        ax.imshow(grid[(p, j + 1)], cmap="Greys", vmin=0, vmax=1, aspect="auto", interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
        if i == 0:
            ax.set_title(f"Oracle clip\n{j + 1}", fontsize=7)
    axs[i, 5].text(70, 5, str(p), fontsize=7, va="center")
axs[2, 0].set_ylabel("Repeats", fontsize=7)
fig.text(0.95, 0.9, "Oracle\npercentile", fontsize=7, ha="center")
fig.subplots_adjust(right=0.88, wspace=0.08, hspace=0.25)
fig.savefig(Path(__file__).with_name("fig3f_replot.png"), dpi=150)
