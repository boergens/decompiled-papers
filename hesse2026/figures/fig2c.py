#!/usr/bin/env python3
"""Redraw Figure 2c (proportion of time points in state 1 / state 2 vs time from flash) from fig2c.csv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("fig2c.csv", comment="#")
ORANGE, PURPLE = "#fcae34", "#543379"

fig, ax = plt.subplots(figsize=(2.3, 1.7), dpi=200)
for nm, col in [("state1", ORANGE), ("state2", PURPLE)]:
    ax.fill_between(d["time_s"], d[f"{nm}_sd_lo_pct"], d[f"{nm}_sd_hi_pct"], color=col, alpha=0.25, lw=0)
    ax.plot(d["time_s"], d[f"{nm}_pct"], color=col, lw=1.2, label=f"State {nm[-1]}")
ax.axvline(0, color="#a6a6a6", lw=0.6, ls="--")
ax.axhline(50, color="#a6a6a6", lw=0.6, ls="--")
ax.set_xlim(-1, 1); ax.set_ylim(0, 100)
ax.set_xticks([-1, 0, 1]); ax.set_yticks([0, 25, 50, 75, 100])
ax.set_xlabel("Time from flash (seconds)", fontsize=7); ax.set_ylabel("Proportion state (%)", fontsize=7)
ax.tick_params(labelsize=6)
ax.text(-0.5, 104, "Priming", ha="center", va="bottom", fontsize=6.5)
ax.text(0.5, 104, "Binocular", ha="center", va="bottom", fontsize=6.5)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("fig2c_replot.png", dpi=200)
