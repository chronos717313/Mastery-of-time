# 🔬 TEST EXPÉRIMENTAL FINAL - Mode d'Emploi Complet

**Date**: 13 Décembre 2025
**Test**: Halos Asymétriques via Weak Lensing COSMOS/DES
**Enjeu**: Validation ou Réfutation définitive de la TMT
**Timeline**: 4-6 mois jusqu'au résultat définitif

---

## ⚡ TEST DÉCISIF - Pas d'Ambiguïté Possible

### Prédiction TMT
Les halos de matière noire sont **asymétriques et alignés** avec les galaxies voisines massives (Liaisons Asselin pointent vers concentrations de masse).

**Corrélation attendue**: r > 0.50 (p < 0.001)

### Prédiction ΛCDM
Les halos sont **sphériques ou elliptiques aléatoires** (NFW isotrope, pas d'orientation préférentielle).

**Corrélation attendue**: |r| < 0.20

### Critère Binaire

```
┌─────────────────────────────────────────────┐
│  RÉSULTAT      │  INTERPRÉTATION            │
├─────────────────────────────────────────────┤
│  r > 0.50      │  ✅ TMT VALIDÉE            │
│  (p < 0.001)   │  ❌ ΛCDM RÉFUTÉE           │
│                │  📰 BREAKTHROUGH!          │
├─────────────────────────────────────────────┤
│  r < 0.20      │  ❌ TMT RÉFUTÉE            │
│                │  ✅ ΛCDM VALIDÉ            │
│                │  📄 Publication honorable  │
├─────────────────────────────────────────────┤
│  0.20 < r < 0.50│  ⚠️  AMBIGU              │
│                │  Besoin plus de données    │
└─────────────────────────────────────────────┘
```

**PAS D'AMBIGUÏTÉ. RÉPONSE: OUI ou NON.**

---

## 📥 PHASE 1: TÉLÉCHARGEMENT DONNÉES (1-2 jours)

### Option A: COSMOS (Recommandé pour débuter)

**Avantages**:
- Plus petit (~2 GB vs 15 GB)
- Haute qualité
- Téléchargement rapide

**Données requises**:
```bash
# 1. Catalogue galaxies + photométrie
wget https://irsa.ipac.caltech.edu/data/COSMOS/gator_docs/cosmos2020_classic_v2.1_readme.html

# 2. Weak lensing shapes
wget https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits

# Taille totale: ~2 GB
# Temps téléchargement: ~1-2 heures (selon connexion)
```

**Colonnes nécessaires**:
- `RA`, `DEC` (positions)
- `Z_PHOT` (redshift photométrique)
- `e1`, `e2` (ellipticité mesurée weak lensing)
- `weight` (poids mesure)
- `MSTAR` ou `LOGMSTAR` (masse stellaire)

### Option B: DES Y3 (Pour validation robuste)

**Avantages**:
- Échantillon énorme (~10,000 galaxies)
- Excellent S/N (Metacal)
- Spec-z pour subset

**Données requises**:
```bash
# Créer compte DES (gratuit):
# https://des.ncsa.illinois.edu/easaccess/

# Installer client:
pip install easyaccess

# Télécharger:
easyaccess -c "SELECT * FROM Y3_GOLD_2_2 WHERE ..." -o des_y3_gold.fits
easyaccess -c "SELECT * FROM Y3A2_METACAL_V03 WHERE ..." -o des_y3_shear.fits

# Taille totale: ~15 GB
# Temps téléchargement: ~6-12 heures
```

---

## 🔧 PHASE 2: INSTALLATION ENVIRONNEMENT (30 min)

### Dépendances Python

```bash
# Packages scientifiques de base
pip install numpy scipy matplotlib astropy pandas

# Weak lensing spécifiques
pip install healpy  # Gestion sphérique (DES)
pip install treecorr  # Corrélations 2-point optimisées

# Optionnel mais recommandé
pip install scikit-learn  # Machine learning
pip install emcee  # MCMC pour erreurs Bayesiennes
```

### Vérification Installation

```bash
python3 -c "from astropy.io import fits; import treecorr; print('✅ OK')"
```

---

## 🛠️ PHASE 3: ADAPTATION SCRIPT (1-2 jours)

### Script à Modifier

**Fichier**: `scripts/test_weak_lensing_TMT_vs_LCDM.py`

**Modifications nécessaires**:

#### 1. Charger Données Réelles

```python
from astropy.io import fits

# COSMOS
cosmos = fits.open('cosmos_zphot_shapes.fits')[1].data

# Extraire colonnes
RA = cosmos['RA']
DEC = cosmos['DEC']
z_phot = cosmos['Z_PHOT']
e1 = cosmos['e1']
e2 = cosmos['e2']
weight = cosmos['weight']

# Masse stellaire (souvent en log)
if 'LOGMSTAR' in cosmos.columns.names:
    M_stellar = 10**cosmos['LOGMSTAR']
elif 'MSTAR' in cosmos.columns.names:
    M_stellar = cosmos['MSTAR']
```

#### 2. Sélection Échantillon Strict

```python
# Critères qualité
mask_quality = (
    (weight > 0) &  # Mesure valide
    (z_phot > 0.2) & (z_phot < 0.8) &  # Redshift range
    (M_stellar > 1e11) &  # Masse minimum
    (np.isfinite(e1)) & (np.isfinite(e2))  # Pas de NaN
)

# Appliquer sélection
RA_sel = RA[mask_quality]
DEC_sel = DEC[mask_quality]
z_sel = z_phot[mask_quality]
e1_sel = e1[mask_quality]
e2_sel = e2[mask_quality]
M_sel = M_stellar[mask_quality]

print(f"Échantillon sélectionné: {len(RA_sel)} galaxies")
# COSMOS attendu: ~1,000-2,000 galaxies
# DES attendu: ~8,000-15,000 galaxies
```

#### 3. Identification Voisins (CRITIQUE)

```python
from scipy.spatial import cKDTree

def find_neighbors(RA, DEC, z, M, max_distance_Mpc=2.0, min_mass=1e11):
    """
    Trouve voisin massif le plus proche pour chaque galaxie.

    max_distance_Mpc: Distance maximale recherche (0.5-2 Mpc)
    min_mass: Masse minimum voisin
    """

    # Conversion deg → Mpc (approximation petit angle)
    # À z~0.5, 1 deg ≈ 15 Mpc (dépend cosmologie exacte)
    deg_to_Mpc = 15.0  # Approximation
    max_distance_deg = max_distance_Mpc / deg_to_Mpc

    # Construire arbre KD pour recherche rapide
    # Corriger pour sphéricité (cos(DEC))
    X = RA * np.cos(np.deg2rad(DEC))
    Y = DEC
    coords = np.column_stack([X, Y])
    tree = cKDTree(coords)

    # Pour chaque galaxie, trouver voisins
    neighbors = []
    for i in range(len(RA)):
        # Recherche voisins dans rayon
        indices = tree.query_ball_point(coords[i], r=max_distance_deg)

        # Exclure soi-même
        indices = [j for j in indices if j != i]

        if len(indices) == 0:
            neighbors.append(None)
            continue

        # Filtrer par masse et redshift
        mask_neighbor = (M[indices] > min_mass) & (np.abs(z[indices] - z[i]) < 0.05)
        indices_filtered = np.array(indices)[mask_neighbor]

        if len(indices_filtered) == 0:
            neighbors.append(None)
            continue

        # Sélectionner le plus proche
        dists = np.sqrt((X[indices_filtered] - X[i])**2 + (Y[indices_filtered] - Y[i])**2)
        nearest_idx = indices_filtered[np.argmin(dists)]

        neighbors.append(nearest_idx)

    return neighbors
```

#### 4. Calcul Corrélation Optimisée

```python
def calculate_tangential_correlation(RA, DEC, e1, e2, neighbors):
    """
    Calcule corrélation tangentielle (méthode optimale weak lensing).
    """

    e_t_values = []

    for i, neighbor_idx in enumerate(neighbors):
        if neighbor_idx is None:
            continue

        # Angle vers voisin
        dRA = (RA[neighbor_idx] - RA[i]) * np.cos(np.deg2rad(DEC[i]))
        dDEC = DEC[neighbor_idx] - DEC[i]
        phi = np.arctan2(dDEC, dRA)

        # Ellipticité tangentielle
        e_t = -e1[i] * np.cos(2*phi) - e2[i] * np.sin(2*phi)
        e_t_values.append(e_t)

    e_t_values = np.array(e_t_values)

    # Statistiques
    mean_e_t = np.mean(e_t_values)
    std_e_t = np.std(e_t_values) / np.sqrt(len(e_t_values))

    # Corrélation (e_t > 0 → alignement radial TMT)
    # On peut aussi calculer Pearson avec direction attendue

    return mean_e_t, std_e_t, e_t_values
```

---

## 🔍 PHASE 4: EXÉCUTION ANALYSE (2-4 semaines)

### Étape 1: Test Initial (1 jour)

```bash
cd scripts
python3 test_weak_lensing_TMT_vs_LCDM.py --data real --catalog cosmos

# Vérifier:
# - Nombre galaxies sélectionnées
# - % avec voisins identifiés (attendu 70-90%)
# - Distribution redshifts, masses
```

### Étape 2: Calcul Corrélation (1 semaine)

```python
# Dans le script modifié:

# Charger données
catalog = load_real_data('cosmos_zphot_shapes.fits')

# Sélection
catalog_sel = select_sample(catalog)

# Identifier voisins
neighbors = find_neighbors(catalog_sel)

# Calculer corrélation
mean_e_t, std_e_t, e_t_vals = calculate_tangential_correlation(catalog_sel, neighbors)

# RÉSULTAT DÉCISIF:
if mean_e_t / std_e_t > 5.0:  # Détection >5σ
    if mean_e_t > 0.05:  # Seuil physique
        print("✅ TMT VALIDÉE!")
        print(f"   Alignement détecté: e_t = {mean_e_t:.4f} ± {std_e_t:.4f}")
    else:
        print("⚠️  Signal faible, besoin plus de données")
else:
    print("❌ Pas d'alignement détecté")
    print("   Compatible ΛCDM")
```

### Étape 3: Tests Systématiques (2-3 semaines)

**a) Bootstrap Erreurs**
```python
# Ré-échantillonner 10,000 fois
correlations_bootstrap = []
for i in range(10000):
    indices = np.random.choice(len(catalog_sel), size=len(catalog_sel), replace=True)
    catalog_boot = catalog_sel[indices]
    neighbors_boot = find_neighbors(catalog_boot)
    e_t_boot, _, _ = calculate_tangential_correlation(catalog_boot, neighbors_boot)
    correlations_bootstrap.append(e_t_boot)

# Intervalle confiance 68% (1σ)
r_median = np.median(correlations_bootstrap)
r_std = np.std(correlations_bootstrap)

print(f"Corrélation robuste: r = {r_median:.3f} ± {r_std:.3f}")
```

