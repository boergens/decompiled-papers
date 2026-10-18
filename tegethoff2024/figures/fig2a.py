"""Re-plot Figure 2A of Tegethoff & Briggman 2024 from fig2a.csv -> fig2a_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig2a.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"medium hard": "#0072BD", "hard": "#D95319", "very hard": "#808080", "LX 112": "#EDB120",
       "Durcupan": "#7E2F8E", "Spurr's": "#77AC30"}
fig, ax = plt.subplots(figsize=(5, 2.6))
for s, c in COL.items():
    r = [x for x in rows if x["series"] == s]
    ax.plot([float(x["x_tick"]) for x in r], [float(x["hardness_HV"]) for x in r], "o", ms=1.8, color=c, label=s)
ax.set_xlim(0, 29)
ax.set_ylim(9, 19)
ax.set_xticks(range(1, 29))
ax.set_xticklabels([])
ax.set_yticks(range(10, 19, 2))
ax.set_yticks(range(9, 20), minor=True)
ax.grid(axis="y", which="both", color="0.92")
ax.set_ylabel("Hardness (HV)")
for s, xm in [("medium\nhard", 3.5), ("hard", 8.5), ("very\nhard", 13), ("LX 112", 17), ("Durcupan", 21.5), ("Spurr's", 26.5)]:
    ax.text(xm, 8.2, s, ha="center", va="top", fontsize=8, color=list(COL.values())[[ "medium\nhard","hard","very\nhard","LX 112","Durcupan","Spurr's"].index(s)])
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2a_replot.png"), dpi=150)
