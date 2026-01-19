#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERSION RAPIDE: Formulation Maxwell avec Ancrage par les Bulbes
================================================================

VERSION OPTIMISÉE pour test rapide:
- Seulement 5 galaxies (pas de superamas)
- Moins de points d'intégration (20 au lieu de 50)
- Optimisation rapide (20 itérations)
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
# GALAXIES PROCHES SEULEMENT
# ============================================================================

GALAXIES = [
    {'nom': 'Voie Lactée', 'M': 8.0e10 * M_soleil, 'position': np.array([0.0, 0.0, 0.0])},
    {'nom': 'M31', 'M': 1.5e12 * M_soleil, 'position': np.array([750.0, 250.0, 100.0])},
    {'nom': 'M33', 'M': 4.0e10 * M_soleil, 'position': np.array([840.0, 120.0, -50.0])},
    {'nom': 'LMC', 'M': 1.0e10 * M_soleil, 'position': np.array([-40.0, 30.0, -20.0])},
    {'nom': 'SMC', 'M': 7.0e9 * M_soleil, 'position': np.array([-50.0, 40.0, -15.0])},
]

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

def densite_visible(r_kpc):
    """Densité visible ρ_vis(r)"""
    if r_kpc < 0.1:
        r_kpc = 0.1

    dr = 0.1
    dM_dr = (masse_visible(r_kpc + dr/2) - masse_visible(r_kpc - dr/2)) / dr
    dM_dr_SI = dM_dr / kpc_to_m

    r_m = r_kpc * kpc_to_m
    rho = dM_dr_SI / (4 * math.pi * r_m**2)

    return rho

def densite_bulbe_reference():
    """Densité du bulbe (référence)"""
    return densite_visible(0.5)

# ============================================================================
# d_eff VARIABLE AVEC ANCRAGE
# ============================================================================

def d_eff_ancrage(r_kpc, d_min, d_max, alpha):
    """
    d_eff(r) = d_min + (d_max - d_min) · [ρ(r)/ρ_bulbe]^α

    Haute ρ (bulbe) → d_eff = d_max → ancrage fort
    Basse ρ (halo) → d_eff = d_min → expansion domine
    """
    rho_r = densite_visible(r_kpc)
    rho_bulbe = densite_bulbe_reference()

    ratio = max(rho_r / rho_bulbe, 1e-10)
    d_eff = d_min + (d_max - d_min) * ratio**alpha

    return d_eff

# ============================================================================
# LIGNE ASSELIN SIMPLIFIÉE
# ============================================================================

class LigneAsselinAncrage:
    """Ligne Asselin avec d_eff variable"""

    def __init__(self, gal_i, gal_j, params_ancrage):
        self.r_i = gal_i['position']
        self.r_j = gal_j['position']
        self.params = params_ancrage  # (d_min, d_max, alpha)

        self.d_ij = np.linalg.norm(self.r_j - self.r_i)
        self.M_i = gal_i['M']
        self.M_j = gal_j['M']

    def point_sur_ligne(self, s):
        """Point paramétrique, s ∈ [0,1]"""
        return self.r_i + s * (self.r_j - self.r_i)

    def intensite_au_point(self, r_vec):
        """
        Intensité avec d_eff local

        I(r⃗) = √(M_i·M_j) / d_ij² · exp(-d_ij/d_eff(r⃗))
        """
        r_kpc = np.linalg.norm(r_vec)
        d_min, d_max, alpha = self.params
        d_eff = d_eff_ancrage(r_kpc, d_min, d_max, alpha)

        intensite = math.sqrt(self.M_i * self.M_j / M_soleil**2) / self.d_ij**2 * math.exp(-self.d_ij / d_eff)
        return intensite

def creer_lignes_ancrage(galaxies, params_ancrage):
    """Crée lignes Asselin"""
    lignes = []
    N = len(galaxies)
    for i in range(N):
        for j in range(i+1, N):
            ligne = LigneAsselinAncrage(galaxies[i], galaxies[j], params_ancrage)
            lignes.append(ligne)
    return lignes

# ============================================================================
# CHAMP γ_DESPRÉS
# ============================================================================

def gamma_despres_visible(r_kpc):
    """γ depuis masse visible"""
    M_vis = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    return -G * M_vis / (c**2 * r_m)

def gamma_despres_ligne_ancrage(r_kpc, ligne, n_integration=20):
    """
    Contribution ligne avec ancrage (RAPIDE: 20 points au lieu de 50)
    """
    r_eval = np.array([r_kpc, 0.0, 0.0])
    gamma_contrib = 0.0

    s_array = np.linspace(0, 1, n_integration)
    ds = 1.0 / (n_integration - 1)

    for s in s_array:
        r_ligne = ligne.point_sur_ligne(s)
        distance_kpc = max(np.linalg.norm(r_eval - r_ligne), 0.01)

        intensite_locale = ligne.intensite_au_point(r_ligne)
        lambda_ligne = intensite_locale * ligne.d_ij * M_soleil / kpc_to_m

        dl = ligne.d_ij * ds * kpc_to_m
        dgamma = -G / c**2 * lambda_ligne * dl / (distance_kpc * kpc_to_m)

        gamma_contrib += dgamma

    return gamma_contrib

