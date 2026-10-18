# xie2019: decompiled

Wenkun Xie, Fengzhou Fang. "Cutting-based single atomic layer removal mechanism of monocrystalline copper: edge
radius effect." *Nanoscale Research Letters* **2019**, 14:370 (NANO EXPRESS). DOI
[10.1186/s11671-019-3195-4](https://doi.org/10.1186/s11671-019-3195-4) (printed in the PDF's page-1 header and in its
metadata). Received 17 July 2019, accepted 28 October 2019, published online 06 December 2019.

**Licence:** © The Author(s) 2019, open access under the Creative Commons Attribution 4.0 International License (CC BY 4.0),
as stated on p. 1.

**DOI check:** the DOI is printed in the PDF itself. There is no verify-sources receipt for it
(`~/.local/share/verify-sources/receipts/` and `web/checks/receipts/` have none), and the paper is not cited in
`web/whitepaper.md`.

**Collection key note:** the key `xie2019` is also the natural key for this paper's own ref. 20 (Xie & Fang 2019,
*Nanomanuf Metrol*, "... atomic sizing effect"), a companion paper. The PDF here is the **edge radius effect** paper
in *Nanoscale Res Lett*, which matches `SOURCE.txt`.

## Source files (`source/`)

| file | what it is |
|---|---|
| `source/xie2019.pdf` | the article, 18 pp., copied from `papers/xie2019/xie2019.pdf`. **Publisher version of record** (SpringerOpen typesetting, running header "Xie and Fang *Nanoscale Research Letters* (2019) 14:370 … Page n of 18", PDF metadata "Nanoscale Research Letters, 2019, doi:10.1186/s11671-019-3195-4"), served by the University of Strathclyde repository. Fetch note in `papers/xie2019/SOURCE.txt`: "xie2019.pdf: https://strathprints.strath.ac.uk/81380/1/Xie_Fang_NRL2019_...pdf (doi:10.1186/s11671-019-3195-4) curl 2026-10-13 by simulation agent; downloaded for context, no claims used". |

`papers/xie2019/xie2019.txt` (an earlier text extraction) was not used.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, correspondence and
  affiliations (moved from the foot of p. 1, noted), abstract, keywords, licence (moved from the foot of p. 1, noted),
  all sections, Eqs. (1)–(2), Tables 1–3, Figs. 1–19 with captions, descriptions and data links, abbreviations,
  authors' contributions, funding, data availability, competing interests, dates (incl. "Published online", which is
  an image in the PDF), 22 references, publisher's note.
- `figures/`: every figure rendered with `crop.py` at 200 dpi from the embedded-image bbox + 2 pt (`fig1.png` …
  `fig19.png`; the embedded images are 300 ppi JPEGs); data CSVs, extraction scripts, plot scripts and replots (below).
- `tables/table1.csv`, `table2.csv`, `table3.csv`: the three tables (caption and layout notes in `#` lines), written by
  `work/scripts/make_tables.py` with `csv.writer`.
- `tools/`: helper modules imported by the figure scripts: `digitize_common.py` (copied unchanged from the osmium
  tools), `excel_markers.py` (gridlines and round-marker centres of the Excel charts; written for this paper),
  `colourkey_map.py` (colour-key conversion of the atom renderings; written for this paper).
- `decomp.sty`: copied from the osmium tools; `lualatex -interaction=nonstopmode -halt-on-error main.tex` compiles from
  this folder with no TEXINPUTS (run twice). It compiles without errors; 37 over/underfull box warnings (long lines).
- `work/`: scratch (page renders, native embedded images, overlays `fig12_overlay.png`/`fig13_overlay.png`, colour-map
  checks `*_map_check.png`, side-by-side comparisons `cmp_*.png`, glyph crops, `annot.txt` font-annotated text layer,
  scripts `crop_all.sh`, `make_tables.py`, `annot.py`). May be deleted.

Re-run the data (from any directory): `python3 -I -B figures/<fig>_extract.py`, then `python3 -I -B figures/<fig>.py`.
All paths in the scripts are relative to the script; they read `source/xie2019.pdf` directly with PyMuPDF.

## Figures

