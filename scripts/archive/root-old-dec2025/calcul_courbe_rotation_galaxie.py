#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcul de la Courbe de Rotation Galactique
Théorie de Maîtrise du Temps - Validation Liaison Asselin

Ce script calcule la courbe de rotation d'une galaxie spirale (Voie Lactée)
en utilisant la formulation de la Liaison Asselin avec effet cumulatif.

Objectif : Vérifier si la Liaison Asselin peut expliquer les courbes de rotation
plates observées SANS matière noire exotique.

Formules :
    L_Asselin(M₁, M₂, d) = √(M₁·M₂) / d² · exp(-d/d_horizon)
    v(r) = √(G·M_eff(r) / r)  où M_eff inclut l'effet cumulatif Asselin

Date : 2025-12-04
Version : 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# ============================================================================
# CONSTANTES PHYSIQUES FONDAMENTALES
# ============================================================================

# Constante gravitationnelle (SI)
G = 6.67430e-11  # m³/(kg·s²)

# Vitesse de la lumière (SI)
c = 299792458  # m/s

# Âge de l'univers
t_0 = 13.8e9 * 365.25 * 24 * 3600  # secondes (13.8 Ga)

# Distance horizon gravitationnel
d_horizon = c * t_0  # mètres
d_horizon_kpc = d_horizon / (3.086e19)  # en kpc

print("=" * 80)
print("CALCUL DE COURBE DE ROTATION GALACTIQUE")
print("Théorie de Maîtrise du Temps - Liaison Asselin")
print("=" * 80)
print(f"\nConstantes fondamentales :")
print(f"  G = {G:.5e} m³/(kg·s²)")
print(f"  c = {c:.0f} m/s")
print(f"  t₀ = {t_0/(365.25*24*3600*1e9):.1f} Ga")
print(f"  d_horizon = {d_horizon_kpc:.2f} kpc = {d_horizon_kpc/1000:.2f} Mpc")

# ============================================================================
# PARAMÈTRES DE LA VOIE LACTÉE
# ============================================================================

# Masse du bulbe central
M_bulbe = 1.5e10 * 1.989e30  # kg (1.5×10¹⁰ M☉)

# Paramètres du disque exponentiel
M_disque_total = 6.0e10 * 1.989e30  # kg (6×10¹⁰ M☉)
r_disque = 3.5  # kpc (rayon d'échelle du disque)

# Rayon du bulbe
r_bulbe = 1.0  # kpc

print(f"\nParamètres de la Voie Lactée :")
print(f"  M_bulbe = {M_bulbe/(1.989e30):.2e} M☉")
print(f"  M_disque = {M_disque_total/(1.989e30):.2e} M☉")
print(f"  r_disque = {r_disque} kpc")
print(f"  r_bulbe = {r_bulbe} kpc")

# ============================================================================
# FONCTIONS DE DISTRIBUTION DE MASSE
# ============================================================================

def masse_bulbe(r_kpc):
    """
    Masse du bulbe contenue dans le rayon r (profil sphérique de Plummer)

    Args:
        r_kpc: rayon en kpc

    Returns:
        masse en kg
    """
    if r_kpc < 0.01:
        return 0.0

    # Profil de Plummer simplifié
    M_r = M_bulbe * (r_kpc**3) / ((r_kpc**2 + r_bulbe**2)**(3/2))
    return M_r


def densite_disque(r_kpc):
    """
    Densité surfacique du disque exponentiel

    Args:
        r_kpc: rayon en kpc

    Returns:
        densité surfacique en kg/kpc²
    """
    Sigma_0 = M_disque_total / (2 * math.pi * r_disque**2)
    Sigma_r = Sigma_0 * math.exp(-r_kpc / r_disque)
    return Sigma_r


def masse_disque(r_kpc):
    """
    Masse du disque contenue dans le rayon r (disque exponentiel)

    Args:
        r_kpc: rayon en kpc

    Returns:
        masse en kg
    """
    if r_kpc < 0.01:
        return 0.0

    # Pour un disque exponentiel : M(r) = M_total × [1 - (1 + r/r_d)·exp(-r/r_d)]
    x = r_kpc / r_disque
    M_r = M_disque_total * (1 - (1 + x) * math.exp(-x))
    return M_r


