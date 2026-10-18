# templier2019: decompiled

Thomas Templier. "MagC, magnetic collection of ultrathin sections for volumetric correlative light and
electron microscopy." *eLife* **2019**;8:e45696. DOI [10.7554/eLife.45696](https://doi.org/10.7554/eLife.45696).
Received 31 January 2019; accepted 02 July 2019; published 11 July 2019. Tools and Resources, Neuroscience.

**Licence:** "Copyright Templier. This article is distributed under the terms of the Creative Commons
Attribution License, which permits unrestricted use and redistribution provided that the original author
and source are credited." (p. 1; CC BY 4.0.)

## Local and external

**In the local collection**
- Source files:
  - `papers/templier2019/elife-45696-v3.pdf` – the article, 18 pp., eLife version of record (v3)
  - `papers/templier2019/elife_figure_supplements/` – the 11 figure supplements as full-size JPEGs (fig1-figsupp1.jpg … fig1-figsupp5.jpg, fig2-figsupp1.jpg … fig2-figsupp6.jpg), `papers/templier2019/elife_figure_supplements/elife_api_article.json` (source of their legends) and a SOURCE.txt → `decompiled/templier2019/supplement.tex`
  - `papers/templier2019/elife-45696-v3.txt`, `papers/templier2019/elife-45696-v3.raw.txt` – earlier text extractions (not used)
  - `papers/templier2019/SOURCE.txt` – fetch note
- Cited works decompiled here: kasthuri2015 (`decompiled/kasthuri2015/`), mikula2015 (`decompiled/mikula2015/`)

**External pull needed** (not on this machine)
- Videos 1–3 – https://youtu.be/o13r-tHT9-c, https://youtu.be/UC8Zrl2Xud4, https://youtu.be/VL0F9DkZVaQ – only a still frame of each is in the PDF (`decompiled/templier2019/figures/video1.png` … video3.png)
- Transparent reporting form – DOI 10.7554/eLife.45696.021 – not needed for the decompile
- Decision letter and author response – DOI 10.7554/eLife.45696.027, 10.7554/eLife.45696.028 – not needed for the decompile
- Datasets 1 and 2 (templier19_dataset_1, templier19_dataset_2) – https://neurodata.io/data/templier2019/ – image volumes, not plot source data
- Code – https://github.com/templiert/MagC (archived copy https://github.com/elifesciences-publications/MagC) – produced the similarity matrices of Fig. 2a; run on the datasets it would be the tier-1 source for that panel
- All other cited references: 43 entries in the reference list (45 unnumbered, alphabetical entries) without a [local: …] tag.

## Source files (`../../papers/templier2019/`)

| file | what it is |
|---|---|
| `elife-45696-v3.pdf` | the article, 18 pp. **Publisher version of record**, eLife typeset PDF, version 3 (`SOURCE.txt`: fetched from cdn.elifesciences.org). |
| `elife-45696-v3.txt`, `.raw.txt` | earlier text extractions of the same PDF (looked at, not used). |
| `elife_figure_supplements/fig1-figsupp1..5.jpg`, `fig2-figsupp1..6.jpg` | the 11 figure supplements, full-size JPEGs from iiif.elifesciences.org (added by the coordinator on 2026-10-17; `SOURCE.txt` there). |
| `elife_figure_supplements/elife_api_article.json` | the eLife API record of the article; source of the supplement legends (objects `fig1s1` … `fig2s6`: label, title, caption). |

**The figure supplements are not in the PDF**, which prints only their titles and DOIs (pp. 2 and 4). They
are decompiled in `supplement.tex` from the JPEGs and the legends in the API JSON (see below).

**Naming of the supplement files:** Figure N—figure supplement M → `figures/sfigN-M.jpg` (the source JPEG,
copied unchanged; not re-encoded to PNG because the largest are 3780 × 4442 px), panel x → `sfigN-Mx.csv`,
`sfigN-Mx.py` etc. Example: Figure 2—figure supplement 2, panel a → `figures/sfig2-2a.csv`.

