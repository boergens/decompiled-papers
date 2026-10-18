# kubota2018: decompiled

> **This folder is a self-contained copy** of `~/ephemeral/sep_28__osmium_chemistry/decompiled/kubota2018/` (made 2026-10-17): source PDFs in `source/`, shared helpers in `tools/`, `decomp.sty` here; the figure scripts' paths were adapted. Paths in the text below that point to `../../papers/kubota2018/` or `../tools/` refer to the original project; here they are `source/` and `tools/`. Scratch (`work/`) was not copied.


Yoshiyuki Kubota, Jaerin Sohn, Sayuri Hatada, Meike Schurr, Jakob Straehle, Anjali Gour, Ralph Neujahr,
Takafumi Miki, Shawn Mikula, Yasuo Kawaguchi. "A carbon nanotube tape for serial-section electron
microscopy of brain ultrastructure." *Nature Communications* **9**, 437 (2018).
DOI [10.1038/s41467-017-02768-7](https://doi.org/10.1038/s41467-017-02768-7).
Received 3 March 2017, accepted 26 December 2017, published online 30 January 2018.
(All taken from the PDF; they agree with the task message.)

**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), "Open Access" statement on p. 15;
"© The Author(s) 2018".

Why it is here: pointed to by Sarah Mikula (mail of 2026-10-13, per `SOURCE.txt`) for its fixation protocol
(picric acid in the fixative). See "Protocol: where to find it" below.

## Local and external

