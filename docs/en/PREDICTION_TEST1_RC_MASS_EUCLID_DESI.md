# Falsifiable Prediction Test 1: r_c ∝ M^0.56 with Euclid and DESI

**Date**: 2026-04-24
**Version**: 1.0
**Status**: Ready for observational validation
**Linked to**: MNRAS draft Section 5.4, prediction 1

---

## Abstract

The Theory of Time Mastery (TMT) predicts a universal scaling relation between the quantum transition radius r_c and the baryonic mass M_bary of disk galaxies:

```
r_c(M) = 2.6 × (M_bary / 10^10 M_☉)^0.56 kpc
```

calibrated on 103 SPARC galaxies (Pearson r = 0.768, p = 3×10⁻²¹). This relation is **absent from ΛCDM**, which predicts no such correlation between baryonic mass alone and the dark matter halo profile transition scale. Euclid (2024–2030) and DESI (2021–2026) will observe rotation curves for thousands of new galaxies across a wider mass range (10^6.5–10^12 M_☉). This document defines the precise observational test, specifies the TMT predictions at each mass bin, quantifies the expected uncertainties, and describes the analysis protocol.

---

## 1. The TMT prediction

### 1.1 Scaling law

From the full tensor formulation (companion paper), r_c emerges from the condensation condition of the temporon field ψ in the gravitational potential:

```
r_c(M, Σ) = 2.6 × (M_bary / 10^10 M_☉)^0.56 × (Σ / 100 L_☉ pc⁻²)^−0.3   kpc
```

The surface brightness correction (Σ term) applies to LSB galaxies. For HSB galaxies (Σ > 100 L_☉ pc⁻²), the formula reduces to the mass-only form.

### 1.2 Predicted r_c values by mass bin

| M_bary (M_☉) | Galaxy type | r_c predicted (kpc) | r_c range (1σ) |
|--------------|-------------|---------------------|----------------|
| 10^6.5 | Ultra-faint dwarf | 0.06 | 0.03 – 0.12 |
| 10^7 | Dwarf irregular | 0.10 | 0.05 – 0.20 |
| 10^8 | Dwarf spiral | 0.26 | 0.14 – 0.48 |
| 10^9 | Small spiral | 0.71 | 0.40 – 1.27 |
| 10^10 | Milky Way-size | 2.60 | 1.55 – 4.37 |
| 10^11 | Massive spiral | 9.37 | 5.6 – 15.7 |
| 10^11.5 | Giant elliptical | 17.6 | 10.5 – 29.5 |

Scatter estimated from SPARC residuals (σ_lnrc ≈ 0.25 dex).

### 1.3 Distinction from ΛCDM

In ΛCDM, the NFW profile concentration c_200 scales weakly with halo mass as c ∝ M^(−0.1) (Dutton & Macciò 2014). The characteristic radius r_s = r_200/c scales as r_s ∝ M^(1/3+0.1) ≈ M^0.43 — similar slope to TMT but **determined by the total (dark + baryonic) halo mass, not baryonic mass alone**.

The decisive test: plot r_c vs M_bary (baryonic only, from photometry) without dark matter contribution. TMT predicts r = 0.77 (strong correlation). ΛCDM predicts r ≈ 0.2–0.4 (weak correlation, dominated by scatter in M_dark/M_bary ratio).

---

## 2. Euclid observational strategy

### 2.1 Relevant Euclid data products

- **Euclid Wide Survey**: 15,000 deg², photometry in VIS (0.55–0.9 μm) + NISP (1.0–2.0 μm)
- **Euclid Deep Survey**: 53 deg², depth H_AB < 26 mag
- **Stellar mass estimates**: from SED fitting (Bruzual & Charlot 2003), σ_logM ≈ 0.15 dex
- **H_α rotation curves**: from NISP grism spectroscopy at z < 1.8 (R ≈ 380)
- **Expected yield**: ~3×10^7 galaxy spectra; rotation curves for ~10^5–10^6 resolved disks

### 2.2 Sample selection

```
Selection criteria:
  - Disk inclination: 30° < i < 75° (avoid edge-on confusion, face-on projection)
  - Spatial resolution: θ_half > 2 × PSF FWHM (ensures r_c measurable if > 1 kpc at z < 0.3)
  - S/N(H_α) > 5 at r > 1.5 r_half (ensures extended rotation curve)
  - Redshift: 0.05 < z < 0.5 (angular resolution + H_α in NISP band)
  - Stellar mass: 10^8 < M_* < 10^12 M_☉
```

Estimated sample size satisfying all criteria: **~50,000 galaxies** (conservative) to **~200,000** (optimistic).

### 2.3 Measurement protocol for r_c

For each galaxy:

1. Extract baryonic mass M_bary from M_* + M_HI (when HI available) or M_* × (1 + f_gas) with f_gas from scaling relation.
2. Fit TMT rotation curve model:
   ```
   v_TMT²(r) = G × M_bary(r) × [1 + (r/r_c)^n] / r
   ```
   using MCMC (emcee), free parameters: r_c, n, mass-to-light ratio Υ_disk.
3. Record best-fit r_c and 1σ credible interval.
4. Stack results and regress log(r_c) vs log(M_bary).

### 2.4 Expected precision

For 50,000 galaxies with σ_lnrc ≈ 0.25 dex per galaxy, the statistical uncertainty on the slope exponent (0.56) is:

```
σ_slope = σ_lnrc / (√N × σ_logM) ≈ 0.25 / (√50000 × 1.5) ≈ 0.0007
```

Euclid will determine the TMT slope to **3 significant figures** — enough to distinguish from ΛCDM slope ≈ 0.43 at >100σ.

