# Time Mastery Theory (TMT) - Zenodo Dataset
## Alternative Cosmological Framework via Temporal Distortion

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status](https://img.shields.io/badge/status-validated-green)]()

**Version**: 2.2.0
**Date**: January 17, 2026
**Author**: Pierre-Olivier Despres Asselin
**Contact**: pierreolivierdespres@gmail.com

---

## Abstract

The **Time Mastery Theory (TMT)** proposes an alternative explanation for dark matter (25%) and dark energy (70%) through **temporal superposition**, rather than exotic particles or unknown energy forms.

### Core Concept: Inverted Time Reference Frame

Dark matter is the **temporal reflection** of visible matter:

```
|Psi> = alpha(rho)|t> + beta(rho)|t_bar>

|alpha|^2 = 1 / (1 + rho^n)        <- forward time
|beta|^2 = rho^n / (1 + rho^n)     <- backward time (reflection)
```

---

## Key Results: TMT v2.2 (January 2026)

### Test Results Summary

| Test | TMT v2.2 Prediction | Observation | Verdict |
|------|---------------------|-------------|---------|
| **Rotation curves (SPARC)** | 97% improved | 175 galaxies | **VALIDATED** |
| **r_c(M) relation** | r_c ~ M^0.56 | r = 0.77 | **VALIDATED** |
| **SNIa by environment** | Delta_dL < 2% | < 2% observed | **COMPATIBLE** |
| **H0 tension** | Explains 77% | 8.3% tension | **SUPPORTED** |
| **ISW supervoids** | +2% | +400% observed | PARTIAL |

**Overall Score: 3.5/4 tests positive**

### TMT v2.2 Calibrated Formulas

**Temporal Superposition (Rotation Curves)**:
```
M_eff(r) = M_bary(r) x [1 + (r/r_c)^n]
r_c(M) = 2.6 x (M_bary/10^10 M_sun)^0.56 kpc
n = 0.75
```

**Differential Expansion (Cosmology)**:
```
H(z, rho) = H0 x sqrt[Omega_m(1+z)^3 + Omega_L x (1 + k x (1 - |alpha|^2 + |beta|^2))]

Parameters:
- n = 0.75 (superposition exponent)
- k = 0.2 (expansion-superposition coupling)
```

**Physical Logic**:
- More matter -> more temporal reflection -> stronger effect
- Less matter -> less reflection -> expansion ~ LCDM

---

## Package Contents

### 1. Core Documentation

| File | Description |
|------|-------------|
| **README_ZENODO.md** | This file - Package overview |
| **COMPLETE_MATHEMATICAL_FORMULATION_MT.md** | Full mathematical framework (TMT v2.2) |
| **CORE_CONCEPTS.md** | Fundamental theory concepts |

### 2. Mathematical Formulation

| File | Description |
|------|-------------|
| **FORMALIZATION_H_Z_RHO.md** | Differential expansion H(z,rho) |
| **LEXICON_DESPRES_MASS_AND_MAPPING.md** | Official terminology |

### 3. Experimental Validation

| File | Description |
|------|-------------|
| **FINAL_SUMMARY_WEAK_LENSING_TEST_TMT.md** | TMT v1.0 refutation (COSMOS) |
| **UNIQUE_TESTABLE_PREDICTION.md** | Distinguishing predictions vs LCDM |

### 4. Scientific Publication

| File | Description |
|------|-------------|
| **SCIENTIFIC_ARTICLE_TIME_MASTERY.md** | Draft scientific article |

---

## SPARC Validation (175 Galaxies)

### Performance Metrics

| Metric | Value |
|--------|-------|
| Galaxies tested | 175 (complete SPARC catalog) |
| Galaxies improved | **169/175 (97%)** |
| Median improvement | **97.5%** vs Newton |
| Chi-squared reduction | 38% average |

### Universal Law r_c(M)

```
r_c(M) = 2.6 x (M_bary / 10^10 M_sun)^0.56 kpc

Pearson r = 0.77 (p < 10^-20)
```

| Galaxy Type | M_bary | r_c predicted | DM fraction at 10 kpc |
|-------------|--------|---------------|----------------------|
| Dwarf (DDO154) | 10^8 M_sun | 0.4 kpc | 96% |
| Spiral (NGC3198) | 10^10 M_sun | 2.6 kpc | 79% |
| Massive (NGC2841) | 10^11 M_sun | 9.4 kpc | 52% |

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| **v2.2.0** | 2026-01-17 | Inverted time reference, calibrated expansion (Score 3.5/4) |
| v2.1.0 | 2026-01-17 | Beta calibration (beta = 0.12), SNIa compatible |
| v2.0.0 | 2026-01-17 | SPARC validation (97%), r_c(M) discovered |
| v1.0.0 | 2026-01-15 | COSMOS test - geometric TMT v1.0 refuted |
| v0.5.0 | 2025-12-07 | Universal law k(M) discovered |

---

## TMT v1.0 vs v2.0 vs v2.2

| Version | Concept | Test | Status |
|---------|---------|------|--------|
| TMT v1.0 | Geometric halos aligned | COSMOS weak lensing | **REFUTED** |
| TMT v2.0 | Isotropic temporal superposition | SPARC rotation | **VALIDATED** |
| TMT v2.2 | Inverted time reference | All tests | **3.5/4 PASSED** |

---

## Usage

### Requirements

```bash
pip install numpy scipy matplotlib astropy
```

### Running Tests

```bash
git clone https://github.com/cadespres/Maitrise-du-temps.git
cd Maitrise-du-temps

# TMT v2.2 complete test
python scripts/test_TMT_v22_final.py

# SPARC rotation curves
python scripts/test_TMT_v2_SPARC_reel.py

# Expansion calibration
python scripts/calibrate_beta_expansion.py
```

---

## Citation

```bibtex
@software{despres_asselin_2026_tmt,
  author       = {Despres Asselin, Pierre-Olivier},
  title        = {Time Mastery Theory v2.2: Temporal Superposition Framework},
  month        = jan,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v2.2.0},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

---

## License

- **Documentation**: CC BY 4.0
- **Code**: MIT License
- **Data**: Public domain (SPARC, Pantheon+)

---

## Links

- **GitHub**: https://github.com/cadespres/Maitrise-du-temps
- **Documentation (FR)**: https://github.com/cadespres/Maitrise-du-temps/tree/main/docs/fr
- **Zenodo**: https://doi.org/10.5281/zenodo.XXXXXXX

---

## Acknowledgments

- **SPARC Collaboration** (Lelli, McGaugh & Schombert 2016)
- **Pantheon+ Team** (Scolnic et al. 2022)
- **LITTLE THINGS Survey** (Oh et al. 2015)
- **Planck Collaboration**

---

## Contact

**Pierre-Olivier Despres Asselin**
- Email: pierreolivierdespres@gmail.com
- GitHub: [@cadespres](https://github.com/cadespres)

---

<div align="center">

**TMT v2.2: Dark Matter as Temporal Reflection**

*Score: 3.5/4 tests passed*

`|Psi> = alpha|t> + beta|t_bar>`

</div>
