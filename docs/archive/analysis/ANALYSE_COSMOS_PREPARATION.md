# Analyse COSMOS : Préparation et Implémentation
## Test Corrélation θ_halo ↔ θ_voisin

**Date** : 2025-12-06
**Auteur** : Pierre-Olivier Després Asselin
**Objectif** : Tester prédiction MT avec données publiques COSMOS

---

## 1. Vue d'Ensemble COSMOS

### COSMOS Survey (Cosmic Evolution Survey)

**Site officiel** : https://cosmos.astro.caltech.edu/

**Caractéristiques** :
- **Champ** : 2 deg² (région équatoriale)
- **Profondeur** : Observations HST + Subaru + VLT
- **Galaxies** : ~2 millions de galaxies photométriques
- **Weak lensing** : ~500,000 galaxies avec mesures shear
- **Redshift** : 0.2 < z < 1.2 (photométrique)
- **Catalogues publics** : OUI ✅

**Avantages pour notre test** :
- ✅ Données weak lensing de haute qualité
- ✅ Catalogues galaxies voisines disponibles
- ✅ Redshifts photométriques précis
- ✅ Masses stellaires estimées
- ✅ Téléchargement gratuit

---

## 2. Données Nécessaires

### A) Catalogue Weak Lensing COSMOS

**Fichier** : `COSMOS_shear_catalog.fits`

**Contenu requis** :
- `RA`, `DEC` : Position (degrés)
- `z_photo` : Redshift photométrique
- `e1`, `e2` : Composantes ellipticité (shear)
- `weight` : Poids statistique
- `theta_halo` : Position angle du halo (calculé depuis e1, e2)

**Source** : COSMOS2015 catalog
**Lien** : https://cosmos.astro.caltech.edu/page/data-releases

### B) Catalogue Galaxies Massives

**Fichier** : `COSMOS_galaxies_massives.fits`

**Contenu requis** :
- `RA`, `DEC` : Position
- `z_photo` : Redshift
- `M_stellar` : Masse stellaire (M☉)
- `M_halo` : Masse du halo (estimée, si disponible)

**Critère sélection** : M_stellar > 10¹¹ M☉ (voisins massifs)

### C) Catalogue Paires Galaxie-Voisin

**À créer** : `COSMOS_paires_analyse.fits`

**Contenu** :
- ID galaxie lentille (avec weak lensing)
- θ_halo : Orientation du halo (0-180°)
- e_halo : Ellipticité du halo
- ID voisin le plus massif
- θ_voisin : Direction vers voisin (0-360°)
- M_voisin : Masse du voisin
- d_voisin : Distance projetée (Mpc)
- Δz : Différence redshift

---

## 3. Téléchargement des Données

### Script de Téléchargement

```bash
#!/bin/bash
# download_cosmos_data.sh

# Créer répertoire données
mkdir -p data/COSMOS
cd data/COSMOS

# COSMOS2015 Catalog (galaxies)
echo "Téléchargement COSMOS2015 catalog..."
wget https://cosmos.astro.caltech.edu/data/COSMOS2015_Laigle+_v1.1.fits
mv COSMOS2015_Laigle+_v1.1.fits cosmos2015_galaxies.fits

# COSMOS Shear Catalog (weak lensing)
echo "Téléchargement COSMOS shear catalog..."
wget https://cosmos.astro.caltech.edu/data/shear/cosmos_shear_v2.fits
mv cosmos_shear_v2.fits cosmos_shear.fits

# Vérification
echo "Fichiers téléchargés:"
ls -lh

echo "✓ Téléchargement terminé"
```

**Exécution** :
```bash
chmod +x download_cosmos_data.sh
./download_cosmos_data.sh
```

**Taille totale** : ~2-3 GB

---

## 4. Code Python : Préparation des Données

### Script 1 : Lecture et Nettoyage

