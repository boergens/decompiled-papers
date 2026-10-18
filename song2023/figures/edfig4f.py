"""Re-plot Extended Data Fig. 4f of Song et al. 2023 from edfig4f.csv -> edfig4f_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

r = read_csv(os.path.join(HERE, "edfig4f.csv"))
fig, ax = plt.subplots(figsize=(2.2, 2))
for s, ls in (("no CaC", "--"), ("CaC wash", "-")):
    q = {x["location"]: x for x in r if x["series"] == s}
    y = [float(q[l]["fe_wt_pct"]) for l in ("Periphery", "Center")]
    e = [float(q[l]["half_errorbar"] or 0) for l in ("Periphery", "Center")]
    ax.errorbar([0, 1], y, yerr=e, color="k", ls=ls, capsize=5, lw=1.3, label=s)
ax.set_xticks([0, 1], ["Periphery", "Center"]); ax.set_xlim(-0.3, 1.3)
ax.set_ylim(0, 0.105); ax.set_yticks([0, 0.05, 0.1], ["0", "", "0.1"])
ax.set_ylabel("Fe wt.%")
ax.legend(frameon=False, fontsize=7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "edfig4f_replot.png"), dpi=200)
