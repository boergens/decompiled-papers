"""Re-plot fig13 from its CSVs -> fig13_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import f4_atommap as fm  # noqa: E402

PANELS = [
    ('fig13_shear_i', '(i) h_c = 5 Å', 's'),
    ('fig13_shear_ii', '(ii) h_c = 10 Å', 's'),
    ('fig13_shear_iii', '(iii) h_c = 15 Å', 's'),
    ('fig13_shear_iv', '(iv) h_c = 20 Å', 's'),
    ('fig13_shear_v', '(v) h_c = 25 Å', 's'),
]
fm.replot("fig13", HERE, PANELS, {'s': (0, 0.4, 'shear strain')}, HERE / "fig13_replot.png", 5)
