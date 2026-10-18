#!/usr/bin/env python3
"""Redraw Figure 2j (decoding accuracy vs number of faces, 5 series with +/- SD bands) from fig2j.csv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("fig2j.csv", comment="#")
ORANGE, PURPLE, BLACK = "#fcae34", "#543379", "#1c0f29"
x = d["n_faces"]
series = [("priming_average", BLACK, "-", "Priming, average"),
          ("binocular_conscious_state1", ORANGE, "-", "Binocular conscious, state 1"),
          ("binocular_conscious_state2", PURPLE, "-", "Binocular conscious, state 2"),
          ("binocular_suppressed_state1", ORANGE, "--", "Binocular suppressed, state 1"),
          ("binocular_suppressed_state2", PURPLE, "--", "Binocular suppressed, state 2")]

fig, ax = plt.subplots(figsize=(2.9, 2.9), dpi=200)
for nm, col, ls, lab in series:
    ax.fill_between(x, d[f"{nm}_sd_lo_pct"], d[f"{nm}_sd_hi_pct"], color=col, alpha=0.2, lw=0)
for nm, col, ls, lab in series:
    ax.plot(x, d[f"{nm}_pct"], color=col, lw=1.3, ls=ls, label=lab)
ax.set_xlim(0, 60); ax.set_ylim(0, 100)
ax.set_xticks([0, 20, 40, 60]); ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Number of faces", fontsize=7); ax.set_ylabel("Decoding accuracy (%)", fontsize=7)
ax.tick_params(labelsize=6)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(fontsize=5, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False, columnspacing=0.8, handlelength=1.8)
fig.tight_layout()
fig.savefig("fig2j_replot.png", dpi=200, bbox_inches="tight")
