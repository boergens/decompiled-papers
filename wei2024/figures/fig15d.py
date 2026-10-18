"""Re-plot wei2024 Fig. 15d from figures/fig15d.csv -> figures/fig15d_replot.png. Run: python3 -I -B figures/fig15d.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig15d.csv", HERE / "fig15d_replot.png", "$h_c$ = 20 Å, 1.5 Å/ps")
