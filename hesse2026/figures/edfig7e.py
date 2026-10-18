"""Redraw Extended Data Fig. 7e (explained variance of face features, shuffle-template control compared to the presented faces) from edfig7e.csv.
Run from inside figures/:  python3 edfig7e.py  ->  edfig7e_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PANEL = "edfig7e"
df = pd.read_csv(PANEL + ".csv", comment="#")

BLACK, ORANGE, PURPLE = "#1c0f29", "#fcae34", "#543379"
series = [  # column, colour, linestyle, legend label
    ("priming_average_ev_pct", BLACK, "-", "Priming, average"),
    ("binocular_conscious_state1_ev_pct", ORANGE, "-", "Binocular conscious, state 1"),
    ("binocular_conscious_state2_ev_pct", PURPLE, "-", "Binocular conscious, state 2"),
    ("binocular_suppressed_state1_ev_pct", ORANGE, (0, (4, 4)), "Binocular suppressed, state 1"),
    ("binocular_suppressed_state2_ev_pct", PURPLE, (0, (4, 4)), "Binocular suppressed, state 2"),
]

fig, ax = plt.subplots(figsize=(2.3, 2.6), dpi=200)
x = df["feature_index"]
for col, c, ls, label in series:
    ax.plot(x, df[col], color=c, lw=1, ls=ls, label=label, solid_joinstyle="miter")

ax.set_xlim(1, 50)
ax.set_ylim(-100, 100)
ax.set_xticks([10, 20, 30, 40, 50])
ax.set_yticks([-100, -50, 0, 50, 100])
ax.set_xlabel("Feature #", fontsize=7, labelpad=1)
ax.set_ylabel("Explained variance of features (%)", fontsize=7, labelpad=2)
ax.tick_params(labelsize=6.5, length=2.5, width=0.5)
ax.spines[["top", "right"]].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(0.5)

# "Shape" (features 1-20) and "Appearance" (21-50) brackets above the plot, as in the original
for x0, x1, txt in ((1, 20, "Shape"), (21, 50, "Appearance")):
    y = 110
    ax.plot([x0, x0, x1, x1], [y - 5, y, y, y - 5], color="k", lw=0.5, clip_on=False)
    ax.text((x0 + x1) / 2, y + 2, txt, ha="center", va="bottom", fontsize=6.5)

# legend below the plot, laid out as in the original (3 columns: priming | conscious 1,2 | suppressed 1,2)
handles, labels = ax.get_legend_handles_labels()
blank = matplotlib.patches.Rectangle((0, 0), 1, 1, fill=False, edgecolor="none", visible=False)
order = [0, None, 1, 2, 3, 4]
fig.legend([blank if i is None else handles[i] for i in order], [" " if i is None else labels[i] for i in order],
           loc="upper center", ncol=3, fontsize=5, frameon=False, bbox_to_anchor=(0.5, 0.0),
           handlelength=2.2, columnspacing=1.0)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(PANEL + "_replot.png", dpi=200, bbox_inches="tight")
