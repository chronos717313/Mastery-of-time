#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOIE 1 : d_eff Fonction de la Densité Locale
==============================================

Date: 2025-12-05
Objectif: Tester l'hypothèse "Le halo galactique est la limite d'expansion du vide"

Concept:
- Matière ancre l'espace-temps → empêche expansion → GRAND d_eff
- Vide permet expansion temporelle → PETIT d_eff
- d_eff(r) varie radialement avec la densité locale ρ(r)

Formulation:
    d_eff(r) = d_min + (d_max - d_min) · [ρ(r)/ρ₀]^α

Paramètres à optimiser:
- d_min : Distance effective dans le vide (5-20 kpc)
- d_max : Distance effective en haute densité (100-500 kpc)
- α : Exposant de couplage densité (0.1-1.0)

Prédiction: Si correct, χ² < Newton avec paramètres physiquement motivés
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
# DONNÉES OBSERVATIONNELLES - VOIE LACTÉE
# ============================================================================

r_obs_kpc = np.array([
    0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0,
    9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 18.0, 20.0,
    22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0,
    42.0, 44.0, 46.0, 48.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0,
    80.0, 85.0, 90.0, 95.0, 100.0, 110.0, 120.0, 130.0, 140.0
])

v_obs_kms = np.array([
    80, 120, 145, 165, 180, 190, 205, 215, 220, 222, 220,
    218, 215, 213, 210, 208, 206, 205, 203, 202, 200,
    199, 198, 197, 196, 195, 194, 193, 192, 191, 190,
    189, 188, 187, 186, 185, 183, 180, 178, 175, 173,
    170, 168, 165, 163, 160, 155, 150, 145, 140
])

sigma_obs_kms = np.array([10.0] * len(v_obs_kms))

# ============================================================================
# PROFIL DE MASSE VISIBLE
# ============================================================================

def masse_visible(r_kpc):
    """
    Masse visible M_vis(r) - Voie Lactée

    Composantes: Bulbe (Hernquist) + Disque (exp) + Gaz (exp)
    """
    # Bulbe
    M_bulbe = 1.5e10 * M_soleil
    a_bulbe = 0.7
    M_bulbe_r = M_bulbe * (r_kpc**2) / ((r_kpc + a_bulbe)**2)

    # Disque
    M_disque = 6.0e10 * M_soleil
    R_d = 3.5
    x = r_kpc / R_d
    M_disque_r = M_disque * (1 - (1 + x) * math.exp(-x))

    # Gaz
    M_gaz = 1.0e10 * M_soleil
    R_gaz = 7.0
    x_gaz = r_kpc / R_gaz
    M_gaz_r = M_gaz * (1 - (1 + x_gaz) * math.exp(-x_gaz))

    return M_bulbe_r + M_disque_r + M_gaz_r

def dM_visible_dr(r_kpc, dr=0.1):
    """Dérivée numérique dM/dr (kg/kpc)"""
    if r_kpc < dr:
        return (masse_visible(r_kpc + dr) - masse_visible(r_kpc)) / dr
    else:
        return (masse_visible(r_kpc + dr/2) - masse_visible(r_kpc - dr/2)) / dr

# ============================================================================
# DENSITÉ EFFECTIVE
# ============================================================================

def densite_effective(r_kpc):
    """
    Densité effective ρ_eff(r) en kg/m³

    Calculée depuis le profil de masse:
        ρ(r) = (1/4πr²) · dM/dr

    Cette densité inclut toute la matière visible (étoiles, gaz, poussière)
    qui "ancre" l'espace-temps localement.
    """
    if r_kpc < 0.1:
        r_kpc = 0.1  # Éviter division par zéro

    dM_dr = dM_visible_dr(r_kpc)  # kg/kpc

    # Conversion kpc → m
    dM_dr_SI = dM_dr / kpc_to_m  # kg/m

    # Densité surfacique → densité volumique (approximation sphérique)
    r_m = r_kpc * kpc_to_m
    rho = dM_dr_SI / (4 * math.pi * r_m**2)

    return rho  # kg/m³

