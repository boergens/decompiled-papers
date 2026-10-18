"""Re-plot wei2024 Fig. 15c from figures/fig15c.csv -> figures/fig15c_replot.png. Run: python3 -I -B figures/fig15c.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig15c.csv", HERE / "fig15c_replot.png", "$h_c$ = 20 Å, 1.0 Å/ps")
