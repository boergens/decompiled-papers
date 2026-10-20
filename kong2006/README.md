# kong2006: decompiled

Kong, George Y., and Jian-Qiang Kong. "Sliding blade microtome." United States Patent US 7,146,895 B2, filed
Oct. 21, 2004 (Appl. No. 10/969,350), date of patent Dec. 12, 2006. Prior publication US 2006/0086221 A1,
Apr. 27, 2006. Int. Cl. B26D 1/10 (2006.01); U.S. Cl. 83/705; 83/409.2; 83/703. 11 claims, 4 drawing sheets.
Primary Examiner Charles Goodman; Attorney, Agent, or Firm Richard C. Litman. No assignee is printed: the front
page lists the two inventors under code (76) (inventors who are also the applicants), George Y. Kong, Santa
Clara, CA, and Jian-Qiang Kong, Greenville, NC. (All from the front page of the PDF.)

The task message and `source/SOURCE.txt` cite the patent as "Kong G. Y." / "Kong, George Y." alone; the PDF
prints "Kong et al." with two inventors, and the PDF wins.

**Number:** US 7,146,895 B2 (no DOI; USPTO document). **Licence:** a public USPTO document with no copyright
notice: the patent prints no copyright notice anywhere (checked on all 8 page images).

**Version:** the USPTO full-text image of the granted patent (the version of record).

## Source files (`source/`)

| file | what it is |
|---|---|
| `US7146895B2.pdf` | 8 pages, 457 kB, "USPTO PDF Builder", PDF 1.2. `pdfimages -list`: one 2560 × 3300 px 1-bit CCITT image per page and nothing else; `pdffonts`: no fonts at all, so **there is no text layer**. The PDF declares each page as 2560 × 3300 pt with the scan placed at 1 px per pt, i.e. the scan is a **300-ppi letter-size image** (8.53 × 11 in) stretched to a 35.6 × 45.8 in page box. Page 1 front page (bibliographic data, abstract, representative drawing), pages 2–5 drawing sheets 1–4 (FIGS. 1–4, printed sideways), pages 6–8 the description and claims in two columns (columns 1–6) with line numbers in the gutter. |
| `US7146895B2.google_patents.txt` | the text of the same patent from patents.google.com (HTML stripped), used only as a second opinion; the page images are authoritative. |
| `US7146895B2.reference.txt` | the Abstract/Description/Claims span of the Google Patents text, one paragraph per line (3370 tokens), for `check_text.py --reference-text`; see Text checks. |
| `SOURCE.txt` | fetch note (2026-10-20, oct-20-compresstome session). |

No supplement, data set or other file is named by the patent; nothing is missing.

## Method: tool-first transcript

The patent's text in `main.tex` was **not typed by the decompiler**. It was placed by a script from an OCR of
the scan and then proofread against the page images:

1. **OCR:** Datalab API, "accurate" mode, run by the coordinator on 2026-10-20 on the PDF:
   `work/datalab/US7146895B2.md` (markdown with `{n}----` page delimiters, headings, the citation lists as
   markdown tables, the five drawings as image files with their reference numerals listed as text;
   `US7146895B2.meta.json`: 8 pages, no failed pages, parse quality score 4.75, 6.0 cents).
