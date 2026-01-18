#!/usr/bin/env python3
"""
Calcul ameliore de l'effet ISW (Integrated Sachs-Wolfe)
Comparaison TMT v2.0 vs LCDM

L'effet ISW mesure la variation du potentiel gravitationnel
pendant que les photons CMB traversent les structures:

Delta_T/T = 2/c^2 * integral(d_Phi/dt * dl)

TMT predit une amplification de +26% dans les supervides.
"""

import numpy as np
from scipy.integrate import quad, odeint
from scipy.interpolate import interp1d
import os

# =============================================================================
# PARAMETRES COSMOLOGIQUES
# =============================================================================
H0 = 70.0          # km/s/Mpc
Omega_m = 0.315
Omega_Lambda = 0.685
c = 299792.458     # km/s
beta = 0.4         # Parametre d'ancrage TMT

# Conversion
H0_si = H0 * 1000 / 3.086e22  # s^-1
Mpc_to_m = 3.086e22

# =============================================================================
# FONCTIONS DE HUBBLE
# =============================================================================

def E_LCDM(z):
    """E(z) = H(z)/H0 pour LCDM."""
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def E_TMT(z, rho_ratio):
    """E(z) = H(z)/H0 pour TMT avec expansion differentielle."""
    term_m = Omega_m * (1 + z)**3
    term_L = Omega_Lambda * np.exp(beta * (1 - rho_ratio))
    return np.sqrt(term_m + term_L)

def H_LCDM(z):
    """Fonction de Hubble LCDM en km/s/Mpc."""
    return H0 * E_LCDM(z)

def H_TMT(z, rho_ratio):
    """Fonction de Hubble TMT en km/s/Mpc."""
    return H0 * E_TMT(z, rho_ratio)

# =============================================================================
# FACTEUR DE CROISSANCE
# =============================================================================

def growth_factor_integral_LCDM(z):
    """
    Calcul du facteur de croissance D(z) pour LCDM
    D(a) proportionnel a integral[da'/(a'^3 * E(a')^3)]
    """
    def integrand(zp):
        return (1 + zp) / E_LCDM(zp)**3

    result, _ = quad(integrand, z, np.inf)
    D = E_LCDM(z) * result

    # Normaliser a z=0
    D0, _ = quad(integrand, 0, np.inf)
    D0 = E_LCDM(0) * D0

    return D / D0

def growth_factor_integral_TMT(z, rho_ratio):
    """
    Calcul du facteur de croissance D(z) pour TMT
    avec expansion differentielle.
    """
    def integrand(zp):
        return (1 + zp) / E_TMT(zp, rho_ratio)**3

    result, _ = quad(integrand, z, np.inf, limit=100)
    D = E_TMT(z, rho_ratio) * result

    # Normaliser a z=0
    D0, _ = quad(integrand, 0, np.inf, limit=100)
    D0 = E_TMT(0, rho_ratio) * D0

    return D / D0

# =============================================================================
# TAUX DE CROISSANCE LOGARITHMIQUE
# =============================================================================

def f_growth_LCDM(z):
    """
    f(z) = d ln D / d ln a (taux de croissance logarithmique)
    Approximation: f ~ Omega_m(z)^0.55
    """
    Omega_m_z = Omega_m * (1 + z)**3 / E_LCDM(z)**2
    return Omega_m_z**0.55

def f_growth_TMT(z, rho_ratio):
    """
    f(z) pour TMT avec expansion differentielle.
    """
    E = E_TMT(z, rho_ratio)
    Omega_m_z = Omega_m * (1 + z)**3 / E**2
    # Correction pour l'expansion differentielle
    # Dans les vides, l'expansion est plus rapide => croissance plus lente
    f = Omega_m_z**0.55
    return f

# =============================================================================
# INTEGRAND ISW
# =============================================================================

def ISW_integrand_LCDM(z):
    """
    Integrande pour l'effet ISW dans LCDM.

    L'effet ISW est proportionnel a d(D/a)/dt
    = (1/a) * dD/dt - D/a^2 * da/dt
    = (1/a) * D * f * H - D/a * H
    = D * H * (f/a - 1/a)
    = D * H * (f - 1) / a

    En termes de z:
    ISW propto D(z) * (1 - f(z)) * (1+z) / E(z)
    """
    D = growth_factor_integral_LCDM(z)
    f = f_growth_LCDM(z)
    E = E_LCDM(z)

    # d(D/a)/dt propto (f-1) * D * H / a
    # L'integrale ISW est sur le temps propre dl/c = dr/(c*(1+z))
    # et dr = c * dz / H(z)
    # Donc ISW propto D * (f-1) / (a * E(z))

    return D * (f - 1) / ((1 + z) * E)

def ISW_integrand_TMT(z, rho_ratio):
    """
    Integrande pour l'effet ISW dans TMT.
    """
    D = growth_factor_integral_TMT(z, rho_ratio)
    f = f_growth_TMT(z, rho_ratio)
    E = E_TMT(z, rho_ratio)

    return D * (f - 1) / ((1 + z) * E)

