"""Re-plot Figure 17 (left plot) of Wei et al. 2025 from fig17.csv -> fig17_replot.png (broken y axis as two panels)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig17.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"R = 10 Å": "k", "R = 14.5 Å": "r", "R = 20 Å": "b", "R = 25 Å": "m"}
fig, (axu, axl) = plt.subplots(2, 1, sharex=True, figsize=(5, 4.5), gridspec_kw={"height_ratios": [1, 2.9], "hspace": 0.05})
for s, c in COL.items():
    rr = [r for r in rows if r["series"] == s]
    for ax in (axu, axl):
        ax.plot([float(r["hc_over_R"]) for r in rr], [float(r["friction_coefficient"]) for r in rr], "o", color=c, label=s)
    for r in rr:
        if "circled" in r["flag"]:
            for ax in (axu, axl):
                ax.plot(float(r["hc_over_R"]), float(r["friction_coefficient"]), "o", ms=22, mfc="none", mec="r", ls="--")
axl.axhline(1.0, color="r", ls="--", lw=2)
axl.text(1.0, 1.04, "1.0", color="r", fontweight="bold")
axu.set_ylim(4.05, 4.3)
axl.set_ylim(0.6, 2.1)
axu.set_yticks([4.1, 4.2, 4.3])
axl.set_yticks([0.8, 1.2, 1.6, 2.0])
axl.set_xlim(0, 2.75)
axu.spines["bottom"].set_visible(False)
axl.spines["top"].set_visible(False)
axu.tick_params(bottom=False)
axu.legend(loc="upper left", fontsize=7, frameon=False)
axl.set_xlabel("$h_c$/R")
axl.set_ylabel("Friciton coefficient")
fig.savefig(HERE / "fig17_replot.png", dpi=150, bbox_inches="tight")
