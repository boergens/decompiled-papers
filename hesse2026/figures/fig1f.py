"""Redraw Figure 1f (ML and AM response heatmaps, cells x 96 stimuli) from the matrix CSVs and the colourbar CSV.
Run from inside figures/:  python3 fig1f.py  ->  fig1f_replot.png
The stimulus thumbnail strip (fig1f_stimuli.png, an embedded raster) is placed below each heatmap if present."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

cb = pd.read_csv("fig1f_colourbar.csv", comment="#")
cmap = ListedColormap((cb[["r", "g", "b"]].values / 255.0)[::-1])   # CSV level 0 is the +1 end -> reverse for -1..1
PANELS = [("fig1f_ML.csv", "ML", "145 visual cells"), ("fig1f_AM.csv", "AM", "215 visual cells")]
strip = plt.imread("fig1f_stimuli.png") if os.path.exists("fig1f_stimuli.png") else None

fig = plt.figure(figsize=(7.0, 3.2), dpi=200)
gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 0.05], height_ratios=[4.4, 1], hspace=0.08, wspace=0.25,
                      left=0.07, right=0.88, top=0.92, bottom=0.08)
for j, (csv, title, ylabel) in enumerate(PANELS):
    M = pd.read_csv(csv, comment="#").iloc[:, 1:].values.astype(float)
    ax = fig.add_subplot(gs[0, j])
    im = ax.imshow(M, cmap=cmap, vmin=-1, vmax=1, aspect="auto", interpolation="nearest", extent=(0, 96, M.shape[0], 0))
    ax.set_title(title, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_xticks(range(0, 96, 16)); ax.set_xticklabels([]); ax.set_yticks([])
    ax.tick_params(length=2)
    axs = fig.add_subplot(gs[1, j])
    if strip is not None:
        axs.imshow(strip, aspect="auto")
    axs.set_xticks([]); axs.set_yticks([])
    for s in axs.spines.values(): s.set_visible(False)
    axs.set_xlabel("96 stimuli", fontsize=8)
cax = fig.add_subplot(gs[0, 2])
cbar = fig.colorbar(im, cax=cax, ticks=[-1, 1])
cbar.set_label("Response (norm.)", fontsize=8); cbar.ax.tick_params(labelsize=8)
fig.savefig("fig1f_replot.png")
