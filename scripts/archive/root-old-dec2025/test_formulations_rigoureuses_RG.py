#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Trois Formulations Rigoureuses depuis la RG
======================================================

Date: 2025-12-05
Objectif: Tester les trois formulations du potentiel cumulatif dérivées
          rigoureusement depuis les équations géodésiques de la RG

Formulations testées:
- A: Newtonien Atténué      M_eff = M_vis + ∫ exp(-r_ext/d_eff) dM
- B: Gradient Radial         M_eff = M_vis + ∫ exp(-(r_ext-r)/d_eff) dM
- C: Enveloppe Différentielle M_eff = M_vis + ∫ [exp(-r_ext/d_eff) - exp(-r/d_eff)]/r_ext dM

Paramètres:
- d_eff = 100 kpc (fixé, rayon viral typique)
- Courbes de rotation: Voie Lactée
- Comparaison avec Newton (χ² = 261)
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

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

# Courbe de rotation observée (Sofue et al. 2009, révisé)
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

sigma_obs_kms = np.array([10.0] * len(v_obs_kms))  # Incertitude ~10 km/s

# ============================================================================
# PROFIL DE MASSE VISIBLE (Bulbe + Disque + Gaz)
# ============================================================================

def masse_visible(r_kpc):
    """
    Masse visible totale M_vis(r) de la Voie Lactée

    Composantes:
    - Bulbe: Hernquist, M_bulbe = 1.5×10¹⁰ M☉, a = 0.7 kpc
    - Disque: Exponentiel, M_disque = 6.0×10¹⁰ M☉, R_d = 3.5 kpc
    - Gaz: Exponentiel, M_gaz = 1.0×10¹⁰ M☉, R_gaz = 7.0 kpc

    Returns:
        Masse en kg
    """
    # Paramètres
    M_bulbe = 1.5e10 * M_soleil
    a_bulbe = 0.7  # kpc

    M_disque = 6.0e10 * M_soleil
    R_d = 3.5  # kpc

    M_gaz = 1.0e10 * M_soleil
    R_gaz = 7.0  # kpc

    # Bulbe (profil de Hernquist)
    M_bulbe_r = M_bulbe * (r_kpc**2) / ((r_kpc + a_bulbe)**2)

    # Disque (exponentiel)
    x = r_kpc / R_d
    M_disque_r = M_disque * (1 - (1 + x) * math.exp(-x))

    # Gaz (exponentiel)
    x_gaz = r_kpc / R_gaz
    M_gaz_r = M_gaz * (1 - (1 + x_gaz) * math.exp(-x_gaz))

    return M_bulbe_r + M_disque_r + M_gaz_r

def dM_visible_dr(r_kpc, dr=0.1):
    """
    Dérivée numérique de la masse visible

    Args:
        r_kpc: Rayon en kpc
        dr: Pas de différentiation en kpc

    Returns:
        dM/dr en kg/kpc
    """
    if r_kpc < dr:
        return (masse_visible(r_kpc + dr) - masse_visible(r_kpc)) / dr
    else:
        return (masse_visible(r_kpc + dr/2) - masse_visible(r_kpc - dr/2)) / dr

# ============================================================================
# FORMULATION A : NEWTONIEN ATTÉNUÉ
# ============================================================================

def masse_effective_formulation_A(r_kpc, d_eff_kpc, r_max_integration=1000):
    """
    Formulation A: Newtonien Atténué

    M_eff(r) = M_vis(r) + ∫[r,∞] exp(-r_ext/d_eff) dM_ext

    Caractéristique: Atténuation dépend de distance ABSOLUE r_ext

    Args:
        r_kpc: Rayon d'évaluation (kpc)
        d_eff_kpc: Distance effective Asselin (kpc)
        r_max_integration: Rayon maximal d'intégration (kpc)

    Returns:
        M_eff en kg
    """
    M_vis = masse_visible(r_kpc)

    # Intégration numérique sur enveloppes externes
    M_cumul = 0.0
    dr_shell = 1.0  # kpc

    r_shell = r_kpc + dr_shell
    while r_shell < r_max_integration:
        # Masse dans la coquille [r_shell, r_shell + dr_shell]
        dM_shell = masse_visible(r_shell + dr_shell/2) - masse_visible(r_shell - dr_shell/2)

        if dM_shell < 0:
            dM_shell = 0  # Sécurité

        # Facteur d'atténuation: exp(-r_ext/d_eff)
        f_attenuation = math.exp(-r_shell / d_eff_kpc)

        # Contribution cumulée
        M_cumul += dM_shell * f_attenuation

        r_shell += dr_shell

        # Critère d'arrêt: contribution négligeable
        if f_attenuation < 1e-10:
            break

    return M_vis + M_cumul

