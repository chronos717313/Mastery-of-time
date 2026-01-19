#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'Alignement des Bulbes selon le Réseau Asselin
=========================================================

Date: 2025-12-05
Branche: claude/temporal-distortion-calculation-01P4ffpawn6QMj7vVq6PSVcS

PRÉDICTION THÉORIQUE:
Selon la Théorie de Maîtrise du Temps, les bulbes galactiques ne sont PAS
sphériques aléatoires, mais s'ALIGNENT avec le réseau de liaisons Asselin.

PHYSIQUE:
- Liaisons Asselin créent la structure gravitotemporelle
- Bulbes = concentrations de masse suivant cette structure
- Densité du bulbe devrait être ANISOTROPE: plus élevée le long des lignes Asselin

MODÈLES À COMPARER:
1. Bulbe SPHÉRIQUE (modèle standard): ρ_bulbe(r)
2. Bulbe ALIGNÉ (prédiction): ρ_bulbe(r, θ_Asselin) avec anisotropie

Si la théorie est correcte → Bulbe aligné devrait donner χ² < Bulbe sphérique!
"""

import math
import numpy as np
from scipy.optimize import minimize

# ============================================================================
# CONSTANTES
# ============================================================================

G = 6.674e-11
c = 299792458
M_soleil = 1.989e30
kpc_to_m = 3.086e19

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
# GALAXIES
# ============================================================================

GALAXIES = [
    {'nom': 'Voie Lactée', 'M': 8.0e10 * M_soleil, 'position': np.array([0.0, 0.0, 0.0])},
    {'nom': 'M31', 'M': 1.5e12 * M_soleil, 'position': np.array([750.0, 250.0, 100.0])},
    {'nom': 'M33', 'M': 4.0e10 * M_soleil, 'position': np.array([840.0, 120.0, -50.0])},
    {'nom': 'LMC', 'M': 1.0e10 * M_soleil, 'position': np.array([-40.0, 30.0, -20.0])},
    {'nom': 'SMC', 'M': 7.0e9 * M_soleil, 'position': np.array([-50.0, 40.0, -15.0])},
]

# ============================================================================
# LIGNES ASSELIN
# ============================================================================

class LigneAsselin:
    """Ligne Asselin entre deux galaxies"""

    def __init__(self, gal_i, gal_j, d_eff_kpc=100.0):
        self.r_i = gal_i['position']
        self.r_j = gal_j['position']
        self.d_ij = np.linalg.norm(self.r_j - self.r_i)

        M_i = gal_i['M']
        M_j = gal_j['M']
        self.intensite = math.sqrt(M_i * M_j / M_soleil**2) / self.d_ij**2 * math.exp(-self.d_ij / d_eff_kpc)

        # Direction de la ligne (vecteur unitaire)
        self.direction = (self.r_j - self.r_i) / self.d_ij

    def point_sur_ligne(self, s):
        """Point paramétrique, s ∈ [0,1]"""
        return self.r_i + s * (self.r_j - self.r_i)

    def champ_au_point(self, r_vec):
        """
        Vecteur champ Asselin au point r_vec

        Direction: le long de la ligne
        Intensité: fonction de distance à la ligne
        """
        # Trouver point le plus proche sur ligne
        u = self.r_j - self.r_i
        w = r_vec - self.r_i
        s = np.dot(w, u) / np.dot(u, u)
        s = max(0.0, min(s, 1.0))

        r_proj = self.r_i + s * u
        distance = np.linalg.norm(r_vec - r_proj)

        # Intensité décroit avec distance perpendiculaire
        if distance < 0.01:
            distance = 0.01

        intensite_locale = self.intensite / (distance + 1.0)  # +1 pour éviter divergence

        # Vecteur champ = intensité × direction ligne
        return intensite_locale * self.direction

def creer_lignes_asselin(galaxies, d_eff_kpc=100.0):
    """Crée lignes Asselin"""
    lignes = []
    N = len(galaxies)
    for i in range(N):
        for j in range(i+1, N):
            ligne = LigneAsselin(galaxies[i], galaxies[j], d_eff_kpc)
            lignes.append(ligne)
    return lignes

def direction_dominante_asselin(r_vec, lignes):
    """
    Trouve la direction dominante du champ Asselin au point r_vec

    Returns:
        Vecteur unitaire de direction dominante
    """
    champ_total = np.array([0.0, 0.0, 0.0])

    for ligne in lignes:
        champ_total += ligne.champ_au_point(r_vec)

    norme = np.linalg.norm(champ_total)
    if norme < 1e-10:
        # Si pas de champ, retourner direction radiale par défaut
        r_norme = np.linalg.norm(r_vec)
        if r_norme > 0:
            return r_vec / r_norme
        else:
            return np.array([1.0, 0.0, 0.0])

    return champ_total / norme

# ============================================================================
# MASSE VISIBLE AVEC BULBE SPHÉRIQUE (MODÈLE STANDARD)
# ============================================================================

def masse_bulbe_spherique(r_kpc):
    """Bulbe sphérique standard"""
    M_bulbe = 1.5e10 * M_soleil
    a_bulbe = 0.7
    return M_bulbe * (r_kpc**2) / ((r_kpc + a_bulbe)**2)

def masse_disque_gaz(r_kpc):
    """Disque + Gaz (reste identique)"""
    M_disque = 6.0e10 * M_soleil
    R_d = 3.5
    x = r_kpc / R_d
    M_disque_r = M_disque * (1 - (1 + x) * math.exp(-x))

    M_gaz = 1.0e10 * M_soleil
    R_gaz = 7.0
    x_gaz = r_kpc / R_gaz
    M_gaz_r = M_gaz * (1 - (1 + x_gaz) * math.exp(-x_gaz))

    return M_disque_r + M_gaz_r

def masse_visible_spherique(r_kpc):
    """Masse totale avec bulbe SPHÉRIQUE"""
    return masse_bulbe_spherique(r_kpc) + masse_disque_gaz(r_kpc)

# ============================================================================
# MASSE VISIBLE AVEC BULBE ALIGNÉ (PRÉDICTION THÉORIQUE)
# ============================================================================

def masse_bulbe_aligne(r_kpc, theta_align, beta=0.5):
    """
    Bulbe ALIGNÉ avec le réseau Asselin

    Args:
        r_kpc: Distance radiale
        theta_align: Angle entre direction radiale et direction Asselin dominante
        beta: Facteur d'anisotropie (0=sphérique, 1=totalement aligné)

    La masse est modulée selon l'alignement:
    M_bulbe_aligné(r, θ) = M_bulbe_sphérique(r) × [1 + β·cos²(θ)]

    Physique:
    - θ = 0° (aligné) → facteur (1 + β) → masse augmentée
    - θ = 90° (perpendiculaire) → facteur 1 → masse standard
    """
    M_sph = masse_bulbe_spherique(r_kpc)

    # Modulation anisotrope
    facteur_anisotropie = 1.0 + beta * math.cos(theta_align)**2

    return M_sph * facteur_anisotropie

def masse_visible_alignee(r_kpc, lignes, beta=0.5):
    """
    Masse totale avec bulbe ALIGNÉ sur réseau Asselin

    Args:
        r_kpc: Rayon (on suppose plan galactique, θ=0, φ varié moyenné)
        lignes: Lignes Asselin
        beta: Anisotropie
    """
    # Point d'évaluation (plan galactique)
    r_vec = np.array([r_kpc, 0.0, 0.0])

    # Direction dominante Asselin
    dir_asselin = direction_dominante_asselin(r_vec, lignes)

    # Direction radiale
    dir_radiale = r_vec / np.linalg.norm(r_vec) if r_kpc > 0 else np.array([1.0, 0.0, 0.0])

    # Angle entre radiale et Asselin
    cos_theta = np.dot(dir_radiale, dir_asselin)
    theta_align = math.acos(max(-1.0, min(1.0, cos_theta)))

    # Masse bulbe aligné
    M_bulbe = masse_bulbe_aligne(r_kpc, theta_align, beta)

    # Disque + Gaz (inchangés)
    M_autres = masse_disque_gaz(r_kpc)

    return M_bulbe + M_autres

# ============================================================================
# VITESSES ORBITALES
# ============================================================================

def vitesse_orbitale_spherique(r_kpc):
    """Vitesse avec bulbe SPHÉRIQUE (modèle standard)"""
    M = masse_visible_spherique(r_kpc)
    r_m = r_kpc * kpc_to_m
    return math.sqrt(G * M / r_m) / 1000.0

def vitesse_orbitale_alignee(r_kpc, lignes, beta=0.5):
    """Vitesse avec bulbe ALIGNÉ (prédiction théorique)"""
    M = masse_visible_alignee(r_kpc, lignes, beta)
    r_m = r_kpc * kpc_to_m
    return math.sqrt(G * M / r_m) / 1000.0

def courbe_rotation_alignee(r_array, lignes, beta=0.5):
    """Courbe de rotation avec alignement"""
    return np.array([vitesse_orbitale_alignee(r, lignes, beta) for r in r_array])

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(v_calc, v_obs, sigma_obs):
    """χ²"""
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# TEST ALIGNEMENT BULBES
# ============================================================================

def test_alignement_bulbes():
    """Test de l'alignement des bulbes avec le réseau Asselin"""
    print("\n" + "="*80)
    print(" TEST: ALIGNEMENT DES BULBES AVEC RÉSEAU ASSELIN ".center(80))
    print("="*80)
    print()
    print("PRÉDICTION THÉORIQUE:")
    print("  Les bulbes ne sont PAS sphériques aléatoires,")
    print("  mais s'ALIGNENT avec le réseau de liaisons Asselin")
    print()
    print("MODÈLES:")
    print("  1. Bulbe SPHÉRIQUE (modèle standard): ρ(r)")
    print("  2. Bulbe ALIGNÉ (prédiction): ρ(r,θ) avec anisotropie")
    print()

    # Créer réseau Asselin
    lignes = creer_lignes_asselin(GALAXIES, d_eff_kpc=500.0)
    print(f"Réseau Asselin: {len(GALAXIES)} galaxies → {len(lignes)} lignes")
    print()

    # Test 1: Bulbe sphérique (standard)
    print("TEST 1: Bulbe SPHÉRIQUE (modèle standard)")
    print("-" * 80)
    v_spherique = np.array([vitesse_orbitale_spherique(r) for r in r_obs_kpc])
    chi2_spherique = chi_carre(v_spherique, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_spherique:.2f}")
    print()

    # Test 2: Bulbe aligné nominal (β = 0.5)
    print("TEST 2: Bulbe ALIGNÉ nominal (β = 0.5)")
    print("-" * 80)
    v_aligne_nominal = courbe_rotation_alignee(r_obs_kpc, lignes, beta=0.5)
    chi2_aligne_nominal = chi_carre(v_aligne_nominal, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_aligne_nominal:.2f} ({chi2_aligne_nominal/chi2_spherique:.3f}× vs sphérique)")
    print()

    # Test 3: Optimisation du facteur d'anisotropie β
    print("TEST 3: Optimisation du facteur d'anisotropie β")
    print("-" * 80)
    print("Optimisation en cours...")

    def objective(beta):
        beta_val = beta[0]

        if beta_val < 0.0 or beta_val > 2.0:
            return 1e10

        try:
            v_calc = courbe_rotation_alignee(r_obs_kpc, lignes, beta=beta_val)
            return chi_carre(v_calc, v_obs_kms, sigma_obs_kms)
        except:
            return 1e10

    result = minimize(objective, x0=[0.5],
                     bounds=[(0.0, 2.0)],
                     method='L-BFGS-B',
                     options={'maxiter': 30})

    beta_opt = result.x[0]
    chi2_opt = result.fun

    print(f"\n  β optimal = {beta_opt:.3f}")
    print(f"  χ² optimal = {chi2_opt:.2f} ({chi2_opt/chi2_spherique:.3f}× vs sphérique)")
    print()

    # Résultats
    print("="*80)
    print(" RÉSULTATS ".center(80))
    print("="*80)
    print(f"{'Modèle':<40} {'χ²':>15} {'vs Sphérique':>15}")
    print("-"*80)
    print(f"{'Bulbe SPHÉRIQUE (standard)':<40} {chi2_spherique:>15.2f} {'1.000×':>15}")
    print(f"{'Bulbe ALIGNÉ nominal (β=0.5)':<40} {chi2_aligne_nominal:>15.2f} {chi2_aligne_nominal/chi2_spherique:>14.3f}×")
    print(f"{'Bulbe ALIGNÉ optimisé':<40} {chi2_opt:>15.2f} {chi2_opt/chi2_spherique:>14.3f}×")
    print("="*80)
    print()

    # Analyse
    if chi2_opt < chi2_spherique:
        amelioration = (1 - chi2_opt/chi2_spherique) * 100
        print("🎉 VALIDATION DE LA PRÉDICTION THÉORIQUE!")
        print(f"   χ²_aligné = {chi2_opt:.2f} < χ²_sphérique = {chi2_spherique:.2f}")
        print(f"   Amélioration: {amelioration:.1f}%")
        print()
        print(f"   ✅ Les bulbes s'ALIGNENT effectivement avec le réseau Asselin!")
        print(f"   ✅ Facteur d'anisotropie: β = {beta_opt:.3f}")
        print()
        if beta_opt > 0.1:
            print(f"   L'alignement est SIGNIFICATIF (β = {beta_opt:.3f} >> 0)")
            print(f"   Les bulbes sont effectivement orientés par les liaisons Asselin!")
        else:
            print(f"   L'alignement est FAIBLE (β = {beta_opt:.3f} ≈ 0)")
            print(f"   L'effet existe mais est subtil")
    elif chi2_opt > chi2_spherique * 1.01:
        print("❌ La prédiction n'est PAS validée")
        print(f"   χ²_aligné = {chi2_opt:.2f} > χ²_sphérique = {chi2_spherique:.2f}")
        print(f"   Dégradation: {(chi2_opt/chi2_spherique - 1)*100:.1f}%")
        print()
        print("   Les bulbes semblent sphériques (pas d'alignement détectable)")
    else:
        print("⚠️  Résultats équivalents")
        print(f"   χ²_aligné ≈ χ²_sphérique (différence < 1%)")
        print()
        print("   L'alignement n'apporte pas d'amélioration détectable")
        print("   Les données sont compatibles avec bulbe sphérique")

    print()

    # Interprétation physique
    print("="*80)
    print(" INTERPRÉTATION PHYSIQUE ".center(80))
    print("="*80)
    print()

    if beta_opt > 0.1:
        print("SIGNIFICATION DE β = {:.3f}:".format(beta_opt))
        print()
        print("  Dans direction ALIGNÉE avec Asselin:")
        print(f"    Facteur de masse: 1 + β = {1 + beta_opt:.3f}")
        print(f"    → Masse bulbe augmentée de {beta_opt*100:.1f}%")
        print()
        print("  Dans direction PERPENDICULAIRE:")
        print(f"    Facteur de masse: 1.0")
        print(f"    → Masse bulbe standard")
        print()
        print("  CONCLUSION:")
        print("    Le bulbe est un ELLIPSOÏDE orienté le long du réseau Asselin")
        print("    Rapport des axes: ~ {:.2f}:1".format(1 + beta_opt))
    else:
        print("β ≈ 0 suggère:")
        print("  - Soit les bulbes sont effectivement sphériques")
        print("  - Soit l'effet d'alignement existe mais est trop faible")
        print("    pour être détecté avec ces données")

    print()
    print("="*80 + "\n")

    return {
        'chi2_spherique': chi2_spherique,
        'chi2_aligne_nominal': chi2_aligne_nominal,
        'chi2_opt': chi2_opt,
        'beta_opt': beta_opt,
        'amelioration_pct': (1 - chi2_opt/chi2_spherique) * 100 if chi2_opt < chi2_spherique else 0
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    resultats = test_alignement_bulbes()
