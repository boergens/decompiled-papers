"""Re-plot Figure 6F of Tegethoff & Briggman 2024 from fig6f.csv -> fig6f_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"LX 112": "#EDB120", "Spurr's": "#77AC30"}
with open(os.path.join(HERE, "fig6f.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
order = [("LX 112", "0.3"), ("LX 112", "0.6"), ("LX 112", "1.2"), ("Spurr's", "0.3"), ("Spurr's", "0.6"), ("Spurr's", "1.2")]
fig, ax = plt.subplots(figsize=(4.2, 3.0))
for r in rows:
    x = order.index((r["series"], r["speed_mm_s"])) + 1 + float(r["x_offset"])
    ax.plot(x, float(r["compression_percent"]), "o", ms=2.5, color=COL[r["series"]])
ax.set_xlim(0, 7)
ax.set_xticks(range(1, 7))
ax.set_xticklabels([o[1] for o in order])
ax.set_ylim(0, 35)
ax.set_yticks([0, 10, 20, 30])
ax.grid(axis="y", color="0.92")
ax.set_xlabel("cutting speed (mm/s)")
ax.set_ylabel("section compression (%)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig6f_replot.png"), dpi=150)
