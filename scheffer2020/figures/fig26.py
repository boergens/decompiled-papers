"""Re-plot Fig. 26 from fig26.csv -> fig26_replot.png (compartment labels at their positions, bound lines, band edges)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
with open(HERE / "fig26.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fits = {r["label"]: (float(r["p"]), float(r["c"])) for r in rows if r["kind"] == "line_fit"}
T = np.logspace(2, 6, 200)
fig, ax = plt.subplots(figsize=(9, 6.6))
ln = lambda k: fits[k][1] * T ** fits[k][0]
ax.fill_between(T, ln("blue line (lower bound)"), ln("green line (upper bound)"), color="#ffffe3")
ax.fill_between(T, ln("3D bottom (mid grey lower edge)"), ln("3D top (light grey upper edge)"), color="#e5e5e5")
ax.fill_between(T, ln("2D bottom (olive lower edge)"), ln("2D top (mid grey upper edge)"), color="#e5e5ce")
ax.fill_between(T, ln("3D bottom (mid grey lower edge)"), ln("2D top (mid grey upper edge)"), color="#cfcfd1")
ax.plot(T, ln("green line (upper bound)"), color="#36fe28", lw=1)
ax.plot(T, ln("blue line (lower bound)"), color="#0b0bf7", lw=1)
for r in rows:
    if r["kind"] == "compartment":
        ax.text(float(r["x"]), float(r["y"]), r["label"], ha="center", va="center", fontsize=8,
                color="k" if r["status"].startswith(("isolated", "overlapping")) else "r")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(100, 1e6); ax.set_ylim(1, 1e6)
ax.set_xlabel("Tbars"); ax.set_ylabel("Neurons shared with other compartments"); ax.set_title("Rent's rule for hemibrain")
fig.tight_layout(); fig.savefig(HERE / "fig26_replot.png", dpi=100)
