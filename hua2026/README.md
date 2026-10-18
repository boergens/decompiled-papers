# hua2026: decompiled

Yunfeng Hua, Linlin Li, Hua Han. "Preparing large biological specimens for high-throughput volume electron
microscopy." *Methods in Microscopy* (De Gruyter Brill) **2026**, aop (advance online publication), Review Article.
DOI [10.1515/mim-2026-0015](https://doi.org/10.1515/mim-2026-0015).
Received July 30, 2026; accepted August 31, 2026; published online September 24, 2026.

**Licence:** "Open Access. © 2026 the author(s), published by De Gruyter on behalf of Thoss Media. This work is
licensed under the Creative Commons Attribution 4.0 International License" (CC BY 4.0), footer of p. 1.

## Local and external

**In the local collection**
- Source files:
  - `papers/hua2026/10.1515_mim-2026-0015.pdf` – the review article, 10 pp., publisher's version of record
  - `papers/hua2026/10.1515_mim-2026-0015.txt`, `papers/hua2026/10.1515_mim-2026-0015.raw.txt` – earlier text extractions (not used)
  - `papers/hua2026/SOURCE.txt` – fetch note (copied from the papers/README.md manifest)
- Cited works decompiled here: templier2019 (`decompiled/templier2019/`), nguyen2016 (`decompiled/nguyen2016/`), white1979 (`decompiled/white1979/`), seligman1966 (`decompiled/seligman1966/`), hua2015 (`decompiled/hua2015/`), mikula2015 (`decompiled/mikula2015/`), stroh2022 (`decompiled/stroh2022/`), song2023 (`decompiled/song2023/`), karlupia2023 (`decompiled/karlupia2023/`), genoud2018 (`decompiled/genoud2018/`), wildenberg2025 (`decompiled/wildenberg2025/`), li2024 (`decompiled/li2024/`)

**External pull needed** (not on this machine)
- Supplementary Video 1 – https://doi.org/10.1515/mim-2026-0015 (the paper's pointer to its supplementary material, p. 10) – the article's only supplement, cited on p. 7; "Data availability: Not applicable."
- All other cited references: 58 entries in the reference list ([1]–[70]) without a [local: …] tag.

## Source files (`../../papers/hua2026/`)

| file | what it is |
|---|---|
| `10.1515_mim-2026-0015.pdf` | the article, 10 pp. **Publisher's version of record** (De Gruyter typesetting, running header "Methods in Microscopy 2026; aop" on p. 1, page headers "Y. Hua et al.: Development of sample preparation for volume electron microscopy", page numbers 2–10). PDF metadata: LaTeX + Acrobat Distiller, created 2026-09-24. |
| `10.1515_mim-2026-0015.txt`, `.raw.txt` | earlier text extractions of the PDF (looked at, not used). |

**Not available:** Supplementary Video 1, the article's only supplementary material ("This article contains
supplementary material (https://doi.org/10.1515/mim-2026-0015)", p. 10; cited in the text on p. 7, "(Supplementary
Video 1)"). It is not in `../../papers/hua2026/` and was not fetched. The paper names no data sets ("Data
availability: Not applicable."), so there is no tier-1 source data to miss.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal line, article type, authors, title, the
  corresponding-author footnote and the licence footer (both moved up from the foot of p. 1, noted in the file),
  DOI and dates, abstract, keywords, introduction, sections 1–4, Table 1, Figures 1–6 with captions,
  acknowledgments and the declarations block (research ethics, informed consent, author contributions, use of
  LLMs/AI, conflict of interest, research funding, data availability), the "References" heading (printed in the
  paper) and references [1]–[70], and the supplementary-material note. `\pdfpage{N}` marks the start of each PDF page.
- `figures/fig1.png` … `fig6.png`: each figure rendered from the PDF at 200 dpi (`tools/crop.py`, bbox of the
  embedded image + 3 pt), without caption.
- `tables/table1.csv`: Table 1, with caption and footnote in `#` lines.
- `work/`: scratch (page renders, native embedded images, zooms, the line dump `lines.txt`, the text-layer draft
  `draft.tex`/`blocks.json`, `refs.tex`, the template and the one-shot build scripts in `work/scripts/`,
  `check.json`, LaTeX aux files). May be deleted.

How main.tex was made: `work/scripts/dump_lines.py` dumps every text line with font flags; `draft.py` turns the
text layer into LaTeX paragraphs (italic → `\emph`, small raised/lowered spans → super/subscripts, line-end
hyphens joined unless the hyphenated form occurs mid-line elsewhere or is a real compound: Drift-EM, heavy-metal,
1 mm-diameter, reduced-osmium, large-volume, post-staining, lipid-selective, time-consuming, pH-dependent,
cryo-condition, large-scale, freeze-substitution); `refs.py` assembles the reference list; `build_main.py`
fills `work/main_template.tex`. main.tex was then edited by hand (title layout, table width, decompiler notes),
so the build scripts must not be re-run over it.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` from this folder; it
compiles without errors (run twice), with a few sub-1-pt overfull lines and one long reference line.

## Figures

All six figures are single **raster images** (embedded images, 974–1787 px wide); the only vector paths on the
figure pages are the 55 × 6 pt header rule, and the PDF text layer has no text inside any figure. **No figure has a
quantitative plot** (no axes with numbers or units): they are micrographs, photographs and schematics. So, as the
spec says for such papers, there are **no CSVs, extraction or plotting scripts**, and the overlay/`compare.py`
checks do not apply. Each figure has a panel-by-panel `\alttext`; the reaction list of Fig. 3 and the
protocol diagram of Fig. 2 are transcribed in full there.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | schematic (biopsy → en bloc staining → block-face imaging → regions 1–4) | – | – | |
| Fig. 1B | 4 SEM images (rOTO, regions 1–4) | – | – | scale bars 200 μm (B1), 2 μm (B2); precipitate ring arrowhead |
| Fig. 1C | 4 SEM images (ORTO, regions 1–4) | – | – | no scale bars in row C |
| Fig. 2 | schematic (protocol family tree, colour-coded) | – | – | transcribed in `\alttext` |
| Fig. 3 (top) | schematic (Os oxidation states across a bilayer, steps 1–4) | – | – | |
| Fig. 3 (bottom) | reaction list (1)–(4) | – | – | transcribed in `\alttext`; see errors |
| Fig. 4 | schematic (incubation outcomes) | – | – | key, counts of symbols in `\alttext` |
| Fig. 5A | photographs (16 tubes, 4 times × 4 buffer/temperature conditions) | – | – | colour per tube in `\alttext` (qualitative only) |
| Fig. 5B | 2 SEM images with block-face insets | – | – | scale bars 1 mm (insets), 1 μm |
| Fig. 6 (left) | SEM block-face image, HPF sample | – | – | scale bar 10 μm, white box |
| Fig. 6 (right) | SEM image, magnified box region | – | – | scale bar 1 μm, filled and open red arrowheads |

Fig. 3 and Fig. 6 parts carry no letters; "top/bottom", "left/right" are my names, used only here.

## Text check (`tools/check_text.py`, version of 2026-10-17 14:53)

| file | coverage of PDF tokens | coverage without text repeated on ≥ 3 pages | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|
| `main.tex` | 97.9 % | **99.7 %** (114 repeated tokens) | 99.5 % | 1 run (6 tokens) | 3 runs (29 tokens) |

Explanation of everything unmatched (`--min-run 1`, `work/check_minrun1.txt`):

- **Repeated (left out on purpose):** the running header "Y. Hua et al.: Development of sample preparation for
  volume electron microscopy" with page number, pp. 2–10. One leftover "electron microscopy" (2 tokens, p. 4)
  is the end of that header on p. 4.
- **Table 1 (all remaining MISSING and EXTRA runs, p. 3):** the PDF text layer of the rotated table gives every
  "OsO₄" in the table body as "OsO" (the subscript 4 is an empty glyph), so the PDF has "oso" where main.tex
  has "oso 4". The table was transcribed from the page image; the page clearly shows the subscript 4. No other
  differences.
- Not visible to the checker but handled: the reference list's text layer has an invisible comma before each
  final period ("2022,."); the page shows "2022." and main.tex follows the page. Ref. [69] has "1288− 98" in the
  text layer, "1288−98" on the page. Page ranges keep the text layer's U+2212 character (printed as a long dash).

Read-through against the page images (step 4) done for: all sub- and superscripts (OsO₄, OsO₂, Os^VIII/VI/IV,
Fe^II, Na₂SO₃/NaHSO₃, mm³, table footnote marks a–c), μm/μs, °C, ">3 h", en dashes in citation ranges and
numeric ranges, curly quotes, italics (en bloc, in situ, in-situ, et al., journal names), bold labels in the
back matter, the table cells, and the order of text around the figures and the table (each figure/table placed
after the paragraph it interrupts; Fig. 3, printed in the right column of p. 4, comes after the paragraph that
ends on p. 5, noted in the file).

## Errors and oddities in the paper (kept verbatim; the main ones flagged with `\decompnote`)

- **Fig. 3, reaction (4)** as printed, 2[Os^VI O₂(OH)₄]²⁻ ⟶ [Os^VIII O₄(OH)₂]²⁻ + Os^IV O₂(solid) + 2OH⁻, balances Os
  and charge but not O and H (left 12 O, 8 H; right 10 O, 4 H): 2 H₂O are missing on the right. Reactions
  (1)–(3) balance.
- **p. 5:** "ferrocyanide rapidly depletes available OsO₄ to generate water-soluble Os^IV species"; everywhere else
  (text, Fig. 3 and its caption) the water-soluble intermediate is Os^VI and Os^IV is the insoluble OsO₂. Probably
  meant Os^VI.
- **Pallotto spelling:** reference [29] is "M. Pallotto"; the text and the Fig. 2 caption write "Palloto", Table 1
  and Fig. 2 "Pulloto".
- **Fig. 2 caption:** "extracellular space (ESC, blue)"; the text, the figure and the caption's own later sentence use "ECS".
- **Fig. 4 caption:** "ferrocyanide (green squares)", but Fe^II is drawn as green hexagons in the figure and its key;
  "Right:" is printed twice; "Note that slow washout of water-soluble Os^VI species (grey arrows) in the presence of
  ferrocyanide." is not a complete sentence.
- **Table 1 footnote:** the last sentence, "Necessary for improved tissue integrity.", follows footnote c on its own
  line without a footnote mark, so which entry it qualifies is not stated.
- **Reference [51]** (Li et al., ChemBioChem, the `li2024` paper of this collection) is printed without a year (2024).
- **Fig. 6 caption:** "Axon viscosity (red solid arrow)" — "viscosity" is not something an SEM image shows; the
  intended word is unclear (kept as printed, not flagged in main.tex).
- p. 3: "Consequently, it is not surprisingly that" (grammar); p. 6: "same incubation duration at 4 °C substantially
  alleviate" (grammar). Kept.
- Funding: the Acknowledgments name grant 32171461 to H.H. only, the "Research funding" statement also 82171133 to Y.H.
- The running header title ("Development of sample preparation for volume electron microscopy") differs from the
  article title.

## Known problems

- Table 1 is set as one wide `tabular` scaled to the text width (`\resizebox`), so it prints small in main.pdf;
  `tables/table1.csv` is the readable version.
- Figure descriptions of the micrographs are qualitative; the paper gives no measurements in the figures beyond
  scale bars and the imaging parameters in the Fig. 6 caption.