No figure has vector plot data: every figure is one embedded 300 ppi JPEG, and `vector_dump.py` finds only the
figure-frame strokes on pp. 11–12 (Figs. 12, 13). The paper names no data set or supplement ("all the data used for
the analysis are included in this article"), so there is no tier-1 source.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 | MD model rendering (workpiece layers, tool) | – | – | description |
| Fig. 2 | schematic + MD snapshot (cutting depth definition) | – | – | description |
| Fig. 3a–f | MD snapshots, side view, layer colouring (no key) | – | – | description |
| Fig. 4a–f | MD snapshots, side view, layer colouring | – | – | description |
| Fig. 5a–f | MD snapshots, side view, layer colouring | – | – | description |
| Fig. 6a–f | top-view atom renderings coloured by z height, colour key −200 … −232 Å | `figures/fig6a.csv.gz` … `fig6f.csv.gz` | 3 (colour key) | grid at native resolution; authors' ellipses blanked in c, d |
| Fig. 7a–f | top views, layer colouring (no key) | – | – | description |
| Fig. 8a–f | side views coloured by CSP, key 3 … 10 | `figures/fig8a.csv.gz` … `fig8f.csv.gz` | 3 (colour key) | |
| Fig. 9a–e | cross-section views coloured by CSP, key 3 … 10 | `figures/fig9a.csv.gz` … `fig9e.csv.gz` | 3 (colour key) | |
| Fig. 10a–e | close-up MD views with displacement vectors, no key | – | – | description |
| Fig. 11a–d | perspective renderings coloured by x displacement, key 2.2 … −10.2 Å | `figures/fig11a.csv.gz` … `fig11d.csv.gz` | 3 (colour key) | semi-quantitative, see below |
| Fig. 12a | line chart, Ft and Fn vs tool edge radius | `figures/fig12a.csv` | 3 digitized | 2 × 8 markers |
| Fig. 12b | line chart, Ft vs tool edge radius | `figures/fig12b.csv` | 3 digitized | 8 markers |
| Fig. 13 | line chart, Ft and Fn vs cutting depth | `figures/fig13.csv` | 3 digitized | 2 × 19 markers |
| Figs. 14–19 | schematics (atom-circle drawings, labels) | – | – | descriptions; all labels transcribed |

Counts: **24 data panels, all tier 3**: 3 plotted chart panels (12a, 12b, 13) and 21 colour-key panels (6a–f, 8a–f,
9a–e, 11a–d); 0 tier 1, 0 tier 2, 0 tier 4. The other 37 image panels (Figs. 1, 2, 3a–f, 4a–f, 5a–f, 7a–f, 10a–e, 14–19) have descriptions only.
Every image panel has an `\alttext`.

**Line charts (Figs. 12, 13):** Excel charts with light-grey gridlines. Axes calibrated on all gridlines (13 + 10 for
Fig. 13; 11 + 9 and 11 + 7 for Fig. 12a/b), max residuals ≤ 0.29 nN and ≤ 0.017 nm/0.0023 Å. Each marker centre is a
least-squares circle fit to its rim (fallback: centroid of the colour-mask core); fitted radii 8.4–9.1 px, centres
within 0.3 px of the core centroids. Legend markers excluded by position. Checks done and looked at: overlays of the
centres on the native image (`work/fig12_overlay.png`, `work/fig13_overlay.png`: every dot sits in its marker) and
side-by-side replots (`work/cmp_fig12.png`, `work/cmp_fig13.png`: series, ranges, ticks match). Panel a and b of
Fig. 12 plot the same Ft: they agree within 0.4 nN. The smoothed connecting lines are Excel drawing, not data, so only
markers are given.

**Colour-key panels (Figs. 6, 8, 9, 11):** these are OVITO-style renderings of shaded spheres, so pixel colours are the
key colours darkened or paled across each sphere; RGB matching fails (the first try left Fig. 6's green patches empty).
`tools/colourkey_map.py` matches **hue** instead: the jet key's hue falls monotonically from blue (240°) to red (0°),
and each pixel gets the median value of the key rows within 2° of its hue. Limits, all stated in each CSV header:
the dark ends of the key differ from their neighbours only in brightness, so the end runs (e.g. CSP 9.1–10 and
3.0–3.9; z −204.4 to −200.2 Å and −231.8 to −227.7 Å) collapse to their middle value and are counted in the header;
white background, grey tool atoms, black labels and unsaturated sphere edges are empty cells; grids are image pixels
(no length scale; Fig. 11 is a perspective view). Checks looked at: `work/fig*_map_check.png` (source image beside the
mapped values redrawn in key colours) and `work/cmp_fig6/8/9/11.png` (original beside the replot).

- *Sanity checks (my own reasoning, not from the paper):* in Fig. 6a the processed surface band maps to a median of
  −212.6 Å and the unprocessed side band to −210.5 Å, a 2.1 Å step, close to the paper's d_layer = 2.087 Å
  (p. 3), so the height conversion looks consistent. In Fig. 11 the slipped-zone blue renders at hue ~250°, outside
  the key's 240°, and the far, undisturbed workpiece (which I would expect near 0 displacement; background
  expectation, not a statement of the paper) maps to about −1.6 Å. So Fig. 11 values may carry a bias of 1–2 Å and are
  flagged semi-quantitative. The allowed hue distance was widened to 15° so the blue zone maps at all.
- Fig. 11: the four red "Chip" arrows are blanked (boxes in the script); the white "Slipped zone" text stays empty
  but its anti-aliased edges take the surrounding blue. Fig. 6c/d: the authors' blue-grey ellipses are blanked by
  colour (hue 170–250°, max channel < 190, grown 2 px).
- Figs. 3, 4, 5, 7, 10 are coloured by layer/category without a numeric key: description only.

## Text check (`check_text.py` 2026-10-17j)

Command (from this folder): `python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/xie2019.pdf` — no options needed.

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 98.9 % | **99.8 %** (68 repeated tokens) | 99.8 % (0 in-figure tokens unmatched) | 99.9 % | 0 | 0 |

Every unmatched run (`--min-run 1`):
- REPEATED: the running header/footer "Page # of #" (17 pages), left out as boilerplate.
- MISSING (13 tokens): equation glyphs of the "Adv" math fonts in Eqs. (1)–(2) on pp. 2–3 ("=" stored as
  "¼", "+" as "þ", the equation-number parentheses as "ð … Þ", the large brackets as "h … i"): "1 4", "d", "th",
  "d h i d", "max 1 4"; and "cuttingedge" (p. 12), where a real hyphen ("cutting-edge") falls at a line end. No prose
  word is among them.
- EXTRA (7 tokens): "nanoscale research letters" (the large journal name at the top right of p. 1, which is not in the
  text layer) and "published online 06 december" (printed as an embedded image on p. 17, transcribed from it).

**Glyph audit** (`decompile_work/tools/glyph_audit.py source/xie2019.pdf --crops work/glyphs`): 1 hidden glyph
(p. 3, U+0002 in Eq. (2)); its crop shows an asterisk operator "0.5∗d_layer", written as `0.5{\ast}d_{layer}` in
main.tex. Checked.

Read-through against the page images: Eqs. (1)–(2) (incl. the printed sign in Eq. (1)), subscripts (r_w, d_layer,
a_max, F_t, F_n, C₁/C₂ where printed as subscripts and "C1"/"T1" where printed plain, T₁/T₂, D₀, r₀), nm⁻¹, Å, °,
×, nm³, Δ, α, ∞ in Table 3, italics of a, R, a/R, the a./b./c. and 1./2./3. list labels, and the reading order around
figures (each figure/table after the paragraph spanning its position; p. 13 and p. 16 hold only figures, so their
`\pdfpage` markers come after p. 14's and p. 17's, noted in the file). Line-end hyphens kept as real hyphens:
high-performance, cutting-edge, extrusion-dominated, nano-cutting (ref. 1; ref. 18 prints "nano-cutting" mid-line);
joined: micro-structure → microstructure (ref. 7), mono-crystalline → monocrystalline (ref. 3), sub-surface, co-hesion.

## Errors and oddities in the paper (kept verbatim; the ones marked * also flagged with `\decompnote` in main.tex)

- *a/R for the sharp tool (R = 0 nm) at a = 2 Å is given as 5.70 (p. 4 text, Fig. 8a) but 2.86/2.85 elsewhere (Figs.
  5a, 6a, 7a; text pp. 6, 11). The other a/R values in Figs. 3–5 are consistent with an effective "sharp" radius of
  0.7 Å (1.1/1.57, 1.4/2.0, 2/2.86); 5.70 is twice 2.85.
- *p. 5: at R = 3 nm "the ratio of a/R is 0.134"; 2 Å / 3 nm = 0.067 (as in Figs. 5c–8c). Again a factor 2.
- *Fig. 7e prints a/R = 0.054 for R = 7.5 nm; Fig. 6e prints 0.027 (= 2 Å / 7.5 nm).
- *p. 11: "Ft of 16.4 nN is evidently smaller than Fn of 23.7 nN" for the sharp tool, but Fig. 12a/b plot Ft ≈ 23.7 nN
  and Fn ≈ 16.8 nN at R = 0 (`fig12a.csv`, `fig12b.csv`): the two values appear swapped.
- p. 11: "When the tool edge radius is 3 nm and 5 nm, the ratios of a/R are 0.04 and 0.067": 3 nm gives 0.067 and 5 nm
  gives 0.04 (order reversed). Also "smaller than about 3 nm, namely, the ratio of a/R is 0.067 … always smaller than
  25 nN": the plotted Ft is 25.4 nN at 2 nm and 25.7 nN at 3 nm (Fig. 12b).
- *p. 11: the a/r_w values 0.055 and 0.080 for a = 1.1 Å and 1.6 Å equal a/R for R = 2 nm; a/r_w would be 0.86 and
  1.25. The same 0.055/0.080 recur on p. 12. On p. 4, "about 1.1 Å" is paired with a/r_w = 0.781, which is 1.0 Å/1.28 Å
  (1.1/1.28 = 0.86).
- *Eq. (1) prints the second exponent as +α(r − r₀). (My background knowledge, not from the paper: the usual Morse form
  has −α(r − r₀) there.) Not changed.
- *Fig. 8's caption repeats Fig. 7's "Surface composition of the processed surfaces"; the text calls Fig. 8 the defect
  structures in the subsurface.
- Fig. 12 has markers at R = 1 nm, which Table 1's list of tool edge radii (0, 2, 3, 4, 5, 7.5, 10 nm) does not include.
- Fig. 13 has no marker near 1.98 Å, and its markers sit at 0.18, 0.38, … (not at the round tick values).
- p. 8: "As displayed in Fig. 9a–c, … no subsurface defect …, when the tool edge radius is 2 nm or 3 nm": Fig. 9c is
  R = 4 nm.
- Text refers to numbered sections ("Section 3.3", "Sections 3.3 and 3.4", "Section 3.1", "Section 2 … 5"); the PDF's
  headings are unnumbered.
- Typos kept: "25 Nn" (p. 12), "0.087ev", "finical support", "stead stage", "underling", "If this case", "C₂," with the
  comma inside the subscript (p. 11).

Cross-checks of figure values against the text that agree: Fn ≈ 32 nN at 1.1 Å, Ft ≈ 25 nN and Fn ≈ 58 nN between 1.1
and 1.6 Å (Fig. 13); Ft ≈ 38.5 nN at 5 nm (Fig. 12b); a/R values printed in Figs. 3–9 vs a/R computed from a and R
(except those listed above).

## References in the collection

None of the 22 references is in `decompile_work/manifest.json` (checked by key prefix: fang/liu/merchant/woon/…;
the only hit, `xie2019`, is this paper itself, not its ref. 20).

## Not available

- No supplementary material or data set is named; nothing is missing.

## Figures re-viewed

All 19 figure crops, the two chart overlays, the four colour-map checks and six side-by-side comparisons were looked
at in this session; no image was described without being seen.

**Coordinator note (2026-10-18).** DOI 10.1186/s11671-019-3195-4 confirmed at Crossref (same title, Nanoscale Research Letters
14, 370, authors Xie and Fang). Coordinator's decision on 3D atom renderings: the grids for Figs. 8, 9 and 11 stay, but treat them
as semi-quantitative (pixel positions have no spatial meaning; Fig. 11 values may be biased 1–2 Å).
