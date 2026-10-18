"""Re-plot fig5d from its CSVs -> fig5d_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import f4_atommap as fm  # noqa: E402

PANELS = [
    ('fig5d_strain0', '0 (initial state)', 'd'),
    ('fig5d_strain0p1', '0.1', 'd'),
    ('fig5d_strain0p2', '0.2', 'd'),
    ('fig5d_strain0p3', '0.3', 'd'),
]
fm.replot("fig5d", HERE, PANELS, {'d': (0, 20, 'displacement magnitude (Å)')}, HERE / "fig5d_replot.png", 4)
