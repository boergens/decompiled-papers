#!/usr/bin/env python3
"""Redraw Figure 2d (log-likelihood ratio autocorrelation vs lag, data vs time-shuffled) from fig2d.csv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import re, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("fig2d.csv", comment="#")
# position of the vertical dashed reference line is recorded in the CSV header comments
ref_lag = None
for line in open("fig2d.csv"):
    if not line.startswith("#"):
        break
    m = re.search(r"reference line at lag = ([\d.]+) ms", line)
    if m:
        ref_lag = float(m.group(1))

fig, ax = plt.subplots(figsize=(2.3, 1.7), dpi=200)
for nm, col, lab in [("shuffled", "#808080", "time-shuffled"), ("data", "#000000", "data")]:
    ax.fill_between(d["lag_ms"], d[f"{nm}_sd_lo"], d[f"{nm}_sd_hi"], color=col, alpha=0.3, lw=0)
    ax.plot(d["lag_ms"], d[f"{nm}_autocorr"], color=col, lw=1.2, label=lab)
if ref_lag is not None:
    ax.axvline(ref_lag, color="#a6a6a6", lw=0.6, ls="--")
ax.set_xlim(0, 200); ax.set_ylim(-0.12, 1.0)
ax.set_xticks([0, 100, 200]); ax.set_yticks([0, 0.5, 1])
ax.set_xlabel("Lag (ms)", fontsize=7); ax.set_ylabel("Log-likelihood\nautocorrelation", fontsize=7)
ax.tick_params(labelsize=6)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("fig2d_replot.png", dpi=200)
