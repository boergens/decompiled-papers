"""Shared re-plot for Figure 8B/D/F: reads fig8<panel>.csv only."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def f(v):
    return float(v) if v not in ("", "nan") else float("nan")


def plot(panel, xmax, xticks):
    with open(os.path.join(HERE, f"fig8{panel}.csv")) as fh:
        rows = list(csv.DictReader(l for l in fh if not l.startswith("#")))
    fig, ax = plt.subplots(figsize=(4.2, 2.6))
    for s, c in [("sectional (blue)", "#1f6fb8"), ("transverse (red)", "#b4202f")]:
        r = [x for x in rows if x["series"] == s]
        t = [f(x["time_s"]) for x in r]
        ax.fill_between(t, [f(x["band_bottom"]) for x in r], [f(x["band_top"]) for x in r], color="0.75", lw=0)
        ax.plot(t, [f(x["thin_upper"]) for x in r], color=c, lw=0.5)
        ax.plot(t, [f(x["thin_lower"]) for x in r], color=c, lw=0.5)
        ax.plot(t, [f(x["mean_mid"]) for x in r], color=c, lw=1.5)
    ax.set_xlim(0, xmax)
    ax.set_xticks(xticks)
    ax.set_ylim(-10, 125)
    ax.set_yticks([0, 40, 80, 120])
    ax.set_xlabel("time (s)")
    ax.set_ylabel("force (mN/mm)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"fig8{panel}_replot.png"), dpi=150)