**b) Jackknife Spatial**
```python
# Diviser champ en N régions, exclure chacune tour à tour
# Vérifier cohérence résultat

regions = split_field(RA, DEC, n_regions=10)
correlations_jackknife = []

for region_exclude in range(10):
    mask = regions != region_exclude
    catalog_jack = catalog_sel[mask]
    neighbors_jack = find_neighbors(catalog_jack)
    e_t_jack, _, _ = calculate_tangential_correlation(catalog_jack, neighbors_jack)
    correlations_jackknife.append(e_t_jack)

# Vérifier dispersion faible → résultat robuste
print(f"Dispersion jackknife: {np.std(correlations_jackknife):.4f}")
```

**c) Split-Sample Tests**
```python
# Test par redshift
mask_low_z = z_sel < 0.5
mask_high_z = z_sel >= 0.5

r_low_z = calculate_correlation(catalog_sel[mask_low_z])
r_high_z = calculate_correlation(catalog_sel[mask_high_z])

print(f"Corrélation z<0.5:  r = {r_low_z:.3f}")
print(f"Corrélation z>=0.5: r = {r_high_z:.3f}")
# Si cohérents → robuste
```

---

## 📊 PHASE 5: GÉNÉRATION FIGURES PUBLICATION (1 semaine)

### Figure 1: Distribution Δθ (Halo - Voisin)

