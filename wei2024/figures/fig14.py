"""Re-plot fig14 from its CSVs -> fig14_replot.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import f4_atommap as fm  # noqa: E402

PANELS = [
    ('fig14a_hidden_i', 'Hidden quartz (i) 0 Å', 'a'),
    ('fig14a_hidden_ii', 'Hidden quartz (ii) 10 Å', 'a'),
    ('fig14a_hidden_iii', 'Hidden quartz (iii) 20 Å', 'a'),
    ('fig14a_hidden_iv', 'Hidden quartz (iv) 30 Å', 'a'),
    ('fig14a_nohidden_i', 'No hidden quartz (i) 0 Å', 'a'),
    ('fig14a_nohidden_ii', 'No hidden quartz (ii) 30 Å', 'a'),
    ('fig14a_xy_iii', '(iii) 30 Å, top view (x right, y up)', 'a'),
    ('fig14c_i', '(i) 0 Å', 'c'),
    ('fig14c_ii', '(ii) 10 Å', 'c'),
    ('fig14c_iii', '(iii) 20 Å', 'c'),
    ('fig14c_iv', '(iv) 30 Å', 'c'),
    ('fig14d_i', '(i) 0 Å', 'd'),
    ('fig14d_ii', '(ii) 10 Å', 'd'),
    ('fig14d_iii', '(iii) 20 Å', 'd'),
    ('fig14d_iv', '(iv) 30 Å', 'd'),
]
fm.replot("fig14", HERE, PANELS, {'a': (0, 5, 'displacement magnitude (Å)'), 'c': (0, 0.4, 'shear strain'), 'd': (0, 0.2, 'volumetric strain')}, HERE / "fig14_replot.png", 4)
