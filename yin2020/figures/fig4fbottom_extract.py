"""Digitize Fig. 4f (bottom histogram, 'Montage rate with 50 MPixel tiles (fps)') of Yin et al. 2020, Nat. Commun. 11:4949 (PDF p. 7).

    python3 -I fig4fbottom_extract.py   -> fig4fbottom.csv (+ ../work/fig4fbottom_overlay.png for checking)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from hist4f import digitize  # noqa: E402

rows, total = digitize(
    str(HERE.parent / "source" / "yin2020.pdf"), 7, (117.3, 454.2, 277.5, 534.3),
    ["1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], ["200", "150", "100", "50", "0"],
    str(HERE / "fig4fbottom.csv"), str(HERE.parent / "work" / "fig4fbottom_overlay.png"),
    "Yin et al. 2020 Nat. Commun. 11:4949, Fig. 4f, bottom histogram: x 'Montage rate with 50 MPixel tiles (fps)', y 'Counts'.")
print(len(rows), "bins, total", total)
