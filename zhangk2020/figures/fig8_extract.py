"""Fig. 8 (p. 9): evaluated radii vs indentation depth. Vector paths in the PDF -> fig8.csv.

Run: python3 -I -B figures/fig8_extract.py   (from any directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import vec  # noqa: E402

HERE = Path(__file__).resolve().parent
PAGE, CLIP = 9, (150, 150, 415, 333)

ds = vec.drawings(PAGE, CLIP)
tx = vec.texts(PAGE, CLIP)
L, T, R, B = vec.frame(ds)
xt = vec.tick_rects(ds, "x", B)
yt = vec.tick_rects(ds, "y", L)
xl = [(t, r) for t, r in tx if r.y0 > B]
yl = [(t, r) for t, r in tx if r.x1 < L]
ax, bx, rx, px = vec.axis_fit(xt, xl, "x")
ay, by, ry, py = vec.axis_fit(yt, yl, "y")

series = [("R_tool_m", (0, 0.5, 0.07), "green open diamonds"),
          ("R_tool", (0, 0, 0.83), "blue open squares"),
          ("R_mark_m", (0.87, 0.03, 0.02), "red open circles")]
rows = []
chk = []
for name, rgb, _ in series:
    ms = sorted(vec.stroke_markers(ds, rgb), key=lambda r: r.x0)
    for r in ms:
        cx, cy = vec.centre(r)
        chk.append((cx, cy))
        rows.append((name, round(float(ax * cx + bx), 2), round(float(ay * cy + by), 2)))

# consistency with Eq. (4) for xi = 0: R_tool = (R_tool_m + R_mark_m)/2
by_s = {n: [r for r in rows if r[0] == n] for n, _, _ in series}
dev = [abs((a[2] + c[2]) / 2 - b[2]) for a, b, c in zip(by_s["R_tool_m"], by_s["R_tool"], by_s["R_mark_m"])]
mean_tool = sum(r[2] for r in by_s["R_tool"]) / len(by_s["R_tool"])

hdr = [
    "zhangk2020 Fig. 8 (p. 9): Experimental results under various indentation depths.",
    "Provenance: tier 2, vector paths in the PDF (PyMuPDF get_drawings); marker centre = centre of the marker's stroked outline.",
    f"x calibration: tick marks {', '.join(f'{p:.2f} pt={v:g}' for p, v in px)}; max residual {rx:.3g} nm.",
    f"y calibration: tick marks {', '.join(f'{p:.2f} pt={v:g}' for p, v in py)}; max residual {ry:.3g} nm.",
    "Uncertainty: about 0.1 nm in both axes (PDF coordinate precision 0.01-0.1 pt; 1 pt = 0.85 nm in x, 0.45 nm in y).",
    "series: R_tool_m = green open diamonds, R_tool = blue open squares, R_mark_m = red open circles (labels in the plot, no legend box).",
    "x_indentation_depth_nm: indentation depth (nm); y_radius_nm: Evaluated Radius (nm).",
    f"Check (decompiler): |(R_tool_m + R_mark_m)/2 - R_tool| per depth = {', '.join(f'{d:.2f}' for d in dev)} nm (Eq. 4 with xi = 0);",
    f"mean of the R_tool points = {mean_tool:.2f} nm (text: 30.38 nm).",
]
vec.write_csv(HERE / "fig8.csv", hdr, ["series", "x_indentation_depth_nm", "y_radius_nm"], rows)
print("\n".join(hdr))
for r in rows:
    print(r)

vec.overlay_pts(PAGE, CLIP, chk, HERE.parent / "work" / "fig8_overlay.png")
