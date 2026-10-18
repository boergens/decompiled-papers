"""Re-plot helper for zhao2025's scatter panels with error bars (reads the CSV written by markerpanel.py)."""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def read(path):
    with open(path) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def fitline(path):
    """(slope, intercept, x_from, x_to) parsed from the 'Fit line' comment of the CSV."""
    import re
    txt = open(path).read()
    m = re.search(r"from \S+ = ([-\d.e]+) to ([-\d.e]+), i\.e\. \S+ = ([-\d.e]+) \* \S+ \+ \(([-\d.e]+)\)", txt)
    a, b, s, c = map(float, m.groups())
    return s, c, a, b


def plot(csv_path, out, xlim, ylim, xticks, yticks, xlabel, ylabel, shades=None, figsize=(4, 2.8)):
    rows = read(csv_path)
    fig, ax = plt.subplots(figsize=figsize)
    for (a, b, col) in shades or []:
        ax.axvspan(a, b, color=col, lw=0)
    for r in rows:
        x, y = float(r["x"]), float(r["y"])
        col = "#5b9bd5" if r["series"] == "Tearing-induced" else "#e74c3c"
        if r["y_err_low"]:
            ax.errorbar([x], [y], yerr=[[y - float(r["y_err_low"])], [float(r["y_err_high"]) - y]], color=col, capsize=3)
        if r["x_err_low"]:
            ax.errorbar([x], [y], xerr=[[x - float(r["x_err_low"])], [float(r["x_err_high"]) - x]], color=col, capsize=3)
        ax.plot([x], [y], "s", color=col, ms=5, label=r["series"])
    s, c, a, b = fitline(csv_path)
    ax.plot([a, b], [s * a + c, s * b + c], "r-.", lw=2)
    h, l = ax.get_legend_handles_labels()
    seen = {}
    for hh, ll in zip(h, l):
        seen.setdefault(ll, hh)
    ax.legend(seen.values(), seen.keys(), fontsize=7, loc="upper left")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_xticks(xticks); ax.set_yticks(yticks)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
