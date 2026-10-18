"""Fig. 17 (a-d): digitize the grouped bar charts (Fx, Fy, Fz vs sliding velocity) with error bars.

Tier 3 (digitized) from the embedded 300 ppi JPEG (page 20, xref 271), read straight from the PDF.
Per panel: y axis calibrated on the 9 major ticks (6 ... -10 nN, step 2) found on the left axis line
(linear least-squares fit, residual reported). Bars: colour masks (blue Fx, red Fy, magenta Fz);
bar end = zero-line centre +/- the summed colour fraction of the bar's pixel columns (sub-pixel),
rows hidden under the 3 px zero line counted as bar. Error bars: the dark (max channel < 190)
vertical line at the bar centre; ends = extremes of the contiguous run (gaps <= 2 px) through the bar
end, limited to the axis range; ends within 3 px of the axis limits (6 or -10 nN) are flagged clipped.
Writes figures/fig17.csv, work/fig17_overlay.png.
"""
import csv
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import digitize_common as dc  # noqa: E402

PDF = ROOT / "source" / "wei2024.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)

a = dc.embedded_image(str(PDF), 20, bbox_near=(71, 59, 524, 411)).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
colourness = {
    "Fx": np.clip((B - np.maximum(R, G)) / 255.0, 0, 1),
    "Fy": np.clip((R - np.maximum(G, B)) / 255.0, 0, 1),
    "Fz": np.clip((np.minimum(R, B) - G) / 255.0, 0, 1),
}
line = a.max(axis=2) < 190          # error-bar / axis ink (grey, dark)
dark = a.mean(axis=2) < 128

# panel: (letter, h_c label, axis column search range, row range of the plot, x range)
PANELS = [("a", 5, (80, 100), (0, 640), (95, 940)),
          ("b", 10, (1050, 1070), (0, 640), (1068, 1887)),
          ("c", 15, (80, 100), (760, 1400), (95, 940)),
          ("d", 20, (1050, 1070), (760, 1400), (1068, 1887))]
VEL = [0.1, 0.5, 1.0, 1.5, 2.0]
TICKS = [6, 4, 2, 0, -2, -4, -6, -8, -10]


def axis_ticks(cx, rows):
    y0, y1 = rows
    cols = [c for c in range(cx[0], cx[1]) if dark[y0:y1, c].sum() > 400]
    xr = max(cols) + 1
    runs = []
    for y in range(y0, y1):
        n = 0
        while dark[y, xr + n]:
            n += 1
        runs.append(n)
    runs = np.array(runs)
    major = (runs >= 9) & (runs < 40)        # major ticks are ~11 px, minor ~5 px; zero line is long
    zero = runs > 400
    lab, n = ndi.label(major | zero)
    centres = ndi.center_of_mass(np.ones_like(runs), lab, range(1, n + 1))
    centres = [y0 + c[0] for c in centres]
    return xr, centres


ink = 1.0 - a.min(axis=2) / 255.0    # 0 white, 1 for saturated bar colours and black


def bar_edge(cols, zr, direction):
    """Median over columns of the bar's outer edge (pixel-centre row coordinates): walk from the zero
    line (row round(zr)) outward while ink >= 0.5, then add the ink fraction of the first lighter pixel
    (sub-pixel edge). direction -1 = upward (positive bar), +1 = downward."""
    edges = []
    r0 = int(round(zr))
    for c in cols:
        r = r0
        while 0 < r < ink.shape[0] - 1 and ink[r + direction, c] >= 0.5:
            r += direction
        p = ink[r + direction, c]
        edges.append(r + direction * (0.5 + p))
    return float(np.median(edges))


