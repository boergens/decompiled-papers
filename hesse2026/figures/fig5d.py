"""Redraw Figure 5d (fit accuracy vs median dwell time) from fig5d.csv.
Run from this folder: python3 fig5d.py  ->  fig5d_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("fig5d.csv", comment="#")
x = df["median_dwell_ms"]
fig, ax = plt.subplots(figsize=(2.1, 2.4), dpi=200)
for st, col in [("state1", "#fcae34"), ("state2", "#543379")]:
    ax.fill_between(x, df[f"{st}_norm_cllr_sem_lo"], df[f"{st}_norm_cllr_sem_hi"], color=col, alpha=0.25, lw=0)
    ax.plot(x, df[f"{st}_norm_cllr_mean"], color=col, lw=1, marker="o", ms=3, label=f"state {st[-1]}")
ax.set_xlim(0, 250); ax.set_xticks(range(0, 251, 50))
ax.set_ylim(0.5, 1.0); ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0]); ax.set_yticklabels(["0.5", "0.6", "0.7", "0.8", "0.9", "1"])
ax.set_xlabel("Median Dwell time (ms)", fontsize=7)
ax.set_ylabel("Normalized conditional\nlog-likelihood ratio", fontsize=7)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(labelsize=7, width=0.5, length=2.5)
for s in ax.spines.values(): s.set_linewidth(0.5)
fig.tight_layout()
fig.savefig("fig5d_replot.png", dpi=200)
