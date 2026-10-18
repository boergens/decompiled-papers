"""Re-plot Figure 4C of Tegethoff & Briggman 2024 from fig4c.csv -> fig4c_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig4c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"F_S 50 nm": "#1e69af", "F_S 35 nm": "#6eb9dc", "F_T 50 nm": "#a51e2d", "F_T 35 nm": "#d25519"}
fig, ax = plt.subplots(figsize=(3.2, 2.6))
for s, c in COL.items():
    r = [x for x in rows if x["series"] == s]
    ax.plot([float(x["time_s"]) for x in r], [float(x["force_mN_per_mm_mid"]) for x in r], ".", ms=1.5, color=c, label=s)
ax.set_xlim(0, 1.6)
ax.set_ylim(-8, 68)
ax.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
ax.set_yticks([0, 20, 40, 60])
ax.legend(frameon=False, fontsize=7, markerscale=4)
ax.set_xlabel("time (sec)")
ax.set_ylabel("force (mN/mm)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4c_replot.png"), dpi=150)
