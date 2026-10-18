"""Re-plot Figure 7E of Tegethoff & Briggman 2024 from fig7e.csv -> fig7e_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig7e", "mean_FS_mN_per_mm", (0, 70), [0, 20, 40, 60], "mean F_S (mN/mm)", xpos=lambda gi, s, g: gi + (gi - 1) // 7, px_per_unit=28.0, xlabel="clearance angle (deg)")
