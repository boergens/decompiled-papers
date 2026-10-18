"""Fig. 6d: displacement magnitude (0-5 Angstrom key) of atoms, top views at four loading rates, h_c = 25 A.

Tier 3 colour-key mapping (tools/f4_atommap.py) of the embedded image on PDF page 11 (xref 196).
The yellow dashed circles and arrows (annotations "More/Little movement and rearrangement of atoms")
are removed: pure-yellow components of >= 60 px, dilated 3 px.
Writes figures/fig6d_<rate>.csv and work/f4_fig6d_overlay.png.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import f4_atommap as fm  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
PAGE, BBOX = 11, (117, 59, 478, 545)
KEYS = {"d": ((620, 1470, 820, 1520), 0, 5, "displacement magnitude of atoms (Angstrom)")}
PANELS = [("fig6d_0p10", (66, 1557, 401, 1893), "d", "0.10 Å/ps"),
          ("fig6d_0p5", (417, 1559, 753, 1893), "d", "0.5 Å/ps"),
          ("fig6d_1p50", (792, 1556, 1127, 1891), "d", "1.50 Å/ps"),
          ("fig6d_2p0", (1167, 1557, 1502, 1893), "d", "2.0 Å/ps")]

if __name__ == "__main__":
    a = fm.embedded(PDF, PAGE, BBOX)
    ex = fm.annotation_mask(a, (200, 200, 0), (255, 255, 90), min_area=60, dilate=3)
    rep = fm.run_figure("fig6d", PDF, PAGE, BBOX, KEYS, PANELS, ex, HERE, ROOT / "work",
                        "Fig. 6d, displacement magnitude of atoms (top views, x right, y up) at different "
                        "loading rates and h_c of 25 Angstrom")
    for r in rep:
        print(r)
