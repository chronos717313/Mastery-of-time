#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REFORMULATION RÉSEAU ASSELIN depuis Relativité Générale

PROBLÈME ACTUEL:
- Formule ad-hoc: L = √(M_i·M_j)/d² · exp(-d/d_eff)
- Intensités incontrôlées (M31: 10⁹, détruit le fit)
- Pas de normalisation naturelle

NOUVELLE APPROCHE GR:
Dériver le réseau Asselin depuis le couplage de marée gravitationnelle
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
# THÉORIE: COUPLAGE DE MARÉE GRAVITATIONNEL
# ============================================================================
"""
DÉRIVATION depuis GR:

1. Tenseur de marée (équation géodésique):
   K_ij = -∇_i∇_j Φ

   Pour deux masses M_i, M_j séparées par d:
   K_ij ∝ (GM_i/r_i²) · (GM_j/r_j²)

2. Énergie de couplage de marée:
   E_tidal = -∫ K_ij dx

   Donne contribution à ρ_eff:
   ρ_Asselin(r) ∝ (GM_i GM_j)/(c² d³) · f(|r-r_ligne|)

   où f(x) est fonction de forme (exponentielle ou gaussienne)

3. Normalisation naturelle:
   Le préfacteur (GM_i GM_j)/(c² d³) a dimensions [densité]
   C'est la DENSITÉ EFFECTIVE de couplage

4. Fonction de forme:
   f(x) = exp(-x²/λ²) / (λ³ √π³)

   Normalisée: ∫ f(x) d³x = 1

5. Paramètre d'échelle λ:
   λ ~ √(d · d_eff)

   - Géométrique: dépend de la séparation ET de l'échelle caractéristique
   - Limite correcte: λ → 0 quand d → 0 (pas de divergence!)
"""

# ============================================================================
# FORMULATION GR DU RÉSEAU ASSELIN
# ============================================================================

class LigneAsselinGR:
    """
    Ligne Asselin avec formulation GR rigoureuse

    Densité effective de couplage de marée:
    ρ_Asselin(r) = α · (GM_i GM_j)/(c² d³) · exp(-|r-r_centre|²/λ²) / (λ³ π^(3/2))

    où:
    - α: paramètre sans dimension (ordre 1)
    - λ = √(d · d_eff): échelle spatiale du couplage
    - Normalisation garantit ∫ ρ d³r ~ GM_i GM_j / (c² d³)
    """

    def __init__(self, i, j, M_i, M_j, r_i, r_j, d_eff_kpc, alpha=1.0):
        self.i = i
        self.j = j
        self.M_i = M_i  # kg
        self.M_j = M_j  # kg
        self.r_i = r_i  # kpc
        self.r_j = r_j  # kpc
        self.d_eff_kpc = d_eff_kpc
        self.alpha = alpha  # paramètre sans dimension

        # Distance entre masses
        self.d_ij_kpc = np.linalg.norm(r_j - r_i)

        if self.d_ij_kpc < 0.1:
            self.d_ij_kpc = 0.1  # régularisation

        # Échelle spatiale couplage: λ = √(d · d_eff)
        self.lambda_kpc = math.sqrt(self.d_ij_kpc * d_eff_kpc)

        # Centre et direction ligne
        self.r_centre = 0.5 * (r_i + r_j)
        self.direction = (r_j - r_i) / self.d_ij_kpc

        # Préfacteur densité (normalisation GR)
        # ρ_0 = α · (G M_i M_j) / (c² d³)
        d_ij_m = self.d_ij_kpc * kpc_to_m
        self.rho_0 = (alpha * G * M_i * M_j) / (c**2 * d_ij_m**3)

        # Normalisation gaussienne
        lambda_m = self.lambda_kpc * kpc_to_m
        self.norm_gauss = 1.0 / (lambda_m**3 * math.pi**(3.0/2.0))

        # Intensité caractéristique (pour comparaison)
        self.intensite = self.rho_0 * self.norm_gauss * lambda_m**3

    def densite_asselin(self, r_kpc):
        """
        Densité effective Asselin en un point r

        ρ(r) = ρ_0 · exp(-|r-r_centre|²/λ²) / (λ³ π^(3/2))
        """
        r_vec = np.array([r_kpc, 0.0, 0.0])
        dr = r_vec - self.r_centre
        distance_kpc = np.linalg.norm(dr)

        # Gaussienne normalisée
        x2 = (distance_kpc / self.lambda_kpc)**2
        gauss = math.exp(-x2)

        # Densité
        rho = self.rho_0 * self.norm_gauss * gauss

        return rho

