#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle de Double Expansion : Spatial + Temporel
Théorie de Maîtrise du Temps

Énergie noire = α × expansion_spatiale + (1-α) × expansion_temporelle

Optimisation du paramètre α pour trouver la meilleure partition.

Date : 2025-12-04
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize_scalar

# Constantes
G = 6.67430e-11  # m³/(kg·s²)
c = 299792458  # m/s
M_solaire = 1.989e30  # kg
kpc_to_m = 3.086e19  # m

# Paramètres galactiques
M_bulbe = 1.5e10 * M_solaire
M_disque_total = 6.0e10 * M_solaire
r_disque = 3.5  # kpc
r_bulbe = 1.0  # kpc

print("=" * 80)
print("MODÈLE DE DOUBLE EXPANSION : SPATIAL + TEMPOREL")
print("Optimisation de la Partition de l'Énergie Noire")
print("=" * 80)

# Fonction de masse visible
def masse_bulbe(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    return M_bulbe * (r_kpc**3) / ((r_kpc**2 + r_bulbe**2)**(3/2))

def masse_disque(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    x = r_kpc / r_disque
    return M_disque_total * (1 - (1 + x) * math.exp(-x))

def masse_visible(r_kpc):
    return masse_bulbe(r_kpc) + masse_disque(r_kpc)

# Horizon gravitationnel avec paramètre alpha
def distance_horizon(alpha, t_0=13.8e9*365.25*24*3600):
    """
    Distance horizon dépendant de la proportion d'expansion temporelle

    alpha = 0 : tout temporel (formulation originale)
    alpha = 1 : tout spatial (Lambda-CDM)

    L'horizon gravitationnel effectif dépend de la composante temporelle
    """
    # Composante temporelle
    beta_temporal = 2.0/3.0 * (1 - alpha)  # Proportion temporelle

    # Distance effective d'atténuation
    # Plus alpha est grand (spatial), plus d_eff est grand (moins d'atténuation locale)
    d_eff_kpc = 100 * (1 + 40 * alpha)  # 100 kpc à 4100 kpc

    return d_eff_kpc

def facteur_expansion(d_kpc, d_eff):
    if d_eff <= 0:
        return 1.0
    return math.exp(-d_kpc / d_eff)

def masse_effective_asselin(r_kpc, d_eff, N_shells=100):
    M_local = masse_visible(r_kpc)
    r_max = 50.0
    dr = (r_max - r_kpc) / N_shells
    contribution_externe = 0.0

    for i in range(N_shells):
        r_shell = r_kpc + (i + 0.5) * dr
        dM = masse_visible(r_shell + dr/2) - masse_visible(r_shell - dr/2)
        if dM <= 0:
            continue
        d = abs(r_shell - r_kpc)
        if d < 0.01:
            continue
        f = facteur_expansion(d, d_eff)
        contribution_externe += dM * f * (r_kpc / r_shell)

    return M_local + contribution_externe

def vitesse_rotation(r_kpc, alpha):
    """
    Vitesse de rotation avec paramètre alpha

    alpha : proportion d'expansion spatiale
    (1-alpha) : proportion d'expansion temporelle
    """
    if r_kpc < 0.01:
        return 0.0

    d_eff = distance_horizon(alpha)
    M_eff = masse_effective_asselin(r_kpc, d_eff)
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_eff / r_m)
    return v_ms / 1000  # km/s

def vitesse_newtonienne(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    M_r = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_r / r_m)
    return v_ms / 1000

# Données observées
r_obs = np.array([0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30])
v_obs = np.array([80, 140, 190, 210, 220, 225, 225, 225, 220, 220, 215, 210, 205, 200, 195, 185, 175])
v_err = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 20, 20, 25, 30])

# Fonction objectif
def chi2_fonction(alpha):
    """Calcule χ² pour une valeur de alpha donnée"""
    if alpha < 0 or alpha > 1:
        return 1e10

    chi2 = 0.0
    for i, r in enumerate(r_obs):
        v_pred = vitesse_rotation(r, alpha)
        chi2 += ((v_pred - v_obs[i]) / v_err[i])**2

    return chi2

# Test de différentes valeurs
print("\n" + "=" * 80)
print("TEST DE DIFFÉRENTES PROPORTIONS")
print("=" * 80)
print("\nα = 0.0 : 100% temporel (formulation originale)")
print("α = 1.0 : 100% spatial (Lambda-CDM)")
print("\n")

alphas_test = [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]
print(f"{'α (spatial)':<15} {'1-α (temporel)':<18} {'d_eff (kpc)':<15} {'χ²':<12}")
print("-" * 65)

resultats_test = {}
for alpha in alphas_test:
    d_eff = distance_horizon(alpha)
    chi2 = chi2_fonction(alpha)
    resultats_test[alpha] = {'d_eff': d_eff, 'chi2': chi2}
    print(f"{alpha:<15.2f} {1-alpha:<18.2f} {d_eff:<15.1f} {chi2:<12.2f}")

