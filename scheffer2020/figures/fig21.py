"""Re-plot Fig. 21 from fig21.csv -> fig21_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig21.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
ob = [(float(r["x"]), float(r["y"])) for r in rows if r["series"] == "observed"]
fit = sorted((float(r["x"]), float(r["y"])) for r in rows if r["series"] == "rough fit")
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot([p[0] for p in ob], [p[1] for p in ob], "+", color="#0773b4", ms=5, label="observed")
ax.plot([p[0] for p in fit], [p[1] for p in fit], "-", color="#d56128", lw=1.5, label="rough fit")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.8, 1000); ax.set_ylim(0.6, 1e7)
ax.set_xlabel("Strength of connection"); ax.set_ylabel("Number of links with specified strength")
ax.set_title("Number of connections vs strength of connection")
ax.grid(True, color="w"); ax.set_facecolor("#f2f2f3"); ax.legend(loc="upper right")
fig.tight_layout(); fig.savefig(HERE / "fig21_replot.png", dpi=100)
