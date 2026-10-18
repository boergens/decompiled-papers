"""Redraw Figure 4c (three stacked gain histograms) from fig4c.csv.
Run from inside figures/:  python3 fig4c.py  ->  fig4c_replot.png
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
from matplotlib.lines import Line2D

df = pd.read_csv("fig4c.csv", comment="#")
labels = {"state1_conscious": "State 1,\nconscious", "state1_suppressed": "State 1,\nsuppressed",
          "state2_conscious": "State 2,\nconscious", "state2_suppressed": "State 2,\nsuppressed"}
colours = {"state1_conscious": "#fcae34", "state1_suppressed": "#ffd28a",
           "state2_conscious": "#b56cc7", "state2_suppressed": "#543379"}
# series order within each subplot as drawn in the original (first drawn = underneath)
order = {1: ["state1_conscious", "state1_suppressed"], 2: ["state2_suppressed", "state2_conscious"],
         3: ["state1_conscious", "state2_suppressed"]}
ylims = {1: 204, 2: 136, 3: 136}   # top of the y axis line in the original

fig, axes = plt.subplots(3, 1, figsize=(2.6, 1.3), dpi=200, sharex=True)
for sp, ax in zip([1, 2, 3], axes):
    for name in order[sp]:
        d = df[(df.subplot == sp) & (df.series == name)].sort_values("gain_bin_lo")
        lo, hi, cnt = d.gain_bin_lo.to_numpy(), d.gain_bin_hi.to_numpy(), d.count_rounded.to_numpy()
        width = np.median(hi - lo)
        # translucent bars (only non-empty bins exist in the CSV)
        ax.bar(lo, cnt, width=hi - lo, align="edge", color=colours[name], alpha=0.3, linewidth=0)
        # opaque stair outline over the full range, inserting empty bins where needed
        edges = np.round(np.arange(lo.min(), hi.max() + width / 2, width), 6)
        full = np.zeros(len(edges) - 1)
        for l, c in zip(lo, cnt):
            full[int(round((l - lo.min()) / width))] = c
        ax.stairs(full, edges, color=colours[name], linewidth=0.8, baseline=0)
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(0, ylims[sp])
    ax.set_yticks([0, 100]); ax.set_xticks([0, 2])
    ax.tick_params(labelsize=6, length=2, pad=1)
    ax.spines[["top", "right"]].set_visible(False)
axes[-1].set_xlabel("Gain", fontsize=6, labelpad=1)
fig.text(0.03, 0.57, "Number of neurons", fontsize=6, rotation=90, ha="center", va="center")
handles = [Line2D([0], [0], color=colours[n], lw=2.25) for n in labels]
fig.legend(handles, list(labels.values()), loc="center left", bbox_to_anchor=(0.66, 0.5), fontsize=6, frameon=False,
           handlelength=1.2, labelspacing=0.9, borderaxespad=0)
fig.subplots_adjust(left=0.2, right=0.64, top=0.97, bottom=0.17, hspace=0.35)
fig.savefig("fig4c_replot.png", dpi=200)
print("wrote fig4c_replot.png")
