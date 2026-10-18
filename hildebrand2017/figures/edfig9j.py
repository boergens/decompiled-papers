"""Re-plot Extended Data Fig. 9j from edfig9j.csv -> edfig9j_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from heatmap_plot import plot  # noqa: E402

plot(HERE / "edfig9j.csv", HERE / "edfig9j_replot.png", 180, "°", "j  angle difference", [2013, 5013, 8013, 11013], size=(8, 3.6),
     ylabel="pairs (231 bands, not resolved)")
