# xu2017: decompiled

C Shan Xu, Kenneth J Hayworth, Zhiyuan Lu, Patricia Grob, Ahmed M Hassan, José G García-Cerdán, Krishna K Niyogi,
Eva Nogales, Richard J Weinberg, Harald F Hess. "Enhanced FIB-SEM systems for large-volume 3D imaging."
*eLife* **2017**;6:e25916 (Tools and Resources; Cell Biology, Neuroscience). DOI
[10.7554/eLife.25916](https://doi.org/10.7554/eLife.25916) (printed on every page of the PDF).
Received 10 February 2017; accepted 09 May 2017; published 13 May 2017. Reviewing editor: Jeremy Nathans.

**Licence:** Copyright Xu et al.; distributed under the Creative Commons Attribution License (CC BY), as stated on p. 1.

**DOI check:** verify-sources receipt `vs-20261013-106e540c2a` (Crossref resolved 10.7554/eLife.25916 and matched it to this
PDF, same 26 438 351 bytes).

## Source files

| file | what it is |
|---|---|
| `source/elife-25916-v3.pdf` | the article, 36 pp., eLife typeset **publisher version of record** (file version 3; Arbortext/Ghostscript PDF of 21 June 2017). Copied from `papers/xu2017/`; `SOURCE.txt` there says: "elife-25916-v3.pdf: https://cdn.elifesciences.org/articles/25916/elife-25916-v3.pdf (curl, 2026-10-12)". |

`papers/xu2017/` also holds `elife-25916-v3.txt` / `.raw.txt` (earlier text extractions; the `.raw.txt` was not used, the
draft text came from the PDF's text layer via `work/draft.py` and was proofread against the page images).

Cited works that are in this collection (from `decompile_work/manifest.json`): **hayworth2015** (Hayworth et al., 2015),
**denk2004** (Denk and Horstmann, 2004), **wanner2015** (Wanner et al., 2015), **bouwer2016** (cited as "Bouwer et al., 2016";
the reference list gives 2017, *Advanced Structural and Chemical Imaging* 2:11).

### Not available (named by the paper, not in `papers/xu2017/`)

- **Videos 1–8** (eLife video files); only the still frames printed in the PDF are here (`figures/video1.png` … `video8.png`).
- **Figure 12—figure supplement 1** ("Enlarged figures from Figure 12 to illustrate the manual thresholding method of Nm and
  Nc estimates", DOI 10.7554/eLife.25916.023): the PDF prints only its title; the image and legend are on the eLife web
  page / API (`papers/xu2017/elife_figure_supplements/` does not exist).
- **Source code 1** ("3D FIB-SEM LabVIEW codes", DOI 10.7554/eLife.25916.031), a download on the eLife page.
- No source-data files are named, so no plotted panel has a tier-1 source.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block (once), title, authors, affiliations, the p. 1
  margin column (correspondence, present address, competing interests, funding pointer, dates, reviewing editor, copyright
  licence; placed after the affiliations, noted), abstract, eLife digest (placed after the paragraph it interrupts, noted),
  all sections of Introduction, Results and discussion, Technology and methods, Acknowledgements, Additional information
  (funding table, author contributions, ORCIDs, ethics), Additional files, and the 44 references, plus all 19 figures, 8 video
  stills and the figure-supplement title with verbatim captions, `\alttext` descriptions and `\figuredata` lines.
  Figures are placed after the paragraph that spans their position; `\decompnote`s say where each is printed.
- `figures/`: every figure and video still rendered at 200 dpi from its embedded-image bbox (`fig1.png` … `fig19.png`,
  `video1.png` … `video8.png`); per plotted panel `<panel>.csv`, `<panel>.py` (re-plot) and `<panel>_replot.png`, and the
  extraction scripts `*_extract.py` (some shared by panels of one figure: `fig12b_extract.py`, `fig12e_extract.py`,
  `fig13_extract.py`, `fig14bd_extract.py`, `fig15b_extract.py`, `fig16ab_extract.py`, `fig17abc_extract.py`,
  `fig17de_extract.py`, `fig1_extract.py`). The Fig. 17(a–c) data are gzipped (`fig17a.csv.gz` …).
- `tables/`: tables printed as images inside figures, transcribed: `fig9a_interrupts.csv`, `fig9a_challenges.csv`,
  `fig9b_solutions.csv`, `fig11j.csv`, `fig12f.csv`, `fig13_tables.csv`, `fig15a.csv`; and the funding table `funding.csv`.
  The paper has no numbered tables.
- `tools/`: `digitize_common.py` (copied from the osmium tools, unchanged) and `xu_helpers.py` (this paper's helpers:
  image loading, blob centroids, log/linear maps, splitting touching circular markers by circle fits).
- `decomp.sty`; `work/` (scratch: page renders, drafts, overlays `*_overlay.png`, comparisons `cmp_*.png`, check output,
  `PROGRESS.md`). May be deleted.

Compile from this folder: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice). Compiles without errors
(34 overfull-box warnings from long URLs, DOIs and the funding table). Re-run data: `python3 -I -B figures/<x>_extract.py`,
then `python3 -I -B figures/<panel>.py` (any working directory; all paths are relative to the scripts).

## Figures

All figures are raster images (JPEG/Flate, 300–441 ppi; a few video stills at 75–300 ppi); `get_drawings()` and
`vector_dump.py`-style checks find no vector paths or text inside any figure area, so no panel is tier 2. Every plotted panel
is **tier 3 (digitized)** from the embedded image at native resolution. Each extraction writes an overlay of the extracted
points on the source image (`work/<panel>_overlay.png` / `work/fig..._ov.png`) and each re-plot was put next to the
original with `tools/compare.py` (`work/cmp_*.png`); I looked at both for every panel and fixed the extractions until all
series, ranges and scales matched (fixes included: dropping frame tick marks picked up as data in Figs. 12e, 15b, 16;
masking the "1 μm" scale-bar label inside Fig. 12b; trimming the frame outline from the Fig. 14b boundary; a band-boundary
column that ran through label text in Fig. 1).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Video 1–8 | video stills | – | – | videos not available |
| Fig. 1 | chart of coloured regions, log–log axes, 3 red contours, star | `figures/fig1.csv` | 3 | region corners, contour end points, star; axes exact to the pixel |
| Fig. 2 | 3D renderings + orthoslices | – | – | |
| Fig. 3a–c | 3D rendering, FIB-SEM re-slices | – | – | |
| Fig. 4a–c | 3D rendering, colour-coded segmentations | – | – | |
| Fig. 5a–e | micro-CT renderings, light micrographs, photo, FIB-SEM | – | – | |
| Fig. 6a,b | FIB-SEM images | – | – | |
| Fig. 7a–d | FIB-SEM images | – | – | |
| Fig. 8a–c | 3D renderings | – | – | |
| Fig. 9a,b | tables printed as an image | `tables/fig9a_*.csv`, `fig9b_solutions.csv` | – | transcribed |
| Fig. 10 | CAD rendering + block diagram | – | – | |
| Fig. 11a–i | SEM images | – | – | |
| Fig. 11j | table (image) | `tables/fig11j.csv` | – | transcribed; all SNR/contrast values consistent |
| Fig. 12a, c, d | image strips | – | – | |
| Fig. 12b | line profile, y without numbers | `figures/fig12b.csv` | 3 | y from the caption's 0–4000 range (assumption, confirmed by panel f) |
| Fig. 12e | 9 histograms, log x, no y scale | `figures/fig12e.csv`, `fig12e_markers.csv` | 3 | heights as box fraction; Nc/Nm marker lines |
| Fig. 12f | table (image) | `tables/fig12f.csv` | – | transcribed |
| Fig. 13 (left, middle, right) | 3 dense Monte Carlo scatter plots | `figures/fig13left.csv`, `fig13middle.csv`, `fig13right.csv` | 3 | ink-density grids (2° × 0.025 keV), not counts |
| Fig. 13 tables | 3 tables (image) | `tables/fig13_tables.csv` | – | transcribed |
| Fig. 14a, c | electron-trajectory simulations | – | – | |
| Fig. 14b, d | detection maps (scatter + boundary) | `figures/fig14b.csv`, `fig14d.csv` | 3 | yellow boundary + reference dots; the ~10 000 electrons not extracted |
| Fig. 15a | table (image) | `tables/fig15a.csv` | – | transcribed |
| Fig. 15b | line + markers, log y | `figures/fig15b.csv` | 3 | |
| Fig. 16a, b (images) | FIB-SEM images | – | – | |
| Fig. 16a, b (profiles) | line profiles | `figures/fig16a.csv`, `fig16b.csv` | 3 | x has no scale (fraction of frame) |
| Fig. 17a, b, c | Monte Carlo maps, colour = energy (colour bar) | `figures/fig17a.csv.gz`, `fig17b.csv.gz`, `fig17c.csv.gz` | 3 | one row per coloured pixel; energies < ~250 eV indistinguishable from black |
| Fig. 17d, e | scatter (2 series) | `figures/fig17d.csv`, `fig17e.csv` | 3 | touching markers split by circle fits |
| Fig. 18 | schematic + photo | – | – | |
| Fig. 19 | 4 × 6 image grid | – | – | |

**Panels per provenance tier:** tier 1: 0; tier 2: 0; tier 3: 16 (Fig. 1, 12b, 12e, 13 left/middle/right, 14b, 14d, 15b,
16a, 16b, 17a, 17b, 17c, 17d, 17e); tier 4: 0. Plus 8 tables transcribed from figure images.

**Cross-checks of digitized data against numbers printed in the paper:**
- Fig. 12b plateau medians vs (Nm+Nc)/2 from Fig. 12f: 1297/1325, 1665/1655, 2003/2055, 2757/2745, 3021/3070, 3166/3160,
  1279/1275, 685/675, 490/497 counts (within 2.5 %), which confirms the assumed 0–4000 y calibration.
- Fig. 12e marker lines vs table f: e.g. −600 V 1254/1362 vs Nc 1270 / Nm 1380; 0 V 2584/2879 vs 2594/2896; 800 V 442/519 vs
  458/536 (within ~4 %). At −200 V a third short line at 1830 is picked up (probably part of the outline); kept, see CSV.
- Fig. 16a profile: epoxy part averages 484 counts (printed 478), Pt Tetrakis part 634 (printed 634); 16b epoxy 481
  (printed 468; the noisy line's mid-band is biased slightly upward).
- Fig. 17e: the 50 % points of the Z step edge come out at about 4.7 nm (800 V) and 11.4 nm (1200 V); the text says 5 nm and
  11 nm. Fig. 17d: the 800 V step at x = 0 is from 8.70 to 9.74 (about half of the 8.31→10.24 rise), consistent with "about
  half … within 1.0 nm".
- Fig. 14b/d: the reference dots come out at 1100/600/50 eV (b, after calibrating on the tick labels) and 1100/601/51 eV (d).
- Fig. 1: the yellow star is at 1006 μm (≈ 1 mm, i.e. 1 mm³), 16 nm.

## Text check (`check_text.py` version 2026-10-17j, no options)

`python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/elife-25916-v3.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 99.1 % | **99.7 %** (108 repeated tokens: the "n of 36" footer) | 99.7 % | 99.7 % | 0 | 0 |

With `--min-run 1`: 56 MISSING runs (65 tokens) and 47 EXTRA runs (48 tokens), all explained:
- **μ** is stored in the text layer as "m" (font AdvP697C), so every "μm" is "mm" in the PDF (≈ 45 runs both ways);
- the same symbol font stores ∼ as "~", π as "p" and δ as "d" (p. 9 "2π", p. 33 "I(δ)", "δ³");
- the focus-index equation on p. 17 (broken math fonts: "¼" for =, "ð Þ" for parentheses, a row of "ﬃ" for the root bar);
- "μs" on pp. 21 and 32; real hyphens at line ends that the checker joins ("large-volume" in the title, "energy-angle" p. 23);
- the running header "TOOLS AND RESOURCES" / "Tools and resources Cell Biology Neuroscience" (given once at the top).

**Hidden glyphs (`decompile_work/tools/glyph_audit.py --crops work/glyphs`): 50**, all checked against their crops
(`work/glyph_montage.png`): 39 × U+0002 = "×" (all 39 "×" are in main.tex), 9 × U+0000 = "−" (pp. 17, 22, 23, 25, 29; all
present), 2 × U+0003 = "∗" (convolution in the p. 17 equation, written `\ast`).

Read-through against the page images (step 4) done for: the p. 17 equation, the SNR formulas on pp. 20–22 (italic N with
subscripts m, c, p, e-), chemical formulas Pt[(C₆H₅)₃P]₄, C₂₁H₂₅O₅, C₄₂H₈₀N₁O₈P₁Os₁.₀, Os₀.₈, X_Os/x_Os, superscripts
(μm³, nm³, 10⁶, Ga⁺, (100 μm)³), "≲1%" on p. 22 (stored as "<" + "~"), degree signs (˚ as printed; "90o" with a superscript o
in the Fig. 14 caption), ±, en dashes, the accents in García-Cerdán and Mendonça, and the order of text around every figure.

## Errors and oddities in the paper (kept verbatim)

- Fig. 15b: the x axis is labelled "Landing Energy (eV)" but its numbers (0.6, 1.0, 1.4) are keV.
- Fig. 13 caption: Pt Tetrakis "with 15% by weight of high Z element"; the text says 16 % (pp. 23, 26).
- Fig. 13 and Fig. 15a tables disagree on model values at 1.2 keV: epoxy masked 3.9 % vs 4.2 %, detection efficiency 47 %
  vs 50.6 %; Pt Tetrakis total 10.4 % vs 10.3 %, masked 5.2 % vs 5.5 %, efficiency 50 % vs 53.1 %.
- Fig. 13/15a: measured Pt Tetrakis detection efficiency printed as 60 % although 7.3 / 12.7 = 57.5 %; Fig. 15a gold
  measured 54 % at 1.0 keV (14/27 = 51.9 %) and 47 % at 0.8 keV (14/29 = 48.3 %).
- Fig. 12f: Nm − Nc printed 303, 91, 79 where Nm − Nc = 302, 90, 78; SNR Measured 5.6 at 400 V where 354/65 = 5.45 (others
  agree to rounding; details in `tables/fig12f.csv`).
- p. 9: "(referenced to a 25–75% step edge rise resolution criteria, consistent with … (spatial period = 21 nm/2π)." – the
  first parenthesis is never closed (decompnote in main.tex).
- p. 24: "back-scatted electrons" (typo); p. 23: "triphyenylphosphine" (typo); Fig. 15a: "Lechitin"; Fig. 18: "Embeding".
- p. 21: "a positive bias of the specimen above 500 eV" (a voltage given in eV).
- In-text "Bouwer et al., 2016" vs reference-list year 2017; "Takemura et al., submitted" (p. 6) has no reference entry;
  Hanslovsky et al. "2014" carries an ISBI 2015 DOI.
- Fig. 9: "System Drifting (nm to sub mm)" as printed (possibly meant sub-μm; the image clearly shows "mm").

## Known limitations

- Fig. 12b: the y scale is an assumption from the caption (0–4000), cross-checked against panel f (above).
- Fig. 13: ink density, not electron counts; saturated near 1.2 keV in the gold plot; bins under the dashed window lines and
  under the printed sample labels use fewer pixels or are omitted.
- Fig. 17a/c: the only colour bar is printed in (b) ("1.2 KeV" at the top); whether (a)/(c) (0.8 keV) share that scale or use
  one normalised to 0.8 keV is not stated (CSV gives the bar fraction as well as energies on the printed scale). Energies
  below ~250 eV cannot be separated from the black background.
- Fig. 14b/d: the ~10 000 simulated electrons are not extracted (too dense); only the boundary and the reference dots.
- Fig. 12e: the first ~8 px inside each box are skipped (frame ticks), which cuts the rising flank of the 800 V histogram.
