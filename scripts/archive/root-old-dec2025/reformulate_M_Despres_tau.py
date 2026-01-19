#!/usr/bin/env python3
"""
Reformulation M_Després avec τ(r) et Φ(r)
Théorie de Maîtrise du Temps

PROBLÈME: M_D ∝ ∫|∇γ|² dV ne fonctionne pas (γ ≈ 1)

NOUVELLES FORMULATIONS:
1. M_D ∝ ∫|∇τ|² · r^n dV   (gradient distorsion temporelle)
2. M_D ∝ ∫Φ² · r^m dV       (potentiel gravitationnel)

Où:
- τ(r) = GM/(rc²) = Φ/c²
- Φ(r) = -GM/r

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-07
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

# Constantes
G = 4.302e-6  # kpc (km/s)² / M☉
c = 299792.458  # km/s

# Données SPARC
SPARC_SAMPLE = {
    'NGC2403': {
        'M_stellar': 3.5e9, 'M_gas': 1.8e9, 'R_max': 25.0,
        'data_points': [(2.0, 62.3), (4.0, 86.2), (6.0, 99.5), (8.0, 107.8),
                        (10.0, 112.4), (12.0, 114.4), (15.0, 115.8), (20.0, 115.2)]
    },
    'NGC3198': {
        'M_stellar': 6.2e9, 'M_gas': 2.1e9, 'R_max': 30.0,
        'data_points': [(3.0, 85.4), (6.0, 121.6), (9.0, 138.2), (12.0, 147.3),
                        (15.0, 150.0), (18.0, 151.8), (21.0, 151.2), (25.0, 149.5)]
    },
    'NGC6503': {
        'M_stellar': 1.8e9, 'M_gas': 8e8, 'R_max': 15.0,
        'data_points': [(1.0, 45.2), (2.0, 68.7), (3.0, 84.5), (4.0, 95.3),
                        (5.0, 102.1), (7.0, 109.8), (10.0, 115.6), (12.0, 117.2)]
    },
    'DDO154': {
        'M_stellar': 1.5e8, 'M_gas': 5e8, 'R_max': 8.0,
        'data_points': [(0.5, 18.2), (1.0, 28.5), (2.0, 42.3), (3.0, 48.7),
                        (4.0, 51.2), (5.0, 51.8), (6.0, 51.5)]
    },
    'UGC2885': {
        'M_stellar': 5.0e10, 'M_gas': 8e9, 'R_max': 80.0,
        'data_points': [(10.0, 185.3), (20.0, 245.6), (30.0, 270.2), (40.0, 282.4),
                        (50.0, 285.6), (60.0, 284.8), (70.0, 282.1)]
    },
    'NGC2841': {
        'M_stellar': 3.8e10, 'M_gas': 3.2e9, 'R_max': 60.0,
        'data_points': [(8.0, 165.8), (15.0, 225.3), (22.0, 257.8), (30.0, 275.4),
                        (38.0, 280.6), (45.0, 281.2), (55.0, 278.5)]
    }
}

# ==============================================================================
# PROFIL GALACTIQUE
# ==============================================================================

class GalaxyProfile:
    def __init__(self, M_disk, R_disk):
        self.M_disk = M_disk
        self.R_disk = R_disk

    def M_enclosed(self, r):
        """Masse contenue dans rayon r (disque exponentiel)"""
        if r <= 0:
            return 0
        x = r / self.R_disk
        M_r = self.M_disk * (1 - (1 + x) * np.exp(-x))
        return M_r

    def Phi(self, r):
        """Potentiel gravitationnel"""
        if r <= 0.01:
            r = 0.01
        M_r = self.M_enclosed(r)
        return -G * M_r / r

    def tau(self, r):
        """Distorsion temporelle τ = Φ/c²"""
        return self.Phi(r) / c**2

    def v_circular(self, r):
        """Vitesse circulaire baryonique"""
        if r <= 0:
            return 0
        M_r = self.M_enclosed(r)
        return np.sqrt(G * M_r / r)

# ==============================================================================
# FORMULATION 1: M_D ∝ ∫|∇τ|² · r^n dV
# ==============================================================================

def gradient_tau(r, galaxy, dr=0.1):
    """
    Gradient de τ(r)
    |∇τ| = |dτ/dr|
    """
    if r <= dr:
        r = dr + 0.01

    tau1 = galaxy.tau(r - dr)
    tau2 = galaxy.tau(r + dr)

    grad = abs((tau2 - tau1) / (2 * dr))
    return grad

def M_Despres_tau_formulation(r_obs, galaxy, k_tau, n_power=2):
    """
    M_Després = k_tau · ∫ |∇τ(r')|² · r'^n dV'

    n_power:
    - n=2: Standard (surface 4πr²)
    - n=3: Volumétrique linéaire
    - n=4: Volumétrique quadratique
    """
    r_max = r_obs * 3

    def integrand(r_prime):
        grad_tau = gradient_tau(r_prime, galaxy)
        volume_element = 4 * np.pi * r_prime**2
        volumetric_factor = r_prime**n_power

        return grad_tau**2 * volume_element * volumetric_factor

    integral, _ = quad(integrand, 0.01, r_max, limit=100)
    M_D = k_tau * integral

    return M_D

# ==============================================================================
# FORMULATION 2: M_D ∝ ∫Φ² · r^m dV
# ==============================================================================

def M_Despres_Phi_formulation(r_obs, galaxy, k_phi, m_power=2):
    """
    M_Després = k_phi · ∫ Φ(r')² · r'^m dV'

    m_power:
    - m=0: Intégrale Φ² pure
    - m=2: Standard avec volume
    - m=3: Volumétrique linéaire
    """
    r_max = r_obs * 3

    def integrand(r_prime):
        Phi = galaxy.Phi(r_prime)
        volume_element = 4 * np.pi * r_prime**2
        volumetric_factor = r_prime**m_power

        return Phi**2 * volume_element * volumetric_factor

    integral, _ = quad(integrand, 0.01, r_max, limit=100)
    M_D = k_phi * integral

    return M_D

# ==============================================================================
# CALIBRATION
# ==============================================================================

def calibrate_k(galaxy, r_obs, v_obs, formulation='tau', power=2):
    """
    Calibre k pour reproduire v_obs
    """
    M_bary = galaxy.M_enclosed(r_obs)
    v_bary = np.sqrt(G * M_bary / r_obs)

    # Masse Després nécessaire
    M_D_needed = (v_obs**2 - v_bary**2) * r_obs / G

    if M_D_needed <= 0:
        return 0

    # Fonction objectif
    def objective(k):
        if formulation == 'tau':
            M_D = M_Despres_tau_formulation(r_obs, galaxy, k, n_power=power)
        elif formulation == 'phi':
            M_D = M_Despres_Phi_formulation(r_obs, galaxy, k, m_power=power)
        else:
            M_D = 0

        error = abs(M_D - M_D_needed)
        return error

    # Optimisation
    result = minimize_scalar(objective, bounds=(1e-30, 1e30), method='bounded')
    k_optimal = result.x

    return k_optimal

# ==============================================================================
# TEST GALAXIES
# ==============================================================================

def test_galaxy(galaxy_name, galaxy_data, formulation='tau', power=2):
    """Test formulation sur une galaxie"""
    M_total = galaxy_data['M_stellar'] + galaxy_data['M_gas']
    R_disk = galaxy_data['R_max'] / 4.0

    galaxy = GalaxyProfile(M_disk=M_total, R_disk=R_disk)
    data_points = galaxy_data['data_points']

    # Calibrer sur point milieu
    mid_index = len(data_points) // 2
    r_calib, v_calib = data_points[mid_index]

    k_calib = calibrate_k(galaxy, r_calib, v_calib, formulation=formulation, power=power)

    # Prédire courbe complète
    results = []
    for r_obs, v_obs in data_points:
        M_bary = galaxy.M_enclosed(r_obs)
        v_bary = np.sqrt(G * M_bary / r_obs) if r_obs > 0 else 0

        if formulation == 'tau':
            M_D = M_Despres_tau_formulation(r_obs, galaxy, k_calib, n_power=power)
        elif formulation == 'phi':
            M_D = M_Despres_Phi_formulation(r_obs, galaxy, k_calib, m_power=power)
        else:
            M_D = 0

        M_total = M_bary + M_D
        v_pred = np.sqrt(G * M_total / r_obs) if r_obs > 0 else 0

        results.append({
            'r': r_obs,
            'v_obs': v_obs,
            'v_bary': v_bary,
            'v_pred': v_pred,
            'M_D': M_D,
            'M_bary': M_bary
        })

    # χ²
    chi2 = sum(((res['v_pred'] - res['v_obs']) / res['v_obs'])**2 for res in results)
    chi2_red = chi2 / len(results)

    return {
        'galaxy': galaxy_name,
        'k': k_calib,
        'chi2_red': chi2_red,
        'results': results
    }

# ==============================================================================
# COMPARAISON
# ==============================================================================

def compare_formulations():
    """Compare formulations τ et Φ"""
    print("="*80)
    print("REFORMULATION M_DESPRÉS: τ(r) et Φ(r)")
    print("="*80)
    print()

    formulations = [
        # Gradient τ
        {'name': '|∇τ|² · r² (n=2)', 'type': 'tau', 'power': 2},
        {'name': '|∇τ|² · r³ (n=3)', 'type': 'tau', 'power': 3},
        {'name': '|∇τ|² · r⁴ (n=4)', 'type': 'tau', 'power': 4},

        # Potentiel Φ
        {'name': 'Φ² · r⁰ (m=0)', 'type': 'phi', 'power': 0},
        {'name': 'Φ² · r² (m=2)', 'type': 'phi', 'power': 2},
        {'name': 'Φ² · r³ (m=3)', 'type': 'phi', 'power': 3},
    ]

    all_results = {}

    for formulation in formulations:
        print(f"\n{'='*80}")
        print(f"FORMULATION: {formulation['name']}")
        print(f"{'='*80}\n")

        form_results = []

        for galaxy_name, galaxy_data in SPARC_SAMPLE.items():
            result = test_galaxy(
                galaxy_name, galaxy_data,
                formulation=formulation['type'],
                power=formulation['power']
            )

            form_results.append(result)

            print(f"{galaxy_name}:")
            print(f"  k = {result['k']:.6e}")
            print(f"  χ²_red = {result['chi2_red']:.2f}")

            # Quelques points
            for res in result['results'][::2]:
                ratio = res['v_pred'] / res['v_obs'] if res['v_obs'] > 0 else 0
                print(f"    r={res['r']:5.1f} kpc: v_obs={res['v_obs']:6.1f}, "
                      f"v_pred={res['v_pred']:6.1f}, ratio={ratio:.2f}")
            print()

        # Moyenne
        mean_chi2 = np.mean([r['chi2_red'] for r in form_results])
        mean_k = np.mean([r['k'] for r in form_results])

        print(f"MOYENNE:")
        print(f"  <χ²_red> = {mean_chi2:.2f}")
        print(f"  <k> = {mean_k:.6e}")

        all_results[formulation['name']] = {
            'mean_chi2': mean_chi2,
            'mean_k': mean_k,
            'galaxies': form_results
        }

    # Résumé
    print(f"\n{'='*80}")
    print("RÉSUMÉ COMPARATIF")
    print(f"{'='*80}\n")

    print(f"{'Formulation':<25} {'<χ²_red>':<12} {'<k>':<15}")
    print("-"*80)

    sorted_results = sorted(all_results.items(), key=lambda x: x[1]['mean_chi2'])

    for name, data in sorted_results:
        print(f"{name:<25} {data['mean_chi2']:>10.2f}  {data['mean_k']:>15.6e}")

    print()
    best_name, best_data = sorted_results[0]
    print("MEILLEURE FORMULATION:")
    print(f"  → {best_name}")
    print(f"  → χ²_red = {best_data['mean_chi2']:.2f}")
    print(f"  → k = {best_data['mean_k']:.6e}")
    print()

    if best_data['mean_chi2'] < 2:
        print("  ✓✓✓ EXCELLENT FIT (χ²_red < 2) - SUCCÈS!")
    elif best_data['mean_chi2'] < 10:
        print("  ✓✓ BON FIT (χ²_red < 10)")
    elif best_data['mean_chi2'] < 50:
        print("  ✓ FIT ACCEPTABLE (χ²_red < 50)")
    else:
        print("  ✗ FIT MÉDIOCRE (χ²_red > 50)")

    return all_results, best_name

# ==============================================================================
# GRAPHIQUES
# ==============================================================================

def plot_results(all_results, best_name):
    """Graphiques comparatifs"""
    print("\nCréation graphiques...")

    best_data = all_results[best_name]

    # Figure 1: Courbes rotation (meilleure formulation)
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    axes = axes.flatten()

    for idx, galaxy_result in enumerate(best_data['galaxies']):
        ax = axes[idx]

        results = galaxy_result['results']
        r_vals = [res['r'] for res in results]
        v_obs = [res['v_obs'] for res in results]
        v_pred = [res['v_pred'] for res in results]
        v_bary = [res['v_bary'] for res in results]

        ax.plot(r_vals, v_obs, 'ko', markersize=8, label='v_obs', zorder=3)
        ax.plot(r_vals, v_pred, 'b-', linewidth=2.5, label='v_pred (MT)', zorder=2)
        ax.plot(r_vals, v_bary, 'r--', linewidth=2, label='v_bary', alpha=0.7, zorder=1)

        ax.set_xlabel('Rayon (kpc)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Vitesse (km/s)', fontsize=11, fontweight='bold')
        ax.set_title(f'{galaxy_result["galaxy"]}\nχ²_red = {galaxy_result["chi2_red"]:.2f}',
                     fontsize=12, fontweight='bold')
        ax.legend(fontsize=9, loc='best')
        ax.grid(True, alpha=0.3)

    fig.suptitle(f'Courbes Rotation - Formulation: {best_name}',
                 fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('figures/rotation_curves_tau_phi_formulation.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/rotation_curves_tau_phi_formulation.png")

    # Figure 2: Comparaison χ²
    fig, ax = plt.subplots(figsize=(12, 8))

    names = list(all_results.keys())
    chi2_vals = [all_results[name]['mean_chi2'] for name in names]
    colors = ['green' if name == best_name else 'gray' for name in names]

    ax.barh(range(len(names)), chi2_vals, color=colors, alpha=0.7)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('χ²_red moyen', fontsize=12, fontweight='bold')
    ax.set_title('Qualité Fit: Formulations τ et Φ', fontsize=14, fontweight='bold')
    ax.axvline(2, color='green', linestyle='--', linewidth=2, label='Excellent (χ²<2)')
    ax.axvline(10, color='orange', linestyle='--', linewidth=2, label='Bon (χ²<10)')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/comparison_tau_phi_formulations.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/comparison_tau_phi_formulations.png")

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    import os
    os.makedirs('figures', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    all_results, best_name = compare_formulations()
    plot_results(all_results, best_name)

    # Sauvegarder
    best_data = all_results[best_name]

    with open('results/reformulation_tau_phi_results.txt', 'w') as f:
        f.write("REFORMULATION M_DESPRÉS: τ(r) et Φ(r)\n")
        f.write("="*80 + "\n\n")
        f.write(f"MEILLEURE FORMULATION: {best_name}\n")
        f.write(f"χ²_red moyen: {best_data['mean_chi2']:.2f}\n")
        f.write(f"k moyen: {best_data['mean_k']:.6e}\n\n")

        f.write("RÉSULTATS PAR GALAXIE:\n")
        f.write("-"*80 + "\n")
        for galaxy_result in best_data['galaxies']:
            f.write(f"\n{galaxy_result['galaxy']}:\n")
            f.write(f"  k = {galaxy_result['k']:.6e}\n")
            f.write(f"  χ²_red = {galaxy_result['chi2_red']:.2f}\n")

    print("\n" + "="*80)
    print("✓ ANALYSE TERMINÉE")
    print("="*80)
    print("\nFichiers:")
    print("  - figures/rotation_curves_tau_phi_formulation.png")
    print("  - figures/comparison_tau_phi_formulations.png")
    print("  - results/reformulation_tau_phi_results.txt")
