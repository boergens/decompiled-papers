"""Write tables/table1..5.csv (transcribed by hand from the page images of source/wei2024.pdf)."""
import csv
from pathlib import Path
out = Path(__file__).resolve().parent.parent / "tables"
out.mkdir(exist_ok=True)

def w(name, comments, header, rows):
    with open(out / name, "w", newline="", encoding="utf-8") as f:
        for c in comments:
            f.write("# " + c + "\n")
        cw = csv.writer(f)
        cw.writerow(header)
        cw.writerows(rows)

t1 = """c3 0.054 4.01 0.056 3.479 0.7 4.05 1.4∼4.05 3.3
hc 0.02 2.995 0.020 2.589 0.25 2.45 0.5∼2.45 2.4
c 0.054 4.01 0.056 3.479 0.7 5.65 1.4∼4.05 3.3
cp 0.064 4.01 0.066 3.479 0.7 6.05 1.4∼6.05 3.3
oc 0.24 3.535 0.246 3.065 0.6 4.85 1.2∼4.85 2.9
c2 0.054 4.01 0.056 3.479 0.7 4.35 1.4∼4.05 3.3
c1 0.054 4.01 0.056 3.479 0.7 4.45 1.4∼4.05 3.3
oh 0.24 3.535 0.246 3.065 0.6 2.85 1.2∼4.85 2.9
c3h 0.054 4.01 0.056 3.479 0.7 3.75 1.4∼4.05 3.3
o3e 0.24 3.535 0.246 3.065 0.6 4.35 1.2∼4.85 2.9
ho 0.013 1.098 0.013 0.949 0.25 2.35 0.5∼2.35 0.9
nb 0.065 4.07 0.065 3.524 0.65 3.55 1.3∼3.55 3.3
hn 0.013 1.098 0.013 0.949 0.25 2.45 0.5∼2.35 0.9"""
rows = []
for line in t1.splitlines():
    p = line.split()
    lo, hi = p[7].split("∼")
    rows.append(p[:7] + [lo, hi, p[8]])
w("table1.csv",
  ["Table 1 (p. 5 of source/wei2024.pdf): Based on the 9–6 LJ potential parameters of each atom in epoxy system, its 12–6 LJ potential parameters were obtained through the fitting method",
   "Columns: atom type of epoxy resin; 9–6 LJ potential ε (kcal/mol) and σ (Å); 12–6 LJ potential ε (kcal/mol) and σ (Å); atomic radius (Å);",
   "the position of the first peak of RDF (Å); the range of starting point positions for fitting (Å), printed as 'lo ∼ hi', split into two columns here;",
   "the position of the final selected fitting starting point (Å). Values verbatim (e.g. rows c, c2, c1, c3h print a range ending at 4.05 although their RDF peak differs)."],
  ["atom_type", "eps_96_kcal_per_mol", "sigma_96_A", "eps_126_kcal_per_mol", "sigma_126_A", "atomic_radius_A", "first_RDF_peak_A",
   "fit_start_range_low_A", "fit_start_range_high_A", "final_fit_start_A"], rows)

t2 = [("Epoxy", "Carbon in the methyl group", "c3", "0.056", "3.479"),
      ("Epoxy", "Hydrogen, bonded to carbon", "hc", "0.02", "2.589"),
      ("Epoxy", "Generic carbon", "c", "0.056", "3.479"),
      ("Epoxy", "Aromatic carbon", "cp", "0.066", "3.479"),
      ("Epoxy", "Oxygen in ether", "oc", "0.246", "3.065"),
      ("Epoxy", "Carbon bonded to 2 H’s", "c2", "0.056", "3.479"),
      ("Epoxy", "Carbon bonded to 1 H", "c1", "0.056", "3.479"),
      ("Epoxy", "Hydroxyl oxygen", "oh", "0.246", "3.065"),
      ("Epoxy", "Carbon in 3-membered ring with hydrogens", "c3h", "0.056", "3.479"),
      ("Epoxy", "Oxygen in 3-membered ring", "o3e", "0.246", "3.065"),
      ("Epoxy", "Hydroxyl hydrogen", "ho", "0.013", "0.949"),
      ("Epoxy", "Nitrogen in aromatic amines", "nb", "0.065", "3.524"),
      ("Epoxy", "Hydrogen bonded to nitrogen", "hn", "0.013", "0.949"),
      ("Quartz", "Silicon in silicate", "sz", "0.040", "4.053"),
      ("Quartz", "Hydroxyl oxygen", "oh", "0.228", "2.860"),
      ("Quartz", "Hydroxyl hydrogen", "ho", "0.000", "0.000"),
      ("Quartz", "Oxygen", "oz", "0.228", "2.860")]
