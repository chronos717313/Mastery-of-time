#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOIE 2 : Réseau de Lignes Asselin
==================================

Date: 2025-12-05
Objectif: Tester l'hypothèse du réseau géométrique 3D avec intersections

Concept:
- Chaque paire de galaxies (i,j) crée une ligne Asselin L_ij
- Les lignes s'intersectent (ou quasi-intersectent) dans l'espace 3D
- Aux intersections: RENFORCEMENT NON-LINÉAIRE
- Structure émerge de la géométrie

Formulation:
    L_ij(s) = r⃗_i + s(r⃗_j - r⃗_i),  s ∈ [0,1]
    Intensité: I_ij = √(M_i·M_j) / d²_ij · exp(-d_ij/d_eff)

    Potentiel au point P:
    Φ_réseau(P) = -G Σ_lignes w(d_ligne) · I_ligne

    où d_ligne = distance de P à la ligne L_ij
    w(d) = exp(-d²/σ²) (poids gaussien)

Prédiction: Si correct, χ² << Newton avec effets géométriques
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
# GALAXIES DU GROUPE LOCAL
# ============================================================================

# Position de la Voie Lactée au centre du référentiel
# Coordonnées en kpc: (x, y, z)

GALAXIES_GROUPE_LOCAL = [
    {
        'nom': 'Voie Lactée',
        'M': 8.0e10 * M_soleil,
        'position': np.array([0.0, 0.0, 0.0])  # Centre du référentiel
    },
    {
        'nom': 'M31 (Andromède)',
        'M': 1.5e12 * M_soleil,
        'position': np.array([750.0, 250.0, 100.0])  # ~780 kpc
    },
    {
        'nom': 'M33 (Triangulum)',
        'M': 4.0e10 * M_soleil,
        'position': np.array([840.0, 120.0, -50.0])  # ~850 kpc
    },
    {
        'nom': 'Grand Nuage Magellan (LMC)',
        'M': 1.0e10 * M_soleil,
        'position': np.array([-40.0, 30.0, -20.0])  # ~50 kpc
    },
    {
        'nom': 'Petit Nuage Magellan (SMC)',
        'M': 7.0e9 * M_soleil,
        'position': np.array([-50.0, 40.0, -15.0])  # ~63 kpc
    },
    {
        'nom': 'Naine du Sagittaire',
        'M': 4.0e8 * M_soleil,
        'position': np.array([20.0, -15.0, 10.0])  # ~26 kpc
    },
    {
        'nom': 'Naine du Sculpteur',
        'M': 2.0e8 * M_soleil,
        'position': np.array([70.0, -50.0, 30.0])  # ~86 kpc
    },
    {
        'nom': 'Naine du Fourneau',
        'M': 2.0e8 * M_soleil,
        'position': np.array([-120.0, 80.0, -40.0])  # ~147 kpc
    },
    {
        'nom': 'Naine de la Carène',
        'M': 1.5e8 * M_soleil,
        'position': np.array([60.0, -70.0, 25.0])  # ~94 kpc
    },
    {
        'nom': 'Naine du Dragon',
        'M': 1.0e8 * M_soleil,
        'position': np.array([70.0, 50.0, -40.0])  # ~92 kpc
    }
]

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
# PROFIL DE MASSE VISIBLE - VOIE LACTÉE
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
# LIGNES ASSELIN
# ============================================================================

class LigneAsselin:
    """Représente une ligne Asselin entre deux galaxies"""

    def __init__(self, galaxie_i, galaxie_j, d_eff):
        """
        Args:
            galaxie_i, galaxie_j: Dictionnaires avec 'M' et 'position'
            d_eff: Distance effective (kpc)
        """
        self.i = galaxie_i
        self.j = galaxie_j
        self.r_i = galaxie_i['position']
        self.r_j = galaxie_j['position']

        # Distance entre galaxies
        self.d_ij = np.linalg.norm(self.r_j - self.r_i)

        # Intensité Asselin
        self.intensite = self.calculer_intensite(d_eff)

    def calculer_intensite(self, d_eff):
        """
        Intensité Liaison Asselin

        I_ij = √(M_i·M_j) / d²_ij · exp(-d_ij/d_eff)
        """
        M_i = self.i['M']
        M_j = self.j['M']

        if self.d_ij < 0.1:  # Protection
            self.d_ij = 0.1

        I = math.sqrt(M_i * M_j) / (self.d_ij**2) * math.exp(-self.d_ij / d_eff)
        return I

    def distance_point(self, P):
        """
        Distance d'un point P à la ligne

        Args:
            P: Position 3D (array)

        Returns:
            d: Distance minimale de P à la ligne (kpc)
            s: Paramètre de projection [0,1]
        """
        # Vecteur direction
        u = self.r_j - self.r_i

        # Vecteur vers le point
        w = P - self.r_i

        # Projection
        s = np.dot(w, u) / np.dot(u, u)

        # Clamp à [0,1] (limiter au segment)
        s = max(0.0, min(s, 1.0))

        # Point le plus proche sur la ligne
        P_proj = self.r_i + s * u

        # Distance
        d = np.linalg.norm(P - P_proj)

        return d, s

