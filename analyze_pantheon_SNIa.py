#!/usr/bin/env python3
"""
Analyse Pantheon+ SNIa - Test Expansion Différentielle
Théorie de Maîtrise du Temps

Test: SNIa dans vides vs amas ont distances différentes
Prédiction MT: Δd_L(vide-amas) ~ 5-10% à z fixe

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-06
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import ttest_ind
from scipy.optimize import minimize

# Paramètres cosmologiques
H0 = 70  # km/s/Mpc
Omega_m = 0.315
Omega_Lambda_eff = 0.685
c_km_s = 299792.458  # km/s

def H_MT(z, rho_ratio, beta=0.4):
    """Fonction de Hubble Maîtrise du Temps"""
    term_matter = Omega_m * (1 + z)**3
    term_Lambda = Omega_Lambda_eff * np.exp(beta * (1 - rho_ratio))
    return H0 * np.sqrt(term_matter + term_Lambda)

def H_LCDM(z):
    """Fonction de Hubble Lambda-CDM"""
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda_eff)

def luminosity_distance_MT(z_target, rho_ratio, beta=0.4):
    """
    Distance de luminosité MT en Mpc
    d_L = (1+z) ∫₀^z c/H(z', ρ) dz'
    """
    def integrand(z):
        return c_km_s / H_MT(z, rho_ratio, beta)

    integral, _ = quad(integrand, 0, z_target, limit=100)
    d_L = (1 + z_target) * integral
    return d_L

def luminosity_distance_LCDM(z_target):
    """Distance de luminosité LCDM en Mpc"""
    def integrand(z):
        return c_km_s / H_LCDM(z)

    integral, _ = quad(integrand, 0, z_target, limit=100)
    d_L = (1 + z_target) * integral
    return d_L

def distance_modulus(d_L_Mpc):
    """
    Module de distance μ = 5 log₁₀(d_L/10pc)
    d_L en Mpc → μ
    """
    d_L_pc = d_L_Mpc * 1e6  # Mpc → pc
    return 5 * np.log10(d_L_pc / 10)

# ============================================
# TÉLÉCHARGEMENT DONNÉES PANTHEON+
# ============================================

def download_pantheon_data():
    """
    Télécharge catalogue Pantheon+ SNIa
    """
    print("Téléchargement données Pantheon+...")
    print("Note: Pour vraie analyse, télécharger depuis:")
    print("  https://github.com/PantheonPlusSH0ES/DataRelease")
    print()
    print("Pour démonstration, générons données synthétiques...")

    # DÉMONSTRATION: Générer données synthétiques
    # En pratique: télécharger vraies données Pantheon+

    np.random.seed(42)
    n_sn = 300

    # Redshifts
    z = np.random.uniform(0.01, 1.2, n_sn)

    # Environnements (classification simulée)
    # 40% vide, 40% moyen, 20% amas
    env_type = np.random.choice(['void', 'mean', 'cluster'],
                                size=n_sn, p=[0.4, 0.4, 0.2])

    rho_map = {'void': 0.3, 'mean': 1.0, 'cluster': 5.0}
    rho_ratios = [rho_map[e] for e in env_type]

    # Générer magnitudes apparentes avec MT
    m_obs = []
    for z_i, rho_i in zip(z, rho_ratios):
        # Distance luminosité MT
        d_L = luminosity_distance_MT(z_i, rho_i, beta=0.4)
        mu = distance_modulus(d_L)

        # Magnitude absolue SNIa ~ -19.3
        M_abs = -19.3
        m = M_abs + mu

        # Ajouter bruit observationnel
        m += np.random.normal(0, 0.15)  # σ ~ 0.15 mag

        m_obs.append(m)

    df = pd.DataFrame({
        'z': z,
        'mB': m_obs,  # Magnitude B apparente
        'environment': env_type,
        'rho_ratio': rho_ratios
    })

    df = df.sort_values('z').reset_index(drop=True)

    print(f"✓ {len(df)} SNIa générées")
    print(f"  Vides: {(df['environment']=='void').sum()}")
    print(f"  Moyenne: {(df['environment']=='mean').sum()}")
    print(f"  Amas: {(df['environment']=='cluster').sum()}")
    print()

    return df

# ============================================
# ANALYSE: DIFFÉRENCE VIDE vs AMAS
# ============================================

def analyze_environment_dependence(df):
    """
    Test: SNIa dans vides sont-elles plus proches qu'en amas?
    """
    print("="*60)
    print("ANALYSE: DÉPENDANCE ENVIRONNEMENT")
    print("="*60)
    print()

    # Sélectionner redshift bins
    z_bins = [(0.2, 0.4), (0.4, 0.6), (0.6, 0.8)]

    results = []

    for z_min, z_max in z_bins:
        print(f"\nBin redshift: {z_min} < z < {z_max}")

        mask_z = (df['z'] >= z_min) & (df['z'] < z_max)

        # SNIa dans vides
        mask_void = mask_z & (df['environment'] == 'void')
        mB_void = df.loc[mask_void, 'mB'].values

        # SNIa dans amas
        mask_cluster = mask_z & (df['environment'] == 'cluster')
        mB_cluster = df.loc[mask_cluster, 'mB'].values

        if len(mB_void) < 5 or len(mB_cluster) < 5:
            print("  ⚠ Pas assez de données")
            continue

        # Différence moyenne
        delta_mB = np.mean(mB_cluster) - np.mean(mB_void)

        # Test t de Student
        t_stat, p_value = ttest_ind(mB_cluster, mB_void)

        print(f"  N_void = {len(mB_void)}, N_cluster = {len(mB_cluster)}")
        print(f"  ⟨m_B⟩_cluster - ⟨m_B⟩_void = {delta_mB:+.3f} mag")
        print(f"  Test t: t = {t_stat:.2f}, p = {p_value:.3e}")

        # Interprétation
        # MT prédit: SNIa dans amas plus lointaines → m_B plus grande
        # Delta positif = cohérent MT

        if delta_mB > 0.05 and p_value < 0.05:
            print("  → ✓ COHÉRENT avec MT (amas plus lointains)")
        elif delta_mB < -0.05 and p_value < 0.05:
            print("  → ✗ INCOHÉRENT avec MT")
        else:
            print("  → Pas de différence significative")

        results.append({
            'z_center': (z_min + z_max) / 2,
            'delta_mB': delta_mB,
            'p_value': p_value,
            'n_void': len(mB_void),
            'n_cluster': len(mB_cluster)
        })

    return pd.DataFrame(results)

# ============================================
# CALIBRATION β
# ============================================

def calibrate_beta(df):
    """
    Calibre paramètre β pour minimiser χ²
    """
    print("\n" + "="*60)
    print("CALIBRATION PARAMÈTRE β")
    print("="*60)
    print()

    def chi_squared(beta):
        """
        Calcule χ² entre observations et prédictions MT
        """
        chi2 = 0
        M_abs = -19.3  # Magnitude absolue SNIa

        for i, row in df.iterrows():
            z_obs = row['z']
            mB_obs = row['mB']
            rho = row['rho_ratio']

            # Prédiction MT
            d_L_MT = luminosity_distance_MT(z_obs, rho, beta)
            mu_MT = distance_modulus(d_L_MT)
            mB_pred = M_abs + mu_MT

            # χ²
            sigma_mB = 0.15  # Erreur magnitude
            chi2 += ((mB_obs - mB_pred) / sigma_mB)**2

        return chi2

    # Minimisation
    print("Recherche β optimal...")

    result = minimize(chi_squared, x0=0.4, bounds=[(0.1, 0.8)], method='L-BFGS-B')

    beta_best = result.x[0]
    chi2_min = result.fun
    ndof = len(df) - 1

    print(f"  β optimal = {beta_best:.3f}")
    print(f"  χ²_min = {chi2_min:.1f}")
    print(f"  ndof = {ndof}")
    print(f"  χ²_red = {chi2_min/ndof:.2f}")

    if chi2_min / ndof < 1.5:
        print("  → ✓ Bon fit (χ²_red < 1.5)")
    else:
        print("  → ⚠ Fit moyen")

    return beta_best

# ============================================
# VISUALISATIONS
# ============================================

def plot_hubble_diagram(df, beta=0.4):
    """
    Diagramme de Hubble: mB vs z
    """
    print("\nCréation diagramme de Hubble...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Panel 1: Diagramme de Hubble par environnement
    colors = {'void': 'blue', 'mean': 'green', 'cluster': 'red'}
    labels = {'void': 'Vide', 'mean': 'Moyenne', 'cluster': 'Amas'}

    for env in ['void', 'mean', 'cluster']:
        mask = df['environment'] == env
        ax1.scatter(df.loc[mask, 'z'], df.loc[mask, 'mB'],
                   alpha=0.6, s=30, color=colors[env], label=labels[env])

    # Prédictions MT et LCDM
    z_theory = np.linspace(0.01, 1.2, 100)
    M_abs = -19.3

    # MT pour différents environnements
    for env, rho in [('void', 0.3), ('mean', 1.0), ('cluster', 5.0)]:
        mB_MT = [M_abs + distance_modulus(luminosity_distance_MT(z, rho, beta))
                 for z in z_theory]
        ax1.plot(z_theory, mB_MT, '--', color=colors[env], linewidth=2, alpha=0.7)

    # LCDM
    mB_LCDM = [M_abs + distance_modulus(luminosity_distance_LCDM(z))
               for z in z_theory]
    ax1.plot(z_theory, mB_LCDM, 'k:', linewidth=3, label='LCDM (uniforme)', alpha=0.8)

    ax1.set_xlabel('Redshift z', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Magnitude apparente m_B', fontsize=14, fontweight='bold')
    ax1.set_title('Diagramme de Hubble SNIa\nMT vs LCDM (β={:.2f})'.format(beta),
                  fontsize=16, fontweight='bold')
    ax1.legend(fontsize=12, loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.invert_yaxis()

    # Panel 2: Résidus
    for env in ['void', 'mean', 'cluster']:
        mask = df['environment'] == env
        residuals = []

        for i, row in df[mask].iterrows():
            z_i = row['z']
            mB_obs = row['mB']

            # Prédiction LCDM
            d_L_LCDM = luminosity_distance_LCDM(z_i)
            mB_LCDM = M_abs + distance_modulus(d_L_LCDM)

            residuals.append(mB_obs - mB_LCDM)

        ax2.scatter(df.loc[mask, 'z'], residuals,
                   alpha=0.6, s=30, color=colors[env], label=labels[env])

    ax2.axhline(0, color='black', linestyle='--', linewidth=2)
    ax2.set_xlabel('Redshift z', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Résidu: m_B_obs - m_B_LCDM (mag)', fontsize=14, fontweight='bold')
    ax2.set_title('Résidus par rapport à LCDM\nSignature expansion différentielle',
                  fontsize=16, fontweight='bold')
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)

    # Ajouter bandes ±1σ
    ax2.axhspan(-0.15, 0.15, alpha=0.2, color='gray', label='±1σ')

    plt.tight_layout()
    plt.savefig('figures/pantheon_hubble_diagram.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/pantheon_hubble_diagram.png")

def plot_distance_difference(df):
    """
    Δd_L(vide - amas) vs redshift
    """
    print("Création graphique différences de distance...")

    z_array = np.linspace(0.1, 1.0, 50)

    # Calculer différences pour β = 0.4
    beta = 0.4
    delta_d_L_percent = []

    for z in z_array:
        d_L_void = luminosity_distance_MT(z, 0.3, beta)
        d_L_cluster = luminosity_distance_MT(z, 5.0, beta)

        delta_percent = 100 * (d_L_cluster - d_L_void) / d_L_void
        delta_d_L_percent.append(delta_percent)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(z_array, delta_d_L_percent, linewidth=3, color='darkblue',
            label='MT (β=0.4): d_L(amas) - d_L(vide)')
    ax.axhline(0, color='red', linestyle='--', linewidth=2, label='LCDM (pas de différence)')

    # Zone prédiction
    ax.fill_between(z_array, 3, 10, alpha=0.2, color='green',
                    label='Prédiction MT: 3-10%')

    ax.set_xlabel('Redshift z', fontsize=15, fontweight='bold')
    ax.set_ylabel('Δd_L = (d_L_amas - d_L_vide) / d_L_vide (%)', fontsize=15, fontweight='bold')
    ax.set_title('Différence Distance Luminosité : Amas vs Vide\nSignature Expansion Différentielle',
                 fontsize=17, fontweight='bold')
    ax.legend(fontsize=13, loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/pantheon_distance_difference.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/pantheon_distance_difference.png")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    import os
    os.makedirs('figures', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    print("="*60)
    print("ANALYSE PANTHEON+ SNIa")
    print("Test Expansion Différentielle MT")
    print("="*60)
    print()

    # 1. Télécharger/générer données
    df = download_pantheon_data()

    # 2. Analyser dépendance environnement
    df_results = analyze_environment_dependence(df)

    # 3. Calibrer β
    beta_best = calibrate_beta(df)

    # 4. Visualisations
    plot_hubble_diagram(df, beta=beta_best)
    plot_distance_difference(df)

    # 5. Sauvegarder
    df.to_csv('data/pantheon_synthetic_data.csv', index=False)
    if len(df_results) > 0:
        df_results.to_csv('data/pantheon_analysis_results.csv', index=False)

    print("\n" + "="*60)
    print("RÉSUMÉ ANALYSE")
    print("="*60)
    print(f"✓ β calibré = {beta_best:.3f}")
    print("✓ Graphiques générés:")
    print("  - pantheon_hubble_diagram.png")
    print("  - pantheon_distance_difference.png")
    print()
    print("PROCHAINES ÉTAPES:")
    print("1. Télécharger vraies données Pantheon+ (GitHub)")
    print("2. Classifier environnement avec SDSS/catalogues vides")
    print("3. Refaire analyse avec vraies données")
    print("4. Si Δd_L(vide-amas) ~ 5-10% → MT VALIDÉE!")
    print("="*60)
