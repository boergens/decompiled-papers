"""Re-plot wei2024 Fig. 15e from figures/fig15e.csv -> figures/fig15e_replot.png. Run: python3 -I -B figures/fig15e.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig15e.csv", HERE / "fig15e_replot.png", "$h_c$ = 20 Å, 2.0 Å/ps")
