# yeatts2026: decompiled

MariPen Yeatts, Nirupama Chinthalapati, Bahar Baradaran, Henry M. Heinks, Emily Liao, Rachael Huxford, Vasilis
Karlaftis, Taylor Grafft, Tanya K. Casta, Ayana Hellevik, Pramod K. Pisharady, Amy Howard, Jan Zimmermann, Thomas
Pengo, Jonathan L. Baker, Keith P. Purpura, Matthew D. Johnson, R. Clay Reid, Franco Pestilli, Saad Jbabdi, Sarah R.
Heilbronner, Taner Akkin. "Scaling up polarization-sensitive optical coherence tomography to image the whole macaque
brain." bioRxiv preprint, **version 1, posted June 15, 2026**, not certified by peer review.
DOI [10.64898/2026.06.11.731509](https://doi.org/10.64898/2026.06.11.731509). Correspondence: Taner Akkin (akkin@umn.edu).

**Licence:** CC BY-NC 4.0 International, as printed in the bioRxiv stamp on every page of the main PDF. (The
citation, dates and licence above are taken from the PDF; they agree with `source/SOURCE.txt`.)

## Local and external

**In this folder**
- `source/yeatts2026.pdf` – the preprint, 23 pp., born-digital (embedded Arial/Cambria fonts, no scan), bioRxiv
  stamp on every page, the manuscript's margin line numbers 1–505.
- `source/yeatts2026_supplement.pdf` – "Supplemental Methods and Results" (bioRxiv media-1.pdf), 5 pp., born-digital,
  no stamp, margin line numbers 1–54.
- `source/SOURCE.txt` – where and when the PDFs were obtained (bioRxiv, 2026-10-20).
- `screening.md` – an earlier screening note by another agent, from a web read of the PMC version; kept as is, **not
  used as a source** for any .tex file.

**Named by the paper but not available here (tier-1 sources that were not available)**
- The data and processing code: "Data and processing code are publicly available at brainlife.io" (p. 15, line 278;
  also the Acknowledgements, p. 1). No specific project or dataset identifier is printed. Not retrieved (no network).
- The **Supplemental Videos for Subjects M and V** (p. 13, lines 264–266: axis-orientation images with brightness
  controlled by retardance): not in the supplement PDF, not available.
- The only plotted panels (Supplemental Fig. 2 a–c) have no source-data file; they are digitized (tier 3) below.

## Contents

- `main.tex` / `main.pdf` – the whole preprint in reading order: title, authors with affiliation superscripts, the
  11 affiliations (hanging-indent list), correspondence block, keywords, acknowledgements, competing interests,
  Summary, Introduction, Results (with its sub-headings), Discussion, Methods, and the 39 references with their
  printed numbering. Each figure is placed before its caption, where it is printed. `\pdfpage{N}` marks every page,
  including the figure-only page 14 (marker before the Fig. 5 block).
- `supplement.tex` / `supplement.pdf` – the whole supplement: the underlined title, the two text sections
  ("Compresstome Customization", "Alternative Gelling Investigation") and Supplemental Figures 1–4 with captions.
- `figures/` – every figure as a 200-dpi render (`fig1.png` … `fig6.png`, `sfig1.png` … `sfig4.png`; crop = the
  bbox of the embedded figure image(s) plus a 3-pt margin, without the caption), and for the plotted panels of
  Supplemental Fig. 2: `sfig2atop.csv`, `sfig2abottom.csv`, `sfig2btop.csv`, `sfig2bbottom.csv` (line plots),
  `sfig2ctop.csv`, `sfig2cbottom.csv` (grey-level grids), with `sfig2a_extract.py`, `sfig2b_extract.py`,
  `sfig2c_extract.py`, the plot scripts `sfig2a.py`, `sfig2b.py`, `sfig2c.py` and the re-plots `sfig2a_replot.png`,
  `sfig2b_replot.png`, `sfig2c_replot.png`.
- `tables/text_values.csv` – **compiler-created** (not a table of the paper; the paper has no tables): the key
  numbers from the running text, each with the printed wording, PDF page and the preprint's line numbers. Started by
  the coordinator from the screening read; every row verified against the PDF, the scope wording corrected to the
  printed wording ("speed setting 2", "oscillation setting 8", not "dial"), the PMC URL column replaced by page/line
  references, and 24 rows added about the sectioning (slicer and its modifications, section thickness, cutting
  settings, agarose concentrations and what happened with each, tube dimensions, mounting, cooling, failures and
  fixes, section storage, throughput, data volume).
- `work/` – scratch: `build_main.py` (the text extraction, see below), `alt/*.tex` (the figure descriptions the
  build inserts), page renders, overlays, side-by-side comparisons (`cmp_sfig2*.png`), check JSON, lualatex logs.
  May be deleted (but `build_main.py` and `alt/` are needed to rebuild the .tex files).

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (and `supplement.tex`) from this folder; both
compile without errors (run twice; 19 and 6 pages). Rebuild the text: `python3 -I -B work/build_main.py`.
Re-run the data: `python3 -I -B figures/sfig2a_extract.py` (then `sfig2b_extract.py`, `sfig2c_extract.py`) and
`python3 -I -B figures/sfig2a.py` etc. The scripts import `/home/admin/ephemeral/oct_17_papers/tools/digitize_common.py`
by absolute path (this folder is outside the oct_17_papers collection, so `../tools/` does not exist here).

## How the text was made

`work/build_main.py` reads every text span of both PDFs with PyMuPDF (font, size, flags, bbox), drops the bioRxiv
stamp (Helvetica 8 pt), the margin line numbers (bare integers left of the text column) and the page numbers,
clusters spans into lines and lines into paragraphs (blank numbered lines, vertical gaps, outdents of the
hanging-indent lists, bold headings, bold "Label:" starts, caption starts), converts the span styles (bold → `\textbf`,
italic → `\emph`, superscript flag or 7-pt size → `\textsuperscript`), escapes LaTeX specials, joins lines (without a
space after a line-end hyphen: every line-end hyphen in this Word-made preprint is a real compound hyphen, e.g.
whole-brain, near-distortion-free, PS-OCT, two-axis), inserts the `\pdfpage` markers, the figure blocks and the
descriptions from `work/alt/`. The only correction table entry is the p. 10 equation, set in Cambria Math whose text
layer is private-use glyph codes, written as `$A(z)e^{i\theta(z)}$` from the page image. The result was proofread
against the page images (hyphen joins, superscripts, °C, μm/µm as printed, ×, en dashes, the bold figure references,
the odd spacings the paper prints such as "Amy Howard⁹ ,", "larger brains ¹²,²⁴,²⁸,³⁰" and "yellow rectangle .",
the reference formatting) and no transcription errors were found.

## Text check (`/home/admin/ephemeral/oct_17_papers/tools/check_text.py` version 2026-10-17j, run 2026-10-20)

Options used: `--drop-line-numbers` for both files (the preprint's margin line numbers); no `--pages`, `--exclude`
or `--figure-box`.

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text only (also without text inside figures) | tex tokens found in PDF | MISSING runs ≥ 6 | EXTRA runs ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 82.2 % | **99.9 %** (1380 repeated tokens) | **99.9 %** (0 figure-internal tokens) | 100.0 % | 0 | 0 |
| `supplement.tex` | **100.0 %** | 100.0 % (0 repeated) | 100.0 % | 100.0 % | 0 | 0 |

PDF tokens 7790 / tex tokens 6404 (main); 748 / 748 (supplement). What is not matched (`--min-run 1`):

- **main, repeated text** (left out by the second number): the bioRxiv stamp on all 22 text pages (quoted once in the
  `\decompnote` at the top of `main.tex`; it is boilerplate, left out on purpose).
- **main, MISSING**: 8 single tokens, all margin line numbers (79, 105, 129, 166, 238, 376, 429, 436). They are
  exactly the line numbers of the lines that follow a line ending in a hyphen ("near-", "whole-", "whole-", "PS-",
  "cross-", "two-", "polarization-", "Multi-"): the tool's dehyphenation glues the number to the hyphenated word
  before `--drop-line-numbers` sees it. Not text of the paper.
- **main, EXTRA**: one run of 2 tokens, "i z", from `$A(z)e^{i\theta(z)}$` (the PDF text layer holds private-use
  glyph codes for the Cambria Math equation; the LaTeX is transcribed from the page image).
- **supplement**: nothing unmatched at any run length.

Text inside the figures (labels, axis titles, legend entries) is in the embedded raster images, not in the text
layer, so the checker has nothing to count there; it is transcribed in the `\alttext` descriptions.

Read-through against the page images (spec step 4) done for: all superscripts (citation numbers, affiliation
numbers, mm², the "36,37" at a line start), °C and the degree signs in 22.5°/45°/6°, μm (U+03BC) and µm (U+00B5) as
printed, ×, en dashes in reference page ranges and "polarization-sensitive optical coherence tomography – a review",
the 6"x6" plate, the Cambria equation, bold/italic in the references (bold volumes, italic journals and "et al."),
the underlined "References" and "Supplemental Methods and Results" headings, the correspondence block's line
breaks, and the order of text around the six figures (Fig. 1's caption continues on p. 7, Fig. 4's on p. 13;
page 14 is figure-only; Fig. 5's caption is on p. 15).

## Figures

Every figure is included as a 200-dpi render with an `\alttext` description panel by panel. **No panel in the main
PDF has quantitative axes** (schematics, cartoons, a flow diagram with equations, enface micrographs, 3D renderings
and montages), so the main paper gets no CSVs. The only plotted panels are in **Supplemental Fig. 2**, which is a
single 768 × 652 px raster at ~121 ppi (the 33 vector paths on that page are Word's white picture-frame
rectangles, nothing of the plot; `vector_dump.py` checked), so all its data are **tier 3 (digitized)**. No axis in it
has numbers, so every coordinate is the fraction of the axis box (0 = left/bottom axis line, 1 = right/top end), and
the unlabelled tick positions are recorded in each CSV header.

**Checks:** every extraction was drawn back onto the native image (`work/sfig2a_overlay.png`, `sfig2b_overlay.png`,
zooms `z_sfig2a_overlay.png`/`z_sfig2b_overlay.png`; the panel-c box detection in `work/sfig2c_boxes.png`) and every
re-plot was put next to a 300-dpi crop of the original with `compare.py` (`work/cmp_sfig2a.png`, `cmp_sfig2b.png`,
`cmp_sfig2c.png`); all were looked at: the magenta points sit on the traces, and the re-plots show the same series,
shapes, ranges and the same two B-scans with the same grey ramp.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | schematic (interferometer) | – | – | |
| Fig. 1b | illustration (colour-coded fibre bundles, colour wheel 0°/90°) | – | – | |
| Fig. 1c | grey-scale coronal brain image with a tile-FOV rectangle | – | – | |
| Fig. 1d | cartoon/block diagram (challenges and solutions) | – | – | transcribed in `\alttext` |
| Fig. 1e | 3D rendering (hardware; exploded storage container) | – | – | |
| Fig. 1f | axis-orientation enface image, whole coronal section | – | – | colour wheel, no scale bar |
| Fig. 2a–d | schematics (gel injection, mold, tube, container) | – | – | |
| Fig. 3 | flow diagram with equations and three illustrations + three small images | – | – | equations transcribed in `\alttext` |
| Fig. 4a | 3 × 4 grid of coronal enface images (slices 081, 169, 203; four contrasts) | – | – | zoom rectangles cyan/green/yellow |
| Fig. 4b–d | enface zooms (reflectivity, cross polarization, retardance) with anatomical labels | – | – | |
| Fig. 4e | three axis-orientation zooms, scale bar 1mm | – | – | |
| Fig. 5a | 3 × 4 grid of sagittal enface images (slices 083, 138, 172), scale bar 15 mm | – | – | |
| Fig. 5b–d | enface zooms + their orientation images with orange rectangles | – | – | |
| Fig. 5e | three axis-orientation zooms, scale bar 1 mm | – | – | |
| Fig. 6a–c | 3D stack renderings, three reconstructed views, two montages | – | – | see "errors" for the view labels |
| Suppl. Fig. 1a–f | schematics, one rendered view, one photograph (scale bar 10 mm) | – | – | |
| Suppl. Fig. 2a, top box | line plot, 2 series (raw spectra vs pixel number), no numbers | `figures/sfig2atop.csv` | 3 digitized | axis fractions; 10 x ticks, 3 y ticks recorded |
| Suppl. Fig. 2a, bottom box | line plot, 2 series (interferogram), no numbers | `figures/sfig2abottom.csv` | 3 digitized | per-column envelope (top/bottom) matters here |
| Suppl. Fig. 2b, top box | line plot, 2 series (dB vs depth, no background subtraction) | `figures/sfig2btop.csv` | 3 digitized | 5 x ticks |
| Suppl. Fig. 2b, bottom box | line plot, 2 series (with background subtraction) | `figures/sfig2bbottom.csv` | 3 digitized | |
| Suppl. Fig. 2c, top image | grey-scale B-scan with unnumbered grey bar | `figures/sfig2ctop.csv` | 3 (raster grid, uncalibrated) | 184 × 714 grey levels; bar ramp sampled in header |
| Suppl. Fig. 2c, bottom image | grey-scale B-scan with unnumbered grey bar | `figures/sfig2cbottom.csv` | 3 (raster grid, uncalibrated) | 184 × 713 grey levels |
| Suppl. Fig. 3a–b | three reconstructed views, two montages (monkey V) | – | – | |
| Suppl. Fig. 4 | optical schematic with legend | – | – | legend transcribed in `\alttext` |

Panels per provenance tier: tier 1: 0; tier 2: 0; tier 3: 6 (the six CSVs above, i.e. the three lettered panels
a–c of Supplemental Fig. 2, each with two sub-plots); tier 4: 0; image-only panels: all the rest.

Notes on Supplemental Fig. 2: the two series of each box are the caption's "blue representing channel 2 and orange
channel 1". Where one trace hides the other, the hidden series has no row in that column. The x ticks of panel a are
evenly spaced at 0.0977 of the box width = 1/10.24, which would fit an axis of 0–1024 camera pixels ticked every 100
(the text says each channel has 1024 pixels); that is my inference, flagged as such in the CSV header, not printed in
the figure. The panel-c grey bars have no numbers, so the grids are the published 8-bit rendering, not dB values;
the bar ramp is linear (sampled 253 → 3 over the bar's interior, see the headers).

## Known problems and oddities in the paper (kept verbatim)

- **Fig. 6 caption vs. image:** the caption says "c. Sagittal (top) and axial (bottom) views", but the top montage
  shows bilaterally symmetric sections (axial-looking) and the bottom montage lateral profiles with the cerebellum
  (sagittal-looking), i.e. the reverse; and "b. Coronal (imaging slice) and axial views" while panel b shows three
  images (the third looks sagittal). Noted in the `\alttext`, not changed.
- Fig. 5 caption ends "in b,c,and d" without a full stop; Fig. 4 caption prints "yellow rectangle ." (space before the
  period); the author list prints "Amy Howard⁹ ," (space before the comma); p. 4 prints "larger brains ¹²,²⁴,²⁸,³⁰"
  (space before the superscript); the citation "16-22" uses a hyphen where the others use en dashes.
- Methods, p. 18, line 330–331: "To improve slice quality, extra care was taken to remove blood vessels and dura
  mater prior to embedding to improve slice quality." (doubled phrase, verbatim).
- The text calls the instrument "VF800" (p. 5) and the supplement "VF-800" (supp. p. 1).
- References 36 and 37 have no journal, year or identifier ("Tendler, B. Diffusion-weighted steady-state free
  precession imaging …"; "Warrington, S. et al. 10.5 Tesla High-Resolution Macaque Brain MRI …"); reference 17
  prints "(CRC Press, Boca Raton : Taylor & Francis, 2017., 2017)" with a narrow no-break space before the colon
  (kept, U+202F).
- "Figs. 4b and 5b)" has the closing parenthesis in bold (p. 11); kept as printed.
- Supplement p. 1 refers to "figure 2d" and "Figure 6" of the main text and to "supplemental figures 1,2, and 4"
  (no space after the first comma).

## Tool and spec notes

- `check_text.py --drop-line-numbers` misses a line number whenever the previous line ends with a hyphen (8 cases
  here): the dehyphenation runs before the line-number filter and glues the number to the word. Suggested fix: drop
  the margin numbers (by position) before joining hyphenated line ends.
- The SPEC's `../tools/` paths are wrong for a folder outside the collection (this one is in `oct_20_compresstome/`);
  all scripts here use the absolute tools path, as the task message asked.
- `digitize_common.tick_positions()` needs the band length to match the tick height (the ticks here are 2 px, the
  default example uses 3): worth saying in its docstring.
- The `\alttext` macro is not `\long`, so a description cannot contain a paragraph break; all descriptions here are
  single paragraphs ("Panel a: … Panel b: …"). A `\long` definition (or `\newcommand` → `\NewDocumentCommand` with
  `+m`) in `decomp.sty` would allow paragraphs in long descriptions.

## Time

About 35 minutes of wall-clock: reading brief/spec/tools and all 28 pages ~6 min; build script, rebuild cycles and
proofreading ~10 min; Supplemental Fig. 2 extraction with overlays and comparisons ~9 min; descriptions,
text_values.csv, README and checks ~10 min.
