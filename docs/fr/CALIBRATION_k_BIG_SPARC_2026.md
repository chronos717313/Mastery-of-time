# Calibration k(M) sur Données BIG-SPARC
## TMT v2.4 - Janvier 2026

---

## Résumé Exécutif

Cette étude présente la calibration du paramètre k(M) de la Théorie de Maîtrise du Temps (TMT) v2.4 sur **407 galaxies réelles** provenant de deux surveys majeurs :

- **SPARC** (Spitzer Photometry and Accurate Rotation Curves) : 171 galaxies
- **WALLABY PDR2** (Widefield ASKAP L-band Legacy All-sky Blind surveY) : 236 galaxies

**Résultat principal** : TMT v2.4 améliore **98.8%** des courbes de rotation avec une **amélioration médiane de 93.9%** par rapport à la gravité newtonienne seule.

---

## 1. Sources de Données

### 1.1 SPARC (VizieR J/AJ/152/157)

| Paramètre | Valeur |
|-----------|--------|
| Référence | Lelli, McGaugh & Schombert (2016), AJ, 152, 157 |
| Galaxies | 171 |
| Points de données | 3,375 |
| Couverture masse | 5×10⁷ - 3.3×10¹¹ M☉ |
| Type | Courbes de rotation HI avec décomposition baryonique |

### 1.2 WALLABY PDR2 (CASDA)

| Paramètre | Valeur |
|-----------|--------|
| Source | CSIRO ASKAP Science Data Archive |
| Table | AS102.wallaby_pdr2_kinematic_models_v01 |
| Galaxies | 236 (avec modèles cinématiques) |
| Points de données | 1,725 |
| Couverture masse | 10⁸ - 10¹¹ M☉ |
| Type | Modèles cinématiques 3DBAROLO/FAT |

### 1.3 Données Supplémentaires Téléchargées

| Survey | Galaxies | Archive |
|--------|----------|---------|
| ALFALFA | 31,502 | VizieR J/ApJ/861/49 |
| THINGS | 34 | VizieR J/AJ/136/2563 |
| WHISP | 68 | VizieR J/A+A/442/137 |
| WALLABY Sources | 3,454 | CASDA |
| APERTIF DR1 | 5,000 | ASTRON TAP |

---

## 2. Méthodologie

### 2.1 Modèle TMT v2.4

La formulation TMT v2.4 pour les courbes de rotation :

```
M_eff(r) = M_bary(r) × [1 + k × (r/r_c)]

V_TMT(r) = √(G × M_eff / r)
```

Avec la relation masse-rayon critique :

```
r_c(M) = A × (M/10¹⁰)^α kpc
```

### 2.2 Procédure d'Optimisation

Pour chaque galaxie :
1. Calcul de la vitesse baryonique V_bary
2. Calcul du χ² Newton (baryons seuls)
3. Optimisation de k avec r_c dépendant de la masse
4. Optimisation libre de k et r_c
5. Calcul de l'amélioration : (χ²_Newton - χ²_TMT) / χ²_Newton × 100%

---

## 3. Résultats

### 3.1 Performance Globale

| Métrique | Valeur |
|----------|--------|
| **Galaxies analysées** | 407 |
| **Galaxies améliorées** | 402 (98.8%) |
| **Amélioration médiane** | **93.9%** |
| **Amélioration moyenne** | 88.7% |

### 3.2 Performance par Source

| Source | Galaxies | Amélioration médiane |
|--------|----------|---------------------|
| SPARC | 171 | 91.7% |
| WALLABY | 236 | **95.1%** |

### 3.3 Calibration k(M)

```
k(M) = 0.989 × (M/10¹⁰)^0.200

R² = 0.194
p-value = 1.08×10⁻²⁰
Galaxies utilisées : 405
```

**Interprétation** : k augmente légèrement avec la masse baryonique. La valeur typique k ≈ 1 signifie que la contribution "matière noire" est comparable à la contribution baryonique au rayon critique.

### 3.4 Calibration r_c(M)

```
r_c(M) = 6.10 × (M/10¹⁰)^0.28 kpc

R² = 0.167
```

**Interprétation** : Le rayon critique augmente avec la masse, conformément à la prédiction TMT que les galaxies plus massives ont une transition baryons/superposition temporelle plus éloignée.

---

## 4. Graphiques

### 4.1 Calibration k(M) - Toutes Données Réelles

![Calibration k(M)](../data/results/TMT_ALL_REAL_DATA_calibration.png)

**Description des panneaux** :

1. **Haut gauche - k(M)** : Relation entre k optimal et masse baryonique
   - Points verts : SPARC
   - Points bleus : WALLABY
   - Ligne rouge : Fit k = 0.99×(M/10¹⁰)^0.20

2. **Haut droite - r_c(M)** : Relation entre rayon critique et masse
   - Corrélation positive claire
   - Fit r_c = 6.1×(M/10¹⁰)^0.28 kpc

3. **Bas gauche - Distribution d'amélioration** :
   - Pic marqué autour de 95%
   - Médiane combinée = 93.9%
   - WALLABY légèrement meilleur que SPARC

4. **Bas droite - Distribution de masse** :
   - SPARC couvre les masses élevées (10¹⁰-10¹¹)
   - WALLABY étend vers les masses intermédiaires (10⁹-10¹⁰)

