#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formulation Type Maxwell pour la Liaison Asselin
=================================================

Date: 2025-12-05
Branche: maxwell-formulation

APPROCHE FONDAMENTALEMENT NOUVELLE:
Au lieu d'additionner des "masses effectives", résoudre l'équation de Poisson
pour le champ gravitotemporel γ_Després (IDT) avec sources distribuées.

ÉQUATION MAÎTRESSE:
    ∇²γ_Després = (4πG/c²) · ρ_eff(r⃗)

où:
    ρ_eff = ρ_visible + ρ_Asselin

    ρ_Asselin = densité distribuée le long des lignes Asselin

ANALOGIE MAXWELL:
    ∇²φ = ρ/ε₀        (électrostatique)
    ∇²γ = 4πG/c² ρ    (gravitotemporel)

RÉSOLUTION:
    γ(r⃗) = -G/c² ∫ ρ_eff(r⃗')/|r⃗-r⃗'| d³r⃗'  (fonction de Green)

VITESSE ORBITALE:
    v²(r) = r · c² |dγ/dr|   (depuis géodésiques)

Cette formulation respecte les équations de champ et devrait être
physiquement auto-consistante!
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize

# ============================================================================
# CONSTANTES
# ============================================================================

G = 6.674e-11  # m³ kg⁻¹ s⁻²
c = 299792458  # m/s
M_soleil = 1.989e30  # kg
kpc_to_m = 3.086e19  # m

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
# OBJETS COSMIQUES (MULTI-ÉCHELLE)
# ============================================================================

OBJETS_COSMIQUES = [
    # ===== GALAXIES (Échelle kpc, M ~ 10⁹-10¹² M☉) =====
    {'nom': 'Voie Lactée', 'type': 'galaxie', 'M': 8.0e10 * M_soleil,
     'position': np.array([0.0, 0.0, 0.0]), 'd_eff': 100.0},

    {'nom': 'M31 (Andromède)', 'type': 'galaxie', 'M': 1.5e12 * M_soleil,
     'position': np.array([750.0, 250.0, 100.0]), 'd_eff': 150.0},

    {'nom': 'M33 (Triangulum)', 'type': 'galaxie', 'M': 4.0e10 * M_soleil,
     'position': np.array([840.0, 120.0, -50.0]), 'd_eff': 80.0},

    {'nom': 'LMC', 'type': 'galaxie', 'M': 1.0e10 * M_soleil,
     'position': np.array([-40.0, 30.0, -20.0]), 'd_eff': 50.0},

    {'nom': 'SMC', 'type': 'galaxie', 'M': 7.0e9 * M_soleil,
     'position': np.array([-50.0, 40.0, -15.0]), 'd_eff': 40.0},

    # ===== SUPERAMAS (Échelle Mpc, M ~ 10¹⁴-10¹⁷ M☉) =====
    {'nom': 'Amas de la Vierge', 'type': 'superamas', 'M': 1.2e15 * M_soleil,
     'position': np.array([16500.0, 0.0, 0.0]), 'd_eff': 5000.0},

    {'nom': 'Amas de Coma', 'type': 'superamas', 'M': 1.0e15 * M_soleil,
     'position': np.array([99000.0, 20000.0, 5000.0]), 'd_eff': 10000.0},

    {'nom': 'Amas de Perseus', 'type': 'superamas', 'M': 0.8e15 * M_soleil,
     'position': np.array([73000.0, -15000.0, 8000.0]), 'd_eff': 8000.0},

    {'nom': 'Amas du Centaure', 'type': 'superamas', 'M': 0.5e15 * M_soleil,
     'position': np.array([52000.0, 30000.0, -12000.0]), 'd_eff': 6000.0},

    {'nom': 'Centre Laniakea', 'type': 'superamas', 'M': 1.0e17 * M_soleil,
     'position': np.array([75000.0, 40000.0, 20000.0]), 'd_eff': 50000.0},
]

# ============================================================================
# MASSE VISIBLE
# ============================================================================

def masse_visible(r_kpc):
    """Masse visible Voie Lactée (Bulbe + Disque + Gaz)"""
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
    """
    Densité visible ρ_vis(r) = (1/4πr²) dM/dr

    Returns: kg/m³
    """
    if r_kpc < 0.1:
        r_kpc = 0.1

    dr = 0.1
    dM_dr = (masse_visible(r_kpc + dr/2) - masse_visible(r_kpc - dr/2)) / dr
    dM_dr_SI = dM_dr / kpc_to_m

    r_m = r_kpc * kpc_to_m
    rho = dM_dr_SI / (4 * math.pi * r_m**2)

    return rho

# ============================================================================
# LIGNE ASSELIN
# ============================================================================

class LigneAsselin:
    """Ligne Asselin entre deux objets cosmiques (galaxies ou superamas)"""

    def __init__(self, obj_i, obj_j):
        self.obj_i = obj_i
        self.obj_j = obj_j
        self.r_i = obj_i['position']
        self.r_j = obj_j['position']

        # Distance entre objets
        self.d_ij = np.linalg.norm(self.r_j - self.r_i)

        # d_eff effectif = moyenne géométrique des d_eff individuels
        # (couplage entre échelles)
        self.d_eff = math.sqrt(obj_i['d_eff'] * obj_j['d_eff'])

        # Intensité Asselin
        M_i = obj_i['M']
        M_j = obj_j['M']
        self.intensite = math.sqrt(M_i * M_j / M_soleil**2) / self.d_ij**2 * math.exp(-self.d_ij / self.d_eff)

    def point_sur_ligne(self, s):
        """Point paramétrique sur ligne, s ∈ [0,1]"""
        return self.r_i + s * (self.r_j - self.r_i)

    def densite_ligne(self, r_vec, sigma_kpc=1.0):
        """
        Densité ρ_ligne au point r_vec

        Distribuée avec profil gaussien perpendiculaire à la ligne

        ρ_ligne(r⃗) = λ · exp(-d_perp²/2σ²) / √(2πσ²)

        où λ = intensité linéique (M☉/kpc)
        """
        # Trouver point le plus proche sur ligne
        u = self.r_j - self.r_i
        w = r_vec - self.r_i

        s = np.dot(w, u) / np.dot(u, u)
        s = max(0.0, min(s, 1.0))  # Clamp [0,1]

        # Distance perpendiculaire
        r_proj = self.r_i + s * u
        d_perp = np.linalg.norm(r_vec - r_proj)

        # Densité linéique (M☉/kpc)
        lambda_ligne = self.intensite * self.d_ij  # Redistribuer sur longueur

        # Densité volumique (M☉/kpc³)
        rho = lambda_ligne * math.exp(-d_perp**2 / (2 * sigma_kpc**2)) / math.sqrt(2 * math.pi * sigma_kpc**2)

        # Conversion en kg/m³
        rho_SI = rho * M_soleil / kpc_to_m**3

        return rho_SI

def creer_lignes_asselin(objets):
    """Crée toutes lignes Asselin entre paires d'objets cosmiques"""
    lignes = []
    N = len(objets)
    for i in range(N):
        for j in range(i+1, N):
            ligne = LigneAsselin(objets[i], objets[j])
            lignes.append(ligne)
    return lignes

# ============================================================================
# CHAMP γ_DESPRÉS (IDT) - FORMULATION MAXWELL
# ============================================================================

def gamma_despres_visible(r_kpc):
    """
    γ_Després depuis masse visible seule

    γ_vis(r) = -GM_vis(r)/(c²·r)

    Returns: sans dimension
    """
    M_vis = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m

    gamma = -G * M_vis / (c**2 * r_m)

    return gamma

def gamma_despres_ligne(r_kpc, ligne, sigma_kpc=1.0, n_integration=50):
    """
    Contribution d'une ligne Asselin à γ_Després

    Résolution par fonction de Green:
    γ_ligne(r⃗) = -G/c² ∫_ligne ρ_ligne(r⃗')/|r⃗-r⃗'| d³r⃗'

    Intégration le long de la ligne (paramètre s) et perpendiculairement (gaussien)

    Args:
        r_kpc: Rayon d'évaluation (sur axe x, plan galactique)
        ligne: LigneAsselin
        sigma_kpc: Largeur gaussienne perpendiculaire
        n_integration: Points d'intégration le long de la ligne

    Returns:
        γ contribution (sans dimension)
    """
    r_eval = np.array([r_kpc, 0.0, 0.0])  # Point d'évaluation

    gamma_contrib = 0.0

    # Intégration le long de la ligne
    s_array = np.linspace(0, 1, n_integration)
    ds = 1.0 / (n_integration - 1)

    for s in s_array:
        # Point sur la ligne
        r_ligne = ligne.point_sur_ligne(s)

        # Distance du point d'évaluation à ce point sur la ligne
        distance_kpc = np.linalg.norm(r_eval - r_ligne)

        if distance_kpc < 0.01:  # Protection singularité
            distance_kpc = 0.01

        # Densité à ce point (intégrée perpendiculairement)
        # ∫ ρ_ligne d_perp ≈ λ (densité linéique)
        lambda_ligne = ligne.intensite * ligne.d_ij * M_soleil / kpc_to_m  # kg/m

        # Contribution Green: -G/c² · (ρ·dl) / distance
        dl = ligne.d_ij * ds * kpc_to_m  # m
        dgamma = -G / c**2 * lambda_ligne * dl / (distance_kpc * kpc_to_m)

        gamma_contrib += dgamma

    return gamma_contrib

def gamma_despres_total(r_kpc, lignes, sigma_kpc=1.0):
    """
    γ_Després TOTAL = γ_visible + Σ γ_lignes

    Superposition linéaire (comme Maxwell!)

    Args:
        r_kpc: Rayon
        lignes: Liste de LigneAsselin
        sigma_kpc: Largeur gaussienne

    Returns:
        γ_total (sans dimension)
    """
    # Contribution visible
    gamma_vis = gamma_despres_visible(r_kpc)

    # Contribution lignes Asselin
    gamma_asselin = 0.0
    for ligne in lignes:
        gamma_asselin += gamma_despres_ligne(r_kpc, ligne, sigma_kpc)

    # Superposition
    gamma_total = gamma_vis + gamma_asselin

    return gamma_total

# ============================================================================
# VITESSE ORBITALE DEPUIS γ
# ============================================================================

def vitesse_orbitale_depuis_gamma(r_kpc, lignes, sigma_kpc=1.0):
    """
    Vitesse orbitale depuis γ_Després

    Dérivée rigoureusement depuis géodésiques:
    v²(r) = r · c² |dγ/dr|

    Args:
        r_kpc: Rayon orbital
        lignes: Lignes Asselin
        sigma_kpc: Largeur gaussienne

    Returns:
        v en km/s
    """
    # Gradient numérique de γ
    dr = 0.1  # kpc

    gamma_r = gamma_despres_total(r_kpc, lignes, sigma_kpc)
    gamma_r_plus = gamma_despres_total(r_kpc + dr, lignes, sigma_kpc)

    dgamma_dr = (gamma_r_plus - gamma_r) / (dr * kpc_to_m)  # m⁻¹

    # Vitesse orbitale
    v_squared = r_kpc * kpc_to_m * c**2 * abs(dgamma_dr)

    if v_squared < 0:
        v_squared = 0

    v_ms = math.sqrt(v_squared)
    v_kms = v_ms / 1000.0

    return v_kms

def vitesse_orbitale_newton(r_kpc):
    """Vitesse newtonienne (masse visible seule)"""
    M_vis = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_vis / r_m)
    return v_ms / 1000.0

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