```python
#!/usr/bin/env python3
# 01_prepare_cosmos_data.py
"""
Préparation données COSMOS pour analyse θ_halo ↔ θ_voisin
"""

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.cosmology import FlatLambdaCDM
import matplotlib.pyplot as plt

# Cosmologie
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

# ============================================
# 1. CHARGER DONNÉES COSMOS
# ============================================

def load_cosmos_shear(filename='data/COSMOS/cosmos_shear.fits'):
    """
    Charge catalogue weak lensing COSMOS
    """
    print("Chargement catalogue shear COSMOS...")

    with fits.open(filename) as hdul:
        data = hdul[1].data

    # Créer DataFrame
    df = pd.DataFrame({
        'ID': data['NUMBER'],
        'RA': data['ALPHA_J2000'],
        'DEC': data['DELTA_J2000'],
        'z_photo': data['PHOTOZ'],
        'e1': data['E1'],
        'e2': data['E2'],
        'weight': data['WEIGHT'],
        'mag_i': data['MAG_AUTO']  # Magnitude bande i
    })

    print(f"  → {len(df)} galaxies chargées")

    return df

def load_cosmos_galaxies(filename='data/COSMOS/cosmos2015_galaxies.fits'):
    """
    Charge catalogue galaxies COSMOS2015
    """
    print("Chargement catalogue galaxies COSMOS2015...")

    with fits.open(filename) as hdul:
        data = hdul[1].data

    # Créer DataFrame
    df = pd.DataFrame({
        'ID': data['NUMBER'],
        'RA': data['ALPHA_J2000'],
        'DEC': data['DELTA_J2000'],
        'z_photo': data['PHOTOZ'],
        'z_spec': data['ZQ'],  # Redshift spectroscopique si disponible
        'M_stellar': 10**data['MASS_MED'],  # Masse stellaire en M☉
        'mag_i': data['ip_MAG_AUTO']
    })

    print(f"  → {len(df)} galaxies chargées")

    return df

# ============================================
# 2. CALCULER ORIENTATION HALOS
# ============================================

def calculate_halo_orientation(e1, e2):
    """
    Calcule angle de position du halo depuis ellipticité

    θ_halo = 0.5 * arctan2(e2, e1)  [radians]

    Convention: 0° = Nord, 90° = Est
    Retourne angles dans [0, 180°] (ellipse symétrique)
    """
    theta_rad = 0.5 * np.arctan2(e2, e1)
    theta_deg = np.degrees(theta_rad)

    # Ramener à [0, 180°]
    theta_deg = theta_deg % 180

    return theta_deg

def calculate_ellipticity_modulus(e1, e2):
    """
    Calcule module ellipticité e = √(e1² + e2²)
    """
    return np.sqrt(e1**2 + e2**2)

# ============================================
# 3. SÉLECTION ÉCHANTILLON
# ============================================

def select_lensing_sample(df_shear,
                          z_min=0.2, z_max=0.6,
                          e_min=0.1, e_max=0.8,
                          weight_min=0.5):
    """
    Sélectionne galaxies avec weak lensing fiable
    """
    print("\nSélection échantillon weak lensing...")
    print(f"  Critères:")
    print(f"    {z_min} < z < {z_max}")
    print(f"    {e_min} < e < {e_max}")
    print(f"    weight > {weight_min}")

    # Calculer ellipticité
    df_shear['e_modulus'] = calculate_ellipticity_modulus(
        df_shear['e1'], df_shear['e2']
    )

    # Calculer orientation
    df_shear['theta_halo'] = calculate_halo_orientation(
        df_shear['e1'], df_shear['e2']
    )

    # Sélection
    mask = (
        (df_shear['z_photo'] >= z_min) &
        (df_shear['z_photo'] <= z_max) &
        (df_shear['e_modulus'] >= e_min) &
        (df_shear['e_modulus'] <= e_max) &
        (df_shear['weight'] >= weight_min)
    )

    df_selected = df_shear[mask].copy()

    print(f"  → {len(df_selected)} galaxies sélectionnées")
    print(f"     ({100*len(df_selected)/len(df_shear):.1f}% de l'échantillon)")

    return df_selected

def select_massive_neighbors(df_galaxies, M_min=1e11):
    """
    Sélectionne galaxies massives (voisins potentiels)
    """
    print(f"\nSélection voisins massifs (M > {M_min:.0e} M☉)...")

    mask = df_galaxies['M_stellar'] >= M_min
    df_massive = df_galaxies[mask].copy()

    print(f"  → {len(df_massive)} galaxies massives")

    return df_massive

# ============================================
# 4. TROUVER VOISINS
# ============================================

def find_nearest_massive_neighbor(lens_coords, lens_z,
                                  neighbor_coords, neighbor_z, neighbor_mass,
                                  d_max_physical=2.0,  # Mpc
                                  dz_max=0.05):
    """
    Trouve voisin le plus massif pour chaque galaxie lentille

    Parameters:
    - lens_coords: SkyCoord des lentilles
    - neighbor_coords: SkyCoord des voisins
    - d_max_physical: Distance physique maximale (Mpc)
    - dz_max: Différence redshift maximale

    Returns:
    - idx_neighbors: Indices voisins (ou -1 si pas de voisin)
    - separations: Séparations angulaires (deg)
    - position_angles: Angles de position (deg, 0=N, 90=E)
    """
    n_lens = len(lens_coords)
    idx_neighbors = np.full(n_lens, -1, dtype=int)
    separations_angular = np.full(n_lens, np.nan)
    position_angles = np.full(n_lens, np.nan)
    separations_physical = np.full(n_lens, np.nan)

    print(f"\nRecherche voisins pour {n_lens} galaxies...")

    for i in range(n_lens):
        if i % 1000 == 0:
            print(f"  Progression: {i}/{n_lens} ({100*i/n_lens:.1f}%)")

        # Coordonnées lentille
        lens_coord = lens_coords[i:i+1]
        z_lens = lens_z.iloc[i]

        # Contrainte redshift
        dz = np.abs(neighbor_z - z_lens)
        mask_z = dz <= dz_max

        if mask_z.sum() == 0:
            continue

        # Séparations angulaires
        seps = lens_coord.separation(neighbor_coords[mask_z])
        seps_deg = seps.deg

        # Conversion en distance physique projetée
        D_A = cosmo.angular_diameter_distance(z_lens).value  # Mpc
        seps_physical = D_A * np.radians(seps_deg)  # Mpc

        # Contrainte distance physique
        mask_dist = seps_physical <= d_max_physical

        if mask_dist.sum() == 0:
            continue

        # Indices voisins candidats (dans neighbor_coords)
        idx_candidates_local = np.where(mask_z)[0][mask_dist]

        # Trouver le plus massif
        masses_candidates = neighbor_mass.iloc[idx_candidates_local]
        idx_most_massive_local = masses_candidates.idxmax()
        idx_most_massive_global = idx_candidates_local[
            masses_candidates.index.get_loc(idx_most_massive_local)
        ]

        # Stocker résultats
        idx_neighbors[i] = idx_most_massive_global
        separations_angular[i] = seps_deg[mask_dist][
            masses_candidates.index.get_loc(idx_most_massive_local)
        ]
        separations_physical[i] = seps_physical[mask_dist][
            masses_candidates.index.get_loc(idx_most_massive_local)
        ]

        # Position angle (direction lens → voisin)
        pa = lens_coord.position_angle(
            neighbor_coords[idx_most_massive_global:idx_most_massive_global+1]
        )
        position_angles[i] = pa.deg

    n_found = (idx_neighbors >= 0).sum()
    print(f"  → {n_found} voisins trouvés ({100*n_found/n_lens:.1f}%)")

    return idx_neighbors, separations_angular, position_angles, separations_physical

# ============================================
# 5. CRÉER CATALOGUE PAIRES
# ============================================

def create_pairs_catalog(df_lensing, df_massive):
    """
    Crée catalogue de paires galaxie-voisin
    """
    print("\n" + "="*60)
    print("CRÉATION CATALOGUE PAIRES")
    print("="*60)

    # Convertir en SkyCoord
    lens_coords = SkyCoord(
        ra=df_lensing['RA'].values*u.deg,
        dec=df_lensing['DEC'].values*u.deg
    )

    neighbor_coords = SkyCoord(
        ra=df_massive['RA'].values*u.deg,
        dec=df_massive['DEC'].values*u.deg
    )

    # Trouver voisins
    idx_neighbors, sep_ang, pos_angles, sep_phys = find_nearest_massive_neighbor(
        lens_coords,
        df_lensing['z_photo'],
        neighbor_coords,
        df_massive['z_photo'],
        df_massive['M_stellar'],
        d_max_physical=2.0,
        dz_max=0.05
    )

    # Créer DataFrame paires
    mask_valid = idx_neighbors >= 0

    df_pairs = pd.DataFrame({
        'lens_ID': df_lensing.iloc[mask_valid]['ID'].values,
        'lens_RA': df_lensing.iloc[mask_valid]['RA'].values,
        'lens_DEC': df_lensing.iloc[mask_valid]['DEC'].values,
        'lens_z': df_lensing.iloc[mask_valid]['z_photo'].values,
        'theta_halo': df_lensing.iloc[mask_valid]['theta_halo'].values,
        'e_halo': df_lensing.iloc[mask_valid]['e_modulus'].values,

        'neighbor_ID': df_massive.iloc[idx_neighbors[mask_valid]]['ID'].values,
        'neighbor_M': df_massive.iloc[idx_neighbors[mask_valid]]['M_stellar'].values,
        'neighbor_z': df_massive.iloc[idx_neighbors[mask_valid]]['z_photo'].values,
        'theta_neighbor': pos_angles[mask_valid],
        'separation_ang': sep_ang[mask_valid],
        'separation_Mpc': sep_phys[mask_valid],
    })

    print(f"\nCatalogue paires créé: {len(df_pairs)} paires")

    return df_pairs

# ============================================
# 6. MAIN
# ============================================

if __name__ == "__main__":

    print("="*60)
    print("PRÉPARATION DONNÉES COSMOS")
    print("Test θ_halo ↔ θ_voisin")
    print("="*60)

    # 1. Charger données
    df_shear = load_cosmos_shear()
    df_galaxies = load_cosmos_galaxies()

    # 2. Sélectionner échantillons
    df_lensing = select_lensing_sample(df_shear)
    df_massive = select_massive_neighbors(df_galaxies, M_min=1e11)

    # 3. Créer catalogue paires
    df_pairs = create_pairs_catalog(df_lensing, df_massive)

    # 4. Sauvegarder
    output_file = 'data/COSMOS/cosmos_pairs_analysis.csv'
    df_pairs.to_csv(output_file, index=False)
    print(f"\n✓ Catalogue sauvegardé: {output_file}")

    # 5. Statistiques
    print("\n" + "="*60)
    print("STATISTIQUES ÉCHANTILLON")
    print("="*60)
    print(f"Nombre de paires: {len(df_pairs)}")
    print(f"Redshift moyen lentilles: {df_pairs['lens_z'].mean():.3f}")
    print(f"Masse moyenne voisins: {df_pairs['neighbor_M'].mean():.2e} M☉")
    print(f"Séparation moyenne: {df_pairs['separation_Mpc'].mean():.2f} Mpc")
    print(f"Ellipticité moyenne halos: {df_pairs['e_halo'].mean():.3f}")

    print("\n✓ Préparation terminée!")
```

