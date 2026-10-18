"""Re-plot Figure 5A of Tegethoff & Briggman 2024 from fig5a.csv -> fig5a_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig5a", "mean_FS_mN_per_mm", (0, 90), [0, 20, 40, 60, 80], "mean F_S (mN/mm)", xpos=lambda gi, s, g: gi + (1.2 if g == "35 nm" else 0), xlabel="50 nm | 35 nm")