w("table2.csv",
  ["Table 2 (p. 7 of source/wei2024.pdf): Epoxy-quartz pair interactions potential parameters",
   "Columns: model; atom species; symbol; ε (kcal/mol); σ (Å) -- lj/cut (12–6 LJ potential). Values verbatim."],
  ["model", "atom_species", "symbol", "eps_kcal_per_mol", "sigma_A"], t2)

t3 = [("MD simulations", "Epoxy resin (containing 2000 DGEBA + 1000 mPDA) with a conversion percentage of 84% through uniaxial tension using MD simulation in this work", "2.203", "1.906", "2.105", "2.075", "2.419", ""),
      ("MD simulations", "Epoxy resin (containing 200 DGEBA + 100 mPDA) with a conversion percentage of 86% through uniaxial tension using MD simulation [46]", "", "", "", "", "", "2.61 ± 0.28"),
      ("MD simulations", "Epoxy resin composed of EPON862 and curing agent DETDA with conversion degrees of 0% ∼ 86% using MD simulation [21]", "", "", "", "", "", "1.0 ∼ 3.0"),
      ("MD simulations", "Epoxy resin (containing EPON862 + DETDA) [39]", "", "", "", "", "", "2.56 (experimental), 1.61 (MD simulation)"),
      ("Various experiments in previous works", "DGEBA epoxy networks (containing DGEBA/D230, DGEBA/TETA, DGEBA/TEPA) through dynamic mechanical analyses experiments [3]", "", "", "", "", "", "2.21 ∼ 2.72"),
      ("Various experiments in previous works", "A DGEBA-based epoxy resin through tensile test [51]", "", "", "", "", "", "3.5 (unmodified epoxy resin), 3.85 (epoxy + 8.5% nanofiller)"),
      ("Various experiments in previous works", "Matrix epoxy Epon 862 [25]", "", "", "", "", "", "2.83"),
      ("Various experiments in previous works", "Epoxy resin composite by ultrasonic velocity Measurement [27]", "", "", "", "", "", "3.441 ∼ 4.601 (DGEBA/AGE), 3.441 ∼ 6.293 (DGEBA/GMA)"),
      ("Various experiments in previous works", "Epoxy resin through uniaxial tension and nanoindentation test [40]", "", "", "", "", "", "3.3 ± 0.12 (uniaxial tension), 3.9 ± 0.12 (nanoindentation test)"),
      ("Various experiments in previous works", "Epoxy resin with 0.78 wt% Polyaniline added by 0 ∼ 1.0 wt% ZnO nanoparticles using nanoindentation test [31]", "", "", "", "", "", "3.76 (0 wt%), 3.49 (0.5 wt%), 3.47 (1.0 wt%)"),
      ("Various experiments in previous works", "Epoxy composite with 0 ∼ 5% CNF using nanoindentation test [32]", "", "", "", "", "", "4.0 ∼ 7.1"),
      ("Various experiments in previous works", "Er of epoxy resin at different loading rates of 0.25 ∼ 6.0 mN/s using nanoindentation test [14]", "", "", "", "", "", "4.78 ∼ 5.35"),
      ("Various experiments in previous works", "Er of nanoclay/epoxy composite at 40 °C [20]", "", "", "", "", "", "1.5 ∼ 7.5")]
w("table3.csv",
  ["Table 3 (p. 9 of source/wei2024.pdf): Young’s modulus of epoxy resin in this work and similar materials in previous studies at room temperature",
   "Columns: method group; Young’s modulus of epoxy (GPa) row description; Ex, Ey, Ez, overall (Ē), reduced modulus Er (GPa) for this work;",
   "value_text: the value printed across the numeric columns for the other rows, verbatim.",
   "Footnote: The overall Young’s modulus (Ē) is the square average value of Young’s modulus along three directions (i.e., Ex, Ey, Ez). The reduced modulus Er was calculated through Eq. (10)",
   "Footnote: DGEBA Diglycidyl Ether of Bisphenol A, mPDA m-phenylenediamine, DETDA Diethyltoluenediamine, EPON862 Bisphenol F diglycidyl ether, TETA triethylenetetramine, TEPA tetraethylenepentamine, D230 Jeffamine D230, AGE Allyl glycidyl ether, GMA glycidyl methacrylate, CNF carbon nanofiber"],
  ["methods", "description", "Ex_GPa", "Ey_GPa", "Ez_GPa", "E_overall_GPa", "Er_GPa", "value_text"], t3)

