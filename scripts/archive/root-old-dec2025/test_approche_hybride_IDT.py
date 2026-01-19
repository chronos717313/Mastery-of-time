#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'Approche Hybride : d_eff = 100 kpc + Matière IDT Centrale
Théorie de Maîtrise du Temps

Combinaison de deux contributions :
1. Matière non-lumineuse au centre (détectée par IDT)
2. Effet cumulatif Liaison Asselin avec d_eff = 100 kpc

Date : 2025-12-04
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import minimize

# Constantes
G = 6.67430e-11  # m³/(kg·s²)
c = 299792458  # m/s
M_solaire = 1.989e30  # kg
kpc_to_m = 3.086e19  # m

# Paramètres Voie Lactée (matière VISIBLE)
M_bulbe = 1.5e10 * M_solaire
M_disque_total = 6.0e10 * M_solaire
r_disque = 3.5  # kpc
r_bulbe = 1.0  # kpc

print("=" * 80)
print("TEST APPROCHE HYBRIDE : d_eff = 100 kpc + MATIÈRE IDT")
print("=" * 80)

# ============================================================================
# MASSE VISIBLE (INCHANGÉ)
# ============================================================================

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

# ============================================================================
# MATIÈRE NON-LUMINEUSE (IDT) - NOUVELLE
# ============================================================================

def masse_IDT_NFW(r_kpc, M_IDT_total, r_s_IDT):
    """
    Profil NFW pour matière non-lumineuse détectée par IDT

    Args:
        r_kpc: rayon en kpc
        M_IDT_total: masse totale IDT en kg
        r_s_IDT: rayon d'échelle en kpc

    Returns:
        masse IDT contenue dans r en kg
    """
    if r_kpc < 0.01 or M_IDT_total <= 0 or r_s_IDT <= 0:
        return 0.0

    # Paramètre de concentration (typique)
    c = 10.0

    # Fonction f(x) = ln(1+x) - x/(1+x)
    x = r_kpc / r_s_IDT
    f_x = math.log(1 + x) - x / (1 + x)
    f_c = math.log(1 + c) - c / (1 + c)

    M_IDT_r = M_IDT_total * f_x / f_c

    return M_IDT_r

# ============================================================================
# MASSE TOTALE (VISIBLE + IDT)
# ============================================================================

def masse_totale_avec_IDT(r_kpc, M_IDT_total, r_s_IDT):
    """Masse totale = visible + IDT"""
    return masse_visible(r_kpc) + masse_IDT_NFW(r_kpc, M_IDT_total, r_s_IDT)

# ============================================================================
# EFFET CUMULATIF AVEC d_eff FIXE
# ============================================================================

def facteur_expansion(d_kpc, d_eff):
    if d_eff <= 0:
        return 1.0
    return math.exp(-d_kpc / d_eff)

def masse_effective_hybride(r_kpc, M_IDT_total, r_s_IDT, d_eff=100, N_shells=100):
    """
    Masse effective hybride :
    M_eff = M_totale(visible+IDT) + effet cumulatif Asselin

    Args:
        r_kpc: rayon en kpc
        M_IDT_total: masse IDT totale en kg
        r_s_IDT: rayon d'échelle IDT en kpc
        d_eff: distance effective atténuation (défaut 100 kpc)
        N_shells: nombre de coquilles pour intégration
    """
    # Masse locale totale (visible + IDT)
    M_local = masse_totale_avec_IDT(r_kpc, M_IDT_total, r_s_IDT)

    # Contribution cumulative
    r_max = 50.0
    dr = (r_max - r_kpc) / N_shells
    contribution_externe = 0.0

    for i in range(N_shells):
        r_shell = r_kpc + (i + 0.5) * dr
        dM = (masse_totale_avec_IDT(r_shell + dr/2, M_IDT_total, r_s_IDT) -
              masse_totale_avec_IDT(r_shell - dr/2, M_IDT_total, r_s_IDT))

        if dM <= 0:
            continue

        d = abs(r_shell - r_kpc)
        if d < 0.01:
            continue

        f = facteur_expansion(d, d_eff)
        contribution_externe += dM * f * (r_kpc / r_shell)

    return M_local + contribution_externe

