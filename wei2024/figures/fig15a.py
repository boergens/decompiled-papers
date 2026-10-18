"""Re-plot wei2024 Fig. 15a from figures/fig15a.csv -> figures/fig15a_replot.png. Run: python3 -I -B figures/fig15a.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig15a.csv", HERE / "fig15a_replot.png", "$h_c$ = 20 Å, 0.1 Å/ps")