# ============================================================================
# DISTANCE EFFECTIVE VARIABLE : d_eff(ρ)
# ============================================================================

def d_eff_variable(r_kpc, d_min, d_max, alpha, r_ref=8.0):
    """
    Distance effective fonction de la densité locale

    Formulation:
        d_eff(r) = d_min + (d_max - d_min) · [ρ(r)/ρ_ref]^α

    Physique:
    - Haute densité → matière ancre espace-temps → GRAND d_eff
    - Basse densité → expansion domine → PETIT d_eff

    Args:
        r_kpc: Rayon d'évaluation (kpc)
        d_min: Distance effective minimale (vide) (kpc)
        d_max: Distance effective maximale (haute densité) (kpc)
        alpha: Exposant de couplage
        r_ref: Rayon de référence (défaut: 8 kpc, position du Soleil)

    Returns:
        d_eff en kpc
    """
    # Densités
    rho = densite_effective(r_kpc)
    rho_ref = densite_effective(r_ref)

    # Éviter division par zéro
    if rho_ref < 1e-30:
        rho_ref = 1e-30

    # Ratio de densité
    ratio = (rho / rho_ref)

    # Protection contre ratios extrêmes
    ratio = max(0.001, min(ratio, 1000.0))

    # Distance effective
    d_eff = d_min + (d_max - d_min) * (ratio ** alpha)

    # Clamp aux limites
    d_eff = max(d_min, min(d_eff, d_max))

    return d_eff

# ============================================================================
# MASSE EFFECTIVE AVEC d_eff VARIABLE
# ============================================================================

def masse_effective_d_eff_variable(r_kpc, d_min, d_max, alpha, r_max_integration=500):
    """
    Masse effective avec d_eff fonction de ρ(r)

    Utilise la Formulation C (Enveloppe Différentielle) mais avec
    d_eff LOCAL qui varie selon la densité au point d'évaluation.

    M_eff(r) = M_vis(r) + ∫[r,∞] K(r, r_ext, d_eff(r)) dM_ext

    Kernel: K = [exp(-r/d_eff) - exp(-r_ext/d_eff)] / r_ext

    Args:
        r_kpc: Rayon d'évaluation (kpc)
        d_min, d_max, alpha: Paramètres de d_eff(ρ)
        r_max_integration: Rayon maximal d'intégration

    Returns:
        M_eff en kg
    """
    M_vis = masse_visible(r_kpc)

    # Distance effective au point d'évaluation (variable!)
    d_eff_local = d_eff_variable(r_kpc, d_min, d_max, alpha)

    # Pré-calculer exp(-r/d_eff)
    exp_r = math.exp(-r_kpc / d_eff_local)

    # Intégration sur enveloppes externes
    M_cumul = 0.0
    dr_shell = 1.0  # kpc

    r_shell = r_kpc + dr_shell
    while r_shell < r_max_integration:
        # Masse dans la coquille
        dM_shell = masse_visible(r_shell + dr_shell/2) - masse_visible(r_shell - dr_shell/2)

        if dM_shell < 0:
            dM_shell = 0

        # Kernel avec d_eff LOCAL (au point d'évaluation, pas à r_shell)
        exp_r_ext = math.exp(-r_shell / d_eff_local)
        f_kernel = (exp_r - exp_r_ext) / r_shell

        # Contribution
        M_cumul += dM_shell * f_kernel

        r_shell += dr_shell

        # Critère d'arrêt
        if exp_r_ext < 1e-10:
            break

    # Sécurité
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
    return v_ms / 1000.0  # km/s

def vitesse_orbitale_newton(r_kpc):
    """Vitesse newtonienne (masse visible seule)"""
    M_vis = masse_visible(r_kpc)
    return vitesse_orbitale(r_kpc, M_vis)

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(v_calc, v_obs, sigma_obs):
    """χ² = Σ[(v_calc - v_obs)²/σ²]"""
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# COURBE DE ROTATION AVEC d_eff VARIABLE
# ============================================================================

