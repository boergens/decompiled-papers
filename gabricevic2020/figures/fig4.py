"""Re-plot Figure 4 of Gabričević et al. 2020 from fig4.csv -> fig4_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gab_common import read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "fig4.csv"))
style = {"TCE": ("v", "green"), "trans-DCE": ("o", "red"), "cis-DCE": ("D", "blue")}
fig, ax = plt.subplots(figsize=(6, 4.3))
for name, (mk, c) in style.items():
    r = [x for x in rows if x["series"] == name]
    ax.plot([float(x["substrate_mol_dm3"]) for x in r], [float(x["kobs_s-1"]) for x in r], mk, color=c, ls="", label=name)
ax.set_xlim(0, 0.0215)
ax.set_ylim(0, 0.75)
ax.set_xticks([0, 0.005, 0.010, 0.015, 0.020])
ax.set_yticks([0, 0.2, 0.4, 0.6])
ax.set_xlabel("[Substrate] (mol/dm$^3$)")
ax.set_ylabel("$k_\\mathrm{obs}$ (s$^{-1}$)")
ax.legend(loc="lower left", bbox_to_anchor=(0.12, 0.05), frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4_replot.png"), dpi=150)
