"""Re-plot Appendix 1-figure 3 from afig3.csv.gz -> afig3_replot.png (each coloured source pixel as a small square)."""
import csv
import gzip
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

HERE = Path(__file__).resolve().parent
with gzip.open(HERE / "afig3.csv.gz", "rt") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
x = [float(r["x"]) for r in rows]; y = [float(r["y"]) for r in rows]; c = [float(r["freq"]) for r in rows]
fig, ax = plt.subplots(figsize=(7, 5.6))
sc = ax.scatter(x, y, c=c, s=1, marker="s", cmap="plasma", norm=LogNorm(1, 8.7e5), linewidths=0)
ax.set_xlim(0, 500); ax.set_ylim(0, 500); ax.grid(True)
ax.set_xlabel("cascade synapse count"); ax.set_ylabel("synful+ synapse count")
fig.colorbar(sc, label="neuron pair frequency")
fig.tight_layout(); fig.savefig(HERE / "afig3_replot.png", dpi=100)
