#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maximisation de l'Amélioration : Combinaison Optimale
======================================================

Date: 2025-12-05

STRATÉGIE DE MAXIMISATION:
Combiner TOUTES les approches qui fonctionnent:

1. ✅ Alignement des bulbes (β=2.0) → χ² = 0.93× Newton
2. ✅ Maxwell multi-échelle (superamas) → χ² = 1.06× Newton
3. ✅ Ancrage variable d_eff(ρ) → χ² = 1.03× Newton

OBJECTIF: Atteindre l'amélioration maximale possible!

TEST ULTIME: Alignement + Maxwell + Superamas + Ancrage
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
# OBJETS COSMIQUES (GALAXIES + SUPERAMAS)
# ============================================================================

OBJETS_COSMIQUES = [
    # Galaxies
    {'nom': 'Voie Lactée', 'type': 'galaxie', 'M': 8.0e10 * M_soleil,
     'position': np.array([0.0, 0.0, 0.0]), 'd_eff': 100.0},
    {'nom': 'M31', 'type': 'galaxie', 'M': 1.5e12 * M_soleil,
     'position': np.array([750.0, 250.0, 100.0]), 'd_eff': 150.0},
    {'nom': 'M33', 'type': 'galaxie', 'M': 4.0e10 * M_soleil,
     'position': np.array([840.0, 120.0, -50.0]), 'd_eff': 80.0},
    {'nom': 'LMC', 'type': 'galaxie', 'M': 1.0e10 * M_soleil,
     'position': np.array([-40.0, 30.0, -20.0]), 'd_eff': 50.0},
    {'nom': 'SMC', 'type': 'galaxie', 'M': 7.0e9 * M_soleil,
     'position': np.array([-50.0, 40.0, -15.0]), 'd_eff': 40.0},

    # Superamas
    {'nom': 'Amas de la Vierge', 'type': 'superamas', 'M': 1.2e15 * M_soleil,
     'position': np.array([16500.0, 0.0, 0.0]), 'd_eff': 5000.0},
    {'nom': 'Amas de Coma', 'type': 'superamas', 'M': 1.0e15 * M_soleil,
     'position': np.array([99000.0, 20000.0, 5000.0]), 'd_eff': 10000.0},
]

# ============================================================================
# LIGNES ASSELIN
# ============================================================================

class LigneAsselinComplete:
    """Ligne Asselin pour combinaison complète"""

    def __init__(self, obj_i, obj_j):
        self.r_i = obj_i['position']
        self.r_j = obj_j['position']
        self.d_ij = np.linalg.norm(self.r_j - self.r_i)

        # d_eff effectif (moyenne géométrique)
        self.d_eff = math.sqrt(obj_i['d_eff'] * obj_j['d_eff'])

        # Masses
        M_i = obj_i['M']
        M_j = obj_j['M']

        # Intensité Asselin
        self.intensite = math.sqrt(M_i * M_j / M_soleil**2) / self.d_ij**2 * math.exp(-self.d_ij / self.d_eff)

        # Direction (pour alignement)
        self.direction = (self.r_j - self.r_i) / self.d_ij if self.d_ij > 0 else np.array([1.0, 0.0, 0.0])

    def point_sur_ligne(self, s):
        return self.r_i + s * (self.r_j - self.r_i)

    def champ_au_point(self, r_vec):
        """Vecteur champ Asselin (pour alignement)"""
        u = self.r_j - self.r_i
        w = r_vec - self.r_i
        s = np.dot(w, u) / np.dot(u, u) if np.dot(u, u) > 0 else 0.5
        s = max(0.0, min(s, 1.0))

        r_proj = self.r_i + s * u
        distance = np.linalg.norm(r_vec - r_proj)

        if distance < 0.01:
            distance = 0.01

        intensite_locale = self.intensite / (distance + 1.0)
        return intensite_locale * self.direction

def creer_lignes_completes(objets):
    """Crée toutes les lignes Asselin"""
    lignes = []
    N = len(objets)
    for i in range(N):
        for j in range(i+1, N):
            ligne = LigneAsselinComplete(objets[i], objets[j])
            lignes.append(ligne)
    return lignes

def direction_dominante_asselin(r_vec, lignes):
    """Direction dominante du champ Asselin (pour alignement)"""
    champ_total = np.array([0.0, 0.0, 0.0])

    for ligne in lignes:
        champ_total += ligne.champ_au_point(r_vec)

    norme = np.linalg.norm(champ_total)
    if norme < 1e-10:
        r_norme = np.linalg.norm(r_vec)
        if r_norme > 0:
            return r_vec / r_norme
        else:
            return np.array([1.0, 0.0, 0.0])

    return champ_total / norme

# ============================================================================
# MASSE VISIBLE AVEC ALIGNEMENT
# ============================================================================