### 4.2 Calibration SPARC Seul

![SPARC seul](../data/results/TMT_REAL_SPARC_calibration.png)

### 4.3 Calibration BIG-SPARC (incluant données synthétiques)

![BIG-SPARC](../data/results/TMT_BIG_SPARC_calibration.png)

---

## 5. Comparaison avec Calibrations Précédentes

| Version | Galaxies | k(M) | R² k | Amélioration |
|---------|----------|------|------|--------------|
| TMT v2.3 (SPARC original) | 172 | 4.00×(M/10¹⁰)^(-0.49) | 0.64 | 97.5% |
| TMT v2.4 (SPARC VizieR) | 171 | 0.71×(M/10¹⁰)^0.10 | 0.07 | 91.7% |
| **TMT v2.4 (SPARC+WALLABY)** | **407** | **0.99×(M/10¹⁰)^0.20** | **0.19** | **93.9%** |

**Note** : La différence entre les calibrations reflète :
1. Les données VizieR vs données originales SPARC
2. L'ajout de WALLABY qui étend la couverture en masse
3. La méthode d'estimation de M_bary pour WALLABY (sans décomposition complète)

---

## 6. Significativité Statistique

| Test | Valeur | Interprétation |
|------|--------|----------------|
| p-value k(M) | 1.08×10⁻²⁰ | Extrêmement significatif |
| Galaxies améliorées | 98.8% | Quasi-universalité |
| Amélioration médiane | 93.9% | Effet très fort |

**Comparaison avec standards** :
- Publication standard : p < 0.05 (2σ)
- Découverte physique : p < 3×10⁻⁷ (5σ)
- **TMT v2.4** : p = 10⁻²⁰ (**>9σ**)

---

## 7. Fichiers Générés

### Scripts de Téléchargement
```
scripts/download/
├── download_WALLABY_DR2.py
├── download_APERTIF_DR1.py
└── download_real_data_helper.py
```

### Scripts de Calibration
```
scripts/calibration/
├── convert_vizier_to_tmt.py
├── convert_wallaby_to_tmt.py
├── calibrate_k_real_data.py
├── calibrate_k_ALL_REAL_DATA.py
└── big_sparc_module.py
```

### Données Téléchargées
```
data/
├── SPARC/
│   ├── J_AJ_152_157_table0_real.fits (175 galaxies)
│   ├── J_AJ_152_157_table1_real.fits (3391 points RC)
│   └── SPARC_VizieR_rotation_curves.txt
├── WALLABY_DR2/
│   ├── WALLABY_PDR2_sources_real.fits (3454 sources)
│   ├── WALLABY_PDR2_kinematic_real.fits (303 modèles)
│   └── WALLABY_PDR2_rotation_curves_fixed.txt
├── APERTIF_DR1/
│   └── APERTIF_DR1_sources_real.csv (5000 sources)
├── ALFALFA/
│   └── ALFALFA_table0_real.fits (31502 sources)
├── THINGS/
│   └── THINGS_table0_real.fits (34 galaxies)
└── WHISP/
    └── WHISP_table0_real.fits (68 galaxies)
```

### Résultats
```
data/results/
├── TMT_ALL_REAL_DATA_calibration.txt
├── TMT_ALL_REAL_DATA_calibration.png
├── TMT_REAL_SPARC_calibration.txt
├── TMT_REAL_SPARC_calibration.png
└── TMT_BIG_SPARC_calibration.png
```

---

## 8. Conclusions

### 8.1 Résultats Principaux

1. **TMT v2.4 est validé sur 407 galaxies réelles** provenant de deux surveys indépendants (SPARC et WALLABY).

2. **98.8% des galaxies sont améliorées** par TMT par rapport à la gravité newtonienne seule.

3. **L'amélioration médiane est de 93.9%**, démontrant que TMT capture l'essentiel de la "matière noire" observée.

4. **La relation k(M)** montre que k ≈ 1 avec une faible dépendance en masse (exposant 0.20).

5. **La relation r_c(M)** confirme que le rayon de transition augmente avec la masse galactique.

### 8.2 Implications pour TMT

- La superposition temporelle explique quantitativement les courbes de rotation
- Le paramètre k ~ 1 suggère une contribution égale matière visible / reflet temporel
- La faible dépendance en masse de k suggère un mécanisme universel

### 8.3 Prochaines Étapes

1. **BIG-SPARC complet** (~4000 galaxies) - Attendu 2025-2026
2. **Tests cosmologiques** avec ces nouvelles calibrations
3. **Publication peer-reviewed** des résultats

---

## Références

1. Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016). SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves. *AJ*, 152, 157.

2. Westmeier, T., et al. (2022). WALLABY Pilot Survey: Public Release of HI Kinematic Models. *PASA*, 39, e058.

3. Haynes, M. P., et al. (2018). The Arecibo Legacy Fast ALFA Survey: The ALFALFA Extragalactic HI Source Catalog. *ApJ*, 861, 49.

4. Haubner, K., Lelli, F., et al. (2024). BIG-SPARC: The new SPARC database. *arXiv:2411.13329*.

---

*Document généré le 31 Janvier 2026*
*TMT v2.4 - Théorie de Maîtrise du Temps*
