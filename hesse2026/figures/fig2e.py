#!/usr/bin/env python3
"""Redraw Figure 2e (population rasters aligned to state transitions) from fig2e_state2_to_state1.csv and
fig2e_state1_to_state2.csv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ORANGE, PURPLE = "#fcae34", "#543379"
panels = [("fig2e_state2_to_state1.csv", 2178, [("State 2", PURPLE), (" → ", "k"), ("State 1", ORANGE)]),
          ("fig2e_state1_to_state2.csv", 1936, [("State 1", ORANGE), (" → ", "k"), ("State 2", PURPLE)])]

fig, axs = plt.subplots(1, 2, figsize=(3.0, 1.9), dpi=200)
for ax, (fn, nrows, title) in zip(axs, panels):
    d = pd.read_csv(fn, comment="#")
    ax.plot(d["time_ms"] + 0.5, d["row_from_top"], ",", color="#222222")   # 1-ms bins, drawn at the bin centre
    sep = d.loc[d["cell_prefers"] == "suppressed", "row_from_top"].min() - 0.5
    ax.axhline(sep, color="k", lw=0.6)
    ax.axvline(0, color="#888888", lw=0.4)
    ax.set_xlim(-50, 50); ax.set_ylim(nrows + 1, 0)
    ax.set_xticks([-50, 0, 50]); ax.set_yticks([])
    ax.set_ylabel(f"{nrows} cell-transitions", fontsize=6.5)
    ax.tick_params(labelsize=6)
    ax.spines[["top", "right"]].set_visible(False)
    xt = 0.5 - 0.42
    for txt, col in title:
        tt = ax.text(xt, 1.02, txt, color=col, fontsize=6.5, transform=ax.transAxes, va="bottom", ha="left")
        fig.canvas.draw()
        xt += tt.get_window_extent().transformed(ax.transAxes.inverted()).width
fig.supxlabel("Time from transition (ms)", fontsize=7, y=0.02)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("fig2e_replot.png", dpi=200)