def creer_reseau_asselin(galaxies, d_eff):
    """
    Crée toutes les lignes Asselin entre paires de galaxies

    Args:
        galaxies: Liste de dictionnaires galaxies
        d_eff: Distance effective (kpc)

    Returns:
        lignes: Liste de LigneAsselin
    """
    lignes = []
    N = len(galaxies)

    for i in range(N):
        for j in range(i+1, N):
            ligne = LigneAsselin(galaxies[i], galaxies[j], d_eff)
            lignes.append(ligne)

    return lignes

# ============================================================================
# POTENTIEL RÉSEAU
# ============================================================================

def potentiel_reseau(P, lignes, sigma=1.0):
    """
    Potentiel au point P depuis le réseau de lignes Asselin

    Φ_réseau(P) = -G Σ_lignes w(d_ligne) · I_ligne

    Args:
        P: Position 3D (kpc)
        lignes: Liste de LigneAsselin
        sigma: Largeur gaussienne (kpc)

    Returns:
        Φ en unités de (G M☉ / kpc)
    """
    Phi = 0.0

    for ligne in lignes:
        # Distance du point à la ligne
        d_ligne, s = ligne.distance_point(P)

        # Poids gaussien
        w = math.exp(-d_ligne**2 / sigma**2)

        # Contribution au potentiel (proportionnel à intensité)
        Phi += w * ligne.intensite

    return Phi  # Unités: M☉ / kpc²

# ============================================================================
# MASSE EFFECTIVE AVEC RÉSEAU
# ============================================================================

def masse_effective_reseau(r_kpc, lignes, sigma, kappa=1e9):
    """
    Masse effective incluant contribution du réseau Asselin

    APPROCHE SIMPLIFIÉE:
    M_eff(r) = M_vis(r) + κ · Σ_lignes w(d_ligne) · √(M_i·M_j)

    où:
    - w(d) = exp(-d²/σ²) : poids gaussien
    - κ : facteur de couplage (M☉ → kg)

    Args:
        r_kpc: Rayon galactique (kpc)
        lignes: Réseau de lignes Asselin
        sigma: Largeur gaussienne (kpc)
        kappa: Facteur de couplage réseau

    Returns:
        M_eff en kg
    """
    M_vis = masse_visible(r_kpc)

    # Point d'évaluation (dans plan galactique z=0)
    P = np.array([r_kpc, 0.0, 0.0])

    # Contribution réseau : somme pondérée des lignes proches
    contribution_reseau = 0.0

    for ligne in lignes:
        # Distance du point à la ligne
        d_ligne, s = ligne.distance_point(P)

        # Poids gaussien
        w = math.exp(-d_ligne**2 / (sigma**2))

        # Contribution: √(M_i·M_j) pondéré par proximité
        M_i = ligne.i['M']
        M_j = ligne.j['M']
        contribution_reseau += w * math.sqrt(M_i * M_j / M_soleil**2)

    # Masse effective totale
    M_reseau = kappa * M_soleil * contribution_reseau  # kg

    M_eff = M_vis + M_reseau

    return M_eff

# ============================================================================
# VITESSE ORBITALE
# ============================================================================

def vitesse_orbitale(r_kpc, M_eff_kg):
    """v = sqrt(GM_eff/r)"""
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_eff_kg / r_m)
    return v_ms / 1000.0

