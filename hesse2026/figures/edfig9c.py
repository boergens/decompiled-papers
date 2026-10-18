"""Redraw Extended Data Fig. 9c (explained variance of features vs feature index) from edfig9c.csv.
Run from this folder: python3 edfig9c.py -> edfig9c_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
from _style import plt, save, ORANGE, PURPLE, BLACK

d = pd.read_csv("edfig9c.csv", comment="#")
SERIES = [  # column, label, colour, linestyle
    ("priming_average", "Priming, average", BLACK, "-"),
    ("binocular_conscious_state1", "Binocular conscious, state 1", ORANGE, "-"),
    ("binocular_conscious_state2", "Binocular conscious, state 2", PURPLE, "-"),
    ("binocular_suppressed_state1", "Binocular suppressed, state 1", ORANGE, (0, (4, 1.5))),
    ("binocular_suppressed_state2", "Binocular suppressed, state 2", PURPLE, (0, (4, 1.5))),
]
fig, ax = plt.subplots(figsize=(1.9, 2.55))
for col, label, color, ls in SERIES:
    s = d[["feature_index", col]].copy()
    if col == "binocular_conscious_state2":
        # empty cells = value below -100 % (not recoverable, the drawn line leaves the axes there); draw the line
        # running off the bottom of the axes like the original, using an off-axis placeholder that is clipped away
        s[col] = s[col].fillna(-115)
    else:
        s = s.dropna()  # (no empty cells expected for the other series)
    ax.plot(s.feature_index, s[col], color=color, ls=ls, lw=1.0, label=label, clip_on=True)
ax.set_xlim(1, 50); ax.set_ylim(-100, 100)
ax.set_xticks([10, 20, 30, 40, 50]); ax.set_yticks([-100, -50, 0, 50, 100])
ax.set_xlabel("Feature #"); ax.set_ylabel("Explained variance of features (%)")
# "Shape" (features 1-20) / "Appearance" (21-50) brackets above the axes
for x0, x1, txt in [(1, 20, "Shape"), (21, 50, "Appearance")]:
    ax.plot([x0, x0, x1, x1], [104, 108, 108, 104], color="black", lw=0.5, clip_on=False)
    ax.text((x0 + x1) / 2, 110, txt, ha="center", va="bottom", fontsize=6)
ax.legend(loc="upper center", bbox_to_anchor=(0.35, -0.2), ncol=1, frameon=False, handlelength=2.2, borderaxespad=0)
fig.subplots_adjust(left=0.24, right=0.97, top=0.9, bottom=0.37)
save(fig, "edfig9c")
