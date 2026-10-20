# pesce2022: decompiled

Luca Pesce, Marina Scardigli, Vladislav Gavryusev, Annunziatina Laurino, Giacomo Mazzamuto, Niamh Brady,
Giuseppe Sancataldo, Ludovico Silvestri, Christophe Destrieux, Patrick R. Hof, Irene Costantini, Francesco S. Pavone.
"3D molecular phenotyping of cleared human brain tissues with light-sheet fluorescence microscopy."
*Communications Biology* **5**, 447 (2022). DOI [10.1038/s42003-022-03390-0](https://doi.org/10.1038/s42003-022-03390-0).
Received 19 August 2021; accepted 21 April 2022 (printed on p. 10; the publication date, 12 May 2022, is not printed
in the PDF and comes from `source/SOURCE.txt`). All taken from the PDF; they agree with the task message.

**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), "Open Access" statement on p. 12;
"© The Author(s) 2022". The Peer Review File carries its own CC BY 4.0 statement (p. 1).

Why it is here: the oct_20_compresstome collection (vibratome/Compresstome papers). The sectioning facts are
collected in `tables/text_values.csv` (see below).

## Local and external

**In the local collection**
- Source files (`source/`, see `source/SOURCE.txt`): main article, Supplementary Information, Peer Review File,
  Description of Additional Supplementary Files, Reporting Summary (all born-digital, publisher files).
- `screening.md` and the first five rows of `tables/text_values.csv` were written by an earlier agent from a web read;
  the table rows were verified and corrected against the PDF (below). `screening.md` was not used as a source.

**External pull needed** (not on this machine)
- **Supplementary Movies 1–4** (GIF/MP4 on the publisher page; described in `pesce2022_supplementary_file_descriptions.pdf`,
  transcribed at the end of `supplement.tex`): high-resolution stacks labelled for CR, SST, NeuN and a downscaled NeuN
  reconstruction of Broca's area. Movies, not plot data.
- **DANDI dandiset 000026** (`https://gui.dandiarchive.org/#/dandiset/000026`), named on p. 8 (Discussion) and in the
  Reporting Summary as the data set of the Broca's-area reconstruction (ref. 62, Costantini et al. 2021): image data,
  not the numbers behind any plotted panel. "Raw data other than the representative images are available from the
  corresponding author upon reasonable request" (Data availability, p. 10). The paper has no Source Data file, so
  no plotted panel has a tier-1 source; all plots are vector graphics in the PDFs (tier 2).
- ZetaStitcher (`https://github.com/lens-biophotonics/ZetaStitcher`), the stitching software named in the Methods (p. 10).
- All cited references (70 in the main list; the Peer Review File cites a few more by DOI) without a [local: …] tag.

## Source files (`source/`)

| file | what it is |
|---|---|
| `pesce2022.pdf` | main article, 12 pp. **Publisher version of record** (Springer/iText typesetting; running headers "ARTICLE", footers with the citation line and page numbers, "Check for updates" button, ORCID icons, the vertical "1234567890():,;" stamp on p. 1). Born-digital, embedded fonts. Figs. 2, 4, 5 are 300 ppi raster images; Fig. 1 is a raster (panels a, b) plus vector plots (c–f); Fig. 3 is raster images plus vector bar charts (a, d) whose individual data points are tiny raster tiles. |
| `pesce2022_supplement.pdf` | Supplementary Information (publisher file MOESM2), 17 pp., the authors' Word document: title page, Supplementary Figs. 1–14 (one per page; the profile plots of Figs. 2 and 3 and the bar charts of Figs. 9, 10, 12 are vector graphics, the images raster), Supplementary Tables 1–2 (real text tables). Running header "Pesce et al." and page numbers. |
| `pesce2022_peer_review.pdf` | Peer Review File (MOESM1), 22 pp.: three first-round reports, the authors' point-by-point response (blue text; quoted manuscript text in blue italics) with eight embedded figures (copies/earlier versions of the paper's figures; the Fig. 1 copy on p. 21 is vector graphics), second-round reports and response. |
| `pesce2022_supplementary_file_descriptions.pdf` | Description of Additional Supplementary Files (MOESM3), 1 p.: the four movies. Transcribed at the end of `supplement.tex`. |
| `pesce2022_reporting_summary.pdf` | Nature Portfolio Reporting Summary (MOESM8), 3 pp. Produced by "Microsoft: Print To PDF": **no text layer at all** (no fonts; the text is drawn as outlines), so it was OCRed with tesseract at 300 dpi (`work/rs/`), proofread against the page images. |

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order (journal block, title, authors, affiliations after the author
  list, abstract, introduction (unheaded, with the drop cap rejoined), Results, Discussion, Methods with the bullet lists,
  Data availability, dates, 70 references in `hangpars`, Acknowledgements, Author contributions, Competing interests,
  Additional information, Open Access statement). Figs. 1–5 at their pages with verbatim captions, descriptions and data
  pointers; `\pdfpage{}` at every page. Built by `work/build_main.py` from the PDF text layer (PyMuPDF spans) and then
  proofread; the corrections found in proofreading are the `CORRECTIONS` list in that script.
