"""Re-plot Figure 7F of Tegethoff & Briggman 2024 from fig7f.csv -> fig7f_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig7f", "mean_FT_mN_per_mm", (0, 12), [0, 4, 8, 12], "mean F_T (mN/mm)", xpos=lambda gi, s, g: gi + (gi - 1) // 7, px_per_unit=28.0, xlabel="clearance angle (deg)")