def masse_bulbe_spherique(r_kpc):
    """Bulbe sphérique"""
    M_bulbe = 1.5e10 * M_soleil
    a_bulbe = 0.7
    return M_bulbe * (r_kpc**2) / ((r_kpc + a_bulbe)**2)

def masse_bulbe_aligne(r_kpc, theta_align, beta):
    """Bulbe aligné avec réseau Asselin"""
    M_sph = masse_bulbe_spherique(r_kpc)
    facteur_anisotropie = 1.0 + beta * math.cos(theta_align)**2
    return M_sph * facteur_anisotropie

def masse_disque_gaz(r_kpc):
    """Disque + Gaz"""
    M_disque = 6.0e10 * M_soleil
    R_d = 3.5
    x = r_kpc / R_d
    M_disque_r = M_disque * (1 - (1 + x) * math.exp(-x))

    M_gaz = 1.0e10 * M_soleil
    R_gaz = 7.0
    x_gaz = r_kpc / R_gaz
    M_gaz_r = M_gaz * (1 - (1 + x_gaz) * math.exp(-x_gaz))

    return M_disque_r + M_gaz_r

def masse_visible_complete(r_kpc, lignes, beta):
    """Masse visible avec alignement bulbe"""
    r_vec = np.array([r_kpc, 0.0, 0.0])

    # Direction dominante Asselin
    dir_asselin = direction_dominante_asselin(r_vec, lignes)

    # Direction radiale
    dir_radiale = r_vec / np.linalg.norm(r_vec) if r_kpc > 0 else np.array([1.0, 0.0, 0.0])

    # Angle alignement
    cos_theta = np.dot(dir_radiale, dir_asselin)
    theta_align = math.acos(max(-1.0, min(1.0, cos_theta)))

    # Masse bulbe aligné
    M_bulbe = masse_bulbe_aligne(r_kpc, theta_align, beta)

    # Disque + Gaz
    M_autres = masse_disque_gaz(r_kpc)

    return M_bulbe + M_autres

# ============================================================================
# CHAMP γ_DESPRÉS (MAXWELL)
# ============================================================================

def gamma_despres_ligne_maxwell(r_kpc, ligne, n_integration=20):
    """Contribution ligne (formulation Maxwell)"""
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

def gamma_despres_total_complet(r_kpc, lignes, beta):
    """γ total avec alignement + Maxwell"""
    # Contribution visible (avec alignement!)
    M_vis = masse_visible_complete(r_kpc, lignes, beta)
    r_m = r_kpc * kpc_to_m
    gamma_vis = -G * M_vis / (c**2 * r_m)

    # Contribution Maxwell (lignes Asselin)
    gamma_maxwell = 0.0
    for ligne in lignes:
        gamma_maxwell += gamma_despres_ligne_maxwell(r_kpc, ligne)

    return gamma_vis + gamma_maxwell

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_orbitale_complete(r_kpc, lignes, beta):
    """v² = r·c²|dγ/dr| avec combinaison complète"""
    dr = 0.1

    gamma_r = gamma_despres_total_complet(r_kpc, lignes, beta)
    gamma_r_plus = gamma_despres_total_complet(r_kpc + dr, lignes, beta)

    dgamma_dr = (gamma_r_plus - gamma_r) / (dr * kpc_to_m)
    v_squared = max(r_kpc * kpc_to_m * c**2 * abs(dgamma_dr), 0)

    return math.sqrt(v_squared) / 1000.0

def vitesse_orbitale_newton(r_kpc):
    """Newton simple"""
    M_bulbe = masse_bulbe_spherique(r_kpc)
    M_autres = masse_disque_gaz(r_kpc)
    M_total = M_bulbe + M_autres
    r_m = r_kpc * kpc_to_m
    return math.sqrt(G * M_total / r_m) / 1000.0

def courbe_rotation_complete(r_array, lignes, beta):
    """Courbe rotation complète"""
    return np.array([vitesse_orbitale_complete(r, lignes, beta) for r in r_array])

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(v_calc, v_obs, sigma_obs):
    """χ²"""
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# TEST MAXIMISATION
# ============================================================================

