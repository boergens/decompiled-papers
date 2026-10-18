"""Redraw Extended Data Fig. 10e (held-out tuning correlation per model and state) from edfig10e.csv.
Run from inside figures/:  python3 edfig10e.py  ->  edfig10e_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PANEL = "edfig10e"
df = pd.read_csv(PANEL + ".csv", comment="#")

MODELS = ["Real", "2-state", "Average", "Uncoord"]
series = [("state1", "#fcae34", -0.2, "State 1"), ("state2", "#543379", 0.2, "State 2")]

fig, ax = plt.subplots(figsize=(3.5, 1.9), dpi=200)
for name, c, off, label in series:
    sub = df[df["series"] == name].set_index("model").loc[MODELS]
    x = [i + off for i in range(len(MODELS))]
    ax.bar(x, sub["value_tuning_r"], width=0.36, color=c, label=label, lw=0)
    ax.errorbar(x, sub["value_tuning_r"], yerr=[sub["value_tuning_r"] - sub["err_lo_tuning_r"],
                                                sub["err_hi_tuning_r"] - sub["value_tuning_r"]],
                fmt="none", ecolor="k", elinewidth=0.5, capsize=1.2, capthick=0.5)

ax.axhline(0, color="k", lw=0.5)
ax.set_xlim(-0.6, 3.6)
ax.set_ylim(-1, 1)
ax.set_xticks(range(len(MODELS)))
ax.set_xticklabels(MODELS, fontsize=6.5)
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_ylabel("Held-out tuning correlation", fontsize=6.5, labelpad=2)
ax.tick_params(labelsize=6.5, length=2.5, width=0.5)
ax.spines[["top", "right"]].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(0.5)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6, frameon=False, handlelength=1,
          handleheight=1, columnspacing=1.5)
fig.tight_layout()
fig.savefig(PANEL + "_replot.png", dpi=200, bbox_inches="tight")
