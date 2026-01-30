# Scripts de Reproduction

Cette page fournit tous les scripts Python nécessaires pour reproduire les 8 tests de validation de TMT v2.4.

## Prérequis

### Installation des dépendances

```bash
pip install numpy scipy matplotlib astropy
```

### Structure des données

```
Maitrise-du-temps/
├── data/
│   ├── sparc/
│   │   ├── SPARC_Lelli2016c.mrt
│   │   └── MassModels_Lelli2016c.mrt
│   └── Pantheon+/
│       └── Pantheon+SH0ES.dat
└── scripts/
    └── [scripts ci-dessous]
```

---

## Tableau des Tests et Scripts

| Test | Résultat | Script | Données |
|------|----------|--------|---------|
| [Courbes de rotation SPARC](#1-courbes-de-rotation-sparc) | 156/156 (100%) | `test_TMT_v2_SPARC_reel.py` | SPARC |
| [Loi r_c(M)](#2-loi-rcm) | r = 0.768 | `investigation_r_c_variation.py` | SPARC |
| [Loi k(M)](#3-loi-km) | R² = 0.64 | `test_TMT_v2_SPARC_reel.py` | SPARC |
| [Isotropie Weak Lensing](#4-isotropie-weak-lensing) | -0.024% | `test_weak_lensing_TMT_vs_LCDM.py` | COSMOS |
| [COSMOS2015 Masse-Env](#5-cosmos2015-masse-environnement) | r = 0.150 | `test_weak_lensing_TMT_vs_LCDM_real_data.py` | COSMOS2015 |
| [SNIa par environnement](#6-snia-par-environnement) | préd: 0.57% | `test_3_predictions_TMT.py` | Pantheon+ |
| [Effet ISW](#7-effet-isw) | préd: 18.2% | `calculate_ISW_improved.py` | Planck |
| [Tension Hubble](#8-tension-hubble) | 100% résolue | `calibrate_TMT_v23_cosmologie.py` | Planck+SH0ES |

---

## Sources de Données

### SPARC (Inclus dans le dépôt)

Les données SPARC sont incluses dans `data/sparc/`. Source originale :

- **URL** : [http://astroweb.cwru.edu/SPARC/](http://astroweb.cwru.edu/SPARC/)
- **Référence** : Lelli, McGaugh & Schombert (2016), AJ 152, 157
- **Fichiers** :
    - `SPARC_Lelli2016c.mrt` : Propriétés des 175 galaxies
    - `MassModels_Lelli2016c.mrt` : Courbes de rotation

### Pantheon+ (Inclus dans le dépôt)

Les données Pantheon+ sont incluses dans `data/Pantheon+/`. Source originale :

- **URL** : [https://github.com/PantheonPlusSH0ES/DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease)
- **Référence** : Scolnic et al. (2022), ApJ 938, 113
- **Fichier** : `Pantheon+SH0ES.dat` (1701 supernovae Ia)

### COSMOS2015 (Téléchargement externe)

- **URL** : [CDS VizieR](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/224/24)
- **Référence** : Laigle et al. (2016), ApJS 224, 24
- **Script d'aide** : `scripts/download_cosmos_auto.py`

### Planck CMB (Données publiques)

- **URL** : [Planck Legacy Archive](https://pla.esac.esa.int/)
- **Référence** : Planck Collaboration (2020), A&A 641, A6

---

## Scripts Détaillés

### 1. Courbes de rotation SPARC

**Résultat** : 156/156 galaxies (100%) | **Fichier** : `test_TMT_v2_SPARC_reel.py`

Ce script teste la formulation TMT v2.0 sur les 175 galaxies SPARC réelles (156 retenues après filtrage qualité).

**Exécution** :
```bash
cd scripts
python test_TMT_v2_SPARC_reel.py
```

**Sortie attendue** : `data/results/TMT_v2_SPARC_reel_results.txt`

??? note "Afficher le code source"
    ```python
    #!/usr/bin/env python3
    """
    Test TMT v2.0 avec les VRAIES données SPARC (175 galaxies)
    Calibration de la loi k = a × (M/10^10)^b
    
    Données: http://astroweb.cwru.edu/SPARC/
    Référence: Lelli, McGaugh & Schombert (2016)
    """
    
    import numpy as np
    from scipy.optimize import minimize_scalar, curve_fit
    from pathlib import Path
    import warnings
    warnings.filterwarnings('ignore')
    
    # Constantes
    G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
    C_KMS = 299792.458  # km/s
    
    # Paramètres TMT v2.0
    R_C_DEFAULT = 18.0  # kpc - rayon critique calibré
    N_DEFAULT = 1.6     # exposant calibré
    
    # ... [Code complet disponible sur GitHub]
    ```

[:material-download: Télécharger le script complet](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py){ .md-button }

---

### 2. Loi r_c(M)

**Résultat** : r = 0.768 (p < 10⁻²¹) | **Fichier** : `investigation_r_c_variation.py`

Ce script analyse la dépendance du rayon critique r_c avec la masse baryonique.

**Exécution** :
```bash
cd scripts
python investigation_r_c_variation.py
```

**Relation découverte** :
```
r_c(M) = 2.6 × (M_bary / 10¹⁰ M_☉)^0.56 kpc
```

??? note "Afficher le code source"
    ```python
    #!/usr/bin/env python3
    """
    INVESTIGATION r_c : Pourquoi 5 vs 10 vs 18 kpc?
    
    Analyse des différentes valeurs de r_c obtenues selon les méthodes.
    Découverte: r_c dépend de la masse baryonique!
    
    Auteur: Pierre-Olivier Després Asselin
    Date: Janvier 2026
    """
    
    import numpy as np
    from scipy.optimize import minimize
    from pathlib import Path
    
    # Constantes
    G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
    
    # ... [Code complet disponible sur GitHub]
    ```

[:material-download: Télécharger le script complet](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/investigation_r_c_variation.py){ .md-button }

---

### 3. Loi k(M)

**Résultat** : R² = 0.64 | **Fichier** : `test_TMT_v2_SPARC_reel.py`

La loi k(M) est calibrée dans le même script que les courbes de rotation.

**Loi calibrée** :
```
k = 3.97 × (M/10¹⁰)^(-0.48)
```

---

### 4. Isotropie Weak Lensing

**Résultat** : -0.024% | **Fichier** : `test_weak_lensing_TMT_vs_LCDM.py`

Ce script teste si les halos de matière noire sont isotropes (TMT v2.0) ou alignés (TMT v1.0 réfuté).

**Exécution** :
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM.py
```

??? note "Afficher le code source"
    ```python
    #!/usr/bin/env python3
    """
    TEST PRIMAIRE: Halos Asymétriques - Prédiction TMT vs ΛCDM
    
    PRÉDICTION TMT v2.0 (ISOTROPE):
      Les halos sont sphériques, pas d'alignement préférentiel.
      Corrélation attendue: r ≈ 0.00 ± 0.05
    
    RÉSULTAT: r = -0.024% → TMT v2.0 VALIDÉ (isotrope)
    """
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import pearsonr, spearmanr
    
    # ... [Code complet disponible sur GitHub]
    ```

[:material-download: Télécharger le script complet](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM.py){ .md-button }

---

### 5. COSMOS2015 Masse-Environnement

**Résultat** : r = 0.150 | **Fichier** : `test_weak_lensing_TMT_vs_LCDM_real_data.py`

Analyse de la corrélation masse-environnement sur données COSMOS2015 réelles.

**Données requises** : Télécharger COSMOS2015 depuis VizieR

**Exécution** :
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM_real_data.py
```

[:material-download: Télécharger le script complet](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py){ .md-button }

---

### 6. SNIa par environnement

**Résultat** : préd: 0.57% | **Fichier** : `test_3_predictions_TMT.py`

Test de l'expansion différentielle H(z,ρ) via les supernovae Ia dans différents environnements.

**Exécution** :
```bash
cd scripts
python test_3_predictions_TMT.py
```

??? note "Afficher le code source"
    ```python
    #!/usr/bin/env python3
    """
    TEST DES 3 PREDICTIONS DISTINCTIVES TMT v2.0
    
    1. SNIa par environnement: Delta_dL = 5-10% (vide vs amas)
    2. ISW amplifié +26% dans supervides
    3. Validation r_c(M) par validation croisée
    
    Auteur: Pierre-Olivier Després Asselin
    Date: Janvier 2026
    """
    
    import numpy as np
    from scipy.integrate import quad
    from scipy.stats import pearsonr, ttest_ind
    
    H0 = 70  # km/s/Mpc
    Omega_m = 0.315
    Omega_Lambda = 0.685
    beta = 0.4  # Paramètre TMT
    
    # ... [Code complet disponible sur GitHub]
    ```

[:material-download: Télécharger le script complet](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_3_predictions_TMT.py){ .md-button }

---

### 7. Effet ISW

**Résultat** : préd: 18.2% | **Fichier** : `calculate_ISW_improved.py`

Calcul de l'effet Sachs-Wolfe intégré (ISW) pour TMT vs ΛCDM.

**Exécution** :
```bash
cd scripts
python calculate_ISW_improved.py
```

??? note "Afficher le code source"
    ```python
    #!/usr/bin/env python3
    """
    Calcul amélioré de l'effet ISW (Integrated Sachs-Wolfe)
    Comparaison TMT v2.0 vs LCDM
    
    L'effet ISW mesure la variation du potentiel gravitationnel
    pendant que les photons CMB traversent les structures:
    
    Delta_T/T = 2/c² × ∫(dΦ/dt × dl)
    """
    
    import numpy as np
    from scipy.integrate import quad, odeint
    
    H0 = 70.0          # km/s/Mpc
    Omega_m = 0.315
    Omega_Lambda = 0.685
    beta = 0.4         # Paramètre TMT
    
    # ... [Code complet disponible sur GitHub]
    ```

[:material-download: Télécharger le script complet](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calculate_ISW_improved.py){ .md-button }

---

### 8. Tension Hubble

**Résultat** : 100% résolue | **Fichier** : `calibrate_TMT_v23_cosmologie.py`

Démonstration de la résolution de la tension H₀ via le champ de temporons.

**Exécution** :
```bash
cd scripts
python calibrate_TMT_v23_cosmologie.py
```

**Principe** : 
```
Φ_T(ρ=1) = 0 → CMB = ΛCDM exactement
Φ_T(ρ<1) > 0 → H_local > H_CMB (vide local)
```

[:material-download: Télécharger le script complet](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calibrate_TMT_v23_cosmologie.py){ .md-button }

---

## Exécution Complète

Pour reproduire tous les tests :

```bash
# Cloner le dépôt
git clone https://github.com/cadespres/Maitrise-du-temps.git
cd Maitrise-du-temps

# Installer les dépendances
pip install numpy scipy matplotlib astropy

# Exécuter les tests principaux
cd scripts
python test_TMT_v2_SPARC_reel.py          # SPARC + k(M)
python investigation_r_c_variation.py      # r_c(M)
python test_3_predictions_TMT.py           # SNIa + ISW + validation
python test_weak_lensing_TMT_vs_LCDM.py   # Weak lensing
python calculate_ISW_improved.py           # ISW détaillé
python calibrate_TMT_v23_cosmologie.py     # Tension H0
```

---

## Résultats Attendus

| Test | Valeur Attendue | Signification |
|------|-----------------|---------------|
| SPARC | 156/156 (100%) | Toutes galaxies améliorées vs Newton |
| r_c(M) | r = 0.768 | Forte corrélation r_c - masse |
| k(M) | R² = 0.64 | Bon ajustement loi puissance |
| Weak Lensing | ~0% | Halos isotropes confirmés |
| SNIa | <2% Δd_L | Compatible observations |
| ISW | ~18% | Effet détectable |
| H₀ | 0σ tension | Résolution complète |

---

**Significativité statistique globale** : p = 10⁻¹¹² (>15σ) | Réduction Chi² : 81.2%

*Tous les scripts sont sous licence MIT et peuvent être librement utilisés et modifiés.*