def masse_totale_visible(r_kpc):
    """
    Masse totale visible (bulbe + disque) à l'intérieur du rayon r

    Args:
        r_kpc: rayon en kpc

    Returns:
        masse totale en kg
    """
    return masse_bulbe(r_kpc) + masse_disque(r_kpc)


# ============================================================================
# FACTEUR D'EXPANSION TEMPORELLE
# ============================================================================

def facteur_expansion(d_kpc):
    """
    Facteur d'atténuation de la gravitation par expansion temporelle

    f(d) = exp(-d/d_horizon)

    Args:
        d_kpc: distance en kpc

    Returns:
        facteur sans dimension (0 < f ≤ 1)
    """
    f = math.exp(-d_kpc / d_horizon_kpc)
    return f


# ============================================================================
# LIAISON ASSELIN
# ============================================================================

def liaison_asselin(M1, M2, d_kpc):
    """
    Liaison Asselin entre deux masses séparées par distance d

    L_Asselin(M₁, M₂, d) = √(M₁·M₂) / d² · exp(-d/d_horizon)

    Args:
        M1: masse 1 en kg
        M2: masse 2 en kg
        d_kpc: distance en kpc

    Returns:
        Liaison en kg/kpc²
    """
    if d_kpc < 0.01:
        return 0.0

    f = facteur_expansion(d_kpc)
    L = math.sqrt(M1 * M2) / (d_kpc**2) * f
    return L


# ============================================================================
# VITESSE DE ROTATION - NEWTONIENNE CLASSIQUE
# ============================================================================

def vitesse_newtonienne(r_kpc):
    """
    Vitesse de rotation newtonienne classique (matière visible seulement)

    v(r) = √(G·M(r) / r)

    Args:
        r_kpc: rayon en kpc

    Returns:
        vitesse en km/s
    """
    if r_kpc < 0.01:
        return 0.0

    M_r = masse_totale_visible(r_kpc)
    r_m = r_kpc * 3.086e19  # conversion kpc → m

    v_ms = math.sqrt(G * M_r / r_m)  # m/s
    v_kms = v_ms / 1000  # km/s

    return v_kms


# ============================================================================
# VITESSE DE ROTATION - AVEC LIAISON ASSELIN CUMULATIVE
# ============================================================================

def masse_effective_asselin(r_kpc, N_shells=100):
    """
    Calcul de la masse effective à la position r incluant l'effet cumulatif
    de la Liaison Asselin de toute la matière galactique.

    On intègre la contribution de chaque coquille sphérique de matière,
    pondérée par le facteur d'expansion f(d).

    Args:
        r_kpc: rayon où on calcule v(r) en kpc
        N_shells: nombre de coquilles pour l'intégration

    Returns:
        masse effective en kg
    """
    # Masse locale (newtonienne standard)
    M_local = masse_totale_visible(r_kpc)

    # Contribution cumulative des coquilles externes
    # (matière au-delà de r contribue par Liaison Asselin)

    r_max = 50.0  # kpc - rayon max de la galaxie
    dr = (r_max - r_kpc) / N_shells

    contribution_externe = 0.0

    for i in range(N_shells):
        r_shell = r_kpc + (i + 0.5) * dr

        # Masse dans cette coquille
        dM = masse_totale_visible(r_shell + dr/2) - masse_totale_visible(r_shell - dr/2)

        if dM <= 0:
            continue

        # Distance entre r et r_shell
        d = abs(r_shell - r_kpc)

        if d < 0.01:
            continue

        # Facteur d'atténuation
        f = facteur_expansion(d)

        # Contribution effective (approximation : contribution proportionnelle à √(dM) × f / d)
        # Cette formulation est une approximation pour l'effet gravitationnel cumulatif
        contribution_externe += dM * f * (r_kpc / r_shell)

    M_eff = M_local + contribution_externe

    return M_eff


def vitesse_asselin(r_kpc):
    """
    Vitesse de rotation incluant l'effet cumulatif de la Liaison Asselin

    v(r) = √(G·M_eff(r) / r)  où M_eff inclut contributions Asselin

    Args:
        r_kpc: rayon en kpc

    Returns:
        vitesse en km/s
    """
    if r_kpc < 0.01:
        return 0.0

    M_eff = masse_effective_asselin(r_kpc)
    r_m = r_kpc * 3.086e19  # conversion kpc → m

    v_ms = math.sqrt(G * M_eff / r_m)  # m/s
    v_kms = v_ms / 1000  # km/s

    return v_kms


