"""Re-plot Figure 9 of Fu et al. 2025 from fig9.csv -> fig9_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
STYLE = {"Plain PMMA": ("#505050", "s"), "PMMA/0.1 wt% CNT": ("#ff4444", "o"), "PMMA/0.2 wt% CNT": ("#1166dd", "^"),
         "PMMA/0.5 wt% CNT": ("#33aa66", "v"), "PMMA/1.0 wt% CNT": ("#bb77dd", "D")}
data = {}
with open(HERE / "fig9.csv") as f:
    for r in csv.DictReader(line for line in f if not line.startswith("#")):
        data.setdefault(r["series"], []).append(r)
fig, ax = plt.subplots(figsize=(5, 4))
for name, rs in data.items():
    col, mk = STYLE[name]
    x = [float(r["chip_thickness_nm"]) for r in rs]
    y = [float(r["force_N_per_m"]) for r in rs]
    ax.plot(x, y, "-", marker=mk, color=col, lw=2, ms=7, label=name)
    for r in rs:
        if r["err_top"] and r["err_bottom"]:
            xv = float(r["chip_thickness_nm"])
            ax.errorbar([xv], [float(r["force_N_per_m"])],
                        yerr=[[float(r["force_N_per_m"]) - float(r["err_bottom"])],
                              [float(r["err_top"]) - float(r["force_N_per_m"])]],
                        color=col, capsize=4, lw=1.5)
ax.set_xlim(50, 210)
ax.set_ylim(0, 80)
ax.set_yticks([0, 25, 50, 75])
ax.set_xticks([50, 100, 150, 200])
ax.set_xlabel("Undeformed chip thickness (nm)")
ax.set_ylabel("Resultant cutting force (N/m)")
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(HERE / "fig9_replot.png", dpi=150)
