"""Re-plot Figure 13 of Xie & Fang 2019 from fig13.csv -> fig13_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig13.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(6, 3.6))
for s, c in (("Ft", "#4472c4"), ("Fn", "#ed7d31")):
    x = [float(r["cutting_depth_A"]) for r in rows if r["series"] == s]
    y = [float(r["cutting_force_nN"]) for r in rows if r["series"] == s]
    ax.plot(x, y, "o-", color=c, label=s, ms=6)
ax.set_xlim(0, 2.4)
ax.set_xticks([i * 0.2 for i in range(13)])
ax.set_ylim(-10, 80)
ax.set_yticks(range(-10, 81, 10))
ax.grid(color="0.85")
ax.set_xlabel("Cutting depth(Å)")
ax.set_ylabel("Cutting force(nN)")
ax.legend(loc="center right")
fig.tight_layout()
fig.savefig(HERE / "fig13_replot.png", dpi=150)
