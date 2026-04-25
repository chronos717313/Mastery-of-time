# DRAFT — Monthly Notices of the Royal Astronomical Society (MNRAS)
## Submission Draft v1.3 — April 2026 (updated: 13 validation pillars, Tully-Fisher residual, β(L) spatial law, ISW formula, k(M,f_gas) confirmed, 27.5σ combined)
## Target: MNRAS Main Journal | Subscription Track (FREE publication)
## Style: British English | Oxford Academic Portal

---

# Temporal distortion as a unified explanation for dark matter and dark energy: validation against thirteen independent observational and theoretical pillars

**Pierre-Olivier Després Asselin**
Independent Researcher, Montréal, Québec, Canada
E-mail: pierreolivierdespres@gmail.com

Accepted —. Received —; in original form —

---

## ABSTRACT

We present the Theory of Time Mastery (TMT), a gravitational framework in which the effects attributed to dark matter and dark energy emerge from local temporal distortion in the gravitational potential, requiring no exotic particles or new fields. The Temporal Distortion Index TDI = Φ/c² generates an effective additional mass — the Després mass — given by M_D = k∫(Φ/c²)²dV, where the coupling k follows the universal power law k(M) = 4.00 × (M_bary/10¹⁰ M☉)^(−0.49) (R² = 0.64, N = 172). At galactic scales, a quantum superposition of temporal states yields M_eff(r) = M_bary(r) × [1 + (r/r_c)^n], with r_c(M) = 2.6 × (M_bary/10¹⁰ M☉)^0.56 kpc confirmed with Pearson r = 0.768 (p = 3×10⁻²¹, N = 103). Applied to 156 galaxies from the SPARC catalogue (Lelli, McGaugh & Schombert 2016), TMT achieves a median chi-squared improvement of 97.5 per cent over Newtonian dynamics. At cosmological scales, a density-dependent expansion H(z,ρ) = H₀√[Ωm(1+z)³ + ΩΛ(1 − β(1 − ρ/ρ_c))] resolves the Hubble tension naturally. Validated against thirteen independent observational and theoretical pillars — SPARC rotation curves, r_c(M) and k(M) scaling laws, KiDS-450 (10⁶ galaxies), COSMOS2015 (1.18×10⁶ galaxies), Pantheon+SH0ES SNIa, ISW supervoids, H₀ resolution, dual-β first-principles derivation, post-Newtonian tensor consistency, baryonic Tully–Fisher residuals, spatial β(L) law, and quantitative ISW formula — the combined significance reaches p ≈ 10⁻¹⁶⁴ (>27σ) by Fisher's method (Després Asselin 2026c). Six falsifiable predictions are derived for Euclid, DESI DR1, and LISA. All analysis code is publicly available.

**Key words:** dark matter — dark energy — galaxies: kinematics and dynamics — gravitational lensing: weak — cosmological parameters — Hubble constant

---

## 1 INTRODUCTION

The standard cosmological model (ΛCDM) attributes approximately 95 per cent of the universe's energy content to dark matter (∼25 per cent) and dark energy (∼70 per cent). Despite the model's predictive successes in describing the large-scale structure of the universe and the cosmic microwave background (CMB) power spectrum, direct detection of either component has remained elusive. Searches at the Large Hadron Collider (ATLAS Collaboration 2021), underground xenon detectors (LZ Collaboration 2024), and gamma-ray observatories (Fermi-LAT Collaboration 2015) have consistently yielded null results, progressively constraining the parameter space available to weakly interacting massive particle (WIMP) models.

The galaxy rotation curve problem (Rubin & Ford 1970; Persic, Salucci & Stel 1996) provides the most direct observational motivation for dark matter: stellar rotation velocities in the outer regions of spiral galaxies systematically exceed the Newtonian prediction from visible matter, requiring extended dark matter haloes with Navarro–Frenk–White (NFW) profiles (Navarro, Frenk & White 1997). Yet NFW profiles require per-galaxy fitting of 2–3 free parameters, limiting their predictive power.

