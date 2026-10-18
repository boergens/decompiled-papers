"""Re-plot Fig. 1k of Kubota et al. 2018 from fig1k.csv -> fig1k_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig1k.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
x = [float(r["days"]) for r in rows]
y = [float(r["pwca_deg"]) for r in rows]
lo = [y[i] - float(r["sd_lower_deg"]) for i, r in enumerate(rows)]
hi = [float(r["sd_upper_deg"]) - y[i] for i, r in enumerate(rows)]
fig, ax = plt.subplots(figsize=(4, 2.8))
ax.errorbar(x, y, yerr=[lo, hi], fmt="o-", color="k", ms=5, lw=1.2, capsize=3)
ax.set_xlim(-2.2, 15.2)
ax.set_ylim(-2, 92)
ax.set_xticks([-1, 0, 1, 2, 3, 7, 14])
ax.set_xticks(range(-2, 16), minor=True)
ax.set_yticks([0, 20, 40, 60, 80])
ax.set_yticks(range(0, 91, 10), minor=True)
ax.text(12.5, 22, "n = 3")
ax.set_xlabel("Days after plasma treatment")
ax.set_ylabel("Pure water contact angle (°)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1k_replot.png"), dpi=150)