def courbe_rotation_d_eff_variable(r_array, d_min, d_max, alpha):
    """
    Calcule courbe de rotation avec d_eff(ρ)

    Args:
        r_array: Rayons (kpc)
        d_min, d_max, alpha: Paramètres

    Returns:
        v_array: Vitesses (km/s)
    """
    v_array = []

    for r in r_array:
        M_eff = masse_effective_d_eff_variable(r, d_min, d_max, alpha)
        v = vitesse_orbitale(r, M_eff)
        v_array.append(v)

    return np.array(v_array)

# ============================================================================
# OPTIMISATION
# ============================================================================

def optimiser_parametres_d_eff_variable():
    """
    Optimise (d_min, d_max, α) pour minimiser χ²

    Bornes physiquement motivées:
    - d_min: 5-50 kpc (vide, expansion forte)
    - d_max: 50-500 kpc (haute densité, ancrage fort)
    - alpha: 0.1-1.0 (couplage densité)

    Returns:
        params_opt, chi2_opt
    """
    print("Optimisation des paramètres (d_min, d_max, α)...")
    print("Cela peut prendre quelques minutes...")
    print()

    def objective(params):
        """Fonction objectif: χ²"""
        d_min, d_max, alpha = params

        # Vérification cohérence
        if d_min >= d_max:
            return 1e10  # Pénalité

        try:
            v_calc = courbe_rotation_d_eff_variable(r_obs_kpc, d_min, d_max, alpha)
            chi2 = chi_carre(v_calc, v_obs_kms, sigma_obs_kms)
            return chi2
        except:
            return 1e10

    # Valeurs initiales
    x0 = [10.0, 150.0, 0.4]

    # Bornes
    bounds = [
        (5.0, 50.0),    # d_min
        (50.0, 500.0),  # d_max
        (0.1, 1.0)      # alpha
    ]

    # Optimisation
    result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds,
                     options={'maxiter': 100, 'disp': True})

    d_min_opt, d_max_opt, alpha_opt = result.x
    chi2_opt = result.fun

    print()
    print("Résultats de l'optimisation:")
    print(f"  d_min   = {d_min_opt:.2f} kpc")
    print(f"  d_max   = {d_max_opt:.2f} kpc")
    print(f"  α       = {alpha_opt:.3f}")
    print(f"  χ²      = {chi2_opt:.2f}")
    print()

    return result.x, chi2_opt

# ============================================================================
# TESTS ET COMPARAISONS
# ============================================================================