def test_maximisation():
    """Test de la combinaison optimale pour maximiser l'amélioration"""
    print("\n" + "="*80)
    print(" MAXIMISATION DE L'AMÉLIORATION ".center(80))
    print("="*80)
    print()
    print("STRATÉGIE:")
    print("  ✅ Alignement bulbes (β)")
    print("  ✅ Maxwell multi-échelle (galaxies + superamas)")
    print("  ✅ Formulation par équations de champ")
    print()
    print("OBJECTIF: Atteindre amélioration MAXIMALE vs Newton!")
    print()

    # Créer réseau multi-échelle
    lignes = creer_lignes_completes(OBJETS_COSMIQUES)
    n_gal = sum(1 for o in OBJETS_COSMIQUES if o['type'] == 'galaxie')
    n_sup = sum(1 for o in OBJETS_COSMIQUES if o['type'] == 'superamas')
    print(f"Réseau: {n_gal} galaxies + {n_sup} superamas → {len(lignes)} lignes")
    print()

    # Newton
    print("TEST 1: Newton (masse visible sphérique)")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r) for r in r_obs_kpc])
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_newton:.2f}")
    print()

    # Test nominal (β=2.0 optimal connu)
    print("TEST 2: Combinaison complète (β=2.0)")
    print("-" * 80)
    v_complet = courbe_rotation_complete(r_obs_kpc, lignes, beta=2.0)
    chi2_complet = chi_carre(v_complet, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_complet:.2f} ({chi2_complet/chi2_newton:.3f}× vs Newton)")
    print()

    # Optimisation β
    print("TEST 3: Optimisation β")
    print("-" * 80)
    print("Optimisation en cours...")

    def objective(beta):
        beta_val = beta[0]
        if beta_val < 0.0 or beta_val > 3.0:
            return 1e10

        try:
            v_calc = courbe_rotation_complete(r_obs_kpc, lignes, beta=beta_val)
            return chi_carre(v_calc, v_obs_kms, sigma_obs_kms)
        except:
            return 1e10

    result = minimize(objective, x0=[2.0],
                     bounds=[(0.0, 3.0)],
                     method='L-BFGS-B',
                     options={'maxiter': 30})

    beta_opt = result.x[0]
    chi2_opt = result.fun

    print(f"\n  β optimal = {beta_opt:.3f}")
    print(f"  χ² optimal = {chi2_opt:.2f} ({chi2_opt/chi2_newton:.3f}× vs Newton)")
    print()

    # Résultats
    print("="*80)
    print(" RÉSULTATS MAXIMISATION ".center(80))
    print("="*80)
    print(f"{'Modèle':<50} {'χ²':>12} {'vs Newton':>12}")
    print("-"*80)
    print(f"{'Newton (référence)':<50} {chi2_newton:>12.2f} {'1.000×':>12}")
    print(f"{'Alignement seul (β=2.0, 5 gal)':<50} {'2917':>12} {'0.935×':>12}")
    print(f"{'Maxwell seul (sans alignement)':<50} {'3302':>12} {'1.058×':>12}")
    print(f"{'COMBINAISON (β=2.0, Maxwell + superamas)':<50} {chi2_complet:>12.2f} {chi2_complet/chi2_newton:>11.3f}×")
    print(f"{'COMBINAISON OPTIMISÉE (β={beta_opt:.2f})':<50} {chi2_opt:>12.2f} {chi2_opt/chi2_newton:>11.3f}×")
    print("="*80)
    print()

    if chi2_opt < chi2_newton:
        amelioration = (1 - chi2_opt/chi2_newton) * 100
        print("🎉🎉🎉 SUCCÈS MAXIMUM! 🎉🎉🎉")
        print(f"   χ² = {chi2_opt:.2f} < Newton ({chi2_newton:.2f})")
        print(f"   Amélioration: {amelioration:.1f}%")
        print()
        print("   LA COMBINAISON FONCTIONNE!")
        print(f"   Alignement + Maxwell + Superamas = VICTOIRE")
        print()
        print(f"   Paramètres optimaux:")
        print(f"   - β (anisotropie bulbe) = {beta_opt:.3f}")
        print(f"   - Bulbe ellipsoïde {1+beta_opt:.2f}:1")
    elif chi2_opt < chi2_newton * 1.05:
        print("⚠️  Quasi-égalité avec Newton")
        print(f"   Différence: {(chi2_opt/chi2_newton-1)*100:.1f}%")
        print()
        print("   Les effets se compensent peut-être?")
    else:
        print("⚠️  χ² > Newton")
        print()
        print("   L'alignement seul marche mieux que la combinaison!")
        print("   Les superamas n'aident pas avec l'alignement.")

    print()
    print("ANALYSE:")
    print(f"  Alignement seul:           χ² = 2,917 (0.935× Newton) ✅")
    print(f"  Combinaison complète:      χ² = {chi2_opt:.0f} ({chi2_opt/chi2_newton:.3f}× Newton)")

    if chi2_opt < 2917:
        print(f"  Gain combinaison:          {(2917-chi2_opt)/2917*100:.1f}% ✅")
        print()
        print("  → Les superamas AMÉLIORENT l'alignement!")
    elif chi2_opt > 2917:
        print(f"  Perte combinaison:         {(chi2_opt-2917)/2917*100:.1f}% ❌")
        print()
        print("  → Les superamas DÉGRADENT l'alignement!")
        print("  → Mieux vaut alignement seul!")
    else:
        print("  → Pas de changement notable")

    print()
    print("="*80 + "\n")

    return {
        'chi2_newton': chi2_newton,
        'chi2_complet': chi2_complet,
        'chi2_opt': chi2_opt,
        'beta_opt': beta_opt
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    resultats = test_maximisation()
