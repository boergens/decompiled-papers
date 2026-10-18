"""Re-plot one digitized panel of Ta, Tran & Righi 2023 from its CSV (used by figures/<panel>.py).

Markers at the digitized points; the connecting curve is a cubic spline through them, drawn only to
resemble the paper's smooth curves (the paper's curves are its plotting program's interpolation).
Points with an empty value (hidden markers) are left out.
"""
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.interpolate import CubicSpline  # noqa: E402


def read(path):
    with open(path) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def series(rows, ycol):
    out = {}
    for r in rows:
        if r[ycol] == "":
            continue
        out.setdefault(r["series"], []).append((float(r["displacement_A"]), float(r[ycol])))
    return {k: np.array(sorted(v)) for k, v in out.items()}


def draw(ax, xy, colour, marker, ls="-", label=None, ms=7):
    x, y = xy[:, 0], xy[:, 1]
    if len(x) >= 3 and np.all(np.diff(x) > 0):
        xx = np.linspace(x[0], x[-1], 300)
        ax.plot(xx, CubicSpline(x, y, bc_type="natural")(xx), ls, color=colour, lw=1.5)
    else:
        ax.plot(x, y, ls, color=colour, lw=1.5)
    ax.plot(x, y, marker, color=colour, ms=ms, alpha=0.75, ls="none", label=label)


def panel(csv_path, out_png, styles, xlim, ylim, ylabel="Energy (eV)", ycol="energy_eV", title=None,
          xticks=(0, 0.5, 1, 1.5, 2, 2.5), yticks=None, legend=True, twin=None, figsize=(5, 3.6)):
    """styles: {series: (colour, marker)}. twin: dict(ycol, ylim, ylabel, styles, yticks) for a right axis."""
    rows = read(csv_path)
    fig, ax = plt.subplots(figsize=figsize)
    data = series(rows, ycol)
    for name, (c, m) in styles.items():
        if name in data:
            draw(ax, data[name], c, m, label=name)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    ax.set_xlabel("Displacement (Å)")
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=10)
    if twin:
        ax2 = ax.twinx()
        d2 = series(rows, twin["ycol"])
        for name, (c, m) in twin["styles"].items():
            if name in d2:
                draw(ax2, d2[name], c, m, ls="--", label=name)
        ax2.set_ylim(*twin["ylim"])
        if twin.get("yticks") is not None:
            ax2.set_yticks(twin["yticks"])
        ax2.set_ylabel(twin["ylabel"], color="red")
    if legend:
        ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