def gamma_despres_ligne_gr(r_kpc, ligne):
    """
    Contribution γ d'une ligne Asselin (formulation GR)

    On résout ∇²γ = (4πG/c²) ρ_Asselin

    Pour une distribution gaussienne:
    γ(r) = -(G M_eff)/(c² |r-r_centre|) · erf(|r-r_centre|/λ)

    où M_eff = ∫ ρ_Asselin d³r
    """
    r_vec = np.array([r_kpc, 0.0, 0.0])
    dr = r_vec - ligne.r_centre
    distance_kpc = np.linalg.norm(dr)

    if distance_kpc < 0.01:
        distance_kpc = 0.01  # régularisation

    # Masse effective de la ligne
    # M_eff ~ (G M_i M_j) / (c² d³) · λ³ = (G M_i M_j) / (c² d^(3/2) d_eff^(1/2))
    d_m = ligne.d_ij_kpc * kpc_to_m
    lambda_m = ligne.lambda_kpc * kpc_to_m

    M_eff = (ligne.alpha * G * ligne.M_i * ligne.M_j) / (c**2 * d_m**3) * lambda_m**3

    # Potentiel γ avec fonction erreur (solution exacte gaussienne)
    distance_m = distance_kpc * kpc_to_m
    x = distance_m / lambda_m

    # erf(x) ≈ 1 pour x >> 1, erf(x) ≈ 2x/√π pour x << 1
    if x > 3.0:
        erf_x = 1.0
    elif x < 0.1:
        erf_x = (2.0 / math.sqrt(math.pi)) * x
    else:
        erf_x = math.erf(x)

    gamma = -(G * M_eff) / (c**2 * distance_m) * erf_x

    return gamma

# ============================================================================
# DONNÉES GALAXIES (M31 comme test)
# ============================================================================

M31_r_obs = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 35])
M31_v_obs = np.array([120, 180, 210, 225, 235, 240, 245, 250, 255, 260, 258, 255, 252, 250, 248, 245, 240])
M31_sigma = np.array([15.0] * len(M31_v_obs))

M31_M_bulbe = 3.0e10 * M_soleil
M31_a_bulbe = 1.0
M31_M_disque = 1.2e11 * M_soleil
M31_R_d = 5.5
M31_M_gaz = 1.5e10 * M_soleil
M31_R_gaz = 12.0

# Réseau M31
GALAXIES_M31_GR = [
    {'nom': 'M31', 'M': 1.5e12 * M_soleil, 'position': np.array([0.0, 0.0, 0.0])},
    {'nom': 'Voie Lactée', 'M': 8.0e10 * M_soleil, 'position': np.array([-750.0, -250.0, -100.0])},
    {'nom': 'M33', 'M': 4.0e10 * M_soleil, 'position': np.array([90.0, -130.0, -150.0])},
    {'nom': 'M32', 'M': 3.0e9 * M_soleil, 'position': np.array([5.0, 3.0, 0.0])},
    {'nom': 'NGC 205', 'M': 4.0e9 * M_soleil, 'position': np.array([-8.0, 5.0, 2.0])},
]

# ============================================================================
# MASSE ET VITESSES
# ============================================================================

def masse_bulbe_spherique(r_kpc, M_bulbe, a):
    return M_bulbe * r_kpc**2 / (r_kpc + a)**2

def masse_disque(r_kpc, M_disque, R_d):
    return M_disque * (1.0 - np.exp(-r_kpc/R_d) * (1.0 + r_kpc/R_d))

def masse_gaz(r_kpc, M_gaz, R_g):
    return M_gaz * (1.0 - np.exp(-r_kpc/R_g) * (1.0 + r_kpc/R_g))

def masse_visible_m31(r_kpc):
    return (masse_bulbe_spherique(r_kpc, M31_M_bulbe, M31_a_bulbe) +
            masse_disque(r_kpc, M31_M_disque, M31_R_d) +
            masse_gaz(r_kpc, M31_M_gaz, M31_R_gaz))

def masse_bulbe_aligne(r_kpc, theta, beta, M_bulbe, a):
    M_sph = masse_bulbe_spherique(r_kpc, M_bulbe, a)
    return M_sph * (1.0 + beta * math.cos(theta)**2)

def gamma_despres_total_gr(r_kpc, lignes_gr, beta):
    """γ total avec alignement + formulation GR du réseau"""
    r_m = r_kpc * kpc_to_m

    # Alignement simplifié (θ ≈ 45°)
    theta = math.pi / 4.0
    M_bulbe_align = masse_bulbe_aligne(r_kpc, theta, beta, M31_M_bulbe, M31_a_bulbe)
    M_disque_val = masse_disque(r_kpc, M31_M_disque, M31_R_d)
    M_gaz_val = masse_gaz(r_kpc, M31_M_gaz, M31_R_gaz)
    M_vis = M_bulbe_align + M_disque_val + M_gaz_val

    # γ visible
    gamma_vis = -G * M_vis / (c**2 * r_m)

    # γ réseau GR
    gamma_reseau = sum(gamma_despres_ligne_gr(r_kpc, ligne) for ligne in lignes_gr)

    return gamma_vis + gamma_reseau

