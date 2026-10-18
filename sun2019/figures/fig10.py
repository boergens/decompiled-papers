"""Re-plot Figure 10 of Sun & Gamstedt 2019 from fig10.csv -> fig10_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig10.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))


def series(name):
    rr = [r for r in rows if r["series"] == name]
    return [float(r["cutting_speed_mm_s"]) for r in rr], [float(r["shear_stress_MPa"]) for r in rr]


fig, ax = plt.subplots(figsize=(5, 3.8))
ax.plot(*series("tau_PSZ"), color="red", lw=1.2, label=r"$\tau_\mathrm{PSZ}$")
x, y = series("tau_Bulk")
ax.plot(x, y, "k.", ms=1.5, label=r"$\tau_\mathrm{Bulk}$ (dashed in the paper)")
vx = [float(r["cutting_speed_mm_s"]) for r in rows if r["series"] == "critical line"][0]
ax.axvline(vx, color="0.4", lw=0.8)
ax.text(1.5, 118, "Critical $v_0$ = 4.7 mm/s (line as drawn)")
ax.set_xlim(0, 10)
ax.set_ylim(113, 140)
ax.set_yticks(range(115, 141, 5))
ax.set_xlabel("Cutting speed $v_0$, mm/s")
ax.set_ylabel(r"Shear stress $\tau$, MPa")
ax.legend(loc="center right", frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig10_replot.png", dpi=150)
