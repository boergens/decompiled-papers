"""Digitize Figure 2(a) of Ta, Tran & Righi 2023 (p. 3): energy vs displacement, clean surfaces.

Source: the embedded 300 ppi RGB image of Figure 2 (xref 284, 1735 x 596 px; panel a in its left third).
    python3 -I -B figures/fig2a_extract.py   -> figures/fig2a.csv (+ work/ov_fig2a.png for checking)
Method: tools/panel.py (marker blobs after an elliptic opening; axis fit on the major ticks).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = HERE.parent
sys.path.insert(0, str(KEY / "tools"))
from panel import run, write  # noqa: E402

H = "under the C(001) square drawn on top"
cfg = dict(
    page=3, xref=284,
    vwin=(55, 80, 90, 520), hwin=(70, 570, 495, 530),       # windows holding the y and x axis lines
    ylow=-1, ystep=1, xlow=0, xstep=0.5,                      # labels of the lowest / leftmost major ticks
    plot=(68, 95, 570, 506),
    exclude=[(66, 95, 178, 362),      # three structure insets at the upper left
             (498, 0, 610, 114),      # blue-framed inset, top right
             (500, 144, 614, 225),    # green-framed inset, right
             (490, 340, 602, 440),    # red-framed inset, lower right
             (336, 405, 470, 480),    # legend
             (100, 378, 158, 428), (514, 262, 570, 314)],   # call-outs 1 and 2
    overlay=str(KEY / "work" / "ov_fig2a.png"),
    series=[
        dict(name="C(001)", colour="green", k=7, close=3, dy=-0.5, amin=100,
             manual=[(507.5, "bottom", "partly hidden", "top edge under the green-framed inset", 4)]),
        dict(name="C(110)", colour="red", k=7, close=3, dy=-1.0, amin=70,
             manual=[(86.5, "curve", "hidden", H, 4, 470, 10)]),
        dict(name="C(111)", colour="blue", k=7, close=3, dy=0.5, amin=100,
             manual=[(86.5, 469.0, "hidden", H + "; the C(111) curve leaves the square at its centre, so the "
                      "C(001) square's centre is given", 4),
                     (131.0, "curve", "hidden", H, 4, 458, 10),
                     (177.5, "curve", "hidden", H, 4, 418, 10)]),
    ])
r = run(cfg)
c = r["cal"]
header = [
    "Ta, Tran & Righi 2023, Langmuir 39, 14396, Figure 2(a) 'Clean surface': energy vs displacement of the pulled C atom.",
    "Columns: series (legend names C(001) green squares, C(110) red triangles, C(111) blue circles);",
    "  displacement_A = x of the marker centre in Angstrom (measured, not snapped to the 0.25 A step grid);",
    "  energy_eV = y of the marker centre in eV; energy_eV_unc = estimated uncertainty in eV;",
    "  x_px, y_px = marker centre in the embedded image (xref 284); status ok / partly hidden / hidden; note.",
    "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig2a_extract.py.",
    f"  y calibrated on the {len(c['majv'])} major ticks -1..10 eV (max residual {c['res_y']:.3f} eV, {abs(c['my']):.4f} eV/px);",
    f"  x on the {len(c['majh'])} major ticks 0..2.5 A (max residual {c['res_x']:.4f} A, {abs(c['mx']):.5f} A/px).",
    "  Marker centre = bbox centre of the colour blob left after an elliptic opening (7 px) of the closed colour mask;",
    "  row offsets (-0.5, -1.0, +0.5 px) from the legend, where the legend line passes through each marker.",
    "Uncertainty: 2 px for clear markers (0.05 eV); 4-5 px for partly hidden or hidden ones (0.11-0.14 eV).",
    "  'hidden': the marker lies under another one; its value is read from that marker or from the series' curve",
    "  on both sides of it (straight-line fit), as the note says.",
    "The smooth curves of the figure are interpolations through the markers and are not given.",
    "The C(001) curve continues past the last listed square (x~2.3) under the green-framed inset; any further marker",
    "  there is hidden. The arrows (first-atom detachment per the text) point at C(001) x~1.0, C(110) x~1.25, C(111) x~1.75.",
]
write(HERE / "fig2a.csv", header, r["rows"])
print("fig2a:", len(r["rows"]), "points; y res", round(c["res_y"], 4), "x res", round(c["res_x"], 4))