def test_d_eff_variable_complet():
    """
    Test complet de la Voie 1: d_eff(ρ)

    Compare:
    1. Newton (référence)
    2. d_eff constant = 100 kpc (formulation C standard)
    3. d_eff variable optimisé
    """
    print("=" * 80)
    print(" VOIE 1 : TEST d_eff FONCTION DE ρ(r) ".center(80))
    print("=" * 80)
    print()
    print("Concept: Le halo galactique est la limite d'expansion du vide")
    print("         Matière ancre l'espace-temps → GRAND d_eff")
    print("         Vide permet expansion → PETIT d_eff")
    print()

    # Test 1: Newton
    print("TEST 1: Newton (masse visible seule)")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r) for r in r_obs_kpc])
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_newton:.2f}")
    print()

    # Test 2: d_eff constant = 100 kpc
    print("TEST 2: d_eff constant = 100 kpc (Formulation C)")
    print("-" * 80)
    v_constant = courbe_rotation_d_eff_variable(r_obs_kpc, 100.0, 100.0, 0.0)
    chi2_constant = chi_carre(v_constant, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_constant:.2f} ({chi2_constant/chi2_newton:.2f}× vs Newton)")
    print()

    # Test 3: d_eff variable optimisé
    print("TEST 3: d_eff variable (optimisé)")
    print("-" * 80)
    params_opt, chi2_opt = optimiser_parametres_d_eff_variable()
    d_min_opt, d_max_opt, alpha_opt = params_opt

    v_variable = courbe_rotation_d_eff_variable(r_obs_kpc, d_min_opt, d_max_opt, alpha_opt)

    # Récapitulatif
    print("=" * 80)
    print(" RÉCAPITULATIF ".center(80))
    print("=" * 80)
    print(f"{'Modèle':<30} {'χ²':>15} {'vs Newton':>15}")
    print("-" * 80)
    print(f"{'Newton (référence)':<30} {chi2_newton:>15.2f} {'1.00×':>15}")
    print(f"{'d_eff = 100 kpc (constant)':<30} {chi2_constant:>15.2f} {chi2_constant/chi2_newton:>14.2f}×")
    print(f"{'d_eff variable (optimisé)':<30} {chi2_opt:>15.2f} {chi2_opt/chi2_newton:>14.2f}×")
    print("=" * 80)
    print()

    # Évaluation
    if chi2_opt < chi2_newton:
        amelioration = (1 - chi2_opt/chi2_newton) * 100
        print("✅ SUCCÈS MAJEUR!")
        print(f"   χ² = {chi2_opt:.2f} < Newton ({chi2_newton:.2f})")
        print(f"   Amélioration: {amelioration:.1f}%")
        print()
        print("   LA VOIE 1 FONCTIONNE! 🎉")
        print()
        print("   Paramètres optimaux:")
        print(f"   - d_min = {d_min_opt:.2f} kpc (distance effective dans le vide)")
        print(f"   - d_max = {d_max_opt:.2f} kpc (distance effective en haute densité)")
        print(f"   - α     = {alpha_opt:.3f} (exposant de couplage densité)")
        print()
        print("   PROCHAINES ÉTAPES:")
        print("   1. Tester sur 10 autres galaxies")
        print("   2. Vérifier universalité des paramètres")
        print("   3. Mesurer IDT (γ_Després) pour validation directe")
        print("   4. Préparer publication")
    elif chi2_opt < chi2_constant:
        amelioration = (1 - chi2_opt/chi2_constant) * 100
        print("⚠️  AMÉLIORATION PARTIELLE")
        print(f"   χ² = {chi2_opt:.2f}")
        print(f"   Meilleur que d_eff constant ({amelioration:.1f}% amélioration)")
        print(f"   Mais toujours > Newton ({chi2_opt/chi2_newton:.2f}×)")
        print()
        print("   INTERPRÉTATION:")
        print("   - d_eff variable améliore la formulation")
        print("   - Mais pas suffisant pour dépasser Newton")
        print("   - Tester Voie 2 (réseau Asselin)")
    else:
        print("❌ ÉCHEC")
        print(f"   χ² = {chi2_opt:.2f} ≥ d_eff constant ({chi2_constant:.2f})")
        print()
        print("   INTERPRÉTATION:")
        print("   - d_eff variable ne améliore pas")
        print("   - Hypothèse densité-ancrage insuffisante")
        print("   - Passer à Voie 2 (réseau Asselin)")

    print()

    # Retourner résultats pour graphiques
    return {
        'newton': {'v': v_newton, 'chi2': chi2_newton},
        'constant': {'v': v_constant, 'chi2': chi2_constant},
        'variable': {'v': v_variable, 'chi2': chi2_opt, 'params': params_opt}
    }

# ============================================================================
# GRAPHIQUES
# ============================================================================

