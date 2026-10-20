# abdelaal2015: decompiled

Hadia M Abdelaal, Hyeon O Kim, Reece Wagstaff, Ryoko Sawahata, Peter J Southern & Pamela J Skinner.
"Comparison of Vibratome and Compresstome sectioning of fresh primate lymphoid and genital tissues for *in situ*
MHC-tetramer and immunofluorescence staining." *Biological Procedures Online* **17**:2 (2015).
DOI [10.1186/s12575-014-0012-4](https://doi.org/10.1186/s12575-014-0012-4). Article type "METHODOLOGY", "Open Access".
Received 25 September 2014; accepted 29 November 2014; published online 07 January 2015 (the last date is an image
stamped into the PDF, not text). All of this is printed in the PDF and agrees with `source/SOURCE.txt`.

**Licence:** CC BY 4.0, printed in the footer of PDF p. 2: "© 2015 Abdelaal et al.; licensee BioMed Central. This is an
Open Access article distributed under the terms of the Creative Commons Attribution License
(http://creativecommons.org/licenses/by/4.0), which permits unrestricted use, distribution, and reproduction in any
medium, provided the original work is properly credited. The Creative Commons Public Domain Dedication waiver
(http://creativecommons.org/publicdomain/zero/1.0/) applies to the data made available in this article, unless
otherwise stated." (kept verbatim in `main.tex`).

## Source files (`source/`)

| file | what it is |
|---|---|
| `abdelaal2015.pdf` | **Publisher's version of record** (BioMed Central / Springer typesetting), 8 PDF pages: p. 1 a cover sheet (journal logo, a cover image, title, "Abdelaal et al.", citation line), pp. 2–8 the article's pages 1–7. Born-digital: embedded Type 1C fonts (`pdffonts`), typesetter's text layer; the four figure images and the "Published online" stamp are the only raster images (`pdfimages -list`). |
| `SOURCE.txt` | fetch note (link.springer.com PDF, 2026-10-20, browser slot 0). |

No supplement, data set, source-data file or video is named by the paper ("unpublished data" in Results is not a
file), so nothing was needed and nothing is missing.

## Method (tool-first)

`work/build_main.py` writes `main.tex` and `tables/table1.csv` from the Datalab API conversion of the PDF
(`work/datalab/abdelaal2015.md`, "accurate" mode, run by the coordinator). The PDF's own text layer (PyMuPDF) was the
second opinion: a word-by-word diff of the markdown against the text layer (37 hunks, all accounted for: the
in-figure labels Datalab read off the images, the licence footer it dropped, the ordering of the Fig. 3 caption,
line-end hyphens, and the real differences below), and the span fonts for every italic, bold and superscript. The
result was then proofread against the page images. Two blocks Datalab left out, the licence footer of p. 2 and the
citation/DOI lines of pp. 1–2, are read from the text layer by the script (`pdf_text`), not typed. The script is
re-runnable from any directory (`python3 -I -B work/build_main.py`; a re-run from the scratchpad reproduced
`main.tex` byte for byte).

**Corrections to the Datalab markdown** (the script's `CORRECTIONS`, 8 entries, 11 replacements), each a thing
Datalab silently "corrected" or mis-set:

| PDF p. | Datalab | as printed | evidence |
|---|---|---|---|
| 4 | `( $0.64 \text{ cm}^2$ Vs. $0.25 \text{ cm}^2$ )` (math, spaces inside the parenthesis) | `(0.64 cm² Vs. 0.25 cm²)` | text layer, page image |
| 5 | *Macaca mulatta* (italic) | Macaca mulatta (upright) | regular font in the text layer, page image |
| 5 | *Mamu-A1\*001:01* | *Mamu- A1\*001:01* (space after the hyphen) | text layer `Mamu- A1*001:01`, visible gap on the page |
| 6 | Quick Set™ | Quick SetTM (the letters TM, as on p. 5) | text layer `SetTM` |
| 7 | **Published online: 07 January 2015** (bold) | plain | the stamp image is a plain serif face |
| 3, 5 | **Figure 1**, **Figure 2** bold, title sentence plain | the whole caption title bold | label font in the text layer (Fig. 3 was right) |
| 4, 5, 6, 6 | *Mamu-A1/Gag* (4×) | *Mamu-A1*/Gag | `/Gag` is in the regular font |

**Rules applied by code** (not single entries): the reference list's journal names, which Datalab set in italics, are
upright in print (only "in situ" is italic there, as the text layer flags it); the caption panel ranges "(A-B)",
"(C-D)", "(E-F)" are bold (label font). Confirmed as printed and left alone: all 23 en dashes, the 7 tildes, ×, °,
®, ö, the curly quotes in "Authors' contributions" and "Corresponding Author", "intra- rectally", "anti- CD20",
"saline- containing", "(181– 189)", "Compresstome™,", "Loctite® 404®", "Buffalo Grobe", "Confocal mages",
"Neruomol Med.".

## What is in `main.tex`

Every word of the article in reading order, pages marked with `\pdfpage{N}` (PDF page numbers; the cover sheet is
p. 1). Cover sheet: the cover image (`figures/cover.png`, described), title, "Abdelaal et al.", citation line and
DOI. Article: the citation/DOI header (once), the METHODOLOGY / Open Access banner, title, authors with their
affiliation superscripts, then in a quote block the correspondence line, the affiliation-1 footnote, the "Full list
of author information" line and the licence statement (printed at the foot of p. 2; a `\decompnote` says so), the
Abstract (Background, Results, Conclusions, Keywords), Background, Results and discussion, Conclusions, Table 1,
Materials and methods (four subsections), Competing interests, Authors' contributions, Acknowledgments, Author
details, the dates, the 25 references (`hangpars`, numbers as text) and Figures 1–3 with their full captions.

Left out: the running headers ("Abdelaal et al. Biological Procedures Online (2015) 17:2", "Page N of 7"), the
journal logo with its wordmark "Biological Procedures Online" (pp. 1–2; check_text counts the wordmark as text
inside a figure), the BioMed Central logos, and the "Submit your next manuscript to BioMed Central ..." box on the
last page (publisher advertisement).

Placement: Fig. 1 (foot of p. 3) is placed after the paragraph that spans p. 3/4; Fig. 3 (top of p. 6) after the
paragraph that spans p. 5/6 (the `\pdfpage{6}` marker sits inline in that paragraph, so the figure comes after
it); Fig. 2 (top of p. 5) and Table 1 (foot of p. 4) are in place. Seven column/page breaks inside sentences are
joined (`JOINS`), with the page marker inline. Each has a `\decompnote`.

Table 1 is a `tabular` and `tables/table1.csv` (caption in `#` lines; the first column, which the table prints
without a header, is called `parameter`; "cm²" with the Unicode superscript).

## Figures

| figure | panel | type | data |
|---|---|---|---|
| cover (p. 1) | single | two-part confocal immunofluorescence composite, tissue not named, no caption | description only |
| Fig. 1 | A | photograph: Compresstome VF-300 on the bench | description only |
| Fig. 1 | B | photograph: Compresstome buffer tank with frozen PBS-H cubes | description only |
| Fig. 1 | C | photograph: Vibratome 3000 | description only |
| Fig. 1 | D | photograph: Vibratome bath with ice | description only |
| Fig. 2 | A, B | confocal immunofluorescence, lymph node, Compresstome / Vibratome, with montage insets | description only |
| Fig. 2 | C, D | confocal immunofluorescence, spleen, Compresstome / Vibratome | description only |
| Fig. 3 | A, B | confocal immunofluorescence, vagina, Compresstome / Vibratome | description only |
| Fig. 3 | C, D | confocal immunofluorescence, cervix | description only |
| Fig. 3 | E, F | confocal immunofluorescence, uterus | description only |

**No plotted panel in the paper**: 14 photograph/micrograph panels plus the cover image, all description only; no
CSV, extraction or plotting script, and the data checks (overlay, compare.py) do not apply. Panels per provenance
tier: source data 0, vector 0, digitized 0, read by eye 0. `vector_dump.py` on the Fig. 2 region: 0 paths, 0 text
spans, 1 raster image (the figures are single JPEG/flate images at 150 ppi, 710 px wide, with the panel letters,
row/column labels, insets, arrows and scale bars inside the raster; they are in the `\alttext` blocks).

`figures/fig1.png`, `fig2.png`, `fig3.png`, `cover.png`: 200 dpi renders (crop.py) of the embedded-image boxes
plus a 2 pt margin, without the captions. Descriptions were written from 2× zooms of the embedded images
(`work/z_*.png`).

## Checks

- `lualatex` ×2: compiles without errors (13 pages).
- `python3 -I ../../tools/check_text.py main.tex source/abdelaal2015.pdf` (no options; version 2026-10-20a):
  PDF tokens 4485, tex tokens 4358; **coverage 98.2 % raw; 98.8 % without text repeated on ≥ 3 pages (24 tokens);
  100.0 % of the running text** (55 unmatched tokens inside figures). MISSING runs ≥ 6: **0**; EXTRA runs ≥ 6: **0**.
  With `--min-run 2`: MISSING 0; EXTRA 1 run (5 tokens): "published online 07 january 2015", which is the stamped
  image on p. 7 (not in the text layer) and is kept as the paper's publication date.
- REPEATED: "Page # of #" (6 pages). The 55 in-figure tokens are the advertisement box on p. 8 (inside a drawn box
  with the BioMed Central logo), the journal wordmark next to the logo on pp. 1–2, and nothing from the figures
  themselves (their lettering is raster). No `--exclude` or `--figure-box` option was needed.
- Read-through against the page images: the author superscripts (1,3 / 1 / 1 / 1 / 2 / 1*), the affiliation
  superscripts, cm², "200–500", "20 to 50 um", "40C", "0-2C", "0C", "4C", "4°C" (the only degree sign), "(181–
  189)", "1:4.5", "1:10,000", "0.3% triton x-100 0.3%", "36–42 um", "800x800 pixels 200X", "20 X objective",
  "×" in "0.5-cm-wide × 0.5-cm-tall", the italics of every "in situ", "Mamu-" alleles and "et al." (only in the
  headers), and the bold of the abstract labels, caption titles and panel ranges.

## Errors and oddities in the paper (transcribed as printed)

- "up to about 60% larger sized sections (0.64 cm² Vs. 0.25 cm²)" (p. 4, and Table 1): 0.64/0.25 is 2.56, i.e. 156 %
  larger by area; 60 % larger describes the side length (0.8 cm vs 0.5 cm pieces in the Methods). Decompiler's
  arithmetic from the printed numbers only.
- "Confocal mages" (both captions, for "images"); "Buffalo Grobe, IL" (p. 7; Leica's Buffalo Grove, decompiler's
  background knowledge); "Neruomol Med." (ref. 19); "larger sized tissues sections" (Conclusions); "kidney [13,14]
  larynx" (missing comma); "euthanized as we have described [1,3-5,24])." (stray parenthesis); "The Compresstome™,
  VF-300" (stray comma); "Viviani et al., used"; "college of veterinary medicine" lower case; "Departments of
  Microbiology, MMC 196" (plural for one department).
- Temperatures without a degree sign ("40C", "0-2C", "4C", "0C") except one "4°C"; "um"/"ug" for μm/μg; "200um",
  "100mg/ml" without spaces; "0.3% triton x-100 0.3%" (doubled concentration); "Quick SetTM" with TM as letters.
- "intra- rectally or intra- vaginally": the second hyphen falls at a line end; whether a space follows it cannot be
  seen on the page. Transcribed with the space (as Datalab read it, matching "intra- rectally"); `\decompnote`.
- Authors' contributions: two authors have the initials PS (Peter J Southern, Pamela J Skinner); the text says "PS,
  'Corresponding Author'" and then "PS:", so only the asterisk on the author line (Skinner) tells them apart.
- References: ref. 6 has no pages; ref. 12 ends "Daems." and ref. 17 "Hahn." without initials; ref. 13 "LD VDk.";
  ref. 21 "2013;4:138–8"; ref. 25 "1–17. 4.9."; ref. 8 journal "Am J Reprod Immunol (1989)."
- Background knowledge, not in the .tex: the Compresstome and Vibratome model names are as printed; nothing else
  was added.

## Problems and suggestions for the spec and tools

- **Datalab "accurate" mode silently normalises**: it italicised all 25 journal names and a species name that are
  upright in print, closed a printed space ("Mamu- A1"), turned the letters "TM" into ™, bolded a stamped date line,
  set a parenthesis as a formula, OCR'd the in-figure labels (A, B, LN, Spleen, ...) into the text flow after each
  image, and dropped the licence footer and the page headers. The word-by-word diff against the text layer plus a
  span-font dump for italics/bold caught all of it in one pass; worth making that diff a standard step (or a tool)
  for Datalab-based builds of born-digital PDFs.
- `check_text.py` counts the last-page advertisement box and the journal wordmark next to the logo as "inside
  figures", so dropping them produces no MISSING run (fine), but including the wordmark produces an EXTRA run. A
  note in the tool's docstring that in-figure PDF text is removed from the PDF side (so matching tex text becomes
  EXTRA) would save a puzzled minute.
- A literal `\alttext` written inside a `\decompnote` is executed as the macro (it swallowed the next letter and
  printed a stray "Description" box on the cover page in a first build); the SPEC could say to write macro names
  in notes as `\texttt{\textbackslash alttext}`.
- The SPEC's "`../tools/`" is "`../../tools/`" for folders under `incoming/` (noted in the task message).
- The handed-over `decomp.sty` and layout worked without changes.

## Time

About 13 minutes wall-clock (23:15–23:28 UTC by the machine clock) for reading the brief, spec, example and the eight
pages, the text-layer diff, the build script with its descriptions, compile, check, and this README.
