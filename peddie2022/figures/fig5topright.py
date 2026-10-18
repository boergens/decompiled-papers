#!/usr/bin/env python3
"""Re-plot Figure 5 (top-right histogram) from fig5topright.csv -> fig5topright_replot.png."""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig5topright.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
fig, ax = plt.subplots(figsize=(4.6, 2.9))
for r in rows:
    l, rr, c = float(r["bin_left"]), float(r["bin_right"]), float(r["count"])
    ax.bar(l, c, width=rr - l, align="edge", color="tab:blue")
ax.set_xlim(-5, 101)
ax.set_ylim(0, 28.5)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 5, 10, 15, 20, 25])
ax.set_xlabel("Mitochondria volume (10$^3$ pixels)")
ax.set_ylabel("Count")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "fig5topright_replot.png", dpi=150)
