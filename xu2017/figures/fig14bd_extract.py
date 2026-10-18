"""Digitize Figure 14(b) and 14(d) of Xu et al. 2017 (PDF p. 25): detected / not-detected boundary in backscatter energy vs angle.

Source: the embedded raster image of Figure 14 (2880 x 1794 px, ~403 ppi); panels b and d at its right.
    python3 -I -B figures/fig14bd_extract.py  -> figures/fig14b.csv, figures/fig14d.csv (+ work/fig14bd_overlay.png)
Extracted: the yellow boundary line, and the three coloured reference lines with their dots (blue, green, red).
Not extracted: the ~10,000 simulated electrons drawn as black (detected) and grey (not detected) dots.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from digitize_common import write_csv, overlay  # noqa: E402
from xu_helpers import load, lin, blobs, work_path  # noqa: E402

a = load(25).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
# Frames (work/explore.py): b: cols 1494-1502 / 2842-2850, rows 39-47 / 750-758; d: cols 1488-1496 / 2836-2844, rows 948-956 / 1660-1668.
# The axis labels 0 and 90 (x) and 0 and 1200 (y) are centred on the frame lines; the intermediate labels (every 10 deg,
# every 200 eV) are evenly spaced between them (label centroids within 2 px of the linear map).
# Panel b, y: calibrated on the label centroids 0 (row 758) and 1200 (row 45.5), 118.75 px per 200 eV; with the frame
# centres (754 / 43) instead, the three reference lines came out 4-7 eV low (1096, 595, 43 eV), with the labels they come
# out at 1100, 600 and 50 eV. Panel d: frame centres (the reference lines come out at 1100, 601, 51 eV).
PANELS = {"b": dict(x=(1498, 2846), y=(758, 45.5), box=(1503, 48, 2842, 750)),
          "d": dict(x=(1492, 2840), y=(1664, 952), box=(1497, 957, 2836, 1660))}
YEL = (R > 200) & (G > 200) & (B < 90)
COLS = {"blue (1.1 keV)": (B - R > 100) & (B - G > 60), "green (600 eV)": (G - R > 100) & (G - B > 100),
        "red (50 eV)": (R - G > 120) & (R - B > 120)}
pts = []
for key, P in PANELS.items():
    fx = lin(P["x"][0], 0, P["x"][1], 90)
    fy = lin(P["y"][0], 0, P["y"][1], 1200)
    x0, y0, x1, y1 = P["box"]
    win = np.zeros(R.shape, bool)
    win[y0:y1, x0:x1] = True
    m = YEL & win
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    m = lab == (1 + int(np.argmax(sizes)))                    # the boundary line is one connected piece
    # centre points of the ~6 px wide line: row runs where the line is steep, column runs where it is flat
    cand = []
    for r in range(y0, y1):
        c = np.nonzero(m[r])[0]
        if len(c):
            for run in np.split(c, np.where(np.diff(c) > 1)[0] + 1):
                if len(run) <= 10:
                    cand.append((run.mean(), r))
    for c in range(x0, x1):
        rr = np.nonzero(m[:, c])[0]
        if len(rr):
            for run in np.split(rr, np.where(np.diff(rr) > 1)[0] + 1):
                if len(run) <= 10:
                    cand.append((c, run.mean()))
    cand = np.array(sorted(set((round(x, 1), round(y, 1)) for x, y in cand)))
    # order along the line: start at the topmost point and walk to the nearest unused point
    used = np.zeros(len(cand), bool)
    i = int(np.argmin(cand[:, 1]))
    order = [i]
    used[i] = True
    for _ in range(len(cand) - 1):
        dist = np.hypot(*(cand - cand[i]).T)
        dist[used] = np.inf
        j = int(np.argmin(dist))
        if dist[j] > 25:
            break
        order.append(j)
        used[j] = True
        i = j
    line = cand[order]
    # thin to one point per ~2 px of path
    keep, last = [], None
    for x, y in line:
        if last is None or np.hypot(x - last[0], y - last[1]) >= 2:
            keep.append((x, y))
            last = (x, y)
    # in b the yellow outline of the 'Not Detected' area also runs along the top and right frame lines: drop those parts
    keep = [(x, y) for x, y in keep if y > y0 + 8 and x < x1 - 8]
    rows = [("boundary", float(fx(x)), float(fy(y))) for x, y in keep]
    pts += keep
    # reference lines and dots
    checks = []
    for name, cm in COLS.items():
        cm = cm & win
        # the dots sit on a thin line of the same colour: an opening with a 9 x 9 disc removes the line
        yy, xx = np.mgrid[-4:5, -4:5]
        cm = ndimage.binary_opening(cm, structure=(xx ** 2 + yy ** 2) <= 16)
        dots = [b for b in blobs(cm, min_area=60) if b[2] < 1500]
        for x, y, area, _ in sorted(dots):
            rows.append((name + " dot", float(fx(x)), float(fy(y))))
            pts.append((x, y))
        if dots:
            checks.append(f"{name}: mean {np.mean([fy(d[1]) for d in dots]):.0f} eV, {len(dots)} dots")
    write_csv(str(HERE / f"fig14{key}.csv"), [
        f"Xu et al. 2017 eLife 6:e25916, Figure 14({key}): detection map in 'Backscatter Energy (eV)' vs 'Backscatter Angle (degrees)'"
        + (" (0 V sample bias)." if key == "b" else " (+600 V sample bias)."),
        "Columns: series, angle_deg, energy_eV. 'boundary' = the yellow line separating 'Detected' (left/below, black dots) from",
        "  'Not Detected' (pale yellow area), ordered along the line from its top end; one point per ~2 px of path. Points within",
        "  8 px of the top and right frame lines are left out (the yellow outline of the area also runs along the frame there).",
        "  '<colour> dot' = the coloured dots on the three horizontal reference lines (caption: 1.1 keV blue, 600 eV green, 50 eV red",
        "  electrons simulated in (a)/(c)); dots hidden behind others or the frame are missing.",
        "Not extracted: the ~10,000 simulated electrons (black and grey dots), which overlap too much to be separated.",
        "Provenance: tier 3, digitized from the embedded raster image (~403 ppi, no vector data in the PDF) by fig14bd_extract.py.",
        "  Axes: linear; x: frame lines = 0 and 90 deg; y: " + ("tick-label centroids 0 and 1200 eV" if key == "b" else "frame lines = 0 and 1200 eV") + " (see the script).",
        "  Check: " + "; ".join(checks) + ".",
        f"Uncertainty: +-{abs(fx(1) - fx(0)):.2f} deg and +-{abs(fy(1) - fy(0)):.1f} eV per pixel; the yellow line is ~6 px wide.",
    ], ["series", "angle_deg", "energy_eV"], rows, fmt=["{}", "{:.2f}", "{:.1f}"])
    print(key, len(keep), "boundary points;", checks)
overlay(a.astype(np.uint8), pts, work_path("fig14bd_overlay.png"))
