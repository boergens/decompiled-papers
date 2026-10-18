"""Re-plot wei2024 Fig. 12e from figures/fig12e.csv -> figures/fig12e_replot.png. Run: python3 -I -B figures/fig12e.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig12e.csv", HERE / "fig12e_replot.png", "$h_c$ = 25 Å, 1.0 Å/ps")