t4 = [("Uniaxial tension using MD simulation in this work", "0.351", "0.407", "0.338", "0.420", "0.368", "0.378", "0.377", ""),
      ("Epoxy resin composed of EPON862 and curing agent DETDA (conversion degrees of 0% ∼ 86%) [21]", "", "", "", "", "", "", "", "0.27 ∼ 0.475"),
      ("Epoxy resin (containing EPON862 + DETDA) [39]", "", "", "", "", "", "", "", "0.353 (experimental), 0.448 (MD simulation)"),
      ("Matrix epoxy Epon 862 [25]", "", "", "", "", "", "", "", "0.3"),
      ("Epoxy resin composite by ultrasonic velocity Measurement [27]", "", "", "", "", "", "", "", "0.3461 ∼ 0.3911 (DGEBA/AGE), 0.341 ∼ 0.346 (DGEBA/GMA)"),
      ("Araldite LY5052 epoxy resin by uniaxial relaxation tests [33]", "", "", "", "", "", "", "", "0.32 ∼ 0.44")]
w("table4.csv",
  ["Table 4 (p. 10 of source/wei2024.pdf): Poisson’s ratio of epoxy resin in this work and similar materials in previous studies at room temperature",
   "Columns: Poisson’s ratio of epoxy (row description); v_xy, v_xz, v_yx, v_yz, v_zx, v_zy and the average v̄ for this work; value_text: value printed across the columns for other rows.",
   "Footnote: The average Poisson’s ratio (v̄) is the geometric average value of the six components of the matrix"],
  ["description", "v_xy", "v_xz", "v_yx", "v_yz", "v_zx", "v_zy", "v_mean", "value_text"], t4)

t5 = [("MD nanoindentation simulation in this work, where nanoindenter is rigid quartz", "", "0.25", "9.757", "1.492"),
      ("MD nanoindentation simulation in this work, where nanoindenter is rigid quartz", "", "0.5", "10.594", "1.620"),
      ("MD nanoindentation simulation in this work, where nanoindenter is rigid quartz", "", "0.75", "13.052", "1.997"),
      ("MD nanoindentation simulation in this work, where nanoindenter is rigid quartz", "", "1.0", "13.115", "2.006"),
      ("MD nanoindentation simulation in this work, where nanoindenter is rigid quartz", "", "1.5", "14.813", "2.266"),
      ("MD nanoindentation simulation in this work, where nanoindenter is rigid quartz", "", "2.0", "14.215", "2.174"),
      ("Nanoindentation experiments in previous works, where nanoindenter is usually diamond", "Epoxy-reinforced nanocomposites with fumed silica of 0 ∼ 3% [40]", "", "", "0.256 ∼ 0.318"),
      ("Nanoindentation experiments in previous works, where nanoindenter is usually diamond", "RTM6 Epoxy resin with strain rate of 0.01 ∼ 0.25 and 25 °C [12]", "", "", "0.23 ∼ 0.35"),
      ("Nanoindentation experiments in previous works, where nanoindenter is usually diamond", "SWNT of 0% ∼ 1.0% reinforced epoxy composites [9]", "", "", "0.23 ∼ 0.31"),
      ("Nanoindentation experiments in previous works, where nanoindenter is usually diamond", "Epoxy resin at different loading rate of 0.25 ∼ 6.0 mN/s [14]", "", "", "0.26 ∼ 0.276"),
      ("Nanoindentation experiments in previous works, where nanoindenter is usually diamond", "Epoxy resin with 0.78 wt% Polyaniline added by 0 ∼ 1.0 wt% ZnO nanoparticles [31]", "", "", "0.18 (0 wt%) ∼ 0.206 (1.0 wt%)"),
      ("Nanoindentation experiments in previous works, where nanoindenter is usually diamond", "Epoxy composite with 0 ∼ 5% CNF [32]", "", "", "0.26 ∼ 0.67")]
w("table5.csv",
  ["Table 5 (p. 14 of source/wei2024.pdf): The indentation hardness (H) of the epoxy resin obtained by Eq. (9) in MD nanoindentation simulation at different loading rates and in previous experimental works",
   "Columns: methods; conditions and other notes (text); loading rate (Å/ps); Pmax (nN); H (GPa), verbatim (ranges as printed).",
   "Footnote: RTM resin transfer molding, SWNT single-walled carbon nanotube, CNF: carbon nanofiber"],
  ["methods", "conditions", "loading_rate_A_per_ps", "Pmax_nN", "H_GPa"], t5)
print("ok")
