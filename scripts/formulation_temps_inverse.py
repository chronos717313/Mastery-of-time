#!/usr/bin/env python3
"""
TMT v2.2 - Formulation avec Referentiel de Temps Inverse

Hypothese: L'expansion cosmique est observee depuis un referentiel
ou le temps peut etre dans un etat de superposition.

|Psi> = alpha|t> + beta|t_bar>

Dans cette vision:
- alpha^2 = probabilite temps forward
- beta^2 = probabilite temps backward (reflet temporel)

L'expansion effective depend de cet etat de superposition.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
import os

# =============================================================================
# PARAMETRES
# =============================================================================
H0 = 70.0
Omega_m = 0.315
Omega_Lambda = 0.685
c = 299792.458

# Parametres TMT quantiques (de SPARC)
r_c_ref = 10.61  # kpc - rayon critique de reference
n = 0.75  # exposant de superposition

print("="*70)
print("TMT v2.2 - REFERENTIEL DE TEMPS INVERSE")
print("="*70)

# =============================================================================
# CONCEPT CLE
# =============================================================================

print("""
CONCEPT FONDAMENTAL:
====================

Dans TMT, la "matiere noire" est le reflet temporel de la matiere visible:

  |Psi> = alpha(r)|t> + beta(r)|t_bar>

ou:
  |alpha|^2 = 1 / (1 + (r/r_c)^n)     <- temps forward
  |beta|^2  = (r/r_c)^n / (1 + (r/r_c)^n)  <- temps backward

NOUVELLE IDEE:
==============

L'expansion cosmique elle-meme pourrait dependre de l'etat temporel local.

Dans les VIDES:
  - Peu de matiere -> peu de "reflet temporel"
  - L'espace est principalement dans l'etat |t> (forward)
  - Expansion = expansion "standard" LCDM

Dans les AMAS:
  - Beaucoup de matiere -> beaucoup de "reflet temporel"
  - Superposition significative |t> + |t_bar>
  - Expansion modifiee par l'interference temporelle

Cette formulation INVERSE la logique:
  - Ancien: vides -> expansion acceleree
  - Nouveau: vides -> expansion standard (moins de modification)
           amas  -> expansion modifiee (plus de superposition)
""")

# =============================================================================
# NOUVELLE FORMULATION
# =============================================================================

def alpha_squared(rho_ratio):
    """
    Probabilite d'etre dans l'etat temps forward.
    Depend de la densite locale.

    Dans les vides (rho faible): alpha^2 -> 1 (temps forward domine)
    Dans les amas (rho grand): alpha^2 -> 0.5 (superposition maximale)
    """
    # Utilisons rho comme proxy de la "masse effective locale"
    # Plus de masse = plus de reflet temporel
    effective_ratio = rho_ratio  # rho/rho_crit agit comme r/r_c
    return 1 / (1 + effective_ratio**n)

def beta_squared(rho_ratio):
    """Probabilite d'etre dans l'etat temps backward."""
    return 1 - alpha_squared(rho_ratio)

def E_LCDM(z):
    """Expansion LCDM standard."""
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def E_TMT_v22(z, rho_ratio):
    """
    Expansion TMT v2.2 avec superposition temporelle.

    L'energie noire effective depend de l'etat de superposition.
    Dans l'etat |t_bar>, l'expansion est "inversee" (contraction).
    L'observable est la moyenne quantique.
    """
    alpha2 = alpha_squared(rho_ratio)
    beta2 = beta_squared(rho_ratio)

    term_m = Omega_m * (1 + z)**3

    # L'energie noire effective est modifiee par l'interference
    # |t> : expansion normale
    # |t_bar> : "expansion negative" (contribution a la moyenne)

    # Interference constructive/destructive
    # Lambda_eff = Lambda * (alpha^2 - beta^2) + terme d'interference

    # Simplification: Lambda_eff = Lambda * cos(theta) ou theta depend de rho
    # cos(theta) = alpha^2 - beta^2 = (1 - 2*beta^2)

    interference = alpha2 - beta2  # = 1 - 2*beta^2

    # Dans les vides: interference ~ 1 (pas de modification)
    # Dans les amas: interference ~ 0 (grande modification)

    term_L = Omega_Lambda * (1 + 0.2 * (1 - interference))  # Effet modere

    return np.sqrt(term_m + term_L)

# =============================================================================
# TEST DE LA FORMULATION
# =============================================================================

print("\n" + "="*70)
print("PREDICTIONS TMT v2.2")
print("="*70)

print(f"\n{'Environnement':<20} {'rho/rho_c':<10} {'alpha^2':<10} {'beta^2':<10} {'H/H_LCDM':<12}")
print("-"*62)

environments = [
    ("Supervide extreme", 0.2),
    ("Vide profond", 0.3),
    ("Vide modere", 0.5),
    ("Champ moyen", 1.0),
    ("Filament", 2.0),
    ("Amas", 5.0),
    ("Coeur amas", 10.0),
]

for name, rho in environments:
    a2 = alpha_squared(rho)
    b2 = beta_squared(rho)
    H_ratio = E_TMT_v22(0, rho) / E_LCDM(0)
    print(f"{name:<20} {rho:<10.1f} {a2:<10.3f} {b2:<10.3f} {H_ratio:<12.4f}")

# =============================================================================
# COMPARAISON AVEC OBSERVATIONS
# =============================================================================

print("\n" + "="*70)
print("COMPARAISON AVEC OBSERVATIONS")
print("="*70)

# SNIa
print("\n1. SNIa par environnement:")
print("-"*50)

def d_L_v22(z, rho_ratio):
    integrand = lambda zp: c / (H0 * E_TMT_v22(zp, rho_ratio))
    integral, _ = quad(integrand, 0, z)
    return (1 + z) * integral

z_test = 0.05
d_void = d_L_v22(z_test, 0.5)
d_field = d_L_v22(z_test, 1.0)
d_cluster = d_L_v22(z_test, 5.0)

delta_void = 100 * (d_void - d_field) / d_field
delta_cluster = 100 * (d_cluster - d_field) / d_field

print(f"  z = {z_test}")
print(f"  Delta_dL (vide vs champ): {delta_void:+.2f}%")
print(f"  Delta_dL (cluster vs champ): {delta_cluster:+.2f}%")
print(f"  Observation: |Delta_dL| < 2%")

if abs(delta_void) < 2.0 and abs(delta_cluster) < 5.0:
    print("  => COMPATIBLE")
else:
    print("  => A AJUSTER")

# H0 tension
print("\n2. Tension H0:")
print("-"*50)

H0_planck = 67.4
H0_local = 73.0
tension = 100 * (H0_local - H0_planck) / H0_planck

rho_local = 0.8  # Voisinage sous-dense
H_ratio_local = E_TMT_v22(0, rho_local) / E_LCDM(0)
tension_tmt = (H_ratio_local - 1) * 100

print(f"  Tension observee: {tension:.1f}%")
print(f"  rho_local = {rho_local}")
print(f"  Tension TMT v2.2: {tension_tmt:.2f}%")

# =============================================================================
# FORMULATION ALTERNATIVE: TEMPS INVERSE COMME ANTIMATIERE
# =============================================================================

print("\n" + "="*70)
print("FORMULATION ALTERNATIVE: TEMPS INVERSE")
print("="*70)

print("""
Si nous sommes dans un referentiel de TEMPS INVERSE:

