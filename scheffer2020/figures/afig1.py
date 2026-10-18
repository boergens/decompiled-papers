"""Re-plot Appendix 1-figure 1 from afig1.csv -> afig1_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "afig1.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"initial": "tab:blue", "cascade": "tab:orange", "hybrid": "tab:red", "synful+": "tab:green"}
fig, ax = plt.subplots(figsize=(5.6, 5.6))
for s, c in COL.items():
    p = sorted((float(r["x"]), float(r["y"])) for r in rows if r["series"] == s)
    if p:
        ax.plot([q[0] for q in p], [q[1] for q in p], ".", ms=2, color=c, label=s)
m = [r for r in rows if r["series"] == "manual estimated"]
ax.plot([float(r["x"]) for r in m], [float(r["y"]) for r in m], "o", ms=10, color="tab:purple", label="manual estimated")
ax.set_xlim(0.2, 1.0)
ax.set_ylim(0.85, 1.0)
ax.set_xlabel("recall"); ax.set_ylabel("precision"); ax.grid(True); ax.legend(loc="upper right")
fig.tight_layout(); fig.savefig(HERE / "afig1_replot.png", dpi=100)
