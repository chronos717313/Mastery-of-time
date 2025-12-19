#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST: Superposition Temporelle (Temps Forward + Backward)

MODÈLE:
M_eff(r) = M_visible(r) × [1 + β²(r)/α²(r)]

où:
- α²(r) + β²(r) = 1
- α²(r) = 1/(1 + (r/r_c)^n)  (temps forward)
- β²(r) = (r/r_c)^n/(1 + (r/r_c)^n)  (temps backward)
- r_c: rayon caractéristique superposition
- n: exposant (contrôle transition)
"""

import numpy as np
import math
from scipy.optimize import minimize

# ============================================================================
# CONSTANTES
# ============================================================================
G = 6.67430e-11  # m^3 kg^-1 s^-2
c = 299792458.0  # m/s
kpc_to_m = 3.0857e19  # m
M_soleil = 1.989e30  # kg

# ============================================================================
# DONNÉES GALAXIES
# ============================================================================

# M31
M31_r_obs = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 35])
M31_v_obs = np.array([120, 180, 210, 225, 235, 240, 245, 250, 255, 260, 258, 255, 252, 250, 248, 245, 240])
M31_sigma = np.array([15.0] * len(M31_v_obs))
M31_M_bulbe = 3.0e10 * M_soleil
M31_a_bulbe = 1.0
M31_M_disque = 1.2e11 * M_soleil
M31_R_d = 5.5
M31_M_gaz = 1.5e10 * M_soleil
M31_R_gaz = 12.0

# Voie Lactée
VL_r_obs = np.array([0.5, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 120, 140])
VL_v_obs = np.array([45, 100, 150, 175, 190, 200, 205, 210, 215, 218, 220, 221, 220, 218, 215, 210, 208, 205, 203, 201, 200, 198, 195])
VL_sigma = np.array([10.0] * len(VL_v_obs))
VL_M_bulbe = 1.5e10 * M_soleil
VL_a_bulbe = 0.7
VL_M_disque = 6.0e10 * M_soleil
VL_R_d = 2.5
VL_M_gaz = 5.0e9 * M_soleil
VL_R_gaz = 7.0

# NGC 3198
NGC_r_obs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30])
NGC_v_obs = np.array([60, 90, 110, 125, 135, 145, 150, 152, 153, 155, 157, 158, 158, 157, 155, 154, 152, 150, 148, 145])
NGC_sigma = np.array([10.0] * len(NGC_v_obs))
NGC_M_bulbe = 8.0e9 * M_soleil
NGC_a_bulbe = 0.6
NGC_M_disque = 4.0e10 * M_soleil
NGC_R_d = 3.0
NGC_M_gaz = 5.0e9 * M_soleil
NGC_R_gaz = 8.0

# ============================================================================
# FONCTIONS MASSE
# ============================================================================

def masse_bulbe_spherique(r_kpc, M_bulbe, a):
    return M_bulbe * r_kpc**2 / (r_kpc + a)**2

def masse_disque(r_kpc, M_disque, R_d):
    return M_disque * (1.0 - np.exp(-r_kpc/R_d) * (1.0 + r_kpc/R_d))

def masse_gaz(r_kpc, M_gaz, R_g):
    return M_gaz * (1.0 - np.exp(-r_kpc/R_g) * (1.0 + r_kpc/R_g))

def masse_visible(r_kpc, M_bulbe, a, M_disque, R_d, M_gaz, R_g):
    return (masse_bulbe_spherique(r_kpc, M_bulbe, a) +
            masse_disque(r_kpc, M_disque, R_d) +
            masse_gaz(r_kpc, M_gaz, R_g))

# ============================================================================
# SUPERPOSITION TEMPORELLE
# ============================================================================

def alpha_squared(r_kpc, r_c, n):
    """
    Fraction temps forward: α²(r)

    α²(r) = 1 / (1 + (r/r_c)^n)

    - r << r_c: α² → 1 (temps forward pur)
    - r >> r_c: α² → 0 (temps backward dominant)
    - r = r_c: α² = 0.5 (superposition maximale)
    """
    x = (r_kpc / r_c)**n
    return 1.0 / (1.0 + x)

def beta_squared(r_kpc, r_c, n):
    """
    Fraction temps backward: β²(r)

    β²(r) = (r/r_c)^n / (1 + (r/r_c)^n)

    Normalisation: α²(r) + β²(r) = 1
    """
    x = (r_kpc / r_c)**n
    return x / (1.0 + x)

def facteur_superposition(r_kpc, r_c, n):
    """
    Facteur multiplicatif masse effective:

    f(r) = 1 + β²(r)/α²(r)

    - r << r_c: f → 1 (pas d'effet)
    - r = r_c: f = 2 (doublement!)
    - r >> r_c: f → ∞ (diverge, mais masse visible → cste)
    """
    alpha2 = alpha_squared(r_kpc, r_c, n)
    beta2 = beta_squared(r_kpc, r_c, n)

    if alpha2 < 1e-10:
        alpha2 = 1e-10  # régularisation

    return 1.0 + (beta2 / alpha2)

def masse_effective_superposition(r_kpc, M_visible, r_c, n):
    """
    Masse effective avec superposition temporelle

    M_eff(r) = M_vis(r) × [1 + β²(r)/α²(r)]
    """
    f = facteur_superposition(r_kpc, r_c, n)
    return M_visible * f

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_superposition(r_kpc, r_c, n, M_bulbe, a, M_disque, R_d, M_gaz, R_g):
    """
    Vitesse orbitale avec superposition temporelle

    v²(r) = G M_eff(r) / r
    """
    M_vis = masse_visible(r_kpc, M_bulbe, a, M_disque, R_d, M_gaz, R_g)
    M_eff = masse_effective_superposition(r_kpc, M_vis, r_c, n)

    r_m = r_kpc * kpc_to_m
    v2 = G * M_eff / r_m

    if v2 > 0:
        return math.sqrt(v2) / 1000.0  # km/s
    return 0.0

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi2_superposition(r_obs, v_obs, sigma, r_c, n, M_bulbe, a, M_disque, R_d, M_gaz, R_g):
    """Chi² modèle superposition temporelle"""
    chi2 = 0.0
    for r, v_o, sig in zip(r_obs, v_obs, sigma):
        v_t = vitesse_superposition(r, r_c, n, M_bulbe, a, M_disque, R_d, M_gaz, R_g)
        chi2 += ((v_o - v_t) / sig)**2
    return chi2

def chi2_newton(r_obs, v_obs, sigma, M_bulbe, a, M_disque, R_d, M_gaz, R_g):
    """Chi² Newton"""
    chi2 = 0.0
    for r, v_o, sig in zip(r_obs, v_obs, sigma):
        M_vis = masse_visible(r, M_bulbe, a, M_disque, R_d, M_gaz, R_g)
        v_n = math.sqrt(G * M_vis / (r * kpc_to_m)) / 1000.0
        chi2 += ((v_o - v_n) / sig)**2
    return chi2

# ============================================================================
# TESTS PAR GALAXIE
# ============================================================================

def tester_galaxie(nom, r_obs, v_obs, sigma, M_bulbe, a, M_disque, R_d, M_gaz, R_g):
    """Test superposition temporelle sur une galaxie"""

    print(f"\n{'='*80}")
    print(f"  {nom}")
    print(f"{'='*80}")

    # Newton
    chi2_n = chi2_newton(r_obs, v_obs, sigma, M_bulbe, a, M_disque, R_d, M_gaz, R_g)
    print(f"χ² Newton: {chi2_n:.2f}")
    print()

    # Optimisation (r_c, n)
    print("Optimisation r_c et n...")

    def objectif(params):
        r_c, n = params
        if r_c <= 0 or n <= 0:
            return 1e10
        return chi2_superposition(r_obs, v_obs, sigma, r_c, n, M_bulbe, a, M_disque, R_d, M_gaz, R_g)

    # Recherche initiale grossière
    meilleur_chi2 = float('inf')
    meilleur_params = None

    for r_c_init in [10, 30, 50, 100]:
        for n_init in [1.0, 2.0, 3.0]:
            result = minimize(objectif, [r_c_init, n_init],
                            method='Nelder-Mead',
                            options={'maxiter': 1000})

            if result.fun < meilleur_chi2:
                meilleur_chi2 = result.fun
                meilleur_params = result.x

    r_c_opt, n_opt = meilleur_params
    chi2_opt = meilleur_chi2

    ratio = chi2_opt / chi2_n
    amelioration = (1.0 - ratio) * 100.0

    print(f"r_c optimal: {r_c_opt:.1f} kpc")
    print(f"n optimal: {n_opt:.2f}")
    print(f"χ² optimal: {chi2_opt:.2f} ({ratio:.3f}× Newton)")
    print()

    if ratio < 1.0:
        print(f"✅ SUCCÈS! Amélioration: {amelioration:.1f}%")
    else:
        print(f"❌ Échec. Dégradation: {-amelioration:.1f}%")

    # Analyser profil α²(r), β²(r)
    print()
    print("Profil superposition temporelle:")
    r_test = [0, 10, 30, 50, 100]
    for r in r_test:
        if r <= max(r_obs):
            alpha2 = alpha_squared(r, r_c_opt, n_opt)
            beta2 = beta_squared(r, r_c_opt, n_opt)
            ratio_ba = beta2/alpha2 if alpha2 > 1e-10 else float('inf')
            print(f"  r={r:>3} kpc: α²={alpha2:.3f}, β²={beta2:.3f}, β²/α²={ratio_ba:.2f}")

    return chi2_n, chi2_opt, r_c_opt, n_opt

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("    TEST: SUPERPOSITION TEMPORELLE (Forward + Backward)")
    print("="*80)
    print()
    print("MODÈLE: M_eff(r) = M_vis(r) × [1 + β²(r)/α²(r)]")
    print()
    print("où:")
    print("  α²(r) = temps forward")
    print("  β²(r) = temps backward")
    print("  α²(r) + β²(r) = 1 (normalisation)")
    print()

    resultats = {}

    # Test galaxies
    resultats['M31'] = tester_galaxie(
        'M31 (ANDROMÈDE)', M31_r_obs, M31_v_obs, M31_sigma,
        M31_M_bulbe, M31_a_bulbe, M31_M_disque, M31_R_d, M31_M_gaz, M31_R_gaz
    )

    resultats['VL'] = tester_galaxie(
        'VOIE LACTÉE', VL_r_obs, VL_v_obs, VL_sigma,
        VL_M_bulbe, VL_a_bulbe, VL_M_disque, VL_R_d, VL_M_gaz, VL_R_gaz
    )

    resultats['NGC'] = tester_galaxie(
        'NGC 3198 (ISOLÉE)', NGC_r_obs, NGC_v_obs, NGC_sigma,
        NGC_M_bulbe, NGC_a_bulbe, NGC_M_disque, NGC_R_d, NGC_M_gaz, NGC_R_gaz
    )

    # Tableau récapitulatif
    print("\n" + "="*80)
    print("                      TABLEAU RÉCAPITULATIF")
    print("="*80)
    print(f"{'Galaxie':<15} {'Newton':>10} {'Superpos.':>12} {'Ratio':>10} {'r_c (kpc)':>12} {'n':>6}")
    print("-"*80)

    galaxies = [
        ('M31', resultats['M31']),
        ('Voie Lactée', resultats['VL']),
        ('NGC 3198', resultats['NGC']),
    ]

    for nom, (chi2_n, chi2_s, r_c, n) in galaxies:
        ratio = chi2_s / chi2_n
        print(f"{nom:<15} {chi2_n:>10.0f} {chi2_s:>12.0f} {ratio:>10.3f}× {r_c:>12.1f} {n:>6.2f}")

    # Comparaison avec autres approches
    print("\n" + "="*80)
    print("        COMPARAISON AVEC APPROCHES PRÉCÉDENTES (M31)")
    print("="*80)
    print(f"{'Approche':<35} {'χ²':>12} {'vs Newton':>12}")
    print("-"*80)
    print(f"{'Newton (baseline)':<35} {resultats['M31'][0]:>12.0f} {'1.000×':>12}")
    print(f"{'Alignement seul':<35} {'390':>12} {'0.907×':>12}")
    print(f"{'Maxwell ad-hoc':<35} {'348,958':>12} {'811×':>12}")
    print(f"{'GR tidal':<35} {'10^16':>12} {'10^13×':>12}")
    ratio_super = resultats['M31'][1]/resultats['M31'][0]
    print(f"{'Superposition temporelle':<35} {resultats['M31'][1]:>12.0f} {ratio_super:.3f}×")
    print("="*80)

    print()
    print("CONCLUSION:")
    succès = sum(1 for _, (chi2_n, chi2_s, _, _) in galaxies if chi2_s < chi2_n)
    print(f"  Succès: {succès}/3 galaxies")

    if succès == 3:
        print("  ✅ La superposition temporelle FONCTIONNE pour toutes les galaxies!")
    elif succès >= 2:
        print("  ✅ La superposition temporelle fonctionne pour la majorité")
    else:
        print("  ❌ La superposition temporelle ne fonctionne pas mieux")

    print()

if __name__ == "__main__":
    main()
