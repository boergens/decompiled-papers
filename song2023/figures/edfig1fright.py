"""Re-plot Extended Data Fig. 1f (right) of Song et al. 2023 from edfig1fright.csv -> edfig1fright_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

rows = [x for x in read_csv(os.path.join(HERE, "edfig1fright.csv")) if x["plotted"] == "yes"]
els = ["Os", "Fe", "U"]
fig, ax = plt.subplots(figsize=(2.3, 2.3))
for cond, col in (("TCH", "#2b4ba0"), ("no TCH", "#f0a020"), ("PG", "#e02030")):
    r = {x["element"]: x for x in rows if x["condition"] == cond}
    ax.errorbar(range(3), [float(r[e]["conc_wt"]) for e in els], yerr=[float(r[e]["error_2sig"]) for e in els],
                color=col, capsize=3, lw=1.2, label=cond)
ax.set_xticks(range(3), els)
ax.set_ylim(0, 60)
ax.set_yticks([0, 20, 40, 60])
ax.set_ylabel("wt.%")
ax.legend(frameon=False, fontsize=8, loc="upper right")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "edfig1fright_replot.png"), dpi=200)
