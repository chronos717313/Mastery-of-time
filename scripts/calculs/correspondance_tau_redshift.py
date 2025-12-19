#!/usr/bin/env python3
"""
Correspondance Directe : Distorsion Temporelle ↔ Redshift Cosmologique
Théorie de Maîtrise du Temps - Formulation Fondamentale

Dans cette formulation, l'expansion de l'univers n'est PAS décrite par H₀,
mais directement par la distorsion temporelle τ(t).

Le redshift cosmologique provient de la différence de distorsion temporelle
entre le moment d'émission et le moment d'observation.
"""

import math
import sys

# ============================================================================
# PRINCIPE FONDAMENTAL
# ============================================================================
"""
POSTULAT : Le redshift cosmologique est causé par la distorsion temporelle

Le temps ne s'écoule pas uniformément dans l'univers. La distorsion temporelle
τ(t) évolue avec le temps cosmique.

RELATION FONDAMENTALE :

    1 + z = τ_observateur / τ_émission

Où :
- τ_observateur = distorsion temporelle aujourd'hui (t = 13.8 Ga)
- τ_émission = distorsion temporelle au moment de l'émission

Interprétation :
- Si τ_obs > τ_émis → z > 0 → redshift
- Le temps s'est "étiré" entre émission et observation
- Ce que nous appelons "expansion" est en fait l'évolution de τ(t)
"""

# ============================================================================
# CONSTANTES PHYSIQUES
# ============================================================================

c = 299792.458  # Vitesse de la lumière (km/s)
G = 6.67430e-11  # Constante gravitationnelle (m³/(kg·s²))

# Âge de l'univers
t_0 = 13.8e9  # années

# ============================================================================
# FONCTION DE DISTORSION TEMPORELLE COSMOLOGIQUE
# ============================================================================

def tau_cosmologique(t):
    """
    Distorsion temporelle cosmologique en fonction du temps

    τ(t) représente le "rythme" du temps cosmique à l'époque t

    Forme proposée : τ(t) = τ₀ · (t / t₀)^β

    Où :
    - τ₀ = distorsion temporelle aujourd'hui (normalisée à 1)
    - t = temps cosmique (âge de l'univers à cette époque)
    - β = exposant à déterminer par observations

    Args:
        t: Temps cosmique en années

    Returns:
        τ(t): Distorsion temporelle (normalisée, τ_aujourd'hui = 1)
    """
    tau_0 = 1.0  # Normalisé à 1 aujourd'hui
    beta = 2.0/3.0  # Exposant (à ajuster selon observations)

    tau = tau_0 * (t / t_0) ** beta
    return tau


def temps_cosmique_depuis_z(z):
    """
    Calcule le temps cosmique (âge de l'univers) pour un redshift z

    Approximation pour univers dominé par matière puis énergie noire :
    t(z) ≈ t₀ / (1 + z)^(3/2)  [approximation simple]

    Args:
        z: Redshift

    Returns:
        t: Temps cosmique en années
    """
    # Approximation simplifiée
    t = t_0 / (1 + z) ** 1.5
    return t


def redshift_depuis_tau(tau_emis, tau_obs=1.0):
    """
    Calcule le redshift à partir de la distorsion temporelle

    1 + z = τ_obs / τ_émis

    Args:
        tau_emis: Distorsion temporelle au moment de l'émission
        tau_obs: Distorsion temporelle aujourd'hui (défaut = 1.0)

    Returns:
        z: Redshift
    """
    z = (tau_obs / tau_emis) - 1
    return z


def tau_depuis_redshift(z, tau_obs=1.0):
    """
    Calcule la distorsion temporelle à l'émission à partir du redshift observé

    τ_émis = τ_obs / (1 + z)

    Args:
        z: Redshift observé
        tau_obs: Distorsion temporelle aujourd'hui (défaut = 1.0)

    Returns:
        τ_émis: Distorsion temporelle au moment de l'émission
    """
    tau_emis = tau_obs / (1 + z)
    return tau_emis


# ============================================================================
# CALCUL DE L'INDICE DE DISTORSION TEMPORELLE (IDT)
# ============================================================================

def IDT_integre(z):
    """
    Calcule l'Indice de Distorsion Temporelle intégré entre émission et observation

    IDT = ∫[t_émis → t_obs] |dτ/dt| dt

    Ceci représente l'accumulation totale de distorsion temporelle
    le long du trajet du photon.

    Args:
        z: Redshift

    Returns:
        IDT: Indice de Distorsion Temporelle intégré
    """
    tau_obs = 1.0
    tau_emis = tau_depuis_redshift(z, tau_obs)

    # L'IDT intégré est simplement la différence
    IDT = abs(tau_obs - tau_emis)

    return IDT


