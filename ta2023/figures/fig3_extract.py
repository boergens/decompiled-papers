"""Digitize Figure 3 of Ta, Tran & Righi 2023 (p. 3): energy (blue, left axis) and force (red, right axis)
vs displacement for the detachment of a carbon chain on C(110).

Source: the embedded 300 ppi RGB image of Figure 3 (xref 285, 1000 x 665 px).
    python3 -I -B figures/fig3_extract.py   -> figures/fig3.csv (+ work/ov_fig3.png for checking)
Method: tools/panel.py. The left axis is drawn in blue, the right one in red; each is calibrated on its own
major ticks with a colour mask.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = HERE.parent
sys.path.insert(0, str(KEY / "tools"))
from panel import run, write  # noqa: E402


def axis_blue(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (b > r + 60) & (b > g + 60) & (r < 200)


def axis_red(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > g + 40) & (r > b + 40)


def red(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > g + 60) & (r > b + 60)


def blue(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (b > r + 50) & (b > g + 50) & ~((b > g + 40) & (g > r + 40))   # not the steel-blue call-outs


cfg = dict(
    page=3, xref=285,
    vmask=axis_blue, vwin=(40, 70, 60, 620), hwin=(55, 935, 590, 615),
    ylow=-1, ystep=1, xlow=0, xstep=0.5,
    vmask2=axis_red, vwin2=(925, 945, 60, 620), ylow2=0, ystep2=2,
    plot=(56, 112, 934, 598),
    exclude=[(140, 155, 940, 215)],             # numbered call-outs 1-6 above the dotted lines
    overlay=str(KEY / "work" / "ov_fig3.png"),
    series=[
        dict(name="Energy", colour="blue", mask=blue, k=7, close=3, amin=80, size=(23, 22),
             manual=[(741.0, "top", "partly hidden", "lower part under the force square", 4)]),
        dict(name="Force", colour="red", mask=red, k=7, close=3, amin=80, axis=2),
    ])
r = run(cfg)
c, c2 = r["cal"], r["cal2"]
for row in r["rows"]:
    row[0] = {"Energy": "Energy (eV)", "Force": "Force (nN)"}[row[0]]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 3: energy (blue circles, left axis, eV) and force (red squares,",
    "  right axis, nN; the axis title is printed 'Forcce (nN)') vs displacement during detachment of a carbon chain on C(110).",
    "Columns: series ('Energy (eV)' or 'Force (nN)'); displacement_A = x of the marker centre in Angstrom (measured);",
    "  value = y of the marker centre in the series' unit; value_unc = estimated uncertainty in that unit;",
    "  x_px, y_px = marker centre in the embedded image (xref 285); status; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig3_extract.py.",
    f"  Energy axis calibrated on the {len(c['majv'])} blue major ticks -1..9 eV (the 10 eV tick lies under the inset row;",
    f"  max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px); force axis on the {len(c2['maj'])} red major ticks 0..12 nN",
    f"  (max residual {c2['res']:.3f} nN, {abs(c2['my']):.4f} nN/px); x on the {len(c['majh'])} major ticks 0..2.5 A",
    f"  (max residual {c['res_x']:.4f} A).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening (7 px) of the closed colour mask.",
    "Uncertainty: 2 px for clear markers (0.04 eV, 0.05 nN); 5 px for partly hidden ones.",
    "The smooth blue curve and the dashed red curve of the figure are interpolations through the markers and are not",
    "  given; the dashed force curve dips to about -0.9 nN near x~1.35 A, below the markers either side of it.",
    "Black dotted lines mark steps 1-6 at x = 0.25, 0.5, 0.75, 1.0, 2.25, 2.5 A (call-outs and structure insets).",
]
write(HERE / "fig3.csv", header, r["rows"], ycol="value")
print("fig3:", len(r["rows"]), "points; y res", round(c["res_y"], 4), round(c2["res"], 4), "x res", round(c["res_x"], 4))
