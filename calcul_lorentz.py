#!/usr/bin/env python3
"""
Calcul des facteurs de Lorentz aux différentes échelles cosmologiques
Pour la théorie de Maîtrise du Temps
"""

import math

# Constante : vitesse de la lumière
c = 299792.458  # km/s

# Vitesses aux différentes échelles
vitesses = {
    "Rotation Terre (équateur)": 0.465,
    "Révolution Terre autour Soleil": 29.78,
    "Soleil → Centre Galactique": 220,
    "Voie Lactée → CMB": 600,
    "Amas galactiques (rapides)": 1000,
    "Quasar rapide (exemple)": 10000,  # ~0.033c
}

def calcul_lorentz(v):
    """
    Calcule le facteur de Lorentz et la dilatation temporelle

    Args:
        v: vitesse en km/s

    Returns:
        tuple: (beta, gamma, gamma-1, approximation)
    """
    beta = v / c
    if beta >= 1:
        return None, None, None, None

    gamma = 1 / math.sqrt(1 - beta**2)
    gamma_minus_1 = gamma - 1
    approximation = 0.5 * beta**2

    return beta, gamma, gamma_minus_1, approximation

def temps_pour_1_seconde(gamma_minus_1):
    """
    Calcule le temps nécessaire pour accumuler 1 seconde de décalage

    Args:
        gamma_minus_1: facteur γ-1

    Returns:
        float: temps en secondes
    """
    if gamma_minus_1 > 0:
        return 1 / gamma_minus_1
    return float('inf')

print("=" * 90)
print("FACTEURS DE LORENTZ AUX DIFFÉRENTES ÉCHELLES COSMOLOGIQUES")
print("=" * 90)
print()

print(f"{'Système':<35} {'v (km/s)':<12} {'v/c':<14} {'γ-1':<14}")
print("-" * 90)

for nom, v in vitesses.items():
    beta, gamma, gamma_minus_1, approx = calcul_lorentz(v)

    if beta is None:
        print(f"{nom:<35} {v:<12.3f} RELATIVISTE (v >= c)")
        continue

    print(f"{nom:<35} {v:<12.3f} {beta:<14.6e} {gamma_minus_1:<14.6e}")

    # Temps pour accumuler 1 seconde
    t_secondes = temps_pour_1_seconde(gamma_minus_1)
    t_jours = t_secondes / 86400
    t_annees = t_jours / 365.25

    if t_annees > 1:
        print(f"  → 1 seconde de décalage en {t_annees:.2f} ans")
    elif t_jours > 1:
        print(f"  → 1 seconde de décalage en {t_jours:.2f} jours")
    else:
        print(f"  → 1 seconde de décalage en {t_secondes:.2f} secondes")

    # Vérification de l'approximation
    erreur_relative = abs(gamma_minus_1 - approx) / gamma_minus_1 * 100
    if erreur_relative < 0.01:
        print(f"  ✓ Approximation v²/2c² excellente (erreur: {erreur_relative:.4f}%)")
    else:
        print(f"  ⚠ Approximation v²/2c² imprécise (erreur: {erreur_relative:.2f}%)")
    print()

print("=" * 90)
print("\nCOMPARAISON AVEC EFFETS GRAVITATIONNELS")
print("=" * 90)
print()

# Dilatation gravitationnelle à la surface de la Terre
G = 6.674e-11  # m³ kg⁻¹ s⁻²
M_terre = 5.972e24  # kg
R_terre = 6.371e6  # m
c_ms = 299792458  # m/s

dilatation_grav_terre = (G * M_terre) / (R_terre * c_ms**2)
print(f"Dilatation gravitationnelle à la surface Terre : {dilatation_grav_terre:.4e}")

# Comparaison
beta_rot, _, gamma_rot, _ = calcul_lorentz(vitesses["Rotation Terre (équateur)"])
beta_rev, _, gamma_rev, _ = calcul_lorentz(vitesses["Révolution Terre autour Soleil"])

ratio_grav_rotation = dilatation_grav_terre / gamma_rot
ratio_grav_revolution = dilatation_grav_terre / gamma_rev

print(f"Dilatation rotation Terre            : {gamma_rot:.4e}")
print(f"Dilatation révolution Terre          : {gamma_rev:.4e}")
print()
print(f"Gravité / Rotation   = {ratio_grav_rotation:.2f}× (gravité domine)")
print(f"Gravité / Révolution = {ratio_grav_revolution:.2f}× ", end="")
if ratio_grav_revolution > 1:
    print("(gravité domine)")
else:
    print("(cinématique domine)")

print()
print("=" * 90)
print("\nEFFET CUMULATIF DES VITESSES")
print("=" * 90)
print()

# Pour un observateur sur Terre
v_rot = vitesses["Rotation Terre (équateur)"]
v_rev = vitesses["Révolution Terre autour Soleil"]
v_gal = vitesses["Soleil → Centre Galactique"]
v_cmb = vitesses["Voie Lactée → CMB"]

# Composition naïve (addition quadratique - approximation)
v_total_quad = math.sqrt(v_rot**2 + v_rev**2 + v_gal**2 + v_cmb**2)

print("Observateur sur Terre - Composition des vitesses:")
print(f"  Rotation Terre       : {v_rot:>8.3f} km/s")
print(f"  Révolution Terre     : {v_rev:>8.3f} km/s")
print(f"  Mouvement Galactique : {v_gal:>8.3f} km/s")
print(f"  Mouvement CMB        : {v_cmb:>8.3f} km/s")
print(f"  ─────────────────────────────────")
print(f"  Total (quadratique)  : {v_total_quad:>8.3f} km/s")
print()

beta_total, gamma_total, gamma_total_m1, _ = calcul_lorentz(v_total_quad)
print(f"Facteur de Lorentz total : γ - 1 = {gamma_total_m1:.6e}")
print()

# Somme des effets individuels
effets_individuels = (
    calcul_lorentz(v_rot)[2] +
    calcul_lorentz(v_rev)[2] +
    calcul_lorentz(v_gal)[2] +
    calcul_lorentz(v_cmb)[2]
)

print(f"Somme des effets individuels : {effets_individuels:.6e}")
print(f"Différence : {abs(gamma_total_m1 - effets_individuels)/gamma_total_m1 * 100:.2f}%")
print()
print("Note: La différence vient de la non-linéarité de la composition relativiste")
print("      et de la nature vectorielle des vitesses (angles non pris en compte)")

print()
print("=" * 90)
print("\nQUESTIONS POUR LA THÉORIE")
print("=" * 90)
print()
print("1. Votre distorsion temporelle τ(r) ∝ 1/r² est-elle:")
print("   a) Additionnelle aux effets de Lorentz γ(v) ?")
print("   b) Une réinterprétation des effets de Lorentz ?")
print("   c) Dominante à grande échelle cosmologique ?")
print()
print("2. Par rapport à quel référentiel mesurez-vous la distorsion ?")
print("   a) CMB (référentiel cosmologique)")
print("   b) Centre galactique")
print("   c) Chaque masse définit son propre référentiel")
print()
print("3. Comment composez-vous les effets à différentes échelles ?")
print("   a) Addition simple")
print("   b) Composition relativiste")
print("   c) Effet dominant seulement")
print()
print("4. Les horloges atomiques peuvent mesurer des effets > 10⁻¹⁶")
print("   Votre théorie prédit-elle des effets mesurables dans le système solaire ?")
print()
print("=" * 90)
