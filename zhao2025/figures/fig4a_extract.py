"""Fig. 4a of Zhao et al. 2025: damage zone depth d vs stretch ratio lambda, from the PDF's vector paths (page 5).
Writes fig4a.csv and work/fig4a_overlay.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import markerpanel  # noqa: E402
import vecplot as vp  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
X = vp.Axis([(139.53, 1.0), (204.65, 1.2), (269.52, 1.4)])          # tick marks with labels 1, 1.2, 1.4
Y = vp.Axis([(176.16, 0), (149.01, 20), (121.81, 40), (94.57, 60)])   # labels 0, 20, 40, 60 (top frame unlabelled)
head = [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 4a: damage zone depth d (um) vs applied stretch ratio lambda.",
    "Columns: series (red squares = Cutting-induced; the last point, at lambda ~1.45 in region III, carries the blue",
    "  'Tearing-induced' icon drawn over a red square and a blue error bar drawn over a red one of the same length);",
    "  x = lambda; y = d (um); x_err_* empty (no horizontal bars); y_err_low/high = ends of the error bar (standard",
    "  deviation per the caption) at the cap lines; marker_box_centre_* = centre of the square's bounding box;",
    "  centre_from: x from the vertical error-bar line (vbar) / y from the junction of the two half-bars (vjunction);",
    "  these agree with the square centres to <0.1 pt.",
    "Provenance: tier 2, vector paths in the PDF (page 5), exact to ~0.01 pt (~0.0001 in lambda, ~0.01 um in d).",
    "  " + X.describe("x"),
    "  " + Y.describe("y"),
    "  Note the frame's left edge (139.53 pt) is the '1' tick; the 1.2/1.4 spacing puts lambda = 1 at 139.78 pt",
    "  (fit residual shown above). Background shading: region I lambda < %.4f, II %.4f-%.4f, III > %.4f (fill edges)."
    % (X(185.83), X(185.83), X(278.63), X(278.63)),
]
rows, fit = markerpanel.extract(PDF, 5, (135, 50, 306, 180), X, Y, "#e74c3c", 142, HERE / "fig4a.csv",
                                ROOT / "work" / "fig4a_overlay.png", head, "lambda", "d")
for r in rows:
    print(r)
print(fit)