# ============================================================================
# VITESSE DE ROTATION
# ============================================================================

def vitesse_rotation(r_kpc, M_IDT_total, r_s_IDT, d_eff=100):
    """
    Vitesse de rotation avec modèle hybride
    """
    if r_kpc < 0.01:
        return 0.0

    M_eff = masse_effective_hybride(r_kpc, M_IDT_total, r_s_IDT, d_eff)
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_eff / r_m)
    return v_ms / 1000  # km/s

def vitesse_newtonienne(r_kpc):
    """Vitesse avec matière visible seule"""
    if r_kpc < 0.01:
        return 0.0
    M_r = masse_visible(r_kpc)
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_r / r_m)
    return v_ms / 1000

# ============================================================================
# DONNÉES OBSERVÉES
# ============================================================================

r_obs = np.array([0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30])
v_obs = np.array([80, 140, 190, 210, 220, 225, 225, 225, 220, 220, 215, 210, 205, 200, 195, 185, 175])
v_err = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 20, 20, 25, 30])

# ============================================================================
# FONCTION OBJECTIF POUR OPTIMISATION
# ============================================================================

def chi2_fonction(params):
    """
    Calcule χ² pour paramètres donnés

    params[0] = M_IDT_total en unités de 10¹⁰ M☉
    params[1] = r_s_IDT en kpc
    """
    M_IDT_total = params[0] * 1e10 * M_solaire
    r_s_IDT = params[1]
    d_eff = 100.0  # Fixé

    # Contraintes
    if M_IDT_total < 0 or r_s_IDT < 0.5 or r_s_IDT > 10:
        return 1e10

    chi2 = 0.0
    for i, r in enumerate(r_obs):
        v_pred = vitesse_rotation(r, M_IDT_total, r_s_IDT, d_eff)
        chi2 += ((v_pred - v_obs[i]) / v_err[i])**2

    return chi2

# ============================================================================
# OPTIMISATION
# ============================================================================

print("\n" + "=" * 80)
print("OPTIMISATION DES PARAMÈTRES IDT")
print("=" * 80)
print("\nParamètres à optimiser :")
print("  - M_IDT_total : Masse totale non-lumineuse (en 10¹⁰ M☉)")
print("  - r_s_IDT : Rayon d'échelle du profil NFW (en kpc)")
print("  - d_eff : FIXÉ à 100 kpc (rayon viral)")

# Valeur initiale
params_init = [2.0, 3.0]  # M_IDT=2×10¹⁰ M☉, r_s=3 kpc

print(f"\nValeur initiale : M_IDT = {params_init[0]:.1f}×10¹⁰ M☉, r_s = {params_init[1]:.1f} kpc")
chi2_init = chi2_fonction(params_init)
print(f"χ² initial = {chi2_init:.2f}")

print("\nOptimisation en cours...")
result = minimize(chi2_fonction, params_init, method='Nelder-Mead',
                 options={'maxiter': 1000, 'xatol': 0.01, 'fatol': 1.0})

M_IDT_optimal = result.x[0] * 1e10 * M_solaire
r_s_IDT_optimal = result.x[1]
chi2_optimal = result.fun

print(f"\n✓ Optimisation terminée")
print(f"\nParamètres optimaux :")
print(f"  M_IDT_total = {result.x[0]:.2f} × 10¹⁰ M☉")
print(f"  r_s_IDT = {r_s_IDT_optimal:.2f} kpc")
print(f"  d_eff = 100 kpc (fixé)")
print(f"\nχ² optimal = {chi2_optimal:.2f}")

