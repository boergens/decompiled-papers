"""Digitize Figure 11 (a-f) of Wei et al. 2025 (PDF p. 11): forces Fx, Fy, Fz on the spherical
quartz indenter (R = 14.5 A) vs sliding distance at hc = 4, 7, 10, 16, 22, 25 A.

Source: the 300 ppi embedded image of Figure 11 (2100 x 1178 px). Tier 3 (digitized).
    python3 -I -B figures/fig11_extract.py  -> figures/fig11a.csv ... fig11f.csv, work/fig11?_overlay.png
Boxes below (pixels of the embedded image) mark the legend lines (excluded for all series) and the
legend/annotation text (excluded for the black Fx series); located on a pixel grid drawn over the image.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from figC_markers import run_figure  # noqa: E402

PDF = HERE.parent / "source" / "wei2025.pdf"
CAP = "Evolution of forces on spherical quartz indenter (R = 14.5 A) with sliding distance under different indentation depths (hc) of "
PANELS = {
    "a": dict(search=(0, 700, 0, 580), xfirst=0, xstep=10, nx=8, yfirst=10, ystep=-5, ny=6,
              legend_lines=(140, 265, 220, 395), black_boxes=[(140, 265, 265, 400), (240, 15, 595, 72)], hc="4"),
    "b": dict(search=(700, 1400, 0, 580), xfirst=0, xstep=10, nx=6, yfirst=10, ystep=-5, ny=6,
              legend_lines=(835, 275, 912, 400), black_boxes=[(835, 275, 955, 405), (930, 15, 1295, 72)], hc="7"),
    "c": dict(search=(1400, 2100, 0, 580), xfirst=0, xstep=5, nx=8, yfirst=10, ystep=-5, ny=6,
              legend_lines=(1525, 290, 1600, 415), black_boxes=[(1525, 290, 1645, 420), (1630, 15, 2010, 72)], hc="10"),
    "d": dict(search=(0, 700, 560, 1178), xfirst=0, xstep=5, nx=8, yfirst=10, ystep=-5, ny=6,
              legend_lines=(110, 870, 190, 1000), black_boxes=[(110, 870, 235, 1005), (325, 940, 605, 990)], hc="16"),
    "e": dict(search=(700, 1400, 560, 1178), xfirst=0, xstep=5, nx=7, yfirst=10, ystep=-5, ny=6,
              legend_lines=(800, 905, 880, 1035), black_boxes=[(800, 905, 925, 1035), (940, 990, 1305, 1030)], hc="22"),
    "f": dict(search=(1400, 2100, 560, 1178), xfirst=0, xstep=5, nx=7, yfirst=12, ystep=-4, ny=7,
              legend_lines=(1500, 915, 1575, 1045), black_boxes=[(1500, 915, 1625, 1045), (1635, 615, 2005, 672)], hc="25"),
}
CAPS = {p: CAP + f"hc = {c['hc']} A (panel {p})" for p, c in PANELS.items()}
if __name__ == "__main__":
    run_figure(PDF, 11, (45.5, 32.6, 549.5, 315.3), "fig11", PANELS, CAPS, HERE.parent / "work", HERE,
               "sphere R = 14.5 A")