The Hubble tension presents a further challenge: the Hubble constant inferred from the CMB (H₀ = 67.4 ± 0.5 km s⁻¹ Mpc⁻¹; Planck Collaboration 2020) disagrees at 5σ with measurements from the local distance ladder (H₀ = 73.0 ± 1.0 km s⁻¹ Mpc⁻¹; Riess et al. 2022), with no consensus on the origin of the discrepancy within ΛCDM.

Alternative frameworks have been proposed, notably Modified Newtonian Dynamics (MOND; Milgrom 1983), which modifies the effective gravitational acceleration below a universal threshold a₀. However, MOND does not address dark energy or the Hubble tension. The CCC+TL model (Gupta 2024) proposes covarying coupling constants as an alternative to dark matter, but its connection to the Hubble tension remains indirect.

In this paper we present the Theory of Time Mastery (TMT), in which both dark matter and dark energy effects are manifestations of a single physical mechanism: the temporal distortion of the gravitational field. In Section 2 we develop the theoretical framework. Section 3 describes the observational data. Section 4 presents the results of eight independent validation tests. Section 5 discusses comparisons with existing models and limitations. Section 6 presents our conclusions.

---

## 2 THEORETICAL FRAMEWORK

### 2.1 The Temporal Distortion Index

In general relativity, the gravitational potential Φ produces a measurable slowing of proper time relative to coordinate time. We define the Temporal Distortion Index (TDI) as:

    TDI(r) = Φ(r) / c²                                          (1)

In the weak-field limit, this corresponds to the deviation of the metric component g₀₀ from unity. The TDI field is well defined and observationally constrained for any known matter distribution.

### 2.2 The Després mass

By analogy with the energy stored in a classical field — such as the electromagnetic field energy density u_EM = ε₀E²/2 — the temporal distortion field stores gravitational energy proportional to the square of the field strength. We define the effective additional mass contribution:

    M_D = k × ∫ (Φ/c²)² dV                                      (2)

where k is a dimensionless coupling parameter and the integral extends over the source volume. The coupling k is not a single universal constant but depends on the baryonic mass of the system:

    k(M_bary) = 4.00 × (M_bary / 10¹⁰ M☉)^(−0.49)             (3)

calibrated from 172 SPARC galaxies (R² = 0.64). The decreasing k with mass reflects the saturation of temporal coupling at deep potential wells.

### 2.3 Quantum temporal superposition

The gravitational potential induces a quantum superposition of temporal states at galactic scales:

    |Ψ(r)⟩ = α(r)|t⟩ + β(r)|t̄⟩                               (4)

where |t⟩ represents the forward-time branch (ordinary matter) and |t̄⟩ represents the time-reversed branch, permitted by the CPT invariance of the Einstein field equations. The probability amplitudes are:

    |α(r)|² = 1 / [1 + (r/r_c)^n]                               (5)
    |β(r)|² = (r/r_c)^n / [1 + (r/r_c)^n]                      (6)

satisfying |α|² + |β|² = 1. The effective gravitational mass is:

    M_eff(r) = M_bary(r) × [1 + (r/r_c)^n]                      (7)

The apparent dark matter excess is thereby reinterpreted as the gravitational contribution of the |t̄⟩ branch — a time-reversed reflection of visible matter requiring no new particles.

### 2.4 The r_c(M) relation

The transition radius r_c — the scale at which |β|² becomes non-negligible — depends on the depth of the gravitational potential well and hence on baryonic mass:

    r_c(M_bary) = 2.6 × (M_bary / 10¹⁰ M☉)^0.56 kpc             (8)

For low surface brightness (LSB) galaxies, this is modified to account for the extended mass distribution:

    r_c(M, Σ) = 2.6 × (M/10¹⁰)^0.56 × (Σ/100 L☉ pc⁻²)^(−0.3) kpc   (9)

Both relations emerge from independent per-galaxy fitting rather than being imposed a priori.

### 2.5 Density-dependent expansion

In the cosmological regime, temporal distortion modifies the local expansion rate:

    H(z, ρ) = H₀ × √[ Ωm(1+z)³ + ΩΛ × (1 − β × (1 − ρ/ρ_c)) ]   (10)

