"""Re-plot Supplementary Fig. 12 of Pesce et al. 2022 from sfig12.csv -> sfig12_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"CR": "#00ff00", "SST": "#eac429", "NeuN": "#ff0000"}
with open(os.path.join(HERE, "sfig12.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
bars = [r for r in rows if r["row_type"] == "bar"]
pts = [r for r in rows if r["row_type"] == "point"]
markers = ["CR", "SST", "NeuN"]
conds = []
for r in bars:
    if r["condition"] not in conds:
        conds.append(r["condition"])
xpos = {(r["marker"], r["condition"]): markers.index(r["marker"]) * 4 + conds.index(r["condition"]) for r in bars}
fig, ax = plt.subplots(figsize=(8, 3.8))
for r in bars:
    x = xpos[(r["marker"], r["condition"])]
    m, sd = float(r["mean"]), float(r["sd"])
    ax.bar(x, m, width=0.64, color=COL[r["marker"]], edgecolor="0.25", lw=1.5)
    ax.plot([x, x], [m, m + sd], color="0.25", lw=1.5)
    ax.plot([x - 0.16, x + 0.16], [m + sd, m + sd], color="0.25", lw=1.5)
for r in pts:
    x = xpos[(r["marker"], r["condition"])]
    ax.plot(x, float(r["value"]), "o", color="0.3", alpha=0.45, ms=7, mec="none")
for mk, sig, y in (("CR", "**", 8.9), ("NeuN", "*", 4.0)):      # brackets as printed (over the first two bars)
    x0, x1 = xpos[(mk, conds[0])], xpos[(mk, conds[1])]
    ax.plot([x0, x1], [y, y], color="k", lw=2)
    ax.text((x0 + x1) / 2, y + 0.1, sig, ha="center", va="bottom", fontsize=12)
ax.set_xticks([xpos[(mk, c)] for mk in markers for c in conds])
ax.set_xticklabels([c.replace(" after", "\nafter").replace("LSFM ", "LSFM\n") for mk in markers for c in conds], fontsize=6, fontweight="bold")
ax.set_xlim(-1, 11)
ax.set_ylim(0, 9.5)
ax.set_yticks(range(0, 9, 2))
ax.set_ylabel("Signal retained", fontweight="bold")
for mk in markers:
    ax.text(markers.index(mk) * 4 + 1, 9.2, mk, ha="center", color=COL[mk], fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig12_replot.png"), dpi=150)
