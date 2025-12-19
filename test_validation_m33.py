#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDATION: M33 (Triangle)

Prédiction: Succès MODÉRÉ
Groupe Local mais masse plus faible
β attendu ≈ 2.0-3.0
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
# DONNÉES OBSERVATIONNELLES M33
# Source: Corbelli & Salucci (2000), Gratier et al. (2017)
# ============================================================================
r_obs_kpc = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20
])

v_obs_kms = np.array([
    50, 75, 90, 100, 105, 110, 115, 120, 122, 125,
    125, 124, 123, 122, 120, 118, 115, 110
])

sigma_obs_kms = np.array([8.0] * len(v_obs_kms))

# ============================================================================
# MASSE VISIBLE M33
# ============================================================================
M_bulbe_M33 = 5.0e9 * M_soleil  # kg
a_bulbe_M33 = 0.5  # kpc

M_disque_M33 = 3.0e10 * M_soleil  # kg
R_d_M33 = 2.0  # kpc

M_gaz_M33 = 5.0e9 * M_soleil  # kg
R_gaz_M33 = 5.0  # kpc

def masse_bulbe_spherique_m33(r_kpc):
    """Bulbe sphérique M33 (Hernquist)"""
    M = M_bulbe_M33
    a = a_bulbe_M33
    return M * r_kpc**2 / (r_kpc + a)**2

def masse_disque_m33(r_kpc):
    """Disque exponentiel M33"""
    M = M_disque_M33
    R_d = R_d_M33
    return M * (1.0 - np.exp(-r_kpc/R_d) * (1.0 + r_kpc/R_d))

def masse_gaz_m33(r_kpc):
    """Gaz M33"""
    M = M_gaz_M33
    R_g = R_gaz_M33
    return M * (1.0 - np.exp(-r_kpc/R_g) * (1.0 + r_kpc/R_g))

def masse_visible_m33(r_kpc):
    """Masse visible totale M33"""
    return (masse_bulbe_spherique_m33(r_kpc) +
            masse_disque_m33(r_kpc) +
            masse_gaz_m33(r_kpc))

# ============================================================================
# RÉSEAU ASSELIN M33
# ============================================================================

class LigneAsselin:
    def __init__(self, i, j, M_i, M_j, r_i, r_j, d_eff_kpc):
        self.i = i
        self.j = j
        self.M_i = M_i  # kg
        self.M_j = M_j  # kg
        self.r_i = r_i  # kpc (vecteur 3D)
        self.r_j = r_j  # kpc
        self.d_eff_kpc = d_eff_kpc

        # Distance entre galaxies
        self.d_ij_kpc = np.linalg.norm(r_j - r_i)

        # Intensité liaison
        self.intensite = (math.sqrt(M_i * M_j) / (self.d_ij_kpc**2 * M_soleil)) * \
                        math.exp(-self.d_ij_kpc / d_eff_kpc)

        # Point milieu et vecteur direction
        self.r_centre = 0.5 * (r_i + r_j)
        self.direction = (r_j - r_i) / self.d_ij_kpc

        # Masse effective ligne
        self.M_ligne = math.sqrt(M_i * M_j)

# GALAXIES DU RÉSEAU M33 (référentiel centré sur M33)
GALAXIES_M33 = [
    {'nom': 'M33 (centre)', 'M': 4.0e10 * M_soleil,
     'position': np.array([0.0, 0.0, 0.0])},

    {'nom': 'M31', 'M': 1.5e12 * M_soleil,
     'position': np.array([-90.0, 130.0, 150.0])},

    {'nom': 'Voie Lactée', 'M': 8.0e10 * M_soleil,
     'position': np.array([-840.0, -120.0, 50.0])},

    {'nom': 'LMC', 'M': 1.0e10 * M_soleil,
     'position': np.array([-800.0, -90.0, 30.0])},

    {'nom': 'IC 10', 'M': 6.0e9 * M_soleil,
     'position': np.array([250.0, -100.0, -80.0])},
]

# Superamas (positions relatives à M33)
# Centre Laniakea est à ~840 kpc de M33 (direction Voie Lactée)
SUPERAMAS_M33 = [
    {'nom': 'Centre Laniakea', 'M': 1.0e17 * M_soleil,
     'position': np.array([840.0, 120.0, -50.0])},

    {'nom': 'Grand Attracteur', 'M': 5.0e16 * M_soleil,
     'position': np.array([65840.0, 120.0, -50.0])},
]

