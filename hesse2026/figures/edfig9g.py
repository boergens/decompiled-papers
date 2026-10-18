"""Redraw Extended Data Fig. 9g (normalised mean response, state 2 vs state 1, one dot per cell) from edfig9g.csv.
Run from this folder: python3 edfig9g.py -> edfig9g_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
from _style import plt, save

d = pd.read_csv("edfig9g.csv", comment="#")
fig, ax = plt.subplots(figsize=(1.45, 1.35))
ax.plot([0, 3], [0, 3], color="black", lw=0.5, ls=(0, (5, 3)))  # identity line
ax.axvline(0, color="black", lw=0.5, ls=(0, (5, 3)))
ax.axhline(0, color="black", lw=0.5, ls=(0, (5, 3)))
ax.scatter(d.mean_state1_norm, d.mean_state2_norm, s=0.5, color="black", lw=0, zorder=3)
ax.set_xlim(0, 3); ax.set_ylim(0, 3)
ax.set_xticks([0, 3]); ax.set_yticks([0, 3])
ax.set_xlabel("Mean state 1 (norm.)"); ax.set_ylabel("Mean state 2 (norm.)")
fig.subplots_adjust(left=0.22, right=0.97, top=0.97, bottom=0.2)
save(fig, "edfig9g")
