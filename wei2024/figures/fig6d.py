"""Re-plot Fig. 6d from its CSVs -> fig6d_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import f4_atommap as fm  # noqa: E402

PANELS = [("fig6d_0p10", "0.10 Å/ps", "d"), ("fig6d_0p5", "0.5 Å/ps", "d"),
          ("fig6d_1p50", "1.50 Å/ps", "d"), ("fig6d_2p0", "2.0 Å/ps", "d")]
fm.replot("fig6d", HERE, PANELS, {"d": (0, 5, "displacement (Å)")}, HERE / "fig6d_replot.png", 4)
