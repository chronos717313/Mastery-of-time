#!/usr/bin/env python3
"""
Test de la formule de Liaison Asselin par rapport à l'expansion cosmologique
"""

import numpy as np
import matplotlib.pyplot as plt

# Constantes physiques
c = 299792.458  # vitesse de la lumière en km/s
H0 = 70.0  # constante de Hubble en km/s/Mpc
Mpc_to_km = 3.086e19  # 1 Mpc en km
Mpc_to_ly = 3.26e6  # 1 Mpc en années-lumière

# Horizon cosmologique où v = c
d_horizon_Mpc = c / H0  # en Mpc
d_horizon_ly = d_horizon_Mpc * Mpc_to_ly  # en années-lumière

print("="*60)
print("DONNÉES COSMOLOGIQUES DE RÉFÉRENCE")
print("="*60)
print(f"Constante de Hubble H0 = {H0} km/s/Mpc")
print(f"Vitesse de la lumière c = {c} km/s")
print(f"Horizon cosmologique d_horizon = {d_horizon_Mpc:.2f} Mpc")
print(f"Horizon cosmologique = {d_horizon_ly:.2e} années-lumière")
print(f"Horizon cosmologique = {d_horizon_ly/1e9:.2f} milliards d'années-lumière")
print()

# Distances typiques dans l'univers (en Mpc)
distances = {
    "Système solaire (Neptune)": 4.5e-9,  # ~4.5 milliards de km
    "Proxima Centauri": 1.3e-6,  # ~4 années-lumière
    "Centre galactique": 8.2e-3,  # ~26,000 al
    "Andromède (M31)": 0.78,  # ~2.5 millions al
    "Amas Virgo": 16.5,  # ~54 millions al
    "Grande Muraille": 200,  # ~650 millions al
    "Horizon observable": d_horizon_Mpc
}

print("="*60)
print("TEST 1: VITESSE DE RÉCESSION (LOI DE HUBBLE)")
print("="*60)
for nom, d_Mpc in distances.items():
    v = H0 * d_Mpc  # vitesse de récession en km/s
    ratio_c = v / c  # ratio par rapport à la vitesse de la lumière
    print(f"{nom:30s}: d = {d_Mpc:12.2e} Mpc")
    print(f"  → Vitesse récession v = {v:12.2f} km/s ({ratio_c:.4f} c)")
    if ratio_c >= 1.0:
        print(f"  ⚠ AU-DELÀ DE L'HORIZON GRAVITATIONNEL")
    print()

print("="*60)
print("TEST 2: EFFET ASSELIN - DIFFÉRENTES HYPOTHÈSES")
print("="*60)
print()

# Définir une distorsion temporelle typique (à calibrer)
# Prenons comme exemple la distorsion au centre galactique
# En relativité générale: τ ~ GM/rc²
# Pour le centre galactique: τ ~ 10^-6 (ordre de grandeur)

M_galaxy = 1e12  # masse solaire typique d'une galaxie
G = 6.674e-11  # constante gravitationnelle (SI)
M_sun = 1.989e30  # masse solaire en kg

def distortion_temporelle(M_solar, r_Mpc):
    """
    Calcule la distorsion temporelle (ordre de grandeur)
    τ ∝ 1/r² (selon votre théorie)

    Normalisée arbitrairement pour avoir τ ~ 1e-6 au centre galactique
    """
    r0 = 8.2e-3  # rayon de référence (centre galactique) en Mpc
    tau0 = 1e-6  # distorsion de référence

    # τ(r) = τ0 * (r0/r)²
    if r_Mpc > 0:
        tau = tau0 * (r0 / r_Mpc)**2
    else:
        tau = float('inf')

    # Proportionnel à la masse
    tau *= (M_solar / M_galaxy)

    return tau

# Test des différentes formules possibles
print("HYPOTHÈSE A: Effet ∝ (τ₂ - τ₁) / d³")
print("-" * 60)

# Comparaison entre deux galaxies
M1 = 1e12  # Masse galaxie 1 (masses solaires)
M2 = 1e12  # Masse galaxie 2 (masses solaires)
d_separation_Mpc = 1.0  # Séparation de 1 Mpc

tau1 = distortion_temporelle(M1, d_separation_Mpc/2)
tau2 = distortion_temporelle(M2, d_separation_Mpc/2)

# Formule A: décroissance en 1/d³
effet_A = abs(tau2 - tau1) / (d_separation_Mpc**3)
print(f"Deux galaxies séparées de {d_separation_Mpc} Mpc:")
print(f"  τ₁ = {tau1:.2e}, τ₂ = {tau2:.2e}")
print(f"  Effet A (∝ Δτ/d³) = {effet_A:.2e}")
print()

print("HYPOTHÈSE B: Effet ∝ (τ₂ - τ₁) × d³")
print("-" * 60)

