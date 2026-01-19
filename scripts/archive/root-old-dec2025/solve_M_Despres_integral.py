#!/usr/bin/env python3
"""
Résolution Numérique Équation Intégrale M_Després
Théorie de Maîtrise du Temps

Équation à résoudre:
M_Després(r) = k_Asselin · ∫∫∫ |∇γ_Després(r')|² dV'

Avec:
γ_Després(r) = 1/√(1 - v²(r)/c² - 2Φ(r)/c²)

Méthode: Intégration numérique 3D (sphérique)

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-06
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, dblquad, tplquad
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d import Axes3D
import warnings
warnings.filterwarnings('ignore')

# Constantes
G = 4.302e-6  # kpc (km/s)² M☉⁻¹
c = 299792.458  # km/s

# ============================================
# PROFIL MASSE BARYONIQUE
# ============================================

class GalaxyProfile:
    """
    Profil masse baryonique réaliste
    Disque exponentiel + Bulbe (optionnel)
    """

    def __init__(self, M_disk, R_disk, M_bulge=0, R_bulge=1.0):
        """
        Parameters:
        - M_disk: Masse totale disque (M☉)
        - R_disk: Rayon échelle disque (kpc)
        - M_bulge: Masse bulbe (M☉)
        - R_bulge: Rayon échelle bulbe (kpc)
        """
        self.M_disk = M_disk
        self.R_disk = R_disk
        self.M_bulge = M_bulge
        self.R_bulge = R_bulge

    def M_enclosed(self, r):
        """
        Masse enfermée à rayon r

        Disque exponentiel: M(r) = M_total [1 - (1 + r/R_d) exp(-r/R_d)]
        """
        # Disque
        x = r / self.R_disk
        M_disk_r = self.M_disk * (1 - (1 + x) * np.exp(-x))

        # Bulge (Hernquist approximation)
        if self.M_bulge > 0:
            M_bulge_r = self.M_bulge * (r / (r + self.R_bulge))**2
        else:
            M_bulge_r = 0

        return M_disk_r + M_bulge_r

    def rho(self, r):
        """
        Densité de masse à rayon r
        ρ(r) = (1/4πr²) dM/dr
        """
        dr = 0.01  # kpc
        M1 = self.M_enclosed(r + dr/2)
        M2 = self.M_enclosed(r - dr/2) if r > dr/2 else 0

        dM = M1 - M2
        volume = 4 * np.pi * r**2 * dr

        return dM / volume if volume > 0 else 0

# ============================================
# CARTOGRAPHIE DESPRÉS : γ_Després(r)
# ============================================

def gamma_Despres(r, galaxy_profile):
    """
    Facteur de Lorentz Després

    γ_Després(r) = 1/√(1 - v²(r)/c² - 2Φ(r)/c²)

    Avec:
    - v(r) = vitesse képlérienne
    - Φ(r) = potentiel gravitationnel
    """
    if r < 0.01:  # Éviter division par 0
        r = 0.01

    # Masse enfermée
    M_r = galaxy_profile.M_enclosed(r)

    # Vitesse képlérienne
    v_kepler = np.sqrt(G * M_r / r)

    # Potentiel gravitationnel Φ = -GM/r
    Phi = -G * M_r / r

    # Terme sous racine
    term = 1 - v_kepler**2/c**2 - 2*Phi/c**2

    # γ_Després
    if term > 0:
        gamma = 1.0 / np.sqrt(term)
    else:
        # Régime relativiste extrême (rare)
        gamma = 10.0  # Valeur cap

    return gamma

def gradient_gamma_Despres(r, galaxy_profile, dr=0.1):
    """
    Gradient radial de γ_Després

    |∇γ| = |dγ/dr| (symétrie sphérique)
    """
    if r < dr:
        # Forward difference
        gamma_1 = gamma_Despres(r, galaxy_profile)
        gamma_2 = gamma_Despres(r + dr, galaxy_profile)
        grad = (gamma_2 - gamma_1) / dr
    else:
        # Central difference
        gamma_1 = gamma_Despres(r - dr, galaxy_profile)
        gamma_2 = gamma_Despres(r + dr, galaxy_profile)
        grad = (gamma_2 - gamma_1) / (2*dr)

    return abs(grad)

# ============================================
# INTÉGRALE M_DESPRÉS
# ============================================

def M_Despres_integrand(r_prime, r_obs, galaxy_profile):
    """
    Intégrande pour M_Després

    f(r') = |∇γ_Després(r')|² · W(r', r_obs)

    Avec W(r', r_obs) = facteur poids spatial
    """
    # Gradient γ_Després au point r'
    grad_gamma = gradient_gamma_Despres(r_prime, galaxy_profile)

    # Facteur poids: décroissance avec distance de r_obs
    # Simple: poids uniforme (peut être modifié)
    weight = 1.0

    # Si on veut un poids décroissant:
    # distance = abs(r_prime - r_obs)
    # weight = np.exp(-distance / lambda_decay)

    # Élément volume en coordonnées sphériques: 4π r'²
    volume_element = 4 * np.pi * r_prime**2

    # Intégrande total
    integrand = grad_gamma**2 * weight * volume_element

    return integrand

def M_Despres_enclosed(r_obs, galaxy_profile, k_asselin, r_max=None):
    """
    Masse Després enfermée à rayon r_obs

    M_Després(r) = k_Asselin · ∫₀^r |∇γ_Després(r')|² · 4πr'² dr'

    Parameters:
    - r_obs: rayon où calculer M_Després (kpc)
    - galaxy_profile: profil galaxie
    - k_asselin: constante couplage
    - r_max: rayon maximal intégration (si None, = r_obs)

    Returns:
    - M_Després en M☉
    """
    if r_max is None:
        r_max = r_obs

    # Intégration numérique
    try:
        integral, error = quad(
            M_Despres_integrand,
            0.01,  # r_min (éviter 0)
            r_max,
            args=(r_obs, galaxy_profile),
            limit=100,
            epsabs=1e-6,
            epsrel=1e-6
        )
    except:
        integral = 0
        error = 0

    # M_Després
    M_Despres = k_asselin * integral

    return M_Despres

def M_Despres_profile(galaxy_profile, k_asselin, r_array):
    """
    Profil complet M_Després(r)

    Returns:
    - M_Després(r) pour chaque r dans r_array
    """
    M_Despres_array = []

    print("Calcul profil M_Després...")
    for i, r in enumerate(r_array):
        if i % 10 == 0:
            print(f"  r = {r:.1f} kpc ({i}/{len(r_array)})")

        M_D = M_Despres_enclosed(r, galaxy_profile, k_asselin, r_max=r)
        M_Despres_array.append(M_D)

    return np.array(M_Despres_array)

# ============================================
# VITESSE ROTATION TOTALE
# ============================================

def v_rotation_total(r, M_baryonique, M_Despres):
    """
    Vitesse rotation totale

    v²_tot = GM_bary/r + GM_Després/r
    """
    if r < 0.01:
        r = 0.01

    v_squared = G * (M_baryonique + M_Despres) / r

    return np.sqrt(v_squared)

# ============================================
# CALIBRATION k_Asselin
# ============================================

def calibrate_k_asselin_iterative(galaxy_profile, r_obs, v_obs, r_max=50.0):
    """
    Calibre k_Asselin itérativement pour reproduire v_obs à r_obs

    Méthode: dichotomie
    """
    print(f"\nCalibration k_Asselin pour v({r_obs} kpc) = {v_obs} km/s...")

    # Bornes
    k_min = 1e-8
    k_max = 1e-2
    tolerance = 0.01  # 1%

    M_bary = galaxy_profile.M_enclosed(r_obs)

    for iteration in range(20):
        k_mid = (k_min + k_max) / 2

        # Calculer M_Després avec k_mid
        M_D = M_Despres_enclosed(r_obs, galaxy_profile, k_mid, r_max=r_max)

        # Vitesse prédite
        v_pred = v_rotation_total(r_obs, M_bary, M_D)

        # Erreur relative
        error = abs(v_pred - v_obs) / v_obs

        print(f"  Iter {iteration+1}: k = {k_mid:.3e}, v_pred = {v_pred:.1f} km/s, error = {100*error:.1f}%")

        if error < tolerance:
            print(f"  → Convergé!")
            return k_mid

        # Ajuster bornes
        if v_pred < v_obs:
            # Besoin plus de M_Després → augmenter k
            k_min = k_mid
        else:
            # Trop de M_Després → réduire k
            k_max = k_mid

    print(f"  → Maximum iterations atteint")
    return k_mid

# ============================================
# VISUALISATIONS
# ============================================

def plot_gamma_Despres_profile(galaxy_profile, r_max=50.0):
    """
    Profil γ_Després(r)
    """
    print("\nCréation graphique γ_Després(r)...")

    r_array = np.linspace(0.1, r_max, 200)

    gamma_array = [gamma_Despres(r, galaxy_profile) for r in r_array]
    grad_gamma_array = [gradient_gamma_Despres(r, galaxy_profile) for r in r_array]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Panel 1: γ_Després(r)
    ax1.plot(r_array, gamma_array, linewidth=2.5, color='blue')
    ax1.axhline(1.0, color='red', linestyle='--', linewidth=2, alpha=0.5,
               label='γ = 1 (espace plat)')
    ax1.set_xlabel('Rayon r (kpc)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('γ_Després(r)', fontsize=14, fontweight='bold')
    ax1.set_title('Facteur de Lorentz Després\nγ = 1/√(1 - v²/c² - 2Φ/c²)',
                 fontsize=15, fontweight='bold')
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)

    # Panel 2: |∇γ_Després|
    ax2.plot(r_array, grad_gamma_array, linewidth=2.5, color='green')
    ax2.set_xlabel('Rayon r (kpc)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('|∇γ_Després| (kpc⁻¹)', fontsize=14, fontweight='bold')
    ax2.set_title('Gradient γ_Després\nSource de M_Després',
                 fontsize=15, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/gamma_Despres_profile.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/gamma_Despres_profile.png")

def plot_M_Despres_profile(r_array, M_bary_array, M_Despres_array):
    """
    Profils M_baryonique et M_Després
    """
    print("\nCréation graphique profils masse...")

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(r_array, M_bary_array/1e9, linewidth=2.5, label='M_baryonique',
           color='blue')
    ax.plot(r_array, M_Despres_array/1e9, linewidth=2.5, label='M_Després',
           color='red')
    ax.plot(r_array, (M_bary_array + M_Despres_array)/1e9, linewidth=2.5,
           label='M_totale', color='black', linestyle='--')

    ax.set_xlabel('Rayon r (kpc)', fontsize=15, fontweight='bold')
    ax.set_ylabel('Masse enfermée (10⁹ M☉)', fontsize=15, fontweight='bold')
    ax.set_title('Profils de Masse - Théorie Maîtrise du Temps\nM_Després via intégrale numérique',
                fontsize=16, fontweight='bold')
    ax.legend(fontsize=13, loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/M_Despres_mass_profiles.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/M_Despres_mass_profiles.png")

def plot_rotation_curve(r_array, v_bary, v_total, v_obs=None):
    """
    Courbes de rotation
    """
    print("\nCréation courbe de rotation...")

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(r_array, v_bary, linewidth=2.5, label='Baryonique seul (Newton)',
           color='blue', linestyle='--')
    ax.plot(r_array, v_total, linewidth=2.5, label='Baryonique + M_Després (MT)',
           color='red')

    if v_obs is not None:
        ax.scatter(v_obs[0], v_obs[1], s=100, marker='o', color='black',
                  zorder=5, label='Observations')

    ax.set_xlabel('Rayon r (kpc)', fontsize=15, fontweight='bold')
    ax.set_ylabel('Vitesse rotation v(r) (km/s)', fontsize=15, fontweight='bold')
    ax.set_title('Courbe de Rotation - Maîtrise du Temps\nM_Després = k_Asselin · ∫|∇γ_Després|² dV',
                fontsize=16, fontweight='bold')
    ax.legend(fontsize=13, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(v_total)*1.2)

    plt.tight_layout()
    plt.savefig('figures/rotation_curve_M_Despres.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/rotation_curve_M_Despres.png")

# ============================================
# MAIN - EXEMPLE NGC 3198
# ============================================

if __name__ == "__main__":

    import os
    os.makedirs('figures', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    print("="*70)
    print("RÉSOLUTION NUMÉRIQUE ÉQUATION M_DESPRÉS")
    print("Théorie de Maîtrise du Temps")
    print("="*70)
    print()

    # ========================================
    # EXEMPLE: NGC 3198 (galaxie spirale)
    # ========================================

    print("Galaxie: NGC 3198")
    print("-"*70)

    # Paramètres observationnels
    M_stellar = 6.2e9  # M☉
    M_gas = 2.1e9      # M☉
    M_disk_total = M_stellar + M_gas
    R_disk = 5.0       # kpc (rayon échelle disque)
    R_max = 30.0       # kpc (rayon maximal)

    print(f"M_disk = {M_disk_total:.2e} M☉")
    print(f"R_disk = {R_disk} kpc")
    print(f"R_max = {R_max} kpc")
    print()

    # Créer profil galaxie
    galaxy = GalaxyProfile(M_disk=M_disk_total, R_disk=R_disk)

    # ========================================
    # 1. PROFIL γ_DESPRÉS
    # ========================================

    plot_gamma_Despres_profile(galaxy, r_max=R_max)

    # ========================================
    # 2. CALIBRATION k_Asselin
    # ========================================

    # Point de calibration (observation)
    r_calib = 15.0    # kpc
    v_calib = 150.0   # km/s (vitesse observée typique)

    k_asselin = calibrate_k_asselin_iterative(
        galaxy, r_calib, v_calib, r_max=R_max
    )

    print(f"\n✓ k_Asselin calibré = {k_asselin:.6e}")

    # ========================================
    # 3. PROFIL M_DESPRÉS COMPLET
    # ========================================

    r_array = np.linspace(1.0, R_max, 30)

    M_bary_array = np.array([galaxy.M_enclosed(r) for r in r_array])
    M_Despres_array = M_Despres_profile(galaxy, k_asselin, r_array)

    plot_M_Despres_profile(r_array, M_bary_array, M_Despres_array)

    # ========================================
    # 4. COURBE DE ROTATION
    # ========================================

    v_bary = np.array([np.sqrt(G * M / r) for M, r in zip(M_bary_array, r_array)])
    v_total = np.array([
        v_rotation_total(r, M_b, M_D)
        for r, M_b, M_D in zip(r_array, M_bary_array, M_Despres_array)
    ])

    plot_rotation_curve(r_array, v_bary, v_total, v_obs=([r_calib], [v_calib]))

    # ========================================
    # 5. RAPPORT M_DESPRÉS / M_BARYONIQUE
    # ========================================

    print("\n" + "="*70)
    print("RAPPORT M_DESPRÉS / M_BARYONIQUE")
    print("="*70)

    for i in [5, 10, 15, 20, 25]:
        idx = np.argmin(np.abs(r_array - i))
        r = r_array[idx]
        M_b = M_bary_array[idx]
        M_D = M_Despres_array[idx]
        ratio = M_D / M_b if M_b > 0 else 0

        print(f"r = {r:5.1f} kpc : M_D/M_b = {ratio:.2f}  "
              f"(M_D = {M_D:.2e} M☉, M_b = {M_b:.2e} M☉)")

    # ========================================
    # 6. SAUVEGARDER RÉSULTATS
    # ========================================

    np.savetxt('results/M_Despres_NGC3198.txt',
               np.column_stack([r_array, M_bary_array, M_Despres_array, v_bary, v_total]),
               header='r(kpc)  M_bary(Msun)  M_Despres(Msun)  v_bary(km/s)  v_total(km/s)',
               fmt='%.3f  %.6e  %.6e  %.3f  %.3f')

    with open('results/k_asselin_NGC3198.txt', 'w') as f:
        f.write("="*70 + "\n")
        f.write("CALIBRATION k_Asselin - NGC 3198\n")
        f.write("Résolution numérique M_Després = k ∫|∇γ_Després|² dV\n")
        f.write("="*70 + "\n\n")
        f.write(f"Galaxie: NGC 3198\n")
        f.write(f"M_disk = {M_disk_total:.2e} M☉\n")
        f.write(f"R_disk = {R_disk} kpc\n\n")
        f.write(f"Point calibration:\n")
        f.write(f"  r = {r_calib} kpc\n")
        f.write(f"  v_obs = {v_calib} km/s\n\n")
        f.write(f"k_Asselin = {k_asselin:.6e}\n\n")
        f.write(f"Rapport M_Després/M_baryonique à {R_max} kpc: {M_Despres_array[-1]/M_bary_array[-1]:.2f}\n")

    print("\n" + "="*70)
    print("✓ RÉSOLUTION TERMINÉE")
    print("="*70)
    print(f"k_Asselin = {k_asselin:.6e}")
    print(f"M_Després({R_max} kpc) = {M_Despres_array[-1]:.2e} M☉")
    print(f"M_Després / M_baryonique = {M_Despres_array[-1]/M_bary_array[-1]:.2f}")
    print()
    print("Fichiers générés:")
    print("  - figures/gamma_Despres_profile.png")
    print("  - figures/M_Despres_mass_profiles.png")
    print("  - figures/rotation_curve_M_Despres.png")
    print("  - results/M_Despres_NGC3198.txt")
    print("  - results/k_asselin_NGC3198.txt")
    print()
    print("ÉQUATION RÉSOLUE:")
    print("  M_Després(r) = k_Asselin · ∫₀^r |∇γ_Després(r')|² · 4πr'² dr'")
    print("  avec γ_Després = 1/√(1 - v²/c² - 2Φ/c²)")
    print("="*70)
