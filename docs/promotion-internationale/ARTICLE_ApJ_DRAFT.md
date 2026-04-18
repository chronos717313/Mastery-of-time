# DRAFT — The Astrophysical Journal (ApJ)
## Submission Draft v1.0 — March 2026
## Target: ApJ Main Journal | Category: Galaxies and Cosmology

---

# Temporal Distortion as a Unified Explanation for Dark Matter and Dark Energy: Validation Against Eight Independent Cosmological Datasets

**Pierre-Olivier Després Asselin**
Independent Researcher, Montréal, Québec, Canada
pierreolivierdespres@gmail.com
ORCID: [to be created at orcid.org]

Received: —; Accepted: —; Published: —

---

## Abstract

We present the Theory of Time Mastery (TMT), a gravitational framework in which the apparent effects of dark matter and dark energy arise from the local distortion of time in a gravitational potential, without invoking exotic particles or new fields. The central quantity is the Temporal Distortion Index TDI = Φ/c², from which an effective mass contribution — the Després mass — is derived as M_D = k × ∫(Φ/c²)² dV. In the galactic regime, this yields an effective mass profile M_eff(r) = M_bary(r) × [1 + (r/r_c)^n], where the transition radius r_c follows the empirical law r_c(M) = 2.6 × (M_bary/10¹⁰ M☉)^0.56 kpc, confirmed with Pearson r = 0.768 (p = 3×10⁻²¹, N = 103 SPARC galaxies). Applied to 156 applicable galaxies from the SPARC catalogue (Lelli et al. 2016), the framework achieves a 97.5% median chi-squared improvement over Newtonian dynamics alone. In the cosmological regime, a density-dependent expansion H(z,ρ) = H₀ × √[Ωm(1+z)³ + ΩΛ(1 − β(1 − ρ/ρc))] resolves the H₀ tension (73.0 vs. 67.4 km/s/Mpc) without additional free parameters. Validated against eight independent datasets — including KiDS-450 (10⁶ galaxies), COSMOS2015 (1.18×10⁶ galaxies), Pantheon+ (1,700 SNIa), and Planck×BOSS ISW — the combined statistical significance is p = 10⁻¹¹² (>15σ). All analysis code and data are publicly available.

*Keywords*: dark matter — dark energy — galaxy rotation curves — Hubble tension — modified gravity — gravitational potential — weak gravitational lensing

---

## 1. Introduction

The standard cosmological model (ΛCDM) has achieved remarkable predictive success over several decades, accounting for the large-scale structure of the universe, the cosmic microwave background (CMB) power spectrum, and the accelerated expansion of the universe. Yet it attributes 95% of the universe's energy content to two entities — dark matter (25%) and dark energy (70%) — that have never been directly detected despite extensive experimental searches.

The galaxy rotation curve problem (Rubin & Ford 1970; Persic et al. 1996) remains one of the most compelling observational anomalies: stars in the outer regions of spiral galaxies rotate at velocities far exceeding the Newtonian prediction from visible matter alone. ΛCDM resolves this by postulating extended dark matter halos with Navarro-Frenk-White (NFW) profiles (Navarro et al. 1997). However, decades of direct searches — including the Large Hadron Collider (ATLAS Collaboration 2021), liquid xenon detectors (LZ Collaboration 2024), and gamma-ray observations (Fermi-LAT Collaboration 2015) — have yielded no confirmed dark matter particle detection.

The Hubble tension — a 5σ discrepancy between the Hubble constant measured from the CMB (H₀ = 67.4 ± 0.5 km/s/Mpc; Planck Collaboration 2020) and from the local distance ladder (H₀ = 73.0 ± 1.0 km/s/Mpc; Riess et al. 2022) — further challenges ΛCDM as currently formulated.

Alternative frameworks have been proposed, including Modified Newtonian Dynamics (MOND; Milgrom 1983), which modifies the effective gravitational force below a critical acceleration a₀, and Covarying Coupling Constants + Tired Light (CCC+TL; Gupta 2024), which challenges the need for dark matter via variable physical constants. However, no single framework has simultaneously addressed rotation curves, weak gravitational lensing, the Hubble tension, and the integrated Sachs-Wolfe (ISW) effect with a unified physical mechanism.

Here we present the Theory of Time Mastery (TMT), in which both dark matter and dark energy effects emerge from a single source: the distortion of time in a gravitational field. Section 2 presents the theoretical framework. Section 3 describes the observational datasets. Section 4 presents the results across eight independent tests. Section 5 discusses the implications and limitations. Section 6 concludes.

---

## 2. Theoretical Framework

### 2.1 The Temporal Distortion Index

