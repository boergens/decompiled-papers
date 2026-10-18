"""Re-plot fig10b from figures/fig10b.csv -> figures/fig10b_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(line for line in open(HERE / "fig10b.csv") if not line.startswith("#")))
f = lambda s: float(s) if s else float("nan")
fig, ax = plt.subplots(figsize=(5.8, 4.1))
mk = [r for r in rows if r["kind"] == "marker"]
x = [f(r["x_K"]) for r in mk]
y = [f(r["y"]) for r in mk]
if mk[0]["y_err_low"]:
    lo = [f(r["y"]) - f(r["y_err_low"]) for r in mk]
    hi = [f(r["y_err_high"]) - f(r["y"]) for r in mk]
    ax.errorbar(x, y, yerr=[lo, hi], fmt="s", color="black", ms=4, capsize=4, lw=0.8, label="MSD")
else:
    ax.plot(x, y, "s", color="black", ms=6, label="MSD")
for name in ("line_low", "line_high"):
    L = [r for r in rows if r["kind"] == name]
    ax.plot([f(r["x_K"]) for r in L], [f(r["y"]) for r in L], "-", color="red", lw=1)
d = [r for r in rows if r["kind"] == "dot"][0]
lab = [r for r in rows if r["kind"] == "label"][0]
ax.plot(f(d["x_K"]), f(d["y"]), "o", color="red", ms=6)
ax.annotate("%sK" % lab["x_K"].rstrip("0").rstrip(".") if False else "419.46K", (f(d["x_K"]), f(d["y"])), xytext=(8, -14), textcoords="offset points")
ax.set_xlim(275, 625)
ax.set_ylim(0.5, 3.5)
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("MSD(Å$^2$)")
ax.legend(loc="upper left", fontsize=8)
ax.text(0.98, 0.97, "(b)", transform=ax.transAxes, ha="right", va="top", fontsize=14, weight="bold")
fig.tight_layout()
fig.savefig(HERE / "fig10b_replot.png", dpi=150)
