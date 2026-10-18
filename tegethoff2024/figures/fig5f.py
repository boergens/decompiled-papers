"""Re-plot Figure 5F of Tegethoff & Briggman 2024 from fig5f.csv -> fig5f_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig5ef_plot import plot  # noqa: E402

plot("f", "mean_dFS_mN_per_mm", (0, 30), [0, 10, 20, 30], "δF_S (mN/mm)")
