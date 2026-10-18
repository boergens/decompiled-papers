"""Fig. 7 of Sun & Gamstedt 2019 (PDF p. 5): AFM height maps of the cut surfaces, v0 = 0.5 mm/s (a) and 3.0 mm/s
(b), converted to heights through the colour bar printed at the left -> fig7a.csv, fig7b.csv.

Source: the embedded 300 ppi JPEG of Fig. 7 (1500 x 606 px): colour bar at columns ~65-115, panel (a) = columns
221-846, panel (b) = columns 874-1499. Run: python3 -I -B figures/fig7_extract.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from afm_map import embedded, bar_lut, to_height, white_mask, write_grid  # noqa: E402

PDF = str(HERE.parent / "source" / "sun2019.pdf")
img = embedded(PDF, 5, (184, 570, 544, 716))
# colour bar: frame-line centres at rows 103.5 (top, labelled 3.0 nm) and 511 (bottom, -3.0 nm; the bottom frame
# merges with the black end of the bar), sampled over columns 72-108
TOP, BOT = 103.5, 511.0
lut_rgb, lut_val = bar_lut(img, (72, 109), TOP, BOT, 3.0, -3.0)
dark = lut_val[(lut_rgb.max(1) < 12)]
light = lut_val[(lut_rgb.min(1) > 243)]
clip_lo = float(dark.max())
clip_hi = float(light.min())

PANELS = {   # (first col, end col, label boxes masked whole, arrow boxes masked where near-white), panel coordinates
    "a": (221, 847, [(0, 0, 4, 606), (621, 0, 626, 606), (7, 12, 344, 68), (454, 515, 626, 606)], [(4, 395, 234, 485)], "v0 = 0.5 mm/s"),
    "b": (874, 1500, [(0, 0, 4, 606), (622, 0, 626, 606), (6, 12, 344, 68), (451, 515, 626, 606)], [(4, 420, 211, 460)], "v0 = 3.0 mm/s"),
}
for p, (c0, c1, full, white, what) in PANELS.items():
    sub = img[:, c0:c1]
    # scale bar: white line in the panel's bottom-right box, longest horizontal run of white pixels
    sb = sub[560:600, 440:626].min(2) > 230
    best = 0
    for row in sb:
        idx = np.where(row)[0]
        if len(idx):
            runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
            best = max(best, max(len(q) for q in runs))
    mask = white_mask(sub, full, white)
    z = to_height(sub, lut_rgb, lut_val, mask)
    n_ok = int(np.isfinite(z).sum())
    lo = int(np.sum(z <= clip_lo + 1e-9))
    hi = int(np.sum(z >= clip_hi - 1e-9))
    hdr = [
        f"Sun & Gamstedt 2019, Nanomanuf Metrol 2:45-55, Fig. 7({p}): AFM image of the cut surface created at {what}",
        "  (t_u = 85 nm per Sect. 3.2.1; arrow in the panel: cutting direction). Height map converted from the printed colours.",
        "Format: one CSV row per pixel row of the panel (row 0 = top); columns c0..cN = pixel columns (c0 = left);",
        "  values = height in nm on the colour bar's scale (-3.0 nm black ... 3.0 nm white). Empty = annotation",
        "  (label, arrow, scale bar, the 4-5 px at the panel's left and right edges; masked) or a colour not on the bar.",
        f"Scale: the panel's scale bar ('400 nm') is {best} px long, i.e. {400 / best:.3f} nm per pixel.",
        f"Panel ({p}) is columns {c0}-{c1 - 1} of the embedded image (1500 x 606 px, JPEG, PDF p. 5).",
        "Provenance: tier 3, digitized: the colour bar sampled down its centre between its frame lines",
        f"  (rows {TOP}-{BOT} = 3.0 to -3.0 nm, linear), each pixel mapped to the bar height of the nearest bar",
        "  colour(s) (tools/afm_map.py).",
        f"Uncertainty: the bar resolves about {6 / (BOT - TOP):.3f} nm per bar row, but JPEG compression changes",
        "  colours by several units, so single pixels are uncertain by roughly +-0.1 nm (more in dark areas); use",
        "  local averages. The original AFM data were resampled for printing (the true scan resolution is unknown).",
        f"Clipping: the bar is pure black below about {clip_lo:.2f} nm and near-white above about {clip_hi:.2f} nm;",
        f"  such pixels get the middle of that bar range. This panel: {lo} pixels at the dark limit, {hi} at the light",
        f"  limit, {n_ok} pixels with a value.",
    ]
    write_grid(str(HERE / f"fig7{p}.csv"), hdr, z, 2)
    print(p, "valid", n_ok, "of", z.size, "range", np.nanmin(z), np.nanmax(z), "median", np.nanmedian(z),
          "clip", clip_lo, clip_hi, lo, hi, "bar px", best)
