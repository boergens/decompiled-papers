"""Re-plot Fig. 5c from figures/fig5c.csv -> figures/fig5c_replot.png (line centre with its upper/lower band)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
rows = list(csv.reader(l for l in open(HERE / "fig5c.csv") if not l.startswith("#")))
hdr, rows = rows[0], rows[1:]
i = {k: n for n, k in enumerate(hdr)}
fig, ax = plt.subplots(figsize=(5.0, 4.0))
for s, c in (("x", "k"), ("y", "r"), ("z", "m")):
    pts = sorted((float(r[i["tensile_strain"]]), float(r[i["density"]]), float(r[i["upper"]]), float(r[i["lower"]])) for r in rows if r[i["series"]] == s)
    x = [p[0] for p in pts]
    ax.vlines(x, [p[3] for p in pts], [p[2] for p in pts], color=c, lw=0.5, alpha=0.5)
    ax.plot(x, [p[1] for p in pts], ".", ms=1.5, color=c, label=s)
ax.set_xlim(-0.025, 0.325)
ax.set_ylim(1.090, 1.1315)
ax.set_xticks([0, .05, .1, .15, .2, .25, .3])
ax.set_xlabel("Tensile strain")
ax.set_ylabel("Density (kg/m3)")
ax.legend(title="Tensile direction", frameon=False)
ax.set_title("(c) Density-tensile strain", y=-0.25, fontsize=9)
fig.tight_layout()
fig.savefig(HERE / "fig5c_replot.png", dpi=150)