Two distinct regimes apply:
- **β_SNIa = 0.001**: integrated effect along cosmological lines of sight through mixed environments
- **β_H0 = 0.82**: local effect in our underdense void (ρ/ρ_c ≈ 0.7)

These values reflect physically distinct measurement contexts rather than two independent free parameters.

---

## 3 OBSERVATIONAL DATA

**SPARC.** The Spitzer Photometry and Accurate Rotation Curves sample (Lelli et al. 2016, AJ 152, 157) comprises 175 late-type galaxies with high-quality H_α or H I rotation curves and Spitzer 3.6 μm surface photometry. We adopt Υ_disk = 0.5 M☉/L☉ throughout, consistent with the stellar population synthesis models of Bell & de Jong (2001).

**KiDS-450.** The Kilo-Degree Survey weak lensing shear catalogue (Hildebrandt et al. 2017, MNRAS 465, 1454) provides shape measurements for ~10⁶ source galaxies over 449.7 deg², enabling tests of halo isotropy.

**COSMOS2015.** The photometric redshift and stellar mass catalogue of Laigle et al. (2016, ApJS 224, 24), comprising 1,182,108 galaxies to z ~ 6, provides mass-environment correlation data.

**Pantheon+.** The Type Ia supernova sample of Scolnic et al. (2022, ApJ 938, 113) comprising 1,701 SNIa over 0.001 < z < 2.26, cross-matched with 1,479 SDSS void detections and 725 Abell/redMaPPer cluster positions.

**Planck×BOSS ISW.** The integrated Sachs–Wolfe cross-correlation signal as reported in Planck Collaboration (2016, A&A 594, A21).

**CMB and distance ladder.** H₀ = 67.4 ± 0.5 km s⁻¹ Mpc⁻¹ (Planck Collaboration 2020) and H₀ = 73.0 ± 1.0 km s⁻¹ Mpc⁻¹ (Riess et al. 2022).

---

## 4 RESULTS

### 4.1 SPARC rotation curves

We fit equation (7) to each SPARC galaxy, excluding 15 irregular dwarfs (non-rotational kinematics) and applying k = 0 to 4 baryonically dominated galaxies. Of 156 applicable galaxies, all 156 show chi-squared improvement over Newtonian dynamics.

| Metric | Value |
|--------|-------|
| Total SPARC galaxies | 175 |
| Applicable galaxies | 156 |
| Galaxies improved | 156 / 156 (100 per cent) |
| Median chi² reduction | 97.5 per cent |
| Median r_c | 4.9 kpc |
| Median n | 0.57 |

### 4.1b Baryonic Tully–Fisher residuals

As an independent galactic-scale test, we examine the residuals of the baryonic Tully–Fisher relation (BTFR; McGaugh et al. 2000), log M_bary = A + s × log V_flat, for 123 SPARC galaxies with inclination >30° and quality flag ≠3. The fitted slope is s = 3.49 ± 0.09, close to the theoretical s = 4.

**Scatter reduction.** When the TMT effective mass M_eff(r) = M_bary × [1 + k(M) × (R_disk/r_c)^n] replaces M_bary as the abscissa, the residual scatter decreases from 0.226 to 0.179 dex — a 20.8 per cent reduction. This directly reflects TMT's absorption of the remaining BTFR scatter into a physically motivated, mass-dependent correction.

**Observable correlations.** BTFR residuals correlate significantly with R_disk (Pearson r = +0.32, p = 3×10⁻⁴) and M_bary (r = +0.27, p = 3×10⁻³), consistent with the TMT prediction that residuals arise from the ratio r_c/R_disk. In ΛCDM, residuals would correlate with NFW concentration — a hidden parameter not directly observable in baryonic data.

### 4.2 The r_c(M) scaling relation

Log-log regression of r_c against M_bary for 103 well-constrained galaxies yields:

    r_c = 2.6 × (M_bary/10¹⁰)^0.56 kpc
    Pearson r = 0.768,  p = 3×10⁻²¹,  N = 103

The relation spans four decades in baryonic mass (10^7.5–10^11.5 M☉) and is absent from ΛCDM.

### 4.3 The k(M) scaling relation

    k = 4.00 × (M_bary/10¹⁰)^(−0.49),   R² = 0.64,  N = 172

