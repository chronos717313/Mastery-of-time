#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALYSE: Dépendance Environnementale vs Liaison Asselin

Test: Le problème vient-il du réseau Asselin (Maxwell) ou de l'alignement?

Pour chaque galaxie:
1. Newton (baseline)
2. Alignement SEUL (β optimisé, SANS Maxwell)
3. Alignement + Maxwell (théorie complète)
"""

import numpy as np
import math
from scipy.optimize import minimize_scalar

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

# Voie Lactée (de test_maximisation_amelioration.py)
VL_r_obs = np.array([0.5, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 120, 140])
VL_v_obs = np.array([45, 100, 150, 175, 190, 200, 205, 210, 215, 218, 220, 221, 220, 218, 215, 210, 208, 205, 203, 201, 200, 198, 195])
VL_sigma = np.array([10.0] * len(VL_v_obs))
VL_M_bulbe = 1.5e10 * M_soleil
VL_a_bulbe = 0.7
VL_M_disque = 6.0e10 * M_soleil
VL_R_d = 2.5
VL_M_gaz = 5.0e9 * M_soleil
VL_R_gaz = 7.0

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

# M33
M33_r_obs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20])
M33_v_obs = np.array([50, 75, 90, 100, 105, 110, 115, 120, 122, 125, 125, 124, 123, 122, 120, 118, 115, 110])
M33_sigma = np.array([8.0] * len(M33_v_obs))
M33_M_bulbe = 5.0e9 * M_soleil
M33_a_bulbe = 0.5
M33_M_disque = 3.0e10 * M_soleil
M33_R_d = 2.0
M33_M_gaz = 5.0e9 * M_soleil
M33_R_gaz = 5.0

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

def masse_bulbe_spherique(r_kpc, M_bulbe, a_bulbe):
    """Bulbe sphérique (Hernquist)"""
    return M_bulbe * r_kpc**2 / (r_kpc + a_bulbe)**2

def masse_disque(r_kpc, M_disque, R_d):
    """Disque exponentiel"""
    return M_disque * (1.0 - np.exp(-r_kpc/R_d) * (1.0 + r_kpc/R_d))

def masse_gaz(r_kpc, M_gaz, R_gaz):
    """Gaz"""
    return M_gaz * (1.0 - np.exp(-r_kpc/R_gaz) * (1.0 + r_kpc/R_gaz))

def masse_visible_totale(r_kpc, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz):
    """Masse visible totale"""
    return (masse_bulbe_spherique(r_kpc, M_bulbe, a_bulbe) +
            masse_disque(r_kpc, M_disque, R_d) +
            masse_gaz(r_kpc, M_gaz, R_gaz))

def masse_bulbe_aligne(r_kpc, theta, beta, M_bulbe, a_bulbe):
    """Bulbe aligné (anisotrope)"""
    M_sph = masse_bulbe_spherique(r_kpc, M_bulbe, a_bulbe)
    return M_sph * (1.0 + beta * math.cos(theta)**2)

# ============================================================================
# VITESSES
# ============================================================================

def vitesse_newton(r_kpc, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz):
    """Vitesse newtonienne (masse visible sphérique)"""
    M_vis = masse_visible_totale(r_kpc, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz)
    r_m = r_kpc * kpc_to_m
    v2 = G * M_vis / r_m
    if v2 > 0:
        return math.sqrt(v2) / 1000.0  # km/s
    return 0.0

def vitesse_alignement_seul(r_kpc, beta, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz):
    """
    Vitesse avec alignement SEUL (pas de Maxwell/Asselin)

    Hypothèse simplifiée: alignement moyen θ ≈ 45° (cos²(45°) = 0.5)
    """
    theta = math.pi / 4.0  # 45 degrés
    M_bulbe_align = masse_bulbe_aligne(r_kpc, theta, beta, M_bulbe, a_bulbe)
    M_disque_val = masse_disque(r_kpc, M_disque, R_d)
    M_gaz_val = masse_gaz(r_kpc, M_gaz, R_gaz)
    M_total = M_bulbe_align + M_disque_val + M_gaz_val

    r_m = r_kpc * kpc_to_m
    v2 = G * M_total / r_m
    if v2 > 0:
        return math.sqrt(v2) / 1000.0  # km/s
    return 0.0

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi2_newton(r_obs, v_obs, sigma, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz):
    """Chi² Newton"""
    chi2 = 0.0
    for r, v_o, sig in zip(r_obs, v_obs, sigma):
        v_t = vitesse_newton(r, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz)
        chi2 += ((v_o - v_t) / sig)**2
    return chi2

def chi2_alignement(r_obs, v_obs, sigma, beta, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz):
    """Chi² alignement seul"""
    chi2 = 0.0
    for r, v_o, sig in zip(r_obs, v_obs, sigma):
        v_t = vitesse_alignement_seul(r, beta, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz)
        chi2 += ((v_o - v_t) / sig)**2
    return chi2

# ============================================================================
# TESTS PAR GALAXIE
# ============================================================================

def tester_galaxie(nom, r_obs, v_obs, sigma, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz,
                   chi2_complet_connu=None):
    """
    Test complet d'une galaxie

    chi2_complet_connu: χ² avec alignement + Maxwell (des tests précédents)
    """
    print(f"\n{'='*80}")
    print(f"  {nom}")
    print(f"{'='*80}")

    # Newton
    chi2_n = chi2_newton(r_obs, v_obs, sigma, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz)
    print(f"χ² Newton:                {chi2_n:>12.2f}  (1.000×)")

    # Alignement seul (optimisation β)
    def objectif_align(beta):
        return chi2_alignement(r_obs, v_obs, sigma, beta, M_bulbe, a_bulbe, M_disque, R_d, M_gaz, R_gaz)

    result = minimize_scalar(objectif_align, bounds=(0.0, 5.0), method='bounded')
    beta_opt_align = result.x
    chi2_align = result.fun

    ratio_align = chi2_align / chi2_n
    print(f"χ² Alignement seul (β={beta_opt_align:.2f}): {chi2_align:>12.2f}  ({ratio_align:.3f}×)")

    # Complet (si connu)
    if chi2_complet_connu is not None:
        ratio_complet = chi2_complet_connu / chi2_n
        print(f"χ² Alignement + Maxwell:     {chi2_complet_connu:>12.2f}  ({ratio_complet:.3f}×)")

        # Analyse
        print()
        if chi2_align < chi2_n and chi2_complet_connu < chi2_n:
            print("✅ Alignement seul: SUCCÈS")
            print("✅ Alignement + Maxwell: SUCCÈS")
            if chi2_complet_connu < chi2_align:
                print("   → Maxwell AMÉLIORE l'alignement")
            else:
                print("   → Maxwell DÉGRADE légèrement")

        elif chi2_align < chi2_n and chi2_complet_connu > chi2_n:
            print("✅ Alignement seul: SUCCÈS")
            print("❌ Alignement + Maxwell: ÉCHEC")
            print("🚨 → Le réseau Asselin/Maxwell DÉTRUIT le succès!")

        elif chi2_align > chi2_n and chi2_complet_connu > chi2_n:
            print("❌ Alignement seul: ÉCHEC")
            print("❌ Alignement + Maxwell: ÉCHEC")
            print("   → Problème pas lié au réseau Asselin")

        else:
            print("❌ Alignement seul: ÉCHEC")
            print("✅ Alignement + Maxwell: SUCCÈS")
            print("   → Le réseau Asselin CORRIGE l'alignement!")

    return chi2_n, chi2_align, beta_opt_align

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("    ANALYSE: DÉPENDANCE ENVIRONNEMENTALE vs LIAISON ASSELIN")
    print("="*80)
    print()
    print("QUESTION: Le problème vient-il du réseau Asselin (Maxwell)?")
    print()
    print("TEST: Pour chaque galaxie")
    print("  1. Newton (baseline)")
    print("  2. Alignement SEUL (sans Maxwell)")
    print("  3. Alignement + Maxwell (théorie complète)")
    print()

    # Résultats connus (alignement + Maxwell)
    # De test_maximisation_amelioration.py et tests validation
    chi2_complet = {
        'Voie Lactée': 2563.35,
        'M31': 348957.59,
        'M33': 84812.34,
        'NGC 3198': 249.30,
    }

    # Tests
    resultats = {}

    resultats['VL'] = tester_galaxie(
        'VOIE LACTÉE', VL_r_obs, VL_v_obs, VL_sigma,
        VL_M_bulbe, VL_a_bulbe, VL_M_disque, VL_R_d, VL_M_gaz, VL_R_gaz,
        chi2_complet['Voie Lactée']
    )

    resultats['M31'] = tester_galaxie(
        'M31 (ANDROMÈDE)', M31_r_obs, M31_v_obs, M31_sigma,
        M31_M_bulbe, M31_a_bulbe, M31_M_disque, M31_R_d, M31_M_gaz, M31_R_gaz,
        chi2_complet['M31']
    )

    resultats['M33'] = tester_galaxie(
        'M33 (TRIANGLE)', M33_r_obs, M33_v_obs, M33_sigma,
        M33_M_bulbe, M33_a_bulbe, M33_M_disque, M33_R_d, M33_M_gaz, M33_R_gaz,
        chi2_complet['M33']
    )

    resultats['NGC'] = tester_galaxie(
        'NGC 3198 (ISOLÉE)', NGC_r_obs, NGC_v_obs, NGC_sigma,
        NGC_M_bulbe, NGC_a_bulbe, NGC_M_disque, NGC_R_d, NGC_M_gaz, NGC_R_gaz,
        chi2_complet['NGC 3198']
    )

    # Tableau récapitulatif
    print("\n" + "="*80)
    print("                      TABLEAU RÉCAPITULATIF")
    print("="*80)
    print(f"{'Galaxie':<15} {'Newton':>10} {'Align seul':>12} {'Align+Maxwell':>15} {'Verdict':<20}")
    print("-"*80)

    galaxies = [
        ('Voie Lactée', resultats['VL'], chi2_complet['Voie Lactée']),
        ('M31', resultats['M31'], chi2_complet['M31']),
        ('M33', resultats['M33'], chi2_complet['M33']),
        ('NGC 3198', resultats['NGC'], chi2_complet['NGC 3198']),
    ]

    for nom, (chi2_n, chi2_a, beta), chi2_c in galaxies:
        ratio_a = chi2_a / chi2_n
        ratio_c = chi2_c / chi2_n

        if chi2_a < chi2_n and chi2_c > chi2_n:
            verdict = "Maxwell DÉTRUIT ❌"
        elif chi2_a < chi2_n and chi2_c < chi2_n:
            verdict = "Tous OK ✅"
        elif chi2_a > chi2_n and chi2_c > chi2_n:
            verdict = "Tous ÉCHEC ❌"
        else:
            verdict = "Maxwell SAUVE ✅"

        print(f"{nom:<15} {chi2_n:>10.0f} {chi2_a:>12.0f} {chi2_c:>15.0f} {verdict:<20}")

    # Conclusion
    print("\n" + "="*80)
    print("                           CONCLUSION")
    print("="*80)
    print()

    # Compter les cas
    maxwell_detruit = 0
    maxwell_ok = 0
    align_marche = 0

    for nom, (chi2_n, chi2_a, beta), chi2_c in galaxies:
        if chi2_a < chi2_n:
            align_marche += 1
            if chi2_c > chi2_n:
                maxwell_detruit += 1
            else:
                maxwell_ok += 1

    print(f"Alignement seul fonctionne: {align_marche}/4 galaxies")
    print(f"Maxwell préserve succès:    {maxwell_ok}/{align_marche} cas")
    print(f"Maxwell détruit succès:     {maxwell_detruit}/{align_marche} cas")
    print()

    if maxwell_detruit > 0:
        print("🚨 DIAGNOSTIC:")
        print("   Le RÉSEAU ASSELIN/MAXWELL cause les échecs catastrophiques!")
        print("   L'alignement seul fonctionne, mais Maxwell le détruit.")
        print()
        print("   → La formulation Maxwell est INCORRECTE")
        print("   → Intensités réseau trop élevées pour certaines galaxies")
        print("   → Besoin révision complète du modèle Maxwell")
    elif align_marche == 4:
        print("✅ L'ALIGNEMENT fonctionne pour TOUTES les galaxies!")
        print("✅ Le réseau Maxwell préserve ou améliore le succès")
        print()
        print("   → Théorie validée!")
    else:
        print("⚠️ Problème mixte:")
        print("   L'alignement seul ne fonctionne pas partout")
        print("   → Problème plus profond que juste le réseau")

    print()
    print("="*80)

if __name__ == "__main__":
    main()
