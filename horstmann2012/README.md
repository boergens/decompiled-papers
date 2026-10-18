# horstmann2012: decompiled

Heinz Horstmann, Christoph Körber, Kurt Sätzler, Daniel Aydin, Thomas Kuner. "Serial Section Scanning
Electron Microscopy (S³EM) on Silicon Wafers for Ultra-Structural Volume Imaging of Cells and Tissues."
*PLoS ONE* **2012**, 7(4): e35172. DOI [10.1371/journal.pone.0035172](https://doi.org/10.1371/journal.pone.0035172)
(printed in the PDF, p. 1 and in every figure caption). Received December 15, 2011; accepted March 9, 2012;
published April 16, 2012. Editor: Michael A. Fox.

**Licence:** © 2012 Horstmann et al., open access under the Creative Commons Attribution License (p. 1).

**DOI check:** verify-sources receipt `vs-20261013-9be334fbf4` (outcome verified_with_warnings): Crossref
resolved the DOI to this article (authors, PLoS ONE 7(4)), and the receipt's PDF SHA-256
(`13808c63…549595`, 896 540 bytes, 8 pp.) is identical to `source/horstmann2012_s3em.pdf`. The whitepaper
cites it the same way (`web/whitepaper.md`, References).

## Source files

| file | what it is |
|---|---|
| `source/horstmann2012_s3em.pdf` | the article, 8 pp. **Publisher version of record** (PLoS ONE typeset PDF, 3B2 Total Publishing System, Acrobat Distiller 9; created 2012-04-06). Copied from `papers/horstmann2012/`, whose `SOURCE.txt` says: "horstmann2012_s3em.pdf: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0035172&type=printable (curl, 2026-10-13)". |

`papers/horstmann2012/` also holds `horstmann2012_s3em.txt` / `.raw.txt` (earlier text extractions; not used,
not copied). There is no supplement PDF: the paper's Supporting Information is three movies (below).

**Not available (tier-1 / supplementary material named by the paper):** Movie S1 (100 raw consecutive
sections, AVI), Movie S2 (40 cropped, aligned images, AVI), Movie S3 (3D representation, AVI). The paper
names no data set or source-data file; the OpenCAR software is cited at http://opencar.ulster.ac.uk
(not fetched). "blue print available from the authors" for the mounting device (p. 2): not available.

**Cited works in our collection** (from `decompile_work/manifest.json`): ref. 14, Denk & Horstmann 2004
(PLoS Biol 2: e329) = `denk2004`. No other reference of this paper is in the manifest (ref. 28, Hayworth
et al. 2006, is a Microsc Microanal abstract, not `hayworth2014`).

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: title, authors, affiliations, abstract,
  the p. 1 citation/editor/dates/copyright/funding/competing-interests/e-mail block (after the abstract, as
  printed), Introduction, Materials and Methods, Results, Discussion, Supporting Information (movie
  legends), Author Contributions, References 1–37. `\pdfpage{N}` markers at each page start.
- `figures/`: `fig1.png` … `fig5.png` (crops at 200 dpi, the native resolution of the embedded JPEGs);
  `fig5e.csv`, `fig5e_extract.py`, `fig5e.py`, `fig5e_replot.png`.
- `tools/digitize_common.py`: copy of the osmium helper module, imported by `fig5e_extract.py`.
- `decomp.sty`: copy of the macro file; compile from this folder with
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` (run twice). Compiles without errors; 7 overfull
  lines of < 2 pt.
- `tables/`: not created. The paper has no tables.
- `work/`: scratch (page renders, embedded images, overlay, side-by-side comparison, check JSON,
  `fixtext.py` = a text-layer dump with the broken symbol glyphs mapped, used as a transcription aid). May be deleted.

Re-run the data: `python3 -I -B figures/fig5e_extract.py` then `python3 -I -B figures/fig5e.py` (any working
directory; paths are relative to the scripts).

## Figures

All five figures are single embedded 200 ppi RGB JPEGs; the PDF has no vector drawings on pp. 2–8
(`page.get_drawings()` is empty; p. 1 has only the logo/abstract-box paths). Image digests are all distinct
(no repeated plates). Only Fig. 5E is a plot.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | photograph: positioning frame | – | – | |
| Fig. 1B | photograph: frame on ultramicrotome | – | – | |
| Fig. 1C | photograph: micromanipulator, forceps, knife boat | – | – | |
| Fig. 1D | photograph: wafer in knife boat close to the knife edge | – | – | |
| Fig. 1E | photograph: wafer on SEM sample holder in chamber | – | – | |
| Fig. 1F | photograph: wafer with two ribbons, arrows at jumper link | – | – | |
| Fig. 2A | SEM, ribbon on wafer, 27x, bar 500 μm | – | – | |
| Fig. 2B | SEM, trapezoid sections, 90x, bar 100 μm | – | – | |
| Fig. 2C | SEM, section with landmarks, 500x, bar 20 μm | – | – | asterisks, arrows |
| Fig. 2D | SEM, MNTB principal neuron, 2000x, bar 10 μm | – | – | box E |
| Fig. 2E | SEM, calyx segment, 10000x, bar 2 μm | – | – | box F |
| Fig. 2F | SEM, 20000x, bar 500 nm | – | – | |
| Fig. 3A | SEM micrograph, synapse, symbols *, +, arrowheads, arrows | – | – | |
| Fig. 3B | SEM micrograph, bar 250 nm | – | – | |
| Fig. 4A₁–A₅ | SEM, 5 consecutive sections, bar 1 μm (A₅) | – | – | boxes B–E in A₄/A₅ |
| Fig. 4B–D | SEM details, bar 200 nm (D) | – | – | |
| Fig. 4E | SEM detail, synaptic cleft, bar 200 nm | – | – | |
| Fig. 5A–C | 3D surface renderings (colour key in caption) | – | – | no scale bars |
| Fig. 5D | 3D rendering, one release site | – | – | |
| Fig. 5E | histogram, No. SVs vs distance SV to AZ | `figures/fig5e.csv` | **3 digitized** | bar heights all within 0.02 of integers; sum 82 |

**Fig. 5E extraction:** axis lines and ticks located in the embedded JPEG (xref 28, 1008 × 1217 px); y
calibrated on the ticks 0, 5, 10 (18.35 px per count, residual 0.009 counts), x on the nine ticks 0–320 nm
(residual 0.4 nm). Each bar's top edge was read in its centre column. 16 bars at 0–340 nm in 20 nm steps,
none at 260 and 320 nm. The CSV gives the digitized height and the rounded integer count; the counts sum to
**82**, matching the text's "n = 82 synaptic vesicles" (p. 5). **Checks done:** the extracted bar tops and
side lines were drawn back onto the source image (`work/fig5e_overlay.png`, `work/fig5e_overlay_crop.png`)
and sit on the printed bar outlines; original and re-plot were put side by side with `compare.py`
(`work/cmp_fig5e.png`); bins, heights, axis ranges and ticks match. I looked at both images.

## Text check (`check_text.py` version 2026-10-17j, options `--min-run 1`)

`python3 -I -B .../tools/check_text.py main.tex source/horstmann2012_s3em.pdf`

| | value |
|---|---|
| coverage of PDF tokens (raw) | 97.2 % |
| without text repeated on ≥ 3 pages | **99.0 %** (112 repeated tokens: the footer "PLoS ONE \| www.plosone.org # April # \| Volume # \| Issue # \| e#") |
| also without unmatched in-figure text | 99.0 % (0 in-figure tokens; all figure lettering is inside the JPEGs) |
| tex tokens found in PDF | 99.0 % |

No option beyond `--min-run 1` is needed. All 37 MISSING runs (60 tokens) and 34 EXTRA runs (63 tokens) are
**broken font encoding in the text layer** (3B2 PDF with custom-encoded symbol fonts), corrected against the
page images:

| PDF text layer | printed | font | approx. count |
|---|---|---|---|
| `m` (so μm reads "mm") | μ | AdvP697C | 29 (μm, μs) |
| `6` | × | AdvPi1 | 14 |
| `6` | ± | AdvP3D3256 | 4 (35±2, 525±25, mean ±, 45.9±0.7) |
| `u` | ° | AdvP44E6F4 | 3 (4°C, 60°C, 35°) |
| `,` | \~ | AdvP7DB7 | 15 (no token, so not counted by the checker) |
| `,` | < | AdvP7DA6 | 2 (no token) |
| `V` | Ω | AdvP3EAA99 | 1 (Ωcm) |
| `\x02` | © | AdvT377 | 1 |

plus two one-token alignment artifacts of split accents ("c" after "Ko¨ rber", p. 1; "k" after
"Sa¨tzler", p. 8: the same token reported once MISSING and once EXTRA) and one real line-end hyphen joined
by the checker ("ultra-thin", p. 7). The running header "Serial Section Scanning Electron Microscopy"
(pp. 2–8) is left out of main.tex but is not reported, because the same words occur in the title. Leaving
these out, every word of the PDF's text is matched.

Read-through against the 200 dpi page images (step 4) done for: all ×, ±, °, μ, \~, <, Ω; superscripts
(S³EM everywhere, μm², μm³), CO₂, A₅ in "Fig. 4A₅", en dashes in citation ranges and page ranges, italics
(*Caenorhabditis elegans* p. 1, *Reconstruct* p. 5; references are not italic), bold panel letters in
captions (Fig. 1 prints "C:" in regular type; noted in main.tex), "N++/As", "#5".

## Errors and oddities in the paper (kept verbatim)

- Typos: "lager areas" (p. 4, = larger); "accelerted" (p. 7); "SFBSEM" (p. 7, for SBFSEM); "Elservier"
  (ref. 20); "evenly space by resin" (Fig. 2 caption); "principle neuron"/"principle cell" (Fig. 2 and 4
  captions; Movie S1 legend has "principal cell"); "potassium ferry cyanide" (p. 2); "calyx of held" (ref. 21).
- "focal ion beam (FIB) milling" (p. 1), while ref. 16's title says "focused ion beam milling".
- Fig. 1 caption: "C:" is not bold, unlike the other panel labels.
- Dwell time vs frame time (my calculation, not in the paper): 3072 × 2304 pixels at \~40 μs/pixel is
  ≈ 283 s ≈ 4.7 min, more than the "\~3 min" per full frame on p. 2 (and the "3 minutes scanning time" on
  p. 7). 3072 × 2304 pixels at 3.7 nm give 11.4 μm × 8.5 μm = 96.9 μm² (consistent with p. 2), slightly more
  than the "\~11 μm×8.3 μm" on p. 3/4.
- Ref. 33 prints "Protoplasma 39: 160–169" for a 1987 paper. From my background knowledge (not checked
  here), the volume is probably 139; flagged as unverified.
- Consistent: Fig. 5E's bars sum to 82, the "n = 82" of p. 5; 100 sections × 35 nm = the 3.5 μm depth.

## Problems and suggestions

- check_text.py could take a per-PDF glyph map (font name + glyph → Unicode, as in `work/fixtext.py`) so
  3B2/PLoS PDFs with custom-encoded symbol fonts reach 100 % instead of needing a manual category table.
  The "\~" and "<" errors (comma glyphs) are invisible to a token checker, so these must be checked by eye.

## Time

About 35 minutes: spec, tools and page reading ~8 min; Fig. 5E digitization and checks ~7 min;
transcription and figure descriptions ~15 min; checks and README ~5 min.
