"""Re-plot Figure 4B of Tegethoff & Briggman 2024 from fig4b.csv -> fig4b_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig4b.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(3.2, 2.6))
for s, c in [("S1", "k"), ("S2", "0.6")]:
    r = [x for x in rows if x["series"] == s]
    t = [float(x["time_s"]) for x in r]
    ax.fill_between(t, [float(x["signal_mV_bottom"]) for x in r], [float(x["signal_mV_top"]) for x in r], color=c, lw=0)
    ax.text(1.5, 18 if s == "S1" else 14, s, color=c)
ax.set_xlim(0, 1.6)
ax.set_ylim(-20, 20)
ax.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
ax.set_xlabel("time (sec)")
ax.set_ylabel("sensor signal (mV)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4b_replot.png"), dpi=150)
