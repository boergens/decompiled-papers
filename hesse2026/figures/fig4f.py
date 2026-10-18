"""Redraw Figure 4f (decoding accuracy vs number of cells, with s.d. band) from fig4f.csv.
Run from inside figures/:  python3 fig4f.py  ->  fig4f_replot.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

d = pd.read_csv("fig4f.csv", comment="#").sort_values("n_cells")
fig, ax = plt.subplots(figsize=(1.35, 1.25), dpi=200)
ax.fill_between(d.n_cells, d.band_lo_pct, d.band_hi_pct, color="k", alpha=0.2, linewidth=0)
ax.plot(d.n_cells, d.decoding_accuracy_pct, color="k", lw=1.2)
ax.axhline(50, color="k", ls="--", lw=0.6, dashes=(4, 3))   # chance level
ax.set_xlim(0, 1000); ax.set_ylim(0, 100)
ax.set_xticks([0, 1000]); ax.set_yticks([0, 50, 100])
ax.tick_params(labelsize=6, length=2, pad=1)
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("Number of cells", fontsize=6, labelpad=1)
ax.set_ylabel("Decoding accuracy", fontsize=6, labelpad=1)
fig.subplots_adjust(left=0.27, right=0.97, top=0.95, bottom=0.2)
fig.savefig("fig4f_replot.png", dpi=200)
print("wrote fig4f_replot.png")
