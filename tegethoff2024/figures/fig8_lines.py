"""Shared code for the force-profile panels of Figure 8 (B, D, F); called by fig8b/d/f_extract.py.

Each panel shows, per force (sectional = blue, transverse = red): a thick line (the mean, per the caption), a thin line
of the same colour above and below it (not explained in the caption), and grey traces underneath (individual cuts,
presumably; not explained either). Per pixel column this script records, for each colour: the centre of the thick
line, the thin lines above and below where they are separate from it, and the vertical extent of the whole band
(grey + colour) around that line.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403


def runs(idx, gap=1):
    out = []
    for i in idx:
        if out and i <= out[-1][1] + 1 + gap:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


def run(panel, box, yt, yv, xt, xv, title):
    a = img(11)
    fy, ry, sy = fit_axis(yt, yv)
    fx, rx, sx = fit_axis(xt, xv)
    x0, y0, x1, y1 = box
    lab = classify(a, [(30, 115, 200), (180, 30, 50)], max_dist=70, min_sat=45)
    grey = (sat(a) < 30) & (gray(a) > 120) & (gray(a) < 225)
    rows, pts = [], []
    for c in range(x0, x1):
        anyc = np.where((lab[y0:y1, c] >= 0) | grey[y0:y1, c])[0] + y0
        bands = runs(anyc, gap=30)
        for k, name in enumerate(["sectional (blue)", "transverse (red)"]):
            col = np.where(lab[y0:y1, c] == k)[0] + y0
            if len(col) == 0:
                continue
            rr = runs(col, gap=1)
            thick = max(rr, key=lambda r: r[1] - r[0])
            mid = (thick[0] + thick[1]) / 2
            above = [r for r in rr if thick[0] - 25 <= r[1] < thick[0] - 2]
            below = [r for r in rr if thick[1] + 2 < r[0] <= thick[1] + 25]
            up = (above[-1][0] + above[-1][1]) / 2 if above else float("nan")   # nearest run above
            lo = (below[0][0] + below[0][1]) / 2 if below else float("nan")     # nearest run below
            band = next((b for b in bands if b[0] <= mid <= b[1]), [thick[0], thick[1]])
            rows.append((name, float(fx(c)), float(fy(mid)), thick[1] - thick[0] + 1, float(fy(up)) if up == up else up,
                         float(fy(lo)) if lo == lo else lo, float(fy(band[0])), float(fy(band[1]))))
            pts.append((c, mid))
            if up == up:
                pts.append((c, up))
            if lo == lo:
                pts.append((c, lo))
    overlay(a, pts, os.path.join(WORK, f"fig8{panel}_overlay.png"))
    write_csv(os.path.join(HERE, f"fig8{panel}.csv"), [
        f"Tegethoff & Briggman 2024 Front Neurosci 18:1286991, {title}",
        "Columns: series = sectional (blue) or transverse (red) force; time_s = x; mean_mid = centre of the thick coloured",
        "  line (the mean, per the caption), mN/mm; thick_px = its thickness in px in this column (> ~6 px where the line is",
        "  steep or where the thin lines merge with it); thin_upper / thin_lower = centre of the thin line of the same",
        "  colour above / below the thick one, within 25 px (not explained in the caption; empty where it merges with the",
        "  thick line);",
        "  band_top / band_bottom = upper and lower edge of the whole drawn band (grey traces + coloured lines) around",
        "  the line in this column (gaps of up to 30 px = ~8 mN/mm between grey traces bridged), mN/mm. One row per pixel column and",
        "  series.",
        "Before and after the cut the blue and red bands merge near 0, so their band edges there are the same.",
        "Provenance: tier 3, digitized from the embedded ~337 ppi JPEG (no vector data in the PDF) by fig8"
        + panel + "_extract.py (fig8_lines.py);",
        f"  y calibrated on 6 ticks 20-120 mN/mm (max residual {ry:.3g}), x on {len(xt)} ticks (max residual {rx:.3g} s).",
        f"Uncertainty: +-{2 * abs(sy):.2g} mN/mm (2 px), +-{2 * abs(sx):.2g} s; band edges also depend on the grey threshold.",
    ], ["series", "time_s", "mean_mid", "thick_px", "thin_upper", "thin_lower", "band_top", "band_bottom"], rows)
    print(panel, len(rows), "rows; residuals", ry, rx)