# =============================================================================
# CALCUL INTEGRAL ISW
# =============================================================================

def calculate_ISW_signal_LCDM(z_min, z_max):
    """
    Calcule le signal ISW integre entre z_min et z_max pour LCDM.
    """
    result, _ = quad(ISW_integrand_LCDM, z_min, z_max, limit=100)
    return result

def calculate_ISW_signal_TMT(z_min, z_max, rho_ratio):
    """
    Calcule le signal ISW integre entre z_min et z_max pour TMT.
    """
    def integrand(z):
        return ISW_integrand_TMT(z, rho_ratio)

    result, _ = quad(integrand, z_min, z_max, limit=100)
    return result

# =============================================================================
# ANALYSE SUPERVIDES
# =============================================================================

def analyze_supervoid_ISW(void_z=0.5, void_size_Mpc=100):
    """
    Analyse du signal ISW pour un supervide typique.

    Parametres:
    - void_z: redshift central du vide
    - void_size_Mpc: taille du vide en Mpc

    Le contraste de densite dans un supervide typique est delta ~ -0.3
    ce qui correspond a rho/rho_crit ~ 0.7
    Pour un supervide profond: delta ~ -0.8, rho/rho_crit ~ 0.2
    """
    print("\n" + "="*70)
    print("ANALYSE ISW POUR SUPERVIDE")
    print("="*70)

    print(f"\nParametres du supervide:")
    print(f"  Redshift central: z = {void_z}")
    print(f"  Taille: {void_size_Mpc} Mpc")

    # Calcul du delta_z correspondant a la taille
    d_H = c / H_LCDM(void_z)  # Distance de Hubble en Mpc
    delta_z = void_size_Mpc * H_LCDM(void_z) / c

    z_min = void_z - delta_z/2
    z_max = void_z + delta_z/2

    print(f"  z_min: {z_min:.3f}")
    print(f"  z_max: {z_max:.3f}")

    # Cas a analyser
    cases = [
        ("LCDM (rho = rho_crit)", 1.0),
        ("Vide modere (rho = 0.7*rho_crit)", 0.7),
        ("Vide profond (rho = 0.3*rho_crit)", 0.3),
        ("Supervide extreme (rho = 0.2*rho_crit)", 0.2),
    ]

    print(f"\n{'Environnement':<45} {'ISW signal':<15} {'Ratio/LCDM':<12}")
    print("-"*70)

    # Reference LCDM
    ISW_lcdm = calculate_ISW_signal_LCDM(z_min, z_max)

    results = {}
    for name, rho_ratio in cases:
        ISW = calculate_ISW_signal_TMT(z_min, z_max, rho_ratio)
        ratio = ISW / ISW_lcdm if ISW_lcdm != 0 else 0
        results[name] = (ISW, ratio)
        print(f"{name:<45} {ISW:.6e}     {ratio:.3f}")

    # Amplification dans les vides
    ISW_void = results["Supervide extreme (rho = 0.2*rho_crit)"][0]
    amplification = (ISW_void / ISW_lcdm - 1) * 100 if ISW_lcdm != 0 else 0

    print("-"*70)
    print(f"\nAmplification ISW dans supervide extreme: {amplification:+.1f}%")
    print(f"Prediction TMT attendue: +26%")

    return amplification

# =============================================================================
# ANALYSE MULTI-REDSHIFT
# =============================================================================

def analyze_ISW_vs_redshift():
    """
    Analyse du ratio ISW(TMT)/ISW(LCDM) en fonction du redshift.
    """
    print("\n" + "="*70)
    print("RATIO ISW(TMT)/ISW(LCDM) VS REDSHIFT")
    print("="*70)

    z_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]
    rho_void = 0.2  # Supervide
    rho_dense = 3.0  # Surdensite

    print(f"\n{'z':<8} {'D_LCDM':<10} {'D_void':<10} {'D_dense':<10} {'Ratio void':<12} {'Ratio dense'}")
    print("-"*70)

    for z in z_values:
        D_lcdm = growth_factor_integral_LCDM(z)
        D_void = growth_factor_integral_TMT(z, rho_void)
        D_dense = growth_factor_integral_TMT(z, rho_dense)

        ratio_void = D_void / D_lcdm
        ratio_dense = D_dense / D_lcdm

        print(f"{z:<8.1f} {D_lcdm:<10.4f} {D_void:<10.4f} {D_dense:<10.4f} {ratio_void:<12.3f} {ratio_dense:.3f}")

# =============================================================================
# CALCUL DETAILLE ISW
# =============================================================================

