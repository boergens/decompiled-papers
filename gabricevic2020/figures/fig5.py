"""Re-plot Figure 5 of Gabričević et al. 2020 from fig5.csv -> fig5_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gab_common import read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "fig5.csv"))
fig, ax = plt.subplots(figsize=(6, 4.4))
line = [r for r in rows if r["kind"] == "line"]
ax.plot([float(r["OH_mol_dm3"]) for r in line], [float(r["kobs_s-1"]) for r in line], "-", color="black", lw=1.2)
style = {"trans-DCE": ("o", "red"), "cis-DCE": ("D", "blue"), "TCE": ("v", "green")}
for name, (mk, c) in style.items():
    r = [x for x in rows if x["series"] == name]
    ax.plot([float(x["OH_mol_dm3"]) for x in r], [float(x["kobs_s-1"]) for x in r], mk, color=c, ls="", ms=8, label=name)
ax.set_xlim(0, 0.11)
ax.set_ylim(0, 4.79)
ax.set_xticks([0, 0.02, 0.04, 0.06, 0.08, 0.10])
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_xlabel("[OH$^-$] (mol/dm$^3$)")
ax.set_ylabel("$k_\\mathrm{obs}$ (s$^{-1}$)")
ax.legend(loc="upper center", frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig5_replot.png"), dpi=150)
