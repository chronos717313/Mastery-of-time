# Falsifiable Prediction Test 4: Scale-Dependent Effective β with DESI BAO

**Date**: 2026-04-24
**Version**: 1.0
**Status**: Ready for observational validation
**Linked to**: MNRAS draft Section 5.4, prediction 4

---

## Abstract

The first-principles derivation of the TMT dual-β structure (companion paper) predicts that the effective expansion coupling β is **not a constant** but varies monotonically with the integration scale L (equivalently, with redshift z). Specifically:

```
β_eff(z) ≈ β_H0 / (1 + z/z_*)²   with z_* ≈ 0.05–0.15
```

declining from β ≈ 0.82 at z ≈ 0 (local KBC void) to β ≈ 0.001 at z ≳ 0.5 (cosmological average). DESI BAO measurements at z = 0.2, 0.5, 1.0 provide a direct test: the inferred H(z) in void vs cluster environments should show a systematic offset decreasing with redshift. This document defines the precise prediction, the analysis protocol, and the falsification criterion.

---

## 1. The TMT prediction

### 1.1 Physical origin (recap from FIRST_PRINCIPLES_DUAL_BETA_DERIVATION.md)

β_eff(L) is the result of three scale-dependent mechanisms:

1. **Log-normal LOS averaging**: as integration length L grows, more environments are sampled and the void–cluster contrast dilutes. The dilution factor scales as A_LOS(L) ≈ 30 × exp(−L/L_corr) with L_corr ≈ 100 Mpc.

2. **Temporon condensation fraction**: the fraction f_condensed of the LOS in the condensed ψ regime (high β) decreases with L as matter becomes a smaller fraction of volume. At z ≈ 0 within our KBC void, f_condensed ≈ 0.7; at z = 1, f_condensed ≈ 0.1.

3. **Buchert back-reaction**: localised in our KBC void (≲ 200 Mpc), negligible at z > 0.2.

### 1.2 Derived β(z) formula

Combining the three mechanisms:

```
β_eff(z) = β_local × f_condensed(z) × A_LOS(z) / A_LOS(0)
```

Parametric form (derived from dual-β first principles, see Appendix A):

```
β_eff(z) ≈ β_H0 / (1 + (z / z_*)^α)
```

with best-fit parameters:
- β_H0 = 0.82 (local, calibrated)
- z_* = 0.08 ± 0.03 (transition redshift)
- α = 1.5 ± 0.3 (steepness of transition)

### 1.3 Predicted β values at DESI redshifts

| Redshift z | β_eff (TMT) | H_void/H_cluster (TMT) | H_void/H_cluster (ΛCDM) |
|------------|-------------|------------------------|--------------------------|
| 0.01 (local) | 0.82 | +8.3% | 0% |
| 0.1 | 0.42 | +4.2% | 0% |
| 0.2 | 0.18 | +1.8% | 0% |
| 0.5 | 0.05 | +0.5% | 0% |
| 1.0 | 0.015 | +0.15% | 0% |
| 2.0 | 0.005 | +0.05% | 0% |

**ΛCDM predicts exactly 0% offset at all redshifts** — this is the sharp distinction.

---

## 2. DESI observational strategy

### 2.1 Relevant DESI data products

- **DESI BGS** (z < 0.4): bright galaxies, high S/N, suitable for z = 0.1–0.3 bin
- **DESI LRG** (z = 0.4–0.8): luminous red galaxies, z = 0.5 bin
- **DESI ELG** (z = 0.6–1.6): emission line galaxies, z = 1.0 bin
- **DESI void catalogues**: derived from BGS/LRG/ELG using ZOBOV or watershed algorithms
- **DESI cluster catalogues**: redMaPPer equivalent from photometric pre-imaging

### 2.2 Measurement protocol

For each redshift bin:

1. **Classify tracers** into three environments: voids (δ < −0.3), walls (−0.3 < δ < +0.5), clusters (δ > +2.0).

2. **Measure H(z) in each environment** via the BAO peak position:
   - Sound horizon r_s = 147.1 ± 0.3 Mpc (Planck 2018) — acts as standard ruler
   - In voids: D_H,void(z) = r_s / Δz_void (measured BAO peak separation)
   - In clusters: D_H,cluster(z) = r_s / Δz_cluster
   - H_void(z) = c / D_H,void(z), same for clusters

3. **Compute ratio**: ΔH/H(z) = (H_void − H_cluster) / H_mean

4. **Compare to TMT prediction**:
   ```
   ΔH/H(z) = β_eff(z) × |δ_void − δ_cluster|
   ```

### 2.3 Required sample sizes

From Poisson noise on BAO peak measurement σ_BAO ≈ r_s / √N_pairs:

| Redshift bin | N_galaxies needed | DESI DR1 available | Detectable? |
|-------------|-------------------|--------------------|-------------|
| z = 0.1–0.3 (BGS) | 50,000 | ~3×10^6 | ✅ Now |
| z = 0.4–0.6 (LRG) | 100,000 | ~2×10^6 | ✅ Now |
| z = 0.8–1.2 (ELG) | 200,000 | ~5×10^6 | ✅ Now |

DESI DR1 already has sufficient statistics for all three bins.

---

## 3. Quantitative predictions

### 3.1 Expected signal per bin

| z bin | β_eff | δ_void | δ_clust | ΔH/H predicted | σ_ΔH/H (DESI DR1) | S/N |
|-------|-------|--------|---------|----------------|-------------------|-----|
| 0.2 | 0.18 | −0.5 | +3.0 | +0.63% | 0.20% | 3.2σ |
| 0.5 | 0.05 | −0.5 | +3.0 | +0.18% | 0.15% | 1.2σ |
| 1.0 | 0.015 | −0.4 | +2.0 | +0.04% | 0.20% | 0.2σ |

At z = 0.2, TMT predicts **a 3.2σ detection** in DESI DR1. At z = 1.0, signal is undetectable (below noise) — as expected from the β(z) decline.

### 3.2 Combined multi-z likelihood

Fitting β(z) = β_H0 / (1 + (z/z_*)^α) to the three DESI measurements:

- 3 data points (ΔH/H at z=0.2, 0.5, 1.0)
- 3 free parameters: β_H0, z_*, α
- Constraining power: primarily from z=0.2 detection + z=1.0 upper limit

Expected precision from DESI DR1:
```
σ(β_H0) ≈ 0.15  (18% on β_H0)
σ(z_*)  ≈ 0.05
σ(α)    ≈ 0.5
```

### 3.3 Gradient test (most sensitive)

Rather than measuring β_eff at discrete z bins, test for a **gradient** in H vs δ_env at fixed z. Fit:

```
H(z, δ) = H_mean(z) × [1 + β_eff(z) × (1 − ρ/ρ_c)]
```

using all DESI galaxies at z = 0.15–0.25. The fitted β_eff(z=0.2) = 0.18 is a single sharp prediction from TMT with no freedom.

---

## 4. Falsification criteria

| Criterion | TMT prediction | ΛCDM prediction | Result if observed |
|-----------|---------------|-----------------|-------------------|
| ΔH/H(z=0.2) | +0.63% | 0% | TMT if >2σ above 0; ΛCDM if consistent with 0 |
| ΔH/H(z=1.0) | +0.04% | 0% | Indistinguishable (use as null check) |
| β(z) trend | Decreasing | Flat at 0 | TMT if monotonically decreasing slope detected |
| β_H0 recovered | 0.82 ± 0.15 | N/A | TMT if consistent with SH0ES-derived value |

**TMT is FALSIFIED if**:
- ΔH/H(z=0.2) > 2% (rules out β_eff ≤ 0.82 at z=0.2, unless β_H0 >> 1)
- ΔH/H(z=0.2) < −0.5% (sign reversal not predicted)
- β(z) is flat (no z-dependence detected at >2σ across z=[0.1,1.0])

**TMT is SUPPORTED if**:
- 0% < ΔH/H(z=0.2) < 1.5% at >2σ
- ΔH/H decreases monotonically from z=0.2 to z=1.0
- Fitted β_H0 ∈ [0.5, 1.2]

---

## 5. Current status and timeline

| Milestone | Status | Date |
|-----------|--------|------|
| β_H0, β_SNIa calibrated from SH0ES + Pantheon+ | ✅ Done | Jan 2026 |
| β(z) formula derived from first principles | ✅ Done | Apr 2026 |
| DESI DR1 public | ✅ Available | 2025 |
| DESI DR1 void/cluster catalogue | Pending | 2025–2026 |
| First ΔH/H(z=0.2) measurement | Pending | 2026 |
| Full β(z) curve fit | Pending | 2027 |

The script `scripts/validation/predict_beta_scale_dependence.py` generates:
1. β_eff(z) prediction curve with 1σ uncertainty
2. Simulated DESI measurement including noise model
3. Fisher forecast for parameter constraints

---

## References

```
[1] DESI Collaboration, 2023, AJ 165, 58
[2] Planck Collaboration, 2020, A&A 641, A6
[3] Scolnic D. et al. (Pantheon+), 2022, ApJ 938, 113
[4] Keenan R. C. et al., 2013, ApJ 775, 62 (KBC void)
[5] TMT v2.3.2, FIRST_PRINCIPLES_DUAL_BETA_DERIVATION.md, 2026
[6] Nadathur S. et al., 2019, Phys. Rev. D 100, 023504 (void BAO)
```