def vitesse_orbitale_gr(r_kpc, lignes_gr, beta):
    """Vitesse orbitale v²(r) = r·c²|dγ/dr|"""
    if r_kpc < 0.5:
        r_kpc = 0.5

    dr = 0.01
    gamma_plus = gamma_despres_total_gr(r_kpc + dr, lignes_gr, beta)
    gamma_moins = gamma_despres_total_gr(r_kpc - dr, lignes_gr, beta)

    dgamma_dr = (gamma_plus - gamma_moins) / (2.0 * dr)
    dgamma_dr_m = dgamma_dr / kpc_to_m

    v2 = r_kpc * kpc_to_m * c**2 * abs(dgamma_dr_m)

    if v2 > 0:
        return math.sqrt(v2) / 1000.0
    return 0.0

# ============================================================================
# CHI-CARRÉ
# ============================================================================

def chi2_gr(r_obs, v_obs, sigma, lignes_gr, beta):
    """Chi² formulation GR"""
    chi2 = 0.0
    for r, v_o, sig in zip(r_obs, v_obs, sigma):
        v_t = vitesse_orbitale_gr(r, lignes_gr, beta)
        chi2 += ((v_o - v_t) / sig)**2
    return chi2

def chi2_newton_m31():
    """Chi² Newton M31"""
    chi2 = 0.0
    for r, v_o, sig in zip(M31_r_obs, M31_v_obs, M31_sigma):
        M_vis = masse_visible_m31(r)
        v_n = math.sqrt(G * M_vis / (r * kpc_to_m)) / 1000.0
        chi2 += ((v_o - v_n) / sig)**2
    return chi2

# ============================================================================
# TEST M31 avec FORMULATION GR
# ============================================================================

def test_m31_formulation_gr():
    """Test M31 avec nouvelle formulation GR du réseau Asselin"""

    print("="*80)
    print("  TEST M31: FORMULATION GR DU RÉSEAU ASSELIN")
    print("="*80)
    print()
    print("NOUVELLE APPROCHE:")
    print("  - Dérivée du tenseur de marée gravitationnel")
    print("  - Normalisation naturelle depuis GR")
    print("  - ρ_Asselin = (GM_i GM_j)/(c² d³) · gaussienne")
    print("  - λ = √(d · d_eff): régularisation automatique")
    print()

    # Newton
    chi2_n = chi2_newton_m31()
    print(f"χ² Newton: {chi2_n:.2f}")
    print()

    # Test plusieurs valeurs de d_eff et α
    print("CALIBRATION d_eff et α:")
    print()

    resultats = []

    for d_eff in [100, 500, 1000, 5000]:
        for alpha in [0.01, 0.1, 1.0, 10.0]:
            # Créer réseau GR
            lignes_gr = []
            for i, gal_i in enumerate(GALAXIES_M31_GR):
                for j, gal_j in enumerate(GALAXIES_M31_GR):
                    if i < j:
                        ligne = LigneAsselinGR(
                            i, j,
                            gal_i['M'], gal_j['M'],
                            gal_i['position'], gal_j['position'],
                            d_eff, alpha
                        )
                        lignes_gr.append(ligne)

            # Optimiser β
            def objectif(beta):
                return chi2_gr(M31_r_obs, M31_v_obs, M31_sigma, lignes_gr, beta)

            result = minimize_scalar(objectif, bounds=(0.0, 5.0), method='bounded')
            beta_opt = result.x
            chi2_opt = result.fun

            ratio = chi2_opt / chi2_n

            resultats.append({
                'd_eff': d_eff,
                'alpha': alpha,
                'beta': beta_opt,
                'chi2': chi2_opt,
                'ratio': ratio
            })

            print(f"  d_eff={d_eff:>5} kpc, α={alpha:>5.2f}: β={beta_opt:.2f}, χ²={chi2_opt:>8.1f} ({ratio:.3f}×)")

    # Meilleur résultat
    print()
    print("="*80)
    print("MEILLEUR RÉSULTAT:")
    print("="*80)

    meilleur = min(resultats, key=lambda x: x['chi2'])

    print(f"d_eff = {meilleur['d_eff']} kpc")
    print(f"α = {meilleur['alpha']}")
    print(f"β = {meilleur['beta']:.2f}")
    print(f"χ² = {meilleur['chi2']:.2f} ({meilleur['ratio']:.3f}× Newton)")
    print()

    if meilleur['ratio'] < 1.0:
        amelioration = (1.0 - meilleur['ratio']) * 100.0
        print(f"✅ SUCCÈS! Amélioration: {amelioration:.1f}%")
    else:
        degradation = (meilleur['ratio'] - 1.0) * 100.0
        print(f"❌ Échec. Dégradation: {degradation:.1f}%")

    print()
    print("COMPARAISON:")
    print(f"  Newton:              χ² = {chi2_n:.2f}")
    print(f"  Alignement seul:     χ² = 390 (0.907× Newton)")
    print(f"  Ancien Maxwell:      χ² = 348,958 (811× Newton)")
    print(f"  Nouveau GR:          χ² = {meilleur['chi2']:.2f} ({meilleur['ratio']:.3f}× Newton)")
    print()

    return meilleur

if __name__ == "__main__":
    test_m31_formulation_gr()
