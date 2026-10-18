"""Redraw Extended Data Fig. 9e (three stacked gain histograms) from edfig9e.csv.
Run from this folder: python3 edfig9e.py -> edfig9e_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from _style import plt, save, ORANGE, PURPLE, PALE_ORANGE, PALE_PURPLE

d = pd.read_csv("edfig9e.csv", comment="#")
COL = {"state1_conscious": ORANGE, "state1_suppressed": PALE_ORANGE, "state2_conscious": PALE_PURPLE, "state2_suppressed": PURPLE}
LABEL = {"state1_conscious": "State 1,\nconscious", "state1_suppressed": "State 1,\nsuppressed",
         "state2_conscious": "State 2,\nconscious", "state2_suppressed": "State 2,\nsuppressed"}
ROWS = [(1, ["state1_suppressed", "state1_conscious"]), (2, ["state2_conscious", "state2_suppressed"]),
        (3, ["state1_conscious", "state2_suppressed"])]
fig, axes = plt.subplots(3, 1, figsize=(2.05, 1.35), sharex=True)
for ax, (row, series) in zip(axes, ROWS):
    for s in series:
        h = d[(d.panel_row == row) & (d.series == s)].sort_values("gain_bin_lo")
        edges = np.r_[h.gain_bin_lo.values, h.gain_bin_hi.values[-1]]
        ax.stairs(h["count"].values, edges, fill=True, color=COL[s], alpha=0.3, lw=0)   # 30 %-opacity fill
        ax.stairs(h["count"].values, edges, fill=False, color=COL[s], lw=0.5, baseline=0)  # step outline
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(0, 160 if row > 1 else 130)
    ax.set_yticks([0, 100]); ax.set_xticks([0, 2])
    ax.tick_params(axis="x", labelbottom=(row == 3))
axes[-1].set_xlabel("Gain")
handles = [Patch(facecolor=COL[s], edgecolor="none", label=LABEL[s]) for s in ["state1_conscious", "state1_suppressed", "state2_conscious", "state2_suppressed"]]
axes[1].legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, handlelength=1.3, handleheight=0.6, labelspacing=1.0, borderaxespad=0)
fig.subplots_adjust(left=0.2, right=0.66, top=0.97, bottom=0.2, hspace=0.45)
save(fig, "edfig9e")
