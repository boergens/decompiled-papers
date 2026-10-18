"""Redraw Figure 4g (modulation index binocular vs unambiguous, four scatter plots) from fig4g.csv.
Run from inside figures/:  python3 fig4g.py  ->  fig4g_replot.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

d = pd.read_csv("fig4g.csv", comment="#")
panels = [("all_states", "All states", "k", +1), ("state1", "State 1", "#fbae34", +1),
          ("state2", "State 2", "#6d429c", -1), ("slope_equalized", "Slope-equalized", "k", +1)]
fig, axes = plt.subplots(2, 2, figsize=(3.5, 2.55), dpi=200)
for (name, title, tcol, diag), ax in zip(panels, axes.ravel()):
    s = d[d.subplot == name]
    ax.plot([-1, 1], [-diag, diag], "k--", lw=0.6, dashes=(4, 3))   # identity (anti-identity for state 2)
    ax.axhline(0, color="k", ls="--", lw=0.6, dashes=(4, 3))
    ax.axvline(0, color="k", ls="--", lw=0.6, dashes=(4, 3))
    ax.scatter(s.modulation_index_unambiguous, s.modulation_index_binocular, s=0.5, c="k", linewidths=0)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    ax.tick_params(labelsize=6, length=2, pad=1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title(title, fontsize=6, color=tcol, pad=2)
for ax in axes[1]:
    ax.set_xlabel("Modulation index unambiguous", fontsize=6, labelpad=1)
for ax in axes[:, 0]:
    ax.set_ylabel("Modulation index binocular", fontsize=6, labelpad=1)
fig.subplots_adjust(left=0.13, right=0.98, top=0.93, bottom=0.11, wspace=0.55, hspace=0.45)
fig.savefig("fig4g_replot.png", dpi=200)
print("wrote fig4g_replot.png")
