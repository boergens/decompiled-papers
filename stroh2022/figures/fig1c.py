"""Re-plot Figure 1c of Ströh et al. 2022 from fig1c.csv -> fig1c_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig1c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(2.6, 3.2))
for s, kw in (("fit_line", dict(color="k", lw=1.5)), ("reference_line", dict(color="k", lw=0.8))):
    r = [q for q in rows if q["series"] == s]
    ax.plot([float(q["conc_vol_percent"]) for q in r], [float(q["intensity_au"]) for q in r], **kw)
r = [q for q in rows if q["series"] == "dot"]
ax.scatter([float(q["conc_vol_percent"]) for q in r], [float(q["intensity_au"]) for q in r], s=60, color="0.75", zorder=3)
ax.set_xlim(0, 4.75); ax.set_ylim(0, 1.1)
ax.set_xticks(range(5)); ax.set_yticks([0, 0.5, 1])
ax.spines[["top", "right"]].set_visible(False)
ax.set_xlabel("OsO$_4$ conc. (vol %)"); ax.set_ylabel("Intensity (a.u.)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig1c_replot.png"), dpi=150)
