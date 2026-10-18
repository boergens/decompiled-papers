"""Re-plot Figure 7C of Tegethoff & Briggman 2024 from fig7c.csv -> fig7c_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_plot import plot  # noqa: E402

plot("fig7c", "dFS_mN_per_mm", (0, 60), [0, 20, 40, 60], "δF_S (mN/mm)", xpos=lambda gi, s, g: gi + (gi - 1) // 3, px_per_unit=56.0, xlabel="cutting speed (mm/s)")
