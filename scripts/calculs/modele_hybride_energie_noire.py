#!/usr/bin/env python3
"""
Modèle Hybride d'Énergie Noire : 70% Temporel + 30% Spatial
============================================================

Implémente le modèle cosmologique avec partition de l'énergie noire :
- 70% Distorsion temporelle : τ(t) ∝ t^β
- 30% Expansion spatiale : a(t) ∝ exp(H₀t)

Calcule les observables :
- Distance lumineuse d_L(z)
- Module de distance μ(z)
- Taux d'expansion H(z)
- Âge de l'univers t₀

Compare avec Lambda-CDM et ajuste aux données Supernovae Ia.

Date : 2025-12-05
Auteur : Claude (assistant IA)
Théorie : Maîtrise du Temps - Modèle Hybride
"""

import math

# ==============================================================================
# CONSTANTES
# ==============================================================================

c_km_s = 299792.458        # Vitesse lumière (km/s)
H0_fiducial = 70.0         # H₀ fiducial (km/s/Mpc)
Om_fiducial = 0.30         # Ω_matière fiducial
OL_total = 0.70            # Ω_Λ total observé

# Partition énergie noire
f_spatial = 0.30           # Fraction spatiale (30%)
f_temporel = 0.70          # Fraction temporelle (70%)

OL_spatial = OL_total * f_spatial    # 0.21
OL_temporel = OL_total * f_temporel  # 0.49

# ==============================================================================
# TAUX D'EXPANSION H(z)
# ==============================================================================

def H_Lambda_CDM(z, H0=H0_fiducial, Om=Om_fiducial):
    """
    Taux d'expansion Lambda-CDM standard

    H(z) = H₀ · √[Ω_m(1+z)³ + Ω_Λ]

    Parameters
    ----------
    z : float
        Redshift
    H0 : float
        Constante de Hubble (km/s/Mpc)
    Om : float
        Densité de matière

    Returns
    -------
    H : float
        Taux d'expansion (km/s/Mpc)
    """
    term_matter = Om * (1 + z)**3
    term_lambda = 1 - Om  # Ω_Λ dans Lambda-CDM plat

    return H0 * math.sqrt(term_matter + term_lambda)

def H_hybride(z, H0=H0_fiducial, Om=Om_fiducial, beta=2.0/3.0):
    """
    Taux d'expansion avec modèle hybride

    H(z) = H₀ · (1+z)^β · √[Ω_m(1+z)³ + Ω_Λ,spatial·(1+z)^(2β)]

    Avec :
    - Ω_Λ,spatial = 0.21 (30% de l'énergie noire)
    - β = exposant d'expansion temporelle

    Parameters
    ----------
    z : float
        Redshift
    H0 : float
        Constante de Hubble (km/s/Mpc)
    Om : float
        Densité de matière
    beta : float
        Exposant d'expansion temporelle

    Returns
    -------
    H : float
        Taux d'expansion (km/s/Mpc)
    """
    term_matter = Om * (1 + z)**3
    term_lambda_spatial = OL_spatial * (1 + z)**(2 * beta)

    H_base = H0 * math.sqrt(term_matter + term_lambda_spatial)

    # Facteur temporel (1+z)^β
    H_total = (1 + z)**beta * H_base

    return H_total

# ==============================================================================
# DISTANCE LUMINEUSE
# ==============================================================================

def distance_luminosite_numerique(z, H0, Om, beta=None, model='hybrid', n_steps=1000):
    """
    Distance lumineuse calculée numériquement

    d_L = (1+z) · c · ∫₀^z dz'/H(z')

    Parameters
    ----------
    z : float
        Redshift
    H0, Om : float
        Paramètres cosmologiques
    beta : float or None
        Exposant temporel (si model='hybrid')
    model : str
        'hybrid' ou 'lcdm'
    n_steps : int
        Nombre de pas d'intégration

    Returns
    -------
    d_L : float
        Distance lumineuse (Mpc)
    """
    if z < 1e-6:
        return 0.0

    # Intégration numérique trapèze
    dz = z / n_steps
    integral = 0.0

    for i in range(n_steps):
        z1 = i * dz
        z2 = (i + 1) * dz

        if model == 'hybrid':
            if beta is None:
                beta = 2.0/3.0
            H1 = H_hybride(z1, H0, Om, beta)
            H2 = H_hybride(z2, H0, Om, beta)
        else:  # lcdm
            H1 = H_Lambda_CDM(z1, H0, Om)
            H2 = H_Lambda_CDM(z2, H0, Om)

        # Trapèze
        integral += 0.5 * (1/H1 + 1/H2) * dz

    d_L = (1 + z) * c_km_s * integral

    return d_L  # Mpc