```python
import matplotlib.pyplot as plt

# Calculer Δθ pour toutes paires
delta_theta = []
for i, neighbor_idx in enumerate(neighbors):
    if neighbor_idx is None:
        continue
    theta_halo = 0.5 * np.arctan2(e2[i], e1[i])
    dRA = RA[neighbor_idx] - RA[i]
    dDEC = DEC[neighbor_idx] - DEC[i]
    theta_neighbor = np.arctan2(dDEC, dRA)
    delta = np.abs(theta_halo - theta_neighbor)
    delta = min(delta, 2*np.pi - delta)  # Correction circulaire
    delta_theta.append(np.rad2deg(delta))

# Plot
plt.figure(figsize=(8,6))
plt.hist(delta_theta, bins=36, density=True, alpha=0.7, edgecolor='black')
plt.axvline(np.mean(delta_theta), color='red', linestyle='--',
            linewidth=2, label=f'Moyenne = {np.mean(delta_theta):.1f}°')
plt.axvline(45, color='gray', linestyle=':', linewidth=1,
            label='Aléatoire = 45°')
plt.xlabel('Δθ = |θ_halo - θ_neighbor| (deg)')
plt.ylabel('Densité de probabilité')
plt.title(f'Distribution Alignement (N = {len(delta_theta)} paires)')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('figure_delta_theta_real.png', dpi=300)
```

