"""Re-plot Figure 3A of Tegethoff & Briggman 2024 from fig3a.csv -> fig3a_replot.png (broken x axis as two panels)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig3a.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"24 hr cure": "#0072BD", "48 hr cure": "#D95319", "72 hr cure": "#808080"}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5, 3), sharey=True, gridspec_kw={"width_ratios": [4.5, 2.2], "wspace": 0.05})
for s, c in COL.items():
    r = [x for x in rows if x["series"] == s]
    for ax in (a1, a2):
        ax.plot([float(x["x_days"]) for x in r], [float(x["hardness_HV"]) for x in r], "o", ms=1.8, color=c, label=s + ", 70C")
a1.set_xlim(-0.66, 4.4)
a2.set_xlim(28.0, 35.0)
a1.set_xticks([0, 1, 2, 3])
a2.set_xticks([30, 31, 32])
a2.set_xticklabels(["30", "", "32"])
a1.set_ylim(8.5, 15)
for ax in (a1, a2):
    ax.grid(axis="y", color="0.92")
a2.tick_params(left=False)
a1.set_ylabel("Hardness (HV)")
a1.legend(frameon=False, fontsize=7, loc="upper left", handlelength=0.5)
a1.set_xlabel("Days post cure", x=0.75)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3a_replot.png"), dpi=150)
