"""Digitize Figure 4(b) of Ta, Tran & Righi 2023 (p. 4): energy vs displacement of the ketone O atom on C(110)
with an additional O adatom O3 (red squares) or O4 (blue circles).

Source: the embedded 300 ppi RGB image of Figure 4 (xref 315, 1388 x 633 px; panel b in its right half).
    python3 -I -B figures/fig4b_extract.py   -> figures/fig4b.csv (+ work/ov_fig4b.png for checking)
Method: tools/panel.py. Both marker kinds are semi-transparent; the blue circles lie on top of the red squares.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = HERE.parent
sys.path.insert(0, str(KEY / "tools"))
from panel import run, write  # noqa: E402


def red(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > g + 40) & (r > b + 40)


def blue(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (b > r + 40) & (b > g + 40) & ~((b > g + 40) & (g > r + 40))   # not the steel-blue call-outs


SQ = ("under the O4 circle; centre from the square's visible corners (columns {}, rows {}) in the red mask, "
      "minus the 0.5 px legend offset")
cfg = dict(
    page=4, xref=315,
    vwin=(700, 730, 90, 560), hwin=(710, 1360, 530, 560),
    ylow=-1, ystep=1, xlow=0, xstep=0.5,
    plot=(717, 95, 1360, 534),
    exclude=[(718, 100, 852, 234), (718, 242, 852, 374),          # insets at the left
             (1252, 40, 1388, 182), (1252, 382, 1388, 517),       # insets at the right
             (708, 402, 768, 448), (1296, 296, 1356, 348),        # call-outs 1 and 2
             (980, 410, 1110, 480)],                             # legend
    overlay=str(KEY / "work" / "ov_fig4b.png"),
    series=[
        dict(name="O3", colour="red", mask=red, k=9, close=3, dy=-0.5, amin=100, size=(17, 17),
             manual=[(740.0, 479.0, "partly hidden", SQ.format("732-748", "471-488"), 3),
                     (798.5, 461.5, "partly hidden", SQ.format("791-806", "454-470"), 3),
                     (856.0, 412.0, "partly hidden", SQ.format("848-864", "404-421"), 3)]),
        dict(name="O4", colour="blue", mask=blue, k=9, close=5, dy=0.0, amin=100, size=(17, 17)),
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 4(b): energy change vs out-of-plane displacement of the ketone O atom",
    "  on C(110) with an additional O adatom: O3 (red squares) or O4 (blue circles) (legend names).",
    "Columns: series; displacement_A = x of the marker centre in Angstrom (measured, not snapped to the 0.25 A grid);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 315); status ok / partly hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig4b_extract.py.",
    f"  y calibrated on the {len(c['majv'])} major ticks -1..7 eV (max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} major ticks 0..2.5 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening (9 px) of the closed colour mask;",
    "  row offsets (-0.5 px squares, 0 px circles) from the legend, where the legend line passes through each marker.",
    "Uncertainty: 2 px for clear markers (0.04 eV); 3-5 px for partly hidden ones.",
    "The smooth curves of the figure are interpolations through the markers and are not given.",
]
write(HERE / "fig4b.csv", header, r["rows"])
print("fig4b:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
