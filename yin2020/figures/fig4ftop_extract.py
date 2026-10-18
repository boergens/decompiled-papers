"""Digitize Fig. 4f (top histogram, 'Montage rate with 20 MPixel tiles (fps)') of Yin et al. 2020, Nat. Commun. 11:4949 (PDF p. 7).

    python3 -I fig4ftop_extract.py   -> fig4ftop.csv (+ ../work/fig4ftop_overlay.png for checking)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from hist4f import digitize  # noqa: E402

rows, total = digitize(
    str(HERE.parent / "source" / "yin2020.pdf"), 7, (117.3, 347.5, 276.9, 427.7),
    ["1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], ["150", "125", "100", "75", "50", "25", "0"],
    str(HERE / "fig4ftop.csv"), str(HERE.parent / "work" / "fig4ftop_overlay.png"),
    "Yin et al. 2020 Nat. Commun. 11:4949, Fig. 4f, top histogram: x 'Montage rate with 20 MPixel tiles (fps)', y 'Counts'.")
print(len(rows), "bins, total", total)