- `supplement.tex` / `supplement.pdf`: the whole Supplementary Information (`work/build_supp.py`) and, after its own
  `\sourcefile`, the one-page MOESM3 file. Supplementary Tables 1 and 2 as `tabular`s and as `tables/stable1.csv`,
  `tables/stable2.csv`; the value table printed inside Supplementary Fig. 13 as a `tabular` and `figures/sfig13.csv`.
- `peer_review.tex` / `peer_review.pdf`: the Peer Review File verbatim (`work/build_pr.py`), with the authors' replies
  in blue (`\reply{}`), the red comment letters (`\redmark{}`), italics and bold as printed, and the eight embedded
  figures as `figures/prfig_pNN.png` with short descriptions.
- `reporting_summary.tex` / `reporting_summary.pdf`: the Reporting Summary from the OCR (`work/build_rs.py`): the form's
  text and the authors' answers verbatim, tick-box states as `\decompnote{}`s, the grey placeholder sentences of the
  unanswered fields (Data exclusions, Blinding) in italics.
- `figures/`: `fig1.png`–`fig5.png`, `sfig1.png`–`sfig14.png`, `prfig_p7.png` … `prfig_p21.png` (200 dpi crops without
  captions) and, per plotted panel, `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png` (21 panels:
  fig1a–f, fig3a (one CSV for the CR and PV charts), fig3d, sfig2b–e, sfig3b–f, sfig9, sfig10a, sfig10b, sfig12; plus
  `sfig13.csv`, a printed table); shared helper `profiles_common.py` for the 13 profile panels; `fig1b_*.py` import
  from `fig1a_*.py`.
- `tables/`: `stable1.csv`, `stable2.csv` (the paper's tables) and `text_values.csv` (compiler-created: key numbers from
  the running text, each with the PDF page and the printed wording; **not a table of the paper**).
- `work/`: scratch (page renders `work/pages/`, build scripts, `work/alt/` with the figure descriptions, OCR output
  `work/rs/`, the figure agents' overlays and side-by-side comparisons in `work/agent_profiles/` and `work/agent_bars/`,
  check JSON, LaTeX logs). May be deleted except the `build_*.py` scripts and `work/alt/`, which regenerate the .tex files.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (and `supplement.tex`, `peer_review.tex`,
`reporting_summary.tex`) from this folder; all four compile without errors (run twice; a few overfull lines from long URLs).
Rebuild the text: `python3 -I -B work/build_main.py` etc. (they read `source/` and `work/alt/`).
Re-run the data: `python3 -I -B figures/<panel>_extract.py`, then `python3 -I -B figures/<panel>.py`, from any directory.

## The sectioning facts (why this paper is in the collection)

