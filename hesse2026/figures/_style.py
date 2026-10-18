"""Shared matplotlib style for the Extended Data Figure 9 redraw scripts (imported by edfig9*.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ORANGE, PURPLE, BLACK = "#fcae34", "#543379", "#1c0f29"
PALE_ORANGE, PALE_PURPLE = "#ffd28a", "#b56cc7"
AXCOL = "#333333"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 6, "axes.labelsize": 6, "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6,
    "axes.linewidth": 0.5, "axes.edgecolor": AXCOL, "xtick.color": AXCOL, "ytick.color": AXCOL,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "savefig.dpi": 200,
})


def save(fig, stem):
    fig.savefig(stem + "_replot.png", dpi=200)