# ============================================================================
# DONNÉES OBSERVÉES - VOIE LACTÉE
# ============================================================================

# Courbe de rotation observée de la Voie Lactée (approximative)
# Source : mesures combinées (HI, CO, étoiles traçeuses)
r_obs = np.array([0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 25, 30])  # kpc
v_obs = np.array([80, 140, 190, 210, 220, 225, 225, 225, 220, 220, 215, 210, 205, 200, 195, 185, 175])  # km/s

# Incertitudes observationnelles (estimées)
v_err = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 20, 20, 25, 30])  # km/s

print(f"\nDonnées observées : {len(r_obs)} points de 0.5 à 30 kpc")

# ============================================================================
# CALCUL DES COURBES DE ROTATION
# ============================================================================

print("\n" + "=" * 80)
print("CALCUL DES COURBES DE ROTATION")
print("=" * 80)

# Grille de rayons pour calcul
r_array = np.linspace(0.5, 30, 60)  # kpc

# Calcul Newton classique
print("\nCalcul courbe newtonienne (matière visible seule)...")
v_newton = np.array([vitesse_newtonienne(r) for r in r_array])

# Calcul avec Liaison Asselin
print("Calcul courbe avec Liaison Asselin (cela peut prendre 1-2 minutes)...")
v_asselin = np.array([vitesse_asselin(r) for r in r_array])

print("✓ Calculs terminés")

# ============================================================================
# ANALYSE DES RÉSULTATS
# ============================================================================

print("\n" + "=" * 80)
print("ANALYSE DES RÉSULTATS")
print("=" * 80)

# Vitesses aux rayons caractéristiques
rayons_test = [5, 10, 15, 20]

print("\nComparaison aux rayons caractéristiques :")
print(f"{'Rayon (kpc)':<15} {'v_Newton (km/s)':<20} {'v_Asselin (km/s)':<20} {'v_obs (km/s)':<15}")
print("-" * 70)

for r_test in rayons_test:
    idx = np.argmin(np.abs(r_array - r_test))
    v_n = v_newton[idx]
    v_a = v_asselin[idx]

    # Trouver observation la plus proche
    idx_obs = np.argmin(np.abs(r_obs - r_test))
    v_o = v_obs[idx_obs]

    print(f"{r_test:<15.1f} {v_n:<20.1f} {v_a:<20.1f} {v_o:<15.1f}")

# Facteur d'amélioration
print("\nAmélioration par Liaison Asselin (rapport v_Asselin/v_Newton) :")
for r_test in rayons_test:
    idx = np.argmin(np.abs(r_array - r_test))
    ratio = v_asselin[idx] / v_newton[idx] if v_newton[idx] > 0 else 0
    print(f"  r = {r_test} kpc : facteur = {ratio:.3f}")

# ============================================================================
# VISUALISATION
# ============================================================================

print("\n" + "=" * 80)
print("GÉNÉRATION DES GRAPHIQUES")
print("=" * 80)

plt.figure(figsize=(14, 10))

# ---- Graphique 1 : Courbes de rotation ----
plt.subplot(2, 2, 1)

plt.errorbar(r_obs, v_obs, yerr=v_err, fmt='o', color='black',
             label='Observations', markersize=6, capsize=4, capthick=1.5)

plt.plot(r_array, v_newton, '--', color='blue', linewidth=2,
         label='Newton (matière visible)')

plt.plot(r_array, v_asselin, '-', color='red', linewidth=2.5,
         label='Liaison Asselin (matière visible + effet cumulatif)')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Vitesse de rotation (km/s)', fontsize=12)
plt.title('Courbe de Rotation de la Voie Lactée', fontsize=14, fontweight='bold')
plt.legend(fontsize=10, loc='lower right')
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(0, 250)

# ---- Graphique 2 : Distribution de masse ----
plt.subplot(2, 2, 2)

M_bulbe_array = np.array([masse_bulbe(r)/(1.989e30) for r in r_array])
M_disque_array = np.array([masse_disque(r)/(1.989e30) for r in r_array])
M_total_array = M_bulbe_array + M_disque_array

