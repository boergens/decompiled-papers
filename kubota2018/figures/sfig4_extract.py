"""Supplementary Fig. 4d, 4e, 4f, 4g (kubota2018 SI p. 13): digitize marker positions (tier 3).

Writes sfig4d.csv ... sfig4g.csv and ../work/supp_sfig4_overlay.png. Method in sfig45_common.py.
Also writes sfig4c_inset.csv (tier 4, read by eye; see the notes there).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig45_common import WORK, overlay, run_panel, si_image, write_csv, write_panel  # noqa: E402

DWELL = [("6.4 µsec", "red", "solid"), ("3.2 µsec", "orange", "dashed"),
         ("1.6 µsec", "blue", "solid"), ("0.8 µsec", "magenta", "dashed")]
KEV = [("2 keV", "gray", "solid"), ("3 keV", "cyan", "dashed"), ("4 keV", "blue", "solid"),
       ("5 keV", "orange", "dashed"), ("6 keV", "red", "solid")]
# Depths printed under the imaged squares in panel c (nm), read off the image; columns are the
# dwell times 0.8, 1.6, 3.2, 6.4 µs (left to right, as in the panel b header), rows the keV.
PANEL_C = {6: [-240, -245, -250, -265], 5: [-169, -131, -147, -165], 4: [-80, -94, -95, -98],
           3: [-93, -82, -74, -92], 2: [-65, -63, -67, -67]}
DW = [0.8, 1.6, 3.2, 6.4]
printed_d = {(f"{d:g} µsec", kev): PANEL_C[kev][i] for kev in PANEL_C for i, d in enumerate(DW)}
printed_f = {(f"{kev} keV", d): PANEL_C[kev][i] for kev in PANEL_C for i, d in enumerate(DW)}

IMG = "885 x 595 px JPEG, 150 ppi"
COMMON = dict(page=13, ycol=760, xcol0=762, imgdesc=IMG, script="sfig4_extract.py")
PANELS = {
    "d": dict(COMMON, name="d", row=127, y0=5, xvals=[0, 1, 2, 3, 4, 5, 6], yvals=[0, -50, -100, -150, -200, -250],
              xs=[2, 3, 4, 5, 6], series=DWELL, limits=[(2, None, 0, 70)], printed=printed_d,
              title="Supplementary Figure 4d (kubota2018 SI): depression depth vs acceleration voltage, BSD, one series per dwell time",
              xname="acceleration voltage, keV", yname="depression depth, nm"),
    "e": dict(COMMON, name="e", row=272, y0=150, xvals=[0, 1, 2, 3, 4, 5, 6], yvals=[6, 5, 4, 3, 2, 1, 0],
              xs=[2, 3, 4, 5, 6], series=DWELL,
              title="Supplementary Figure 4e (kubota2018 SI): electron dose vs acceleration voltage, one series per dwell time (no legend in e; colours as in d)",
              xname="acceleration voltage, keV", yname="electron dose, ke- nm-2 (axis label 'Electron dose (ke- nm-2)')"),
    "f": dict(COMMON, name="f", row=414, y0=295, xvals=[0, 0.8, 1.6, 3.2, 6.4], yvals=[0, -50, -100, -150, -200, -250],
              xs=[0.8, 1.6, 3.2, 6.4], series=KEV, printed=printed_f,
              title="Supplementary Figure 4f (kubota2018 SI): depression depth vs dwell time, one series per acceleration voltage (no legend in f; colours as in the g legend)",
              xname="dwell time, µsec", yname="depression depth, nm"),
    "g": dict(COMMON, name="g", row=563, y0=440, xvals=[0, 0.8, 1.6, 3.2, 6.4], yvals=[6, 5, 4, 3, 2, 1, 0],
              xs=[0.8, 1.6, 3.2, 6.4], series=KEV, limits=[(0.8, None, 505, 999), (1.6, None, 505, 999), (3.2, None, 505, 999)],
              title="Supplementary Figure 4g (kubota2018 SI): electron dose vs dwell time, one series per acceleration voltage",
              xname="dwell time, µsec", yname="electron dose (axis label printed 'Electron dose (e- nm-2)', but the values 0-6 match panel e in ke- nm-2)"),
}
EXTRA = {
    "d": ["printed_panel_c: the depth printed under each imaged square of panel c (columns 0.8, 1.6, 3.2, 6.4 µs left"
          " to right; rows 6 ... 2 keV); the digitized markers agree with these within about 2-4 nm where visible"],
    "f": ["printed_panel_c: as in sfig4d.csv; the same measurements as panel d, arranged by dwell time"],
    "g": ["legend (verbatim, with the dose rate in e- nm-2 µs-1 printed after each label): 2 keV 714.5; 3 keV 768.7;"
          " 4 keV 822.9; 5 keV 877.1; 6 keV 931.2 (the 931.2 is printed on the line below '6 keV')",
          "decompiler's check: dose rate x dwell time (e.g. 931.2 x 6.4 = 5.96, 714.5 x 6.4 = 4.57 ke- nm-2) agrees"
          " with the clearly visible markers within about 0.05; the small-blob value of 2 keV at 3.2 µs (2.15) is"
          " 0.14 below 714.5 x 3.2 = 2.29 and is unreliable"],
    "e": ["decompiler's check: the values agree with the panel g legend dose rates x dwell time within about 0.05"],
}

if __name__ == "__main__":
    img = si_image(13)
    ov_all = []
    for k, cfg in PANELS.items():
        rows, ov, info = run_panel(cfg, img)
        write_panel(cfg, rows, info, os.path.join(HERE, f"sfig4{k}.csv"), EXTRA.get(k, ()))
        ov_all += ov
        print(k, f"res_y={info['res_y']:.3g} res_x={info['res_x']:.3g} 1px={info['unit_y']:.3g}")
        for r in rows:
            print("  ", r[0], r[1], "" if r[3] != r[3] else round(r[3], 2), r[4], r[5], r[6])
    overlay(img, ov_all, os.path.join(WORK, "supp_sfig4_overlay.png"))

    # Inset graph of panel c (bottom right): white marks on the colour height map, about 75 x 60 px.
    # Too faint and small for colour masks; the marker centres and tick-label centres were located by
    # eye on an 8x zoom of the native image (whiteness = min(R,G,B) > 180), rows/cols in the embedded image.
    ylab_rows = {-50: 512.3, -100: 524.0, -150: 536.0, -200: 549.0, -250: 564.0}  # centres of the y tick labels
    import numpy as np
    m, b = np.polyfit(list(ylab_rows.values()), list(ylab_rows.keys()), 1)
    marks = [(2, 670.5, 514.5), (3, 681.5, 520.0), (4, 693.0, 521.0), (5, 703.5, 537.5), (6, 715.0, 563.5)]
    rows = []
    for kev, cx, cy in marks:
        mean_c = sum(PANEL_C[kev]) / 4
        rows.append(("average", kev, m * cy + b, mean_c, cx, cy))
    write_csv(os.path.join(HERE, "sfig4c_inset.csv"), [
        "Supplementary Figure 4c, inset graph at the bottom right of panel c (kubota2018 SI): averaged depression depth"
        " per acceleration voltage ('Inlet graph at right bottom indicates averaged depression depth for each acceleration voltage')",
        "columns: series, acceleration_voltage_keV (nominal, x ticks 1 ... 6), depth_nm (read from the inset),"
        " mean_of_panel_c_values_nm (decompiler's arithmetic mean of the four depths printed in panel c for that keV,"
        " for comparison; not printed in the figure), pixel_x, pixel_y",
        "provenance: tier 4, read by eye: white marks (axis, ticks, labels, markers with short error bars) on the"
        " colour height map, about 75 x 60 px in the embedded 150 ppi JPEG; the y tick labels (-50 ... -250) are"
        " barely legible; y calibrated on the centres of the tick labels (linear fit), marker centres located by eye"
        " on an 8x zoom; script sfig4_extract.py",
        "uncertainty: about +-10 nm in y; error bars are visible at 3 and 5 keV but their ends cannot be read",
        "no marker visible at 1 keV",
    ], ["series", "acceleration_voltage_keV", "depth_nm", "mean_of_panel_c_values_nm", "pixel_x", "pixel_y"], rows,
        fmt=["{}", "{:g}", "{:.0f}", "{:.1f}", "{:.1f}", "{:.1f}"])
    for r in rows:
        print("inset", r[1], round(r[2]), r[3])