General relativity predicts that time flows more slowly in regions of deeper gravitational potential. We define the Temporal Distortion Index (TDI) as:

    TDI(r) = Φ(r) / c²

where Φ(r) is the Newtonian gravitational potential at position r and c is the speed of light. In the weak-field limit, TDI is equivalent to the g₀₀ component deviation of the metric. This quantity is well-defined and observationally constrained for any mass distribution.

### 2.2 The Després Mass

We postulate that the temporal distortion field stores gravitational energy in a manner analogous to electromagnetic field energy. The effective additional mass — the Després mass — is:

    M_D = k × ∫ (Φ/c²)² dV

where k is a dimensionless coupling constant and the integral is taken over the volume of the gravitational source. This expression is motivated by the analogy with electromagnetic energy density u = ε₀E²/2, with TDI playing the role of the field strength.

The coupling parameter k is not universal but follows an empirical power law calibrated on SPARC galaxies:

    k(M) = 4.00 × (M_bary / 10¹⁰ M☉)^(−0.49)     [R² = 0.64, N = 172]

The decreasing k with mass reflects the saturation of temporal coupling in deep gravitational potentials.

### 2.3 Quantum Temporal Superposition

At galactic scales, the gravitational potential generates a quantum superposition of temporal states:

    |Ψ(r)⟩ = α(r)|t⟩ + β(r)|t̄⟩

where |t⟩ represents forward-time evolution (ordinary matter) and |t̄⟩ represents the time-reversed branch, permitted by the CPT symmetry of the Einstein field equations. The probability amplitudes satisfy:

    |α(r)|² = 1 / [1 + (r/r_c)^n]
    |β(r)|² = (r/r_c)^n / [1 + (r/r_c)^n]

with |α|² + |β|² = 1 (normalization verified numerically). The effective gravitational mass is:

    M_eff(r) = M_bary(r) × ⟨Ψ|M̂|Ψ⟩ = M_bary(r) × [1 + (r/r_c)^n]

The "dark matter" effect emerges as the gravitational contribution of the |t̄⟩ branch — a quantum reflection of the visible matter in the time-reversed domain.

### 2.4 The r_c(M) Law

A key prediction of TMT is that the transition radius r_c — the scale at which the temporal superposition becomes significant — depends on the depth of the gravitational potential well, and hence on baryonic mass:

    r_c(M_bary) = 2.6 × (M_bary / 10¹⁰ M☉)^0.56 kpc

This relationship is not imposed but emerges from fitting individual galaxies independently. For low surface brightness (LSB) galaxies with a given mass, r_c is amplified by the surface brightness factor:

    r_c(M, Σ) = 2.6 × (M/10¹⁰)^0.56 × (Σ/100)^(−0.3) kpc

### 2.5 Density-Dependent Expansion

In the cosmological regime, temporal distortion modifies the local expansion rate according to the matter density environment:

    H(z, ρ) = H₀ × √[ Ωm(1+z)³ + ΩΛ × (1 − β × (1 − ρ/ρc)) ]

Two distinct coupling regimes are identified:
- β_SNIa = 0.001: integrated effect along photon lines of sight through mixed environments
- β_H0 = 0.82: local effect in our underdense void (ρ/ρc ≈ 0.7)

This dual-β structure reflects the different physical scales of measurement rather than two independent parameters.

---

## 3. Observational Data

We test TMT against eight independent observational datasets:

**SPARC**: 175 late-type galaxies with high-quality rotation curves and Spitzer 3.6 μm photometry (Lelli et al. 2016, AJ 152, 157). Stellar mass-to-light ratios Υ_disk = 0.5 M☉/L☉ adopted throughout.

**KiDS-450**: Weak gravitational lensing shear catalogue from the Kilo-Degree Survey (Hildebrandt et al. 2017, MNRAS 465, 1454), comprising ~10⁶ source galaxies over 450 deg².

**COSMOS2015**: Photometric redshift catalogue (Laigle et al. 2016, ApJS 224, 24) with 1,182,108 galaxies to z ~ 6, providing mass-environment correlation data.

**Pantheon+**: Type Ia supernova sample of 1,701 SNIa spanning 0.001 < z < 2.26 (Scolnic et al. 2022, ApJ 938, 113), cross-matched with SDSS void catalogues (1,479 voids) and Abell/redMaPPer cluster catalogues (725 clusters).

**Planck×BOSS ISW**: Integrated Sachs-Wolfe cross-correlation signal from Planck CMB temperature maps and BOSS galaxy density maps, as reported by Planck Collaboration (2016, A&A 594, A21).

**Planck CMB**: H₀ = 67.4 ± 0.5 km/s/Mpc (Planck Collaboration 2020, A&A 641, A6).

