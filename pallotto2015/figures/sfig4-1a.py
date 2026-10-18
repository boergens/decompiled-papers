"""Re-plot Figure 4-figure supplement 1A from sfig4-1a.csv -> sfig4-1a_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = read_csv(os.path.join(HERE, "sfig4-1a.csv"))
fig, ax = plt.subplots(figsize=(3.4, 3.4))
for s, st in (("cleft contact (grey x)", dict(marker="x", color="0.5", ls="")),
              ("cone bipolar cell tight contact (green)", dict(marker="o", color="#00ee00", ls="")),
              ("AII amacrine cell tight contact (blue)", dict(marker="o", color="#0000dd", ls=""))):
    rr = [r for r in rows if r["series"] == s]
    ax.plot([float(r["surface_area_voxels"]) for r in rr], [float(r["convex_hull_volume_voxels"]) for r in rr], ms=5, **st)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(10, 1e5); ax.set_ylim(10, 1e5)
ax.set_xlabel("Surface area (voxels)"); ax.set_ylabel("Convex hull volume (voxels)")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "sfig4-1a_replot.png"), dpi=150)