# Optimisation fine
print("\n" + "=" * 80)
print("OPTIMISATION FINE")
print("=" * 80)

result = minimize_scalar(chi2_fonction, bounds=(0, 1), method='bounded')
alpha_optimal = result.x
chi2_optimal = result.fun
d_eff_optimal = distance_horizon(alpha_optimal)

print(f"\n✓ Optimisation terminée")
print(f"\nParamètres optimaux :")
print(f"  α (spatial) = {alpha_optimal:.4f} ({alpha_optimal*100:.2f}%)")
print(f"  1-α (temporel) = {1-alpha_optimal:.4f} ({(1-alpha_optimal)*100:.2f}%)")
print(f"  d_eff = {d_eff_optimal:.1f} kpc")
print(f"  χ² = {chi2_optimal:.2f}")

# Comparaison avec Newton
r_array = np.linspace(0.5, 30, 60)
v_newton = np.array([vitesse_newtonienne(r) for r in r_array])
v_newton_interp = np.interp(r_obs, r_array, v_newton)
chi2_newton = np.sum(((v_newton_interp - v_obs) / v_err)**2)

print(f"\nComparaison :")
print(f"  χ² Newton = {chi2_newton:.2f}")
print(f"  χ² Optimal (α={alpha_optimal:.3f}) = {chi2_optimal:.2f}")
print(f"  Ratio = {chi2_optimal/chi2_newton:.2f}×")

if chi2_optimal < chi2_newton:
    print(f"\n✓ SUCCÈS : Meilleur que Newton de {(chi2_newton-chi2_optimal)/chi2_newton*100:.1f}%")
else:
    print(f"\n⚠ Moins bon que Newton de {(chi2_optimal-chi2_newton)/chi2_newton*100:.1f}%")

# Calcul courbes
print("\n" + "=" * 80)
print("CALCUL DES COURBES DE ROTATION")
print("=" * 80)

v_alpha_0 = np.array([vitesse_rotation(r, 0.0) for r in r_array])
v_alpha_05 = np.array([vitesse_rotation(r, 0.5) for r in r_array])
v_alpha_optimal = np.array([vitesse_rotation(r, alpha_optimal) for r in r_array])
v_alpha_1 = np.array([vitesse_rotation(r, 1.0) for r in r_array])

# Visualisation
print("\n" + "=" * 80)
print("GÉNÉRATION DES GRAPHIQUES")
print("=" * 80)

fig = plt.figure(figsize=(16, 12))

# Graphique 1 : Courbes de rotation
ax1 = plt.subplot(2, 3, 1)
plt.errorbar(r_obs, v_obs, yerr=v_err, fmt='o', color='black',
             label='Observations', markersize=7, capsize=4, capthick=1.5, zorder=10)

plt.plot(r_array, v_newton, '--', color='gray', linewidth=2, label='Newton', alpha=0.7)
plt.plot(r_array, v_alpha_0, ':', color='blue', linewidth=2, label='α=0.0 (100% temporel)', alpha=0.7)
plt.plot(r_array, v_alpha_05, '-.', color='green', linewidth=2, label='α=0.5 (50-50)', alpha=0.7)
plt.plot(r_array, v_alpha_optimal, '-', color='red', linewidth=3, label=f'α={alpha_optimal:.2f} (optimal)', alpha=0.9)
plt.plot(r_array, v_alpha_1, ':', color='purple', linewidth=2, label='α=1.0 (100% spatial)', alpha=0.7)

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Vitesse (km/s)', fontsize=12)
plt.title('Courbes de Rotation - Double Expansion', fontsize=14, fontweight='bold')
plt.legend(fontsize=9, loc='lower right')
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(0, 250)

# Graphique 2 : χ² vs α
ax2 = plt.subplot(2, 3, 2)

alphas_plot = np.linspace(0, 1, 50)
chi2_plot = [chi2_fonction(a) for a in alphas_plot]

plt.plot(alphas_plot, chi2_plot, '-', color='purple', linewidth=2.5)
plt.axvline(alpha_optimal, color='red', linestyle='--', linewidth=2, label=f'α optimal = {alpha_optimal:.3f}')
plt.axhline(chi2_newton, color='gray', linestyle=':', linewidth=2, label=f'χ² Newton = {chi2_newton:.0f}')

plt.xlabel('α (proportion spatiale)', fontsize=12)
plt.ylabel('χ²', fontsize=12)
plt.title('Qualité d\'Ajustement vs Proportion', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 1)

# Graphique 3 : d_eff vs α
ax3 = plt.subplot(2, 3, 3)

d_eff_plot = [distance_horizon(a) for a in alphas_plot]

