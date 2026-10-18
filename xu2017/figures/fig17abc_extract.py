"""Digitize Figure 17(a), (b), (c) of Xu et al. 2017 (PDF p. 28): Monte Carlo scattering locations coloured by energy.

Source: the embedded raster image of Figure 17 (2880 x 2160 px JPEG, ~403 ppi). Each panel shows dots on black,
coloured by electron energy through the colour bar at the right of (b) ('1.2 KeV' red at the top ... '0 eV' black at
the bottom). The output is one row per coloured pixel at native resolution (gzipped CSV):
    python3 -I -B figures/fig17abc_extract.py  -> figures/fig17a.csv.gz, fig17b.csv.gz, fig17c.csv.gz
                                                 (+ work/fig17abc_energy.png, a false-colour check image)
"""
import csv
import gzip
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from xu_helpers import load, work_path  # noqa: E402

a = load(28).astype(int)

# Colour bar: inside the white frame at cols 2796-2862, rows 82-911 (frame rows 77-81 and 912-914). Its top is labelled
# '1.2 KeV', its bottom '0 eV'; assumed linear in between (no other labels).
BAR_TOP, BAR_BOT = 82, 911
bar = a[BAR_TOP:BAR_BOT + 1, 2815:2845].mean(1)                    # mean colour of each bar row
bar_e = 1200.0 * (BAR_BOT - np.arange(BAR_TOP, BAR_BOT + 1)) / (BAR_BOT - BAR_TOP)   # eV


def energy(cols):
    """Map colours (N x 3) to energy via the bar rows within 6 colour units of the best match; returns mean and spread."""
    if len(cols) > 4000:
        parts = [energy(cols[i:i + 4000]) for i in range(0, len(cols), 4000)]
        return tuple(np.concatenate([q[k] for q in parts]) for k in range(4))
    d = np.sqrt(((cols[:, None, :] - bar[None, :, :]) ** 2).sum(2))
    best = d.min(1)
    ok = d <= best[:, None] + 6
    cnt = ok.sum(1)
    e = (ok * bar_e).sum(1) / cnt
    lo = np.where(ok, bar_e, np.inf).min(1)
    hi = np.where(ok, bar_e, -np.inf).max(1)
    return e, lo, hi, best


