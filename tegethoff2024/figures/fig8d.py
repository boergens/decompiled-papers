"""Re-plot Figure 8D of Tegethoff & Briggman 2024 from fig8d.csv -> fig8d_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_lineplot import plot  # noqa: E402

plot("d", 1.82, [0, 0.4, 0.8, 1.2, 1.6])
