"""Re-plot Figure 3(a) of Wei et al. 2025 from fig3a.csv -> fig3a_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig3a.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
tr = [r for r in rows if r["kind"] == "trace"]
sy = [r for r in rows if r["kind"] == "symbol"]
fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.fill_between([float(r["time_ps"]) for r in tr], [float(r["E_lower_kcal_mol"]) for r in tr],
                [float(r["E_upper_kcal_mol"]) for r in tr], color="red", lw=0, alpha=0.3)
ax.plot([float(r["time_ps"]) for r in tr], [float(r["E_kcal_mol"]) for r in tr], "-", color="red", lw=1, label="trace")
ax.plot([float(r["time_ps"]) for r in sy], [float(r["E_kcal_mol"]) for r in sy], "o", ms=3.5, mfc="white", mec="red",
        label="symbols")
ax.set_xlim(-100, 1100)
ax.set_ylim(-110000, 0)
ax.set_xticks([0, 200, 400, 600, 800, 1000])
ax.set_yticks([0, -20000, -40000, -60000, -80000, -100000])
ax.set_xlabel("Time (ps)")
ax.set_ylabel("Total energy (kcal/mol)")
ax.legend(loc="lower right", fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig3a_replot.png", dpi=150)