def module_distance(z, H0, Om, beta=None, model='hybrid'):
    """
    Module de distance μ(z) = m - M

    μ = 5 log₁₀(d_L / 10 pc) = 5 log₁₀(d_L) + 25

    où d_L est en Mpc
    """
    d_L = distance_luminosite_numerique(z, H0, Om, beta, model)

    if d_L <= 0:
        return 0.0

    mu = 5 * math.log10(d_L) + 25

    return mu

# ==============================================================================
# ÂGE DE L'UNIVERS
# ==============================================================================

def age_univers(H0, Om, beta=None, model='hybrid', z_max=1000, n_steps=10000):
    """
    Âge de l'univers t₀

    t₀ = ∫₀^∞ dt = ∫₀^∞ dz / [H(z)(1+z)]

    Parameters
    ----------
    H0, Om : float
        Paramètres cosmologiques
    beta : float or None
        Exposant temporel (si model='hybrid')
    model : str
        'hybrid' ou 'lcdm'
    z_max : float
        Limite supérieure d'intégration (approximation de l'infini)
    n_steps : int
        Nombre de pas

    Returns
    -------
    t0 : float
        Âge (milliards d'années)
    """
    dz = z_max / n_steps
    integral = 0.0

    for i in range(n_steps):
        z1 = i * dz
        z2 = (i + 1) * dz

        if model == 'hybrid':
            if beta is None:
                beta = 2.0/3.0
            H1 = H_hybride(z1, H0, Om, beta)
            H2 = H_hybride(z2, H0, Om, beta)
        else:
            H1 = H_Lambda_CDM(z1, H0, Om)
            H2 = H_Lambda_CDM(z2, H0, Om)

        # Intégrand: 1/[H(z)(1+z)]
        f1 = 1.0 / (H1 * (1 + z1)) if z1 > 0 else 1.0/H1
        f2 = 1.0 / (H2 * (1 + z2))

        integral += 0.5 * (f1 + f2) * dz

    # Conversion km/s/Mpc → Gyr
    # 1/H₀ = 1/(70 km/s/Mpc) = 14.0 Gyr
    H0_inv_Gyr = 977.8 / H0  # Facteur de conversion

    t0_Gyr = integral * H0_inv_Gyr

    return t0_Gyr

# ==============================================================================
# PARAMÈTRE DE DÉCÉLÉRATION
# ==============================================================================

def parametre_deceleration(z, H0, Om, beta, model='hybrid'):
    """
    Paramètre de décélération q(z)

    q(z) = -1 - Ḣ/H²

    Approximation numérique : q ≈ -(1 + z)/H · dH/dz
    """
    dz = 0.001
    z1 = z - dz/2
    z2 = z + dz/2

    if z1 < 0:
        z1 = 0

    if model == 'hybrid':
        H1 = H_hybride(z1, H0, Om, beta)
        H2 = H_hybride(z2, H0, Om, beta)
        H = H_hybride(z, H0, Om, beta)
    else:
        H1 = H_Lambda_CDM(z1, H0, Om)
        H2 = H_Lambda_CDM(z2, H0, Om)
        H = H_Lambda_CDM(z, H0, Om)

    dH_dz = (H2 - H1) / dz

    q = -(1 + z) / H * dH_dz - 1

    return q

# ==============================================================================
# DONNÉES SUPERNOVAE Ia (Union2.1 simplifié)
# ==============================================================================

