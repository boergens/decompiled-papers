"""Re-plot fig4b from figures/fig4b.csv -> figures/fig4b_replot.png (solid series as dots, dashed series as x; vertical ticks = upper..lower)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
data = {}
for r in csv.DictReader(line for line in open(HERE / "fig4b.csv") if not line.startswith("#")):
    d = data.setdefault(r["series"], ([], [], [], []))
    d[0].append(float(r["r_A"]))
    d[1].append(float(r["density_mid"]))
    d[2].append(float(r["density_upper"]))
    d[3].append(float(r["density_lower"]))
STYLE = {"MTHPA": ("black", "."), "NA": ("red", "."), "DGEBA-MTHPA": ("#555555", "x"), "DGEBA-NA": ("#ff8080", "x")}
fig, ax = plt.subplots(figsize=(5.6, 4.1))
for s, (col, ls) in STYLE.items():
    x, y, yu, yl = data[s]
    ax.vlines(x, yl, yu, color=col, lw=0.6)
    ax.plot(x, y, ls, color=col, ms=1.2, label=s)
ax.set_xlim(1.0, 1.6)
ax.set_ylim(-3.2, 40.2)
ax.set_xlabel("r(Å)")
ax.set_ylabel("Probability density")
ax.legend(loc="upper left", fontsize=8, markerscale=4)
ax.text(0.97, 0.96, "(b)", transform=ax.transAxes, ha="right", va="top", fontsize=13, weight="bold")
fig.tight_layout()
fig.savefig(HERE / "fig4b_replot.png", dpi=150)
