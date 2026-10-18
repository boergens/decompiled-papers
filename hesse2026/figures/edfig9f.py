"""Redraw Extended Data Fig. 9f (gain suppressed state 2 vs gain conscious state 1, one dot per cell) from edfig9f.csv.
Run from this folder: python3 edfig9f.py -> edfig9f_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
from _style import plt, save

d = pd.read_csv("edfig9f.csv", comment="#")
fig, ax = plt.subplots(figsize=(1.45, 1.35))
ax.plot([-0.5, 2.5], [-0.5, 2.5], color="black", lw=0.5, ls=(0, (5, 3)))  # identity line
ax.axvline(0, color="black", lw=0.5, ls=(0, (5, 3)))
ax.axhline(0, color="black", lw=0.5, ls=(0, (5, 3)))
ax.scatter(d.gain_conscious_state1, d.gain_suppressed_state2, s=0.5, color="black", lw=0, zorder=3)
ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.5, 2.5)
ax.set_xticks([0, 2]); ax.set_yticks([0, 2])
ax.set_xlabel("Gain conscious state 1"); ax.set_ylabel("Gain suppressed\nstate 2")
fig.subplots_adjust(left=0.27, right=0.97, top=0.97, bottom=0.2)
save(fig, "edfig9f")