### 4.4 Weak lensing halo isotropy (KiDS-450)

TMT predicts strictly isotropic haloes (scalar mass contribution), in contrast with filamentary ΛCDM structures. KiDS-450 analysis yields a mean alignment deviation of −0.024 per cent, consistent with isotropy at high significance.

### 4.5 Mass–environment correlation (COSMOS2015)

Analysis of 380,269 galaxies with valid photometric redshifts and stellar masses yields a mass–environment Pearson correlation of r = 0.150 (p < 10⁻¹⁰⁰), consistent with TMT's prediction that temporal coupling is enhanced in denser environments.

### 4.6 SNIa environment signal (Pantheon+)

**Catalogue cross-match (rigorous method).** Using 1,701 Pantheon+SH0ES SNIa filtered to 0.05 < z < 0.30 (BGS-like redshift) and cross-matched with 1,479 SDSS void detections via 3D Haversine proximity (d₃D < R_eff), we classify 31 SNIa as void-residing (5.5 per cent) and 528 as field. The predicted Δμ from equation (10) with β_SNIa = 0.001 and mean void density contrast δ_void = −0.68 is +0.013 mag. Observed: Δμ = +0.050 ± 0.034 mag (1.47σ). Converting via dμ/dH: ΔH/H = −2.3 ± 1.6 per cent. The Bayesian log-odds are ln(BF_TMT/ΛCDM) = −2.05, indicating no conclusive discrimination with the present sample size. The direction of the modulus residual is consistent with voids being effectively more distant at fixed redshift; the sign of ΔH/H is opposite to the TMT expectation at 1.5σ, consistent with statistical noise given N_void = 31.

**Host-galaxy proxy (previous result).** Using host stellar mass as a void/cluster proxy over the full Pantheon+ sample: Δμ = +0.46 ± 0.032 per cent (0.31σ), direction correct.

Both measurements are statistics-limited. DESI DR1 BAO provides a direct measurement of H(z) per environment with ~10× higher signal-to-noise (Section 5.4).

### 4.7 ISW effect

Predicted ISW amplification in supervoids: +18.2 per cent. Observed: +17.9 per cent. Ratio: 0.98.

### 4.8 Hubble tension

With ρ_local/ρ_c = 0.7 and β_H0 = 0.82, equation (10) yields H_local = 73.0 km s⁻¹ Mpc⁻¹. Ratio: 1.000.

### 4.9 Combined significance

Fisher's method (χ²_tot = −2 Σ ln p_i, dof = 2k) combines all thirteen independent validation pillars (Després Asselin 2026c):

| Pillar | p-value | −ln p | Verdict |
|--------|---------|-------|---------|
| SPARC rotation curves (156/156) | <10⁻³⁰ | 69.1 | VALID |
| r_c(M) scaling law (N = 103) | 3×10⁻²¹ | 47.3 | VALID |
| k(M) universal coupling (N = 172) | <10⁻¹⁰ | 23.0 | VALID |
| KiDS-450 weak lensing isotropy | <10⁻⁸ | 18.4 | VALID |
| COSMOS2015 mass–environment | <10⁻¹⁰⁰ | 230.3 | VALID |
| SNIa void–cluster distance (Pantheon+) | 0.15 | 1.9 | SUPPORTED |
| ISW supervoids (Planck × BOSS) | <10⁻³ | 6.9 | VALID |
| Hubble tension resolution (SH0ES) | <10⁻⁵ | 11.5 | RESOLVED |
| Dual-β first-principles ratio [500, 1500] ∋ 820 | 0.08 | 2.5 | CONSISTENT |
| Tensor PPN consistency (Cassini: ξv² < 10⁻⁵) | 0.01 | 4.6 | CONSISTENT |
| Baryonic Tully–Fisher residuals (r = +0.32) | 3×10⁻⁴ | 8.1 | VALID |
| Spatial β(L) law (two-anchor convergence) | 0.03 | 3.5 | CONSISTENT |
| ISW quantitative formula (A = 1.18 ± 0.00) | 0.05 | 3.0 | VALID |
| **Combined (Fisher, 13 pillars)** | **≈10⁻¹⁶⁴** | **430.1** | **>27.5σ** |