---

## 5. Code Python : Analyse Corrélation

### Script 2 : Test θ_halo ↔ θ_voisin

```python
#!/usr/bin/env python3
# 02_analyze_correlation.py
"""
Analyse corrélation θ_halo ↔ θ_voisin
Test décisif Maîtrise du Temps vs Lambda-CDM
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from scipy.stats import vonmises
import seaborn as sns

# ============================================
# 1. CHARGER DONNÉES
# ============================================

def load_pairs(filename='data/COSMOS/cosmos_pairs_analysis.csv'):
    """
    Charge catalogue paires
    """
    print("Chargement catalogue paires...")
    df = pd.read_csv(filename)
    print(f"  → {len(df)} paires chargées")
    return df

# ============================================
# 2. CALCULER DIFFÉRENCE ANGULAIRE
# ============================================

def calculate_angular_difference(theta_halo, theta_neighbor):
    """
    Calcule différence angulaire Δθ = θ_neighbor - θ_halo

    Ramène à [-90°, 90°] car ellipse symétrique (θ et θ+180° équivalents)
    """
    # theta_halo dans [0, 180°]
    # theta_neighbor dans [0, 360°]

    # Convertir theta_neighbor dans [0, 180°] aussi
    theta_neighbor_mod = theta_neighbor % 180

    # Différence
    delta = theta_neighbor_mod - theta_halo

    # Ramener à [-90, 90]
    delta[delta > 90] -= 180
    delta[delta < -90] += 180

    return delta

# ============================================
# 3. TESTS STATISTIQUES
# ============================================

def test_correlation(df_pairs):
    """
    Tests de corrélation θ_halo ↔ θ_voisin
    """
    print("\n" + "="*60)
    print("TESTS DE CORRÉLATION")
    print("="*60)

    # Calculer Δθ
    df_pairs['delta_theta'] = calculate_angular_difference(
        df_pairs['theta_halo'].values,
        df_pairs['theta_neighbor'].values
    )

    # Test 1: Corrélation de Pearson
    print("\n1. Corrélation de Pearson (θ_halo vs θ_neighbor)")

    # Convertir theta_neighbor en [0, 180°] pour corrélation
    theta_neighbor_mod = df_pairs['theta_neighbor'].values % 180

    r_pearson, p_pearson = pearsonr(
        df_pairs['theta_halo'].values,
        theta_neighbor_mod
    )

    print(f"   r = {r_pearson:.4f}")
    print(f"   p-value = {p_pearson:.2e}")

    # Interprétation
    if r_pearson > 0.5:
        print("   → FORTE CORRÉLATION (Maîtrise du Temps favorisée)")
    elif r_pearson > 0.2:
        print("   → Corrélation modérée (résultat ambigu)")
    else:
        print("   → Pas de corrélation (Lambda-CDM favorisé)")

    # Test 2: Distribution Δθ
    print("\n2. Distribution Δθ (alignement parfait = 0°)")

    mean_abs_delta = np.mean(np.abs(df_pairs['delta_theta']))
    std_delta = np.std(df_pairs['delta_theta'])

    print(f"   |Δθ| moyen = {mean_abs_delta:.1f}°")
    print(f"   Écart-type = {std_delta:.1f}°")
    print(f"   Attendu si aléatoire: |Δθ| ≈ 45°, σ ≈ 26°")

    if mean_abs_delta < 30:
        print("   → ALIGNEMENT SIGNIFICATIF (Maîtrise du Temps)")
    elif mean_abs_delta < 40:
        print("   → Alignement partiel (ambigu)")
    else:
        print("   → Pas d'alignement (Lambda-CDM)")

    # Test 3: Fraction alignée (|Δθ| < 30°)
    print("\n3. Fraction galaxies bien alignées (|Δθ| < 30°)")

    frac_aligned = (np.abs(df_pairs['delta_theta']) < 30).sum() / len(df_pairs)

    print(f"   Fraction = {100*frac_aligned:.1f}%")
    print(f"   Attendu si aléatoire: 33%")
    print(f"   Attendu si MT (forte corrélation): > 60%")

    if frac_aligned > 0.6:
        print("   → FORTE ÉVIDENCE Maîtrise du Temps")
    elif frac_aligned > 0.45:
        print("   → Évidence modérée MT")
    else:
        print("   → Pas d'évidence MT")

    # Test 4: Bootstrap pour intervalle de confiance
    print("\n4. Bootstrap (10000 itérations) pour IC 95% sur r")

    n_bootstrap = 10000
    r_bootstrap = []

    for _ in range(n_bootstrap):
        sample = df_pairs.sample(n=len(df_pairs), replace=True)
        theta_n_mod = sample['theta_neighbor'].values % 180
        r, _ = pearsonr(sample['theta_halo'].values, theta_n_mod)
        r_bootstrap.append(r)

    r_bootstrap = np.array(r_bootstrap)
    ci_low, ci_high = np.percentile(r_bootstrap, [2.5, 97.5])

    print(f"   r = {r_pearson:.4f}")
    print(f"   IC 95%: [{ci_low:.4f}, {ci_high:.4f}]")

    # Résultat global
    print("\n" + "="*60)
    print("RÉSULTAT GLOBAL")
    print("="*60)

    score_MT = 0

    if r_pearson > 0.5: score_MT += 3
    elif r_pearson > 0.2: score_MT += 1

    if mean_abs_delta < 30: score_MT += 3
    elif mean_abs_delta < 40: score_MT += 1

    if frac_aligned > 0.6: score_MT += 3
    elif frac_aligned > 0.45: score_MT += 1

    print(f"Score Maîtrise du Temps: {score_MT}/9")

    if score_MT >= 7:
        print("VERDICT: FORTE ÉVIDENCE POUR MAÎTRISE DU TEMPS ✓✓✓")
    elif score_MT >= 4:
        print("VERDICT: Évidence modérée pour MT, nécessite plus de données")
    else:
        print("VERDICT: Pas d'évidence pour MT, Lambda-CDM favorisé")

    return r_pearson, p_pearson, df_pairs

# ============================================
# 4. ANALYSES SECONDAIRES
# ============================================

def analyze_mass_dependence(df_pairs):
    """
    Corrélation dépend-elle de la masse du voisin ?
    """
    print("\n" + "="*60)
    print("DÉPENDANCE EN MASSE DU VOISIN")
    print("="*60)

    # Bins de masse
    mass_bins = [1e11, 3e11, 10e11, 1e13]
    mass_labels = ['10¹¹-3×10¹¹', '3×10¹¹-10¹²', '>10¹²']

    for i, (m_low, m_high) in enumerate(zip(mass_bins[:-1], mass_bins[1:])):
        mask = (
            (df_pairs['neighbor_M'] >= m_low) &
            (df_pairs['neighbor_M'] < m_high)
        )

        if mask.sum() < 10:
            continue

        subset = df_pairs[mask]
        theta_n_mod = subset['theta_neighbor'].values % 180
        r, p = pearsonr(subset['theta_halo'].values, theta_n_mod)
        mean_delta = np.mean(np.abs(subset['delta_theta']))

        print(f"\nMasse voisin: {mass_labels[i]} M☉")
        print(f"  N = {len(subset)}")
        print(f"  r = {r:.3f} (p = {p:.2e})")
        print(f"  |Δθ| = {mean_delta:.1f}°")

    print("\nPrédiction MT: Corrélation augmente avec masse voisin")

def analyze_distance_dependence(df_pairs):
    """
    Corrélation dépend-elle de la distance au voisin ?
    """
    print("\n" + "="*60)
    print("DÉPENDANCE EN DISTANCE")
    print("="*60)

    # Bins de distance
    dist_bins = [0.3, 0.8, 1.5, 2.0]
    dist_labels = ['0.3-0.8 Mpc', '0.8-1.5 Mpc', '1.5-2.0 Mpc']

    for i, (d_low, d_high) in enumerate(zip(dist_bins[:-1], dist_bins[1:])):
        mask = (
            (df_pairs['separation_Mpc'] >= d_low) &
            (df_pairs['separation_Mpc'] < d_high)
        )

        if mask.sum() < 10:
            continue

        subset = df_pairs[mask]
        theta_n_mod = subset['theta_neighbor'].values % 180
        r, p = pearsonr(subset['theta_halo'].values, theta_n_mod)
        mean_delta = np.mean(np.abs(subset['delta_theta']))

        print(f"\nDistance: {dist_labels[i]}")
        print(f"  N = {len(subset)}")
        print(f"  r = {r:.3f} (p = {p:.2e})")
        print(f"  |Δθ| = {mean_delta:.1f}°")

    print("\nPrédiction MT: Corrélation décroît avec distance")

# ============================================
# 5. VISUALISATIONS
# ============================================

def plot_results(df_pairs, r_pearson):
    """
    Graphiques des résultats
    """
    print("\nCréation graphiques...")

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    # 1. Histogramme Δθ
    ax = axes[0, 0]
    ax.hist(df_pairs['delta_theta'], bins=36, range=(-90, 90),
            alpha=0.7, edgecolor='black', color='steelblue')
    ax.axvline(0, color='red', linestyle='--', linewidth=2,
               label='Alignement parfait')
    ax.set_xlabel('Δθ = θ_neighbor - θ_halo (°)', fontsize=12)
    ax.set_ylabel('Nombre de galaxies', fontsize=12)
    ax.set_title('Distribution des différences angulaires', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # Ajouter texte statistique
    mean_delta = np.mean(np.abs(df_pairs['delta_theta']))
    ax.text(0.05, 0.95, f'|Δθ| moyen = {mean_delta:.1f}°\nAttendu aléatoire: 45°',
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 2. Scatter θ_halo vs θ_neighbor
    ax = axes[0, 1]
    theta_n_mod = df_pairs['theta_neighbor'].values % 180
    ax.scatter(df_pairs['theta_halo'], theta_n_mod, alpha=0.3, s=10)
    ax.plot([0, 180], [0, 180], 'r--', linewidth=2, label='Alignement parfait (y=x)')
    ax.set_xlabel('θ_halo (°)', fontsize=12)
    ax.set_ylabel('θ_neighbor (°)', fontsize=12)
    ax.set_title(f'Corrélation θ_halo ↔ θ_neighbor\nr = {r_pearson:.3f}', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 180)

    # 3. |Δθ| vs Masse voisin
    ax = axes[0, 2]
    ax.scatter(df_pairs['neighbor_M'], np.abs(df_pairs['delta_theta']),
               alpha=0.3, s=10)
    ax.axhline(45, color='red', linestyle='--', label='Attendu si aléatoire')
    ax.set_xlabel('Masse voisin (M☉)', fontsize=12)
    ax.set_ylabel('|Δθ| (°)', fontsize=12)
    ax.set_title('Alignement vs Masse du voisin', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # 4. |Δθ| vs Distance
    ax = axes[1, 0]
    ax.scatter(df_pairs['separation_Mpc'], np.abs(df_pairs['delta_theta']),
               alpha=0.3, s=10)
    ax.axhline(45, color='red', linestyle='--', label='Attendu si aléatoire')
    ax.set_xlabel('Distance au voisin (Mpc)', fontsize=12)
    ax.set_ylabel('|Δθ| (°)', fontsize=12)
    ax.set_title('Alignement vs Distance', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # 5. Fraction alignée par bin de masse
    ax = axes[1, 1]
    mass_bins = np.logspace(11, 12.5, 8)
    frac_aligned_bins = []
    mass_centers = []

    for i in range(len(mass_bins)-1):
        mask = (
            (df_pairs['neighbor_M'] >= mass_bins[i]) &
            (df_pairs['neighbor_M'] < mass_bins[i+1])
        )
        if mask.sum() > 5:
            frac = (np.abs(df_pairs.loc[mask, 'delta_theta']) < 30).sum() / mask.sum()
            frac_aligned_bins.append(frac)
            mass_centers.append(np.sqrt(mass_bins[i] * mass_bins[i+1]))

    ax.plot(mass_centers, frac_aligned_bins, 'o-', linewidth=2, markersize=8)
    ax.axhline(0.33, color='red', linestyle='--', label='Attendu LCDM (33%)')
    ax.axhline(0.60, color='green', linestyle='--', label='Attendu MT (>60%)')
    ax.set_xlabel('Masse voisin (M☉)', fontsize=12)
    ax.set_ylabel('Fraction bien alignée (|Δθ|<30°)', fontsize=12)
    ax.set_title('Fraction alignée vs Masse', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # 6. Distribution ellipticité
    ax = axes[1, 2]
    ax.hist(df_pairs['e_halo'], bins=30, alpha=0.7, edgecolor='black', color='coral')
    ax.axvline(df_pairs['e_halo'].mean(), color='red', linestyle='--',
               linewidth=2, label=f'Moyenne = {df_pairs["e_halo"].mean():.3f}')
    ax.set_xlabel('Ellipticité halo e', fontsize=12)
    ax.set_ylabel('Nombre de galaxies', fontsize=12)
    ax.set_title('Distribution ellipticités', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/cosmos_correlation_analysis.png', dpi=300, bbox_inches='tight')
    print("  ✓ Graphique sauvegardé: results/cosmos_correlation_analysis.png")

    plt.show()

# ============================================
# 6. MAIN
# ============================================

if __name__ == "__main__":

    print("="*60)
    print("ANALYSE CORRÉLATION θ_halo ↔ θ_voisin")
    print("Test Maîtrise du Temps vs Lambda-CDM")
    print("="*60)

    # Créer répertoire résultats
    import os
    os.makedirs('results', exist_ok=True)

    # 1. Charger données
    df_pairs = load_pairs()

    # 2. Test corrélation principal
    r_pearson, p_pearson, df_pairs = test_correlation(df_pairs)

    # 3. Analyses secondaires
    analyze_mass_dependence(df_pairs)
    analyze_distance_dependence(df_pairs)

    # 4. Visualisations
    plot_results(df_pairs, r_pearson)

    # 5. Sauvegarder résultats détaillés
    df_pairs.to_csv('results/cosmos_pairs_with_analysis.csv', index=False)
    print("\n✓ Résultats sauvegardés: results/cosmos_pairs_with_analysis.csv")

    print("\n" + "="*60)
    print("ANALYSE TERMINÉE")
    print("="*60)
```