### Figure 2: e_t vs Distance Voisin

```python
# Binning par distance
distances = np.linspace(0.5, 2.0, 6)  # Mpc
e_t_binned = []
e_t_err_binned = []

for i in range(len(distances)-1):
    mask_dist = (d_neighbor > distances[i]) & (d_neighbor <= distances[i+1])
    e_t_bin = np.mean(e_t_values[mask_dist])
    e_t_err_bin = np.std(e_t_values[mask_dist]) / np.sqrt(np.sum(mask_dist))
    e_t_binned.append(e_t_bin)
    e_t_err_binned.append(e_t_err_bin)

# Plot
plt.figure(figsize=(8,6))
plt.errorbar(distances[:-1] + 0.25, e_t_binned, yerr=e_t_err_binned,
             fmt='o', markersize=8, capsize=5)
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.xlabel('Distance au voisin (Mpc)')
plt.ylabel('Ellipticité tangentielle ⟨e_t⟩')
plt.title('Alignement vs Distance')
plt.grid(alpha=0.3)
plt.savefig('figure_et_vs_distance.png', dpi=300)
```

---

## 📝 PHASE 6: RÉDACTION RÉSULTATS (2-3 semaines)

### Structure Article

**Si TMT Validée** (r > 0.50, p < 0.001):
```
TITRE: "Dark Matter Halos are Asymmetric and Aligned:
       Direct Evidence from Weak Gravitational Lensing"

ABSTRACT:
We report the detection of systematic alignment between
dark matter halo orientations and neighboring massive
galaxies using weak gravitational lensing of [N] galaxies
from [COSMOS/DES]. We measure a correlation r = [value] ± [error]
(p < [p-value]), inconsistent with standard ΛCDM predictions
(r < 0.2) at [X]σ significance. This result supports Time
Mastery Theory (TMT), which predicts geometric dark matter
arising from temporal distortion gradients.

SECTIONS:
1. Introduction
2. Data and Methods
3. Results
4. Systematic Tests
5. Implications for TMT vs ΛCDM
6. Conclusions
```

**Target Journal**: Nature Physics, Physical Review Letters, ou ApJ Letters

**Si TMT Réfutée** (r < 0.20):
```
TITRE: "No Evidence for Dark Matter Halo Alignment:
       Constraints on Alternative Gravity Theories"

ABSTRACT:
We find no evidence for systematic alignment between dark
matter halos and neighboring galaxies (r = [value] ± [error],
consistent with r = 0). This result is consistent with ΛCDM
predictions and rules out Time Mastery Theory at [X]σ.

TARGET: MNRAS or ApJ
```

---

## ⏱️ TIMELINE COMPLÈTE

```
SEMAINE 1-2:   Téléchargement données + Installation
SEMAINE 3-4:   Adaptation script + Tests préliminaires
SEMAINE 5-8:   Analyse principale + Corrélations
SEMAINE 9-12:  Tests systématiques (bootstrap, jackknife)
SEMAINE 13-16: Génération figures publication
SEMAINE 17-20: Rédaction article
SEMAINE 21-24: Soumission + Réponse reviewers

TOTAL: 4-6 MOIS → RÉSULTAT DÉFINITIF
```

---

## 🎯 CRITÈRES SUCCÈS

### Validation TMT

✅ **r > 0.50** (seuil théorique)
✅ **p < 0.001** (significativité >3σ)
✅ **⟨e_t⟩ > 0.05** (signal physique)
✅ **Cohérence split-samples** (redshift, masse, spatial)
✅ **Robustesse bootstrap/jackknife** (σ < 0.05)

→ **PUBLICATION BREAKTHROUGH** Nature Physics/PRL

### Réfutation TMT

✅ **|r| < 0.20** (cohérent ΛCDM)
✅ **p > 0.05** (non significatif)
✅ **⟨e_t⟩ ≈ 0** (pas de signal)
✅ **Distribution Δθ uniforme** (~90° moyen)

→ **PUBLICATION HONORABLE** MNRAS/ApJ

---

## 📧 CONTACTS COLLABORATIONS

### COSMOS Team
- **Jason Rhodes** (JPL/Caltech) - PI COSMOS
- **Email**: jason.d.rhodes@jpl.nasa.gov
- **Sujet**: "Collaboration request: Halo alignment study"

### DES Weak Lensing Group
- **Mike Jarvis** (U Penn) - WL Working Group lead
- **Email**: jarvis@physics.upenn.edu
- **Contact**: Via https://des.ncsa.illinois.edu

