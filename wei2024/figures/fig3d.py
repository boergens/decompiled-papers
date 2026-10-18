"""Re-plot Fig. 3d from figures/fig3d.csv -> figures/fig3d_replot.png (same axes as the paper)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CSV = HERE / "fig3d.csv"
OUT = HERE / "fig3d_replot.png"

rows = [r for r in csv.reader(l for l in open(CSV) if not l.startswith("#"))]
hdr, rows = rows[0], rows[1:]
i = {k: n for n, k in enumerate(hdr)}
fig, ax = plt.subplots(figsize=(5.2, 4.2))
for name, col in (("9-6 LJ", "#5b9bd5"), ("12-6 LJ (Fitting)", "#ed7d31")):
    line = sorted((float(r[i["r_A"]]), float(r[i["E_kcal_per_mol"]])) for r in rows if r[i["series"]] == name and r[i["kind"]] == "line")
    mk = [(float(r[i["r_A"]]), float(r[i["E_kcal_per_mol"]])) for r in rows if r[i["series"]] == name and r[i["kind"]] == "marker"]
    if line:
        ax.plot(*zip(*line), ".", ms=1.5, color=col, label=name)
    if mk:
        ax.plot(*zip(*mk), "o", ms=5, mfc="none", color=col)
ax.set_xlim(0, 15)
ax.set_ylim(-0.1, 0.5)
ax.set_xticks(range(0, 16, 3))
ax.grid(color="#d9d9d9")
ax.set_xlabel("r (Å)")
ax.set_ylabel("E (kcal/mol)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=2, frameon=False)
ax.set_title("(d)", y=-0.25)
fig.tight_layout()
fig.savefig(OUT, dpi=150)