def generer_graphiques(resultats):
    """
    Génère graphiques comparatifs

    Args:
        resultats: Dictionnaire avec résultats des tests
    """
    print("Génération des graphiques...")

    params_opt = resultats['variable']['params']
    d_min, d_max, alpha = params_opt

    # Figure 1: Courbes de rotation
    plt.figure(figsize=(16, 12))

    # Subplot 1: Courbes complètes
    plt.subplot(2, 3, 1)
    plt.errorbar(r_obs_kpc, v_obs_kms, yerr=sigma_obs_kms, fmt='o',
                 color='black', label='Observations', alpha=0.7, markersize=4)
    plt.plot(r_obs_kpc, resultats['newton']['v'], 'r--', linewidth=2,
             label=f"Newton (χ²={resultats['newton']['chi2']:.0f})")
    plt.plot(r_obs_kpc, resultats['constant']['v'], 'b:', linewidth=2,
             label=f"d_eff constant (χ²={resultats['constant']['chi2']:.0f})")
    plt.plot(r_obs_kpc, resultats['variable']['v'], 'g-', linewidth=2.5,
             label=f"d_eff variable (χ²={resultats['variable']['chi2']:.0f})")
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Vitesse (km/s)', fontsize=11)
    plt.title('Courbes de Rotation Comparées', fontsize=13, fontweight='bold')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)

    # Subplot 2: Résidus d_eff variable
    plt.subplot(2, 3, 2)
    residus_var = resultats['variable']['v'] - v_obs_kms
    plt.plot(r_obs_kpc, residus_var, 'go-', linewidth=1.5, markersize=4)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Résidus (km/s)', fontsize=11)
    plt.title('Résidus: d_eff Variable', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Subplot 3: d_eff(r) profil
    plt.subplot(2, 3, 3)
    r_plot = np.linspace(0.5, 150, 150)
    d_eff_profile = [d_eff_variable(r, d_min, d_max, alpha) for r in r_plot]
    plt.plot(r_plot, d_eff_profile, 'b-', linewidth=2)
    plt.axhline(d_min, color='r', linestyle='--', linewidth=1, label=f'd_min={d_min:.1f} kpc')
    plt.axhline(d_max, color='g', linestyle='--', linewidth=1, label=f'd_max={d_max:.1f} kpc')
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('d_eff(r) (kpc)', fontsize=11)
    plt.title(f'Profil d_eff(r) (α={alpha:.3f})', fontsize=13, fontweight='bold')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)

    # Subplot 4: Densité ρ(r)
    plt.subplot(2, 3, 4)
    rho_profile = [densite_effective(r) for r in r_plot]
    plt.semilogy(r_plot, rho_profile, 'purple', linewidth=2)
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('ρ(r) (kg/m³)', fontsize=11)
    plt.title('Densité Effective', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)

    # Subplot 5: Masse effective
    plt.subplot(2, 3, 5)
    M_vis_plot = [masse_visible(r) / M_soleil / 1e10 for r in r_plot]
    M_eff_var = [masse_effective_d_eff_variable(r, d_min, d_max, alpha) / M_soleil / 1e10
                 for r in r_plot]
    plt.plot(r_plot, M_vis_plot, 'r--', linewidth=2, label='M_visible')
    plt.plot(r_plot, M_eff_var, 'g-', linewidth=2, label='M_eff (d_eff variable)')
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Masse (10¹⁰ M☉)', fontsize=11)
    plt.title('Masse Effective', fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)

    # Subplot 6: Contribution cumulative
    plt.subplot(2, 3, 6)
    M_cumul = np.array(M_eff_var) - np.array(M_vis_plot)
    plt.plot(r_plot, M_cumul, 'orange', linewidth=2)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('M_cumulatif (10¹⁰ M☉)', fontsize=11)
    plt.title('Contribution Cumulative Asselin', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)

    plt.tight_layout()
    plt.savefig('voie1_d_eff_variable.png', dpi=300, bbox_inches='tight')
    print("  ✓ Graphique sauvegardé: voie1_d_eff_variable.png")
    print()

# ============================================================================
# PROGRAMME PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print(" VOIE 1 : d_eff FONCTION DE LA DENSITÉ LOCALE ".center(80))
    print("="*80 + "\n")

    # Tests complets
    resultats = test_d_eff_variable_complet()

    # Graphiques
    generer_graphiques(resultats)

    print("="*80)
    print(" FIN DU TEST ".center(80))
    print("="*80)
    print()
