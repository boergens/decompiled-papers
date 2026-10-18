"""Redraw Figure 4d (gain suppressed state 2 vs gain conscious state 1, one dot per cell) from fig4d.csv.
Run from inside figures/:  python3 fig4d.py  ->  fig4d_replot.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

d = pd.read_csv("fig4d.csv", comment="#")
fig, ax = plt.subplots(figsize=(1.35, 1.25), dpi=200)
ax.plot([-0.5, 2.5], [-0.5, 2.5], "k--", lw=0.6, dashes=(4, 3))   # identity
ax.axhline(0, color="k", ls="--", lw=0.6, dashes=(4, 3))
ax.axvline(0, color="k", ls="--", lw=0.6, dashes=(4, 3))
ax.scatter(d.gain_conscious_state1, d.gain_suppressed_state2, s=0.3, c="k", linewidths=0)
ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.5, 2.5)
ax.set_xticks([0, 2]); ax.set_yticks([0, 2])
ax.tick_params(labelsize=6, length=2, pad=1)
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Gain conscious state 1", fontsize=6, labelpad=1)
ax.set_ylabel("Gain suppressed\nstate 2", fontsize=6, labelpad=1)
fig.subplots_adjust(left=0.3, right=0.97, top=0.95, bottom=0.2)
fig.savefig("fig4d_replot.png", dpi=200)
print("wrote fig4d_replot.png")
