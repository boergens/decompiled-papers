"""Re-plot Figure 2C of Tegethoff & Briggman 2024 from fig2c.csv -> fig2c_replot.png
(y: the primary, tick-mark calibration; see the CSV header for the label/tick mismatch of the original)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig2c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 2.8))
ax.plot([float(r["bdma_percent"]) for r in rows], [float(r["hardness_HV"]) for r in rows], "o", ms=1.8, color="k")
ax.set_xlim(0, 5.75)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(["1.0", "2.0", "3.0", "4.0", "5.0"])
ax.set_ylim(8, 12.5)
ax.set_yticks([9, 10, 11, 12])
ax.set_yticks([8 + 0.5 * i for i in range(10)], minor=True)
ax.grid(axis="y", which="both", color="0.92")
ax.set_xlabel("BDMA concentration (%)")
ax.set_ylabel("Hardness (HV)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2c_replot.png"), dpi=150)