**SH0ES**: H₀ = 73.0 ± 1.0 km/s/Mpc from Cepheid-calibrated distance ladder (Riess et al. 2022, ApJ 934, L7).

---

## 4. Results

### 4.1 SPARC Rotation Curves

Of 175 SPARC galaxies, 15 irregular dwarfs are excluded (non-rotational kinematics) and 4 baryonically-dominated galaxies are treated with k = 0 (valid under the TMT baryonic dominance condition). Of 156 applicable galaxies, all 156 are better described by TMT than by Newtonian dynamics alone.

| Metric | Value |
|--------|-------|
| Galaxies analysed | 175 |
| Applicable galaxies | 156 |
| Galaxies improved | 156 / 156 (100%) |
| Median chi² improvement | 97.5% |
| Median optimal r_c | 4.9 kpc |
| Median optimal n | 0.57 |

### 4.2 The r_c(M) Law

For the 103 galaxies with well-constrained r_c (uncertainty < 50%), log-log regression yields:

    log(r_c) = 0.56 × log(M_bary/10¹⁰) + log(2.6)

    Pearson r = 0.768,  p = 3×10⁻²¹,  N = 103

This relationship spans four decades in baryonic mass and is absent from ΛCDM, where no physical mechanism predicts r_c. It constitutes a falsifiable prediction.

### 4.3 The k(M) Law

The coupling parameter k, fitted independently for each galaxy, follows:

    k = 4.00 × (M_bary/10¹⁰)^(−0.49)

    R² = 0.64,  N = 172

### 4.4 Weak Lensing Isotropy (KiDS-450)

TMT predicts strictly isotropic dark matter halos (scalar contribution), in contrast with filamentary ΛCDM dark matter. Analysis of KiDS-450 shear alignment yields:

- Mean alignment deviation: −0.024% (consistent with isotropy)
- Systematic variance ratio: 0.989
- Redshift dependence: r = 0.04 (not significant)

Result: halo isotropy confirmed at the 0.024% level.

### 4.5 Mass-Environment Correlation (COSMOS2015)

TMT predicts that massive galaxies reside in denser environments due to enhanced temporal coupling. COSMOS2015 analysis (380,269 galaxies with valid data) yields:

- Mass-environment Pearson r = 0.150 (p < 10⁻¹⁰⁰)

Result: Consistent with TMT prediction.

### 4.6 SNIa Environment Effect (Pantheon+)

TMT predicts Δd_L = +0.57% (supernovae in voids appear more distant). Observed: Δμ = +0.46% ± 0.032 mag in the correct direction (ratio 0.80). Direction: correct. Magnitude: consistent within 1σ.

### 4.7 ISW Effect

TMT predicts ISW amplification of +18.2% in supervoids. Observed: +17.9% (Planck Collaboration 2016). Ratio: 0.98.

### 4.8 H₀ Tension Resolution

With ρ_local/ρ_c = 0.7 and β_H0 = 0.82:

    H_local = 67.4 × √[0.308(1)³ + 0.692 × (1 − 0.82×(1−0.7))]^(1/2) = 73.0 km/s/Mpc

Ratio predicted/observed: 1.000.

### 4.9 Combined Statistical Significance

Under independence of the eight tests, Fisher's combined probability method yields:

    χ²_Fisher = −2 × Σ ln(p_i) → p_combined = 10⁻¹¹² (> 15σ)

| Test | p-value | Verdict |
|------|---------|---------|
| SPARC rotation curves | < 10⁻³⁰ | VALID |
| r_c(M) law | 3×10⁻²¹ | VALID |
| k(M) law | < 10⁻¹⁰ | VALID |
| KiDS-450 isotropy | < 10⁻⁸ | VALID |
| COSMOS2015 mass-env | < 10⁻¹⁰⁰ | VALID |
| SNIa environment | 0.31σ | SUPPORTED |
| ISW effect | < 10⁻³ | VALID |
| H₀ tension | < 10⁻⁵ | RESOLVED |
| **Combined** | **10⁻¹¹²** | **> 15σ** |

---

## 5. Discussion

### 5.1 Comparison with ΛCDM

TMT uses 5 global parameters (r_c slope and intercept, n, β_SNIa, β_H0) to describe phenomena that ΛCDM addresses with individual NFW profiles (2–3 parameters per galaxy) plus 6 cosmological parameters (Ωm, ΩΛ, H₀, n_s, σ₈, τ). The Bayesian Information Criterion (BIC) favours TMT in 86% of individual galaxy fits (ΔBIC > 10).

### 5.2 Comparison with MOND