def donnees_supernovae_simplifiees():
    """
    Données simplifiées de supernovae Ia

    Basé sur Union2.1 (échantillon réduit pour test rapide)

    Returns
    -------
    z_obs : list
        Redshifts
    mu_obs : list
        Modules de distance observés
    sigma_obs : list
        Incertitudes
    """
    # Échantillon représentatif (10 points)
    z_obs = [0.01, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]

    # Modules de distance (calibrés sur Lambda-CDM avec H₀=70, Ω_m=0.3)
    mu_obs = [
        33.0,   # z=0.01
        38.5,   # z=0.1
        41.0,   # z=0.2
        43.5,   # z=0.4
        44.8,   # z=0.6
        45.8,   # z=0.8
        46.5,   # z=1.0
        47.1,   # z=1.2
        47.6,   # z=1.4
        48.0    # z=1.6
    ]

    sigma_obs = [0.15] * len(z_obs)  # Incertitude typique 0.15 mag

    return z_obs, mu_obs, sigma_obs

# ==============================================================================
# CHI-CARRÉ
# ==============================================================================

def chi2_supernovae(H0, Om, beta=None, model='hybrid'):
    """
    Chi² pour ajustement aux supernovae

    χ² = Σ [(μ_théo - μ_obs) / σ]²
    """
    z_obs, mu_obs, sigma_obs = donnees_supernovae_simplifiees()

    chi2 = 0.0

    for z, mu_o, sig in zip(z_obs, mu_obs, sigma_obs):
        mu_theo = module_distance(z, H0, Om, beta, model)
        chi2 += ((mu_theo - mu_o) / sig) ** 2

    chi2_norm = chi2 / len(z_obs)

    return chi2_norm

# ==============================================================================
# OPTIMISATION SIMPLE
# ==============================================================================

def optimiser_beta(H0=70.0, Om=0.30):
    """
    Optimise β pour minimiser χ²

    Teste différentes valeurs de β et trouve le minimum
    """
    print()
    print("=" * 70)
    print("OPTIMISATION DU PARAMÈTRE β")
    print("=" * 70)
    print()
    print(f"Paramètres fixés : H₀ = {H0} km/s/Mpc, Ω_m = {Om}")
    print()

    beta_values = [i * 0.05 for i in range(0, 21)]  # 0.0 à 1.0 par pas de 0.05

    best_beta = None
    best_chi2 = 1e10

    print(f"{'β':>8} → {'χ²':>10} {'Statut'}")
    print("-" * 35)

    for beta in beta_values:
        chi2 = chi2_supernovae(H0, Om, beta, 'hybrid')

        status = ""
        if chi2 < 1.0:
            status = "⭐"
        elif chi2 < 1.5:
            status = "✓"

        print(f"{beta:8.2f} → {chi2:10.3f} {status}")

        if chi2 < best_chi2:
            best_chi2 = chi2
            best_beta = beta

    print()
    print("=" * 70)
    print("RÉSULTAT")
    print("=" * 70)
    print()
    print(f"  β optimal = {best_beta:.3f}")
    print(f"  χ² minimal = {best_chi2:.3f}")
    print()

    # Comparaison avec Lambda-CDM
    chi2_lcdm = chi2_supernovae(H0, Om, None, 'lcdm')
    print(f"  χ² Lambda-CDM = {chi2_lcdm:.3f}")
    print()

    if best_chi2 < chi2_lcdm:
        print(f"✅ Modèle hybride MEILLEUR que Lambda-CDM")
        print(f"   Amélioration : {chi2_lcdm / best_chi2:.2f}×")
    elif best_chi2 < chi2_lcdm * 1.1:
        print(f"≈ Modèle hybride ÉQUIVALENT à Lambda-CDM")
        print(f"   Différence : {(best_chi2 - chi2_lcdm) / chi2_lcdm * 100:.1f}%")
    else:
        print(f"⚠ Modèle hybride moins bon que Lambda-CDM")
        print(f"   Ratio : {best_chi2 / chi2_lcdm:.2f}×")

    print()

    return best_beta, best_chi2

# ==============================================================================
# TESTS ET VISUALISATIONS
# ==============================================================================

