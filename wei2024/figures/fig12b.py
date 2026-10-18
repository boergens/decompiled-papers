"""Re-plot wei2024 Fig. 12b from figures/fig12b.csv -> figures/fig12b_replot.png. Run: python3 -I -B figures/fig12b.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig12b.csv", HERE / "fig12b_replot.png", "$h_c$ = 10 Å, 1.0 Å/ps")
