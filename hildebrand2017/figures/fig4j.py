"""Re-plot Fig. 4j from fig4j.csv -> fig4j_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from pairs_plot import plot  # noqa: E402

plot(HERE / "fig4j.csv", HERE / "fig4j_replot.png", 22.5, 1.0, "°", "µm", "variance per pair across z (upper a, lower d)")
