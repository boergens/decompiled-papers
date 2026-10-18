"""Fig. 12: actual cutting edge radius (left axis) and uncertainty (right axis) vs indentation depth.
Vector paths -> fig12.csv.

Run: python3 -I -B figures/fig12_extract.py   (from any directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import vec  # noqa: E402

HERE = Path(__file__).resolve().parent
FIG, PAGE, CLIP = 12, 11, (150, 580, 435, 762)
CAPTION = "Figure 12. Experimental results using Cantilever 2."
TEXT = "text: average radius 29.67 nm, standard deviation 0.16 nm; standard deviation of the uncertainties 0.028 nm"
RED, BLUE = (0.87, 0.03, 0.02), (0, 0, 0.83)

ds = vec.drawings(PAGE, CLIP)
tx = vec.texts(PAGE, CLIP)
L, T, R, B = vec.frame(ds)
ax, bx, rx, px = vec.axis_fit(vec.tick_rects(ds, "x", B), [(t, r) for t, r in tx if r.y0 > B], "x")
ayl, byl, ryl, pyl = vec.axis_fit(vec.tick_rects(ds, "y", L), [(t, r) for t, r in tx if r.x1 < L], "y")
ayr, byr, ryr, pyr = vec.axis_fit(vec.tick_rects(ds, "y", R), [(t, r) for t, r in tx if r.x0 > R], "y")
legend = [r for t, r in tx if t in ("Cutting edge radius", "Uncertainty") and L < r.x0 < R]


def in_legend(c):
    return any(abs(c[1] - (r.y0 + r.y1) / 2) < 5 and r.x0 - 15 < c[0] < r.x0 for r in legend)


rows = []
stats = {}
chk = []
for name, rgb, a, b, marker in (("Cutting edge radius", BLUE, ayl, byl, "blue open square"),
                                ("Uncertainty", RED, ayr, byr, "red open square with an X inside")):
    vals = []
    for r in sorted(vec.stroke_markers(ds, rgb), key=lambda r: r.x0):
        c = vec.centre(r)
        if in_legend(c):
            continue
        y = round(float(a * c[1] + b), 4)
        chk.append(c)
        vals.append(y)
        rows.append((name, "left (The actual cutting edge radius nm)" if rgb == BLUE else "right (Uncertainty nm)",
                     round(float(ax * c[0] + bx), 2), y))
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5
    stats[name] = (m, sd, len(vals))


def cal(p):
    return ", ".join(f"{q:.2f} pt={v:g}" for q, v in p)


hdr = [
    f"zhangk2020 Fig. {FIG} (p. {PAGE}): {CAPTION}",
    "Provenance: tier 2, vector paths in the PDF (PyMuPDF get_drawings); marker centre = centre of the marker's stroked outline; legend markers dropped.",
    f"x calibration: tick marks {cal(px)}; max residual {rx:.3g} nm.",
    f"left y axis (The actual cutting edge radius, nm): tick marks {cal(pyl)}; max residual {ryl:.3g} nm.",
    f"right y axis (Uncertainty, nm): tick marks {cal(pyr)}; max residual {ryr:.3g} nm.",
    "series 'Cutting edge radius' (blue open squares) is read on the left axis, 'Uncertainty' (red open squares with an X inside) on the right axis.",
    "Uncertainty of the extraction: about 0.05 nm in x, 0.002 nm (left) and 0.0003 nm (right) in y (PDF coordinate precision).",
    "Check (decompiler): " + "; ".join(f"{k}: n={n}, mean {m:.4f} nm, sample SD {s:.4f} nm" for k, (m, s, n) in stats.items()),
    "(" + TEXT + ").",
]
vec.write_csv(HERE / f"fig{FIG}.csv", hdr, ["series", "axis", "x_indentation_depth_nm", "y_nm"], rows)
print("\n".join(hdr))
for r in rows:
    print(r)

vec.overlay_pts(PAGE, CLIP, chk, HERE.parent / "work" / "fig12_overlay.png")