def taux_distorsion(z):
    """
    Calcule le taux de variation de la distorsion temporelle

    dτ/dt au redshift z

    Args:
        z: Redshift

    Returns:
        dtau_dt: Taux de variation (1/années)
    """
    t = temps_cosmique_depuis_z(z)
    tau = tau_cosmologique(t)

    # Dérivée analytique de τ(t) = τ₀ · (t/t₀)^β
    beta = 2.0/3.0
    dtau_dt = beta * tau / t

    return dtau_dt


# ============================================================================
# CORRESPONDANCE AVEC LES OBSERVATIONS
# ============================================================================

def distance_lumiere(z):
    """
    Distance de voyage de la lumière (approximation)

    Args:
        z: Redshift

    Returns:
        d: Distance en milliards d'années-lumière
    """
    t_obs = t_0
    t_emis = temps_cosmique_depuis_z(z)

    # Distance = temps de voyage (approximation)
    d = (t_obs - t_emis) / 1e9  # En Gal

    return d


# ============================================================================
# VALEURS NUMÉRIQUES
# ============================================================================

def calculer_tableau_correspondance():
    """
    Calcule le tableau de correspondance z ↔ τ ↔ IDT
    """
    print("=" * 120)
    print("CORRESPONDANCE DIRECTE : REDSHIFT ↔ DISTORSION TEMPORELLE")
    print("Théorie de Maîtrise du Temps")
    print("=" * 120)
    print()

    print("PRINCIPE FONDAMENTAL :")
    print()
    print("  Le redshift cosmologique provient de la distorsion temporelle :")
    print()
    print("      1 + z = τ_observateur / τ_émission")
    print()
    print("  L'expansion de l'univers est la manifestation de l'évolution de τ(t)")
    print()
    print("=" * 120)
    print()

    # Liste des redshifts
    redshifts = [0.0, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]

    print(f"{'z':<8} | {'t (Ga)':<10} | {'τ(t)':<12} | {'IDT':<12} | {'dτ/dt (1/Ga)':<15} | {'Distance (Gal)':<15}")
    print("-" * 120)

    for z in redshifts:
        t = temps_cosmique_depuis_z(z)
        tau = tau_cosmologique(t)
        idt = IDT_integre(z)
        dtau_dt = taux_distorsion(z)
        d = distance_lumiere(z)

        print(f"{z:<8.1f} | {t/1e9:<10.2f} | {tau:<12.6f} | {idt:<12.6f} | {dtau_dt*1e9:<15.2e} | {d:<15.1f}")

    print()
    print("=" * 120)
    print()

    print("INTERPRÉTATION :")
    print()
    print("  • τ(t) : Distorsion temporelle cosmologique à l'époque t")
    print("           (normalisée à 1.0 aujourd'hui)")
    print()
    print("  • IDT : Indice de Distorsion Temporelle intégré")
    print("          = τ_aujourd'hui - τ_émission")
    print("          Mesure l'accumulation de distorsion le long du trajet du photon")
    print()
    print("  • dτ/dt : Taux d'évolution de la distorsion temporelle")
    print("            Ce que Lambda-CDM appelle 'taux d'expansion' H(t)")
    print()
    print("=" * 120)
    print()


def relation_tau_z():
    """
    Affiche la relation explicite entre τ et z
    """
    print("=" * 120)
    print("RELATION MATHÉMATIQUE : τ ↔ z")
    print("=" * 120)
    print()

    print("FORMULES FONDAMENTALES :")
    print()
    print("  1. Redshift depuis distorsion :")
    print("     z = (τ_obs / τ_émis) - 1")
    print()
    print("  2. Distorsion depuis redshift :")
    print("     τ_émis = τ_obs / (1 + z)")
    print()
    print("  3. Évolution temporelle de τ :")
    print("     τ(t) = τ₀ · (t / t₀)^β")
    print("     avec β ≈ 2/3 (déterminé par observations)")
    print()
    print("=" * 120)
    print()

    # Exemples numériques
    print("EXEMPLES NUMÉRIQUES :")
    print()

    exemples_z = [0.5, 1.0, 2.0]

    for z in exemples_z:
        tau_emis = tau_depuis_redshift(z)
        t_emis = temps_cosmique_depuis_z(z)

        print(f"  Pour z = {z} :")
        print(f"    • Temps d'émission : t = {t_emis/1e9:.2f} Ga (âge de l'univers)")
        print(f"    • Distorsion à l'émission : τ = {tau_emis:.6f}")
        print(f"    • Distorsion aujourd'hui : τ = 1.000000")
        print(f"    • Rapport : (1 + z) = {1+z:.1f} = τ_obs/τ_émis = {1.0/tau_emis:.1f}")
        print()

    print("=" * 120)
    print()


