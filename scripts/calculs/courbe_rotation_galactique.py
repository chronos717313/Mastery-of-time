#!/usr/bin/env python3
"""
Courbe de Rotation Galactique avec Effet Asselin
Inclut l'influence des galaxies externes

Théorie de Maîtrise du Temps - Liaison Asselin
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# CONSTANTES PHYSIQUES
# ============================================================================
G = 6.674e-11  # m³/kg/s² - Constante gravitationnelle
c = 2.998e8    # m/s - Vitesse de la lumière
M_sun = 1.989e30  # kg - Masse solaire
pc_to_m = 3.086e16  # m - 1 parsec en mètres
kpc_to_m = 1000 * pc_to_m  # m - 1 kiloparsec en mètres
Mpc_to_m = 1e6 * pc_to_m  # m - 1 mégaparsec en mètres

# ============================================================================
# PARAMÈTRES DE LA GALAXIE MODÈLE
# ============================================================================
# Basé sur NGC 3198 (galaxie spirale bien étudiée)
M_bulge = 1.0e10 * M_sun  # Masse du bulbe central
R_bulge = 1.5 * kpc_to_m  # Rayon du bulbe

M_disk = 5.0e10 * M_sun   # Masse du disque visible
R_disk = 10.0 * kpc_to_m  # Rayon caractéristique du disque

# Profil de densité du disque (exponentiel)
def rho_disk(r):
    """Densité surfacique du disque en fonction du rayon"""
    Sigma_0 = M_disk / (2 * np.pi * R_disk**2)  # Densité centrale
    return Sigma_0 * np.exp(-r / R_disk)

# Masse totale visible jusqu'au rayon r
def M_visible(r):
    """Masse visible (bulbe + disque) jusqu'au rayon r"""
    # Bulbe (approximation: sphère uniforme)
    if r < R_bulge:
        M_bulge_enclosed = M_bulge * (r / R_bulge)**3
    else:
        M_bulge_enclosed = M_bulge

    # Disque (intégration du profil exponentiel)
    M_disk_enclosed = M_disk * (1 - np.exp(-r / R_disk) * (1 + r / R_disk))

    return M_bulge_enclosed + M_disk_enclosed

# ============================================================================
# DISTORSION TEMPORELLE (LIAISON ASSELIN)
# ============================================================================
def distortion_temporelle(M, r):
    """
    Calcule la distorsion temporelle τ créée par une masse M à distance r

    Formule: τ ∝ 1/r²
    Normalisée pour τ ~ GM/rc² (ordre de grandeur relativiste)
    """
    if r == 0:
        return float('inf')

    # Approximation: τ ~ GM/rc² (facteur de Schwarzschild divisé par r)
    tau = (G * M) / (r * c**2)

    return tau

# ============================================================================
# VITESSE NEWTONIENNE
# ============================================================================
def v_newton(r):
    """Vitesse orbitale newtonienne au rayon r"""
    M_enc = M_visible(r)
    if r == 0:
        return 0
    return np.sqrt(G * M_enc / r)

# ============================================================================
# EFFET ASSELIN INTERNE (LIAISONS DANS LA GALAXIE)
# ============================================================================
def effet_asselin_interne(r_test, n_samples=200):
    """
    Calcule l'effet Asselin cumulatif des étoiles intérieures au rayon r_test

    Effet ∝ ∑ Δτᵢ (somme sur toutes les liaisons)

    Paramètres:
    - r_test: rayon de test (position de l'étoile observée)
    - n_samples: nombre d'échantillons pour l'intégration numérique
    """
    if r_test == 0:
        return 0

    # Distorsion temporelle au point de test
    M_test = M_visible(r_test)
    tau_test = distortion_temporelle(M_test, r_test)

    # Intégration numérique: somme des liaisons avec les éléments intérieurs
    effet_total = 0
    radii = np.linspace(0.1 * kpc_to_m, r_test, n_samples)

    for r_i in radii:
        # Masse de l'anneau à rayon r_i
        dr = r_test / n_samples
        dM = 2 * np.pi * r_i * rho_disk(r_i) * dr  # Masse d'un anneau

        # Distorsion créée par cet anneau
        tau_i = distortion_temporelle(dM, abs(r_test - r_i) + 0.1*kpc_to_m)

        # Contribution de cette liaison
        delta_tau = abs(tau_test - tau_i)
        effet_total += delta_tau

    return effet_total

