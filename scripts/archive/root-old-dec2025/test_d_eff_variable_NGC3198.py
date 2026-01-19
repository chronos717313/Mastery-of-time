#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Voie 1 sur NGC 3198
=========================

Date: 2025-12-05
Objectif: Vérifier si d_eff(ρ) fonctionne sur une autre galaxie spirale

Galaxie: NGC 3198
- Type: Galaxie spirale Sc
- Distance: ~13.8 Mpc
- Masse stellaire: ~3×10¹⁰ M☉
- Rayon optique: ~15 kpc
- Courbe de rotation plate bien mesurée

Questions:
1. Les paramètres optimaux de la Voie Lactée fonctionnent-ils pour NGC 3198?
2. Si on optimise pour NGC 3198, trouve-t-on des paramètres similaires?
3. Peut-on trouver des paramètres UNIVERSELS pour les deux galaxies?
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ============================================================================
# CONSTANTES PHYSIQUES
# ============================================================================

G = 6.674e-11  # m^3 kg^-1 s^-2
c = 299792458  # m/s
M_soleil = 1.989e30  # kg
kpc_to_m = 3.086e19  # m

# ============================================================================
# DONNÉES OBSERVATIONNELLES - NGC 3198
# ============================================================================

# Courbe de rotation de NGC 3198 (Begeman et al. 1991)
# Données HI 21 cm, très précises
r_obs_kpc_ngc3198 = np.array([
    0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
    6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
    16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0
])

# Vitesses observées (km/s)
v_obs_kms_ngc3198 = np.array([
    55, 85, 105, 118, 128, 135, 140, 143, 145, 147,
    149, 150, 151, 151, 151, 151, 150, 150, 149, 149,
    148, 148, 147, 147, 146, 145, 144, 143, 142, 141
])

# Incertitudes (km/s) - estimées à ~5 km/s pour NGC 3198
sigma_obs_kms_ngc3198 = np.array([5.0] * len(v_obs_kms_ngc3198))

# ============================================================================
# PROFIL DE MASSE VISIBLE - NGC 3198
# ============================================================================

def masse_visible_ngc3198(r_kpc):
    """
    Masse visible de NGC 3198

    Composantes:
    - Bulbe: Petit (NGC 3198 est Sc, bulbe faible)
    - Disque: Dominant, M_disque ~ 3×10¹⁰ M☉, R_d ~ 2.5 kpc
    - Gaz HI: Significatif, M_gaz ~ 1×10¹⁰ M☉, R_gaz ~ 8 kpc

    Références: Begeman et al. 1991, van Albada et al. 1985
    """
    # Bulbe (très petit pour Sc)
    M_bulbe = 0.3e10 * M_soleil  # Bulbe faible
    a_bulbe = 0.5  # kpc
    M_bulbe_r = M_bulbe * (r_kpc**2) / ((r_kpc + a_bulbe)**2)

    # Disque stellaire (dominant)
    M_disque = 3.0e10 * M_soleil
    R_d = 2.5  # kpc (échelle plus petite que Voie Lactée)
    x = r_kpc / R_d
    M_disque_r = M_disque * (1 - (1 + x) * math.exp(-x))

    # Gaz HI (important)
    M_gaz = 1.0e10 * M_soleil
    R_gaz = 8.0  # kpc
    x_gaz = r_kpc / R_gaz
    M_gaz_r = M_gaz * (1 - (1 + x_gaz) * math.exp(-x_gaz))

    return M_bulbe_r + M_disque_r + M_gaz_r

def dM_visible_dr_ngc3198(r_kpc, dr=0.1):
    """Dérivée numérique dM/dr pour NGC 3198"""
    if r_kpc < dr:
        return (masse_visible_ngc3198(r_kpc + dr) - masse_visible_ngc3198(r_kpc)) / dr
    else:
        return (masse_visible_ngc3198(r_kpc + dr/2) - masse_visible_ngc3198(r_kpc - dr/2)) / dr

# ============================================================================
# DENSITÉ EFFECTIVE - NGC 3198
# ============================================================================

def densite_effective_ngc3198(r_kpc):
    """
    Densité effective ρ(r) pour NGC 3198

    ρ(r) = (1/4πr²) · dM/dr
    """
    if r_kpc < 0.1:
        r_kpc = 0.1

    dM_dr = dM_visible_dr_ngc3198(r_kpc)
    dM_dr_SI = dM_dr / kpc_to_m

    r_m = r_kpc * kpc_to_m
    rho = dM_dr_SI / (4 * math.pi * r_m**2)

    return rho  # kg/m³

