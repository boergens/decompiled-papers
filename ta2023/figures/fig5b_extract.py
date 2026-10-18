"""Digitize Figure 5(b) of Ta, Tran & Righi 2023 (p. 4): energy vs out-of-plane displacement of the H, OH and O
groups on C(110); legend OH (black), H2 (blue circles), H2O (red squares), OOH (green triangles).

Source: the embedded 300 ppi RGB image of Figure 5 (xref 316, 1407 x 581 px; panel b in its right half).
    python3 -I -B figures/fig5b_extract.py   -> figures/fig5b.csv (+ work/ov_fig5b.png for checking)
Method: tools/panel.py. The 0 A tick and the lower part of the y axis lie under insets, so the y axis is
calibrated on the major ticks 1..7 eV and the x axis on the major ticks 0.5..2.5 A. Markers overlap heavily at
x = 0, 0.25, 1.0 and 1.5 A (drawing order from the bottom: red squares, blue circles, green triangles, black
diamonds; the squares and circles are semi-transparent); those points were read from the colour-class maps of
tools/asciimap.py (visible edges of each marker) as the notes say.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = HERE.parent
sys.path.insert(0, str(KEY / "tools"))
from panel import run, write  # noqa: E402


def black(a):
    a = a.astype(int)
    return (a.mean(2) < 150) & ((a.max(2) - a.min(2)) < 40)


def red(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > g + 40) & (r > b + 40)


def blue(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (b > r + 40) & (b > g + 40) & ~((b > g + 40) & (g > r + 40))   # not the steel-blue call-outs


def green(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > r + 60) & (g > b + 60)


C0 = ("all four markers overlap at the origin; the red square's visible edges (columns 783-796, rows 436-450) "
      "give the centre, and the curves leave the cluster there")
cfg = dict(
    page=4, xref=316,
    vwin=(760, 785, 90, 560), hwin=(880, 1300, 480, 515), hline=((492, 492), (889, 1300)),
    ytop=7, ylow=0, ystep=1, xlow=0.5, xstep=0.5,
    plot=(772, 95, 1300, 490),
    exclude=[(778, 92, 882, 185), (778, 186, 882, 282), (778, 282, 882, 374),   # insets at the left
             (773, 466, 887, 567),                                              # inset at the bottom left
             (991, 88, 1097, 184), (1298, 80, 1407, 384),                        # insets top centre and right
             (758, 378, 805, 425), (1058, 164, 1110, 211), (1154, 343, 1206, 390),
             (1268, 161, 1319, 201), (1263, 354, 1318, 401),                     # call-outs 1, 2, 3, 3, 4
             (933, 389, 1047, 476)],                                             # legend
    overlay=str(KEY / "work" / "ov_fig5b.png"),
    series=[
        dict(name="OH", colour="black", mask=black, k=7, close=0, amin=40, size=(11, 11),
             manual=[(789.5, 443.0, "hidden", C0, 4),
                     (838.0, "curve", "hidden", "under the other markers at 0.25 A", 5, 434, 9),
                     (984.0, "curve", "hidden", "merged with the H2 circle at 1.0 A", 5, 312, 10)]),
        dict(name="H2", colour="blue", mask=blue, k=7, close=3, amin=60, size=(14, 14),
             manual=[(789.5, 443.0, "hidden", C0, 4),
                     (984.0, "curve", "hidden", "under the OH diamond at 1.0 A", 5, 314, 10),
                     (1081.5, 221.5, "partly hidden", "dotted line and OH curve across it; top edge row 215, centre "
                      "from it and the 14 px circle height", 4)]),
        dict(name="H2O", colour="red", mask=red, k=7, close=3, amin=60, size=(15, 15),
             manual=[(789.5, 443.0, "partly hidden", C0, 3),
                     (839.5, 438.0, "partly hidden", "under the H2 circle; visible edges columns 833-847, rows 431-445", 4),
                     (887.0, 417.5, "partly hidden", "under the H2 circle; visible edges columns 881-893, rows 410-425", 3),
                     (935.5, 377.0, "partly hidden", "top under the H2 circle; bottom edge row 384, centre from it and "
                      "the 15 px square height", 4),
                     (984.5, 322.0, "partly hidden", "under the H2 circle and OH diamond; visible edges columns "
                      "978-991, rows 315-329", 4)]),
        dict(name="OOH", colour="green", mask=green, k=7, close=3, dy=-1.5, amin=40, size=(10, 14),
             manual=[(789.5, 443.0, "hidden", C0, 4),
                     (838.0, 429.0, "partly hidden", "only the apex (row 422) is visible; centre = apex + 7 px, as for "
                      "the unobstructed triangles (apex to base 14 px)", 4),
                     (1032.5, 246.0, "partly hidden", "base under the H2 circle; apex row 239 visible, centre = apex + 7 px", 4),
                     (1081.0, 225.0, "partly hidden", "under the H2 circle; base row 232 visible, centre = base - 7 px", 4)]),
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 5(b): energy during the out-of-plane displacement of the H, OH and",
    "  O groups on C(110). Legend: OH (black line, grey square in the legend; the plotted markers are small grey diamonds),",
    "  H2 (blue circles), H2O (red squares), OOH (green triangles). The panel prints no y-axis title (energy, eV per the caption",
    "  and the other panels).",
    "Columns: series (legend names); displacement_A = x of the marker centre in Angstrom (measured, not snapped to 0.25 A);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 316); status ok / partly hidden / hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig5b_extract.py.",
    f"  y calibrated on the {len(c['majv'])} visible major ticks 1..7 (max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} visible major ticks 0.5..2.5 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px);",
    "  the 0 and -1 ticks and the 0 A tick lie under insets.",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening (7 px) of the closed colour mask;",
    "  green triangles -1.5 px row offset from the legend; covered markers from their visible edges (notes).",
    "Uncertainty: 2 px for clear markers (0.04 eV); 3-5 px for partly hidden or hidden ones (0.06-0.10 eV).",
    "  'hidden': value read from the cluster on top or from the series' curve on both sides (straight-line fit).",
    "The smooth curves of the figure are interpolations through the markers and are not given.",
]
write(HERE / "fig5b.csv", header, r["rows"])
print("fig5b:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