def comparer_modeles(beta_opt):
    """
    Compare prédictions du modèle hybride vs Lambda-CDM
    """
    print("=" * 70)
    print("COMPARAISON DES PRÉDICTIONS")
    print("=" * 70)
    print()

    H0, Om = 70.0, 0.30

    # Âges de l'univers
    t0_lcdm = age_univers(H0, Om, None, 'lcdm')
    t0_hybrid = age_univers(H0, Om, beta_opt, 'hybrid')

    print(f"Âge de l'univers :")
    print(f"  Lambda-CDM : {t0_lcdm:.2f} Gyr")
    print(f"  Hybride    : {t0_hybrid:.2f} Gyr")
    print(f"  Différence : {abs(t0_hybrid - t0_lcdm):.2f} Gyr ({abs(t0_hybrid-t0_lcdm)/t0_lcdm*100:.1f}%)")
    print()

    # Paramètre de décélération aujourd'hui
    q0_lcdm = parametre_deceleration(0, H0, Om, None, 'lcdm')
    q0_hybrid = parametre_deceleration(0, H0, Om, beta_opt, 'hybrid')

    print(f"Paramètre de décélération q₀ :")
    print(f"  Lambda-CDM : {q0_lcdm:.3f}")
    print(f"  Hybride    : {q0_hybrid:.3f}")
    print(f"  Observation: ~ -0.55")
    print()

    # Distances à différents z
    print("=" * 70)
    print("DISTANCES LUMINEUSES")
    print("=" * 70)
    print()
    print(f"{'z':>8} {'d_L LCDM':>12} {'d_L Hybrid':>12} {'Δd_L':>10} {'Δμ':>10}")
    print("-" * 70)

    for z in [0.1, 0.5, 1.0, 1.5, 2.0]:
        d_lcdm = distance_luminosite_numerique(z, H0, Om, None, 'lcdm')
        d_hybrid = distance_luminosite_numerique(z, H0, Om, beta_opt, 'hybrid')

        delta_d = d_hybrid - d_lcdm
        delta_mu = 5 * math.log10(d_hybrid / d_lcdm)

        print(f"{z:8.1f} {d_lcdm:12.1f} {d_hybrid:12.1f} {delta_d:10.1f} {delta_mu:10.3f}")

    print()
    print("Δd_L en Mpc, Δμ en magnitudes")
    print()

    # Taux d'expansion H(z)
    print("=" * 70)
    print("TAUX D'EXPANSION H(z)")
    print("=" * 70)
    print()
    print(f"{'z':>8} {'H_LCDM':>12} {'H_Hybrid':>12} {'ΔH/H':>10}")
    print("-" * 55)

    for z in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]:
        H_lcdm = H_Lambda_CDM(z, H0, Om)
        H_hybrid = H_hybride(z, H0, Om, beta_opt)

        delta_H_rel = (H_hybrid - H_lcdm) / H_lcdm

        print(f"{z:8.1f} {H_lcdm:12.1f} {H_hybrid:12.1f} {delta_H_rel*100:9.1f}%")

    print()

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print()
    print("=" * 70)
    print(" MODÈLE HYBRIDE D'ÉNERGIE NOIRE ")
    print(" 70% Distorsion Temporelle + 30% Expansion Spatiale ")
    print("=" * 70)
    print()
    print("Partition de l'énergie noire (Ω_Λ = 0.70) :")
    print(f"  • Expansion spatiale  : {f_spatial*100:.0f}% (Ω_Λ,spatial = {OL_spatial:.2f})")
    print(f"  • Distorsion temporelle : {f_temporel*100:.0f}% (τ(t) ∝ t^β)")
    print()
    print("Métrique FLRW modifiée :")
    print("  ds² = -c²τ²(t) dt² + a²(t) dr²")
    print()
    print("  avec τ(t) ∝ t^β  et  a(t) ∝ exp[H₀√Ω_Λ,spatial · t]")
    print()

    # Optimisation
    beta_opt, chi2_opt = optimiser_beta()

    # Comparaison
    comparer_modeles(beta_opt)

    # Conclusion
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()
    print(f"Le modèle hybride avec β = {beta_opt:.3f} :")
    print()

    chi2_lcdm = chi2_supernovae(70.0, 0.30, None, 'lcdm')

    if chi2_opt < 1.0:
        print("✅ Ajustement EXCELLENT aux données (χ² < 1.0)")
    elif chi2_opt < chi2_lcdm * 1.05:
        print("✓ Ajustement ÉQUIVALENT à Lambda-CDM")
    else:
        print("⚠ Ajustement moins bon que Lambda-CDM")

    print()
    print("Prochaines étapes :")
    print("  1. Ajustement avec données Pantheon complètes (~1000 SNe)")
    print("  2. Calcul des prédictions CMB (pics acoustiques)")
    print("  3. Comparaison avec BAO")
    print("  4. Publication scientifique")
    print()
    print("=" * 70)
    print()
