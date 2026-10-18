"""Re-plot Figure 5i of Nguyen et al. 2016 from fig5i.csv -> fig5i_replot.png (same code as fig5h.py)"""
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = os.path.splitext(os.path.basename(__file__))[0]          # fig5i (fig5h.py runs the same code)
COLOURS = {"purple": "#c070f0", "blue": "#5050f0", "green": "#50c050"}
SETUP = {
    "fig5h": dict(col="voxel_size_nm3", ylim=(0, 9000), yticks=[0, 3000, 6000, 9000], ylabel="Voxel size (nm$^3$)"),
    "fig5i": dict(col="electron_dose_e_per_nm2", ylim=(0, 80), yticks=[0, 20, 40, 60, 80],
                  ylabel="Electron dose (e$^{-}$/nm$^2$)"),
}[NAME]


def main():
    with open(os.path.join(HERE, NAME + ".csv")) as f:
        rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
    pairs = {}
    for r in rows:
        pairs.setdefault(r["pair"], {"colour": r["colour"]})[r["group"]] = float(r[SETUP["col"]])
    fig, ax = plt.subplots(figsize=(2.2, 2.6))
    for p in pairs.values():
        ax.plot([0, 1], [p["Cont"], p["Carbon"]], "-o", color=COLOURS[p["colour"]], alpha=0.7, ms=6, lw=1)
    top = SETUP["ylim"][1]
    ax.plot([0, 0, 1, 1], [top * 0.97, top, top, top * 0.97], color="k", lw=1.5, clip_on=False)
    ax.text(0.5, top * 1.01, "*", ha="center", va="bottom", fontsize=14)
    ax.set_xlim(-0.5, 2.0)
    ax.set_ylim(*SETUP["ylim"])
    ax.set_yticks(SETUP["yticks"])
    ax.set_xticks([0, 1], ["Cont", "Carbon"], rotation=45)
    ax.set_ylabel(SETUP["ylabel"])
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, NAME + "_replot.png"), dpi=150)


if __name__ == "__main__":
    sys.exit(main())