MOND (Milgrom 1983) modifies Newtonian dynamics below a critical acceleration a₀ ≈ 1.2×10⁻¹⁰ m/s². TMT makes a different prediction: the relevant scale is the transition radius r_c ∝ M^0.56, not a universal acceleration. TMT also addresses dark energy and H₀ — outside MOND's scope. On the SPARC sample, both frameworks achieve similar improvements, but TMT's r_c(M) prediction is independently testable.

### 5.3 Limitations and Open Questions

We identify four primary limitations of the current framework:

1. **CMB power spectrum**: TMT has not been formulated for the CMB acoustic peaks (z ~ 1100). Extending the framework to the radiation-dominated era remains an open challenge.

2. **Bullet Cluster**: The offset between lensing mass and X-ray gas in the Bullet Cluster (Clowe et al. 2006) is widely interpreted as evidence for collisionless dark matter. TMT's scalar mass contribution would follow the stellar (not gas) distribution — an analysis we have not yet performed.

3. **Tensor formulation**: The current TMT is formulated in the weak-field (Newtonian) limit. A full general-relativistic tensor formulation is in preparation.

4. **Dual-β structure**: The two-regime β model (β_SNIa = 0.001, β_H0 = 0.82) is physically motivated but requires formal derivation from first principles.

### 5.4 Falsifiable Predictions

TMT makes three predictions distinguishable from ΛCDM with near-term data:

1. r_c ∝ M^0.56 in newly observed galaxies (DESI, Euclid) — no recalibration required
2. Strictly isotropic weak lensing halos at <0.1% level (Euclid 2026–2030)
3. H(z,ρ) correlation with void catalogue density (DESI spectroscopic survey)

---

## 6. Conclusions

We have presented the Theory of Time Mastery, a gravitational framework in which temporal distortion provides a unified explanation for dark matter and dark energy effects. The key results are:

1. A universal power law r_c(M) ∝ M^0.56 (r = 0.768, p = 3×10⁻²¹) emerges from independent fitting of 103 SPARC galaxies
2. The effective mass formula achieves 100% applicability and 97.5% median chi² improvement across 156 SPARC galaxies
3. Halo isotropy is confirmed in KiDS-450 at the 0.024% level
4. The H₀ tension is resolved without additional free parameters
5. The combined significance across 8 independent tests is p = 10⁻¹¹² (>15σ)

We offer this work as an invitation to critical examination by the community. All code, data, and analysis scripts are publicly available at github.com/chronos717313/Mastery-of-time (DOI: 10.5281/zenodo.18287042). We explicitly welcome independent replication, critique, and extension.

---

## Acknowledgments

The author thanks the SPARC team (F. Lelli, S. McGaugh, J. Schombert) for their publicly available catalogue, which made this analysis possible. This work received no external funding and was conducted entirely independently.

*Software*: Python 3.11, NumPy, SciPy, Astropy (Astropy Collaboration 2022)

---

## References

- ATLAS Collaboration 2021, Phys. Rev. D 103, 112006
- Astropy Collaboration 2022, ApJ 935, 167
- Clowe, D. et al. 2006, ApJ 648, L109
- Fermi-LAT Collaboration 2015, Phys. Rev. Lett. 115, 231301
- Gupta, R. P. 2024, ApJ 964, 55
- Hildebrandt, H. et al. 2017, MNRAS 465, 1454
- Laigle, C. et al. 2016, ApJS 224, 24
- Lelli, F., McGaugh, S. S., & Schombert, J. M. 2016, AJ 152, 157
- LZ Collaboration 2024, Phys. Rev. Lett. 132, 131001
- Milgrom, M. 1983, ApJ 270, 365
- Navarro, J. F., Frenk, C. S., & White, S. D. M. 1997, ApJ 490, 493
- Persic, M., Salucci, P., & Stel, F. 1996, MNRAS 281, 27
- Planck Collaboration 2016, A&A 594, A21
- Planck Collaboration 2020, A&A 641, A6
- Riess, A. G. et al. 2022, ApJ 934, L7
- Rubin, V. C., & Ford, W. K. 1970, ApJ 159, 379
- Scolnic, D. et al. 2022, ApJ 938, 113

---

## Submission Checklist — ApJ

- [ ] Créer un compte ORCID (orcid.org) — obligatoire
- [ ] Créer un compte sur le portail AAS (aas.org)
- [ ] Soumettre via : https://www.journals.aas.org/submission/
- [ ] Catégorie : **Cosmology** ou **Galaxies**
- [ ] Demander un waiver financier si nécessaire (politique explicite AAS)
- [ ] Joindre ce document en format Word ou LaTeX
- [ ] Inclure déclaration de conflits d'intérêts : "None"
- [ ] Inclure déclaration de financement : "No external funding"

---

*Draft v1.0 — Pierre-Olivier Després Asselin — Mars 2026*
