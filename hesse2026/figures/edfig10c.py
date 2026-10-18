"""Redraw Extended Data Fig. 10c (conscious-face reconstruction EV in state 1 vs achieved mean HMM dwell time)
from edfig10c.csv.  Run from inside figures/:  python3 edfig10c.py  ->  edfig10c_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PANEL = "edfig10c"
df = pd.read_csv(PANEL + ".csv", comment="#", dtype={"self_transition_p": str})

series = [("real_data", "#cc2929", "Real data", (7, -8)), ("average_model", "#2970bf", "Average model", (-9, -8))]

fig, ax = plt.subplots(figsize=(3.5, 1.9), dpi=200)
for name, c, label, (dx, dy) in series:
    sub = df[df["series"] == name]
    x, y = sub["achieved_mean_dwell_ms"].values, sub["reconstruction_ev_conscious_pct"].values
    ax.errorbar(x, y, xerr=[x - sub["dwell_err_lo_ms"].values, sub["dwell_err_hi_ms"].values - x],
                fmt="none", ecolor=c, elinewidth=0.5, capsize=1, capthick=0.5)
    ax.plot(x, y, "-o", color=c, lw=1, ms=3.5, label=label)
    for xi, yi, p in zip(x, y, sub["self_transition_p"]):   # the imposed self-transition probability, printed next to each point
        off = (dx, dy)
        if name == "average_model" and p in ("0.50", "0.60", "0.99"):   # as in the original: 0.50 left, 0.60 right-below, 0.99 above-left
            off = {"0.50": (-10, -6), "0.60": (9, -8), "0.99": (-6, 7)}[p]
        ax.annotate(p, (xi, yi), xytext=off, textcoords="offset points", fontsize=4.5, ha="center", va="center",
                    color="#222222")

ax.set_xlim(0, 300)
ax.set_ylim(45, 65)
ax.set_xticks([0, 50, 100, 150, 200, 250, 300])
ax.set_yticks([45, 50, 55, 60, 65])
ax.set_xlabel("Achieved mean HMM dwell (ms)", fontsize=6.5, labelpad=1)
ax.set_ylabel("Reconstruction EV, conscious (%)", fontsize=6.5, labelpad=2)
ax.tick_params(labelsize=6.5, length=2.5, width=0.5)
ax.spines[["top", "right"]].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(0.5)
ax.legend(loc="upper right", fontsize=6, frameon=False, handlelength=2)
fig.tight_layout()
fig.savefig(PANEL + "_replot.png", dpi=200, bbox_inches="tight")
