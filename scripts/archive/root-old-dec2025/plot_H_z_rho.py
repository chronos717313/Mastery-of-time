#!/usr/bin/env python3
"""
Graphiques H(z, ρ) - Expansion Différentielle
Théorie de Maîtrise du Temps vs Lambda-CDM

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-06
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Paramètres cosmologiques
H0 = 70  # km/s/Mpc
Omega_m = 0.315
Omega_Lambda_eff = 0.685
beta = 0.4  # Paramètre d'ancrage

def H_MT(z, rho_ratio, beta=0.4):
    """
    Fonction de Hubble Maîtrise du Temps

    H(z, ρ) = H₀ · √[Ωₘ(1+z)³ + ΩΛ_eff · exp(β · (1 - ρ/ρ_crit))]

    Parameters:
    - z: redshift
    - rho_ratio: ρ/ρ_critique (densité locale normalisée)
    - beta: paramètre d'ancrage

    Returns:
    - H(z, ρ) en km/s/Mpc
    """
    # Terme matière
    term_matter = Omega_m * (1 + z)**3

    # Terme énergie noire effective (dépend de ρ)
    term_Lambda = Omega_Lambda_eff * np.exp(beta * (1 - rho_ratio))

    # Hubble parameter
    H = H0 * np.sqrt(term_matter + term_Lambda)

    return H

def H_LCDM(z):
    """
    Fonction de Hubble Lambda-CDM standard
    """
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda_eff)

# ============================================
# GRAPHIQUE 1: H(z) pour différents environnements
# ============================================

def plot_H_z_environments():
    """
    H(z) pour vide, moyenne, filament, amas
    """
    print("Création graphique 1: H(z) par environnement...")

    z_array = np.linspace(0, 2, 200)

    # Environnements
    environments = {
        'Vide profond': 0.2,
        'Vide': 0.5,
        'Moyenne cosmique': 1.0,
        'Filament': 3.0,
        'Amas': 10.0,
        'Cœur amas': 50.0
    }

    colors = ['purple', 'blue', 'green', 'orange', 'red', 'darkred']

    fig, ax = plt.subplots(figsize=(14, 9))

    # Tracer H(z, ρ) pour chaque environnement
    for (env_name, rho_ratio), color in zip(environments.items(), colors):
        H_values = [H_MT(z, rho_ratio) for z in z_array]
        linestyle = '--' if env_name == 'Moyenne cosmique' else '-'
        linewidth = 3 if env_name == 'Moyenne cosmique' else 2
        ax.plot(z_array, H_values, label=f'{env_name} (ρ = {rho_ratio}ρ_crit)',
                color=color, linewidth=linewidth, linestyle=linestyle)

    # Lambda-CDM pour comparaison
    H_standard = [H_LCDM(z) for z in z_array]
    ax.plot(z_array, H_standard, label='Lambda-CDM (uniforme)',
            color='black', linewidth=2.5, linestyle=':')

    ax.set_xlabel('Redshift z', fontsize=16, fontweight='bold')
    ax.set_ylabel('H(z, ρ) [km/s/Mpc]', fontsize=16, fontweight='bold')
    ax.set_title('Expansion Différentielle : H(z, ρ) pour β = 0.4\nThéorie de Maîtrise du Temps',
                 fontsize=18, fontweight='bold')
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.tick_params(axis='both', labelsize=13)

    # Ajouter annotations
    ax.text(0.98, 0.05,
            'H(z, ρ) = H₀√[Ωₘ(1+z)³ + ΩΛ exp(β(1-ρ/ρ_crit))]\n'
            'Vides: expansion rapide (ΩΛ augmentée)\n'
            'Amas: expansion ralentie (ΩΛ réduite)',
            transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('figures/H_z_rho_environments.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/H_z_rho_environments.png")

    return fig

# ============================================
# GRAPHIQUE 2: Surface 3D H(z, ρ)
# ============================================

def plot_H_z_rho_3D():
    """
    Surface 3D de H(z, ρ)
    """
    print("Création graphique 2: Surface 3D H(z, ρ)...")

    z_array = np.linspace(0, 2, 100)
    rho_array = np.logspace(-1, 1.5, 100)  # 0.1 à 30 ρ_crit

    Z, RHO = np.meshgrid(z_array, rho_array)
    H_values = np.zeros_like(Z)

    for i in range(len(rho_array)):
        for j in range(len(z_array)):
            H_values[i, j] = H_MT(Z[i, j], RHO[i, j])

    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Surface
    surf = ax.plot_surface(Z, RHO, H_values, cmap=cm.viridis,
                          linewidth=0, antialiased=True, alpha=0.8)

    # Lambda-CDM (plan à ρ=1)
    H_lcdm_plane = np.array([[H_LCDM(z) for z in z_array] for _ in rho_array])
    ax.plot_surface(Z, RHO, H_lcdm_plane, color='red', alpha=0.3, linewidth=0)

    ax.set_xlabel('Redshift z', fontsize=14, fontweight='bold', labelpad=10)
    ax.set_ylabel('ρ/ρ_crit', fontsize=14, fontweight='bold', labelpad=10)
    ax.set_zlabel('H(z, ρ) [km/s/Mpc]', fontsize=14, fontweight='bold', labelpad=10)
    ax.set_title('Surface H(z, ρ) - Expansion Différentielle MT\n(Plan rouge = Lambda-CDM)',
                 fontsize=16, fontweight='bold', pad=20)

    ax.set_yscale('log')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='H(z, ρ)')

    plt.tight_layout()
    plt.savefig('figures/H_z_rho_3D_surface.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/H_z_rho_3D_surface.png")

    return fig

# ============================================
# GRAPHIQUE 3: Contours H(z, ρ)
# ============================================

def plot_H_z_rho_contours():
    """
    Carte de contours H(z, ρ)
    """
    print("Création graphique 3: Contours H(z, ρ)...")

    z_array = np.linspace(0, 2, 200)
    rho_array = np.logspace(-1, 1.5, 200)

    Z, RHO = np.meshgrid(z_array, rho_array)
    H_values = np.zeros_like(Z)

    for i in range(len(rho_array)):
        for j in range(len(z_array)):
            H_values[i, j] = H_MT(Z[i, j], RHO[i, j])

    fig, ax = plt.subplots(figsize=(14, 10))

    # Contours remplis
    contourf = ax.contourf(Z, RHO, H_values, levels=20, cmap='RdYlBu_r', alpha=0.8)

    # Lignes de contour
    contours = ax.contour(Z, RHO, H_values, levels=10, colors='black', linewidths=0.5, alpha=0.5)
    ax.clabel(contours, inline=True, fontsize=9, fmt='%d km/s/Mpc')

    # Ligne ρ = ρ_crit (Lambda-CDM)
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=3, label='ρ = ρ_crit (LCDM)')

    # Marquer environnements typiques
    environments_z = [0.5, 0.5, 0.5, 0.5]
    environments_rho = [0.2, 1.0, 3.0, 10.0]
    environments_labels = ['Vide', 'Moyenne', 'Filament', 'Amas']

    for z, rho, label in zip(environments_z, environments_rho, environments_labels):
        ax.plot(z, rho, 'o', markersize=12, color='yellow', markeredgecolor='black', markeredgewidth=2)
        ax.text(z+0.05, rho, label, fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('Redshift z', fontsize=16, fontweight='bold')
    ax.set_ylabel('ρ/ρ_crit (densité locale normalisée)', fontsize=16, fontweight='bold')
    ax.set_title('Carte H(z, ρ) - Expansion Différentielle\nThéorie de Maîtrise du Temps',
                 fontsize=18, fontweight='bold')
    ax.set_yscale('log')
    ax.legend(fontsize=13, loc='upper right')
    ax.grid(True, alpha=0.3)

    cbar = fig.colorbar(contourf, ax=ax)
    cbar.set_label('H(z, ρ) [km/s/Mpc]', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('figures/H_z_rho_contours.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/H_z_rho_contours.png")

    return fig

# ============================================
# GRAPHIQUE 4: Ratio H_MT / H_LCDM
# ============================================

def plot_H_ratio():
    """
    Ratio H_MT(z, ρ) / H_LCDM(z)
    """
    print("Création graphique 4: Ratio H_MT / H_LCDM...")

    z_array = np.linspace(0, 2, 200)

    environments = {
        'Vide (ρ=0.2ρ_crit)': 0.2,
        'Filament (ρ=3ρ_crit)': 3.0,
        'Amas (ρ=10ρ_crit)': 10.0,
    }

    fig, ax = plt.subplots(figsize=(14, 9))

    for env_name, rho_ratio in environments.items():
        ratio = [H_MT(z, rho_ratio) / H_LCDM(z) for z in z_array]
        ax.plot(z_array, ratio, label=env_name, linewidth=2.5)

    ax.axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='LCDM (ratio = 1)')

    ax.set_xlabel('Redshift z', fontsize=16, fontweight='bold')
    ax.set_ylabel('H_MT(z, ρ) / H_LCDM(z)', fontsize=16, fontweight='bold')
    ax.set_title('Ratio Expansion MT / LCDM\nβ = 0.4',
                 fontsize=18, fontweight='bold')
    ax.legend(fontsize=13, loc='best')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='both', labelsize=13)

    # Zone grisée ±10%
    ax.fill_between(z_array, 0.9, 1.1, alpha=0.2, color='gray', label='±10% de LCDM')

    plt.tight_layout()
    plt.savefig('figures/H_ratio_MT_LCDM.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/H_ratio_MT_LCDM.png")

    return fig

# ============================================
# GRAPHIQUE 5: Λ_eff(ρ) - Énergie Noire Effective
# ============================================

def plot_Lambda_eff():
    """
    Énergie noire effective vs densité
    """
    print("Création graphique 5: Λ_eff(ρ)...")

    rho_array = np.logspace(-1, 2, 300)  # 0.1 à 100 ρ_crit

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Panel 1: Λ_eff(ρ) / Λ₀
    beta_values = [0.2, 0.3, 0.4, 0.5, 0.6]

    for beta in beta_values:
        Lambda_eff = Omega_Lambda_eff * np.exp(beta * (1 - rho_array))
        ratio = Lambda_eff / Omega_Lambda_eff
        ax1.plot(rho_array, ratio, label=f'β = {beta}', linewidth=2.5)

    ax1.axhline(y=1.0, color='black', linestyle='--', linewidth=2, alpha=0.5)
    ax1.axvline(x=1.0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='ρ = ρ_crit')

    # Marquer environnements
    ax1.plot(0.2, np.exp(0.4 * 0.8), 'o', markersize=12, color='blue', label='Vide')
    ax1.plot(10, np.exp(0.4 * -9), 'o', markersize=12, color='red', label='Amas')

    ax1.set_xlabel('ρ/ρ_crit', fontsize=15, fontweight='bold')
    ax1.set_ylabel('Λ_eff / Λ₀', fontsize=15, fontweight='bold')
    ax1.set_title('Énergie Noire Effective\nΛ_eff(ρ) = Λ₀ exp[β(1-ρ/ρ_crit)]',
                  fontsize=16, fontweight='bold')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.legend(fontsize=12, loc='best')
    ax1.grid(True, alpha=0.3, which='both')

    # Panel 2: Ω_Lambda_eff(ρ) valeur absolue
    for beta in beta_values:
        Omega_Lambda_eff_rho = Omega_Lambda_eff * np.exp(beta * (1 - rho_array))
        ax2.plot(rho_array, Omega_Lambda_eff_rho, label=f'β = {beta}', linewidth=2.5)

    ax2.axhline(y=Omega_Lambda_eff, color='black', linestyle='--', linewidth=2, alpha=0.5, label='ΩΛ standard')
    ax2.axvline(x=1.0, color='red', linestyle='--', linewidth=2, alpha=0.5)

    ax2.set_xlabel('ρ/ρ_crit', fontsize=15, fontweight='bold')
    ax2.set_ylabel('Ω_Λ_eff(ρ)', fontsize=15, fontweight='bold')
    ax2.set_title('Densité Énergie Noire Locale\nΩ_Λ_eff = 0.685 × exp[β(1-ρ/ρ_crit)]',
                  fontsize=16, fontweight='bold')
    ax2.set_xscale('log')
    ax2.legend(fontsize=12, loc='best')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/Lambda_eff_rho.png', dpi=300, bbox_inches='tight')
    print("  ✓ Sauvegardé: figures/Lambda_eff_rho.png")

    return fig

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    import os
    os.makedirs('figures', exist_ok=True)

    print("="*60)
    print("GÉNÉRATION GRAPHIQUES H(z, ρ)")
    print("Théorie de Maîtrise du Temps - Expansion Différentielle")
    print("="*60)
    print()

    # Générer tous les graphiques
    plot_H_z_environments()
    plot_H_z_rho_3D()
    plot_H_z_rho_contours()
    plot_H_ratio()
    plot_Lambda_eff()

    print()
    print("="*60)
    print("✓ TOUS LES GRAPHIQUES GÉNÉRÉS")
    print("="*60)
    print("Fichiers créés dans: figures/")
    print("  1. H_z_rho_environments.png - H(z) par environnement")
    print("  2. H_z_rho_3D_surface.png - Surface 3D complète")
    print("  3. H_z_rho_contours.png - Carte de contours")
    print("  4. H_ratio_MT_LCDM.png - Ratio MT/LCDM")
    print("  5. Lambda_eff_rho.png - Énergie noire effective")
    print()
    print("Pour afficher: ouvrir les fichiers .png")
    print("Pour régénérer: python3 plot_H_z_rho.py")
