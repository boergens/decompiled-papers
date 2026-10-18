"""Fig. 6g and 6h of Kubota et al. 2018 (main PDF p. 10): Michelson contrast and CNR vs acceleration voltage,
BSD (filled circles, solid line) and In-Lens SE (open circles, dashed line).

Tier 1: the plotted values are listed in Supplementary Table 3 ("Michelson contrast and Contrast-to-noise
ratio", Supplementary Information p. 25; the table is an image in that PDF, the numbers below were read off it).
This script writes them to fig6g.csv / fig6h.csv and checks them against the published raster plots: each
value is mapped into the embedded 300 ppi image through the tick calibration, the marker centre is located
next to it, and the offset is reported (CSV header + ../work/fig6g_overlay.png, fig6h_overlay.png).
    python3 -I fig6gh_extract.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from kubota_main_common import Img, calib, opened, blobs, WORK  # noqa: E402
from digitize_common import tick_positions, tick_positions_v, write_csv, overlay  # noqa: E402

# Supplementary Table 3, transcribed from the table image (Supplementary Information p. 25)
TABLE = {
    "BSD": {"kev": [2, 3, 4, 5, 6, 7],
            "michelson": [0.277, 0.374, 0.376, 0.272, 0.302, 0.273],
            "cnr": [0.144, 0.209, 0.208, 0.211, 0.199, 0.193]},
    "In-Lens SE": {"kev": [1, 1.5, 2, 3, 4, 5],
                   "michelson": [0.156, 0.231, 0.246, 0.211, 0.180, 0.168],
                   "cnr": [0.145, 0.202, 0.219, 0.195, 0.161, 0.141]},
}
PANELS = {
    "g": dict(bb=(83.8, 543.8, 166.4, 626.3), key="michelson", ylab="Michelson contrast"),
    "h": dict(bb=(216.0, 542.7, 300.3, 626.3), key="cnr", ylab="CNR"),
}

for panel, P in PANELS.items():
    im = Img(10, P["bb"])
    k = im.g < 128
    H, W = k.shape
    from digitize_common import frame_lines
    XAX = frame_lines(k, 1, 0.6)[-1]
    YAX = frame_lines(k, 0, 0.6)[0]
    xt = tick_positions(k, XAX, +1, 4, YAX[1] + 1, W)
    yt = tick_positions_v(k, YAX, -1, 4, 0, XAX[0])
    labs = im.labels((P["bb"][0] - 25, P["bb"][1] - 5, P["bb"][2] + 5, P["bb"][3] + 12))
    fx, rx, sx, xp, xv = calib(xt, [l for l in labs if l[2] > XAX[1]], 1)
    fy, ry, sy, yp, yv = calib(yt, [l for l in labs if l[1] < 0], 2)
    # inverse maps value -> pixel
    x0, x1 = float(fx(0)), float(fx(1))
    y0, y1 = float(fy(0)), float(fy(1))
    px = lambda v: (v - x0) / (x1 - x0)  # noqa: E731
    py = lambda v: (v - y0) / (y1 - y0)  # noqa: E731
    filled = opened(k, 4)
    rows, pts, offs = [], [], []
    for det, T in TABLE.items():
        for kev, val in zip(T["kev"], T[P["key"]]):
            cx, cy = px(kev), py(val)
            if det == "BSD":
                cand = [b for b in blobs(filled, 40) if abs(b[0] - cx) < 15 and abs(b[1] - cy) < 15]
                mx, my = (cand[0][0], cand[0][1]) if cand else (np.nan, np.nan)
            else:
                x_lo, y_lo = int(cx) - 16, int(cy) - 16
                win = (255 - im.g[y_lo:y_lo + 33, x_lo:x_lo + 33]).astype(np.uint8)
                c = cv2.HoughCircles(win, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=8, minRadius=5, maxRadius=10)
                if c is None:
                    mx = my = np.nan
                else:
                    best = min(c[0], key=lambda q: (q[0] - 16) ** 2 + (q[1] - 16) ** 2)
                    mx, my = x_lo + best[0], y_lo + best[1]
            dx = float(fx(mx)) - kev if mx == mx else np.nan
            dy = float(fy(my)) - val if my == my else np.nan
            offs.append((det, kev, dx, dy))
            rows.append((det, kev, val, float(fy(my)) if my == my else np.nan))
            pts += [(cx, cy)]
    overlay(im.a, pts, os.path.join(WORK, f"fig6{panel}_overlay.png"), colour=(255, 0, 255))
    maxdy = max(abs(o[3]) for o in offs if o[3] == o[3])
    maxdx = max(abs(o[2]) for o in offs if o[2] == o[2])
    nmiss = sum(1 for o in offs if o[3] != o[3])
    write_csv(os.path.join(HERE, f"fig6{panel}.csv"), [
        f"Kubota et al. 2018 Nat Commun 9:437, Fig. 6{panel}: {P['ylab']} vs acceleration voltage (main PDF p. 10);",
        "  BSD = filled circles + solid line, In-Lens SE = open circles + dashed line (labels in the panel: 'BSD', 'In-Lens SE').",
        "Columns: detector; acceleration_voltage_kev (x axis 'Acceleration voltage (keV)'); "
        f"{P['key']} = the value (tier 1);",
        f"  {P['key']}_marker_digitized = the centre of the plotted marker in the published raster, for comparison.",
        "Provenance: tier 1, source data = Supplementary Table 3 'Michelson contrast and Contrast-to-noise ratio'",
        "  (Supplementary Information, 41467_2017_2768_MOESM1_ESM.pdf p. 25; the table is an image there, values read off it).",
        "  The table heads the BSD rows 'Detector: BSE' and the others 'In-Lens SE'; the figure labels them 'BSD' and 'In-Lens SE'.",
        "Check (fig6gh_extract.py): each table value was mapped into the embedded 300 ppi plot image through the tick",
        f"  calibration (x: {len(xp)} labelled ticks, max residual {rx:.3f} keV; y: {len(yp)} labelled ticks, max residual {ry:.4f})",
        "  and the marker centre located next to it (filled: opening + connected components; open: Hough circle).",
        f"  Largest offset table vs plotted marker: {maxdx:.3f} keV in x, {maxdy:.4f} in y "
        f"(1 px = {abs(sy):.4f}); {nmiss} marker(s) not located.",
    ], ["detector", "acceleration_voltage_kev", P["key"], P["key"] + "_marker_digitized"], rows,
        fmt=["{}", "{:g}", "{:.3f}", "{:.4f}"])
    print(panel, "x", xp, xv, rx, "y", yp, yv, ry)
    for o in offs:
        print("  ", o)
