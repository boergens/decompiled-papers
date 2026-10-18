"""Fig. 4b of Zhao et al. 2025: damage zone depth d vs stretch ratio lambda, from the PDF's vector paths (page 5).
Writes fig4b.csv and work/fig4b_overlay.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import markerpanel  # noqa: E402
import vecplot as vp  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
X = vp.Axis([(324.83, 1.0), (386.96, 1.2), (449.03, 1.4)])          # frame (label 1) and tick marks 1.2, 1.4
Y = vp.Axis([(177.22, 0), (149.78, 2), (122.34, 4), (94.81, 6), (67.37, 8)])   # labels 0-8
head = [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 4b: dimensionless damage surface density Sigma-bar vs lambda.",
    "Columns: series (red squares = Cutting-induced; the last point, at lambda ~1.45 in region III, carries the blue",
    "  'Tearing-induced' icon drawn over a red square and a blue error bar drawn over a red one of the same length);",
    "  x = lambda; y = Sigma-bar (dimensionless, printed as a Sigma with an overbar); x_err_* empty (no horizontal bars); y_err_low/high = ends of the error bar (standard",
    "  deviation per the caption) at the cap lines; marker_box_centre_* = centre of the square's bounding box;",
    "  centre_from: x from the vertical error-bar line (vbar) / y from the junction of the two half-bars (vjunction);",
    "  these agree with the square centres to <0.1 pt.",
    "Provenance: tier 2, vector paths in the PDF (page 5), exact to ~0.01 pt (~0.0001 in lambda, ~0.001 in Sigma-bar).",
    "  " + X.describe("x"),
    "  " + Y.describe("y"),
    "  The frame's left edge (324.83 pt) carries the '1' label; it fits the 1.2/1.4 tick spacing (residual above).",
    "  The legend's text layer also holds the word 'PDMS', hidden under the legend entry (not visible on the page).",
    "  Background shading: region I lambda < %.4f, II %.4f-%.4f, III > %.4f (fill edges)."
    % (X(369.2), X(369.2), X(457.75), X(457.75)),
]
rows, fit = markerpanel.extract(PDF, 5, (320, 50, 485, 180), X, Y, "#e74c3c", 52, HERE / "fig4b.csv",
                                ROOT / "work" / "fig4b_overlay.png", head, "lambda", "Sigma_bar")
for r in rows:
    print(r)
print(fit)
