"""Redraw Figure 5e (explained variance of face features, cross-area HMM states) from
fig5e_ML_to_AM.csv and fig5e_AM_to_ML.csv.  Run from this folder: python3 fig5e.py  ->  fig5e_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLACK, ORANGE, PURPLE = "#1c0f29", "#fcae34", "#543379"
series = [  # column, colour, linestyle, legend label
    ("priming_average_pct", BLACK, "-", "Priming, average"),
    ("binocular_conscious_state1_pct", ORANGE, "-", "Binocular conscious, state 1"),
    ("binocular_conscious_state2_pct", PURPLE, "-", "Binocular conscious, state 2"),
    ("binocular_suppressed_state1_pct", ORANGE, "--", "Binocular suppressed, state 1"),
    ("binocular_suppressed_state2_pct", PURPLE, "--", "Binocular suppressed, state 2"),
]
fig, axes = plt.subplots(1, 2, figsize=(4.6, 3.0), dpi=200)
for ax, (fname, title) in zip(axes, [("fig5e_ML_to_AM.csv", "ML → AM"), ("fig5e_AM_to_ML.csv", "AM → ML")]):
    df = pd.read_csv(fname, comment="#")
    for col, c, ls, lab in series:
        line, = ax.plot(df["feature_index"], df[col], color=c, ls=ls, lw=1, label=lab)
        if ls == "--":
            line.set_dashes((3, 1))
    ax.set_title(title, fontsize=7, pad=4)
    ax.set_xlim(1, 50); ax.set_xticks([10, 20, 30, 40, 50])
    ax.set_ylim(-100, 100); ax.set_yticks([-100, -50, 0, 50, 100])
    ax.set_xlabel("Feature #", fontsize=7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=7, width=0.5, length=2.5)
    for s in ax.spines.values(): s.set_linewidth(0.5)
axes[0].set_ylabel("Explained variance of features (%)", fontsize=7)
from matplotlib.lines import Line2D
h, l = axes[0].get_legend_handles_labels()
blank = Line2D([], [], color="none")
# three legend columns as in the original: priming | conscious 1, 2 | suppressed 1, 2 (columns fill top to bottom)
fig.legend([h[0], blank, h[1], h[2], h[3], h[4]], [l[0], " ", l[1], l[2], l[3], l[4]], loc="lower center", ncol=3,
           fontsize=6, frameon=False, bbox_to_anchor=(0.5, 0.0), handlelength=2.0, columnspacing=1.0, handletextpad=0.6)
fig.tight_layout(rect=(0, 0.1, 1, 1))
fig.savefig("fig5e_replot.png", dpi=200)
