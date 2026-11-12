# eberle2015: decompiled

A.L. Eberle, S. Mikula, R. Schalek, J.W. Lichtman, M.L. Knothe Tate and D. Zeidler. "High-resolution, high-throughput
imaging with a multibeam scanning electron microscope." *Journal of Microscopy* **259**(2), 114–120 (2015).
Received 12 September 2014; accepted 23 December 2014. DOI [10.1111/jmi.12224](https://doi.org/10.1111/jmi.12224).
Affiliations: Carl Zeiss Microscopy GmbH, Oberkochen (Eberle, Zeidler); Max-Planck-Institute for Medical Research,
Heidelberg (Mikula); Department of Molecular and Cellular Biology, Harvard University (Schalek, Lichtman); Graduate
School of Biomedical Engineering, University of New South Wales (Knothe Tate).

The citation is taken from the PDF (p. 1: "Journal of Microscopy, Vol. 259, Issue 2 2015, pp. 114–120", "doi:
10.1111/jmi.12224", the received/accepted line, the title and author block; footers "…, 259, 114–120"). It agrees with
the task message and `source/SOURCE.txt`; the issue number 2 is printed only in the journal line.

**Licence:** p. 1 footer: "© 2015 The Authors / Journal of Microscopy © 2015 Royal Microscopical Society" and "This is
an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution
and reproduction in any medium, provided the original work is properly cited." (CC BY; the version is not stated).
A footnote on p. 1 says: "The copyright line for this article was changed on June 17, 2015 after original online
publication." Openly licensed; published on the public mirror with Kevin's OK of 2026-11-12 (`SOURCE.txt`).

**Why it is in the library:** another session (deep-UV imaging throughput comparison) cites it for the multibeam SEM's
61 beams (p. 2: "The multibeam SEM currently uses 61 electron beams in a single column") and its total detector
bandwidth (p. 2: "The total possible detector bandwidth of the multibeam SEM is the single detector bandwidth times the
number of beams, in this case 1.22 GPixel/s"). Note for that use: 1.22 GPixel/s is the *possible* detector bandwidth;
the images shown were acquired at 0.45 (Figs. 2, 3), 0.18 (Fig. 4) and 0.72 GPixel/s (Fig. 5) (captions), and the
Conclusions say "approaching 1 GHz" (p. 6). See also the dose arithmetic below.

## Source files (`source/`)

| file | what it is |
|---|---|
| `jmi0259-0114.pdf` | the article, 7 pp. (journal pp. 114–120). **Publisher's version of record** (Wiley typesetting) as deposited in PubMed Central (PMC4670696). Born-digital: Type 1C fonts without Unicode maps (PhotinaMT in MacRoman/WinAnsi, MTSY, CMSY10, RMTMI), all decoded correctly by PyMuPDF and poppler through their encodings. One embedded raster per figure page (pp. 2–6: Fig. 1 a 1516×1184 grey PNG-type image, Figs. 2–5 grey JPEGs of 1425–1486 px, all 300 dpi in print). The journal masthead on p. 1 ("Journal of Microscopy", white on a blue band) is vector outlines. No vector drawings on the figure pages. |
| `SOURCE.txt` | provenance note (download 2026-11-12 from PMC, browser slot 1) |

The paper names no data set, source data, supplementary material or video, and the PMC page lists no supplementary
material (`SOURCE.txt`), so nothing tier-1 is missing.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal line, DOI, dates, title, authors, affiliations,
  the two p. 1 footnotes (copyright-line change; correspondence), the p. 1 footer (© lines and the CC BY statement,
  given once), Key words, Summary, Introduction, the sections "Throughput limitations of single-beam SEMs",
  "Circumventing the single-beam limitations with a multibeam approach", "Application examples of the multibeam SEM",
  "Operating a multibeam SEM", Conclusions, Acknowledgements, References (29 entries, author–year, as printed);
  Figs. 1–5 with verbatim captions and descriptions. Written by `work/build_main.py` (do not edit by hand). Compile:
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice): no errors; three overfull lines of 8–14 pt in
  the front matter (the journal/DOI line, an affiliation, the e-mail address).
- `figures/fig1.png` … `fig5.png`: each figure rendered from the PDF at 200 dpi (`tools/crop.py`, image bbox + 2 pt).
- `figures/figs2to5_scalebars.csv` + `figs2to5_scalebars_extract.py`: my measurement of the scale bars against the
  mosaic geometry (below). Not data of the paper; no plotting script, as there is nothing plotted.
- `tables/text_values.csv`: the key numbers of the running text and captions (21 rows: quantity, value, unit, printed
  wording, where, page), compiled by `work/text_values.py` from `main.tex`. The paper has no tables.
- `work/*.py` (kept with the entry, each with a docstring): `build_main.py` (the build), `pdfchars.py` (glyphs with
  font, size, position), `figure_texts.py` (descriptions and figure notes), `text_values.py`, `dose_check.py`
  (arithmetic checks), proofreading and probe scripts `zoom.py`, `page_pairs.py`, `inset_sheets.py`, `dump_spans.py`,
  `gap_probe.py`, `image_info.py`, `scalebars.py`, `mosaic_geometry.py`, `nospace_lines.py`. Everything else in
  `work/` (page renders,
  sheets, logs, `pdftotext.txt`) is scratch.

## How the text was made

`work/pdfchars.py` reads every glyph (PyMuPDF rawdict) with font, size and position. `work/build_main.py` clusters
baselines into lines, splits them at the column gutter, and turns each line into LaTeX:

- **Missing word spaces.** In many justified lines the text layer has no space characters at all (word spacing is set
  by positioning), e.g. p. 1 "imagingspeedbyclosetotwoordersofmagnitudeanddemon-". Letters in this PDF touch exactly
  (gap 0.00 × size) and word gaps are ≥ 0.115 × size, so a space is inserted where the gap exceeds 0.08 × size; the
  letter-spaced author line (gaps 0.117 between capitals) keeps only its explicit spaces. A space glyph of a maths font
  narrower than 0.2 × size is a kern, not a word space ("EBERLE*").
- **Special characters**, checked against 300-dpi crops (`work/zoom.py special`): the diaeresis is a separate glyph
  over its letter and is composed with it (Helmstädter, Müller, Körber, Sätzler); µ is an italic µ from the maths font
  RMTMI (written as µ; "12µm" on p. 3 and "1µm" in the Fig. 3 caption have no space in print, the other µm values
  have one); × from MTSY; † ‡ from CMSY10; the superscript asterisks from MTSY; © is printed as a small "C" inside an
  enclosing circle (MTSY U+20DD) and written as ©; the subscript of SiO₂ (Fig. 5 caption) is a smaller, lowered glyph.
  "SE1", "SE2" (p. 4) and "S3EM" (reference Horstmann) are printed with full-size digits on the baseline, and kept so.
- Italic and semibold runs become `\textit`/`\textbf` (et al., journal names, volume numbers, x and y on p. 3).
- Line-end hyphens: 53 removed, 4 kept as real compounds that are also printed with their hyphen mid-line or are
  hyphenated by form: signal-to-noise (p. 2), single-beam (Fig. 4 caption), hexagonal-like (p. 6), high-throughput
  (p. 6). All decisions are printed by the build. Page ranges broken after the en dash ("618–/623") are joined.
- Running headers and the footers of pp. 2–7 are left out; the p. 1 footer is given once (a `\decompnote` says so).
- No corrections of the text layer were needed (`CORR` in the build is empty).

Read-through (step 4): every line of `main.tex` against the text-layer listing (`build_main.py --raw`), the page images
of pp. 1–7 (paragraph indents, headings, italics, the order around the figures), and the special characters above at
300 dpi. Paragraph breaks follow the printed indents; p. 4 starts without an indent, so "The sample preparation …"
continues the paragraph from p. 3.

## Text check (`tools/check_text.py` 2026-11-07a)

`python3 -I ../tools/check_text.py main.tex source/jmi0259-0114.pdf` (no options):

| measure | value |
|---|---|
| coverage of PDF tokens | 97.2 % |
| without text repeated on ≥ 3 pages (66 tokens) | **98.8 %** |
| also without unmatched in-figure text (0 tokens; the figures are rasters without text layer) | 98.8 % |
| tex tokens found in PDF | 95.5 % |
| MISSING runs ≥ 6 | 0 |
| EXTRA runs ≥ 6 | 15 (140 tokens) |
| `--words-only` | 98.7 % / 99.0 % / 99.0 %; 94.8 % of tex words in PDF; 0 MISSING, 15 EXTRA |

All 15 EXTRA runs are lines without space characters (above): the tool reads such a line as one glued token
("imagingspeedbyclosetotwoordersofmagnitudeanddemon"), which matches nothing in the .tex. `work/nospace_lines.py`
lists about 20 such lines on pp. 1, 2 and 4–7 (body text and references); the 15 runs are those long enough to leave
≥ 6 unmatched tex tokens in a row. The repeated text is the running headers and footers.

Second opinion with poppler's text, which inserts spaces from glyph positions:
`pdftotext source/jmi0259-0114.pdf work/pdftotext.txt` and
`python3 -I ../tools/check_text.py main.tex source/jmi0259-0114.pdf --reference-text work/pdftotext.txt`:

| measure | value |
|---|---|
| coverage of reference tokens | 95.7 % |
| without text repeated on ≥ 3 pages (120 tokens) | 98.6 % |
| tex tokens found in reference | **99.5 %** |
| MISSING runs ≥ 6 | 3 (47 tokens): the letter-spaced author line, which pdftotext splits into single letters ("e b e r l e s m i k u l a …") |
| EXTRA runs ≥ 6 | 1 (10 tokens): the p. 1 © lines, where the reference has the letter "C" of the © sign between the words |
| `--words-only` | 97.9 % / 99.8 % / 99.8 %; 99.5 % of tex words in reference; 0 MISSING, 2 EXTRA (the same two places) |

At `--min-run 1` the reference run adds only: "singlebeam" (pdftotext joins the real hyphen of "single-/beam", Fig. 4
caption), "lead-"/"ing" (pdftotext does not join a hyphen across the column break on p. 6) and the page numbers in
the headers.

## Figures

All five figures are raster images with no text layer and no vector drawings; none has a plotted panel, so there are
**no data CSVs and no re-plots**, and the overlay/compare checks do not apply. Each figure has a description
(`\alttext`); Figs. 2–5 also carry two decompiler notes (scale bars; electrons per pixel), placed after Fig. 2.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 | schematic of the multibeam SEM: Multi-Beam Source, Beam Splitter, Objective, Specimen, Projector, Multi-Detector; key Illumination (solid) / Detection (dotted) | – | – | description only; all labels transcribed |
| Fig. 2 main | SEM mosaic, mouse cortex block-face, "10 µm" bar | – | – | description only |
| Fig. 2 inset (lower right) | single-beam subimage, unlabelled bar (5 µm per caption) | – | – | description only |
| Fig. 3 main | SEM mosaic, mouse cortex ultrathin section, "10 µm" bar | – | – | description only |
| Fig. 3 inset lower right | single-beam subimage (5 µm bar per caption) | – | – | description only |
| Fig. 3 inset upper right | detail of that subimage (1 µm bar per caption) | – | – | description only |
| Fig. 4 main | SEM mosaic, femoral neck block-face, "10 µm" bar | – | – | description only |
| Fig. 4 inset (lower right) | single-beam subimage (5 µm per caption) | – | – | description only |
| Fig. 5 main | SEM mosaic, test chip, "10 µm" bar | – | – | description only; block numbers 1–9, 13–15 and 19 around the centre read at native resolution, the rest not transcribed |
| Fig. 5 inset (lower right) | single-beam subimage of block "1" | – | – | description only; its labels "12", "200", "1:2", "1", "584" transcribed |

Panels per tier: tier 1: 0; tier 2: 0; tier 3: 0; tier 4: 0; description only: 10 (Fig. 1; Figs. 2–5 main images and
their 5 insets).

### My measurements and checks (not statements of the paper)

**Scale bars of Figs. 2–5** (`figures/figs2to5_scalebars_extract.py`, method in its docstring; results in
`figures/figs2to5_scalebars.csv`). In the native images, each main "10 µm" bar is 103–107 px long. Three other lengths
agree with each other but not with that bar:
- the tile pitch of the mosaic: the stepped outline moves by half a tile (78–82 px) per tile row, so a tile is
  156–165 px wide; the rows are 134–141 px apart, a ratio of 0.85–0.87 (the text's "aspect ratio of about 0.866",
  p. 3). The text gives the distance between beams as 12 µm (p. 3);
- the insets' own scale bars (207–217 px for 5 µm) make the insets 11.6–12.6 µm wide, as the captions say
  ("12 µm × 10 µm"); the inset magnification is 2.8–3.1 relative to the marked rectangle;
- the whole field is then 108–110 µm wide (text: "a hexagonal area approximately 100 µm wide", p. 3; Fig. 1 caption:
  "100-µm wide").
On these scales the "10 µm" bars measure 7.0–8.0 µm; taken at face value they would make the field about 138 µm wide
and the 12 µm subimages about 16 µm wide. So either the main scale bars are too short (by about a quarter) or their
label is wrong; the insets' bars are consistent. Uncertainty about ±2 px per length.

**Electrons per pixel vs. acquisition speed** (`work/dose_check.py`): with the captions' total current *I* and
acquisition speed *R*, *I*/(*eR*) = 361 electrons per pixel for Figs. 2 and 3 (printed: 270), 1387 for Fig. 4
(printed: 420) and 347 for Fig. 5 (printed: 210). The printed values correspond to pixel rates of 0.60 GPixel/s
(Figs. 2–4) and 1.19 GPixel/s (Fig. 5), i.e. 61 beams at about 10 MHz and 20 MHz; the printed acquisition speeds are
lower, so they apparently include time without pixel exposure. The paper does not define them.

**Other arithmetic, consistent:** 61 × 20 MHz = 1.22 GPixel/s (the p. 1 example's 20 MHz and the p. 2 bandwidth); a
1 mm cube at 4 nm voxels is 1.56 × 10¹⁶ voxels, 15.6 PB at one byte per voxel ("almost 16 petabytes") and 24.8 years at
20 MHz ("almost 25 years"); 61 subimages of 12 µm × 10 µm at 3.8 nm are 507 MPixel ("up to 500 MPixel").

## Errors in the paper (kept as printed)

- **Scale bars, Figs. 2–5** (pp. 3–6): the "10 µm" bars disagree with the 12 µm beam distance, the "12 µm × 10 µm"
  insets with their 5 µm bars, and the "approximately 100 µm" field by a factor of about 1.3 (my measurement, above;
  `\decompnote` after Fig. 2).
- **Reference Cazaux (p. 6):** "Cazaux, J. (2004) About the role of the various types of secondary electrons (SE; SE;
  SE) on the performance of LVSEM." The three "SE" carry no indices (checked at 300 dpi). From my background knowledge,
  not checked here: the cited article's title reads "(SE1; SE2; SE3)". `\decompnote` at the reference.
- **Name spelling:** the text cites "Helmstädter *et al*., 2013" (p. 1); the reference list has "Helmstaedter, M.,
  Briggman, K.L., …" (p. 7). `\decompnote` at the reference.
- Typography only: "(Bright *et al*. 1998)" without the comma used elsewhere (p. 2); "12µm" (p. 3) and "1µm" (Fig. 3
  caption) without the space of the other µm values; the references Moore *et al*. (2014) and Platzgummer *et al*.
  (2013) have no "&" before the last author; Griffin (2011) "detectors-a further variable" with a hyphen for a dash.
- Cited "in preparation" and not in the reference list (normal for such citations): "Mikula & Denk, 2014, in
  preparation" (p. 3), "Knothe Tate, 2015, in preparation" (p. 4). Every other citation in the text has its entry,
  and every entry is cited.

## Known problems

- Figure descriptions give no absolute sizes from the main scale bars (see above).
- Fig. 5: only the block numbers around the centre were read (13, 4, 3, 9 / 14, 5, 1, 2, 8 / 15, 6, 7, 19); the
  others are small at the printed resolution and were not transcribed.
- The © sign is written as © although the PDF builds it from a letter "C" and a circle, so check_text sees a stray
  "c" token in the footers (part of the repeated text, and of the one EXTRA run in the reference-text check).
- 18 image reads were used; none returned the request-limit placeholder.
