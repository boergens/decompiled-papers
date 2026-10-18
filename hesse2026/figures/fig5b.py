"""Redraw Figure 5b (HMM state partition heatmap, trials x time) from fig5b_state1_fraction.csv.
Run from this folder: python3 fig5b.py  ->  fig5b_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

df = pd.read_csv("fig5b_state1_fraction.csv", comment="#")
trial = df.iloc[:, 0].to_numpy()                      # estimated trial index of each pixel row (top to bottom)
t = np.array([float(c) for c in df.columns[1:]])      # time (s) of each pixel column
M = df.iloc[:, 1:].to_numpy(float)                    # fraction of state 1 (1 = orange, 0 = purple)
dt, dtr = t[1] - t[0], trial[1] - trial[0]
cmap = LinearSegmentedColormap.from_list("state", ["#543379", "#fcae34"])   # state 2 purple -> state 1 orange

fig, ax = plt.subplots(figsize=(2.3, 2.2), dpi=200)
ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto", interpolation="nearest",
          extent=[t[0] - dt / 2, t[-1] + dt / 2, trial[-1] + dtr / 2, trial[0] - dtr / 2])
ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_xticklabels(["-1", "", "0", "", "1"])
ax.set_yticks(np.arange(100, 801, 100)); ax.set_yticklabels([])
ax.tick_params(direction="in", length=2, width=0.5, top=True, right=True)
ax.set_xlabel("Time from flash (s)", fontsize=7)
ax.set_ylabel("800 trials", fontsize=7)
ax.tick_params(labelsize=7)
for s in ax.spines.values(): s.set_linewidth(0.5)
fig.tight_layout()
fig.savefig("fig5b_replot.png", dpi=200)
