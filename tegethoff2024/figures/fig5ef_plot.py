"""Shared re-plot for Figure 5E/5F: reads fig5<panel>.csv only."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"LX 112": "#EDB120", "M Epon": "#A2142F", "MH Epon": "#0072BD", "H Epon": "#D95319", "VH Epon": "#4DBEEE",
       "Durcupan": "#7E2F8E", "Spurr's": "#77AC30"}


def plot(panel, ycol, ylim, yticks, ylabel):
    with open(os.path.join(HERE, f"fig5{panel}.csv")) as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    for r in rows:
        c = COL[r["series"]]
        x, y = float(r["hardness_HV"]), float(r[ycol])
        if r["bar_low"] not in ("", "nan"):
            ax.errorbar(x, y, yerr=[[y - float(r["bar_low"])], [float(r["bar_high"]) - y]], color=c, lw=0.8, capsize=2)
        if r["marker"] == "filled":
            ax.plot(x, y, "o", color=c, ms=4)
        else:
            ax.plot(x, y, "s", mfc="none", mec=c, ms=4)
        if "asterisk" in r["flag"]:
            ax.text(x, y + 2.5, "*", ha="center", color="0.4")
    ax.set_xlim(12, 18)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.set_xlabel("Hardness (HV)")
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"fig5{panel}_replot.png"), dpi=150)
