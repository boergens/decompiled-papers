# peddie2022: decompiled

Christopher J. Peddie, Christel Genoud, Anna Kreshuk, Kimberly Meechan, Kristina D. Micheva, Kedar Narayan,
Constantin Pape, Robert G. Parton, Nicole L. Schieber, Yannick Schwab, Benjamin Titze, Paul Verkade,
Aubrey Weigel (printed "Aubrey Aubrey", see below), Lucy M. Collinson. "Volume electron microscopy."
*Nature Reviews Methods Primers* **2**, 2022 (article number not printed in this version).
DOI [10.1038/s43586-022-00131-9](https://doi.org/10.1038/s43586-022-00131-9), printed on p. 1 ("Published in final
edited form as: Nat Rev Methods Primers. ; 2: . doi:10.1038/s43586-022-00131-9.").

**Version:** Europe PMC Funders Group **author manuscript** (accepted manuscript), "available in PMC 2023 July 05",
typeset by Europe PMC (Antenna House), 53 pages. Not the publisher's version of record. In this version the boxes and the
figures with their legends follow the reference list (pp. 42–53).

**Licence:** "This work is licensed under a CC BY 4.0 International license." (p. 1 footnote).

**DOI confirmation:** verify-sources receipts `vs-20261013-851926a578` and `vs-20261013-bfcebcd8a3`
(`~/.local/share/verify-sources/receipts/`): Crossref resolved the DOI to "Volume electron microscopy", Nature Reviews Methods
Primers vol. 2 (issue 1), 2022, and matched it to this PDF (sha256 2e29dac5…, 53 pages). The Crossref record lists the
13th author as **Weigel** and a **Correction** (10.1038/s43586-022-00163-1, 2022-09-07); the correction is not in our
collection and it is not known whether this author manuscript includes it.

## Source files

| file | what it is |
|---|---|
| `source/peddie2022_vEM_primer_AAM.pdf` | the article, 53 pp., Europe PMC author manuscript; copied from `papers/peddie2022/`. Fetch note (`papers/peddie2022/SOURCE.txt`): "peddie2022_vEM_primer_AAM.pdf: https://serval.unil.ch/resource/serval:BIB_6FE84FD376F0.P001/REF.pdf (curl, 2026-10-13)" (served by the University of Lausanne repository SERVAL). |

`papers/peddie2022/` also holds `.txt`/`.raw.txt` text extractions (not used).

**Not available (not on this machine):**
- "Supplementary Material — Refer to Web version on PubMed Central for supplementary material." (p. 24): **Supplementary
  Movie 1** and **Supplementary Movie 2**, cited in the text (Experimentation: TEM-based vEM, SEM-based vEM). Not fetched.
- The example analysis workflows named under Code availability and Related Links
  (https://github.com/kreshuklab/vem-primer-examples) – code, not data for a figure.
- The paper names no data set or source data for its figures; Figure 5 uses the MitoEM data challenge data
  (https://mitoem.grand-challenge.org/), not fetched. So no panel has a tier-1 source.

## Contents

- `main.tex` / `main.pdf`: the whole manuscript in reading order: Europe PMC header block (citation line kept once),
  title, authors, affiliations 1–13 (p. 1–2), the p. 1 footnotes (licence, e-mail, Author contributions, Competing
  Interests, Related Links: 33 links; placed after the affiliations, noted in the file), Abstract, Introduction,
  Experimentation, Results, Applications, Reproducibility and data deposition, Limitations and optimizations, Outlook,
  Supplementary Material, Acknowledgements, Code availability, Glossary (18 terms), References 1–289, the second
  "References" list of 12 annotated key references (Ref 5 … Ref 138, printed in bold), Box 1, Box 2, Figures 1–8 with
  their legends. `\pdfpage{N}` marks every page start. Italics were recovered from the slanted text runs (`mutool trace`,
  skewed text matrix) – species names, *n*, *x, y*, *z*, *DNAH11*.
- Left out: running header ("Peddie et al.", "Page N"), running footer ("Nat Rev Methods Primers. Author manuscript;
  available in PMC 2023 July 05.", kept once in the header block), the vertical sidebar "Europe PMC Funders Author
  Manuscripts" with its logo (twice per page).
- `figures/fig1.png … fig8.png`: each figure rendered from the PDF at 200 dpi (embedded-image bbox + 2 pt).
- `figures/fig3.csv` (+ `_extract.py`, `.py`, `_replot.png`), `figures/fig5topright.csv` (same set).
- `tools/digitize_common.py`: copied helper module (osmium tools, read-only copy), imported by the extract scripts.
- No `tables/`: the manuscript has no tables.
- `work/`: scratch – `gen/` (scripts that drafted the LaTeX from the text layer: `gen.py`, `assemble.py`, `refs.py`,
  `captions.py`, `italics.py`; every result was checked afterwards), `alt/` (description drafts), overlays and
  side-by-side comparisons, `PROGRESS.md`. May be deleted.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (from this folder, run twice; `decomp.sty` is here).
Compiles without errors, no "Missing character"; 76 overfull-box warnings from long URLs and DOIs.

Re-run the data: `python3 -I figures/<panel>_extract.py`, then `python3 -I figures/<panel>.py` (any working directory).

## Figures

All eight figures are single embedded 300 ppi JPEG images (2096 px wide; Fig. 8 1544 × 2099 px); there are no
vector plot paths (the only drawings on the figure pages are the sidebar band, a fill and a line, checked with
`get_drawings()`), and no text layer inside the figures. Embedded-image digests are all different (no duplicated plate).

| figure / panel | type | data file | provenance |
|---|---|---|---|
| Fig. 1 A–D + bottom flow | workflow schematic (drawings, a 3D rendering, an unlabelled bar chart without axes) | – | description only (bar chart illustrative, no axes) |
| Fig. 2 (TEM, SEM, ssTEM, ssET, GridTape TEM, SBF-SEM, FIB-/pFIB-SEM, eFIB-SEM, array tomography, AT + ATUM) | schematic drawings | – | description only |
| Fig. 3 (single panel) | region chart: resolution vs target volume, soft coloured regions | `fig3.csv` | tier 3, digitized (colour unmixing of the raster, outlines at half colour strength) |
| Fig. 4 | schematic (correlative and comparative vEM workflows) | – | description only |
| Fig. 5 mSEM image, semantic segmentation, instance segmentation, analysis result, volume rendering | micrograph, label/colour maps without a colour key, 3D rendering | – | description only (colour maps without key) |
| Fig. 5 top right | histogram (Count vs mitochondria volume, 10³ pixels) | `fig5topright.csv` | tier 3, digitized |
| Fig. 6 A (cell rendering + 3 insets), B, C, D | 3D renderings, FIB-SEM slice, annotation | – | description only |
| Fig. 6 E, F | FIB-SEM slices | – | description only |
| Fig. 7 A, B | volume rendering with dimensions; neuron rendering with a count legend (transcribed in the description) | – | description only |
| Fig. 7 C | 3D renderings + developmental timeline (category axis, no numbers) | – | description only |
| Fig. 7 D | 8 wiring diagrams, axes without numbers | – | description only (qualitative) |
| Fig. 8 A–J | 3D renderings and SBF-SEM/EM images | – | description only |

Panels per provenance tier: tier 1: 0; tier 2: 0; tier 3: 2 (Fig. 3, Fig. 5 histogram); tier 4: 0.
All other panels are images or qualitative schematics with a description (`\alttext`) and the PNG.

**Fig. 3** has evenly spaced ticks on both axes. x: 100 nm, 1 μm, 10 μm, 100 μm, 1 mm – one decade per tick (labelled
"Target volume" but the ticks are lengths); given as log10(nm). y: 1, 5, 10, 50, 100, 1000 nm, evenly spaced although the
values are not (category-style axis); given as the tick position (0–5) and, marked as an interpretation, as nm interpolated
log-linearly between neighbouring labels. Regions are blurred: each pixel's colour is unmixed into strengths of the five
region colours (at most two per pixel), and an outline is drawn where the strength is 0.5. Edges hidden under another
region (right ends of the FIB-SEM and SBF-SEM bands, bottom of the X-ray region) are uncertain.
**Fig. 5 histogram:** bars by colour mask, axes fitted on 6 ticks each (max residual 0.05 units in x, 0.03 counts in y).
Counts 28, 16, 4, 2, (four empty bins), 3, 1 = 54 mitochondria; bin width ≈ 9.55 (10 equal bins from ≈1.1 to ≈96.7 –
consistent with matplotlib's default of 10 bins; that is my reading, not stated in the paper).

**Checks:** each extraction draws its result back on the source image (`work/fig3_overlay.png`,
`work/fig5topright_overlay.png`), and each replot was put next to the original with `compare.py`
(`work/cmp_fig3.png`, `work/cmp_fig5topright.png`); I looked at all four: outlines follow the half-strength edges of the
regions and the bar edges and tops sit on the printed bars; ranges, ticks and scales match.
**Cross-check with the text:** the Fig. 3 FIB-SEM band (≈3–10 nm) agrees with the text's "4 nm isotropic resolution" and
"5 nm for FIB-SEM" slices; the X-ray region (≈43 nm and up) with Box 2 ("tens to hundreds of nanometres" for synchrotrons).
No mismatch found.

All figure descriptions were written from the 200 dpi crops (and 250–400 dpi zooms of Fig. 7 B/C legend text), each
viewed with the image tool in this session (Figs. 1–8; no "media removed" message).

## Check results

`python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/peddie2022_vEM_primer_AAM.pdf`
(check_text.py 2026-10-17j, no options):

- PDF tokens 26 520, tex tokens 25 131; coverage **97.0 %** raw; **100.0 %** without text repeated on ≥ 3 pages
  (790 tokens); **100.0 %** also without in-figure text (0 tokens: the figures are rasters with no text layer).
  100.0 % of tex tokens found in the PDF.
- REPEATED: the sidebar "Europe PMC Funders Author Manuscripts" (53 pages, twice per page) and the header
  "Peddie et al. Page #" (52 pages). MISSING runs ≥ 6: 0. EXTRA runs ≥ 6: 0.
- `glyph_audit.py source/peddie2022_vEM_primer_AAM.pdf --crops work/glyphs`: **0** hidden glyphs (clean born-digital
  text layer; the only non-Latin glyphs are two β from a Code2000 font, which extract correctly). The one "~" (p. 21,
  "is ~200 μm") is an ASCII tilde in print and written `\textasciitilde{}`.
- Read-through against the page images: superscript citations (8 pt spans in 10 pt text, including those broken onto
  their own line at a line start), the one non-superscript citation "used 267:" in the Fig. 8 legend (printed full size,
  kept so), μm³ superscripts, ±70°, ×, <, italics, bold run-in headings ("Fixation—" etc.), glossary, boxes.

## Errors and oddities in the paper (kept as printed, noted in `main.tex`)

- Author list and PDF metadata print **"Aubrey Aubrey"**; the contributions and acknowledgements say "A.W." and Crossref lists
  Aubrey **Weigel**.
- Acknowledgements: "Wellcome Trust (FC001999." – closing parenthesis missing.
- Code availability: "…vem-primer-examples.Figure Legends" – a conversion heading run into the text.
- Figure 6 legend: no "E:" label; the panel-E description is followed by "F:" and panel F is described again.
- Figure 8 legend: citation "267" printed full size ("SBF-SEM was used 267:"), not as a superscript.
- References: literal conversion markup "<em>…</em>" (refs. 82, 143, 253, 285) and
  "<emphasis emphasistype=“mono”>elastix</emphasis>" (ref. 161); ref. 252 "Platynereislarval" (missing space).
- "Published in final edited form as: Nat Rev Methods Primers. ; 2: ." – issue and article number missing in the PMC line.

## References in our collection (from `decompile_work/manifest.json`, checked by title)

Same work: 36 → luft1961, 40 → staeubli1963, 41 → spurr1969, 51 → hayworth2015, 52 → xu2017, 85 → yin2020,
92 → denk2004, 94 → titze2013, 95 → deerinck2018 (cited as 2017, same DOI 10.1111/jmi.12667), 141 → hayworth2014,
173 → scheffer2020.
Other version of the cited work: 13 → hildebrand2017 (local: bioRxiv preprint; cited: Nature 2017), 82 → zheng2018 (local:
bioRxiv 2017 preprint; cited: Cell 2018), 84 → phelps2021 (local: bioRxiv 2020 preprint; cited: Cell 2021),
248 → microns2025 (cited: the 2021 bioRxiv preprint; local: the 2025 Nature paper).
Not the same work despite the key: ref. 88 (Kubota, Sohn, Kawaguchi 2018, Front Neural Circuits) ≠ kubota2018 (Nat Commun);
ref. 238 (Baena & Terasaki 2019, ovarian follicle) ≠ baena2019 (Methods Cell Biol); ref. 125 (Wanner et al. 2016) ≠ wanner2015;
ref. 129 (Kremer et al. 2021) ≠ kremer2015; ref. 37 (Glauert et al. 1956) ≠ glauert1958.

## Known problems

- Fig. 3 regions are qualitative soft shapes; outlines depend on the half-strength convention and are uncertain where
  regions overlap.
- Paragraph breaks at page boundaries were inferred (p. 7→8 assumed a new paragraph: p. 7 ends a sentence at the bottom
  of a full page and p. 8 starts with a capital; not decidable from the layout).
- Italics were recovered from slanted text runs only; the manuscript has no italic font, so any italics drawn otherwise
  would be missed (none seen in the read-through).
