"""Redraw Extended Data Fig. 10f (held-out log likelihood, two-state minus one-state, per model) from edfig10f.csv.
Run from inside figures/:  python3 edfig10f.py  ->  edfig10f_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PANEL = "edfig10f"
df = pd.read_csv(PANEL + ".csv", comment="#")

MODELS = ["Real", "2-state", "Average", "Uncoord"]
sub = df.set_index("model").loc[MODELS]
x = range(len(MODELS))

fig, ax = plt.subplots(figsize=(3.5, 1.9), dpi=200)
ax.bar(x, sub["value_loglik"], width=0.55, color="#262626", lw=0)
ax.errorbar(x, sub["value_loglik"], yerr=[sub["value_loglik"] - sub["err_lo_loglik"],
                                          sub["err_hi_loglik"] - sub["value_loglik"]],
            fmt="none", ecolor="k", elinewidth=0.5, capsize=1.2, capthick=0.5)
ax.axhline(0, color="k", lw=0.5)
ax.set_xlim(-0.6, 3.6)
ax.set_ylim(-0.15, 0.1)
ax.set_xticks(list(x))
ax.set_xticklabels(MODELS, fontsize=6.5)
ax.set_yticks([-0.15, -0.1, -0.05, 0, 0.05, 0.1])
ax.set_ylabel("Held-out log likelihood\n(2-state - 1-state)", fontsize=6.5, labelpad=2)
ax.tick_params(labelsize=6.5, length=2.5, width=0.5)
ax.spines[["top", "right"]].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(0.5)
fig.tight_layout()
fig.savefig(PANEL + "_replot.png", dpi=200, bbox_inches="tight")