All in `tables/text_values.csv` with page and wording. In short: blocks of "approximately 3 cm³" of hippocampus,
precentral gyrus, prefrontal cortex, motor cortex and Broca's area (3 donors, Supplementary Table 2) were cut with
"a custom-made vibratome (Compresstome VF-900-0Z)" into "450 ± 50 μm-thick coronal sections" (Methods, p. 9; the
Results say "up to 500 μm", everywhere else "500-μm thick"); slices stored at 4 °C in PBS with 0.02 % NaN₃. The paper
gives no embedding medium, blade, speed, amplitude or any other cutting parameter, and no measurement of cutting quality;
the only statements about cutting are that 500 µm "increases by 5 times the slice thickness treated with the classic
SWITCH technique allowing to reduce the cutting artifact and the acquisition times" (p. 2, repeated in the peer-review
response p. 15) and the reply to reviewer 3 that an 8 mm block needs 16 slabs instead of 80 slices (PR pp. 16–17). The
slicing of specimen 2 is credited to Jiarui Yang and David Boas (Boston University) in the Acknowledgements; "C.D.
prepared the human brain slices" (Author contributions).

## Figures

**Provenance.** No source data exist, so the best tier is 2. Every plotted panel of both PDFs is vector graphics
(`vector_dump.py` / `pdfplot.drawings`): the 13 depth-profile panels (Fig. 1c–f, Suppl. Fig. 2b–e, 3b–f) are drawn as
one tiny filled marker per data point (≈1272 per series, one per 0.55 µm camera pixel) plus three polylines per series
(mean and the two ±SD band edges); the bar charts as bar outlines/fills, whisker strokes and marker fills. Two exceptions:
(1) **Fig. 1a, b** are a 300 ppi raster in the main PDF, but the authors' response in the Peer Review File (p. 21)
reproduces the same Fig. 1 as vector graphics, so the bars, SD and the 20 points per bar were taken from that copy
(tier 2) and checked against the published raster (bar tops and SD caps agree within 1.8 native px = 1.4 A.U. in a and 2.4 px = 2.0 A.U. in b;
`work/agent_bars/fig1a_overlay_published.png`, `fig1b_overlay_published.png`); (2) in **Fig. 3a and 3d** the bars and
SD are vector but the individual data points are 16 × 16 px raster tiles, which were located in a 600 dpi render
(tier 3 for the points; see the CSV headers).

