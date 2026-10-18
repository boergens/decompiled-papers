"""Redraw Figure 4e (mean response state 2 vs state 1, one dot per cell) from fig4e.csv.
Run from inside figures/:  python3 fig4e.py  ->  fig4e_replot.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

d = pd.read_csv("fig4e.csv", comment="#")
fig, ax = plt.subplots(figsize=(1.35, 1.25), dpi=200)
ax.plot([0, 3], [0, 3], "k--", lw=0.6, dashes=(4, 3))   # identity
ax.scatter(d.mean_response_state1_norm, d.mean_response_state2_norm, s=0.3, c="k", linewidths=0)
ax.set_xlim(0, 3); ax.set_ylim(0, 3)
ax.set_xticks([0, 3]); ax.set_yticks([0, 3])
ax.tick_params(labelsize=6, length=2, pad=1)
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Mean state 1 (norm.)", fontsize=6, labelpad=1)
ax.set_ylabel("Mean state 2 (norm.)", fontsize=6, labelpad=1)
fig.subplots_adjust(left=0.25, right=0.97, top=0.95, bottom=0.2)
fig.savefig("fig4e_replot.png", dpi=200)
print("wrote fig4e_replot.png")