# ============================================================================
# d_eff VARIABLE
# ============================================================================

def d_eff_variable(r_kpc, d_min, d_max, alpha, densite_func, r_ref=8.0):
    """
    Distance effective fonction de ρ(r)

    Args:
        r_kpc: Rayon
        d_min, d_max, alpha: Paramètres
        densite_func: Fonction de densité (spécifique à la galaxie)
        r_ref: Rayon de référence
    """
    rho = densite_func(r_kpc)
    rho_ref = densite_func(r_ref)

    if rho_ref < 1e-30:
        rho_ref = 1e-30

    ratio = rho / rho_ref
    ratio = max(0.001, min(ratio, 1000.0))

    d_eff = d_min + (d_max - d_min) * (ratio ** alpha)
    d_eff = max(d_min, min(d_eff, d_max))

    return d_eff

# ============================================================================
# MASSE EFFECTIVE
# ============================================================================

def masse_effective_d_eff_variable(r_kpc, d_min, d_max, alpha,
                                    masse_func, densite_func, r_max=300):
    """
    Masse effective avec d_eff variable

    Args:
        r_kpc: Rayon
        d_min, d_max, alpha: Paramètres d_eff
        masse_func: Fonction de masse visible
        densite_func: Fonction de densité
        r_max: Rayon max intégration
    """
    M_vis = masse_func(r_kpc)

    d_eff_local = d_eff_variable(r_kpc, d_min, d_max, alpha, densite_func)
    exp_r = math.exp(-r_kpc / d_eff_local)

    M_cumul = 0.0
    dr_shell = 1.0

    r_shell = r_kpc + dr_shell
    while r_shell < r_max:
        dM_shell = masse_func(r_shell + dr_shell/2) - masse_func(r_shell - dr_shell/2)

        if dM_shell < 0:
            dM_shell = 0

        exp_r_ext = math.exp(-r_shell / d_eff_local)
        f_kernel = (exp_r - exp_r_ext) / r_shell

        M_cumul += dM_shell * f_kernel
        r_shell += dr_shell

        if exp_r_ext < 1e-10:
            break

    M_eff = M_vis + M_cumul
    if M_eff < M_vis:
        M_eff = M_vis

    return M_eff

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_orbitale(r_kpc, M_eff_kg):
    """v = sqrt(GM_eff/r)"""
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_eff_kg / r_m)
    return v_ms / 1000.0

def vitesse_orbitale_newton(r_kpc, masse_func):
    """Vitesse newtonienne"""
    M_vis = masse_func(r_kpc)
    return vitesse_orbitale(r_kpc, M_vis)

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(v_calc, v_obs, sigma_obs):
    """χ² = Σ[(v_calc - v_obs)²/σ²]"""
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# COURBE DE ROTATION
# ============================================================================

def courbe_rotation_d_eff_variable(r_array, d_min, d_max, alpha,
                                    masse_func, densite_func):
    """Calcule courbe de rotation avec d_eff variable"""
    v_array = []
    for r in r_array:
        M_eff = masse_effective_d_eff_variable(r, d_min, d_max, alpha,
                                                masse_func, densite_func)
        v = vitesse_orbitale(r, M_eff)
        v_array.append(v)
    return np.array(v_array)

# ============================================================================
# TEST NGC 3198
# ============================================================================

