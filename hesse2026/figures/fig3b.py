#!/usr/bin/env python3
"""Redraw Figure 3b: population spike rasters (held-out half of neurons) aligned to State 2 -> State 1 transitions
(left, 1196 cell-transitions) and State 1 -> State 2 transitions (right, 988 cell-transitions).
Reads fig3b_state2_to_state1.csv, fig3b_state1_to_state2.csv, fig3b_meta.csv; writes fig3b_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib.pyplot as plt

from fig3_common import ORANGE, PURPLE, coloured_title, read_csv, save

meta = read_csv("fig3b_meta.csv").set_index("raster")
panels = [("state2_to_state1", [("State 2", PURPLE), (" → ", "k"), ("State 1", ORANGE)]),
          ("state1_to_state2", [("State 1", ORANGE), (" → ", "k"), ("State 2", PURPLE)])]

fig, axes = plt.subplots(1, 2, figsize=(3.4, 1.65), dpi=200)
for ax, (name, title) in zip(axes, panels):
    d = read_csv(f"fig3b_{name}.csv")
    n = int(meta.loc[name, "n_rows"])
    # the original draws each spike as a 0.3-pt-thick mark 0.18 ms long (left end at its 1-ms bin), alpha 0.7; at the
    # row pitch of 0.046 pt that is a dot about 6 rows tall, reproduced here as a small square dot
    ax.scatter(d["time_ms"] + 0.09, d["row_index"], marker="s", s=0.7, color="k", alpha=0.7, lw=0)
    ax.axhline(meta.loc[name, "separator_row_y"], color="k", lw=0.5)        # above: prefer conscious face; below: suppressed
    ax.axvline(0, color="k", lw=0.25, ls=(0, (5, 3)))                        # state transition
    ax.set_xlim(-50, 50)
    ax.set_ylim(n + 1, 0)                                                    # row 1 at the top
    ax.set_xticks([-50, 0, 50])
    ax.set_yticks([])
    ax.set_ylabel(f"{n} cell-transitions")
    coloured_title(ax, title)
fig.supxlabel("Time from transition (ms)", y=0.02)
fig.tight_layout(pad=0.3, w_pad=1.0, rect=(0, 0.06, 1, 1))
save(fig, "fig3b")
