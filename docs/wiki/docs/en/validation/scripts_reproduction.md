# Reproduction Scripts

This page provides all Python scripts needed to reproduce the 8 validation tests of TMT v2.4.

## Prerequisites

### Installing dependencies

```bash
pip install numpy scipy matplotlib astropy
```

### Data structure

```
Maitrise-du-temps/
├── data/
│   ├── sparc/
│   │   ├── SPARC_Lelli2016c.mrt
│   │   └── MassModels_Lelli2016c.mrt
│   └── Pantheon+/
│       └── Pantheon+SH0ES.dat
└── scripts/
    └── [scripts below]
```

---

## Tests and Scripts Table

| Test | Result | Script | Data |
|------|--------|--------|------|
| [SPARC rotation curves](#1-sparc-rotation-curves) | 156/156 (100%) | `test_TMT_v2_SPARC_reel.py` | SPARC |
| [r_c(M) law](#2-rcm-law) | r = 0.768 | `investigation_r_c_variation.py` | SPARC |
| [k(M) law](#3-km-law) | R² = 0.64 | `test_TMT_v2_SPARC_reel.py` | SPARC |
| [Weak Lensing Isotropy](#4-weak-lensing-isotropy) | -0.024% | `test_weak_lensing_TMT_vs_LCDM.py` | COSMOS |
| [COSMOS2015 Mass-Env](#5-cosmos2015-mass-environment) | r = 0.150 | `test_weak_lensing_TMT_vs_LCDM_real_data.py` | COSMOS2015 |
| [SNIa by environment](#6-snia-by-environment) | pred: 0.57% | `test_3_predictions_TMT.py` | Pantheon+ |
| [ISW Effect](#7-isw-effect) | pred: 18.2% | `calculate_ISW_improved.py` | Planck |
| [Hubble Tension](#8-hubble-tension) | 100% resolved | `calibrate_TMT_v23_cosmologie.py` | Planck+SH0ES |

---

## Data Sources

### SPARC (Included in repository)

SPARC data is included in `data/sparc/`. Original source:

- **URL**: [http://astroweb.cwru.edu/SPARC/](http://astroweb.cwru.edu/SPARC/)
- **Reference**: Lelli, McGaugh & Schombert (2016), AJ 152, 157
- **Files**:
    - `SPARC_Lelli2016c.mrt`: Properties of 175 galaxies
    - `MassModels_Lelli2016c.mrt`: Rotation curves

### Pantheon+ (Included in repository)

Pantheon+ data is included in `data/Pantheon+/`. Original source:

- **URL**: [https://github.com/PantheonPlusSH0ES/DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease)
- **Reference**: Scolnic et al. (2022), ApJ 938, 113
- **File**: `Pantheon+SH0ES.dat` (1701 Type Ia supernovae)

### COSMOS2015 (External download)

- **URL**: [CDS VizieR](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/224/24)
- **Reference**: Laigle et al. (2016), ApJS 224, 24
- **Helper script**: `scripts/download_cosmos_auto.py`

### Planck CMB (Public data)

- **URL**: [Planck Legacy Archive](https://pla.esac.esa.int/)
- **Reference**: Planck Collaboration (2020), A&A 641, A6

---

## Detailed Scripts

### 1. SPARC Rotation Curves

**Result**: 156/156 galaxies (100%) | **File**: `test_TMT_v2_SPARC_reel.py`

This script tests TMT v2.0 formulation on the 175 real SPARC galaxies (156 retained after quality filtering).

**Execution**:
```bash
cd scripts
python test_TMT_v2_SPARC_reel.py
```

**Expected output**: `data/results/TMT_v2_SPARC_reel_results.txt`

??? note "Show source code"
    ```python
    #!/usr/bin/env python3
    """
    Test TMT v2.0 with REAL SPARC data (175 galaxies)
    Calibration of k = a × (M/10^10)^b law
    
    Data: http://astroweb.cwru.edu/SPARC/
    Reference: Lelli, McGaugh & Schombert (2016)
    """
    
    import numpy as np
    from scipy.optimize import minimize_scalar, curve_fit
    from pathlib import Path
    import warnings
    warnings.filterwarnings('ignore')
    
    # Constants
    G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
    C_KMS = 299792.458  # km/s
    
    # TMT v2.0 parameters
    R_C_DEFAULT = 18.0  # kpc - calibrated critical radius
    N_DEFAULT = 1.6     # calibrated exponent
    
    # ... [Full code available on GitHub]
    ```

[:material-download: Download full script](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py){ .md-button }

---

### 2. r_c(M) Law

**Result**: r = 0.768 (p < 10⁻²¹) | **File**: `investigation_r_c_variation.py`

This script analyzes the dependence of critical radius r_c on baryonic mass.

**Execution**:
```bash
cd scripts
python investigation_r_c_variation.py
```

**Discovered relation**:
```
r_c(M) = 2.6 × (M_bary / 10¹⁰ M_☉)^0.56 kpc
```

??? note "Show source code"
    ```python
    #!/usr/bin/env python3
    """
    INVESTIGATION r_c: Why 5 vs 10 vs 18 kpc?
    
    Analysis of different r_c values obtained by different methods.
    Discovery: r_c depends on baryonic mass!
    
    Author: Pierre-Olivier Després Asselin
    Date: January 2026
    """
    
    import numpy as np
    from scipy.optimize import minimize
    from pathlib import Path
    
    # Constants
    G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
    
    # ... [Full code available on GitHub]
    ```

[:material-download: Download full script](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/investigation_r_c_variation.py){ .md-button }

---

### 3. k(M) Law

**Result**: R² = 0.64 | **File**: `test_TMT_v2_SPARC_reel.py`

The k(M) law is calibrated in the same script as rotation curves.

**Calibrated law**:
```
k = 3.97 × (M/10¹⁰)^(-0.48)
```

---

### 4. Weak Lensing Isotropy

**Result**: -0.024% | **File**: `test_weak_lensing_TMT_vs_LCDM.py`

This script tests if dark matter halos are isotropic (TMT v2.0) or aligned (TMT v1.0 refuted).

**Execution**:
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM.py
```

??? note "Show source code"
    ```python
    #!/usr/bin/env python3
    """
    PRIMARY TEST: Asymmetric Halos - TMT vs ΛCDM Prediction
    
    TMT v2.0 PREDICTION (ISOTROPIC):
      Halos are spherical, no preferential alignment.
      Expected correlation: r ≈ 0.00 ± 0.05
    
    RESULT: r = -0.024% → TMT v2.0 VALIDATED (isotropic)
    """
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import pearsonr, spearmanr
    
    # ... [Full code available on GitHub]
    ```

[:material-download: Download full script](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM.py){ .md-button }

---

### 5. COSMOS2015 Mass-Environment

**Result**: r = 0.150 | **File**: `test_weak_lensing_TMT_vs_LCDM_real_data.py`

Analysis of mass-environment correlation on real COSMOS2015 data.

**Required data**: Download COSMOS2015 from VizieR

**Execution**:
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM_real_data.py
```

[:material-download: Download full script](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py){ .md-button }

---

### 6. SNIa by Environment

**Result**: pred: 0.57% | **File**: `test_3_predictions_TMT.py`

Test of differential expansion H(z,ρ) via Type Ia supernovae in different environments.

**Execution**:
```bash
cd scripts
python test_3_predictions_TMT.py
```

??? note "Show source code"
    ```python
    #!/usr/bin/env python3
    """
    TEST OF 3 DISTINCTIVE TMT v2.0 PREDICTIONS
    
    1. SNIa by environment: Delta_dL = 5-10% (void vs cluster)
    2. ISW amplified +26% in supervoids
    3. r_c(M) validation by cross-validation
    
    Author: Pierre-Olivier Després Asselin
    Date: January 2026
    """
    
    import numpy as np
    from scipy.integrate import quad
    from scipy.stats import pearsonr, ttest_ind
    
    H0 = 70  # km/s/Mpc
    Omega_m = 0.315
    Omega_Lambda = 0.685
    beta = 0.4  # TMT parameter
    
    # ... [Full code available on GitHub]
    ```

[:material-download: Download full script](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_3_predictions_TMT.py){ .md-button }

---

### 7. ISW Effect

**Result**: pred: 18.2% | **File**: `calculate_ISW_improved.py`

Calculation of the Integrated Sachs-Wolfe (ISW) effect for TMT vs ΛCDM.

**Execution**:
```bash
cd scripts
python calculate_ISW_improved.py
```

??? note "Show source code"
    ```python
    #!/usr/bin/env python3
    """
    Improved ISW (Integrated Sachs-Wolfe) effect calculation
    Comparison TMT v2.0 vs LCDM
    
    The ISW effect measures the gravitational potential variation
    as CMB photons traverse structures:
    
    Delta_T/T = 2/c² × ∫(dΦ/dt × dl)
    """
    
    import numpy as np
    from scipy.integrate import quad, odeint
    
    H0 = 70.0          # km/s/Mpc
    Omega_m = 0.315
    Omega_Lambda = 0.685
    beta = 0.4         # TMT parameter
    
    # ... [Full code available on GitHub]
    ```

[:material-download: Download full script](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calculate_ISW_improved.py){ .md-button }

---

### 8. Hubble Tension

**Result**: 100% resolved | **File**: `calibrate_TMT_v23_cosmologie.py`

Demonstration of H₀ tension resolution via the temporon field.

**Execution**:
```bash
cd scripts
python calibrate_TMT_v23_cosmologie.py
```

**Principle**: 
```
Φ_T(ρ=1) = 0 → CMB = ΛCDM exactly
Φ_T(ρ<1) > 0 → H_local > H_CMB (local void)
```

[:material-download: Download full script](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calibrate_TMT_v23_cosmologie.py){ .md-button }

---

## Complete Execution

To reproduce all tests:

```bash
# Clone repository
git clone https://github.com/cadespres/Maitrise-du-temps.git
cd Maitrise-du-temps

# Install dependencies
pip install numpy scipy matplotlib astropy

# Run main tests
cd scripts
python test_TMT_v2_SPARC_reel.py          # SPARC + k(M)
python investigation_r_c_variation.py      # r_c(M)
python test_3_predictions_TMT.py           # SNIa + ISW + validation
python test_weak_lensing_TMT_vs_LCDM.py   # Weak lensing
python calculate_ISW_improved.py           # Detailed ISW
python calibrate_TMT_v23_cosmologie.py     # H0 tension
```

---

## Expected Results

| Test | Expected Value | Meaning |
|------|----------------|---------|
| SPARC | 156/156 (100%) | All galaxies improved vs Newton |
| r_c(M) | r = 0.768 | Strong r_c - mass correlation |
| k(M) | R² = 0.64 | Good power law fit |
| Weak Lensing | ~0% | Isotropic halos confirmed |
| SNIa | <2% Δd_L | Compatible with observations |
| ISW | ~18% | Detectable effect |
| H₀ | 0σ tension | Complete resolution |

---

**Overall statistical significance**: p = 10⁻¹¹² (>15σ) | Chi² reduction: 81.2%

*All scripts are under MIT license and can be freely used and modified.*
