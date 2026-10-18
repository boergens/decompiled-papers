"""Redraw Extended Data Fig. 10d (cross-validated reconstruction explained variance per model and state) from edfig10d.csv.
Run from inside figures/:  python3 edfig10d.py  ->  edfig10d_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PANEL = "edfig10d"
YLABEL = "Held-out reconstruction EV (%)"
LEGEND = False
df = pd.read_csv(PANEL + ".csv", comment="#", dtype={"printed_label": str})

MODELS = ["Real", "2-state", "Average", "Uncoord"]
ORANGE, PURPLE = "#fcae34", "#543379"
series = [  # name, colour, alpha, x offset within the group, legend label
    ("state1_conscious", ORANGE, 1.0, -0.3, "State 1 conscious"),
    ("state1_suppressed", ORANGE, 0.35, -0.1, "State 1 suppressed"),
    ("state2_conscious", PURPLE, 0.35, 0.1, "State 2 conscious"),
    ("state2_suppressed", PURPLE, 1.0, 0.3, "State 2 suppressed"),
]
YMIN, YMAX = -100, 100

fig, ax = plt.subplots(figsize=(3.5, 1.9), dpi=200)
for name, c, a, off, label in series:
    sub = df[df["series"] == name].set_index("model").loc[MODELS]
    x = [i + off for i in range(len(MODELS))]
    drawn = sub["bar_drawn_to_ev_pct"].values          # bars below the axis limit are drawn down to it, as in the original
    ax.bar(x, drawn, width=0.18, color=c, alpha=a, label=label, lw=0)
    ok = sub["err_lo_ev_pct"].notna().values
    ax.errorbar([xi for xi, o in zip(x, ok) if o], sub["bar_drawn_to_ev_pct"].values[ok],
                yerr=[(sub["bar_drawn_to_ev_pct"] - sub["err_lo_ev_pct"]).values[ok],
                      (sub["err_hi_ev_pct"] - sub["bar_drawn_to_ev_pct"]).values[ok]],
                fmt="none", ecolor="k", elinewidth=0.5, capsize=1.2, capthick=0.5)
    for xi, lab in zip(x, sub["printed_label"].values):   # numbers printed inside the clipped bars
        if isinstance(lab, str) and lab.strip():
            ax.text(xi, -60, lab, rotation=90, ha="center", va="center", fontsize=4, color="#222222")

ax.axhline(0, color="k", lw=0.5)
ax.set_xlim(-0.6, 3.6)
ax.set_ylim(YMIN, YMAX)
ax.set_xticks(range(len(MODELS)))
ax.set_xticklabels(MODELS, fontsize=6.5)
ax.set_yticks([-100, -50, 0, 50, 100])
ax.set_ylabel(YLABEL, fontsize=6.5, labelpad=2)
ax.tick_params(labelsize=6.5, length=2.5, width=0.5)
ax.spines[["top", "right"]].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(0.5)
if LEGEND:
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6, frameon=False, handlelength=1,
              handleheight=1, columnspacing=1.0)
fig.tight_layout()
fig.savefig(PANEL + "_replot.png", dpi=200, bbox_inches="tight")
