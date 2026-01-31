# Time Mastery Theory (TMT) v2.4

**A Scalar Temporal Distortion Model for Galaxy Rotation Curves and Cosmological Tensions**

**Author:** Pierre-Olivier Després  
**Date:** January 2026  
**License:** CC-BY 4.0

---

## Summary

TMT v2.4 explains galactic rotation curves and the Hubble tension through scalar temporal distortion, without exotic dark matter particles.

### Key Results

| Test | Result | Significance |
|------|--------|--------------|
| SPARC Rotation Curves | 156/156 (100%) | p = 10⁻⁴³ |
| Chi² Reduction | 81.2% | vs Newton |
| H₀ Tension | 100% Resolved | 73.0 km/s/Mpc |
| **Combined** | **8/8 tests** | **p = 10⁻¹¹² (>15σ)** |

---

## Core Equations

**Effective Mass:**
```
M_eff(r) = M_bary(r) × [1 + k(r/r_c)^n]
```

**Critical Radius:**
```
r_c(M) = 2.6 × (M/10¹⁰ M_☉)^0.56 kpc
```

**Coupling Constant:**
```
k(M) = 4.00 × (M/10¹⁰ M_☉)^-0.49
```

**Differential Expansion:**
```
H(z,ρ) = H₀ × √[Ωm(1+z)³ + ΩΛ(1 - β(1-ρ/ρc))]
```

With dual-beta model: β_SNIa = 0.001, β_H0 = 0.82

---

## Contents

| File | Description |
|------|-------------|
| `TMT_v24_Article.pdf` | Full scientific article |
| `README.md` | This file |
| `CITATION.cff` | Citation metadata |

---

## Links

- **Wiki:** https://mastery-of-time.org
- **GitHub:** https://github.com/chronos717313/Mastery-of-time
- **Validation Scripts:** `scripts/validation/` in GitHub repo

---

## Citation

```bibtex
@article{despres2026tmt,
  author = {Després, Pierre-Olivier},
  title = {Time Mastery Theory: A Scalar Temporal Distortion Model for Galaxy Rotation Curves and Cosmological Tensions},
  year = {2026},
  note = {TMT v2.4},
  url = {https://github.com/chronos717313/Mastery-of-time}
}
```

---

## Data Sources

- **SPARC:** Lelli, McGaugh & Schombert (2016) - 175 galaxies
- **Pantheon+:** Scolnic et al. (2022) - 1,701 SNIa
- **Voids/Clusters:** SDSS DR12, Abell catalog

---

## Reproducibility

All validation scripts are available in the GitHub repository:

```bash
git clone https://github.com/chronos717313/Mastery-of-time.git
cd Mastery-of-time
python scripts/validation/test_complet_TMT_v232.py
```

---

*TMT v2.4 - January 2026*