# ============================================================================
# COMPARAISON AVEC MODÈLES DE RÉFÉRENCE
# ============================================================================

print("\n" + "=" * 80)
print("CALCUL DES COURBES DE ROTATION")
print("=" * 80)

r_array = np.linspace(0.5, 30, 60)

# 1. Newton (matière visible seule)
print("\nCalcul Newton...")
v_newton = np.array([vitesse_newtonienne(r) for r in r_array])
v_newton_interp = np.interp(r_obs, r_array, v_newton)
chi2_newton = np.sum(((v_newton_interp - v_obs) / v_err)**2)
rms_newton = np.sqrt(np.mean((v_newton_interp - v_obs)**2))

# 2. Modèle hybride optimal
print("Calcul modèle hybride optimal...")
v_hybride = np.array([vitesse_rotation(r, M_IDT_optimal, r_s_IDT_optimal, 100)
                      for r in r_array])
v_hybride_interp = np.interp(r_obs, r_array, v_hybride)
chi2_hybride = np.sum(((v_hybride_interp - v_obs) / v_err)**2)
rms_hybride = np.sqrt(np.mean((v_hybride_interp - v_obs)**2))

# 3. Seulement IDT (sans effet cumulatif, d_eff = infini)
print("Calcul IDT seul (sans cumulatif)...")
v_IDT_seul = np.array([vitesse_rotation(r, M_IDT_optimal, r_s_IDT_optimal, 1e10)
                       for r in r_array])
v_IDT_interp = np.interp(r_obs, r_array, v_IDT_seul)
chi2_IDT_seul = np.sum(((v_IDT_interp - v_obs) / v_err)**2)
rms_IDT_seul = np.sqrt(np.mean((v_IDT_interp - v_obs)**2))

# ============================================================================
# TABLEAU COMPARATIF
# ============================================================================

print("\n" + "=" * 80)
print("RÉSULTATS COMPARATIFS")
print("=" * 80)

print(f"\n{'Modèle':<40} {'χ²':<12} {'RMS (km/s)':<12} {'vs Newton'}")
print("-" * 80)
print(f"{'Newton (matière visible seule)':<40} {chi2_newton:<12.2f} {rms_newton:<12.2f} 1.00×")
print(f"{'IDT seul (M_IDT + M_vis, sans cumulatif)':<40} {chi2_IDT_seul:<12.2f} {rms_IDT_seul:<12.2f} {chi2_IDT_seul/chi2_newton:.2f}×")
print(f"{'Hybride (IDT + cumulatif d_eff=100 kpc)':<40} {chi2_hybride:<12.2f} {rms_hybride:<12.2f} {chi2_hybride/chi2_newton:.2f}×")

print(f"\n{'─'*80}")
if chi2_hybride < chi2_newton:
    amelioration = (chi2_newton - chi2_hybride) / chi2_newton * 100
    print(f"✓ SUCCÈS : Le modèle hybride est MEILLEUR que Newton !")
    print(f"  Amélioration χ² : {amelioration:.1f}%")
else:
    degradation = (chi2_hybride - chi2_newton) / chi2_newton * 100
    print(f"⚠ Le modèle hybride reste moins bon que Newton")
    print(f"  Dégradation χ² : {degradation:.1f}%")

# ============================================================================
# ANALYSE DE LA CONTRIBUTION IDT
# ============================================================================

print("\n" + "=" * 80)
print("ANALYSE DE LA MATIÈRE IDT")
print("=" * 80)

print(f"\nMasse totale visible : {(M_bulbe + M_disque_total)/M_solaire:.2e} M☉")
print(f"Masse totale IDT : {M_IDT_optimal/M_solaire:.2e} M☉")
print(f"Rapport M_IDT / M_visible : {M_IDT_optimal/(M_bulbe + M_disque_total):.2f}")

print(f"\nDistribution de masse aux rayons caractéristiques :")
print(f"{'Rayon (kpc)':<15} {'M_visible':<15} {'M_IDT':<15} {'M_totale':<15} {'% IDT'}")
print("-" * 75)

