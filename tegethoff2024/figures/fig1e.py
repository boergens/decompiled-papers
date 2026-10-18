"""Re-plot Figure 1E of Tegethoff & Briggman 2024 from fig1e.csv -> fig1e_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig1_mapplot import plot  # noqa: E402

plot("e")
