"""Re-plot Fig. 6g and 6h of Kubota et al. 2018 from fig6g.csv / fig6h.csv -> fig6g_replot.png, fig6h_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
for panel, key, ylab, ylim, yt in (("g", "michelson", "Michelson contrast", (0.09, 0.41), np.arange(0.10, 0.401, 0.05)),
                                   ("h", "cnr", "CNR", (0.115, 0.245), np.arange(0.12, 0.241, 0.02))):
    with open(os.path.join(HERE, f"fig6{panel}.csv")) as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    fig, ax = plt.subplots(figsize=(2.6, 2.6))
    for det, sty, mfc in (("BSD", "-", "black"), ("In-Lens SE", "--", "white")):
        r = [q for q in rows if q["detector"] == det]
        ax.plot([float(q["acceleration_voltage_kev"]) for q in r], [float(q[key]) for q in r], "o" + sty,
                color="black", mfc=mfc, ms=6, label=det)
    ax.set_xlim(-0.5, 8.5)
    ax.set_xticks([0, 2, 4, 6, 8])
    ax.set_xticks(range(0, 9), minor=True)
    ax.set_ylim(*ylim)
    ax.set_yticks(yt)
    ax.set_xlabel("Acceleration voltage (keV)")
    ax.set_ylabel(ylab)
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"fig6{panel}_replot.png"), dpi=150)
