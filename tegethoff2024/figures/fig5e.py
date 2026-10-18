"""Re-plot Figure 5E of Tegethoff & Briggman 2024 from fig5e.csv -> fig5e_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig5ef_plot import plot  # noqa: E402

plot("e", "mean_FR_mN_per_mm", (30, 90), [30, 50, 70, 90], "mean F_R (mN/mm)")
