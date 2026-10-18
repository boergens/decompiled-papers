"""Digitize Figure 6(b) of Ta, Tran & Righi 2023 (p. 5): energy vs displacement for the detachment of a silicate
cluster from C(110); legend Case #1 (blue squares), Case #2 (red circles), Case #3 (grey triangles, black line).

Source: the embedded 300 ppi RGB image of Figure 6 (xref 342, 1718 x 803 px; panel b in its right half).
    python3 -I -B figures/fig6b_extract.py   -> figures/fig6b.csv (+ work/ov_fig6b.png for checking)
Method: tools/panel.py. Markers that others cover were read from the colour-class maps of
tools/asciimap.py (visible edges), as the notes say.
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
    return (b > r + 40) & (b > g + 40) & ~((b > g + 40) & (g > r + 70))   # not the steel-blue call-outs


C0 = ("all three markers overlap at the origin; the Case #1 square's visible edges (columns 901-922, rows 599-621) "
      "give the centre, and the curves leave the cluster there")
cfg = dict(
    page=5, xref=342,
    vwin=(860, 895, 60, 720), hwin=(880, 1710, 684, 694), hline=((688, 689), (882, 1710)),
    ylow=-1, ystep=1, xlow=0, xstep=0.5,
    plot=(882, 62, 1715, 686),
    exclude=[(894, 90, 1015, 210), (894, 212, 1015, 333), (890, 337, 1010, 457),       # insets at the left
             (1099, 58, 1217, 137), (1099, 140, 1218, 260), (1099, 261, 1218, 382),   # insets at 0.75 A
             (1340, 58, 1459, 148), (1341, 149, 1462, 269),                           # insets at 1.5 A
             (1244, 539, 1365, 662), (1590, 406, 1710, 527), (1592, 526, 1717, 648),  # lower insets
             (885, 503, 940, 553), (1121, 571, 1176, 623), (1274, 463, 1327, 512),
             (1351, 472, 1405, 521), (1658, 335, 1712, 388),                          # call-outs 1-5
             (1519, 103, 1682, 200)],                                                 # legend
    overlay=str(KEY / "work" / "ov_fig6b.png"),
    series=[
        dict(name="Case #1", colour="blue", mask=blue, k=9, close=3, dy=-0.5, amin=100, size=(23, 23),
             manual=[(911.5, 609.5, "partly hidden", C0, 3),
                     (988.5, 603.5, "partly hidden", "top under the Case #2 circle; bottom edge row 615, centre from it "
                      "and the 23 px square height", 4)]),
        dict(name="Case #2", colour="red", mask=red, k=9, close=3, dy=0.0, amin=100, size=(22, 23),
             manual=[(911.5, 610.0, "hidden", C0, 4),
                     (989.5, 590.0, "partly hidden", "lower part merges with the Case #1 square; top edge row 579, "
                      "centre from it and the 23 px circle height", 4)]),
        dict(name="Case #3", colour="black", mask=black, k=7, close=0, dy=-2.5, amin=60, size=(17, 17),
             manual=[(911.5, 610.0, "hidden", C0, 4),
                     (988.5, "curve", "hidden", "under the Case #2 circle", 5, 590, 13),
                     (1066.0, "curve", "hidden", "under the Case #2 circle", 5, 538, 13, 22),
                     (1220.5, "curve", "hidden", "under the Case #1 square", 5, 428, 13),
                     (1683.0, 289.0, "partly hidden", "lower part under the Case #2 circle; apex row 279 visible, "
                      "centre = apex + 10 px (unobstructed triangles: apex to base 21 px)", 4)]),
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 6(b): energy vs displacement during detachment of a silicate cluster",
    "  from C(110). Legend: Case #1 (blue squares), Case #2 (red circles), Case #3 (grey triangles, black line).",
    "Columns: series (legend names); displacement_A = x of the marker centre in Angstrom (measured, not snapped to 0.25 A);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 342); status ok / partly hidden / hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig6b_extract.py.",
    f"  y calibrated on the {len(c['majv'])} major ticks -1..7 eV (max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} major ticks 0..2.5 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening of the closed colour mask; row",
    "  offsets from the legend (squares -0.5 px, circles 0, triangles -2.5 px, where the opening blunts the apex).",
    "Uncertainty: 2 px for clear markers (0.03 eV); 3-5 px for partly hidden or hidden ones (0.04-0.07 eV).",
    "  'hidden': value read from the cluster on top or from the series' curve on both sides (straight-line fit).",
    "Case #1 has no markers beyond x~2.0 A (its curve ends there). The smooth curves are interpolations and are not given.",
]
write(HERE / "fig6b.csv", header, r["rows"])
print("fig6b:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
