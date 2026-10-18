"""Re-plot Fig. 2c of Zhao et al. 2025 from fig2c.csv -> fig2c_replot.png"""
import csv
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
txt = open(HERE / "fig2c.csv").read()
e1, e2 = map(float, re.search(r"edges are at lambda ([\d.]+) and ([\d.]+)", txt).groups())
with open(HERE / "fig2c.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(3.8, 2.8))
ax.axvspan(1.0, e1, color="#eff6fb"); ax.axvspan(e1, e2, color="#ddecf7"); ax.axvspan(e2, 1.5, color="#bfdaef")
col = {"Crack extension energy": "#ffbe7a", "Blade contribution": "#2878b5", "Stretch contribution": "red"}
frac = {r["series"]: r for r in rows if r["series"].startswith("Fracture")}
exitp = [r for r in rows if "leaves the top" in r["series"]][0]
for s, c in col.items():
    rr = [r for r in rows if r["series"] == s]
    x = [float(r["lambda"]) for r in rr]; y = [float(r["G_J_m2"]) for r in rr]
    if s == "Crack extension energy":
        x = [float(exitp["lambda"])] + x; y = [float(exitp["G_J_m2"])] + y
    fr = [v for k, v in frac.items() if ("Blade" in k) == (s == "Blade contribution")][0]
    x.append(float(fr["lambda"])); y.append(float(fr["G_J_m2"]))
    ax.plot(x, y, "-", color=c)
    ax.plot([float(r["lambda"]) for r in rr], [float(r["G_J_m2"]) for r in rr], "s", color=c, ms=5, label=s)
    for r in rr:
        if r["err_low"]:
            v = float(r["G_J_m2"])
            ax.errorbar([float(r["lambda"])], [v], yerr=[[v - float(r["err_low"])], [float(r["err_high"]) - v]],
                        color="#41a0dd", capsize=3, lw=0.8)
for k, r in frac.items():
    ax.plot([float(r["lambda"])], [float(r["G_J_m2"])], "X", color="k", ms=6,
            label="Fracture without blade" if "Blade" in k else None)
ax.set_xlim(1, 1.5); ax.set_ylim(0, 1200)
ax.set_xticks([1, 1.1, 1.2, 1.3, 1.4, 1.5]); ax.set_yticks([0, 400, 800, 1200])
ax.set_xlabel("λ"); ax.set_ylabel("G, G$_1$, and G$_2$ (J m$^{-2}$)")
ax.legend(fontsize=6, loc="upper right")
fig.tight_layout()
fig.savefig(HERE / "fig2c_replot.png", dpi=150)
