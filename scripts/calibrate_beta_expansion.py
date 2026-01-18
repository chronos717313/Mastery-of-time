#!/usr/bin/env python3
"""
Calibration du parametre beta pour l'expansion differentielle TMT v2.0

Probleme:
- beta = 0.4 donne Delta_dL ~ 6% (trop fort)
- Observations SNIa: Delta_dL < 2%

Solution:
- Trouver beta optimal compatible avec observations
- Verifier coherence avec ISW et H0 tension
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, brentq
import os

# =============================================================================
# PARAMETRES COSMOLOGIQUES
# =============================================================================
H0 = 70.0
Omega_m = 0.315
Omega_Lambda = 0.685
c = 299792.458  # km/s

# =============================================================================
# FONCTIONS COSMOLOGIQUES
# =============================================================================

def E_LCDM(z):
    """E(z) = H(z)/H0 pour LCDM."""
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def E_TMT(z, rho_ratio, beta):
    """E(z) = H(z)/H0 pour TMT avec expansion differentielle."""
    term_m = Omega_m * (1 + z)**3
    term_L = Omega_Lambda * np.exp(beta * (1 - rho_ratio))
    return np.sqrt(term_m + term_L)

def d_L_LCDM(z):
    """Distance de luminosite LCDM en Mpc."""
    integrand = lambda zp: c / (H0 * E_LCDM(zp))
    integral, _ = quad(integrand, 0, z)
    return (1 + z) * integral

def d_L_TMT(z, rho_ratio, beta):
    """Distance de luminosite TMT en Mpc."""
    integrand = lambda zp: c / (H0 * E_TMT(zp, rho_ratio, beta))
    integral, _ = quad(integrand, 0, z)
    return (1 + z) * integral

# =============================================================================
# ANALYSE DU PROBLEME
# =============================================================================

def analyze_current_problem():
    """Analyse le probleme avec beta = 0.4"""
    print("="*70)
    print("ANALYSE DU PROBLEME ACTUEL")
    print("="*70)

    beta_old = 0.4

    print(f"\nParametre actuel: beta = {beta_old}")
    print("\nPredictions Delta_dL (vide vs champ):")
    print(f"{'z':<8} {'rho_void':<10} {'Delta_dL':<12} {'Observation'}")
    print("-"*50)

    z_values = [0.05, 0.1, 0.3, 0.5]
    rho_void = 0.5  # Vide modere

    for z in z_values:
        d_field = d_L_TMT(z, 1.0, beta_old)
        d_void = d_L_TMT(z, rho_void, beta_old)
        delta = 100 * (d_void - d_field) / d_field
        obs = "< 2%" if z < 0.2 else "non mesure"
        print(f"{z:<8.2f} {rho_void:<10.1f} {delta:+.2f}%      {obs}")

    print("\n=> Probleme: TMT predit ~6% mais observations < 2%")

# =============================================================================
# CALIBRATION DE BETA
# =============================================================================

def find_optimal_beta():
    """Trouve le beta optimal compatible avec observations."""
    print("\n" + "="*70)
    print("CALIBRATION DU PARAMETRE BETA")
    print("="*70)

    # Contrainte: Delta_dL < 2% pour vide modere (rho = 0.5) a z ~ 0.05
    z_constraint = 0.05
    rho_void = 0.5
    max_delta = 2.0  # %

    def delta_dL(beta):
        d_field = d_L_TMT(z_constraint, 1.0, beta)
        d_void = d_L_TMT(z_constraint, rho_void, beta)
        return abs(100 * (d_void - d_field) / d_field)

    # Chercher beta tel que Delta_dL = 2%
    def objective(beta):
        return delta_dL(beta) - max_delta

    # Trouver la racine
    try:
        beta_max = brentq(objective, 0.01, 0.5)
    except:
        beta_max = 0.1

    print(f"\nContrainte: Delta_dL < {max_delta}% a z = {z_constraint}")
    print(f"Pour rho_void = {rho_void}")
    print(f"\n=> Beta maximum compatible: {beta_max:.3f}")

    # Tester plusieurs valeurs de beta
    print("\n" + "-"*50)
    print("Test de differentes valeurs de beta:")
    print(f"{'beta':<10} {'Delta_dL(z=0.05)':<18} {'Delta_dL(z=0.5)':<18}")
    print("-"*50)

    beta_values = [0.05, 0.10, 0.12, 0.15, 0.20, 0.30, 0.40]

    for beta in beta_values:
        d1 = delta_dL(beta)

        d_field2 = d_L_TMT(0.5, 1.0, beta)
        d_void2 = d_L_TMT(0.5, rho_void, beta)
        d2 = abs(100 * (d_void2 - d_field2) / d_field2)

        mark = " *" if beta <= beta_max else ""
        print(f"{beta:<10.2f} {d1:<18.2f}% {d2:<18.2f}%{mark}")

    print("-"*50)
    print("* = compatible avec observations")

    return beta_max

# =============================================================================
# NOUVELLE FORMULATION
# =============================================================================

def propose_new_formulation(beta_new):
    """Propose une nouvelle formulation avec beta ajuste."""
    print("\n" + "="*70)
    print("NOUVELLE FORMULATION TMT v2.1")
    print("="*70)

    print(f"\nAncienne formulation (TMT v2.0):")
    print("  H(z, rho) = H0 * sqrt[Omega_m(1+z)^3 + Omega_L * exp(0.4 * (1 - rho/rho_c))]")

    print(f"\nNouvelle formulation (TMT v2.1):")
    print(f"  H(z, rho) = H0 * sqrt[Omega_m(1+z)^3 + Omega_L * exp({beta_new:.2f} * (1 - rho/rho_c))]")

    print("\n" + "-"*50)
    print("Predictions avec nouveau beta:")
    print(f"{'Environnement':<20} {'rho/rho_c':<12} {'H/H_LCDM (z=0)':<15}")
    print("-"*50)

    environments = [
        ("Supervide extreme", 0.2),
        ("Vide profond", 0.3),
        ("Vide modere", 0.5),
        ("Champ moyen", 1.0),
        ("Filament", 2.0),
        ("Amas", 5.0),
    ]

    for name, rho in environments:
        H_ratio = E_TMT(0, rho, beta_new) / E_LCDM(0)
        print(f"{name:<20} {rho:<12.1f} {H_ratio:<15.4f}")

    return beta_new

# =============================================================================
# VERIFICATION COHERENCE
# =============================================================================

def verify_coherence(beta_new):
    """Verifie la coherence avec les autres tests."""
    print("\n" + "="*70)
    print("VERIFICATION DE COHERENCE")
    print("="*70)

    # 1. Tension H0
    print("\n1. TENSION H0:")
    print("-"*50)

    # Mesure locale dans vide local (rho ~ 0.8)
    rho_local = 0.8  # Notre voisinage est legerement sous-dense

    H_local = H0 * E_TMT(0, rho_local, beta_new)
    H_cmb = H0  # CMB mesure la moyenne cosmique

    H0_planck = 67.4
    H0_local_obs = 73.0
    tension_obs = 100 * (H0_local_obs - H0_planck) / H0_planck

    tension_tmt = 100 * (E_TMT(0, rho_local, beta_new) - 1)

    print(f"  H0 Planck (CMB): {H0_planck} km/s/Mpc")
    print(f"  H0 local observe: {H0_local_obs} km/s/Mpc")
    print(f"  Tension observee: {tension_obs:.1f}%")
    print(f"\n  rho_local estime: {rho_local}")
    print(f"  Tension predite TMT (beta={beta_new:.2f}): {tension_tmt:.1f}%")

    if abs(tension_tmt) < tension_obs / 2:
        h0_verdict = "PARTIEL"
        print(f"\n  => TMT explique partiellement la tension ({tension_tmt:.1f}% vs {tension_obs:.1f}%)")
    else:
        h0_verdict = "POSSIBLE"
        print(f"\n  => TMT peut expliquer une partie de la tension")

    # 2. ISW
    print("\n2. EFFET ISW:")
    print("-"*50)

    # Amplification ISW dans supervide
    rho_supervoid = 0.3
    z_void = 0.5

    H_ratio = E_TMT(z_void, rho_supervoid, beta_new) / E_LCDM(z_void)
    isw_amplification = (H_ratio - 1) * 100

    print(f"  Supervide (rho = {rho_supervoid}):")
    print(f"  H_TMT / H_LCDM = {H_ratio:.4f}")
    print(f"  Amplification ISW estimee: {isw_amplification:+.1f}%")
    print(f"\n  Observation: A_ISW ~ 5 (+400%)")
    print(f"  => TMT sous-estime toujours l'anomalie ISW")

    # 3. SNIa
    print("\n3. SNIa PAR ENVIRONNEMENT:")
    print("-"*50)

    z_test = 0.05
    rho_void = 0.5

    d_field = d_L_TMT(z_test, 1.0, beta_new)
    d_void = d_L_TMT(z_test, rho_void, beta_new)
    delta = abs(100 * (d_void - d_field) / d_field)

    print(f"  Delta_dL (z={z_test}, rho={rho_void}): {delta:.2f}%")
    print(f"  Limite observationnelle: < 2%")

    if delta <= 2.0:
        snia_verdict = "COMPATIBLE"
        print(f"  => COMPATIBLE avec observations")
    else:
        snia_verdict = "TENSION"
        print(f"  => Encore en tension")

    return {
        'H0_tension': tension_tmt,
        'ISW_amplification': isw_amplification,
        'SNIa_delta': delta,
        'H0_verdict': h0_verdict,
        'SNIa_verdict': snia_verdict
    }

# =============================================================================
# FORMULATION ALTERNATIVE
# =============================================================================

def alternative_formulation():
    """
    Explore une formulation alternative qui:
    - Garde l'effet faible a bas z (SNIa)
    - Amplifie l'effet a haut z (ISW)
    - Explique la tension H0
    """
    print("\n" + "="*70)
    print("FORMULATION ALTERNATIVE (TMT v2.2)")
    print("="*70)

    print("\nIdee: L'effet depend du redshift")
    print("  beta_eff(z) = beta_0 * (1 + z)^gamma")
    print("\nCeci permet:")
    print("  - Effet faible a z ~ 0 (compatible SNIa)")
    print("  - Effet plus fort a z > 0.5 (ISW amplifie)")

    beta_0 = 0.08  # Faible a z=0
    gamma = 1.5    # Amplification avec z

    def beta_eff(z):
        return beta_0 * (1 + z)**gamma

    def E_TMT_v22(z, rho_ratio):
        b = beta_eff(z)
        term_m = Omega_m * (1 + z)**3
        term_L = Omega_Lambda * np.exp(b * (1 - rho_ratio))
        return np.sqrt(term_m + term_L)

    print(f"\nParametres: beta_0 = {beta_0}, gamma = {gamma}")
    print(f"\n{'z':<8} {'beta_eff':<12} {'H_void/H_LCDM':<15} {'Delta H %'}")
    print("-"*50)

    z_values = [0.0, 0.05, 0.1, 0.3, 0.5, 0.7, 1.0]
    rho_void = 0.3

    for z in z_values:
        b = beta_eff(z)
        H_ratio = E_TMT_v22(z, rho_void) / E_LCDM(z)
        delta_H = (H_ratio - 1) * 100
        print(f"{z:<8.2f} {b:<12.3f} {H_ratio:<15.4f} {delta_H:+.1f}%")

    # Verifier SNIa
    print("\n" + "-"*50)
    print("Verification SNIa (z = 0.05, rho = 0.5):")

    def d_L_v22(z, rho_ratio):
        integrand = lambda zp: c / (H0 * E_TMT_v22(zp, rho_ratio))
        integral, _ = quad(integrand, 0, z)
        return (1 + z) * integral

    d_field = d_L_v22(0.05, 1.0)
    d_void = d_L_v22(0.05, 0.5)
    delta_dL = abs(100 * (d_void - d_field) / d_field)

    print(f"  Delta_dL = {delta_dL:.2f}% (limite: < 2%)")

    # ISW a z = 0.5
    print("\nVerification ISW (z = 0.5, rho = 0.3):")
    H_ratio_isw = E_TMT_v22(0.5, 0.3) / E_LCDM(0.5)
    print(f"  H_TMT / H_LCDM = {H_ratio_isw:.3f} (+{(H_ratio_isw-1)*100:.1f}%)")

    return beta_0, gamma

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("CALIBRATION EXPANSION DIFFERENTIELLE TMT")
    print("="*70)

    # 1. Analyser le probleme actuel
    analyze_current_problem()

    # 2. Trouver beta optimal
    beta_optimal = find_optimal_beta()

    # 3. Proposer nouvelle formulation
    beta_new = min(beta_optimal, 0.12)  # Prendre une valeur conservative
    propose_new_formulation(beta_new)

    # 4. Verifier coherence
    results = verify_coherence(beta_new)

    # 5. Formulation alternative
    beta_0, gamma = alternative_formulation()

    # Resume
    print("\n" + "="*70)
    print("RESUME ET RECOMMANDATIONS")
    print("="*70)

    print("\nOption 1: TMT v2.1 (beta constant)")
    print(f"  beta = {beta_new:.2f}")
    print(f"  SNIa: {results['SNIa_verdict']}")
    print(f"  H0 tension: explique {results['H0_tension']:.1f}%")
    print(f"  ISW: +{results['ISW_amplification']:.1f}% (insuffisant)")

    print("\nOption 2: TMT v2.2 (beta evolutif)")
    print(f"  beta(z) = {beta_0} * (1+z)^{gamma}")
    print("  Permet effet faible a bas z, fort a haut z")
    print("  A valider avec donnees detaillees")

    print("\n" + "="*70)
    print("FORMULE RECOMMANDEE: TMT v2.1")
    print("="*70)
    print(f"\nH(z, rho) = H0 * sqrt[Omega_m(1+z)^3 + Omega_L * exp({beta_new:.2f} * (1 - rho/rho_c))]")
    print(f"\navec beta = {beta_new:.2f} (au lieu de 0.4)")
    print("="*70)

    # Sauvegarder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "..", "data", "results")
    os.makedirs(results_dir, exist_ok=True)

    results_path = os.path.join(results_dir, "calibration_beta.txt")

    with open(results_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("CALIBRATION BETA - RESULTATS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Ancien beta: 0.4\n")
        f.write(f"Nouveau beta: {beta_new:.2f}\n\n")
        f.write("Formule TMT v2.1:\n")
        f.write(f"H(z, rho) = H0 * sqrt[Om*(1+z)^3 + OL*exp({beta_new:.2f}*(1-rho/rho_c))]\n\n")
        f.write(f"SNIa Delta_dL: {results['SNIa_delta']:.2f}% (limite < 2%)\n")
        f.write(f"H0 tension expliquee: {results['H0_tension']:.1f}%\n")
        f.write(f"ISW amplification: +{results['ISW_amplification']:.1f}%\n")

    print(f"\nResultats sauvegardes: {results_path}")