def creer_reseau_m33():
    """Réseau Asselin pour M33"""
    lignes = []

    # Échelle galactique (un peu plus petit, masse plus faible)
    d_eff_gal = 400.0  # kpc

    for i, gal_i in enumerate(GALAXIES_M33):
        for j, gal_j in enumerate(GALAXIES_M33):
            if i < j:
                ligne = LigneAsselin(
                    i, j,
                    gal_i['M'], gal_j['M'],
                    gal_i['position'], gal_j['position'],
                    d_eff_gal
                )
                lignes.append(ligne)

    # Superamas
    d_eff_super = 50000.0  # kpc

    for gal in GALAXIES_M33:
        for sup in SUPERAMAS_M33:
            ligne = LigneAsselin(
                -1, -1,
                gal['M'], sup['M'],
                gal['position'], sup['position'],
                d_eff_super
            )
            lignes.append(ligne)

    # Tri par intensité
    lignes.sort(key=lambda x: x.intensite, reverse=True)

    print(f"Réseau M33: {len(lignes)} lignes Asselin")
    print(f"  Intensité max: {lignes[0].intensite:.2e}")
    print(f"  Intensité min: {lignes[-1].intensite:.2e}")

    return lignes

# ============================================================================
# ALIGNEMENT BULBE
# ============================================================================

def direction_dominante_asselin(r_vec_kpc, lignes):
    """Direction dominante du réseau Asselin en un point"""
    if len(lignes) == 0:
        return np.array([1.0, 0.0, 0.0])

    direction_totale = np.zeros(3)
    intensite_totale = 0.0

    for ligne in lignes:
        # Distance au centre de la ligne
        d_centre = np.linalg.norm(r_vec_kpc - ligne.r_centre)

        # Poids décroissant avec distance
        poids = ligne.intensite * np.exp(-d_centre / ligne.d_eff_kpc)

        # Direction pondérée
        direction_totale += poids * ligne.direction
        intensite_totale += poids

    if intensite_totale > 0:
        direction_totale /= intensite_totale

    # Normaliser
    norme = np.linalg.norm(direction_totale)
    if norme > 0:
        return direction_totale / norme
    else:
        return np.array([1.0, 0.0, 0.0])

def masse_bulbe_aligne_m33(r_kpc, theta_align, beta):
    """Bulbe aligné avec réseau Asselin"""
    M_sph = masse_bulbe_spherique_m33(r_kpc)
    facteur_anisotropie = 1.0 + beta * math.cos(theta_align)**2
    return M_sph * facteur_anisotropie

def masse_visible_complete_m33(r_kpc, lignes, beta):
    """Masse visible avec alignement bulbe"""
    r_vec = np.array([r_kpc, 0.0, 0.0])

    # Direction dominante Asselin
    dir_asselin = direction_dominante_asselin(r_vec, lignes)

    # Angle alignement
    dir_radiale = r_vec / np.linalg.norm(r_vec)
    cos_theta = np.dot(dir_radiale, dir_asselin)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    theta_align = math.acos(abs(cos_theta))

    # Masse bulbe aligné
    M_bulbe = masse_bulbe_aligne_m33(r_kpc, theta_align, beta)
    M_disque = masse_disque_m33(r_kpc)
    M_gaz = masse_gaz_m33(r_kpc)

    return M_bulbe + M_disque + M_gaz

# ============================================================================
# FORMULATION MAXWELL
# ============================================================================

def gamma_despres_ligne_maxwell(r_kpc, ligne):
    """γ d'une ligne Asselin (intégration 10 points)"""
    r_eval = np.array([r_kpc, 0.0, 0.0])

    # Intégration ligne (10 points)
    n_pts = 10
    gamma_total = 0.0

    for k in range(n_pts):
        s = (k + 0.5) / n_pts
        r_ligne = ligne.r_i + s * (ligne.r_j - ligne.r_i)

        # Distance
        dr = r_eval - r_ligne
        distance_kpc = np.linalg.norm(dr)

        if distance_kpc < 0.1:
            distance_kpc = 0.1

        # Contribution point
        M_segment_kg = ligne.M_ligne / n_pts
        distance_m = distance_kpc * kpc_to_m

        gamma_total += -G * M_segment_kg / (c**2 * distance_m)

    return gamma_total

def gamma_despres_total_complet(r_kpc, lignes, beta):
    """γ total avec alignement + Maxwell"""
    r_m = r_kpc * kpc_to_m

    # Masse visible complète (avec alignement)
    M_vis_kg = masse_visible_complete_m33(r_kpc, lignes, beta)

    # γ visible
    gamma_vis = -G * M_vis_kg / (c**2 * r_m)

    # γ Maxwell (réseau)
    gamma_maxwell = sum(gamma_despres_ligne_maxwell(r_kpc, ligne)
                       for ligne in lignes)

    return gamma_vis + gamma_maxwell

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_orbitale_theorie(r_kpc, lignes, beta):
    """Vitesse orbitale v(r) = sqrt(r·c²|dγ/dr|)"""
    if r_kpc < 0.5:
        r_kpc = 0.5

    dr = 0.01  # kpc

    gamma_plus = gamma_despres_total_complet(r_kpc + dr, lignes, beta)
    gamma_moins = gamma_despres_total_complet(r_kpc - dr, lignes, beta)

    dgamma_dr = (gamma_plus - gamma_moins) / (2.0 * dr)
    dgamma_dr_par_m = dgamma_dr / kpc_to_m

    v2 = r_kpc * kpc_to_m * c**2 * abs(dgamma_dr_par_m)

    if v2 > 0:
        return math.sqrt(v2) / 1000.0  # km/s
    else:
        return 0.0

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(r_obs, v_obs, sigma_obs, lignes, beta):
    """Chi-carré entre théorie et observations"""
    chi2 = 0.0

    for r, v_o, sig in zip(r_obs, v_obs, sigma_obs):
        v_t = vitesse_orbitale_theorie(r, lignes, beta)
        chi2 += ((v_o - v_t) / sig)**2

    return chi2

