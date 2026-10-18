# hesse2026: decompiled

Janis K. Hesse, Frank F. Lanfranchi, Conor McGrory, Yuelin Shi, Tatiana A. Engel, Doris Y. Tsao. "Rapid alternation of
conscious and suppressed stimulus representations in the primate brain." *bioRxiv* preprint, version 1, posted
16 October 2026. DOI [10.64898/2026.10.15.759299](https://doi.org/10.64898/2026.10.15.759299).

**Licence:** CC-BY 4.0 International, as stated in the footer of every text page of the PDF ("The copyright holder
for this preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a license
to display the preprint in perpetuity. It is made available under a CC-BY 4.0 International license.").

**Version:** preprint version 1 (not peer reviewed), the bioRxiv full-text PDF. There is no journal version.

## Source files (`source/`)

| file | what it is |
|---|---|
| `2026.10.15.759299v1.full.pdf` | the bioRxiv full-text PDF, 50 pages: 34 text pages (title and summary, introduction, results, discussion, figure legends on pp. 16–20, Extended Data legends on pp. 20–23, methods, acknowledgements, 35 references) and 16 figure pages (Figures 1–6 on pp. 35–40, Extended Data Figures 1–10 on pp. 41–50; images only, no footer). |
| `SOURCE.txt` | where and how the PDF was obtained. |

**Not available locally** (named in the paper): the electrophysiology data (DANDI Archive, "upon publication") and
the analysis code (GitHub, "upon publication"). There are no source-data files and no supplement; every plotted
panel is therefore tier 2 (vector paths) or tier 3 (embedded raster image), never tier 1.

## Contents

- `main.tex` / `main.pdf`: the whole preprint in reading order: title, authors, affiliations and present addresses,
  Summary, Introduction, Results, Discussion, the figure legends (pp. 16–20), "Extended Data Figures" legends
  (pp. 20–23), Methods, Data and Code availability, Acknowledgements, Funding, Author contributions, Competing
  interests, Additional Information, the 35 references (original numbering, as text in `hangpars`), and then the 16
  figure pages (pp. 35–50), each as a 200-dpi render with a panel-by-panel `\alttext` description and one
  `\figuredata` line per data file. Citations are kept as the superscript numbers the PDF prints (ranges such as
  "21-23" as printed; one citation number that the PDF prints as plain text is kept as plain text, with a note).
  `\pdfpage{N}` marks the start of every PDF page; `\decompnote` marks the few decompiler remarks.
- `decomp.sty`: copy of `../tools/decomp.sty`, so `lualatex main.tex` works from this folder.
- `figures/` (flat, 696 files):
  - `fig1.png` … `fig6.png`, `edfig1.png` … `edfig10.png`: the whole figure pages rendered at 200 dpi (the PDF's
    figure pages carry no caption text, so there is nothing to crop away);
  - 102 CSVs, one or more per plotted panel (`<panel>.csv`, `<panel>_<series>.csv`; `#` header lines give page,
    paths used, tick values used for the axis calibration, calibration residual and caveats);
  - 94 Python scripts: `<fig>_extract.py` (one per figure, regenerates all CSVs and extracted images of that
    figure from the PDF; `edfig6_extract.py` runs `edfig5_extract.py` for page 46, which handles both pages), `<panel>.py`
    (re-plots the panel from its CSVs only → `<panel>_replot.png`), and helper modules (`fig3_common.py`, `_style.py`,
    `helpers.py`, `edfig_extract_lib.py`, `dashgeo.py`, `_edfig8_common.py`, `fig4b_raw.py`);
  - 73 `<panel>_replot.png` re-plots and 73 `<panel>_compare.png` side-by-side checks (original 300-dpi crop | re-plot);
  - 337 PNGs of image panels and embedded images at native resolution (`fig1a.png`, face-image grids
    `edfig5a_r<row>_<column>.png`, stimulus icons, colour bars, …), see the figure table.
- `tables/`: none. The paper prints no table; the only tabular panel (Extended Data Fig. 10a, a model × test
  check/cross matrix) is transcribed in its `\alttext` and stored as `figures/edfig10a.csv`.
- `work/`: scratch (page renders, the earlier `paper.tex` layout, the per-figure panel files, conversion scripts,
  check output, extraction regression). May be deleted.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` from this folder (twice); compiles without
errors; a few overfull lines from unbreakable grant numbers, e-mail addresses and file names.
Re-run the data: `python3 -I figures/<fig>_extract.py` (rewrites that figure's CSVs and extracted PNGs; needs
`../tools/pdfplot.py`, found relative to the script) and `python3 -I figures/<panel>.py` (any working directory;
each script changes into `figures/`).

**Layout history.** Decompiled 2026-10-17 in an earlier layout (`paper.tex` with `natbib` citations, per-figure
folders `figures/<fig>/` with `<fig>_panels.tex` holding the alt text as `graphicx` `alt=` keys, redraws as
`<panel>.pdf/.png`); converted to this SPEC layout on 2026-10-18. The text, CSVs, extraction and plotting code and
alt texts were carried over unchanged (the conversion only moved files, rewrote paths, renamed the re-plot outputs
and merged the per-panel alt texts into one `\alttext` per figure). The old files are in `work/`.

The figures in the PDF are vector graphics: data lines are stroke paths (typically one vertex per sample),
error bands are filled polygons, scatter points are small closed paths, histogram bars and heatmap cells are
rectangles, and tick marks are thin rectangles. Coordinates were read from the PDF with PyMuPDF and mapped to
data coordinates by calibrating each axis on its tick marks (tick values were read off the rendered panel,
because the numeric tick labels are glyph outlines, not text). Each CSV starts with `#` comment lines giving
the page, the paths used, the tick values used for calibration and the calibration residual. Face stimuli,
MRI scans and some heatmaps are embedded raster images and were extracted at native resolution.

Numbers in the CSVs are therefore as precise as the PDF's coordinates (~0.01 pt), not the authors' original
numbers; see each figure's README for what could and could not be recovered.

## Text check (`../tools/check_text.py` version 2026-10-17j, run 2026-10-18)

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text only (also without text printed inside figures) | tex tokens found in PDF | MISSING runs ≥ 6 | EXTRA runs ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 85.4 % | **98.0 %** (2838 repeated tokens) | **98.7 %** (137 figure-internal tokens) | 100.0 % | 12 runs, 151 tokens, all inside figures | 0 |

PDF tokens 22157, tex tokens 18933. What is not matched:

- **Repeated text** (left out by the second number): the bioRxiv footer on all 34 text pages (quoted once in a
  `\decompnote` at the top of `main.tex`), and axis labels, keys and panel letters that recur on several figure
  pages ("explained variance of features", "number of faces decoding accuracy", "conscious ground truth
  reconstruction state 1", …).
- **MISSING runs** (all on the figure pages 35–50): text printed inside the figures (axis titles, tick numbers,
  keys, panel letters), which belongs in the `\alttext` descriptions, where it is:

| page | tokens | run |
|---|---|---|
| p. 35 | 9 | 145 visual cells 215 visual cells left eye suppressed |
| p. 35 | 14 | left eye right eye binocular flash suppression percept left eye right eye time stimulus |
| p. 35 | 16 | 2 0 2 4 6 0 20 40 60 80 100 2 0 2 4 6 |
| p. 35 | 16 | 1 0 5 0 0 5 1 1 1 0 1 0 1 response norm 1 |
| p. 36 | 13 | k time from transition ms time from transition ms time from transition ms |
| p. 37 | 13 | time from transition ms time from transition ms time from transition ms state |
| p. 38 | 12 | projection onto preferred axis a u projection onto orthogonal axis a u |
| p. 38 | 8 | 1 1 1 1 1 1 1 1 |
| p. 38 | 17 | number of neurons mean state 2 norm mean state 1 norm number of cells gain 0 3 |
| p. 39 | 12 | norm conditional log likelihood ratio median dwell time ms bin size ms |
| p. 45 | 7 | leave one neuron out 50 high confidence |
| p. 49 | 14 | mean state 2 norm mean state 1 norm number of cells gain 0 3 |

- **EXTRA runs:** none. Every run of six or more tex tokens is found in the PDF.
- The only intentional deviation from the printed text: none. Line-end hyphens were checked by hand in the first
  pass (all 28 are compound hyphens and were kept). The citation superscripts are printed as in the PDF.
- Before the conversion, a word-level diff of the compiled `paper.pdf` against the original (letters only,
  ignoring math and citation numbers) showed no missing or altered words; this check is now superseded by
  `check_text.py`.

## Figures

Every figure page is included as a 200-dpi render with an `\alttext` description written panel by panel (printed
labels, axes, ranges, series, approximate values, statistics marks) and one `\figuredata` line per data file.
Provenance tiers: 2 = vector paths in the PDF (exact up to the PDF's ~0.01 pt precision; axes calibrated on the tick
marks, whose values were read off the rendered panel because the tick labels are glyph outlines); 3 = embedded
raster image at native resolution (heatmaps, Fig. 5b's state map); image panels (schematics, MRI, face images)
have no data. The original figure work checked every re-plot against the original two ways: the recovered points
were drawn back onto 300-dpi crops of the original during extraction, and `<panel>_compare.png` puts the original
crop next to the re-plot (both inspected; details per figure below). On 2026-10-18 every `<panel>.py` was run
again from the CSVs to produce the `_replot.png` files (71 scripts, no failures), and every `<fig>_extract.py` was
run again in a scratch copy (`work/regress/`): all 16 ran without error and wrote 381 files, 374 of them byte-identical to the
committed ones; the 7 CSVs that differ (`fig2i.csv`, `edfig5b.csv`, `edfig5c.csv`, `edfig5e.csv`, `edfig5f.csv`, `edfig6b.csv`,
`edfig6c.csv`; 37 data lines in all) are exactly the ones whose dashed-series values were corrected with `../tools/dashlines.py`
after extraction (see "Known problems"); the extract scripts reproduce the pre-correction values. The 300-dpi crops of the
original panels (`<panel>_orig.png`) that the re-run produced for Extended Data Figs. 5, 6, 7, 9 and 10 were added to `figures/`,
so every figure now has the crops its `_compare.png` images were made from.

| figure | panel | type | data | tier | scripts |
|---|---|---|---|---|---|
| Fig. 1 | a | image: schematic | `fig1a.png` … (3 PNGs) | – | – |
| Fig. 1 | b | plot: two line plots side by side | `fig1b_left_eye_suppressed.csv`, `fig1b_right_eye_suppressed.csv` | 2 vector | `fig1_extract.py`; `fig1b.py` → `fig1b_replot.png` |
| Fig. 1 | c | image: colour cartoon | `fig1c.png` | – | – |
| Fig. 1 | d | image: rendered CAD drawing | `fig1d.png` | – | – |
| Fig. 1 | e | image: black line drawing | `fig1e.png` | – | – |
| Fig. 1 | f | plot: two heatmaps side by side | `fig1f_AM.csv`, `fig1f_ML.csv`, `fig1f_colourbar.csv` | 3 embedded raster | `fig1_extract.py`; `fig1f.py` → `fig1f_replot.png` |
| Fig. 1 | g | plot: spike raster | `fig1g_layout.csv`, `fig1g_spikes.csv` | 2 vector | `fig1_extract.py`; `fig1g.py` → `fig1g_replot.png` |
| Fig. 1 | h | plot: scatter plot | `fig1h.csv` | 2 vector | `fig1_extract.py`; `fig1h.py` → `fig1h_replot.png` |
| Fig. 2 | a | image: schematic | `fig2a.png` | – | – |
| Fig. 2 | b | plot: spike raster | `fig2b_spikes.csv`, `fig2b_states.csv` | 2 vector | `fig2_extract.py`; `fig2b.py` → `fig2b_replot.png` |
| Fig. 2 | c | plot: line plot | `fig2c.csv` | 2 vector | `fig2_extract.py`; `fig2c.py` → `fig2c_replot.png` |
| Fig. 2 | d | plot: autocorrelation | `fig2d.csv` | 2 vector | `fig2_extract.py`; `fig2d.py` → `fig2d_replot.png` |
| Fig. 2 | e | plot: two dense spike rasters aligned to state transitions, x axis time from | `fig2e_state1_to_state2.csv`, `fig2e_state2_to_state1.csv` | 2 vector | `fig2_extract.py`; `fig2e.py` → `fig2e_replot.png` |
| Fig. 2 | f | plot: two spike rasters | `fig2f_state1_to_state2.csv`, `fig2f_state2_to_state1.csv` | 2 vector | `fig2_extract.py`; `fig2fg.py` → `fig2f_replot.png` |
| Fig. 2 | g | plot: same layout as panel f | `fig2g_state1_to_state2.csv`, `fig2g_state2_to_state1.csv` | 2 vector | `fig2_extract.py`; `fig2fg.py` → `fig2g_replot.png` |
| Fig. 2 | h | image: grid of 20 face images (embedded rasters) | `fig2h_r1_gt_conscious.png` … (20 PNGs) | – | – |
| Fig. 2 | i | plot: explained variance | `fig2i.csv` | 2 vector | `fig2_extract.py`; `fig2i.py` → `fig2i_replot.png` |
| Fig. 2 | j | plot: decoding accuracy | `fig2j.csv` | 2 vector | `fig2_extract.py`; `fig2j.py` → `fig2j_replot.png` |
| Fig. 2 | k | plot: three small plots | `fig2k.csv` | 2 vector | `fig2_extract.py`; `fig2k.py` → `fig2k_replot.png` |
| Fig. 2 | l | plot: single-trial decoding accuracy | `fig2l.csv` | 2 vector | `fig2_extract.py`; `fig2l.py` → `fig2l_replot.png` |
| Fig. 3 | a | plot: box plot | `fig3a_box.csv`, `fig3a_points.csv` | 2 vector | `fig3_extract.py`; `fig3a.py` → `fig3a_replot.png` |
| Fig. 3 | b | plot: two dense spike rasters side by side | `fig3b_meta.csv`, `fig3b_state1_to_state2.csv`, `fig3b_state2_to_state1.csv` | 2 vector | `fig3_extract.py`; `fig3b.py` → `fig3b_replot.png` |
| Fig. 3 | c | plot: two small spike rasters | `fig3c_state1_to_state2.csv`, `fig3c_state2_to_state1.csv` | 2 vector | `fig3_extract.py`; `fig3c.py` → `fig3c_replot.png` |
| Fig. 3 | d | plot: two small spike rasters, same layout as panel c, | `fig3d_state1_to_state2.csv`, `fig3d_state2_to_state1.csv` | 2 vector | `fig3_extract.py`; `fig3d.py` → `fig3d_replot.png` |
| Fig. 3 | e | image: grid of 20 face images (embedded rasters) | `fig3e_r1_gt_conscious.png` … (20 PNGs) + `fig3e_orig.png` (300-dpi crop of the original) | – | – |
| Fig. 3 | f | plot: line plot | `fig3f.csv` | 2 vector | `fig3_extract.py`; `fig3f.py` → `fig3f_replot.png` |
| Fig. 3 | g | plot: line plot | `fig3g.csv` | 2 vector | `fig3_extract.py`; `fig3g.py` → `fig3g_replot.png` |
| Fig. 3 | h | plot: three small line plots | `fig3h_average.csv`, `fig3h_state1.csv`, `fig3h_state2.csv` | 2 vector | `fig3_extract.py`; `fig3h.py` → `fig3h_replot.png` |
| Fig. 3 | i | plot: paired line plot | `fig3i.csv` | 2 vector | `fig3_extract.py`; `fig3i.py` → `fig3i_replot.png` |
| Fig. 4 | a | plot: four scatter plots in a 2 by 2 grid | `fig4a.csv`, `fig4a_inset.csv` | 2 vector | `fig4_extract.py`; `fig4a.py` → `fig4a_replot.png` |
| Fig. 4 | b | plot: four heatmaps in a 2 by 2 grid | `fig4b_state1_conscious.csv`, `fig4b_state1_suppressed.csv`, `fig4b_state2_conscious.csv`, `fig4b_state2_suppressed.csv` | 3 embedded raster | `fig4_extract.py`; `fig4b.py` → `fig4b_replot.png` |
| Fig. 4 | c | plot: three stacked histograms | `fig4c.csv` | 2 vector | `fig4_extract.py`; `fig4c.py` → `fig4c_replot.png` |
| Fig. 4 | d | plot: scatter plot | `fig4d.csv` | 2 vector | `fig4_extract.py`; `fig4d.py` → `fig4d_replot.png` |
| Fig. 4 | e | plot: scatter plot | `fig4e.csv` | 2 vector | `fig4_extract.py`; `fig4e.py` → `fig4e_replot.png` |
| Fig. 4 | f | plot: line plot | `fig4f.csv` | 2 vector | `fig4_extract.py`; `fig4f.py` → `fig4f_replot.png` |
| Fig. 4 | g | plot: four scatter plots in a 2 by 2 grid | `fig4g.csv` | 2 vector | `fig4_extract.py`; `fig4g.py` → `fig4g_replot.png` |
| Fig. 5 | a | image: schematic | `fig5a.png` | – | – |
| Fig. 5 | b | plot: heatmap | `fig5b_state.csv`, `fig5b_state1_fraction.csv` | 2 vector + 3 raster | `fig5_extract.py`; `fig5b.py` → `fig5b_replot.png` |
| Fig. 5 | c | plot: two stacked line plots against HMM bin size in ms on a logarithmic x a | `fig5c.csv` | 2 vector | `fig5_extract.py`; `fig5c.py` → `fig5c_replot.png` |
| Fig. 5 | d | plot: line plot | `fig5d.csv` | 2 vector | `fig5_extract.py`; `fig5d.py` → `fig5d_replot.png` |
| Fig. 5 | e | plot: two line plots | `fig5e_AM_to_ML.csv`, `fig5e_ML_to_AM.csv` | 2 vector | `fig5_extract.py`; `fig5e.py` → `fig5e_replot.png` |
| Fig. 6 | a | image: grid of 20 face images (embedded rasters) | `fig6a_r1_gt_conscious.png` … (20 PNGs) + `fig6a_orig.png` (300-dpi crop of the original) | – | – |
| Fig. 6 | b | plot: line plot | `fig6b.csv`, `fig6b_offaxis.csv` | 2 vector | `fig6_extract.py`; `fig6b.py` → `fig6b_replot.png` |
| Fig. 6 | c | plot: line plot | `fig6c.csv` | 2 vector | `fig6_extract.py`; `fig6c.py` → `fig6c_replot.png` |
| Fig. 6 | d | plot: line plot | `fig6d.csv`, `fig6d_offaxis.csv` | 2 vector | `fig6_extract.py`; `fig6d.py` → `fig6d_replot.png` |
| Fig. 6 | e | plot: line plot | `fig6e.csv` | 2 vector | `fig6_extract.py`; `fig6e.py` → `fig6e_replot.png` |
| Fig. 6 | f | plot: four square scatter plots side by side | `fig6f_all_states.csv`, `fig6f_slope_equalized.csv`, `fig6f_state1.csv`, `fig6f_state2.csv` | 2 vector | `fig6_extract.py`; `fig6f.py` → `fig6f_replot.png` |
| ED Fig. 1 | a | image: coronal T1-weighted MRI slice through the temporal lobe | `edfig1a.png` … (2 PNGs) | – | – |
| ED Fig. 1 | b | image: coronal MRI slice at a more anterior level | `edfig1b.png` … (2 PNGs) | – | – |
| ED Fig. 1 | c | image: coronal MRI slice through the prefrontal cortex, dorsal at the top, | `edfig1c.png` … (2 PNGs) | – | – |
| ED Fig. 1 | d | image: coronal MRI slice through the prefrontal cortex at a level similar to  | `edfig1d.png` … (2 PNGs) | – | – |
| ED Fig. 2 | a | image: grid of 15 face images (embedded rasters) | `edfig2a_r1_gt_conscious.png` … (15 PNGs) + `edfig2a_orig.png` (300-dpi crop of the original) | – | – |
| ED Fig. 2 | b | plot: line plot | `edfig2b.csv` | 2 vector | `edfig2_extract.py`; `edfig2b.py` → `edfig2b_replot.png` |
| ED Fig. 2 | c | plot: line plot | `edfig2c.csv` | 2 vector | `edfig2_extract.py`; `edfig2c.py` → `edfig2c_replot.png` |
| ED Fig. 3 | a | image: grid of 20 face images (embedded rasters) | `edfig3a_r1_gt_conscious.png` … (20 PNGs) + `edfig3a_orig.png` (300-dpi crop of the original) | – | – |
| ED Fig. 3 | b | plot: line plot | `edfig3b.csv` | 2 vector | `edfig3_extract.py`; `edfig3b.py` → `edfig3b_replot.png` |
| ED Fig. 3 | c | plot: line plot | `edfig3c.csv` | 2 vector | `edfig3_extract.py`; `edfig3c.py` → `edfig3c_replot.png` |
| ED Fig. 3 | d | image: grid of 20 face images (embedded rasters) | `edfig3d_r1_gt_conscious.png` … (20 PNGs) + `edfig3d_orig.png` (300-dpi crop of the original) | – | – |
| ED Fig. 3 | e | plot: line plot | `edfig3e.csv` | 2 vector | `edfig3_extract.py`; `edfig3e.py` → `edfig3e_replot.png` |
| ED Fig. 3 | f | plot: line plot | `edfig3f.csv` | 2 vector | `edfig3_extract.py`; `edfig3f.py` → `edfig3f_replot.png` |
| ED Fig. 4 | – | plot: box plot | `edfig4_boxes.csv`, `edfig4_points.csv` | 2 vector | `edfig4_extract.py`; `edfig4.py` → `edfig4_replot.png` |
| ED Fig. 5 | a | image: grid of 20 face images (embedded rasters) | `edfig5a_r1_gt_conscious.png` … (20 PNGs) | – | – |
| ED Fig. 5 | b | plot: line plot | `edfig5b.csv` | 2 vector | `edfig5_extract.py`; `edfig5b.py` → `edfig5b_replot.png` |
| ED Fig. 5 | c | plot: line plot | `edfig5c.csv` | 2 vector | `edfig5_extract.py`; `edfig5c.py` → `edfig5c_replot.png` |
| ED Fig. 5 | d | image: grid of 20 face images (embedded rasters) | `edfig5d_r1_gt_conscious.png` … (20 PNGs) | – | – |
| ED Fig. 5 | e | plot: line plot | `edfig5e.csv` | 2 vector | `edfig5_extract.py`; `edfig5e.py` → `edfig5e_replot.png` |
| ED Fig. 5 | f | plot: line plot | `edfig5f.csv` | 2 vector | `edfig5_extract.py`; `edfig5f.py` → `edfig5f_replot.png` |
| ED Fig. 6 | a | image: grid of 20 face images (embedded rasters) | `edfig6a_r1_gt_conscious.png` … (20 PNGs) | – | – |
| ED Fig. 6 | b | plot: line plot | `edfig6b.csv` | 2 vector | `edfig6_extract.py` (runs `edfig5_extract.py` for page 46); `edfig6b.py` → `edfig6b_replot.png` |
| ED Fig. 6 | c | plot: line plot | `edfig6c.csv` | 2 vector | `edfig6_extract.py` (runs `edfig5_extract.py` for page 46); `edfig6c.py` → `edfig6c_replot.png` |
| ED Fig. 6 | d | plot: three small line plots | `edfig6d.csv` | 2 vector | `edfig6_extract.py` (runs `edfig5_extract.py` for page 46); `edfig6d.py` → `edfig6d_replot.png` |
| ED Fig. 6 | e | plot: paired line plot | `edfig6e.csv` | 2 vector | `edfig6_extract.py` (runs `edfig5_extract.py` for page 46); `edfig6e.py` → `edfig6e_replot.png` |
| ED Fig. 7 | a | image: grid of 20 face images (embedded rasters) | `edfig7a_r1_gt_conscious.png` … (20 PNGs) | – | – |
| ED Fig. 7 | b | plot: line plot | `edfig7b.csv` | 2 vector | `edfig7_extract.py`; `edfig7b.py` → `edfig7b_replot.png` |
| ED Fig. 7 | c | plot: line plot | `edfig7c.csv` | 2 vector | `edfig7_extract.py`; `edfig7c.py` → `edfig7c_replot.png` |
| ED Fig. 7 | d | image: grid of 20 face images (embedded rasters) | `edfig7d_r1_gt_conscious.png` … (20 PNGs) | – | – |
| ED Fig. 7 | e | plot: line plot | `edfig7e.csv` | 2 vector | `edfig7_extract.py`; `edfig7e.py` → `edfig7e_replot.png` |
| ED Fig. 7 | f | plot: line plot | `edfig7f.csv` | 2 vector | `edfig7_extract.py`; `edfig7f.py` → `edfig7f_replot.png` |
| ED Fig. 8 | left | plot: overlaid step histograms | `edfig8_left_state1.csv` | 2 vector | `edfig8_extract.py`; `edfig8_left_state1.py` → `edfig8_left_state1_replot.png` |
| ED Fig. 8 | right | plot: overlaid step histograms | `edfig8_right_state2.csv` | 2 vector | `edfig8_extract.py`; `edfig8_right_state2.py` → `edfig8_right_state2_replot.png` |
| ED Fig. 9 | a | plot: spike raster | `edfig9a_spikes.csv`, `edfig9a_state_epochs.csv` | 2 vector | `edfig9_extract.py`; `edfig9a.py` → `edfig9a_replot.png` |
| ED Fig. 9 | b | image: grid of 20 face images (embedded rasters) | `edfig9b_r1_gt_conscious.png` … (20 PNGs) + `edfig9b_orig.png` (300-dpi crop of the original) | – | – |
| ED Fig. 9 | c | plot: line plot | `edfig9c.csv` | 2 vector | `edfig9_extract.py`; `edfig9c.py` → `edfig9c_replot.png` |
| ED Fig. 9 | d | plot: line plot | `edfig9d.csv` | 2 vector | `edfig9_extract.py`; `edfig9d.py` → `edfig9d_replot.png` |
| ED Fig. 9 | e | plot: three stacked histograms | `edfig9e.csv` | 2 vector | `edfig9_extract.py`; `edfig9e.py` → `edfig9e_replot.png` |
| ED Fig. 9 | f | plot: scatter plot | `edfig9f.csv` | 2 vector | `edfig9_extract.py`; `edfig9f.py` → `edfig9f_replot.png` |
| ED Fig. 9 | g | plot: scatter plot | `edfig9g.csv` | 2 vector | `edfig9_extract.py`; `edfig9g.py` → `edfig9g_replot.png` |
| ED Fig. 9 | h | plot: line plot | `edfig9h_decoding_vs_cells.csv`, `edfig9h_modulation_index.csv` | 2 vector | `edfig9_extract.py`; `edfig9h_decoding_vs_cells.py`, `edfig9h_modulation_index.py` → `edfig9h_decoding_vs_cells_replot.png`, `edfig9h_modulation_index_replot.png` |
| ED Fig. 10 | a | table: check/cross matrix (transcribed in the description) | `edfig10a.csv` | 2 vector | `edfig10_extract.py` |
| ED Fig. 10 | b | plot: grouped bar chart | `edfig10b.csv` | 2 vector | `edfig10_extract.py`; `edfig10b.py` → `edfig10b_replot.png` |
| ED Fig. 10 | c | plot: line plot | `edfig10c.csv` | 2 vector | `edfig10_extract.py`; `edfig10c.py` → `edfig10c_replot.png` |
| ED Fig. 10 | d | plot: grouped bar chart | `edfig10d.csv` | 2 vector | `edfig10_extract.py`; `edfig10d.py` → `edfig10d_replot.png` |
| ED Fig. 10 | e | plot: bar chart | `edfig10e.csv` | 2 vector | `edfig10_extract.py`; `edfig10e.py` → `edfig10e_replot.png` |
| ED Fig. 10 | f | plot: bar chart | `edfig10f.csv` | 2 vector | `edfig10_extract.py`; `edfig10f.py` → `edfig10f_replot.png` |

Panel letters are the paper's; Extended Data Fig. 4 has a single unlettered panel, Extended Data Fig. 8 two
unlettered panels (left/right), and Extended Data Fig. 9 prints two panels labelled "h" (both kept as h).

## Figure notes

Written during the original figure work (one note per figure, by the agent that took the figure apart) and kept
verbatim apart from file paths: the files named below now live flat in `figures/`, `extract_<fig>.py` is now
`<fig>_extract.py`, the redraws are `<panel>_replot.png` (the `.pdf` redraws were dropped), and `<fig>_panels.tex`
(the per-panel alt texts) is replaced by the `\alttext` block of the figure in `main.tex`. "Run from this folder"
means `python3 -I figures/<script>` from anywhere now.

### Figure 1 (PDF page 35, legend on p. 16)

Source: `source/2026.10.15.759299v1.full.pdf`, page 35 (page box 518.8 x 399.6 pt). All coordinates below are PDF
points, origin top-left. Scripts `fig1b.py`, `fig1f.py`, `fig1g.py`, `fig1h.py` are run from this folder and read
only the CSV/PNG files next to them. `fig1_panels.tex` lays the panels out with ALT text.

| Panel | Type | Files | Recovered from |
|---|---|---|---|
| a | schematic (image) | `fig1a.png` (300 dpi), `fig1a_stimulus_priming.png`, `fig1a_stimulus_flashed.png` | render of vector art + text + 2 embedded rasters |
| b | 2 line plots with error bands | `fig1b_left_eye_suppressed.csv`, `fig1b_right_eye_suppressed.csv`, `fig1b.py`, `fig1b_replot.png`, `fig1b_icons.png`, `fig1b_compare.png` | vector paths |
| c | cartoon (image) | `fig1c.png` (1293 x 1217 px, native) | embedded JPEG raster xref 103 |
| d | CAD rendering (image) | `fig1d.png` (469 x 593 px, native) | embedded Flate raster xref 99 |
| e | brain schematic (image) | `fig1e.png` (300 dpi) | render of embedded raster xref 96 (357 x 297 px) + text labels |
| f | 2 heatmaps + colourbar + thumbnails | `fig1f_ML.csv`, `fig1f_AM.csv`, `fig1f_colourbar.csv`, `fig1f.py`, `fig1f_replot.png`, `fig1f_ML_heatmap_raw.png`, `fig1f_AM_heatmap_raw.png`, `fig1f_colourbar.png`, `fig1f_stimuli.png`, `fig1f_compare.png` | embedded rasters, colours inverted through the colourbar |
| g | spike raster | `fig1g_spikes.csv`, `fig1g_layout.csv`, `fig1g.py`, `fig1g_replot.png`, `fig1g_icons.png`, `fig1g_compare.png` | vector paths |
| h | scatter | `fig1h.csv`, `fig1h.py`, `fig1h_replot.png`, `fig1h_compare.png` | vector paths |

#### a - paradigm schematic

300-dpi render of clip (20, 14, 258, 133) (panel letter excluded). The two monkey-face stimuli are embedded
300 x 300 px rasters that are re-used in panels b and g: xref 98 (priming stimulus, shown first to one eye) saved as
`fig1a_stimulus_priming.png`, xref 97 (flashed stimulus) as `fig1a_stimulus_flashed.png`. Boxes, arrow and labels
are vector art / real text. Nothing approximated.

#### b - human psychophysics (plots)

- Axes: tick labels are real text, tick marks are 1-pt strokes. Calibrated on the tick-mark x positions for t = -2, 0,
  2, 4, 6 s (residual 3e-4 s) and tick y positions for 0, 20, ..., 100 % (residual 0). Left subplot axes box
  x 287.4-381.9, y 46.6-119.1; right subplot x 396.3-491.0, y 46.0-118.6.
- Mean curves: 2-pt stroke polylines, 83 vertices each. The first and last vertex (t = -2.001 and 6.001, same y as
  the neighbouring sample) are clip-boundary artefacts and were dropped, leaving exactly 81 samples at 0.1-s steps
  from -2.0 to 6.0 s. Value precision ~0.1 %.
- Error bands: filled polygons of the same colour (alpha in the PDF), 190-197 vertices (upper edge, a run of clipped
  vertices along t = -2, lower edge, a run along t = 6). `band_lo`/`band_hi` = min/max polygon y at each sample time,
  clip runs excluded. Bands are roughly symmetric (+/- 3-5 %) around the mean; the legend does not say whether they
  are SEM or CI.
- Colours: left eye `#d95319`, right eye `#0072bd`, mixed `#edb120` (the legend swatch for "Right eye" is drawn in
  `#2888c7`, the curve itself in `#0072bd`; the CSV/py use the curve colour).
- Dashed vertical line at t = 0.00 s in both subplots. Original limits -2..6 s, 0..100 %.
- The icon strip above the plots (stimulus cartoons + curly brackets) is not data; it is rendered at 300 dpi as
  `fig1b_icons.png` (the right subplot's "100" tick label that intrudes into that strip was painted white).
- Observation (not fixed, just noting): the legend says the priming stimulus appears at t = 0 and the flash at 2 s,
  but the axis is "Time from flash" and the percept flips at t = 0-0.5 s, i.e. the drawn t = 0 is the flash.

#### c, d, e - images

- c: embedded JPEG raster xref 103, 1293 x 1217 px (placed at 88 x 83 pt, ~1055 dpi), saved as-is.
- d: embedded raster xref 99, 469 x 593 px (~594 dpi), saved as-is. No text labels in c or d.
- e: the brain drawing is an embedded raster (xref 96, 357 x 297 px, ~278 dpi at its placed size) with the labels
  ML, AM, PO, PVL as real text on top, so the panel is a 300-dpi render of clip (155, 153, 252, 238) which keeps
  the labels and loses no raster resolution.

#### f - response heatmaps

- The two heatmaps are embedded lossless (Flate, indexed colour) rasters of 251 x 193 px: xref 101 (ML) placed at
  (287.3, 151.1)-(381.1, 223.1), xref 102 (AM) at (396.4, 151.1)-(490.2, 223.1). Raw copies:
  `fig1f_ML_heatmap_raw.png`, `fig1f_AM_heatmap_raw.png`.
- Colour inversion: the colourbar is a 24 x 192 px raster (xref 95, every row one uniform colour, labels "1" at the
  top edge and "-1" at the bottom edge). Each heatmap pixel was mapped to the nearest colourbar row in RGB
  (mean distance 1.1, max 8.7 on a 0-255 scale, so every pixel colour is on the colourbar) and given the value
  `1 - 2*(row + 0.5)/192`. Value resolution therefore 2/192 = 0.0104. The colourmap is a diverging blue-white-
  orange-red map (`fig1f_colourbar.csv` has level, value, r, g, b, hex; `fig1f.py` uses it as the colormap).
- Grid: the 251 columns consist of exactly 96 groups of identical adjacent columns (widths 1,3,3,2,3,3,2,... ,1:
  nearest-neighbour upsampling of 96 stimulus columns), so one value per stimulus was taken. Rows:
  - ML: the 193 pixel rows form exactly 145 groups of identical adjacent rows (heights 1-2) = the 145 cells, so
    `fig1f_ML.csv` is the true 145 x 96 matrix (row = cell in display order, top to bottom; column = stimulus
    left to right, `stim01..stim96`).
  - AM: 215 cells were rendered into 193 pixel rows (no identical adjacent rows), i.e. the image is a
    nearest-neighbour DOWNsampling and about 22 cells are dropped. `fig1f_AM.csv` keeps the 193 pixel rows
    (`pixel_row` 1..193, top to bottom); the 215-cell matrix cannot be recovered from the PDF.
- Stimulus order within the 96 columns is not given anywhere in the PDF beyond the thumbnail strip; the strip
  (`fig1f_stimuli.png`, embedded JPEG 2167 x 365 px, used under both heatmaps) shows six thumbnails under six
  equal 16-column blocks, marked by x tick marks every 16 stimuli: face, body, fruit (grapes), object (camera),
  hand, scrambled pattern. Per-category means in the CSVs: ML 0.47 / 0.08 / 0.13 / 0.05 / -0.02 / -0.02,
  AM 0.42 / 0.13 / 0.14 / 0.13 / 0.09 / 0.08.
- `fig1f.py` reproduces both heatmaps with the paper's colourmap, the colourbar, and places the thumbnail strip
  below each heatmap (the strip is read from `fig1f_stimuli.png`; the script still works without it).
- Curiosity: an invisible, unlabelled axis frame (x 435.8-489.2, y 151.1-223.1, 0.67/1-pt strokes with 6 ticks each
  way) is drawn underneath the AM heatmap image; it is hidden by the image and was ignored.

#### g - spike raster

- 5258 spike ticks. Each tick is a stroke path of one 0.107-pt horizontal segment drawn 2 pt wide (so it appears
  as a 2-pt-tall vertical tick); spike time = segment centre. These paths have zero-height bounding boxes, which
  `fitz.Rect.intersects` treats as non-intersecting, so `pdfplot.drawings(page, clip)` drops them - they were taken
  from the whole-page drawing list and filtered by coordinates instead (same for the 1-pt axis/tick strokes, whose
  bboxes are zero-width).
- x axis: tick marks at -1, -0.5, 0, 0.5, 1 s (real text labels), residual 4e-6 s. Time precision ~0.01 ms; the
  times are not quantised to whole milliseconds.
- Rows: all spike y positions fall on one regular grid, spacing 0.23229 pt, fit residual 0.002 pt. The grid is
  indexed in `row_from_top` with row 1 = the upper y-axis tick mark (278.97 pt). The lower tick mark (374.44 pt) is
  row 412 and is also the last row with spikes; the axis box extends 5 rows further down. The 0.5-pt horizontal
  separator line is at y = 315.55 = row 158.5, so ML = rows 1-158 and AM = rows 159-412 (254 rows). 326 rows
  contain at least one spike (132 ML, 194 AM).
- CAVEAT: the grid has 412 rows between the y ticks while the label says 429 cells; the absolute cell numbering
  cannot be read from the PDF. (For what it is worth, 254 AM rows and 157-158 ML rows match the 254 AM / 157 ML
  selective cells of Fig. 2b, so the raster may show 411-412 cells with the "429" label referring to a different
  count.) Which end of the y axis is cell 1 is also unknown; rows are numbered top-down as displayed.
- `fig1g_layout.csv` holds the layout numbers the script needs (row count, separator row, flash time, limits).
- The icon strip with curly brackets above the raster is rendered as `fig1g_icons.png`.
- Redraw: `|` markers 3.5 pt tall at roughly 2x the original scale; in the compare image the redrawn ticks look
  slightly heavier than the hairline originals, but positions match.

#### h - modulation-index scatter

- 3498 dots, each a filled black circle of 0.87 pt diameter (4 Bezier segments); x, y = circle centre. No two dots
  share a centre. Axes calibrated on the tick marks at -1, 0, 1 on both axes (residuals 7e-5 and 7e-7).
  Precision ~0.001 index units.
- CAVEAT: the legend states n = 5550 cell-stimulus pairs but only 3498 dots exist in the PDF (no duplicates or
  hidden/clipped paths found anywhere on the page). 2052 pairs are therefore not drawn; the CSV contains exactly
  what is plotted.
- Reference lines: dashed identity line from (-1,-1) to (1,1), dashed vertical at x = 0, dashed horizontal at y = 0
  (all drawn as sequences of filled rectangles in the PDF).
- Summary of the recovered data: median x 0.17, median y 0.04; 92 % of dots with x > 0 lie below the identity line.

#### QA

`fig1b_compare.png`, `fig1f_compare.png`, `fig1g_compare.png`, `fig1h_compare.png`: original 300-dpi crop (left)
next to the regenerated PNG (right). All were inspected; curves, bands, dot clouds, heatmap structure, separator
and reference lines match. Cosmetic differences only (fonts, exact marker weights, colourbar rendering).

### Figure 2 (PDF page 36, legend on p. 17)

Source: `source/2026.10.15.759299v1.full.pdf`, page 36 (518.8 x 487.6 pt). Everything was recovered from the PDF's
vector paths (via `../tools/pdfplot.py`), the embedded raster images, or text spans. `fig2_extract.py` (run from this
folder) regenerates all CSVs and PNG extractions; the `fig2X.py` scripts redraw the plot panels from the CSVs only and
write `fig2X_replot.png` (200 dpi). `fig2X_compare.png` = original crop (300 dpi) next to the redraw.
`fig2_panels.tex` lays the panels out with ALT text.

How the figure is built (matters for the caveats below): every panel is a Form XObject; data lines are stroke paths
(one vertex per sample); error bands are filled polygons; **dashed lines are not dashed strokes but one filled outline
polygon per dash** (stroke width 1 pt, butt caps, mitre joins); spikes in the rasters are 2-point strokes with a
zero-width bounding box; tick labels are glyph outlines (values read off the rendered crops and used to calibrate the
axes with `axis_from_ticks`, all residuals < 2e-3).

#### Panels

| panel | type | files | recovery | precision / caveats |
|---|---|---|---|---|
| a | image (schematic) | `fig2a.png` | 300-dpi render of the vector drawing + text (clip 4-126 x 27-98 pt, i.e. without the panel letter) | no data; formula written out in the ALT text |
| b | raster + state shading | `fig2b_spikes.csv`, `fig2b_states.csv`, `fig2b.py`, icons `fig2b_icon_face1/2.png` | 6201 spikes = horizontal 1-ms-wide strokes; rows from a fitted grid (pitch 0.1155 pt, rounding error < 0.01 row); 104 state rectangles | time 1 ms (bin start); rows exact. Row 1 = top. Cell 1 is at the bottom y tick, the thin separator is at 254.5 cells from the bottom: rows 1-157 = ML, 158-411 = AM (matches the legend's 157 + 254). The 1-pt-thick spike marks of the original overlap ~9 rows, so individual rows are not visually resolvable there either |
| c | lines + SD bands | `fig2c.csv`, `fig2c.py` | stroke paths (1 ms) + band polygons | ~0.1 % units; dashed reference lines at t = 0 and 50 % |
| d | lines + SD bands | `fig2d.csv`, `fig2d.py` | strokes, lag 0-200 ms in 1-ms steps (201 points; the strokes' duplicated end sample 0.02 ms after 200 ms is dropped) + bands | ~0.002; the dashed vertical reference line is at lag 67.1 ms (stored in the CSV header comment, read by `fig2d.py`) |
| e | two population rasters | `fig2e_state2_to_state1.csv`, `fig2e_state1_to_state2.csv`, `fig2e.py` | 2456 + 2257 spikes (horizontal 1-ms strokes); row grid fitted (pitch 0.0255 / 0.0288 pt, rounding error < 0.04 row); the axes span N+1 row pitches (rows 1..N inside) | time 1 ms (bin start), rows exact; `cell_prefers` from the solid separator line (row 810 of 2178; row 722 of 1936). Spikes exist in rows 2..N-1 / 2..N only |
| f, g | single-neuron rasters | `fig2f_*.csv`, `fig2g_*.csv`, `fig2fg.py` | vertical ticks (110 + 87 and 50 + 29 spikes), 22 and 17 rows | time to 0.01 ms, rows exact; dashed vertical line at 0 |
| h | image grid | `fig2h_r{1..5}_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png` | 20 embedded grayscale images at native resolution (143x143 or 144x144 px) | named by row (top to bottom) and column as in the figure; column headers transcribed in the tex |
| i | 5 lines | `fig2i.csv`, `fig2i.py` | solid lines: stroke vertices at integer features; dashed lines: dash centre lines (see below) | solid ~0.1 % units; dashed ~0.3 % units (two-sided estimates agree to < 0.2 pt = 0.4 % units; one steep spike up to 3 pt). **Clipping:** the purple solid line (conscious, state 2) and the orange dashed line (suppressed, state 1) go below -100 % at many appearance features; the figure clips them at -100 %. Those vertices are EMPTY in the CSV with `*_clipped = 1` (15 and 21 features); `fig2i.py` draws them at -100 % so the redraw looks like the original. 6 of the 21 orange-dashed flags are inferred (no dash visible, both neighbours clipped) |
| j | 5 lines + SD bands | `fig2j.csv`, `fig2j.py` | solid lines: stroke vertices; bands: polygon crossings at integer n (handles the clipped edges); dashed lines: band midpoint where the band is unclipped (the band is symmetric about its line: checked on the solid series, max deviation 0.007 % units), else dash centre lines (agree with the midpoints to 0.01 % units) | ~0.05 % units. Bands are clipped at 0 and 100 %; where a band polygon is cut away entirely (the two series at 0 %) the `sd_*` cells are empty. Where the orange dashed line runs along the 0 % axis (half the stroke clipped) its value is 0 by construction (neighbours at 0) |
| k | 3 time courses | `fig2k.csv`, `fig2k.py` | solid lines: stroke vertices on a 10-ms grid from -0.1 to 2.0 s (211 points; the stroke's duplicated end sample at +0.2 ms is dropped); dashed lines: least-squares fit of the polyline to each dash outline (vertex spacing 0.21 pt is too fine for the edge-pairing method) | solid ~0.3 % units; dashed ~0.3-0.5 % units but **only where a dash is drawn**: 180/175/194 of 211 time points recovered, the rest (inside gaps between dashes) are empty, so `fig2k.py` draws the suppressed series as pieces, which reproduces the dashed look. The paper's axis title says "Time from flash (ms)" although the ticks 0, 1, 2 are seconds; the CSV column is `time_s` |
| l | paired lines + markers | `fig2l.csv`, `fig2l.py` | thin solid strokes (10 sessions, conscious), thin dashed outlines (10 sessions, suppressed), thick mean lines, circle-marker centres | ~0.2 % units (thin dashed ~0.5). Sessions are numbered by drawing order within each condition; which solid and which dashed line belong to the same session is not encoded in the PDF (same order is likely, not verifiable). Marker centres and thick-line vertices agree to 0.01 |

##### Dashed-line recovery

Each dash is a closed outline polygon (5 points per straight dash, more at joints, with self-intersections at inner
corners). Two methods are used:

* **centre lines (i, j, l):** the two long sides of a straight dash piece are antiparallel edges exactly 1 stroke width
  apart; the mid-line between them is the centre line (after `figures/edfig9_extract.py`). Pieces are assigned
  to the polyline segment containing their midpoint; the pieces of a segment define its line, evaluated at the two
  vertices; a vertex takes the mean of the estimates from its two adjacent segments. Vertices that fall inside a gap
  are still determined by the directions of the dashes on both sides. The disagreement between the two sides is
  printed by `fig2_extract.py` (i: 0.17 pt purple, up to 3 pt at one steep spike of the orange dashed; j, l: 0.02 pt).
* **least squares (k):** polyline with known vertex x fitted so that all outline sample points lie at distance 0.5 pt
  (robust loss), one dash at a time; residual rms 0.12 pt.

##### Things not recovered / approximated

* True values of the clipped vertices in panel i (below -100 %): left empty, flagged.
* Time points inside the gaps of the dashed series in panel k: left empty.
* The pairing of conscious and suppressed session lines in panel l (see above).
* The two face icons above panel b are 27x27 px embedded images, placed by `fig2b.py` at the positions of the original
  (-0.58 s; 0.44 s and 0.56 s). The grey rounded icon boxes and the period brackets are redrawn, not extracted.
* Panel a is an image render; the raster, dice and state strip inside it are drawings, not data.

##### Validation

* Axis calibrations: residuals < 2e-3 everywhere (x of i: 1.6e-3 is the largest).
* Rasters: all spike rows fall on the fitted grid (max rounding error 0.006 row in b, 0.03 in e, 0.000 in f/g); all
  bin starts are integer ms (error < 0.05 ms in b, 0.001 ms elsewhere).
* j: band midpoints equal the solid lines (max 0.007 % units); dash centre lines equal the band midpoints of the dashed
  lines (max 0.01 % units) where both exist.
* l: marker centres equal the thick-line vertices (0.01 % units).
* Overlays of the recovered polylines on the 300-dpi crops were inspected for i, j, k, l (dashed series) during
  extraction; the `*_compare.png` images show the final redraws next to the originals.

#### Corrections 2026-10-18 (../tools/dashlines.py)
The dashed series of i, j and l were re-extracted with `../tools/dashlines.py` (`dashed_series`; j's bands with
`band_extent` + `check_band_symmetry`) and compared with the CSVs; a value was replaced only where it differs by more
than 0.05 % units (these files carry no per-value se) and an independent check supports the new value (vertex point
present in the outline, or pattern gap end-cap -> vertex -> start-cap = 4.000 pt). `fig2i.csv` ends with a `#` line
listing its corrections.
* **i**: the old centre-line fit has ~0.3 % precision; dashlines reads vertices inside a dash exactly. Changed
  (exact vertex reads unless marked 'pattern'): suppressed state 1 features 20 (2.15 -> 2.25, pattern),
  40 (-52.07 -> -51.82), 48 (-94.4 -> -94.34); state 2 features 20 (2.5 -> 2.56), 31 (31.28 -> 31.21, pattern),
  38 (69.52 -> 69.6), 39 (66.0 -> 66.49, pattern), 40 (14.01 -> 13.93), 43 (35.08 -> 35.21, pattern),
  44 (58.41 -> 58.47), 48 (44.96 -> 45.03), 49 (72.5 -> 72.34). Largest change 0.49 % (state 2, feature 39).
  Not changed: differences <= 0.05 % (most vertices); 'anchor' reads (state 1 features 10, 29; state 2 feature 50;
  0.06 %, see `the Extended Data Fig. 5 notes` for why these are not trusted); non-pattern segment fits whose difference is
  within 2 se (state 1 feature 31, state 2 features 32, 41; 0.09-0.27 %). Clipped vertices stay empty (dashlines
  extrapolates 9 of the 21 to -127 ... -199 % with se 0.2-2.6 %; not stored, per this file's convention).
* **j**: checked, not changed. The stored dashed values are band midpoints where the band is unclipped; dashlines
  agrees with them to < 0.36 % and its own values there are weaker (gap interpolations, se 0.2-0.4). Band edges from
  `band_extent` agree with the stored sd columns to < 0.05 %. Face 2 of suppressed state 1 (24.01; dashlines anchor
  read 24.34, dash-side slope estimate 24.3 +- 0.5, no band): not decisive, kept.
* **l**: checked, not changed (all 33 suppressed values agree with dashlines.py to <= 0.02 %).
* `fig2i_replot.png` and `fig2i_compare.png` regenerated.

### Figure 3 (PDF page 37, legend on p. 18)

Hesse et al. 2026, *Rapid alternation of conscious and suppressed stimulus representations in the primate brain*,
bioRxiv 10.64898/2026.10.15.759299v1. Page 37 is a figure-sized page (518.8 x 416.8 pt); every panel is a Form
XObject built from vector paths (MATLAB figure passed through Illustrator), except panel e, which is 20 embedded JPEGs.

#### Files

| file | what |
|---|---|
| `fig3_extract.py` | recovers all data from the PDF (vector paths, embedded images) and writes the CSVs and panel-e PNGs |
| `fig3_common.py` | colours, CSV reader and helpers shared by the redraw scripts |
| `fig3<p>.py` | standalone redraw of panel p from its CSV(s) only; writes `fig3<p>.pdf` + `fig3<p>.png` (200 dpi). Run from inside this folder |
| `fig3_qa.py` | renders each original panel at 300 dpi and writes `fig3<p>_compare.png` (original left, redraw right; panel e: montage of the extracted images) |
| `fig3_panels.tex` | LaTeX layout of the panels with ALT text |

Every CSV starts with `#` comment lines giving provenance, the tick values used to calibrate each axis, the
calibration residual and the caveats. Coordinates in the comments are PDF points (origin top-left).

#### How the PDF is built (what mattered here)

* Axes and tick marks are 0.5-pt filled rectangles; numeric tick labels are glyph outlines, so tick values were
  read off rendered crops and axes calibrated with `pdfplot.axis_from_ticks` (max residuals 1e-3 or better,
  mostly ~1e-5).
* **Dashed lines are not dashed strokes.** They are exported as *filled polygons, one per dash* (the outline of a
  1-pt stroke, with joins). I recover the centre line from pairs of anti-parallel polygon edges one line-width
  apart (the two sides of the same piece of the stroke), requiring the same perpendicular offset at both ends of
  the overlap (so consecutive steep segments of a spike are not confused with each other) and excluding butt-cap
  edges (length = width, perpendicular to their two neighbours). Each recovered piece is extrapolated to the data
  vertices at both ends of the grid interval it lies in; several pieces give independent estimates of a vertex,
  combined by inverse-variance weights (sigma = extrapolation length x 0.0015 pt / overlap length) and the spread
  between them is reported. Validation: in panel i the mean of the ten recovered suppressed session values is
  29.60 / 13.45 / 37.13, the recovered thick dashed mean line is 29.60 / 13.45 / 37.14 and the open-circle markers
  are at 29.60 / 13.45 / 37.13; in panel g the dashed lines agree with the midpoints of their (symmetric) error
  bands to 0.05 % on average (max 0.8 %). Vertices that fall in a gap between dashes have no coverage: flagged
  (`gap`: linear interpolation; in g replaced by the band midpoint where the band is unclipped, `band_midpoint`).
* `pdfplot.drawings(page, clip)` originally dropped every path whose bounding rect has zero height or width (all
  the horizontal spike marks of panel b, the vertical ticks of c/d), because `fitz.Rect.intersects` is False for
  empty rects. `fig3_extract.py` therefore takes the unclipped drawing list and filters by rect centre itself. The
  toolkit has since been fixed by the coordinator; the extraction was re-run afterwards with identical counts.

#### Panels

##### a: box plot (CSV + code)
`fig3a_box.csv` (whisker min, q1, median, q3, whisker max) and `fig3a_points.csv` (19 session points, sorted by
value; `x_jitter_pt` is the horizontal jitter in the original). Box geometry from the box rectangle, the median
stroke and the whisker-cap strokes; points are the circle centres (diameter 2.24 pt). y axis calibrated from the
five ticks 0..0.8 (residual 6e-8). Precision ~0.002. Values: min 0.008, q1 0.047, median 0.162, q3 0.409, max
0.765; all 19 points > 0. The dashed reference line maps to 0.0000. Sessions are not identifiable from the figure.

##### b: population rasters (CSV + code)
`fig3b_state2_to_state1.csv` (1196 rows, 1207 spikes) and `fig3b_state1_to_state2.csv` (988 rows, 1007 spikes),
one CSV row per spike (`row_index`, `time_ms`), plus `fig3b_meta.csv` (rows per raster, position of the solid
separator line: row 368 / 304, cells above prefer the conscious face). Each spike is a 0.3-pt-thick horizontal
stroke 0.43 pt (0.18 ms) long whose left end sits exactly on an integer millisecond (100 distinct x positions), so
spike times are binned at 1 ms; `time_ms` is that integer (-50..49). Rows: the y axis spans rows 0..n+1 (MATLAB
ylim); the pitch (0.046 / 0.056 pt) is ~45 x the coordinate precision and every spike lands within 0.014 of an
integer row, so row indices are exact. x axis from the three ticks -50, 0, 50 (residual 1e-5). Row 1 is the top
row. Not recoverable: which cell/transition a row is (only the sort order is in the figure).

##### c, d: example-cell rasters (CSV + code)
`fig3c_*.csv`, `fig3d_*.csv`: one row per spike; `row_index` (1 = top) from the two y ticks (rows 1 and n;
residual 0), `time_ms` = x of the 0.14-pt vertical tick (unbinned, precision ~0.02 ms). Spike counts 95 / 100
(c) and 57 / 35 (d). The y axes carry two tick marks but no numeric labels in the original (the redraw matches).

##### e: face images (image files)
`fig3e_r<1-5>_<gt_conscious|recon_state1|gt_suppressed|recon_state2>.png`: the 20 embedded JPEGs at native
resolution (143 x 143 px, three of the ground-truth-suppressed ones 144 x 144), placed 51.5 pt wide in the
figure. Grey-scale faces on a mid-grey background. Rows are numbered top to bottom, columns left to right.
Laid out as a 5 x 4 `tabular` in the tex snippet with the column headers of the original.

##### f: explained variance (CSV + code)
`fig3f.csv`: feature 1..50 (`feature_type` shape for 1-20, appearance for 21-50 per the Fig. 2i legend; the
brackets in the figure span features 1.0-19.7 and 20.2-50.1) and five series. Solid lines are stroke paths with
one vertex per feature (exact; the exported paths end with a 0.01-pt tail segment that was dropped). Dashed
lines recovered from dash polygons as described above: orange dashed 49/50 vertices from dashes, purple dashed
46/50 (`gap` at features 35 and 38 = interpolated; `none` at 1 and 50 = the line starts/ends inside a gap, value
left empty). Max spread between independent estimates of one vertex: orange 2.7 %, purple 0.3 % (weighted sigma
< 0.02 %). **Clipping:** the figure clips the orange dashed line at the -100 axis limit at feature 25 (the
exported line is split into two fragments there, with the clipped vertex projected onto -100); the CSV leaves that
value empty with `clipped_at_axis_min` (true value <= -100); the redraw draws it at -100 like the original.
Axes: x from ticks 10..50 (residual 1.6e-3 features), y from ticks -100..100 (residual 7e-4 %).

##### g: decoding accuracy vs number of faces (CSV + code)
`fig3g.csv`: faces 1..60; for each of the five series the line value, the band's lower/upper edge and a
`_band_clip` flag; `_recovery` for the two dashed series. Solid lines are 60-vertex strokes (exact). Bands are
filled polygons (alpha 0.2); their edges were read by intersecting the polygon with a vertical line at each
integer x, so where the band is clipped to the 0..100 axes the edge value is the axis limit and the flag says
`lo`/`hi` (at 1 face every series is exactly 100 with a zero-width band, also flagged `hi`). The bands are
symmetric about their lines (solid lines = band midpoint to 0.00 %); the legend does not say whether they are SD
or SEM. Dashed lines: orange 56/60 vertices from dashes, 3 `gap` (band clipped at 0, so interpolated), 1 `none`
(face 60, beyond the last dash; the band there is 0..0.11 so the value is about 0.1); purple 54/60 from dashes
and 6 `band_midpoint`. Axes from ticks 0,20,40,60 and 0..100 (residuals 0 and 3e-4).

##### h: single-trial decoding time courses (CSV + code)
`fig3h_average.csv`, `fig3h_state1.csv`, `fig3h_state2.csv`: 211 samples at 10-ms steps from -0.1 to 2.0 s.
`conscious_pct` is the solid stroke (exact, ~0.2 % precision). `suppressed_pct` is the dashed line: values only
where a dash covers the sample (146 / 145 / 156 of 211), empty in the gaps between dashes (invisible in the figure,
not recoverable; the redraw plots the series with those gaps, which reproduces the dashed look). Because the
samples are only 0.2 pt apart and the stroke is 1 pt wide, the dash outlines overlap themselves; the column
`suppressed_estimate_spread_pct` gives the disagreement between independent estimates of a sample (typically
< 0.5 %, max 0.8 % in Average and State 1; two samples in State 2 near 1.55-1.6 s have spreads of 2.4 and
6.2 % and are uncertain by about that much). **Axis label:** the figure says "Time from flash (ms)" but the
range 0-2 with a 200-ms sliding window is seconds (Fig. 2c says "seconds"); the CSV column is
`time_from_flash_s`, the redraw keeps the printed label.

##### i: paired session plot (CSV + code)
`fig3i.csv`: 10 sessions x 2 conditions, the thick mean lines, the large marker centres and (as a check) the
mean of the session rows. Thin solid lines are 3-vertex strokes (exact); the thin dashed lines (0.10-pt-wide dash
quads) and the thick dashed mean line were recovered from the dash polygons (max spread 0.11 %). The figure does
not link a session's conscious line to its suppressed line: `session_k` is the k-th line in PDF path order within
each condition (probably, but not verifiably, the same order for both conditions). y axis from ticks 0..100
(residual 3e-4).

#### QA
`fig3<p>_compare.png` for a, b, c, d, f, g, h, i (original crop at 300 dpi | redraw) and `fig3e_compare.png`
(original crop | montage of the 20 extracted images) were inspected; the redraws match the originals in shape,
colours, line styles, axis ranges and legends. Fonts: Liberation Sans in place of Arial.

### Figure 4 (PDF page 38, legend on p. 19)

Source: `source/2026.10.15.759299v1.full.pdf`, page 38 (page box 518.76 x 362.88 pt, not US letter). All coordinates
below are PDF points, origin top-left. Everything was extracted with `../tools/pdfplot.py` by `fig4_extract.py` (kept
here for provenance; re-running it regenerates every CSV and the raw PNGs). The `fig4<p>.py` scripts read only the CSVs
and write `fig4<p>.pdf` + `fig4<p>.png`; `fig4<p>_compare.png` shows the original crop (left) next to the redraw.

Hex colours in the CSVs are written as `rrggbb` without `#`, because `pandas.read_csv(comment="#")` would otherwise
truncate the row.

#### Colour scale shared by a and b (`fig4_colourbar.csv`, `fig4_colourbar_raw.png`)

The colourbar is an embedded 13 x 89 px image (xref 250, FlateDecode): a linear ramp from pure red (255,0,0) in the top
row (label "6") through white in the middle row to pure blue (0,0,255) in the bottom row (label "-3"). White is thus at
z = 1.5, the midpoint of the colour axis, not at 0. Colours are inverted with z = 1.5 + 4.5 (R - B)/255, which is linear
along the whole ramp (and, for blended pixels, returns the mean z of the blend). Caveats: the "6"/"-3" labels are text
spans centred about 1 pt inside the image ends; that offset is within the label-placement jitter seen on the other axes
of this figure, so the colour axis is taken to be exactly [-3, 6]; the 89-row colourbar vs the continuous model differ
by at most 0.10 z-units depending on which row-to-value convention one assumes. Treat colour-derived values as +/- 0.1.

#### a -- four scatter plots + inset (plot panel; `fig4a.csv`, `fig4a_inset.csv`; `fig4a.py`)

- Vector paths. Each subplot has exactly 1500 filled circles (2.24 pt), i.e. all points are recovered (6000 rows).
  Axes calibrated on the tick marks at -1 and 1 (the only ticks; residual ~1e-16). Position precision ~0.0005 axis
  units. `draw_order` is the order of the markers in the content stream (probably the stimulus index, unverified).
- `response_zscored` is the marker colour inverted through the colourbar (see above). Marker colours are quantised in
  steps of 2/255 (~0.035 z-units). 147 (state 1) / 101 (state 2) points per face are pure red = saturated at >= 6
  (`colour_saturated = high`); no point reaches pure blue. 648 points share the colour #6a6aff (z = -1.13), presumably
  the floor value for stimuli with zero spikes. Note the two faces in the same state have identical colour sets (same
  cell responses, the dots are just placed by different face features).
- Inset: 6 bins per series from the stroke vertices; error bars from the vertical error-bar strokes (the legend does not
  say whether they are s.e.m. or s.d.). Axes: ticks -1/1 (x) and 0/9 (y), residual 0. The y axis is just "Response".
- Check: correlation between x and z is 0.48 (conscious, state 1) and 0.38 (suppressed, state 2) versus 0.11 and -0.05
  for the other two subplots, matching the visible ramps.

#### b -- four population heatmaps (`fig4b_<state>_<face>.csv`, `fig4b_<state>_<face>_raw.png`; `fig4b_raw.py`, `fig4b.py`)

- The heatmaps are embedded raster images (xrefs 248, 246, 247, 249), **169 x 169 px each, JPEG (DCTDecode) RGB**, placed
  in 61.0 x 61.0 pt boxes. The panel states 554 cells x 1500 stimuli, so the image is a ~3.3 x 8.9-fold downsampled
  version of the data; the original matrix cannot be recovered. The pixel grid is kept: each CSV is a 169 x 169 matrix
  (rows = cells top to bottom as displayed, columns = stimuli left to right), values rounded to 0.01.
- `get_image_rects` reports a second placement of every image directly below the visible one; it lies outside the Form
  XObject clip and is invisible (the gap between the panels renders pure white), so the visible panel is the whole image
  (orientation checked against a high-resolution render: unflipped orientation matches, flips do not).
- Per-pixel values are the colour inversion z = 1.5 + 4.5 (R - B)/255. Because of downsampling and JPEG chroma
  subsampling, most pixels are blends of red and blue (purple-ish) that lie far from the colourbar ramp (only 0.7 % of
  pixels are within 4/255 of the ramp, 48 % within 40/255). The R - B functional gives the mean z of the blended
  cells/stimuli (plus a 2 x 2 chroma smoothing from JPEG); it cannot reproduce the individual saturated values. Hence
  `fig4b_replot.png` (redrawn from the CSVs) is much paler than the original (`fig4b_compare.png`: original | raw composite |
  CSV redraw). Values are indicative only (+/- 0.5 or worse for individual pixels; row/column means are more reliable).
- For the LaTeX snippet the faithful image is used: `fig4b_raw_replot.png`, composed pixel-for-pixel from the four extracted
  rasters with the original labels and colour bar by `fig4b_raw.py` (reads the raw PNGs, not the PDF).
- Pattern check from the CSVs: in conscious/state 1 the mean z of the left third of columns is 0.78 vs 1.90 in the right
  third (0.43 vs 2.24 in the top 30 rows); suppressed/state 2: 1.02 vs 1.99; the other two panels 1.70 vs 1.87 and
  1.59 vs 2.01.

#### c -- three stacked gain histograms (plot panel; `fig4c.csv`; `fig4c.py`)

- Vector paths. Each series is a translucent fill (opacity 0.30, one rectangle per bar) plus an opaque stair outline.
  Bin edges and counts come from the bar rectangles; x axis calibrated on ticks 0 and 2 (residual 4e-16), each subplot's
  y axis on its ticks 0 and 100 (residual 0). All measured counts are within 0.006 of an integer, so the counts are exact.
- MATLAB merged adjacent bars of equal height into single rectangles; these were split into bins of the series' bin
  width (0.2 for state1_conscious, state1_suppressed, state2_suppressed; 0.1 for state2_conscious). The first/last bins
  are clipped by the axis limits (-0.5, 2.5): their drawn rectangle is narrower than a bin and the outer edge is inferred
  (`bin_clipped_at_axis = 1`; `drawn_rect_lo/hi` give the rectangle actually drawn). Empty bins are not drawn and are
  absent from the CSV.
- Totals: state1_suppressed 543 and state2_conscious 543 (= n in the legend), state1_conscious 534, state2_suppressed
  540: the missing 9 / 3 cells presumably have gains beyond the plotted range (> 2.6) and are not drawn.
- Subplot y limits (top of the axis line): 204 (subplot 1), 136 (subplots 2 and 3). Legend colours: #fcae34, #ffd28a,
  #b56cc7, #543379 (from the swatch strokes).

#### d -- gain scatter (plot panel; `fig4d.csv`; `fig4d.py`)

- 531 filled 0.5-pt circles (vector paths); the legend says n = 543 cells, so 12 cells are not drawn (presumably outside
  the -0.5..2.5 range, culled on export; cannot be recovered). Axes on ticks 0/2 (residual 0); precision ~0.001.
- Reference lines: dashed identity from (-0.5, -0.5) to (2.46, 2.46), dashed x = 0 and y = 0 (dash paths; positions
  within 0.002 of 0). Check: Pearson r of the 531 dots = 0.901 (legend: 0.90).

#### e -- mean-response scatter (plot panel; `fig4e.csv`; `fig4e.py`)

- 531 filled 0.5-pt circles (12 of 543 cells not drawn, as in d). Axes on ticks 0/3 (residual ~1e-15); precision ~0.001.
  Dashed identity line from (0, 0) to (2.96, 2.96). r = 0.95 from the dots.

#### f -- decoding accuracy vs number of cells (plot panel; `fig4f.csv`; `fig4f.py`)

- Mean line: black 1-pt stroke with 24 vertices at n = 1..10, 20..100 (step 10), 200..500 (step 100), 1000. Band:
  black fill at opacity 0.2, envelope sampled at the same 24 x values. Axes: ticks 0/1000 (residual 5e-13) and 0/50/100
  (residual 0). Dashed chance line measured at 49.9 (= 50 %, dash thickness). Precision ~0.05 percentage points.

#### g -- modulation-index scatters (plot panel; `fig4g.csv`; `fig4g.py`)

- 0.72-pt filled circles. all_states, state1 and state2 each have exactly 2885 dots (= n in the legend);
  slope_equalized has only 1612 drawn dots (1273 missing, presumably outside the -1..1 range after slope equalisation,
  culled on export; cannot be recovered). Axes on ticks -1/0/1 (residual < 4e-7); precision ~0.001.
- Reference lines: dashed x = 0, y = 0 and a diagonal from (-1, -1) to (0.97, 0.97) (identity) in all_states, state1
  and slope_equalized, and from (-1, 1) to (0.97, -0.97) (anti-identity) in state2.
- Check: Pearson r from the recovered dots: all_states 0.454, state1 0.656, state2 -0.443 (legend: 0.45, 0.66, -0.44);
  slope_equalized 0.055 vs -0.02 in the legend, consistent with 44 % of its dots not being drawn.

#### Not recovered / approximate

- b: the 554 x 1500 matrices (only a 169 x 169 JPEG exists in the PDF); per-pixel values are approximate mean-z blends.
- d, e: 12 of 543 cells; g slope-equalized: 1273 of 2885 pairs; c: 9 / 3 cells beyond the plotted gain range.
- a: z for the 147 + 101 pure-red points is >= 6 (true value unknown); colour-derived z carries +/- 0.1 systematic
  uncertainty from the colourbar convention.
- a inset: error-bar type (s.e.m. or s.d.) not stated in the legend; the "Response" axis has no unit.

### Figure 5 (PDF page 39, legend on p. 20)

Everything here was produced by `fig5_extract.py` (reads the PDF, writes the CSVs, the original crops
`fig5*_orig.png`, the panel-a render and the panel-b raster) and the redraw scripts `fig5b.py` ... `fig5e.py`
(read only their CSVs, write `fig5<p>.pdf` + `fig5<p>.png` at 200 dpi). `fig5<p>_compare.png` = original
crop (300 dpi) next to the redraw. `fig5_panels.tex` is the layout snippet with the ALT texts.
Page 39 is a cropped page (289 x 482 pt), not US letter; all coordinates below are PDF points on that page.

Colours (read from the paths): state 1 orange `#fcae34`, state 2 purple `#543379`, panel-c black line `#000000`,
panel-e "priming" line `#1c0f29`.

#### a -- HMM schematic (image panel)

`fig5a.png`: 300-dpi render of the clip (0.5, 30.4, 157.0, 152.0) pt (vector art + text; the bold panel letter is
excluded). Nothing to recover as data. Note: the transition diagram contains the labels "S1" and "S2" as white
text between the orange and purple rows, invisible on the white background; the ALT text describes the rows by
colour instead.

#### b -- state partition heatmap (plot panel, embedded raster)

- The heatmap is an embedded raster image (xref 269), **249 x 266 px**, placed at x 171.68..261.41 pt,
  y 27.36..123.21 pt. That is a ~200-dpi rasterisation of the plot area, **not** the trial x time-bin matrix:
  with ~849 trial rows and 2.05 s of time it is ~3.2 trials per pixel row and ~8.2 ms per pixel column, and
  pixels at row/column boundaries are colour mixtures. `fig5b_raster.png` is the raster at native resolution.
- `fig5b_state1_fraction.csv`: 266 rows x 249 columns; value = projection of the pixel colour onto the
  purple-to-orange colour axis (0 = pure purple/state 2, 1 = pure orange/state 1). Every pixel lies on that
  axis (max off-axis residual 1.0/255), so the values are a faithful "fraction of state 1" per pixel.
  `fig5b_state.csv`: the same thresholded at 0.5 to 1 (state 1) / 2 (state 2).
- Axis calibration. Header row = time (s) of each pixel-column centre, from the 5 tick marks on the bottom
  frame at -1, -0.5, 0, 0.5, 1 s (resid 7e-6); the image spans -1.0165..1.0335 s (slightly asymmetric,
  presumably half-bin padding of the original time bins). First column = estimated trial index of each
  pixel-row centre from the 8 tick marks on the left frame. Those ticks carry no visible labels; the PDF
  contains invisible outline-glyph labels next to them whose path item counts (49, 62, 70, 54, 62, 68, 51, 73)
  match "100", "200", ..., "800" with the digit outlines used elsewhere on the page (0 = 20 items, 1 = 9,
  2 = 22, 5 = 22, 8 = 33, ...), so the ticks are taken as trials 100..800 (resid 0.017 trials). With that, the
  image spans trials 0.5..849.5, i.e. the session has about 849 trials although the axis label says
  "800 trials". The same kind of hidden labels under the x axis read "-1000", "-500", "0", "500", "1000"
  (ms), consistent with the visible -1, 0, 1 s labels.
- Visible summary: 7 % of pixels before the flash are state 1, 47 % after; a thin orange strip occupies the
  first ~2 pixel columns (t < -1.0 s) in ~40 % of rows.
- Redraw: `fig5b.py` shows the fraction matrix with a purple-to-orange colormap, extent from the calibrated axes.

#### c -- fit accuracy and median dwell time vs bin size (plot panel)

- `fig5c.csv`, 8 rows (bins 2, 3, 5, 10, 20, 50, 75, 100 ms -- the 75 ms point has no tick; 49.99 and 75.0 come out
  of the log calibration). Means = vertices of the 1-pt stroke paths (the circle markers sit on the vertices to
  0.002 pt); s.e.m. bands = filled polygons (upper edge then lower edge), sampled at the vertex x positions.
- x: log10 axis calibrated on all 18 tick marks (2..9, 10..90, 100), max residual 7.8e-5 log10 units.
  Top y: ticks 0.6/0.8/1.0, resid 1e-6; bottom y: 0/100/200 ms, resid 0. Precision ~0.001 (top) and ~0.1 ms (bottom).
- Caveat: the bottom axis ends at 200 ms. The state-1 mean at 100 ms is exactly on the axis limit (200.0) and the
  upper edges of both s.e.m. bands at 100 ms are clipped at 200 (the orange band polygon has an extra clipping
  vertex at x = 97 ms). So `median_dwell_state1_ms` at 100 ms should be read as ">= 200" and the two `_sem_hi`
  values at 100 ms as ">= 200".

#### d -- fit accuracy vs median dwell time (plot panel)

- `fig5d.csv`, 6 rows at the dwell-time bin centres 15, 35, 60, 85, 150, 250 ms (x of the stroke vertices after
  calibration on the ticks 0..250, resid 2e-5). y calibrated on ticks 0.5..1.0 (resid 2e-6); precision ~0.001.
- Means from the stroke vertices (markers coincide to 0.000 pt), bands from the polygons as in c.
- The two states have identical mean and band at the first bin (0.594, 0.529..0.660) in the PDF.

#### e -- explained variance vs feature, ML -> AM and AM -> ML (plot panel)

- `fig5e_ML_to_AM.csv`, `fig5e_AM_to_ML.csv`: 50 rows (feature 1..50) x 5 series, in percent.
- Solid series (priming average, conscious state 1, conscious state 2): stroke paths with 51 vertices; the 51st
  lies 0.01 pt right of the 50th (an export artefact) and was dropped. x calibrated on ticks 10..50 (resid
  1.6e-3 features), y on ticks -100..100 (resid 7e-4 %); precision ~0.05 %.
- Dashed series (suppressed state 1, suppressed state 2) are **not strokes** in the PDF: each is one filled path
  of 35-61 dash polygons. Each dash polygon is a chain of 1-pt-wide rectangles (one piece per polyline segment
  it covers), traced as a single outline in which the junction between two pieces is an explicit point equal to
  the data vertex. The centre line was reconstructed as follows: (1) rectangle pieces = pairs of antiparallel
  outline edges 1 pt apart; the midpoints of their ends lie on the centre line; all pieces on one segment
  (between consecutive feature x positions) are fitted with one straight line, evaluated at the two bounding
  vertices (this also recovers vertices that fall in a gap between dashes); (2) outline points whose x equals a
  vertex x and that agree with that line within 0.3 pt are taken as the exact vertex (22-30 of the 50 vertices
  per series). Junction points agree with the fitted lines to <= 0.035 pt. The least-squares uncertainty
  (assuming 0.01 pt corner rounding) is <= 0.04 pt (<= 0.07 %) for every vertex except one: AM -> ML,
  suppressed state 1, feature 43, where both adjacent segments are gaps and the value (-34.5 %) comes from two
  sub-0.4-pt stubs at the neighbouring junctions (s.d. 0.095 pt = 0.17 %).
- The legend's dashed sample line in the PDF has width 0.75 pt and dash pattern (2.25, 0.75); the plotted dashes
  are 1 pt wide with ~4 pt dashes; the redraw uses matplotlib dashes (3, 1).

#### QA

`fig5b_compare.png`, `fig5c_compare.png`, `fig5d_compare.png`, `fig5e_compare.png` were inspected; redraws
match the originals in shape, levels, colours, line styles, axis ranges, ticks, titles and legend layout.
Cosmetic differences only (fonts, marker size, band alpha).

#### Not recovered / approximations

- b: only the ~200-dpi rasterised pixel grid exists in the PDF, not the per-trial, per-bin state matrix
  (see above). Trial indices are derived from hidden tick labels; the "800 trials" label is approximate.
- c: state-1 median dwell time at 100 ms and both s.e.m. upper edges at 100 ms are clipped at the 200 ms limit.
- e: dashed series are reconstructed geometrically (uncertainty quoted above); one vertex has 0.17 % s.d.

### Figure 6 (PDF page 40, legend on p. 20)

Source: `source/2026.10.15.759299v1.full.pdf`, page 40 (page box 518.76 x 425.28 pt, not US letter).
All data were recovered from the PDF's vector paths and embedded images with `../tools/pdfplot.py`; the
extraction script is `fig6_extract.py` in this folder (`python3 fig6_extract.py all` regenerates the CSVs,
the face images and the `*_orig.png` crops). Redraw scripts read only their CSVs.

Legend note: the prompt guessed that d/e show a second prefrontal region; the legend says a-c pool patches
PO and PVL and d/e repeat b/c with the held-out half of neurons (as Fig. 3f/g). Files are named accordingly.

Series naming and colours (from the legend/paths): `priming_average` black `#1c0f29` solid;
`binocular_conscious_state1` orange `#fcae34` solid; `binocular_conscious_state2` purple `#543379` solid;
`binocular_suppressed_state1` orange dashed; `binocular_suppressed_state2` purple dashed.

#### How the dashed lines were recovered (b, c, d, e)

The solid lines are ordinary stroke polylines (one vertex per x value). The dashed lines were exported as
**filled dash polygons** (every dash a 1-pt-wide quad, dashes split at polyline vertices, with extra
outline vertices at the joins). `fig6_extract.dash_pieces` pairs antiparallel polygon edges 1 pt apart and
takes the midpoints of corresponding corners as centre-line pieces; `fit_polyline` then fits the 50 (or 60)
vertex values by weighted least squares, using that the line is straight between consecutive x values
(each piece gives two equations), rejecting pieces whose perpendicular residual exceeds 0.03 pt (spurious
cap-to-cap pairings; 0-6 per series). Precision is propagated from 0.005 pt coordinate rounding and is
typically 0.01-0.2 % (worst for steep segments).

Validation: in c and e every shaded band is exactly symmetric about its line (band midpoint minus fitted
line: max 0.007 pt = 0.008 %, for solid and dashed series alike), so the dashed-line fits are confirmed
independently of the dash geometry. In f the recovered points reproduce the legend's Pearson r (see below).

#### Panels

##### a (image grid): `fig6a_r{1-5}_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png`
20 embedded grayscale rasters extracted at native resolution (143 x 143 px; the `gt_suppressed`
images of rows 1, 3, 4 and 5 are 144 x 144). Rows = 5 example stimulus pairs; columns = ground-truth conscious
face, reconstruction from state-1 activity, ground-truth suppressed face, reconstruction from state-2
activity. The column headers are text in the original ("State 1" in orange, "State 2" in purple); they are
typeset in the tex snippet (uncoloured). Nothing approximated.

##### b (line plot): `fig6b.csv`, `fig6b_offaxis.csv`, `fig6b.py` -> `fig6b_replot.png`
Explained variance (%) vs feature index 1-50 (shape 1-20, appearance 21-50), 5 series.
- x axis: tick marks at 10..50 (residual 0.002 features); feature 1 sits on the y-axis line. y axis: ticks
  -100..100 (residual 0.0007 %). Precision ~0.01 % (solid), 0.01-0.2 % (dashed).
- **Clipping**: `binocular_conscious_state2` (purple solid) and `binocular_suppressed_state1` (orange
  dashed) dive below -100 % at many appearance features; the original clips them at the axes. The main CSV
  leaves those cells empty (36/50 and 25/50 values visible). `fig6b_offaxis.csv` lists, for each clipped
  feature, the value **extrapolated from the straight line segment(s) that enter the clipped region**
  (least-squares fit; precision 0.05-1.5 %), so the redraw leaves the axes at the correct slope; these are
  not drawn data points. 2 + 18 features are unrecoverable (both neighbouring segments fully below -100 %).
- The "Shape"/"Appearance" brackets above the axes are redrawn as plain brackets.
- Legend: the original has one legend for b-e between the rows; each redraw carries its own legend (b/d in
  the empty lower-left corner, c/e upper right).

##### c (line plot with bands): `fig6c.csv`, `fig6c.py` -> `fig6c_replot.png`
Decoding accuracy (%) vs number of faces 1-60 (60 vertices per series), 5 lines + 5 shaded bands.
- x axis: ticks 0, 20, 40, 60 (residual 0); y axis: ticks 0..100 (residual 0.0003 %).
- Columns per series: `<series>_pct`, `<series>_band_lo_pct`, `<series>_band_hi_pct`. The legend does not
  say what the band is (presumably SEM across the 30 stimulus pairs). Bands are clipped at 0 % (lower
  edges of the two near-zero series at 28 and 47 x positions; recorded as 0.00) and at 100 % (upper edges at
  x = 2 for the two high series; recorded as 100.00). Where the band polygon has no vertex at all (purple
  solid band at 30 and 35-60 faces: line at 0 % with zero width, clipped away entirely), band cells are empty.
- **Dash gaps**: with a 4-on/4-off dash pattern and 1.575 pt per face, some vertices of the dashed lines fall
  inside a gap with no dash in either adjacent segment. 8 + 1 such vertices were filled from the band
  midpoint (bands are symmetric about the line; listed in the CSV comments). 7 vertices of
  `binocular_suppressed_state1` (faces 11, 16, 21, 26, 31, 36, 52) are empty: gap plus band clipped at 0
  (the line is within 0-2 % there). `fig6c.py` interpolates linearly across empty cells for drawing only.
- The ordering of the five curves and their values are in the ALT text; e.g. at 60 faces: priming 5.0 %,
  conscious state 1 6.7 %, suppressed state 2 10.0 %, conscious state 2 0.0 %, suppressed state 1 0.0 %.

##### d (line plot): `fig6d.csv`, `fig6d_offaxis.csv`, `fig6d.py` -> `fig6d_replot.png`
Same type as b, held-out half of neurons. Nothing leaves the axes; all 50 x 5 values recovered.
Feature 8 of `binocular_suppressed_state2` sits in a dash gap and was recovered from short dash fragments
(0.2-0.55 pt) only; `fig6d_offaxis.csv` is empty apart from its header. Precision 0.01-0.1 %.

##### e (line plot with bands): `fig6e.csv`, `fig6e.py` -> `fig6e_replot.png`
Same type as c, held-out half of neurons. 9 + 9 dash-gap vertices filled from band midpoints; one vertex
(`binocular_suppressed_state1`, 11 faces, about 6 %) empty (gap plus clipped band), interpolated for drawing.
Band upper edges clipped at 100 % at x = 2; lower edges clipped at 0 % for several series.

##### f (four scatter plots): `fig6f_{all_states,state1,state2,slope_equalized}.csv`, `fig6f.py` -> `fig6f_replot.png`
Modulation index binocular vs unambiguous, one row per marker (filled circle, 0.72 pt diameter), x and y in
index units, precision ~0.0002 (axes calibrated from the -1/0/1 tick marks, residual < 1e-6).
- All states, State 1, State 2: exactly **283 markers each**, matching the legend's n = 283. Pearson r of the
  recovered points: 0.555, 0.629, -0.316 (legend: 0.56, 0.63, -0.32). The three panels share the same 283 x
  values (unambiguous index), as expected.
- Slope-equalized ("gain-equalized" in the legend): only **126 markers** are drawn inside the axes; the
  other 157 cell-stimulus pairs have no marker in the PDF, so they must lie outside the +/-1 range and were
  clipped by the plotting software (the x values present are a subset of the 283). r of the 126 visible
  points is 0.143 vs 0.24 in the legend. Not recoverable from the figure.
- Reference lines: dashed x = 0, y = 0 in all panels; dashed identity line y = x in All states, State 1 and
  Slope-equalized, but **y = -x** in State 2 (read from the dash coordinates).
- Overlapping markers are listed individually; no de-duplication.

#### QA
`fig6{b,c,d,e,f}_compare.png`: 300-dpi crop of the original (left/top) next to the redraw (right/bottom);
all were inspected. `fig6a_orig.png`, `fig6legend_orig.png` and `fig6f_*_orig.png` are the original crops.

#### Known limitations
- b: 20 feature values of the two diving series are below -100 % and unrecoverable; the extrapolated
  off-axis values are inferred, not drawn data.
- c/e: 8 dashed-line vertices unrecoverable (dash gap + clipped band), all within 0-6 %.
- f, slope-equalized: 157 of 283 points are not in the PDF.
- The shaded-band statistic (SEM vs. SD vs. CI) is not stated in the legend.

### Extended Data Figure 1 (PDF page 41, legend on p. 20)

Four image panels, no plots. Everything here comes from `edfig1_extract.py` (run it to regenerate).

| panel | file used in the tex | raw raster | what it is |
|---|---|---|---|
| a | `edfig1a.png` (372 x 376 px, 300-dpi render of clip x 17-106, y 19-109 pt) | `edfig1a_mri_native.png` (235 x 236 px, xref 298) | coronal slice, ML (temporal lobe) |
| b | `edfig1b.png` (371 x 376 px, clip x 144-233) | `edfig1b_mri_native.png` (235 x 236 px, xref 299) | coronal slice, AM (anterior temporal lobe) |
| c | `edfig1c.png` (376 x 376 px, clip x 273-363) | `edfig1c_mri_native.png` (238 x 236 px, xref 301) | coronal slice, PO (prefrontal) |
| d | `edfig1d.png` (376 x 376 px, clip x 401-491) | `edfig1d_mri_native.png` (237 x 236 px, xref 300) | coronal slice, PVL (prefrontal) |

- Each panel is **one embedded raster** (235-238 x 236 px placed in ~85 x 85 pt, i.e. 200 dpi) in which the
  grey anatomy **and the coloured fMRI overlay are already baked in**; the activation map cannot be separated from
  the anatomy. On top of it the PDF has vector/text annotations: a white 1 cm scale bar (filled rect 2.26 pt wide),
  a white arrowhead (filled triangle), the patch label (real text, Arial 6 pt, white) and the colourbar (a
  second embedded raster, 10 x 31 px, xref 297, placed 4 times, mirrored horizontally) with its labels
  (real text, Cambria Math, white).
- The tex uses the 300-dpi render of the full panel clip so that scale bar, arrow, label and colourbar are
  shown; this is a 1.5x upsample of the 200-dpi raster. Use `*_mri_native.png` for the unresampled pixels.
  The panel letters a-d (bold 8 pt text at y = 23.4 pt, left of each image) are excluded from the clips; the
  tex snippet adds them.
- `edfig1_colourbar_native.png`: the colourbar image (10 x 31 px, vertical gradient). Mean RGB per row,
  top to bottom: row 0 (251,255,128) pale yellow -> row 3 (248,206,0) yellow -> row 7 (244,137,8) orange ->
  row 12 (246,24,0) red -> row 18 (208,25,22) -> row 24 (151,54,54) -> row 30 (112,97,96) dark greyish red.
  Transcribed labels (text spans next to each bar, top label at the top of the bar, bottom label at the bottom):
  - a (ML) and b (AM): top `10^-10`, bottom `10^-3`, italic `p` between them -> yellow = p = 1e-10, dark red = p = 1e-3.
  - c (PO) and d (PVL): top `10^-5`, bottom `10^-2`, italic `p` -> yellow = p = 1e-5, dark red = p = 1e-2.
  The paper does not say whether the mapping between the two labels is log-linear; only the end points are given.
- Scale bars ("1 cm", white text to the right of the bar). Measured lengths from the rect geometry:
  a 12.76 pt, b 14.17 pt, c 20.09 pt, d 20.09 pt. With the image widths (a 84.62, b 84.62, c 85.94, d 85.41 pt)
  the slices are about 6.6 cm (a), 6.0 cm (b), 4.3 cm (c), 4.3 cm (d) across, i.e. ~0.28, 0.25, 0.18, 0.18 mm
  per native pixel. Panels a and b are therefore shown at a lower magnification than c and d, and a and b are not
  at identical scales either.
- Arrowheads / targets (page coordinates in pt; fractions of the image width/height from the left/top):
  a: ML, arrow apex (96.66, 74.29) pointing up, label "ML" below at (96.6, 84.3); 0.92 / 0.62.
  b: AM, apex (213.07, 93.06) pointing up, label "AM" at (213.1, 103.1); 0.79 / 0.84.
  c: PO, apex (335.79, 79.99) pointing up, label "PO" at (335.6, 92.0); 0.71 / 0.68.
  d: PVL, apex (473.24, 84.12) pointing right, label "PVL" to the left at (459.8, 84.3); 0.82 / 0.73.
- Content description (by eye, from the renders): a: yellow blob at the right lateral IT surface above the ML
  arrow, smaller orange spot at the mirrored left position. b: yellow-orange blob at the right ventral anterior
  temporal surface above the AM arrow, larger bright-yellow blob at the left ventral surface, one small blue spot
  (opposite sign of the contrast) on the right lateral surface. c: small orange spot above the PO arrow on the
  ventral prefrontal surface plus a few small orange spots elsewhere (ventral midline, far left edge, lower
  right edge). d: orange spot at the right lateral prefrontal surface at the PVL arrow tip, small spots near the
  centre and lower left; bright vertical midline streak. Hemisphere labelling (left/right) is as displayed,
  radiological vs neurological convention is not stated in the paper.
- Nothing had to be approximated; no data CSV applies (image panels).

### Extended Data Figure 2 (PDF page 42, legend on p. 21)

Legend title: "Weak reconstructions from average responses". Three panels: (a) face grid, (b) explained
variance vs feature #, (c) decoding accuracy vs number of faces. Everything here was recovered from the PDF
with `edfig2_extract.py` (uses `edfig_extract_lib.py`, which sits in this folder and, as an identical copy, in
`../edfig3/`; both build on `../../tools/pdfplot.py`). Re-run with `python3 edfig2_extract.py`, then
`python3 edfig2b.py` and `python3 edfig2c.py` for the redraws.

#### Files

| file | what |
|---|---|
| `edfig2a_r{1-5}_{gt_conscious,recon_average,gt_suppressed}.png` | panel a, one embedded raster per cell |
| `edfig2b.csv`, `edfig2b.py`, `edfig2b_replot.png` | panel b data, redraw script, redrawn panel |
| `edfig2c.csv`, `edfig2c.py`, `edfig2c_replot.png` | panel c data, redraw script, redrawn panel |
| `edfig2_panels.tex` | layout snippet with ALT text (`\includegraphics[...,alt={...}]`, needs graphicx >= 2021) |
| `edfig2{a,b,c}_orig.png` | 300-dpi renders of the original panels (QA) |
| `edfig2{b,c}_compare.png` | original (left) next to the redraw (right) |
| `edfig2{b,c}_overlay.png` | QA: original at 600 dpi with the recovered dashed polylines (red; green circles = `direct`, blue = other codes) and band edges (magenta = lower, cyan = upper) drawn on top |
| `edfig2_extract.py`, `edfig_extract_lib.py` | extraction code |

#### Panel a -- face grid (image panel)

* 5 rows x 3 visible columns (ground truth conscious, reconstruction from average activity, ground truth
  suppressed). Each cell is one embedded RGB raster, extracted at native resolution: 143 x 143 px (the
  ground-truth suppressed faces of rows 1, 3, 4, 5 are 144 x 144 px), placed 51.5 pt (52.0 pt) wide on the
  page. The images are grayscale content stored as RGB.
* The ground-truth faces are the very same image objects (same PDF xrefs) as in Extended Data Fig. 3a/d, so
  the stimulus pairs are identical across these figures.
* Caveat: the page actually contains a **fourth image column** (x = 225.8-277.3 pt, xrefs 328, 330, 332,
  334, 336) that is clipped away by the form XObject's clip rectangle and is not visible in the rendered
  figure. Its images differ from both the reconstruction column (mean |diff| 13-14 grey levels) and the
  suppressed faces (20-28); presumably a leftover of the 4-column template of Fig. 2h / ED Fig. 3. They were
  not extracted because they are not part of the figure as published.

#### Panel b -- explained variance vs feature # (plot: `edfig2b.csv` + `edfig2b.py`)

* Axes: x from the five tick marks (10...50; linear fit residual 1.6e-3 pt), y from the five tick marks
  (-100...100; residual 1.4e-3 pt). 1 pt = 1.80 %. All series have exactly one vertex per feature 1..50 (the
  solid strokes' x coordinates sit on that grid to < 0.01 pt).
* `priming_average` (black solid, #1c0f29) and `binocular_conscious_average` (grey solid, #808080): stroke
  path vertices; precision ~0.01 pt = 0.02 %.
* `priming_average_predicting_flashed` (black dashed) and `binocular_suppressed_average` (grey dashed): the
  PDF does **not** contain dashed strokes; the dashed lines were expanded into filled dash outlines (every
  dash a closed polygon, 1 pt wide, 4 pt dash / 4 pt gap, miter joins or bevel+foot joins at the polyline
  vertices). The centreline was rebuilt from those polygons: inside a dash the two long outline edges of a
  polyline segment are anti-parallel and exactly 1 pt apart, so their midline is the data line; pieces are
  assigned to the segment of the known x grid that contains them, one straight line is fitted per segment
  and evaluated at its two end vertices; join point pairs (symmetric about the vertex) are used as exact
  anchors. Quality code per value in the `*_qc` columns:
  * `direct` -- vertex inside a dash (precision ~0.02 pt = 0.04 %); `extrap` -- vertex in a dash gap,
    extrapolated along the adjacent straight segment (~0.01-0.4 pt); `interp` -- both adjacent segments
    fall inside one 4-pt gap, linear interpolation of the neighbours (geometric bound +/-1.2 pt = 2.2 %);
    `extrap_offscale` -- the line leaves the -100..100 box there; the value is the straight-line
    extrapolation of the visible part of that segment (precision ~1-2 pt, i.e. a few %); `clipped` -- the
    line is below -100 % and not drawn (empty); `gap` -- no dash coverage (empty).
  * The method was validated on the decoding panels (here and in ED Fig. 3), where the shaded band is exactly
    symmetric about the line: dash-recovered `direct`/`extrap` values agreed with the band midpoints to
    <= 0.02 pt over ~230 vertices, `interp` values to <= 1.05 pt.
  * Grey dashed: 39 `direct`, 11 `extrap` (features 6, 10, 18, 20, 27, 31, 35, 37, 40, 45, 47); complete.
  * Black dashed: 20 `direct`, 3 `extrap`; features 21, 23, 25, 39 are `extrap_offscale` (-269, -265,
    -246, -249 %: the line dives below the axis there and only the visible parts of the steep segments
    determine them); 21 features are `clipped` (22, 26-38, 44-50: below -100 %, unknown); features 42 and 43
    are `gap` (right after the spike at 40-41 the line is at -99 % and leaves the box inside a dash gap, so
    these two values cannot be pinned down; they are certainly at or below about -100 %).
* The "Shape" (1-20) / "Appearance" (21-50) brackets above the axes are reproduced; the legend below the
  panel lists all four series (in the original a single legend sits below panels b and c).
* Legend swatches in the original use slightly different greys/blacks (#7f7f7f, #1f122c) than the data
  lines (#808080, #1c0f29); the redraw uses the data-line colours.

#### Panel c -- decoding accuracy vs number of faces (plot: `edfig2c.csv` + `edfig2c.py`)

* Axes: x from tick marks 0, 20, 40, 60 (residual 7e-6 pt), y from 0...100 (residual 7e-4 pt); 1 pt =
  0.90 %. One vertex per n_faces = 1..60 for every series.
* Solid lines: stroke vertices (~0.01 pt). Shaded bands: one filled polygon per series (upper edge then
  lower edge, alpha 0.2), columns `*_lo` / `*_hi`. The legend does not say what the band is (the related
  main-figure panels use SD); it is exactly symmetric about the line (band midpoint = line to 0.005 pt for
  the solid lines). Bands are clipped by the axes box: `priming_average_hi` = 100 for n = 1-9 (true value
  above 100), the black dashed line's band has its lower edge clipped at 0 for n = 2-8 and is absent for
  n >= 10 (entirely at the 0 boundary; written as lo = hi = line); all bands collapse to zero height at
  n = 1 and n = 60 (written as lo = hi = line). The CSV header comments list these cases.
* Dashed lines: wherever the band is unclipped its midpoint gives the line to ~0.01 pt (`band_mid`), which
  is what the CSV holds for the grey dashed line (58 of 60 values; n = 1 `direct`, n = 60 `band` = value of
  the collapsed band). The black dashed line has no usable band (it is on the 0 boundary from n = 9 on), so
  its values come from the dash recovery: 36 `direct`, 13 `extrap`, 8 `interp` (n = 10, 25, ..., 55, all 0),
  3 `band` (n = 19, 20, 60: the band lies entirely at the 0 boundary, so the line is at 0). It is 0.00 from
  n = 9 onward.

#### Known limitations

* Band statistic unknown (see above); values beyond the axis range are unknown except where noted.
* Fonts/line widths of the redraws approximate the original (DejaVu Sans vs Arial).

### Extended Data Figure 3 (PDF page 43, legend on p. 21)

Legend title: "Interleaved representations in individual monkeys". Left half monkey A (a: face grid, b:
explained variance, c: decoding accuracy), right half monkey M (d, e, f: same). Everything was recovered from
the PDF with `edfig3_extract.py` (uses `edfig_extract_lib.py`, identical copy of the one in `../edfig2/`,
built on `../../tools/pdfplot.py`). Re-run with `python3 edfig3_extract.py`, then `python3 edfig3{b,c,e,f}.py`.

#### Files

| file | what |
|---|---|
| `edfig3a_r{1-5}_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png` | panel a (monkey A), one embedded raster per cell |
| `edfig3d_r{1-5}_...png` | panel d (monkey M), same naming |
| `edfig3{b,c,e,f}.csv`, `.py`, `_replot.png` | plot data, redraw scripts, redrawn panels |
| `edfig3_panels.tex` | layout snippet with ALT text (`alt={...}` needs graphicx >= 2021; the coloured "State 1/2" column headers use xcolor if it is loaded, plain text otherwise) |
| `edfig3{a,d,b,c,e,f}_orig.png` | 300-dpi renders of the original panels (QA) |
| `edfig3{b,c,e,f}_compare.png` | original (left) next to the redraw (right) |
| `edfig3{b,c,e,f}_overlay.png` | QA: original at 600 dpi with recovered dashed polylines (red; green = `direct`, blue = other) and band edges (magenta lower, cyan upper) |
| `edfig3_extract.py`, `edfig_extract_lib.py` | extraction code |

#### Panels a, d -- face grids (image panels)

* 5 rows x 4 columns each (ground truth conscious, reconstruction state 1, ground truth suppressed,
  reconstruction state 2). Each cell is an embedded RGB raster (grayscale content) extracted at native
  resolution: 143 x 143 px, the ground-truth suppressed faces of rows 1, 3, 4, 5 are 144 x 144 px; placed
  51.5 / 52.0 pt wide.
* The ground-truth faces are the same image objects (same xrefs) in panel a, panel d and ED Fig. 2a.
* Caveat for panel d (monkey M): every cell carries **three stacked image placements** (one image from an
  earlier form XObject, then another image drawn twice on top, all at the same position +/-0.1 pt). The
  visible one was chosen by rendering each cell and comparing with the candidates (mean |diff| 2.6-5.2
  grey levels for the match vs 7.0-20 for the hidden one; the same comparison gives 2-5 for the
  unambiguous monkey-A cells). Result: the ground-truth columns show the shared faces (xrefs 184, 176,
  180, 182, 177 / 185, 179, 181, 183, 178), the reconstruction columns show xrefs 352-370; the hidden
  reconstructions (xrefs 371-380) and hidden ground-truth variants (351, 355, 359, 363, 367, 353, 357, 361,
  365, 369) differ from the visible ones and were not extracted (not part of the figure as published).

#### Panels b, e -- explained variance vs feature # (plots: `edfig3b.csv`/`edfig3b.py`, `edfig3e.csv`/`edfig3e.py`)

* Axes from the tick marks (x: 10...50, y: -100...100; linear residuals <= 1.6e-3 pt); 1 pt = 1.80 %. One
  vertex per feature 1..50 for every series (solid strokes on the grid to < 0.01 pt).
* Solid lines (stroke vertices, ~0.01 pt = 0.02 %): `priming_average` black #1c0f29,
  `binocular_conscious_state1` orange #fcae34, `binocular_conscious_state2` purple #543379. (The legend
  swatch for state 2 is drawn in a lighter purple, #6d429c; the redraw uses the data-line colour.)
* Dashed lines `binocular_suppressed_state1` (orange dashed) and `binocular_suppressed_state2` (purple
  dashed) are stored as filled dash outlines (4 pt dash / 4 pt gap, 1 pt wide), not as dashed strokes. The
  centreline was rebuilt from the dash polygons (anti-parallel outline edges 1 pt apart -> midline; one line
  fitted per polyline segment of the known x grid; join point pairs as exact anchors). `*_qc` codes:
  `direct` (vertex inside a dash, ~0.02 pt), `extrap` (vertex in a gap, extrapolated along the adjacent
  straight segment, ~0.01-0.4 pt), `interp` (both adjacent segments inside one gap: linear interpolation,
  bound +/-1.2 pt = 2.2 %), `extrap_offscale` (line leaves the -100..100 box; straight-line extrapolation of
  the visible part of that segment, ~1-2 pt). Validation: on the decoding panels (c, f and ED Fig. 2c), where
  the shaded band is exactly symmetric about the line, dash-recovered `direct`/`extrap` values agreed with
  the band midpoints to <= 0.02 pt over ~230 vertices and `interp` values to <= 1.05 pt.
  * b, state 1: 43 `direct`, 7 `extrap`. b, state 2: 36 `direct`, 13 `extrap`, 1 `interp` (feature 19).
  * e, state 1: 43 `direct`, 6 `extrap`, 1 `extrap_offscale` (feature 23 = -108.8 %, the line touches the
    bottom of the axis there). e, state 2: 36 `direct`, 14 `extrap`. No missing values.

#### Panels c, f -- decoding accuracy vs number of faces (plots: `edfig3c.csv`/`edfig3c.py`, `edfig3f.csv`/`edfig3f.py`)

* Axes from tick marks (x: 0, 20, 40, 60; y: 0...100; residuals <= 7e-4 pt); 1 pt = 0.90 %. One vertex per
  n_faces = 1..60 for every series.
* Solid lines: stroke vertices (~0.01 pt). Bands: one filled polygon per series (alpha 0.2), `*_lo`/`*_hi`;
  the legend does not say what statistic the band is (the related main-figure panels use SD). Bands are
  clipped by the axes box; clipped edges are written as the clip value (0 or 100) and listed per series in
  the CSV header comments (e.g. in c the upper edge of the priming band is clipped at 100 for n = 1-6 and the
  lower edge of the conscious-state-2 band at 0 for 44 of the 60 values, listed in the CSV header); every band collapses to zero height at n = 1
  and n = 60 (lo = hi = line).
* Dashed lines: the band midpoint (exactly symmetric about the line) gives the value to ~0.01 pt wherever
  both band edges are unclipped (`band_mid`: c state 1 49 values, c state 2 57, f state 1 58, f state 2 58);
  the remaining values come from the dash recovery (`direct`, `extrap` -- in c, state 1, n = 7, 10, 11, 15,
  60 are `extrap` because its band is clipped at 0 there). No missing values.

#### Known limitations

* Band statistic unknown (see above).
* Fonts/line widths of the redraws approximate the original (DejaVu Sans vs Arial); the single shared legend
  of the original is repeated under each redrawn panel.

### Extended Data Figure 4 (PDF page 44, legend on p. 21)

One plot panel (no panel letter in the original). Files:

- `edfig4_boxes.csv` -- one row per condition: whisker min, Q1, median, Q3, whisker max (percent explained
  variance), colour and opacities, box width.
- `edfig4_points.csv` -- one row per session point (9 per condition, 45 rows): `x_position` (category index
  plus the original horizontal jitter, in category units) and `explained_variance_pct`.
- `edfig4.py` -- redraws the panel from the two CSVs -> `edfig4_replot.png` (200 dpi).
- `edfig4_orig.png` -- 300-dpi crop of the original; `edfig4_compare.png` -- original | redraw, checked by eye.
- `edfig4_extract.py` -- the extraction (needs the PDF and `../tools/pdfplot.py`).

How the data were recovered (all from vector paths, nothing read by eye except the tick values):

- y axis: the eight 0.5-pt tick rectangles at x = 35-42 pt, paired with the values -60, -40, ..., 80 read off
  the render (tick labels are glyph outlines, not text). Linear fit residual 0.002 %. The dotted zero line
  (556 tiny black rects, opacity 0.70) maps to 0.000 %, confirming the calibration.
- x axis: categorical; the five tick marks at 74.62, 128.16, 181.70, 235.24, 288.78 pt (spacing 53.54 pt) are
  the category centres; the text labels are real text spans. Box width is 0.6 category units.
- Boxes: single filled rectangles (Q1-Q3); medians: 1-pt horizontal strokes across the box; whiskers: 1-pt vertical
  strokes above and below the box. Points: filled circles, 2.83 pt diameter, with the original jitter.
- Colours: Priming black (box opacity 0.50); Conscious State 1 `#fcae34` (box 0.50, lines/points 1.0);
  Suppressed State 1 `#fcae34` at reduced opacity (box 0.18, lines/points 0.35; this is the "light orange");
  Conscious State 2 `#543379` at reduced opacity (box 0.18, lines/points 0.35; the "light purple");
  Suppressed State 2 `#543379` (box 0.50, lines/points 1.0). The redraw uses the same colours and alphas.
- Consistency checks: whisker ends coincide with the extreme points (range, as the legend says); the box
  edges match MATLAB `prctile` quartiles ((k-0.5)/n interpolation) computed from the 9 recovered points, and the
  median line is the 5th point, in every condition. So boxes and points are mutually consistent.

Precision: PDF coordinates are exact to ~0.01 pt, i.e. ~0.013 % on the y axis; values are rounded to 0.01 %.
Not recoverable: which point is which session (points are unlabelled; the CSV orders them by value within a
condition), and whether the same session is at the same rank across conditions.

### Extended Data Figure 5 (PDF page 45, legend on p. 21)

Legend: "Interleaved representations using leave-one-neuron-out cross-validation and high-confidence time
points." Left half (a-c) = leave-one-neuron-out cross-validation, right half (d-f) = analysis restricted to the
50 % most confidently assigned time points; conventions as Fig. 3e-g.

Files: `edfig5_panels.tex` (layout + ALT text), `edfig5a_*.png` / `edfig5d_*.png` (face grids),
`edfig5{b,c,e,f}.csv` + `.py` (+ `.pdf`/`.png` output and `_compare.png` QA images).

#### Panels

##### a, d -- face-image grids (image panels)
* Type: 5 rows x 4 columns of embedded raster images (143x143 px, four of them 144x144; RGB PNG, grayscale
  content), extracted at native resolution with `pdfplot.extract_image`. Files
  `edfig5a_r<1-5>_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png`, same for `edfig5d`.
* The ground-truth images are the same PDF objects in a and d (and in Fig. 2h/3e/EDF6a: xrefs 184/176/180/182/177
  conscious, 185/179/181/183/178 suppressed); only the reconstructions differ (a: xrefs 432/424/426/428/430 and
  423/425/427/429/431; d: 413/415/417/419/421 and 414/416/418/420/422). Row/column assignment comes from the image
  placement bboxes; column headers are real text in the PDF ("Ground truth / Conscious", "Reconstruction / State 1"
  in orange #fcae34, "Ground truth / Suppressed", "Reconstruction / State 2" in purple #6d429c).
* Nothing approximated.

##### b, e -- explained variance of features vs feature index (plots)
* Type: line plot, 5 series, x = feature 1..50, y = -100..100 %; "Shape"/"Appearance" brackets above the plot
  (curly-bracket strokes spanning features 1.02-19.69 and 20.24-50.11 in axis units; the redraw draws them as
  square brackets at the same x positions).
* Axes: tick marks are 0.5-pt filled rectangles; calibrated with `axis_from_ticks` on x = 10,20,30,40,50 (residual
  1.6e-3 pt) and y = -100,-50,0,50,100 (residual 7e-4 pt). 1 % = 0.555 pt.
* Solid lines (priming average #1c0f29, conscious state 1 #fcae34, conscious state 2 #543379): 50-point stroke
  paths, one vertex per feature, read directly. Precision = PDF coordinate precision (~0.02 pt = 0.04 %).
* Dashed lines (suppressed state 1/2): in this PDF dashed lines are **not** dashed strokes but filled polygons,
  one per dash, each being the outline of a 1-pt-wide stroked piece of the polyline. Recovery (scratch module
  `dashgeo.py`, described in the CSV header): where a dash spans a polyline vertex the outline contains the vertex
  point itself (the outer join is drawn offset -> vertex -> offset, two edges of exactly 0.5 pt), so those values
  are exact ("vertex" in the CSV header counts). Vertices that fall in a dash gap were solved from (i) the
  adjacent segments' centre lines (fitted to exact centre-line points: known vertices, cap midpoints, midlines of
  antiparallel outline edges) and (ii) the dash-pattern constraint: the path length from the end of one dash to the
  start of the next is a constant 4.000 pt (measured on all vertex-free gaps, spread 0.003 pt), which pins the
  vertex on the line x = x_i. Each recovered value carries an estimated uncertainty column `*_se_pct`
  (% units). Values with se > 3 % are left empty. Result: b: all 100 dashed values recovered, max se 2.0 % (one
  spike vertex, feature 37 of suppressed state 1; 3 values with se > 1 %), typically 0.02-0.1 %; e: 97/100
  recovered, max se 2.5 %.
* e, suppressed state 1: the original line is clipped at the -100 % axis limit for 12 of the features 21-50
  (features 21, 23, 25, 26, 30, 34, 38, 39, 42, 44, 46, 47; the dash polygons are cut at y = -100). The CSV
  reports the extrapolation of the visible straight segments to the vertex (values below -100, e.g. -140 % at
  feature 23, with their se, 9 of them with se > 1 %) and leaves 3 vertices empty where the extrapolation was too
  uncertain (features 22, 32, 49). The redraw clips at -100 like the original.
* The dashed values were checked by overlaying the recovered polyline on the 300-dpi crop (every dash is
  followed) and the full redraw is compared in `edfig5b_compare.png` / `edfig5e_compare.png`.
* Values in the CSV are rounded to 0.01 %.

##### c, f -- decoding accuracy vs number of faces (plots with shaded bands)
* Type: 5 lines (same series/colours as b) with a translucent band (fill opacity 0.2, same colour) around each;
  x = 1..60 faces, y = 0..100 %.
* Axes: x ticks 0,20,40,60 (residual 2e-6 pt), y ticks 0..100 step 20 (residual 1.3e-3 pt); 1 % = 1.11 pt.
* Solid lines: 60-point strokes, exact. Dashed lines: recovered as in b; in the flat part near 0 % the 4-pt dash
  gap covers up to three consecutive faces, so a few values are empty (c: faces 29, 34, 60 of suppressed state 1
  and 27, 55, 60 of state 2; f: face 37 of state 1 and 35, 60 of state 2). Max se 1.2 % (face 1, where all lines
  start at 100 %), typically < 0.1 %.
* Bands: single filled polygons (upper edge forward, lower edge back). Extent at each integer face obtained by
  slicing the polygon vertically (necessary because where the band is clipped at 100 % or 0 % the clipped edge has
  no vertex at integer x). Validation: every band is symmetric about its line (mean |band midpoint - line| <= 0.02 %
  over unclipped faces), which also fixes the assignment of the two same-colour bands to the solid vs dashed
  line. Clipped edges are reported as 100 / 0. The band of suppressed state 1 is clipped at 0 % from face 3 on and
  disappears entirely beyond face 46 (c) / 32 (f) where it lies wholly below 0 (empty in the CSV, not drawn, as in
  the original). All bands shrink to zero width at face 60 (as drawn).
* The legend does not say whether the band is SD or SEM (across the 30 stimulus pairs); column names say
  `_band_lo_pct` / `_band_hi_pct`.

#### Shared legend
The original has one legend under panels b and c (line samples: solid #1f122c, #fcae34, #6d429c; dashed
#fcae34, #6d429c with pattern [2.25 0.75] at 0.75 pt). The redraws of b and e include this legend below the plot;
c and f have none (as in the original). Data colours in the plots are #1c0f29 / #fcae34 / #543379.

#### Not recovered / caveats
* 3 (e) + 6 (c) + 3 (f) dashed values empty (listed above); nothing else missing.
* Dashed values in gaps are reconstructions from the dash geometry, not direct reads; their `se` columns are
  estimates (coordinate precision assumed 0.02 pt, pattern-gap spread 0.003 pt), not formal confidence intervals.
* Feature numbering 1-50 follows the x-axis ticks (tick 10 = feature 10); the bracket boundary sits at x ~= 20.

#### Corrections 2026-10-18 (../tools/dashlines.py)
The dashed series were re-extracted with the consolidated tool `../tools/dashlines.py` (`dashed_series`; bands with
`band_extent`, validated with `check_band_symmetry`) and compared with the CSVs. `dashgeo.py` had applied the
dash-pattern constraint at spike vertices whose adjacent dashes overlap in x, and next to polygons cut by the -100 %
axis; dashlines.py reads such vertices directly from the outline. A value was replaced only where the new one differs
by more than max(0.05 %, old se) AND an independent check supports it (vertex point present in the outline; pattern
gap end-cap -> vertex -> start-cap = 4.000 pt; dash-side slopes anchored at the neighbour; band midpoint). Each CSV
ends with a `#` line listing its corrections; the method counts in the older header lines are the original ones.
* **b**: suppressed state 1 features 31 (-44.84 -> -41.95), 37 (-58.48 -> -55.59), 43 (-43.82 -> -40.92): exact
  vertex reads, se 0.01 instead of 1.8-2.0; state 2 feature 34 (22.01 -> 21.87, se 0.02): pattern solution re-fitted.
  Largest change 2.90 %.
* **e**: suppressed state 1 features 3 (-59.38 -> -59.08), 23 (-139.76 -> -133.54), 25 (-138.36 -> -131.98),
  40 (-38.23 -> -35.34); feature 32 filled (-144.55, se 1.26), so 13 values are below -100 % and features 22, 49 stay
  empty; state 2 feature 40 (-17.42 -> -20.32). Largest change 6.38 % (feature 25).
* **c**: suppressed state 2 face 50 (22.96 -> 23.23): replaced by the band midpoint (the file's own band_lo/hi columns
  give 23.23; the dash geometry there has se 0.26); faces 27, 55 filled with band midpoints (33.49, 21.39). Still
  empty: state 1 faces 29, 34, 60; state 2 face 60. Band edges re-derived with `band_extent` agree with the stored
  columns to < 0.05 %.
* **f**: suppressed state 2 faces 8 (60.53 -> 60.58), 26 (42.50 -> 42.09), 40 (37.52 -> 36.75) replaced by band
  midpoints (face 40's change equals its old se, face 8's the 0.05 threshold); face 35 filled (38.43). Still empty:
  state 1 face 37, both faces 60.
* Not changed although dashlines.py differs by 0.07-0.26 %: its 'anchor' reads (vertex taken from a dash cap or a
  symmetric outline pair sitting on the grid x) at steep vertices, b: state 1 features 35, 42; e: state 2 features
  14, 20. The stored pattern-constrained values reproduce the 4.000-pt pattern gap there and the dashlines values do
  not (3.5-3.9 pt): on a near-vertical segment a cap within 0.015 pt in x of the vertex can be 0.15 pt away along
  the line, which the dashlines se (0.04-0.14 %) does not cover.
* Redraws and `_compare.png` images regenerated.

### Extended Data Figure 6 (PDF page 46, legend on p. 22)

Legend: "Balance-trial control. (a)-(e) Same conventions as Fig. 3e-i but for subsampling time points so that for
each trial there is the same number of state 1 and state 2 time points." States inferred from one half of the
neurons, reconstruction/decoding on the held-out half.

Files: `edfig6_panels.tex` (layout + ALT text), `edfig6a_*.png` (face grid), `edfig6{b,c,d,e}.csv` + `.py`
(+ `.pdf`/`.png` output and `_compare.png` QA images).

#### Panels

##### a -- face-image grid (image panel)
* 5 rows x 4 columns of embedded rasters (143x143 px, four 144x144; RGB PNG, grayscale content), native
  resolution. Files `edfig6a_r<1-5>_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png`.
* Ground-truth images are the same PDF objects as in EDF5a/d (xrefs 184/176/180/182/177 and 185/179/181/183/178);
  reconstructions are xrefs 446/448/450/452/454 (state 1) and 447/449/451/453/455 (state 2).

##### b -- explained variance of features vs feature index (plot)
* Same construction as EDF5b (see `the Extended Data Fig. 5 notes` for the method): 5 series, x = feature 1..50,
  y = -100..100 %, Shape/Appearance brackets at features 1.02-19.69 and 20.24-50.11.
* Axes: x ticks 10..50 (residual 1.6e-3 pt), y ticks -100..100 (residual 7e-4 pt); 1 % = 0.555 pt.
* Solid lines: 51-point strokes whose last point is a near-duplicate of feature 50 (0.01 pt to the right, same
  value within 0.03 %); dropped. Dashed lines: all 100 values recovered geometrically (50 + 48 exact vertex reads
  or pattern/line solutions), max se 1.9 % (feature 9 of suppressed state 2; two values with se > 1 %),
  typically < 0.1 %.

##### c -- decoding accuracy vs number of faces (plot with bands)
* Same construction as EDF5c. x ticks 0..60 (residual 0), y ticks 0..100 (residual 3e-4 pt); 1 % = 1.11 pt.
* Dashed lines: empty at faces 10, 19, 45, 60 (suppressed state 1) and 11, 20, 51 (suppressed state 2), where
  the vertex fell in a dash gap without enough constraints; max se 1.1 % (face 1), typically < 0.1 %.
* Bands symmetric about their lines (<= 0.02 %); suppressed-state-1 band clipped at 0 % from face 4 and absent
  beyond face 46.

##### d -- decoding accuracy vs time from flash, three sub-panels (plots)
* Type: three small line plots (Average grey #808080 top-left, State 1 orange bottom-left, State 2 purple
  bottom-right), each with a solid line (decoder output compared with the conscious stimulus) and a dashed line
  (compared with the suppressed stimulus); y = 0..100 %, x ticks 0, 1, 2.
* **Unit caveat:** the printed x label is "Time from flash (ms)", but the lines have 211 samples at 0.01 axis
  units from -0.1 to 2.0 and the identical window is labelled "(seconds)" in Fig. 2c; the data are in seconds
  (200-ms sliding window, 10-ms steps). CSV column `time_from_flash_s`; the redraw labels the axis "(s)".
* Axes per sub-panel: x ticks 0,1,2 (residual 2e-5 pt), y ticks 0,50,100 (residual 2e-5 pt); 1 % = 0.44 pt.
* Solid lines: 212-point strokes whose last point duplicates the previous one 0.005 pt to the right; dropped ->
  211 samples, exact.
* Dashed lines: filled dash polygons (1 pt wide). Samples inside a dash are exact (the outline contains the
  vertex); samples inside a dash gap are not recoverable (with 0.2 pt between samples a 4-pt gap hides several
  samples), except the first sample beyond a dash end, which is extrapolated along the dash's end segment when its
  estimated uncertainty is <= 3 %. Recovered: Average 134/211 samples (87 exact), State 1 143/211 (91 exact),
  State 2 147/211 (87 exact); longest run of missing samples 7 (= 70 ms). Missing samples are empty in the CSV;
  `edfig6d.py` interpolates them linearly **for display only** (stated in the script).
* `*_suppressed_se_pct` columns give the estimated uncertainty (0.04 % for exact reads).

##### e -- paired plot over sessions (plot)
* Type: three x categories (Average, State 1, State 2), ten thin lines per condition (sessions), one thick line
  per condition (mean), filled/open circles at the means (grey/orange/purple).
* y axis ticks 0..100 step 20 (residual 3e-4 pt), 1 % = 1.11 pt; x categories = the three tick marks.
* Conscious (solid): 3-point strokes (thin 0.14 pt, thick 1 pt), exact. Suppressed (dashed): filled dash polygons
  (thin 0.1 pt wide, mean 1 pt), recovered geometrically with se <= 0.05 %.
* Validation: the mean of the ten session rows equals the thick-line values to 0.01 % for both conditions
  (38.37/39.88/18.68 and 28.45/13.35/37.10), and the circle centres coincide with the thick-line vertices.
* Caveat: session numbering is the drawing order within each condition; the conscious and suppressed lines of a
  session cannot be paired from the PDF (rows with the same number are probably, but not verifiably, the same
  session). Chance (10 %) is not drawn.

#### Legend
The shared legend under b/c (same as EDF5) is included in the redraw of b. Data colours: #1c0f29 (priming),
#fcae34 (state 1), #543379 (state 2), #808080 (average).

#### Not recovered / caveats
* c: 7 dashed values empty; d: 77 + 68 + 64 of 211 suppressed samples empty (dash gaps), recovered values have
  se <= 2.9 %; nothing else missing.
* Dashed values in gaps are geometric reconstructions with estimated uncertainties, not direct reads.
* Axis-label unit of d ("ms" printed, seconds in fact) -- see above.

#### Corrections 2026-10-18 (../tools/dashlines.py)
Same procedure and acceptance rule as described in `the Extended Data Fig. 5 notes` (same section). Each CSV ends with a `#`
line listing its corrections.
* **b**: suppressed state 2 features 9 (-6.02 -> -8.91), 31 (11.43 -> 8.54): exact vertex reads, se 0.01 instead
  of 1.88; state 1 features 14 (-28.84 -> -28.33, se 0.12; confirmed by the dash-side slope on segment 13-14) and
  16 (-17.09 -> -16.82, se 0.04; the weakest correction: pattern gap 4.001 vs 3.993 pt, candidates 0.15 pt apart
  along a steep segment). Largest change 2.89 %. Kept: 'anchor' reads at state 1 features 23, 24, 25 (dashlines
  differs by 0.12-0.40 %, but the stored values reproduce the 4.000-pt pattern gap, see the edfig5 note).
* **c**: suppressed state 2 faces 33 (17.93 -> 18.59), 52 (10.41 -> 10.28), 57 (9.17 -> 9.23) replaced by band
  midpoints (face 33's change equals its old se); faces 11, 20, 51 filled with band midpoints (39.67, 27.10, 10.48);
  state 1 faces 10 (4.16), 19 (0.95) filled from dashlines segment fits (se 0.07). Checked and kept: state 1 face 2
  and state 2 face 42 (band midpoints 41.67 / 13.71 agree with the stored values; dashlines' anchor / ambiguous
  values there are 0.25-0.32 % off). Still empty: state 1 faces 45, 60; state 2 face 60. Largest change 0.66 %.
* **d**: checked, not changed. dashlines.py reproduces the exact samples (its 112/122/121 vertex reads agree with the
  CSV to < 0.05 %) but at the extrapolated samples (first sample beyond a dash end) it disagrees with the stored
  per-dash extrapolation by 0.1-6.3 % at 18 samples (average 0.21, 0.33, 0.67, 0.75, 0.89, 1.16, 1.35 s; state 1
  0.35, 0.85, 1.53, 1.63 s; state 2 -0.05, 0.55, 0.77, 0.80, 0.98, 1.19, 1.89 s) and would add ~60 samples with
  se <= 3 % (mostly anchor reads and interpolations). With 0.21-pt sample spacing both are extrapolations of the same
  short dash ends with no independent check, and the anchor reads are unreliable on steep pieces (see b), so the CSV
  was left alone; a re-extraction of d needs its own validation.
* **e**: checked, not changed (all 33 suppressed values agree with dashlines.py to <= 0.005 %).
* Redraws and `_compare.png` images of b and c regenerated.

### Extended Data Figure 7 (PDF page 47, legend on p. 22)

Page geometry: 518.76 x 487.56 pt (not US letter). All panels are vector graphics drawn inside form XObjects
placed at 1:1 scale; the face images are embedded rasters. Tick labels are glyph outlines, so every axis was
calibrated from the tick-mark rectangles with the tick values read off a 300-dpi render (`pdfplot.axis_from_ticks`);
calibration residuals are < 0.002 pt everywhere.

Files per panel (snippet: `edfig7_panels.tex`):

| panel | type | files | recovery |
|---|---|---|---|
| a | image grid 5 x 4 | `edfig7a_r<1-5>_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png` | embedded rasters, native resolution |
| b | line plot, 5 series | `edfig7b.csv`, `edfig7b.py` -> `edfig7b_replot.png`, QA `edfig7b_compare.png` | vector paths |
| c | line plot + shaded bands | `edfig7c.csv`, `edfig7c.py` -> `edfig7c_replot.png`, QA `edfig7c_compare.png` | vector paths |
| d | image grid 5 x 4 | `edfig7d_r<1-5>_*.png` | embedded rasters, native resolution |
| e | line plot, 5 series | `edfig7e.csv`, `edfig7e.py`, QA `edfig7e_compare.png` | vector paths |
| f | line plot + shaded bands | `edfig7f.csv`, `edfig7f.py`, QA `edfig7f_compare.png` | vector paths |

Run the scripts from inside this folder (`python3 edfig7b.py` etc.); they read only their CSV.

#### a, d: face grids

40 separate embedded grayscale images (143 x 143 px, the "ground truth suppressed" column 144 x 144 px), extracted
with `pdfplot.extract_image` at native resolution and named by row (top = r1) and column. The column headers
("Ground truth / Conscious", "Reconstruction / State 1" in orange, "Ground truth / Suppressed", "Reconstruction /
State 2" in purple) are real text in the PDF and are re-set in the tex snippet. Panels a and d use different
image objects for every cell (40 distinct xrefs), including the reconstruction columns, so all 40 were kept.
The ground-truth columns differ between a (reassigned templates A', B') and d (presented faces A, B), as the
legend says. The reconstruction images of a and d are virtually identical pixel-wise (mean absolute difference
about 1 grey level, maximum 13 of 255, i.e. re-encoding noise); all of them are smooth, average-like faces.
The PNGs are RGB files with grey content, as embedded.

#### b, e: explained variance of features (%) vs feature # (1-50)

- x axis: ticks at 10, 20, 30, 40, 50 (the axis starts at feature 1, where the y axis is). y axis: ticks at
  -100, -50, 0, 50, 100 %; 1 % = 0.555 pt.
- The three solid series (priming average, black `#1c0f29`; binocular conscious state 1, orange `#fcae34`;
  binocular conscious state 2, purple `#543379`) are 1-pt stroke polylines with 51 points (50 vertices on the
  integer features plus a duplicated end point 0.01 pt away). Values are exact to the content-stream precision
  (0.001 pt = 0.002 %).
- The two dashed series (binocular suppressed state 1 orange dashed, state 2 purple dashed) are NOT strokes: the
  dashes are filled outlines (1 pt wide, 4 pt long, butt caps, 4 pt gaps), 56/65 dashes in b and 36/56 in e.
  The polyline was recovered geometrically: in each dash outline, pairs of parallel edges 1 pt apart (the two sides
  of a straight stroke piece) give a point on the centreline and the exact direction of that segment; each such
  piece is assigned to the inter-vertex interval that contains it and extrapolated to both vertices; the vertex
  value is the overlap-weighted mean of all estimates (`*_n_estimates` = how many, `*_spread_pct` = max-min of
  them). Mean spread is 0.03-0.13 %; the largest are 1.4 % (b, feature 40) and 0.8 % (b, 41; e, 33) on the
  steepest segments. Bends inside a dash (sharp V-shaped joins) are handled because only straight pieces are used.
- One vertex (e, binocular suppressed state 2, feature 7) sits inside a dash gap with no dash in either adjacent
  interval: its value is not in the PDF and was linearly interpolated between features 6 and 8 (flagged with
  `n_estimates = 0`).
- The "Shape" (features 1-20) and "Appearance" (21-50) brackets above the plot are text + 0.5-pt stroke brackets
  and are redrawn as such. The legend below b/c (shared by b-c and e-f in the original) is included in the b and e
  redraws.

#### c, f: decoding accuracy (%) vs number of faces (1-60)

- x axis: ticks at 0, 20, 40, 60 (data start at 1 face); y axis: 0, 20, ..., 100 %; 1 % = 1.11 pt.
- Solid lines: 60-point strokes, exact. Bands: filled polygons at opacity 0.2, one per series (5 bands), clipped to
  0-100 % in the PDF (extra vertices at the clip edges); the band edges were read as the vertical extent of each
  polygon at each integer x, so clipping is handled. Where a band collapsed onto the 0 % axis and was not drawn
  (purple conscious-state-2 band beyond ~56 faces in c) the band columns are `nan`. Two bands share the colour of a
  solid and a dashed line; they were assigned by which line's values the band centre tracks (unambiguous:
  distances 2-20 pt vs 150-550 pt summed over 60 points). Band values at 1 face can read 100.0x % because of the
  clipped polygon corners (rounding, < 0.06 %).
- Dashed lines: centreline recovered as in b/e (22-24 dashes per line). Independent check: each error band is
  exactly symmetric about its line, so the band midpoint must equal the line value wherever the band is not
  clipped at 0/100 %; the solid lines agree with their band midpoints to 0.005 %, and the dash-recovered vertices
  agree to within 0.05 % (c) / 0.02 % (f) at every checkable vertex, which also confirms the band assignment.
- Because the dash period (8 pt) is about 5 faces, 11-14 vertices per dashed line fall inside a dash gap with no
  dash in either neighbouring interval and are absent from the dash geometry. These were taken from the band
  midpoint (real geometry, same precision as above) where the band is unclipped, flagged `*_gap_fill =
  band_midpoint` (with `*_n_estimates = 0`): c orange 34, 38, 39, 44, 49, 54, 59, 60; c purple 12, 16, 21, 26, 31,
  36, 41, 46, 51, 55, 56; f orange 11, 15, 20, 24, 25, 29, 34, 39, 44, 49, 54, 55, 59, 60; f purple 18, 22, 23, 27, 32,
  37, 42, 47, 52, 53, 57. Five vertices of the orange dashed line in c (faces 9, 14, 19, 24, 29), where the band is
  clipped at 0 %, were linearly interpolated between their neighbours (`*_gap_fill = interpolated`; the curve is
  smooth there, values about 2-8 %, neighbours differing by < 1.5 %, so the error is a fraction of a percent).
  The redraw scripts simply plot the CSV, so these vertices appear as ordinary line vertices.

#### Not recovered / approximations

- The five interpolated dashed-line vertices listed above (c, orange dashed, faces 9, 14, 19, 24, 29); they are not
  visible in the PDF either (they sit in dash gaps).
- Everything else is read from vector geometry or embedded rasters; nothing was read off by eye except the tick
  values used for calibration.

### Extended Data Figure 8 (PDF page 48, legend on p. 22)

Two plot panels (no letters in the original: "Left, state 1; right, state 2"). Files:

- `edfig8_left_state1.csv` -- 40 bins (`bin_left`, `bin_right`, `bin_centre`, width 0.05 from -1 to 1) with
  integer cell counts for `state1_conscious`, `state1_suppressed`, `priming_half_trials`.
- `edfig8_right_state2.csv` -- same bins, counts for `state2_conscious`, `state2_suppressed`, `priming_half_trials`.
- `edfig8_left_state1.py`, `edfig8_right_state2.py` -- redraw each panel from its CSV (shared code in
  `_edfig8_common.py`) -> `edfig8_<panel>.png` (200 dpi) and `.pdf`.
- `edfig8_<panel>_orig.png` (300-dpi crops of the original) and `edfig8_<panel>_compare.png` (original | redraw).
- `edfig8_extract.py` -- the extraction (needs the PDF and `../tools/pdfplot.py`).

How the data were recovered (vector paths only):

- Each series is drawn twice in the PDF: translucent bar rectangles (fill opacity 0.30, one rect per non-empty
  bin, adjacent equal bins occasionally merged into one polygon) and an opaque 0.5-pt-wide step outline drawn as a
  filled band. Counts were taken from the bar tops; the outline band gives identical values (max difference
  0.000 counts). Bar edges lie on the 0.05 grid to within 0.0002.
- x axes calibrated from the five tick marks (values -1, -0.5, 0, 0.5, 1 read off the render; labels are glyph
  outlines), residual 3e-5. y axes from the two tick marks: 0 and 50 (left), 0 and 60 (right), residual ~0;
  the baseline of the bars coincides with the 0 tick. 1 count = 2.610 pt (left) / 2.175 pt (right).
- Every count came out within 0.002 of an integer and every series sums to exactly 548 cells (the legend's
  n = 548), so the recovery is exact. The priming half-trials series is identical in both panels, as expected.
- Colours (fill = outline): State 1 conscious `#fcae34`, State 1 suppressed `#ffd28a`, State 2 conscious
  `#b56cc7`, State 2 suppressed `#543379`, Priming half-trials `#000000`. Grey reference line at cosine = 0:
  `#b3b3b3`, 0.5 pt, opacity 0.70. Draw order (bottom to top): conscious, suppressed, priming (left); conscious,
  suppressed, priming (right). Legend swatches in the original are 2.25-pt lines.
- Layout differences in the redraw: the original has one legend with all five entries between the two panels
  and the y-axis title "Cell count" only on the left panel; each redraw carries a legend with its own three
  entries, and the right panel again has no y title.

Summary of the recovered distributions (bin of the peak, fraction of cells above 0 / above 0.5):
state1_conscious peak 45 at 0.55-0.60, 0.93 / 0.55; state1_suppressed peak 41 at 0.15-0.20, 0.66 / 0.10;
priming_half_trials peak 49 at 0.75-0.80, 0.91 / 0.61; state2_conscious peak 41 at 0.25-0.30, 0.73 / 0.21;
state2_suppressed peak 55 at 0.65-0.70, 0.94 / 0.57.

Nothing had to be approximated. Not recoverable: per-cell values (only binned counts are plotted) and the
t-test statistics quoted in the legend (text, not plotted).

### Extended Data Figure 9 (PDF page 49, legend on p. 22)

Source: Hesse et al. 2026, bioRxiv 10.64898/2026.10.15.759299v1, Extended Data Figure 9 ("On/Off states are
separate from conscious/suppressed states"). Everything here was recovered from the vector paths and embedded
images of PDF page 49 with `../tools/pdfplot.py`; nothing was typed in from the text.

Files:

- `edfig9_extract.py` -- the extraction script (reads the PDF, writes all CSVs and the panel-b images; prints the
  counts quoted below). `edfig9_make_compare.sh` builds the `*_compare.png` QA images (original 300-dpi crop left,
  regenerated PNG right). `_style.py` is the shared matplotlib style for the redraw scripts.
- `edfig9<p>.py` redraw scripts: run from this folder, each reads only its CSV(s) and writes `edfig9<p>.pdf` and
  `edfig9<p>_replot.png` (200 dpi). `edfig9_panels.tex` lays the panels out with ALT text.
- **Duplicate panel letter:** the preprint labels two different panels "h": the decoding-accuracy-vs-number-of-cells
  plot (here `edfig9h_decoding_vs_cells.*`) and the 2 x 2 modulation-index scatters (`edfig9h_modulation_index.*`).

Axis calibration everywhere: numeric tick labels are glyph outlines, so each axis was calibrated from the tick-mark
rectangles paired with the tick values read off a 300-dpi render; all axes are linear with fit residual < 0.03 pt.
Colours read from the paths: black `#1c0f29`, orange `#fcae34`, purple `#543379`, pale orange `#ffd28a`, pale purple
`#b56cc7`, axes `#333333`.

#### a -- spike raster with four-state shading (plot; `edfig9a_spikes.csv`, `edfig9a_state_epochs.csv`, `edfig9a.py`)

- **Spikes:** 5258 black stroke segments (1 pt line width, 0.1 pt long, i.e. one 1-ms bin). `time_s` = segment centre
  mapped through the x axis (ticks at -1, -0.5, 0, 0.5, 1 s; 107.1 pt/s), precision about 0.5 ms. Spikes span
  -1.010 to 1.002 s; the flash line is at 0.000 s.
- **Rows:** the spike y positions lie on an exact lattice (pitch 0.23199 pt, max residual 0.005 pt). `row_index`
  counts lattice rows downward from the upper y-axis tick (row 1); the lower y-axis tick falls exactly on row 412
  (= the lowest row with spikes), the axes box ends at row 417, and the thin ML/AM separator line lies between
  rows 158 and 159 (ML above). Only 326 rows contain spikes, and rows 1-8 are empty. The y-axis label says
  "429 cells", but the tick-to-tick span is 411 row pitches, so the mapping from row to cell number (and why 412
  rather than 429 rows span the ticks) could not be determined from the figure; the `row_index` is a drawing-based
  index, not the paper's cell number.
- **Shading:** two independent tilings of 20 %-opacity rectangles spanning the full plot height: orange/purple
  (144 rects) for conscious (state 1) / suppressed (state 2), and white/black (120 rects) for On / Off ("bright and
  dark overlays correspond to On and Off states", legend). `edfig9a_state_epochs.csv` lists the 219 intervals of the
  combined four-state sequence (`state` = `<percept>_<On|Off>`, plus the two factors as separate columns), contiguous
  from -1.014 s (the shading starts 1.5 pt left of the -1 s tick) to 1.002 s. Edge precision 0.1 ms (0.01 pt);
  27 seams between the two tilings shorter than 0.1 ms were dropped. Rendered colours: conscious+On pale orange,
  conscious+Off dark tan, suppressed+On pale lavender, suppressed+Off dark grey-purple.
- The redraw composites the same two 20 %-alpha layers, so the colours match the original.

#### b -- face grid (images; `edfig9b_r<1-5>_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png`)

20 embedded raster images extracted at native resolution (143 x 143 px; the ground-truth-suppressed column is
144 x 144 px), RGB files with grey-scale content. Rows 1-5 top to bottom; columns left to right as in the
original headers ("Ground truth / Conscious", "Reconstruction / State 1" (orange), "Ground truth / Suppressed",
"Reconstruction / State 2" (purple)). The column headers are typeset in the tex snippet (plain text; the orange and
purple header colours of the original are not reproduced to avoid a package dependency).

#### c -- explained variance vs feature (plot; `edfig9c.csv`, `edfig9c.py`)

- x axis: ticks 10-50 (features 1-50 at 1.93 pt spacing); y axis: ticks -100..100 %.
- The three solid series are 1-pt stroke polylines with one vertex per feature (precision ~0.1 %).
  `binocular_conscious_state2` is clipped at the lower axis limit: at features 21, 22, 23, 25, 30, 38, 39, 42 and 49
  the line leaves the axes below -100 % and the value is not recoverable (empty cells). The redraw script draws
  those segments running off the bottom of the axes, as in the original, using an off-axis placeholder that is
  clipped away.
- The two dashed series were exported as **filled dash outlines** (not dashed strokes). Each dash polygon's two long
  parallel edges (1 pt apart) were paired to get the dash centre line; the vertex values were read where dashes
  cover a vertex or by extending the adjacent dash segments to the vertex x. Estimates from the two adjacent
  segments agree within 0.25 % at every vertex; expected precision about 0.5 % (worse on very steep segments). All
  50 vertices of both dashed series were recovered.

#### d -- decoding accuracy vs number of faces (plot; `edfig9d.csv`, `edfig9d.py`)

- x axis: ticks 0, 20, 40, 60 (faces 1-60 at 1.575 pt spacing); y axis: ticks 0..100 %.
- Solid series: stroke polylines, one vertex per face count (precision ~0.1 %).
- Dashed series: same dash-outline reconstruction as in c (adjacent-segment agreement within 0.05 %). Here the dash
  pattern is 4 pt on / 4 pt off, longer than the 1.575-pt vertex spacing, so 13 vertices of each dashed series fall
  inside a gap with no dash on either adjacent segment and are left empty (suppressed state 1: faces 11, 16, 21, 26,
  31, 36, 37, 41, 46, 51, 52, 56, 57; suppressed state 2: faces 17, 21, 22, 26, 30, 35, 39, 43, 44, 48, 49, 53, 58).
  The redraw joins the neighbouring vertices across these gaps (linear), which is what the eye sees in the original.
- Bands (`_lo`, `_hi`): the 20 %-opacity band polygons are clipped by the axes box at 0 and 100 %, so the band
  edges were measured as the vertical cross-section of each polygon at every face position (precision ~0.1 %) and
  clamped to [0, 100]; `_lo = 0` / `_hi = 100` can therefore stand for values beyond the axis. The
  `binocular_conscious_state2` band has zero area beyond 14 faces (line and band both at 0 %), so its `_lo/_hi` are
  empty there and the redraw simply draws no band.
- Band assignment to series was done by colour and by which series' line lies inside the band (printed by the
  extraction script).

#### e -- gain histograms (plot; `edfig9e.csv`, `edfig9e.py`)

- Three rows, each overlaying two series drawn as 30 %-opacity filled bars plus a step outline. x axis: ticks at
  0 and 2 (axis -0.5 to 2.53); each row has its own y axis with ticks at 0 and 100 counts (row 1 scale differs from
  rows 2-3).
- Counts were measured from the filled bars; every measured height was within 0.005 of an integer and was rounded.
  Bin widths differ between series: `state1_conscious` and `state2_suppressed` use 0.2-wide bins starting at 0,
  `state1_suppressed` and `state2_conscious` use 0.1-wide bins starting at -0.2 / -0.1. The right-most 0.2-wide bin
  (2.4-2.6) is cut by the axis limit at 2.5 (listed as 2.4-2.5005). Totals: state1_conscious 542, state1_suppressed
  543, state2_conscious 543, state2_suppressed 541 (Fig. 4c quotes n = 543 cells; the missing 1-2 cells presumably
  lie beyond gain 2.5). Rows 1 and 3 contain identical `state1_conscious` bars, rows 2 and 3 identical
  `state2_suppressed` bars (both kept, with `panel_row`).

#### f, g -- scatter plots (plots; `edfig9f.csv`, `edfig9g.csv`, `edfig9f.py`, `edfig9g.py`)

One row per marker (0.5-pt filled black circles; centre of the marker path, precision ~0.001 units). f: 539 markers,
axes -0.5..2.5 (ticks 0, 2), dashed identity and zero lines. g: 446 markers, axes 0..3, dashed identity line. The
Fig. 4d/e legends quote n = 543 cells; the lower marker counts are what is drawn (coincident markers cannot be
separated and points outside the axes are not drawn). The dashed reference lines are drawn by the scripts, not
stored as data.

#### h (first) -- decoding accuracy vs number of cells (plot; `edfig9h_decoding_vs_cells.csv`, `edfig9h_decoding_vs_cells.py`)

24 line vertices at 1-10, 20-100 (step 10), 200-500 (step 100) and 1000 cells (x snapped to these integers; the
vertex spacing matched them to < 0.01 pt); accuracy precision ~0.1 %. The 20 %-opacity grey band's lower/upper
edges are given at the same cell counts. The dashed 50 % chance line is drawn by the script.

#### h (second) -- modulation index scatters (plot; `edfig9h_modulation_index.csv`, `edfig9h_modulation_index.py`)

Four subpanels calibrated separately from their own tick marks at -1, 0, 1 (both axes). 0.72-pt filled black
circles, one row per marker, precision ~0.001. Marker counts: all_states 2906, state1 2906, state2 2906,
slope_equalized 1256 (the Fig. 4g legend quotes n = 2885 cell-stimulus pairs for each; the slope-equalized panel is
drawn with far fewer points -- that is what the PDF contains, one contiguous block of 1256 marker paths). The dashed
diagonal is y = x in three subpanels and y = -x in the State 2 subpanel; these and the zero lines are drawn by the
script.

#### Toolkit note

`pdfplot.drawings(page, clip)` originally dropped paths with a zero-height/zero-width bbox (the raster's spike
ticks) because `fitz.Rect.intersects` is False for empty rects; `edfig9_extract.py` therefore takes the whole-page
drawing list and filters by bbox position itself. The toolkit has since been fixed; re-running the script with the
fixed toolkit gives identical CSVs.

### Extended Data Figure 10 (PDF page 50, legend on p. 22)

Page geometry: 518.76 x 393.96 pt. Only the panel letters and the legend entries of b and e are real text; the
table text, axis titles, tick labels and the numbers printed inside bars are glyph outlines. Each plot is drawn
inside a form XObject (bars, error bars, markers and labels), placed on the page with a `cm` transform; the axes and
tick marks are page-level 0.5-pt filled rectangles. Every axis was calibrated from the tick-mark rectangles with the
tick values read off a 300-dpi render (residuals < 0.003 pt). Error bars are single 0.5-pt stroke segments; their
bounding boxes have zero width, which the first version of `pdfplot.drawings` dropped at the clip test (the toolkit
was fixed during this work and the results were re-extracted and checked).

Files per panel (snippet: `edfig10_panels.tex`):

| panel | type | files | recovery |
|---|---|---|---|
| a | table (model x test, check/cross) | `edfig10a.csv`; LaTeX `tabular` in the snippet (uses `pifont` `\ding{51}`/`\ding{55}` and `xcolor`) | transcribed: mark colours from the paths, positions mapped to rows/columns |
| b | grouped bars + error bars | `edfig10b.csv`, `edfig10b.py` -> `_replot.png`, QA `edfig10b_compare.png` | vector paths + 6 printed numbers read by eye |
| c | line plot with labelled points | `edfig10c.csv`, `edfig10c.py`, QA `edfig10c_compare.png` | vector paths + 18 point labels read by eye |
| d | grouped bars + error bars | `edfig10d.csv`, `edfig10d.py`, QA `edfig10d_compare.png` | vector paths + 2 printed numbers read by eye |
| e | grouped bars + error bars | `edfig10e.csv`, `edfig10e.py`, QA `edfig10e_compare.png` | vector paths |
| f | bars + error bars | `edfig10f.csv`, `edfig10f.py`, QA `edfig10f_compare.png` | vector paths |

Run the scripts from inside this folder (`python3 edfig10b.py` etc.); they read only their CSV. The CSVs avoid a
leading `#` in data cells (colours are stored as `fcae34`, not `#fcae34`) so that `pandas.read_csv(comment="#")`
works.

#### a: model x test matrix

Green check (`#33a13d`) = pass, red cross (`#d63030`) = fail; 20 marks, assigned to the 5 columns (Real, 2-state,
C-only, Average, Uncoord) and 4 rows (Reconstruction, Reconstruction^coord, Reversal, Log likelihood) by their
positions relative to the column/row tick marks. Result: Real and 2-state pass all four tests, C-only fails all
four, Average and Uncoord pass only Reconstruction. The row/column labels are glyph outlines and were transcribed
from the render (they match the legend text).

#### b, d: reconstruction EV (%) bars

- 16 bars each (4 models x 4 series), bar rectangles 7.55 pt wide. Series by colour and fill opacity:
  state 1 conscious = `#fcae34` at opacity 1, state 1 suppressed = `#fcae34` at opacity 0.35, state 2 conscious =
  `#543379` at opacity 0.35, state 2 suppressed = `#543379` at opacity 1 (the legend swatches of b use the flattened
  colours `#fee3b8` / `#c3b8d0` for the light variants). Bar order within a group is the legend order.
- `value_ev_pct` = bar top mapped through the y axis (precision ~0.05 %). Bars whose value is below the axis minimum
  (-100 %) are drawn down to exactly -100 % with the value printed inside as rotated text; for these,
  `value_ev_pct` is the printed number (read by eye from the 300-dpi render: b: -183, -182, -108, -106, -109, -105;
  d: -124, -128; each label's position was matched to its bar programmatically), `bar_drawn_to_ev_pct` is -100 and
  `printed_label` holds the text. These clipped bars have no error bars in the PDF (`err_lo/err_hi` = nan,
  `n_error_bar_segments` = 0).
- Error bars: two vertical 0.5-pt black segments from the bar top (plus 2-pt caps); `err_lo/err_hi` are their ends.
  They are read from the unclipped geometry, so the Real state-1-suppressed bar in b (value -98.7 %) has
  `err_lo` = -100.0 % although the figure clips it at the axis.
- The thin black zero line and the axis spines are redrawn; the grouped layout (bar width 0.18 of the group
  spacing, offsets +/-0.1, +/-0.3) reproduces the original proportions.

#### c: reconstruction EV (conscious, state 1) vs achieved mean HMM dwell (ms)

- Two 9-vertex 1-pt stroke polylines (red `#cc2929` real data, blue `#2970bf` averaging model) with 3-pt filled
  circle markers at the vertices (markers coincide with the vertices to < 0.05 pt). Coordinates are precise to
  ~0.1 ms and ~0.01 %.
- Each point has a small horizontal x-error bar (0.5-pt strokes of the series colour, caps 1 pt), extents in
  `dwell_err_lo_ms` / `dwell_err_hi_ms` (about +/-0.1 to +/-3 ms, growing with dwell time). No vertical error bars.
- The point labels (imposed self-transition probability p) are glyph outlines; 18 label groups were found, one next
  to each point. Their text was read by eye from the render: 0.50, 0.60, 0.70, 0.80, 0.87, 0.92, 0.95, 0.97, 0.99
  for both series, in order of increasing dwell time (matches the legend: p varied from 0.5 to 0.99).
- Axes: x ticks 0..300 ms (7 ticks), y ticks 45..65 % (5 ticks).

#### e: held-out tuning correlation bars

8 bars (state 1 orange, state 2 purple; 13.4 pt wide) with error bars, y ticks -1, -0.5, 0, 0.5, 1.
Values (r): Real +0.595 / -0.424; 2-state +0.646 / -0.658; Average +0.009 / +0.020; Uncoord +0.011 / +0.009;
error bars +/-0.010 to 0.016. Precision ~0.001.

#### f: held-out log likelihood (2-state minus 1-state) bars

4 dark grey (`#262626`, fill+stroke) bars with error bars, y ticks -0.15 .. 0.1 (step 0.05).
Values: Real 0.080 (0.067-0.093), 2-state 0.053 (0.039-0.066), Average -0.122 (-0.136 to -0.108),
Uncoord -0.122 (-0.136 to -0.108). The two negative bars are numerically identical to 3 decimals in the PDF
geometry (the same within 0.0005). Precision ~0.0003.

#### Transcribed by eye (everything else is from the vector geometry)

Tick values used for calibration; the 8 numbers printed inside clipped bars (b, d); the 18 point labels of c; the
row/column labels of the table a.

## Observations about the paper made while decompiling it

These are inconsistencies in the preprint itself (version 1), found when the figures were taken apart;
details and counts are in the per-figure READMEs.

- Fig. 1h states n = 5550 cell-stimulus pairs; the PDF draws 3498 distinct points.
- Fig. 4g and Fig. 6f, "slope-equalized" panels: the +/-1 axes clip a large part of the data (1612 of 2885 and
  126 of 283 points drawn); the quoted Pearson r values for those panels are not reproducible from the visible
  points, and the legends do not mention clipping.
- Fig. 1g and Extended Data Fig. 9a are labelled "429 cells" but the raster grid has 412 rows between the axis
  ticks (326 rows with spikes); Fig. 2b gives 157 + 254 = 411 cells for the same session.
- Fig. 2k, Fig. 3h and Extended Data Fig. 6d label the x axis "Time from flash (ms)" although it runs 0-2 s.
- The Fig. 1b legend describes a priming-aligned time axis (priming at t = 0, flash at 2 s); the panel is aligned
  to the flash at t = 0.
- Extended Data Fig. 9 has two panels labelled "h".
- Methods: "Kilosort3" cites ref. 33, titled "Spike sorting with Kilosort4"; "described in more detail in 13" has
  the citation number typeset as plain text; ref. 11 lists the COGITATE Consortium as "Consortium, C.".
- Results, On/Off section: the 80 % agreement between four-state and two-state models is cited to "Fig. 2a"
  (the LLR schematic), probably meaning Extended Data Fig. 9.
- Figure production: Fig. 4b's "554 cells x 1500 stimuli" heatmaps are 169 x 169-pixel JPEGs in the PDF;
  Fig. 1f's AM heatmap (215 cells) is a 193-row raster; Fig. 5b is a ~200-dpi rasterisation of the state map.
  Several explained-variance traces (Fig. 6b, Extended Data Figs. 2b, 5e, 6b, 9c) run below the -100 % axis
  limit and are cut off without mention in the legends.

## Known problems and things not recovered

- Values that the figures clip (lines below the −100 % axis limit in Fig. 2i, Fig. 6b, Extended Data Figs. 2b, 5e,
  6b, 9c; points outside the ±1 axes of Fig. 4g and Fig. 6f "slope-equalized") are not in the PDF and are left empty
  or flagged in the CSVs; see the notes of those figures.
- Dashed series are recovered from dash outline polygons (the PDF has no dashed strokes); vertices inside dash gaps
  are interpolated or fitted and carry a larger uncertainty, given per value where the CSV has an `se` column
  (Extended Data Figs. 2, 3, 5, 6, 7) and as a per-panel statement otherwise. Thirty-three values in seven CSVs were
  corrected on 2026-10-18 with `../tools/dashlines.py` (listed in the "Corrections" paragraphs of the notes and in a
  trailing `#` line of each corrected CSV); `edfig5_extract.py`/`edfig6_extract.py` and `fig2_extract.py` therefore
  do not reproduce those values exactly when re-run.
- Heatmaps (Fig. 1f, Fig. 4b) and the state map (Fig. 5b) are embedded rasters at a lower resolution than the data
  they show (e.g. 169 × 169 px for "554 cells × 1500 stimuli"); their CSVs are per pixel, mapped through the colour
  bar, not per cell.
- Fig. 1h: the PDF draws 3498 distinct points where the legend states n = 5550.
- The paper names no data or code files; nothing is missing from `source/` that the paper offers.
