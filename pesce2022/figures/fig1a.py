"""Re-plot Fig. 1a of Pesce et al. 2022 from fig1a.csv -> fig1a_replot.png (fig1b.py does the same for panel b)."""
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
COLORS = {"405": "#1f4fd8", "488": "#00d000", "561": "#ff8000", "638": "#ff0000"}


def replot(panel, ylim):
    with open(os.path.join(HERE, f"fig1{panel}.csv")) as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    bars = [r for r in rows if r["row_type"] == "bar"]
    pts = [r for r in rows if r["row_type"] == "point"]
    groups = []
    for r in bars:
        if r["group"] not in groups:
            groups.append(r["group"])
    series = ["405", "488", "561", "638"]
    xpos = {}
    for r in bars:                       # 4 bars per group on consecutive slots, one empty slot between groups
        g, s = groups.index(r["group"]), series.index(r["excitation_nm"])
        xpos[(r["group"], r["excitation_nm"])] = g * 5 + s
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for r in bars:
        x = xpos[(r["group"], r["excitation_nm"])]
        m, sd = float(r["mean"]), float(r["sd"])
        ax.bar(x, m - ylim[0], bottom=ylim[0], width=0.65, fill=False, edgecolor=COLORS[r["excitation_nm"]], lw=1.6,
               label=r["excitation_nm"] if r["group"] == groups[0] else None)
        ax.plot([x, x], [m, m + sd], color=COLORS[r["excitation_nm"]], lw=1.6)
        ax.plot([x - 0.16, x + 0.16], [m + sd, m + sd], color=COLORS[r["excitation_nm"]], lw=1.6)
        if int(r["asterisks"]):
            ax.text(x, m + sd + 12, "\n".join("*" * int(r["asterisks"])), ha="center", va="bottom", fontsize=6, linespacing=1.6)
    for r in pts:
        x = xpos[(r["group"], r["excitation_nm"])]
        ax.plot(x, float(r["value"]), "o", color="k", alpha=0.2, ms=3.5, mec="none")
    ax.set_xticks([g * 5 + 1.5 for g in range(len(groups))])
    ax.set_xticklabels([g.replace("H2O2", "H$_2$O$_2$").replace("NaBH4", "NaBH$_4$").replace("CuSO4", "CuSO$_4$")
                        .replace(" Ascorbic", "\nAscorbic").replace(" Hydroquinone", "\nHydroquinone")
                        .replace(" NaBH", "\nNaBH").replace(" CuSO", "\nCuSO") for g in groups], fontsize=7, fontweight="bold")
    ax.set_xlim(-1, len(groups) * 5 - 1)
    ax.set_ylim(*ylim)
    ax.set_yticks(range(100, 701, 100))
    ax.set_yticklabels([f"{k}x10$^2$" for k in range(1, 8)])
    ax.set_ylabel("Autofluorescence (A.U.)")
    ax.legend(ncol=2, loc="upper right", fontsize=8, frameon=True)
    ax.text(-0.08, 1.02, panel, transform=ax.transAxes, fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"fig1{panel}_replot.png"), dpi=150)


if __name__ == "__main__":
    replot(sys.argv[1] if len(sys.argv) > 1 else "a", (100, 760))