def vitesse_orbitale_newton(r_kpc):
    """Newtonien (masse visible seule)"""
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
# COURBE DE ROTATION AVEC RÉSEAU
# ============================================================================

def courbe_rotation_reseau(r_array, lignes, sigma, kappa=1e9):
    """
    Calcule courbe de rotation avec réseau Asselin

    Args:
        r_array: Rayons (kpc)
        lignes: Réseau de lignes
        sigma: Largeur gaussienne (kpc)
        kappa: Facteur de couplage

    Returns:
        v_array: Vitesses (km/s)
    """
    v_array = []

    for r in r_array:
        M_eff = masse_effective_reseau(r, lignes, sigma, kappa)
        v = vitesse_orbitale(r, M_eff)
        v_array.append(v)

    return np.array(v_array)

# ============================================================================
# TEST RÉSEAU ASSELIN
# ============================================================================

def test_reseau_asselin():
    """
    Test complet Voie 2: Réseau de Lignes Asselin

    Compare:
    1. Newton (référence)
    2. d_eff = 100 kpc, σ = 1 kpc (valeurs nominales)
    3. Optimisation de (d_eff, σ)
    """
    print("=" * 80)
    print(" VOIE 2 : RÉSEAU DE LIGNES ASSELIN ".center(80))
    print("=" * 80)
    print()
    print("Concept: Géométrie 3D avec effets non-linéaires aux intersections")
    print()

    # Afficher galaxies
    print(f"Galaxies du Groupe Local: {len(GALAXIES_GROUPE_LOCAL)}")
    for gal in GALAXIES_GROUPE_LOCAL:
        pos = gal['position']
        d = np.linalg.norm(pos)
        print(f"  - {gal['nom']:<30} M={gal['M']/M_soleil:.2e} M☉, d={d:.1f} kpc")
    print()

    # Nombre de lignes
    N_gal = len(GALAXIES_GROUPE_LOCAL)
    N_lignes = N_gal * (N_gal - 1) // 2
    print(f"Nombre de lignes Asselin: {N_lignes}")
    print()

    # Test 1: Newton
    print("TEST 1: Newton (masse visible seule)")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r) for r in r_obs_kpc])
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_newton:.2f}")
    print()

    # Test 2: Réseau avec paramètres nominaux
    print("TEST 2: Réseau Asselin (d_eff=100 kpc, σ=10 kpc, κ=1e9)")
    print("-" * 80)
    lignes_nominal = creer_reseau_asselin(GALAXIES_GROUPE_LOCAL, d_eff=100.0)
    v_nominal = courbe_rotation_reseau(r_obs_kpc, lignes_nominal, sigma=10.0, kappa=1e9)
    chi2_nominal = chi_carre(v_nominal, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_nominal:.2f} ({chi2_nominal/chi2_newton:.2f}× vs Newton)")
    print()

    # Test 3: Optimisation
    print("TEST 3: Optimisation (d_eff, σ, κ)")
    print("-" * 80)
    print("Optimisation en cours...")
    print()

    def objective(params):
        d_eff, sigma, log_kappa = params
        kappa = 10**log_kappa  # Optimiser en log pour mieux explorer

        if d_eff < 10 or d_eff > 1000:
            return 1e10
        if sigma < 0.1 or sigma > 100:
            return 1e10

        try:
            lignes = creer_reseau_asselin(GALAXIES_GROUPE_LOCAL, d_eff)
            v_calc = courbe_rotation_reseau(r_obs_kpc, lignes, sigma, kappa)
            return chi_carre(v_calc, v_obs_kms, sigma_obs_kms)
        except:
            return 1e10

    result = minimize(objective, x0=[100.0, 10.0, 9.0],  # log_kappa=9 → kappa=1e9
                     bounds=[(10.0, 500.0), (0.1, 50.0), (6.0, 12.0)],
                     method='L-BFGS-B',
                     options={'maxiter': 50})

    d_eff_opt, sigma_opt, log_kappa_opt = result.x
    kappa_opt = 10**log_kappa_opt
    chi2_opt = result.fun

    print(f"  d_eff optimal = {d_eff_opt:.2f} kpc")
    print(f"  σ optimal     = {sigma_opt:.2f} kpc")
    print(f"  κ optimal     = {kappa_opt:.2e}")
    print(f"  χ²            = {chi2_opt:.2f} ({chi2_opt/chi2_newton:.2f}× vs Newton)")
    print()

    # Récapitulatif
    print("=" * 80)
    print(" RÉCAPITULATIF ".center(80))
    print("=" * 80)
    print(f"{'Modèle':<35} {'χ²':>15} {'vs Newton':>15}")
    print("-" * 80)
    print(f"{'Newton (référence)':<35} {chi2_newton:>15.2f} {'1.00×':>15}")
    print(f"{'Réseau nominal (100kpc, 1kpc)':<35} {chi2_nominal:>15.2f} {chi2_nominal/chi2_newton:>14.2f}×")
    print(f"{'Réseau optimisé':<35} {chi2_opt:>15.2f} {chi2_opt/chi2_newton:>14.2f}×")
    print("=" * 80)
    print()

    # Évaluation
    if chi2_opt < chi2_newton:
        amelioration = (1 - chi2_opt/chi2_newton) * 100
        print("✅ SUCCÈS MAJEUR!")
        print(f"   χ² = {chi2_opt:.2f} < Newton ({chi2_newton:.2f})")
        print(f"   Amélioration: {amelioration:.1f}%")
        print()
        print("   LA VOIE 2 FONCTIONNE! 🎉")
        print("   Le réseau géométrique 3D améliore Newton!")
        print()
        print("   PROCHAINES ÉTAPES:")
        print("   1. Combiner avec d_eff(ρ) (Voie 1 + Voie 2)")
        print("   2. Tester sur NGC 3198 et autres galaxies")
        print("   3. Calculer intersections explicites (ordre 2)")
        print("   4. Préparer publication")
    elif chi2_opt < chi2_nominal:
        amelioration = (1 - chi2_opt/chi2_nominal) * 100
        print("⚠️  AMÉLIORATION PARTIELLE")
        print(f"   χ² optimisé ({chi2_opt:.2f}) meilleur que nominal ({chi2_nominal:.2f})")
        print(f"   Amélioration: {amelioration:.1f}%")
        print(f"   Mais toujours > Newton ({chi2_opt/chi2_newton:.2f}×)")
        print()
        print("   INTERPRÉTATION:")
        print("   - Le réseau améliore vs paramètres nominaux")
        print("   - Mais pas suffisant pour battre Newton")
        print("   - Explorer:")
        print("     • Combiner Voie 1 + Voie 2")
        print("     • Ajouter intersections ordre 2")
        print("     • Réviser formulation potentiel")
    else:
        print("❌ PAS D'AMÉLIORATION")
        print(f"   χ² = {chi2_opt:.2f} ≈ nominal ({chi2_nominal:.2f})")
        print()
        print("   INTERPRÉTATION:")
        print("   - Réseau seul ne suffit pas")
        print("   - Combiner avec Voie 1 nécessaire")
        print("   - Ou réviser formulation fondamentale")

    print()

    # Retourner résultats
    lignes_opt = creer_reseau_asselin(GALAXIES_GROUPE_LOCAL, d_eff_opt)
    v_opt = courbe_rotation_reseau(r_obs_kpc, lignes_opt, sigma_opt, kappa_opt)

    return {
        'newton': {'v': v_newton, 'chi2': chi2_newton},
        'nominal': {'v': v_nominal, 'chi2': chi2_nominal},
        'optimized': {'v': v_opt, 'chi2': chi2_opt,
                     'params': (d_eff_opt, sigma_opt, kappa_opt),
                     'lignes': lignes_opt}
    }