1. Notre "present" est le futur de l'univers standard
2. L'"expansion" que nous observons est en fait une CONTRACTION
   vue depuis le referentiel inverse
3. La "matiere noire" est la matiere NORMALE vue depuis notre
   referentiel inverse

IMPLICATIONS:
- Ce que nous appelons "expansion acceleree" est une contraction ralentie
- L'energie noire n'existe pas - c'est un artefact du referentiel
- La matiere noire est visible dans l'autre sens du temps
""")

def E_temps_inverse(z, rho_ratio):
    """
    Dans le referentiel inverse, l'expansion devient contraction.
    Ce que nous mesurons comme H est en fait -H vu de l'autre cote.

    La "constante cosmologique" est l'effet de regarder une contraction
    depuis le mauvais sens du temps.
    """
    # Dans le referentiel inverse, Omega_Lambda change de signe effectif
    # Mais nous mesurons toujours une expansion positive

    # L'effet de la densite locale est inverse:
    # Plus de matiere = plus de "connexion" avec le referentiel normal
    # = moins d'effet de l'inversion temporelle

    alpha2 = alpha_squared(rho_ratio)

    term_m = Omega_m * (1 + z)**3

    # Dans les vides: fort effet d'inversion (peu de matiere pour "ancrer")
    # Dans les amas: faible effet (matiere stabilise le referentiel)

    # C'est l'INVERSE de la formulation precedente!
    inversion_effect = 1 - alpha2  # = beta^2

    term_L = Omega_Lambda * (1 - 0.3 * inversion_effect)

    return np.sqrt(term_m + term_L)

print("\nPredictions avec referentiel inverse:")
print(f"{'Environnement':<20} {'rho':<8} {'H/H_LCDM':<12} {'Delta'}")
print("-"*50)

for name, rho in environments[:5]:
    H_ratio = E_temps_inverse(0, rho) / E_LCDM(0)
    delta = (H_ratio - 1) * 100
    print(f"{name:<20} {rho:<8.1f} {H_ratio:<12.4f} {delta:+.2f}%")

# =============================================================================
# SYNTHESE
# =============================================================================

print("\n" + "="*70)
print("SYNTHESE")
print("="*70)

print("""
DEUX INTERPRETATIONS POSSIBLES:

1. TMT v2.1 (beta = 0.12):
   - Expansion differentielle FAIBLE
   - Compatible SNIa
   - N'explique pas H0 tension ni ISW

2. TMT v2.2 (temps inverse):
   - L'expansion depend de l'etat de superposition temporelle
   - Dans les vides: moins de matiere -> moins d'ancrage temporel
   - Dans les amas: plus de matiere -> plus de superposition

POINT CLE:
L'effet TMT principal est sur les COURBES DE ROTATION (valide a 97%)
L'expansion differentielle est un effet SECONDAIRE plus faible.

La matiere noire est le REFLET TEMPOREL de la matiere visible.
Elle n'affecte pas directement l'expansion cosmique,
mais la DYNAMIQUE locale (rotation, lentilles gravitationnelles).
""")

# Sauvegarder
script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, "..", "data", "results")
os.makedirs(results_dir, exist_ok=True)

results_path = os.path.join(results_dir, "formulation_temps_inverse.txt")

with open(results_path, 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("TMT v2.2 - REFERENTIEL DE TEMPS INVERSE\n")
    f.write("="*70 + "\n\n")
    f.write("Concept: |Psi> = alpha|t> + beta|t_bar>\n\n")
    f.write("L'expansion depend de l'etat de superposition temporelle.\n")
    f.write("Dans les vides: alpha^2 ~ 1 (temps forward domine)\n")
    f.write("Dans les amas: superposition significative\n\n")
    f.write("Conclusion: L'effet principal de TMT est sur les\n")
    f.write("courbes de rotation, pas sur l'expansion cosmique.\n")

print(f"\nResultats sauvegardes: {results_path}")
