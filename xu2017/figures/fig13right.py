"""Re-plot the right scatter plot of Figure 13 of Xu et al. 2017 from fig13right.csv (ink density) -> fig13right_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig13right.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
A = sorted({float(r["angle_deg"]) for r in rows})
E = sorted({float(r["energy_keV"]) for r in rows})
img = np.full((len(E), len(A)), np.nan)
for r in rows:
    img[E.index(float(r["energy_keV"])), A.index(float(r["angle_deg"]))] = float(r["ink_fraction"])
fig, ax = plt.subplots(figsize=(4, 3))
ax.imshow(img, origin="lower", cmap="Greys", vmin=0, vmax=0.8, aspect="auto",
          extent=(A[0] - 1, A[-1] + 1, E[0] - 0.0125, E[-1] + 0.0125))
ax.plot([0, 45, 45, 0, 0], [0.1, 0.1, 1.2, 1.2, 0.1], "k--", lw=1.5)
ax.set_xlim(0, 88)
ax.set_ylim(0, 1.22)
ax.set_xlabel("Back Scatter Angle(degrees)")
ax.set_ylabel("Energy (KeV)")
fig.tight_layout()
fig.savefig(HERE / "fig13right_replot.png", dpi=150)