**In the local collection**
- Source files:
  - `papers/kubota2018/s41467-017-02768-7.pdf` – main article, 15 pp., publisher version of record
  - `papers/kubota2018/41467_2017_2768_MOESM1_ESM.pdf` – Supplementary Information, 26 pp. (authors' Word file with line numbers)
  - `papers/kubota2018/41467_2017_2768_MOESM2_ESM.pdf` – Peer Review File, 32 pp.
  - `papers/kubota2018/41467_2017_2768_MOESM3_ESM.pdf` – Description of Supplementary Files, 1 p.
  - `papers/kubota2018/SOURCE.txt` – fetch note
- Cited works decompiled here: to be tagged by the coordinator (`tools/mark_local.py`); likely candidates
  are ref. 5 (Kasthuri 2015), ref. 22 (Mikula & Denk 2015), ref. 38 (Seligman 1966), ref. 41 (Hua 2015),
  ref. 60 (Mikula 2012) and SI refs 2 and 9.

**External pull needed** (not on this machine)
- **Supplementary Movie 1** (MOESM4, mp4; "Serial ultrathin section images with GABA post-embedding
  immunoreaction ...", main text p. 5 and MOESM3) – URL in `SOURCE.txt` – a movie, not plot data.
- **Ref. 70**, Kubota, Y. "Electron micrographs and raw data for the signal intensity histograms", figshare
  (printed link `https://figshare.com/account/home`, which is a login page, not a data-set DOI) – the
  **tier-1 source for Fig. 6c and 6f** (they stay tier 3 here).
- Data availability: "available from the corresponding authors upon reasonable request" – nothing else is named.
- All other cited references (70 in the main list, 9 in the SI list) without a [local: …] tag.

## Source files (`../../papers/kubota2018/`)

| file | what it is |
|---|---|
| `s41467-017-02768-7.pdf` | main article, 15 pp. **Publisher version of record** (Nature Communications typesetting, Springer/iText). Born-digital; all figures are 300 ppi raster images with axis labels as PDF text; no vector plot paths. The line "Published online: 30 January 2018" (p. 14) is a 1-bit image without text layer. |
| `41467_2017_2768_MOESM1_ESM.pdf` | Supplementary Information, 26 pp.: Notes 1–4, Supplementary Methods, Supplementary Figures 1–13 (one embedded 150–231 ppi image each, legend below), Supplementary Tables 1–3 (**images**, p. 25), Supplementary References 1–9. Line numbers 1–425 in the margin. |
| `41467_2017_2768_MOESM2_ESM.pdf` | Peer Review File, 32 pp. (three reviewers, several rounds, authors' replies). Text only, no images. |
| `41467_2017_2768_MOESM3_ESM.pdf` | "Description of Supplementary Files" (one entry: Supplementary Movie 1). Transcribed at the end of `supplement.tex`. |

## Contents

- `main.tex` / `main.pdf`: the whole article (journal block, title, authors, affiliations moved after the
  author list, abstract, introduction, Results, Discussion, Methods with all equations, data availability,
  dates, 70 references, Acknowledgements, Author contributions, Additional information, licence).
  Figs. 1–7 and Table 1 with verbatim captions, descriptions and data pointers. `\pdfpage{}` at every page.
- `supplement.tex` / `supplement.pdf`: the whole SI (MOESM1) and, at the end, MOESM3.
- `peer_review.tex` / `peer_review.pdf`: the Peer Review File, verbatim text.
- `figures/`: `fig1.png`–`fig7.png`, `sfig1.png`–`sfig13.png` (200 dpi crops, captions not included) and
  per plotted panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png`. Shared helper
  modules: `kubota_main_common.py` (main figures), `sfig_common.py`, `sfig45_common.py` (SI figures).
- `tables/`: `table1.csv` (Table 1, the staining-protocol comparison), `stable1.csv`–`stable3.csv`
  (Supplementary Tables 1–3, transcribed from images).
- `work/`: scratch (page renders, drafts, conversion scripts in `work/scripts/`, overlays `*_overlay.png`,
  side-by-side comparisons `cmp_*.png`, LaTeX logs). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (and
`supplement.tex`, `peer_review.tex`); all three compile without errors (run twice).

Re-run the data: `python3 -I -B figures/<x>_extract.py`, then `python3 -I -B figures/<x>.py`, from any directory.

## Protocol: where to find it

All in `main.tex` (Methods, p. 12) and Table 1 (p. 7, also `tables/table1.csv`), verbatim:
- **Perfusion/fixation** (Methods "Tissue preparation", p. 12): rats anesthetized with pentobarbital
  (60–75 mg kg⁻¹), perfused with 5–10 ml of 250 mM sucrose, 5 mM MgCl₂ in 0.02 M phosphate buffer (pH 7.4),
  then 300 ml of **4 % paraformaldehyde containing 0.2 % picric acid and 1–2 % glutaraldehyde in 0.1 M PB**
  (citing ref. 63, Kubota, Neuromethods 110). 50 µm vibratome sections, stored in cryoprotectant (30 %
  glycerol, 30 % ethylene glycol, 0.04 M PBS) at −20 or −30 °C. The paper gives no post-fixation time for
  the brain, no osmolarity and no perfusion rate or temperature.
- **Heavy-metal staining** ("Metal post-fixation and preparation for EM observations", p. 12, and Table 1):
  TO (ferrocyanide-reduced OsO₄ then OsO₄), TOLA (TO + uranyl acetate en bloc + Walton's lead aspartate,
  recipe given), mHMS (rOTO with TCH + UA + lead aspartate); BROPA and Hua (2015) columns in Table 1 are
  the published protocols of refs. 22 and 41. Lead citrate recipe (ref. 66) also given.
- **Dehydration/embedding**: "graded dilutions of ethanol" (no steps given), flat-embedding in Durcupan ACM
  or EMbed-812, 60 °C for 48–72 h.

**Inconsistencies between Table 1 and the Methods text** (both kept verbatim; my reading, not the paper's):
- mHMS step 4: Table 1 "2% OsO4 unbuffered, 0.5h @ RT"; Methods "incubated for 1 h in 2% osmium tetroxide".
- Uranyl acetate for mHMS and TOLA: Table 1 "overnight @ RT"; Methods "at 4 °C protected from light overnight".
- TOLA lead aspartate: Table 1 "1h @ 60 °C"; Methods (TOLA paragraph) "in the oven for 30 min".
- TO uranyl acetate: Table 1 lists a separate step "1% uranyl acetate unbuffered, 40 min @ RT"; Methods
  says UA was "added at the 70% ethanol dehydration state".
- Step 1 temperature (1 h @ 4 °C in Table 1) is not stated in the Methods.
- Table 1 "Figure panels" row: the TO column lists "Figs. 4f–k, 6b–d, h–j, n-p, t-v, x"; the TO panels of
  Fig. 5 are b–d, h–j, n–p, t–v, x (per the Fig. 5 caption), so "6b–d …" probably means "5b–d …"; and Fig. 4j, k
  are TOLA per the Fig. 4 caption.

## Figures

All plots in both PDFs are raster images; `vector_dump.py` / `get_drawings()` finds no plot paths (main
pp. 3, 6, 10: only the □ glyph and the ⇦/⇨ outlines; SI: none). Fig. 6g, h are **tier 1** from Supplementary
Table 3 (values checked against the plotted markers: all 24 within 1–1.5 px). Everything else is
**tier 3 (digitized)**: axes calibrated on tick marks in the embedded images (main: tick labels from the PDF
text), series traced with colour masks / marker detection / histogram top edges. Colour maps with colour
bars (3D laser SCM depth images) were mapped through the bar.

**Checks:** every extraction draws its points back onto the source image (`work/*_overlay.png`) and every
replot was put next to the original with `tools/compare.py` (`work/cmp_*.png`); both were looked at for every
panel. Fig. 1b reproduces the text's "242 ± 18.0 Ω □⁻¹, between 223–305" (digitized: 242.3 ± 18.0, 222.7–304.8).

**Fig. 3d colour map is unreliable**: mapping the colours through the printed colour bar (labels −550, −400,
−200, 0 nm, no ticks) gives about −374, −445, −466, −466 nm (median per square) for the four squares labelled
−223, −337, −371, −383 nm. The ordering agrees, the values do not: the bar labels seem not to match the bar
colours (the −400/−200 labels sit off a linear scale), and the rendering is shaded. Use the printed depths.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | schematic (tape layers) | – | – | |
| Fig. 1b | line plot with markers, broken y axis | `figures/fig1b.csv` | 3 digitized | 32 points; mean/SD/range match the text |
| Fig. 1c, f, i, j | SEM overviews of sections on tape | – | – | |
| Fig. 1d, g | photographs of water droplets (contact angle) | – | – | 79.5°, 7.4° printed |
| Fig. 1e, h | schematics (section landing) | – | – | |
| Fig. 1k | markers + SD error bars (n = 3) | `figures/fig1k.csv` | 3 digitized | caps at the marker edge flagged |
| Fig. 2a–d | SEM micrographs | – | – | |
| Fig. 3a–c, e–i | SEM micrographs | – | – | |
| Fig. 3d | 3D laser SCM colour map with colour bar | `figures/fig3d.csv` (grid, nm) | 3 digitized | approximate, disagrees with the printed depths (above) |
| Fig. 4a | 4 line-plot sub-panels, broken y axis | `figures/fig4a.csv` | 3 digitized | `excitation` column |
| Fig. 4b | line plot, 3 reflection spectra | `figures/fig4b.csv` | 3 digitized | |
| Fig. 4c | line plot, 3 transmission spectra | `figures/fig4c.csv` | 3 digitized | cc-Kapton ≈ 0 on the axis below ~465 nm flagged |
| Fig. 4d | bar chart | `figures/fig4d.csv` | printed values + 3 digitized bars | |
| Fig. 4e | bar chart | `figures/fig4e.csv` | printed values + 3 digitized bars | |
| Fig. 4f–i | SEM micrographs (immunogold) | – | – | |
| Fig. 4j, k | fluorescence micrographs | – | – | |
| Fig. 5a–y | SEM/TEM micrographs | – | – | |
| Fig. 6a, b, d, e | SEM micrographs | – | – | |
| Fig. 6c | 6 filled histograms | `figures/fig6c.csv` | 3 digitized | tier-1 source (ref. 70) not available |
| Fig. 6f | 6 filled histograms | `figures/fig6f.csv` | 3 digitized | ref. 70 not available |
| Fig. 6g | markers + lines | `figures/fig6g.csv` | **1** (Suppl. Table 3) | |
| Fig. 6h | markers + lines | `figures/fig6h.csv` | **1** (Suppl. Table 3) | |
| Fig. 7a | 3D rendering (microCT) | – | – | |
| Fig. 7b–g | SEM mosaics/micrographs | – | – | |
| Suppl. Fig. 1a–j | SEM images, photographs (winder, torch) | – | – | panel d title/legend mismatch |
| Suppl. Fig. 2a–n | photographs, schematic (g), SEM images | – | – | |
| Suppl. Fig. 3a, c | sET images | – | – | |
| Suppl. Fig. 3b | SCM colour height map with colour bar | `figures/sfig3b.csv` (+ `_colourbar.csv`) | 3 colour map | by hue; black and red bar ends not resolved; 8–10 keV far too shallow vs printed |
| Suppl. Fig. 3d | SCM colour height map | `figures/sfig3d.csv` (+ `_colourbar.csv`) | 3 colour map | systematically below the printed heights |
| Suppl. Fig. 3e | scatter, 2 series | `figures/sfig3e.csv` | 3 digitized | agrees with the depths printed in b, d within ~1 px |
| Suppl. Fig. 3f | scatter | `figures/sfig3f.csv` | 3 digitized | |
| Suppl. Fig. 4a, b | SEM images | – | – | |
| Suppl. Fig. 4c | SCM colour map | `figures/sfig4c.csv` (+ `_colourbar.csv`) | 3 colour map | printed depths transcribed in `\alttext` and in sfig4d/f CSVs |
| Suppl. Fig. 4c inset | tiny line graph | `figures/sfig4c_inset.csv` | 4 read by eye | ±10 nm; no extract/plot script (5 values) |
| Suppl. Fig. 4d–g | line plots | `figures/sfig4d.csv` … `sfig4g.csv` | 3 digitized | hidden markers flagged; panel-c depths in a column |
| Suppl. Fig. 5a, b | SEM images | – | – | |
| Suppl. Fig. 5c | SCM colour map | `figures/sfig5c.csv` (+ `_colourbar.csv`) | 3 colour map | black bar end not resolved |
| Suppl. Fig. 5d–g | line plots | `figures/sfig5d.csv` … `sfig5g.csv` | 3 digitized | 5g mostly hidden (only 6 keV complete) |
| Suppl. Fig. 6a–f | SEM images | – | – | |
| Suppl. Fig. 7a–c, e | SEM images | – | – | |
| Suppl. Fig. 7d | SCM colour map | `figures/sfig7d.csv` (+ `_colourbar.csv`) | 3 colour map | bump heights (>400 nm) not resolved |
| Suppl. Fig. 8–12 | SEM images | – | – | |
| Suppl. Fig. 9a, d | SEM images | – | – | |
| Suppl. Fig. 9b | Monte Carlo trajectory images | – | – | |
| Suppl. Fig. 9c | 2 line plots, 11 series each | `figures/sfig9c.csv` | 3 digitized (approximate) | solid = row trace, dashed = dash centroids; some mis-assignments listed in the CSV |
| Suppl. Fig. 13 | dimensioned engineering drawing | – | – | dimensions in `\alttext` |

**Colour maps (Fig. 3d; Suppl. Figs. 3b, 3d, 4c, 5c, 7d):** the 3D laser SCM depth images are shaded
renderings, so nearest-colour matching through the colour bar fails (70–100 % unmatched); the CSVs map by hue,
which leaves 7–23 % unmapped and cannot resolve bar stretches of constant hue (black and red ends). Compared with
the depths printed on the images they are good to roughly ±50 nm at mid-range and poor elsewhere. **Use the
printed depth numbers** (transcribed in the `\alttext`, and for Suppl. Figs. 4c/5c in the `printed_panel_c`
column of `sfig4d/f.csv`, `sfig5d/f.csv`) for anything quantitative; the maps are qualitative.

## Text check (`tools/check_text.py` 2026-10-17j)

| file | options | coverage | without repeated text | running text (also without in-figure text) | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | – | 93.4 % | 94.0 % (80 repeated tokens) | 96.1 % | 14 runs, 399 tokens | 0 |
| `supplement.tex` (vs MOESM1 + MOESM3) | `--drop-line-numbers` | 99.5 % | 99.5 % | 99.5 % | 0 | 6 runs, 402 tokens |
| `peer_review.tex` | – | 99.9 % | 99.9 % | 99.9 % | 0 | 0 |

No `--exclude` or `--figure-box` was needed. For the supplement, `--drop-line-numbers` is needed
(the SI has margin line numbers 1–425).

- **main, MISSING:** all 14 runs ≥ 6 are text printed around or inside figures that the tool does not
  recognise as figure text (axis tick labels, axis titles, panel titles such as "Before plasma", "2 keV In-lens
  SE", "Gray scale", "Reduced signal … Good … Greater the noise from tape", the Fig. 5 row labels); it is
  described in `\alttext`. Short runs (`--min-run 1`): running header "ARTICLE" and footers (repeated), panel
  letters, the margin stamp "1234567890():,;", real hyphens joined by the tool's dehyphenation ("In-lens",
  "cc-Kapton", "well-preserved", "CNT-coated", "to-noise"), and the Methods equations, whose text layer uses
  a math font with private codes ("¼" for =, "ð Þ" for brackets).
- **main, EXTRA:** none ≥ 6; short ones are equation tokens and "Published online: 30 January 2018" (an image
  in the PDF).
- **supplement, EXTRA:** the six runs are Supplementary Tables 1–3, transcribed from images (no text layer).
  MISSING (`--min-run 1`): page numbers and four line numbers the option does not catch.
- **peer review:** the text layer inserts spaces inside words ("hav e", "C NT -PET"); spacing was rebuilt from
  glyph gaps (`work/scripts/pr2tex.py`), so 7 single-token MISSING runs remain where the tool sees a word split
  or joined differently ("ima ge", "pape r", "CNT-PET").

Read-through against the page images (step 4) done for: title block, Table 1 (every cell), the Methods
equations (electron dose, SE-50 nm, σ = 1/(R_s × t), Michelson contrast, C, Vm/Vb, CNR, double Gaussian),
Ω □⁻¹ units, superscript citations, λ, ±, the SI depth numbers printed in the SCM panels.

## Errors and oddities in the paper (kept verbatim)

- Table 1 vs Methods disagree on several times/temperatures (list above), and the Table 1 figure-panel
  pointers for TO look wrong ("6b–d …" for Fig. 5 panels).
- Supplementary Table 2: PE depth at 5.5 keV printed "1231" without the minus sign.
- Supplementary Fig. 1: panel d is titled "In-lens SE" but the legend calls it a BSD image.
- Supplementary Fig. 8 legend: "60 nm aperture" (elsewhere apertures are in µm).
- Supplementary Methods cite refs "47,68" and "69", which are main-text reference numbers; the SI list has only 1–9.
- Fig. 3c panel title "sET, 5 keV, 10 pixel⁻¹" lacks a unit; Fig. 4d axis title "Total light ransmittance (%)".
- Fig. 4d/4e bar tops sit slightly below the printed values (largest: CNT-PET haze drawn ≈1.8 vs "1.9").
- Fig. 3d: colour-bar labels inconsistent with the printed depths (see Figures).
- Acknowledgements: "Supplmentary Fig. 6e"; affiliation 5: "D- 873447 Oberkochen".
- Ref. 70 gives a figshare login URL instead of a data-set link; ref. 68 prints the year in the volume slot
  ("J. Appl. Phys. **2007**, 123101").
- Supplementary Table 3 calls the BSD rows "BSE".
- Supplementary Fig. 4g: y axis labelled "Electron dose (e- nm-2)" but the values (0–6) are ke⁻ nm⁻² as in 4e.
- Colour-bar labels of Fig. 3d and Suppl. Figs. 3d, 4c are not evenly spaced relative to the bar.

## Problems and suggestions for the spec/tools

- `check_text.py`: text labels printed *around* raster plots (tick labels and axis titles as PDF text just
  outside the image bbox) are not counted as in-figure text, so the main-text "running text" coverage stays at
  96 % although nothing of the article's running text is missing. Suggest growing the image bbox by ~15 pt
  when classifying in-figure text.
- `digitize_common.embedded_image()` crashes on the SI PDF: the soft masks are stored at a different
  resolution from their images (e.g. 887×331 image, 2417×900 mask). All masks here are fully opaque. Fix:
  resize the mask to the image size (or skip a fully opaque mask). Worked around in `figures/sfig_common.py`.
- `digitize_common.tick_positions*` only detect near-black ticks; the light-grey ticks of these 150 ppi JPEGs
  are missed. A threshold parameter would help.
- SPEC: no method for 3D-shaded colour maps; hue mapping works partly but cannot resolve constant-hue stretches
  of a bar. Worth a sentence in SPEC.md (and the "calibrated colour map" requirement could allow "printed
  values preferred, map qualitative" in such cases).
- `check_text.py --drop-line-numbers` misses a few line numbers (those sharing a line with text at the right
  end of a block, e.g. "87", "156"); harmless.
- `digitize_common.fit_axis` silently returns a constant map with fewer than two points (main fork hit this);
  suggest an assert. Splitting multi-number text spans ("120 160 200 240") into positioned tokens would be a
  useful helper (one exists in `figures/kubota_main_common.py`).
- A shared helper for calibrated colour maps (bar sampling, hue mapping, NaN for unsaturated pixels) would
  save time: this paper alone has six SCM depth maps.

## Time

About 2.5 h wall-clock, with two parallel helper agents for the plot digitizing (main and SI figures).