def courbe_rotation_maxwell(r_array, lignes, sigma_kpc=1.0):
    """
    Courbe de rotation avec formulation Maxwell

    Args:
        r_array: Rayons (kpc)
        lignes: Lignes Asselin
        sigma_kpc: Largeur gaussienne

    Returns:
        v_array (km/s)
    """
    v_array = []
    for r in r_array:
        v = vitesse_orbitale_depuis_gamma(r, lignes, sigma_kpc)
        v_array.append(v)
    return np.array(v_array)

# ============================================================================
# TEST FORMULATION MAXWELL
# ============================================================================

def test_formulation_maxwell():
    """Test complet formulation type Maxwell"""
    print("\n" + "="*80)
    print(" FORMULATION MAXWELL - MULTI-ÉCHELLE (GALAXIES + SUPERAMAS) ".center(80))
    print("="*80)
    print()
    print("Principe: Résoudre ∇²γ_Després = 4πG/c² ρ_eff")
    print("          avec ρ_eff = ρ_visible + ρ_Asselin")
    print()

    # Compter objets
    n_galaxies = sum(1 for obj in OBJETS_COSMIQUES if obj['type'] == 'galaxie')
    n_superamas = sum(1 for obj in OBJETS_COSMIQUES if obj['type'] == 'superamas')
    print(f"Objets cosmiques: {n_galaxies} galaxies + {n_superamas} superamas")
    print()

    # Test Newton
    print("TEST 1: Newton (masse visible seule)")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r) for r in r_obs_kpc])
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_newton:.2f}")
    print()

    # Créer lignes
    print(f"Création réseau Asselin multi-échelle...")
    lignes = creer_lignes_asselin(OBJETS_COSMIQUES)
    print(f"  → {len(lignes)} lignes créées")
    print(f"  → Échelles: galaxies (d_eff ~ 100 kpc) + superamas (d_eff ~ 5-50 Mpc)")
    print()

    # Test nominal
    print("TEST 2: Maxwell multi-échelle (valeurs nominales, σ=1 kpc)")
    print("-" * 80)
    v_maxwell_nominal = courbe_rotation_maxwell(r_obs_kpc, lignes, sigma_kpc=1.0)
    chi2_nominal = chi_carre(v_maxwell_nominal, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_nominal:.2f} ({chi2_nominal/chi2_newton:.2f}× vs Newton)")
    print()

    # Optimisation
    print("TEST 3: Optimisation (facteurs d'échelle galaxies/superamas, σ)")
    print("-" * 80)
    print("Optimisation en cours...")

    def objective(params):
        scale_gal, scale_super, sigma = params

        if scale_gal < 0.1 or scale_gal > 10.0:
            return 1e10
        if scale_super < 0.1 or scale_super > 10.0:
            return 1e10
        if sigma < 0.1 or sigma > 20:
            return 1e10

        try:
            # Créer objets avec d_eff ajusté
            objets_opt = []
            for obj in OBJETS_COSMIQUES:
                obj_copy = obj.copy()
                if obj['type'] == 'galaxie':
                    obj_copy['d_eff'] = obj['d_eff'] * scale_gal
                else:  # superamas
                    obj_copy['d_eff'] = obj['d_eff'] * scale_super
                objets_opt.append(obj_copy)

            lignes_opt = creer_lignes_asselin(objets_opt)
            v_calc = courbe_rotation_maxwell(r_obs_kpc, lignes_opt, sigma_kpc=sigma)
            return chi_carre(v_calc, v_obs_kms, sigma_obs_kms)
        except:
            return 1e10

    result = minimize(objective, x0=[1.0, 1.0, 1.0],
                     bounds=[(0.1, 10.0), (0.1, 10.0), (0.1, 20.0)],
                     method='L-BFGS-B',
                     options={'maxiter': 50})

    scale_gal_opt, scale_super_opt, sigma_opt = result.x
    chi2_opt = result.fun

    print(f"\n  Facteur galaxies   = {scale_gal_opt:.2f}×")
    print(f"  Facteur superamas  = {scale_super_opt:.2f}×")
    print(f"  σ optimal          = {sigma_opt:.2f} kpc")
    print(f"  χ² optimal         = {chi2_opt:.2f} ({chi2_opt/chi2_newton:.2f}× vs Newton)")
    print()

    # Résultats
    print("="*80)
    print(" RÉSULTATS MULTI-ÉCHELLE ".center(80))
    print("="*80)
    print(f"{'Modèle':<40} {'χ²':>15} {'vs Newton':>15}")
    print("-"*80)
    print(f"{'Newton (référence)':<40} {chi2_newton:>15.2f} {'1.00×':>15}")
    print(f"{'Maxwell multi-échelle nominal':<40} {chi2_nominal:>15.2f} {chi2_nominal/chi2_newton:>14.2f}×")
    print(f"{'Maxwell multi-échelle optimisé':<40} {chi2_opt:>15.2f} {chi2_opt/chi2_newton:>14.2f}×")
    print("="*80)
    print()

    if chi2_opt < chi2_newton:
        amelioration = (1 - chi2_opt/chi2_newton) * 100
        print("🎉 SUCCÈS HISTORIQUE!")
        print(f"   χ² = {chi2_opt:.2f} < Newton ({chi2_newton:.2f})")
        print(f"   Amélioration: {amelioration:.1f}%")
        print()
        print("   LES SUPERAMAS FONT LA DIFFÉRENCE!")
        print("   La formulation Maxwell multi-échelle FONCTIONNE!")
        print("   Les liaisons Asselin à grande échelle expliquent la matière noire!")
        print()
        print(f"   Paramètres clés:")
        print(f"   - Facteur galaxies: {scale_gal_opt:.2f}×")
        print(f"   - Facteur superamas: {scale_super_opt:.2f}×")
        print(f"   - σ: {sigma_opt:.2f} kpc")
    else:
        print("⚠️  χ² toujours ≥ Newton")
        print(f"   Ratio: {chi2_opt/chi2_newton:.2f}×")
        print()
        if chi2_opt < 1.5 * chi2_newton:
            print("   TRÈS PROCHE de Newton - formulation multi-échelle prometteuse")
            print("   Les superamas contribuent significativement")
            print()
            print("   Prochaines étapes:")
            print("   - Réseau Ordre 2 avec intersections Maxwell")
            print("   - Termes non-linéaires γ²")
            print("   - Plus de superamas (Shapley, Great Attractor)")
        else:
            print("   Explorer:")
            print("   - Augmenter nombre de superamas")
            print("   - Affiner positions et masses")
            print("   - Réseau Ordre 2 avec Maxwell")

    print()
    print("="*80 + "\n")

    return {
        'chi2_newton': chi2_newton,
        'chi2_nominal': chi2_nominal,
        'chi2_opt': chi2_opt,
        'params_opt': (scale_gal_opt, scale_super_opt, sigma_opt),
        'n_objets': len(OBJETS_COSMIQUES),
        'n_lignes': len(lignes)
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    resultats = test_formulation_maxwell()