for r_test in [1, 5, 10, 20, 30]:
    M_vis = masse_visible(r_test) / M_solaire
    M_IDT = masse_IDT_NFW(r_test, M_IDT_optimal, r_s_IDT_optimal) / M_solaire
    M_tot = M_vis + M_IDT
    pct_IDT = (M_IDT / M_tot * 100) if M_tot > 0 else 0

    print(f"{r_test:<15} {M_vis:<15.2e} {M_IDT:<15.2e} {M_tot:<15.2e} {pct_IDT:<.1f}%")

# ============================================================================
# VISUALISATION
# ============================================================================

print("\n" + "=" * 80)
print("GÉNÉRATION DES GRAPHIQUES")
print("=" * 80)

fig = plt.figure(figsize=(16, 12))

# Graphique 1 : Courbes de rotation
ax1 = plt.subplot(2, 3, 1)
plt.errorbar(r_obs, v_obs, yerr=v_err, fmt='o', color='black',
             label='Observations', markersize=7, capsize=4, capthick=1.5, zorder=10)
plt.plot(r_array, v_newton, '--', color='blue', linewidth=2,
         label='Newton (visible)', alpha=0.7)
plt.plot(r_array, v_IDT_seul, ':', color='green', linewidth=2.5,
         label=f'Visible + IDT ({M_IDT_optimal/M_solaire/1e10:.1f}e10 M☉)')
plt.plot(r_array, v_hybride, '-', color='red', linewidth=3,
         label='Hybride (IDT + cumulatif d=100kpc)')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Vitesse (km/s)', fontsize=12)
plt.title('Approche Hybride : IDT + Liaison Asselin', fontsize=14, fontweight='bold')
plt.legend(fontsize=10, loc='lower right')
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(0, 250)

# Graphique 2 : Distribution de masse
ax2 = plt.subplot(2, 3, 2)

M_vis_array = np.array([masse_visible(r)/M_solaire for r in r_array])
M_IDT_array = np.array([masse_IDT_NFW(r, M_IDT_optimal, r_s_IDT_optimal)/M_solaire
                        for r in r_array])
M_tot_array = M_vis_array + M_IDT_array

