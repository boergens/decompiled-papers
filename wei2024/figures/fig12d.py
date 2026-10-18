"""Re-plot wei2024 Fig. 12d from figures/fig12d.csv -> figures/fig12d_replot.png. Run: python3 -I -B figures/fig12d.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig12d.csv", HERE / "fig12d_replot.png", "$h_c$ = 20 Å, 1.0 Å/ps")
