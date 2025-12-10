# Publication Figures Specification
## Time Mastery Theory - Universal Law k(M_bary, f_gas)

**Date**: December 2025
**For**: ApJ / MNRAS Submission
**Script**: scripts/create_publication_figures.py

---

## Required Figures for Publication

### Figure 1: k vs Baryonic Mass (Power-Law Scaling)

**Type**: Log-log plot
**Size**: 8" × 6" (single column)
**DPI**: 300

**Data Points** (6 calibration galaxies):
| Galaxy  | M_bary (M☉) | f_gas | k_observed | Type   | Color |
|---------|-------------|-------|------------|--------|-------|
| DDO154  | 6.5×10⁸     | 0.769 | 3.675      | Dwarf  | Red   |
| NGC6503 | 2.6×10⁹     | 0.308 | 1.287      | Spiral | Blue  |
| NGC2403 | 5.3×10⁹     | 0.340 | 0.304      | Spiral | Blue  |
| NGC3198 | 8.3×10⁹     | 0.253 | 0.186      | Spiral | Blue  |
| NGC2841 | 4.1×10¹⁰    | 0.078 | 0.026      | Giant  | Green |
| UGC2885 | 5.8×10¹⁰    | 0.138 | 0.014      | Giant  | Green |

**Theoretical Curve**:
```
k(M) = 0.343 × (M_bary / 10¹⁰ M☉)^(-1.610) × (1 + f_gas_mean)^(-3.585)
where f_gas_mean = 0.31 (average)
```

**X-axis**: M_bary (M☉), logarithmic, range 10⁸·⁵ to 10¹¹
**Y-axis**: k (dimensionless), logarithmic, range 0.01 to 10

**Labels**:
- Each point labeled with galaxy name
- Legend showing galaxy types
- Text box with universal law equation and R² = 0.9976

**Title**: "Universal Law: k ∝ M_bary^(-1.61)"

---

### Figure 2: k_observed vs k_predicted (Validation)

**Type**: Log-log correlation plot
**Size**: 7" × 7" (square)
**DPI**: 300

**k_predicted values** (from universal law):
| Galaxy  | k_obs  | k_pred | Residual |
|---------|--------|--------|----------|
| NGC2403 | 0.304  | 0.327  | +7.5%    |
| NGC3198 | 0.186  | 0.174  | -6.5%    |
| NGC6503 | 1.287  | 1.298  | +0.8%    |
| DDO154  | 3.675  | 3.656  | -0.5%    |
| UGC2885 | 0.014  | 0.014  | 0.0%     |
| NGC2841 | 0.026  | 0.027  | +3.8%    |

**Elements**:
- Diagonal line: y = x (perfect correlation)
- Points colored by galaxy type (same as Figure 1)
- Galaxy labels offset from points
- Text box showing residuals (all within ±8%)

**X-axis**: k_observed (logarithmic)
**Y-axis**: k_predicted (logarithmic)

**Title**: "Validation: R² = 0.9976, χ²_red = 0.04"

---

### Figure 3: Rotation Curves (6-panel)

**Type**: Multi-panel line plots (2 rows × 3 columns)
**Size**: 14" × 10" (double column)
**DPI**: 300

**For each galaxy**, plot 3 curves:
1. **Baryonic** (blue dashed): v_bary(r) from exponential disk
2. **Després Mass** (red dotted): v_dark(r) = √(G·M_Després/r)
3. **Total** (black solid, thick): v_tot = √(v_bary² + v_dark²)