plt.plot(r_array, M_bulbe_array, '-', color='orange', linewidth=2, label='Bulbe')
plt.plot(r_array, M_disque_array, '-', color='green', linewidth=2, label='Disque')
plt.plot(r_array, M_total_array, '-', color='black', linewidth=2.5, label='Total visible')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Masse cumulée (M☉)', fontsize=12)
plt.title('Distribution de Masse Visible', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.xlim(0, 32)

# ---- Graphique 3 : Facteur d'expansion f(d) ----
plt.subplot(2, 2, 3)

d_array = np.linspace(0, 100, 200)  # kpc
f_array = np.array([facteur_expansion(d) for d in d_array])

plt.plot(d_array, f_array, '-', color='purple', linewidth=2.5)
plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=0.9, color='gray', linestyle=':', alpha=0.5)

plt.xlabel('Distance (kpc)', fontsize=12)
plt.ylabel('Facteur d\'expansion f(d)', fontsize=12)
plt.title('Atténuation Gravitationnelle par Expansion Temporelle', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim(0, 100)
plt.ylim(0.85, 1.01)

# Annotations
plt.text(20, 0.99, 'f ≈ 1 : gravitation classique', fontsize=9)
plt.text(20, 0.96, 'f < 1 : atténuation par expansion', fontsize=9)

# ---- Graphique 4 : Résidus ----
plt.subplot(2, 2, 4)

# Interpoler v_asselin et v_newton sur r_obs
v_asselin_interp = np.interp(r_obs, r_array, v_asselin)
v_newton_interp = np.interp(r_obs, r_array, v_newton)

residus_newton = (v_newton_interp - v_obs) / v_obs * 100
residus_asselin = (v_asselin_interp - v_obs) / v_obs * 100

plt.plot(r_obs, residus_newton, 'o-', color='blue', linewidth=2,
         markersize=6, label='Newton')
plt.plot(r_obs, residus_asselin, 's-', color='red', linewidth=2,
         markersize=6, label='Asselin')

plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
plt.fill_between([0, 35], -10, 10, color='green', alpha=0.1, label='±10% (acceptable)')

plt.xlabel('Rayon (kpc)', fontsize=12)
plt.ylabel('Résidu (% de v_obs)', fontsize=12)
plt.title('Résidus par Rapport aux Observations', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.xlim(0, 32)
plt.ylim(-60, 20)

# ---- Finalisation ----
plt.tight_layout()
plt.savefig('courbe_rotation_voie_lactee.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé : courbe_rotation_voie_lactee.png")

# ============================================================================
# STATISTIQUES FINALES
# ============================================================================

print("\n" + "=" * 80)
print("STATISTIQUES FINALES")
print("=" * 80)

# Chi-carré
chi2_newton = np.sum(((v_newton_interp - v_obs) / v_err)**2)
chi2_asselin = np.sum(((v_asselin_interp - v_obs) / v_err)**2)

print(f"\nChi² (plus petit = meilleur ajustement) :")
print(f"  Newton  : χ² = {chi2_newton:.2f}")
print(f"  Asselin : χ² = {chi2_asselin:.2f}")
print(f"  Amélioration : {((chi2_newton - chi2_asselin)/chi2_newton * 100):.1f}%")

# RMS
rms_newton = np.sqrt(np.mean((v_newton_interp - v_obs)**2))
rms_asselin = np.sqrt(np.mean((v_asselin_interp - v_obs)**2))

print(f"\nRMS (plus petit = meilleur) :")
print(f"  Newton  : RMS = {rms_newton:.2f} km/s")
print(f"  Asselin : RMS = {rms_asselin:.2f} km/s")
print(f"  Amélioration : {((rms_newton - rms_asselin)/rms_newton * 100):.1f}%")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

if chi2_asselin < chi2_newton * 0.5:
    print("\n✓ SUCCÈS : La Liaison Asselin améliore significativement l'ajustement !")
    print("  → La théorie peut potentiellement expliquer les courbes de rotation")
    print("    SANS matière noire exotique.")
elif chi2_asselin < chi2_newton:
    print("\n⚠ PARTIEL : La Liaison Asselin améliore l'ajustement, mais modérément.")
    print("  → Des ajustements des paramètres (M_disque, r_disque, etc.) sont nécessaires.")
else:
    print("\n✗ PROBLÈME : La Liaison Asselin n'améliore pas l'ajustement.")
    print("  → Révision de la formulation ou des paramètres nécessaire.")

print("\n" + "=" * 80)
print("FIN DU CALCUL")
print("=" * 80)
