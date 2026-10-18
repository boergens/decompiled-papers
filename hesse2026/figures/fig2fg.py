#!/usr/bin/env python3
"""Redraw Figure 2f and 2g (single-neuron rasters aligned to state transitions) from
fig2f_state2_to_state1.csv, fig2f_state1_to_state2.csv, fig2g_state2_to_state1.csv, fig2g_state1_to_state2.csv.
Writes fig2f.png/pdf and fig2g.png/pdf."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ORANGE, PURPLE = "#fcae34", "#543379"

def draw(letter):
    panels = [(f"fig2{letter}_state2_to_state1.csv", 22, [("State 2", PURPLE), (" → ", "k"), ("State 1", ORANGE)]),
              (f"fig2{letter}_state1_to_state2.csv", 17, [("State 1", ORANGE), (" → ", "k"), ("State 2", PURPLE)])]
    fig, axs = plt.subplots(1, 2, figsize=(3.0, 1.9), dpi=200)
    for ax, (fn, nrows, title) in zip(axs, panels):
        d = pd.read_csv(fn, comment="#")
        ax.vlines(d["time_ms"], d["row_from_top"] - 0.5, d["row_from_top"] + 0.5, color="#222222", lw=0.5)
        ax.axvline(0, color="#888888", lw=0.5, ls=(0, (5, 3)))
        ax.set_xlim(-50, 50); ax.set_ylim(nrows + 0.5, 0.5)
        ax.set_xticks([-50, 0, 50]); ax.set_yticks([])
        ax.set_ylabel(f"{nrows} transitions", fontsize=6.5)
        ax.tick_params(labelsize=6)
        ax.spines[["top", "right"]].set_visible(False)
        xt = 0.5 - 0.42
        for txt, col in title:
            tt = ax.text(xt, 1.02, txt, color=col, fontsize=6.5, transform=ax.transAxes, va="bottom", ha="left")
            fig.canvas.draw()
            xt += tt.get_window_extent().transformed(ax.transAxes.inverted()).width
    fig.supxlabel("Time from transition (ms)", fontsize=7, y=0.02)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(f"fig2{letter}_replot.png", dpi=200)
    plt.close(fig)

draw("f")
draw("g")