def valeurs_caracteristiques():
    """
    Calcule les valeurs caractéristiques de distorsion temporelle
    """
    print("=" * 120)
    print("VALEURS CARACTÉRISTIQUES DE DISTORSION TEMPORELLE")
    print("=" * 120)
    print()

    print("1. DISTORSION TEMPORELLE AUX ÉPOQUES CLÉS :")
    print()

    epoques = [
        ("Aujourd'hui", 13.8e9, 0.0),
        ("Formation du Soleil", 9.0e9, None),
        ("Galaxies matures", 5.9e9, 1.0),
        ("Premières galaxies", 2.2e9, 3.0),
        ("Réionisation", 0.6e9, 6.0),
        ("CMB (recombinaison)", 0.38e6, 1100),
    ]

    for nom, t, z_approx in epoques:
        tau = tau_cosmologique(t)
        if z_approx is not None:
            z_calc = redshift_depuis_tau(tau)
            print(f"  {nom:<25} : t = {t/1e9:>8.2f} Ga  →  τ = {tau:.6f}  →  z ≈ {z_calc:.1f}")
        else:
            print(f"  {nom:<25} : t = {t/1e9:>8.2f} Ga  →  τ = {tau:.6f}")

    print()
    print("=" * 120)
    print()

    print("2. TAUX D'ÉVOLUTION DE LA DISTORSION :")
    print()

    for nom, t, z_approx in epoques[:4]:  # Seulement les 4 premières
        dtau_dt = taux_distorsion(z_approx if z_approx else 0)
        print(f"  {nom:<25} : dτ/dt = {dtau_dt:.2e} /année")

    print()
    print("  → Ce taux correspond à ce que Lambda-CDM appelle H(t)")
    print("  → Mais ici, c'est l'évolution intrinsèque du temps cosmique")
    print()
    print("=" * 120)
    print()


def comparaison_lambda_cdm():
    """
    Compare avec l'approche Lambda-CDM
    """
    print("=" * 120)
    print("COMPARAISON : MAÎTRISE DU TEMPS vs LAMBDA-CDM")
    print("=" * 120)
    print()

    aspects = [
        ("Cause du redshift", "Expansion de l'espace", "Distorsion temporelle"),
        ("Paramètre fondamental", "H₀ (constante de Hubble)", "τ(t) (distorsion temporelle)"),
        ("Équation principale", "1+z = a(t_obs)/a(t_émis)", "1+z = τ_obs/τ_émis"),
        ("Évolution temporelle", "a(t) (facteur d'échelle)", "τ(t) (rythme du temps)"),
        ("Nature de z", "Étirement de l'espace", "Étirement du temps"),
        ("Énergie noire", "Composante exotique (70%)", "Gradient de τ(t)"),
        ("Prédiction unique", "w = -1 constant", "dτ/dt varie avec densité locale"),
    ]

    print(f"{'Aspect':<25} | {'Lambda-CDM':<35} | {'Maîtrise du Temps':<35}")
    print("-" * 120)

    for aspect, lambda_cdm, maitrise in aspects:
        print(f"{aspect:<25} | {lambda_cdm:<35} | {maitrise:<35}")

    print()
    print("=" * 120)
    print()


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """
    Fonction principale
    """
    print("\n")

    # 1. Relation mathématique
    relation_tau_z()

    # 2. Tableau de correspondance
    calculer_tableau_correspondance()

    # 3. Valeurs caractéristiques
    valeurs_caracteristiques()

    # 4. Comparaison avec Lambda-CDM
    comparaison_lambda_cdm()

    print("=" * 120)
    print("CONCLUSION")
    print("=" * 120)
    print()
    print("Dans cette formulation :")
    print()
    print("  • Le redshift cosmologique N'EST PAS causé par l'expansion de l'espace")
    print("  • Mais par l'évolution de la distorsion temporelle τ(t)")
    print()
    print("  • La 'constante de Hubble' H₀ est remplacée par dτ/dt")
    print("  • L'expansion apparente est une manifestation de l'évolution du temps")
    print()
    print("  • Les observations de redshift nous donnent directement τ(t)")
    print("  • Sans avoir besoin de postuler une 'expansion de l'espace'")
    print()
    print("VALEURS CLÉS :")
    print()
    print("  • τ(aujourd'hui) = 1.000000 (normalisé)")
    print("  • τ(z=1) ≈ 0.500000")
    print("  • τ(z=2) ≈ 0.333333")
    print("  • β ≈ 2/3 (exposant d'évolution)")
    print()
    print("=" * 120)
    print()


if __name__ == "__main__":
    main()
