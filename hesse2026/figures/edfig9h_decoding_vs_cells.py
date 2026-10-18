"""Redraw Extended Data Fig. 9h (first panel h: state-1-vs-state-2 decoding accuracy vs number of cells) from
edfig9h_decoding_vs_cells.csv. Run from this folder: python3 edfig9h_decoding_vs_cells.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
from _style import plt, save

d = pd.read_csv("edfig9h_decoding_vs_cells.csv", comment="#")
fig, ax = plt.subplots(figsize=(1.45, 1.35))
ax.fill_between(d.n_cells, d.band_lo_pct, d.band_hi_pct, color="black", alpha=0.2, lw=0)
ax.plot(d.n_cells, d.decoding_accuracy_pct, color="black", lw=1.0)
ax.axhline(50, color="black", lw=0.5, ls=(0, (5, 3)))  # chance level
ax.set_xlim(0, 1000); ax.set_ylim(0, 100)
ax.set_xticks([0, 1000]); ax.set_yticks([0, 50, 100])
ax.set_xlabel("Number of cells"); ax.set_ylabel("Decoding accuracy (%)")
fig.subplots_adjust(left=0.25, right=0.97, top=0.97, bottom=0.2)
save(fig, "edfig9h_decoding_vs_cells")