2. **Build:** `work/build_main.py` reads the markdown and writes `main.tex`: `{n}` delimiters → `\pdfpage{n+1}`
   (inline where a page or column starts mid-sentence); the front page's blocks are labelled by their INID
   codes and emitted in reading order (the OCR had put the right column's continuation of the U.S. patent
   documents list before field (21)); the three markdown tables → one tabular of 17 U.S. documents and one of
   2 foreign documents; the abstract; "11 Claims, 4 Drawing Sheets"; the five image links → `figures/front.png`,
   `fig1.png` … `fig4.png` with the decompiler's `\alttext` (the sheets are rotated upright with `\rotatebox`);
   the column-number headings (`# 1`, `###### 5`, …) dropped; `## X` → `\section*` (the title) or
   `\subsection*`, `### X` → `\subsubsection*`; reference numerals 100–299 and the digits after "FIG."/"FIGS."
   made bold from the Brief Description on, as printed (the OCR's bold was partial: present on PDF pages 6 and
   8, absent on page 7, never on the FIG. numbers); "We claim:" and the 11 claims in `hangpars`, the claim
   elements (the OCR's `- ` items) as indented paragraphs, the nested "motorized means" items indented further;
   the closing `* * * * *` centred. The script asserts that each `\alttext` names every numeral the OCR listed
   for its drawing. `work/make_figures.py` makes the five PNGs with `tools/crop.py`.
3. **Proofreading** against the page images: the 2560 × 3300 px scans (`work/pages/p-N.png`, `pdftoppm -r 72`,
   i.e. the native pixels), each text column in three native-resolution pieces (`work/cols/p{6,7,8}c{1,2}k{1,2,3}.png`),
   the two front-page columns (`work/cols/p1{L,R}.png`), and upright zooms of the drawings (`work/views/`), word
   by word, with attention to the numbers, the bold numerals, the citation tables, the claim structure and the
   two printed oddities ("angel", "rushed", both confirmed). In parallel, `work/compare_google.py` compared the
   placed text word by word with the Google Patents text (below). **Result: no word error in the Datalab text.**

The `CORRECTIONS` table of the script is empty: the proofreading changed no word. What the script fixes or
supplies, all recorded there (`JOINS`, `BLOCKS`, the bold rule):

| PDF page | what | fix |
|---|---|---|
| 1 | `US007146895B2` printed under the barcode: dropped by the OCR | supplied as a constant (`BLOCKS["barcode"]`), with a `\decompnote` |
| 1 | front-page reading order: the right column's 10 citation rows emitted before field (21) | the U.S. patent documents list assembled as one 17-row table, fields in column order |
| 1 | `( \* ) Notice:` | `( * ) Notice:` (markdown escape) |
| 6 | paragraph broken at the column 1 → 2 break ("The blade can be" / "angled by rotating") | joined (`JOINS`) |
| 6 → 7 | "support arm 152 of the base" / "115. The mounting accessory" (page break) | joined, `\pdfpage{7}` inline |
| 7 | column 3 → 4 break ("the blade 168 and the" / "cutting plane 170.") | joined |
| 7 → 8 | "slidingly cut specimen 148" / "directly within the bath 120" (page break) | joined, `\pdfpage{8}` inline |
| 8 | claim 8 broken at the column 5 → 6 break ("abutting the" / "second end of the plunger") | joined |
| 6–8 | bold of the reference numerals inconsistent (none on page 7), FIG. numbers never bold | bold applied by rule, verified on the images |
| 2 | FIG. 1's numerals not listed by the OCR | read off the sheet for the `\alttext` check (20 numerals) |
| 5 | numeral 232 of FIG. 4 missing from the OCR's list | added for the check (15 numerals) |
| 3 | the OCR listed "3 3" for FIG. 2: the section-line marks 3—3, not numerals | described in the `\alttext`; excluded from the numeral check |

Left out as layout: the drawing-sheet headers ("U.S. Patent Dec. 12, 2006 Sheet n of 4 US 7,146,895 B2"), the
text-page header ("US 7,146,895 B2"), the column numbers 1–6 and the line numbers 5, 10, 15, … in the gutter.
Kept as printed text: the barcode line, every bibliographic field, "11 Claims, 4 Drawing Sheets", the "FIG. n"
labels of the sheets, "We claim:", the closing "* * * * *".

## What the folder contains

- `main.tex` / `main.pdf`: the whole patent in reading order (front page with the barcode line, all INID
  fields, the two citation tables, examiner and attorney lines, abstract, claims line, representative drawing;
  the four drawing sheets; the description with its headings; the 11 claims; the end marks). Compile with
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` in this folder (decomp.sty is here); compiles
  without errors (run twice), 13 pages. Five overfull boxes of 0.8 pt from the `\alttext` frames, cosmetic.
- `figures/front.png`, `fig1.png` … `fig4.png`: the drawings cropped with `tools/crop.py` at the ink bounding
  box plus 30 px (`work/make_figures.py`, rectangles in the script). **Resolution:** the scan is 300 ppi; the
  PNGs are at 200 dpi of the printed page, which for this PDF means `crop.py`'s dpi argument is **48**
  (48/72 = 2/3 of the scan's pixels, because the page box is 1 pt per scan pixel; "200" would give 2.8× the
  scan). The sheet PNGs are as printed, sideways (the figure is upright when the sheet is turned a quarter turn
  clockwise); `main.tex` rotates them with `\rotatebox[origin=c]{-90}`. `front.png` is upright as printed.
- `work/`: `datalab/` (the Datalab markdown, its image crops, meta), `build_main.py` (re-runnable: rebuilds
  `main.tex`), `make_figures.py` (re-runnable), `compare_google.py` (the word-level check, re-runnable),
  `check_text.json`, `pages/` (native renders), `cols/` and `views/` (proofreading crops), `out_sheet.png` and
  `figs_sheet.png` (contact sheets of the compiled output and the figures), lualatex logs. Scratch except the
  scripts.

No tables in the patent other than the citation lists on the front page (kept as tabulars in `main.tex`; not
data tables, so no `tables/` folder).

## Figures

No plotted panel: **0 panels in tiers 1–4, no CSV, no extraction or plotting script, no replot or compare.py
check**. All five images are patent line drawings, each described part by part (every printed reference
numeral with the part name from the description) in its `\alttext`.

| drawing | PDF page | type | PNG | numerals | notes |
|---|---|---|---|---|---|
| front page | 1 | representative drawing, identical to FIG. 3 (upright, smaller) | `figures/front.png` 974 × 691 px | 32 | described by reference to FIG. 3 |
| Sheet 1, FIG. 1 | 2 | environmental perspective view of the first embodiment 100 | `figures/fig1.png` 1167 × 1410 px (sideways) | 20 | 126 and 174 not numbered in this view |
| Sheet 2, FIG. 2 | 3 | front view of the first embodiment, with section line 3—3 | `figures/fig2.png` 1150 × 1568 px (sideways) | 18 (+ the two "3" marks) | broken-away patch shows the syringe end-on |
| Sheet 3, FIG. 3 | 4 | sectional side view of the first embodiment (section 3—3) | `figures/fig3.png` 1169 × 1479 px (sideways) | 32 | all parts of the first embodiment |
| Sheet 4, FIG. 4 | 5 | sectional side view (schematic) of the automated second embodiment 200 | `figures/fig4.png` 1174 × 1277 px (sideways) | 15 | 230 and 234 are printed but not named in the description |

## Text checks

**`tools/check_text.py` (2026-10-20a):** `python3 -I ../../tools/check_text.py main.tex source/US7146895B2.pdf`
reports **0 PDF tokens** (the PDF has no text layer), 3715 tex tokens, coverage 0.0 % and one EXTRA run of all
3715 tokens. This is the expected result for a text-less scan and says nothing about the transcript; the
`--figure-box`/`--exclude` options do not apply. No options were used.

**`check_text.py` 2026-10-20b with `--reference-text`:** `source/US7146895B2.reference.txt` is exactly the Google
Patents span that `work/compare_google.py` compares against (the Abstract, Description and Claims part of
`source/US7146895B2.google_patents.txt`, from its "Abstract" line to the end of claim 11, one paragraph per line,
79 lines, 3370 tokens; written by the decompiler from that file, not edited). `python3 -I ../../tools/check_text.py
main.tex source/US7146895B2.pdf --reference-text source/US7146895B2.reference.txt`: reference tokens 3370, tex
tokens 3715, **coverage 99.9 %** of the reference found in the tex (also 99.9 % without repeated text and for the
running text; 0 repeated tokens), 90.7 % of tex tokens found in the reference; MISSING ≥ 6: 0; at `--min-run 1`
the 2 missing tokens are Google's own headings `description` and `claims` (its `11` matches the claims line); EXTRA ≥ 6: 3 runs, 344 tokens, all
text the reference does not carry: the front-page bibliographic block (307 + 21 tokens: barcode line, INID fields,
citation tables, examiner lines) and the 16 layout tokens `11 claims 4 drawing sheets fig 1 fig 2 fig 3 fig 4
sliding blade microtome` (claims line, sheet labels, the title at the head of column 1). No options besides
`--reference-text`.

**Word-level comparison against the Google Patents text** (`work/compare_google.py`: `check_text.tex_text` and
`check_text.tokens` on `main.tex` from the abstract on, versus the Abstract/Description/Claims part of
`source/US7146895B2.google_patents.txt`, `difflib.SequenceMatcher`):

| tex tokens (abstract → end) | Google tokens (Abstract → Claims) | matching | differing runs |
|---|---|---|---|
| 3385 | 3370 | **3367 = 99.91 % of Google, 99.47 % of tex** | 2 |

Every difference explained:
- run 1: tex has `11 claims 4 drawing sheets fig 1 fig 2 fig 3 fig 4 sliding blade microtome` where Google has
  `description`: the claims line of the front page, the four "FIG. n" labels of the drawing sheets and the title
  printed at the head of column 1 (all printed text, all layout lines that Google does not carry), against
  Google's own section heading "Description" (not printed in the patent).
- run 2: tex has `we claim` (printed) where Google has `claims 11` (Google's heading "Claims (11)", not printed).
- OCR errors fixed: none (the Datalab text had no word error).
- Google's own errors in the running text: none found; Google's text and the OCR agree word for word, including
  the two printed oddities below. One discrepancy in Google's bibliographic data: its citation list gives
  6,651,538 (Tamura et al.) the kind code B2, the patent prints "6,651,538 B1"; the transcript follows the print.
- The front page's bibliographic fields are not in Google's running text; they were checked field by field on
  the page image (`work/cols/p1L.png`, `p1R.png`), and the 19 citations against Google's "Patent Citations (19)"
  list (same 17 U.S. and 2 foreign documents).

Read-through against the page images (SPEC step 4) done for: every INID field and date, the application and
publication numbers, the classification numbers (83/705; 83/409.2; 83/703; 83/915.5, 83/703, 409.2, 705, 563,
613, 638), every row of the two citation tables, every bold reference numeral in the description (all 100–299
numbers are printed bold; "FIG. 1"–"FIG. 4" and "FIGS. 1–3" have bold digits), the claim numbers (bold digit,
plain period) and the "claim 1"/"claim 3"/"claim 10" references (bold digit), the claim element structure
(which elements are indented, the nested "motorized means" pair), the en dash in "FIGS. 1–3", the hyphen in
"specimen-cutting" (printed at a line end in column 1 and mid-line in the Summary and the Detailed
Description), and the end marks.

## Errors and oddities in the patent (kept verbatim)

- Column 3, "The blade 168 forms an acute **angel** with the cutting plane 170." ("angle"; claim 6 has
  "acute angle"). Confirmed on the page image (`work/cols/p7c1k3.png`).
- Claim 9, last element: "whereby the specimen is **rushed** through the syringe shaft into the bath" (claim 1's
  parallel element reads "pushed"). Confirmed on the page image (`work/cols/p8c2k2.png`).
- Claim 2: "wherein the specimen **syringe** is defined in the peripheral wall of said bath" reads as if
  "syringe aperture" were meant (claim 1 defines the aperture in the bath). Printed so.
- FIG. 4 prints the reference numerals **230** and **234**, which the description never names (230 is a dashed
  outline at the cutting mechanism, 234 a collar at the right end of the plunger 236); the `\alttext` says so.
- Column 3: "and **consequentially** defines a compressed lip" (sic). Column 4: "lead screw 246, 256" (singular
  for two). The Summary says "the cutting assembly" once where the rest says "cutting mechanism". The Brief
  Description calls FIG. 4 "a mechanical control mechanism", the Detailed Description "an automated microtome".
- Headings: the Background's subheadings "1. Field of the Invention" and "2. Description of the Related Art" are
  printed as plain indented lines, the four main headings in capitals; `main.tex` uses `\subsection*` and
  `\subsubsection*` for them (looks differ, text identical).

## Not available

Nothing: the patent names no data set, supplement or other file.

## Known problems

- `check_text.py` has no PDF text layer to check against; it is run with `--reference-text` (the Google span) instead.
- The sheet PNGs are sideways, on purpose (as printed); the `.tex` rotates them.
- The front-page `\alttext` describes the drawing by reference to FIG. 3's description rather than repeating it.

## Tool notes (for the coordinator)

- `check_text.py` on a PDF without a text layer prints "PDF tokens 0" and one EXTRA run containing the whole
  transcript. It would help if it said plainly "no text layer: nothing to check" and, better, accepted a
  reference text file (`--reference-text file.txt`: a Google Patents text, a tesseract run) to compare against
  instead; `work/compare_google.py` here does that ad hoc with the tool's own tokenizer.
- `crop.py`'s dpi argument assumes the page box is at the physical page size. This USPTO PDF declares the page
  box in scan pixels (2560 × 3300 pt), so "200 dpi" must be passed as 48; `crop.py` could print the page size
  and the rendered pixel size, or accept a zoom factor.
- Datalab on this scan: no word errors in 3,385 running-text tokens, headings and tables right, but it dropped
  the barcode line, emitted the front page's right column out of order, listed the drawings' numerals for four
  of the five drawings (not FIG. 1) and missed 232 on FIG. 4, and its bold markup was inconsistent across pages.
  A tool-first patent build should therefore always re-derive the bold by rule and re-read the numerals from
  the sheets.
- The Read tool shows the 2560 × 3300 px scan at 1552 × 2000 px, too small to proofread 9-pt patent text; native
  column crops (`work/cols/`) were needed.

## Time

About 55 minutes: reading the brief, spec and example (5), page inspection and drawing study (15), build script
and descriptions (15), proofreading all columns and the front page (10), checks and README (10).
