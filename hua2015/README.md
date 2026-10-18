# hua2015: decompiled

Yunfeng Hua, Philip Laserstein, Moritz Helmstaedter. "Large-volume *en-bloc* staining for electron
microscopy-based connectomics." *Nature Communications* **6**, 7923 (2015). DOI
[10.1038/ncomms8923](https://doi.org/10.1038/ncomms8923). Received 6 Apr 2015, accepted 25 Jun 2015,
published 3 Aug 2015.

**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), statement on p. 7. Each page also
carries "© 2015 Macmillan Publishers Limited. All rights reserved." in the footer.

## Local and external

**In the local collection**
- Source files:
  - `papers/hua2015/hua2015.pdf` – main article, 7 pp., publisher version of record
  - `papers/hua2015/41467_2015_BFncomms8923_MOESM728_ESM.pdf` – Supplementary Information, 5 pp. (Suppl. Figs 1–3, Supplementary Tables 1–2)
  - `papers/hua2015/esm_zips/41467_2015_BFncomms8923_MOESM729_ESM.zip` – the Supplementary Software zip (RESCOP MATLAB code + 3 .mat files)
  - `papers/hua2015/esm_zips/extracted/supplMATLABcode_RESCOPanalysis/suppl. software/` – the same, unpacked: 6 .m files and the .mat files YH_MH_traceabilityData_fit_mh_v2.mat (this paper's data), KMB_MH_traceabilityData_fit_mh_v2.mat (cortex comparison), YH_MH_old_e1088Data_refit_mh_v2.mat (retina e1088); tier-1 source for Fig. 4d–f and the solid lines of Fig. 4g
  - `papers/hua2015/hua2015.txt`, `papers/hua2015/hua2015.raw.txt` – older text extractions (only glanced at)
  - `papers/hua2015/SOURCE.txt` – fetch note
- Cited works decompiled here: mikula2015 (`decompiled/mikula2015/`), korn1967 (`decompiled/korn1967/`), white1976 (`decompiled/white1976/`), white1979 (`decompiled/white1979/`), seligman1966 (`decompiled/seligman1966/`)

**External pull needed** (not on this machine)
- Supplementary Movie 1 (Fig. 4b, the SBEM data set) – no link given – a movie, not plot data
- The tracings ("together with all tracings", Methods) and the input files the RESCOP script loads (YH_MH_voteHist.mat, vote_matrix_for_mh_2014-12-30.mat, the e1088 vote-histogram file) – no link given (not in the Supplementary Software zip) – the raw input behind the vote histograms of Fig. 4d–g
- The *_FocAnn.mat focused-re-annotation results – no link given – tier-1 source for the dashed lines of Fig. 4g (they stay tier 2 here)
- The helper betainc_unnorm called by RESCOP_getPriorCiNTmatrix_v2.m – no link given – not needed here
- The comparison cortex data set itself (Boergens et al., cited as unpublished; only its fit is here, in KMB_MH_traceabilityData_fit_mh_v2.mat) – no link given
- All other cited references: 17 entries in the reference list (1–22) without a [local: …] tag. The SI has no reference list.

## Source files (`../../papers/hua2015/`)

| file | what it is |
|---|---|
| `hua2015.pdf` | main article, 7 pp. **Publisher version of record** (Nature Communications typesetting, running header/footer, "OPEN" badge; PDF metadata: Arbortext APP, re-distilled 2019). |
| `41467_2015_BFncomms8923_MOESM728_ESM.pdf` | Supplementary Information, 5 pp. (Illustrator-made, 2015): Suppl. Figs 1–3 (no captions, only the label "Hua, Laserstein & Helmstaedter / Suppl. Fig. N") and Supplementary Tables 1–2 with titles and captions. |
| `hua2015.txt`, `hua2015.raw.txt` | older text extractions of the main PDF (only glanced at; the text was taken from PyMuPDF blocks and the page images). |
| `esm_zips/extracted/supplMATLABcode_RESCOPanalysis/suppl. software/` | the **Supplementary Software** (added later): `RESCOP_mh_v3_forSuppl.m` and 5 helper `.m` files (read, never run), and three `.mat` files read with `scipy.io.loadmat`: `YH_MH_traceabilityData_fit_mh_v2.mat` (this paper's tracing data set), `KMB_MH_traceabilityData_fit_mh_v2.mat` (rOTO cortex comparison data set, Boergens et al.), `YH_MH_old_e1088Data_refit_mh_v2.mat` (retina e1088, ref. 21). They hold the vote histograms, the fits, the priors and the error predictions: **tier-1 source for Fig. 4d–f and the solid lines of 4g**. |

**Not available (named by the paper, not in the source folder, not fetched):**
- **Supplementary Movie** (Supplementary Movie 1; main text p. 4, "Fig. 4b, Supplementary Movie").
- From the Supplementary Software: **the tracings themselves** ("together with all tracings", Methods p. 7;
  the zip holds only vote histograms derived from them), the input files the script loads
  (`YH_MH_voteHist.mat`, `vote_matrix_for_mh_2014-12-30.mat`, the e1088 vote-histogram file), and the
  `*_FocAnn.mat` results of the focused-re-annotation Monte Carlo, which would be the tier-1 source for the
  **dashed lines of Fig. 4g** (they stay tier 2). The helper `betainc_unnorm` called by
  `RESCOP_getPriorCiNTmatrix_v2.m` is also missing (not needed here).
- The comparison cortex data set (Boergens et al.) is cited as unpublished.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: header block (ARTICLE, dates, DOI, OPEN), the
  footer citation line and copyright line given once, title, authors, affiliation footnote (moved after the
  author list), abstract, introduction, Results, Discussion, Methods, 22 references, Acknowledgements, Author
  contributions, Additional information, licence. Figures 1–4 with verbatim captions, descriptions and data
  pointers. `\pdfpage{}` marks every page start.
- `supplement.tex` / `supplement.pdf`: the whole SI (Suppl. Figs 1–3 with their labels and descriptions,
  Supplementary Tables 1 and 2 as `tabular` with titles and captions).
- `figures/`: `fig1.png`–`fig4.png`, `sfig1.png`–`sfig3.png` (200 dpi crops with `tools/crop.py`, captions not
  included); data and scripts for the plotted panels (below).
- `tables/`: `stable1.csv`, `stable2.csv` (Supplementary Tables 1 and 2; title and caption in `#` lines). The
  main article has no tables.
- `work/`: scratch (page renders, zooms, text-block dumps, vector dump `p6_plots.json`, overlays
  `*_overlay.png`, side-by-side comparisons `cmp_*.png`, check JSON, LaTeX logs). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (and `supplement.tex`);
both compile without errors (run twice; a few overfull lines from long URLs/footer lines).

Re-run the data: `python3 -I figures/fig4_extract.py` (tier 1, from the .mat files; needs the `*_digitized.csv`
and `*_vector.csv` for its comparison report and for the dashed 4g lines, so run `fig4de_digitized_extract.py`,
`fig4f_vector_extract.py`, `fig4g_vector_extract.py` first), then `python3 -I figures/fig4de.py`, `fig4f.py`,
`fig4g.py`, from any directory.

## Figures

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | schematic (biopsy → staining → blockface SEM → screening regions 1–4) | – | – | |
| Fig. 1b–e | 4 × 4 SEM micrographs (overview + 3 regions per protocol) | – | – | |
| Fig. 2a–f | SEM micrographs (zoom series to high resolution) | – | – | |
| Fig. 3a, b | chemical reaction schemes (steps 1–5) | – | – | transcribed in `\alttext` |
| Fig. 3c–e | cartoons of membranes and Os species (with legend) | – | – | transcribed in `\alttext` |
| Fig. 3f, h | photographs (vials, test tubes) | – | – | |
| Fig. 3g | SEM micrograph with inset | – | – | |
| Fig. 4a | SEM overview | – | – | |
| Fig. 4b | 3D rendering with skeleton tracings | – | – | |
| Fig. 4c | skeleton tracings | – | – | |
| Fig. 4d | heat map (vote histogram, "Meas."), log colour bar | `figures/fig4d.csv` | 1 source data | `RP_histMeasStar` (+ raw `RP_histMeas`); comparison: `fig4d_digitized.csv` (tier 3) |
| Fig. 4e | heat map (vote histogram, "Fit"), same colour bar | `figures/fig4e.csv` | 1 source data | `RP_histPredFinal`; comparison: `fig4e_digitized.csv` (tier 3) |
| Fig. 4f | line plot, log y (spikes) | `figures/fig4f.csv` | 1 source data | `RP_priorx`, `RP_priory` (81 points); comparison: `fig4f_vector.csv` (tier 2) |
| Fig. 4g | line plot, log y, 3 series × solid/dashed | `figures/fig4g.csv` | 1 (solid) + 2 (dashed) | solid `RP_rp/RP_p_errN`; dashed from the vector paths; **legend mismatch**, see below; comparison: `fig4g_vector.csv` |
| Fig. 4h | schematic (sample sizes 350, 400, 1,000 µm) | – | – | |
| Suppl. Fig. 1a–f | SEM zoom series | – | – | |
| Suppl. Fig. 2a, b | SEM micrographs | – | – | |
| Suppl. Fig. 3 (14 panels) | SEM overviews + high-magnification regions | – | – | |

Per tier: **tier 1 (source data): 4 panels** (4d, 4e, 4f, and the solid lines of 4g); the dashed lines of 4g
stay **tier 2** (vector); tier 3 and 4: none in the final CSVs (the earlier tier-2/3 extractions are kept as
`*_vector.csv` / `*_digitized.csv` for comparison).

How the data were obtained:
- **Tier 1 (`fig4_extract.py`):** the .mat variables, with their meaning taken from `RESCOP_mh_v3_forSuppl.m`
  (details in the script docstring and CSV headers). 4d = `RP_histMeasStar` = round(`RP_histMeas`/T) (T = 0 row
  NaN), 4e = `RP_histPredFinal`, 4f = `RP_priorx`/`RP_priory`, all from the YH file; 4g solid = `RP_rp ./
  RP_p_errN` for N = 1…50 (figure shows 1…23) with `RP_rp` as set in the script's final plotting section
  (1.2 µm e1088, 0.8 µm YH and KMB). The YH file's stored `RP_errDist` uses 1.2 µm and does **not** match the
  figure; the 0.8 µm version matches the vector paths within 0.4 %. No MATLAB code was ported or run; only
  this one division was redone in Python.
- **Agreement of the earlier extractions with the source data** (`work/fig4_compare.txt`):
  - 4d digitized (27 coloured cells): log10 ratio mean −0.011, sd 0.018, max 0.044 (11 %); all 36 darkest-blue
    cells are NaN, 0 or ≤ 1.2 in the source; the darkest-red cell N = T = 7 was read as ≥ 6,180 (clipped), source 7,442.
  - 4e digitized (34 cells): mean −0.007, sd 0.022, max 0.050 (12 %); 29/29 darkest-blue cells correct; N = T = 7
    read ≥ 6,180, source 7,083.
  - 4f vector: the 17 visible peak vertices sit within 0.0004 of a basis point in p_e and within 0.26 % in p(p_e);
    the clipped vertices are where the source drops below 0.1; the p_e = 1 point is 3,867 (cut at 10³ in the figure).
  - 4g vector solid lines: each matches one source curve within 0.4 % over all 23 points (and differs from the
    other two by 34–194 %), but **not the one its legend names** (next item).
- **Fig. 4g legend does not match the data.** Red (legend "e1088 (retina)") = YH, this paper's data set; green
  (legend "This protocol (cortex)") = KMB, the rOTO cortex data set; blue (legend "rOTO (cortex)") = e1088 retina.
  Evidence: the curve matches (above); the red curve comes from the same fit as panels d–f, which match the YH
  file exactly and are captioned as this data set; and the authors' plotting code draws e1088 `'b'`, YH `'r'`, KMB
  `'g'` (title string "e1008 (b); YH (r); KMB (g)"), i.e. exactly the printed colours, so the legend text was
  attached to the wrong colours. `fig4g.csv` gives both `data_set` and the printed `legend_label`; the dashed lines
  are assigned by colour in the same way (no source file to check them).
- **Earlier tier-2/3 extractions (kept for comparison):** `fig4f_vector_extract.py`, `fig4g_vector_extract.py`,
  `fig4de_digitized_extract.py`, as described next.
- **Fig. 4f, 4g (tier 2):** axes, ticks and the data lines are vector paths. Axis maps fitted on the tick
  marks (x linear on 2 ticks + a check tick, y log10 on 5–7 decade ticks; residuals in the CSV headers).
  Every vertex of every visible line is given. 4f: the line is clipped by the bottom of the axis box
  (vertices at 10⁻¹ flagged `below_axis`), the p_e = 1 spike reaches the top (`at_top`). 4g: the PDF draws
  the three dashed curves first all in blue and then redraws two of them in red and green; only the visible
  (last-drawn) strokes are kept. The red dashed line is cut by the right end of the axis box (flagged).
- **Fig. 4d, 4e (tier 3):** both heat maps and the colour bar are one embedded 304 × 122 px JPEG; the axis
  frames and the colour-bar ticks are vectors and give the exact cell grid and colour-bar calibration
  (log10, 10.288 pt per decade, bar from 1 to 10^3.87). Each cell's median colour is matched to the nearest
  colour-bar colour. Uncertainty ≈ ±0.06 decades (the 64-step jet colour map and JPEG noise). The darkest blue
  (≤ about 1 edge, which includes empty cells) and the darkest red (top of the bar) are flagged. The
  shared scripts are `fig4de_digitized_extract.py` and `fig4de.py` (one replot per panel plus `fig4de_replot.png`).
- Tick labels vs tick marks in 4d/4e: the numbers 0, 3, 6 stand at cells 0, 3, 6, but the small tick marks
  sit at the centres of cells 1, 3, 5, 7. The CSVs use the cell index = number of votes, as the labels imply.

**Checks:** the tier-2/3 extractions draw their points back onto a render of the source (`work/fig4f_overlay.png`,
`work/fig4g_overlay.png`, `work/fig4de_overlay.png`); the tier-1 data were checked against them numerically
(above). The replots, now drawn from the tier-1 CSVs, were put next to the original with `tools/compare.py`
(`work/cmp_fig4f.png`, `cmp_fig4g.png`, `cmp_fig4de.png`) and I looked at all of them: series, ranges, scales
and colours match (the 4g replot keeps the printed colours and legend texts and adds the true data set).

## Text check (`tools/check_text.py`)

Tool version 2026-10-17f (frozen).

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without text inside figures) | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` vs `hua2015.pdf` | 94.7 % | 94.7 % (no repeated text found) | 96.8 % (139 figure tokens) | 99.2 % | 11 runs, 127 tokens | 2 runs, 16 tokens |
| `supplement.tex` vs SI PDF | 92.7 % | 92.7 % | 100.0 % (61 figure tokens) | 100.0 % | 0 | 0 |

Explanation (all runs checked with `--min-run 1`):
- **main, MISSING:** almost all is **text inside figures** (vector labels of Fig. 1a, Fig. 2 panel letters,
  the Fig. 3 reaction schemes and cartoon labels ≈ 160 tokens, the Fig. 4 axis labels, ticks and legends
  ≈ 70 tokens); this text is transcribed in the `\alttext` descriptions instead. The rest are short runs of the
  **running header/footer** ("ARTICLE NATURE COMMUNICATIONS", page numbers; the footer line is given once, so
  the tool's repeated-text filter, which misses footers containing page numbers, reported none), and
  **Symbol-font glyphs** in the text layer: µ read as "m" (so "µm" is "mm"/"m", "µs" is "ms"), ∼ as "B", < as
  "o", > as "4", Θ as "Y", = as "¼", × and − dropped; "Os^VI" etc. glued in the text layer (`osvi` vs `os vi`);
  `p(pe)` and `rp` subscripts glued; "Du¨sseldorf" (spacing diaeresis) vs "Düsseldorf"; the drop cap "M apping";
  and real hyphens at line ends that the tool's dehyphenation joins (high-resolution, black-colored,
  high-contrast, Sigma-Aldrich, PATCO-stained, osmium-thiocarbohydrazide).
- **main, EXTRA:** only the µ/Symbol-font counterparts of the above ("m in a 40 m in b 2 m", "m 3 from the core
  500 m") and the split superscripts/hyphens. No transcription errors.
- **supplement, MISSING:** only the panel letters inside Suppl. Figs 1–3 (a–f, a1–d2). EXTRA: none.
- The remaining 3.2 % of the main running text are the Symbol-font, superscript and hyphen cases above
  (the tool does not count all figure-internal text as such: e.g. the Fig. 4 axis labels are still listed as
  MISSING runs).

Read-through against the page images (step 4) done for: ∼, <, >, ×, −1 (minus) vs "-1" (hyphen, printed so in
"via steps 1, -1"), °C (missing from the text layer), µm/µs, superscript oxidation states (Os^IV, Os^VI,
Os^VIII), [OsO₄(OH)₂]²⁻ and [OsO₂(OH)₄]²⁻, K₄Fe(CN)₆, µm³/nm³/mm², Θ = 375 nm, r_p, p(p_e), "116 × 7 = 812",
the double hyphens in ref. 16 ("lipid--containing", "tetroxide--fixed", kept), the "º" ordinal signs in the SI
tables (kept), italics (en-bloc, vice versa, et al., T, N, x, y) and reference formatting (italic journal, bold
volume with comma).

## Errors and oddities in the paper (kept verbatim; flagged with `\decompnote` where useful)

- **Fig. 3 caption, panel b:** "Os^IV dismutation", but panel b and the main text ("dismutation of Os^VI
  compounds (Fig. 3b)") show the dismutation of Os^VI (2 Os^VI → Os^IV + Os^VIII).
- **Fig. 1 caption:** the panel letters at the end look misplaced: "(e) PATCO provides good stain penetration
  but stains myelinated neurites only, (d) Scale bars" (PATCO is panel d). It also calls the first column the
  periphery, while panel a and "regions 1–4, left to right columns" make column 1 the overview and column 2 the
  periphery.
- **Fig. 4g legend is attached to the wrong curves** (see Figures): red = this paper's data (legend says
  e1088 retina), green = rOTO cortex (legend says This protocol), blue = e1088 retina (legend says rOTO). With
  the true assignment, this protocol's solid curve is above the retina curve at 22 of 23 points but below the
  rOTO-cortex curve at 1 and at 11–23 annotators (e.g. at 23 annotators: 235 µm vs 689 µm), which weakens the text's
  claim that the reconstructions "are at least as good as those from the retina data set and a
  conventionally-stained cortex data set (Fig. 4g)".
- **Supplementary Software:** the YH .mat file's stored `RP_errDist` uses `RP_rp` = 1.2 µm; the figure uses 0.8 µm
  (set in the script's final plotting section). Methods give the correspondence radius r_p as 225 nm; the
  script's `RP_rp` (1.2 or 0.8 µm, "% µm") is a different length (it scales p_errN to a distance) and is not
  explained in the paper.
- **Fig. 4g:** the x-axis tick labelled "1" sits at the left end of the axis, one unit left of where the ticks
  labelled 10 and 20 place the value 1 (the solid lines start there and their vertices fall on whole numbers
  1–23 on the 10/20 scale).
- **Fig. 4d/e:** the small tick marks are at cells 1, 3, 5, 7, while the tick labels 0, 3, 6 are at cells 0, 3, 6.
- **Reference 14** is garbled: "Subbaraman, L. R., Subbaraman, J. & Behrman, E. J. Inorganic Chemistry
  (Department of Biochemistry, Ohio State Univ.11, 2621–2627, 1972)." (no title; affiliation in place of
  publisher).
- Spelling: "dihydroxilation" / "Sharpless-dihydroxilation" (main text and Fig. 3 caption) next to
  "dihydroxylation"; "periodic acide" (SI Table 1); "Mouse s1 cortex" (SI Table 2); "insert" for inset (Fig. 3
  caption); "experimentators".
- Possible inconsistencies, not certain errors: Methods give thiocarbohydrazide as a "saturated aqueous
  solution", SI Table 1 as "1% TCH"; Methods (SBEM stack acquisition) cite "Supplementary Table 1" for the
  traced sample, which is listed in Supplementary Table 2 (scPL0052, "Traceability test"); SI Table 2 dates the
  Fig. 2 / Suppl. Fig. 1 sample (scYH1012) 2015/05/07, after the received date (6 Apr 2015), and gives
  scYH1059 the same date as scYH0056 (2014/01/22).

## Problems with the spec and tools (reported to the coordinator)

- `tools/vector_dump.py` dropped every horizontal/vertical path (zero-area bbox → `Rect.intersects` False),
  so the first dump of Fig. 4 showed no axes or ticks. I worked around it with a patched copy in `work/` and
  my own closed-interval test in the extract scripts; the coordinator has since fixed the tool, and the fixed
  tool gives the same 237 paths (the patched copy was then deleted).
- `check_text.py`'s repeated-text filter misses footers with page numbers (coordinator is fixing it).
- The token check cannot tell Symbol-font µ from "m"; for this paper that alone makes ~60 short MISSING/EXTRA
  runs. A small substitution table for known Symbol-font misreadings (m→µ before units, B→∼, o→<, 4→>, Y→Θ,
  ¼→=) applied to the PDF side would make the numbers far more useful.
- Supplementary figures without captions: the spec assumes captions; here only a label line exists.
- check_text.py 2026-10-17f: its "inside figures" exclusion missed the Fig. 4 axis/legend text (vector text
  inside the figure area), so the running-text number is a lower bound here.
