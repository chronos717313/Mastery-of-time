#!/usr/bin/env python3
"""
Test Simplifié : d_eff(ρ) Variable
===================================

Version sans dépendances pour test rapide du concept
"""

import math

# ==============================================================================
# CONSTANTES
# ==============================================================================

G = 6.67430e-11      # m³ kg⁻¹ s⁻²
M_solaire = 1.989e30 # kg
kpc_to_m = 3.086e19  # m

# ==============================================================================
# PROFIL DE MASSE
# ==============================================================================

def masse_visible(r_kpc):
    """Masse visible (exponentiel simplifié)"""
    M_totale = 6e10  # M☉
    r_scale = 3.0
    exp_term = math.exp(-r_kpc / r_scale)
    return M_totale * (1 - exp_term * (1 + r_kpc / r_scale))

def densite(r_kpc):
    """Densité (kg/m³)"""
    if r_kpc < 0.1:
        r_kpc = 0.1

    dr = 0.01
    dM = (masse_visible(r_kpc + dr/2) - masse_visible(r_kpc - dr/2)) / dr
    dM_kg_m = dM * M_solaire / kpc_to_m

    r_m = r_kpc * kpc_to_m
    rho = dM_kg_m / (4 * math.pi * r_m**2)

    return rho

# ==============================================================================
# D_EFF VARIABLE
# ==============================================================================

def d_eff_variable(r_kpc, d_min, d_max, alpha):
    """Distance effective fonction de densité"""
    rho = densite(r_kpc)
    rho_ref = densite(8.0)  # Référence au Soleil

    ratio = (rho / rho_ref) ** alpha
    d_eff = d_min + (d_max - d_min) * ratio

    # Clamp
    if d_eff < d_min:
        d_eff = d_min
    if d_eff > d_max:
        d_eff = d_max

    return d_eff

# ==============================================================================
# MASSE EFFECTIVE
# ==============================================================================

def masse_effective(r_kpc, d_min, d_max, alpha):
    """Masse effective avec d_eff(ρ)"""
    M_vis = masse_visible(r_kpc)
    M_eff = M_vis

    # Coquilles
    n_shells = 150
    r_max = 150
    dr = r_max / n_shells

    for i in range(n_shells):
        r_shell = (i + 0.5) * dr

        if abs(r_shell - r_kpc) < 0.5:
            continue

        # Densité à la coquille
        rho_shell = densite(r_shell)

        # d_eff LOCAL (à la source)
        d_eff_local = d_eff_variable(r_shell, d_min, d_max, alpha)

        # Masse dans coquille
        r_m = r_shell * kpc_to_m
        dM_kg = 4 * math.pi * r_m**2 * dr * kpc_to_m * rho_shell
        dM_solaire = dM_kg / M_solaire

        # Atténuation
        distance = abs(r_kpc - r_shell)
        f = math.exp(-distance / d_eff_local)

        M_eff += dM_solaire * f

    return M_eff

# ==============================================================================
# VITESSE
# ==============================================================================

def vitesse(r_kpc, d_min, d_max, alpha):
    """Vitesse de rotation (km/s)"""
    M_eff = masse_effective(r_kpc, d_min, d_max, alpha)
    r_m = r_kpc * kpc_to_m
    v_m_s = math.sqrt(G * M_eff * M_solaire / r_m)
    return v_m_s / 1000

def vitesse_newton(r_kpc):
    """Newton (référence)"""
    M_vis = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    v_m_s = math.sqrt(G * M_vis * M_solaire / r_m)
    return v_m_s / 1000

# ==============================================================================
# CHI²
# ==============================================================================

def chi2(d_min, d_max, alpha):
    """Chi² normalisé"""
    # Observations Voie Lactée (simplifié)
    r_obs = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50]
    v_obs = [50, 100, 150, 180, 200, 210, 215, 220, 220, 220, 220, 220, 215, 210, 200, 190]
    sigma = 10

    chi2_sum = 0
    for r, v_o in zip(r_obs, v_obs):
        v_m = vitesse(r, d_min, d_max, alpha)
        chi2_sum += ((v_m - v_o) / sigma) ** 2

    return chi2_sum / len(r_obs)

# ==============================================================================
# TEST
# ==============================================================================

if __name__ == "__main__":
    print()
    print("=" * 70)
    print(" TEST : d_eff(ρ) VARIABLE ")
    print("=" * 70)
    print()

    # Test quelques configurations
    configs = [
        (10, 100, 0.3),
        (10, 150, 0.4),
        (15, 200, 0.5),
        (5, 100, 0.3),
        (20, 150, 0.4),
    ]

    print("Test de différentes configurations :")
    print()
    print(f"{'d_min':>8} {'d_max':>8} {'alpha':>8} → {'χ²':>10}")
    print("-" * 40)

    best_chi2 = 1e6
    best_config = None

    for d_min, d_max, alpha in configs:
        chi2_val = chi2(d_min, d_max, alpha)
        print(f"{d_min:8.1f} {d_max:8.1f} {alpha:8.3f} → {chi2_val:10.3f}")

        if chi2_val < best_chi2:
            best_chi2 = chi2_val
            best_config = (d_min, d_max, alpha)

    print()
    print("=" * 70)
    print("MEILLEURE CONFIGURATION")
    print("=" * 70)
    print()
    print(f"  d_min = {best_config[0]:.1f} kpc")
    print(f"  d_max = {best_config[1]:.1f} kpc")
    print(f"  alpha = {best_config[2]:.3f}")
    print()
    print(f"  χ² = {best_chi2:.3f}")
    print()

    # Comparaison
    print("=" * 70)
    print("COMPARAISON")
    print("=" * 70)
    print()

    # Chi² Newton
    r_obs = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50]
    v_obs = [50, 100, 150, 180, 200, 210, 215, 220, 220, 220, 220, 220, 215, 210, 200, 190]
    chi2_newton = sum(((vitesse_newton(r) - v) / 10) ** 2 for r, v in zip(r_obs, v_obs)) / len(r_obs)

    print(f"  Newton                     : χ² = {chi2_newton:.3f}")
    print(f"  Tests précédents (1-6)     : χ² = 1.083 - 1.367")
    print(f"  d_eff(ρ) variable (Test #7): χ² = {best_chi2:.3f} ⭐")
    print()

    if best_chi2 < 1.0:
        print("✅ SUCCÈS ! χ² < 1.0")
        print()
        print("🎉 BLOCAGE PHASE 2 RÉSOLU !")
    elif best_chi2 < 1.08:
        print("⚠️  PROGRÈS ! Meilleur que toutes les approches précédentes")
    else:
        print("❌ Encore insuffisant")

    print()
    print("=" * 70)
    print("COURBE DE ROTATION DÉTAILLÉE")
    print("=" * 70)
    print()
    print(f"{'r (kpc)':>10} {'v_obs':>10} {'v_Newton':>10} {'v_MT':>10} {'d_eff':>10}")
    print("-" * 55)

    d_min, d_max, alpha = best_config

    for r, v_o in zip(r_obs[::2], v_obs[::2]):  # Un point sur deux
        v_n = vitesse_newton(r)
        v_mt = vitesse(r, d_min, d_max, alpha)
        d_eff_val = d_eff_variable(r, d_min, d_max, alpha)
        print(f"{r:10.1f} {v_o:10.1f} {v_n:10.1f} {v_mt:10.1f} {d_eff_val:10.1f}")

    print()
    print("MT = Maîtrise du Temps (avec d_eff variable)")
    print()
    print("Test terminé.")
    print()
