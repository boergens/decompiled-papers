# lavollee2023: decompiled

Jérémy Lavollée and Konrad Swanepoel. "A tight bound for the number of edges of matchstick graphs."
arXiv:2209.09800v2 [math.CO], 15 Jun 2023 (v1: 20 September 2022). 2020 MSC Primary 52C10, Secondary 05C10.

**Versions.** The PDF here is the **arXiv preprint, v2** (the stamp "arXiv:2209.09800v2 [math.CO] 15 Jun 2023" is
printed in the left margin of p. 1; the PDF prints no journal, DOI or dates). The paper was later published as
*Discrete & Computational Geometry* **72** (2024), 1530–1544, DOI
[10.1007/s00454-023-00530-z](https://doi.org/10.1007/s00454-023-00530-z) (online 18 August 2023); those details come
from `source/SOURCE.txt` (Crossref), the journal version was not read and may differ.

**Licence:** the arXiv listing says CC BY 4.0; the PDF itself prints no licence line.

## Source files (`source/`)

| file | what it is |
|---|---|
| `lavollee2023.pdf` | arXiv v2, 12 pages, born-digital (LaTeX via dvips + Ghostscript 9.22; embedded Computer Modern Type 1C fonts, `pdffonts`). The text layer is the typesetter's, not OCR. TeX rules (radical overlines, fraction bars, the footnote rule) are 1×1 stencil images scaled to size; the three figures are vector paths. |
| `lavollee2023.txt` | `pdftotext -layout` dump, used as a second opinion. |
| `SOURCE.txt` | fetch note (arXiv, 2026-10-11). |

The paper names no data set, supplement, code or video, so nothing was missing.

## Method (tool first)

`main.tex` was produced by `work/build_main.py` from the PDF's own text layer (PyMuPDF `rawdict`: every character
with its font, size and baseline), with the hand-written parts in `work/build_tables.py`:

- rows are clustered by baseline; 7-pt characters (sub/superscripts, inline-fraction parts, sum limits) and radical
  glyphs are attached to their row; CM accents set as separate glyphs are composed (É, å, ö, ó, è, ä);
- fonts drive the markup: CMTI → `\textit`, CMBX → `\textbf`, CMCSC → `\textsc`; characters of the math fonts
  (CMMI, CMSY, CMEX, MSBM, MSAM) are math, CMR digits and punctuation next to them join the formula, and maximal
  math runs become `$...$`; a radical glyph plus its overline rule becomes `\sqrt{...}` over the characters under
  the rule (nested radicals included), a short rule with 7-pt characters above and below becomes `\frac{}{}`, other
  7-pt characters become `^{}`/`_{}`; `)` takes the mode of its `(`;
- the 34 displayed formulas are detected by position (indented rows with math, or word-less rows) and their LaTeX
  was written by hand from the page images in `DISPLAYS` (the script prints the linearised text layer of each block
  as a hint and refuses to build if a block has no entry); the equation numbers (1)–(11) are the paper's own, as
  `\tag{}`; a proof that ends on a display gets the printed `\square` as `\tag*{}`;
- headers, page numbers and the figure drawings are dropped; captions, the two centred section heads, the run-in
  subsection heads (`\subsection*{1.1. Proof outline.}`), theorem/lemma/claim heads (`\textbf{Claim 1.}` + italic
  statement, as printed), `\textit{Proof.}` paragraphs, the abstract, the MSC/key-words footnotes and the references
  (`hangpars`, the printed `[n]` labels) are recognised from font and position; `\pdfpage{N}` sits at the first word
  of each page; line-end hyphens are removed except the five real ones (unit-, high-, edge-, Leibniz-, Springer-);
- the decompiler proofread the result against the page images and the compiled `main.pdf` page by page. One
  correction is in `CORRECTIONS` (the `]` of the half-open interval `(3n/4 − 3, 3n/4]` on p. 7, which the bracket
  rule had left outside the formula); everything else was fixed in the script's rules.

