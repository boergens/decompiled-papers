"""Digitize Fig. 13 (p. 8 of the PDF, journal p. 031104-7): transmission and extinction ratio vs "clear" defect
density at 400, 600 and 800 nm, for a 150 nm x 150 nm defect (a) and a 5 um x 5 um defect (b); left panels
transmission, right panels extinction ratio. Tier 3: one embedded JPEG (1908 x 1243 px, 300 ppi); no vector
paths on the page. Method: work/markers.py (category x axis from label centres, y from gridlines, each value
from the series' line on both sides of its marker, the marker centre as a check).
Writes figures/fig13a_left.csv, fig13a_right.csv, fig13b_left.csv, fig13b_right.csv, work/fig13_overlay.png.

    python3 -I -B figures/fig13_extract.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "work"))
import digi  # noqa: E402
import markers  # noqa: E402

a = digi.image(8, (84.9, 417.0, 542.8, 715.4))
T = [round(1.0 - 0.1 * k, 1) for k in range(11)]
E = [5000 - 500 * k for k in range(11)]
PANELS = {
    "a_left": dict(xl=((490, 525), 60, 900), grid=((180, 260), 0, 470, 9.3, 45.47, T), plot=(100, 745, 5, 470),
                   boxes=[(130, 5, 570, 65)], hint={"400nm": 105, "600nm": 116, "800nm": 120},
                   title="150nm x150nm clear defect", ylabel="Transmission"),
    "a_right": dict(xl=((490, 525), 1040, 1900), grid=((1170, 1250), 0, 470, 11.84, 45.33, E),
                    plot=(1092, 1735, 5, 470), boxes=[(1150, 5, 1600, 75)],
                    hint={"400nm": 402, "600nm": 293, "800nm": 121},
                    title="150nm x150nm clear defect", ylabel="Extinction Ratio"),
    "b_left": dict(xl=((1140, 1165), 60, 900), grid=((180, 260), 640, 1115, 653.51, 45.45, T),
                   plot=(100, 745, 645, 1112), boxes=[(135, 650, 545, 720)],
                   hint={"400nm": 751, "600nm": 760, "800nm": 765},
                   title="5 µm x 5 µm clear defect", ylabel="Transmission"),
    "b_right": dict(xl=((1140, 1165), 1040, 1900), grid=((1170, 1250), 640, 1115, 653.53, 45.45, E),
                    plot=(1092, 1735, 645, 1112), boxes=[(1175, 650, 1570, 725)],
                    hint={"400nm": 1043, "600nm": 935, "800nm": 767},
                    title="5 µm x 5 µm clear defect", ylabel="Extinction Ratio"),
}
allpts = []
for name, P in PANELS.items():
    rows, pts, info = markers.panel(a, P)
    allpts += pts
    print(name, "grid res %.3g, skipped %s" % (info["grid_res"], info["skipped"]))
    for r in rows:
        print("  %-6s %6d %8.4g  marker %8s  spread %s" % (r["series"], r["category"], r["value"],
              "%.4g" % r["marker_value"] if r["marker_value"] is not None else "-",
              "%.2g" % r["side_spread"] if r["side_spread"] is not None else "-"))
    markers.write(os.path.join(HERE, "fig13%s.csv" % name), "13", "(%s) %s" % (name[0], name.split("_")[1]),
                  P["title"], P["ylabel"], rows, info,
                  ["The panel's title box and the legend ('wavelength', outside the plot) are not data."])
digi.overlay(a, [((255, 0, 255), allpts)], os.path.join(ROOT, "work", "fig13_overlay.png"))
