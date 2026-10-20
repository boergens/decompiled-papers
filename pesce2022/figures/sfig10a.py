"""Re-plot Supplementary Fig. 10a of Pesce et al. 2022 from sfig10a.csv -> sfig10a_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "sfig10a.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
bar = [r for r in rows if r["row_type"] == "bar"][0]
pts = [float(r["value"]) for r in rows if r["row_type"] == "point"]
m, sd = float(bar["mean"]), float(bar["sd"])
fig, ax = plt.subplots(figsize=(3.2, 3.2))
ax.bar(0, m, width=0.4, fill=False, edgecolor="0.25", lw=1.5)
ax.plot([0, 0], [m, m + sd], color="0.25", lw=1.5)
ax.plot([-0.1, 0.1], [m + sd, m + sd], color="0.25", lw=1.5)
ax.plot([-0.09, 0.0, 0.08], pts, "o", color="#d51606", ms=8)      # x offsets only spread the 3 markers
ax.set_xlim(-0.5, 0.5)
ax.set_xticks([0])
ax.set_xticklabels([bar["label"]])
ax.set_ylim(0, 1.0)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(["0,0", "0,2", "0,4", "0,6", "0,8", "1,0"])
ax.set_ylabel("SSIM index")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig10a_replot.png"), dpi=150)
