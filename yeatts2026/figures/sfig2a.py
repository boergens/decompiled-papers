#!/usr/bin/env python3
"""Re-plot Supplemental Figure 2, panel a (two stacked boxes) from sfig2atop.csv and sfig2abottom.csv.

    python3 -I sfig2a.py   -> sfig2a_replot.png

Both axes are unnumbered in the paper, so the plot uses axis-box fractions (0..1) on both axes and draws each
series as its per-column mean with the per-column envelope (top..bottom) as a lighter band.  Run with argument
'b' (or via sfig2b.py) to re-plot panel b from sfig2btop.csv / sfig2bbottom.csv.
"""
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COLOURS = {"channel 2 (blue)": "#0072bd", "channel 1 (orange)": "#d95319"}
LABELS = {"a": ("Pixel number (axis fraction)", "Intensity (axis fraction)"),
          "b": ("Depth (axis fraction)", "Intensity (dB) (axis fraction)")}


def read(path):
    data = {}
    with open(path) as f:
        rows = [r for r in csv.reader(l for l in f if not l.startswith("#"))]
    head, body = rows[0], rows[1:]
    for r in body:
        d = dict(zip(head, r))
        data.setdefault(d["series"], []).append((float(d["x_frac"]), float(d["y_frac"]),
                                                 float(d["y_frac_top"]), float(d["y_frac_bottom"])))
    return data


def replot(panel):
    xl, yl = LABELS[panel]
    fig, axes = plt.subplots(2, 1, figsize=(6, 4.2), sharex=True)
    for ax, pos in zip(axes, ("top", "bottom")):
        data = read(os.path.join(HERE, "sfig2%s%s.csv" % (panel, pos)))
        for name, pts in data.items():
            pts.sort()
            x = [p[0] for p in pts]
            ax.fill_between(x, [p[3] for p in pts], [p[2] for p in pts], color=COLOURS[name], alpha=0.25, lw=0)
            ax.plot(x, [p[1] for p in pts], color=COLOURS[name], lw=0.8, label=name)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_ylabel(yl, fontsize=8)
        ax.set_title("%s box" % pos, fontsize=8, loc="left")
        ax.tick_params(labelsize=7)
    axes[0].legend(fontsize=7, loc="upper right")
    axes[1].set_xlabel(xl, fontsize=8)
    fig.suptitle("Supplemental Fig. 2%s (re-plot of the digitized data)" % panel, fontsize=9)
    fig.tight_layout()
    out = os.path.join(HERE, "sfig2%s_replot.png" % panel)
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    replot(sys.argv[1] if len(sys.argv) > 1 else "a")