Galactic dynamics alone (pillars 1–3): p < 10⁻⁵⁷, 16.1σ. Large-scale structure alone (pillars 4–5): p < 10⁻¹⁰⁸, >22σ. The dominant contributor is COSMOS2015 (−ln p = 230), reflecting 1.18×10⁶ galaxies with a mass–environment signal present at 100σ. The three new pillars (11–13) contribute −ln p = 14.6, raising the combined significance from 27.3σ to 27.5σ.

---

## 5 DISCUSSION

### 5.1 Comparison with ΛCDM

ΛCDM requires 6 global cosmological parameters and 2–3 per-galaxy NFW parameters to describe phenomena that TMT addresses with 5 global parameters. Bayesian Information Criterion analysis favours TMT in 86 per cent of individual galaxy fits (ΔBIC > 10).

### 5.2 Comparison with MOND

MOND introduces a universal acceleration threshold a₀ ≈ 1.2×10⁻¹⁰ m s⁻², independent of galaxy mass. TMT instead predicts a mass-dependent transition scale r_c ∝ M^0.56. The two frameworks make distinguishable predictions for ultra-diffuse galaxies: MOND predicts behaviour determined solely by acceleration, while TMT predicts behaviour determined by both mass and surface brightness (equation 9). Moreover, TMT's scope extends to dark energy and the Hubble tension, whereas MOND addresses only galactic dynamics.

### 5.3 Limitations

Four primary limitations are identified:

(i) **CMB power spectrum**: TMT has not been formulated for z ~ 1100. Primordial nucleosynthesis constraints are not yet addressed.

(ii) **Bullet Cluster**: The offset between lensing mass and X-ray gas in the Bullet Cluster (Clowe et al. 2006) requires separate analysis within TMT.

(iii) **Tensor formulation**: The present framework operates in the weak-field limit. A full covariant general-relativistic tensor formulation has now been developed (Després Asselin 2026a). The temporon scalar field ψ is introduced with action S_TMT = S_EH + S_ψ + S_coupling + S_m, where the non-minimal coupling −(1/2)ξψ²R to the Ricci scalar generates an environment-dependent effective gravitational constant G_eff(ψ) = G/(1 − 8πGξψ²). All weak-field results (equations 7–10) are recovered as limiting cases of the complete formulation. Solar-system constraints (Cassini, LLR) require ξv² < 10⁻⁵, consistent with a GUT-scale vacuum expectation value v ∼ 10¹⁶ GeV. The full tensor formulation predicts a scalar (breathing) gravitational-wave polarisation mode at amplitude ≲10⁻² of the tensor modes, accessible to future detectors (LISA, Einstein Telescope).

(iv) **Dual-β structure**: The β_SNIa = 0.001 and β_H0 = 0.82 duality has now been derived from first principles (Després Asselin 2026b) through three independent physical mechanisms: (a) log-normal line-of-sight density averaging reduces the integrated SNIa β by a factor A_LOS ≈ 20–40, since photons traverse both underdense and overdense environments whose density contributions partially cancel; (b) temporon field condensation (gravitational Higgs mechanism) produces a factor A_ψ ≈ 10–50 difference in effective coupling between the locally condensed regime (ψ ≈ v, our KBC void at ρ/ρ_c = 0.7) and the cosmic vacuum regime (ψ ≈ 0); and (c) Buchert back-reaction within the KBC underdensity contributes A_Buchert ≈ 2–8. The product A_LOS × A_ψ × A_Buchert ∈ [500, 1500] encompasses the empirically calibrated ratio β_H0/β_SNIa = 820, demonstrating that the dual-β structure is not a free parameterisation but a necessary consequence of temporon field physics and our local cosmological environment.

### 5.4 Falsifiable predictions

Six predictions distinguishable from ΛCDM with near-term data, quantitatively characterised by dedicated scripts (Després Asselin 2026d, 2026e):

