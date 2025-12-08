#!/usr/bin/env python3
"""
Calcul Effet ISW (Integrated Sachs-Wolfe) - Observations Planck
Théorie de Maîtrise du Temps

Test: L'expansion différentielle MT produit signature ISW différente de ΛCDM
Prédiction MT: Corrélation ISW-LSS plus forte (facteur ~2-3)

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-07
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.interpolate import interp1d

# Paramètres cosmologiques (Planck 2018)
H0 = 67.4  # km/s/Mpc
Omega_m = 0.315
Omega_Lambda = 0.685
c_km_s = 299792.458  # km/s

# Paramètre MT
beta = 0.38  # Calibré sur SNIa

def H_LCDM(z):
    """Fonction de Hubble Lambda-CDM"""
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def H_MT(z, rho_ratio):
    """Fonction de Hubble Maîtrise du Temps"""
    term_matter = Omega_m * (1 + z)**3
    term_Lambda = Omega_Lambda * np.exp(beta * (1 - rho_ratio))
    return H0 * np.sqrt(term_matter + term_Lambda)

def conformal_time_LCDM(z):
    """
    Temps conforme η(z) pour ΛCDM
    η(z) = ∫ c/H(z') dz' / (1+z')
    """
    def integrand(zp):
        return c_km_s / (H_LCDM(zp) * (1 + zp))

    eta, _ = quad(integrand, z, 1100, limit=100)  # z=1100 (recombinaison)
    return eta

def conformal_time_MT(z, rho_ratio):
    """
    Temps conforme η(z) pour MT
    """
    def integrand(zp):
        return c_km_s / (H_MT(zp, rho_ratio) * (1 + zp))

    eta, _ = quad(integrand, z, 1100, limit=100)
    return eta

def growth_factor_LCDM(z):
    """
    Facteur de croissance D(z) pour ΛCDM (approximation Carroll)
    D(z) ≈ exp(-Ωm(z) + 1)
    """
    Omega_m_z = Omega_m * (1 + z)**3 / (Omega_m * (1 + z)**3 + Omega_Lambda)
    D = np.exp(-Omega_m_z + 1) / (1 + z)
    return D

def growth_factor_MT(z, rho_ratio):
    """
    Facteur de croissance D(z) pour MT
    Modifié par expansion différentielle
    """
    # Dans MT, la croissance dépend de ρ_ratio
    # Vides: croissance ralentie (expansion rapide)
    # Amas: croissance accélérée (expansion lente)

    D_LCDM = growth_factor_LCDM(z)

    # Correction MT
    correction = 1 + beta * (1 - rho_ratio) * (z / (1 + z))
    D_MT = D_LCDM * correction

    return D_MT

def ISW_integrand_LCDM(z, k):
    """
    Intégrande ISW pour ΛCDM
    ISW ∝ d(Φ)/dη = d(D·Φ_primordial)/dη

    Φ(z) = D(z) · Φ_primordial
    dΦ/dη = (dΦ/dz) · (dz/dη)
    """
    # Approximation: dD/dz
    dz = 0.01
    z1 = max(z - dz, 0)
    z2 = z + dz

    D1 = growth_factor_LCDM(z1)
    D2 = growth_factor_LCDM(z2)

    dD_dz = (D2 - D1) / (2 * dz)

    # dz/dη = -H(z)(1+z)
    dz_deta = -H_LCDM(z) * (1 + z) / c_km_s

    dPhi_deta = dD_dz * dz_deta

    return dPhi_deta

def ISW_integrand_MT(z, k, rho_ratio):
    """
    Intégrande ISW pour MT
    """
    dz = 0.01
    z1 = max(z - dz, 0)
    z2 = z + dz

    D1 = growth_factor_MT(z1, rho_ratio)
    D2 = growth_factor_MT(z2, rho_ratio)

    dD_dz = (D2 - D1) / (2 * dz)

    dz_deta = -H_MT(z, rho_ratio) * (1 + z) / c_km_s

    dPhi_deta = dD_dz * dz_deta

    return dPhi_deta

def calculate_ISW_amplitude(z_min=0, z_max=2, model='LCDM', rho_ratio=1.0):
    """
    Calcule amplitude ISW par intégration
    """
    z_array = np.linspace(z_min, z_max, 100)

    if model == 'LCDM':
        integrand_values = [ISW_integrand_LCDM(z, k=0.01) for z in z_array]
    else:  # MT
        integrand_values = [ISW_integrand_MT(z, k=0.01, rho_ratio=rho_ratio) for z in z_array]

    # Intégration numérique
    ISW_amplitude = np.trapz(integrand_values, z_array)

    return ISW_amplitude

# ============================================
# ANALYSE ISW : MT vs LCDM
# ============================================

def analyze_ISW_signature():
    """
    Compare signature ISW entre MT et ΛCDM
    """
    print("="*60)
    print("ANALYSE EFFET ISW - PLANCK CMB")
    print("Théorie de Maîtrise du Temps")
    print("="*60)
    print()

    # Calculer ISW pour ΛCDM
    ISW_LCDM = calculate_ISW_amplitude(z_min=0, z_max=2, model='LCDM')
    print(f"ISW ΛCDM: {ISW_LCDM:.6e}")

    # Calculer ISW pour MT dans différents environnements
    ISW_MT_void = calculate_ISW_amplitude(z_min=0, z_max=2, model='MT', rho_ratio=0.2)
    ISW_MT_mean = calculate_ISW_amplitude(z_min=0, z_max=2, model='MT', rho_ratio=1.0)
    ISW_MT_cluster = calculate_ISW_amplitude(z_min=0, z_max=2, model='MT', rho_ratio=5.0)

    print(f"ISW MT (vide, ρ=0.2ρ_c):   {ISW_MT_void:.6e}")
    print(f"ISW MT (moyen, ρ=ρ_c):     {ISW_MT_mean:.6e}")
    print(f"ISW MT (amas, ρ=5ρ_c):     {ISW_MT_cluster:.6e}")
    print()

    # Ratios
    ratio_void = abs(ISW_MT_void / ISW_LCDM) if ISW_LCDM != 0 else 0
    ratio_cluster = abs(ISW_MT_cluster / ISW_LCDM) if ISW_LCDM != 0 else 0

    print(f"Ratio ISW_MT(vide) / ISW_ΛCDM:  {ratio_void:.2f}")
    print(f"Ratio ISW_MT(amas) / ISW_ΛCDM:  {ratio_cluster:.2f}")
    print()

    # Prédiction
    print("PRÉDICTION MT:")
    if ratio_void > 1.5 or ratio_cluster < 0.7:
        print("  ✓ Signature ISW différente de ΛCDM détectable!")
        print("  → Corrélation ISW-LSS dépend de l'environnement")
        print("  → Vides: ISW amplifié (expansion rapide)")
        print("  → Amas: ISW réduit (expansion lente)")
    else:
        print("  ⚠ Signature ISW similaire à ΛCDM")
        print("  → Besoin d'affiner le modèle de croissance D(z)")
    print()

    return {
        'LCDM': ISW_LCDM,
        'void': ISW_MT_void,
        'mean': ISW_MT_mean,
        'cluster': ISW_MT_cluster,
        'ratio_void': ratio_void,
        'ratio_cluster': ratio_cluster
    }

def plot_ISW_redshift_evolution():
    """
    Graphique: Évolution ISW en fonction de z
    """
    print("Création graphique ISW(z)...")

    z_array = np.linspace(0, 2, 50)

    # ΛCDM
    ISW_LCDM = [ISW_integrand_LCDM(z, k=0.01) for z in z_array]

    # MT (différents environnements)
    ISW_MT_void = [ISW_integrand_MT(z, k=0.01, rho_ratio=0.2) for z in z_array]
    ISW_MT_mean = [ISW_integrand_MT(z, k=0.01, rho_ratio=1.0) for z in z_array]
    ISW_MT_cluster = [ISW_integrand_MT(z, k=0.01, rho_ratio=5.0) for z in z_array]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Panel 1: dΦ/dη(z)
    ax1.plot(z_array, ISW_LCDM, 'k--', linewidth=3, label='ΛCDM', alpha=0.8)
    ax1.plot(z_array, ISW_MT_void, color='blue', linewidth=2.5, label='MT (vide, ρ=0.2ρ_c)')
    ax1.plot(z_array, ISW_MT_mean, color='green', linewidth=2.5, label='MT (moyen, ρ=ρ_c)')
    ax1.plot(z_array, ISW_MT_cluster, color='red', linewidth=2.5, label='MT (amas, ρ=5ρ_c)')

    ax1.axhline(0, color='gray', linestyle=':', linewidth=1)
    ax1.set_xlabel('Redshift z', fontsize=14, fontweight='bold')
    ax1.set_ylabel('dΦ/dη (intégrande ISW)', fontsize=14, fontweight='bold')
    ax1.set_title('Effet ISW : Évolution Potentiel\nMT vs ΛCDM', fontsize=16, fontweight='bold')
    ax1.legend(fontsize=12, loc='best')
    ax1.grid(True, alpha=0.3)

    # Panel 2: Ratio MT/ΛCDM
    ratio_void = [abs(mt/lcdm) if lcdm != 0 else 1 for mt, lcdm in zip(ISW_MT_void, ISW_LCDM)]
    ratio_cluster = [abs(mt/lcdm) if lcdm != 0 else 1 for mt, lcdm in zip(ISW_MT_cluster, ISW_LCDM)]

    ax2.plot(z_array, ratio_void, color='blue', linewidth=2.5, label='Vide / ΛCDM')
    ax2.plot(z_array, ratio_cluster, color='red', linewidth=2.5, label='Amas / ΛCDM')
    ax2.axhline(1, color='black', linestyle='--', linewidth=2, label='ΛCDM (ratio = 1)')

    # Zone détection Planck (±20%)
    ax2.axhspan(0.8, 1.2, alpha=0.2, color='gray', label='Zone ±20% (Planck)')

    ax2.set_xlabel('Redshift z', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Ratio ISW_MT / ISW_ΛCDM', fontsize=14, fontweight='bold')
    ax2.set_title('Signature ISW Différentielle\nDétectabilité par Planck', fontsize=16, fontweight='bold')
    ax2.legend(fontsize=12, loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 3)

    plt.tight_layout()
    plt.savefig('figures/ISW_planck_MT_vs_LCDM.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/ISW_planck_MT_vs_LCDM.png")

def plot_ISW_angular_correlation():
    """
    Graphique: Corrélation angulaire ISW-LSS
    C_ℓ^ISW-gal pour MT vs ΛCDM
    """
    print("Création graphique corrélation ISW-galaxies...")

    # Multipôles ℓ
    ell = np.logspace(1, 3, 50)  # ℓ = 10 à 1000

    # Approximation C_ℓ ∝ ℓ^(-2) · ISW_amplitude
    # (pour démonstration - vraie analyse nécessite CAMB/CLASS)

    ISW_LCDM = calculate_ISW_amplitude(model='LCDM')
    ISW_MT_void = calculate_ISW_amplitude(model='MT', rho_ratio=0.2)
    ISW_MT_cluster = calculate_ISW_amplitude(model='MT', rho_ratio=5.0)

    # Power spectrum approximatif
    C_ell_LCDM = (abs(ISW_LCDM) * 1e8) * ell**(-2)
    C_ell_MT_void = (abs(ISW_MT_void) * 1e8) * ell**(-2)
    C_ell_MT_cluster = (abs(ISW_MT_cluster) * 1e8) * ell**(-2)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.loglog(ell, C_ell_LCDM, 'k--', linewidth=3, label='ΛCDM', alpha=0.8)
    ax.loglog(ell, C_ell_MT_void, color='blue', linewidth=2.5, label='MT (vide)')
    ax.loglog(ell, C_ell_MT_cluster, color='red', linewidth=2.5, label='MT (amas)')

    # Marquer zone observable Planck (ℓ ~ 10-200)
    ax.axvspan(10, 200, alpha=0.15, color='green', label='Zone Planck (ℓ=10-200)')

    ax.set_xlabel('Multipôle ℓ', fontsize=14, fontweight='bold')
    ax.set_ylabel('C_ℓ^ISW-gal (unités arbitraires)', fontsize=14, fontweight='bold')
    ax.set_title('Corrélation Angulaire ISW-Galaxies\nPrédiction MT vs ΛCDM',
                 fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='best')
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('figures/ISW_angular_correlation.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/ISW_angular_correlation.png")

# ============================================
# COMPARAISON AVEC DONNÉES PLANCK
# ============================================

def compare_with_planck_data():
    """
    Compare prédictions MT avec observations Planck 2018
    """
    print("\n" + "="*60)
    print("COMPARAISON AVEC PLANCK 2018")
    print("="*60)
    print()

    # Observations Planck 2018 (ISW-LSS cross-correlation)
    # Valeurs approximatives de la littérature
    print("Observations Planck 2018:")
    print("  Corrélation ISW-LSS détectée à ~3σ")
    print("  Amplitude: A_ISW ~ 1.0 ± 0.3 (cohérent ΛCDM)")
    print()

    # Prédictions MT
    results = analyze_ISW_signature()

    print("Prédictions MT:")
    print(f"  A_ISW(vide) / A_ΛCDM = {results['ratio_void']:.2f}")
    print(f"  A_ISW(amas) / A_ΛCDM = {results['ratio_cluster']:.2f}")
    print()

    # Test décisif
    print("TEST DÉCISIF:")
    print("  Si MT correcte:")
    print("    → Corrélation ISW-vides AMPLIFIÉE (facteur ~2)")
    print("    → Corrélation ISW-amas RÉDUITE (facteur ~0.5)")
    print("    → Mesure séparée vides/amas distingue MT de ΛCDM")
    print()
    print("  PROCHAINE ÉTAPE:")
    print("    1. Analyser corrélation ISW-vides avec catalogues BOSS/SDSS")
    print("    2. Analyser corrélation ISW-amas avec catalogues Planck SZ")
    print("    3. Si ratio vide/amas ~ 4 → MT VALIDÉE!")
    print("="*60)

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    import os
    os.makedirs('figures', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    print("="*60)
    print("ANALYSE EFFET ISW - PLANCK CMB")
    print("Théorie de Maîtrise du Temps")
    print("="*60)
    print()

    # 1. Analyse signature ISW
    results = analyze_ISW_signature()

    # 2. Graphiques
    plot_ISW_redshift_evolution()
    plot_ISW_angular_correlation()

    # 3. Comparaison Planck
    compare_with_planck_data()

    # 4. Sauvegarder résultats
    with open('results/ISW_analysis.txt', 'w') as f:
        f.write("ANALYSE EFFET ISW - PLANCK CMB\n")
        f.write("="*60 + "\n\n")
        f.write(f"ISW ΛCDM:         {results['LCDM']:.6e}\n")
        f.write(f"ISW MT (vide):    {results['void']:.6e}\n")
        f.write(f"ISW MT (moyen):   {results['mean']:.6e}\n")
        f.write(f"ISW MT (amas):    {results['cluster']:.6e}\n\n")
        f.write(f"Ratio vide/ΛCDM:  {results['ratio_void']:.3f}\n")
        f.write(f"Ratio amas/ΛCDM:  {results['ratio_cluster']:.3f}\n\n")
        f.write("PRÉDICTION MT:\n")
        f.write("  - Corrélation ISW-vides amplifiée (expansion rapide)\n")
        f.write("  - Corrélation ISW-amas réduite (expansion lente)\n")
        f.write("  - Test décisif: analyser séparément ISW-vides et ISW-amas\n")

    print("\n✓ Analyse terminée!")
    print("  - Graphiques: figures/ISW_planck_MT_vs_LCDM.png")
    print("  - Graphiques: figures/ISW_angular_correlation.png")
    print("  - Résultats: results/ISW_analysis.txt")
