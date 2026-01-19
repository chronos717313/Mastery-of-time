#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des Échelles Galactiques Recommandées
Théorie de Maîtrise du Temps

Test des 3 échelles recommandées :
- d_eff = 50 kpc (rayon halo galactique)
- d_eff = 70 kpc (moyenne géométrique)
- d_eff = 100 kpc (rayon viral)

Compare avec :
- d_eff = 10 kpc (optimisation numérique)
- d_cosmo = 4,231 Mpc (horizon cosmologique)
- Newton (matière visible seule)

Date : 2025-12-04
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# Constantes
G = 6.67430e-11  # m³/(kg·s²)
c = 299792458  # m/s
t_0 = 13.8e9 * 365.25 * 24 * 3600  # s
d_horizon_cosmo = c * t_0 / (3.086e19)  # kpc

# Paramètres Voie Lactée
M_bulbe = 1.5e10 * 1.989e30  # kg
M_disque_total = 6.0e10 * 1.989e30  # kg
r_disque = 3.5  # kpc
r_bulbe = 1.0  # kpc

# Fonctions de masse
def masse_bulbe(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    return M_bulbe * (r_kpc**3) / ((r_kpc**2 + r_bulbe**2)**(3/2))

def masse_disque(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    x = r_kpc / r_disque
    return M_disque_total * (1 - (1 + x) * math.exp(-x))

def masse_totale_visible(r_kpc):
    return masse_bulbe(r_kpc) + masse_disque(r_kpc)

# Facteur d'expansion
def facteur_expansion(d_kpc, d_eff):
    if d_eff <= 0:
        return 1.0
    return math.exp(-d_kpc / d_eff)

# Masse effective
def masse_effective_asselin(r_kpc, d_eff, N_shells=100):
    M_local = masse_totale_visible(r_kpc)
    r_max = 50.0
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

    return M_local + contribution_externe

# Vitesse de rotation
def vitesse_asselin(r_kpc, d_eff):
    if r_kpc < 0.01:
        return 0.0
    M_eff = masse_effective_asselin(r_kpc, d_eff)
    r_m = r_kpc * 3.086e19
    v_ms = math.sqrt(G * M_eff / r_m)
    return v_ms / 1000

def vitesse_newtonienne(r_kpc):
    if r_kpc < 0.01:
        return 0.0
    M_r = masse_totale_visible(r_kpc)
    r_m = r_kpc * 3.086e19
    v_ms = math.sqrt(G * M_r / r_m)
    return v_ms / 1000

# Données observées
r_obs = np.array([0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30])
v_obs = np.array([80, 140, 190, 210, 220, 225, 225, 225, 220, 220, 215, 210, 205, 200, 195, 185, 175])
v_err = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 20, 20, 25, 30])

# Échelles à tester
echelles_test = {
    'd_eff = 10 kpc (optimisation)': 10,
    'd_eff = 50 kpc (rayon halo)': 50,
    'd_eff = 70 kpc (moyenne)': 70,
    'd_eff = 100 kpc (rayon viral)': 100,
    'd_cosmo = 4231 Mpc': d_horizon_cosmo
}

print("=" * 80)
print("TEST DES ÉCHELLES GALACTIQUES RECOMMANDÉES")
print("=" * 80)

# Grille de calcul
r_array = np.linspace(0.5, 30, 60)

# Stockage résultats
resultats = {}

# Newton (référence)
print("\nCalcul courbe newtonienne...")
v_newton = np.array([vitesse_newtonienne(r) for r in r_array])
v_newton_interp = np.interp(r_obs, r_array, v_newton)
chi2_newton = np.sum(((v_newton_interp - v_obs) / v_err)**2)
rms_newton = np.sqrt(np.mean((v_newton_interp - v_obs)**2))

resultats['Newton'] = {
    'courbe': v_newton,
    'chi2': chi2_newton,
    'rms': rms_newton,
    'd_eff': None
}

