"""Digitize Figure 2(b) of Ta, Tran & Righi 2023 (p. 3): energy vs displacement, ether configuration.

Source: the embedded 300 ppi RGB image of Figure 2 (xref 284, 1735 x 596 px; panel b in its middle third).
    python3 -I -B figures/fig2b_extract.py   -> figures/fig2b.csv (+ work/ov_fig2b.png for checking)
Method: tools/panel.py. In this panel the red triangles and blue circles are semi-transparent and the red
triangles are drawn on top of the green squares, so the masks are widened: the green mask also takes the
brown red-over-green mixture, and the red/blue masks take the paler colours.
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


def green(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return ((g > r + 60) & (g > b + 40)) | ((r > 120) & (b < 70) & (g < 150) & (r > g + 30))


H = "under the C(001) square and C(110) triangle drawn on top"
cfg = dict(
    page=3, xref=284,
    vwin=(630, 660, 100, 525), hwin=(650, 1160, 505, 530),
    ylow=-1, ystep=1, xlow=0, xstep=0.5,
    plot=(644, 100, 1160, 512),
    exclude=[(660, 40, 778, 392),      # three structure insets at the left
             (1038, 15, 1152, 130), (1038, 130, 1152, 242), (1038, 392, 1152, 502),   # insets at the right
             (694, 402, 752, 448), (1093, 336, 1152, 388)],   # call-outs 1 and 2
    overlay=str(KEY / "work" / "ov_fig2b.png"),
    series=[
        dict(name="C(001)", colour="green", mask=green, k=9, close=5, dy=-0.5, amin=100, size=(16, 16)),
        dict(name="C(110)", colour="red", mask=red, k=7, close=3, dy=-1.0, amin=60, size=(13, 12),
             drop=[(967.5, 332.0)]),                                    # red arrowhead
        dict(name="C(111)", colour="blue", mask=blue, k=7, close=3, dy=0.5, amin=60, size=(17, 16),
             drop=[(900.5, 369.0)],                                     # blue arrowhead
             manual=[(666.5, 475.5, "hidden", H + "; the C(111) curve leaves them at their centre, so the C(001) "
                      "square's centre is given", 4),
                     (723.5, "curve", "hidden", H, 4, 462, 10),
                     (780.5, "bottom", "partly hidden", "upper part under the C(001) square", 4),
                     (895.0, "bottom", "partly hidden", "upper part under the C(110) triangle", 4),
                     (1125.5, "top", "partly hidden", "lower edge touches call-out 2", 4)]),
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 2(b) 'Ether': energy vs displacement of the pulled O atom.",
    "Columns: series (legend names of Figure 2(a): C(001) green squares, C(110) red triangles, C(111) blue circles);",
    "  displacement_A = x of the marker centre in Angstrom (measured, not snapped to the 0.25 A step grid);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 284); status ok / partly hidden / hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig2b_extract.py.",
    f"  y calibrated on the {len(c['majv'])} major ticks -1..10 eV (max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} major ticks 0..2 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening of the closed colour mask;",
    "  row offsets (-0.5, -1.0, +0.5 px) from the legend of Figure 2(a) (same plot style).",
    "  Red triangles and blue circles are semi-transparent here; the red triangles lie on top of the green squares.",
    "Uncertainty: 2 px for clear markers (0.05 eV); 4-5 px for partly hidden or hidden ones (0.11-0.14 eV).",
    "  'hidden': value read from the marker on top or from the series' curve on both sides (straight-line fit).",
    "The smooth curves of the figure are interpolations through the markers and are not given.",
    "The arrows (first O detachment per the text) point at C(001) x~1.25 (green), C(110) x~1.25 (red), C(111) x~1.0 (blue).",
]
write(HERE / "fig2b.csv", header, r["rows"])
print("fig2b:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
