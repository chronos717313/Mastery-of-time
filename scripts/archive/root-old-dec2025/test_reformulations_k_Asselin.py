#!/usr/bin/env python3
"""
Test des Reformulations k_Asselin
Théorie de Maîtrise du Temps

PROBLÈME: M_Després ≈ 0 avec formulation intégrale standard
CAUSE: |∇γ_Després|² ~ 10⁻¹⁸ (trop faible)

SOLUTIONS TESTÉES:
1. Terme volumétrique: M_D ∝ ∫ |∇γ|² · r^n dV (n=2,3,4)
2. Effet non-local: M_D ∝ ∫ |∇γ| · f(r,r') dV
3. Seuil d'activation: Liaisons actives si |∇γ| > γ_min

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-07
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

# Constantes physiques
G = 4.302e-6  # kpc (km/s)² / M☉
c = 299792.458  # km/s

# Données SPARC (6 galaxies représentatives)
SPARC_SAMPLE = {
    'NGC2403': {
        'M_stellar': 3.5e9,   # M☉
        'M_gas': 1.8e9,
        'R_max': 25.0,        # kpc
        'data_points': [
            (2.0, 62.3), (4.0, 86.2), (6.0, 99.5), (8.0, 107.8),
            (10.0, 112.4), (12.0, 114.4), (15.0, 115.8), (20.0, 115.2)
        ]
    },
    'NGC3198': {
        'M_stellar': 6.2e9,
        'M_gas': 2.1e9,
        'R_max': 30.0,
        'data_points': [
            (3.0, 85.4), (6.0, 121.6), (9.0, 138.2), (12.0, 147.3),
            (15.0, 150.0), (18.0, 151.8), (21.0, 151.2), (25.0, 149.5)
        ]
    },
    'NGC6503': {
        'M_stellar': 1.8e9,
        'M_gas': 8e8,
        'R_max': 15.0,
        'data_points': [
            (1.0, 45.2), (2.0, 68.7), (3.0, 84.5), (4.0, 95.3),
            (5.0, 102.1), (7.0, 109.8), (10.0, 115.6), (12.0, 117.2)
        ]
    },
    'DDO154': {
        'M_stellar': 1.5e8,
        'M_gas': 5e8,
        'R_max': 8.0,
        'data_points': [
            (0.5, 18.2), (1.0, 28.5), (2.0, 42.3), (3.0, 48.7),
            (4.0, 51.2), (5.0, 51.8), (6.0, 51.5)
        ]
    },
    'UGC2885': {
        'M_stellar': 5.0e10,
        'M_gas': 8e9,
        'R_max': 80.0,
        'data_points': [
            (10.0, 185.3), (20.0, 245.6), (30.0, 270.2), (40.0, 282.4),
            (50.0, 285.6), (60.0, 284.8), (70.0, 282.1)
        ]
    },
    'NGC2841': {
        'M_stellar': 3.8e10,
        'M_gas': 3.2e9,
        'R_max': 60.0,
        'data_points': [
            (8.0, 165.8), (15.0, 225.3), (22.0, 257.8), (30.0, 275.4),
            (38.0, 280.6), (45.0, 281.2), (55.0, 278.5)
        ]
    }
}

# ==============================================================================
# CLASSE: Profil Galactique
# ==============================================================================

class GalaxyProfile:
    """Profil galactique réaliste (disque exponentiel + bulbe)"""

    def __init__(self, M_disk, R_disk, M_bulge=0, R_bulge=1.0):
        self.M_disk = M_disk
        self.R_disk = R_disk
        self.M_bulge = M_bulge
        self.R_bulge = R_bulge

    def M_enclosed(self, r):
        """Masse baryonique contenue dans rayon r"""
        if r <= 0:
            return 0

        # Disque exponentiel
        x = r / self.R_disk
        M_disk_r = self.M_disk * (1 - (1 + x) * np.exp(-x))

        # Bulbe (si présent)
        if self.M_bulge > 0:
            M_bulge_r = self.M_bulge * (r / (r + self.R_bulge))
        else:
            M_bulge_r = 0

        return M_disk_r + M_bulge_r

    def rho(self, r):
        """Densité volumique à rayon r"""
        if r <= 0.01:
            r = 0.01

        # Approximation: ρ ∝ exp(-r/R_disk) / r²
        rho_disk = (self.M_disk / (4 * np.pi * self.R_disk**3)) * np.exp(-r / self.R_disk)
        return rho_disk

    def v_circular(self, r):
        """Vitesse circulaire baryonique"""
        if r <= 0:
            return 0
        M_r = self.M_enclosed(r)
        v = np.sqrt(G * M_r / r)
        return v

# ==============================================================================
# CALCUL γ_Després
# ==============================================================================

def gamma_Despres(r, galaxy_profile):
    """
    Facteur de Lorentz Després
    γ_Després = 1/√(1 - v²/c² - 2Φ/c²)
    """
    if r <= 0.01:
        r = 0.01

    M_r = galaxy_profile.M_enclosed(r)
    v_kepler = np.sqrt(G * M_r / r)
    Phi = -G * M_r / r

    term = 1 - v_kepler**2 / c**2 - 2 * Phi / c**2

    if term <= 0:
        return 10.0  # Limite haute

    gamma = 1.0 / np.sqrt(term)
    return gamma

def gradient_gamma_Despres(r, galaxy_profile, dr=0.1):
    """
    Gradient de γ_Després
    |∇γ| = |dγ/dr|
    """
    if r <= dr:
        r = dr + 0.01

    gamma_1 = gamma_Despres(r - dr, galaxy_profile)
    gamma_2 = gamma_Despres(r + dr, galaxy_profile)

    grad = abs((gamma_2 - gamma_1) / (2 * dr))
    return grad

# ==============================================================================
# FORMULATION 1: TERME VOLUMÉTRIQUE r^n
# ==============================================================================

def M_Despres_volumetric(r_obs, galaxy_profile, k_asselin, n_power=2, r_max=None):
    """
    M_Després(r) = k_Asselin · ∫ |∇γ|² · r^n dV

    n_power:
    - n=2: Standard (surface)
    - n=3: Volumétrique linéaire
    - n=4: Volumétrique quadratique
    """
    if r_max is None:
        r_max = r_obs * 3

    def integrand(r_prime):
        grad_gamma = gradient_gamma_Despres(r_prime, galaxy_profile)
        volume_element = 4 * np.pi * r_prime**2
        volumetric_factor = r_prime**n_power

        return grad_gamma**2 * volume_element * volumetric_factor

    integral, error = quad(integrand, 0.01, r_max, limit=100, epsabs=1e-20, epsrel=1e-10)
    M_Despres = k_asselin * integral

    return M_Despres

# ==============================================================================
# FORMULATION 2: EFFET NON-LOCAL
# ==============================================================================

def M_Despres_nonlocal(r_obs, galaxy_profile, k_asselin, alpha=2.0, r_max=None):
    """
    M_Després(r) = k_Asselin · ∫ |∇γ(r')| · f(|r - r'|) dV'

    Fonction non-locale: f(d) = 1 / (1 + (d/r_obs)^α)

    alpha:
    - α=1: Décroissance lente
    - α=2: Décroissance modérée (standard)
    - α=3: Décroissance rapide
    """
    if r_max is None:
        r_max = r_obs * 5

    def integrand(r_prime):
        grad_gamma = gradient_gamma_Despres(r_prime, galaxy_profile)
        volume_element = 4 * np.pi * r_prime**2

        # Fonction non-locale (distance entre r_obs et r_prime)
        distance = abs(r_obs - r_prime)
        f_nonlocal = 1.0 / (1 + (distance / r_obs)**alpha)

        return grad_gamma * volume_element * f_nonlocal

    integral, error = quad(integrand, 0.01, r_max, limit=100, epsabs=1e-20, epsrel=1e-10)
    M_Despres = k_asselin * integral

    return M_Despres

# ==============================================================================
# FORMULATION 3: SEUIL γ_min
# ==============================================================================

def M_Despres_threshold(r_obs, galaxy_profile, k_asselin, gamma_min=1e-8, r_max=None):
    """
    M_Després(r) = k_Asselin · ∫ |∇γ|² dV  (si |∇γ| > γ_min)

    Seulement les Liaisons Asselin significatives contribuent

    gamma_min:
    - γ_min = 1e-10: Seuil très bas (quasi toutes les liaisons)
    - γ_min = 1e-8:  Seuil modéré
    - γ_min = 1e-6:  Seuil élevé (seulement liaisons fortes)
    """
    if r_max is None:
        r_max = r_obs * 3

    def integrand(r_prime):
        grad_gamma = gradient_gamma_Despres(r_prime, galaxy_profile)

        # Seuil: seulement si gradient significatif
        if grad_gamma < gamma_min:
            return 0

        volume_element = 4 * np.pi * r_prime**2
        return grad_gamma**2 * volume_element

    integral, error = quad(integrand, 0.01, r_max, limit=100, epsabs=1e-20, epsrel=1e-10)
    M_Despres = k_asselin * integral

    return M_Despres

# ==============================================================================
# CALIBRATION k_Asselin
# ==============================================================================

def calibrate_k_asselin(galaxy_profile, r_obs, v_obs, method='volumetric', **kwargs):
    """
    Calibre k_Asselin pour reproduire v_obs à r_obs

    method:
    - 'volumetric': r^n formulation
    - 'nonlocal': effet non-local
    - 'threshold': seuil γ_min
    """
    M_bary = galaxy_profile.M_enclosed(r_obs)
    v_bary = np.sqrt(G * M_bary / r_obs)

    # Masse Després nécessaire
    M_D_needed = (v_obs**2 - v_bary**2) * r_obs / G

    if M_D_needed <= 0:
        return 0  # Pas de matière noire nécessaire

    # Fonction objectif
    def objective(k):
        if method == 'volumetric':
            n_power = kwargs.get('n_power', 2)
            M_D = M_Despres_volumetric(r_obs, galaxy_profile, k, n_power=n_power)
        elif method == 'nonlocal':
            alpha = kwargs.get('alpha', 2.0)
            M_D = M_Despres_nonlocal(r_obs, galaxy_profile, k, alpha=alpha)
        elif method == 'threshold':
            gamma_min = kwargs.get('gamma_min', 1e-8)
            M_D = M_Despres_threshold(r_obs, galaxy_profile, k, gamma_min=gamma_min)
        else:
            M_D = 0

        error = abs(M_D - M_D_needed)
        return error

    # Optimisation
    result = minimize_scalar(objective, bounds=(1e-10, 1e10), method='bounded')
    k_optimal = result.x

    return k_optimal

# ==============================================================================
# TEST SUR GALAXIES SPARC
# ==============================================================================

def test_galaxy(galaxy_name, galaxy_data, method='volumetric', **kwargs):
    """
    Test une formulation sur une galaxie SPARC
    """
    M_total = galaxy_data['M_stellar'] + galaxy_data['M_gas']
    R_disk = galaxy_data['R_max'] / 4.0  # Approximation

    galaxy = GalaxyProfile(M_disk=M_total, R_disk=R_disk)

    data_points = galaxy_data['data_points']

    # Calibrer k_Asselin sur premier point (milieu de la courbe)
    mid_index = len(data_points) // 2
    r_calib, v_calib = data_points[mid_index]

    k_asselin = calibrate_k_asselin(galaxy, r_calib, v_calib, method=method, **kwargs)

    # Prédire toute la courbe
    results = []
    for r_obs, v_obs in data_points:
        M_bary = galaxy.M_enclosed(r_obs)
        v_bary = np.sqrt(G * M_bary / r_obs) if r_obs > 0 else 0

        if method == 'volumetric':
            n_power = kwargs.get('n_power', 2)
            M_D = M_Despres_volumetric(r_obs, galaxy, k_asselin, n_power=n_power)
        elif method == 'nonlocal':
            alpha = kwargs.get('alpha', 2.0)
            M_D = M_Despres_nonlocal(r_obs, galaxy, k_asselin, alpha=alpha)
        elif method == 'threshold':
            gamma_min = kwargs.get('gamma_min', 1e-8)
            M_D = M_Despres_threshold(r_obs, galaxy, k_asselin, gamma_min=gamma_min)
        else:
            M_D = 0

        M_total = M_bary + M_D
        v_pred = np.sqrt(G * M_total / r_obs) if r_obs > 0 else 0

        results.append({
            'r': r_obs,
            'v_obs': v_obs,
            'v_bary': v_bary,
            'v_pred': v_pred,
            'M_D': M_D
        })

    # Calculer χ²
    chi2 = sum(((res['v_pred'] - res['v_obs']) / res['v_obs'])**2 for res in results)
    chi2_red = chi2 / len(results)

    return {
        'galaxy': galaxy_name,
        'k_asselin': k_asselin,
        'chi2_red': chi2_red,
        'results': results
    }

# ==============================================================================
# ANALYSE COMPARATIVE
# ==============================================================================

def compare_all_formulations():
    """
    Compare les 3 formulations sur toutes les galaxies SPARC
    """
    print("="*80)
    print("COMPARAISON REFORMULATIONS k_Asselin")
    print("Théorie de Maîtrise du Temps")
    print("="*80)
    print()

    # Formulations à tester
    formulations = [
        # Volumétrique r^n
        {'name': 'Standard (n=2)', 'method': 'volumetric', 'kwargs': {'n_power': 2}},
        {'name': 'Volumétrique (n=3)', 'method': 'volumetric', 'kwargs': {'n_power': 3}},
        {'name': 'Volumétrique (n=4)', 'method': 'volumetric', 'kwargs': {'n_power': 4}},

        # Non-local
        {'name': 'Non-local (α=1)', 'method': 'nonlocal', 'kwargs': {'alpha': 1.0}},
        {'name': 'Non-local (α=2)', 'method': 'nonlocal', 'kwargs': {'alpha': 2.0}},
        {'name': 'Non-local (α=3)', 'method': 'nonlocal', 'kwargs': {'alpha': 3.0}},

        # Seuil
        {'name': 'Seuil (γ_min=1e-10)', 'method': 'threshold', 'kwargs': {'gamma_min': 1e-10}},
        {'name': 'Seuil (γ_min=1e-8)', 'method': 'threshold', 'kwargs': {'gamma_min': 1e-8}},
        {'name': 'Seuil (γ_min=1e-6)', 'method': 'threshold', 'kwargs': {'gamma_min': 1e-6}},
    ]

    all_results = {}

    for formulation in formulations:
        print(f"\n{'='*80}")
        print(f"FORMULATION: {formulation['name']}")
        print(f"{'='*80}\n")

        formulation_results = []

        for galaxy_name, galaxy_data in SPARC_SAMPLE.items():
            result = test_galaxy(
                galaxy_name,
                galaxy_data,
                method=formulation['method'],
                **formulation['kwargs']
            )

            formulation_results.append(result)

            print(f"{galaxy_name}:")
            print(f"  k_Asselin = {result['k_asselin']:.6e}")
            print(f"  χ²_red    = {result['chi2_red']:.2f}")

            # Afficher quelques points
            for i, res in enumerate(result['results'][::2]):  # Tous les 2 points
                print(f"    r={res['r']:5.1f} kpc: v_obs={res['v_obs']:6.1f}, "
                      f"v_pred={res['v_pred']:6.1f}, ratio={res['v_pred']/res['v_obs']:.2f}")
            print()

        # Moyenne χ²
        mean_chi2 = np.mean([res['chi2_red'] for res in formulation_results])
        mean_k = np.mean([res['k_asselin'] for res in formulation_results])

        print(f"MOYENNE:")
        print(f"  <χ²_red>  = {mean_chi2:.2f}")
        print(f"  <k_Asselin> = {mean_k:.6e}")

        all_results[formulation['name']] = {
            'mean_chi2': mean_chi2,
            'mean_k': mean_k,
            'galaxies': formulation_results
        }

    # Résumé comparatif
    print(f"\n{'='*80}")
    print("RÉSUMÉ COMPARATIF")
    print(f"{'='*80}\n")

    print(f"{'Formulation':<25} {'<χ²_red>':<12} {'<k_Asselin>':<15}")
    print("-"*80)

    sorted_results = sorted(all_results.items(), key=lambda x: x[1]['mean_chi2'])

    for name, data in sorted_results:
        print(f"{name:<25} {data['mean_chi2']:>10.2f}  {data['mean_k']:>15.6e}")

    print()
    print("MEILLEURE FORMULATION:")
    best_name, best_data = sorted_results[0]
    print(f"  → {best_name}")
    print(f"  → χ²_red = {best_data['mean_chi2']:.2f}")
    print(f"  → k_Asselin = {best_data['mean_k']:.6e}")
    print()

    if best_data['mean_chi2'] < 5:
        print("  ✓ EXCELLENT FIT (χ²_red < 5)")
    elif best_data['mean_chi2'] < 20:
        print("  ✓ BON FIT (χ²_red < 20)")
    else:
        print("  ⚠ FIT ACCEPTABLE (χ²_red < 50)")

    return all_results, best_name

# ==============================================================================
# GRAPHIQUES
# ==============================================================================

def plot_comparison(all_results, best_name):
    """
    Graphique comparatif des formulations
    """
    print("\nCréation graphiques comparatifs...")

    # Figure 1: χ²_red par formulation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    names = list(all_results.keys())
    chi2_values = [all_results[name]['mean_chi2'] for name in names]

    colors = ['green' if name == best_name else 'gray' for name in names]

    ax1.barh(range(len(names)), chi2_values, color=colors, alpha=0.7)
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels(names, fontsize=10)
    ax1.set_xlabel('χ²_red moyen', fontsize=12, fontweight='bold')
    ax1.set_title('Qualité du Fit par Formulation\n(plus bas = meilleur)',
                  fontsize=14, fontweight='bold')
    ax1.axvline(5, color='green', linestyle='--', linewidth=2, label='Excellent (χ²<5)')
    ax1.axvline(20, color='orange', linestyle='--', linewidth=2, label='Bon (χ²<20)')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Figure 2: k_Asselin par formulation
    k_values = [all_results[name]['mean_k'] for name in names]

    ax2.barh(range(len(names)), k_values, color=colors, alpha=0.7)
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, fontsize=10)
    ax2.set_xlabel('k_Asselin moyen', fontsize=12, fontweight='bold')
    ax2.set_title('Constante de Couplage par Formulation',
                  fontsize=14, fontweight='bold')
    ax2.set_xscale('log')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/comparison_reformulations_k_Asselin.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/comparison_reformulations_k_Asselin.png")

    # Figure 3: Courbes de rotation pour meilleure formulation
    best_results = all_results[best_name]['galaxies']

    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    axes = axes.flatten()

    for idx, galaxy_result in enumerate(best_results):
        ax = axes[idx]

        galaxy_name = galaxy_result['galaxy']
        results = galaxy_result['results']

        r_values = [res['r'] for res in results]
        v_obs = [res['v_obs'] for res in results]
        v_pred = [res['v_pred'] for res in results]
        v_bary = [res['v_bary'] for res in results]

        ax.plot(r_values, v_obs, 'ko', markersize=8, label='v_obs (SPARC)', zorder=3)
        ax.plot(r_values, v_pred, 'b-', linewidth=2.5, label='v_pred (MT)', zorder=2)
        ax.plot(r_values, v_bary, 'r--', linewidth=2, label='v_bary', zorder=1, alpha=0.7)

        ax.set_xlabel('Rayon (kpc)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Vitesse (km/s)', fontsize=11, fontweight='bold')
        ax.set_title(f'{galaxy_name}\nχ²_red = {galaxy_result["chi2_red"]:.2f}',
                     fontsize=12, fontweight='bold')
        ax.legend(fontsize=9, loc='best')
        ax.grid(True, alpha=0.3)

    fig.suptitle(f'Courbes de Rotation - Meilleure Formulation: {best_name}',
                 fontsize=16, fontweight='bold', y=1.00)

    plt.tight_layout()
    plt.savefig('figures/rotation_curves_best_formulation.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/rotation_curves_best_formulation.png")

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":

    import os
    os.makedirs('figures', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    # Test comparatif
    all_results, best_name = compare_all_formulations()

    # Graphiques
    plot_comparison(all_results, best_name)

    # Sauvegarder résultats
    best_data = all_results[best_name]

    with open('results/best_reformulation_k_Asselin.txt', 'w') as f:
        f.write("MEILLEURE REFORMULATION k_Asselin\n")
        f.write("="*80 + "\n\n")
        f.write(f"Formulation: {best_name}\n")
        f.write(f"χ²_red moyen: {best_data['mean_chi2']:.2f}\n")
        f.write(f"k_Asselin moyen: {best_data['mean_k']:.6e}\n\n")

        f.write("RÉSULTATS PAR GALAXIE:\n")
        f.write("-"*80 + "\n")
        for galaxy_result in best_data['galaxies']:
            f.write(f"\n{galaxy_result['galaxy']}:\n")
            f.write(f"  k_Asselin = {galaxy_result['k_asselin']:.6e}\n")
            f.write(f"  χ²_red = {galaxy_result['chi2_red']:.2f}\n")

    print("\n" + "="*80)
    print("✓ ANALYSE TERMINÉE")
    print("="*80)
    print(f"\nFichiers générés:")
    print("  - figures/comparison_reformulations_k_Asselin.png")
    print("  - figures/rotation_curves_best_formulation.png")
    print("  - results/best_reformulation_k_Asselin.txt")