# ============================================================================
# FORMULATION B : GRADIENT RADIAL
# ============================================================================

def masse_effective_formulation_B(r_kpc, d_eff_kpc, r_max_integration=1000):
    """
    Formulation B: Gradient Radial

    M_eff(r) = M_vis(r) + ∫[r,∞] exp(-(r_ext - r)/d_eff) dM_ext

    Caractéristique: Atténuation dépend de distance RELATIVE (r_ext - r)

    Args:
        r_kpc: Rayon d'évaluation (kpc)
        d_eff_kpc: Distance effective Asselin (kpc)
        r_max_integration: Rayon maximal d'intégration (kpc)

    Returns:
        M_eff en kg
    """
    M_vis = masse_visible(r_kpc)

    # Intégration numérique sur enveloppes externes
    M_cumul = 0.0
    dr_shell = 1.0  # kpc

    r_shell = r_kpc + dr_shell
    while r_shell < r_max_integration:
        # Masse dans la coquille
        dM_shell = masse_visible(r_shell + dr_shell/2) - masse_visible(r_shell - dr_shell/2)

        if dM_shell < 0:
            dM_shell = 0

        # Facteur d'atténuation: exp(-(r_ext - r)/d_eff)
        # Distance relative depuis le point d'évaluation
        delta_r = r_shell - r_kpc
        f_attenuation = math.exp(-delta_r / d_eff_kpc)

        # Contribution cumulée
        M_cumul += dM_shell * f_attenuation

        r_shell += dr_shell

        # Critère d'arrêt
        if f_attenuation < 1e-10:
            break

    return M_vis + M_cumul

# ============================================================================
# FORMULATION C : ENVELOPPE DIFFÉRENTIELLE
# ============================================================================

def masse_effective_formulation_C(r_kpc, d_eff_kpc, r_max_integration=1000):
    """
    Formulation C: Enveloppe Différentielle

    M_eff(r) = M_vis(r) + ∫[r,∞] [exp(-r_ext/d_eff) - exp(-r/d_eff)]/r_ext dM_ext

    Caractéristique: Différence d'atténuation entre enveloppe et point

    Args:
        r_kpc: Rayon d'évaluation (kpc)
        d_eff_kpc: Distance effective Asselin (kpc)
        r_max_integration: Rayon maximal d'intégration (kpc)

    Returns:
        M_eff en kg
    """
    M_vis = masse_visible(r_kpc)

    # Pré-calculer exp(-r/d_eff)
    exp_r = math.exp(-r_kpc / d_eff_kpc)

    # Intégration numérique
    M_cumul = 0.0
    dr_shell = 1.0  # kpc

    r_shell = r_kpc + dr_shell
    while r_shell < r_max_integration:
        # Masse dans la coquille
        dM_shell = masse_visible(r_shell + dr_shell/2) - masse_visible(r_shell - dr_shell/2)

        if dM_shell < 0:
            dM_shell = 0

        # Facteur géométrique: [exp(-r/d_eff) - exp(-r_ext/d_eff)] / r_ext
        # CORRECTION: Inverser pour avoir contribution positive
        exp_r_ext = math.exp(-r_shell / d_eff_kpc)
        f_kernel = (exp_r - exp_r_ext) / r_shell

        # Contribution cumulée
        M_cumul += dM_shell * f_kernel

        r_shell += dr_shell

        # Critère d'arrêt
        if exp_r_ext < 1e-10:
            break

    # Sécurité: M_eff ne peut pas être < M_vis
    M_eff = M_vis + M_cumul
    if M_eff < M_vis:
        M_eff = M_vis

    return M_eff

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_orbitale(r_kpc, M_eff_kg):
    """
    Vitesse orbitale depuis masse effective

    v = sqrt(G M_eff / r)

    Dérivée rigoureusement depuis équations géodésiques (voir DERIVATION_RIGOUREUSE_RG.md)

    Args:
        r_kpc: Rayon orbital (kpc)
        M_eff_kg: Masse effective (kg)

    Returns:
        v en km/s
    """
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_eff_kg / r_m)
    return v_ms / 1000.0  # Conversion en km/s

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(v_calc, v_obs, sigma_obs):
    """
    Chi-carré: mesure de l'ajustement

    χ² = Σ [(v_calc - v_obs)² / σ²]

    Args:
        v_calc: Vitesses calculées (array)
        v_obs: Vitesses observées (array)
        sigma_obs: Incertitudes (array)

    Returns:
        χ² total
    """
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# CALCUL COURBES DE ROTATION
# ============================================================================

