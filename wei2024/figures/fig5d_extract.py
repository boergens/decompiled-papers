"""Fig. 5d (bottom row): displacement magnitude (0-20 Angstrom key) of the bulk epoxy at tensile strains 0, 0.1, 0.2, 0.3 along x.

Tier 3 colour-key mapping (tools/f4_atommap.py) of the embedded image on PDF page 8.
The top row of Fig. 5d (atoms in element colours) and the 3D bulk-system view are not colour-keyed and are not mapped.
Writes figures/<panel>.csv for the panels below and work/f4_fig5d_overlay.png.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import f4_atommap as fm  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
PAGE, BBOX = 8, (75, 442, 520, 686)
KEYS = {'d': ((1610, 715, 1790, 760), 0, 20, 'displacement magnitude of atoms (Angstrom)')}
PANELS = [
    ('fig5d_strain0', (632, 778, 917, 893), 'd', '0 (initial state)'),
    ('fig5d_strain0p1', (946, 782, 1231, 883), 'd', '0.1'),
    ('fig5d_strain0p2', (1264, 787, 1550, 882), 'd', '0.2'),
    ('fig5d_strain0p3', (1568, 787, 1854, 878), 'd', '0.3'),
]

if __name__ == "__main__":
    a = fm.embedded(PDF, PAGE, BBOX)
    ex = None
    pass
    rep = fm.run_figure("fig5d", PDF, PAGE, BBOX, KEYS, PANELS, ex, HERE, ROOT / "work",
                        "Fig. 5d bottom row, displacement magnitude of the bulk epoxy (side views) under tensile strain along x")
    for r in rep:
        print(r)
