"""Redraw Extended Data Fig. 9d (decoding accuracy vs number of faces, with bands) from edfig9d.csv.
Run from this folder: python3 edfig9d.py -> edfig9d_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
from _style import plt, save, ORANGE, PURPLE, BLACK

d = pd.read_csv("edfig9d.csv", comment="#")
SERIES = [
    ("priming_average", "Priming, average", BLACK, "-"),
    ("binocular_conscious_state1", "Binocular conscious, state 1", ORANGE, "-"),
    ("binocular_conscious_state2", "Binocular conscious, state 2", PURPLE, "-"),
    ("binocular_suppressed_state1", "Binocular suppressed, state 1", ORANGE, (0, (4, 2))),
    ("binocular_suppressed_state2", "Binocular suppressed, state 2", PURPLE, (0, (4, 2))),
]
fig, ax = plt.subplots(figsize=(1.9, 2.55))
for col, label, color, ls in SERIES:
    line = d[["n_faces", col]].dropna()                       # dashed series: vertices inside dash gaps are empty
    band = d[["n_faces", col + "_lo", col + "_hi"]].dropna()   # band absent where it was clipped to zero area
    ax.fill_between(band.n_faces, band[col + "_lo"], band[col + "_hi"], color=color, alpha=0.2, lw=0)
    ax.plot(line.n_faces, line[col], color=color, ls=ls, lw=1.0, label=label)
ax.set_xlim(0, 60); ax.set_ylim(0, 100)
ax.set_xticks([0, 20, 40, 60]); ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Number of faces"); ax.set_ylabel("Decoding accuracy (%)")
ax.legend(loc="upper center", bbox_to_anchor=(0.35, -0.2), ncol=1, frameon=False, handlelength=2.2, borderaxespad=0)
fig.subplots_adjust(left=0.24, right=0.97, top=0.9, bottom=0.37)
save(fig, "edfig9d")
