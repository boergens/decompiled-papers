"""Fig. 10 (p. 10): theoretical elastic recovery vs indentation depth. Vector paths -> fig10.csv.

Run: python3 -I -B figures/fig10_extract.py   (from any directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import vec  # noqa: E402

HERE = Path(__file__).resolve().parent
PAGE, CLIP = 10, (145, 85, 445, 298)
RED = (0.87, 0.03, 0.02)

ds = vec.drawings(PAGE, CLIP)
tx = vec.texts(PAGE, CLIP)
L, T, R, B = vec.frame(ds)
xt = vec.tick_rects(ds, "x", B)
yt = vec.tick_rects(ds, "y", L)
xl = [(t, r) for t, r in tx if r.y0 > B]
yl = [(t, r) for t, r in tx if r.x1 < L]
ax, bx, rx, px = vec.axis_fit(xt, xl, "x")
ay, by, ry, py = vec.axis_fit(yt, yl, "y")

rows = []
chk = []
for r in sorted(vec.stroke_markers(ds, RED), key=lambda r: r.x0):
    cx, cy = vec.centre(r)
    chk.append((cx, cy))
    rows.append(("theoretical elastic recovery", round(float(ax * cx + bx), 3), round(float(ay * cy + by), 6)))

right_ticks = vec.tick_rects(ds, "y", R)
hdr = [
    "zhangk2020 Fig. 10 (p. 10): The theoretical elastic recovery under various indentation depths.",
    "Provenance: tier 2, vector paths in the PDF (PyMuPDF get_drawings); marker centre = centre of the square's stroked outline;",
    "The red line joins the markers: its filled thick segments start and end at the marker centres (checked in the path data), so only the markers are given.",
    f"x calibration: tick marks {', '.join(f'{p:.2f} pt={v:g}' for p, v in px)}; max residual {rx:.3g} nm.",
    f"y calibration: tick marks {', '.join(f'{p:.2f} pt={v:g}' for p, v in py)}; max residual {ry:.3g} nm.",
    f"Unlabelled right-frame ticks at {', '.join(f'{float(ay * p + by):.5f}' for p in right_ticks)} nm (y scale of the left axis).",
    "Uncertainty: about 0.05 nm in x and 0.00002 nm in y (PDF coordinate precision).",
    "Markers: red squares, lower right half filled. x_indentation_depth_nm: Indentation depth (nm); y_elastic_recovery_nm: Theoretical elastic recovery (nm).",
]
vec.write_csv(HERE / "fig10.csv", hdr, ["series", "x_indentation_depth_nm", "y_elastic_recovery_nm"], rows)
print("\n".join(hdr))
for r in rows:
    print(r)

vec.overlay_pts(PAGE, CLIP, chk, HERE.parent / "work" / "fig10_overlay.png")
