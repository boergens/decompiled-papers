"""Re-plot Fig. 4a of Kubota et al. 2018 from fig4a.csv -> fig4a_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig4a.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"CNT-PET": "red", "Kapton": "blue", "cc-Kapton": "black"}
fig, axs = plt.subplots(1, 4, figsize=(11, 2.8), sharey=True)
for ax, exc in zip(axs, ("405", "488", "561", "633")):
    for s, c in COL.items():
        r = [q for q in rows if q["excitation_nm"] == exc and q["series"] == s]
        x = np.array([float(q["wavelength_nm"]) for q in r])
        y = np.array([float(q["intensity_x1e3_mid"]) for q in r])
        if len(x) > 1:   # break the line at missing columns (hidden under another series)
            gap = np.where(np.diff(x) > 3)[0] + 1
            x, y = np.insert(x, gap, np.nan), np.insert(y, gap, np.nan)
        ax.plot(x, y, color=c, lw=1.5, label=s)
    ax.set_xlim(400, 710)
    ax.set_xticks([400, 500, 600, 700])
    ax.set_ylim(0, 30)
    ax.set_title(f"Excitation {exc} nm", fontsize=9)
    ax.set_xlabel("Wavelength (nm)")
axs[0].set_yticks([0, 5, 10, 15, 20, 25])
axs[0].set_ylabel("Intensity gradations (16 bit) ×10$^3$")
axs[0].text(400, 29, "(axis broken above 25; top label 65.5)", fontsize=6)
fig.suptitle("Emission spectra", fontsize=9)
axs[3].legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4a_replot.png"), dpi=150)
