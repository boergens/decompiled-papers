#!/usr/bin/env python3
"""Redraw Figure 3c: spike rasters of the example ML cell (prefers the conscious face) aligned to 21 State 2 -> State 1
transitions (left) and 18 State 1 -> State 2 transitions (right), states inferred from all other neurons.
Reads fig3c_state2_to_state1.csv and fig3c_state1_to_state2.csv; writes fig3c_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib.pyplot as plt

from fig3_common import ORANGE, PURPLE, coloured_title, read_csv, save

# number of transitions (rows) per raster, as printed on the y axes of the figure
panels = [("state2_to_state1", 21, [("State 2", PURPLE), (" → ", "k"), ("State 1", ORANGE)]),
          ("state1_to_state2", 18, [("State 1", ORANGE), (" → ", "k"), ("State 2", PURPLE)])]

fig, axes = plt.subplots(1, 2, figsize=(3.0, 1.65), dpi=200)
for ax, (name, n, title) in zip(axes, panels):
    d = read_csv(f"fig3c_{name}.csv")
    ax.vlines(d["time_ms"], d["row_index"] - 0.5, d["row_index"] + 0.5, color="k", lw=0.4, alpha=0.8)  # one tick per spike
    ax.axvline(0, color="k", lw=0.25, ls=(0, (5, 3)))                                                 # state transition
    ax.set_xlim(-50, 50)
    ax.set_ylim(n + 0.5, 0.5)                                                                           # row 1 at the top
    ax.set_xticks([-50, 0, 50])
    ax.set_yticks([1, n])                                                                              # ticks at rows 1 and n, unlabelled as in the original
    ax.set_yticklabels([])
    ax.set_ylabel(f"{n} transitions")
    coloured_title(ax, title)
fig.supxlabel("Time from transition (ms)", y=0.02)
fig.tight_layout(pad=0.3, w_pad=1.0, rect=(0, 0.06, 1, 1))
save(fig, "fig3c")
