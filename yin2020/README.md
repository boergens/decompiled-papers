# yin2020: decompiled

Wenjing Yin, Derrick Brittain, Jay Borseth, Marie E. Scott, Derric Williams, Jedediah Perkins, Christopher S. Own,
Matthew Murfitt, Russel M. Torres, Daniel Kapner, Gayathri Mahalingam, Adam Bleckert, Daniel Castelli, David Reid,
Wei-Chung Allen Lee, Brett J. Graham, Marc Takeno, Daniel J. Bumbarger, Colin Farrell, R. Clay Reid, Nuno Macarico da Costa.
"A petascale automated imaging pipeline for mapping neuronal circuits with high-throughput transmission electron microscopy."
*Nature Communications* **2020**, 11:4949. DOI [10.1038/s41467-020-18659-3](https://doi.org/10.1038/s41467-020-18659-3)
(printed on p. 1 of the PDF; also confirmed by verify-sources receipt `vs-20261013-0f4932043b`, where Crossref resolved the DOI to this
title, Nature Communications vol. 11, not retracted).
Received 27 November 2019; accepted 28 August 2020; published online 02 October 2020.

**Licence:** open access under the Creative Commons Attribution 4.0 International License (CC BY 4.0), "© The Author(s) 2020", p. 12.

## Source files

| file | what it is |
|---|---|
| `source/yin2020.pdf` | the article, 12 pp. **Publisher version of record** (Springer Nature typesetting, PDF metadata "Nature Communications, doi:10.1038/s41467-020-18659-3", producer iText/Springer). Copied from `papers/yin2020/yin2020.pdf`; `papers/yin2020/SOURCE.txt` says: "yin2020.pdf: https://www.nature.com/articles/s41467-020-18659-3.pdf (curl, 2026-10-12)". |

`papers/yin2020/` also holds `yin2020.txt` and `yin2020.raw.txt` (earlier text extractions, not used).

**Not available here** (named by the paper, not in `papers/yin2020/`):
- the Supplementary Information (Supplementary Figs. 1–10, Supplementary Table 1, Supplementary Movies 1 and 2), at https://doi.org/10.1038/s41467-020-18659-3;
- the Nature Research Reporting Summary and the peer review file;
- the data named in the Data availability statement (http://www.microns-explorer.org, https://github.com/AllenInstitute/piTEAM) and the code/hardware drawings of the Code availability statement (same GitHub repository).
None of these is a source-data file for the plotted panels (Fig. 4f, g); no tier-1 data exist for them as far as the paper says.

Born-digital PDF with a clean text layer (Adobe "Adv" fonts, Unicode mapped), not a scan. `tools/glyph_audit.py` lists
**4 hidden glyphs**, all in the two Methods equations on p. 10 (U+0002 ×2 = the minus signs of Eq. 1; U+0003/U+0004 = the
radical sign pieces of Eq. 2); all 4 crops (`work/glyphs/`) were checked and Eqs. (1) and (2) are written out in full in `main.tex`.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: article-type and journal block, title, authors, the p. 1
  footnote (affiliations, equal contribution, e-mail; placed after the author list), abstract, introduction, Results, Discussion,
  Methods (incl. Eqs. 1–2), Data availability, Code availability, dates, 38 references, Acknowledgements, Author contributions,
  Competing interests, Additional information, open-access licence. Table 1 as a `tabular`. Five figures with verbatim captions,
  `\alttext` descriptions of every panel, and `\figuredata` for the three plotted panels.
- `figures/`: `fig1.png` … `fig5.png` (rendered from the PDF at 200 dpi, without captions); `fig4ftop`, `fig4fbottom`, `fig4g`:
  `.csv`, `_extract.py`, `.py`, `_replot.png`.
- `tables/table1.csv`: Table 1 (caption and footnote in `#` lines).
- `tools/`: `digitize_common.py` (copied from the osmium tools) and `hist4f.py` (shared digitizer of the two Fig. 4f histograms).
- `decomp.sty`: copied from the osmium tools, so `lualatex -interaction=nonstopmode -halt-on-error main.tex` compiles in this folder.
- `work/`: scratch (page renders, embedded images, overlays `*_overlay.png`, side-by-side checks `cmp_*.png`, text-layer drafts,
  `draft.py` that produced the first text draft, check JSON). May be deleted.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice) from this folder: no errors, no missing characters
(the ✉ e-mail symbol is set in DejaVu Sans), 11 overfull-box warnings from long URLs and the long decompiler note.

Re-run the data: `python3 -I -B figures/<panel>_extract.py` then `python3 -I -B figures/<panel>.py` (any working directory;
the scripts read `source/yin2020.pdf` relative to themselves).

## Figures

No figure has vector plot data: `vector_dump.py` on the Fig. 4f/g area finds 0 paths; the plots are embedded raster images
(Fig. 4f: two 300 ppi images, ~665 × 334 px; Fig. 4g: a 300 ppi JPEG, 768 × 515 px) with the tick labels and axis titles set as
PDF text around them. Tick marks are inside the images, so the axes were calibrated on the tick marks found in the image; the
centres of the PDF-text tick labels, mapped into image pixels, agree with them to ≤ 1.6 px (Fig. 4f). All three plotted
panels are **tier 3 (digitized)**.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | flow diagram with drawings and a photograph (sample preparation) | – | – | |
| Fig. 1b | schematic, six microscopes | – | – | |
| Fig. 1c | photograph of an autoTEM | – | – | |
| Fig. 2a | block diagram (software architecture) | – | – | |
| Fig. 2b | GUI screenshot | – | – | small status texts transcribed in `\alttext` from a zoom of the 300 ppi image |
| Fig. 2c | timing diagram (TEM Graph) | – | – | all labels transcribed |
| Fig. 2d | flowchart | – | – | all labels transcribed |
| Fig. 3a | schematic (tile overlap, templates) | – | – | |
| Fig. 3b | two montage QC maps ("Good", "Bad") | – | – | |
| Fig. 3c–f | four QC colour maps | – | – | no colour keys: description only (coordinator's rule) |
| Fig. 4a | schematic (cube scaling) | – | – | 10 × 10 cells on the front face (counted in the image) |
| Fig. 4b | TEM micrograph, tinted somata/glia | – | – | |
| Fig. 4c, d | TEM micrographs (synapses), tinted | – | – | |
| Fig. 4e | low-mag image, montage stack, 3D rendering | – | – | |
| Fig. 4f (top) | histogram, montage rate, 20 MPixel | `figures/fig4ftop.csv` | 3 digitized | 29 bins of 0.070 fps; counts ±1; sum 1325 |
| Fig. 4f (bottom) | histogram, montage rate, 50 MPixel | `figures/fig4fbottom.csv` | 3 digitized | 28 bins of 0.070 fps; counts ±1; sum 1439 |
| Fig. 4g | histogram + fitted curve, stage step-and-settle time | `figures/fig4g.csv` | 3 digitized | 21 bins of 0.0028 s + curve; 2 bar tops hidden by the curve (flagged with their possible range) |
| Fig. 5 | roadmap graphic with drawings, a photograph and an inset schematic | – | – | |

Fig. 4f has no panel letters for its two histograms; "top"/"bottom" are my names, used in file names only.

**Checks.** Every extraction draws its points back onto the source image (`work/fig4ftop_overlay.png`,
`work/fig4fbottom_overlay.png`, `work/fig4g_overlay.png`): the bar-top marks sit on the bar tops and the curve trace on the blue
line; I looked at all three (and a 2× zoom of the Fig. 4g peak). Every replot was put next to the original panel with
`tools/compare.py` (`work/cmp_fig4ftop.png`, `work/cmp_fig4fbottom.png`, `work/cmp_fig4g.png`) and looked at: ranges, ticks,
bar positions and heights and the curve match.

Details of the digitization:
- **Fig. 4f**: solid-blue bars, no outlines; bin grid from the steps of the bar tops (12.0 px = 0.0700 fps); sub-pixel top edge
  from the partial coverage of the first blue row; counts as read (`count_read`) and rounded (`count`). The read values sit
  consistently ~0.3 above whole numbers, a small offset of the baseline estimate; rounding takes care of it, uncertainty ±1 count.
- **Fig. 4g**: JPEG with semi-transparent bars, dark outlines and a thick curve drawn on top, so automatic colour masks did not
  work at first (the curve's pale JPEG fringe and its dark edges were taken for bar tops). The final script finds each bar's top as
  the topmost horizontal grey outline row (light above, bar fill with G − R ≤ 4 below, seen in ≥ 2 adjacent columns); where the
  curve covers the whole top (2 bins) it gives the middle of the curve band and the possible range. Three bar heights were checked by
  eye on a 6× zoom (≈ 12.0, 19.0 and 26.6 counts at 0.085–0.094 s) and agree with the CSV to ≤ 0.1 count. The heights are **not**
  whole numbers (e.g. 26.6), so they are not rounded.

**Cross-checks with the text** (my calculations from the CSVs):
- Fig. 4f top (20 MP): count-weighted mean of the bin centres 3.18 fps, n = 1325; the text says the net speed "averaged 3.3 frames
  per second (fps)" (p. 6) and Table 1 gives 3.2–3.5 Hz. Bottom (50 MP): mean 3.48 fps, n = 1439, Table 1 3.2–3.5 Hz (peak 4.0). Both n
  agree with the caption's "a sample size of over 1000 sections ... each".
- Fig. 4g: bars from ~0.077 to ~0.136 s, highest at 0.100–0.105 s, height-weighted mean 0.103 s (sum of bar heights 354.5). The text
  says "an average around 100 ms" (p. 6, for the light-weight piezo stage, while the caption says "for GridStage") and "over 100 ms"
  for the GridStage (p. 9); the Methods say the step-and-settle time "is averaged at ∼120 ms" (p. 10).

## Text check (`check_text.py` 2026-10-17j)

Run from this folder:
`python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/yin2020.pdf [options]`

| options | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without in-figure text) | tex tokens found in PDF |
|---|---|---|---|---|
| none | 96.5 % | 96.7 % (34 repeated tokens) | 98.2 % (168 in-figure tokens) | 99.9 % |
| `--figure-box 3:85,50,512,378 --figure-box 4:62,50,524,640 --figure-box 6:44,52,292,433 --figure-box 7:85,46,512,556 --figure-box 8:85,278,512,495` | 96.5 % | 96.7 % | **99.6 %** (317 in-figure tokens) | 99.9 % |

The figure boxes are the figure crops of Figs. 1–5 (PDF points). They are needed because much figure text (the Fig. 2c titles,
the Fig. 4f/g tick labels and axis titles, Fig. 5 labels) is PDF text placed *around* raster images, so the tool's automatic
figure detection misses it. All of that text is transcribed in the `\alttext` descriptions.

Unmatched text (`--min-run 1`, with the figure boxes):
- MISSING: running headers/footers ("ARTICLE", "NATURE COMMUNICATIONS", page numbers; the journal block is given once on p. 1),
  the margin string "1234567890():,;" on p. 1 (boilerplate); the PDF glyphs of Eqs. (1)–(2) on p. 10 ("¼", "ð", "þ", the radical
  drawn as a run of "ffi" ligature glyphs: equation tokens, the equations are in LaTeX math); two real hyphens at line ends that the
  tool joins: "post-processing" (p. 5) and the DOI "s41467-020-18659-3" (p. 12). No prose word is missing.
- EXTRA: "re dft i 2 im dft i 2" (Eq. 2 in LaTeX math, the PDF has broken glyphs there) and "Published online … October" (3 tokens:
  the line "Published online: 02 October 2020" is printed as a small 1-bit image on p. 11, not as text; transcribed from the image,
  with a `\decompnote`).

Read-through against the page images (step 4) done for: superscript citations, mm²/mm³/µm²,
C⁺⁺, Sprite™/Cricket™ (superscript TM), LaB₆ (subscript only in "(LaB6)" in the
running text; the heading and the other three mentions print "LaB6" on the line), × in dimensions, ≥ in the Fig. 1 caption, the
tildes (all written ∼), the en dashes in ranges, Eqs. (1) and (2), Table 1 cells, italics (pyTEM, TEM graph, z, x, y, X, Y, journal
names) and bold reference volumes.

## Errors and oddities in the paper (kept verbatim)

- References 35 and 36 are word-for-word repeats of references 15 and 16 (Dorkenwald et al.; Schneider-Mizell et al.). They are cited
  for the "stick-type GridStage Sprite" (p. 6), which those two bioRxiv papers presumably are not about; probably wrong references.
- Methods, Image processing: "https://github.com/saalfeldlab/render10" — the reference number 10 is run into the URL at full size
  (`\decompnote` in main.tex).
- "focus ion beam scanning electron microcopy (FIB-SEM)" (p. 2): "microcopy" for "microscopy" (and "focus" for "focused").
- "20–26 C" (p. 9) is printed without a degree sign; "10 mm s^−1" (p. 10) is printed with a literal caret.
- Ref. 5 gives the journal as "Sci. (80-.)" (a reference-manager artefact for *Science*); ref. 30 spells the author "EBERLE"; ref. 38
  has no volume or pages.
- Fig. 4b labels the box for panel c with a capital "C" (the panel itself is "c").
- Five vs six microscopes: the 1 mm³ sections "were continuously imaged across five microscopes" (p. 6), while the abstract speaks of
  "six microscopes running in parallel" and the Discussion of "our six-microscope piTEAM platform" (p. 9).
- The introduction lists "low signal-to-noise" among the pipeline's advantages (p. 2), next to "TEMs achieve perhaps the highest
  signal-to-noise ratio"; probably a slip for high signal-to-noise / low noise.
- Table 1: FOV per side 21 µm with AOV 468 µm² (21² = 441; 468 µm² is a 21.6 µm side, = 5408 px × 4 nm), i.e. the 21 is rounded;
  "Tiles w/overlap" for the 50 MP average is 2916 while the text gives "∼2600" (the "50 Mpixel peak" column value).
- Step-and-settle times: ∼100 ms in Results (Fig. 4g) vs "averaged at ∼120 ms" in Methods (see cross-checks above).

## References in our collection

From `decompile_work/manifest.json` keys, checked against the first page of each local PDF:
- ref. 6 Denk & Horstmann 2004 → `denk2004`
- ref. 8 Xu et al. 2017 (eLife 6, e25916) → `xu2017`
- ref. 9 Hayworth et al. 2015 (Nat. Methods 12, 319) → `hayworth2015`
- ref. 10 Zheng et al. 2018 (Cell) → `zheng2018` (the local copy is the 2017 bioRxiv preprint 140905, another version)
- ref. 11 Hayworth et al. 2014 (Front. Neural Circuits 8, 68) → `hayworth2014`
- ref. 20 Hildebrand et al. 2017 (Nature) → `hildebrand2017` (the local copy is the bioRxiv preprint 134882, another version)
- ref. 22 Lee et al. 2016 (Nature 532, 370) → `lee2016` (PMC author manuscript)
- ref. 17 Xu et al. 2020, bioRxiv "A Connectome of the Adult *Drosophila* Central Brain" → `scheffer2020` is the eLife article "A
  connectome and analysis of the adult Drosophila central brain"; that it is the published version of ref. 17 is my background
  knowledge, not checked here.
(`wanner2015` is a different Wanner paper (J. Microsc. 2015), not ref. 28.)

## Open problems

- Supplementary Information (Supplementary Figs. 1–10, Table 1, Movies 1–2), Reporting Summary and peer review file not available
  locally (https://doi.org/10.1038/s41467-020-18659-3).
- Data/code named in the availability statements (microns-explorer.org, github.com/AllenInstitute/piTEAM) not fetched.
- Fig. 4g: two bar tops (bins at 0.1249–0.1277 s and 0.1277–0.1305 s) are hidden under the fitted curve and are given as the curve-band
  centre with a range (±0.2 count); bars lower than ~0.5 count outside 0.077–0.136 s cannot be seen under the curve's flat tails.
