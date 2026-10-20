"""Re-plot figures/fig4.csv (FIG. 4 of US 8,109,184 B2) -> figures/fig4_replot.png. Reads only the CSV."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [r for r in csv.reader(l for l in open(os.path.join(HERE, "fig4.csv")) if not l.startswith("#"))]
head, rows = rows[0], rows[1:]
val = [float(r[head.index("value")]) for r in rows]
err = [float(r[head.index("err_high")]) for r in rows]
num = [r[head.index("numeral")] for r in rows]
mark = [r[head.index("mark")] for r in rows]
fill = [r[head.index("fill")] for r in rows]
fig, ax = plt.subplots(figsize=(3.2, 3.6))
x = [1, 2]
for xi, v, e, n, m, fl in zip(x, val, err, num, mark, fill):
    ax.bar(xi, v, width=0.45, color="white", edgecolor="black", hatch="///" if fl == "hatched" else None)
    ax.errorbar(xi, v, yerr=[[0], [e]], color="black", capsize=12)
    ax.text(xi + 0.3, v * 0.75, n, ha="left", va="center")
    if m:
        ax.text(xi, v + e + 0.15, m, ha="center", va="bottom", fontsize=14)
ax.set_xlim(0.5, 2.5)
ax.set_ylim(0, 8)
ax.set_yticks([0, 2, 4, 6, 8])
ax.set_xticks([])
ax.set_ylabel("Live/Dead Cell Ratio")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4_replot.png"), dpi=150)
print("wrote fig4_replot.png")