plt.plot(alphas_plot, d_eff_plot, '-', color='orange', linewidth=2.5)
plt.axvline(alpha_optimal, color='red', linestyle='--', linewidth=2, alpha=0.7)

plt.xlabel('α (proportion spatiale)', fontsize=12)
plt.ylabel('d_eff (kpc)', fontsize=12)
plt.title('Distance Effective vs Proportion', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim(0, 1)

# Graphique 4 : Résidus
ax4 = plt.subplot(2, 3, 4)

v_optimal_interp = np.interp(r_obs, r_array, v_alpha_optimal)
residus_newton = (v_newton_interp - v_obs) / v_obs * 100
residus_optimal = (v_optimal_interp - v_obs) / v_obs * 100

plt.plot(r_obs, residus_newton, 'o--', color='gray', linewidth=2, markersize=6, label='Newton')
plt.plot(r_obs, residus_optimal, 's-', color='red', linewidth=2.5, markersize=7, label=f'α={alpha_optimal:.2f}')

plt.axhline(0, color='black', linestyle='-', linewidth=1)
plt.fill_between([0, 35], -10, 10, color='green', alpha=0.1)

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Résidu (%)', fontsize=12)
plt.title('Résidus', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(-60, 20)

# Graphique 5 : Répartition énergie noire
ax5 = plt.subplot(2, 3, 5)

categories = ['Spatial\n(expansion)', 'Temporel\n(distorsion)']
proportions = [alpha_optimal * 100, (1 - alpha_optimal) * 100]
colors = ['#3498db', '#e74c3c']

bars = plt.bar(categories, proportions, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
for bar, val in zip(bars, proportions):
    plt.text(bar.get_x() + bar.get_width()/2, val + 2, f'{val:.1f}%',
            ha='center', va='bottom', fontsize=14, fontweight='bold')

plt.ylabel('Contribution (%)', fontsize=12)
plt.title('Partition Optimale de l\'Énergie Noire', fontsize=14, fontweight='bold')
plt.ylim(0, 110)
plt.grid(True, alpha=0.3, axis='y')

# Graphique 6 : Tableau récapitulatif
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

tableau_data = [
    ['Paramètre', 'Valeur'],
    ['', ''],
    ['α (spatial)', f'{alpha_optimal:.4f}'],
    ['Proportion spatiale', f'{alpha_optimal*100:.2f}%'],
    ['', ''],
    ['1-α (temporel)', f'{1-alpha_optimal:.4f}'],
    ['Proportion temporelle', f'{(1-alpha_optimal)*100:.2f}%'],
    ['', ''],
    ['d_eff optimal', f'{d_eff_optimal:.1f} kpc'],
    ['', ''],
    ['χ² Newton', f'{chi2_newton:.1f}'],
    ['χ² Optimal', f'{chi2_optimal:.1f}'],
    ['Amélioration', f'{(chi2_newton-chi2_optimal)/chi2_newton*100:.1f}%'],
]

table = plt.table(cellText=tableau_data, cellLoc='left',
                 bbox=[0.05, 0.05, 0.9, 0.9])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

for i in range(len(tableau_data)):
    if i == 0:
        table[(i, 0)].set_facecolor('#4CAF50')
        table[(i, 1)].set_facecolor('#4CAF50')
        table[(i, 0)].set_text_props(weight='bold', color='white')
        table[(i, 1)].set_text_props(weight='bold', color='white')
    elif tableau_data[i][0] == '':
        table[(i, 0)].set_facecolor('#f0f0f0')
        table[(i, 1)].set_facecolor('#f0f0f0')

plt.title('Résultats Optimisation', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('modele_double_expansion.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé : modele_double_expansion.png")

# Conclusion
print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

print(f"\nPartition optimale de l'énergie noire :")
print(f"  • Expansion spatiale : {alpha_optimal*100:.2f}%")
print(f"  • Distorsion temporelle : {(1-alpha_optimal)*100:.2f}%")
print(f"\nDistance effective d_eff = {d_eff_optimal:.1f} kpc")

if alpha_optimal < 0.1:
    print(f"\n→ L'expansion est PRINCIPALEMENT temporelle")
elif alpha_optimal > 0.9:
    print(f"\n→ L'expansion est PRINCIPALEMENT spatiale")
else:
    print(f"\n→ L'expansion est MIXTE (spatiale + temporelle)")

if chi2_optimal < chi2_newton:
    print(f"\n✓ Le modèle double expansion est MEILLEUR que Newton")
    print(f"  Amélioration : {(chi2_newton-chi2_optimal)/chi2_newton*100:.1f}%")
else:
    print(f"\n⚠ Le modèle double expansion reste moins bon que Newton")
    print(f"  χ² optimal / χ² Newton = {chi2_optimal/chi2_newton:.2f}×")

print("\n" + "=" * 80)