def gamma_despres_total_ancrage(r_kpc, lignes):
    """γ total avec ancrage"""
    gamma_vis = gamma_despres_visible(r_kpc)
    gamma_asselin = sum(gamma_despres_ligne_ancrage(r_kpc, ligne) for ligne in lignes)
    return gamma_vis + gamma_asselin

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_orbitale_ancrage(r_kpc, lignes):
    """v²(r) = r·c²|dγ/dr|"""
    dr = 0.1

    gamma_r = gamma_despres_total_ancrage(r_kpc, lignes)
    gamma_r_plus = gamma_despres_total_ancrage(r_kpc + dr, lignes)

    dgamma_dr = (gamma_r_plus - gamma_r) / (dr * kpc_to_m)
    v_squared = max(r_kpc * kpc_to_m * c**2 * abs(dgamma_dr), 0)

    return math.sqrt(v_squared) / 1000.0

def vitesse_orbitale_newton(r_kpc):
    """Vitesse newtonienne"""
    M_vis = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    return math.sqrt(G * M_vis / r_m) / 1000.0

def courbe_rotation_ancrage(r_array, lignes):
    """Courbe de rotation"""
    return np.array([vitesse_orbitale_ancrage(r, lignes) for r in r_array])

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi_carre(v_calc, v_obs, sigma_obs):
    """χ²"""
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# TEST RAPIDE
# ============================================================================

def test_ancrage_rapide():
    """Test rapide de l'ancrage par bulbes"""
    print("\n" + "="*80)
    print(" VERSION RAPIDE: ANCRAGE PAR BULBES ".center(80))
    print("="*80)
    print()
    print("CONCEPT: Bulbes = ancres limitant expansion")
    print("         d_eff(ρ) variable localement")
    print()
    print(f"Réseau: {len(GALAXIES)} galaxies → {len(GALAXIES)*(len(GALAXIES)-1)//2} lignes")
    print(f"Intégration: 20 points/ligne (rapide)")
    print()

    # Newton
    print("TEST 1: Newton")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r) for r in r_obs_kpc])
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_newton:.2f}")
    print()

    # Nominal
    print("TEST 2: Ancrage nominal (d_min=10, d_max=1000, α=0.5)")
    print("-" * 80)
    params_nominal = (10.0, 1000.0, 0.5)
    lignes_nominal = creer_lignes_ancrage(GALAXIES, params_nominal)
    v_nominal = courbe_rotation_ancrage(r_obs_kpc, lignes_nominal)
    chi2_nominal = chi_carre(v_nominal, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_nominal:.2f} ({chi2_nominal/chi2_newton:.2f}× vs Newton)")
    print()

    # Optimisation RAPIDE
    print("TEST 3: Optimisation rapide (20 itérations)")
    print("-" * 80)

    def objective(params):
        d_min, d_max, alpha = params

        if d_min < 1 or d_min > 100:
            return 1e10
        if d_max < 100 or d_max > 5000:
            return 1e10
        if alpha < 0.1 or alpha > 3.0:
            return 1e10
        if d_max <= d_min:
            return 1e10

        try:
            lignes_opt = creer_lignes_ancrage(GALAXIES, params)
            v_calc = courbe_rotation_ancrage(r_obs_kpc, lignes_opt)
            return chi_carre(v_calc, v_obs_kms, sigma_obs_kms)
        except:
            return 1e10

    result = minimize(objective, x0=[10.0, 1000.0, 0.5],
                     bounds=[(1.0, 100.0), (100.0, 5000.0), (0.1, 3.0)],
                     method='L-BFGS-B',
                     options={'maxiter': 20})

    d_min_opt, d_max_opt, alpha_opt = result.x
    chi2_opt = result.fun

    print(f"\n  d_min optimal  = {d_min_opt:.2f} kpc")
    print(f"  d_max optimal  = {d_max_opt:.2f} kpc")
    print(f"  α optimal      = {alpha_opt:.2f}")
    print(f"  χ² optimal     = {chi2_opt:.2f} ({chi2_opt/chi2_newton:.2f}× vs Newton)")
    print()

    # Résultats
    print("="*80)
    print(" RÉSULTATS ".center(80))
    print("="*80)
    print(f"{'Modèle':<30} {'χ²':>15} {'vs Newton':>15}")
    print("-"*80)
    print(f"{'Newton':<30} {chi2_newton:>15.2f} {'1.00×':>15}")
    print(f"{'Ancrage nominal':<30} {chi2_nominal:>15.2f} {chi2_nominal/chi2_newton:>14.2f}×")
    print(f"{'Ancrage optimisé':<30} {chi2_opt:>15.2f} {chi2_opt/chi2_newton:>14.2f}×")
    print("="*80)
    print()

    if chi2_opt < chi2_newton:
        print("🎉 SUCCÈS! L'ancrage par bulbes BAT NEWTON!")
        print(f"   Amélioration: {(1-chi2_opt/chi2_newton)*100:.1f}%")
        print(f"   d_eff: {d_min_opt:.1f} kpc (halo) → {d_max_opt:.1f} kpc (bulbe)")
        print(f"   Couplage: α = {alpha_opt:.2f}")
    elif chi2_opt < 1.2 * chi2_newton:
        print("⚠️  Très proche de Newton!")
        print(f"   L'ancrage contribue significativement")
        print(f"   d_eff: {d_min_opt:.1f} → {d_max_opt:.1f} kpc, α={alpha_opt:.2f}")
    else:
        print("⚠️  χ² > Newton")
        print(f"   Ratio: {chi2_opt/chi2_newton:.2f}×")

    print()
    print("="*80 + "\n")

    return {
        'chi2_newton': chi2_newton,
        'chi2_opt': chi2_opt,
        'params': (d_min_opt, d_max_opt, alpha_opt)
    }

if __name__ == "__main__":
    test_ancrage_rapide()