**Checks:** for every panel the extracted values were drawn back over a 300 dpi render of the panel
(`work/agent_*/<panel>_overlay.png`) and the re-plot was put next to the original with `tools/compare.py`
(`work/agent_*/cmp_<panel>.png`); both were looked at for every panel (the figure agents and then I): series, ranges,
scales and shapes match. The profile extraction also checks the ±SD band for symmetry about the mean (max asymmetry per
series in each CSV header; ≤ 1.5 units in the supplement, where the lines are exact, and up to 600 units in the main PDF,
where the producer simplified the lines to Bézier curves; the marker centres are exact in both).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | bar chart, 7 groups × 4 excitations, n = 20 points per bar, SD, asterisks | `figures/fig1a.csv` | 2 (vector copy in the Peer Review File, checked against the published raster) | 28 bars, 559 points (AR 488 nm has 19 drawn) |
| Fig. 1b | bar chart, 6 groups × 4 excitations | `figures/fig1b.csv` | 2 (as 1a) | 24 bars |
| Fig. 1c–f | depth profiles, 3 series each, mean ± SD band | `figures/fig1c.csv` … `fig1f.csv` | 2 vector | 1272 points per series; Bézier-simplified band edges (caveat in headers); a hidden older legend in the text layer |
| Fig. 2a | schematic (pipeline) | – | – | transcribed in the description |
| Fig. 2b | timeline table (step, duration) | – | – | durations transcribed in the description (3 d, 2-4 d, 1 h, 10 min, 7-14 d, 1-3 d, 10-20 min, stripping 4 h) |
| Fig. 3a (CR, PV) | two bar charts S/B at 0, 350, 700 µm, 8 points per bar, SD; two strip images | `figures/fig3a.csv` (column `chart`) | 2 bars/SD + 3 points (raster tiles, 600 dpi Hough circles) | 12 bars, 74 of 96 points separable (overlapping discs: cluster ranges in the CSV header); stray axis labels "C", "F" |
| Fig. 3b, c | multi-colour micrographs | – | – | |
| Fig. 3d | bar chart SNR, rounds 1–3, n = 30 points, SD; three images | `figures/fig3d.csv` | 2 bars/SD + 3 points | 3 bars, 90 points; means 3.66, 2.49, 2.28 |
| Fig. 4a–q | photographs and LSFM micrographs | – | – | |
| Fig. 5a, b | LSFM micrographs | – | – | |
| Suppl. Fig. 1 | 13 × 5 micrograph grid | – | – | row label "SWITCH-NaNH4" (sic) |
| Suppl. Fig. 2a | 8 micrographs | – | – | |
| Suppl. Fig. 2b–e | depth profiles, 3–4 series | `figures/sfig2b.csv` … `sfig2e.csv` | 2 vector (exact polylines) | 2d: two series' lower band edge clipped at 0 (flagged) |
| Suppl. Fig. 3a | 12 micrographs | – | – | |
| Suppl. Fig. 3b–f | depth profiles, 2–3 series | `figures/sfig3b.csv` … `sfig3f.csv` | 2 vector (exact) | 3b: the red series starts at 8.3 µm (first points not drawn) |
| Suppl. Fig. 4 | 12 + 3 micrographs | – | – | |
| Suppl. Fig. 5 | 9 micrographs | – | – | |
| Suppl. Fig. 6 | 2 micrographs | – | – | |
| Suppl. Fig. 7 | 4 micrographs | – | – | |
| Suppl. Fig. 8 | 2 micrographs | – | – | |
| Suppl. Fig. 9 | bar chart, 3 bars, 40 points each, SD; 3 images | `figures/sfig9.csv` | 2 vector | legend says n = 3 samples; 40 points per bar are drawn |
| Suppl. Fig. 10a | bar + 3 points (SSIM) | `figures/sfig10a.csv` | 2 vector | hidden earlier labels in the text layer |
| Suppl. Fig. 10b | paired lines, 6 pairs (tortuosity) | `figures/sfig10b.csv` | 2 vector | pairs from the connecting segments |
| Suppl. Fig. 11 | schematic, photographs, 2 resliced images | – | – | |
| Suppl. Fig. 12 | bar chart, 9 bars, 10 points each, SD; images | `figures/sfig12.csv` | 2 vector | markers are ellipses (anisotropic scaling) |
| Suppl. Fig. 13 | printed table + 2 photographs | `figures/sfig13.csv` | printed text (exact) | no plot |
| Suppl. Fig. 14 | 3 × 4 micrographs | – | – | |
| Peer Review p. 7, 8, 9, 12, 19, 21 | copies of Suppl. Fig. 5, Fig. 5a, Suppl. Fig. 14, Suppl. Fig. 7, Suppl. Fig. 10, Fig. 1 | – (p. 21 is the source of fig1a/b) | – | described briefly, pointing to the paper's figure |
| Peer Review p. 13 | earlier Suppl. Fig. 12 (t-test version, no points) | – | – | bar heights read by eye in the description; agree with `sfig12.csv` |
| Peer Review p. 18 | earlier Fig. 3d (no points) | – | – | bar heights read by eye in the description |

**Panels per tier:** 0 tier 1 (no source data exist); 19 panels tier 2 (vector); Fig. 3a and 3d mixed (bars/SD tier 2, the
individual points tier 3 from raster tiles); 0 read by eye. Fig. 2b (a timeline) and the Suppl. Fig. 13 table are
transcribed, not plots.

## Text check (`tools/check_text.py` 2026-10-17j)

| file | options | coverage | without repeated text | running text (also without in-figure text) | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | `--figure-box 3:40,45,555,520 --figure-box 5:60,50,545,289 --figure-box 6:40,45,530,333 --figure-box 7:85,45,515,464 --figure-box 8:110,45,485,266` | 93.6 % | 94.9 % (177 repeated tokens) | **99.6 %** | 0 | 0 |
| `supplement.tex` (vs MOESM2 + MOESM3) | `--figure-box P:50,68,545,Y` for P = 2…15 (Y = 343, 344, 343, 341, 257, 318, 476, 342, 610, 355, 389, 520, 330, 444) | 63.2 % | 67.9 % (212) | **99.2 %** | 0 | 0 |
| `peer_review.tex` | `--figure-box 21:56,275,478,773` | 95.3 % | 95.3 % (0) | **99.9 %** | 0 | 0 |
| `reporting_summary.tex` | – | not checkable: the PDF has no text layer (the tool reports 0 PDF tokens and one EXTRA run of all 1089 tex tokens) | | | | |

