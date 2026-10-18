"""Shared bits for the Figure 3 redraw scripts (colours, CSV reader, coloured titles). Pure matplotlib/pandas."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea  # noqa: E402

ORANGE = "#fcae34"   # state 1
PURPLE = "#543379"   # state 2
BLACK = "#1c0f29"    # priming, average (panels f, g)
GREY = "#808080"     # average (panels h, i)
AXCOL = "#333333"

plt.rcParams.update({
    "font.family": ["Liberation Sans", "DejaVu Sans"],
    "font.size": 7, "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.5,
    "axes.edgecolor": AXCOL, "xtick.color": AXCOL, "ytick.color": AXCOL, "axes.labelcolor": "black",
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42,
})


def read_csv(path):
    """Read one of the fig3 CSVs: skip the leading '#' provenance lines, then pandas."""
    with open(path) as f:
        text = "".join(line for line in f if not line.startswith("#"))
    return pd.read_csv(io.StringIO(text))


def coloured_title(ax, parts, size=7, y=1.0):
    """Title made of differently coloured pieces, e.g. [('State 2', PURPLE), (' → ', 'k'), ('State 1', ORANGE)]."""
    box = HPacker(children=[TextArea(t, textprops=dict(color=c, size=size)) for t, c in parts], pad=0, sep=0)
    ab = AnchoredOffsetbox(loc="lower center", child=box, pad=0, frameon=False, bbox_to_anchor=(0.5, y),
                           bbox_transform=ax.transAxes, borderpad=0.3)
    ax.add_artist(ab)


def save(fig, stem):
    fig.savefig(stem + "_replot.png", dpi=200)
