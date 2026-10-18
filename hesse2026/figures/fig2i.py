#!/usr/bin/env python3
"""Redraw Figure 2i (explained variance of face features, 5 series) from fig2i.csv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("fig2i.csv", comment="#")
ORANGE, PURPLE, BLACK = "#fcae34", "#543379", "#1c0f29"
x = d["feature_index"]

def clipped(col):
    """Vertices flagged *_clipped have no value (line leaves the axes below -100 %): draw them at -100 %."""
    y = d[col + "_pct"].to_numpy(float).copy()
    flag = d.get(col + "_clipped")
    if flag is not None:
        y[flag.to_numpy() == 1] = -100.0
    return y

fig, ax = plt.subplots(figsize=(2.9, 2.9), dpi=200)
ax.plot(x, d["priming_average_pct"], color=BLACK, lw=1.3, label="Priming, average")
ax.plot(x, d["binocular_conscious_state1_pct"], color=ORANGE, lw=1.3, label="Binocular conscious, state 1")
ax.plot(x, clipped("binocular_conscious_state2"), color=PURPLE, lw=1.3, label="Binocular conscious, state 2")
ax.plot(x, clipped("binocular_suppressed_state1"), color=ORANGE, lw=1.3, ls="--", label="Binocular suppressed, state 1")
ax.plot(x, d["binocular_suppressed_state2_pct"], color=PURPLE, lw=1.3, ls="--", label="Binocular suppressed, state 2")
ax.set_xlim(1, 50); ax.set_ylim(-100, 100)
ax.set_xticks([10, 20, 30, 40, 50]); ax.set_yticks([-100, -50, 0, 50, 100])
ax.set_xlabel("Feature #", fontsize=7); ax.set_ylabel("Explained variance of features (%)", fontsize=7)
ax.tick_params(labelsize=6)
ax.spines[["top", "right"]].set_visible(False)
# brackets: shape features 1-20, appearance features 21-50
for x0, x1, lab in [(1, 20, "Shape"), (21, 50, "Appearance")]:
    ax.plot([x0, x0, x1, x1], [104, 108, 108, 104], color="k", lw=0.6, clip_on=False)
    ax.text((x0 + x1) / 2, 110, lab, ha="center", va="bottom", fontsize=6.5)
ax.legend(fontsize=5, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False, columnspacing=0.8, handlelength=1.8)
fig.tight_layout()
fig.savefig("fig2i_replot.png", dpi=200, bbox_inches="tight")