The `--figure-box` rectangles are the figure areas (the crop boxes of `figures/*.png`); without them the tool counts
the axis labels, legends and panel labels printed as PDF text beside raster images as missing running text
(main 97.6 %, supplement 87.0 %, peer review 99.0 %). All numbers are from the final files (`work/check_*.json`).

Explanation of what is not matched (`--min-run 1`):
- **main, MISSING:** headers/footers ("ARTICLE", "COMMUNICATIONS BIOLOGY | …", "www.nature.com/commsbio", page numbers),
  the "1234567890():,;" margin stamp, and the figure-internal text (tick labels, legends, panel letters, "Hippocampus",
  "Broca's area", "Multiround", "Merged channels" …), all described in `\alttext`; three line-end hyphens joined by the
  tool but real in the paper ("multi-rounds", "light-sheet"). **EXTRA:** none ≥ 2; "multi" from "multi-rounds".
- **supplement:** page numbers and the running header "Pesce et al."; figure-internal text (row/column labels of
  Suppl. Figs. 1 and 4, strip labels of 2a/3a, tick labels and legends of the plots, "x z" glyph labels); the one EXTRA
  run (2 tokens) is the printed figure title "Stripping efficiency" (p. 10), which the tool counts as in-figure text but
  which is kept as text in `supplement.tex`. Of the supplement's 3081 tokens, 906 are figure labels.
- **peer review:** figure-internal text of the vector Fig. 1 copy (p. 21: tick labels, legends, x labels); line-end
  hyphens joined by the tool ("multi-round", "size-adjustable", "light-sheet", "long-term"). The PDF text layer of the
  response pages is in good shape (no spurious spaces, unlike kubota2018's file).
- **reporting summary:** OCR; every OCR word is in the .tex except the three misreads corrected from the page image
  ("cm43" → "cm^3", "15x1.5x0.5" → "1.5 x 1.5 x 0.5", "intervals}" → "intervals)"), checked by `work/build_rs.py`.

Read-through against the page images (step 4) done for: title block and affiliations (affiliation marks 1–7, ✉),
the SHORT acronym expansions (em dashes, no spaces), subscripts H₂O₂, CuSO₄, NaBH₄, NaN₃ (the text layer sets several of
them at the baseline; the paper itself prints "H²O²" and "CuSO⁴" as superscripts in three places of p. 4, kept), all
"× … cm³/µm²/mm³" exponents, ±, ≈, °C, "3° column", "C + +" (printed with spaces), the Methods bullets, the reference
list (italic journal names, bold volumes), the Supplementary Table cells, the SI captions' symbols (RI ≈ 1.46,
3.5 ± 1.5, "4 °h"), the Reporting Summary tick boxes.

## Errors and oddities in the paper (kept verbatim, flagged with `\decompnote` where they matter)

- p. 2: "volumetric acquisition with LSFM In particular" (no full stop; reviewer 2 asked for it and the authors said
  they corrected it, but the published PDF still lacks it).
- p. 4: "SWICH-processed"; "H²O²" and "CuSO⁴" (superscripts) three times in the "Optimization of SHORT immunostaining"
  paragraph, subscripts elsewhere.
- p. 4: "Sudan Black (SD)" where the abbreviation used everywhere else is SB.
- p. 8: "neuromelin"; "tranced"; Methods p. 9: "Fi. 4b-f", "washed 3 times in PBS for 1 each" (unit missing).
- Fig. 2b timeline prints "Autofluorence treatment".
- Fig. 3a (PV chart): two stray axis labels "C" and "F" between the bar pairs.
- Suppl. Fig. 1 row label "SWITCH-NaNH4" for NaBH4; Suppl. Fig. 5 legend "scale bar 10 = μm"; Suppl. Fig. 9 legend
  "for 4 °h at 80 °C"; Suppl. Fig. 10 legend "post-clearing (red) and after stripping (red)" (the stripping images are
  green) and "not statically significant"; Suppl. Fig. 12 legend "no significant".