# ============================================================================
# TESTS
# ============================================================================

def test_newton_m33():
    """Test Newton (masse visible seule, sphérique)"""
    print("\n" + "="*80)
    print("TEST 1: NEWTON (masse visible sphérique)")
    print("="*80)

    chi2 = 0.0

    for r, v_o, sig in zip(r_obs_kpc, v_obs_kms, sigma_obs_kms):
        # Masse visible sphérique
        M_vis = masse_visible_m33(r)
        r_m = r * kpc_to_m

        # Vitesse newtonienne
        v_newton = math.sqrt(G * M_vis / r_m) / 1000.0  # km/s

        chi2 += ((v_o - v_newton) / sig)**2

    print(f"χ² = {chi2:.2f}")

    return chi2

def test_combinaison_m33():
    """Test combinaison complète (alignement + Maxwell)"""
    print("\n" + "="*80)
    print("TEST 2: COMBINAISON COMPLÈTE (β=3.0)")
    print("="*80)

    # Créer réseau
    lignes = creer_reseau_m33()
    print()

    # Test avec β=3.0 (optimisé Voie Lactée)
    beta = 3.0
    chi2 = chi_carre(r_obs_kpc, v_obs_kms, sigma_obs_kms, lignes, beta)

    print(f"β = {beta}")
    print(f"χ² = {chi2:.2f}")

    return chi2, lignes

def test_optimisation_beta_m33():
    """Optimisation β pour M33"""
    print("\n" + "="*80)
    print("TEST 3: OPTIMISATION β")
    print("="*80)

    # Réseau
    lignes = creer_reseau_m33()
    print("\nOptimisation en cours...\n")

    # Fonction objectif
    def objectif(beta):
        return chi_carre(r_obs_kpc, v_obs_kms, sigma_obs_kms, lignes, beta)

    # Optimisation
    result = minimize_scalar(objectif, bounds=(0.0, 5.0), method='bounded')

    beta_opt = result.x
    chi2_opt = result.fun

    print(f"  β optimal = {beta_opt:.3f}")
    print(f"  χ² optimal = {chi2_opt:.2f}")

    return beta_opt, chi2_opt, lignes

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("                VALIDATION: M33 (TRIANGLE)                ")
    print("="*80)
    print()
    print("PRÉDICTION: Succès MODÉRÉ (Groupe Local, masse plus faible)")
    print("  → χ² < Newton attendu")
    print("  → β ≈ 2.0-3.0")
    print()

    # Tests
    chi2_newton = test_newton_m33()

    chi2_comb, lignes = test_combinaison_m33()

    beta_opt, chi2_opt, lignes = test_optimisation_beta_m33()

    # Résumé
    print("\n" + "="*80)
    print("                        RÉSULTATS M33                       ")
    print("="*80)
    print(f"{'Modèle':<40} {'χ²':>12} {'vs Newton':>12}")
    print("-"*80)
    print(f"{'Newton (référence)':<40} {chi2_newton:>12.2f} {'1.000×':>12}")
    print(f"{'Voie Lactée - Optimisé (β=3.0)':<40} {'2563':>12} {'0.821×':>12}")
    print(f"{'NGC 3198 - Optimisé (β=4.0)':<40} {'249':>12} {'0.626×':>12}")
    print(f"{'M33 - Combinaison (β=3.0)':<40} {chi2_comb:>12.2f} {f'{chi2_comb/chi2_newton:.3f}×':>12}")
    print(f"{'M33 - OPTIMISÉ (β={beta_opt:.2f})':<40} {chi2_opt:>12.2f} {f'{chi2_opt/chi2_newton:.3f}×':>12}")
    print("="*80)

    amelioration_pct = (1.0 - chi2_opt/chi2_newton) * 100.0

    print()
    print(f"Amélioration M33: {amelioration_pct:.1f}%")
    print(f"β optimal M33: {beta_opt:.2f}")
    print()

    return chi2_newton, chi2_opt, beta_opt

if __name__ == "__main__":
    main()
