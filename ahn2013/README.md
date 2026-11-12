# ahn2013: decompiled

Se Hyun Ahn, Shuqiang Yang, Mike Miller, Maha Ganapathisubramanian, Marlon Menezes, Jin Choi, Frank Xu, Douglas J.
Resnick, S. V. Sreenivasan (Molecular Imprints, Inc., Austin, Texas). "High-performance wire-grid polarizers using
jet and Flash™ imprint lithography." *J. Micro/Nanolith. MEMS MOEMS* **12**(3), 031104 (Jul–Sep 2013), 9 pp.
DOI [10.1117/1.JMM.12.3.031104](https://doi.org/10.1117/1.JMM.12.3.031104). Paper 13038SSP received Apr. 2, 2013;
revised manuscript received Jun. 6, 2013; accepted for publication Jun. 19, 2013; published online Aug. 12, 2013.

All of this is from the PDF (title block and abstract block on PDF p. 2, running header "J. Micro/Nanolith. MEMS
MOEMS 12(3), 031104 (Jul–Sep 2013)"); it agrees with the task message and `source/SOURCE.txt`.

**Licence**, as printed on PDF p. 2 (journal p. 031104-1): "© The Authors. Published by SPIE under a Creative Commons
Attribution 3.0 Unported License. Distribution or reproduction of this work in whole or in part requires full
attribution of the original publication, including its DOI." (`SOURCE.txt` notes that Crossref's metadata says
CC BY 4.0; the PDF's own statement, CC BY 3.0, is what this entry follows.)

Why it is in the library: another session (deep-UV near-field grating imaging idea) cites it for roll-based jet-and-flash
imprint of wire-grid polarizer gratings. The paper's own statements on pitch and patterning method are collected below.

## Source files (`source/`)

| file | what it is |
|---|---|
| `ahn2013_jm3_12_3_031104.pdf` | 10 pp., **publisher's version of record** (SPIE Digital Library; Arbortext APP 9.1, Acrobat Distiller 6.0.1, 10 Aug 2013). PDF p. 1 is an SPIE cover page (journal artwork image, title, author names, SPIE logo); the article is PDF pp. 2–10 = journal pp. 031104-1 to 031104-9. Born-digital text layer in embedded Type 1C "AdvTT…/AdvOT…" fonts, WinAnsi encoding, no ToUnicode map except two symbol subsets; the WinAnsi codes decode correctly (checked below). Figures: 14 raster images (JPEG or Flate, 300 ppi) and one vector figure (Fig. 9); see the figure table. |
| `SOURCE.txt` | provenance (download 2026-11-12 via the DOI, browser slot 2) |

`retrieval/` holds the retrieval sheet and was left unchanged. The paper names no data set, source data or
supplementary material, so no tier-1 source exists. "Biographies and photographs of the authors not available." is
printed at the end (p. 10); there are no biographies or author photos.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: the cover page's text (p. 1), the journal line, title,
  authors and affiliation, abstract with licence and DOI, subject terms, received/accepted dates, Secs. 1–5,
  Acknowledgments, References 1–24, the closing line about biographies; Figs. 1–14 with verbatim captions,
  descriptions and data references. Written by `work/build_main.py` (do not edit by hand). Compile:
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice): no errors, no missing glyphs, no overfull boxes
  (18 pages).
- `figures/fig1.png` … `fig14.png`: each figure rendered from the PDF at 200 dpi (`tools/crop.py`, image or drawing
  bbox + 2 pt; `work/make_figures.py`).
- `figures/*.csv`: data of the 24 plotted panels (table below), with `fig5_extract.py`, `fig6_extract.py`,
  `fig8_extract.py`, `fig9_extract.py`, `fig11_extract.py` … `fig14_extract.py` (make the CSVs) and `fig5.py` …
  `fig14.py` (re-plot them, `*_replot.png`). Re-run from any directory: `python3 -I -B figures/fig5_extract.py`, then
  `python3 -I -B figures/fig5.py`. The extract scripts import `work/digi.py` (shared raster helpers on top of
  `tools/digitize_common.py`) and `work/markers.py` (Figs. 13, 14); the plot scripts `work/replot_common.py`.
- `tables/`: none; the paper has no tables.
- `work/*.py` (kept with the entry, each with a docstring): `build_main.py` (the build), `figure_texts.py` (the
  decompiler's descriptions and notes), `make_figures.py`, `digi.py`, `markers.py`, `replot_common.py`, `qa_sheet.py`,
  `er_ratio.py` (the Fig. 11 check below), and probes used to set up the extractions (`inventory.py`, `line_list.py`,
  `special_chars.py`, `render.py`, `zoom.py`, `img_zoom.py`, `extract_images.py`, `axes_probe.py`, `tick_probe.py`,
  `label_probe.py`, `colour_probe.py`, `pix.py`, `dbg_runs.py`, `vd_summary.py`, `fig9_probe.py`, `fig9_path.py`,
  `summarize_csv.py`, `grid_sheet.py`). Everything else in `work/` (page renders, extracted images, sheets, overlays,
  compare images, logs) is scratch.

## How the text was made

`work/build_main.py` reads every text line of the PDF with PyMuPDF (spans with font, size and baseline). Running
headers (y < 50 pt) and footers (y > 765 pt) are dropped; the p. 2 header (the journal line) is kept once as the journal
block. Lines inside figure areas and caption boxes are taken out of the running text; captions are placed with their
figures. Bold / italic fonts become `\textbf` / `\textit`; spans smaller than the line and raised above its baseline
become `\textsuperscript` (citation numbers, cm⁻², µm², 10⁴); a space is added where two spans have a visible gap but
the text layer has none ("Flash™ imprint"). Body text is read left column, then right column; justified lines that
PyMuPDF splits into one line per word (reference 1) are regrouped by baseline. A new paragraph starts at an indented
line, a heading (bold or italic 9.96 pt) or a reference number.

Line-end hyphens: removed except where the joined word is a hyphenated compound (decisions printed by
`python3 -I -B work/build_main.py --raw`): kept in metal-oxide-semiconductor, spin-coated, high-resolution, roll-based,
wire-grid, high-density, paper-like (ref. 2); removed in "imprint non-/fill" → "nonfill" (the paper writes "nonuniform"
elsewhere; the hyphen could be real). The one exact correction (`CORR`) only renders the ratio sign of "3∶1" (p. 4,
U+2236) in DejaVu Sans Mono, since DejaVu Serif has no glyph for it.

Fonts: the "Adv…" fonts have no Unicode map but WinAnsi encoding, and every special character in the text layer was
listed (`work/special_chars.py`: –, “ ”, ™, ©, ×, ∶, −, µ) and compared with 400-dpi crops (µm², 10⁴ cm⁻², ×, ∶, ™ in
"J-FIL™", ">80%", the "5 mm" on p. 9) and the reference list and licence block at 200 dpi
(`work/sheets/zoom_chars1.png`, `zoom_refs.png`). No glyph decodes wrongly, so no `--glyph-map` was needed. The
spaces before closing quotes in the references (", ” Proc. SPIE") and the opening ” of ref. 23 are as printed.

## Text check (`tools/check_text.py` 2026-11-07a)

`python3 -I ../tools/check_text.py main.tex source/ahn2013_jm3_12_3_031104.pdf` (no options needed):

| measure | value |
|---|---|
| coverage of PDF tokens | 97.5 % |
| without text repeated on ≥ 3 pages (96 tokens) | 99.6 % |
| also without unmatched in-figure text (14 tokens) | 100.0 % |
| tex tokens found in PDF | 100.0 % |
| MISSING runs ≥ 6 / EXTRA runs ≥ 6 | 0 / 0 |
| `--words-only` | 98.7 % / 98.7 % / 99.6 %; 100.0 % of tex words in PDF |

Everything unmatched is page furniture: the repeated text is the running header "Ahn et al.: High-performance
wire-grid polarizers using jet and Flash™imprint lithography" (pp. 3–10) and the footers "J. Micro/Nanolith. MEMS
MOEMS 031104-N Jul–Sep 2013/Vol. 12(3)"; at `--min-run 1` the only MISSING run is "flashtmimprint lithography" (p. 10,
the header's "Flash™imprint" read as one token). The 14 "in-figure" tokens are header/footer tokens too: with every
page's header and footer band excluded (`--exclude P:0,0,630,50 --exclude P:0,765,630,810` for P = 1…10) coverage is
100.0 % at every level and the only EXTRA run is the journal line kept from the p. 2 header. Figures carry no
text-layer text (their labels are in the raster images or, in Fig. 9, glyph outlines).

Read-through (step 4): no equations; special characters, superscripts, italics and bold volume numbers checked as
above; the reading order around figures is noted in `main.tex` where a `[p. N]` marker comes before a figure printed
on the previous page (Figs. 4, 7, 9–12, 13) or out of order (p. 7 holds only Figs. 10 and 11, so its marker follows the
[p. 8] marker).

## Figures

`vector_dump.py` / `get_drawings()` find vector paths only on p. 6 (Fig. 9: 524 filled paths); every other figure is a
single embedded raster image with no vector overlay and no text layer. The two small indexed images on p. 6
(225×212, 229×208 px) are the drop-shadowed legend box backgrounds of Fig. 9(a) and (b) (white boxes; the legend
entries are vector paths on top). On p. 1 the 2629×3265 grey JPEG is the cover page background with the journal name
and SPIE logo, the 2629×409 RGB JPEG the dark red "SPIEDigitalLibrary.org/jm3" band (both described in a note, not
figures).

Raster plots (tier 3) are digitized from the embedded images at native resolution: axes from tick marks (darkness
centroids next to the axis line; Excel/Origin ticks are blurred grey) or, where an axis has no visible ticks, from
tick-label centres; Figs. 8, 13 and 14 from their gridlines. Series by colour masks (OpenCV HSV). Thin lines crossed by
other ink (the black moving averages in Figs. 5 and 6, all curves of Figs. 11 and 12) are followed as the smooth path
of most ink (dynamic programming, `work/digi.py`), with legend boxes, annotation boxes and the ellipses/arrows around
the Fig. 11/12 curves masked. Noisy traces (Figs. 5, 6 purple ER, Fig. 8) are given as the range their ink covers in
each pixel column. Fig. 13/14 values come from each series' line on both sides of its marker (marker centre as a
check; where markers of two series overlap, the hidden part biases the marker centre, so the line value is preferred).

Fig. 9 (tier 2) is extracted from the vector paths: every line is a filled outline (dashes are separate closed
subpaths, tick marks grey filled rectangles, labels glyph outlines); outlines are cut at every 10 nm (their vertex
spacing) and the stroke centre taken; axes from the tick rectangles (max residuals 0.055 nm in x, 0.00013 in
transmission, 0.0023 decades in ER). Series
identity from dash length matched to the legend samples (100nmAl 9.3 pt dashes, 150nmAl 3.5 pt, 200nmAl 4.7 pt,
250nmAl solid). The outlines run far beyond the axes box (about 200–1200 nm) and are hidden there by the PDF's clip
path; those values are kept in the CSVs with `in_plot = 0` (not printed in the paper's figure); points under the grey
"Increasing Al thickness" arrow are marked in a `note` column.

**Checks:** every extraction draws its points back onto the source (`work/fig*_overlay.png`; Fig. 9 on a 300-dpi
render), and every re-plot was put next to the original with `tools/compare.py` (`work/cmp_fig*.png`; overlay and
compare together in `work/sheets/qa_fig*.png`). I looked at all of them: every overlay (Figs. 13/14 and the Fig. 11/12
curves near the ellipses and legends also as 1:1 crops) and the compare images of all eight plotted figures in their
final form. Faults found this
way and fixed: Fig. 5 TM start cut off (row window), Fig. 5/6 moving averages lost under the purple trace (now
dynamic-programming paths), Fig. 6 purple range inflated by colour fringes of the black annotation text (masked),
Fig. 11/12 TE path jumping onto the blue arrow and ellipse (masked, plus a despike filter) and the legend masks cutting
the TM maxima (narrowed).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 | schematic of the imprint tool concept (rolls R1/R2, roll module, template, inkjet, stage) | – | – | description, labels transcribed |
| Fig. 2(a), (b) | photographs of the LithoFlex 100 and its enclosure | – | – | description only |
| Fig. 3 (two images) | SEM cross-sections of the silicon master (65 nm half pitch) | – | – | data bars transcribed |
| Fig. 4(a) | photograph of the imprinted PC film roll | – | – | description only |
| Fig. 4(b), (c) | SEM top views "Imprint 1", "Imprint 1012" with insets | – | – | inset measurement labels blurred (read as about 60.3 / 99.1 nm in (b)) |
| Fig. 5 left | line plot, TM / TE transmission vs wavelength | `figures/fig5left.csv` | 3 | JPEG |
| Fig. 5 right | line plot, ER(L-B) (noisy, range per column) + unlabelled black line | `figures/fig5right.csv` | 3 | spikes clipped at 7000 flagged |
| Fig. 6 left | line plot "Transmission", TM / TE | `figures/fig6left.csv` | 3 | Flate |
| Fig. 6 right | line plot "Extinction Ratio", ER (range per column) + 200 per. Mov. Avg. (ER) | `figures/fig6right.csv` | 3 | |
| Fig. 7 | photographs TM / TE of the 5.7-in. film polarizer on a display | – | – | description only |
| Fig. 8(a) | line plot, ER (TM/TE) vs wavelength, 0–6000 | `figures/fig8a.csv` | 3 | centre + ink range |
| Fig. 8(b) | line plot, ER (TM/TE), 0–50000, cut at about 725 nm | `figures/fig8b.csv` | 3 | |
| Fig. 9(a), (b) | line plots, transmission vs wavelength, 4 Al thicknesses | `figures/fig9a.csv`, `fig9b.csv` | 2 | vector; hidden out-of-box parts `in_plot = 0` |
| Fig. 9(c), (d) | line plots, ER (log) vs wavelength, 4 Al thicknesses | `figures/fig9c.csv`, `fig9d.csv` | 2 | vector |
| Fig. 10(a), (b) | SEM top views of etched gratings (defects in (a)) | – | – | data bars transcribed |
| Fig. 11(a) left | TM (left axis) / TE (right axis) transmission, defect free | `figures/fig11a_left.csv` | 3 | Flate; TE dashed |
| Fig. 11(a) right | the same, 250 nm × 250 nm clear defect | `figures/fig11a_right.csv` | 3 | |
| Fig. 11(b) left | ER vs wavelength, defect free | `figures/fig11b_left.csv` | 3 | |
| Fig. 11(b) right | ER vs wavelength, clear defect | `figures/fig11b_right.csv` | 3 | |
| Fig. 12 left | TM / TE transmission, opaque defect | `figures/fig12left.csv` | 3 | Flate |
| Fig. 12 right | ER vs wavelength, opaque defect | `figures/fig12right.csv` | 3 | |
| Fig. 13(a) left / right | transmission / ER vs clear-defect density (category axis), 150 nm defect | `figures/fig13a_left.csv`, `fig13a_right.csv` | 3 | JPEG; markers |
| Fig. 13(b) left / right | the same, 5 µm defect | `figures/fig13b_left.csv`, `fig13b_right.csv` | 3 | |
| Fig. 14(a) left / right | transmission / ER vs opaque-defect density, 150 nm defect | `figures/fig14a_left.csv`, `fig14a_right.csv` | 3 | JPEG; markers |
| Fig. 14(b) left / right | the same, 5 µm defect | `figures/fig14b_left.csv`, `fig14b_right.csv` | 3 | |

Panels per tier: tier 2 (vector): 4 (Fig. 9a–d); tier 3 (digitized): 20 (Figs. 5 ×2, 6 ×2, 8 ×2, 11 ×4, 12 ×2,
13 ×4, 14 ×4); description only: Figs. 1, 2(a)(b), 3, 4(a)–(c), 7, 10(a)(b).

Uncertainties (in each CSV header): about one source pixel: Fig. 5 ±0.7 nm, ±0.3 % / ±16; Fig. 6 ±0.7 nm, ±0.25 % /
±9; Fig. 8 ±0.6 / ±0.5 nm, ±12 / ±100 (plus the thick line itself, given as er_min / er_max); Figs. 11/12 ±0.5 nm,
±0.0017 (TM), ±3.4e-6 / ±1.7e-5 (TE), ±1.7–6.8 (ER); Figs. 13/14 ±0.0022 (transmission), ±11 (ER), more where lines
touch (the Fig. 14(a) transmission gridlines fit only to 0.004, i.e. 1.7 px). Fig. 9 is exact to the PDF's precision.

## What the paper says about pitch and patterning method (verbatim, PDF page / journal page)

- p. 2 / 031104-1, abstract: "We have developed a roll-based J-FIL process and applied it to a technology demonstrator
  tool, the LithoFlex 100, to fabricate large-area flexible bilayer wire-grid polarizers (WGPs) and high-performance
  WGPs on rigid glass substrates."
- p. 3 / 031104-2, Sec. 1: "introducing a novel concept: inkjet-based plate-to-roll nanopatterning." … "we have used the
  LithoFlex 100 to fabricate high-performance wire-grid polarizers (WGPs) on both fused silica wafers and flexible
  polycarbonate (PC) films."
- p. 3, Sec. 2.1: "Imprinting is performed by moving the roll module and the template is only translated up or down."
  (Fig. 1 labels the film "PET PEN PC".)
- p. 3, Sec. 2.2: "The template blank is a 6-in. fused silica wafer" … "The primary pattern consisted of 50- and 65-nm
  half-pitch gratings." … "a step and repeat J-FIL tool was used to replicate the pattern on to the 6 in. round blank."
  … "Larger area templates were created by patterning a 300-mm silicon wafer using an immersion-based 193-nm scanner."
  … "Scanning electron microscopy (SEM) images of a grating master with a 65-nm half pitch are shown in Fig. 3."
- p. 4 / 031104-3, Fig. 3 caption: "SEM cross-sections of a silicon master. The grating half pitch is 65 nm."
- p. 4, Sec. 2.3: "curvilinear 120-nm features on a 300-nm pitch"; "A second longevity experiment using a 50-nm grating
  with a 20 mm × 20 mm field was also run."
- p. 4, Sec. 3.1: "Using imprinted 50-nm half-pitch gratings (covering a 50 mm × 50 mm area), samples of a bi-layer
  wire-grid polarizer were fabricated by depositing a thin layer of aluminum (Al) over the printed resist."
- p. 5 / 031104-4, Fig. 5 caption: "50 mm × 50 mm bilayer wire-grid polarizer (WGP) fabricated on a film using
  roll-based jet and flash imprint lithography (J-FIL) and Al deposition."
- pp. 5–6, Sec. 3.2: "Al-based WGPs formed on glass are typically fabricated by depositing the Al on the glass,
  patterning the resist grating, and then using the resist as mask to etch the Al. Gratings with half pitches on the
  order of 50 nm …" … "Initial performance results patterned with an older template with a half pitch of 50 nm are
  compared with the performance of a newer template with a half pitch of 65 nm in Fig. 8(a) and 8(b)." Fig. 8 caption
  (p. 6): "Etched wire-grid polarizers patterned with two different imprint templates."
- p. 6 / 031104-5, Sec. 4.1 (simulation): "Both a 100- and 130-nm pitch WGP are shown below."
- p. 7, Fig. 10 caption: "(b) a WGP made from an automated J-FIL process."; p. 9, Sec. 4.2: "the Al line size and pitch
  were set to 50 and 100 nm, respectively."
- p. 9 / 031104-8, Conclusions: "the LithoFlex 100, was successfully implemented for roll-based J-FIL patterning on
  continuous PC films." … "a prototype roll-based J-FIL tool was assembled and successfully tested. Several different
  templates, including 50-nm half-pitch gratings and 25-nm half-pitch dense hole arrays, were used to evaluate the
  imprinting scheme. The system has been used to fabricate large-area flexible bilayer WGPs as well as high-performance
  WGPs on glass." … "now being routinely achieved at pitches of 100 and 130 nm."

The paper calls the process "roll-based" and "plate-to-roll"; "roll-to-plate" occurs only in the title of ref. 6, and
"roll-to-roll (R2R)" describes the field (abstract, Sec. 1) and the title of ref. 20. The roll-imprinted film WGPs
use 50-nm half-pitch gratings; 65 nm half pitch appears for the silicon master (Fig. 3) and the newer template of the
etched glass WGP (Fig. 8(b)); Sec. 3.2 does not name the tool used for the glass WGPs (the abstract, Sec. 1 and the
Conclusions say the LithoFlex 100 / the system made WGPs on glass).

## Errors and inconsistencies in the paper (kept as printed; `\decompnote` where they matter)

- p. 9 (031104-8), Sec. 4.2: "Both a smaller (150 nm × 150 nm) and larger (5 mm× 5 mm) defect size were modeled" —
  printed with a roman "mm" (checked at 400 dpi; the µ of "16 µm²" on the same page is a different glyph), while the
  title boxes of Figs. 13 and 14 say "5 µm x 5 µm".
- Fig. 9 cited for the measured polarizers: p. 6 (031104-5), "despite the fact that the half pitch of the polarizer shown
  in Fig. 9(a) is smaller than the WGP in Fig. 9(b) there is a substantial difference in the optical performance";
  p. 8, "Since the Al thickness is nearly the same for both WGPs in Fig. 9"; p. 9, "consistent with the experimental
  observations from Fig. 9". Fig. 9 is the GSolver simulation (100/130 nm pitch, varied Al thickness); the two
  measured etched polarizers (50/65 nm half pitch) are Fig. 8, which is probably meant.
- Fig. 9 caption (p. 6): "ER as a function of wavelength and Al thickness for a 100-nm pitch WGP (a) and for a 130-nm
  pitch WGP (b)", but the figure has four panels: (a), (b) transmission, (c), (d) ER ("100nm pitch", "130nm pitch").
  The transmission axes are labelled "Transmission (%)" with tick labels 0 to 1.
- Fig. 11 caption (p. 7): "The clear defect causes a decrease in the ER by more than order of magnitude." The panel
  says ">5x decrease in extinction ratio" and the text (p. 9) "drops by more than a factor of 5"; in the digitized
  curves of Fig. 11(b) the ratio is 3.4 at 400 nm, at most about 8 (near 630 nm) and 5.0 at 800 nm (my measurement,
  `work/er_ratio.py`).
- p. 2 (031104-1): "There are additional requirements keeping for the adoption of R2R nanoimprint lithography."
  (a word seems missing); "In additional, a manufacturing infrastructure must be established".
- p. 3 (031104-2): "have been previously been reported" (doubled "been").
- Fig. 2 caption: "LithoFlex100" (text: "LithoFlex 100").
- References: ref. 17 "Proc. SPIE 797007 (2011)" has no volume (797007 is printed in the bold volume position);
  ref. 18 gives the same article number, "Proc. SPIE 7823, 797007 (2010)"; refs. 15 and 19 spell the author
  "Selenidis" and "Selinidis"; ref. 23 opens its title with ” instead of “.

## Observations from the digitized data (mine, not statements of the paper)

Fig. 5: TM at 700 nm is 79.3 ± 0.3 % (text: ">80%"; panel: "Max TR = 80%"); the black curve through the ER data is
about 3700 at 700 nm, the noisy ER(L-B) trace spans about 3300–5000 there (text: ">4500"). Fig. 6: TM at 400 nm is
64 % (text: "better than 60%"), the moving average 3240 at 700 nm (panel: "ER > 3000 @ 700nm"). Fig. 8(b) is below
10,000 only between 400 and about 455 nm (abstract: "Extinction ratios of better than 10,000").

## Known problems

- Digitized values are good to about one source pixel (see above); dashed TE lines (Figs. 11, 12) and dashed Fig. 9
  series have values only where a dash is; the noisy ER traces of Figs. 5 and 6 are given as ranges, not values.
- Fig. 5/6 moving-average lines have short gaps where other ink hides them (e.g. under the red arrow in Fig. 5).
- Fig. 13/14 `marker_value` is biased where markers of two series overlap (transmission panels); use `value`.
- Fig. 4 inset labels and the SEM data bars of Fig. 4 are partly blurred or cut; read as far as possible.
- The cover page (PDF p. 1) is kept as text in `main.tex` (title and authors appear twice).
- 25 image reads were used; none returned the request-limit placeholder.
