# sun2019: decompiled

Fengzhen Sun, E. Kristofer Gamstedt. "Homogeneous and Localized Deformation in Poly(Methyl Methacrylate)
Nanocutting." *Nanomanufacturing and Metrology* **2019**, 2:45–55. DOI
[10.1007/s41871-018-0034-7](https://doi.org/10.1007/s41871-018-0034-7).
Received 17 September 2018; revised 7 December 2018; accepted 17 December 2018; published online 1 February 2019.

**Licence:** © The Author(s) 2019; open access under the Creative Commons Attribution 4.0 International License
(CC BY 4.0), as stated on p. 10 ("Open Access").

What the paper is (from its text): ultramicrotome nanocutting of PMMA with a 40° diamond knife at cutting
thicknesses 60–200 nm (v0 = 1.0 mm/s) and speeds 0.25–10 mm/s (t_u = 85 nm), with cutting/thrust forces
(Tables 2–3), chip thickness and shear-plane angle (Figs. 3, 6), AFM of the cut surfaces (Figs. 4, 7, 8), a
Komanduri–Hou adiabatic-shear model (Fig. 10, critical v0 ≈ 4.7 mm/s) and Abaqus/Explicit FE simulations of
the chip (Figs. 11–14). (The task message called it an FE/experimental study of ultramicrotome cutting of
PMMA; the PDF's title and author list above win.)

## Source files

| file | what it is |
|---|---|
| `source/sun2019.pdf` | the article, 11 pp., **publisher version of record** (Springer typesetting, "Check for updates" button, Springer footers; PDF metadata: Creator "Springer", Acrobat Distiller 10.1.8, 2019-01-31). Copied from `papers/sun2019/sun2019.pdf`. Fetch note (`papers/sun2019/SOURCE.txt`): "sun2019.pdf: https://d-nb.info/1181762847/34 (DNB copy of OA article doi:10.1007/s41871-018-0034-7; Springer link gave bot page) curl 2026-10-13 by simulation agent". |
| (`papers/sun2019/sun2019.txt`, `sun2019_raw.txt`) | earlier text extractions in the papers folder; not used, not copied. |

Not available: the paper names no data set, supplement or source-data file. The underlying experiments are
in refs. [7] and [8] (Figs. 2, 5, 8, 10 are "from [7]"/"from [8]"; Fig. 1 "adopted from [7]").

**Cited works in this collection** (keys from `decompile_work/manifest.json`, identity checked against the
local PDFs' first pages/titles): ref. [2] Atkins 2016 Interface Focus = `atkins2016`; ref. [7] Sun et al. 2017
Eng Fract Mech 182:595 = `sun2017efm`; ref. [12] Atkins 2003 Int J Mech Sci 45:373 = `atkins2003`; ref. [14]
Patel, Blackman, Williams 2009 Eng Fract Mech 76:2711 = `patel2009`. Ref. [8] (Sun et al. 2017 Int J Solids
Struct 129:40) has no key of its own; it is listed as Paper II in the list of papers of `sun2017thesis`
(the local thesis PDF has 52 pages). Related but not cited: `sun2018ijms` (same authors, shear banding in
nanomachining of a glassy polymer, Int J Mech Sci 151, 2018).

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal line, title, authors, corresponding
  author and affiliations (a footnote on p. 1, placed after the author line), dates, abstract, keywords,
  Sections 1–5, Tables 1–3, Equations (1)–(6), Figures 1–14 with verbatim captions and descriptions,
  acknowledgements, open-access licence, references 1–22 and the two author biographies with their photos.
  Left out: running headers/page numbers, the Springer footer logo ("13" in the text layer), the
  "Vol.:(0123456789)" stamp, the "Check for updates" button and the ORCID icon (noted in the file).
- `figures/`: every figure rendered at 200 dpi from the PDF (`fig1.png` … `fig14.png`, plus `bio_sun.png`,
  `bio_gamstedt.png`); per plotted panel `<panel>.csv`, `<fig>_extract.py`, `<fig>.py`, `<fig>_replot.png`.
- `tables/`: `table1.csv`, `table2.csv`, `table3.csv` (caption in `#` lines). **Tables 2 and 3 are the
  measured forces** (F_c/w_u and F_t/w_u in N/m vs t_u and vs v0).
- `tools/`: `digitize_common.py` (copied from the osmium tools), `fe_contour.py` and `fe_extract_common.py`
  (FE contour-map classification, written for this paper), `afm_map.py` (AFM colour-bar conversion, written
  for this paper). Scripts import them via `Path(__file__).resolve().parent.parent / "tools"`.
- `decomp.sty`: copied from the osmium tools, so `lualatex -interaction=nonstopmode -halt-on-error main.tex`
  compiles from this folder.
- `work/`: scratch (page renders `work/pages/`, embedded images `work/emb/`, overlays, classified-map checks,
  side-by-side comparisons `cmp_*.png`, probe scripts, `afm_roundtrip.py`). May be deleted.

Re-run the data: `python3 -I -B figures/<fig>_extract.py`, then `python3 -I -B figures/<fig>.py` (any working
directory). All extraction scripts read the embedded images straight from `source/sun2019.pdf`.

## Figures

All figures are **raster images** at 300 ppi (JPEG: Figs. 1, 2, 4, 5, 7, 10, 11 and the photos; lossless: Figs. 3, 6,
9 (greyscale), 8 and 12–14 (RGB)). `vector_dump.py` finds no plot paths in any figure area (only one clip/background
rectangle per region), so there is no tier 1 or 2; every data panel is **tier 3 (digitized)**.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 | photograph of the instrumented ultramicrotome set-up, 3 labels | – | – | |
| Fig. 2a, 2b | light micrographs (CCD) of chips, t_u = 60 / 140 nm, width arrows 0.60 / 0.47 mm | – | – | |
| Fig. 3 | line plot, 2 y axes: chip thickness and shear plane angle vs cutting thickness | `figures/fig3.csv` | 3 | category x axis (6 evenly spaced labels); marker centres |
| Fig. 4a, 4b | AFM height maps, t_u = 60 / 140 nm, colour bar ±25.0 nm, 400 nm scale bar (in a) | `figures/fig4a.csv`, `fig4b.csv` | 3 | height grid via colour bar; (b) has no own scale bar |
| Fig. 5a, 5b | light micrographs of chips, v0 = 0.25 / 10.0 mm/s, 0.61 mm arrows | – | – | |
| Fig. 6 | line plot, 2 y axes: chip thickness and shear plane angle vs cutting speed | `figures/fig6.csv` | 3 | marker centres |
| Fig. 7a, 7b | AFM height maps, v0 = 0.5 / 3.0 mm/s, colour bar ±3.0 nm, 400 nm scale bars | `figures/fig7a.csv`, `fig7b.csv` | 3 | height grid via colour bar |
| Fig. 8 | line plot, 5 AFM height profiles (offset) vs distance | `figures/fig8.csv` | 3 | per pixel column; gaps where a line crosses its own label |
| Fig. 9 | schematic of shear localization (Komanduri–Hou), labels 1–5, α, ϕ, ϕ′, t_c, t_u | – | – | transcribed in `\alttext` |
| Fig. 10 | line plot, τ_PSZ and τ_Bulk vs cutting speed, "Critical v0 = 4.7 mm/s" line | `figures/fig10.csv` | 3 | per pixel column; includes the drawn line position and the traced crossing |
| Fig. 11 | FE model screenshot (mesh, knife, BCs, inset with 40° and cutting plane) | – | – | |
| Fig. 12a–c | FE PEEQ contour maps, t_u = 85 nm, v0 = 0.01 / 0.1 / 1.0 mm/s | `figures/fig12a.csv` … `fig12c.csv` | 3 | band code per pixel through each panel's colour key; no length scale |
| Fig. 13a–c | FE PEEQ contour maps, t_u = 200 nm, v0 = 0.01 / 0.1 / 1.0 mm/s | `figures/fig13a.csv` … `fig13c.csv` | 3 | as Fig. 12 |
| Fig. 14a–b | FE PEEQ contour maps, CPE3 triangles, t_u = 85 nm, v0 = 0.1 / 1.0 mm/s | `figures/fig14a.csv`, `fig14b.csv` | 3 | as Fig. 12 |
| author photos (p. 11) | portrait photographs | – | – | `bio_sun.png`, `bio_gamstedt.png` |

Counts: **16 data panels, all tier 3** (line/marker plots Figs. 3, 6, 8, 10; AFM height maps 4a, 4b, 7a, 7b;
FE contour maps 12a–c, 13a–c, 14a–b); 11 image-only panels (Figs. 1, 2a, 2b, 5a, 5b, 9, 11 and the two photos).
Every image panel has an `\alttext`.

**How the data were obtained and checked**

- *Line/marker plots (Figs. 3, 6, 8, 10):* frame lines and tick marks located in the embedded image, linear
  pixel→data fit per axis on the ticks (and labelled frames); residuals in each CSV header (all ≤ 0.5 nm or
  0.04 MPa, i.e. under 1 px). Markers (Figs. 3, 6) by connected components after a 9 px morphological opening;
  the overlapping circle/square at t_u = 140 nm in Fig. 3 from their outer edges (flagged). Fig. 8 lines by
  colour masks per pixel column, following the line through its own label (the labels of v0 = 1.0, 3.0 and 10.0
  overlap their lines; in those boxes the line is followed along its extrapolated path, columns where it merges
  with a letter are left empty, and every value inside a label box is flagged). Fig. 10: red line by colour mask,
  dashed black line by a grey mask with the printed labels masked out (gaps between dashes stay empty).
  Each extraction draws its points back on the source image (`work/fig3_overlay.png`, `fig6_overlay.png`,
  `fig8_overlay.png`, `fig10_overlay.png`; I looked at all, including zooms of the label crossings in Fig. 8)
  and each re-plot was put next to the original with `tools/compare.py` (`work/cmp_fig*.png`, all looked at):
  series, ranges and scales match.
- *Consistency check (my own computation, not in the paper):* Eq. (2) with α = 40° applied to the digitized
  chip thicknesses of Fig. 3 gives ϕ = 47.6°, 54.0°, …, 53.9° for t_u = 60, 85, …, 200 nm, against the digitized
  47.3°, 54.0°, …, 53.7°; for Fig. 6 (t_u = 85 nm) 63.6° and 56.3° at 0.25 and 1 mm/s, as digitized. So the
  plotted angles follow from the plotted chip thicknesses through Eq. (2), and the digitization is good to a few
  tenths of a degree.
- *FE contour maps (Figs. 12–14):* the embedded images are lossless and flat-shaded; the model colours are the key
  colours × 206/255 (Abaqus lighting; verified on the most frequent colours). Every pixel is assigned the band of
  the nearest model colour (RGB distance ≤ 30); white, knife grey, annotation boxes (key, panel label, axis
  triad) and unclassified pixels (black outlines, anti-aliased band boundaries) get their own codes. The grey
  top band (PEEQ > 3, present in the keys of 12a, 13a, 13c, 14a, 14b) cannot be separated from the knife's and
  the image border's anti-aliased grey edges, so it is not classified (left '#'). Check: `work/fig*_classified.png`
  (source strip next to the classified map) and `work/cmp_fig12/13/14.png` (looked at): band layout, shear
  bands and cut-surface spikes reproduce. The figures have **no length scale**, so positions are image pixels.
  Each CSV is one row per pixel row with a 1418-character code string (~1 MB per panel).
- *AFM maps (Figs. 4, 7):* the printed colour bar is sampled down its centre between its frame lines (ends = the
  printed ±25.0 / ±3.0 nm, linear in between); each pixel gets the height of the nearest bar colour(s). Labels,
  arrows, scale bars, the colour-bar box and the panel edges next to the white separators are masked (empty).
  Round trip heights → bar colours vs printed pixels (`work/afm_roundtrip.py`): median colour error 4.3/4.4
  (Fig. 4a/b) and 2.2/2.4 (Fig. 7a/b) RGB units, 95th percentile ≤ 7 – about JPEG noise. Side-by-side
  `work/cmp_fig4.png`, `cmp_fig7.png` looked at. Scales: Fig. 4a bar 400 nm = 152 px (2.63 nm/px); Fig. 7a
  123 px, 7b 124 px (≈ 3.24 nm/px). These are printed images of resampled AFM data: use local averages, not
  single pixels. CSVs are one row per pixel row (≈1.5–2.2 MB each).
- Data volume: the 12 map CSVs total about 15 MB.

## Tables

`tables/table1.csv` (settings), `table2.csv` (forces vs t_u at v0 = 1.0 mm/s), `table3.csv` (forces vs v0 at
t_u = 85 nm); all cells checked against the page images.

## Text check (`check_text.py` version 2026-10-17j, no special options; `--min-run 1` for the listing)

`python3 -I -B .../tools/check_text.py main.tex source/sun2019.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF |
|---|---|---|---|---|
| `main.tex` | **98.4 %** | 98.4 % (0 repeated tokens) | 98.4 % (0 in-figure tokens) | 99.2 % |

All figure labels are inside raster images, so the PDF text layer has no in-figure text. Every MISSING run is
explained: page numbers 46–55 and the Springer footer logo glyph "13" on every page (the repeated-text filter
does not catch them because the number changes / the run is too short), the "Vol.:(0123456789)" stamp (p. 1),
the "Check for updates" text, equation numbers and display-math tokens of Eqs. (2), (4), (5), (6) (the text
layer orders math differently from LaTeX: "tan 1 t u cos …", "exp u 2 udu", limits l s and 0), and the
licence URL, which the text layer splits as "creat iveco mmons" (zero-width breaks). The EXTRA runs are the same
equation tokens in LaTeX order and "creativecommons org"; there is no EXTRA run of the paper's prose.

Read-through against page renders (spec step 4): Eqs. (1)–(6) incl. tan⁻¹, sinh⁻¹, the ^{1/n} exponent and
slashed fractions in (5) and (6), dotted ε, Δ*H*_β, *α*_t; subscripts t_u, v_0, w_u, l_u, w_c, l_c, F_c, F_t,
τ_y, τ_PSZ, τ_Bulk, σ_i(0), k_B, V_a, G_c; "~ 10⁻⁷ m²/s", "~ 110 MPa", "~ 10 J/m²", "~ 1.5 J/m²", "≥ 85 nm",
en dashes in page ranges and in "Komanduri–Hou", "isothermal–adiabatic", "cube–square"; Table cells.

## Errors and oddities in the paper (kept verbatim)

- Sect. 4.1, after Eq. (6): "The values of the parameters in Eq. (5) can be found in Richeton et al. [3]" – the
  parameters listed are those of Eq. (6) (`\decompnote` in `main.tex`).
- Fig. 10: the vertical line is drawn at **4.81 mm/s** (digitized) and the traced curves cross at **4.78 mm/s**,
  while the label says "Critical v0 = 4.7 mm/s" and the text "4–5 mm/s". Small, but the line and label disagree
  by about 1.5 px of the source image (recorded in `fig10.csv`).
- Sect. 3.2.1 says chip thickness "increases monotonically … from 0.25 to 1.0 mm/s and then decreases slightly";
  Fig. 6 shows it falling to ≈ 92 nm at 3 mm/s and rising again to ≈ 96 nm at 10 mm/s.
- Sect. 4.2 calls CPE4R a "4-node quadratic plane strain element"; *background knowledge, not from the paper:*
  CPE4R in Abaqus is a 4-node bilinear element (and Sect. 4.2.3 later calls the elements "quadratic" again).
- Ref. 19 journal abbreviation "Arch Compt Methods Eng"; *background knowledge:* the journal is Archives of
  Computational Methods in Engineering ("Arch Comput Methods Eng").

## Known problems of this decompilation

- Fig. 8: in 14 pixel columns where the v0 = 1.0 and 3.0 lines cross their own labels the height is left
  empty, and values inside the label boxes (flagged) can be pulled by up to ~0.3 nm towards the letters (the
  v0 = 3.0 line around 325–350 nm runs along the tops of the "mm" letters).
- Figs. 12–14: the grey PEEQ band (> 3) is not classified (see above); the panel strips' rows are given in the
  extract scripts.
- Figs. 4, 7: heights at the colour bar's saturated ends are clipped (none or only a few pixels reach them);
  Fig. 4b's lateral scale is not printed.

## Time

About 1 h 45 min wall-clock: reading spec, tools and pages ~15 min; four line plots with checks ~35 min;
FE and AFM colour maps ~30 min; transcription and descriptions ~20 min; checks and README ~10 min.