---

## 6. Instructions d'Exécution

### Étape par Étape

```bash
# 1. Télécharger données COSMOS
bash download_cosmos_data.sh

# 2. Préparer données (création catalogue paires)
python3 01_prepare_cosmos_data.py

# 3. Analyse corrélation
python3 02_analyze_correlation.py

# 4. Résultats dans:
#    - results/cosmos_correlation_analysis.png
#    - results/cosmos_pairs_with_analysis.csv
```

### Temps Estimé

- Téléchargement: 30-60 min (dépend connexion)
- Préparation: 10-20 min (recherche voisins)
- Analyse: 2-5 min
- **Total: ~1-2 heures**

---

## 7. Résultats Attendus

### Scénario A: Maîtrise du Temps Validée

**Si r > 0.5, |Δθ| < 30°, frac_aligned > 60%** :

```
RÉSULTAT GLOBAL
Score Maîtrise du Temps: 9/9
VERDICT: FORTE ÉVIDENCE POUR MAÎTRISE DU TEMPS ✓✓✓

Corrélation de Pearson: r = 0.67 (p < 10⁻²⁰)
|Δθ| moyen = 24.3° (attendu aléatoire: 45°)
Fraction bien alignée = 68% (attendu: 33%)
```

**Implication** : Publication immédiate ApJ Letters + soumission Nature Astronomy

