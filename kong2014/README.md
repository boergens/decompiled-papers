# kong2014: decompiled

Kong, Jian-Qiang, and George Y-H Kong (both Greenville, NC, US). "Microtome." United States Patent
US 8,635,934 B2, date of patent Jan. 28, 2014. Appl. No. 13/320,215; PCT filed Aug. 25, 2010, PCT/US2010/046665,
§ 371 date Nov. 11, 2011; PCT Pub. No. WO2011/034698 (Mar. 24, 2011); prior publication US 2012/0055300 A1
(Mar. 8, 2012); provisional application No. 61/242,404 filed Sep. 15, 2009. Int. Cl. B26D 7/06 (2006.01).
13 claims, 3 drawing sheets. Primary Examiner Sean Michalski; attorney Richard C. Litman. (All as printed on the
front page, PDF p. 1. The USPTO prints the document as "Kong et al."; the task message's "Kong J.-Q." names the
first of the two inventors.)

**DOI:** none (a patent). Identifier: US8635934B2.

**Licence:** a public USPTO document with no copyright notice. The PDF prints none anywhere; the Google Patents
page likewise. `source/SOURCE.txt` records the same.

**Source files** (`source/`, obtained by the coordinator, see `SOURCE.txt`):
- `US8635934B2.pdf`: the USPTO full-text image PDF (image-ppubs.uspto.gov), 466,805 bytes, 9 pages. Each page is
  one bilevel CCITT image of 2560 × 3300 px placed at one PDF point per pixel (page box 2560 × 3300 pt), i.e. a
  300 ppi scan of the 8.5 × 11 in sheet. `pdffonts` lists no fonts: **no text layer at all**. This is the granted
  patent as issued (kind code B2), the authoritative version.
- `US8635934B2.google_patents.txt`: the text of patents.google.com/patent/US8635934B2/en (HTML stripped), used
  only as a second opinion for doubtful words; it holds the abstract, description and claims (not the front page's
  bibliographic layout, the references list in its printed form, or the drawings).
