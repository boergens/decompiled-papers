"""Re-plot Figure 6E of Tegethoff & Briggman 2024 from fig6e.csv -> fig6e_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"LX 112": "#EDB120", "M Epon": "#A2142F", "MH Epon": "#0072BD", "H Epon": "#D95319", "VH Epon": "#4DBEEE",
       "Durcupan": "#7E2F8E", "Spurr's": "#77AC30"}
with open(os.path.join(HERE, "fig6e.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.2, 3.0))
for r in rows:
    c = COL[r["series"]]
    kw = dict(mfc="none", mec=c) if r["marker"] == "open" else dict(color=c)
    ax.plot(float(r["mean_FR_mN_per_mm"]), float(r["compression_percent"]), "o", ms=2.5, **kw)
ax.text(83.9, 22.5, "*", ha="center")
ax.set_xlim(45, 90)
ax.set_xticks([45, 55, 65, 75, 85])
ax.set_ylim(0, 35)
ax.set_yticks([0, 10, 20, 30])
ax.grid(axis="y", color="0.92")
ax.set_xlabel("mean F_R (mN/mm)")
ax.set_ylabel("section compression (%)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig6e_replot.png"), dpi=150)
