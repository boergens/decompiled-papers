"""Redraw Extended Data Fig. 7c (decoding accuracy vs number of faces, shuffle-template control) from edfig7c.csv.
Run from inside figures/:  python3 edfig7c.py  ->  edfig7c_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PANEL = "edfig7c"
df = pd.read_csv(PANEL + ".csv", comment="#")

BLACK, ORANGE, PURPLE = "#1c0f29", "#fcae34", "#543379"
series = [  # column prefix, colour, linestyle, legend label
    ("priming_average", BLACK, "-", "Priming, average"),
    ("binocular_conscious_state1", ORANGE, "-", "Binocular conscious, state 1"),
    ("binocular_conscious_state2", PURPLE, "-", "Binocular conscious, state 2"),
    ("binocular_suppressed_state1", ORANGE, (0, (4, 4)), "Binocular suppressed, state 1"),
    ("binocular_suppressed_state2", PURPLE, (0, (4, 4)), "Binocular suppressed, state 2"),
]

fig, ax = plt.subplots(figsize=(2.3, 2.45), dpi=200)
x = df["number_of_faces"]
for pre, c, ls, label in series:  # bands first, then all lines on top (as in the original drawing order)
    ax.fill_between(x, df[pre + "_band_lo_pct"], df[pre + "_band_hi_pct"], color=c, alpha=0.2, lw=0)
for pre, c, ls, label in series:
    ax.plot(x, df[pre + "_pct"], color=c, lw=1, ls=ls, label=label)

ax.set_xlim(0, 60)
ax.set_ylim(0, 100)
ax.set_xticks([0, 20, 40, 60])
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Number of faces", fontsize=7, labelpad=1)
ax.set_ylabel("Decoding accuracy (%)", fontsize=7, labelpad=2)
ax.tick_params(labelsize=6.5, length=2.5, width=0.5)
ax.spines[["top", "right"]].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(0.5)
fig.tight_layout()
fig.savefig(PANEL + "_replot.png", dpi=200)