---

### Scénario B: Lambda-CDM Confirmé

**Si r < 0.2, |Δθ| ≈ 45°, frac_aligned ≈ 33%** :

```
RÉSULTAT GLOBAL
Score Maîtrise du Temps: 0/9
VERDICT: Pas d'évidence pour MT, Lambda-CDM favorisé

Corrélation de Pearson: r = 0.08 (p = 0.42)
|Δθ| moyen = 44.7° (cohérent avec aléatoire)
Fraction bien alignée = 34% (comme attendu)
```

**Implication** : MT réfutée, mais résultat publiable (exclusion théorie)

---

### Scénario C: Résultat Ambigu

**Si 0.2 < r < 0.5** :

```
RÉSULTAT GLOBAL
Score Maîtrise du Temps: 4/9
VERDICT: Évidence modérée pour MT, nécessite plus de données

Corrélation de Pearson: r = 0.34 (p = 10⁻⁸)
|Δθ| moyen = 36.2°
Fraction bien alignée = 47%
```

**Implication** : Signal détecté mais pas décisif, analyse UNIONS cruciale

---

## 8. Prochaines Étapes Selon Résultats

### Si COSMOS Positif (r > 0.5)

1. **Immédiat** : Rédiger article court (ApJ Letters, 4 pages)
2. **Semaine 1** : Soumettre preprint arXiv
3. **Semaine 2-4** : Analyse UNIONS pour confirmation indépendante
4. **Mois 2** : Soumission journal (ApJ Letters ou Nature Astronomy)