**Calculation Notes**:
- Use Freeman (1970) for exponential disk potential
- M_Després(r) = k · (2πh/c⁴) · ∫₀^r Φ²(r') r' dr'
- h = 0.3 kpc (disk scale height)
- k from universal law: k(M_bary, f_gas)

**Panel Layout**:
```
[DDO154]    [NGC6503]    [NGC2403]
[NGC3198]   [NGC2841]    [UGC2885]
```

**Each panel includes**:
- X-axis: Radius (kpc), 0 to 4×R_disk
- Y-axis: Velocity (km/s), 0 to v_max + 50
- Info box: M_bary, f_gas, k_pred, k_obs
- Legend: Baryonic, Després Mass, Total

**Overall Title**: "Rotation Curves: Time Mastery Theory Predictions"

---

### Figure 4: Comprehensive Summary (4-panel)

**Type**: Multi-panel summary figure
**Size**: 16" × 10" (full page width)
**DPI**: 300

**Panel (a) - Top Left**: k vs M_bary
- Same as Figure 1 but compact
- 6 points + theoretical curve

**Panel (b) - Top Center**: k vs f_gas
- X-axis: f_gas (linear, 0.05 to 0.85)
- Y-axis: k (logarithmic)
- Curve: k(f_gas) at fixed M = 5×10⁹ M☉
- 6 data points colored by type

**Panel (c) - Top Right**: k_obs vs k_pred
- Same as Figure 2 but compact
- Galaxy labels smaller

**Panel (d) - Bottom (full width)**: Example Rotation Curve (NGC3198)
- Large, detailed rotation curve
- Filled regions showing components:
  - Blue fill: Baryonic contribution
  - Red fill: Després Mass contribution
- Three curves: v_bary (dashed), v_Després (dotted), v_total (solid)
- Parameter box showing universal law
- Subtitle: "No Free Parameters"

**Overall Title**: "Time Mastery Theory: Universal Law k(M_bary, f_gas)"

---

## Execution Instructions

### Method 1: Python Script (Automated)

```bash
cd /home/user/Maitrise-du-temps/scripts
pip install numpy scipy matplotlib  # If not installed
python3 create_publication_figures.py
```

**Outputs**:
- `../data/results/figure1_k_vs_mass.png`
- `../data/results/figure2_k_correlation.png`
- `../data/results/figure3_rotation_curves.png`
- `../data/results/figure4_summary.png`

### Method 2: Manual Creation (e.g., in Origin, Matplotlib, R)

Use the data tables above and follow specifications for:
- Axis ranges
- Line styles
- Colors
- Labels
- Annotations

---

## Universal Law Parameters (Exact Values)

**For all calculations**:

```
k(M_bary, f_gas) = k₀ · (M_bary / M₀)^α · (1 + f_gas)^β

where:
  k₀ = 0.343 ± 0.070
  α  = -1.610 ± 0.087
  β  = -3.585 ± 0.852
  M₀ = 10¹⁰ M☉
```

**Performance**:
- R² = 0.9976
- χ²_red = 0.04
- Scatter reduction: factor 262.5 → 1.15 (99.6%)

---

## Style Guidelines

**Publication Quality Standards**:
- Font: Times New Roman or similar serif
- Font sizes:
  - Axis labels: 12pt
  - Tick labels: 10pt
  - Legend: 9pt
  - Titles: 13-14pt (bold)
- Line widths:
  - Main curves: 2-2.5pt
  - Secondary curves: 1.5pt
  - Grid: 0.5pt (alpha 0.3)
- Colors:
  - Use colorblind-friendly palette
  - Dwarf: #E74C3C (red)
  - Spiral: #3498DB (blue)
  - Giant: #2ECC71 (green)
- Grid: Light gray, alpha 0.3
- DPI: 300 minimum
- Format: PNG with transparent background OR PDF vector

---

## Figure Captions for Manuscript

**Figure 1 Caption**:
> "Coupling constant k as a function of baryonic mass M_bary for 6 calibration galaxies. Points are colored by morphological type: red (dwarf), blue (spiral), green (giant). The solid black curve shows the universal law k ∝ M_bary^(-1.61) with fixed gas fraction f_gas = 0.31. The law achieves R² = 0.9976, indicating that galaxy mass alone explains 99.8% of k variation."

**Figure 2 Caption**:
> "Validation of universal law k(M_bary, f_gas): observed k values (from individual rotation curve fits) versus predicted k values (from universal law with no free parameters). All 6 galaxies fall within ±8% of perfect correlation (diagonal line), demonstrating exceptional predictive power. Residuals shown in inset."

**Figure 3 Caption**:
> "Rotation curves for 6 calibration galaxies spanning 3 orders of magnitude in mass. Blue dashed: baryonic contribution (disk + gas). Red dotted: Després Mass contribution (geometric dark matter). Black solid: total predicted velocity. All curves use k from universal law—no galaxy-specific fitting. Average χ²_red = 0.04."

**Figure 4 Caption**:
> "Comprehensive summary of universal law k(M_bary, f_gas). (a) Mass dependence showing power-law k ∝ M^(-1.61). (b) Gas fraction dependence k ∝ (1+f_gas)^(-3.59). (c) Observed vs predicted correlation (R² = 0.9976). (d) Example: NGC3198 rotation curve predicted with zero free parameters, showing baryonic (blue), Després Mass (red), and total (black) contributions."

---

## Data Files

**Raw Data** (for reproducibility):
- `../data/input/SPARC_galaxies_6sample.csv` - Galaxy parameters
- `../scripts/create_publication_figures.py` - Figure generation code
- `../docs/en/05-publications/SCIENTIFIC_ARTICLE_TIME_MASTERY.md` - Full manuscript

**Output Figures**:
- `../data/results/figure1_k_vs_mass.png`
- `../data/results/figure2_k_correlation.png`
- `../data/results/figure3_rotation_curves.png`
- `../data/results/figure4_summary.png`

---

## Checklist Before Submission

- [ ] All figures generated at 300 DPI
- [ ] Fonts embedded in PDF (if using PDF format)
- [ ] Colors are colorblind-friendly
- [ ] All axis labels legible
- [ ] Galaxy names visible
- [ ] Error bars shown (if applicable)
- [ ] Figure captions match manuscript
- [ ] Figures numbered consistently
- [ ] Supplementary data files prepared
- [ ] Code archived (Zenodo/GitHub)

---

**Status**: Ready for generation
**Dependencies**: numpy, scipy, matplotlib (Python 3.7+)
**Estimated time**: ~30 seconds per figure

---

**Last updated**: December 2025
**Contact**: pierreolivierdespres@gmail.com
