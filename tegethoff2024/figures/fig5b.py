"""Re-plot Figure 5B of Tegethoff & Briggman 2024 from fig5b.csv -> fig5b_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig5b", "mean_FT_mN_per_mm", (0, 15), [0, 5, 10, 15], "mean F_T (mN/mm)", xpos=lambda gi, s, g: gi + (1.2 if g == "35 nm" else 0), xlabel="50 nm | 35 nm")
