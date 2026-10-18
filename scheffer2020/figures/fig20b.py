"""Re-plot Fig. 20(b) from fig20b.csv -> fig20b_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig20b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"Threshold 1": "#0773b4", "Threshold 3": "#cc79a8", "Threshold 5": "#189f74", "Threshold 10": "#d56128",
       "Threshold 20": "#e7a023", "Human designed": "k"}
fig, ax = plt.subplots(figsize=(7, 5.5))
for s, c in COL.items():
    tr = sorted((float(r["x"]), float(r["y"])) for r in rows if r["series"] == s and r["kind"] == "trace")
    if not tr:
        continue
    if s == "Human designed":
        ax.plot([t[0] for t in tr], [t[1] for t in tr], ".", ms=1.5, color=c, label=s)
    else:
        ax.plot([t[0] for t in tr], [t[1] for t in tr], ".", ms=1, color=c, label=s)
    vx = [(float(r["x"]), float(r["y"])) for r in rows if r["series"] == s and r["kind"] == "vertex"]
    if vx:
        ax.plot([v[0] for v in vx], [v[1] for v in vx], "o", ms=3, color=c)
if "b" == "b":
    ax.set_xscale("log")
    ax.set_xlim(1, 200)
else:
    ax.set_xlim(0, 8)
ax.set_ylim(0, 1)
ax.set_xlabel("Number of interneurons needed")
ax.set_ylabel("Fraction of all possible pairs connected")
ax.set_title("(b) Fraction of paths vs synaptic distance")
ax.grid(True, color="w")
ax.set_facecolor("#f2f2f3")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig20b_replot.png", dpi=100)