def test_ngc3198():
    """
    Test complet sur NGC 3198

    1. Test avec paramètres Voie Lactée
    2. Optimisation pour NGC 3198
    3. Comparaison
    """
    print("=" * 80)
    print(" TEST VOIE 1 SUR NGC 3198 ".center(80))
    print("=" * 80)
    print()
    print("Galaxie: NGC 3198")
    print("  Type: Spirale Sc")
    print("  Distance: ~13.8 Mpc")
    print("  Masse stellaire: ~3×10¹⁰ M☉")
    print("  Données: HI 21 cm (Begeman et al. 1991)")
    print()

    # Test 1: Newton
    print("TEST 1: Newton (masse visible seule)")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r, masse_visible_ngc3198)
                         for r in r_obs_kpc_ngc3198])
    chi2_newton = chi_carre(v_newton, v_obs_kms_ngc3198, sigma_obs_kms_ngc3198)
    print(f"χ² = {chi2_newton:.2f}")
    print()

    # Test 2: d_eff constant = 100 kpc
    print("TEST 2: d_eff constant = 100 kpc")
    print("-" * 80)
    v_constant = courbe_rotation_d_eff_variable(r_obs_kpc_ngc3198, 100.0, 100.0, 0.0,
                                                 masse_visible_ngc3198, densite_effective_ngc3198)
    chi2_constant = chi_carre(v_constant, v_obs_kms_ngc3198, sigma_obs_kms_ngc3198)
    print(f"χ² = {chi2_constant:.2f} ({chi2_constant/chi2_newton:.2f}× vs Newton)")
    print()

    # Test 3: Paramètres Voie Lactée (d_min=14.95, d_max=500, α=1.0)
    print("TEST 3: Paramètres optimaux Voie Lactée")
    print("-" * 80)
    print("  d_min = 14.95 kpc, d_max = 500 kpc, α = 1.000")
    v_MW_params = courbe_rotation_d_eff_variable(r_obs_kpc_ngc3198, 14.95, 500.0, 1.0,
                                                  masse_visible_ngc3198, densite_effective_ngc3198)
    chi2_MW_params = chi_carre(v_MW_params, v_obs_kms_ngc3198, sigma_obs_kms_ngc3198)
    print(f"χ² = {chi2_MW_params:.2f} ({chi2_MW_params/chi2_newton:.2f}× vs Newton)")
    print()

    # Test 4: Optimisation pour NGC 3198
    print("TEST 4: Optimisation pour NGC 3198")
    print("-" * 80)
    print("Optimisation en cours...")

    def objective(params):
        d_min, d_max, alpha = params
        if d_min >= d_max:
            return 1e10
        try:
            v_calc = courbe_rotation_d_eff_variable(r_obs_kpc_ngc3198, d_min, d_max, alpha,
                                                     masse_visible_ngc3198, densite_effective_ngc3198)
            return chi_carre(v_calc, v_obs_kms_ngc3198, sigma_obs_kms_ngc3198)
        except:
            return 1e10

    result = minimize(objective, x0=[15.0, 200.0, 0.5],
                     bounds=[(5.0, 50.0), (50.0, 500.0), (0.1, 1.0)],
                     method='L-BFGS-B', options={'maxiter': 100})

    d_min_opt, d_max_opt, alpha_opt = result.x
    chi2_opt = result.fun

    print(f"  d_min   = {d_min_opt:.2f} kpc")
    print(f"  d_max   = {d_max_opt:.2f} kpc")
    print(f"  α       = {alpha_opt:.3f}")
    print(f"  χ²      = {chi2_opt:.2f} ({chi2_opt/chi2_newton:.2f}× vs Newton)")
    print()

    # Récapitulatif
    print("=" * 80)
    print(" RÉCAPITULATIF NGC 3198 ".center(80))
    print("=" * 80)
    print(f"{'Modèle':<35} {'χ²':>15} {'vs Newton':>15}")
    print("-" * 80)
    print(f"{'Newton (référence)':<35} {chi2_newton:>15.2f} {'1.00×':>15}")
    print(f"{'d_eff = 100 kpc (constant)':<35} {chi2_constant:>15.2f} {chi2_constant/chi2_newton:>14.2f}×")
    print(f"{'Paramètres Voie Lactée':<35} {chi2_MW_params:>15.2f} {chi2_MW_params/chi2_newton:>14.2f}×")
    print(f"{'Optimisé pour NGC 3198':<35} {chi2_opt:>15.2f} {chi2_opt/chi2_newton:>14.2f}×")
    print("=" * 80)
    print()

    # Analyse
    print("ANALYSE:")
    print()

    if chi2_opt < chi2_newton:
        print("✅ SUCCÈS pour NGC 3198!")
        print(f"   χ² optimisé ({chi2_opt:.2f}) < Newton ({chi2_newton:.2f})")
    else:
        print("⚠️  Même résultat que pour Voie Lactée")
        print(f"   χ² optimisé ({chi2_opt:.2f}) ≈ Newton ({chi2_newton:.2f})")

    print()
    print("COMPARAISON PARAMÈTRES:")
    print(f"  Voie Lactée  : d_min=14.95 kpc, d_max=500.0 kpc, α=1.000")
    print(f"  NGC 3198     : d_min={d_min_opt:.2f} kpc, d_max={d_max_opt:.2f} kpc, α={alpha_opt:.3f}")
    print()

    # Test universalité
    if abs(d_min_opt - 14.95) < 5 and abs(alpha_opt - 1.0) < 0.2:
        print("✅ PARAMÈTRES SIMILAIRES → Possibilité d'universalité!")
    else:
        print("❌ PARAMÈTRES DIFFÉRENTS → Pas de paramètres universels")

    print()

    # Retour résultats
    return {
        'newton': {'v': v_newton, 'chi2': chi2_newton},
        'constant': {'v': v_constant, 'chi2': chi2_constant},
        'MW_params': {'v': v_MW_params, 'chi2': chi2_MW_params},
        'optimized': {'v': courbe_rotation_d_eff_variable(r_obs_kpc_ngc3198,
                                                           d_min_opt, d_max_opt, alpha_opt,
                                                           masse_visible_ngc3198,
                                                           densite_effective_ngc3198),
                     'chi2': chi2_opt,
                     'params': (d_min_opt, d_max_opt, alpha_opt)}
    }

