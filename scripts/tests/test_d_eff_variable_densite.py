#!/usr/bin/env python3
"""
Test de l'Approche : Halo = Limite d'Expansion du Vide
======================================================

Teste la formulation d_eff(ρ) où la distance effective dépend
de la densité locale de matière.

Hypothèse : La matière "ancre" l'espace-temps, freinant l'expansion.
Plus la densité est élevée, plus les liaisons Asselin ont une grande portée.

d_eff(r) = d_min + (d_max - d_min) * [ρ(r) / ρ_0]^alpha

Date : 2025-12-05
Auteur : Claude (assistant IA)
Théorie : Maîtrise du Temps (Després & Asselin)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ==============================================================================
# CONSTANTES PHYSIQUES
# ==============================================================================

G = 6.67430e-11      # m³ kg⁻¹ s⁻²
c = 299792458        # m/s
M_solaire = 1.989e30 # kg
kpc_to_m = 3.086e19  # m

# ==============================================================================
# PROFIL DE MASSE GALACTIQUE
# ==============================================================================

def masse_visible_voie_lactee(r_kpc):
    """
    Profil de masse visible de la Voie Lactée
    Modèle exponentiel + bulbe
    """
    M_totale = 6e10  # M☉ (matière visible)

    # Composante disque (exponentiel)
    r_scale_disk = 3.0  # kpc
    M_disk = 0.7 * M_totale * (1 - np.exp(-r_kpc / r_scale_disk) * (1 + r_kpc / r_scale_disk))

    # Composante bulbe (Hernquist)
    a_bulge = 0.6  # kpc
    M_bulge = 0.3 * M_totale * (r_kpc / (r_kpc + a_bulge))**2

    return M_disk + M_bulge

def densite_voie_lactee(r_kpc):
    """
    Densité de matière à rayon r
    ρ(r) = (1 / 4πr²) dM/dr
    """
    if r_kpc < 0.1:
        r_kpc = 0.1  # Éviter division par zéro

    # Calcul numérique de dM/dr
    dr = 0.01  # kpc
    M_plus = masse_visible_voie_lactee(r_kpc + dr / 2)
    M_moins = masse_visible_voie_lactee(r_kpc - dr / 2)
    dM_dr = (M_plus - M_moins) / dr  # M☉/kpc

    # Conversion en kg/m³
    dM_dr_kg_m = dM_dr * M_solaire / kpc_to_m

    # Densité volumique
    r_m = r_kpc * kpc_to_m
    rho = dM_dr_kg_m / (4 * np.pi * r_m**2)

    return rho  # kg/m³

# ==============================================================================
# DISTANCE EFFECTIVE VARIABLE
# ==============================================================================

def d_eff_fonction_densite(r_kpc, d_min, d_max, alpha, rho_ref=None):
    """
    Distance effective fonction de la densité locale

    Parameters
    ----------
    r_kpc : float
        Rayon galactique (kpc)
    d_min : float
        Distance effective minimale (vide, expansion domine) [kpc]
    d_max : float
        Distance effective maximale (haute densité, ancrage domine) [kpc]
    alpha : float
        Exposant de transition
    rho_ref : float or None
        Densité de référence (kg/m³). Si None, utilise ρ au rayon solaire (8 kpc)

    Returns
    -------
    d_eff : float
        Distance effective à r (kpc)
    """
    # Densité à r
    rho = densite_voie_lactee(r_kpc)

    # Densité de référence
    if rho_ref is None:
        rho_ref = densite_voie_lactee(8.0)  # Position du Soleil

    # Ratio de densité
    ratio = (rho / rho_ref) ** alpha

    # d_eff linéaire en ratio
    d_eff = d_min + (d_max - d_min) * ratio

    # Clamp entre d_min et d_max
    d_eff = np.clip(d_eff, d_min, d_max)

    return d_eff

# ==============================================================================
# MASSE EFFECTIVE AVEC D_EFF VARIABLE
# ==============================================================================

def masse_effective_d_eff_variable(r_kpc, d_min, d_max, alpha):
    """
    Calcul de M_eff avec d_eff fonction de la densité

    Parameters
    ----------
    r_kpc : float
        Rayon d'évaluation (kpc)
    d_min, d_max, alpha : float
        Paramètres du modèle d_eff(ρ)

    Returns
    -------
    M_eff : float
        Masse effective ressentie à r (M☉)
    """
    # Masse visible à r
    M_vis = masse_visible_voie_lactee(r_kpc)

    # Contribution des coquilles via Liaisons Asselin
    M_eff = M_vis

    # Discrétisation en coquilles
    n_shells = 300
    r_shells = np.linspace(0.1, 200, n_shells)  # Jusqu'à 200 kpc

    for r_shell in r_shells:
        # Éviter la coquille contenant le point d'observation
        if abs(r_shell - r_kpc) < 0.5:
            continue

        # Densité à r_shell
        rho_shell = densite_voie_lactee(r_shell)

        # d_eff à r_shell (CLEF : dépend de la densité LOCALE à la source)
        d_eff_local = d_eff_fonction_densite(r_shell, d_min, d_max, alpha)

        # Masse dans la coquille
        dr = r_shells[1] - r_shells[0] if len(r_shells) > 1 else 1.0
        r_m = r_shell * kpc_to_m
        dM_kg = 4 * np.pi * r_m**2 * dr * kpc_to_m * rho_shell
        dM_solaire = dM_kg / M_solaire

        # Distance entre coquille et point d'observation
        distance = abs(r_kpc - r_shell)

        # Facteur d'atténuation Asselin
        f = np.exp(-distance / d_eff_local)

        # Contribution
        M_eff += dM_solaire * f

    return M_eff

# ==============================================================================
# VITESSE DE ROTATION
# ==============================================================================

def vitesse_rotation_d_eff_variable(r_kpc, d_min, d_max, alpha):
    """
    Vitesse de rotation avec d_eff(ρ)

    Returns
    -------
    v : float
        Vitesse orbitale (km/s)
    """
    M_eff = masse_effective_d_eff_variable(r_kpc, d_min, d_max, alpha)

    # Vitesse orbitale v = sqrt(GM/r)
    r_m = r_kpc * kpc_to_m
    v_m_s = np.sqrt(G * M_eff * M_solaire / r_m)
    v_km_s = v_m_s / 1000

    return v_km_s

def vitesse_rotation_newton(r_kpc):
    """
    Vitesse de rotation newtonienne (matière visible seule)
    """
    M_vis = masse_visible_voie_lactee(r_kpc)
    r_m = r_kpc * kpc_to_m
    v_m_s = np.sqrt(G * M_vis * M_solaire / r_m)
    return v_m_s / 1000

# ==============================================================================
# OBSERVATIONS (Voie Lactée)
# ==============================================================================

def donnees_observees():
    """
    Courbe de rotation observée de la Voie Lactée
    Données simplifiées (valeurs typiques)
    """
    r_obs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50])
    v_obs = np.array([50, 100, 150, 180, 200, 210, 215, 220, 220, 220, 220, 220, 215, 210, 200, 190])

    # Incertitudes (~10 km/s typique)
    sigma_obs = np.ones_like(v_obs) * 10

    return r_obs, v_obs, sigma_obs

# ==============================================================================
# CHI-CARRÉ
# ==============================================================================

def chi_squared(params, verbose=False):
    """
    Calcul du χ² entre modèle et observations

    Parameters
    ----------
    params : list
        [d_min, d_max, alpha]

    Returns
    -------
    chi2 : float
        Chi-carré normalisé
    """
    d_min, d_max, alpha = params

    # Contraintes physiques
    if d_min < 1 or d_min > 50:
        return 1e6
    if d_max < d_min or d_max > 500:
        return 1e6
    if alpha < 0 or alpha > 2:
        return 1e6

    r_obs, v_obs, sigma_obs = donnees_observees()

    chi2 = 0
    n_points = len(r_obs)

    for i, r in enumerate(r_obs):
        try:
            v_model = vitesse_rotation_d_eff_variable(r, d_min, d_max, alpha)
            chi2 += ((v_model - v_obs[i]) / sigma_obs[i]) ** 2
        except:
            return 1e6

    chi2_normalized = chi2 / n_points

    if verbose:
        print(f"d_min={d_min:.1f}, d_max={d_max:.1f}, alpha={alpha:.3f} → χ²={chi2_normalized:.3f}")

    return chi2_normalized

# ==============================================================================
# OPTIMISATION
# ==============================================================================

def optimiser_parametres():
    """
    Optimise d_min, d_max, alpha pour minimiser χ²
    """
    print("=" * 70)
    print("OPTIMISATION DES PARAMÈTRES d_eff(ρ)")
    print("=" * 70)
    print()

    # Valeurs initiales
    params_init = [15, 150, 0.4]

    # Bornes
    bounds = [(5, 50), (50, 300), (0.1, 1.5)]

    print("Valeurs initiales :")
    print(f"  d_min  = {params_init[0]:.1f} kpc")
    print(f"  d_max  = {params_init[1]:.1f} kpc")
    print(f"  alpha  = {params_init[2]:.3f}")
    print()
    print("Optimisation en cours...")
    print()

    # Optimisation
    result = minimize(
        chi_squared,
        params_init,
        method='Nelder-Mead',
        bounds=bounds,
        options={'maxiter': 500, 'disp': True}
    )

    d_min_opt, d_max_opt, alpha_opt = result.x
    chi2_opt = result.fun

    print()
    print("=" * 70)
    print("RÉSULTATS DE L'OPTIMISATION")
    print("=" * 70)
    print()
    print(f"  d_min  = {d_min_opt:.2f} kpc")
    print(f"  d_max  = {d_max_opt:.2f} kpc")
    print(f"  alpha  = {alpha_opt:.4f}")
    print()
    print(f"  χ² normalisé = {chi2_opt:.4f}")
    print()

    return d_min_opt, d_max_opt, alpha_opt, chi2_opt

# ==============================================================================
# VISUALISATION
# ==============================================================================

def tracer_resultats(d_min, d_max, alpha):
    """
    Trace la courbe de rotation théorique vs observations
    """
    r_obs, v_obs, sigma_obs = donnees_observees()

    # Calcul théorique
    r_theory = np.linspace(0.5, 50, 100)
    v_theory = [vitesse_rotation_d_eff_variable(r, d_min, d_max, alpha) for r in r_theory]
    v_newton = [vitesse_rotation_newton(r) for r in r_theory]

    # Profil de d_eff
    d_eff_profile = [d_eff_fonction_densite(r, d_min, d_max, alpha) for r in r_theory]

    # Figure
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))

    # --- Panneau 1 : Courbe de rotation ---
    ax1 = axes[0]

    ax1.errorbar(r_obs, v_obs, yerr=sigma_obs, fmt='o', color='black',
                 label='Observations', markersize=6, capsize=3)

    ax1.plot(r_theory, v_newton, '--', color='gray', linewidth=2,
             label='Newton (matière visible)')

    ax1.plot(r_theory, v_theory, '-', color='blue', linewidth=2.5,
             label=f'Maîtrise du Temps (d_eff variable)')

    ax1.set_xlabel('Rayon galactique (kpc)', fontsize=12)
    ax1.set_ylabel('Vitesse de rotation (km/s)', fontsize=12)
    ax1.set_title(f'Courbe de Rotation - Approche d_eff(ρ)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10, loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 50)
    ax1.set_ylim(0, 300)

    # Chi²
    chi2_val = chi_squared([d_min, d_max, alpha])
    chi2_newton = chi_squared_newton()

    ax1.text(0.05, 0.95, f'χ² = {chi2_val:.3f}\nχ²_Newton = {chi2_newton:.1f}',
             transform=ax1.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # --- Panneau 2 : Profil d_eff(r) ---
    ax2 = axes[1]

    ax2.plot(r_theory, d_eff_profile, '-', color='red', linewidth=2.5)
    ax2.axhline(d_min, linestyle='--', color='gray', alpha=0.5, label=f'd_min = {d_min:.1f} kpc')
    ax2.axhline(d_max, linestyle='--', color='gray', alpha=0.5, label=f'd_max = {d_max:.1f} kpc')

    ax2.set_xlabel('Rayon galactique (kpc)', fontsize=12)
    ax2.set_ylabel('d_eff(r) (kpc)', fontsize=12)
    ax2.set_title(f'Profil de Distance Effective (α = {alpha:.3f})', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10, loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 50)
    ax2.set_ylim(0, d_max * 1.2)

    plt.tight_layout()
    plt.savefig('test_d_eff_variable_densite.png', dpi=150)
    print()
    print(f"Graphique sauvegardé : test_d_eff_variable_densite.png")
    print()
    plt.show()

def chi_squared_newton():
    """
    Chi² pour Newton (référence)
    """
    r_obs, v_obs, sigma_obs = donnees_observees()

    chi2 = 0
    for i, r in enumerate(r_obs):
        v_newton = vitesse_rotation_newton(r)
        chi2 += ((v_newton - v_obs[i]) / sigma_obs[i]) ** 2

    return chi2 / len(r_obs)

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print()
    print("=" * 70)
    print(" TEST : HALO = LIMITE D'EXPANSION DU VIDE ")
    print(" Formulation : d_eff(ρ) variable ")
    print("=" * 70)
    print()

    # Optimisation
    d_min_opt, d_max_opt, alpha_opt, chi2_opt = optimiser_parametres()

    # Comparaison
    chi2_newton = chi_squared_newton()

    print("=" * 70)
    print("COMPARAISON AVEC APPROCHES PRÉCÉDENTES")
    print("=" * 70)
    print()
    print(f"  Newton (référence)              : χ² = {chi2_newton:.3f}")
    print(f"  d_eff constant (Test #1)        : χ² = 1.367")
    print(f"  d_eff optimisé (Test #2)        : χ² = 1.083")
    print(f"  d_eff = 50 kpc (Test #3)        : χ² = 1.294")
    print(f"  d_eff = 100 kpc (Test #4)       : χ² = 1.329")
    print(f"  Hybride IDT (Test #5)           : χ² = 1.329")
    print(f"  Double expansion (Test #6)      : χ² = 1.329")
    print()
    print(f"  d_eff(ρ) variable (Test #7)     : χ² = {chi2_opt:.3f} ⭐")
    print()

    if chi2_opt < 1.0:
        print("✅ SUCCÈS ! χ² < 1.0 → Ajustement acceptable")
        print()
        print("🎉 CETTE APPROCHE RÉSOUT LE BLOCAGE DE LA PHASE 2 !")
    elif chi2_opt < 1.08:
        print("⚠️  PROGRÈS ! χ² amélioré mais encore > 1.0")
        print("   Ajustement meilleur que toutes les approches précédentes")
    else:
        print("❌ ÉCHEC : χ² toujours élevé")
        print("   Cette approche ne suffit pas non plus")

    print()
    print("=" * 70)
    print()

    # Visualisation
    tracer_resultats(d_min_opt, d_max_opt, alpha_opt)

    print()
    print("Test terminé.")
    print()
