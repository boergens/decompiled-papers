"""Digitize Fig. 14 (p. 9 of the PDF, journal p. 031104-8): "TM and ER for two opaque defect sizes" (caption):
transmission (left panels) and extinction ratio (right panels) vs opaque defect density at 400, 600 and 800 nm, for
a 150 nm x 150 nm defect (a) and a 5 um x 5 um defect (b). Tier 3: one embedded JPEG (1872 x 1215 px, 300 ppi); no
vector paths on the page. Method: work/markers.py (category x axis from label centres, y from gridlines, each
value from the series' line on both sides of its marker, the marker centre as a check).
Writes figures/fig14a_left.csv, fig14a_right.csv, fig14b_left.csv, fig14b_right.csv, work/fig14_overlay.png.

    python3 -I -B figures/fig14_extract.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "work"))
import digi  # noqa: E402
import markers  # noqa: E402

a = digi.image(9, (89.2, 59.8, 538.5, 351.4))
T = [round(1.0 - 0.1 * k, 1) for k in range(11)]
E = [5000 - 500 * k for k in range(11)]
PANELS = {
    "a_left": dict(xl=((458, 490), 60, 900), grid=((290, 380), 0, 455, 11.0, 43.8, T), plot=(100, 725, 5, 452),
                   boxes=[(175, 20, 675, 80)], hint={"400nm": 103, "600nm": 112, "800nm": 116},
                   title="150nm x150nm opaque defect", ylabel="Transmission"),
    "a_right": dict(xl=((455, 490), 1040, 1872), grid=((1270, 1360), 0, 455, 10.0, 43.7, E),
                    plot=(1090, 1700, 5, 450), boxes=[(1138, 25, 1645, 88)],
                    hint={"400nm": 377, "600nm": 279, "800nm": 116},
                    title="150nm x150nm opaque defect", ylabel="Extinction Ratio"),
    "b_left": dict(xl=((1088, 1120), 115, 950), grid=((300, 400), 630, 1090, 643.0, 43.8, T),
                   plot=(118, 740, 637, 1084), boxes=[(180, 655, 645, 715)],
                   hint={"400nm": 735, "600nm": 744, "800nm": 748},
                   title="5 µm x 5 µm opaque defect", ylabel="Transmission"),
    "b_right": dict(xl=((1088, 1120), 1090, 1872), grid=((1270, 1360), 630, 1090, 643.0, 43.8, E),
                    plot=(1092, 1700, 637, 1084), boxes=[(1165, 655, 1620, 720)],
                    hint={"400nm": 1011, "600nm": 913, "800nm": 750},
                    title="5 µm x 5 µm opaque defect", ylabel="Extinction Ratio"),
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
    markers.write(os.path.join(HERE, "fig14%s.csv" % name), "14", "(%s) %s" % (name[0], name.split("_")[1]),
                  P["title"], P["ylabel"], rows, info,
                  ["The panel's title box and the legend ('wavelength', outside the plot) are not data."])
digi.overlay(a, [((255, 0, 255), allpts)], os.path.join(ROOT, "work", "fig14_overlay.png"))
