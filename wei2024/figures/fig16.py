"""Re-plot fig16 from its CSVs -> fig16_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import f4_atommap as fm  # noqa: E402

PANELS = [
    ('fig16a_col1', 'column 1 (under it in b: 0.1 Å/ps)', 'a'),
    ('fig16a_col2', 'column 2 (0.5 Å/ps in b)', 'a'),
    ('fig16a_col3', 'column 3 (1.0 Å/ps in b)', 'a'),
    ('fig16a_col4', 'column 4 (1.5 Å/ps in b)', 'a'),
    ('fig16a_col5', 'column 5 (2.0 Å/ps in b)', 'a'),
    ('fig16b_0p1', '0.1 Å/ps', 'b'),
    ('fig16b_0p5', '0.5 Å/ps', 'b'),
    ('fig16b_1p0', '1.0 Å/ps', 'b'),
    ('fig16b_1p5', '1.5 Å/ps', 'b'),
    ('fig16b_2p0', '2.0 Å/ps', 'b'),
]
fm.replot("fig16", HERE, PANELS, {'a': (0, 0.4, 'shear strain'), 'b': (0, 5, 'displacement magnitude (Å)')}, HERE / "fig16_replot.png", 5)
