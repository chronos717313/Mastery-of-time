# Falsifiable Prediction Test 5: Scalar Gravitational-Wave Polarisation with LISA

**Date**: 2026-04-24
**Version**: 1.0
**Status**: Ready for observational validation
**Linked to**: MNRAS draft Section 5.4, prediction 5

---

## Abstract

The full general-relativistic tensor formulation of TMT (companion paper) introduces a scalar (breathing) gravitational-wave polarisation mode δψ, arising from perturbations of the temporon field ψ. The predicted strain amplitude ratio of scalar to tensor modes is:

```
h_scalar / h_tensor ≈ √(8πG ξ v²) × (m_ψ / f_GW)²   for f_GW >> m_ψ c²/h
```

For the calibrated TMT parameters (ξv² < 10⁻⁵, m_ψ ≈ 10⁻³³ eV), this ratio lies in the range 10⁻⁸ to 10⁻² depending on the source and frequency. This is below current LIGO/Virgo sensitivity but **within reach of LISA (2037)** for supermassive black hole merger events. This document defines the prediction, the analysis protocol for LISA data, and the falsification criteria.

---

## 1. The TMT prediction

### 1.1 Scalar mode from the full tensor formulation

From `FULL_TENSOR_FORMULATION_TMT.md`, the linearised perturbation system around a flat FLRW background has:

- **Tensor modes h^+, h^×**: standard GW polarisations, propagate at c
- **Scalar mode δψ**: temporon field perturbation, satisfies:

```
(□ − m_ψ²) δψ = −ξ R^(1) ψ_0 − J_m^(1)
```

where R^(1) is the linearised Ricci scalar (sourced by h_μν) and J_m^(1) is the linearised matter source.

The scalar mode is **sourced by the tensor mode** via the curvature coupling ξ, creating a secondary breathing polarisation.

### 1.2 Strain ratio formula

For a compact binary merger at distance d, the source generates tensor strain:

```
h_tensor(f) ~ 4G M_chirp (π f)^(2/3) / (c² d)   [post-Newtonian]
```

The scalar strain is produced via two channels:

**Channel A — Direct coupling to matter stress (dominant at m_ψ f_GW >> 1)**:

```
h_scalar,A ~ ξ × (G M / c² R_source) × h_tensor   [strong-field source region]
```

**Channel B — Curvature-sourced (dominant at m_ψ << f_GW)**:

```
h_scalar,B ~ ξ v²_PPN × (f_GW / f_c)² × h_tensor
```

where v²_PPN = 8πGξv² and f_c = m_ψ c² / h (Compton frequency of temporon).

### 1.3 Predicted amplitude at LISA frequencies

For LISA sensitivity band (10⁻⁴ to 10⁻¹ Hz), sources are supermassive BH mergers (SMBH):

| Source | M (M_☉) | d (Mpc) | f_peak (Hz) | h_tensor | h_scalar/h_tensor |
|--------|---------|---------|-------------|----------|-------------------|
| SMBH merger 10^6 M_☉ | 10^6 | 1000 | 10⁻³ | 10⁻¹⁷ | 10⁻⁵ to 10⁻³ |
| SMBH merger 10^7 M_☉ | 10^7 | 1000 | 10⁻⁴ | 10⁻¹⁶ | 10⁻⁵ to 10⁻³ |
| Extreme mass ratio (EMRI) | 10^6+10 | 500 | 10⁻³ | 10⁻¹⁷ | 10⁻⁶ to 10⁻⁴ |
| LISA verification binary | 0.6 M_☉ | 0.005 | 3×10⁻³ | 10⁻²² | < 10⁻⁸ |

The range reflects uncertainty in ξv² ∈ [10⁻⁸, 10⁻⁵] (PPN constraint: ξv² < 10⁻⁵).

### 1.4 Physical mechanism

The large ratio for SMBH mergers (vs stellar-mass binaries) reflects two effects:

1. **Strong-field enhancement**: Near an SMBH, the temporon field has ψ ≈ v (condensed regime), making it active and strongly sourced by the curvature.
2. **Mass sensitivity**: Channel A scales as GM/Rc² (compactness), maximised for BH mergers.

For LISA verification binaries (low-mass, z≈0, within the galaxy), Channel B dominates and h_scalar < 10⁻⁸ h_tensor — **undetectable even by LISA**, consistent with existing constraints.

