"""Re-plot Figure 7B of Tegethoff & Briggman 2024 from fig7b.csv -> fig7b_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig7b", "mean_FT_mN_per_mm", (0, 20), [0, 4, 8, 12, 16, 20], "mean F_T (mN/mm)", xpos=lambda gi, s, g: gi + (gi - 1) // 3, px_per_unit=56.0, xlabel="cutting speed (mm/s)")