- Suppl. Fig. 13: the legend claims "an isotropic tissue shrinkage of a factor of 3.5 ± 1.5", but the table printed in
  the same figure gives areas 7.188/7.181/7.396 cm² (PBS) vs 7.048/6.92/7.027 cm² (SHORT), i.e. 2–4 % smaller.
- Methods p. 9: "Tissue sections of 450 ± 50 μm-thick coronal sections"; everywhere else the slices are "500-μm thick".
- Methods p. 9 says "3 different human donors" and "5 different cortical regions"; the Peer Review File shows the
  submitted version said 5 donors (reviewer 2's comment 1).
- The PDF text layer of Fig. 1c–f and Suppl. Fig. 2b/c/e, 10a/b carries older, invisible (overprinted/white-boxed)
  legend and axis labels (e.g. " 4 °C - SWITCH-OP/AR", " SWITCH-PBST-BSA", "SST - Post Clearing"): remnants of earlier
  figure versions, listed in the CSV headers; the printed names are used.
- Reference 26 is garbled ("Sci. (80-.). 347, 543 LP–543548"); ref. 31's author is "Manuscript, A." (an "Author
  Manuscript" header taken as the author); ref. 62 has no journal (the bioRxiv preprint); ref. 34 prints the DOI inside
  the publisher parentheses.
- Fig. 1 caption: "Sudan black" is "SB"; the caption says the 7 reagents include "SB" while the text lists "Sudan Black
  (SD)". The caption's "Statistical analysis (n = 20)" refers to 20 ROIs (Methods).

## Problems and suggestions for the spec/tools

- `check_text.py`: text labels printed beside (not on) raster images and the tick labels of vector plots that sit
  outside the drawing cluster are not counted as in-figure text, so the "running text" number is misleading without
  `--figure-box` (main 97.6 → 99.6 %, supplement 87.0 → 99.2 %). Suggest growing the image bbox by ~20 pt and treating
  any text inside the bbox of a vector-drawing cluster plus its labels as figure text; or let `--figure-box` take a
  file of rectangles (14 boxes for the supplement made the command line long).
- `check_text.py` has no way to say "this PDF has no text layer"; it reports 0 PDF tokens. A note in the SPEC on
  Print-To-PDF files (text as outlines, OCR needed) would help: the Reporting Summary here is such a file.
- `pdfplot.py`: `text_spans()` returns `bbox` but no `x0/y0` keys (the docstring example in the brief suggested otherwise);
  and there is no helper for tick labels with decimal commas and separate superscript exponent spans ("3,5x10" + "4"),
  which both agents had to write (`profiles_common.y_axis`). Worth adding to `pdfplot.axis_from_labels`.
- Markers as raster tiles inside a vector chart (Fig. 3a/3d: Origin exports translucent markers as 16 × 16 px images,
  split into tiles where they overlap) are not covered by the SPEC's tiers; here bars/SD are tier 2 and the points
  tier 3 within one CSV. A sentence in the SPEC on mixed-tier panels would help.
- `pdfplot.segments` has no colour filter (white "gap" strokes on an axis line and black x ticks at bar centres were
  caught as ticks/whiskers until filtered by colour), and `thin_segments` reports a whisker shorter than wide as
  horizontal; whiskers are also split into pieces where a raster point tile covers them (handled in `fig3a_extract.py`).
- The SPEC's "figures/" layout has no place for figures of a Peer Review File; `prfig_pNN.png` was used.
- `decomp.sty`: DejaVu Serif has no ✉ (U+2709); it is set in `\textsf` here. Adding a fallback font for symbols to the
  style would avoid per-paper fixes.
- The Word-made SI/PR PDFs keep every line-end hyphen real (no automatic hyphenation), the Springer PDF does not: the
  build scripts therefore keep all hyphens for the former and use a word list for the latter; a note in the SPEC would
  save the next agent the check.

## Time

About 2.5 h wall-clock for the text (four .tex files, OCR of the Reporting Summary, descriptions, tables, README),
plus two parallel figure agents for the 22 plotted panels, one of which had to be resumed after an API rate limit.