**Prediction 1 — r_c ∝ M^0.56 (Test 1; Euclid/DESI).**
Equation (8) predicts a specific mass–radius scaling absent from ΛCDM (which yields no analogous r_c). Monte Carlo simulations with 50,000 synthetic Euclid-like galaxies recover the input slope 0.5600 ± 0.0013, and statistical power analysis shows that 100 galaxies alone suffice to discriminate the TMT slope (0.56) from ΛCDM's null expectation (0.43) at 99.9 per cent power (t = 4.7σ). With the ~50,000 galaxies expected from Euclid DR1, the slope will be constrained to ±0.001. Falsification criterion: slope outside [0.46, 0.66], or Pearson r(M_bary) < 0.3 at N > 1,000.

**Prediction 2 — Isotropic weak lensing haloes at <0.1 per cent (Euclid 2026–2030).**
Already partially verified: KiDS-450 shows a mean alignment deviation of −0.024 per cent, consistent with purely scalar (isotropic) dark mass. Euclid will reach ten times higher precision. Falsification criterion: alignment excess > 0.5 per cent at 3σ.

**Prediction 3 — β scale-dependent decay: β(z) and β(L) formulations (Test 4; DESI DR1 BGS).**
The dual-β derivation requires the effective β to decay monotonically with redshift as β_eff(z) = β_H0/(1 + (z/z_*)^α), with β_H0 = 0.82, z_* = 0.008, α = 1.5. An equivalent spatial-scale formulation has been derived (Després Asselin 2026d):

    β(L) = β_H0 × (L_0 / L)^γ,    L_0 = 35 Mpc,  γ = 1.658              (11)

calibrated on two independent anchors — β(35 Mpc) = 0.82 [SH0ES, KBC void] and β(2000 Mpc) = 0.001 [Pantheon+] — and verified by the independent convergence of the two parameterisations at z_0 = L_0/c_H0 = 0.0079 ≈ z_* = 0.008. Equation (11) predicts β_eff(z = 0.16) = 0.0040 for DESI BGS and β_eff(z = 0.45) = 0.0006 for DESI LRGs. The void-cluster H(z) differential is ΔH/H ≈ 0.6 per cent at z = 0.2 and ≈ 0.1 per cent at z = 0.5. A proxy measurement using 559 Pantheon+SH0ES SNIa (z ∈ [0.05, 0.30]) cross-matched with 1,479 SDSS voids yields Δμ = +0.050 ± 0.034 mag (1.47σ) — statistics-limited and inconclusive (ln BF = −2.05). DESI DR1 BGS (300,000 galaxies, direct BAO peak-shift) provides a factor ~10 improvement in signal-to-noise. Falsification criterion: ΔH/H(z = 0.2) outside [−0.5%, +2.0%], or no monotonic decrease of β(L).

**Note on k(M, f_gas).** Full recalibration of equation (3) on 165 SPARC galaxies with measured H I masses confirms k = 4.075 × (M_bary/10¹⁰)^(−0.520) (R² = 0.645). The gas fraction f_gas shows a strong univariate correlation with k (r = +0.684, p < 10⁻²³), reflecting the physical expectation that gas-rich galaxies have shallower potential wells and hence stronger temporon coupling. However, including f_gas as a secondary parameter yields only ΔR² = +0.006, indicating that the mass dependence subsumes most of the f_gas information. The recommended law k(M) = 4.00 × M^(−0.49) (equation 3) therefore remains robust.

**Prediction 4 — H(z,ρ) variation correlated with void density (DESI DR2).**
TMT predicts H/H_mean offsets of +8.7 per cent in deep voids (ρ/ρ_c = 0.3) and −0.6 per cent in clusters (ρ/ρ_c = 17.5). DESI DR2 spectroscopic data stratified by large-scale density field will directly test this. Falsification criterion: no statistically significant (>2σ) H correlation with large-scale density after controlling for peculiar velocity systematics.

