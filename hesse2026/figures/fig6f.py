"""Redraw Figure 6f (modulation index binocular vs unambiguous, PFC; four scatter panels) from
fig6f_all_states.csv, fig6f_state1.csv, fig6f_state2.csv, fig6f_slope_equalized.csv.
Run from inside figures/:  python3 fig6f.py  ->  fig6f_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PANELS = [  # csv suffix, title, title colour, identity line slope (+1: y = x, -1: y = -x)
    ("all_states", "All states", "k", +1),
    ("state1", "State 1", "#fcae34", +1),
    ("state2", "State 2", "#6d429c", -1),
    ("slope_equalized", "Slope-equalized", "k", +1),
]


def main():
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 1.9), dpi=200)
    for ax, (suffix, title, tcol, slope) in zip(axes, PANELS):
        df = pd.read_csv(f"fig6f_{suffix}.csv", comment="#")
        x = df["modulation_index_unambiguous"].to_numpy()
        y = df["modulation_index_binocular"].to_numpy()
        ax.axhline(0, color="k", lw=0.5, ls=(0, (4, 3)))
        ax.axvline(0, color="k", lw=0.5, ls=(0, (4, 3)))
        ax.plot([-1, 1], [-slope, slope], color="k", lw=0.5, ls=(0, (4, 3)))
        ax.scatter(x, y, s=1.2, color="k", lw=0, zorder=3)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=6, color=tcol, pad=3)
        ax.set_xlabel("Modulation index unambiguous", fontsize=6)
        ax.set_ylabel("Modulation index binocular", fontsize=6)
        ax.tick_params(labelsize=6, length=2, width=0.5, direction="out")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_linewidth(0.5)
    fig.tight_layout(pad=0.3, w_pad=1.0)
    fig.savefig("fig6f_replot.png", dpi=200)


if __name__ == "__main__":
    main()
