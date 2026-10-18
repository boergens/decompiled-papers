"""Shared re-plot for the beeswarm profile CSVs (Figure 5A-D, 7A-H): reads <panel>.csv only.
Each swarm is drawn as its silhouette: one horizontal segment per pixel row from left_px to right_px."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"LX 112": "#EDB120", "M Epon": "#A2142F", "MH Epon": "#0072BD", "H Epon": "#D95319", "VH Epon": "#4DBEEE",
       "Durcupan": "#7E2F8E", "Spurr's": "#77AC30"}


def plot(panel, ycol, ylim, yticks, ylabel, xpos=None, px_per_unit=52.0, xlabel="", figsize=(4.2, 3.0)):
    """xpos(group_index, series, group) -> x position of the group centre (default: group_index)."""
    with open(os.path.join(HERE, f"{panel}.csv")) as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    fig, ax = plt.subplots(figsize=figsize)
    groups = {}
    for r in rows:
        gi = int(r["group_index"])
        x = xpos(gi, r["series"], r["group"]) if xpos else gi
        groups[gi] = (x, r["series"], r["group"])
        ax.plot([x + float(r["left_px"]) / px_per_unit, x + float(r["right_px"]) / px_per_unit], [float(r[ycol])] * 2,
                color=COL[r["series"]], lw=0.6, solid_capstyle="butt")
    xs = sorted(v[0] for v in groups.values())
    ax.set_xlim(xs[0] - 1, xs[-1] + 1)
    ax.set_xticks([v[0] for v in groups.values()])
    ax.set_xticklabels([v[2] for v in groups.values()], fontsize=6, rotation=90)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"{panel}_replot.png"), dpi=150)