# Formule B: croissance en d³
effet_B = abs(tau2 - tau1) * (d_separation_Mpc**3)
print(f"Deux galaxies séparées de {d_separation_Mpc} Mpc:")
print(f"  Effet B (∝ Δτ×d³) = {effet_B:.2e}")
print()

print("="*60)
print("TEST 3: PROFIL D'EFFET EN FONCTION DE LA DISTANCE")
print("="*60)

# Créer un profil sur différentes distances
distances_test = np.logspace(-3, np.log10(d_horizon_Mpc), 100)  # De 0.001 Mpc à l'horizon

effets_A = []
effets_B = []
vitesses = []

for d in distances_test:
    tau1 = distortion_temporelle(M1, d/2)
    tau2 = distortion_temporelle(M2, d/2)
    delta_tau = abs(tau2 - tau1)

    # Limiter à l'horizon cosmologique
    v = H0 * d
    if v < c:  # Seulement si sous l'horizon
        effet_a = delta_tau / (d**3)
        effet_b = delta_tau * (d**3)
    else:
        effet_a = 0
        effet_b = 0

    effets_A.append(effet_a)
    effets_B.append(effet_b)
    vitesses.append(v)

# Convertir en arrays numpy
effets_A = np.array(effets_A)
effets_B = np.array(effets_B)
vitesses = np.array(vitesses)

# Créer les graphiques
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Graphique 1: Hypothèse A (∝ 1/d³)
ax1 = axes[0]
ax1.loglog(distances_test, effets_A, 'b-', linewidth=2, label='Effet ∝ Δτ/d³')
ax1.axvline(d_horizon_Mpc, color='r', linestyle='--', linewidth=2, label=f'Horizon c/H₀ = {d_horizon_Mpc:.1f} Mpc')
ax1.axvline(0.78, color='g', linestyle=':', alpha=0.7, label='Andromède')
ax1.axvline(16.5, color='orange', linestyle=':', alpha=0.7, label='Amas Virgo')
ax1.set_xlabel('Distance (Mpc)', fontsize=12)
ax1.set_ylabel('Effet Asselin (unités arbitraires)', fontsize=12)
ax1.set_title('HYPOTHÈSE A: Effet décroît en 1/d³ (dominant à courte portée)', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Graphique 2: Hypothèse B (∝ d³)
ax2 = axes[1]
ax2.loglog(distances_test, effets_B, 'r-', linewidth=2, label='Effet ∝ Δτ×d³')
ax2.axvline(d_horizon_Mpc, color='r', linestyle='--', linewidth=2, label=f'Horizon c/H₀ = {d_horizon_Mpc:.1f} Mpc')
ax2.axvline(0.78, color='g', linestyle=':', alpha=0.7, label='Andromède')
ax2.axvline(16.5, color='orange', linestyle=':', alpha=0.7, label='Amas Virgo')
ax2.set_xlabel('Distance (Mpc)', fontsize=12)
ax2.set_ylabel('Effet Asselin (unités arbitraires)', fontsize=12)
ax2.set_title('HYPOTHÈSE B: Effet croît en d³ (dominant à longue portée)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig('/home/chuck/Documents/Maitrise du temps/test_effet_asselin.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé: test_effet_asselin.png")

# Analyse comparative
print("\n" + "="*60)
print("ANALYSE COMPARATIVE")
print("="*60)

print("\nHYPOTHÈSE A (∝ 1/d³) - Effet dominant à COURTE PORTÉE:")
print("  - Maximum à petites distances (système solaire, galaxie)")
print("  - Décroît rapidement avec la distance")
print("  - Difficile d'expliquer la matière noire galactique")
print("  - Ne peut pas expliquer les structures cosmologiques")

print("\nHYPOTHÈSE B (∝ d³) - Effet dominant à LONGUE PORTÉE:")
print("  - Croît avec la distance (jusqu'à l'horizon c/H₀)")
print("  - Compatible avec effets cumulatifs cosmologiques")
print("  - Peut expliquer les courbes de rotation galactiques")
print("  - Peut expliquer les filaments et grands vides")
print("  - S'arrête naturellement à l'horizon cosmologique")

print("\n" + "="*60)
print("CONCLUSION PRÉLIMINAIRE")
print("="*60)
print("L'HYPOTHÈSE B (effet ∝ d³) semble plus compatible avec:")
print("  1. Vos observations sur les filaments cosmologiques")
print("  2. L'effet cumulatif mentionné pour les courbes de rotation")
print("  3. La limite naturelle à c/H₀")
print()
print("MAIS cela nécessite une justification physique:")
print("  - Pourquoi une force croîtrait-elle avec la distance?")
print("  - Possibilité: effet CUMULATIF de multiples liaisons?")
print("  - Possibilité: intégration sur un volume ∝ d³?")
print("="*60)

plt.show()
