#!/usr/bin/env python3
"""Redraw Figure 2k (single-trial decoding time courses for one session: Average / State 1 / State 2) from fig2k.csv.
The suppressed (dashed) series are only known where a dash was drawn (gaps are NaN in the CSV), so they are drawn
as solid pieces, which reproduces the dashed look."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("fig2k.csv", comment="#")
t = d["time_s"]
panels = [("average", "#808080", "Average", 0, 0), ("state1", "#fcae34", "State 1", 1, 0), ("state2", "#543379", "State 2", 1, 1)]

fig, axs = plt.subplots(2, 2, figsize=(2.7, 2.8), dpi=200)
axs[0, 1].axis("off")
for nm, col, title, r, c in panels:
    ax = axs[r, c]
    ax.plot(t, d[f"{nm}_conscious_pct"], color=col, lw=1.3)
    ax.plot(t, d[f"{nm}_suppressed_pct"], color=col, lw=1.3)   # dash pieces (NaN in the gaps)
    ax.set_xlim(-0.1, 2); ax.set_ylim(0, 100)
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 50, 100])
    ax.tick_params(labelsize=6)
    ax.set_title(title, fontsize=7, pad=2)
    ax.spines[["top", "right"]].set_visible(False)
# legend (line styles as in the paper: solid = conscious, dashed = suppressed)
axl = axs[0, 1]
axl.plot([], [], color="k", lw=1.3, label="Conscious")
axl.plot([], [], color="k", lw=1.3, ls="--", label="Suppressed")
axl.legend(fontsize=6.5, loc="center", frameon=False)
fig.supxlabel("Time from flash (ms)", fontsize=7, y=0.01)   # axis title as printed in the paper (ticks are seconds)
fig.supylabel("Decoding accuracy (%)", fontsize=7, x=0.02)
fig.tight_layout(rect=(0.04, 0.04, 1, 1))
fig.savefig("fig2k_replot.png", dpi=200)
