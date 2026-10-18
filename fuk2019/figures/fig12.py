"""Re-plot Fig. 12 from figures/fig12.csv -> figures/fig12_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(line for line in open(HERE / "fig12.csv") if not line.startswith("#")))
systems = ["DGEBA/MTHPA", "DGEBA/NA"]
fig, ax = plt.subplots(figsize=(4.4, 3.4))
for k, (ser, col, hatch) in enumerate([("Experimental", "#118888", "\\\\\\\\"), ("Simulated", "#22a0cc", "\\\\\\\\")]):
    rs = [next(r for r in rows if r["system"] == s and r["series"] == ser) for s in systems]
    xs = [i + (k - 0.5) * 0.4 for i in range(2)]
    ys = [float(r["modulus_GPa"]) for r in rs]
    err = [[float(r["err_low_GPa"]) for r in rs], [float(r["err_high_GPa"]) for r in rs]]
    ax.bar(xs, ys, width=0.4, color=col, hatch=hatch, edgecolor="black", label=ser, yerr=err, capsize=4)
    for x, r in zip(xs, rs):
        ax.text(x, float(r["modulus_GPa"]) + float(r["err_high_GPa"]) + 0.08, r["printed_label"], ha="center")
ax.set_xticks(range(2), systems)
ax.set_xlim(-0.6, 1.6)
ax.set_ylim(0, 6)
ax.set_ylabel("Young Modulus (GPa)")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(HERE / "fig12_replot.png", dpi=150)