- `US8635934B2.reference.txt`: the span of that Google text from the abstract to the end of the claims, as plain
  text (3,789 words, 3,695 check tokens), written by `python3 -I -B work/diff_google.py reference` for
  `check_text.py --reference-text` (added at the coordinator's request; not listed in `SOURCE.txt`, which is the
  coordinator's file).

## What is included

`main.tex` (compiled: `main.pdf`, 12 pages) holds, in the PDF's order:
- p. 1, the front page: the (12)/(10)/(45) header, INID items (54), (76), (\*), (21), (22), (86), § 371, (87),
  (65), the Related U.S. Application Data (60), (51), (52), (58), (56) with the first 14 U.S. patent documents,
  the foreign patent documents, examiner and attorney, (57) the abstract, "13 Claims, 3 Drawing Sheets"; the
  front page's reduced reproduction of FIG. 1 is noted (a `\decompnote`), not cropped separately.
- p. 2: References Cited, continued (16 U.S. patent documents) and "\* cited by examiner".
- pp. 3–5: the three drawing sheets as figure blocks (`figures/fig1.png`–`fig3.png`, each with its printed
  label "FIG. n" and an `\alttext` naming every reference numeral).
- pp. 6–9: the description (title, cross-reference, background, disclosure, brief description of the drawings,
  best modes) and the 13 claims (`hangpars`, numbered as printed), ending with the printed "\* \* \* \* \*".

The References Cited are set as `tabular`s (dot leaders left out) and also as `tables/references_cited.csv`
(30 U.S. + 4 foreign rows: page, list, number, kind code or country, cited-by-examiner star, date, name, class).

**Left out** (all said in the top `\decompnote`): the running headers ("US 8,635,934 B2 / Page 2" on p. 2;
"U.S. Patent / Jan. 28, 2014 / Sheet n of 3 / US 8,635,934 B2" on pp. 3–5; "US 8,635,934 B2" on pp. 6–9), the
gutter line numbers 5, 10, 15, … of the description columns, the dot leaders after names and after "USPC", and
the bar code line "US008635934B2" at the top of the front page. The printed column numbers 1–8 are kept as short
`\decompnote`s at each column start ("Column 3 begins."; for a column starting mid-sentence, "Column 4 begins
inside this paragraph, at `wheel 76 at bearing 74`"), so the text can be cited by column as patents are.

## Method (tool-first) and corrections

The text was placed by `work/build_main.py` from the Datalab API OCR (accurate mode, 2026-10-20,
`work/datalab/US8635934B2.md`, "{n}----" page delimiters, headings, two markdown tables for the front matter, the
drawing sheets as images plus their OCR'd numerals). The script reassembles the front page in print reading order
(the OCR had interleaved the left column's INID items and the right column's reference entries in one table),
builds the reference tabulars and the CSV, places the figure blocks, converts the description and claims, and
applies the corrections below. The decompiler proofread the generated text against the page images (every column
of pp. 1–2 and 6–9 at the scan's native resolution) and against the Google Patents text, and typed none of the
patent's text.

`CORRECTIONS` in the script (each applied once to the markdown):

| PDF page | fix | reason |
|---|---|---|
| 1 | `(*)` → `( * )` | printed with spaces inside the parentheses |
| 9 | three gutter line numbers (5, 10, 15) removed from the ends of claim-13 lines | OCR'd into the text |
| 7 | "…attached to an eccentric" + "wheel 76 at bearing 74." joined | one sentence across the column 3/4 break, split by the OCR |

Systematic rules in the script (verified against the page images): (1) the reference numerals of the Best Modes
section are printed bold; the OCR marked them bold in columns 1–2 and 5 but not in columns 3–4, so every numeral
10–86 there is set bold; (2) figure numbers after "FIG."/"FIGS." are printed bold throughout ("FIG. **1**",
"FIGS. **1-3**", "FIGS. **1** and **2**"); (3) claim numbers are printed "**1**." (bold numeral, plain period),
the OCR wrote "**1.**". The OCR's `$\mu\text{m}$` and `$\alpha$` become μm and α; the pages' first words carry
`\pdfpage{n}`, inline where p. 8 starts mid-sentence ("…resulting in a sliced | sample.").

The OCR'd drawing-sheet numerals are not used (they are in the `\alttext`, read from the images); for the record,
the OCR missed label 80 on sheet 1 and label 44 on sheet 2, and listed none for sheet 3.

## Checks

- `lualatex -interaction=nonstopmode -halt-on-error main.tex`, twice: no errors (six overfull boxes of ≤ 3.8 pt).
- `python3 -I ../../tools/check_text.py main.tex source/US8635934B2.pdf` (version 2026-10-20a, no options): the
  PDF has no text layer, so the tool reports **PDF tokens 0, tex tokens 4241, coverage 0.0 %**, and one EXTRA run
  of all 4241 tokens (`work/check_text.json`). Those numbers say nothing about the transcript; the two
  comparisons below replace them.
- `python3 -I /home/admin/ephemeral/oct_17_papers/tools/check_text.py main.tex source/US8635934B2.pdf
  --reference-text source/US8635934B2.reference.txt` (version 2026-10-20b, run from this folder; output in
  `work/check_text_reference.txt` and `.json`):
  `reference text: source/US8635934B2.reference.txt (3695 tokens) used instead of the PDF text layer`;
  `PDF tokens 3695, tex tokens 4241`; **`coverage 100.0% of PDF tokens found in tex; 87.2% of tex tokens found in
  PDF`**; coverage without repeated text (0 tokens) 100.0 %; coverage of the running text (0 in-figure tokens)
  100.0 %; REPEATED 0; **MISSING runs ≥ 6: 0**; **EXTRA runs ≥ 6: 3 (541 tokens)**, all expected: (1) 125 tokens,
  the front page's header and INID items (12), (10), (45), (54), (76), (\*), (21), (22), (86), § 371; (2) 232
  tokens, (60)'s date, (51), (52), (58), (56) and the front page's 14 reference entries; (3) 184 tokens, "13 Claims,
  3 Drawing Sheets" and p. 2's 16 reference entries. None of these is in the reference span (the Google dump has
  no printed front page or references list); the three figure labels "FIG. n" are too short to form a run. The
  reference text is the Google Patents transcription, not the scan, so this is a check of agreement between two
  independent readings of the same print, not against the image itself.
- **Word-level comparison of `main.tex` against the Google Patents text** (`work/diff_google.py tex`, lower-case
  letter/digit tokens, the decompiler macros removed; the abstract, description and claims, which is all the
  Google dump has in printed form): Google 3,695 tokens, tex 3,697 tokens, **3,695 matching, 0 Google tokens
  unmatched, 2 tex tokens unmatched**, both explained: "abstract" (the printed heading "(57) ABSTRACT", which the
  Google dump gives as a page label outside its text) and "microtome" (the title printed at the head of column 1,
  which the Google description omits). Output in `work/diff_google_tex.txt`.
- The same comparison of the raw OCR against the Google text (`diff_google.py datalab`,
  `work/diff_google_datalab.txt`): 6 differing runs, all tokenisation (μm and α written as TeX by the OCR, the
  column numbers "1" and "2", the title), i.e. the OCR had no word errors in the body before proofreading.
- The front page, p. 2 and the drawing-sheet numerals are not in the Google text in printed form: proofread by eye
  against the page images (every reference entry, date and class checked; all 34 agree with the OCR).
- Read-through of `main.tex` against the page images for what tokens can't see: bold reference numerals, the
  Greek α, the quotation marks, hyphens (`co-planar`, `I-beam`, `dovetail-like`, `x-y`, `z-axis`, `Hall-Effect`
  are printed hyphens and kept; all line-end hyphenations removed), the claim structure, the column breaks.

No plotted panels: no CSV/extraction/plot scripts and no `compare.py` checks (the three figures are line drawings).

## Figures

Crops by `work/make_figures.py` (uses `tools/crop.py`): the ink bounding box of each sheet below its running
header, isolated scan specks ignored, plus a 40 px margin, rendered at `crop.py` dpi 72, which for this PDF (one
point per scan pixel) is **1 px per scan pixel = the native 300 ppi of the printed sheet**; the SPEC's nominal
200 dpi would here upsample the bilevel scan 2.8× for no gain. The drawings are printed sideways (rotated 90°
counter-clockwise, "FIG. n" reading bottom to top at the sheet's right edge); the PNGs are rotated 90° clockwise so
that drawing and numerals read upright. The as-printed crops are kept in `work/fig*_asprinted.png`.

| file | sheet / PDF page | figure | type | size (px) | labels in the drawing | data |
|---|---|---|---|---|---|---|
| `figures/fig1.png` | Sheet 1 of 3, p. 3 | FIG. 1, diagrammatic top view of the microtome | line drawing | 1944 × 1708 | 33: 10, 20, 25, 26, 27, 40, 41, 42, 50, 52, 53, 55, 56 (×2), 57, 58, 60, 61, 62, 64 (×2), 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, α | none (not a plot) |
| `figures/fig2.png` | Sheet 2 of 3, p. 4 | FIG. 2, diagrammatic front view, specimen feed in section | line drawing | 1999 × 1759 | 26: 10, 12, 14, 16, 21, 22, 24, 26, 27, 28, 30, 40, 42, 44, 46, 48, 50, 51, 52, 53, 54, 55, 56, 57, 78, 80 | none |
| `figures/fig3.png` | Sheet 3 of 3, p. 5 | FIG. 3, diagrammatic side view of the sectioning station | line drawing | 1306 × 1489 | 8: 12, 42, 50, 52, 54, 56 (×2), 78 | none |
| (not cropped) | front page, p. 1 | reduced upright reproduction of FIG. 1 under "13 Claims, 3 Drawing Sheets", same 33 labels | line drawing | — | — | — |

## Errors and oddities in the patent

- Column 1, cross-reference: "U.S. Provisional Patent Application **Seri.** No. 61/242,404" (for "Ser."). Kept.
- Column 4: "the length of the blade 62 is greater than the diameter of the specimen to be **but**" (for "cut").
  Kept; the Google text prints the same.
- Reference numeral **51** is printed in FIG. 2 (a leader to a short horizontal line under the carriage, between
  the mounting plate and the linear bearing 48) but occurs nowhere in the description or claims.
- The first rail 44, linear bearing 48, first stand 46, tank 14, base 12 and bath 16 are labelled only in FIG. 2,
  the control unit 82 only in FIG. 1; in FIG. 1 the base and tank are drawn but unlabelled, in FIG. 2 the control
  unit, mounting plate, blade holder and blade are drawn but unlabelled (the `\alttext`s say so).
- Page 9 prints the column number "8" over an empty column (the text ends in column 7).
- "insure(s)" for "ensure(s)" (columns 1, 3, 4) and "Hall-Effect" are the patent's spellings, kept.
- The description says the second rail "may be an elongate circular rod" and FIG. 2 draws it as a circle in
  section; FIG. 3 shows it along its length as a flat bar.

## Known problems and notes

- The `\alttext` box of FIG. 1 (an `\fbox`, which cannot break across pages) is longer than the space left under
  the figure and moves whole to the next page of `main.pdf`; the `.tex` order is right.
- The column-start notes are `\decompnote`s, the only macro the SPEC allows for structure the paper prints but
  the layout does not reproduce; a dedicated marker for patent columns would be cleaner (see the report).
- `check_text.py` cannot check an image-only PDF (0 tokens); the audit's fresh OCR will see the same scan. The
  word-level comparison above is the substitute, with the Google text as the reference.
- `work/` holds the build, figure and comparison scripts, the Datalab OCR, the check outputs and the as-printed
  figure crops; the page renders used for proofreading were deleted (re-create with
  `pdftoppm -r 72 -png source/US8635934B2.pdf work/pages/p`).
