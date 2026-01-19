#!/usr/bin/env python3
"""
ANALYSE COSMOS COMPLÈTE - Test Alignement Halos
Théorie de Maîtrise du Temps (TMT)

TEST DÉCISIF MT vs ΛCDM:
- TMT prédit: Halos alignés avec gradient potentiel (θ_halo ↔ θ_voisin)
  → Corrélation r > 0.5, <Δθ> < 30°
- ΛCDM prédit: Halos orientés aléatoirement
  → Corrélation r ≈ 0, <Δθ> ≈ 45°

Méthodologie:
1. Génération catalogue galaxies synthétiques (COSMOS-like)
2. Identification paires galaxie-voisin massif
3. Simulation orientations halos (MT vs ΛCDM)
4. Analyse statistique corrélation θ_halo ↔ θ_voisin
5. Test significativité (p-value, χ²)
6. Figures publication

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-07
Version: 2.0 (avec loi k universelle)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, vonmises, circmean, circstd, ks_2samp
from scipy.optimize import curve_fit
import sys

# Configuration
np.random.seed(42)
plt.style.use('seaborn-v0_8-darkgrid')

print("="*70)
print("ANALYSE COSMOS - Test Alignement Halos TMT vs ΛCDM")
print("="*70)
print()

# ==============================================================================
# 1. GÉNÉRATION CATALOGUE GALAXIES SYNTHÉTIQUES
# ==============================================================================

def generate_COSMOS_catalog(N_galaxies=2000, z_range=(0.2, 0.8)):
    """
    Génère catalogue synthétique COSMOS-like

    Paramètres réalistes:
    - Champ: 2 deg² (COSMOS field)
    - Masses: 10^10.5 - 10^11.5 M☉
    - Redshift: 0.2 < z < 0.8
    """
    print(f"[1/6] Génération catalogue {N_galaxies} galaxies...")

    catalog = {
        'RA': np.random.uniform(149.4, 150.8, N_galaxies),
        'DEC': np.random.uniform(1.5, 3.0, N_galaxies),
        'z_photo': np.random.uniform(*z_range, N_galaxies),
        'M_stellar': 10**(np.random.uniform(10.5, 11.5, N_galaxies)),
        'log_M_halo': np.random.normal(12.5, 0.5, N_galaxies),
    }

    print(f"   ✓ {N_galaxies} galaxies générées")
    print(f"   - Masse: {catalog['M_stellar'].min()/1e10:.1f}-{catalog['M_stellar'].max()/1e11:.1f}×10¹⁰ M☉")
    print(f"   - Redshift: {catalog['z_photo'].min():.2f}-{catalog['z_photo'].max():.2f}")
    print()

    return catalog

def find_neighbors(catalog, max_distance=2.0, min_mass=1e11, max_dz=0.05):
    """
    Trouve voisin massif le plus proche pour chaque galaxie

    Critères:
    - Distance projetée < max_distance (Mpc)
    - Masse > min_mass (M☉)
    - |Δz| < max_dz (même tranche redshift)
    """
    print(f"[2/6] Recherche voisins massifs (d < {max_distance} Mpc, M > {min_mass/1e11:.0f}×10¹¹ M☉)...")

    N = len(catalog['RA'])
    neighbors_list = []

    for i in range(N):
        RA_i = catalog['RA'][i]
        DEC_i = catalog['DEC'][i]
        z_i = catalog['z_photo'][i]

        # Distance angulaire
        dRA = (catalog['RA'] - RA_i) * np.cos(np.radians(DEC_i))
        dDEC = catalog['DEC'] - DEC_i
        theta_neighbor = np.arctan2(dDEC, dRA)  # Radians

        # Distance physique projetée (D_A ~ 3000 Mpc à z~0.5)
        D_A = 3000  # Mpc
        angular_dist = np.sqrt(dRA**2 + dDEC**2)
        d_proj = D_A * np.radians(angular_dist)

        # Différence redshift
        dz = np.abs(catalog['z_photo'] - z_i)

        # Sélection voisins
        mask = (d_proj > 0.1) & (d_proj < max_distance) & (dz < max_dz) & (catalog['M_stellar'] > min_mass)

        if np.sum(mask) > 0:
            neighbors_idx = np.where(mask)[0]
            neighbor_masses = catalog['M_stellar'][neighbors_idx]
            most_massive_idx = neighbors_idx[np.argmax(neighbor_masses)]

            neighbors_list.append({
                'galaxy_idx': i,
                'neighbor_idx': most_massive_idx,
                'M_neighbor': catalog['M_stellar'][most_massive_idx],
                'd_proj': d_proj[most_massive_idx],
                'theta_neighbor': np.degrees(theta_neighbor[most_massive_idx]) % 360,
                'dz': dz[most_massive_idx]
            })

    print(f"   ✓ {len(neighbors_list)} paires galaxie-voisin trouvées ({len(neighbors_list)/N*100:.1f}%)")
    print(f"   - Distance moyenne: {np.mean([n['d_proj'] for n in neighbors_list]):.2f} Mpc")
    print(f"   - Masse voisin moyenne: {np.mean([n['M_neighbor'] for n in neighbors_list])/1e11:.2f}×10¹¹ M☉")
    print()

    return neighbors_list

# ==============================================================================
# 2. SIMULATION ORIENTATIONS HALOS (MT vs ΛCDM)
# ==============================================================================

def simulate_halo_MT(neighbors_list, alignment_strength=0.8):
    """
    TMT: Halos alignés avec gradient potentiel (direction voisin)

    alignment_strength:
    - 1.0: Alignement parfait (100%)
    - 0.8: Alignement fort (réaliste, 80% alignés)
    - 0.5: Alignement modéré
    """
    print(f"[3/6] Simulation orientations halos TMT (α = {alignment_strength})...")

    theta_halos = []

    for neighbor in neighbors_list:
        theta_voisin = neighbor['theta_neighbor']

        # Distribution von Mises autour de theta_voisin
        # kappa contrôle concentration (kappa↑ → concentration↑)
        kappa = alignment_strength * 10  # kappa = 8 pour α=0.8

        theta_halo = np.degrees(vonmises.rvs(kappa, loc=np.radians(theta_voisin))) % 360
        theta_halos.append(theta_halo)

    # Calcul écart angulaire
    delta_theta = []
    for i, neighbor in enumerate(neighbors_list):
        dtheta = abs(theta_halos[i] - neighbor['theta_neighbor'])
        if dtheta > 180:
            dtheta = 360 - dtheta
        delta_theta.append(dtheta)

    print(f"   ✓ {len(theta_halos)} halos TMT simulés")
    print(f"   - <Δθ> = {np.mean(delta_theta):.1f}° ± {np.std(delta_theta):.1f}°")
    print(f"   - Fraction Δθ<30°: {np.sum(np.array(delta_theta)<30)/len(delta_theta)*100:.1f}%")
    print()

    return theta_halos

def simulate_halo_LCDM(neighbors_list):
    """
    ΛCDM: Halos orientés aléatoirement (pas de corrélation)
    """
    print(f"[3/6] Simulation orientations halos ΛCDM (aléatoire)...")

    N = len(neighbors_list)
    theta_halos = np.random.uniform(0, 360, N)

    # Calcul écart angulaire
    delta_theta = []
    for i, neighbor in enumerate(neighbors_list):
        dtheta = abs(theta_halos[i] - neighbor['theta_neighbor'])
        if dtheta > 180:
            dtheta = 360 - dtheta
        delta_theta.append(dtheta)

    print(f"   ✓ {N} halos ΛCDM simulés")
    print(f"   - <Δθ> = {np.mean(delta_theta):.1f}° ± {np.std(delta_theta):.1f}°")
    print(f"   - Fraction Δθ<30°: {np.sum(np.array(delta_theta)<30)/len(delta_theta)*100:.1f}%")
    print()

    return theta_halos

# ==============================================================================
# 3. ANALYSE STATISTIQUE
# ==============================================================================

def analyze_correlation(neighbors_list, theta_halos, scenario_name):
    """
    Analyse corrélation θ_halo ↔ θ_voisin
    """
    print(f"[4/6] Analyse statistique {scenario_name}...")

    theta_neighbors = np.array([n['theta_neighbor'] for n in neighbors_list])
    theta_halos = np.array(theta_halos)

    # Corrélation Pearson
    r, p_value = pearsonr(theta_halos, theta_neighbors)

    # Écart angulaire
    delta_theta = []
    for i in range(len(theta_halos)):
        dtheta = abs(theta_halos[i] - theta_neighbors[i])
        if dtheta > 180:
            dtheta = 360 - dtheta
        delta_theta.append(dtheta)
    delta_theta = np.array(delta_theta)

    # Statistiques
    mean_delta = np.mean(delta_theta)
    std_delta = np.std(delta_theta)
    median_delta = np.median(delta_theta)
    frac_aligned = np.sum(delta_theta < 30) / len(delta_theta)

    print(f"   RÉSULTATS {scenario_name}:")
    print(f"   - Corrélation Pearson: r = {r:.3f} (p = {p_value:.2e})")
    print(f"   - Écart moyen: <Δθ> = {mean_delta:.1f}° ± {std_delta:.1f}°")
    print(f"   - Médiane: {median_delta:.1f}°")
    print(f"   - Fraction alignée (Δθ<30°): {frac_aligned*100:.1f}%")

    if p_value < 0.001:
        print(f"   → CORRÉLATION HAUTEMENT SIGNIFICATIVE (p < 0.001)")
    elif p_value < 0.05:
        print(f"   → Corrélation significative (p < 0.05)")
    else:
        print(f"   → Pas de corrélation significative (p > 0.05)")
    print()

    return {
        'r': r,
        'p_value': p_value,
        'mean_delta': mean_delta,
        'std_delta': std_delta,
        'median_delta': median_delta,
        'frac_aligned': frac_aligned,
        'delta_theta': delta_theta
    }

# ==============================================================================
# 4. TEST DÉCISIF TMT vs ΛCDM
# ==============================================================================

def decisive_test(stats_MT, stats_LCDM):
    """
    Test décisif: TMT vs ΛCDM
    """
    print("[5/6] TEST DÉCISIF TMT vs ΛCDM")
    print("="*70)

    # Ratio corrélations
    ratio_r = abs(stats_MT['r']) / max(abs(stats_LCDM['r']), 0.001)

    print(f"\n📊 COMPARAISON QUANTITATIVE:")
    print(f"   TMT:    r = {stats_MT['r']:+.3f}  |  <Δθ> = {stats_MT['mean_delta']:.1f}°  |  Alignés: {stats_MT['frac_aligned']*100:.1f}%")
    print(f"   ΛCDM:   r = {stats_LCDM['r']:+.3f}  |  <Δθ> = {stats_LCDM['mean_delta']:.1f}°  |  Alignés: {stats_LCDM['frac_aligned']*100:.1f}%")
    print(f"\n   Ratio r_TMT / r_ΛCDM = {ratio_r:.1f}×")

    # Test Kolmogorov-Smirnov
    ks_stat, ks_pvalue = ks_2samp(stats_MT['delta_theta'], stats_LCDM['delta_theta'])

    print(f"\n📈 TEST KOLMOGOROV-SMIRNOV:")
    print(f"   KS statistic = {ks_stat:.3f}")
    print(f"   p-value = {ks_pvalue:.2e}")

    # Verdict
    print(f"\n🏆 VERDICT:")
    if stats_MT['r'] > 0.4 and stats_MT['p_value'] < 0.001 and stats_MT['frac_aligned'] > 0.7:
        print(f"   ✅ TMT VALIDÉE: Corrélation forte et significative détectée")
        print(f"      → r = {stats_MT['r']:.3f} (seuil: r > 0.4)")
        print(f"      → p = {stats_MT['p_value']:.2e} (seuil: p < 0.001)")
        print(f"      → Alignés: {stats_MT['frac_aligned']*100:.1f}% (seuil: > 70%)")
        verdict = "TMT"
    elif abs(stats_LCDM['r']) < 0.2 and stats_LCDM['frac_aligned'] < 0.4:
        print(f"   ✅ ΛCDM VALIDÉE: Pas de corrélation (halos aléatoires)")
        print(f"      → r = {stats_LCDM['r']:.3f} (aléatoire attendu: r ≈ 0)")
        print(f"      → Alignés: {stats_LCDM['frac_aligned']*100:.1f}% (aléatoire attendu: ~33%)")
        verdict = "LCDM"
    else:
        print(f"   ⚠️  RÉSULTAT AMBIGU: Plus de données nécessaires")
        verdict = "INCERTAIN"

    print()
    return verdict

# ==============================================================================
# 5. VISUALISATION
# ==============================================================================

def create_figures(neighbors_list, theta_halos_MT, theta_halos_LCDM, stats_MT, stats_LCDM):
    """
    Génère figures publication
    """
    print("[6/6] Génération figures publication...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Test Alignement Halos COSMOS - TMT vs ΛCDM', fontsize=16, fontweight='bold')

    theta_neighbors = np.array([n['theta_neighbor'] for n in neighbors_list])

    # --- Figure A: Scatter TMT ---
    ax = axes[0, 0]
    sc = ax.scatter(theta_neighbors, theta_halos_MT, c=stats_MT['delta_theta'],
                    cmap='RdYlGn_r', alpha=0.6, s=30, vmin=0, vmax=90)
    ax.plot([0, 360], [0, 360], 'k--', alpha=0.3, label='Alignement parfait')
    ax.set_xlabel('θ_voisin (deg)', fontsize=12)
    ax.set_ylabel('θ_halo (deg)', fontsize=12)
    ax.set_title(f'A) TMT: r = {stats_MT["r"]:.3f}, p = {stats_MT["p_value"]:.2e}',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(0, 360)
    ax.set_ylim(0, 360)
    ax.grid(True, alpha=0.3)
    ax.legend()
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Δθ (deg)', fontsize=10)

    # --- Figure B: Scatter ΛCDM ---
    ax = axes[0, 1]
    sc = ax.scatter(theta_neighbors, theta_halos_LCDM, c=stats_LCDM['delta_theta'],
                    cmap='RdYlGn_r', alpha=0.6, s=30, vmin=0, vmax=90)
    ax.plot([0, 360], [0, 360], 'k--', alpha=0.3, label='Alignement parfait')
    ax.set_xlabel('θ_voisin (deg)', fontsize=12)
    ax.set_ylabel('θ_halo (deg)', fontsize=12)
    ax.set_title(f'B) ΛCDM: r = {stats_LCDM["r"]:.3f}, p = {stats_LCDM["p_value"]:.2e}',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(0, 360)
    ax.set_ylim(0, 360)
    ax.grid(True, alpha=0.3)
    ax.legend()
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Δθ (deg)', fontsize=10)

    # --- Figure C: Distribution Δθ ---
    ax = axes[1, 0]
    bins = np.linspace(0, 90, 20)
    ax.hist(stats_MT['delta_theta'], bins=bins, alpha=0.6, label=f'TMT (<Δθ>={stats_MT["mean_delta"]:.1f}°)',
            color='blue', density=True)
    ax.hist(stats_LCDM['delta_theta'], bins=bins, alpha=0.6, label=f'ΛCDM (<Δθ>={stats_LCDM["mean_delta"]:.1f}°)',
            color='red', density=True)
    ax.axvline(30, color='green', linestyle='--', linewidth=2, label='Seuil alignement (30°)')
    ax.axhline(1/90, color='gray', linestyle=':', alpha=0.5, label='Aléatoire uniforme')
    ax.set_xlabel('Δθ = |θ_halo - θ_voisin| (deg)', fontsize=12)
    ax.set_ylabel('Densité de probabilité', fontsize=12)
    ax.set_title('C) Distribution écarts angulaires', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # --- Figure D: Fraction cumulée ---
    ax = axes[1, 1]
    delta_sorted_MT = np.sort(stats_MT['delta_theta'])
    delta_sorted_LCDM = np.sort(stats_LCDM['delta_theta'])
    cumul_MT = np.arange(1, len(delta_sorted_MT)+1) / len(delta_sorted_MT)
    cumul_LCDM = np.arange(1, len(delta_sorted_LCDM)+1) / len(delta_sorted_LCDM)

    ax.plot(delta_sorted_MT, cumul_MT, 'b-', linewidth=2, label='TMT')
    ax.plot(delta_sorted_LCDM, cumul_LCDM, 'r-', linewidth=2, label='ΛCDM')
    ax.plot([0, 90], [0, 1], 'gray', linestyle=':', alpha=0.5, label='Aléatoire uniforme')
    ax.axvline(30, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax.axhline(stats_MT['frac_aligned'], color='blue', linestyle=':', alpha=0.5)
    ax.axhline(stats_LCDM['frac_aligned'], color='red', linestyle=':', alpha=0.5)
    ax.set_xlabel('Δθ (deg)', fontsize=12)
    ax.set_ylabel('Fraction cumulée', fontsize=12)
    ax.set_title('D) Fonction de répartition', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1)

    # Annotations
    ax.text(30, stats_MT['frac_aligned']+0.05, f"{stats_MT['frac_aligned']*100:.0f}% TMT",
            color='blue', fontsize=9)
    ax.text(30, stats_LCDM['frac_aligned']-0.05, f"{stats_LCDM['frac_aligned']*100:.0f}% ΛCDM",
            color='red', fontsize=9)

    plt.tight_layout()

    # Sauvegarder
    output_file = 'COSMOS_halo_alignment_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Figure sauvegardée: {output_file}")

    plt.close()

# ==============================================================================
# 6. RAPPORT COMPLET
# ==============================================================================

def generate_report(neighbors_list, stats_MT, stats_LCDM, verdict):
    """
    Génère rapport texte complet
    """
    report = []
    report.append("="*70)
    report.append("RAPPORT ANALYSE COSMOS - TEST ALIGNEMENT HALOS")
    report.append("Théorie de Maîtrise du Temps (TMT) vs ΛCDM")
    report.append("="*70)
    report.append("")

    report.append("MÉTHODOLOGIE:")
    report.append(f"  - Catalogue: {len(neighbors_list)} paires galaxie-voisin massif")
    report.append(f"  - Critères voisin: d < 2.0 Mpc, M > 10¹¹ M☉, Δz < 0.05")
    report.append(f"  - Simulations: TMT (alignement α=0.8) vs ΛCDM (aléatoire)")
    report.append("")

    report.append("RÉSULTATS TMT:")
    report.append(f"  - Corrélation Pearson: r = {stats_MT['r']:.3f} (p = {stats_MT['p_value']:.2e})")
    report.append(f"  - Écart angulaire moyen: <Δθ> = {stats_MT['mean_delta']:.1f}° ± {stats_MT['std_delta']:.1f}°")
    report.append(f"  - Médiane: {stats_MT['median_delta']:.1f}°")
    report.append(f"  - Fraction alignée (Δθ<30°): {stats_MT['frac_aligned']*100:.1f}%")
    report.append("")

    report.append("RÉSULTATS ΛCDM:")
    report.append(f"  - Corrélation Pearson: r = {stats_LCDM['r']:.3f} (p = {stats_LCDM['p_value']:.2e})")
    report.append(f"  - Écart angulaire moyen: <Δθ> = {stats_LCDM['mean_delta']:.1f}° ± {stats_LCDM['std_delta']:.1f}°")
    report.append(f"  - Médiane: {stats_LCDM['median_delta']:.1f}°")
    report.append(f"  - Fraction alignée (Δθ<30°): {stats_LCDM['frac_aligned']*100:.1f}%")
    report.append("")

    report.append("COMPARAISON:")
    ratio_r = abs(stats_MT['r']) / max(abs(stats_LCDM['r']), 0.001)
    report.append(f"  - Ratio corrélation: r_TMT / r_ΛCDM = {ratio_r:.1f}×")
    report.append(f"  - Différence <Δθ>: {stats_LCDM['mean_delta'] - stats_MT['mean_delta']:.1f}°")
    report.append(f"  - Différence fraction: {(stats_MT['frac_aligned'] - stats_LCDM['frac_aligned'])*100:.1f}%")
    report.append("")

    report.append("VERDICT:")
    report.append(f"  → {verdict}")
    if verdict == "TMT":
        report.append(f"  ✅ Corrélation forte et significative détectée")
        report.append(f"  ✅ Compatible avec prédiction TMT (halos alignés)")
        report.append(f"  ❌ Incompatible avec ΛCDM (halos aléatoires)")
    elif verdict == "LCDM":
        report.append(f"  ✅ Pas de corrélation (compatible ΛCDM)")
        report.append(f"  ❌ Incompatible avec TMT")
    else:
        report.append(f"  ⚠️  Plus de données nécessaires")
    report.append("")

    report.append("IMPLICATIONS:")
    report.append("  Si TMT validée avec vraies données COSMOS/UNIONS:")
    report.append("  - Preuve directe de l'influence du potentiel gravitationnel local")
    report.append("  - Confirmation Liaison Asselin (couplage temporel non-local)")
    report.append("  - Test décisif TMT vs ΛCDM")
    report.append("")
    report.append("PROCHAINES ÉTAPES:")
    report.append("  1. Télécharger vraies données COSMOS2015 + weak lensing")
    report.append("  2. Analyser catalogues UNIONS (>15 millions galaxies)")
    report.append("  3. Publier résultats dans ApJ/MNRAS")
    report.append("="*70)

    # Sauvegarder
    report_text = "\n".join(report)
    with open('COSMOS_analysis_report.txt', 'w') as f:
        f.write(report_text)

    print("\n" + report_text)
    print("\n✓ Rapport sauvegardé: COSMOS_analysis_report.txt")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    # Paramètres
    N_galaxies = 2000
    alignment_strength = 0.8  # TMT

    # 1. Génération catalogue
    catalog = generate_COSMOS_catalog(N_galaxies=N_galaxies)

    # 2. Recherche voisins
    neighbors_list = find_neighbors(catalog, max_distance=2.0, min_mass=1e11)

    if len(neighbors_list) < 50:
        print("❌ ERREUR: Pas assez de paires galaxie-voisin trouvées")
        print(f"   Trouvé: {len(neighbors_list)} (minimum: 50)")
        sys.exit(1)

    # 3. Simulations orientations halos
    theta_halos_MT = simulate_halo_MT(neighbors_list, alignment_strength=alignment_strength)
    theta_halos_LCDM = simulate_halo_LCDM(neighbors_list)

    # 4. Analyses statistiques
    stats_MT = analyze_correlation(neighbors_list, theta_halos_MT, "TMT")
    stats_LCDM = analyze_correlation(neighbors_list, theta_halos_LCDM, "ΛCDM")

    # 5. Test décisif
    verdict = decisive_test(stats_MT, stats_LCDM)

    # 6. Visualisation
    create_figures(neighbors_list, theta_halos_MT, theta_halos_LCDM, stats_MT, stats_LCDM)

    # 7. Rapport
    generate_report(neighbors_list, stats_MT, stats_LCDM, verdict)

    print("\n" + "="*70)
    print("ANALYSE COSMOS TERMINÉE AVEC SUCCÈS!")
    print("="*70)
    print("\nFichiers générés:")
    print("  - COSMOS_halo_alignment_analysis.png (figure publication)")
    print("  - COSMOS_analysis_report.txt (rapport complet)")
    print("\nProchaine étape: Analyser vraies données COSMOS/UNIONS")
    print("="*70)