**Not available** (named by the paper, not in the source folder, not fetched):
- Videos 1–3 (YouTube https://youtu.be/o13r-tHT9-c, https://youtu.be/UC8Zrl2Xud4, https://youtu.be/VL0F9DkZVaQ); the PDF has only a still frame of each, included as `figures/video1.png` … `video3.png`.
- Transparent reporting form (DOI 10.7554/eLife.45696.021).
- Decision letter and author response (10.7554/eLife.45696.027, .028).
- Data: Datasets 1 and 2 on NeuroData (https://neurodata.io/data/templier2019/, `templier19_dataset_1`, `templier19_dataset_2`). These are image volumes, not plot source data.
- Code: https://github.com/templiert/MagC (archived copy https://github.com/elifesciences-publications/MagC). This code produced the similarity matrices of Fig. 2a, so it (run on the datasets) would be the tier-1 source for that panel.

No eLife "source data" files are listed for any figure.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: article type and footer citation (given
  once), title, author, affiliation, the p. 1 margin block (correspondence, present address, competing
  interest, funding pointers, dates, reviewing editor, copyright), abstract, Results, Discussion,
  Materials and methods, Tables 1–3, the figure and video captions, Acknowledgements, Additional
  information (competing interests, funding table, author contributions, ORCID, ethics, decision letter),
  Additional files, Data availability with its datasets table, and the 45 references (unnumbered,
  alphabetical, as printed).
- `supplement.tex` / `supplement.pdf`: the 11 figure supplements (Figure 1—figure supplements 1–5, Figure
  2—figure supplements 1–6) in the eLife order, each with its image, its legend verbatim from the API JSON
  (label, title, caption, DOI) and a description; `\figuredata` for the plotted panels. No PDF pages, so no
  `\pdfpage` marks; "Figure supplements of Figure 1/2" are `\decompnote`s, not headings (the paper prints none).
  Built from `work/legends/supplement_template.tex` + `work/legends/legend_*.tex` (`make_legends.py`, then
  `assemble.py`); edit the template, not supplement.tex, and re-run both.
- `figures/`: `fig1.png`, `fig2.png` (200 dpi crops of the figure boxes), `video1.png`–`video3.png`
  (stills), `sfig1-1.jpg` … `sfig2-6.jpg` (supplements); data for the plotted panels: `fig2a.*`,
  `sfig2-1a.csv`, `sfig2-1b.csv`, `sfig2-1c.csv`, `sfig2-1c_lines.csv`, `sfig2-1d.csv` (one extract script
  `sfig2-1_extract.py`, one plot script `sfig2-1.py` → `sfig2-1_replot.png` for the four panels),
  `sfig2-2a.csv` with `sfig2-2a_extract.py`, `sfig2-2a.py`, `sfig2-2a_replot.png`.
- `tables/`: `table1.csv`, `table2.csv`, `table3.csv`, plus `funding.csv` and `datasets.csv` (the two
  untitled tables on pp. 15–16). Captions/footnotes in `#` lines. Table 3 is transposed (one row per antigen).
- `work/`: scratch (page renders, embedded Fig. 2 image, overlays, rebuilt matrices, `cmp_fig2a.png`,
  `check.json`). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (and
`supplement.tex`); both compile without errors (run twice); some overfull lines from long URLs and table cells.

Re-run the data: `python3 -I figures/<x>_extract.py` then `python3 -I figures/<x>.py` for x = fig2a (≈10 s),
sfig2-1, sfig2-2a.

## Figures

Both figures are single raster JPEGs (Fig. 1: 6957 × 1728 px ≈ 950 ppi; Fig. 2: 9615 × 2297 px ≈ 1313 ppi).
`vector_dump.py` (re-run after the coordinator's fix for zero-width/height lines) finds only the thin
rectangle around each figure box; no plot paths or text inside the figures. So the one plotted panel is tier 3.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | schematic of the block assembly + colour light micrograph of the block face | – | – | |
| Fig. 1b | photograph of the set-up, labelled | – | – | |
| Fig. 1c | light micrographs: wafer overview, close-up, montage | – | – | |
| Fig. 2a (matrices 1–4) | four similarity matrices (greyscale cell images, axes = section index 0–200) | `figures/fig2a.csv` | 3 digitized | no colour bar: grey level only (uncalibrated proxy, darker = more similar) |
| Fig. 2b | 3D rendering of the correlative stack + 2 EM/LM insets | – | – | |
| Fig. 2c | EM micrograph with neurite skeletons | – | – | |
| Video 1–3 | video stills | – | – | videos not available |
| Fig. 1—fs1 a, b, c | LM wafer overview; fluorescence close-up; montage | – | – | |
| Fig. 1—fs2 a–d | SEM/EM micrographs | – | – | |
| Fig. 1—fs3 a–g | photographs (device, oven, block faces) | – | – | |
| Fig. 1—fs4 | LM wafer overview | – | – | |
| Fig. 1—fs5 a–d | LM overview, multibeam EM mosaic, tile, inset | – | – | |
| Fig. 2—fs1 a | similarity matrix (unordered, EM) | `figures/sfig2-1a.csv` | 3 digitized | grey per image pixel (cells not resolved); uncalibrated |
| Fig. 2—fs1 b | similarity matrix (reordered) | `figures/sfig2-1b.csv` | 3 digitized | as a |
| Fig. 2—fs1 c | similarity matrix with coloured lines (legend 1, 2, 3, 4, 7) | `figures/sfig2-1c.csv`, `sfig2-1c_lines.csv` | 3 digitized | lines: position + colour class; a lower bound |
| Fig. 2—fs1 d | bar chart, values printed on the bars | `figures/sfig2-1d.csv` | printed values (exact) + 3 digitized heights | |
| Fig. 2—fs2 a | histogram, 60 bins | `figures/sfig2-2a.csv` | 3 digitized | heights within 0.02 of integers |
| Fig. 2—fs2 b–f | LM and EM micrographs, SIFT crosses | – | – | |
| Fig. 2—fs3 a–g | SEM micrographs, montage with labels | – | – | timeline labels transcribed in `\alttext` |
| Fig. 2—fs4 | gallery of 48 EM images | – | – | |
| Fig. 2—fs5 a–f | schematics (a, f), fluorescence (b), EM (c–e) | – | – | |
| Fig. 2—fs6 | neuroglancer screenshot | – | – | |

Panels per tier: tier 1: 0; tier 2: 0; tier 3: 6 (Fig. 2a; Fig. 2—fs1 a, b, c, d; Fig. 2—fs2 a), of which
Fig. 2—fs1 d also carries the exact printed bar values; tier 4: 0.

**Fig. 2a extraction.** Each matrix is a grid of square cells. The frame lines (minima of the mean grey
profile) give 4.876 px per cell = **204 × 204 cells** per matrix; an independent period/phase fit of the cell
edges inside each matrix gives the same period (4.875–4.8775 px; a 203-cell grid would be 4.90 px and
fits clearly worse) and puts the edges within 0.3 px of the frame-based grid; the ticks 0, 50, …, 200 sit
on cell centres. All 204 diagonal cells are black in matrices 1–3 (202 in matrix 4, where 2 are under the
red lines). Each cell is the median grey of its inner ≤3 × 3 px. Flags: `red_line` (the two horizontal +
two vertical red lines in matrix 4, over rows/columns 200 and 202), `panel_label` (cells under the strokes
of the printed digits 1–4), `partly_hidden` (first/last row and column, half under the frame line).
Grey uncertainty ≈ ±5 levels (JPEG).

**Checks done:** (1) the cell centres drawn over the source image (`work/fig2a_overlay*.png`, including
8× zooms of the top-left and bottom-right corners): every point sits in the middle of a cell; (2) the
matrices rebuilt from the CSV at source resolution (`work/fig2a_rebuilt.png`) differ from the source by a
median of 0 grey levels (95th percentile 1–50, from JPEG ringing at the edges of isolated dark cells);
(3) `tools/compare.py` original vs re-plot (`work/cmp_fig2a.png`), looked at: all four matrices, the
diagonal bands, the white cross at row/column 22 in matrix 4, the red lines, axes ranges and ticks match.

**Fig. 2—fs1 extraction** (`figures/sfig2-1_extract.py`, docstring has the details). The matrices are
381 px wide with ticks 74.2 px per 100 sections, so one pixel is ≈ 1.35 matrix cells: the cells are not
resolved and the CSVs are grids at the image's native resolution (one grey value per pixel; section index of
each pixel from 6 ticks per axis, residual ≤ 0.42 sections). The frame ends at index ≈ 514 (Dataset 1: 507
sections; panel d's counts sum to 513, i.e. 514 sections). Printed panel letters are blanked. The coloured
lines over c are listed in `sfig2-1c_lines.csv`: positions are consistent (75 of 78 vertical lines have a
horizontal line within 2 sections; the matrix is symmetric), colour labels less so (54 of 78 agree), because
JPEG chroma subsampling desaturates and smears 1-px lines; classification is by the signs of R−G and B−G.
Panel d: bar heights digitized within 1.5 of the printed values (375, 103, 26, 7, 1, 0, 0, 1).
**Checks:** tick-fit overlays (`work/sfig2-1a/b/c_overlay.png`), line-position overlay
(`work/sfig2-1c_lines_overlay.png`, marks in the margin at each detected line), bar-top overlay
(`work/sfig2-1d_overlay.png`), and `work/cmp_sfig2-1.png` (original vs re-plot), all looked at: matrices,
band shapes, line pattern, bar heights and axes match.

**Fig. 2—fs2a extraction** (`figures/sfig2-2a_extract.py`): 6 y ticks (0–10), 5 x ticks (500–2500, labels
1000 and 2000), 60 equal bins; every bar height is within 0.02 of an integer; the integers sum to **201**
(the legend says 203 LM-EM pairs). The "0" label sits under the y axis, which by the tick spacing is at
≈ 67 inliers (the histogram starts at the data minimum, not at 0). Checks: `work/sfig2-2a_overlay_zoom.png`
(bar tops marked; all on the bars), `work/cmp_sfig2-2a.png` (side by side), looked at.

## Text check (`tools/check_text.py`, version 2026-10-17e)

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without in-figure text) | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 98.7 % | 99.7 % (125 repeated tokens) | 99.7 % (0 in-figure tokens) | 99.8 % | 0 | 0 |
| `supplement.tex` | not applicable: no PDF (legends checked against the JSON instead, see below) | | | | | |

(The first version of this README gave 98.4 / 99.4 % with the earlier tool version.)

- Repeated text: the running header "Tools and resources / Neuroscience" and footer "n of 18" (boilerplate).
  The footer citation line is given once at the top, so it counts as matched.
- With `--min-run 1` (34 MISSING / 28 EXTRA tokens), every unmatched token is one of: **μ printed in a
  Symbol-type font, read as "m"** (μm, μL in 16 places, μmanager/μManager in two references); **degree signs
  printed as a raised "o"** (text layer "oC"; written °C); split accents (Fédérale ×2, Körber, Pérez,
  Bañobre-López); and "Tools and resources Neuroscience" given once at the top (EXTRA).
- Line-end hyphens: abstract "post-/embedding" is written **post-embedding** (as in the eLife API JSON; the
  first version of this decompilation had "postembedding"). The YouTube ID "o13r-tHT9-c" keeps its line-end
  hyphen (confirmed by the JSON). reel-to-reel, wafer-wide, anti-rhodamine, element-guided, Super-Resolution
  and ethz-b-000267370 were checked against the JSON too.

**Legend check (supplement.tex vs JSON):** `work/legends/check_legends.py` strips the markup on both sides
and compares character by character (output in `work/legends/check_legends_output.txt`): **all 11 supplement
legends (label, title, caption) and DOIs are identical to the JSON.** The same script compares the main
figure, video and table captions of `main.tex` (transcribed from the PDF) with the JSON: Figures 1 and 2,
Videos 1–3 and Tables 2–3 are identical (Table 1 has no caption object in the JSON).

Read-through against the page images (step 4): μ in every unit, × in "0.5 × 0.5 mm", "3 × 3", "2 × 2",
"2000 × 2000", the immunostaining list; ∼ (printed as a tilde; written `\textasciitilde`) in "#∼4000",
"#∼5000", "∼15,000", "∼500", "∼20 mm", "∼50/50", "∼1000", "an ∼ 2 degree"; "dH₂O" subscript in the list but
"ddH2O" plain in the staining protocol (as printed); en dashes in ranges and catalogue numbers
(#SMB-0–038, 66030–668, #S-04–01 N, #16084–1); bold "2-4" in the flip example; "(2 – correlation)";
italic *en passant*; reference formatting (italic journal and book titles, bold volumes).

## Errors and oddities in the paper (kept verbatim, flagged with `\decompnote` where useful)

Figure supplements:
- **Fig. 2—fs1: legend and image disagree for c and d.** The legend says (c) is the unordered bead matrix and (d) the reordered matrix; the image shows (c) a reordered matrix overlaid with coloured lines (legend 1, 2, 3, 4, 7, unexplained) and (d) a bar chart of values 375, 103, 26, 7, 1, 0, 0, 1 for categories 0–7 (unexplained; it looks like the frequency of the link costs of the Methods' "Metric", but the paper does not say so). The deviations "around section number 500" are said to be in the "lower left" of the matrix; section 500 is at the lower right.
- Fig. 2—fs1: the matrices span ≈ 514 sections, and the counts in d sum to 513 (= 514 − 1 links), while Dataset 1 has 507 sections.
- Fig. 2—fs2: the histogram sums to 201, the legend says 203 LM-EM pairs; "(d) Same micrograph as in (a)": the micrograph is (b), (a) is the histogram.
- Fig. 2—fs3: scale bars "200 mm", "100 mm", "500 mm", "2 mm" for single sections and ultrastructure (μm surely meant; the μ seems lost as in the PDF text layer); the legend says the processes are painted "red, green and blue", the image shows red, green and yellow.

Main article:

- Figure 2 title: the first sentence is printed twice ("…collected sections.Volumetric correlative LM-EM with MagC collected sections."); Figure 2—figure supplement 3 title lacks a space ("block.All").
- Metric example (p. 12): "A single flip such as 1-2-4-3-5-6 has the cost 0,1,0,1,0,0": six costs for five links; by the stated rule it is 0,1,0,1,0. (The other two examples are consistent.)
- EM dwell time for Dataset 1: 820 ns in Table 2, 750 ns in Methods (Electron microscopy).
- Fig. 2a: the matrices have 204 × 204 cells, while Dataset 2 has 203 sections (text, Table 2). Not explained in the paper.
- Fig. 2b label "500 sections x 50 nm" vs the caption's "507 consecutive ultrathin sections" (rounded label; not necessarily an error).
- "see Methods, paragraph K" (p. 14): the Methods are not lettered.
- Table 1 "Media-Lateral" (for medio-lateral); "Thor a" in the Deerinck reference; "An horizontal band", "A ionizer" (kept).
- Video 1 caption "Timeline:1." without a space (kept).

## Problems and suggestions for the spec / tools

- **Task brief vs source:** the brief said the figure supplements are inside the PDF; for eLife v3 PDFs they are not (only titles). Fixed by the coordinator (JPEGs + API JSON added). For other eLife papers: put the JSON and JPEGs in the source folder from the start; the JSON also settles line-end hyphens and Symbol-font characters of the main text.
- **Spec, supplements without a PDF:** `\pdfpage` and check_text.py do not apply; the spec could name the legend check (here `work/legends/check_legends.py`) as the replacement, say whether to keep JPEGs or convert to PNG, and allow one plot script for a multi-panel figure (done here for Fig. 2a and Fig. 2—fs1).
- **`vector_dump.py`:** zero-width/height lines were dropped (fixed by the coordinator mid-task; re-run, no change for this paper).
- **`check_text.py`:** Symbol-font μ → "m" and raised-o degree signs make many 1-token MISSING/EXTRA pairs. A small substitution table on the tex side (μ→m, °→o) would make the low-`--min-run` listing much shorter. Split accents in the eLife text layer ("Lo´ pez") break words into two tokens; normalising "letter + spacing accent + space + letters" in the PDF text would fix that.
- **`digitize_common.py`:** has no helper for matrix/heat-map displays (grid finding by period/phase fit, per-cell sampling, masking overlaid labels). I wrote it inline in `fig2a_extract.py`; it could be moved into the tools. `frame_lines()` with one window for a whole row of panels gave a 2 px wrong frame for the lower panels; per-panel detection was needed.
- **Spec:** says nothing about videos; I treated the video stills like figures (caption + description). It could also say how to handle a heat map without a colour bar (I gave the grey level and darkness = 1 − grey/255, with a warning that it is not calibrated).
