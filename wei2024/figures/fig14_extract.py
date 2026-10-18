"""Fig. 14 a, c, d: displacement magnitude (key 0-5 A), shear strain (0-0.4) and volumetric strain (0-0.2) of atoms at different sliding distances, h_c = 20 A, 1.0 A/ps.

Tier 3 colour-key mapping (tools/f4_atommap.py) of the embedded image on PDF page 18.
Panel b (surface mesh, no key) and the fan-shape drawing are not mapped. Annotations removed: the two blue dashed\n'atom packing' ellipses and the blue dashed arrow on a(iii)/a(iv) 'Hidden quartz' (hand-placed ellipse/segment masks),\nthe yellow dotted fan outline on a(iii) top view (yellow components >= 6 px, dilated 2 px) and the red dashed arrow there\n(segment mask).
Writes figures/<panel>.csv for the panels below and work/f4_fig14_overlay.png.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import f4_atommap as fm  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
PAGE, BBOX = 18, (78, 59, 518, 511)
KEYS = {'a': ((40, 480, 250, 530), 0, 5, 'displacement magnitude of atoms (Angstrom)'), 'c': ((50, 1310, 260, 1365), 0, 0.4, 'shear strain of atoms (dimensionless)'), 'd': ((70, 1645, 280, 1700), 0, 0.2, 'volumetric strain of atoms (dimensionless)')}
PANELS = [
    ('fig14a_hidden_i', (315, 76, 670, 240), 'a', 'Hidden quartz (i) 0 Å'),
    ('fig14a_hidden_ii', (693, 73, 1047, 240), 'a', 'Hidden quartz (ii) 10 Å'),
    ('fig14a_hidden_iii', (1069, 66, 1424, 242), 'a', 'Hidden quartz (iii) 20 Å'),
    ('fig14a_hidden_iv', (1443, 66, 1800, 242), 'a', 'Hidden quartz (iv) 30 Å'),
    ('fig14a_nohidden_i', (312, 377, 665, 557), 'a', 'No hidden quartz (i) 0 Å'),
    ('fig14a_nohidden_ii', (693, 378, 1046, 557), 'a', 'No hidden quartz (ii) 30 Å'),
    ('fig14a_xy_iii', (1131, 323, 1440, 632), 'a', '(iii) 30 Å, top view (x right, y up)'),
    ('fig14c_i', (342, 1279, 695, 1443), 'c', '(i) 0 Å'),
    ('fig14c_ii', (717, 1276, 1072, 1443), 'c', '(ii) 10 Å'),
    ('fig14c_iii', (1098, 1277, 1452, 1445), 'c', '(iii) 20 Å'),
    ('fig14c_iv', (1472, 1273, 1827, 1443), 'c', '(iv) 30 Å'),
    ('fig14d_i', (343, 1592, 696, 1756), 'd', '(i) 0 Å'),
    ('fig14d_ii', (720, 1588, 1075, 1756), 'd', '(ii) 10 Å'),
    ('fig14d_iii', (1098, 1591, 1452, 1757), 'd', '(iii) 20 Å'),
    ('fig14d_iv', (1479, 1589, 1832, 1758), 'd', '(iv) 30 Å'),
]

if __name__ == "__main__":
    a = fm.embedded(PDF, PAGE, BBOX)
    ex = None
    ex = fm.annotation_mask(a, (200, 200, 0), (255, 255, 110), min_area=6, dilate=2,
                           region=(1131, 323, 1440, 632))
    ex |= fm.ellipse_mask(a.shape[:2], 1349, 88.5, 37, 42.5, 4)
    ex |= fm.ellipse_mask(a.shape[:2], 1747.5, 95, 37.5, 44, 4)
    ex |= fm.segment_mask(a.shape[:2], (1384, 80), (1430, 55), 7)    # arrow from the a(iii) ellipse
    ex |= fm.segment_mask(a.shape[:2], (1650, 58), (1712, 95), 6)    # arrow from the a(iv) ellipse
    ex |= fm.segment_mask(a.shape[:2], (1365, 449), (1440, 454), 5)  # red dashed arrow on a(iii) top view
    rep = fm.run_figure("fig14", PDF, PAGE, BBOX, KEYS, PANELS, ex, HERE, ROOT / "work",
                        "Fig. 14, atoms at different sliding distances under one slice along x from 64 to 74 A, h_c = 20 A, 1.0 A/ps")
    for r in rep:
        print(r)
