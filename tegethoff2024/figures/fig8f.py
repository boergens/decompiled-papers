"""Re-plot Figure 8F of Tegethoff & Briggman 2024 from fig8f.csv -> fig8f_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_lineplot import plot  # noqa: E402

plot("f", 1.46, [0, 0.4, 0.8, 1.2])
