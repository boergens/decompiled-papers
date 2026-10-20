"""Re-plot Figure 7 of Nikitin et al. 2024 from fig7.csv -> fig7_replot.png: the timeline blocks as a Gantt chart
with the same time axis (ms after the 71 s mark)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig7.csv"), newline="") as f:
    rows = [r for r in csv.reader(l for l in f if not l.startswith("#"))]
hdr, rows = rows[0], rows[1:]
order = []
for r in rows:
    if r[0] not in order:
        order.append(r[0])
colours = {"green": "#68d0a8", "purple": "#d888f8", "kernel": "#7090d0", "small": "#9eeaf3"}
fig, ax = plt.subplots(figsize=(11, 3.6), dpi=150)
prev = None
for r in rows:
    series, label, t0, t1 = r[0], r[1], float(r[3]), float(r[4])
    y = len(order) - 1 - order.index(series)
    key = "green" if "HtoD" in series else "purple" if "DtoH" in series else "small" if "cyan" in series else "kernel"
    ax.barh(y, t1 - t0, left=t0, height=0.6, color=colours[key], edgecolor="black", linewidth=0.3)
    same_block = prev is not None and prev[0] == series and prev[1] == label and t0 - prev[2] < 0.5
    if label and t1 - t0 > 1.2 and not same_block:          # one label per block (memcpy blocks have several sub-boxes)
        ax.text(t0 + 0.3, y, label, ha="left", va="center", fontsize=5)
    prev = (series, label, t1)
ax.set_yticks(range(len(order)))
ax.set_yticklabels([order[len(order) - 1 - i] for i in range(len(order))], fontsize=7)
ax.set_xlim(595, 665)
ax.set_xticks(range(600, 661, 10))
ax.set_xticklabels([f"+{t}ms" for t in range(600, 661, 10)])
ax.set_xlabel("time after the 71 s mark (ms)")
ax.grid(True, axis="x", color="0.85")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig7_replot.png"))
print("wrote fig7_replot.png")