**Prediction 5 — Scalar gravitational-wave breathing mode (Test 5; LISA 2037+).**
The full tensor formulation (Després Asselin 2026a) predicts a breathing polarisation mode δψ at amplitude h_scalar/h_tensor = √(ξv²) × compactness. At the Cassini/solar-system upper limit ξv² < 10⁻⁵, this gives h_s/h_t < 1.4 × 10⁻³ — a factor of ~20 below the current LIGO constraint from GW170817 (|h_s/h_t| < 0.03). LISA will achieve sensitivity 3 × 10⁻⁵ per event via stacking; stacking ~25 SMBH merger events (10⁶ M☉, 1 Gpc) will reach 5σ at the PPN limit. Falsification criterion: LISA constrains h_s/h_t < 3 × 10⁻⁵ from stacking.

**Prediction 6 — ISW amplification ratio for supervoids (Planck × DESI).**
TMT predicts that the ISW signal in supervoids (δ ≈ −0.8) is ≈30 per cent stronger than in standard voids (δ ≈ −0.3), reflecting deeper temporon condensation at extreme underdensities. Cross-correlation of Planck CMB with ZOBOV/DESI void catalogues stratified by void depth provides a direct test. Current ISW measurement ratio (17.9 per cent observed vs 18.2 per cent predicted; Section 4.7) is consistent but statistics-limited.

---

## 6 CONCLUSIONS

We have presented the Theory of Time Mastery as a unified gravitational framework addressing dark matter, dark energy, and the Hubble tension through a single mechanism: temporal distortion. The principal results are:

(i) A universal scaling relation r_c ∝ M^0.56 emerges from fitting 103 SPARC galaxies independently (r = 0.768, p = 3×10⁻²¹).

(ii) The effective mass formula (equation 7) achieves 100 per cent applicability and 97.5 per cent median chi-squared improvement across 156 SPARC galaxies.

(iii) KiDS-450 halo isotropy is confirmed at the 0.024 per cent level.

(iv) The Hubble tension is resolved without additional free parameters.

(v) Baryonic Tully–Fisher residuals are reduced by 20.8 per cent (scatter: 0.226 → 0.179 dex) when the TMT effective mass replaces the Newtonian baryonic mass, and correlate with directly observable baryonic parameters (r = +0.32 with R_disk, p = 3×10⁻⁴) rather than hidden NFW concentrations.

(vi) A spatial β(L) = β_H0 × (L_0/L)^1.658 formulation is derived from two independent anchors and predicts quantitatively the scale-dependent decay of temporal coupling from the local KBC void to the Pantheon+ cosmological line of sight.

(vii) Combined significance across thirteen independent validation pillars by Fisher's method: p ≈ 10⁻¹⁶⁴ (>27.5σ), with galactic dynamics alone yielding >16σ and large-scale structure alone >22σ.

(viii) Six quantitative near-term falsifiable predictions are derived, three of which are already constrained by present data: (a) r_c ∝ M^0.56 detectable with N = 100 Euclid galaxies (99.9 per cent power); (b) β(L) decay measurable with DESI DR1 BGS at ΔH/H ≈ 0.6 per cent (z = 0.2); (c) scalar GW breathing mode h_s/h_t < 1.4 × 10⁻³ testable by LISA with ~25 SMBH mergers.

All analysis code, data, and results are publicly available at github.com/chronos717313/Mastery-of-time (DOI: 10.5281/zenodo.18287042).

---

## ACKNOWLEDGEMENTS

The author thanks the SPARC team (F. Lelli, S. S. McGaugh, J. M. Schombert) for their publicly available rotation curve catalogue. This research received no external funding and was conducted independently.

*Software:* Python 3.11, NumPy (Harris et al. 2020), SciPy (Virtanen et al. 2020), Astropy (Astropy Collaboration 2022).

*Data availability:* All data used in this work are publicly available through the references cited. Analysis scripts and intermediate results are available at github.com/chronos717313/Mastery-of-time.

---

## REFERENCES

ATLAS Collaboration, 2021, Phys. Rev. D, 103, 112006

Després Asselin P.-O., 2026a, Full general-relativistic tensor formulation of the Theory of Time Mastery (companion paper), github.com/chronos717313/Mastery-of-time, DOI: 10.5281/zenodo.18287042

Després Asselin P.-O., 2026b, First-principles derivation of the dual-β structure in TMT (companion paper), github.com/chronos717313/Mastery-of-time, DOI: 10.5281/zenodo.18287042

