"""Re-plot Figure 5D of Tegethoff & Briggman 2024 from fig5d.csv -> fig5d_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig5d", "dFT_mN_per_mm", (0, 6), [0, 2, 4, 6], "δF_T (mN/mm)", xpos=lambda gi, s, g: gi + (1.2 if g == "35 nm" else 0), xlabel="50 nm | 35 nm")
