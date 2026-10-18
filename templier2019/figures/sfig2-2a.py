"""Re-plot Figure 2—figure supplement 2a of Templier 2019 (eLife 8:e45696) from sfig2-2a.csv -> sfig2-2a_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "sfig2-2a.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
left = [float(r["bin_left"]) for r in rows]
right = [float(r["bin_right"]) for r in rows]
h = [int(r["frequency"]) for r in rows]
fig, ax = plt.subplots(figsize=(3.6, 2.7))
ax.bar(left, h, width=[b - a for a, b in zip(left, right)], align="edge", color="#b0b0b0", edgecolor="black", lw=0.5)
ax.set_xlim(left[0], right[-1] + 5)
ax.set_ylim(0, 10.4)
ax.set_xticks([500, 1000, 1500, 2000, 2500])
ax.set_xticklabels(["", "1000", "", "2000", ""])
ax.set_yticks([0, 2, 4, 6, 8, 10])
ax.set_yticklabels(["0", "", "4", "", "8", ""])
ax.set_xlabel("Number of inliers")
ax.set_ylabel("Frequency")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig2-2a_replot.png"), dpi=200)
print("sfig2-2a_replot.png")