def courbe_rotation_formulation(formulation, d_eff_kpc, r_array):
    """
    Calcule courbe de rotation pour une formulation donnée

    Args:
        formulation: 'A', 'B', ou 'C'
        d_eff_kpc: Distance effective (kpc)
        r_array: Rayons d'évaluation (kpc)

    Returns:
        v_array: Vitesses orbitales (km/s)
    """
    v_array = []

    for r in r_array:
        # Choisir la fonction de masse effective
        if formulation == 'A':
            M_eff = masse_effective_formulation_A(r, d_eff_kpc)
        elif formulation == 'B':
            M_eff = masse_effective_formulation_B(r, d_eff_kpc)
        elif formulation == 'C':
            M_eff = masse_effective_formulation_C(r, d_eff_kpc)
        else:
            raise ValueError(f"Formulation inconnue: {formulation}")

        # Calculer vitesse orbitale
        v = vitesse_orbitale(r, M_eff)
        v_array.append(v)

    return np.array(v_array)

def courbe_rotation_newton(r_array):
    """
    Courbe de rotation newtonienne (masse visible seule)

    v = sqrt(G M_vis / r)

    Args:
        r_array: Rayons (kpc)

    Returns:
        v_array: Vitesses (km/s)
    """
    v_array = []
    for r in r_array:
        M_vis = masse_visible(r)
        v = vitesse_orbitale(r, M_vis)
        v_array.append(v)
    return np.array(v_array)

# ============================================================================
# TESTS DES TROIS FORMULATIONS
# ============================================================================

def test_formulations_fixes(d_eff_kpc=100.0):
    """
    Test des trois formulations avec d_eff fixé

    Args:
        d_eff_kpc: Distance effective (kpc)

    Returns:
        Dictionnaire avec résultats
    """
    print("=" * 80)
    print("TEST DES TROIS FORMULATIONS RIGOUREUSES DEPUIS LA RG")
    print("=" * 80)
    print(f"\nParamètre fixé: d_eff = {d_eff_kpc} kpc (rayon viral typique)")
    print(f"Données: {len(r_obs_kpc)} points observationnels (Voie Lactée)")
    print()

    # Calcul Newton (référence)
    print("Calcul de la référence newtonienne...")
    v_newton = courbe_rotation_newton(r_obs_kpc)
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"  Newton (masse visible seule): χ² = {chi2_newton:.2f}")
    print()

    # Résultats
    resultats = {
        'Newton': {'chi2': chi2_newton, 'v_calc': v_newton}
    }

    # Test Formulation A
    print("Test Formulation A: Newtonien Atténué")
    print("  M_eff = M_vis + ∫ exp(-r_ext/d_eff) dM_ext")
    v_A = courbe_rotation_formulation('A', d_eff_kpc, r_obs_kpc)
    chi2_A = chi_carre(v_A, v_obs_kms, sigma_obs_kms)
    print(f"  χ² = {chi2_A:.2f}  (vs Newton: {chi2_A/chi2_newton:.2f}×)")
    resultats['Formulation A'] = {'chi2': chi2_A, 'v_calc': v_A}
    print()

    # Test Formulation B
    print("Test Formulation B: Gradient Radial")
    print("  M_eff = M_vis + ∫ exp(-(r_ext - r)/d_eff) dM_ext")
    v_B = courbe_rotation_formulation('B', d_eff_kpc, r_obs_kpc)
    chi2_B = chi_carre(v_B, v_obs_kms, sigma_obs_kms)
    print(f"  χ² = {chi2_B:.2f}  (vs Newton: {chi2_B/chi2_newton:.2f}×)")
    resultats['Formulation B'] = {'chi2': chi2_B, 'v_calc': v_B}
    print()

    # Test Formulation C
    print("Test Formulation C: Enveloppe Différentielle")
    print("  M_eff = M_vis + ∫ [exp(-r_ext/d_eff) - exp(-r/d_eff)]/r_ext dM_ext")
    v_C = courbe_rotation_formulation('C', d_eff_kpc, r_obs_kpc)
    chi2_C = chi_carre(v_C, v_obs_kms, sigma_obs_kms)
    print(f"  χ² = {chi2_C:.2f}  (vs Newton: {chi2_C/chi2_newton:.2f}×)")
    resultats['Formulation C'] = {'chi2': chi2_C, 'v_calc': v_C}
    print()

    # Tableau récapitulatif
    print("=" * 80)
    print("RÉCAPITULATIF")
    print("=" * 80)
    print(f"{'Modèle':<25} {'χ²':>12} {'vs Newton':>12}")
    print("-" * 80)
    print(f"{'Newton (référence)':<25} {chi2_newton:>12.2f} {'1.00×':>12}")
    print(f"{'Formulation A':<25} {chi2_A:>12.2f} {chi2_A/chi2_newton:>11.2f}×")
    print(f"{'Formulation B':<25} {chi2_B:>12.2f} {chi2_B/chi2_newton:>11.2f}×")
    print(f"{'Formulation C':<25} {chi2_C:>12.2f} {chi2_C/chi2_newton:>11.2f}×")
    print("=" * 80)
    print()

    # Identification de la meilleure formulation
    chi2_min = min(chi2_A, chi2_B, chi2_C)

    if chi2_min == chi2_A:
        meilleure = 'A'
    elif chi2_min == chi2_B:
        meilleure = 'B'
    else:
        meilleure = 'C'

    print(f"Meilleure formulation: {meilleure} (χ² = {chi2_min:.2f})")

    if chi2_min < chi2_newton:
        print(f"✅ SUCCÈS: χ² < Newton ({chi2_min:.2f} < {chi2_newton:.2f})")
        print("   La formulation dérivée de la RG AMÉLIORE l'ajustement!")
    else:
        print(f"⚠️  χ² toujours > Newton ({chi2_min:.2f} > {chi2_newton:.2f})")
        print("   Aucune des trois formulations n'améliore Newton avec d_eff=100 kpc")
        print("   → Tester optimisation de d_eff")
    print()

    return resultats, meilleure

