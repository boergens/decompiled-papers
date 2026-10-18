"""Re-plot fig8 from its CSVs -> fig8_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import f4_atommap as fm  # noqa: E402

PANELS = [
    ('fig8a_top_i', '(i) 0 Å, slice along x from 0 to 74 Å', 'a'),
    ('fig8a_top_ii', '(ii) 10 Å', 'a'),
    ('fig8a_top_iii', '(iii) 20 Å', 'a'),
    ('fig8a_top_iv', '(iv) 25 Å', 'a'),
    ('fig8a_top_v', '(v) 30 Å', 'a'),
    ('fig8a_top_vi', '(vi) 35 Å', 'a'),
    ('fig8a_top_vii', '(vii) 40 Å', 'a'),
    ('fig8a_top_viii', '(viii) 45 Å', 'a'),
    ('fig8a_slice_i', '(i) 35 Å, slice along x from 64 Å to 74 Å', 'a'),
    ('fig8a_slice_ii', '(ii) 40 Å', 'a'),
    ('fig8a_slice_iii', '(iii) 45 Å', 'a'),
    ('fig8b_i', '(i) 0 Å', 'b'),
    ('fig8b_ii', '(ii) 20 Å', 'b'),
    ('fig8b_iii', '(iii) 30 Å', 'b'),
    ('fig8b_iv', '(iv) 40 Å', 'b'),
    ('fig8b_v', '(v) 45 Å', 'b'),
    ('fig8c_i', '(i) 0 Å', 'c'),
    ('fig8c_ii', '(ii) 20 Å', 'c'),
    ('fig8c_iii', '(iii) 30 Å', 'c'),
    ('fig8c_iv', '(iv) 40 Å', 'c'),
    ('fig8c_v', '(v) 45 Å', 'c'),
]
fm.replot("fig8", HERE, PANELS, {'a': (0, 5, 'displacement magnitude (Å)'), 'b': (0, 0.4, 'shear strain'), 'c': (0, 0.2, 'volumetric strain')}, HERE / "fig8_replot.png", 5)
