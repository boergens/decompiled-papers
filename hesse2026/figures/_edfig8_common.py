"""Shared drawing code for the two Extended Data Figure 8 panels (imported by edfig8_left_state1.py and
edfig8_right_state2.py). Reads one CSV of 0.05-wide bins and draws overlaid translucent bar histograms
with opaque step outlines, as in the paper."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SERIES = {  # column stem: (fill/outline colour, legend label)
    "state1_conscious": ("#fcae34", "State 1,\nconscious"),
    "state1_suppressed": ("#ffd28a", "State 1,\nsuppressed"),
    "state2_conscious": ("#b56cc7", "State 2,\nconscious"),
    "state2_suppressed": ("#543379", "State 2,\nsuppressed"),
    "priming_half_trials": ("#000000", "Priming,\nhalf-trials"),
}


def draw(csv, out_stem, ymax, ylabel):
    df = pd.read_csv(csv, comment="#")
    edges = list(df.bin_left) + [df.bin_right.iloc[-1]]
    plt.rcParams.update({"font.size": 6, "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(figsize=(3.9, 2.5), dpi=200)
    handles = []
    for col in df.columns:
        if not col.endswith("_count"):
            continue
        name = col[:-len("_count")]
        colour, label = SERIES[name]
        ax.stairs(df[col], edges, baseline=0, fill=True, color=colour, alpha=0.30, lw=0)
        ax.stairs(df[col], edges, baseline=0, fill=False, color=colour, lw=0.5)
        handles.append(Line2D([], [], color=colour, lw=2.25, label=label))
    ax.axvline(0, color="#b3b3b3", lw=0.5, alpha=0.7, zorder=0)
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, ymax)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xticklabels(["-1", "-0.5", "0", "0.5", "1"])
    ax.set_yticks([0, ymax])
    ax.set_xlabel("Cosine angle")
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(0.5)
    ax.tick_params(length=3, width=0.5, labelsize=6)
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False, labelspacing=1.2, handlelength=1.2)
    fig.tight_layout()
    fig.savefig(out_stem + "_replot.png", dpi=200)