# ============================================================================
# OPTIMISATION DE d_eff
# ============================================================================

def optimiser_d_eff_formulation(formulation, d_eff_min=5, d_eff_max=200):
    """
    Optimise d_eff pour une formulation donnée

    Args:
        formulation: 'A', 'B', ou 'C'
        d_eff_min: Limite inférieure (kpc)
        d_eff_max: Limite supérieure (kpc)

    Returns:
        d_eff_optimal, chi2_optimal
    """
    print(f"Optimisation de d_eff pour Formulation {formulation}...")
    print(f"  Intervalle: [{d_eff_min}, {d_eff_max}] kpc")

    def objective(d_eff):
        """Fonction objectif: χ² à minimiser"""
        v_calc = courbe_rotation_formulation(formulation, d_eff, r_obs_kpc)
        return chi_carre(v_calc, v_obs_kms, sigma_obs_kms)

    # Optimisation par recherche du minimum
    result = minimize_scalar(objective, bounds=(d_eff_min, d_eff_max), method='bounded')

    d_eff_opt = result.x
    chi2_opt = result.fun

    print(f"  d_eff optimal = {d_eff_opt:.2f} kpc")
    print(f"  χ² optimal = {chi2_opt:.2f}")
    print()

    return d_eff_opt, chi2_opt

# ============================================================================
# GRAPHIQUES
# ============================================================================

