"""Fig. 8: displacement magnitude (a, key 0-5 Angstrom), shear strain (b, key 0-0.4) and volumetric strain (c, key 0-0.2) of atoms at different h_z, loading rate 1.0 A/ps.

Tier 3 colour-key mapping (tools/f4_atommap.py) of the embedded image on PDF page 13.
Not mapped: the 3D perspective view (top left of panel a) and its x-y top view, which carry the grey slice plane and red slice-marking annotations.
Writes figures/<panel>.csv for the panels below and work/f4_fig8_overlay.png.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import f4_atommap as fm  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
PAGE, BBOX = 13, (56, 59, 539, 471)
KEYS = {'a': ((1280, 850, 1490, 905), 0, 5, 'displacement magnitude of atoms (Angstrom)'), 'b': ((1290, 1245, 1500, 1295), 0, 0.4, 'shear strain (von Mises) of atoms (dimensionless)'), 'c': ((1290, 1660, 1500, 1712), 0, 0.2, 'volumetric strain of atoms (dimensionless)')}
PANELS = [
    ('fig8a_top_i', (550, 92, 883, 252), 'a', '(i) 0 Å, slice along x from 0 to 74 Å'),
    ('fig8a_top_ii', (893, 92, 1226, 252), 'a', '(ii) 10 Å'),
    ('fig8a_top_iii', (1239, 97, 1572, 256), 'a', '(iii) 20 Å'),
    ('fig8a_top_iv', (1585, 96, 1918, 255), 'a', '(iv) 25 Å'),
    ('fig8a_top_v', (558, 338, 891, 496), 'a', '(v) 30 Å'),
    ('fig8a_top_vi', (904, 335, 1236, 495), 'a', '(vi) 35 Å'),
    ('fig8a_top_vii', (1249, 336, 1582, 498), 'a', '(vii) 40 Å'),
    ('fig8a_top_viii', (1595, 338, 1927, 496), 'a', '(viii) 45 Å'),
    ('fig8a_slice_i', (907, 602, 1240, 752), 'a', '(i) 35 Å, slice along x from 64 Å to 74 Å'),
    ('fig8a_slice_ii', (1255, 604, 1588, 753), 'a', '(ii) 40 Å'),
    ('fig8a_slice_iii', (1606, 608, 1938, 756), 'a', '(iii) 45 Å'),
    ('fig8b_i', (18, 967, 397, 1140), 'b', '(i) 0 Å'),
    ('fig8b_ii', (420, 973, 799, 1147), 'b', '(ii) 20 Å'),
    ('fig8b_iii', (814, 983, 1195, 1153), 'b', '(iii) 30 Å'),
    ('fig8b_iv', (1212, 983, 1591, 1156), 'b', '(iv) 40 Å'),
    ('fig8b_v', (1608, 986, 1987, 1156), 'b', '(v) 45 Å'),
    ('fig8c_i', (0, 1367, 379, 1541), 'c', '(i) 0 Å'),
    ('fig8c_ii', (420, 1376, 799, 1550), 'c', '(ii) 20 Å'),
    ('fig8c_iii', (835, 1382, 1216, 1552), 'c', '(iii) 30 Å'),
    ('fig8c_iv', (1236, 1382, 1615, 1555), 'c', '(iv) 40 Å'),
    ('fig8c_v', (1633, 1390, 2013, 1560), 'c', '(v) 45 Å'),
]

if __name__ == "__main__":
    a = fm.embedded(PDF, PAGE, BBOX)
    ex = None
    pass
    rep = fm.run_figure("fig8", PDF, PAGE, BBOX, KEYS, PANELS, ex, HERE, ROOT / "work",
                        "Fig. 8, atoms at different displacements of the indenter h_z (slices, y right, z up)")
    for r in rep:
        print(r)
