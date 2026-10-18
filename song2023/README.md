# song2023: decompiled

Kun Song, Zhihui Feng, Moritz Helmstaedter. "High-contrast en bloc staining of mouse whole-brain and human brain
samples for EM-based connectomics." *Nature Methods* **20**, 836–840 (2023). DOI
[10.1038/s41592-023-01866-3](https://doi.org/10.1038/s41592-023-01866-3). Brief Communication.
Received 28 February 2022; accepted 27 March 2023; published online 8 May 2023.

**Licence:** Open Access, Creative Commons Attribution 4.0 International (CC BY 4.0), © The Author(s) 2023 (stated on p. 5).
Source data (Edmond, doi 10.17617/3.RG58DU): CC0 1.0; code: MIT licence.

## Local and external

**In the local collection**
- Source files:
  - `papers/song2023/41592_2023_Article_1866.pdf` – publisher's version of record, 25 pp. (article, Methods, Extended Data Figs. 1–7, reporting summary)
  - `papers/song2023/41592_2023_1866_MOESM1_ESM.pdf` – Supplementary Information, 25 pp. (Supplementary Results, Tables 1–4, References 1–22)
  - `papers/song2023/41592_2023_1866_MOESM2_ESM.pdf` – Nature Research Reporting Summary, 3 pp. (no text layer)
  - `papers/song2023/edmond_RG58DU/` – the authors' source data and code (Edmond, https://doi.org/10.17617/3.RG58DU, ref. 30): readme.txt, code.zip, data.zip, unpacked in `papers/song2023/edmond_RG58DU/extracted/data/` and `papers/song2023/edmond_RG58DU/extracted/code/`; tier-1 source for Fig. 2a, 2b and Extended Data Figs. 1a,b, 1f, 1k, 1l, 5d, 5j,k
  - `papers/song2023/SOURCE_DATA.txt` – fetch note for the Edmond set
  - `papers/song2023/41592_2023_Article_1866.txt`, `papers/song2023/41592_2023_Article_1866.raw.txt`, `papers/song2023/si.raw.txt` – older text extractions (not used)
- Cited works decompiled here: debruijn1973 (`decompiled/debruijn1973/`), hua2015 (`decompiled/hua2015/`), mikula2015 (`decompiled/mikula2015/`), stroh2022 (`decompiled/stroh2022/`), seligman1966 (`decompiled/seligman1966/`), karlupia2023 (`decompiled/karlupia2023/`, in the note added in proof), genoud2018 (`decompiled/genoud2018/`), white1979 (`decompiled/white1979/`), litman1972 (`decompiled/litman1972/`), korn1967 (`decompiled/korn1967/`)

**External pull needed** (not on this machine)
- Supplementary Video 1 (ATUM cutting test, main text and Fig. 1e caption) – no link given – a video, not plot data
- The webKnossos data sets in Data availability – 3D EM: https://wklink.org/7781 (H6), https://wklink.org/7718 (H13 striatum), https://wklink.org/7723 (H13 cortex); µCT: https://wklink.org/7798 (H6), https://wklink.org/7732 (H4), https://wklink.org/7742 (W3), https://wklink.org/7789 (W1) – online browsing links to image data, not files
- All other cited references: 40 entries without a [local: …] tag: 20 of main refs. 1–25, all of Methods refs. 26–30 (ref. 30 is the Edmond data set, which *is* here, in `papers/song2023/edmond_RG58DU/`), and 15 of the 22 Supplementary References.

## Source files (`../../papers/song2023/`)

| file | what it is |
|---|---|
| `41592_2023_Article_1866.pdf` | **Publisher's version of record**, 25 pp.: article pp. 1–5 (journal pages 836–840), Methods and back matter pp. 6–11, Extended Data Figs. 1–7 pp. 12–22 (figure and caption on separate pages for ED Figs. 1, 4, 5, 6), and the Nature reporting summary as pp. 23–25 (pixel-identical to MOESM2). |
| `41592_2023_1866_MOESM1_ESM.pdf` | Supplementary Information, 25 pp.: publisher cover page + the authors' document (Supplementary Results, Supplementary Tables 1–4, Supplementary References 1–22). No figures. |
| `41592_2023_1866_MOESM2_ESM.pdf` | Nature Research Reporting Summary, 3 pp. "Microsoft: Print To PDF": **no text layer**, everything is vector outlines. |
| `41592_2023_Article_1866.txt`, `.raw.txt`, `si.raw.txt` | older text extractions (not used). |
| `edmond_RG58DU/` | authors' source data and code (see below). |

**Not available:** Supplementary Video 1 (ATUM cutting test, cited in the main text and Fig. 1e caption).
The webKnossos datasets cited in Data availability (wklink.org/7781, 7718, 7723, 7798, 7732, 7742, 7789) are
online browsing links, not files; not fetched (no network). Nothing else is missing: every plotted panel that has
source data is covered by the Edmond set.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, affiliation (moved
  after the author list, noted), dates, abstract, main text, Figs. 1–2 with captions, Online content, references 1–25,
  Publisher's note, licence, Methods (all subsections), Reporting summary, Data and Code availability, references
  26–30, Acknowledgements, Author contributions, Funding, Competing interests, Additional information, Extended Data
  Figs. 1–7 with captions. `\pdfpage{N}` marks pages 1–22. The reporting summary pages 23–25 are in `reporting_summary.tex`.
- `supplement.tex` / `supplement.pdf`: the whole SI (cover page, Supplementary Results with all subsections,
  Supplementary Tables 1–4 as `longtable`s with their captions and footnotes, Supplementary References 1–22).
- `reporting_summary.tex` / `.pdf`: the full reporting summary form, boilerplate included, transcribed from page
  images (checkboxes as `[x]` / `[ ]`).
- `tables/`: `stable1_staining.csv`, `stable1_dehydration.csv`, `stable1_resin_spurr.csv`, `stable1_resin_epon.csv`
  (Supplementary Table 1, parts I, II, III-left, III-right), `stable2.csv`, `stable3.csv`, `stable4.csv`, and
  `edfig7.csv` (the protocol chart of Extended Data Fig. 7, transcribed). Line breaks inside a CSV cell = paragraph
  breaks in the printed cell. Built by `work/scripts/build_stables.py` (also emits the LaTeX tables).
- `figures/`: `fig1.png`, `fig2.png`, `edfig1.png` … `edfig7.png` (200 dpi crops; "edfig" = Extended Data Figure, the
  spec has no prefix for these), and per plotted panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`,
  `<panel>_replot.png`. `song_common.py` = shared helpers (page images, colour masks, axis fits, EDAX-report parser for
  the `.doc` files, MATLAB `table`-object reader, marker finder).
- `work/`: scratch: page renders, overlays (`*_overlay.png`), side-by-side comparisons (`cmp_*.png`), the scripts that
  drafted the .tex files from the text layer (`work/scripts/`), check JSONs, OCR of the reporting summary. May be deleted.

Compile (from this folder): `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex`
(same for `supplement.tex`, `reporting_summary.tex`); all three compile without errors (run twice).
Re-run data: `python3 -I figures/<panel>_extract.py`, then `python3 -I figures/<panel>.py` (any working directory).
The extract scripts read the Edmond files and the PDF directly and never execute anything from the Edmond folder.

## Figures

Fig. 2a,b plots are vector paths in the PDF (checked with the fixed `vector_dump.py` and `page.get_drawings()`);
all Extended Data figures are single 300-ppi raster images (one per page), so for them tier 2 is impossible.
Wherever Edmond source data exist they are used (tier 1) and the printed figure is used as a check: vector
paths for Fig. 2, raster digitizing (axes fitted on tick marks) for the ED figures. Every CSV header states the
provenance, the agreement with the printed figure and anything odd.

**Checks done:** for every plotted panel the extracted/source points were drawn back onto the source (`work/*_overlay.png`:
4× vector renders for Fig. 2, the embedded 300-ppi image for ED figures) and the replot was put next to the original with
`tools/compare.py` (`work/cmp_*.png`); I looked at both images for every panel. Series, ranges and scales match; the
deviations found are real differences between the deposited data and the printed figure and are listed below and in the CSV headers.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | schematic (sample sizes) | – | – | |
| Fig. 1b | SEM micrographs (overview + 3 positions, 2 protocols) | – | – | raw images: Edmond `Fig.1/Fig.1b` |
| Fig. 1c | µCT views + 5 SEM micrographs | – | – | raw: `Fig.1/Fig.1c` |
| Fig. 1d | sketches + SEM + µCT (artifacts) | – | – | raw: `Fig.1/Fig.1d` |
| Fig. 1e | sketches + photograph (ATUM) | – | – | |
| Fig. 2a left/top | 3D SBEM rendering; skeleton tracings | – | – | tracings: Edmond `.nml` |
| Fig. 2a bottom | bar chart with whiskers | `fig2a.csv` | 1 | checked on vector paths; whiskers differ (see errors) |
| Fig. 2b top | 3D rendering of dense reconstruction | – | – | |
| Fig. 2b bottom | histogram, log y | `fig2b.csv` | 1 | binning reproduced; matches vector stairs to the line width |
| Fig. 2c, d | schematics | – | – | |
| Fig. 2e | SEM overview + 5 micrographs | – | – | raw: `Fig.2/Fig.2e` |
| ED 1a | µCT + SEM block face | – | – | raw: `Extended Data Fig. 1a-b` (SEM .tif, 497-slice µCT stack) |
| ED 1b left | line plot, 3 profiles | `edfig1bleft.csv` | 1 (y) / 3 (x scale) | .mat holds sample indices only; x in µm fitted to figure |
| ED 1b right | line plot with error bars | `edfig1bright.csv` | 1 | EDAX reports; printed points ~0.3 wt.% higher |
| ED 1c, d, e | µCT images (+ photo) | – | – | no source files |
| ED 1f left/middle | SEM micrographs | – | – | raw: `Extended Data Fig. 1f/SEM` |
| ED 1f right | line plot with error bars | `edfig1fright.csv` | 1 | plotted = 2nd report of each file |
| ED 1g | SEM micrographs | – | – | raw: `Extended Data Fig.1g` |
| ED 1h left | µCT examples + photo | – | – | |
| ED 1h right | stacked bar chart | `edfig1h.csv` | 3 | no source data |
| ED 1i | µCT images | – | – | |
| ED 1j | sketch + light micrographs | – | – | |
| ED 1k | line plot, 9 curves | `edfig1k.csv` | 1 | Prism .pzfx; 2 columns 'uncertain' (hidden under others) |
| ED 1l | line plot with error bars | `edfig1l.csv` | 1 | per-image values included |
| ED 1m | SEM overview + 3 micrographs | – | – | raw: `Extended Data Fig. 1m` |
| ED 2a–j | SEM micrograph pairs | – | – | raw: `Extended Data Fig.2` |
| ED 3a–e | overviews + 25 SEM micrographs | – | – | raw: `Extended Data Fig.3-H4/H5/H6/H13/W3` |
| ED 4a left | µCT time series | – | – | |
| ED 4a right | line plot | `edfig4a.csv` | 3 | no source data |
| ED 4b–e | overviews + SEM micrographs | – | – | raw: `Extended Data Fig.4` |
| ED 4f | line plot with error bars | `edfig4f.csv` | 3 | no source data |
| ED 4g, h | µCT views | – | – | |
| ED 4i left | photographs | – | – | |
| ED 4i right | line plot | `edfig4i.csv` | 3 | no source data |
| ED 5a–c, e–h | SEM micrographs | – | – | raw: `Extended Data Fig.5a/b/c/e/f/g/h` |
| ED 5d | line plot (UV-vis) + photo inset | `edfig5d.csv` | 1 | agrees within 0.002 |
| ED 5i | photographs of tubes | – | – | |
| ED 5j | Raman spectra, two x windows | `edfig5j.csv` | 1 | data in folder "Extended Data Fig.6j,k"; right window baseline differs |
| ED 5k | Raman spectra | `edfig5k.csv` | 1 | printed y scale fitted to figure; printed curves smoothed |
| ED 5l, m | schematics | – | – | described in `\alttext` |
| ED 6a–g, i–n | µCT + SEM + photos | – | – | raw: `Extended Data Fig.6b`, `6d,e`, `6m,n` |
| ED 6h | flow diagram | – | – | transcribed in `\alttext` |
| ED 7 | protocol chart (table-like) | `tables/edfig7.csv` | read from image | transcribed, also in `\alttext` |

Panels per tier: **tier 1: 10** (Fig. 2a, 2b; ED 1b left (x scale tier 3), 1b right, 1f right, 1k, 1l, 5d, 5j, 5k);
**tier 2: 0** (Fig. 2 vector paths used as the check of tier-1 data); **tier 3: 4** (ED 1h, 4a, 4f, 4i); tier 4: 0.

## Edmond source data (`edmond_RG58DU/extracted/`; not copied)

`data/` (≈ 960 MB unzipped, by figure folder) — what each folder holds and which panel it belongs to:

| folder | contents | panel |
|---|---|---|
| `Fig.1/Fig.1b/upper row`, `bottom row` | 4 + 4 SEM .tif, 3072×2207 8-bit | Fig. 1b (1-mm / this protocol) |
| `Fig.1/Fig.1c` | 5 SEM .tif 2048×1886 | Fig. 1c |
| `Fig.1/Fig.1d` | 2 .tif (3072×2207, 6144×4415) | Fig. 1d |
| `Fig.2/Fig.2a` | `data.mat` (per-axon path length + discontinuities, 100 resamples, saved means, KS/t-test p), `Fig2a_data.mat` (same per-axon table), `.nml` webKnossos skeletons of the 20 traced axons | Fig. 2a (used) |
| `Fig.2/Fig.2b` | `Fig2b_data.mat` (path lengths of 308,424 H6, 599,706 H13, 323,349 control axons), `Fig2b.m` | Fig. 2b (used) |
| `Fig.2/Fig.2e` | 6 SEM .tif 3072×2207 | Fig. 2e |
| `Extended Data Fig. 1a-b` | 1 SEM .tif; `microCT/` 497 16-bit .tiff slices 492×505 (+Thumbs.db); `EDX/` `EDS raw data.doc` (a .docx: 3 EDAX reports), `Suppl_Fig1b.mat.mat` (profiles), `supp_fig1_EDS.m` | ED 1a, 1b (used) |
| `Extended Data Fig. 1f` | `SEM/` 4 .tif; `EDX/` TCH.doc, no TCH.doc, PG.doc (.docx EDAX reports) | ED 1f (used) |
| `Extended Data Fig.1g`, `1m` | 4 + 4 SEM .tif | ED 1g, 1m |
| `Extended Data Fig.1k` | `resin data.pzfx` (Prism XML, 14 Y columns) | ED 1k (used) |
| `Extended Data Fig. 1l` | `1. Fiji processed raw images/` 9 folders (named Fig.1c/1d/1e × core/intermediate/peripheral, an older figure numbering) with 500×500 subimages `im_*.tif` and Weka probability masks `mask*_*.tif` (118 .tif); `3. Calculated contrast values/contrast_data.mat` | ED 1l (used) |
| `Extended Data Fig.2` | 14 SEM .tif + 2 .jpg (2i, 2j overviews) | ED 2 |
| `Extended Data Fig.3/…-H4, H5, H6, H13, W3` | 20/20/16/13/24 SEM .tif; H4.pptx, H6.pptx (figure layouts) | ED 3 |
| `Extended Data Fig.4` | 8 .tif + 3 .png (4c center/middle/outer) | ED 4b–e |
| `Extended Data Fig.5/5a,5b,5c,5e,5f,5g,5h` | SEM .tif/.png/.jpg (16/4/4/2/2/2/2 files) | ED 5a–c, e–h |
| `Extended Data Fig.5/5d` | `data.mat`: UV-vis spectra of many solutions (data … data5); data4.os_vi_cac* used | ED 5d (used) |
| `Extended Data Fig.6/6b`, `6d,e`, `6m,n` | 3/2/2 .png | ED 6b, 6d,e, 6m,n |
| `Extended Data Fig.6/6j,k` | **Raman spectra** `data_batch1–3.mat` (MATLAB `table` objects), `data_round4.mat`, `peak_calibration_allrounds.mat` | **ED 5j,k** (used; folder name wrong) |

`code/`: MATLAB scripts per figure (`Fig.2a`, `Fig.2b`, `Extended Data Fig.1l`, `5d`, `6jk`) plus a large
`auxiliaryMethods` library (≈ 600 files). Read as text only, to reproduce the plotted processing.
No source data for: ED 1c–e, 1h–j, 4a, 4f–i, 5i, 6a, 6c, 6f–l, 7 (only some of these are plots: 1h, 4a, 4f, 4i).

## Text check (`tools/check_text.py`, version 2026-10-17f)

| file | coverage | without repeated text | tex tokens in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|
| `main.tex` vs article PDF | 97.6 % | 97.9 % (running text without figure labels: 99.1 %) | 100.0 % | 4 runs, 70 tokens | 0 |
| `supplement.tex` vs SI PDF | 96.6 % | 96.6 % | 98.6 % | 0 | 2 runs, 14 tokens |
| `reporting_summary.tex` | – (PDF has no text layer: 0 tokens) | – | – | – | – |

Explanations:
- **main, MISSING:** text printed inside Fig. 1 and Fig. 2 (panel labels, axis labels, tick numbers: 59 tokens in
  3 runs; described in `\alttext`), and the publisher line "Reprints and permissions information is available at
  www.nature.com/reprints" (11 tokens, left out as boilerplate, noted). Repeated: the footer "Nature Methods | Volume 20 |
  June 2023 | 836–840" with page numbers (35 tokens) and short runs "836"/"840", "Check for updates". The running header
  "Brief Communication https://doi.org/…" is given once at the top. Below the 98 % target only because of these
  figure labels and footers; the article’s own running text is 99.1 % covered, and an order-free token comparison
  (`work/scripts/bag_check.py`) leaves only headers/footers, figure labels and 4 hyphenation tokens (below).
- **main, short mismatches:** real hyphens at line ends that the tool's dehyphenation joins: "pyrogallol-related",
  "Micro-breakages" (ED captions), "large-volume" (Fig. 2 caption).
- **supplement:** the arrows of Supplementary Table 3 and the SI text are a Wingdings glyph that the text layer gives as
  "à" (glued to the next word: "àCaC" → token "acac"); transcribed as "→" from the page image. This causes most
  unmatched tokens and the EXTRA run "Os cac FecN cac Pg cac Os" (SI p. 12: "Os→cac→FeCN→cac→Pg→cac→Os" is one token in the
  PDF); the second EXTRA run ("KCl pH1 → KCl 24, pH7", Table 3 exp. 31) comes from the cell interleaving described next. Word wraps inside narrow table
  cells without hyphen ("Solutio|n", "Hemispher|e", "Pyrogal|lol", "Willingha|m", "forma|mide", "Amplificatio|n",
  "concentratio|n") were joined. The order-based check cannot follow the tables at all (the text layer interleaves the
  lines of neighbouring cells; the tool counts 298 such tokens as "inside figures"), so I added an **order-free token
  check**: `python3 -I work/scripts/bag_check.py <tex with → mapped back to à> <pdf>`: after mapping the arrows back,
  the only differences are the glued arrow tokens and the joined word wraps above: no word of the tables is missing or added.
- **reporting summary:** checked the same order-free way against tesseract OCR of 300-dpi renders
  (`work/scripts/bag_check_txt.py`; 1,146 OCR vs 1,142 tex tokens; differences are OCR'd checkbox marks only), and
  every answer box was read against a zoomed page image.
- Read-through against page images (step 4): subscripts/superscripts (OsO₄, e⁻ nm⁻², mm³, 10⁻⁴ Pa, (11.24 nm)², cm⁻¹,
  Os^VI, Os^viii O₄, OsO₂(OH)₂(CN)₂²⁻, Fe²⁺, CN⁻, 1st/2nd/3rd), ×, ±, ≥, °C, µ/μ as printed, \textasciitilde, en dashes in
  ranges, italic "Note added in proof", reference formatting (italic journals, bold volumes), table cells of all four
  supplementary tables.

## Errors and oddities in the paper (kept verbatim; `\decompnote` where it matters)

1. **Fig. 2a vs source data.** The caption gives a Kolmogorov–Smirnov P = 0.4814. The deposited `data.mat` holds the
   resampled inter-error distances; a two-sample KS test on them gives P ≈ 0.26 (asymptotic) or 0.28 (exact), and the
   saved `p` variable is 0.2039 (from the t-test that `Fig2a_MIED.m` runs last). The printed error bars (half-length ≈ 0.19 mm
   for both bars, the hemisphere one centred at 0.475 mm) do not match the saved resamples (0.186 and 0.176 mm); the
   hemisphere bar (0.470 mm) matches the saved scalar mIED_H6 (path 1405.75 µm) but not the saved per-axon table
   (1423.82 µm → 0.475 mm). The figure was evidently made from another random resampling than the one deposited.
2. **Methods, Statistics:** "mean inter-error distance was calculated as the total number of tracing errors divided by
   the total path length" is the inverse of the definition two sections earlier and of the plotted quantity (mm).
3. **ED Fig. 1 caption** cites "Hua protocol¹" and "pyrogallol;²": numbers of the *Supplementary* reference list (1 = Hua,
   2 = Mikula), not of the article (ref. 1 = Karnovsky, 2 = de Bruijn). "time⁻course" and "whole⁻brain" (ED 7) are printed
   with superscript minus signs.
4. **Non-existent items cited:** Methods "Supplementary Fig. 1h" (no supplementary figures exist; ED Fig. 1h shows the
   sampling positions); ED Fig. 3 caption "Supplementary Fig. 7" (ED Fig. 7 meant).
5. **Methods, 1-mm protocol:** "2% UA (17 h at 4 °C, 50 h at 50 °C)" (twice) vs 2 h at 50 °C in Supplementary Table 3 (exp. 1, 2)
   and elsewhere; Spurr's recipe "0.95 g ERL-4221, 5.9 g DER 736, 0.1 g NSA, 113 µl DMAE" (in four Methods sections) vs
   Supplementary Table 1 "4.1 g ERL 4221, 0.95 g DER 736, 5.9 g NSA, 113 μl DMAE".
6. **Pyrogallol concentration** is given as 4 % (Methods definitions; Supplementary Table 1), 2 % (Methods, human sample)
   and 3.75 % (Supplementary Table 2, "1.87 g Pg … in water").
7. **EDS:** Methods say 18 keV; the deposited reports say 10 kV (ED 1b) and 20 kV (ED 1f). Methods say mean ± s.d.;
   ED 1f plots single point measurements (the second report of each file) with ±2σ counting error, and the ED 1b points
   lie 0.2–0.5 wt.% above the deposited report values with bars of about ±1σ.
8. **ED 1b left:** the curve labelled "µCT" (red) is the .mat variable `sem2n` and "SEM" (blue) is `uct2n` (shapes match
   only this way round); and the source has only pixel indices, no µm.
9. **ED 5d:** legend "24 h"; the data field and the authors' script say "20h" (Methods: 24 h).
10. **ED 5j/5k:** the printed 1900–2300 cm⁻¹ window of 5j uses a different baseline/scale than the deposited script
    (printed FeCN peaks ~1.5/1.8 ×10⁴ vs 2.25 ×10⁴ from the script); 5k is rescaled (no multiplier on the axis, 1 unit ≈ 210 counts)
    and smoothed relative to the deposited spectra and script.
11. **Source-data labels:** the folder "Extended Data Fig.6j,k" (and code "Extended Data Fig.6jk") holds the ED Fig. 5j,k
    Raman data; the ED 1l subfolders are named "Fig.1c/1d/1e" after an older numbering.
12. Typos kept: SI "Joural", "Ultrasructure", "occured", "hexacyanoferratte", "Os acq" (Table 3, exp. 6), "FeCn"; ED 7
    "brekage", "diffufsion"; reporting summary "low-vaccum"; ED 1 caption "( j,k)" spacing; SI ref. 12 title garbled as printed.

## Problems and suggestions for the spec and tools

- `vector_dump.py` dropped horizontal/vertical lines (fixed by the coordinator during this run; I re-ran it for Fig. 2).
- **`check_text.py` cannot check tables**: PDF text layers interleave the lines of neighbouring cells, so table text
  ends up unmatched, and the new "inside figures" heuristic then silently drops it from the running-text coverage
  (SI: 100 % "running text" while the tables were not verified). Suggest adding an order-free multiset mode like
  `work/scripts/bag_check.py` (a few lines, uses the tool's own tokenizer) and reporting it alongside.
- Symbol/Wingdings glyphs (arrow → "à") should be normalised by font in `check_text.py` (map Wingdings 0xE0 to "→"
  and treat it as a token separator); otherwise every "→" costs a token and glues words.
- PDFs without a text layer (the reporting summary, also embedded as pp. 23–25 of the article) give 0 tokens. Suggest
  an OCR fallback in `check_text.py` (tesseract is installed) or a documented OCR-based check (`bag_check_txt.py`).
- Spec: no prefix for Extended Data figures (I used `edfig`); worth fixing for consistency across papers.
- Spec: no guidance for partial source data (here the y values were deposited but x only as pixel indices); I used
  "tier 1 for y, tier-3 calibration for x". A "mixed" provenance wording in the spec would help.
- MATLAB `table` objects in v5 .mat files are unreadable with plain `scipy.io.loadmat` (MatlabOpaque). `song_common.mat_tables`
  decodes them from `__function_workspace__`; this could go into `tools/` (h5py is not installed, but not needed here).
- The `.doc` files are .docx; pandoc reads them, and `song_common.docx_eds_reports` parses them with the stdlib.
  Mentioning both in the spec would save time.
- `digitize_common.py` could use a marker finder (opening + connected components; `song_common.find_markers`).
- `tools/check_text.py` output changed version during the run (new "running text" line); a version line in the spec's
  example output would make the numbers comparable across papers.