rows_out = []
overlay_pts = []
summary = []
for letter, hc, cx, rows, xr_ in PANELS:
    xaxis, centres = axis_ticks(cx, rows)
    assert len(centres) == 9, (letter, centres)
    f, res, slope = dc.fit_axis(np.array(centres), np.array(TICKS, float))
    # pixel row of value 0 and of axis limits
    p = np.polyfit(np.array(TICKS, float), np.array(centres), 1)
    rowof = lambda v: np.polyval(p, v)
    zr = rowof(0.0)
    top_lim, bot_lim = rowof(6.0), rowof(-10.0)
    summary.append((letter, res, 1 / abs(p[0])))
    # bar detection: components of each colour touching the zero line, width >= 8, not legend
    for comp in ("Fx", "Fy", "Fz"):
        m = colourness[comp] > 0.5
        m[:, : xr_[0]] = False
        m[:, xr_[1]:] = False
        m[: rows[0]] = False
        m[rows[1]:] = False
        cols = np.where(m[int(zr) - 6:int(zr) + 7].any(axis=0))[0]
        # group columns into bars (merge gaps <= 4 px: the error line splits a bar)
        groups = []
        for c in cols:
            if groups and c - groups[-1][-1] <= 4:
                groups[-1].append(c)
            else:
                groups.append([c])
        groups = [g for g in groups if 15 <= g[-1] - g[0] + 1 <= 45]
        found = {}
        for g in groups:
            x0, x1 = g[0], g[-1]
            k = int(round((x0 - xr_[0] - 42 - ("Fx", "Fy", "Fz").index(comp) * 32) / 157.6))
            found[k] = (x0, x1)
        # tiny bars hidden in the zero line: look slightly wider
        for k in range(5):
            if k in found:
                continue
            ref = [found[j][0] - j * 157.6 for j in found]
            xs = int(round(np.median(ref) + k * 157.6))
            found[k] = (xs, xs + 28)
        for k, (x0, x1) in sorted(found.items()):
            xc = (x0 + x1) / 2
            # error-line column: most line pixels near the centre (exclude zero-line rows)
            band = line[int(top_lim) - 3:int(bot_lim) + 4].copy()
            zr_i = int(round(zr)) - (int(top_lim) - 3)
            band[zr_i - 3:zr_i + 4] = False
            cand = range(int(xc) - 5, int(xc) + 6)
            ec = max(cand, key=lambda c: band[:, c].sum())
            # bar end: ink run from the zero line, in bar columns clear of the error line and its caps;
            # the side is taken from where the bar colour is
            bcols = [c for c in range(x0 + 2, x1 - 1) if abs(c - ec) >= 10]
            col_c = colourness[comp][:, x0 + 2:x1 - 1]
            r0 = int(round(zr))
            up_c = col_c[r0 - 6:r0 - 1].mean()
            dn_c = col_c[r0 + 2:r0 + 7].mean()
            sign = 1 if up_c >= dn_c else -1
            end_row = bar_edge(bcols, zr, -sign)
            if abs(end_row - zr) < 2.5:
                flag = "bar end hidden in the zero line (|value| < ~0.07 nN); "
            else:
                flag = ""
            value = float(f(end_row))
            # error-bar run along column ec (allow +-1 column)
            lc = line[:, ec - 1:ec + 2].any(axis=1)
            lo_lim, hi_lim = int(top_lim) - 3, int(bot_lim) + 3
            start = int(round(end_row))
            # find a line pixel near the bar end
            seeds = [y for y in range(start - 6, start + 7) if lo_lim <= y <= hi_lim and lc[y]]
            if not seeds:
                e_top = e_bot = np.nan
                flag += "no error bar found"
            else:
                y = seeds[len(seeds) // 2]
                t = y
                gap = 0
                while t - 1 >= lo_lim and gap <= 2:
                    t -= 1
                    gap = 0 if lc[t] else gap + 1
                t += gap
                b = y
                gap = 0
                while b + 1 <= hi_lim and gap <= 2:
                    b += 1
                    gap = 0 if lc[b] else gap + 1
                b -= gap
                e_top, e_bot = float(f(t)), float(f(b))
                if t - top_lim < 3:
                    flag += "upper error-bar end at the axis limit (clipped); "
                if bot_lim - b < 3:
                    flag += "lower error-bar end at the axis limit (clipped); "
                overlay_pts += [(ec, t), (ec, b)]
            overlay_pts += [(x, end_row) for x in range(x0, x1 + 1, 3)]
            rows_out.append([letter, hc, comp, VEL[k], round(value, 3), round(e_bot, 3), round(e_top, 3),
                             round((e_top - e_bot) / 2, 3), round((e_top + e_bot) / 2, 3), flag.strip("; ")])

hdr = [
    "# Wei et al. 2024 (Acta Geotech. 20:1599-1620), Fig. 17 a-d: average forces along three directions vs sliding velocity",
    "# at h_c = 5, 10, 15, 20 Angstrom (averaged over sliding distance 15-30 Angstrom, per caption).",
    "# Columns: panel; hc_A = indentation depth h_c (Angstrom); component Fx/Fy/Fz; velocity_A_per_ps = sliding velocity",
    "#   (category position, printed label); force_nN = bar value (nN, from the zero line); err_low_nN/err_high_nN = lower/upper",
    "#   error-bar ends (nN); err_half_nN = half length of the error bar; err_mid_nN = its midpoint (should equal force_nN if",
    "#   the bar is symmetric); flag = notes (clipped error bars at the axis limits 6 / -10 nN, tiny bars).",
    "# Provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF page 20, xref 271) by figures/fig17_extract.py:",
    "#   y axis fitted linearly on the 9 major ticks (6 to -10 nN); bar ends from the colour fraction of the bar columns",
    "#   (sub-pixel); error-bar ends = extremes of the dark vertical line at the bar centre.",
    "# Calibration (residual = max tick residual in nN; scale in nN per pixel): "
    + "; ".join(f"({l}) {r:.3f}, {s:.4f}" for l, r, s in summary),
    "# Uncertainty: bar values about +-0.03 nN (1 px); error-bar ends about +-0.05 nN (line ends, caps 2-3 px thick).",
    "# The paper does not say what the error bars are (presumably the scatter of the force along 15-30 Angstrom).",
]
out = HERE / "fig17.csv"
with open(out, "w", newline="") as fh:
    for h in hdr:
        fh.write(h + "\n")
    w = csv.writer(fh)
    w.writerow(["panel", "hc_A", "component", "velocity_A_per_ps", "force_nN", "err_low_nN", "err_high_nN",
                "err_half_nN", "err_mid_nN", "flag"])
    w.writerows(rows_out)
dc.overlay(a.astype(np.uint8), overlay_pts, str(WORK / "fig17_overlay.png"), colour=(0, 200, 0))
print(out, len(rows_out), summary)
