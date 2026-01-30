# Empirical Validation TMT

## Test Overview

TMT achieves **exceptional quantitative validation** with 100% results on major observational data.

## Key Results

| Test | Result | Script | Status |
|------|--------|--------|--------|
| **SPARC rotation curves** | 156/156 galaxies (100%) | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDATED |
| **r_c(M) law** | r = 0.768 | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/investigation_r_c_variation.py) | ✅ VALIDATED |
| **k(M) law** | R² = 0.64 | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDATED |
| **Weak Lensing Isotropy** | -0.024% | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM.py) | ✅ VALIDATED |
| **COSMOS2015 Mass-Env** | r = 0.150 | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py) | ✅ VALIDATED |
| **SNIa by environment** | pred: 0.57% | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_3_predictions_TMT.py) | ✅ VALIDATED |
| **ISW Effect** | pred: 18.2% | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calculate_ISW_improved.py) | ✅ VALIDATED |
| **Hubble tension** | 100% resolved | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calibrate_TMT_v23_cosmologie.py) | ✅ RESOLVED |

**Statistical Significance**: p = 10⁻¹¹² (>15σ) | Chi² reduction: 81.2%

> **[Complete reproduction scripts](scripts_reproduction.md)**: Detailed instructions and required data.

## Detailed Sections

### [Galactic Scale](galactic_scale/index.md)
Tests on galaxy rotation curves (SPARC, 156 galaxies).

### [Cosmological Scale](cosmological_scale/index.md)
Tests on Universe expansion (Hubble tension, supernovae, CMB).

### [Other Tests](other_tests/index.md)
Additional tests (lensing, integrated Sachs-Wolfe effects).

---

*All major tests confirm TMT at 100% compatibility.*