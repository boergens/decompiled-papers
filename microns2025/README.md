# microns2025: decompiled

The MICrONS Consortium (J. Alexander Bae, Mahaly Baptiste, … Chi Zhang; 96 named members, list on p. 13).
"Functional connectomics spanning multiple areas of mouse visual cortex."
*Nature* **640**, 435–447 (10 April 2025). DOI [10.1038/s41586-025-08790-w](https://doi.org/10.1038/s41586-025-08790-w)
(printed on p. 1 and in the PDF metadata).
Received 18 April 2023; accepted 14 February 2025; published online 9 April 2025.
DOI check: verify-sources receipt `vs-20261013-04e5c49e0b` (Crossref record matched to this PDF, 23,703,454 bytes).

**Licence:** Open Access, Creative Commons Attribution 4.0 International (CC BY 4.0), "© The Author(s) 2025" (p. 13).
Fig. 2 contains image panels adapted from Yin et al. (Springer Nature Limited) and drawings adapted from Mahalingam et al.
(CC BY 4.0), as its caption says.

## Source files

| file | what it is |
|---|---|
| `source/microns2025.pdf` | copied from `papers/microns2025/microns2025.pdf`. **Publisher's version of record** (Springer Nature typeset PDF, 34 pp., created 31 March 2025): article pp. 1–13 (journal pp. 435–447), Methods and back matter pp. 14–22, Extended Data Figs. 1–5 pp. 23–28, Extended Data Tables 1–3 pp. 29–31 (printed as images), Nature Portfolio reporting summary pp. 32–34. `SOURCE.txt` fetch note: "microns2025.pdf: https://www.nature.com/articles/s41586-025-08790-w.pdf (curl, 2026-10-12)". |

`papers/microns2025/` also holds `microns2025.txt` / `microns2025.raw.txt` (older text extractions; not used).

## Contents

- `main.tex` / `main.pdf`: pp. 1–31 in reading order: journal block, title, author line, abstract, affiliation footnote
  (placed after the abstract), all main-text sections, Figs. 1–7, the reference list 1–64, publisher's note, licence,
  consortium author list, Methods (all subsections, with the equations for laser power and the Monet2 filter), Methods
  references 65–96, data and code availability, acknowledgements, author contributions, competing interests, additional
  information, Extended Data Figs. 1–5 and Extended Data Tables 1–3 (transcribed from the page images).
- `reporting_summary.tex` / `.pdf`: pp. 32–34, the Nature Portfolio Reporting Summary with its boilerplate and check-box states.
- `figures/`: every figure cropped at 200 dpi (`fig1.png` … `fig7.png`, `edfig1.png` … `edfig5.png`); per plotted panel a CSV,
  an extraction script (`*_extract.py`) and a plotting script with its `*_replot.png` (see the table below).
- `tables/edtable1.csv`, `edtable2.csv`, `edtable3.csv`: Extended Data Tables 1–3 (written by `work/scripts/make_tables.py`).
  The table panel of Extended Data Fig. 4a is `figures/edfig4a.csv`.
- `tools/`: `mc.py` (small shared helpers written for this paper), `pdfplot.py` (copied from `oct_17_papers/hesse2026/tools/`),
  `digitize_common.py` (copied from the osmium `tools/`). All scripts use paths relative to themselves.
- `decomp.sty` (copied from the osmium tools) so both .tex files compile here.
- `work/`: scratch (page renders, text drafts `work/draft/`, the drafting/assembly scripts `work/draft.py`, `work/assemble.py`,
  `work/scripts/`, overlays `work/overlay_*.png`, side-by-side comparisons `work/cmp_*.png`, check JSON, `PROGRESS.md`). May be deleted.

Compile (from this folder): `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice), same for `reporting_summary.tex`.
Both compile without errors; the only warnings are overfull lines from long URLs. Re-run data: `python3 -I -B figures/<name>_extract.py`
then `python3 -I -B figures/<name>.py` (any working directory; Python with numpy, scipy, matplotlib, PyMuPDF, PIL).

## Text check (`check_text.py` version 2026-10-17j)

| file | options | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without unmatched in-figure text | tex tokens found in PDF |
|---|---|---|---|---|---|
| `main.tex` | `--pages 1-31` | 97.5 % | 97.8 % | **99.0 %** | 96.8 % |
| `reporting_summary.tex` | `--pages 32-34` | 97.9 % | **98.5 %** | 98.5 % | 99.5 % |

`main.tex`, what is not matched (`--min-run 1`):
- MISSING: text inside figures (axis labels, keys, panel titles of Figs. 1, 3, 6, 7; described in `\alttext`; 295 tokens);
  the running header "Article" (15 pages) and the page numbers 441–447 at the end of footer lines; "Check for updates" (p. 1);
  "Reprints and permissions information is available at http://www.nature.com/reprints." (p. 22, publisher boilerplate, left
  out on purpose); one "0" = the subscript of P₀ in the laser-power equation (p. 14, written as LaTeX math).
- EXTRA: all EXTRA runs (≈ 830 tokens) are the three Extended Data Tables (pp. 29–31) and their column heads: these pages are
  images without a text layer, so the transcription has no PDF tokens to match. The table rows were transcribed from the page
  images (tesseract OCR as a start, every cell proofread against 3× crops). Also "article" (the journal block, given once) and
  the "0" of P₀.

`reporting_summary.tex`: MISSING = the margin label "nature portfolio | reporting summary", the "April 2023" form-version
note and page numbers 1–3 (all left out), and "Plants / Seed stocks" (p. 34), which the checker pairs with the earlier
"Plants" check-box item and then reports again as EXTRA (5 tokens): the text is there, in reading order.

Read-through against the page images (step 4) done for: the two display equations (P = P₀ × e^(z/L_z); G(ω; c) = √c H(cω),
H(ω) = ½ + ½ cos ω if |ω| < π and 0 otherwise), superscript citations, units with superscripts (mm³, µm³, nm³, mg kg⁻¹,
° s⁻¹, ° cm⁻¹, 8π s⁻¹), subscripts (CaCl₂, MgSO₄, P₀, L_z, r₁, r₂), ×, ≥, ≪ (written `$\ll$`), Greek letters (σ, ω, ϕ, θ, π, Δ),
the timeline lines, both bullet lists and both numbered lists of the Methods, the run-in bold headings, the consortium list,
and the reference formatting (italic journals, bold volumes). µ (micro sign) and μ (Greek mu) are kept as printed.

## Figures

**No tier-1 source data is in the collection.** The paper's data are on MICrONS Explorer (https://www.microns-explorer.org/cortical-mm3),
BossDB (https://bossdb.org/project/microns-minnie), the DANDI archive (dandiset 000402) and in CAVE tables; the figure code is
in https://github.com/AllenInstitute/MicronsFunctionalConnectomics. None of these were fetched (no network). They are the
tier-1 source for practically every plotted panel (e.g. CAVE tables `proofreading_status_and_strategy`, `nucleus_ref_neuron_svm`,
`coregistration_*` for Extended Data Figs. 2–5 and Fig. 6f).

Vector plots (Extended Data Figs. 2–5, Fig. 6f, h) were read with `vector_dump`-style PyMuPDF path parsing; tick labels in
those figures are outlined glyphs, so tick values were read from renders and paired with tick marks or grid lines. Raster
plots were digitized from the embedded images at native resolution. **Checks:** every extraction writes an overlay
(`work/overlay_*.png`: extracted points drawn on a render of the page region, or a re-built image of the extracted grid
next to the original) and every replot was compared with the original by `tools/compare.py` (`work/cmp_*.png`); I looked
at both for every panel. All series, ranges and scales agree (colour maps of re-plots differ in places; looks were not matched).

Consistency checks that came out right: Ext. Data Fig. 3A bar heights equal the printed counts (to ≤ 0.05) and give
7,050 multi-soma objects with 17,753 neurons, the numbers in the main text (p. 7); Ext. Data Fig. 3B left has exactly
17,753 markers (title n = 17753) and the right 98 (n = 98); Ext. Data Fig. 5c gives 36,387 neurons for the unfiltered
fiducial-based automatch (text: 37,364 EM neurons) and Ext. Data Fig. 5b precision 0.838 (text: 83 %); Fig. 6h's first column splits
74.6 % / 25.4 % (text: 74.5 % / 25.4 %); Fig. 6k's 1 s scale bar spans 6.2 time bins (63 bins per 10 s clip ≈ 6.3 Hz);
Ext. Data Fig. 1 gives the same F₁ per test volume in both plots (66 marker spots each, a few touching, vs 70 test volumes in the text).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | nine thumbnails (traces, EM, renders) | – | – | |
| Fig. 1b | flow diagram | – | – | transcribed in `\alttext` |
| Fig. 2 | workflow schematic with image panels | – | – | |
| Fig. 3a, b, d, e | 3D renders, wireframe, 3D scatter without axes, stimulus frames | – | – | |
| Fig. 3c | line plot (depth of fields) | `figures/fig3c.csv` | 3 | raster lines, vector axis; 98 lines found (caption b: 104 planes; coincident lines cannot be separated) |
| Fig. 3f | 18 raster boxes | `figures/fig3f.csv` | 3 | 10 repeats × 62 bins per box; uncalibrated (no colour bar) |
| Fig. 3g | heat map | `figures/fig3g.csv` | 3 | 80 × 64 cells; uncalibrated (no colour bar) |
| Fig. 4a–h | EM micrographs, overview, schematic | – | – | |
| Fig. 5a–d | neuron reconstructions | – | – | |
| Fig. 6a–e, g | renders of cell positions (no axes) | – | – | key colours in `\alttext` |
| Fig. 6f | scatter, log x | `figures/fig6f.csv` | 2 | 1,407 points |
| Fig. 6h | stacked bars / flow | `figures/fig6h.csv` | 2 | y axis unlabelled except 0: heights in pt, fractions, and counts estimated from the text's 1,412 |
| Fig. 6i, j | EM image, 2P image with annotations | – | – | |
| Fig. 6k | heat maps with colour bar | `figures/fig6k.csv` | 3 | 80 × 63 per clip + presyn row; calibrated (grey colour bar 0–1) |
| Fig. 7a–c | dot-density plots | `figures/fig7a.csv.gz`, `fig7b.csv.gz`, `fig7c.csv.gz` (one script `fig7abc_extract.py`, `fig7abc.py`) | 3 | pixel density maps, uncalibrated ink; single dots not separable |
| Fig. 7d | schematic + heat maps with colour bars | `figures/fig7d.csv` | 3 | all sub-maps; values via each colour bar; depth strip uncalibrated (Pia–WM) |
| Ext. Data Fig. 1 (a) top, (b) bottom | scatter with colour bar (raster) | `figures/edfig1a.csv`, `edfig1b.csv` (`edfig1_extract.py`, `edfig1.py`) | 3 | marker centres; F₁ from colour (fitted marker opacity) |
| Ext. Data Fig. 2A | histogram, log–log | `figures/edfig2a.csv` | 2 | |
| Ext. Data Fig. 2B | scatter, log–log | `figures/edfig2b.csv` | 2 | 1,021 points |
| Ext. Data Fig. 3A | bar chart, broken axis | `figures/edfig3a.csv` | 2 | printed labels included |
| Ext. Data Fig. 3B | two scatters with colour bar | `figures/edfig3b_left.csv`, `edfig3b_right.csv` (`edfig3b_extract.py`, `edfig3b.py`) | 2 (z: 3) | z from marker colour |
| Ext. Data Fig. 4a | table panel | `figures/edfig4a.csv` | transcribed | outlined glyphs |
| Ext. Data Fig. 4b, d | schematics | – | – | transcribed in `\alttext` |
| Ext. Data Fig. 4c | 2D histogram | `figures/edfig4c.csv` | 2 (counts: 3) | counts from colour |
| Ext. Data Fig. 4e | histograms | `figures/edfig4e.csv` | 2 | |
| Ext. Data Fig. 4f, g, h | scatters with colour bar (raster) | `figures/edfig4f.csv`, `edfig4g.csv`, `edfig4h.csv` (`edfig4fgh_extract.py`, `edfig4fgh.py`) | 3 | pixel tables; points overlap |
| Ext. Data Fig. 5a | line plots (2) | `figures/edfig5a.csv` | 2 | |
| Ext. Data Fig. 5b, c | 6 heat maps | `figures/edfig5b.csv`, `edfig5c.csv` (`edfig5bc_extract.py`, `edfig5bc.py`) | 2 (values: 3) | values from colour |

Panel counts by tier: tier 1: 0; tier 2 (all-vector): 9 (Fig. 6f, 6h; Ext. Data 2A, 2B, 3A, 3B left, 3B right, 4e, 5a);
tier 2 positions + tier 3 colour values: 3 (Ext. Data 4c, 5b, 5c; also the z of 3B); tier 3: 13 (Fig. 3c, 3f, 3g, 6k, 7a, 7b, 7c, 7d;
Ext. Data 1a, 1b, 4f, 4g, 4h); transcribed table panel: 1 (Ext. Data 4a). Image panels without axes: described only.

## Not available (named by the paper)

- Supplementary information ("The online version contains supplementary material", p. 22) and the peer review reports.
- The data resources and code listed above (MICrONS Explorer, BossDB, DANDI 000402 (ref. 73), CAVE tables, GitHub repositories
  in Ext. Data Table 2 and the reporting summary, Zenodo cloud-volume release (ref. 94)), and the Neuroglancer states linked in
  the captions of Figs. 4 and 6 (`…/mm3/data_fig/4b.json`, `4f.json`, `4g.json`, `4h.json`, `6f.json`) and the go.nature.com
  example links on p. 1–2.

## Cited works in the collection (from `decompile_work/manifest.json`)

- ref. 25 Lee et al. 2016 → `lee2016` (PMC author manuscript); ref. 44 Scheffer et al. 2020 → `scheffer2020`;
  ref. 63 Yin et al. 2020 → `yin2020` (also cited in the reporting summary).
- Other versions: ref. 34 Zheng et al. 2018 → `zheng2018` (bioRxiv 2017 preprint); ref. 45 Phelps et al. 2021 → `phelps2021`
  (bioRxiv 2020 preprint); ref. 59 Shapson-Coe et al. 2024 → `shapsoncoe2024` (bioRxiv 2021 preprint).

## Errors and inconsistencies in the paper (kept verbatim; the important ones flagged with `\decompnote`)

- Main text p. 7: "(Fig. 5f)" — Fig. 5 has only panels a–d.
- Timeline (Methods): "Structural Stack: 21 March 2018 (P83)" is after "Perfusion: 16 March 2018 (P87)"; counting from the birth
  date, P83 is 12 March (decompiler's arithmetic). The main text gives imaging P75–P81, the timeline P75–P80.
- Ref. 1: DOI printed as "https://doi.org/10.1038/10.1038/s41592-024-02426-z" (prefix twice). Ref. 73 starts "Website.Bae, J. A."
- Proofreading strategy (4) ends mid-sentence: "Any axon leaving the cylinder was cut and".
- Fig. 6 caption: "cell-are type", "i, EM image (i) and corresponding image … (j)" (the label should be i, j); main text
  "(25.4% 359 out of 1.412 synapses)", "have been functional co-registered", "ranging from in length from", "agglomeration (Fig. 5a)
  Segmentation" (no full stop), "National Insitutes of Health", Fig. 4 caption "adapted from from" and "shown in in";
  "Python Jupiter notebooks" (code availability and reporting summary); Ext. Data Fig. 5a title "seperation percentile";
  Ext. Data Table 3 "nucleus_functional_area_assignment 144120" (no thousands separator, "where it lives in the in visual cortex").
- Table/name mismatches: Methods name the table "nucleus_neuron_svm" (p. 20) but Ext. Data Table 3 lists "nucleus_ref_neuron_svm";
  Ext. Data Table 3 describes aibs_metamodel_mtypes_v661_v2 as based on "allen_column_mtypes_v1" while the table listed is
  allen_column_mtypes_v2.
- Figure vs text: Fig. 6h's drawn class split of the 1,053 soma-targeting synapses (≈ 735 excitatory, 296 inhibitory,
  24 uncharacterized, scaled with the text's 1,412 total) differs from the text's 662 / 275 / 116; the "Functionally matched"
  bars (≈ 272 manual, 675 automatic) do not obviously match the text's "365 out of 1,412". Ext. Data Fig. 4a sums to 18,361
  matched nuclei, the text gives 19,181 manually matched ROIs (possibly different units). Ext. Data Fig. 3A ends at 17 neurons
  per ID; the Methods mention one object with 172 neuronal nuclei and "2 to 25 nuclei" (possibly a different time point).
  Fig. 7 caption: "Layer boundaries are shown as dashed grey lines", but no such lines are visible in panels a–c.
- Reporting summary: corresponding author "Nuno Macarico da Costa" (article: "Maçarico"); "Nat Commun11".

## Known problems / limits

- Rasters (Figs. 3f, 3g, 7a–c) have no colour bar: values are uncalibrated darkness; Fig. 7a–c are density maps, not points.
- Ext. Data Fig. 4f–h are pixel tables: the dots overlap and cannot be counted.
- Fig. 7d left map's 0–250 calibration uses the label centre for 250 because its ticks are not at round values (±5 %).
- Ext. Data Fig. 3B left has no colour bar of its own; the right plot's (600–1100 µm) was used.
- Fig. 3c: 98 lines found where the caption of b speaks of 104 planes.

## Time

About 6 h of agent time (23:13–05:10 UTC by the machine clock, including a pause at the account usage limit around 02:00).
