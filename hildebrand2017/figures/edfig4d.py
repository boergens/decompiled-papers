"""Re-plot Extended Data Fig. 4d from edfig4d.csv -> edfig4d_replot.png (one bar per digitized run)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "edfig4d.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
spec = [("lost", 2, "lost (6 sections, 0.04%)", "6 sections"),
        ("partial", 4, "partial (25 sections, 0.17%)", "25 sections"),
        ("adjacent", 1, "adjacent (6 section pairs, 0.04%)", "6 section pairs")]
fig, axes = plt.subplots(3, 1, figsize=(6, 3.2), sharex=True)
for ax, (s, ymax, title, right) in zip(axes, spec):
    for r in rows:
        if r["series"] == s:
            hs = [float(x) for x in r["heights_px"].split()]
            # value spread over the run; height = tallest column in units
            n = int(r["value"])
            w = max(1, round(len(hs) / 1.5)) if len(set(hs)) == 1 else len(hs)
            ax.bar(float(r["z_centre"]), n / w, width=float(r["z_right"]) - float(r["z_left"]), color="0.4")
    ax.set_ylim(0, ymax)
    ax.set_yticks([ymax], [f"{ymax}/50"])
    ax.set_title(title, loc="left", fontsize=8)
    ax.text(0.98, 0.9, right, transform=ax.transAxes, ha="right", va="top", fontsize=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
axes[-1].set_xlim(0, 15046)
axes[-1].set_xticks([0, 5000, 10000, 15000])
axes[-1].set_xlabel("position in series, z")
fig.supylabel("sections per bin", fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "edfig4d_replot.png", dpi=150)