# ============================================================================
# GRAPHIQUES
# ============================================================================

def generer_graphiques_ngc3198(resultats):
    """Génère graphiques pour NGC 3198"""
    print("Génération des graphiques...")

    d_min, d_max, alpha = resultats['optimized']['params']

    plt.figure(figsize=(14, 10))

    # Subplot 1: Courbes de rotation
    plt.subplot(2, 2, 1)
    plt.errorbar(r_obs_kpc_ngc3198, v_obs_kms_ngc3198, yerr=sigma_obs_kms_ngc3198,
                 fmt='o', color='black', label='NGC 3198 (obs)', alpha=0.7, markersize=5)
    plt.plot(r_obs_kpc_ngc3198, resultats['newton']['v'], 'r--', linewidth=2,
             label=f"Newton (χ²={resultats['newton']['chi2']:.0f})")
    plt.plot(r_obs_kpc_ngc3198, resultats['constant']['v'], 'b:', linewidth=2,
             label=f"d_eff constant (χ²={resultats['constant']['chi2']:.0f})")
    plt.plot(r_obs_kpc_ngc3198, resultats['optimized']['v'], 'g-', linewidth=2.5,
             label=f"d_eff variable (χ²={resultats['optimized']['chi2']:.0f})")
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Vitesse (km/s)', fontsize=11)
    plt.title('NGC 3198: Courbes de Rotation', fontsize=13, fontweight='bold')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)

    # Subplot 2: Résidus
    plt.subplot(2, 2, 2)
    residus = resultats['optimized']['v'] - v_obs_kms_ngc3198
    plt.plot(r_obs_kpc_ngc3198, residus, 'go-', linewidth=1.5, markersize=4)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Résidus (km/s)', fontsize=11)
    plt.title('Résidus: d_eff Variable Optimisé', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Subplot 3: Profil d_eff(r)
    plt.subplot(2, 2, 3)
    r_plot = np.linspace(0.5, 35, 100)
    d_eff_profile = [d_eff_variable(r, d_min, d_max, alpha, densite_effective_ngc3198)
                     for r in r_plot]
    plt.plot(r_plot, d_eff_profile, 'b-', linewidth=2)
    plt.axhline(d_min, color='r', linestyle='--', linewidth=1, label=f'd_min={d_min:.1f} kpc')
    plt.axhline(d_max, color='g', linestyle='--', linewidth=1, label=f'd_max={d_max:.1f} kpc')
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('d_eff(r) (kpc)', fontsize=11)
    plt.title(f'Profil d_eff(r) (α={alpha:.3f})', fontsize=13, fontweight='bold')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)

    # Subplot 4: Masse effective
    plt.subplot(2, 2, 4)
    M_vis_plot = [masse_visible_ngc3198(r) / M_soleil / 1e10 for r in r_plot]
    M_eff_plot = [masse_effective_d_eff_variable(r, d_min, d_max, alpha,
                                                  masse_visible_ngc3198,
                                                  densite_effective_ngc3198) / M_soleil / 1e10
                  for r in r_plot]
    plt.plot(r_plot, M_vis_plot, 'r--', linewidth=2, label='M_visible')
    plt.plot(r_plot, M_eff_plot, 'g-', linewidth=2, label='M_eff')
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Masse (10¹⁰ M☉)', fontsize=11)
    plt.title('Masse Effective NGC 3198', fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('voie1_NGC3198.png', dpi=300, bbox_inches='tight')
    print("  ✓ Graphique sauvegardé: voie1_NGC3198.png")
    print()

# ============================================================================
# PROGRAMME PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print(" TEST MULTI-GALAXIES: NGC 3198 ".center(80))
    print("="*80 + "\n")

    resultats = test_ngc3198()
    generer_graphiques_ngc3198(resultats)

    print("="*80)
    print(" FIN DU TEST ".center(80))
    print("="*80)
    print()