# ============================================================================
# EFFET ASSELIN EXTERNE (GALAXIES VOISINES)
# ============================================================================
class GalaxieExterne:
    """Représente une galaxie externe influençant notre galaxie"""
    def __init__(self, masse, distance, nom):
        self.masse = masse * M_sun  # en kg
        self.distance = distance * Mpc_to_m  # en m
        self.nom = nom

    def effet_sur_galaxie(self, r_test):
        """
        Calcule l'effet de cette galaxie externe sur un point à r_test
        dans notre galaxie
        """
        # Distorsion créée par la galaxie externe
        tau_externe = distortion_temporelle(self.masse, self.distance)

        # Distorsion au point de test dans notre galaxie
        M_test = M_visible(r_test)
        tau_test = distortion_temporelle(M_test, r_test)

        # Liaison entre les deux
        delta_tau = abs(tau_externe - tau_test)

        return delta_tau

# Définir les galaxies externes influentes
galaxies_externes = [
    GalaxieExterne(masse=1.0e12, distance=0.78, nom="Andromède (M31)"),
    GalaxieExterne(masse=5.0e10, distance=0.85, nom="M33"),
    GalaxieExterne(masse=3.0e11, distance=3.0, nom="Groupe local (moyenne)"),
]

def effet_asselin_externe(r_test):
    """Somme des effets de toutes les galaxies externes"""
    effet_total = 0
    for galaxie in galaxies_externes:
        effet_total += galaxie.effet_sur_galaxie(r_test)

    return effet_total

# ============================================================================
# VITESSE AVEC EFFET ASSELIN
# ============================================================================
def v_asselin_total(r, k_interne=1e-3, k_externe=1e-5):
    """
    Calcule la vitesse orbitale totale incluant l'effet Asselin

    v² = v_newton² + k_interne * Effet_interne + k_externe * Effet_externe

    Paramètres:
    - k_interne: constante de couplage pour effet interne
    - k_externe: constante de couplage pour effet externe
    """
    # Vitesse newtonienne
    v_n = v_newton(r)

    # Effets Asselin
    effet_int = effet_asselin_interne(r, n_samples=100)
    effet_ext = effet_asselin_externe(r)

    # Contribution à v² (en m²/s²)
    v_squared = v_n**2 + k_interne * effet_int * c**2 + k_externe * effet_ext * c**2

    if v_squared < 0:
        v_squared = 0

    return np.sqrt(v_squared)

# ============================================================================
# DONNÉES OBSERVATIONNELLES (NGC 3198)
# ============================================================================
# Données approximatives de Vera Rubin et al.
r_obs_kpc = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30])
v_obs_kms = np.array([80, 130, 150, 155, 150, 150, 148, 150, 148, 150, 148, 150, 148, 150, 150])

# ============================================================================
# CALCUL DES COURBES
# ============================================================================
print("="*70)
print("CALCUL DE LA COURBE DE ROTATION GALACTIQUE")
print("Modèle: Galaxie spirale type NGC 3198")
print("="*70)
print()

# Rayons de test (de 0 à 35 kpc)
rayons_kpc = np.linspace(0.5, 35, 50)
rayons_m = rayons_kpc * kpc_to_m

# Calcul des vitesses
print("Calcul en cours...")
v_newt = np.array([v_newton(r) / 1000 for r in rayons_m])  # en km/s

print("  - Vitesses newtoniennes: OK")

# Avec effet Asselin (ajuster k_interne et k_externe pour fit)
k_interne = 5e-4  # À ajuster
k_externe = 1e-6  # À ajuster

v_avec_asselin = []
for i, r in enumerate(rayons_m):
    v = v_asselin_total(r, k_interne=k_interne, k_externe=k_externe)
    v_avec_asselin.append(v / 1000)  # en km/s
    if i % 10 == 0:
        print(f"  - Rayon {rayons_kpc[i]:.1f} kpc: v = {v/1000:.1f} km/s")

v_avec_asselin = np.array(v_avec_asselin)

print()
print("Calcul terminé!")
print()

# ============================================================================
# AFFICHAGE DES RÉSULTATS
# ============================================================================
print("="*70)
print("ANALYSE DES CONTRIBUTIONS")
print("="*70)
print()

# Point de test à 20 kpc
r_test = 20 * kpc_to_m
print(f"Point de test: r = 20 kpc")
print()

v_n = v_newton(r_test) / 1000
effet_int = effet_asselin_interne(r_test, n_samples=100)
effet_ext = effet_asselin_externe(r_test)

print(f"1. Vitesse newtonienne:        v_N = {v_n:.1f} km/s")
print(f"2. Effet Asselin interne:      Δτ_int = {effet_int:.2e}")
print(f"3. Effet Asselin externe:      Δτ_ext = {effet_ext:.2e}")
print(f"4. Ratio interne/externe:      {effet_int/effet_ext:.1f}")
print()

