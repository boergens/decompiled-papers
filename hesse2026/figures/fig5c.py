"""Redraw Figure 5c (fit accuracy and median dwell time vs HMM bin size) from fig5c.csv.
Run from this folder: python3 fig5c.py  ->  fig5c_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("fig5c.csv", comment="#")
x = df["bin_size_ms"]
ORANGE, PURPLE = "#fcae34", "#543379"
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(2.2, 2.7), dpi=200, sharex=True)

ax1.fill_between(x, df["norm_cllr_sem_lo"], df["norm_cllr_sem_hi"], color="black", alpha=0.2, lw=0)
ax1.plot(x, df["norm_cllr_mean"], color="black", lw=1, marker="o", ms=3)
ax1.set_ylim(0.6, 1.0); ax1.set_yticks([0.6, 0.8, 1.0]); ax1.set_yticklabels(["0.6", "0.8", "1"])
ax1.set_ylabel("Norm. conditional\nlog-likelihood ratio", fontsize=7)

for st, col in [("state1", ORANGE), ("state2", PURPLE)]:
    ax2.fill_between(x, df[f"median_dwell_{st}_sem_lo"], df[f"median_dwell_{st}_sem_hi"], color=col, alpha=0.3, lw=0)
    ax2.plot(x, df[f"median_dwell_{st}_ms"], color=col, lw=1, marker="o", ms=3, label=f"state {st[-1]}")
ax2.set_ylim(0, 200); ax2.set_yticks([0, 100, 200])
ax2.set_ylabel("Median dwell\ntime (ms)", fontsize=7)
ax2.set_xlabel("Bin size (ms)", fontsize=7)

for ax in (ax1, ax2):
    ax.set_xscale("log"); ax.set_xlim(2, 100)
    ax.set_xticks([2, 3, 5, 10, 20, 50, 100]); ax.set_xticklabels(["2", "3", "5", "10", "20", "50", "100"])
    ax.set_xticks([4, 6, 7, 8, 9, 30, 40, 60, 70, 80, 90], minor=True); ax.set_xticklabels([], minor=True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=7, width=0.5, length=2.5); ax.tick_params(which="minor", length=1.5, width=0.5)
    for s in ax.spines.values(): s.set_linewidth(0.5)
fig.tight_layout(h_pad=0.6)
fig.savefig("fig5c_replot.png", dpi=200)
