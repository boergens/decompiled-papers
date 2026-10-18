"""Re-plot Figure 5C of Tegethoff & Briggman 2024 from fig5c.csv -> fig5c_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig5c", "dFS_mN_per_mm", (0, 40), [0, 10, 20, 30, 40], "δF_S (mN/mm)", xpos=lambda gi, s, g: gi + (1.2 if g == "35 nm" else 0), xlabel="50 nm | 35 nm")
