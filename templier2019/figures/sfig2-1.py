"""Re-plot Figure 2—figure supplement 1 (a-d) of Templier 2019 (eLife 8:e45696) -> sfig2-1_replot.png

Reads sfig2-1a.csv, sfig2-1b.csv, sfig2-1c.csv (grey grids), sfig2-1c_lines.csv (coloured lines over c)
and sfig2-1d.csv (bar chart).
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def grid(name):
    with open(os.path.join(HERE, name)) as f:
        lines = [l for l in f if not l.startswith("#")]
    head = lines[0].strip().split(",")
    x = np.array([float(v) for v in head[1:]])
    y, z = [], []
    for l in lines[1:]:
        p = l.strip().split(",")
        y.append(float(p[0]))
        z.append([float(v) if v else np.nan for v in p[1:]])
    return x, np.array(y), np.array(z)


def rows(name):
    with open(os.path.join(HERE, name)) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


COL = {"1": "#65b365", "2": "#6565fe", "3": "#656565", "4": "#d765da", "7": "#ff6764", "mixed": "#9aa"}
fig, axes = plt.subplots(2, 2, figsize=(6, 5.8))
for ax, k in zip((axes[0, 0], axes[0, 1], axes[1, 0]), "abc"):
    x, y, z = grid(f"sfig2-1{k}.csv")
    dx, dy = x[1] - x[0], y[1] - y[0]
    cm = plt.get_cmap("gray").copy()
    cm.set_bad("#bcd")                      # blank: under the printed panel letter
    ax.imshow(np.ma.masked_invalid(z), cmap=cm, vmin=0, vmax=255, interpolation="nearest",
              extent=(x[0] - dx / 2, x[-1] + dx / 2, y[-1] + dy / 2, y[0] - dy / 2))
    ax.set_xticks(range(0, 501, 100))
    ax.set_yticks(range(0, 501, 100))
    ax.set_xticklabels(["0", "", "200", "", "400", ""] if k in "ab" else [])
    ax.set_yticklabels(["0", "", "200", "", "400", ""] if k in "ac" else [])
    ax.xaxis.tick_top()
    ax.text(0.95, 0.95, k, transform=ax.transAxes, ha="right", va="top", fontsize=18)
    if k == "c":
        for r in rows("sfig2-1c_lines.csv"):
            v = float(r["index"])
            if r["orientation"] == "vertical":
                ax.axvline(v, color=COL[r["legend_label"]], lw=0.6, alpha=0.8)
            else:
                ax.axhline(v, color=COL[r["legend_label"]], lw=0.6, alpha=0.8)
ax = axes[1, 1]
d = rows("sfig2-1d.csv")
cat = [int(r["category"]) for r in d]
ax.bar(cat, [float(r["height_read"]) for r in d], width=0.4, color="blue")
for c, r in zip(cat, d):
    ax.text(c, float(r["height_read"]) + 8, r["printed_value"], ha="center", va="bottom", fontsize=9)
ax.set_xticks(cat)
ax.set_ylim(0, 450)
ax.set_yticks([0, 100, 200, 300, 400])
ax.set_xlim(-1, 7.6)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.text(0.95, 0.95, "d", transform=ax.transAxes, ha="right", va="top", fontsize=18)
handles = [plt.Line2D([], [], color=COL[k], lw=3, label=k) for k in ("1", "2", "3", "4", "7")]
ax.legend(handles=handles, ncol=3, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig2-1_replot.png"), dpi=200)
print("sfig2-1_replot.png")
