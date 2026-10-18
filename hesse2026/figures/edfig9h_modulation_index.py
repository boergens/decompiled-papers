"""Redraw Extended Data Fig. 9h (second panel h: modulation index binocular vs unambiguous, four subpanels) from
edfig9h_modulation_index.csv. Run from this folder: python3 edfig9h_modulation_index.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
from _style import plt, save, ORANGE, PURPLE

d = pd.read_csv("edfig9h_modulation_index.csv", comment="#")
SUB = [("all_states", "All states", "black", +1), ("state1", "State 1", ORANGE, +1),
       ("state2", "State 2", PURPLE, -1), ("slope_equalized", "Slope-equalized", "black", +1)]
fig, axes = plt.subplots(2, 2, figsize=(3.55, 2.55))
for ax, (key, title, tcol, sign) in zip(axes.ravel(), SUB):
    s = d[d.subpanel == key]
    ax.plot([-1, 1], [-sign, sign], color="black", lw=0.5, ls=(0, (5, 3)))  # diagonal (y = -x in the State 2 subpanel)
    ax.axvline(0, color="black", lw=0.5, ls=(0, (5, 3)))
    ax.axhline(0, color="black", lw=0.5, ls=(0, (5, 3)))
    ax.scatter(s.modulation_index_unambiguous, s.modulation_index_binocular, s=0.9, color="black", lw=0, zorder=3)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    ax.set_title(title, color=tcol, fontsize=6, pad=2)
for ax in axes[1]:
    ax.set_xlabel("Modulation index unambiguous")
for ax in axes[:, 0]:
    ax.set_ylabel("Modulation index binocular")
fig.subplots_adjust(left=0.12, right=0.98, top=0.95, bottom=0.11, wspace=0.45, hspace=0.5)
save(fig, "edfig9h_modulation_index")
