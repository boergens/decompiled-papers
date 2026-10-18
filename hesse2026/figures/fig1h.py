"""Redraw Figure 1h (modulation index binocular vs unambiguous) from fig1h.csv.
Run from inside figures/:  python3 fig1h.py  ->  fig1h_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("fig1h.csv", comment="#")
fig, ax = plt.subplots(figsize=(2.9, 2.9), dpi=200)
ax.scatter(df["modulation_index_unambiguous"], df["modulation_index_binocular"], s=2.5, c="k", lw=0, zorder=3)
ax.plot([-1, 1], [-1, 1], color="k", lw=0.8, ls=(0, (6, 4)))       # identity line
ax.axvline(0, color="k", lw=0.8, ls=(0, (6, 4)))
ax.axhline(0, color="k", lw=0.8, ls=(0, (6, 4)))
ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
ax.set_xlabel("Modulation index unambiguous", fontsize=8)
ax.set_ylabel("Modulation index binocular", fontsize=8)
ax.tick_params(labelsize=8)
ax.spines[["top", "right"]].set_visible(False)
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig("fig1h_replot.png")
