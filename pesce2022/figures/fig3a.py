"""Re-plot Fig. 3a of Pesce et al. 2022 (CR and PV charts) from fig3a.csv -> fig3a_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig3a.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, axes = plt.subplots(2, 1, figsize=(4.2, 6.4))
for ax, chart, ymax, ticks, labels in (
        (axes[0], "CR", 25000, range(0, 25001, 5000), ["0,0", "5,0x10$^3$", "1,0x10$^4$", "1,5x10$^4$", "2,0x10$^4$", "2,5x10$^4$"]),
        (axes[1], "PV", 5000, range(0, 5001, 1000), ["0", "1x10$^3$", "2x10$^3$", "3x10$^3$", "4x10$^3$", "5x10$^3$"])):
    bars = [r for r in rows if r["row_type"] == "bar" and r["chart"] == chart]
    pts = [r for r in rows if r["row_type"] == "point" and r["chart"] == chart]
    slot = {}
    for r in bars:                   # S, B at 0 um -> slots 0, 1; one empty slot between depths (as in the figure)
        slot[(r["depth_um"], r["signal_background"])] = [0, 350, 700].index(int(r["depth_um"])) * 3 + ["S", "B"].index(r["signal_background"])
    for r in bars:
        x = slot[(r["depth_um"], r["signal_background"])]
        m, sd = float(r["mean"]), float(r["sd"])
        ax.bar(x, m, width=0.64, fill=False, edgecolor="0.25", lw=1.5)
        ax.plot([x, x], [m, m + sd], color="0.25", lw=1.5)
        ax.plot([x - 0.16, x + 0.16], [m + sd, m + sd], color="0.25", lw=1.5)
    for r in pts:
        x = slot[(r["depth_um"], r["signal_background"])]
        ax.plot(x, float(r["value"]), "o", color="0.45", alpha=0.6, ms=6, mec="none")
    ax.set_xticks(sorted(slot.values()))
    ax.set_xticklabels([k[1] for k in sorted(slot, key=slot.get)], fontweight="bold")
    for d in (0, 350, 700):
        ax.text([0, 350, 700].index(d) * 3 + 0.5, -0.17 * ymax, f"{d} µm", ha="center", va="top", fontsize=8, fontweight="bold")
    ax.set_xlim(-0.7, 7.7)
    ax.set_ylim(0, ymax)
    ax.set_yticks(list(ticks))
    ax.set_yticklabels(labels)
    ax.set_ylabel("Intensity", fontweight="bold")
    ax.text(-0.25, 1.0, chart, transform=ax.transAxes, color="#c00000", fontweight="bold", fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3a_replot.png"), dpi=150)
