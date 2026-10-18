"""Re-plot Figure 7D of Tegethoff & Briggman 2024 from fig7d.csv -> fig7d_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig7d", "dFT_mN_per_mm", (0, 8), [0, 2, 4, 6, 8], "δF_T (mN/mm)", xpos=lambda gi, s, g: gi + (gi - 1) // 3, px_per_unit=56.0, xlabel="cutting speed (mm/s)")
