"""Re-plot wei2024 Fig. 15b from figures/fig15b.csv -> figures/fig15b_replot.png. Run: python3 -I -B figures/fig15b.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from f3_plot import force_panel  # noqa: E402

force_panel(HERE / "fig15b.csv", HERE / "fig15b_replot.png", "$h_c$ = 20 Å, 0.5 Å/ps")