v_total = v_asselin_total(r_test, k_interne=k_interne, k_externe=k_externe) / 1000
print(f"5. Vitesse totale prédite:     v_tot = {v_total:.1f} km/s")
print(f"6. Vitesse observée (~):       v_obs ≈ 150 km/s")
print()

print("Galaxies externes contributrices:")
for galaxie in galaxies_externes:
    effet = galaxie.effet_sur_galaxie(r_test)
    print(f"  - {galaxie.nom}: Δτ = {effet:.2e}")
print()

# ============================================================================
# GRAPHIQUE
# ============================================================================
print("Génération du graphique...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Graphique 1: Courbe de rotation
ax1.plot(rayons_kpc, v_newt, 'b--', linewidth=2, label='Newton seul (matière visible)')
ax1.plot(rayons_kpc, v_avec_asselin, 'r-', linewidth=2, label='Newton + Effet Asselin (interne + externe)')
ax1.scatter(r_obs_kpc, v_obs_kms, color='black', s=50, marker='o', label='Données observées (NGC 3198)', zorder=5)

ax1.set_xlabel('Rayon (kpc)', fontsize=12)
ax1.set_ylabel('Vitesse orbitale (km/s)', fontsize=12)
ax1.set_title('Courbe de Rotation Galactique - Théorie de la Liaison Asselin', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_xlim(0, 35)
ax1.set_ylim(0, 200)

# Graphique 2: Contributions des effets
effet_interne_vals = []
effet_externe_vals = []
for r in rayons_m:
    effet_interne_vals.append(effet_asselin_interne(r, n_samples=50))
    effet_externe_vals.append(effet_asselin_externe(r))

effet_interne_vals = np.array(effet_interne_vals)
effet_externe_vals = np.array(effet_externe_vals)

ax2.semilogy(rayons_kpc, effet_interne_vals, 'g-', linewidth=2, label='Effet Asselin interne (∑Δτ étoiles)')
ax2.semilogy(rayons_kpc, effet_externe_vals, 'm-', linewidth=2, label='Effet Asselin externe (galaxies voisines)')
ax2.semilogy(rayons_kpc, effet_interne_vals + effet_externe_vals, 'k--', linewidth=2, label='Effet total')

ax2.set_xlabel('Rayon (kpc)', fontsize=12)
ax2.set_ylabel('Effet Asselin (Δτ)', fontsize=12)
ax2.set_title('Contributions des Liaisons Asselin', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, which='both')
ax2.legend(fontsize=10)
ax2.set_xlim(0, 35)

plt.tight_layout()
plt.savefig('/home/user/Maitrise-du-temps/courbe_rotation_asselin.png', dpi=300, bbox_inches='tight')
print(f"✓ Graphique sauvegardé: courbe_rotation_asselin.png")
print()

# ============================================================================
# QUALITÉ DU FIT
# ============================================================================
print("="*70)
print("ÉVALUATION DU MODÈLE")
print("="*70)
print()

# Interpoler les prédictions aux points observés
v_pred_aux_obs = np.interp(r_obs_kpc, rayons_kpc, v_avec_asselin)

# Chi² réduit
residus = v_obs_kms - v_pred_aux_obs
chi2 = np.sum(residus**2 / v_obs_kms)
chi2_reduit = chi2 / len(v_obs_kms)

print(f"Paramètres du modèle:")
print(f"  - k_interne (couplage interne): {k_interne:.2e}")
print(f"  - k_externe (couplage externe): {k_externe:.2e}")
print()
print(f"Qualité du fit:")
print(f"  - Chi² réduit: {chi2_reduit:.2f}")
print(f"  - Résidu moyen: {np.mean(np.abs(residus)):.1f} km/s")
print(f"  - Résidu max: {np.max(np.abs(residus)):.1f} km/s")
print()

if chi2_reduit < 2:
    print("✓ Bon accord avec les observations!")
elif chi2_reduit < 5:
    print("⚠ Accord modéré - ajuster k_interne et k_externe")
else:
    print("✗ Accord faible - revoir le modèle")

print()
print("="*70)
print("CONCLUSION")
print("="*70)
print()
print("Le modèle de Liaison Asselin peut reproduire qualitativement les")
print("courbes de rotation plates observées en combinant:")
print("  1. L'effet cumulatif des liaisons internes (étoiles de la galaxie)")
print("  2. L'influence des galaxies externes du groupe local")
print()
print("Les constantes k_interne et k_externe peuvent être ajustées pour")
print("améliorer le fit aux données observationnelles.")
print()
print("Prochaines étapes:")
print("  - Optimiser k_interne et k_externe par régression")
print("  - Tester sur d'autres galaxies (M33, M31, etc.)")
print("  - Comparer avec modèle MOND et matière noire CDM")
print("="*70)

plt.show()
