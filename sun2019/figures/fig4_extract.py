"""Fig. 4 of Sun & Gamstedt 2019 (PDF p. 3): AFM height maps of the cut surfaces, t_u = 60 nm (a) and 140 nm (b),
converted to heights through the colour bar printed in panel (a) -> fig4a.csv, fig4b.csv.

Source: the embedded 300 ppi JPEG of Fig. 4 (1500 x 555 px): panel (a) = columns 0-749, panel (b) = columns
751-1499 (white separator at column 750). Run: python3 -I -B figures/fig4_extract.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from afm_map import embedded, bar_lut, to_height, white_mask, write_grid  # noqa: E402

PDF = str(HERE.parent / "source" / "sun2019.pdf")
img = embedded(PDF, 3, (184, 582, 544, 716))
# colour bar (panel a): frame-line centres at rows 195.5 (top, labelled 25.0 nm) and 431.5 (bottom, -25.0 nm),
# sampled over columns 72-95 (inside the bar's left/right frame lines at about 69 and 99)
TOP, BOT = 195.5, 431.5
lut_rgb, lut_val = bar_lut(img, (72, 96), TOP, BOT, 25.0, -25.0)
dark = lut_val[(lut_rgb.max(1) < 12)]
light = lut_val[(lut_rgb.min(1) > 243)]
clip_lo = float(dark.max()) if len(dark) else None
clip_hi = float(light.min()) if len(light) else None
# scale bar of panel (a): white line, longest run in rows 525-552, columns 560-748
sb = img[525:552, 560:748].min(2) > 230
r = int(np.argmax(sb.sum(1)))
cols = np.where(sb[r])[0]
bar_px = int(cols.max() - cols.min() + 1)

PANELS = {
    "a": (0, 750, [(10, 25, 185, 68), (18, 155, 150, 475), (10, 490, 100, 552), (565, 485, 745, 555), (746, 0, 750, 555)],
          [(500, 60, 690, 190)], "t_u = 60 nm"),
    "b": (751, 1500, [(0, 0, 3, 555), (19, 25, 211, 68), (169, 195, 459, 242), (29, 490, 104, 550)],
          [(527, 18, 714, 138), (254, 245, 389, 380)], "t_u = 140 nm"),
}
for p, (c0, c1, full, white, what) in PANELS.items():
    sub = img[:, c0:c1]
    mask = white_mask(sub, full, white)
    z = to_height(sub, lut_rgb, lut_val, mask)
    n_ok = int(np.isfinite(z).sum())
    lo = int(np.sum(z <= clip_lo + 1e-9)) if clip_lo is not None else 0
    hi = int(np.sum(z >= clip_hi - 1e-9)) if clip_hi is not None else 0
    scale = (f"Scale: the scale bar in panel (a) ('400 nm') is {bar_px} px long, i.e. {400 / bar_px:.3f} nm per pixel."
             if p == "a" else
             "Scale: panel (b) has no scale bar of its own; the bar in panel (a) is " +
             f"{bar_px} px = 400 nm ({400 / bar_px:.3f} nm/px), but the paper does not say that (b) has the same scale.")
    hdr = [
        f"Sun & Gamstedt 2019, Nanomanuf Metrol 2:45-55, Fig. 4({p}): AFM image of the cut surface created at {what}",
        "  (arrow in the panel: cutting direction). Height map converted from the printed colours.",
        "Format: one CSV row per pixel row of the panel (row 0 = top); columns c0..cN = pixel columns (c0 = left);",
        "  values = height in nm on the colour bar's scale (-25.0 nm black ... 25.0 nm white). Empty = annotation",
        "  (labels, arrows, scale bar, colour-bar box, the 3-4 px next to the white panel separator; masked) or a colour",
        "  not on the bar.",
        scale,
        f"Panel (a) is columns 0-749, panel (b) columns 751-1499 of the embedded image (1500 x 555 px, JPEG, PDF p. 3).",
        "Provenance: tier 3, digitized: colour bar of panel (a) sampled down its centre between its frame lines",
        f"  (rows {TOP}-{BOT} = 25.0 to -25.0 nm, linear), each pixel mapped to the bar height of the nearest bar",
        "  colour(s) (tools/afm_map.py).",
        f"Uncertainty: the bar resolves about {50 / (BOT - TOP):.2f} nm per bar row, but JPEG compression changes",
        "  colours by several units, so single pixels are uncertain by roughly +-1 nm (more in dark areas); use",
        "  local averages. The original AFM data were resampled for printing (the true scan resolution is unknown).",
        f"Clipping: the bar is pure black below about {clip_lo:.1f} nm and near-white above about {clip_hi:.1f} nm;"
        if clip_lo is not None and clip_hi is not None else "Clipping: none detected.",
        f"  such pixels get the middle of that bar range. This panel: {lo} pixels at the dark limit, {hi} at the light",
        f"  limit, {n_ok} pixels with a value.",
        "Odd: the straight light-yellow diagonal line crossing the panel is part of the printed image (topography,",
        "  not masked).",
    ]
    write_grid(str(HERE / f"fig4{p}.csv"), hdr, z, 1)
    print(p, "valid", n_ok, "of", z.size, "range", np.nanmin(z), np.nanmax(z), "median", np.nanmedian(z),
          "clip", clip_lo, clip_hi, lo, hi, "bar px", bar_px)
