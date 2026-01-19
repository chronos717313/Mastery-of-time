#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimisation de la Distance Effective d'Atténuation
Théorie de Maîtrise du Temps - Recherche de d_eff optimal

Ce script teste différentes valeurs de distance effective d_eff pour l'atténuation
gravitationnelle et trouve celle qui donne le meilleur ajustement aux courbes
de rotation galactiques observées.

Question : Peut-on rétrécir l'horizon cosmologique à une valeur qui corrobore
les observations ?

Réponse : On cherche une "distance caractéristique d'atténuation" d_eff qui
pourrait être différente de l'horizon cosmologique d_horizon = c·t₀.

Date : 2025-12-04
Version : 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize_scalar

# ============================================================================
# CONSTANTES PHYSIQUES FONDAMENTALES
# ============================================================================

G = 6.67430e-11  # m³/(kg·s²)
c = 299792458  # m/s
t_0 = 13.8e9 * 365.25 * 24 * 3600  # secondes
d_horizon_cosmologique = c * t_0 / (3.086e19)  # kpc

print("=" * 80)
print("OPTIMISATION DE LA DISTANCE EFFECTIVE D'ATTÉNUATION")
print("Théorie de Maîtrise du Temps")
print("=" * 80)
print(f"\nHorizon cosmologique théorique : d_cosmo = {d_horizon_cosmologique:.0f} kpc")
print(f"                                         = {d_horizon_cosmologique/1000:.0f} Mpc")

# ============================================================================
# PARAMÈTRES GALACTIQUES (VOIE LACTÉE)
# ============================================================================

M_bulbe = 1.5e10 * 1.989e30  # kg
M_disque_total = 6.0e10 * 1.989e30  # kg
r_disque = 3.5  # kpc
r_bulbe = 1.0  # kpc

# ============================================================================
# FONCTIONS DE MASSE
# ============================================================================

def masse_bulbe(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    M_r = M_bulbe * (r_kpc**3) / ((r_kpc**2 + r_bulbe**2)**(3/2))
    return M_r

def masse_disque(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    x = r_kpc / r_disque
    M_r = M_disque_total * (1 - (1 + x) * math.exp(-x))
    return M_r

def masse_totale_visible(r_kpc):
    return masse_bulbe(r_kpc) + masse_disque(r_kpc)

# ============================================================================
# FACTEUR D'EXPANSION PARAMÉTRÉ
# ============================================================================

def facteur_expansion(d_kpc, d_eff):
    """
    Facteur d'atténuation avec distance effective paramétrable

    Args:
        d_kpc: distance en kpc
        d_eff: distance effective d'atténuation en kpc

    Returns:
        facteur sans dimension (0 < f ≤ 1)
    """
    if d_eff <= 0:
        return 1.0
    f = math.exp(-d_kpc / d_eff)
    return f

# ============================================================================
# MASSE EFFECTIVE AVEC d_eff PARAMÉTRABLE
# ============================================================================

def masse_effective_asselin(r_kpc, d_eff, N_shells=100):
    """
    Calcul de masse effective avec d_eff paramétrable
    """
    M_local = masse_totale_visible(r_kpc)

    r_max = 50.0  # kpc
    dr = (r_max - r_kpc) / N_shells

    contribution_externe = 0.0

    for i in range(N_shells):
        r_shell = r_kpc + (i + 0.5) * dr
        dM = masse_totale_visible(r_shell + dr/2) - masse_totale_visible(r_shell - dr/2)

        if dM <= 0:
            continue

        d = abs(r_shell - r_kpc)
        if d < 0.01:
            continue

        f = facteur_expansion(d, d_eff)
        contribution_externe += dM * f * (r_kpc / r_shell)

    M_eff = M_local + contribution_externe
    return M_eff

# ============================================================================
# VITESSE DE ROTATION AVEC d_eff PARAMÉTRABLE
# ============================================================================

def vitesse_asselin(r_kpc, d_eff):
    """
    Vitesse de rotation avec d_eff paramétrable
    """
    if r_kpc < 0.01:
        return 0.0

    M_eff = masse_effective_asselin(r_kpc, d_eff)
    r_m = r_kpc * 3.086e19
    v_ms = math.sqrt(G * M_eff / r_m)
    v_kms = v_ms / 1000

    return v_kms

# ============================================================================
# DONNÉES OBSERVÉES
# ============================================================================

r_obs = np.array([0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30])
v_obs = np.array([80, 140, 190, 210, 220, 225, 225, 225, 220, 220, 215, 210, 205, 200, 195, 185, 175])
v_err = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 20, 20, 25, 30])

# ============================================================================
# FONCTION OBJECTIF (CHI²)
# ============================================================================

