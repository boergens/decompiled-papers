"""Fig. 16: a shear strain (key 0-0.4, side views) and b displacement magnitude (key 0-5 A, top views) at sliding distance 30 A and h_c = 20 A, five sliding velocities.

Tier 3 colour-key mapping (tools/f4_atommap.py) of the embedded image on PDF page 19.
Panel a carries no per-panel labels; its panels are named by column (col1 = left), the columns of b are labelled 0.1-2.0 A/ps.
Writes figures/<panel>.csv for the panels below and work/f4_fig16_overlay.png.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import f4_atommap as fm  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
PAGE, BBOX = 19, (56, 383, 539, 557)
KEYS = {'a': ((1640, 180, 1850, 235), 0, 0.4, 'shear strain of atoms (dimensionless)'), 'b': ((1720, 670, 1930, 725), 0, 5, 'displacement magnitude of atoms (Angstrom)')}
PANELS = [
    ('fig16a_col1', (0, 5, 328, 162), 'a', 'column 1 (under it in b: 0.1 Å/ps)'),
    ('fig16a_col2', (422, 6, 748, 162), 'a', 'column 2 (0.5 Å/ps in b)'),
    ('fig16a_col3', (843, 3, 1168, 159), 'a', 'column 3 (1.0 Å/ps in b)'),
    ('fig16a_col4', (1264, 0, 1591, 160), 'a', 'column 4 (1.5 Å/ps in b)'),
    ('fig16a_col5', (1685, 2, 2011, 161), 'a', 'column 5 (2.0 Å/ps in b)'),
    ('fig16b_0p1', (0, 276, 328, 603), 'b', '0.1 Å/ps'),
    ('fig16b_0p5', (422, 276, 748, 603), 'b', '0.5 Å/ps'),
    ('fig16b_1p0', (842, 275, 1168, 601), 'b', '1.0 Å/ps'),
    ('fig16b_1p5', (1264, 273, 1591, 600), 'b', '1.5 Å/ps'),
    ('fig16b_2p0', (1686, 272, 2013, 599), 'b', '2.0 Å/ps'),
]

if __name__ == "__main__":
    a = fm.embedded(PDF, PAGE, BBOX)
    ex = None
    pass
    rep = fm.run_figure("fig16", PDF, PAGE, BBOX, KEYS, PANELS, ex, HERE, ROOT / "work",
                        "Fig. 16, atoms at sliding distance of 30 A and h_c of 20 A at different sliding velocities")
    for r in rep:
        print(r)
