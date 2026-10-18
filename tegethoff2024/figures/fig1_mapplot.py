"""Shared re-plot for the Figure 1 hardness maps (D, E, G): reads fig1<panel>.csv only."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def plot(panel):
    with open(os.path.join(HERE, f"fig1{panel}.csv")) as f:
        lines = f.readlines()
    rows = list(csv.DictReader(l for l in lines if not l.startswith("#")))
    w, h = [float(v) for v in next(l for l in lines if "image_extent_um:" in l).split(":")[1].split()[:2]]
    fig, ax = plt.subplots(figsize=(4.5 * w / max(w, h) + 1.2, 4.5 * h / max(w, h) + 0.6))
    sc = ax.scatter([float(r["x_um"]) for r in rows], [float(r["y_um"]) for r in rows],
                    c=[float(r["hardness_HV"]) for r in rows], cmap="jet", vmin=11.0, vmax=12.8, s=25)
    ax.set_facecolor("0.8")
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.set_aspect("equal")
    ax.set_title("top", fontsize=9)
    ax.set_xlabel("bottom; x (µm)")
    ax.set_ylabel("y (µm)")
    cb = fig.colorbar(sc, ax=ax, ticks=[11.0, 11.4, 11.8, 12.2, 12.6])
    cb.set_label("hardness (HV)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"fig1{panel}_replot.png"), dpi=150)
