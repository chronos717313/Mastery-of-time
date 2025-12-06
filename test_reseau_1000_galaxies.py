#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réseau Asselin à Grande Échelle : 1000 Galaxies
================================================

Date: 2025-12-05
Branche: claude/temporal-distortion-calculation-01P4ffpawn6QMj7vVq6PSVcS

OBJECTIF:
Tester la théorie avec un réseau réaliste de 1000 galaxies

STRUCTURE:
- Distribution spatiale réaliste (filaments cosmiques)
- Distribution de masses réaliste (fonction de masse galactique)
- ~500,000 lignes Asselin potentielles
- Optimisation: seuil sur intensité pour ne garder que lignes significatives

STRATÉGIE COMPUTATIONNELLE:
- Seuil d'intensité: L_min = 1e-6 (unités normalisées)
- Cutoff spatial: d_max = 10 Mpc (au-delà, lignes négligeables)
- Calcul parallélisable (si besoin)
"""

import math
import numpy as np
from scipy.optimize import minimize
import time

# ============================================================================
# CONSTANTES
# ============================================================================

G = 6.674e-11
c = 299792458
M_soleil = 1.989e30
kpc_to_m = 3.086e19
Mpc_to_kpc = 1000.0

# ============================================================================
# DONNÉES OBSERVATIONNELLES
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
# GÉNÉRATION DE 1000 GALAXIES
# ============================================================================

def fonction_masse_schechter(M, M_star=1e11*M_soleil, alpha=-1.25, phi_star=0.01):
    """
    Fonction de masse de Schechter (distribution réaliste)

    Φ(M) ∝ (M/M*)^α · exp(-M/M*)

    Args:
        M: Masse galactique
        M_star: Masse caractéristique (~10¹¹ M☉)
        alpha: Pente faible masse (~-1.25)
        phi_star: Normalisation

    Returns:
        Probabilité (non normalisée)
    """
    x = M / M_star
    return phi_star * x**alpha * np.exp(-x)

def generer_masse_galaxie():
    """Génère masse galactique selon Schechter"""
    # Intervalle: 10⁹ - 10¹³ M☉
    log_M_min = 9.0
    log_M_max = 13.0

    # Échantillonnage par rejet
    while True:
        log_M = np.random.uniform(log_M_min, log_M_max)
        M = 10**log_M * M_soleil

        prob = fonction_masse_schechter(M)
        prob_max = fonction_masse_schechter(1e11 * M_soleil)  # Maximum near M*

        if np.random.uniform(0, prob_max) < prob:
            return M

def generer_position_filament(n_galaxies=1000, longueur_filament_Mpc=20.0,
                               largeur_filament_Mpc=2.0):
    """
    Génère positions galactiques le long de filaments cosmiques

    Structure:
    - 5 filaments principaux radiaux depuis Voie Lactée
    - Dispersion gaussienne autour des filaments
    - Concentration plus forte près du centre

    Args:
        n_galaxies: Nombre de galaxies à générer
        longueur_filament_Mpc: Longueur typique filament
        largeur_filament_Mpc: Largeur typique filament

    Returns:
        Liste de positions (kpc)
    """
    positions = []

    # Voie Lactée au centre
    positions.append(np.array([0.0, 0.0, 0.0]))

    # 5 filaments principaux
    n_filaments = 5
    directions_filaments = [
        np.array([1.0, 0.0, 0.0]),  # X+
        np.array([0.3, 0.9, 0.2]),  # Oblique 1
        np.array([-0.5, 0.7, -0.3]), # Oblique 2
        np.array([0.2, -0.6, 0.8]),  # Oblique 3
        np.array([-0.7, -0.3, -0.5]) # Oblique 4
    ]

    # Normaliser directions
    directions_filaments = [d/np.linalg.norm(d) for d in directions_filaments]

    # Distribuer galaxies sur filaments
    galaxies_par_filament = (n_galaxies - 1) // n_filaments

    for i, direction in enumerate(directions_filaments):
        for j in range(galaxies_par_filament):
            # Distance le long du filament (décroissance exponentielle)
            r_Mpc = np.random.exponential(longueur_filament_Mpc / 3.0)
            r_Mpc = min(r_Mpc, longueur_filament_Mpc)

            # Position le long du filament
            pos_filament = r_Mpc * Mpc_to_kpc * direction

            # Dispersion perpendiculaire (gaussienne)
            perpendiculaire1 = np.cross(direction, np.array([0, 0, 1]))
            if np.linalg.norm(perpendiculaire1) < 0.1:
                perpendiculaire1 = np.cross(direction, np.array([0, 1, 0]))
            perpendiculaire1 = perpendiculaire1 / np.linalg.norm(perpendiculaire1)

            perpendiculaire2 = np.cross(direction, perpendiculaire1)
            perpendiculaire2 = perpendiculaire2 / np.linalg.norm(perpendiculaire2)

            dispersion_Mpc = np.random.normal(0, largeur_filament_Mpc)
            dispersion1 = dispersion_Mpc * Mpc_to_kpc * perpendiculaire1

            dispersion_Mpc = np.random.normal(0, largeur_filament_Mpc)
            dispersion2 = dispersion_Mpc * Mpc_to_kpc * perpendiculaire2

            position = pos_filament + dispersion1 + dispersion2
            positions.append(position)

    # Remplir avec galaxies restantes (distribution sphérique)
    n_restantes = n_galaxies - len(positions)
    for i in range(n_restantes):
        # Rayon avec décroissance exponentielle
        r_Mpc = np.random.exponential(longueur_filament_Mpc / 2.0)
        r_kpc = r_Mpc * Mpc_to_kpc

        # Direction aléatoire
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2*np.pi)

        x = r_kpc * np.sin(theta) * np.cos(phi)
        y = r_kpc * np.sin(theta) * np.sin(phi)
        z = r_kpc * np.cos(theta)

        positions.append(np.array([x, y, z]))

    return positions

def generer_catalogue_1000_galaxies():
    """
    Génère catalogue complet de 1000 galaxies

    Returns:
        Liste de dictionnaires avec nom, masse, position
    """
    print("Génération catalogue 1000 galaxies...")

    galaxies = []

    # Positions
    positions = generer_position_filament(n_galaxies=1000)

    # Masses et noms
    for i, pos in enumerate(positions):
        if i == 0:
            # Voie Lactée
            nom = "Voie Lactée"
            masse = 8.0e10 * M_soleil
        else:
            nom = f"Gal_{i:04d}"
            masse = generer_masse_galaxie()

        galaxies.append({
            'nom': nom,
            'M': masse,
            'position': pos
        })

    # Statistiques
    masses = np.array([g['M']/M_soleil for g in galaxies])
    distances = np.array([np.linalg.norm(g['position']) for g in galaxies[1:]])

    print(f"  ✓ {len(galaxies)} galaxies générées")
    print(f"  Masses: {np.min(masses):.2e} - {np.max(masses):.2e} M☉")
    print(f"  Masse médiane: {np.median(masses):.2e} M☉")
    print(f"  Distances: 0 - {np.max(distances):.0f} kpc ({np.max(distances)/1000:.1f} Mpc)")
    print(f"  Distance médiane: {np.median(distances):.0f} kpc")
    print()

    return galaxies

# ============================================================================
# RÉSEAU ASSELIN OPTIMISÉ
# ============================================================================

class LigneAsselinOptimisee:
    """Ligne Asselin entre deux galaxies (version optimisée)"""

    def __init__(self, gal_i, gal_j, d_eff_kpc=1000.0):
        self.r_i = gal_i['position']
        self.r_j = gal_j['position']
        self.d_ij = np.linalg.norm(self.r_j - self.r_i)

        M_i = gal_i['M']
        M_j = gal_j['M']

        # Intensité Asselin
        self.intensite = math.sqrt(M_i * M_j / M_soleil**2) / self.d_ij**2 * math.exp(-self.d_ij / d_eff_kpc)

    def point_sur_ligne(self, s):
        return self.r_i + s * (self.r_j - self.r_i)

def creer_reseau_asselin_optimise(galaxies, d_eff_kpc=1000.0,
                                   intensite_min=1e-6, d_max_kpc=10000.0):
    """
    Crée réseau Asselin avec optimisations

    Optimisations:
    - Seuil intensité minimale (élimine lignes négligeables)
    - Cutoff distance maximale (limite portée)
    - Affichage progression

    Args:
        galaxies: Liste de galaxies
        d_eff_kpc: Distance effective
        intensite_min: Seuil intensité minimum
        d_max_kpc: Distance maximum entre galaxies

    Returns:
        Liste de lignes Asselin significatives
    """
    print(f"Création réseau Asselin optimisé...")
    print(f"  Paramètres:")
    print(f"    d_eff = {d_eff_kpc:.0f} kpc")
    print(f"    Intensité min = {intensite_min:.2e}")
    print(f"    Distance max = {d_max_kpc:.0f} kpc ({d_max_kpc/1000:.1f} Mpc)")
    print()

    N = len(galaxies)
    lignes = []
    n_total = N * (N - 1) // 2
    n_eliminées_distance = 0
    n_eliminées_intensite = 0

    print(f"  Test de {n_total:,} paires possibles...")

    start_time = time.time()

    for i in range(N):
        if i % 100 == 0 and i > 0:
            elapsed = time.time() - start_time
            progress = i / N * 100
            print(f"    Progress: {progress:.1f}% ({i}/{N} galaxies, {len(lignes):,} lignes, {elapsed:.1f}s)")

        for j in range(i+1, N):
            # Vérifier distance
            d_ij = np.linalg.norm(galaxies[j]['position'] - galaxies[i]['position'])

            if d_ij > d_max_kpc:
                n_eliminées_distance += 1
                continue

            # Créer ligne temporaire pour calculer intensité
            M_i = galaxies[i]['M']
            M_j = galaxies[j]['M']
            intensite = math.sqrt(M_i * M_j / M_soleil**2) / d_ij**2 * math.exp(-d_ij / d_eff_kpc)

            if intensite < intensite_min:
                n_eliminées_intensite += 1
                continue

            # Ligne significative - créer et ajouter
            ligne = LigneAsselinOptimisee(galaxies[i], galaxies[j], d_eff_kpc)
            lignes.append(ligne)

    elapsed = time.time() - start_time

    print()
    print(f"  ✓ Réseau créé en {elapsed:.1f}s")
    print(f"  Lignes conservées: {len(lignes):,} / {n_total:,} ({len(lignes)/n_total*100:.1f}%)")
    print(f"  Éliminées par distance: {n_eliminées_distance:,}")
    print(f"  Éliminées par intensité: {n_eliminées_intensite:,}")
    print()

    return lignes

# ============================================================================
# MASSE VISIBLE
# ============================================================================

def masse_visible(r_kpc):
    """Masse visible Voie Lactée"""
    M_bulbe = 1.5e10 * M_soleil
    a_bulbe = 0.7
    M_bulbe_r = M_bulbe * (r_kpc**2) / ((r_kpc + a_bulbe)**2)

    M_disque = 6.0e10 * M_soleil
    R_d = 3.5
    x = r_kpc / R_d
    M_disque_r = M_disque * (1 - (1 + x) * math.exp(-x))

    M_gaz = 1.0e10 * M_soleil
    R_gaz = 7.0
    x_gaz = r_kpc / R_gaz
    M_gaz_r = M_gaz * (1 - (1 + x_gaz) * math.exp(-x_gaz))

    return M_bulbe_r + M_disque_r + M_gaz_r

# ============================================================================
# CHAMP γ_DESPRÉS
# ============================================================================

def gamma_despres_visible(r_kpc):
    """γ depuis masse visible"""
    M_vis = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    return -G * M_vis / (c**2 * r_m)

def gamma_despres_ligne(r_kpc, ligne, n_integration=10):
    """Contribution ligne Asselin (version ULTRA-rapide)"""
    r_eval = np.array([r_kpc, 0.0, 0.0])
    gamma_contrib = 0.0

    s_array = np.linspace(0, 1, n_integration)
    ds = 1.0 / (n_integration - 1) if n_integration > 1 else 1.0

    for s in s_array:
        r_ligne = ligne.point_sur_ligne(s)
        distance_kpc = max(np.linalg.norm(r_eval - r_ligne), 0.01)

        lambda_ligne = ligne.intensite * ligne.d_ij * M_soleil / kpc_to_m
        dl = ligne.d_ij * ds * kpc_to_m
        dgamma = -G / c**2 * lambda_ligne * dl / (distance_kpc * kpc_to_m)

        gamma_contrib += dgamma

    return gamma_contrib

def gamma_despres_total(r_kpc, lignes, verbose=False):
    """γ total avec progression"""
    gamma_vis = gamma_despres_visible(r_kpc)

    gamma_asselin = 0.0
    for i, ligne in enumerate(lignes):
        if verbose and i % 10000 == 0 and i > 0:
            print(f"      Processing line {i:,}/{len(lignes):,}")
        gamma_asselin += gamma_despres_ligne(r_kpc, ligne)

    return gamma_vis + gamma_asselin

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_orbitale_reseau(r_kpc, lignes):
    """v² = r·c²|dγ/dr|"""
    dr = 0.1

    gamma_r = gamma_despres_total(r_kpc, lignes)
    gamma_r_plus = gamma_despres_total(r_kpc + dr, lignes)

    dgamma_dr = (gamma_r_plus - gamma_r) / (dr * kpc_to_m)
    v_squared = max(r_kpc * kpc_to_m * c**2 * abs(dgamma_dr), 0)

    return math.sqrt(v_squared) / 1000.0

def vitesse_orbitale_newton(r_kpc):
    """Vitesse newtonienne"""
    M_vis = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    return math.sqrt(G * M_vis / r_m) / 1000.0

def courbe_rotation_reseau(r_array, lignes):
    """Courbe de rotation avec réseau 1000 galaxies"""
    print(f"Calcul courbe rotation ({len(r_array)} points)...")
    v_array = []
    for i, r in enumerate(r_array):
        if i % 10 == 0:
            print(f"  Point {i+1}/{len(r_array)}: r={r:.1f} kpc")
        v = vitesse_orbitale_reseau(r, lignes)
        v_array.append(v)
    print()
    return np.array(v_array)

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(v_calc, v_obs, sigma_obs):
    """χ²"""
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# TEST RÉSEAU 1000 GALAXIES
# ============================================================================

def test_reseau_1000_galaxies():
    """Test complet avec 1000 galaxies"""
    print("\n" + "="*80)
    print(" RÉSEAU ASSELIN À GRANDE ÉCHELLE : 1000 GALAXIES ".center(80))
    print("="*80)
    print()

    # Générer catalogue
    galaxies = generer_catalogue_1000_galaxies()

    # Créer réseau (ULTRA-optimisé: seulement lignes dominantes)
    d_eff = 1000.0  # kpc
    lignes = creer_reseau_asselin_optimise(galaxies, d_eff_kpc=d_eff,
                                           intensite_min=1e-4, d_max_kpc=5000.0)

    # Newton
    print("TEST 1: Newton (masse visible)")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r) for r in r_obs_kpc])
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_newton:.2f}")
    print()

    # Réseau 1000 galaxies
    print("TEST 2: Réseau 1000 galaxies")
    print("-" * 80)
    print(f"  Calcul avec {len(lignes):,} lignes Asselin...")
    print()

    start_time = time.time()
    v_reseau = courbe_rotation_reseau(r_obs_kpc, lignes)
    elapsed = time.time() - start_time

    chi2_reseau = chi_carre(v_reseau, v_obs_kms, sigma_obs_kms)

    print(f"  Temps calcul: {elapsed:.1f}s")
    print(f"  χ² = {chi2_reseau:.2f} ({chi2_reseau/chi2_newton:.2f}× vs Newton)")
    print()

    # Résultats
    print("="*80)
    print(" RÉSULTATS ".center(80))
    print("="*80)
    print(f"{'Modèle':<40} {'χ²':>15} {'vs Newton':>15}")
    print("-"*80)
    print(f"{'Newton (référence)':<40} {chi2_newton:>15.2f} {'1.00×':>15}")
    print(f"{'Réseau 1000 galaxies':<40} {chi2_reseau:>15.2f} {chi2_reseau/chi2_newton:>14.2f}×")
    print("="*80)
    print()

    print(f"Réseau:")
    print(f"  - {len(galaxies):,} galaxies")
    print(f"  - {len(lignes):,} lignes Asselin significatives")
    print(f"  - d_eff = {d_eff:.0f} kpc")
    print()

    if chi2_reseau < chi2_newton:
        print("🎉 SUCCÈS! Le réseau 1000 galaxies BAT NEWTON!")
        print(f"   Amélioration: {(1-chi2_reseau/chi2_newton)*100:.1f}%")
    elif chi2_reseau < 1.2 * chi2_newton:
        print("⚠️  Très proche de Newton")
        print(f"   L'échelle cosmique contribue significativement")
    else:
        print("⚠️  χ² > Newton")
        print(f"   Le réseau ne suffit pas à lui seul")

    print()
    print("="*80 + "\n")

    return {
        'chi2_newton': chi2_newton,
        'chi2_reseau': chi2_reseau,
        'n_galaxies': len(galaxies),
        'n_lignes': len(lignes)
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    resultats = test_reseau_1000_galaxies()