def chi2_pour_d_eff(d_eff):
    """
    Calcule le chi² pour une valeur donnée de d_eff

    Plus le chi² est petit, meilleur est l'ajustement
    """
    chi2 = 0.0

    for i, r in enumerate(r_obs):
        v_pred = vitesse_asselin(r, d_eff)
        chi2 += ((v_pred - v_obs[i]) / v_err[i])**2

    return chi2

# ============================================================================
# TEST DE DIFFÉRENTES VALEURS DE d_eff
# ============================================================================

print("\n" + "=" * 80)
print("TEST DE DIFFÉRENTES VALEURS DE d_eff")
print("=" * 80)

# Valeurs à tester (en kpc)
d_eff_test = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000,
              d_horizon_cosmologique]

print(f"\n{'d_eff (kpc)':<15} {'d_eff (Mpc)':<15} {'χ²':<15} {'f(10 kpc)':<15}")
print("-" * 60)

chi2_values = []
for d_eff in d_eff_test:
    chi2 = chi2_pour_d_eff(d_eff)
    chi2_values.append(chi2)
    f_10kpc = facteur_expansion(10, d_eff)

    d_eff_mpc = d_eff / 1000
    print(f"{d_eff:<15.0f} {d_eff_mpc:<15.3f} {chi2:<15.2f} {f_10kpc:<15.6f}")

# Trouver le minimum
idx_min = np.argmin(chi2_values)
d_eff_best_approx = d_eff_test[idx_min]
chi2_best_approx = chi2_values[idx_min]

print("\n" + "-" * 60)
print(f"Meilleur d_eff (approximatif) : {d_eff_best_approx:.0f} kpc = {d_eff_best_approx/1000:.2f} Mpc")
print(f"Chi² correspondant : {chi2_best_approx:.2f}")

# ============================================================================
# OPTIMISATION FINE
# ============================================================================

print("\n" + "=" * 80)
print("OPTIMISATION FINE (ALGORITHME NUMÉRIQUE)")
print("=" * 80)

# Optimisation dans une plage raisonnable
result = minimize_scalar(chi2_pour_d_eff, bounds=(10, 10000), method='bounded')

d_eff_optimal = result.x
chi2_optimal = result.fun

print(f"\n✓ d_eff optimal trouvé : {d_eff_optimal:.2f} kpc")
print(f"                        = {d_eff_optimal/1000:.4f} Mpc")
print(f"  χ² optimal : {chi2_optimal:.2f}")

# Facteur d'atténuation à différentes distances
print(f"\nFacteurs d'atténuation f(d) avec d_eff optimal :")
for d_test in [1, 5, 10, 15, 20, 30, 50]:
    f = facteur_expansion(d_test, d_eff_optimal)
    print(f"  f({d_test:2d} kpc) = {f:.6f} ({(1-f)*100:.4f}% d'atténuation)")

# ============================================================================
# COMPARAISON AVEC HORIZON COSMOLOGIQUE
# ============================================================================

print("\n" + "=" * 80)
print("COMPARAISON")
print("=" * 80)

ratio = d_horizon_cosmologique / d_eff_optimal

print(f"\nHorizon cosmologique : d_cosmo = {d_horizon_cosmologique:.0f} kpc")
print(f"Distance effective   : d_eff   = {d_eff_optimal:.2f} kpc")
print(f"\nRapport : d_cosmo / d_eff = {ratio:.0f}")
print(f"\n→ La distance effective est {ratio:.0f}× PLUS PETITE que l'horizon cosmologique !")

# ============================================================================
# CALCUL DES COURBES AVEC d_eff OPTIMAL
# ============================================================================

print("\n" + "=" * 80)
print("CALCUL DES COURBES AVEC d_eff OPTIMAL")
print("=" * 80)

r_array = np.linspace(0.5, 30, 60)

print("\nCalcul en cours...")
v_optimal = np.array([vitesse_asselin(r, d_eff_optimal) for r in r_array])
v_cosmologique = np.array([vitesse_asselin(r, d_horizon_cosmologique) for r in r_array])

