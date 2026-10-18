"""Supplementary Fig. 5d, 5e, 5f, 5g (kubota2018 SI p. 14): digitize marker positions (tier 3).

Writes sfig5d.csv ... sfig5g.csv and ../work/supp_sfig5_overlay.png. Method in sfig45_common.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig45_common import WORK, overlay, run_panel, si_image, write_panel  # noqa: E402

DWELL = [("6.4 µsec", "red", "solid"), ("3.2 µsec", "orange", "dashed"),
         ("1.6 µsec", "blue", "solid"), ("0.8 µsec", "magenta", "dashed")]
KEV = [("1 keV", "black", "solid"), ("1.5 keV", "gray", "dashed"), ("2 keV", "magenta", "solid"),
       ("3 keV", "cyan", "dashed"), ("4 keV", "blue", "solid"), ("5 keV", "orange", "dashed"),
       ("6 keV", "red", "solid")]
# Depths printed above the imaged squares in panel c (nm), read off the image; columns are the
# dwell times 0.8, 1.6, 3.2, 6.4 µs (left to right, as in the panel b header), rows the keV.
# The second 1.5-keV value reads -38 but could be -36 (blurred JPEG digits).
PANEL_C = {6: [-173, -241, -242, -252], 5: [-176, -185, -205, -224], 4: [-82, -139, -123, -160],
           3: [-53, -95, -63, -91], 2: [-39, -45, -47, -60], 1.5: [-29, -38, -38, -50],
           1: [-17, -25, -24, -32]}
DW = [0.8, 1.6, 3.2, 6.4]
printed_d = {(f"{d:g} µsec", kev): PANEL_C[kev][i] for kev in PANEL_C for i, d in enumerate(DW)}
printed_f = {(f"{kev:g} keV", d): PANEL_C[kev][i] for kev in PANEL_C for i, d in enumerate(DW)}

IMG = "1084 x 951 px JPEG, 184 ppi"
COMMON = dict(page=14, ycol=887, xcol0=892, imgdesc=IMG, script="sfig5_extract.py")
XK = [1, 1.5, 2, 3, 4, 5, 6]
PANELS = {
    "d": dict(COMMON, name="d", row=220, rmax=216, y0=10, xvals=[0, 1, 2, 3, 4, 5, 6],
              yvals=[0, -50, -100, -150, -200, -250], xs=XK, series=DWELL, printed=printed_d,
              limits=[(1, None, 0, 120), (1.5, None, 0, 120)],
              title="Supplementary Figure 5d (kubota2018 SI): depression depth vs acceleration voltage, In-lens SE, one series per dwell time",
              xname="acceleration voltage, keV", yname="depression depth, nm"),
    "e": dict(COMMON, name="e", row=451, rmax=448, y0=260, xvals=[0, 1, 2, 3, 4, 5, 6], yvals=[6, 5, 4, 3, 2, 1, 0],
              xs=XK, series=DWELL,
              title="Supplementary Figure 5e (kubota2018 SI): electron dose vs acceleration voltage, one series per dwell time (no legend in e; colours as in d)",
              xname="acceleration voltage, keV", yname="electron dose, ke- nm-2 (axis label 'Electron dose (ke- nm-2)')"),
    "f": dict(COMMON, name="f", row=675, rmax=672, y0=489, xvals=[0, 0.8, 1.6, 3.2, 6.4],
              yvals=[0, -50, -100, -150, -200, -250], xs=DW, series=KEV, printed=printed_f,
              limits=[(None, "black", 0, 540)],
              title="Supplementary Figure 5f (kubota2018 SI): depression depth vs dwell time, one series per acceleration voltage (no legend in f; colours as in the g legend)",
              xname="dwell time, µsec", yname="depression depth, nm"),
    "g": dict(COMMON, name="g", row=902, rmax=898, y0=700, xvals=[0, 0.8, 1.6, 3.2, 6.4], yvals=[6, 5, 4, 3, 2, 1, 0],
              xs=DW, series=KEV, limits=[(None, None, 840, 999)],
              title="Supplementary Figure 5g (kubota2018 SI): electron dose vs dwell time, one series per acceleration voltage",
              xname="dwell time, µsec", yname="electron dose, ke- nm-2 (axis label read as 'Electron dose (ke- nm-2)')"),
}
EXTRA = {
    "d": ["printed_panel_c: the depth printed above each imaged square of panel c (columns 0.8, 1.6, 3.2, 6.4 µs left"
          " to right; rows 6 ... 1 keV); the second 1.5-keV value reads -38 but could be -36"],
    "e": ["decompiler's consistency check (arithmetic, not printed in panel e): dose = dose rate (5g legend) x dwell"
          " time gives 0.86-1.20 (6.4 µs), 0.43-0.60 (3.2 µs), 0.21-0.30 (1.6 µs), 0.11-0.15 ke- nm-2 (0.8 µs) for 1-6 keV;"
          " the digitized values run about 0.03-0.06 lower (1-2 px), and the 0.8 µs markers lie partly under the 1.6 µs"
          " markers, so their visible lower halves give values that are too low by up to about 0.1"],
    "f": ["printed_panel_c: as in sfig5d.csv; the same measurements as panel d, arranged by dwell time"],
    "g": ["legend (verbatim, with the dose rate in e- nm-2 µs-1 printed after each label): 1 keV 133.8; 1.5 keV 139.4;"
          " 2 keV 144.9; 3 keV 155.8; 4 keV 166.3; 5 keV 177.1; 6 keV 187.6",
          "all seven series lie within 0.1-1.2 ke- nm-2 (a few pixels) and overlap heavily; most markers are hidden",
          "decompiler's check: the 6 keV values agree with 187.6 e- nm-2 µs-1 x dwell time within 0.02"],
}

if __name__ == "__main__":
    img = si_image(14)
    ov_all = []
    for k, cfg in PANELS.items():
        rows, ov, info = run_panel(cfg, img)
        write_panel(cfg, rows, info, os.path.join(HERE, f"sfig5{k}.csv"), EXTRA.get(k, ()))
        ov_all += ov
        print(k, f"res_y={info['res_y']:.3g} res_x={info['res_x']:.3g} 1px={info['unit_y']:.3g}")
        for r in rows:
            print("  ", r[0], r[1], "" if r[3] != r[3] else round(r[3], 2), r[4], r[5], r[6])
    overlay(img, ov_all, os.path.join(WORK, "supp_sfig5_overlay.png"))
