"""Fig. 13 (bottom row): shear strain (key 0-0.4) of atoms at 1.0 A/ps and sliding distance 30 A for h_c = 5-25 A.

Tier 3 colour-key mapping (tools/f4_atommap.py) of the embedded image on PDF page 17.
The top row (atoms in element colours) is not colour-keyed and is not mapped.
Writes figures/<panel>.csv for the panels below and work/f4_fig13_overlay.png.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import f4_atommap as fm  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
PAGE, BBOX = 17, (86, 59, 509, 198)
KEYS = {'s': ((1480, 305, 1690, 360), 0, 0.4, 'shear strain of atoms (dimensionless)')}
PANELS = [
    ('fig13_shear_i', (29, 371, 360, 528), 's', '(i) h_c = 5 Å'),
    ('fig13_shear_ii', (384, 371, 714, 527), 's', '(ii) h_c = 10 Å'),
    ('fig13_shear_iii', (730, 370, 1061, 527), 's', '(iii) h_c = 15 Å'),
    ('fig13_shear_iv', (1084, 368, 1415, 527), 's', '(iv) h_c = 20 Å'),
    ('fig13_shear_v', (1429, 353, 1760, 527), 's', '(v) h_c = 25 Å'),
]

if __name__ == "__main__":
    a = fm.embedded(PDF, PAGE, BBOX)
    ex = None
    pass
    rep = fm.run_figure("fig13", PDF, PAGE, BBOX, KEYS, PANELS, ex, HERE, ROOT / "work",
                        "Fig. 13 bottom row, shear strain of atoms (side views, y right, z up) at 1.0 A/ps and sliding distance of 30 A under different h_c")
    for r in rep:
        print(r)
