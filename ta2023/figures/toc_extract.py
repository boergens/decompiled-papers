"""Digitize the abstract (table-of-contents) graphic of Ta, Tran & Righi 2023 (p. 1): energy (blue, left axis)
and force (red, right axis) vs displacement, with a green-to-red background gradient.

Source: the embedded 300 ppi RGB image on p. 1 (xref 197, 998 x 562 px).
    python3 -I -B figures/toc_extract.py   -> figures/toc.csv (+ work/ov_toc.png for checking)
Method: tools/panel.py; the marker colour masks are set tight enough to ignore the salmon/orange background.
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
    return (r > 200) & (g < 115) & (b < 100)


def blue(a):
    a = a.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (b > r + 100) & (b > g + 100)


cfg = dict(
    page=1, xref=197,
    vmask=axis_blue, vwin=(45, 65, 0, 505), hwin=(58, 935, 495, 515),
    ylow=-1, ystep=1, xlow=0, xstep=0.5,
    vmask2=axis_red, vwin2=(930, 948, 0, 505), ylow2=0, ystep2=2,
    vrows=(4, 500), hline=((500, 500), (60, 935)),
    plot=(60, 2, 935, 498),
    exclude=[],
    overlay=str(KEY / "work" / "ov_toc.png"),
    series=[
        dict(name="Energy", colour="blue", mask=blue, k=7, close=3, amin=60, size=(21, 20),
             manual=[(741.0, "top", "partly hidden", "lower part under the force square", 4)]),
        dict(name="Force", colour="red", mask=red, k=7, close=3, amin=80, axis=2),
    ])
r = run(cfg)
c, c2 = r["cal"], r["cal2"]
for row in r["rows"]:
    row[0] = {"Energy": "Energy (eV)", "Force": "Force (nN)"}[row[0]]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, abstract graphic (p. 1, no caption): energy (blue circles, left axis, eV)",
    "  and force (red squares, right axis, nN; axis title printed 'Forcce (nN)') vs displacement (A), with structure insets.",
    "  It shows the same curves as Figure 3 (compare figures/fig3.csv; README gives the agreement).",
    "Columns: series ('Energy (eV)' or 'Force (nN)'); displacement_A = x of the marker centre in Angstrom (measured);",
    "  value = y of the marker centre in the series' unit; value_unc = estimated uncertainty in that unit;",
    "  x_px, y_px = marker centre in the embedded image (xref 197); status; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by toc_extract.py.",
    f"  Energy axis calibrated on the {len(c['majv'])} blue major ticks -1..10 eV (max residual {c['res_y']:.3f} eV,",
    f"  {abs(c['my']):.4f} eV/px); force axis on the {len(c2['maj'])} red major ticks 0..12 nN (max residual {c2['res']:.3f} nN,",
    f"  {abs(c2['my']):.4f} nN/px); x on the {len(c['majh'])} major ticks 0..2.5 A (max residual {c['res_x']:.4f} A).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening (7 px) of the closed colour mask.",
    "Uncertainty: 2 px for clear markers; 5 px for partly hidden ones.",
    "The curves of the graphic are interpolations through the markers and are not given.",
]
write(HERE / "toc.csv", header, r["rows"], ycol="value")
print("toc:", len(r["rows"]), "points; y res", round(c["res_y"], 4), round(c2["res"], 4), "x res", round(c["res_x"], 4),
      c["majv"], c2["maj"], c["majh"])
