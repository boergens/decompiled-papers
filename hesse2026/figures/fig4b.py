"""Redraw Figure 4b (four population-tuning heatmaps) from the per-pixel matrices fig4b_<state>_<face>.csv.
Run from inside figures/:  python3 fig4b.py  ->  fig4b_replot.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

cmap = LinearSegmentedColormap.from_list("bwr_lin", [(0, 0, 1), (1, 1, 1), (1, 0, 0)])
VMIN, VMAX = -3, 6


def load(name):
    # fig4b_state1_conscious.csv, fig4b_state1_suppressed.csv, fig4b_state2_conscious.csv, fig4b_state2_suppressed.csv
    df = pd.read_csv(f"fig4b_{name}.csv", comment="#")
    return df.drop(columns=["cell_row_px"]).to_numpy(dtype=float)


panels = [("state1", "conscious"), ("state1", "suppressed"), ("state2", "conscious"), ("state2", "suppressed")]
fig, axes = plt.subplots(2, 2, figsize=(3.4, 2.2), dpi=200)
im = None
for (state, face), ax in zip(panels, axes.ravel()):
    Z = load(f"{state}_{face}")
    im = ax.imshow(Z, cmap=cmap, vmin=VMIN, vmax=VMAX, aspect="auto", interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    if state == "state1":
        ax.set_title(face.capitalize(), fontsize=6, pad=3)
    if state == "state2":
        ax.set_xlabel("1500 stimuli", fontsize=6, labelpad=2)
    ax.set_ylabel("554 cells", fontsize=6, labelpad=2)
    if face == "conscious":
        ax.text(-0.42, 0.5, "State 1" if state == "state1" else "State 2", fontsize=6, ha="center", va="center",
                transform=ax.transAxes)
fig.subplots_adjust(left=0.17, right=0.86, top=0.9, bottom=0.12, wspace=0.75, hspace=0.3)
cax = fig.add_axes([0.52, 0.58, 0.018, 0.3])
cb = fig.colorbar(im, cax=cax, ticks=[-3, 6])
cb.outline.set_visible(False)
cax.tick_params(labelsize=6, length=0, pad=1)
cax.set_ylabel("Response\n(z-scored)", fontsize=6, labelpad=2)
cax.yaxis.set_label_position("right")
fig.savefig("fig4b_replot.png", dpi=200)
print("wrote fig4b_replot.png")
