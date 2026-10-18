"""Re-plot Extended Data Fig. 9h from edfig9h_a.csv and edfig9h_d.csv -> edfig9h_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from heatmap_grid import read_grid  # noqa: E402

cmap = plt.get_cmap("winter").copy()
cmap.set_bad("k")
fig, axes = plt.subplots(2, 1, figsize=(4, 3), sharex=True)
for ax, (name, vmax, lab) in zip(axes, (("a", 180, "180°"), ("d", 8, "8 µm"))):
    s, p, v = read_grid(HERE / f"edfig9h_{name}.csv")
    ds = (s[-1] - s[0]) / (len(s) - 1)
    im = ax.imshow(np.ma.masked_invalid(v), cmap=cmap, vmin=0, vmax=vmax, aspect="auto", interpolation="nearest",
                   extent=[s[0] - ds / 2, s[-1] + ds / 2, 15.5, 0.5])
    ax.set_yticks([])
    ax.set_ylabel(name, style="italic")
    cb = fig.colorbar(im, ax=ax, ticks=[0, vmax], pad=0.01)
    cb.ax.set_yticklabels(["0", lab])
axes[0].set_title("concatenation of linearized difference matrices", fontsize=8)
axes[1].set_xticks([5013, 8013])
axes[1].set_xlabel("position in series, slice", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "edfig9h_replot.png", dpi=150)
