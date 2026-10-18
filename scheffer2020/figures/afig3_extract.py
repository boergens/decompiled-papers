"""Appendix 1-figure 3 (p. 75): synful+ vs cascade connection strength, a scatter/density plot coloured by
'neuron pair frequency' (log colour bar, plasma map, 1 to ~9e5). Digitized from the embedded raster (693 x 564 px JPEG).

Tier 3 (semi-quantitative colour map). Appendix 1-figure 3-source data 1 is not available locally.
Calibration: x = cascade synapse count, gridlines 100..400 at columns 165, 268, 371, 473 and frame 0/500 at 63/576;
y = synful+ synapse count, gridlines 100..400 at rows 416, 314, 211, 109, frame 0/500 at 519/6 (positions found by code
in this script and asserted). Colour bar rows 7..518 (columns 612..630), log ticks 1e0..1e5 at rows 519, 433, 346, 260,
174, 88 (86.2 px per decade).
Every plot pixel whose colour lies within a distance of 40 (max RGB difference) of the colour bar is mapped to the
nearest bar colour -> log10 frequency. One source pixel is about 0.98 synapse counts on both axes, and the markers
(about 3 px across) are larger than one count, so the map is a picture of the marker cloud, not a per-count histogram:
neighbouring counts share colours. Pixels hidden by gridlines or with JPEG/anti-aliasing colours far from the bar
(marker edges on white) are omitted.
Writes figures/afig3.csv.gz (x, y, log10 frequency, frequency per coloured pixel) and work/afig3_overlay.png.
"""
import gzip
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import fc_dig as fd  # noqa: E402

a = fd.embedded(75)
g = a.astype(int)
mx, mn = g.max(axis=2), g.min(axis=2)
grey = (mx - mn < 20) & (mx > 140) & (mx < 225)
gc = [float(np.mean(r)) for r in fd.runs(list(np.where(grey[20:500].mean(axis=0) > 0.3)[0]))]
gr = [float(np.mean(r)) for r in fd.runs(list(np.where(grey[:, 70:560].mean(axis=1) > 0.3)[0]))]
assert np.allclose(gc, [165, 268, 371, 473], atol=1) and np.allclose(gr, [109, 211, 314, 416], atol=1), (gc, gr)
fx, rx = fd.fit([63] + gc + [576], [0, 100, 200, 300, 400, 500])
fy, ry = fd.fit([519] + gr[::-1] + [6], [0, 100, 200, 300, 400, 500])
fc, rc = fd.fit([519, 433, 346, 260, 174, 88], [0, 1, 2, 3, 4, 5])          # colour-bar row -> log10 frequency

bar_rows = np.arange(7, 519)
bar = g[7:519, 612:631].mean(axis=1)                                        # mean colour per bar row
bar_lv = fc(bar_rows + 0.0)
X0, Y0, X1, Y1 = 64, 7, 576, 519
sub = g[Y0:Y1, X0:X1].reshape(-1, 3)
d = np.abs(sub[:, None, :] - bar[None, :, :]).max(axis=2)                  # distance to every bar colour
best = d.argmin(axis=1)
ok = d[np.arange(len(best)), best] <= 40
ys, xs = np.divmod(np.arange(len(best)), X1 - X0)
rows = []
for i in np.where(ok)[0]:
    lv = float(bar_lv[best[i]])
    rows.append((round(float(fx(X0 + xs[i])), 2), round(float(fy(Y0 + ys[i])), 2), round(lv, 3), round(10 ** lv, 1)))
out = HERE / "afig3.csv.gz"
with gzip.open(out, "wt", newline="") as f:
    for h in ["Appendix 1-figure 3 of Scheffer et al. 2020 (eLife 9:e57443), p. 75: comparison of synful+ connection strength vs cascade",
              "connection strength (truncated at 500), points coloured by 'neuron pair frequency' (log colour bar, 1e0 to ~9e5).",
              "Provenance: tier 3, semi-quantitative: every coloured pixel of the embedded 693 x 564 px JPEG mapped through the colour bar.",
              "The authors' Appendix 1-figure 3-source data 1 was not available locally.",
              f"Calibration: axes on gridlines and frame (max residual x {rx:.2f}, y {ry:.2f} counts); colour bar on its 6 log ticks (max residual {rc:.3f} decades).",
              "x = cascade synapse count, y = synful+ synapse count at the pixel centre (one pixel ~0.98 count); markers are ~3 px across, so",
              "neighbouring counts share a colour and this is a picture of the marker cloud, not a histogram. Pixels hidden by gridlines or with",
              "colours far from the colour bar (anti-aliased marker edges on white, JPEG artefacts) are omitted.",
              "log10_freq = log10 of the colour-bar value of the nearest bar colour (uncertainty ~0.1-0.3 decade from JPEG colour noise); freq = 10^log10_freq.",
              "Columns: x, y, log10_freq, freq."]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["x", "y", "log10_freq", "freq"])
    w.writerows(rows)
lv = np.array([r[2] for r in rows])
print(len(rows), "pixels; log10 freq range", lv.min(), lv.max(), "rx", rx, "ry", ry, "rc", rc)
# overlay: recoloured map (pixels kept) in grey over the source
ovl = a.copy()
for i in np.where(ok)[0]:
    ovl[Y0 + ys[i], X0 + xs[i]] = (0, 255, 0) if bar_lv[best[i]] > 2 else ovl[Y0 + ys[i], X0 + xs[i]]
from PIL import Image
Image.fromarray(ovl).save(HERE.parent / "work" / "afig3_overlay.png")