# Test chaque échelle
for nom, d_eff_val in echelles_test.items():
    print(f"\nCalcul avec {nom}...")

    v_asselin = np.array([vitesse_asselin(r, d_eff_val) for r in r_array])
    v_asselin_interp = np.interp(r_obs, r_array, v_asselin)

    chi2 = np.sum(((v_asselin_interp - v_obs) / v_err)**2)
    rms = np.sqrt(np.mean((v_asselin_interp - v_obs)**2))

    resultats[nom] = {
        'courbe': v_asselin,
        'chi2': chi2,
        'rms': rms,
        'd_eff': d_eff_val
    }

    print(f"  χ² = {chi2:.2f}")
    print(f"  RMS = {rms:.2f} km/s")

# Tableau comparatif
print("\n" + "=" * 80)
print("TABLEAU COMPARATIF")
print("=" * 80)

print(f"\n{'Modèle':<35} {'d_eff (kpc)':<15} {'χ²':<12} {'RMS (km/s)':<12} {'vs Newton'}")
print("-" * 90)

# Trier par χ²
resultats_tries = sorted(resultats.items(), key=lambda x: x[1]['chi2'])

for nom, res in resultats_tries:
    d_eff_str = f"{res['d_eff']:.0f}" if res['d_eff'] is not None else "N/A"
    ratio = res['chi2'] / chi2_newton
    symbole = "✓" if res['chi2'] < chi2_newton else "✗"

    print(f"{nom:<35} {d_eff_str:<15} {res['chi2']:<12.2f} {res['rms']:<12.2f} {ratio:.2f}× {symbole}")

# Identifier le meilleur
meilleur_nom, meilleur_res = resultats_tries[0]
print(f"\n🏆 MEILLEUR : {meilleur_nom}")
print(f"   χ² = {meilleur_res['chi2']:.2f}")
print(f"   Amélioration vs Newton : {((chi2_newton - meilleur_res['chi2'])/chi2_newton * 100):.1f}%")

# Facteurs f(d) pour les échelles recommandées
print("\n" + "=" * 80)
print("FACTEURS D'ATTÉNUATION f(d)")
print("=" * 80)

distances_test = [5, 10, 20, 30, 50, 100]
print(f"\n{'Distance':<12}", end="")
for nom in ['d_eff = 50 kpc (rayon halo)', 'd_eff = 70 kpc (moyenne)', 'd_eff = 100 kpc (rayon viral)']:
    print(f"{nom:<30}", end="")
print()
print("-" * 102)

for d in distances_test:
    print(f"{d} kpc{'':<7}", end="")
    for nom in ['d_eff = 50 kpc (rayon halo)', 'd_eff = 70 kpc (moyenne)', 'd_eff = 100 kpc (rayon viral)']:
        d_eff_val = echelles_test[nom]
        f = facteur_expansion(d, d_eff_val)
        print(f"{f:.6f} ({(1-f)*100:.1f}%){'':<8}", end="")
    print()

# Visualisation
print("\n" + "=" * 80)
print("GÉNÉRATION DES GRAPHIQUES")
print("=" * 80)

fig = plt.figure(figsize=(16, 12))

# Graphique 1 : Courbes de rotation
ax1 = plt.subplot(2, 3, 1)
plt.errorbar(r_obs, v_obs, yerr=v_err, fmt='o', color='black',
             label='Observations', markersize=6, capsize=4, capthick=1.5, zorder=10)

plt.plot(r_array, v_newton, '--', color='blue', linewidth=2, label='Newton', alpha=0.7)

