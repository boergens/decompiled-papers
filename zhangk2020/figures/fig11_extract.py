"""Fig. 11 (p. 11): measurement uncertainty vs indentation depth (Cantilever 1). Vector paths -> fig11.csv.

Run: python3 -I -B figures/fig11_extract.py   (from any directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import vec  # noqa: E402

HERE = Path(__file__).resolve().parent
PAGE, CLIP = 11, (150, 88, 415, 268)
RED = (0.87, 0.03, 0.02)

ds = vec.drawings(PAGE, CLIP)
tx = vec.texts(PAGE, CLIP)
L, T, R, B = vec.frame(ds)
ax, bx, rx, px = vec.axis_fit(vec.tick_rects(ds, "x", B), [(t, r) for t, r in tx if r.y0 > B], "x")
ay, by, ry, py = vec.axis_fit(vec.tick_rects(ds, "y", L), [(t, r) for t, r in tx if r.x1 < L], "y")

rows = []
chk = []
for r in sorted(vec.stroke_markers(ds, RED), key=lambda r: r.x0):
    cx, cy = vec.centre(r)
    chk.append((cx, cy))
    rows.append(("Uncertainty", round(float(ax * cx + bx), 2), round(float(ay * cy + by), 4)))
vals = [r[2] for r in rows]
m = sum(vals) / len(vals)
sd = (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5

hdr = [
    "zhangk2020 Fig. 11 (p. 11): The measurement uncertainties of cutting edge radius of a diamond tool under various indentation depths.",
    "Provenance: tier 2, vector paths in the PDF (PyMuPDF get_drawings); marker centre = centre of the marker's stroked outline (red open square with an X inside).",
    f"x calibration: tick marks {', '.join(f'{p:.2f} pt={v:g}' for p, v in px)}; max residual {rx:.3g} nm.",
    f"y calibration: tick marks {', '.join(f'{p:.2f} pt={v:g}' for p, v in py)}; max residual {ry:.3g} nm.",
    "Uncertainty of the extraction: about 0.05 nm in x and 0.0003 nm in y (PDF coordinate precision).",
    "x_indentation_depth_nm: Indentation depth (nm); y_uncertainty_nm: Uncertainty (nm).",
    f"Check (decompiler): mean {m:.4f} nm, sample standard deviation {sd:.4f} nm (text: standard deviation 0.005 nm).",
]
vec.write_csv(HERE / "fig11.csv", hdr, ["series", "x_indentation_depth_nm", "y_uncertainty_nm"], rows)
print("\n".join(hdr))
for r in rows:
    print(r)

vec.overlay_pts(PAGE, CLIP, chk, HERE.parent / "work" / "fig11_overlay.png")
