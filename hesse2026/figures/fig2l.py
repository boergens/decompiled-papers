#!/usr/bin/env python3
"""Redraw Figure 2l (single-trial decoding summary across 10 sessions) from fig2l.csv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("fig2l.csv", comment="#")
cats = ["average_pct", "state1_pct", "state2_pct"]
xpos = [0, 1, 2]
colors = ["#808080", "#fcae34", "#543379"]

fig, ax = plt.subplots(figsize=(2.6, 2.6), dpi=200)
for _, r in d.iterrows():
    ls = "-" if r["condition"] == "conscious" else "--"
    y = [r[c] for c in cats]
    if r["line"].startswith("session"):
        ax.plot(xpos, y, color="#000000", lw=0.3, ls=ls, alpha=0.6)
    elif r["line"] == "mean":
        ax.plot(xpos, y, color="#000000", lw=1.6, ls=ls)
    elif r["line"] == "mean_marker":
        for xp, v, col in zip(xpos, y, colors):
            if r["condition"] == "conscious":
                ax.plot(xp, v, "o", color=col, ms=6, zorder=5)
            else:
                ax.plot(xp, v, "o", mfc="white", mec=col, mew=1.3, ms=6, zorder=5)
ax.plot([], [], "o", color="k", ms=6, label="Conscious")
ax.plot([], [], "o", mfc="white", mec="k", mew=1.3, ms=6, label="Suppressed")
ax.set_xlim(-0.5, 2.5); ax.set_ylim(0, 100)
ax.set_xticks(xpos); ax.set_xticklabels(["Average", "State 1", "State 2"], fontsize=7)
ax.set_yticks([0, 20, 40, 60, 80, 100]); ax.tick_params(labelsize=6)
ax.set_ylabel("Decoding accuracy (%)", fontsize=7)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(fontsize=6.5, loc="upper left", frameon=False)
fig.tight_layout()
fig.savefig("fig2l_replot.png", dpi=200)
