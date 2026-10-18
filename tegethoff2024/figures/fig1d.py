"""Re-plot Figure 1D of Tegethoff & Briggman 2024 from fig1d.csv -> fig1d_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig1_mapplot import plot  # noqa: E402

plot("d")