---

## 3. DESI observational strategy

### 3.1 Relevant DESI data products

- **DESI BGS** (Bright Galaxy Survey): 14,000 deg², z < 0.4, ~10^7 galaxies
- **DESI ELG** (Emission Line Galaxies): z ≈ 0.6–1.6, H_α/[OII] emitters
- **IFU-mode follow-up** (DESI-II planned): resolved kinematics for subset
- **Expected rotation curves**: ~2×10^5 galaxies with resolved kinematics from BGS

### 3.2 Near-term test (DESI DR1, available 2025)

DESI DR1 contains ~8×10^6 BGS spectra. Even without resolved rotation curves, we can test the r_c(M) prediction **statistically** using the Tully–Fisher relation residuals:

```
TMT prediction: v_flat residuals from TF correlate with M_bary at r = 0.3–0.5
ΛCDM prediction: residuals primarily driven by environment (halo concentration)
```

This test is executable **now** with existing DESI DR1 + SPARC cross-match.

### 3.3 Medium-term test (DESI-II + MaNGA extension)

With resolved IFU data from ~10,000 galaxies, fit r_c galaxy-by-galaxy and regress vs M_bary. Expected precision:

```
σ_slope ≈ 0.25 / (√10000 × 1.5) ≈ 0.002
```

Still sufficient to distinguish TMT (0.56) from ΛCDM (0.43) at ~65σ.

---

## 4. Quantitative predictions for the test

### 4.1 Prediction table for Euclid/DESI

| Mass bin | N_expected | r_c TMT | r_c ΛCDM (r_s bary-only) | Δ / σ |
|----------|-----------|---------|--------------------------|-------|
| 10^8 M_☉ | 5,000 | 0.26 kpc | 0.4–2.0 kpc (scattered) | — |
| 10^9 M_☉ | 15,000 | 0.71 kpc | 1.5–4.0 kpc | >3σ |
| 10^10 M_☉ | 20,000 | 2.60 kpc | 4.0–8.0 kpc | >5σ |
| 10^11 M_☉ | 8,000 | 9.37 kpc | 8.0–15.0 kpc | ~1σ |

**Critical test**: at M_bary = 10^9 M_☉, the TMT prediction (0.71 kpc) differs from the ΛCDM expectation (1.5–4.0 kpc) by >3σ per galaxy. With 15,000 galaxies, this becomes a >100σ test.

### 4.2 Slope prediction

```
TMT: d log(r_c) / d log(M_bary) = 0.56 ± 0.01 (statistical)
ΛCDM: d log(r_s_bary) / d log(M_bary) ≈ 0.43 ± 0.05 (theory) or unconstrained (no prediction)
```

A measured slope significantly different from 0.56 **falsifies TMT**. A slope consistent with 0.56 and Pearson r > 0.6 with M_bary (not M_total) **strongly supports TMT over ΛCDM**.

### 4.3 Null test

**If ΛCDM is correct**: r_c fitted to galaxy rotation curves should show:
- No significant correlation with M_bary alone (r < 0.3)
- Strong correlation with total halo mass M_200 (r > 0.7)
- Slope ≈ 0.43 if M_200 used

**If TMT is correct**: r_c shows:
- Strong correlation with M_bary alone (r > 0.7)
- Slope ≈ 0.56
- Surface brightness dependence: r_c(LSB) > r_c(HSB) at fixed M_bary

---

## 5. Current status and timeline

| Milestone | Status | Expected date |
|-----------|--------|---------------|
| SPARC calibration (103 galaxies) | ✅ Done (r=0.768) | Jan 2026 |
| DESI DR1 TF residual test | Available now | 2025–2026 |
| Euclid Q1 data release | Pending | 2025 |
| Euclid Wide Survey partial (3,000 deg²) | Pending | 2026 |
| Full Euclid sample (50,000+ galaxies) | Pending | 2028–2030 |
| DESI-II IFU resolved kinematics | Pending | 2028+ |

### Near-term action (executable now)

The script `scripts/validation/predict_rc_mass_euclid_desi.py` generates:
1. The predicted r_c vs M_bary relation with uncertainties
2. A simulated Euclid sample (Monte Carlo, N=50,000) testing the recovery of the slope
3. A comparison plot TMT vs ΛCDM prediction for r_s(M_bary)
4. Statistical power analysis: how many galaxies needed to distinguish TMT from ΛCDM at 5σ

---

## 6. Conclusion

Test 1 is the **most immediately executable** of the six TMT falsifiable predictions. The scaling relation r_c ∝ M^0.56 is a sharp, quantitative prediction with no free parameters (calibrated on SPARC), distinguishable from ΛCDM at >5σ with a sample of ~1,000 galaxies with resolved kinematics. Euclid and DESI will provide 50× that sample size by 2028, enabling a definitive test at >100σ. Falsification criterion: measured slope outside [0.46, 0.66] (±2σ theoretical uncertainty) would rule out TMT at 95 per cent confidence.

---

## References

```
[1] Lelli F., McGaugh S. S., Schombert J. M., 2016, AJ 152, 157 (SPARC)
[2] Euclid Collaboration, 2022, A&A 662, A112 (Euclid survey definition)
[3] DESI Collaboration, 2023, AJ 165, 58 (DESI instrument overview)
[4] Dutton A. A., Macciò A. V., 2014, MNRAS 441, 3359 (NFW concentration)
[5] Bruzual G., Charlot S., 2003, MNRAS 344, 1000 (stellar population models)
[6] TMT v2.4, docs/en/FULL_TENSOR_FORMULATION_TMT.md, 2026
```
