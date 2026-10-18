"""Re-plot Supplementary Figure 5c of He et al. 2018 from sfig5c.csv -> sfig5c_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "sfig5c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))


def get(series):
    r = [q for q in rows if q["series"] == series]
    return [float(q["stain_level_atomic_percent"]) for q in r], [float(q["counts_au"]) for q in r]


fig, ax = plt.subplots(figsize=(4.2, 2.8))
ax.plot(*get("Poly. (0-25 nm)"), color="red", lw=1.5, label="Poly. (0-25 nm)")
ax.plot(*get("Poly. (sum)"), color="#8064a2", lw=1.5, label="Poly. (sum)")
ax.plot(*get("0-25 nm"), "^", color="red", ms=5, ls="none", label="0-25 nm")
ax.plot(*get("sum"), "D", color="#4f81bd", ms=4, ls="none", label="sum")
ax.set_xlim(1, 9)
ax.set_ylim(0, 2000)
ax.set_xticks([1, 3, 5, 7, 9])
ax.set_xticklabels([f"{v}%" for v in [1, 3, 5, 7, 9]])
ax.set_yticks(list(range(0, 2001, 500)))
ax.grid(axis="y", color="0.85")
ax.set_title("low stain level 1.4 keV")
ax.set_xlabel("stain level (atomic percent)")
ax.set_ylabel("counts (a.u.)")
ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig5c_replot.png"), dpi=150)
