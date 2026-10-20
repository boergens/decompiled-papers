"""Digitize Figure 7 of Nikitin et al. 2024 (J. Synchrotron Rad. 31, 851-866; PDF p. 8): the Nvidia Nsight Systems
timeline screenshot of one batch of the 1D USFFT. The quantitative content is the time extent of each block on
the ruler (time axis: '71s' at the left, labelled major ticks +600 ms ... +660 ms): the GPU kernel boxes of
Stream 18, the 'Memcpy HtoD' (green) and 'Memcpy DtoH' (purple) transfer boxes of Streams 17 and 19, and the
memcpy bars of the 'CUDA HW' overview row. Source: the embedded 2205 x 648 px raster (no vector paths), tier 3
"digitized".  Run from anywhere:  python3 -I -B fig7_extract.py  -> fig7.csv next to this script, work/fig7_overlay.png
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for up in range(1, 6):
    cand = os.path.abspath(os.path.join(HERE, *([".."] * up), "tools"))
    if os.path.exists(os.path.join(cand, "digitize_common.py")):
        sys.path.insert(0, cand)
        break
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, write_csv  # noqa: E402

PDF = os.path.join(HERE, "..", "source", "nikitin2024.pdf")
a = embedded_image(PDF, 8, bbox_near=(106.4, 603.8, 503.3, 720.4)).astype(float)
g = a.mean(2)
H, W = g.shape
X0 = 370                                                   # the timeline starts right of the row-label column


def runs(row_mask, min_len=2, gap=0):
    """(start, end) pixel runs of a boolean row; holes up to `gap` pixels are bridged; runs at the left edge dropped."""
    idx = np.where(row_mask)[0]
    out = []
    for i in idx:
        if out and i - out[-1][1] <= gap + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [(s, e) for s, e in out if e - s + 1 >= min_len and s > X0 + 30]


# --- time axis: major tick marks on the ruler (row 34), every second one carries a label ---
ticks = [0.5 * (s + e) for s, e in runs(g[34, :] < 215, min_len=2, gap=1) if s > X0 + 40]
assert len(ticks) == 15, ticks
labelled = [c for c in ticks if (g[18:30, int(c) - 50:int(c) + 50] < 215).sum() > 40]
assert len(labelled) == 7, labelled
ft, res, m = fit_axis(labelled, [600, 610, 620, 630, 640, 650, 660])
unlabelled = [c for c in ticks if c not in labelled]
assert max(abs(ft(c) - round(ft(c) / 5) * 5) for c in unlabelled) < 0.3   # the unlabelled ticks fall on 5 ms

# --- colour masks of the block fills ---
COL = {"kernel": (112, 144, 208), "small": (158, 234, 243), "green": (104, 208, 168), "purple": (216, 136, 248)}
dist = {k: np.sqrt(((a - np.array(v)) ** 2).sum(2)) for k, v in COL.items()}

# Kernel boxes (Stream 18, rows ~349-382) sit edge to edge: their rounded corners leave a light notch (grey > 180,
# 3-6 px wide) in the top row of the boxes (350) where two boxes meet, while the fill is grey ~150 there. A column is
# inside a box when it has the fill colour in the first full-fill row (352, above the label text) and no notch in row 350.
kernel_in = (dist["kernel"][352, :] < 50) & (g[350, :] < 180)
small_in = (dist["small"][352, :] < 45) & (dist["small"][366, :] < 45)   # cyan over the whole height (the
# box gaps are light only in the top/bottom rows)
# The memcpy boxes of Streams 17 and 19 and the overview bars: fill colour in the strip above the label text.
green_s17 = dist["green"][392:397, :].mean(0) < 45
purple_s19 = dist["purple"][474:479, :].mean(0) < 45
green_ov = dist["green"][210:224, :].mean(0) < 45
purple_ov = dist["purple"][210:224, :].mean(0) < 45

# printed text inside the wide kernel boxes of each chunk group, left to right (groups are separated by the light-blue
# cyan chunk-start boxes; group 0 = the tail of the previous chunk: two narrow unlabelled boxes)
KERNEL_LABELS = {1: ["gather1d...", "...", "void regular_fft_factor<(...", "void regul...", "void prime_fft_...", "..."],
                 2: ["gather1d...", "ff...", "void regular_fft_factor<(...", "void regul...", "void prime_fft_...", "..."],
                 3: ["ga..."]}
KERNEL_ANNOT = {1: "GPU calculations chunk N", 2: "GPU calculations chunk N+1"}
HTOD_ANNOT = ["CPU->GPU copy chunk N+1", "CPU->GPU copy chunk N+2"]
DTOH_ANNOT = ["GPU->CPU copy chunk N-1", "GPU->CPU copy chunk N", ""]
DTOH_LABEL = ["Memcpy DtoH", "Memcpy DtoH", "Me..."]


def grouped(rr, max_gap=40):
    """Group runs separated by less than max_gap pixels (the sub-boxes of one memcpy block)."""
    gi, prev, out = -1, None, []
    for s, e in rr:
        if prev is None or s - prev > max_gap:
            gi += 1
        out.append(gi)
        prev = e
    return out


rows_out, boxes = [], []


def emit(series, rr, labels, annots, r0, r1):
    for (s, e), lab, ann in zip(rr, labels, annots):
        t0, t1 = float(ft(s - 0.5)), float(ft(e + 0.5))
        rows_out.append((series, lab, ann, t0, t1, t1 - t0, s, e))
        boxes.append((r0, r1, s, e))
    print(series, len(rr), "boxes")


rr = runs(green_ov, min_len=3)
emit("CUDA HW overview: Memcpy HtoD (green bar)", rr, [""] * len(rr), [""] * len(rr), 210, 224)
rr = runs(purple_ov, min_len=3)
emit("CUDA HW overview: Memcpy DtoH (purple bar)", rr, [""] * len(rr), [""] * len(rr), 210, 224)

small_runs = runs(small_in, min_len=6)
small_starts = [s for s, e in small_runs]
rr = runs(kernel_in, min_len=3)
groups = [sum(1 for x in small_starts if x < s) for s, e in rr]
labels, annots = [""] * len(rr), [""] * len(rr)
for gi in sorted(set(groups)):
    idx = [i for i, gg in enumerate(groups) if gg == gi and rr[i][1] - rr[i][0] >= 25]
    labs = KERNEL_LABELS.get(gi)
    if labs is not None:
        assert len(idx) == len(labs), (gi, [rr[i] for i in idx], labs)
        for i, lab in zip(idx, labs):
            labels[i] = lab
    for i, gg in enumerate(groups):
        if gg == gi:
            annots[i] = KERNEL_ANNOT.get(gi, "")
emit("Stream 18: GPU kernel box", rr, labels, annots, 350, 382)
emit("Stream 18: chunk-start box (cyan, unlabelled)", small_runs, [""] * len(small_runs), [""] * len(small_runs), 350, 382)

rr = runs(green_s17, min_len=3)
gg = grouped(rr)
assert max(gg) == 1, rr
emit("Stream 17: Memcpy HtoD", rr, ["Memcpy HtoD"] * len(rr), [HTOD_ANNOT[i] for i in gg], 390, 422)
rr = runs(purple_s19, min_len=3)
gg = grouped(rr)
assert max(gg) == 2, rr
emit("Stream 19: Memcpy DtoH", rr, [DTOH_LABEL[i] for i in gg], [DTOH_ANNOT[i] for i in gg], 472, 506)

# QA overlay: magenta outline on every detected box, red marks on the labelled ticks
from PIL import Image  # noqa: E402
ov = a.astype(np.uint8).copy()
for r0, r1, s, e in boxes:
    ov[r0 - 2:r1 + 3, s] = (255, 0, 255)
    ov[r0 - 2:r1 + 3, e] = (255, 0, 255)
    ov[r0 - 2, s:e + 1] = (255, 0, 255)
    ov[r1 + 2, s:e + 1] = (255, 0, 255)
for c in labelled:
    ov[30:46, int(round(c))] = (255, 0, 0)
Image.fromarray(ov).save(os.path.join(HERE, "..", "work", "fig7_overlay.png"))

write_csv(os.path.join(HERE, "fig7.csv"), [
    "Nikitin et al. 2024, J. Synchrotron Rad. 31, 851-866, Figure 7 (p. 858): Nvidia Nsight Systems timeline of the",
    "  asynchronous 1D USFFT (laminographic backprojection). One row per box on the timeline.",
    "Columns: series (timeline row and box type as printed), label (the text printed inside the box, truncated as",
    "  printed; empty where none is readable), annotation (the authors' brace label over/under the box: 'GPU calculations",
    "  chunk N', 'CPU->GPU copy chunk N+1', ...), t_start_ms and t_end_ms = box extent on the ruler in ms after the '71s'",
    "  mark (the ruler is labelled +600ms ... +660ms), duration_ms, x0_px/x1_px = pixel columns in the embedded image.",
    "Provenance: tier 3, digitized from the embedded 2205 x 648 px raster screenshot (no vector paths) by fig7_extract.py:",
    "  colour masks of the box fills (kernel boxes split at the light notch their rounded corners leave where two boxes",
    "  meet), time axis fitted on the seven labelled major ticks (+600 ... +660 ms, max residual",
    f"  {res:.3f} ms; one pixel = {abs(m):.4f} ms); the eight unlabelled major ticks fall on 5 ms multiples to < 0.3 ms.",
    "Uncertainty: about +-0.05 ms (1 px) per box edge. The kernel labels are assigned in the printed left-to-right order",
    "  of the six wide boxes of each chunk group (groups are separated by the cyan chunk-start boxes); the narrow",
    "  dark boxes at the end of each group carry no readable label. A memcpy block of a stream row consists of several",
    "  adjacent sub-boxes (seams visible in the screenshot); each sub-box is a row here, the overview bar is one bar.",
    "  Boxes cut by the right edge of the screenshot (the third DtoH 'Me...', the 'ga...' kernel) are given up to the edge.",
    "Not in the CSV: the CPU (64) utilization trace and the 'Processes'/'tomocupy' rows (no readable values), the stream",
    "  percentages printed at the left (52.7% Stream 18, 11.9% Stream 17, 11.8% Stream 16, 11.2% Stream 19, 3 streams",
    "  hidden), and the asterisks marking CPU time spent on pinned memory (see the figure caption and the \\alttext).",
], ["series", "label", "annotation", "t_start_ms", "t_end_ms", "duration_ms", "x0_px", "x1_px"], rows_out,
    fmt=["{}", "{}", "{}", "{:.2f}", "{:.2f}", "{:.2f}", "{}", "{}"])
print("wrote fig7.csv", len(rows_out), "rows; ticks", [round(float(ft(c)), 2) for c in ticks], "res", res)