Left out: the running headers ("JÉRÉMY LAVOLLÉE AND KONRAD SWANEPOEL" / "A TIGHT BOUND FOR THE NUMBER OF EDGES OF
MATCHSTICK GRAPHS") and page numbers. Kept once: the arXiv stamp (p. 1, vertical in the margin), with a note.
The MSC/key-words footnotes of p. 1 are placed at the end of the page-1 text, with a note.

## Figures

| figure | page | type | data | provenance |
|---|---|---|---|---|
| Fig. 1 | 5 | vector line drawing: matchstick graph G (16 vertices) split into G1 (red hexagon with centre) and G2 (blue) sharing the edge pq of a quadrilateral | description only | – |
| Fig. 2 | 8 | vector schematic: filled hexagon G1 (red), region G′ (blue), the six vertices of K (green) on a highlighted path | description only | – |
| Fig. 3 | 9 | vector line drawing: convex polygon P′ with its circumscribed hexagon H, labelled p_i, q_i, r_i, Q_i | description only | – |

Panels per provenance tier: none plotted; 3 drawings with description only. No figure has axes or plotted data, so
there are no CSVs: the vertex coordinates of a matchstick-graph drawing are not data the paper gives (no scale, no
coordinates printed), only the combinatorial structure, which the `\alttext` describes (vertex and edge counts were
read from the vector paths: Fig. 1 has 16 vertex dots, 12 red and 17 blue edges plus the shared edge, all of one
length). `figures/fig1.png`–`fig3.png` are 200-dpi renders of the drawing boxes (crop.py; box = union of the vector
paths and the labels, +5 pt), captions excluded.

## Checks

- `lualatex` ×2: compiles without errors (13 pages).
- `python3 -I ../../tools/check_text.py main.tex source/lavollee2023.pdf` (no options; the tool reported version
  2026-10-20a): PDF tokens 6402, tex tokens 6146; **coverage 96.5 % raw; 97.9 % without text repeated on ≥ 3 pages
  (88 tokens); 98.8 % of the running text** (also without 60 unmatched tokens printed inside the figures: the labels
  G1, G2, p, q, K, p_i, q_i, r_i, Q_i, P′, H, which are in the `\alttext`). MISSING runs ≥ 6: **0**. EXTRA runs ≥ 6:
  **1** (6 tokens), explained below.
- REPEATED: the running header (5 + 1 pages) and two one-letter "texts": `p` (7 pages) and `x` (4 pages). These are
  the CMEX10 glyphs of the big radicals (codes p/q) and display-size sums (code X); CMEX10 has no ToUnicode map, so
  the checker reads the glyph codes as letters. They are math-font tokens, not text.
- EXTRA (with `--min-run 2`: 9 runs, 29 tokens, all in one place): the seven-line display on p. 10 (the bound on
  b(H)). The .tex has `\sum_{i=1}^{6}` for each of its eleven sums, which tokenises as "i 1 6" in reading order; the
  PDF's text layer puts the limits "6" and "i = 1" on separate lines above and below the operators, so the same
  tokens come in another order. The formula was checked symbol by symbol against the page image.
- MISSING (with `--min-run 2`: 11 runs, 32 tokens): p. 7 `l 2`, `l p l`, `l r l`, `l 3 l` are ℓ (the PDF's "ℓ"
  normalises to the letter l, the .tex has `\ell`, a command the checker drops); p. 10 `i 6`, `i 1 r`, `i 1 q` are
  the sum limits of the same display as above; p. 11 `bl asj o` is "Blåsjö" (the PDF sets the accents as separate
  glyphs, so the checker splits the name; the .tex has the composed name); p. 12 `12 j er emy` and `and konrad
  swanepoel` are the header of the last page (the page number glues to it, so the ≥ 3-page rule misses this copy).
- Read-through against the page images and the compiled PDF: every displayed formula (34 blocks), the inline
  radicals (including the nested √(π√3/6) on p. 1), the inline fractions (½, 1/11, √3/4, π√3/6, ¾n, 1/16, 2/√3,
  √3/2, 1/6, 13/24, 3/7), sub/superscripts (n_1, b_*, G′, φ(n)², b², 60°, 120°, 180°, p_{i+1}), ≠, ∅, ∪, ∈, ℤ, ℝ,
  ⌊ ⌋, |K|, the cdots/ldots, the en dashes in citations and page ranges, the equation numbers (1)–(11) and the
  position of every `\square`.

## Errors and oddities in the paper

- **Figure 3 labels vs. the text's definition.** The text (p. 9) defines Q_i as the path of P′ between q_i and
  p_{i+1} and uses the triangle p_{i+1} q_i r_i, so Q_i sits at the corner r_i; in the figure the arc at r_6
  (between q_6 and p_7 = p_1) is labelled Q_1, the one at r_1 is Q_2, and so on: the figure's Q labels are shifted by
  one against the definition. Noted in the `\alttext`; it does not affect the proof.
- p. 5, end of the proof of Claim 5: "contradicting assumption 1" (elsewhere the assumption is cited as "(1)"). As
  printed.
- Reference [3] gives "arXiv preprint arXiv:1401.1799. (1982)": an arXiv number of January 2014 with the year 1982.
  As printed. (Background knowledge, not in the .tex: arXiv identifiers encode year and month; the 1982 manuscript
  was posted in 2014.)
- Punctuation oddities in the references, kept as printed: "Pach. J." [4], "Fejes Tóth G," without a period [7],
  "Vogel. S." [23], [24]; "(4; n)-regular" with a semicolon in [23] against "(4, n)-regular" in [24]; "Problem 664A"
  with the digits upright inside the italic title [10].

## Problems and suggestions for the spec and tools

- **Math papers and "tool first".** The text layer cannot give displayed formulas (sqrt extents, fraction bars and
  sum limits are geometry, not text). What worked here: the script detects the display blocks and prints their
  linearised text as a hint, and the decompiler supplies the LaTeX in a table keyed by (page, index), so the build
  refuses to run if a block is unaccounted for. The brief could name this as the accepted method, and say that the
  inline math (fonts + rule images) can be automated as done in `work/build_main.py` (reusable for any
  Computer Modern / dvips PDF).
- **check_text.py and glyphs without a Unicode map.** CMEX10 (big radicals, sums, delimiters) has no ToUnicode
  map, so its glyph codes become letter tokens (`p`, `q`, `x`, `l`) that show up as REPEATED/MISSING. Suggested
  fix: drop tokens that come from fonts whose name starts with CMEX/CMSY/MSAM/MSBM (or from any CID-read glyph)
  on the PDF side; likewise compose CM accents (an accent glyph above a base letter) so "Blåsjö" is one token.
- The checker's version changed from 2026-10-17j (SPEC) to 2026-10-20a during this task; the numbers above are
  from 2026-10-20a.
- For folders under `incoming/` the SPEC's `../tools/` is `../../tools/` (as the task message said).
- `decomp.sty` has no `unicode-math`, so Greek and ℓ must stay as `\phi`, `\ell` in math; fine, but it is why the
  checker sees ℓ as missing.

## Time

About 2.5 hours of wall-clock over two sessions (the first was cut by a usage limit after the build script was
written; resumed from the files on disk): reading the brief, spec and all 12 pages; the build script and its
tables (34 displays, 3 descriptions); seven build/proofread rounds; compile, checks and this README.
