"""Re-plot Figure 3(b) of Wei et al. 2025 from fig3b.csv -> fig3b_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig3b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.6, 3.6))
for name, col in (("Thermostat layer", "black"), ("Newtonian layer", "red")):
    tr = [r for r in rows if r["series"] == name and r["kind"] == "trace"]
    ax.fill_between([float(r["time_ps"]) for r in tr], [float(r["T_lower_K"]) for r in tr],
                    [float(r["T_upper_K"]) for r in tr], color=col, lw=0, alpha=0.3)
    ax.plot([float(r["time_ps"]) for r in tr], [float(r["T_K"]) for r in tr], "-", color=col, lw=1, label=name)
sy = [r for r in rows if r["kind"] == "symbol"]
ax.plot([float(r["time_ps"]) for r in sy], [float(r["T_K"]) for r in sy], "D", ms=3, mfc="white", mec="red",
        label="Newtonian layer symbols")
ax.set_xlim(-100, 1100)
ax.set_ylim(140, 320)
ax.set_xticks([0, 200, 400, 600, 800, 1000])
ax.set_yticks(range(140, 321, 20))
ax.set_xlabel("Time (ps)")
ax.set_ylabel("Temperature (K)")
ax.legend(loc="center right", fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig3b_replot.png", dpi=150)
