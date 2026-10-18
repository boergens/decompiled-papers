"""Re-plot Figure 7A of Tegethoff & Briggman 2024 from fig7a.csv -> fig7a_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig7a", "mean_FS_mN_per_mm", (0, 90), [0, 20, 40, 60, 80], "mean F_S (mN/mm)", xpos=lambda gi, s, g: gi + (gi - 1) // 3, px_per_unit=56.0, xlabel="cutting speed (mm/s)")