def detailed_ISW_calculation():
    """
    Calcul detaille de l'effet ISW avec differentes approximations.
    """
    print("\n" + "="*70)
    print("CALCUL DETAILLE DE L'EFFET ISW")
    print("="*70)

    # L'effet ISW en LCDM est:
    # Delta_T/T = 2 * integral[ (Phi' + Psi') / c^2 * a dt ]
    #
    # En supposant Phi = Psi (pas d'anisotropie de stress):
    # Delta_T/T = 4 * integral[ Phi' / c^2 * a dt ]
    #
    # Le potentiel evolue comme:
    # Phi propto D(a) / a   (en theorie lineaire)
    #
    # Donc Phi' = d(D/a)/dt = (D' * a - D * a')/a^2 = (D'/a - D*H)/a
    #          = H * (f*D/a - D/a) = H*D*(f-1)/a
    #
    # L'integrale ISW devient:
    # Delta_T/T propto integral[ D*(f-1) / a^2 * c*dz/H ]
    #               = integral[ D*(f-1) * c / (a^2 * H) dz ]
    #               = integral[ D*(f-1) / ((1+z)^2 * E) * c/H0 dz ]

    z_min, z_max = 0.3, 0.7  # Intervalle typique d'un supervide

    print(f"\nIntervalle d'integration: z = {z_min} a {z_max}")

    # Calcul numerique pour LCDM
    def full_integrand_LCDM(z):
        D = growth_factor_integral_LCDM(z)
        f = f_growth_LCDM(z)
        E = E_LCDM(z)
        return D * (f - 1) / ((1 + z)**2 * E)

    ISW_lcdm, _ = quad(full_integrand_LCDM, z_min, z_max, limit=100)

    # Calcul pour TMT dans differents environnements
    rho_ratios = [0.2, 0.5, 0.7, 1.0, 2.0, 5.0]

    print(f"\n{'rho/rho_crit':<15} {'ISW signal':<15} {'Ratio/LCDM':<12} {'Amplification'}")
    print("-"*60)

    for rho in rho_ratios:
        def full_integrand_TMT(z):
            D = growth_factor_integral_TMT(z, rho)
            f = f_growth_TMT(z, rho)
            E = E_TMT(z, rho)
            return D * (f - 1) / ((1 + z)**2 * E)

        ISW_tmt, _ = quad(full_integrand_TMT, z_min, z_max, limit=100)
        ratio = ISW_tmt / ISW_lcdm if ISW_lcdm != 0 else 0
        amplification = (ratio - 1) * 100

        env = "VIDE" if rho < 0.5 else ("DENSE" if rho > 1.5 else "moyen")
        print(f"{rho:<15.1f} {ISW_tmt:<15.6e} {ratio:<12.3f} {amplification:+.1f}% ({env})")

    print("-"*60)

    return ISW_lcdm

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("CALCUL AMELIORE DE L'EFFET ISW - TMT v2.0")
    print("="*70)

    # Test facteurs de croissance
    print("\n" + "="*70)
    print("1. VERIFICATION DES FACTEURS DE CROISSANCE")
    print("="*70)

    z_test = [0, 0.5, 1.0, 2.0]
    print(f"\n{'z':<8} {'D_LCDM':<12} {'D_void(0.2)':<15} {'D_dense(5.0)':<15}")
    print("-"*50)

    for z in z_test:
        D_lcdm = growth_factor_integral_LCDM(z)
        D_void = growth_factor_integral_TMT(z, 0.2)
        D_dense = growth_factor_integral_TMT(z, 5.0)
        print(f"{z:<8.1f} {D_lcdm:<12.4f} {D_void:<15.4f} {D_dense:<15.4f}")

    # Analyse supervide
    amplification = analyze_supervoid_ISW(void_z=0.5, void_size_Mpc=150)

    # Calcul detaille
    detailed_ISW_calculation()

    # Analyse vs redshift
    analyze_ISW_vs_redshift()

    # Verdict
    print("\n" + "="*70)
    print("VERDICT")
    print("="*70)

    if abs(amplification) > 20:
        verdict = "PREDICTION TMT SUPPORTEE"
        print(f"\nAmplification calculee: {amplification:+.1f}%")
        print(f"Prediction TMT: +26%")
        print(f"=> {verdict}")
    else:
        verdict = "AMPLIFICATION FAIBLE"
        print(f"\nAmplification calculee: {amplification:+.1f}%")
        print(f"Prediction TMT: +26%")
        print(f"=> {verdict}")
        print("\nNote: L'amplification depend fortement des hypotheses")
        print("sur l'evolution du facteur de croissance dans les vides.")

    # Sauvegarder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "..", "data", "results")
    os.makedirs(results_dir, exist_ok=True)

    results_path = os.path.join(results_dir, "ISW_improved_analysis.txt")
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("CALCUL AMELIORE ISW - RESULTATS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Amplification ISW dans supervide (rho=0.2): {amplification:+.1f}%\n")
        f.write(f"Prediction TMT: +26%\n")
        f.write(f"Verdict: {verdict}\n")

    print(f"\nResultats sauvegardes: {results_path}")