couleurs = ['red', 'green', 'orange', 'purple']
styles = ['-', '-', '-', '--']
idx = 0
for nom in ['d_eff = 50 kpc (rayon halo)', 'd_eff = 70 kpc (moyenne)',
            'd_eff = 100 kpc (rayon viral)', 'd_eff = 10 kpc (optimisation)']:
    if nom in resultats:
        plt.plot(r_array, resultats[nom]['courbe'], styles[idx],
                color=couleurs[idx], linewidth=2, label=nom.split('(')[0], alpha=0.9)
        idx += 1

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Vitesse (km/s)', fontsize=12)
plt.title('Courbes de Rotation - Comparaison Échelles', fontsize=14, fontweight='bold')
plt.legend(fontsize=9, loc='lower right')
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(0, 250)

# Graphique 2 : χ² vs d_eff
ax2 = plt.subplot(2, 3, 2)

d_eff_vals = []
chi2_vals = []
for nom, res in resultats.items():
    if res['d_eff'] is not None and res['d_eff'] < 1000:
        d_eff_vals.append(res['d_eff'])
        chi2_vals.append(res['chi2'])

plt.scatter(d_eff_vals, chi2_vals, s=100, c='red', marker='o', zorder=5)
for i, nom in enumerate(['d_eff = 10 kpc (optimisation)', 'd_eff = 50 kpc (rayon halo)',
                          'd_eff = 70 kpc (moyenne)', 'd_eff = 100 kpc (rayon viral)']):
    if nom in resultats:
        plt.annotate(f"{resultats[nom]['d_eff']:.0f} kpc",
                    (resultats[nom]['d_eff'], resultats[nom]['chi2']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)

plt.axhline(chi2_newton, color='blue', linestyle='--', linewidth=2, label='Newton', alpha=0.7)
plt.xlabel('d_eff (kpc)', fontsize=12)
plt.ylabel('χ²', fontsize=12)
plt.title('Qualité d\'Ajustement vs Échelle', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xscale('log')

# Graphique 3 : Facteurs f(d)
ax3 = plt.subplot(2, 3, 3)

d_plot = np.linspace(0, 150, 300)
for nom, couleur in [('d_eff = 50 kpc (rayon halo)', 'green'),
                      ('d_eff = 70 kpc (moyenne)', 'orange'),
                      ('d_eff = 100 kpc (rayon viral)', 'purple')]:
    if nom in echelles_test:
        d_eff_val = echelles_test[nom]
        f_vals = [facteur_expansion(d, d_eff_val) for d in d_plot]
        plt.plot(d_plot, f_vals, '-', color=couleur, linewidth=2.5,
                label=f"{d_eff_val:.0f} kpc")

plt.axhline(1.0, color='black', linestyle='-', alpha=0.3)
plt.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
plt.axhline(0.1, color='gray', linestyle=':', alpha=0.5)

plt.xlabel('Distance (kpc)', fontsize=12)
plt.ylabel('f(d) = exp(-d/d_eff)', fontsize=12)
plt.title('Facteurs d\'Atténuation', fontsize=14, fontweight='bold')
plt.legend(fontsize=10, title='d_eff')
plt.grid(True, alpha=0.3)
plt.xlim(0, 150)
plt.ylim(0, 1.05)

# Graphique 4 : Résidus meilleur modèle
ax4 = plt.subplot(2, 3, 4)

v_meilleur = np.interp(r_obs, r_array, meilleur_res['courbe'])
residus_meilleur = (v_meilleur - v_obs) / v_obs * 100
residus_newton = (v_newton_interp - v_obs) / v_obs * 100

plt.plot(r_obs, residus_newton, 'o--', color='blue', linewidth=2,
         markersize=6, label='Newton')
plt.plot(r_obs, residus_meilleur, 's-', color='red', linewidth=2,
         markersize=7, label=meilleur_nom.split('(')[0])

plt.axhline(0, color='black', linestyle='-', linewidth=1)
plt.fill_between([0, 35], -10, 10, color='green', alpha=0.1)

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Résidu (%)', fontsize=12)
plt.title(f'Résidus - Meilleur Modèle ({meilleur_nom.split("(")[0]})',
         fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(-60, 20)

# Graphique 5 : Comparaison χ² (barres)
ax5 = plt.subplot(2, 3, 5)

modeles_plot = ['Newton', 'd_eff = 10 kpc (optimisation)', 'd_eff = 50 kpc (rayon halo)',
                'd_eff = 70 kpc (moyenne)', 'd_eff = 100 kpc (rayon viral)']
chi2_plot = [resultats[m]['chi2'] for m in modeles_plot]
couleurs_plot = ['blue', 'red', 'green', 'orange', 'purple']

bars = plt.bar(range(len(modeles_plot)), chi2_plot, color=couleurs_plot, alpha=0.7, edgecolor='black')
plt.axhline(chi2_newton, color='black', linestyle='--', linewidth=1, alpha=0.5)

plt.xlabel('Modèle', fontsize=12)
plt.ylabel('χ²', fontsize=12)
plt.title('Comparaison χ² par Modèle', fontsize=14, fontweight='bold')
plt.xticks(range(len(modeles_plot)), [m.split('(')[0][:15] for m in modeles_plot],
          rotation=45, ha='right', fontsize=9)
plt.grid(True, alpha=0.3, axis='y')

# Valeurs sur barres
for i, (bar, val) in enumerate(zip(bars, chi2_plot)):
    plt.text(bar.get_x() + bar.get_width()/2, val + 30, f'{val:.0f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Graphique 6 : Tableau récapitulatif
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

tableau_data = [['Modèle', 'd_eff (kpc)', 'χ²', 'RMS (km/s)', 'Rang']]
for i, (nom, res) in enumerate(resultats_tries[:5]):
    d_eff_str = f"{res['d_eff']:.0f}" if res['d_eff'] is not None else "N/A"
    rang = "🏆" if i == 0 else f"#{i+1}"
    tableau_data.append([nom.split('(')[0][:20], d_eff_str, f"{res['chi2']:.1f}",
                        f"{res['rms']:.1f}", rang])

table = plt.table(cellText=tableau_data, cellLoc='left',
                 bbox=[0.05, 0.1, 0.9, 0.8])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style
for i in range(len(tableau_data)):
    if i == 0:
        for j in range(5):
            table[(i, j)].set_facecolor('#4CAF50')
            table[(i, j)].set_text_props(weight='bold', color='white')
    elif i == 1:
        for j in range(5):
            table[(i, j)].set_facecolor('#FFD700')

plt.title('Classement Final', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('test_echelles_recommandees.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé : test_echelles_recommandees.png")

# Conclusion
print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

if meilleur_res['chi2'] < chi2_newton:
    print(f"\n✓ Le modèle '{meilleur_nom}' est MEILLEUR que Newton !")
    print(f"  Amélioration χ² : {((chi2_newton - meilleur_res['chi2'])/chi2_newton * 100):.1f}%")
else:
    print(f"\n⚠ Aucun modèle Asselin n'est meilleur que Newton.")
    print(f"  Meilleur : '{meilleur_nom}' avec χ² = {meilleur_res['chi2']:.2f}")
    print(f"  Newton : χ² = {chi2_newton:.2f}")
    print(f"  Écart : {((meilleur_res['chi2'] - chi2_newton)/chi2_newton * 100):.1f}% pire")

print(f"\n📊 Parmi les échelles galactiques testées :")
echelles_gal = {k: v for k, v in resultats.items()
                if 'd_eff' in k and v['d_eff'] is not None and v['d_eff'] < 200}
meilleur_gal = min(echelles_gal.items(), key=lambda x: x[1]['chi2'])
print(f"  Meilleure échelle galactique : {meilleur_gal[0]}")
print(f"  χ² = {meilleur_gal[1]['chi2']:.2f}")
print(f"  d_eff = {meilleur_gal[1]['d_eff']:.0f} kpc")

print("\n" + "=" * 80)
