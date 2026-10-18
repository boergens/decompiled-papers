"""Digitize Figure 7(b) 'Expansion' of Ta, Tran & Righi 2023 (p. 6): energy vs displacement of the O atom on
C(110) under expansion 0 %, 3 %, 7 %, 10 % (legend: 0% grey circles, 3% red squares, 7% blue triangles,
10% green inverted triangles).

Source: the embedded 300 ppi RGB image of Figure 7 (xref 365, 1758 x 821 px; panel b in its right half).
    python3 -I -B figures/fig7b_extract.py   -> figures/fig7b.csv (+ work/ov_fig7b.png for checking)
Method: tools/panel.py. Covered markers (grey circles under red squares, blue triangles under the green downward
triangles) are located from their visible apex, base or rim (unobstructed circles and triangles are 23 px tall),
read from the colour-class maps of tools/asciimap.py.
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
AP = "base under the 10% downward triangle; apex row {} visible, centre = apex + 11 px (unobstructed triangles: 23 px)"
BA = "apex under the {}; base row {} visible, centre = base - 11 px (unobstructed triangles: 23 px)"
cfg = dict(
    page=6, xref=365,
    vwin=(955, 990, 60, 760), hwin=(975, 1755, 705, 716),
    ylow=-1, ystep=1, xlow=0, xstep=0.5,
    plot=(975, 62, 1755, 709),
    exclude=[(973, 68, 1166, 264), (1170, 68, 1361, 264), (1363, 68, 1555, 264), (1555, 68, 1749, 264),  # insets
             (981, 315, 1175, 480),                                                                   # 'initial'
             (1589, 556, 1727, 677)],                                                                 # legend
    overlay=str(KEY / "work" / "ov_fig7b.png"),
    series=[
        dict(name="0%", colour="black", mask=black, k=9, close=3, amin=80, size=(23, 23),
             manual=[(1002.5, 638.5, "hidden", C0, 4),
                     (1074.5, "curve", "hidden", "between the 3% square and the 10% triangle only a strip of the grey fill "
                      "(rows 606-612) is visible", 5, 612, 14, 16),
                     (1146.0, "bottom", "partly hidden", "upper part under the 3% square", 4),
                     (1219.0, "curve", "hidden", "under the 3% square and 7% triangle", 5, 497, 13, 16),
                     (1290.5, "bottom", "partly hidden", "upper part under the 3% square", 4),
                     (1653.0, "curve", "hidden", "under the 3% square", 5, 404, 14, 16)]),
        dict(name="3%", colour="red", mask=red, k=9, close=3, dy=0.5, amin=80, size=(26, 24),
             manual=[(1002.5, 638.5, "hidden", C0, 4)]),
        dict(name="7%", colour="blue", mask=blue, k=7, close=3, dy=0.0, amin=60, size=(18, 17),
             manual=[(1002.5, 638.5, "hidden", C0, 4),
                     (1073.0, 630.0, "partly hidden", BA.format("10% downward triangle", 641), 4),
                     (1147.0, 583.0, "partly hidden", AP.format(572), 4),
                     (1218.5, 502.0, "partly hidden", BA.format("3% square", 513), 4),
                     (1291.0, 406.0, "partly hidden", AP.format(395), 4),
                     (1363.5, 364.0, "partly hidden", BA.format("10% downward triangle", 375), 4),
                     (1436.0, 363.0, "partly hidden", AP.format(352), 4),
                     (1508.0, 362.0, "partly hidden", AP.format(351), 4),
                     (1580.0, 361.0, "partly hidden", AP.format(350), 4),
                     (1653.0, 359.0, "partly hidden", AP.format(348), 4),
                     (1724.0, 358.0, "partly hidden", AP.format(347), 4)]),
        dict(name="10%", colour="green", mask=green, k=7, close=3, dy=2.0, amin=60, size=(20, 19),
             manual=[(1147.0, 591.5, "partly hidden", "the 10% curve merges with the marker's right edge; top edge "
                      "row 580.5 and left edge column 1136 visible, centre = top + 11 px", 4)]),
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 7(b) 'Expansion': energy vs displacement for oxygen on C(110)",
    "  under expansion; legend 0% (grey circles, black line), 3% (red squares), 7% (blue triangles),",
    "  10% (green downward triangles).",
    "Columns: series (legend names); displacement_A = x of the marker centre in Angstrom (measured, not snapped to 0.25 A);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 365); status ok / partly hidden / hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig7b_extract.py.",
    f"  y calibrated on the {len(c['majv'])} major ticks -1..7 eV (max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} major ticks 0..2.5 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening of the closed colour mask; row",
    "  offsets from the legend (circles 0, squares +0.5, triangles 0, downward triangles +2.0 px).",
    "Uncertainty: 2 px for clear markers (0.03 eV); 4-5 px for partly hidden or hidden ones (0.06-0.07 eV).",
    "The smooth curves are interpolations through the markers and are not given.",
]
write(HERE / "fig7b.csv", header, r["rows"])
print("fig7b:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
