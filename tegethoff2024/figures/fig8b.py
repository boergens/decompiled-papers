"""Re-plot Figure 8B of Tegethoff & Briggman 2024 from fig8b.csv -> fig8b_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_lineplot import plot  # noqa: E402

plot("b", 2.12, [0, 0.5, 1, 1.5, 2])
