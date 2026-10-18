"""Re-plot Figure 4D (main plot) of Tegethoff & Briggman 2024 from fig4d.csv -> fig4d_replot.png (envelope per column)"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig4d.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(3.6, 2.8))
t = [float(r["time_s"]) for r in rows]
ax.vlines(t, [float(r["force_min"]) for r in rows], [float(r["force_max"]) for r in rows], color="#1f6fb8", lw=0.6)
ax.set_xlim(0, 900)
ax.set_ylim(-60, 80)
ax.set_xticks([0, 300, 600, 900])
ax.set_yticks(range(-60, 81, 20))
ax.set_xlabel("time (sec)")
ax.set_ylabel("force (mN/mm)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4d_replot.png"), dpi=150)
