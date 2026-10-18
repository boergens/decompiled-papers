"""Re-plot Fig. 4d of Kubota et al. 2018 from fig4d.csv -> fig4d_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig4d.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(1.6, 2.8))
x = range(len(rows))
ax.bar(x, [float(r["total_light_transmittance_pct_bar"]) for r in rows], color=["red", "#1f4fff", "black"], edgecolor="black", width=0.75)
for i, r in enumerate(rows):
    ax.text(i, float(r["total_light_transmittance_pct_bar"]) + 100 * 0.02, r["printed_value"], ha="center", va="bottom", fontsize=8)
ax.set_xticks(list(x))
ax.set_xticklabels([r["tape"] for r in rows], rotation=45, ha="right")
ax.set_ylim(0, 100)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_ylabel("Total light ransmittance (%)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4d_replot.png"), dpi=150)