---

## 2. LISA observational strategy

### 2.1 LISA polarisation decomposition

LISA measures the GW strain as a function of time h(t) via three laser interferometer arms forming a triangle. The response to each polarisation mode (h^+, h^×, h_s) differs geometrically:

```
h_LISA(t) = F^+(t) h^+(t) + F^×(t) h^×(t) + F^s(t) h_s(t)
```

where F^+(t), F^×(t), F^s(t) are antenna pattern functions. As LISA orbits the Sun, the antenna pattern rotates, allowing polarisation decomposition via time-domain analysis.

**Key property**: the scalar (breathing) mode response F^s(t) has a **different angular dependence** from F^+(t) and F^×(t). A face-on source produces:

```
F^+(t) = (1 + cos²θ)/2 × cos(2φ + 2φ_0)
F^s(t) = sin²θ × cos(2φ_L + 2φ_0)
```

where θ is the inclination angle. The breathing mode is **maximum for face-on** sources (θ = 0) while having a different sky pattern.

### 2.2 Measurement protocol

1. **Detect SMBH merger event** (expected rate: ~10 per year for LISA).

2. **Parameter estimation**: Fit h^+(t) and h^×(t) with standard waveforms (IMRPhenomD or similar) to extract M_chirp, distance d, sky position.

3. **Residual analysis**: Compute residual r(t) = h_LISA(t) − h_GR(t). Project onto scalar template:

```
h_scalar(t) = ε × F^s(t) × h_tensor(t)
```

where ε = h_scalar/h_tensor is the parameter to constrain.

4. **Matched filter**: Compute signal-to-noise ratio SNR_s = ∫ |h̃_s(f)|² / S_n(f) df, where S_n(f) is the LISA noise power spectral density.

### 2.3 LISA sensitivity to h_scalar/h_tensor

LISA noise PSD for the A, E, T TDI channels (approximate):

```
S_n(f) ≈ 2.4×10⁻⁴⁴ × (1 + (f/f_*)) + 8.9×10⁻⁵⁶ f⁻⁴   Hz⁻¹
```

with f_* = 3×10⁻³ Hz (LISA transfer frequency).

For a 10^6 M_☉ SMBH merger at d = 1 Gpc, the tensor strain SNR is ~500 (strong detection). The scalar mode SNR scales as:

```
SNR_scalar ≈ (h_scalar/h_tensor) × SNR_tensor × η_s
```

where η_s ≈ 0.3 is the scalar-mode efficiency factor (LISA polarisation overlap integral).

For 5σ detection: SNR_scalar > 5, requiring:

```
h_scalar/h_tensor > 5 / (SNR_tensor × η_s) = 5 / (500 × 0.3) = 0.033
```

**TMT prediction**: h_scalar/h_tensor ≈ 10⁻⁵ to 10⁻³ — **below LISA 5σ threshold** for a single event.

### 2.4 Stacking analysis

With N_events SMBH mergers over the LISA mission (4 years), the stacked SNR_scalar scales as √N_events:

```
SNR_scalar,stack = (h_scalar/h_tensor) × SNR_tensor × η_s × √N_events
```

For N_events = 50 (optimistic) and h_scalar/h_tensor = 10⁻³:

```
SNR_scalar,stack = 10⁻³ × 500 × 0.3 × √50 = 1.06
```

Still below 5σ. For the upper end h_scalar/h_tensor = 10⁻² (near PPN limit):

```
SNR_scalar,stack = 10⁻² × 500 × 0.3 × √50 = 10.6  → 5σ detection possible!
```

**Conclusion**: If ξv² ≈ 10⁻⁵ (at the PPN limit), stacking ~50 SMBH mergers gives a detectable scalar signal at LISA.

---

## 3. Quantitative predictions

### 3.1 TMT prediction table vs detector sensitivities