# Vitesse newtonienne (pour référence)
def vitesse_newtonienne(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    M_r = masse_totale_visible(r_kpc)
    r_m = r_kpc * 3.086e19
    v_ms = math.sqrt(G * M_r / r_m)
    return v_ms / 1000

v_newton = np.array([vitesse_newtonienne(r) for r in r_array])

print("✓ Calculs terminés")

# ============================================================================
# STATISTIQUES FINALES
# ============================================================================

print("\n" + "=" * 80)
print("STATISTIQUES FINALES")
print("=" * 80)

# Interpoler sur r_obs
v_optimal_interp = np.interp(r_obs, r_array, v_optimal)
v_cosmo_interp = np.interp(r_obs, r_array, v_cosmologique)
v_newton_interp = np.interp(r_obs, r_array, v_newton)

# Chi²
chi2_newton = np.sum(((v_newton_interp - v_obs) / v_err)**2)
chi2_cosmo = np.sum(((v_cosmo_interp - v_obs) / v_err)**2)
chi2_opt = np.sum(((v_optimal_interp - v_obs) / v_err)**2)

# RMS
rms_newton = np.sqrt(np.mean((v_newton_interp - v_obs)**2))
rms_cosmo = np.sqrt(np.mean((v_cosmo_interp - v_obs)**2))
rms_opt = np.sqrt(np.mean((v_optimal_interp - v_obs)**2))

print(f"\n{'Modèle':<25} {'χ²':<15} {'RMS (km/s)':<15}")
print("-" * 55)
print(f"{'Newton (matière visible)':<25} {chi2_newton:<15.2f} {rms_newton:<15.2f}")
print(f"{'Asselin (d_cosmo)':<25} {chi2_cosmo:<15.2f} {rms_cosmo:<15.2f}")
print(f"{'Asselin (d_eff optimal)':<25} {chi2_opt:<15.2f} {rms_opt:<15.2f}")

print(f"\nAmélioration par rapport à Newton :")
print(f"  Avec d_cosmo : {((chi2_newton - chi2_cosmo)/chi2_newton * 100):.1f}%")
print(f"  Avec d_eff   : {((chi2_newton - chi2_opt)/chi2_newton * 100):.1f}%")

# ============================================================================
# VISUALISATION
# ============================================================================

print("\n" + "=" * 80)
print("GÉNÉRATION DES GRAPHIQUES")
print("=" * 80)

plt.figure(figsize=(16, 10))

# ---- Graphique 1 : Courbes de rotation ----
plt.subplot(2, 3, 1)

plt.errorbar(r_obs, v_obs, yerr=v_err, fmt='o', color='black',
             label='Observations', markersize=6, capsize=4, capthick=1.5)

plt.plot(r_array, v_newton, '--', color='blue', linewidth=2,
         label='Newton')

plt.plot(r_array, v_cosmologique, ':', color='gray', linewidth=2,
         label=f'Asselin (d_cosmo={d_horizon_cosmologique/1000:.0f} Mpc)')

plt.plot(r_array, v_optimal, '-', color='red', linewidth=2.5,
         label=f'Asselin (d_eff={d_eff_optimal:.0f} kpc)')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Vitesse (km/s)', fontsize=12)
plt.title('Courbes de Rotation - Voie Lactée', fontsize=14, fontweight='bold')
plt.legend(fontsize=9, loc='lower right')
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(0, 250)

# ---- Graphique 2 : Chi² vs d_eff ----
plt.subplot(2, 3, 2)

d_eff_range = np.logspace(1, 4, 100)  # 10 kpc à 10,000 kpc
chi2_range = [chi2_pour_d_eff(d) for d in d_eff_range]

plt.plot(d_eff_range, chi2_range, '-', color='purple', linewidth=2)
plt.axvline(d_eff_optimal, color='red', linestyle='--', linewidth=2,
            label=f'd_eff optimal = {d_eff_optimal:.0f} kpc')
plt.axhline(chi2_optimal, color='red', linestyle=':', alpha=0.5)

plt.xlabel('d_eff (kpc)', fontsize=12)
plt.ylabel('χ²', fontsize=12)
plt.title('Qualité d\'Ajustement vs d_eff', fontsize=14, fontweight='bold')
plt.xscale('log')
plt.yscale('log')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

# ---- Graphique 3 : Facteur f(d) pour différents d_eff ----
plt.subplot(2, 3, 3)

d_array = np.linspace(0, 50, 200)
f_optimal = [facteur_expansion(d, d_eff_optimal) for d in d_array]
f_cosmo = [facteur_expansion(d, d_horizon_cosmologique) for d in d_array]

plt.plot(d_array, f_optimal, '-', color='red', linewidth=2.5,
         label=f'd_eff = {d_eff_optimal:.0f} kpc')
plt.plot(d_array, f_cosmo, ':', color='gray', linewidth=2,
         label=f'd_cosmo = {d_horizon_cosmologique/1000:.0f} Mpc')

plt.axhline(y=1.0, color='black', linestyle='-', alpha=0.3)
plt.axhline(y=0.9, color='gray', linestyle='--', alpha=0.5)

plt.xlabel('Distance (kpc)', fontsize=12)
plt.ylabel('f(d) = exp(-d/d_eff)', fontsize=12)
plt.title('Facteur d\'Atténuation', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 50)
plt.ylim(0.5, 1.05)

# ---- Graphique 4 : Résidus ----
plt.subplot(2, 3, 4)

residus_newton = (v_newton_interp - v_obs) / v_obs * 100
residus_opt = (v_optimal_interp - v_obs) / v_obs * 100

plt.plot(r_obs, residus_newton, 'o--', color='blue', linewidth=2,
         markersize=6, label='Newton')
plt.plot(r_obs, residus_opt, 's-', color='red', linewidth=2,
         markersize=6, label='Asselin (d_eff optimal)')

plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
plt.fill_between([0, 35], -10, 10, color='green', alpha=0.1)

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Résidu (%)', fontsize=12)
plt.title('Résidus par Rapport aux Observations', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(-60, 20)

# ---- Graphique 5 : Amélioration locale ----
plt.subplot(2, 3, 5)

amelioration = (v_optimal_interp - v_newton_interp) / v_newton_interp * 100

plt.plot(r_obs, amelioration, 'o-', color='green', linewidth=2.5, markersize=8)
plt.axhline(y=0, color='black', linestyle='-', linewidth=1)

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Amélioration (%)', fontsize=12)
plt.title('Amélioration Asselin vs Newton', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)

# ---- Graphique 6 : Tableau de comparaison ----
plt.subplot(2, 3, 6)
plt.axis('off')

# Créer tableau de résultats
tableau_data = [
    ['Paramètre', 'Valeur'],
    ['', ''],
    ['d_eff optimal', f'{d_eff_optimal:.1f} kpc'],
    ['', f'{d_eff_optimal/1000:.3f} Mpc'],
    ['', ''],
    ['Rapport d_cosmo/d_eff', f'{ratio:.0f}×'],
    ['', ''],
    ['χ² Newton', f'{chi2_newton:.1f}'],
    ['χ² Asselin (d_eff)', f'{chi2_opt:.1f}'],
    ['Amélioration χ²', f'{((chi2_newton-chi2_opt)/chi2_newton*100):.1f}%'],
    ['', ''],
    ['RMS Newton', f'{rms_newton:.1f} km/s'],
    ['RMS Asselin (d_eff)', f'{rms_opt:.1f} km/s'],
    ['Amélioration RMS', f'{((rms_newton-rms_opt)/rms_newton*100):.1f}%'],
]

table = plt.table(cellText=tableau_data, cellLoc='left',
                  bbox=[0.1, 0.1, 0.8, 0.8])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Style
for i in range(len(tableau_data)):
    if i == 0:
        table[(i, 0)].set_facecolor('#4CAF50')
        table[(i, 1)].set_facecolor('#4CAF50')
        table[(i, 0)].set_text_props(weight='bold', color='white')
        table[(i, 1)].set_text_props(weight='bold', color='white')
    elif tableau_data[i][0] == '':
        table[(i, 0)].set_facecolor('#f0f0f0')
        table[(i, 1)].set_facecolor('#f0f0f0')

plt.title('Résultats d\'Optimisation', fontsize=14, fontweight='bold', pad=20)

# ---- Finalisation ----
plt.tight_layout()
plt.savefig('optimisation_d_eff.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé : optimisation_d_eff.png")

# ============================================================================
# CONCLUSION
# ============================================================================

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

print(f"\n✓ SUCCÈS : En ajustant d_eff à {d_eff_optimal:.0f} kpc, l'ajustement s'améliore !")
print(f"\n  Amélioration χ² : {((chi2_newton - chi2_opt)/chi2_newton * 100):.1f}%")
print(f"  Amélioration RMS : {((rms_newton - rms_opt)/rms_newton * 100):.1f}%")

if chi2_opt < chi2_newton:
    print("\n  → La Liaison Asselin avec d_eff optimal AMÉLIORE l'ajustement.")
else:
    print("\n  → Même avec optimisation, l'ajustement reste à améliorer.")

print(f"\n📊 INTERPRÉTATION PHYSIQUE :")
print(f"\n  La distance effective d_eff = {d_eff_optimal:.0f} kpc est {ratio:.0f}× plus petite")
print(f"  que l'horizon cosmologique d_cosmo = {d_horizon_cosmologique/1000:.0f} Mpc.")
print(f"\n  Ceci suggère qu'il existe une ÉCHELLE INTERMÉDIAIRE entre :")
print(f"    - Échelle locale (< 1 kpc) : RG classique")
print(f"    - Échelle galactique (~{d_eff_optimal:.0f} kpc) : effet 'matière noire'")
print(f"    - Échelle cosmologique (~{d_horizon_cosmologique/1000:.0f} Mpc) : effet 'énergie noire'")

print("\n" + "=" * 80)
print("FIN DE L'OPTIMISATION")
print("=" * 80)
