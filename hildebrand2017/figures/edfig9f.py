"""Re-plot Extended Data Fig. 9f from edfig9f.csv -> edfig9f_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from pairs_plot import plot  # noqa: E402

plot(HERE / "edfig9f.csv", HERE / "edfig9f_replot.png", 180.0, 8.0, "°", "µm", "construction of difference matrix")