plt.plot(r_array, M_vis_array, '--', color='blue', linewidth=2, label='Visible')
plt.plot(r_array, M_IDT_array, ':', color='green', linewidth=2.5, label='IDT')
plt.plot(r_array, M_tot_array, '-', color='red', linewidth=3, label='Totale (Vis+IDT)')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Masse cumulée (M☉)', fontsize=12)
plt.title('Distribution de Masse', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.xlim(0, 32)

# Graphique 3 : Résidus
ax3 = plt.subplot(2, 3, 3)

residus_newton = (v_newton_interp - v_obs) / v_obs * 100
residus_hybride = (v_hybride_interp - v_obs) / v_obs * 100

plt.plot(r_obs, residus_newton, 'o--', color='blue', linewidth=2,
         markersize=6, label='Newton')
plt.plot(r_obs, residus_hybride, 's-', color='red', linewidth=2.5,
         markersize=7, label='Hybride')

plt.axhline(0, color='black', linestyle='-', linewidth=1)
plt.fill_between([0, 35], -10, 10, color='green', alpha=0.1, label='±10%')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Résidu (%)', fontsize=12)
plt.title('Résidus par Rapport aux Observations', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(-60, 20)

# Graphique 4 : Contribution relative IDT
ax4 = plt.subplot(2, 3, 4)

pct_IDT_array = (M_IDT_array / M_tot_array * 100)
plt.plot(r_array, pct_IDT_array, '-', color='purple', linewidth=3)
plt.axhline(50, color='gray', linestyle='--', alpha=0.5, label='50%')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Contribution IDT (%)', fontsize=12)
plt.title('Pourcentage de Masse IDT', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(0, 100)

# Graphique 5 : Comparaison χ²
ax5 = plt.subplot(2, 3, 5)

modeles = ['Newton', 'IDT seul', 'Hybride\n(optimal)']
chi2_vals = [chi2_newton, chi2_IDT_seul, chi2_hybride]
couleurs = ['blue', 'green', 'red']

bars = plt.bar(range(len(modeles)), chi2_vals, color=couleurs, alpha=0.7, edgecolor='black')
plt.axhline(chi2_newton, color='black', linestyle='--', linewidth=1, alpha=0.5)

plt.ylabel('χ²', fontsize=12)
plt.title('Comparaison Qualité d\'Ajustement', fontsize=14, fontweight='bold')
plt.xticks(range(len(modeles)), modeles, fontsize=11)
plt.grid(True, alpha=0.3, axis='y')

for bar, val in zip(bars, chi2_vals):
    plt.text(bar.get_x() + bar.get_width()/2, val + 10, f'{val:.0f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Graphique 6 : Tableau récapitulatif
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

tableau_data = [
    ['Paramètre', 'Valeur'],
    ['', ''],
    ['M_IDT_total', f'{M_IDT_optimal/M_solaire/1e10:.2f} × 10¹⁰ M☉'],
    ['r_s_IDT', f'{r_s_IDT_optimal:.2f} kpc'],
    ['d_eff', '100 kpc (fixé)'],
    ['', ''],
    ['M_IDT / M_visible', f'{M_IDT_optimal/(M_bulbe + M_disque_total):.2f}'],
    ['', ''],
    ['χ² Newton', f'{chi2_newton:.1f}'],
    ['χ² Hybride', f'{chi2_hybride:.1f}'],
    ['Amélioration', f'{(chi2_newton-chi2_hybride)/chi2_newton*100:.1f}%'],
    ['', ''],
    ['RMS Newton', f'{rms_newton:.1f} km/s'],
    ['RMS Hybride', f'{rms_hybride:.1f} km/s'],
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
plt.savefig('test_approche_hybride_IDT.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé : test_approche_hybride_IDT.png")

# ============================================================================
# CONCLUSION
# ============================================================================

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

print(f"\nApproche testée :")
print(f"  • d_eff = 100 kpc (rayon viral, fixé)")
print(f"  • M_IDT = {M_IDT_optimal/M_solaire/1e10:.2f} × 10¹⁰ M☉ (optimisé)")
print(f"  • r_s_IDT = {r_s_IDT_optimal:.2f} kpc (optimisé)")

if chi2_hybride < chi2_newton:
    print(f"\n🎉 RÉSULTAT : SUCCÈS !")
    print(f"  ✓ χ² hybride ({chi2_hybride:.2f}) < χ² Newton ({chi2_newton:.2f})")
    print(f"  ✓ Amélioration : {(chi2_newton-chi2_hybride)/chi2_newton*100:.1f}%")
    print(f"\n  L'approche hybride (IDT + Liaison Asselin) reproduit MIEUX")
    print(f"  les observations que la matière visible seule !")
else:
    print(f"\n⚠ RÉSULTAT : Amélioration partielle")
    print(f"  χ² hybride ({chi2_hybride:.2f}) vs χ² Newton ({chi2_newton:.2f})")
    print(f"  Ratio : {chi2_hybride/chi2_newton:.2f}×")

print(f"\nInterprétation physique :")
print(f"  • Matière IDT concentrée au centre (r_s = {r_s_IDT_optimal:.2f} kpc)")
print(f"  • Contribue {M_IDT_optimal/(M_bulbe + M_disque_total):.0%} de la masse visible")
print(f"  • Nature : Matière baryonique non-lumineuse (naines brunes, TN noirs, etc.)")
print(f"  • Détectable par IDT (timing pulsars, horloges atomiques)")

print("\n" + "=" * 80)