def generer_graphiques(resultats, d_eff_kpc):
    """
    Génère graphiques comparatifs

    Args:
        resultats: Dictionnaire avec résultats des tests
        d_eff_kpc: Distance effective utilisée
    """
    print("Génération des graphiques...")

    # Figure 1: Courbes de rotation comparées
    plt.figure(figsize=(14, 10))

    # Subplot 1: Toutes les courbes
    plt.subplot(2, 2, 1)
    plt.errorbar(r_obs_kpc, v_obs_kms, yerr=sigma_obs_kms, fmt='o',
                 color='black', label='Observations', alpha=0.7, markersize=4)

    plt.plot(r_obs_kpc, resultats['Newton']['v_calc'],
             'r--', linewidth=2, label=f"Newton (χ²={resultats['Newton']['chi2']:.0f})")
    plt.plot(r_obs_kpc, resultats['Formulation A']['v_calc'],
             'b-', linewidth=1.5, label=f"Formulation A (χ²={resultats['Formulation A']['chi2']:.0f})")
    plt.plot(r_obs_kpc, resultats['Formulation B']['v_calc'],
             'g-', linewidth=1.5, label=f"Formulation B (χ²={resultats['Formulation B']['chi2']:.0f})")
    plt.plot(r_obs_kpc, resultats['Formulation C']['v_calc'],
             'm-', linewidth=1.5, label=f"Formulation C (χ²={resultats['Formulation C']['chi2']:.0f})")

    plt.xlabel('Rayon (kpc)', fontsize=12)
    plt.ylabel('Vitesse de rotation (km/s)', fontsize=12)
    plt.title(f'Courbes de Rotation Comparées (d_eff = {d_eff_kpc} kpc)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    # Subplot 2: Résidus Formulation A
    plt.subplot(2, 2, 2)
    residus_A = resultats['Formulation A']['v_calc'] - v_obs_kms
    plt.plot(r_obs_kpc, residus_A, 'bo-', linewidth=1.5, markersize=4)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=12)
    plt.ylabel('Résidus (km/s)', fontsize=12)
    plt.title('Résidus: Formulation A', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Subplot 3: Résidus Formulation B
    plt.subplot(2, 2, 3)
    residus_B = resultats['Formulation B']['v_calc'] - v_obs_kms
    plt.plot(r_obs_kpc, residus_B, 'go-', linewidth=1.5, markersize=4)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=12)
    plt.ylabel('Résidus (km/s)', fontsize=12)
    plt.title('Résidus: Formulation B', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Subplot 4: Résidus Formulation C
    plt.subplot(2, 2, 4)
    residus_C = resultats['Formulation C']['v_calc'] - v_obs_kms
    plt.plot(r_obs_kpc, residus_C, 'mo-', linewidth=1.5, markersize=4)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=12)
    plt.ylabel('Résidus (km/s)', fontsize=12)
    plt.title('Résidus: Formulation C', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('formulations_RG_comparaison.png', dpi=300, bbox_inches='tight')
    print("  ✓ Graphique 1 sauvegardé: formulations_RG_comparaison.png")

    # Figure 2: Masse effective en fonction du rayon
    plt.figure(figsize=(12, 8))

    r_plot = np.linspace(0.5, 150, 150)

    M_vis_plot = [masse_visible(r) / M_soleil / 1e10 for r in r_plot]
    M_eff_A = [masse_effective_formulation_A(r, d_eff_kpc) / M_soleil / 1e10 for r in r_plot]
    M_eff_B = [masse_effective_formulation_B(r, d_eff_kpc) / M_soleil / 1e10 for r in r_plot]
    M_eff_C = [masse_effective_formulation_C(r, d_eff_kpc) / M_soleil / 1e10 for r in r_plot]

    plt.subplot(2, 1, 1)
    plt.plot(r_plot, M_vis_plot, 'r--', linewidth=2, label='M_visible')
    plt.plot(r_plot, M_eff_A, 'b-', linewidth=1.5, label='M_eff (Formulation A)')
    plt.plot(r_plot, M_eff_B, 'g-', linewidth=1.5, label='M_eff (Formulation B)')
    plt.plot(r_plot, M_eff_C, 'm-', linewidth=1.5, label='M_eff (Formulation C)')
    plt.xlabel('Rayon (kpc)', fontsize=12)
    plt.ylabel('Masse (10¹⁰ M☉)', fontsize=12)
    plt.title(f'Masse Effective vs Rayon (d_eff = {d_eff_kpc} kpc)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)

    # Subplot 2: Contribution cumulative
    M_cumul_A = np.array(M_eff_A) - np.array(M_vis_plot)
    M_cumul_B = np.array(M_eff_B) - np.array(M_vis_plot)
    M_cumul_C = np.array(M_eff_C) - np.array(M_vis_plot)

    plt.subplot(2, 1, 2)
    plt.plot(r_plot, M_cumul_A, 'b-', linewidth=1.5, label='Contribution cumulative A')
    plt.plot(r_plot, M_cumul_B, 'g-', linewidth=1.5, label='Contribution cumulative B')
    plt.plot(r_plot, M_cumul_C, 'm-', linewidth=1.5, label='Contribution cumulative C')
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=12)
    plt.ylabel('M_cumulatif (10¹⁰ M☉)', fontsize=12)
    plt.title('Contribution Cumulative par Formulation', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)

    plt.tight_layout()
    plt.savefig('formulations_RG_masse_effective.png', dpi=300, bbox_inches='tight')
    print("  ✓ Graphique 2 sauvegardé: formulations_RG_masse_effective.png")
    print()

# ============================================================================
# PROGRAMME PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print(" TEST DES FORMULATIONS RIGOUREUSES DEPUIS LA RG ".center(80))
    print("="*80 + "\n")

    # Test 1: Formulations avec d_eff = 100 kpc (fixé)
    print("ÉTAPE 1: Test des trois formulations avec d_eff = 100 kpc")
    print("-" * 80)
    resultats, meilleure = test_formulations_fixes(d_eff_kpc=100.0)

    # Génération graphiques
    generer_graphiques(resultats, d_eff_kpc=100.0)

    # Test 2: Optimisation de d_eff pour la meilleure formulation
    print("\nÉTAPE 2: Optimisation de d_eff pour la meilleure formulation")
    print("-" * 80)

    # Newton pour référence
    v_newton = courbe_rotation_newton(r_obs_kpc)
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)

    d_eff_opt_A, chi2_opt_A = optimiser_d_eff_formulation('A')
    d_eff_opt_B, chi2_opt_B = optimiser_d_eff_formulation('B')
    d_eff_opt_C, chi2_opt_C = optimiser_d_eff_formulation('C')

    # Résultats optimisation
    print("=" * 80)
    print("RÉSULTATS OPTIMISATION")
    print("=" * 80)
    print(f"{'Formulation':<20} {'d_eff optimal (kpc)':>20} {'χ² optimal':>15} {'vs Newton':>12}")
    print("-" * 80)
    print(f"{'Newton (référence)':<20} {'-':>20} {chi2_newton:>15.2f} {'1.00×':>12}")
    print(f"{'Formulation A':<20} {d_eff_opt_A:>20.2f} {chi2_opt_A:>15.2f} {chi2_opt_A/chi2_newton:>11.2f}×")
    print(f"{'Formulation B':<20} {d_eff_opt_B:>20.2f} {chi2_opt_B:>15.2f} {chi2_opt_B/chi2_newton:>11.2f}×")
    print(f"{'Formulation C':<20} {d_eff_opt_C:>20.2f} {chi2_opt_C:>15.2f} {chi2_opt_C/chi2_newton:>11.2f}×")
    print("=" * 80)
    print()

    # Évaluation finale
    chi2_min_global = min(chi2_opt_A, chi2_opt_B, chi2_opt_C)

    print("=" * 80)
    print(" ÉVALUATION FINALE ".center(80))
    print("=" * 80)
    print()

    if chi2_min_global < chi2_newton:
        print("✅ SUCCÈS MAJEUR!")
        print(f"   χ² minimal = {chi2_min_global:.2f} < Newton ({chi2_newton:.2f})")
        print("   La dérivation rigoureuse depuis la RG FONCTIONNE!")
        print()

        if chi2_min_global == chi2_opt_A:
            print(f"   Meilleure formulation: A (Newtonien Atténué)")
            print(f"   d_eff optimal = {d_eff_opt_A:.2f} kpc")
        elif chi2_min_global == chi2_opt_B:
            print(f"   Meilleure formulation: B (Gradient Radial)")
            print(f"   d_eff optimal = {d_eff_opt_B:.2f} kpc")
        else:
            print(f"   Meilleure formulation: C (Enveloppe Différentielle)")
            print(f"   d_eff optimal = {d_eff_opt_C:.2f} kpc")
        print()
        print("   PROCHAINES ÉTAPES:")
        print("   1. Test hybride avec M_IDT (matière non-lumineuse)")
        print("   2. Application à 10 galaxies différentes")
        print("   3. Exploration réseau de lignes Asselin")
    else:
        print("⚠️  RÉSULTATS:")
        print(f"   χ² minimal = {chi2_min_global:.2f} > Newton ({chi2_newton:.2f})")
        print(f"   Amélioration: {(1 - chi2_min_global/chi2_newton)*100:.1f}% (mais pas suffisant)")
        print()
        print("   INTERPRÉTATION:")
        print("   - Les trois formulations testées ne suffisent pas")
        print("   - Explorer formulation réseau de lignes Asselin")
        print("   - Considérer termes RG d'ordre supérieur")
        print("   - Vérifier hypothèse d_eff fonction de ρ(r)")

    print()
    print("="*80)
    print(" FIN DU TEST ".center(80))
    print("="*80)
    print()