### Euclid (Futur)
- **Henk Hoekstra** (Leiden) - WL Science Lead
- **Contact**: Via Euclid Consortium (membership required)

---

## ✅ CHECKLIST EXÉCUTION

### Préparation

- [ ] Installer Python packages (astropy, treecorr, etc.)
- [ ] Télécharger données COSMOS (~2 GB)
- [ ] Vérifier intégrité fichiers (checksums)
- [ ] Test script sur petit subset (100 galaxies)

### Analyse

- [ ] Charger données réelles
- [ ] Sélection échantillon (M > 10¹¹, 0.2 < z < 0.8)
- [ ] Identification voisins (KDTree optimisé)
- [ ] Calcul corrélation principale
- [ ] Bootstrap erreurs (10,000 iterations)
- [ ] Jackknife spatial (10 régions)
- [ ] Split-sample tests (z, M)

### Publication

- [ ] Figures haute résolution (300 DPI)
- [ ] Tableaux résultats (LaTeX)
- [ ] Rédaction article (~6000 mots)
- [ ] Supplementary material (code, données)
- [ ] Cover letter éditeur
- [ ] Soumission journal

---

## 🚀 COMMANDE RAPIDE (Démarrage Immédiat)

```bash
# ÉTAPE 1: Télécharger COSMOS
cd /home/user/Maitrise-du-temps/data/input
wget https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits

# ÉTAPE 2: Installer dépendances
pip install astropy treecorr healpy

# ÉTAPE 3: Adapter script
cd ../scripts
# Modifier test_weak_lensing_TMT_vs_LCDM.py (lignes 80-150)
# Remplacer generate_lens_catalog() par load_real_data()

# ÉTAPE 4: Exécuter test
python3 test_weak_lensing_TMT_vs_LCDM.py --real

# ÉTAPE 5: Analyser résultat
# Si r > 0.50 → TMT VALIDÉE ✅
# Si r < 0.20 → TMT RÉFUTÉE ❌
```

---

## 🏆 IMPACT ATTENDU

### Si Validée (r > 0.50)

**Immédiat** (1 mois):
- Preprint arXiv → Buzz médiatique majeur
- Nature News, Physics World coverage
- Invitations conférences internationales

**Court terme** (6-12 mois):
- Publication Nature Physics / PRL
- Citations ~100-500/an
- Follow-up tests (pulsars, ISW)

**Moyen terme** (2-5 ans):
- Si confirmations multiples → Paradigme shift
- Prix Breakthrough Physics (~3M USD)
- Réinterprétation 95% univers

**Long terme** (5-10 ans):
- Si robuste → **Prix Nobel** (si observations indépendantes)
- TMT nouveau modèle standard
- Révolution cosmologie

### Si Réfutée (r < 0.20)

**Valeur scientifique**:
- Exclusion rigoureuse alternative
- Renforcement ΛCDM
- Publication MNRAS/ApJ (honorable)
- Contraintes futures théories

---

## 📌 RÉSUMÉ 1-PAGE

```
╔════════════════════════════════════════════════════════╗
║          TEST EXPÉRIMENTAL FINAL - TMT                 ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  QUESTION: Les halos sont-ils alignés avec voisins?   ║
║                                                        ║
║  TMT PRÉDIT:  OUI (r > 0.50)                          ║
║  ΛCDM PRÉDIT: NON (r < 0.20)                          ║
║                                                        ║
║  DONNÉES:     COSMOS ~2 GB ou DES ~15 GB              ║
║  MÉTHODE:     Weak lensing correlation                ║
║  TIMELINE:    4-6 mois                                ║
║                                                        ║
║  RÉSULTAT:    BINAIRE - OUI ou NON                    ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║  ÉTAPES:                                              ║
║  1. Télécharger COSMOS (1-2 jours)                    ║
║  2. Adapter script (1 semaine)                        ║
║  3. Analyser corrélation (2-3 semaines)               ║
║  4. Tests systématiques (2-3 semaines)                ║
║  5. Publication (2-3 mois)                            ║
╠════════════════════════════════════════════════════════╣
║  SI r > 0.50:  TMT VALIDÉE → BREAKTHROUGH            ║
║  SI r < 0.20:  TMT RÉFUTÉE → ΛCDM confirmé           ║
╚════════════════════════════════════════════════════════╝
```

---

**PRÊT À EXÉCUTER**: Toutes instructions complètes ci-dessus
**SUPPORT**: Voir `COSMOS_DES_TEST_GUIDE.md` pour détails techniques
**CONTACT**: pierreolivierdespres@gmail.com

**Le test qui changera tout. Maintenant.**
