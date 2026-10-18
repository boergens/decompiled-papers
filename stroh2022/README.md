# stroh2022: decompiled

Sebastian Ströh, Eric W Hammerschmith, David W Tank, H Sebastian Seung, Adrian Andreas Wanner.
"In situ X-ray-assisted electron microscopy staining for large biological samples."
*eLife* **2022**;11:e72147. DOI [10.7554/eLife.72147](https://doi.org/10.7554/eLife.72147).
Preprinted 20 June 2021; received 13 July 2021; accepted 18 October 2022; published 20 October 2022.

**Licence:** CC BY 4.0 ("distributed under the terms of the Creative Commons Attribution License", p. 1).

## Local and external

**In the local collection**
- Source files:
  - `papers/stroh2022/elife-72147-v2.pdf` – main article, 19 pp., eLife version of record
  - `papers/stroh2022/elife-72147-fig1-data1-v2.pdf`, `papers/stroh2022/elife-72147-fig1-data2-v2.pdf`, `papers/stroh2022/elife-72147-fig1-data3-v2.pdf`, `papers/stroh2022/elife-72147-fig1-data4-v2.pdf`, `papers/stroh2022/elife-72147-fig1-data5-v2.pdf`, `papers/stroh2022/elife-72147-fig2-data1-v2.pdf`, `papers/stroh2022/elife-72147-fig2-data2-v2.pdf` – the 7 "Source data" files of Figures 1 and 2: image-only per-sample plots, no numbers (→ `decompiled/stroh2022/source_data.tex`)
  - `papers/stroh2022/elife_figure_supplements/` – the 8 figure supplements as full-size JPEGs (fig1-figsupp1–3, fig2-figsupp1–5), `papers/stroh2022/elife_figure_supplements/elife_api_article.json` (their legends) and a SOURCE.txt (→ `decompiled/stroh2022/supplement.tex`)
  - `papers/stroh2022/elife-72147-v2.txt`, `papers/stroh2022/elife-72147-v2.raw.txt` – earlier text extractions (the .raw.txt was the transcription's starting point)
- Cited works decompiled here: genoud2018 (`decompiled/genoud2018/`), hua2015 (`decompiled/hua2015/`), kasthuri2015 (`decompiled/kasthuri2015/`), korn1967 (`decompiled/korn1967/`), litman1972 (`decompiled/litman1972/`), mikula2015 (`decompiled/mikula2015/`), seligman1966 (`decompiled/seligman1966/`), white1976 (`decompiled/white1976/`)

**External pull needed** (not on this machine)
- X-ray data set EMPIAR-10782 – https://www.ebi.ac.uk/empiar/EMPIAR-10782/ – the raw projection images; tier-1 source for every plotted panel (all are tier 3 here)
- Code – https://github.com/adwanner/XrayAssistedStaining (archived as swh:1:rev:62c9930d08bbdd1602614d515cd20b1cb1f89d15) – analysis and heavy-metal accumulation model; code only, no data
- Transparent reporting form (Supplementary files) – no link given – not needed for the decompile
- Decision letter and author response – https://doi.org/10.7554/eLife.72147.sa1, https://doi.org/10.7554/eLife.72147.sa2 – not needed for the decompile
- All other cited references: 70 entries in the reference list (78 unnumbered, alphabetical entries) without a [local: …] tag.

## Source files (`../../papers/stroh2022/`)

| file | what it is |
|---|---|
| `elife-72147-v2.pdf` | main article, 19 pp., **publisher version of record** (eLife typesetting, "Tools and resources", running footer "Ströh, Hammerschmith et al. eLife 2022;11:e72147 … n of 19"). It prints only the *titles* of the figure supplements, not their images or full legends. |
| `elife-72147-fig1-data1-v2.pdf` … `fig1-data5-v2.pdf`, `fig2-data1-v2.pdf`, `fig2-data2-v2.pdf` | the 7 "Source data" files of Figures 1 and 2: image-only PDFs (no text layer), one 2441 × 1370 px MATLAB figure per sample (13 + 6 + 4 + 4 + 2 + 6 + 4 = 39 pages). They hold per-sample plots, **no numbers**. |
| `elife_figure_supplements/fig1-figsupp1..3.jpg`, `fig2-figsupp1..5.jpg`, `elife_api_article.json`, `SOURCE.txt` | the 8 figure-supplement images (full-size JPEGs from iiif.elifesciences.org) and the eLife API record holding their full legends (added by the coordinator during the work). |
| `elife-72147-v2.txt`, `.raw.txt` | earlier text extractions; `.raw.txt` was used as the starting point for the transcription. |

**Not available** (not in the source folder, not fetched):
- the X-ray data set **EMPIAR-10782** (https://www.ebi.ac.uk/empiar/EMPIAR-10782/, Data availability) — the raw projection images; it would be the tier-1 source for every plotted panel;
- the code repository github.com/adwanner/XrayAssistedStaining (swh:1:rev:62c9930d08bbdd1602614d515cd20b1cb1f89d15): code only, no data;
- the "Transparent reporting form" (Supplementary files);
- the decision letter and author response (sa1, sa2).

There is no tier-1 data in the folder: the source-data PDFs are plots, not numbers. Everything is tier 3.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order (title, authors, affiliations, the p. 1 margin box, abstract, editor's evaluation, all sections, Equations 1–7 and the unnumbered methods equations, the Figure 1/2 legends with the source-data and figure-supplement titles, acknowledgements, additional information with the funding table, author contributions, ORCIDs, ethics, decision letter, additional files, data availability with the dataset table, 78 references). Figure 2 and its legend are placed at the end of the paragraph that spans pp. 6–8, so `\pdfpage{8}` occurs twice (noted in the file).
- `supplement.tex` / `supplement.pdf`: the 8 figure supplements (images, verbatim legends from the eLife JSON, descriptions, data).
- `source_data.tex` / `source_data.pdf`: the 7 source-data PDFs, page by page (39 pages): image, description with every printed title (sample IDs, R²adj/SEres of the model maps, end time of the projection image), data references. Generated by `work/make_source_data.py` from the CSVs and `figures/sd_titles.py`.
- `figures/`: `fig1.png`, `fig2.png` (200 dpi crops), `sfig1s1.png` … `sfig2s5.png` (the JPEGs as PNG), `sd_pages/*.png` (the 39 source-data page images); per plotted panel CSV + `_extract.py` + plot script + `_replot.png`; `sd/` for the source data (see below); shared helpers `main_common.py` (axes/ticks, colour masks, translucent-band model, colour-map reader, dashed-curve tracker), `replot_common.py`, `sdlayout.py`, `sd_templates.py/.npz`, `sd_titles.py`.
- `tables/funding.csv`, `tables/dataset.csv`: the two (unnumbered) tables of the article.
- `work/`: scratch (page renders, embedded images, overlays `*_overlay.png`, `sd_ov/`, side-by-side comparisons `cmp_*.png`, `sd_cmp_*.png`, check scripts and logs). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (and `supplement.tex`, `source_data.tex`); all three compile without errors (run twice).

Re-run: `python3 -I figures/<panel>_extract.py`, then `python3 -I figures/<panel>.py`. Source data: `python3 -I figures/sd_extract.py all` (~17 min), `python3 -I figures/sd_plot.py all`.

## Figures and data

**Vector check:** `tools/vector_dump.py` (re-run after the coordinator's fix for zero-width lines) finds only the figure frame on pp. 3 and 7; Figures 1 and 2 are single embedded rasters (2079 × 2867 px ≈ 348 ppi; 1949 × 2653 px ≈ 322 ppi). The supplements are JPEGs, the source data image-only PDFs. So no panel is tier 2, and none is tier 1 (no numeric source data).

**Methods (tier 3):** spines and tick marks found in the image, tick labels read by eye (main figures, supplements) or by glyph-template matching (source data, see below), linear fits (residuals in each CSV header); lines traced per pixel column with colour masks (top/bottom of the line kept where it is noisy or thick). Overlapping translucent s.d. bands are separated with an alpha-compositing model of the band colours (`main_common.band_masks`); dashed model curves are followed from seed points by linear extrapolation over the dash gaps (`track_extrap`); colour maps are read pixel by pixel through their colour bars (`map_grid`), at native resolution.

**Checks:** every extraction draws its points back on the source image (`work/*_overlay.png`, `work/sd_ov/*.png`), and every re-plot was put next to the original with `tools/compare.py` (`work/cmp_*.png`; source data `work/sd_cmp_*.png`, all 39 pages). I looked at the overlays and comparisons of all main and supplement panels and at the source-data comparisons as montages (about 10 pages in detail).
**Cross-check with the source data:** the means of the 13/6/4/4 per-sample t=1200 min depth profiles digitized from the source-data PDFs agree with the Figure 1e curves digitized from the main figure within 0.006 (a.u.) at all depths (`work/crosscheck_fig1e.py`, `work/crosscheck_fig1e.txt`). This also shows that the Figure 1e y axis (labelled only 0.4 and 1) is linear, not logarithmic.

### Source data (39 pages)

`figures/sd/<file>_traces.csv`: all 12 line plots of every page (columns page, sample, panel, series = data | model | circle, x, y, y_upper, y_lower, r_x); `figures/sd/<file>_maps/<file>_pNN_data.csv` (and `_model.csv` for Figure 1—source data 1): colour maps at native resolution (~315 × 315 px); `figures/sd/<file>_calibration.csv`: tick values, fit residuals and the OCR check of the titles per axes; `figures/sd/<file>_replots/`: re-plots of every page. The tick labels are read by matching each glyph to digit templates cut from labels read by eye (`sd_templates.py`), because tesseract misread many of these small labels (e.g. "0.6" as "20.6"); every page's ticks then agree with a linear fit (max residual 0.0012 a.u.). Page titles, model-map titles (R²adj, SEres) and the end time of the second projection image were read by eye and checked against tesseract (`work/check_sd_titles.py`; all digits agree except the subscripted model titles, which tesseract cannot read — those were checked again at full resolution).

### Figure table

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | schematic (set-up, staining-vial inset) | – | – | |
| Fig. 1b | three X-ray projection images | – | – | |
| Fig. 1c | scatter (n=3 per conc.) + fit line | `figures/fig1c.csv` | 3 | dots overlap; 2 hidden middle dots read by eye (tier 4, flagged) |
| Fig. 1d | line + s.d. band + dashed model | `figures/fig1d.csv` | 3 | legend blanked; a few band-edge columns missing |
| Fig. 1e | 4 lines + overlapping s.d. bands | `figures/fig1e.csv` | 3 | linear y axis (checked vs source data); green band clipped at ≈1.34 |
| Fig. 1f | 4 lines + bands + dashed model | `figures/fig1f.csv` | 3 | |
| Fig. 1g | vial drawings + 4 X-ray projections | – | – | |
| Fig. 2a | colour map + colour bar | `figures/fig2a.csv` | 3 | grid 346 × 346 |
| Fig. 2b | colour map + colour bar | `figures/fig2b.csv` | 3 | grid 346 × 347 |
| Fig. 2c | colour map + colour bar | `figures/fig2c.csv` | 3 | |
| Fig. 2d | 3 lines + faint bands + 3 dashed models | `figures/fig2d.csv` | 3 | |
| Fig. 2e | 3 lines + faint bands + 3 dashed models | `figures/fig2e.csv` | 3 | model 1000 μm unreliable < 250 min |
| Fig. 2f | schematic (geometry) | – | – | |
| Fig. 2g | schematic + process/kinetics table | – | – | table transcribed in `\alttext` |
| Fig. 1—s1 a, g, m | line plots (SEM, μCT) | `figures/sfig1s1{a,g,m}.csv` | 3 | |
| Fig. 1—s1 d, j, p | dense scatter | `figures/sfig1s1{d,j,p}.csv` | 3 | all dark pixels of the dot cloud (dots not separable) |
| Fig. 1—s1 b, c, e, f, h, i, k, l, n, o | μCT/X-ray/SEM images | – | – | |
| Fig. 1—s2 | SEM micrographs (7) | – | – | |
| Fig. 1—s3 a–f | line + band plots | `figures/sfig1s3{a..f}.csv` | 3 | |
| Fig. 2—s1 a–c | X-ray projections | – | – | |
| Fig. 2—s2 (12 line plots, 1 map) | MATLAB page | `figures/sfig2s2_traces.csv`, `_map_data.csv` | 3 | |
| Fig. 2—s2 projection images (2) | images | – | – | |
| Fig. 2—s3 a, b | line plots | `figures/sfig2s3{a,b}.csv` | 3 | |
| Fig. 2—s4 | bar chart + dots | `figures/sfig2s4.csv` | 3 | overlapping dots merge; y ticks unevenly spaced |
| Fig. 2—s5 (12 line plots, 2 maps) | MATLAB page | `figures/sfig2s5_traces.csv`, `_map_{data,model}.csv` | 3 | |
| Source data, 39 pages × (12 line plots + 1–2 maps) | MATLAB pages | `figures/sd/…` | 3 | "from the authors' source-data plots" |

**Panels per tier:** tier 1: 0; tier 2: 0; tier 3: 9 main-figure panels (1c–f, 2a–e), 42 supplement panels (6 + 6 + 13 + 2 + 1 + 14), 520 source-data panels (468 line plots, 52 colour maps); tier 4: none as a whole panel (2 points of Fig. 1c).

## Text check (`tools/check_text.py`, version 2026-10-17h)

| file | raw coverage | without repeated text | running text | tex tokens in source | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` vs `elife-72147-v2.pdf` | 97.4 % | 99.1 % | 99.1 % | 99.7 % | 3 runs (19 tokens) | 1 run (6 tokens) |
| `supplement.tex` vs the eLife JSON legends (`work/check_supp_legends.py`, check_text's tokenizer) | 99.2 % | – | – | 98.4 % | only superscript splits | only superscript splits |
| `source_data.tex` vs the 7 source-data PDFs | 0 PDF tokens (no text layer) | – | – | 0 tex tokens outside the decompiler macros | 0 | 0 |

Explanations (main): repeated text = running header/footer ("Tools and resources Neuroscience Ströh, Hammerschmith et al. eLife 2022;11:e72147 …", 231 tokens, left out). MISSING: "Figure 1/2 continued on next page" (publisher continuation markers, left out on purpose, as are "Figure 1/2 continued") and the methods formula "3. u_i^ref = u_i^min …" whose text-layer token order differs from LaTeX math. EXTRA: the same formula. Shorter unmatched runs are math (sub/superscripts glued in the text layer, "107–109" vs 10^7–10^9) and the software-heritage hash split across pp. 15/16. Supplement: the JSON writes D<sup>e</sup> as "De", LaTeX gives "D e"; that is all.

Read-through against the page images (step 4) done for Equations 1–7 and the methods formulas (flat-field correction, standardization with the underlined b_i, H(t), g(t), v(x,t), d(x), initial and boundary conditions, SE_res), Greek and special characters (μ, τ, ∂, ∝, ±, ≥, ≤, ∈, °, ~40 nm), subscripts in K₄[Fe(CN)₆], OsO₄, H₂O, CaCl₂, superscripts (10⁷–10⁹, nmol/mm³, Os₃O₅⁻), the funding and dataset tables.

## Errors and oddities in the paper (kept verbatim, flagged with `\decompnote`)

- Broken cross-references printed as empty text: "(Figure 1e, )", "K3[Fe(CN)6]+ 8 a,b)" (p. 6), "(Figure 1—figure supplement 3,f, )" (p. 6), "(n=13, )" (p. 9), "(, )" (p. 10).
- Figure 1—figure supplement 3 title: "potassium ferricyanide K4[Fe(CN)6] (green, n=6)" — the green series is ferrocyanide (K4); ferricyanide is K3.
- Figure 1c legend: "r=0.99, <10–6" (the "p" is missing).
- p. 1: the equal-contribution note uses "*", the author line "†".
- Methods, boundary conditions: b(x=L,t) = B⁰·d(L), but B⁰ is never defined.
- Methods typos kept: "where calculated", "were df corresponds", "such particular amino acids".
- Figure 1—figure supplement 1 (o): "same as in Figure 1—figure supplement 3" — the SEM images of that section are in supplement 2.
- Figure 2—figure supplement 1 (a): "Whole mouse brain from Figure 1d" — the whole brain is in Figure 1g.
- Figure 2—figure supplement 4: the y-axis tick marks are not evenly spaced (10→5: 208 px, 5→0: 219 px).
- Source-data page titles: "Os, IAC20200115_B20190113" (Fig. 1—source data 1 p. 7) and "KFeCN, IAC20200116_B20190113" (Fig. 2—source data 1 p. 4) have a B-date a year before the IAC-date, unlike all other pages (2–3 days); probably typos in the sample IDs. Source data 5 is called "Ferri-redOs" in the legend, "FerriOs" on its pages; the meaning of the black circles on the source-data depth profiles is not given (only Fig. 2—s2's legend says they mark axon tracts).
- Figure 1e: the green s.d. band runs above the end of the y axis (flat top at ≈1.34, axis ends at ≈1.27).

## Known problems of this decompilation

- Hidden lines: where one line is drawn over another, the hidden one has no value in those columns (stated in each CSV).
- Bands: the edges of overlapping translucent bands are less certain (±3 px), and some columns are missing (Fig. 1e green band between 100 and 300 μm, Fig. 2e bands).
- Fig. 2e: the steep early part of the 1000 μm model curve is not traced correctly (flagged in the CSV).
- Source-data maps: values are quantized to the colour bar's steps (about 60–66 distinct values per map).
- The source-data descriptions in `source_data.tex` are generated from the digitized data (values at 100 and 1200 min, profile maxima, circle positions), not written page by page.

## Problems and suggestions for the spec and tools (also in my report)

- The brief said the figure supplements were inside the PDF; they are not (only titles). The coordinator supplied them during the work.
- `check_text.py` only takes PDFs: legends from JSON/HTML need a separate check (I wrote `work/check_supp_legends.py`, which reuses `check_text.tokens` and `tex_text`). Suggest a `--text file.txt` option.
- Image-only PDFs give 0 PDF tokens and 0 coverage, which reads like a failure; the tool could say "no text layer".
- `digitize_common.trace_envelope` with `half_width=0` works for 1-px MATLAB lines, but there is no helper for translucent overlapping bands, dashed curves or colour maps; mine are in `figures/main_common.py` (`band_masks`, `band_trace`, `track_extrap`, `map_grid`) and could move to `tools/`.
- tesseract is unreliable on small plot tick labels (decimal points, "0.6" → "20.6"); glyph-template matching (`figures/sdlayout.py: read_label`) was exact on all 39 pages.
- `crop.py`/`compare.py` are fine; `compare.py` could accept several pairs and write a montage, which would make checking 39 pages faster.
- The spec says "one CSV + extract + plot per panel"; for 39 MATLAB pages with 12–14 panels each, one tidy CSV per source file (plus grid CSVs per map) is more usable — the spec could allow that explicitly.

## Time

Roughly 3.5 h of wall-clock: reading spec/tools and the paper ~20 min; main.tex ~40 min; source-data pipeline (layout detection, glyph OCR, tracing, maps, re-plots; two full 17-min runs) ~70 min; main-figure panels ~45 min; figure supplements ~45 min; descriptions, tex generation, checks and README ~30 min.
