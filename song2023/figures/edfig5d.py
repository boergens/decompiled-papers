"""Re-plot Extended Data Fig. 5d of Song et al. 2023 from edfig5d.csv -> edfig5d_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

r = read_csv(os.path.join(HERE, "edfig5d.csv"))
fig, ax = plt.subplots(figsize=(2.2, 2))
for s, c in (("fresh", "#0072bd"), ("2 h", "#d95319"), ("24 h", "#edb120")):
    q = [x for x in r if x["series"] == s]
    ax.plot([float(x["wavelength_nm"]) for x in q], [float(x["absorbance"]) for x in q], color=c, lw=1.5, label=s)
ax.set_xlim(300, 1000); ax.set_ylim(0, 0.3)
ax.set_xticks([400, 600, 800], ["400", "", "800"]); ax.set_yticks([0, 0.1, 0.2, 0.3])
ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Absorption (a.u.)")
ax.legend(frameon=False, fontsize=7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "edfig5d_replot.png"), dpi=200)
