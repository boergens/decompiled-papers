"""Re-plot wei2024 Fig. 12a from figures/fig12a.csv -> figures/fig12a_replot.png. Run: python3 -I -B figures/fig12a.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig12a.csv", HERE / "fig12a_replot.png", "$h_c$ = 5 Å, 1.0 Å/ps")
