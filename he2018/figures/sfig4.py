"""Re-plot Supplementary Figure 4 of He et al. 2018 from sfig4.csv -> sfig4_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "sfig4.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
SER = [("Sectioned biological sample block", "black"), ("Copper standard", "tab:blue"),
       ("Lead standard", "rebeccapurple"), ("Osmium standard", "limegreen"), ("Uranium standard", "red")]
fig, ax = plt.subplots(figsize=(6.5, 4))
for name, col in SER:
    r = [q for q in rows if q["series"] == name]
    x = np.array([float(q["energy_keV"]) for q in r])
    y = np.array([float(q["counts_mid"]) for q in r])
    lo = np.array([float(q["counts_low"]) for q in r])
    hi = np.array([float(q["counts_high"]) for q in r])
    gap = np.where(np.diff(x) > 0.04)[0] + 1        # break the line where the colour was hidden
    x, y, lo, hi = (np.insert(v, gap, np.nan) for v in (x, y, lo, hi))
    ax.fill_between(x, lo, hi, color=col, lw=0)     # steep flanks: the column's full vertical extent
    ax.plot(x, y, color=col, lw=1, label=name)
ax.set_xlim(8, 20)
ax.set_ylim(-10, 700)
ax.set_xticks(range(8, 21, 2))
ax.set_yticks([0, 200, 400, 600])
ax.set_xlabel("X-ray Energy (keV)")
ax.set_ylabel("Counts")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig4_replot.png"), dpi=150)