# ============================================================================
# GRAPHIQUES
# ============================================================================

def generer_graphiques_reseau(resultats):
    """Génère graphiques pour réseau Asselin"""
    print("Génération des graphiques...")

    d_eff_opt, sigma_opt, kappa_opt = resultats['optimized']['params']
    lignes = resultats['optimized']['lignes']

    plt.figure(figsize=(16, 12))

    # Subplot 1: Courbes de rotation
    plt.subplot(2, 3, 1)
    plt.errorbar(r_obs_kpc, v_obs_kms, yerr=sigma_obs_kms, fmt='o',
                 color='black', label='Observations', alpha=0.7, markersize=4)
    plt.plot(r_obs_kpc, resultats['newton']['v'], 'r--', linewidth=2,
             label=f"Newton (χ²={resultats['newton']['chi2']:.0f})")
    plt.plot(r_obs_kpc, resultats['nominal']['v'], 'b:', linewidth=2,
             label=f"Réseau nominal (χ²={resultats['nominal']['chi2']:.0f})")
    plt.plot(r_obs_kpc, resultats['optimized']['v'], 'g-', linewidth=2.5,
             label=f"Réseau optimisé (χ²={resultats['optimized']['chi2']:.0f})")
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Vitesse (km/s)', fontsize=11)
    plt.title('Courbes de Rotation: Réseau Asselin', fontsize=13, fontweight='bold')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)

    # Subplot 2: Résidus
    plt.subplot(2, 3, 2)
    residus = resultats['optimized']['v'] - v_obs_kms
    plt.plot(r_obs_kpc, residus, 'go-', linewidth=1.5, markersize=4)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Résidus (km/s)', fontsize=11)
    plt.title('Résidus: Réseau Optimisé', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Subplot 3: Réseau 3D (projection XY)
    plt.subplot(2, 3, 3)
    for ligne in lignes[:20]:  # Limiter pour lisibilité
        x = [ligne.r_i[0], ligne.r_j[0]]
        y = [ligne.r_i[1], ligne.r_j[1]]
        alpha = min(1.0, ligne.intensite / max([l.intensite for l in lignes]) * 5)
        plt.plot(x, y, 'b-', alpha=alpha, linewidth=0.5)

    # Galaxies
    for gal in GALAXIES_GROUPE_LOCAL:
        pos = gal['position']
        size = math.log10(gal['M']/M_soleil) * 10
        plt.scatter(pos[0], pos[1], s=size, c='red', alpha=0.7, edgecolors='black')

    plt.xlabel('X (kpc)', fontsize=11)
    plt.ylabel('Y (kpc)', fontsize=11)
    plt.title(f'Réseau Asselin (d_eff={d_eff_opt:.0f} kpc)', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')

    # Subplot 4: Distribution intensités
    plt.subplot(2, 3, 4)
    intensites = [l.intensite for l in lignes]
    plt.hist(intensites, bins=20, color='blue', alpha=0.7, edgecolor='black')
    plt.xlabel('Intensité Asselin', fontsize=11)
    plt.ylabel('Nombre de lignes', fontsize=11)
    plt.title('Distribution des Intensités', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.yscale('log')

    # Subplot 5: Potentiel réseau radial
    plt.subplot(2, 3, 5)
    r_plot = np.linspace(0.5, 150, 100)
    Phi_res = []
    for r in r_plot:
        P = np.array([r, 0.0, 0.0])
        Phi = potentiel_reseau(P, lignes, sigma_opt)
        Phi_res.append(Phi)
    plt.plot(r_plot, Phi_res, 'purple', linewidth=2)
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Φ_réseau (M☉/kpc)', fontsize=11)
    plt.title(f'Potentiel Réseau (σ={sigma_opt:.1f} kpc)', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Subplot 6: Masse effective
    plt.subplot(2, 3, 6)
    M_vis_plot = [masse_visible(r) / M_soleil / 1e10 for r in r_plot]
    M_eff_plot = [masse_effective_reseau(r, lignes, sigma_opt, kappa_opt) / M_soleil / 1e10
                  for r in r_plot]
    plt.plot(r_plot, M_vis_plot, 'r--', linewidth=2, label='M_visible')
    plt.plot(r_plot, M_eff_plot, 'g-', linewidth=2, label='M_eff (réseau)')
    plt.xlabel('Rayon (kpc)', fontsize=11)
    plt.ylabel('Masse (10¹⁰ M☉)', fontsize=11)
    plt.title('Masse Effective avec Réseau', fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)

    plt.tight_layout()
    plt.savefig('voie2_reseau_asselin.png', dpi=300, bbox_inches='tight')
    print("  ✓ Graphique sauvegardé: voie2_reseau_asselin.png")
    print()

# ============================================================================
# PROGRAMME PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print(" VOIE 2 : RÉSEAU DE LIGNES ASSELIN ".center(80))
    print("="*80 + "\n")

    resultats = test_reseau_asselin()
    generer_graphiques_reseau(resultats)

    print("="*80)
    print(" FIN DU TEST ".center(80))
    print("="*80)
    print()
