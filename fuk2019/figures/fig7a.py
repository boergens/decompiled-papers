"""Re-plot Fig. 7a from figures/fig7a.csv (grid) -> figures/fig7a_replot.png:
left, the gridded surface in 3D (seen from roughly the same side as the original);
right, the same grid as a map (phi2 across, phi1 up). Colour scale: jet over the colour-key range."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(line for line in open(HERE / "fig7a.csv") if not line.startswith("#")))
p1 = np.array([float(r["phi1_deg"]) for r in rows])
p2 = np.array([float(r["phi2_deg"]) for r in rows])
E = np.array([float(r["E_mean"]) for r in rows])
L1, L2, LE = (-100, 30), (-185, 150), (465.5, 577.0)
fig = plt.figure(figsize=(11, 4.6))
ax = fig.add_subplot(1, 2, 1, projection="3d")
ax.scatter(p1, p2, E, c=E, cmap="jet", vmin=LE[0], vmax=LE[1], s=6)
ax.set_xlim(*L1); ax.set_ylim(*L2); ax.set_zlim(*LE)
ax.set_xlabel("φ1:Torsion angle (deg)"); ax.set_ylabel("φ2:Torsion angle (deg)"); ax.set_zlabel("Total energy (Kcal/mol)")
ax.view_init(elev=22, azim=-120)
ax.set_title("(a)")
ax2 = fig.add_subplot(1, 2, 2)
sc = ax2.scatter(p2, p1, c=E, cmap="jet", vmin=LE[0], vmax=LE[1], marker="s", s=14)
ax2.set_xlim(*L2); ax2.set_ylim(*L1)
ax2.set_xlabel("φ2 (deg)"); ax2.set_ylabel("φ1 (deg)")
fig.colorbar(sc, ax=ax2, label="Total energy (Kcal/mol)")
fig.tight_layout()
fig.savefig(HERE / "fig7a_replot.png", dpi=130)
