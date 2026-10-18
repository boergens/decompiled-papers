"""Digitize Figure 13 (a-f) of Wei et al. 2025 (PDF p. 12): forces Fx, Fy, Fz vs sliding distance
for all six indenters at hc = 4 A.

Source: the 300 ppi embedded JPEG of Figure 13 (2100 x 1197 px). Tier 3 (digitized).
    python3 -I -B figures/fig13_extract.py  -> figures/fig13a.csv ... fig13f.csv, work/fig13?_overlay.png
Boxes below (pixels of the embedded image) mark the legend lines (excluded for all series) and the
legend/annotation text (excluded for the black Fx series); located on a pixel grid drawn over the image.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from figC_markers import run_figure  # noqa: E402

PDF = HERE.parent / "source" / "wei2025.pdf"
CAP = "Evolution of the forces along three directions with sliding distance for all systems at hc of 4 A; panel "
PANELS = {
    "a": dict(search=(0, 700, 0, 600), xfirst=0, xstep=10, nx=6, yfirst=5, ystep=-5, ny=3,
              legend_lines=(110, 310, 185, 440), black_boxes=[(110, 310, 240, 445), (240, 75, 505, 128)], label="Pyramid-0°"),
    "b": dict(search=(700, 1400, 0, 600), xfirst=0, xstep=10, nx=6, yfirst=5, ystep=-5, ny=3,
              legend_lines=(800, 310, 875, 440), black_boxes=[(800, 310, 935, 460), (935, 38, 1235, 88)], label="Pyramid-45°"),
    "c": dict(search=(1400, 2100, 0, 600), xfirst=0, xstep=10, nx=8, yfirst=5, ystep=-5, ny=3,
              legend_lines=(1510, 320, 1585, 445), black_boxes=[(1510, 320, 1645, 450), (1650, 38, 2080, 95)], label="Sphere (R = 14.5 A)"),
    "d": dict(search=(0, 700, 590, 1197), xfirst=0, xstep=10, nx=7, yfirst=5, ystep=-5, ny=3,
              legend_lines=(100, 925, 175, 1050), black_boxes=[(100, 925, 235, 1055), (230, 695, 560, 748)], label="Sphere (R = 10 A)"),
    "e": dict(search=(700, 1400, 590, 1197), xfirst=0, xstep=10, nx=8, yfirst=5, ystep=-5, ny=3,
              legend_lines=(795, 935, 870, 1050), black_boxes=[(795, 935, 935, 1055), (955, 1005, 1295, 1052)], label="Sphere (R = 20 A)"),
    "f": dict(search=(1400, 2100, 590, 1197), xfirst=0, xstep=5, nx=10, yfirst=5, ystep=-5, ny=3,
              legend_lines=(1490, 930, 1565, 1060), black_boxes=[(1490, 930, 1595, 1062), (1640, 1005, 1990, 1050)], label="Sphere (R = 25 A)"),
}
CAPS = {p: CAP + f"({p}) hc = 4 A, {c['label']}" for p, c in PANELS.items()}
if __name__ == "__main__":
    run_figure(PDF, 12, (45.5, 32.1, 549.5, 319.3), "fig13", PANELS, CAPS, HERE.parent / "work", HERE,
               "hc = 4 A")