### Si COSMOS Ambigu (0.2 < r < 0.5)

1. **Attendre** réponse UNIONS (données plus précises)
2. **Combiner** COSMOS + UNIONS pour statistiques accrues
3. **Analyser** sous-échantillons (haute masse, courte distance)

### Si COSMOS Négatif (r < 0.2)

1. **Vérifier** code et procédure (erreurs possibles ?)
2. **Tester** avec échantillon UNIONS plus précis
3. **Si confirmé** : MT réfutée, publier exclusion

---

## 9. Points d'Attention

### Biais Possibles

⚠️ **Biais de sélection** : Galaxies avec weak lensing détectable peuvent être biaisées

⚠️ **Erreurs redshift photométrique** : Peuvent créer fausses paires

⚠️ **Projection 3D → 2D** : Voisin physiquement proche peut sembler éloigné

**Mitigation** : Contraintes strictes Δz, distance physique, poids statistiques

---

## 10. Résumé

**Cette analyse COSMOS vous permet de** :

✅ Tester prédiction MT **immédiatement** (1-2 heures calcul)

✅ Obtenir résultat **avant** réponse UNIONS

✅ Calibrer méthode pour analyse UNIONS ultérieure

✅ Publier résultat **quel que soit le verdict** (positif = découverte, négatif = exclusion)

**Données** : Publiques, gratuites, disponibles maintenant

**Délai** : 1-2 heures (téléchargement + calcul)

**Impact** : Test décisif de votre théorie

---

**Prêt à lancer l'analyse ?** 🚀

Les scripts Python complets sont fournis ci-dessus. Dites-moi si vous voulez que je les crée en fichiers `.py` séparés !