# Grid lines (thin white lines, every 5 nm): rows 134.5, 338.5, 536.5, 734.5, 941.5, 1142.5; columns of (a)/(c):
# 165.5, 369.5, 579.5, 789.5, 993.5 = -10, -5, 0, 5, 10 nm; of (b): 1149.5 ... 2601.5 = -15 ... 20 nm (labels -10, 0 nm,
# 10, 20 and the 'Os 0' arrow at 0). Depth: (a) and (b) start at row 134.5 (0) going down; (c) at row 734.5 (0).
# The grid is not perfectly even (198-210 px per 5 nm), so the maps are piecewise linear through the grid lines.
COLS_AC = ([165.5, 369.5, 579.5, 789.5, 993.5], [-10, -5, 0, 5, 10])
COLS_B = ([1149.5, 1353.5, 1563.5, 1773.5, 1977.5, 2181.5, 2391.5, 2601.5], [-15, -10, -5, 0, 5, 10, 15, 20])
PANELS = {
    "a": dict(cols=(12, 1066), rows=(120, 580), x=COLS_AC, z=([134.5, 338.5, 536.5], [0, -5, -10]),
              title="Os 0, 0.8 KeV"),
    "c": dict(cols=(12, 1066), rows=(720, 1160), x=COLS_AC, z=([734.5, 941.5, 1142.5], [0, -5, -10]),
              title="Os 1, (0.8 KeV)"),
    "b": dict(cols=(1094, 2788), rows=(120, 1160), x=COLS_B,
              z=([134.5, 338.5, 536.5, 734.5, 941.5, 1142.5], [0, -5, -10, -15, -20, -25]), title="Os 0, 1.2 KeV"),
}
check = np.zeros_like(a)
for key, P in PANELS.items():
    c0, c1 = P["cols"]
    r0, r1 = P["rows"]
    sub = a[r0:r1, c0:c1]
    mx = sub.max(2)
    grey = np.ptp(sub, axis=2) < 40                       # white/grey grid lines, labels, arrows
    m = (mx >= 120) & ~grey
    ys, xs = np.nonzero(m)
    cols = sub[ys, xs].astype(float)
    e, lo, hi, dist = energy(cols)
    keep = dist < 60                                      # colour must be close to some bar colour
    X = np.interp(xs + c0, *P["x"], left=np.nan, right=np.nan)
    Z = np.interp(ys + r0, *P["z"], left=np.nan, right=np.nan)
    # extrapolate linearly beyond the outermost grid lines
    for arr, px, (gp, gv) in ((X, xs + c0, P["x"]), (Z, ys + r0, P["z"])):
        s0 = (gv[1] - gv[0]) / (gp[1] - gp[0])
        s1 = (gv[-1] - gv[-2]) / (gp[-1] - gp[-2])
        arr[px < gp[0]] = gv[0] + s0 * (px[px < gp[0]] - gp[0])
        arr[px > gp[-1]] = gv[-1] + s1 * (px[px > gp[-1]] - gp[-1])
    out = HERE / f"fig17{key}.csv.gz"
    with gzip.open(out, "wt", newline="") as f:
        for h in [
            f"Xu et al. 2017 eLife 6:e25916, Figure 17({key}) ('{P['title']}' as printed): Monte Carlo simulation of backscattered electrons;",
            "  each dot is coloured by energy through the colour bar of panel b (red '1.2 KeV' at the top, black '0 eV' at the bottom).",
            "One row per coloured pixel of the source image (native resolution), not per electron (dots are 2-4 px and overlap).",
            "Columns: x_nm = lateral position (axis labels '-10', '0 nm', '10', '20'); z_nm = depth below the sample surface (0 at the surface",
            "  line, negative downwards; labels '0', '-10'); energy_eV = energy read from the colour bar (mean of the bar rows whose colour",
            "  is within 6 units of the best match), read on the bar as printed in (b): 0 eV at the bottom, 1200 eV at the top;",
            "  energy_min_eV / energy_max_eV = range of those bar rows (wide where the bar is saturated, e.g. the red plateau covers",
            "  about 1110-1200 eV); colour_dist = distance of the pixel colour to the best bar colour.",
            "  bar_fraction = energy_eV / 1200 = position on the colour bar (0 bottom, 1 top)." + (
                "" if key == "b" else
                " CAUTION for this 0.8 keV panel: the only colour bar is printed in (b) and labelled '1.2 KeV';"
                " whether (a) and (c) use the same scale or one normalised to their own 0.8 keV landing energy (then energy ="
                " 800 x bar_fraction) is not stated. Dots near the beam axis are red in all three panels, which suggests a"
                " per-panel scale; energy_eV here assumes the printed 1.2 KeV scale."),
            "Provenance: tier 3, from the embedded JPEG (~403 ppi) by fig17abc_extract.py. x and z: piecewise linear through the white",
            "  grid lines every 5 nm (identified with the axis labels), extrapolated beyond the outermost lines. Colour bar assumed linear",
            "  between its two labels. Pixels whose brightest channel is below 120 are left out: the bar runs from purple into black below",
            "  ~250 eV, so the lowest-energy dots cannot be told from the black background and are missing. Grey/white pixels (grid,",
            "  labels, arrows) are left out. JPEG colour noise at dot edges adds scatter of roughly +-50 eV.",
            "Uncertainty: x, z about +-0.03 nm per pixel (~41 px per nm); energy see energy_min/max and the note above.",
        ]:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(["x_nm", "z_nm", "bar_fraction", "energy_eV", "energy_min_eV", "energy_max_eV", "colour_dist"])
        for i in np.nonzero(keep)[0]:
            w.writerow([f"{X[i]:.3f}", f"{Z[i]:.3f}", f"{e[i] / 1200:.3f}", f"{e[i]:.0f}", f"{lo[i]:.0f}", f"{hi[i]:.0f}", f"{dist[i]:.0f}"])
    # check image: energy as grey level at the pixel positions
    ck = np.zeros((r1 - r0, c1 - c0, 3))
    ck[ys[keep], xs[keep]] = (np.array(e[keep])[:, None] / 1200 * 255)
    check[r0:r1, c0:c1] = ck
    print(key, int(keep.sum()), "pixels; energy quartiles", np.percentile(e[keep], [25, 50, 75]).round(), "x range",
          np.nanmin(X).round(2), np.nanmax(X).round(2), "z range", np.nanmin(Z).round(2), np.nanmax(Z).round(2))
from PIL import Image  # noqa: E402
Image.fromarray(check.astype(np.uint8)).save(work_path("fig17abc_energy.png"))
