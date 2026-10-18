"""Re-plot Extended Data Fig. 5j of Song et al. 2023 from edfig5j.csv -> edfig5j_replot.png (two x windows)"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

r = read_csv(os.path.join(HERE, "edfig5j.csv"))
fig, axs = plt.subplots(1, 2, figsize=(4.4, 2), sharey=True, gridspec_kw=dict(width_ratios=[260 * 1.266, 400 * 0.816]))
for ax, w, lim, ticks in ((axs[0], "750-1010", (750, 1010), [800, 900, 1000]), (axs[1], "1900-2300", (1900, 2300), [2000, 2200])):
    for s, c in (("Os vi+FeCN", "r"), ("Os vi", "#2040a0")):
        q = [x for x in r if x["series"] == s and x["window_cm1"] == w]
        ax.plot([float(x["raman_shift_cm1"]) for x in q], [float(x["intensity"]) / 1e4 for x in q], color=c, lw=1.2, label=s)
    ax.set_xlim(*lim); ax.set_xticks(ticks)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
axs[1].spines["left"].set_visible(False); axs[1].tick_params(left=False)
axs[0].set_ylim(0, 2); axs[0].set_yticks([0, 1, 2]); axs[0].set_ylabel("Intensity (a.u.)  x10$^4$")
axs[1].legend(frameon=False, fontsize=7)
fig.supxlabel("Wavelength (cm$^{-1}$)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "edfig5j_replot.png"), dpi=200)
