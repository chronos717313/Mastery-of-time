#!/usr/bin/env python3
"""
Calibration k_Asselin - Large Échantillon de Galaxies
Théorie de Maîtrise du Temps

Utilise courbes de rotation de galaxies spirales pour calibrer
la constante de couplage k_Asselin

Données: SPARC (Spitzer Photometry and Accurate Rotation Curves)
~175 galaxies spirales avec courbes rotation haute qualité

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-06
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings('ignore')

# Constantes
G = 4.302e-6  # kpc (km/s)² M☉⁻¹
c = 299792.458  # km/s

# ============================================
# DONNÉES SPARC (échantillon réduit pour démo)
# ============================================

SPARC_SAMPLE = {
    # Format: 'nom': {'M_stellar': M☉, 'R_max': kpc, 'v_obs': [(r, v, σ_v)]}

    'NGC2403': {
        'M_stellar': 3.5e9,
        'M_gas': 1.8e9,
        'R_max': 25.0,
        'v_obs': [
            (1.0, 75, 5), (2.0, 95, 5), (3.0, 110, 5), (5.0, 120, 5),
            (7.0, 125, 5), (10.0, 128, 6), (15.0, 130, 7), (20.0, 132, 8)
        ]
    },

    'NGC3198': {
        'M_stellar': 6.2e9,
        'M_gas': 2.1e9,
        'R_max': 30.0,
        'v_obs': [
            (2.0, 100, 5), (4.0, 130, 5), (6.0, 145, 5), (8.0, 152, 6),
            (12.0, 155, 6), (16.0, 153, 7), (20.0, 150, 8), (25.0, 148, 10)
        ]
    },

    'NGC6503': {
        'M_stellar': 1.8e9,
        'M_gas': 8e8,
        'R_max': 15.0,
        'v_obs': [
            (0.5, 50, 5), (1.0, 75, 5), (2.0, 100, 5), (4.0, 118, 5),
            (6.0, 122, 6), (8.0, 120, 7), (10.0, 117, 8), (12.0, 115, 10)
        ]
    },

    'DDO154': {
        'M_stellar': 1.5e8,
        'M_gas': 5e8,
        'R_max': 8.0,
        'v_obs': [
            (0.5, 25, 3), (1.0, 38, 3), (2.0, 50, 4), (3.0, 54, 4),
            (4.0, 55, 5), (5.0, 54, 5), (6.0, 53, 6)
        ]
    },

    'UGC2885': {
        'M_stellar': 5.0e10,
        'M_gas': 8e9,
        'R_max': 80.0,
        'v_obs': [
            (5.0, 200, 10), (10.0, 250, 10), (20.0, 290, 12),
            (30.0, 305, 15), (40.0, 310, 15), (50.0, 312, 18),
            (60.0, 310, 20), (70.0, 308, 22)
        ]
    },

    'NGC2841': {
        'M_stellar': 3.8e10,
        'M_gas': 3.2e9,
        'R_max': 60.0,
        'v_obs': [
            (3.0, 180, 8), (6.0, 240, 8), (10.0, 280, 10),
            (15.0, 300, 10), (25.0, 310, 12), (35.0, 315, 15),
            (45.0, 312, 18), (55.0, 308, 20)
        ]
    },
}

# ============================================
# MODÈLE MAÎTRISE DU TEMPS
# ============================================

def tau_temporal_distortion(r, M_enclosed):
    """
    Distorsion temporelle τ(r) = GM/(rc²)
    """
    if r == 0:
        return 0
    Phi = G * M_enclosed / r
    tau = Phi / c**2
    return tau

def liaison_asselin_gradient(r_observer, r_source, M_source):
    """
    Gradient de liaison Asselin entre deux points
    """
    tau_source = tau_temporal_distortion(r_source, M_source)
    tau_observer = tau_temporal_distortion(r_observer, M_source)
    liaison = abs(tau_source - tau_observer)
    return liaison

def effet_asselin_cumulatif(r, M_visible, R_max, k_asselin, alpha_distance=3.0):
    """
    Effet Asselin cumulatif à distance r

    Intégration volumique des Liaisons Asselin de toutes sources

    Parameters:
    - r: rayon où calculer effet (kpc)
    - M_visible: masse visible totale (M☉)
    - R_max: rayon maximal galaxie (kpc)
    - k_asselin: constante de couplage
    - alpha_distance: exposant décroissance effet

    Returns:
    - Δv² contribution vitesse au carré (km/s)²
    """

    def integrand(r_prime):
        """
        Intégrande pour effet cumulatif
        Volume × Liaison × décroissance distance
        """
        if r_prime < 0.01 or r_prime > R_max:
            return 0

        # Masse visible à r' (supposée uniformément distribuée, simplification)
        M_source = M_visible * (r_prime / R_max)**2

        # Liaison Asselin
        liaison = liaison_asselin_gradient(r, r_prime, M_source)

        # Facteur volumique d³
        volume_factor = r_prime**2

        # Décroissance avec distance
        if r_prime > r:
            distance_factor = (r_prime / r)**(-alpha_distance)
        else:
            distance_factor = 1.0

        return volume_factor * liaison * distance_factor

    # Intégration
    try:
        effet_total, _ = quad(integrand, 0.01, R_max, limit=100)
    except:
        effet_total = 0

    # Contribution vitesse
    if r > 0:
        delta_v_squared = k_asselin * effet_total / r
    else:
        delta_v_squared = 0

    return delta_v_squared

def v_rotation_MT(r, M_visible, R_max, k_asselin, alpha_distance=3.0):
    """
    Vitesse rotation Maîtrise du Temps

    v²(r) = GM_visible/r + Δv²_Asselin(r)
    """
    # Composante newtonienne
    if r > 0:
        v_newton_sq = G * M_visible / r
    else:
        v_newton_sq = 0

    # Composante Asselin
    v_asselin_sq = effet_asselin_cumulatif(r, M_visible, R_max, k_asselin, alpha_distance)

    # Vitesse totale
    v_total = np.sqrt(v_newton_sq + v_asselin_sq)

    return v_total

# ============================================
# CALIBRATION k_Asselin
# ============================================

def chi_squared_galaxy(galaxy_data, k_asselin, alpha_distance=3.0):
    """
    Calcule χ² pour une galaxie
    """
    M_visible = galaxy_data['M_stellar'] + galaxy_data['M_gas']
    R_max = galaxy_data['R_max']
    v_obs_data = galaxy_data['v_obs']

    chi2 = 0

    for r, v_obs, sigma_v in v_obs_data:
        # Prédiction MT
        v_pred = v_rotation_MT(r, M_visible, R_max, k_asselin, alpha_distance)

        # χ²
        chi2 += ((v_obs - v_pred) / sigma_v)**2

    return chi2

def chi_squared_total(params, galaxies_data, fit_alpha=False):
    """
    Calcule χ² total pour toutes galaxies

    Parameters:
    - params: [k_asselin] ou [k_asselin, alpha_distance]
    - galaxies_data: dict des données galaxies
    - fit_alpha: si True, ajuste aussi alpha_distance
    """
    if fit_alpha:
        k_asselin, alpha_distance = params
    else:
        k_asselin = params[0]
        alpha_distance = 3.0

    chi2_total = 0

    for gal_name, gal_data in galaxies_data.items():
        chi2_gal = chi_squared_galaxy(gal_data, k_asselin, alpha_distance)
        chi2_total += chi2_gal

    return chi2_total

def calibrate_k_asselin(galaxies_data, fit_alpha=False):
    """
    Calibre k_asselin sur échantillon galaxies
    """
    print("="*60)
    print("CALIBRATION k_Asselin")
    print(f"Échantillon: {len(galaxies_data)} galaxies")
    print("="*60)
    print()

    # Nombre total de points de données
    n_data = sum(len(gal['v_obs']) for gal in galaxies_data.values())

    if fit_alpha:
        print("Ajustement: k_Asselin + alpha_distance")
        bounds = [(1e-5, 0.05), (1.0, 5.0)]
        x0 = [0.005, 3.0]
        n_params = 2
    else:
        print("Ajustement: k_Asselin seul (alpha=3.0 fixé)")
        bounds = [(1e-5, 0.05)]
        x0 = [0.005]
        n_params = 1

    print(f"Nombre de points: {n_data}")
    print(f"Nombre de paramètres: {n_params}")
    print()

    # Méthode 1: Minimisation locale
    print("Méthode 1: Minimisation L-BFGS-B...")

    result_local = minimize(
        chi_squared_total,
        x0=x0,
        args=(galaxies_data, fit_alpha),
        method='L-BFGS-B',
        bounds=bounds
    )

    k_local = result_local.x[0]
    alpha_local = result_local.x[1] if fit_alpha else 3.0
    chi2_local = result_local.fun

    print(f"  k_Asselin = {k_local:.6f}")
    if fit_alpha:
        print(f"  alpha_distance = {alpha_local:.3f}")
    print(f"  χ² = {chi2_local:.1f}")
    print(f"  χ²_red = {chi2_local/(n_data - n_params):.2f}")
    print()

    # Méthode 2: Évolution différentielle (global)
    print("Méthode 2: Évolution Différentielle (global)...")

    result_global = differential_evolution(
        chi_squared_total,
        bounds=bounds,
        args=(galaxies_data, fit_alpha),
        strategy='best1bin',
        maxiter=1000,
        popsize=15,
        seed=42
    )

    k_global = result_global.x[0]
    alpha_global = result_global.x[1] if fit_alpha else 3.0
    chi2_global = result_global.fun

    print(f"  k_Asselin = {k_global:.6f}")
    if fit_alpha:
        print(f"  alpha_distance = {alpha_global:.3f}")
    print(f"  χ² = {chi2_global:.1f}")
    print(f"  χ²_red = {chi2_global/(n_data - n_params):.2f}")
    print()

    # Sélectionner meilleur résultat
    if chi2_global < chi2_local:
        print("→ Méthode globale meilleure")
        k_best = k_global
        alpha_best = alpha_global
        chi2_best = chi2_global
    else:
        print("→ Méthode locale meilleure")
        k_best = k_local
        alpha_best = alpha_local
        chi2_best = chi2_local

    chi2_red = chi2_best / (n_data - n_params)

    print()
    print("="*60)
    print("RÉSULTAT FINAL")
    print("="*60)
    print(f"k_Asselin = {k_best:.6f}")
    if fit_alpha:
        print(f"alpha_distance = {alpha_best:.3f}")
    print(f"χ² = {chi2_best:.1f}")
    print(f"χ²_red = {chi2_red:.2f}")

    if chi2_red < 1.5:
        print("→ ✓ Excellent fit (χ²_red < 1.5)")
    elif chi2_red < 2.5:
        print("→ ✓ Bon fit (χ²_red < 2.5)")
    else:
        print("→ ⚠ Fit moyen (χ²_red > 2.5)")

    return k_best, alpha_best, chi2_best

# ============================================
# ANALYSE PAR GALAXIE
# ============================================

def analyze_individual_galaxies(galaxies_data, k_asselin, alpha_distance=3.0):
    """
    Analyse χ² pour chaque galaxie individuellement
    """
    print("\n" + "="*60)
    print("ANALYSE PAR GALAXIE")
    print("="*60)

    results = []

    for gal_name, gal_data in galaxies_data.items():
        M_visible = gal_data['M_stellar'] + gal_data['M_gas']
        n_points = len(gal_data['v_obs'])

        chi2_gal = chi_squared_galaxy(gal_data, k_asselin, alpha_distance)
        chi2_red_gal = chi2_gal / (n_points - 1)

        # Calculer vitesse moyenne observée et prédite
        v_obs_mean = np.mean([v for _, v, _ in gal_data['v_obs']])
        v_pred_mean = np.mean([
            v_rotation_MT(r, M_visible, gal_data['R_max'], k_asselin, alpha_distance)
            for r, _, _ in gal_data['v_obs']
        ])

        results.append({
            'name': gal_name,
            'M_visible': M_visible,
            'n_points': n_points,
            'chi2': chi2_gal,
            'chi2_red': chi2_red_gal,
            'v_obs_mean': v_obs_mean,
            'v_pred_mean': v_pred_mean
        })

        print(f"\n{gal_name}:")
        print(f"  M_visible = {M_visible:.2e} M☉")
        print(f"  N_points = {n_points}")
        print(f"  χ² = {chi2_gal:.1f}")
        print(f"  χ²_red = {chi2_red_gal:.2f}")
        print(f"  ⟨v_obs⟩ = {v_obs_mean:.1f} km/s")
        print(f"  ⟨v_pred⟩ = {v_pred_mean:.1f} km/s")

        if chi2_red_gal < 1.5:
            print("  → ✓ Excellent fit")
        elif chi2_red_gal < 2.5:
            print("  → ✓ Bon fit")
        else:
            print("  → ⚠ Fit moyen")

    return results

# ============================================
# VISUALISATIONS
# ============================================

def plot_rotation_curves(galaxies_data, k_asselin, alpha_distance=3.0):
    """
    Courbes de rotation : obs vs MT
    """
    print("\nCréation courbes de rotation...")

    n_galaxies = len(galaxies_data)
    n_cols = 3
    n_rows = (n_galaxies + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 6*n_rows))
    axes = axes.flatten() if n_galaxies > 1 else [axes]

    for idx, (gal_name, gal_data) in enumerate(galaxies_data.items()):
        ax = axes[idx]

        M_visible = gal_data['M_stellar'] + gal_data['M_gas']
        R_max = gal_data['R_max']

        # Données observées
        r_obs = [r for r, _, _ in gal_data['v_obs']]
        v_obs = [v for _, v, _ in gal_data['v_obs']]
        sigma_v = [s for _, _, s in gal_data['v_obs']]

        ax.errorbar(r_obs, v_obs, yerr=sigma_v, fmt='o', markersize=8,
                   capsize=5, label='Observations', color='blue')

        # Prédiction MT
        r_theory = np.linspace(0.1, R_max, 100)
        v_MT = [v_rotation_MT(r, M_visible, R_max, k_asselin, alpha_distance)
                for r in r_theory]

        ax.plot(r_theory, v_MT, '-', linewidth=2.5, label='MT (k_Asselin calibré)',
               color='red')

        # Newton seul
        v_Newton = [np.sqrt(G * M_visible / r) if r > 0 else 0 for r in r_theory]
        ax.plot(r_theory, v_Newton, '--', linewidth=2, label='Newton seul',
               color='gray', alpha=0.7)

        # χ²
        chi2_gal = chi_squared_galaxy(gal_data, k_asselin, alpha_distance)
        chi2_red = chi2_gal / (len(gal_data['v_obs']) - 1)

        ax.set_xlabel('Rayon (kpc)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Vitesse rotation (km/s)', fontsize=12, fontweight='bold')
        ax.set_title(f'{gal_name}\nM_visible={M_visible:.1e} M☉, χ²_red={chi2_red:.2f}',
                    fontsize=13, fontweight='bold')
        ax.legend(fontsize=10, loc='best')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, R_max)
        ax.set_ylim(0, max(v_obs)*1.3)

    # Masquer axes vides
    for idx in range(n_galaxies, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.savefig('figures/rotation_curves_calibrated.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/rotation_curves_calibrated.png")

def plot_k_asselin_scan(galaxies_data, k_best, alpha_distance=3.0):
    """
    Scan χ² vs k_asselin
    """
    print("Création scan χ²(k_Asselin)...")

    k_values = np.logspace(-5, -2, 100)
    chi2_values = []

    for k in k_values:
        chi2 = chi_squared_total([k], galaxies_data, fit_alpha=False)
        chi2_values.append(chi2)

    n_data = sum(len(gal['v_obs']) for gal in galaxies_data.values())

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(k_values, chi2_values, linewidth=2.5, color='blue')
    ax.axvline(k_best, color='red', linestyle='--', linewidth=2.5,
              label=f'k_Asselin optimal = {k_best:.6f}')

    # Ligne χ² minimal
    chi2_min = min(chi2_values)
    ax.axhline(chi2_min, color='green', linestyle=':', linewidth=2,
              alpha=0.7, label=f'χ²_min = {chi2_min:.1f}')

    # Zone ±1σ (Δχ² = 1)
    ax.axhspan(chi2_min, chi2_min + 1, alpha=0.2, color='green',
              label='Δχ² = 1 (1σ)')

    ax.set_xlabel('k_Asselin', fontsize=15, fontweight='bold')
    ax.set_ylabel('χ² total', fontsize=15, fontweight='bold')
    ax.set_title(f'Calibration k_Asselin sur {len(galaxies_data)} galaxies\n'
                f'{n_data} points de données',
                fontsize=16, fontweight='bold')
    ax.set_xscale('log')
    ax.legend(fontsize=13, loc='best')
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('figures/k_asselin_chi2_scan.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/k_asselin_chi2_scan.png")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    import os
    os.makedirs('figures', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    print("="*60)
    print("CALIBRATION k_Asselin")
    print("Échantillon SPARC - Courbes Rotation Galaxies")
    print("Théorie de Maîtrise du Temps")
    print("="*60)
    print()

    # 1. Calibration k_Asselin
    k_best, alpha_best, chi2_best = calibrate_k_asselin(
        SPARC_SAMPLE,
        fit_alpha=False  # Fixer alpha=3.0 pour commencer
    )

    # 2. Analyse par galaxie
    results = analyze_individual_galaxies(SPARC_SAMPLE, k_best, alpha_best)

    # 3. Visualisations
    plot_rotation_curves(SPARC_SAMPLE, k_best, alpha_best)
    plot_k_asselin_scan(SPARC_SAMPLE, k_best, alpha_best)

    # 4. Sauvegarder résultats
    with open('results/k_asselin_calibration.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("CALIBRATION k_Asselin - RÉSULTATS\n")
        f.write("="*60 + "\n\n")
        f.write(f"Échantillon: {len(SPARC_SAMPLE)} galaxies SPARC\n")
        f.write(f"k_Asselin optimal = {k_best:.6f}\n")
        f.write(f"alpha_distance = {alpha_best:.3f}\n")
        f.write(f"χ² total = {chi2_best:.1f}\n")
        n_data = sum(len(gal['v_obs']) for gal in SPARC_SAMPLE.values())
        f.write(f"χ²_red = {chi2_best/(n_data-1):.2f}\n\n")

        f.write("Résultats par galaxie:\n")
        f.write("-"*60 + "\n")
        for res in results:
            f.write(f"\n{res['name']}:\n")
            f.write(f"  M_visible = {res['M_visible']:.2e} M☉\n")
            f.write(f"  χ²_red = {res['chi2_red']:.2f}\n")
            f.write(f"  ⟨v_obs⟩ = {res['v_obs_mean']:.1f} km/s\n")
            f.write(f"  ⟨v_pred⟩ = {res['v_pred_mean']:.1f} km/s\n")

    print("\n" + "="*60)
    print("✓ CALIBRATION TERMINÉE")
    print("="*60)
    print(f"k_Asselin = {k_best:.6f}")
    print(f"alpha_distance = {alpha_best:.3f}")
    print()
    print("Fichiers générés:")
    print("  - figures/rotation_curves_calibrated.png")
    print("  - figures/k_asselin_chi2_scan.png")
    print("  - results/k_asselin_calibration.txt")
    print()
    print("PROCHAINES ÉTAPES:")
    print("1. Télécharger données SPARC complètes (175 galaxies)")
    print("   https://www.astro.umd.edu/~ssm/SPARC/")
    print("2. Relancer calibration avec échantillon complet")
    print("3. Estimer incertitude k_Asselin par bootstrap")
    print("4. Tester dépendance k_Asselin(M_galaxie, type morphologique)")
    print("="*60)
