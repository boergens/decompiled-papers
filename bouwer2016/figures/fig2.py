"""Re-plot Fig. 2 of Bouwer et al. 2016 from fig2.csv -> fig2_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
x, y = [], []
with open(HERE / "fig2.csv") as f:
    for r in csv.DictReader(l for l in f if not l.startswith("#")):
        x.append(float(r["applied_potential_V"]))
        y.append(float(r["measured_sample_potential_V"]))
fig, ax = plt.subplots(figsize=(4.5, 4.5))
ax.plot(x, y, "o", mfc="none", mec="k", ms=5, label="Measured Sample Surface Potential", clip_on=False)
ax.set_xlim(-1500, 0)
ax.set_ylim(-1400, 0)
ax.set_xticks([-1500, -1000, -500, 0])
ax.set_yticks(range(-1400, 1, 200))
ax.grid(color="#8080c0", lw=0.6)
ax.set_xlabel("Applied Potential (Volts)")
ax.set_ylabel("Measured Sample Potential (Volts)")
ax.set_title("Applied Voltage Vs. Sample Surface Voltage")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig2_replot.png", dpi=150)
