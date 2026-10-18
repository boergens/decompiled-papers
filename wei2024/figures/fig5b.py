"""Re-plot Fig. 5b from figures/fig5b.csv -> figures/fig5b_replot.png (line centre with its upper/lower band)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
rows = list(csv.reader(l for l in open(HERE / "fig5b.csv") if not l.startswith("#")))
hdr, rows = rows[0], rows[1:]
i = {k: n for n, k in enumerate(hdr)}
fig, ax = plt.subplots(figsize=(5.0, 4.0))
for s, c in (("x", "k"), ("y", "r"), ("z", "m")):
    pts = sorted((float(r[i["tensile_strain"]]), float(r[i["total_energy_kcal_per_mol"]]), float(r[i["upper"]]), float(r[i["lower"]])) for r in rows if r[i["series"]] == s)
    x = [p[0] for p in pts]
    ax.vlines(x, [p[3] for p in pts], [p[2] for p in pts], color=c, lw=0.5, alpha=0.5)
    ax.plot(x, [p[1] for p in pts], ".", ms=1.5, color=c, label=s)
ax.set_xlim(-0.025, 0.325)
ax.set_ylim(-3750, 0)
ax.set_xticks([0, .05, .1, .15, .2, .25, .3])
ax.set_xlabel("Tensile strain")
ax.set_ylabel("Total energy (kcal/mol)")
ax.legend(title="Tensile direction", frameon=False)
ax.set_title("(b) Total energy-tensile strain", y=-0.25, fontsize=9)
fig.tight_layout()
fig.savefig(HERE / "fig5b_replot.png", dpi=150)
