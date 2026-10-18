"""Fig. 5b of Zhao et al. 2025: blunting radius r_b vs damage zone depth d, from the PDF's vector paths (page 6).
Writes fig5b.csv and work/fig5b_overlay.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import markerpanel  # noqa: E402
import vecplot as vp  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
# tick marks are filled ~0.9 pt rectangles (centres used); tick labels are glyph outlines, read off the page
X = vp.Axis([(93.08, 0), (115.6, 10), (138.005, 20), (160.44, 30), (182.96, 40), (205.36, 50), (227.91, 60)])
Y = vp.Axis([(293.925, 0), (264.925, 100), (236.04, 200), (207.035, 300)])
head = [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 5b: blunting radius r_b (um) vs damage zone depth d (um).",
    "Columns: series (red squares = Cutting-induced; the last point, highest r_b, carries the red/white",
    "  'Tearing-induced' icon over a red square); x = d (um); y = r_b (um); x_err_low/high and y_err_low/high =",
    "  ends of the horizontal and vertical error bars at their caps; marker_box_centre_* = centre of the square's",
    "  bounding box; centre_from: x from the vertical bar line (vbar), y from the horizontal bar line (hbar);",
    "  these agree with the square centres to <0.1 pt.",
    "Provenance: tier 2, vector paths in the PDF (page 6), exact to ~0.01 pt (~0.005 um in d, ~0.04 um in r_b).",
    "  " + X.describe("x"),
    "  " + Y.describe("y"),
    "The black open right triangle at lower right of the panel is a slope sketch without numbers (not data).",
]
rows, fit = markerpanel.extract(PDF, 6, (88, 195, 232, 296), X, Y, "#e74c3c", 407, HERE / "fig5b.csv",
                                ROOT / "work" / "fig5b_overlay.png", head, "d", "r_b",
                                legend_box=(95.98, 206.49, 151.0, 226.68))
for r in rows:
    print(r)
print(fit)
