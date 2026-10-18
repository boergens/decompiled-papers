"""Re-plot Figure 6C of Tegethoff & Briggman 2024 from fig6c.csv -> fig6c_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"LX 112": "#EDB120", "M Epon": "#A2142F", "MH Epon": "#0072BD", "H Epon": "#D95319", "VH Epon": "#4DBEEE",
       "Durcupan": "#7E2F8E", "Spurr's": "#77AC30"}
with open(os.path.join(HERE, "fig6c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.2, 3.0))
for s, c in COL.items():
    r = [x for x in rows if x["series"] == s]
    ax.plot([float(x["hardness_HV"]) for x in r], [float(x["compression_percent"]) for x in r], "o", ms=2.5, color=c, label=s)
ax.text(17.7, 23, "*", ha="center")
ax.set_xlim(12, 18)
ax.set_ylim(0, 35)
ax.set_yticks([0, 10, 20, 30])
ax.grid(axis="y", color="0.92")
ax.set_xlabel("hardness (HV)")
ax.set_ylabel("section compression (%)")
ax.legend(frameon=False, fontsize=6, loc="upper right", bbox_to_anchor=(0.9, 1.0))
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig6c_replot.png"), dpi=150)
