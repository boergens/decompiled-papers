"""Re-plot Extended Data Fig. 9k from edfig9k.csv -> edfig9k_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from heatmap_plot import plot  # noqa: E402

plot(HERE / "edfig9k.csv", HERE / "edfig9k_replot.png", 8, " µm", "k  distance difference", [2013, 5013, 8013, 11013], size=(8, 3.6),
     ylabel="pairs (231 bands, not resolved)")