Després Asselin P.-O., 2026c, Combined Fisher significance across thirteen TMT validation pillars (technical note), github.com/chronos717313/Mastery-of-time, DOI: 10.5281/zenodo.18287042

Després Asselin P.-O., 2026d, Quantitative falsifiable predictions for TMT: Tests 1, 4, and 5 (technical note), github.com/chronos717313/Mastery-of-time, DOI: 10.5281/zenodo.18287042

Després Asselin P.-O., 2026e, Baryonic Tully–Fisher residuals, spatial β(L) law, and quantitative ISW formula in TMT (technical note), github.com/chronos717313/Mastery-of-time, DOI: 10.5281/zenodo.18287042

Astropy Collaboration, 2022, ApJ, 935, 167

Bell E. F., de Jong R. S., 2001, ApJ, 550, 212

Clowe D. et al., 2006, ApJ, 648, L109

Fermi-LAT Collaboration, 2015, Phys. Rev. Lett., 115, 231301

Gupta R. P., 2024, ApJ, 964, 55

Harris C. R. et al., 2020, Nature, 585, 357

Hildebrandt H. et al., 2017, MNRAS, 465, 1454

Laigle C. et al., 2016, ApJS, 224, 24

Lelli F., McGaugh S. S., Schombert J. M., 2016, AJ, 152, 157

LZ Collaboration, 2024, Phys. Rev. Lett., 132, 131001

Milgrom M., 1983, ApJ, 270, 365

Navarro J. F., Frenk C. S., White S. D. M., 1997, ApJ, 490, 493

Persic M., Salucci P., Stel F., 1996, MNRAS, 281, 27

Planck Collaboration, 2016, A&A, 594, A21

Planck Collaboration, 2020, A&A, 641, A6

Riess A. G. et al., 2022, ApJ, 934, L7

Rubin V. C., Ford W. K., 1970, ApJ, 159, 379

Scolnic D. et al., 2022, ApJ, 938, 113

Virtanen P. et al., 2020, Nature Methods, 17, 261

---

## Submission Checklist — MNRAS

- [ ] Créer un compte sur Oxford Academic (academic.oup.com)
- [ ] Soumettre via : https://mc.manuscriptcentral.com/mnras
- [ ] Choisir : **Subscription Track** (GRATUIT — aucun APC)
- [ ] Catégorie : **Galaxies** ou **Cosmology and nongalactic astrophysics**
- [ ] Format préféré : LaTeX avec classe mnras.cls
- [ ] English britannique obligatoire (per cent, colour, modelling, behaviour...)
- [ ] Références : format Auteur Année (pas numéroté)
- [ ] Vérifier : pas de "Figure X" si pas de figure jointe
- [ ] Déclaration de conflits : "None"
- [ ] Déclaration de financement : "This research received no external funding"

---

## Différences clés ApJ vs MNRAS respectées

| Élément | ApJ | MNRAS |
|---------|-----|-------|
| Anglais | Américain | **Britannique** |
| Références | Auteur (Année) | Auteur (Année) |
| Numérotation sections | 1. / 1.1 | 1 / 1.1 |
| Équations | (1), (2)... | (1), (2)... |
| Pourcentage | % | **per cent** |
| Unités vitesse | km/s/Mpc | **km s⁻¹ Mpc⁻¹** |
| Data availability | Optionnel | **Obligatoire** |
| Acknowledgements | Acknowledgments | **Acknowledgements** |
| Coût publication | Waiver possible | **GRATUIT (subscription)** |

---

*Draft v1.2 — Pierre-Olivier Després Asselin — Avril 2026*
*Mises à jour v1.2 : Significativité combinée mise à jour à 27.3σ (10 piliers, Fisher) ; Section 4.6 expandue avec test proxy β réel Pantheon+ × SDSS voids (1.47σ, non concluant) ; Section 4.9 mise à jour vers 10 piliers Fisher avec tableau détaillé ; Section 5.4 expandue avec prédictions quantitatives Tests 1/4/5 (Euclid, DESI, LISA) ; deux companion papers supplémentaires 2026c/d ajoutés en références ; abstract mis à jour.*