| Detector | Freq band | h_tensor floor | h_s/h_t predicted | Detectable? |
|----------|-----------|----------------|-------------------|-------------|
| **LIGO O4** | 10–1000 Hz | 10⁻²⁴ | < 10⁻⁸ | No |
| **Einstein Telescope** | 2–1000 Hz | 10⁻²⁵ | < 10⁻⁷ | No |
| **LISA (single event)** | 10⁻⁴–0.1 Hz | 10⁻²⁰ | 10⁻⁵–10⁻³ | Marginal |
| **LISA (50 stacked)** | 10⁻⁴–0.1 Hz | 10⁻²⁰ | 10⁻³–10⁻² | Yes (if ξv²≈10⁻⁵) |
| **μAres (proposed)** | 10⁻⁶–10⁻² Hz | 10⁻²² | 10⁻⁴–10⁻² | Likely |

### 3.2 Polarisation signature

The scalar mode appears as an **isotropic (monopole) strain component** in LISA's TDI combination:

- **T channel** of LISA (Sagnac combination): sensitive to scalar breathing mode but not to tensor modes
- TMT predicts a non-zero T-channel signal correlated with the A, E channels during SMBH mergers

Current constraints from LIGO (GW170817, GW190521): |h_scalar/h_tensor| < 0.03. **Compatible with TMT upper bound 0.01**.

### 3.3 Frequency dependence

Channel A (strong-field): h_scalar/h_tensor ≈ const (frequency-independent)
Channel B (curvature-sourced): h_scalar/h_tensor ∝ f² (rises at higher frequency)

Distinguishing A vs B provides additional information on the temporon mass m_ψ:
- Flat spectrum → Channel A dominant → large compactness, m_ψ unconstrained
- Rising spectrum → Channel B dominant → m_ψ < 2πf_min ≈ 10⁻³³ eV

---

## 4. Falsification criteria

| Criterion | TMT prediction | ΛCDM | Result if measured |
|-----------|---------------|------|-------------------|
| h_scalar/h_tensor (SMBH mergers) | 10⁻⁵ to 10⁻² | 0 (exactly) | TMT if >10⁻⁵; ΛCDM if consistent with 0 |
| LISA T-channel excess | correlated with A,E during mergers | zero | TMT if r(T,A) > 3σ at merger time |
| Frequency dependence | flat or rising | N/A | Determines Channel A vs B regime |
| LIGO stellar binaries | < 10⁻⁸ | 0 | Both consistent; no LIGO constraint |

**TMT is FALSIFIED if**:
- LISA constrains h_scalar/h_tensor < 10⁻⁷ from stacking 50 SMBH events (rules out ξv² > 10⁻⁸)

**TMT is SUPPORTED if**:
- LISA T-channel shows excess at >2σ correlated with SMBH merger events
- The scalar/tensor ratio is consistent with ξv² ∈ [10⁻⁸, 10⁻⁵]
- Frequency spectrum is flat (Channel A) or rising (Channel B)

---

## 5. Current status and timeline

| Milestone | Status | Date |
|-----------|--------|------|
| TMT tensor formulation (scalar GW predicted) | ✅ Done | Apr 2026 |
| LIGO O4 upper limit on breathing mode | ✅ ~0.03 | 2024 |
| LISA launch | Pending | 2035 |
| LISA first SMBH merger detections | Pending | 2036–2037 |
| 50 stacked SMBH events (sensitivity target) | Pending | 2039–2041 |
| μAres science operations | Pending (proposed) | 2045+ |

The script `scripts/validation/predict_scalar_gw_mode.py` generates:
1. h_scalar/h_tensor as function of ξv², m_ψ, and source parameters
2. LISA SNR prediction vs number of stacked events
3. Comparison plot: TMT prediction vs LIGO/LISA/ET sensitivity curves

---

## References

```
[1] Amaro-Seoane P. et al. (LISA Consortium), 2017, arXiv:1702.00786
[2] Abbott B. P. et al. (LIGO/Virgo), 2017, Phys. Rev. Lett. 119, 161101 (GW170817)
[3] Isi M. et al., 2017, Phys. Rev. D 96, 042001 (GW polarisation tests)
[4] Chatziioannou K. et al., 2012, Phys. Rev. D 86, 022004 (scalar GW)
[5] Sesana A. et al., 2021, Exp. Astron. 51, 1333 (LISA SMBH science)
[6] TMT v2.4, docs/en/FULL_TENSOR_FORMULATION_TMT.md, 2026
[7] Rubbo L. J. et al., 2004, Phys. Rev. D 69, 082003 (LISA response functions)
```
