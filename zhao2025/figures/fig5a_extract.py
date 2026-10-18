"""Fig. 5a of Zhao et al. 2025: fracture/cutting energy Gamma vs surface density of broken bonds Sigma_exp, from the
PDF's vector paths (page 6). Writes fig5a.csv and work/fig5a_overlay.png."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import markerpanel  # noqa: E402
import vecplot as vp  # noqa: E402

PDF = ROOT / "source" / "zhao2025.pdf"
# tick marks are filled 0.8 pt rectangles (centres used); the tick labels are glyph outlines, read off the page
X = vp.Axis([(92.28, 0), (125.87, 0.6), (159.46, 1.2), (193.055, 1.8), (226.65, 2.4)])
Y = vp.Axis([(155.225, 0), (124.53, 200), (93.66, 400), (62.97, 600)])
head = [
    "Zhao et al. 2025, Nat. Commun. 16:3203, Fig. 5a: crack extension energy Gamma (J m^-2) vs surface density of",
    "  broken bonds Sigma_exp (chains m^-2, in units of 1e18 as printed: 'Sigma_exp (chains . m^-2) x 10^18').",
    "Columns: series (red squares = Cutting-induced; the last point, highest Gamma, carries the red/white",
    "  'Tearing-induced' icon over a red square); x = Sigma_exp / 1e18 (chains m^-2); y = Gamma (J m^-2);",
    "  x_err_low/high = ends of the horizontal error bar at the caps; y_err_* empty (no vertical bars drawn);",
    "  marker_box_centre_* = centre of the square's bounding box; centre_from: x from the junction of the two",
    "  half-bars (hjunction), y from the bar line (hbar); these agree with the square centres to <0.1 pt.",
    "Provenance: tier 2, vector paths in the PDF (page 6), exact to ~0.01 pt (~0.0002e18 in x, ~0.07 J m^-2 in y).",
    "  " + X.describe("x"),
    "  " + Y.describe("y"),
    "The black open right triangle at lower right of the panel is a slope sketch without numbers (not data).",
]
rows, fit = markerpanel.extract(PDF, 6, (88, 58, 230, 158), X, Y, "#e74c3c", 251, HERE / "fig5a.csv",
                                ROOT / "work" / "fig5a_overlay.png", head, "Sigma_exp", "Gamma",
                                legend_box=(95.18, 69.71, 151.92, 90.48))
for r in rows:
    print(r)
print(fit)
