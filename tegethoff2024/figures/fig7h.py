"""Re-plot Figure 7H of Tegethoff & Briggman 2024 from fig7h.csv -> fig7h_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig7h", "dFT_mN_per_mm", (0, 9), [0, 3, 6, 9], "δF_T (mN/mm)", xpos=lambda gi, s, g: gi + (gi - 1) // 7, px_per_unit=28.0, xlabel="clearance angle (deg)")
