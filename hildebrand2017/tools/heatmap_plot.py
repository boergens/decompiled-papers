"""Re-plot a heatmap grid CSV (tools/heatmap_grid.py format) with the blue-green 'winter' map, black = empty."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from heatmap_grid import read_grid  # noqa: E402


def plot(csv_path, out_png, vmax, unit, label, xticks, size=(8, 1.3), ylabel="pairs"):
    slices, pidx, vals = read_grid(csv_path)
    cmap = plt.get_cmap("winter").copy()
    cmap.set_bad("k")
    fig, ax = plt.subplots(figsize=size)
    ds = (slices[-1] - slices[0]) / (len(slices) - 1)
    im = ax.imshow(np.ma.masked_invalid(vals), cmap=cmap, vmin=0, vmax=vmax, aspect="auto", interpolation="nearest",
                   extent=[slices[0] - ds / 2, slices[-1] + ds / 2, pidx.max() + 0.5, 0.5])
    ax.set_xticks(xticks)
    ax.set_yticks([])
    ax.set_ylabel(ylabel, fontsize=7)
    ax.set_xlabel("position in series, slice", fontsize=7)
    ax.set_title(label, fontsize=8, loc="left")
    cb = fig.colorbar(im, ticks=[0, vmax], pad=0.01)
    cb.ax.set_yticklabels(["0", f"{vmax:g}{unit}"])
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
