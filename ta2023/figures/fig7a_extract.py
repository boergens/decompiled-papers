"""Digitize Figure 7(a) 'Compression' of Ta, Tran & Righi 2023 (p. 6): energy vs displacement of the O atom on
C(110) at compressive stress 0 %, 3 %, 7 %, 10 % (legend: 0% grey circles, 3% red squares, 7% blue triangles,
10% green inverted triangles).

Source: the embedded 300 ppi RGB image of Figure 7 (xref 365, 1758 x 821 px; panel a in its left half).
    python3 -I -B figures/fig7a_extract.py   -> figures/fig7a.csv (+ work/ov_fig7a.png for checking)
Method: tools/panel.py. The semi-transparent red squares cover most grey 0 % circles; those circles are located
from the visible lower rim (bottom row - 11 px; unobstructed circles are 23 px tall), read from the colour-class
maps of tools/asciimap.py.
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
    return (b > r + 40) & (b > g + 40)


def green(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > r + 60) & (g > b + 60)


C0 = ("all four markers overlap at the origin under the 10% marker; the curves leave the cluster at its centre, "
      "so the 10% marker's centre is given")
RIM = "under the 3% square; lower rim visible, bottom row {} - 11 px"
cfg = dict(
    page=6, xref=365,
    vwin=(95, 125, 60, 760), hwin=(115, 900, 705, 716),
    ylow=-6, ystep=1, xlow=0, xstep=0.5,
    plot=(114, 62, 900, 709),
    exclude=[(116, 68, 309, 260), (314, 68, 507, 260), (510, 68, 702, 260), (705, 68, 898, 260),   # insets 0-10 %
             (120, 549, 290, 709),                                                              # 'initial' inset
             (715, 576, 858, 697)],                                                             # legend
    overlay=str(KEY / "work" / "ov_fig7a.png"),
    series=[
        dict(name="0%", colour="black", mask=black, k=9, close=3, amin=80, size=(23, 23),
             manual=[(141.0, 448.0, "hidden", C0, 4),
                     (213.5, 433.0, "partly hidden", RIM.format(444), 4),
                     (286.0, 383.0, "partly hidden", RIM.format(394), 4),
                     (359.0, 360.0, "partly hidden", RIM.format(371), 4),
                     (431.5, 333.0, "partly hidden", RIM.format(344), 4),
                     (720.0, 330.0, "partly hidden", RIM.format(341) + " (also under the 7% triangle)", 4),
                     (793.0, 305.0, "partly hidden", RIM.format(316), 4),
                     (864.0, "top", "partly hidden", "lower part under the 3% square", 4)]),
        dict(name="3%", colour="red", mask=red, k=9, close=3, dy=0.5, amin=80, size=(26, 24),
             drop=[(714.0, 312.0), (727.0, 312.5)],              # two halves of the square at 2.0 A (replaced below)
             manual=[(141.0, 448.0, "hidden", C0, 4),
                     (720.5, 318.0, "partly hidden", "the 7% triangle lies on top; square edges columns 709-732, rows "
                      "306-329 (+0.5 px legend offset)", 3)]),
        dict(name="7%", colour="blue", mask=blue, k=7, close=3, dy=0.0, amin=60, size=(18, 17),
             manual=[(141.0, 448.0, "hidden", C0, 4)]),
        dict(name="10%", colour="green", mask=green, k=7, close=3, dy=2.0, amin=60, size=(20, 19)),
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 7(a) 'Compression': energy vs displacement for oxygen on C(110)",
    "  under compressive stress; legend 0% (grey circles, black line), 3% (red squares), 7% (blue triangles),",
    "  10% (green downward triangles).",
    "Columns: series (legend names); displacement_A = x of the marker centre in Angstrom (measured, not snapped to 0.25 A);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 365); status ok / partly hidden / hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig7a_extract.py.",
    f"  y calibrated on the {len(c['majv'])} major ticks -6..7 eV (max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} major ticks 0..2.5 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening of the closed colour mask; row",
    "  offsets from the legend (circles 0, squares +0.5, triangles 0, downward triangles +2.0 px).",
    "Uncertainty: 2 px for clear markers (0.05 eV); 3-4 px for partly hidden or hidden ones (0.07-0.09 eV).",
    "The smooth curves are interpolations through the markers and are not given.",
]
write(HERE / "fig7a.csv", header, r["rows"])
print("fig7a:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
