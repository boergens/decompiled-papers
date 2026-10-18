"""Digitize Figure 2(c) of Ta, Tran & Righi 2023 (p. 3): energy vs displacement, ketone configuration.

Source: the embedded 300 ppi RGB image of Figure 2 (xref 284, 1735 x 596 px; panel c in its right third).
    python3 -I -B figures/fig2c_extract.py   -> figures/fig2c.csv (+ work/ov_fig2c.png for checking)
Method: tools/panel.py. Drawing order in this panel: green squares at the bottom, semi-transparent red
triangles over them, semi-transparent blue circles on top, the curves over the markers. Green squares that
the others cover are located from their visible edges (figtools.square_edges).
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
    return (b > r + 40) & (b > g + 40)


SQ = "covered by the C(110) triangle and/or C(111) circle"
cfg = dict(
    page=3, xref=284,
    vwin=(1185, 1215, 100, 525), hwin=(1200, 1735, 505, 530),
    ylow=-1, ystep=1, xlow=0, xstep=0.5,
    plot=(1200, 100, 1735, 512),
    exclude=[(1196, 25, 1310, 368),                                    # three structure insets at the left
             (1610, 15, 1725, 120), (1610, 120, 1725, 234), (1610, 398, 1725, 514),   # insets at the right
             (1238, 393, 1297, 440), (1678, 224, 1735, 278)],          # call-outs 1 and 2
    overlay=str(KEY / "work" / "ov_fig2c.png"),
    series=[
        dict(name="C(001)", colour="green", k=13, close=11, dy=-0.5, amin=100, size=(17, 16),
             manual=[(1218.0, "square", "partly hidden", SQ, 4, 477),
                     (1268.0, 465.5, "partly hidden", SQ + "; top edge (row 458) and left edge (column 1260) "
                      "visible, centre from them and the 16 px marker size", 5),
                     (1463.0, "square", "partly hidden", SQ, 4, 386),
                     (1512.0, "square", "partly hidden", SQ, 4, 386),
                     (1561.0, "square", "partly hidden", SQ, 4, 386),
                     (1608.0, "square", "partly hidden", SQ, 4, 386)]),
        dict(name="C(110)", colour="red", mask=red, k=7, close=3, dy=-1.0, amin=60, size=(13, 12),
             drop=[(1378.0, 422.0)],                                    # red arrowhead
             manual=[(1218.5, 477.0, "hidden", "under the C(111) circle; the C(110) curve leaves it at its centre, "
                      "so the circle's centre is given", 4),
                     (1268.0, "curve", "hidden", "under the C(111) circle", 4, 466, 10),
                     (1512.0, 389.0, "partly hidden", "apex under the C(111) circle; base visible at row 396, centre "
                      "= base - 7 px as for the unobstructed triangles", 4)]),
        dict(name="C(111)", colour="blue", mask=blue, k=7, close=3, dy=0.5, amin=60, size=(17, 16),
             drop=[(1462.5, 340.5)]),                                   # blue arrowhead
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 2(c) 'Ketone': energy vs displacement of the pulled O atom.",
    "Columns: series (legend names of Figure 2(a): C(001) green squares, C(110) red triangles, C(111) blue circles);",
    "  displacement_A = x of the marker centre in Angstrom (measured, not snapped to the 0.25 A step grid);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 284); status ok / partly hidden / hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig2c_extract.py.",
    f"  y calibrated on the {len(c['majv'])} major ticks -1..9 eV (the 10 eV tick is under an inset; max residual "
    f"{c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} major ticks 0..2.5 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening of the closed colour mask;",
    "  row offsets (-0.5, -1.0, +0.5 px) from the legend of Figure 2(a) (same plot style).",
    "Uncertainty: 2 px for clear markers (0.05 eV); 4-5 px for partly hidden or hidden ones (0.11-0.14 eV).",
    "  'hidden': value read from the marker on top or from the series' curve on both sides (straight-line fit).",
    "The smooth curves of the figure are interpolations through the markers and are not given.",
    "The arrows (first C detachment per the text) point at C(001) x~0.75 (green), C(110) x~0.75 (red), C(111) x~1.25 (blue).",
    "Text check: the text gives 1.97, 2.51 and 3.13 eV for C(110), C(001), C(111); the arrowed markers read about",
    "  1.96, 2.74 and 3.13 eV here; the C(001) plateau from x=1 to 2.5 reads 2.47-2.52 eV (see README).",
]
write(HERE / "fig2c.csv", header, r["rows"])
print("fig2c:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
