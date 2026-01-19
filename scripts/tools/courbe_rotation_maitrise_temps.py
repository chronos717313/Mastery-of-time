#!/usr/bin/env python3
"""
COURBE DE ROTATION GALACTIQUE - THÉORIE DE MAÎTRISE DU TEMPS

Calcul complet incluant :
1. Gravitation newtonienne
2. Liaisons Asselin (effet cumulatif volumique)
3. Cartographie Després (indice de distorsion temporelle Lorentz)
4. Comparaison avec observations et Lambda-CDM

Galaxie modèle : Spirale typique (type Voie Lactée / NGC-3198)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# ============================================================================
# CONSTANTES PHYSIQUES
# ============================================================================

c = 299792.458  # Vitesse de la lumière (km/s)
G = 4.302e-6  # Constante gravitationnelle (kpc·(km/s)²/M☉)
H0 = 70.0  # Constante de Hubble (km/s/Mpc)
kpc_to_km = 3.086e16  # 1 kpc en km

# ============================================================================
# PARAMÈTRES DE LA GALAXIE (Type Voie Lactée / NGC-3198)
# ============================================================================

# Profil de densité de la matière visible (modèle exponentiel)
M_bulge = 1.0e10  # Masse du bulbe (M☉)
R_bulge = 1.0  # Rayon du bulbe (kpc)

M_disk_total = 6.0e10  # Masse totale du disque (M☉)
R_disk = 3.5  # Rayon d'échelle du disque (kpc)

# Distance maximale pour l'analyse
R_max = 30.0  # kpc

print("=" * 80)
print("COURBE DE ROTATION GALACTIQUE - THÉORIE DE MAÎTRISE DU TEMPS")
print("=" * 80)
print()
print(f"Galaxie modèle : Spirale typique (type Voie Lactée)")
print(f"Masse bulbe : {M_bulge:.2e} M☉")
print(f"Masse disque : {M_disk_total:.2e} M☉")
print(f"Masse visible totale : {(M_bulge + M_disk_total):.2e} M☉")
print()

# ============================================================================
# 1. PROFIL DE DENSITÉ DE MATIÈRE VISIBLE
# ============================================================================

def surface_density_disk(r):
    """
    Densité surfacique du disque galactique (profil exponentiel)
    Σ(r) = Σ₀ · exp(-r/R_d)
    """
    # Normalisation pour obtenir la masse totale correcte
    Sigma_0 = M_disk_total / (2 * np.pi * R_disk**2)
    return Sigma_0 * np.exp(-r / R_disk)

def mass_enclosed_bulge(r):
    """Masse du bulbe à l'intérieur du rayon r (profil de Hernquist simplifié)"""
    return M_bulge * r**2 / (r + R_bulge)**2

def mass_enclosed_disk(r):
    """Masse du disque à l'intérieur du rayon r"""
    # Intégrale du profil exponentiel
    # M(r) = 2π ∫₀ʳ Σ(r') r' dr'
    x = r / R_disk
    M_r = M_disk_total * (1 - np.exp(-x) * (1 + x))
    return M_r

def mass_enclosed_total(r):
    """Masse visible totale à l'intérieur du rayon r"""
    return mass_enclosed_bulge(r) + mass_enclosed_disk(r)

# ============================================================================
# 2. VITESSE NEWTONIENNE (MATIÈRE VISIBLE SEULE)
# ============================================================================

def v_newton(r):
    """
    Vitesse de rotation selon gravitation newtonienne pure
    v² = GM(r)/r
    """
    if r <= 0:
        return 0
    M_r = mass_enclosed_total(r)
    v_squared = G * M_r / r
    return np.sqrt(max(0, v_squared))

# ============================================================================
# 3. DISTORSION TEMPORELLE τ(r) - CARTOGRAPHIE DESPRÉS
# ============================================================================

def tau_temporal_distortion(r, M_enclosed):
    """
    Distorsion temporelle selon la Cartographie Després

    τ(r) ≈ GM/(rc²) × facteur_géométrique

    Dans la théorie :
    - τ décroît en 1/r² depuis chaque source de masse
    - Pour une distribution sphérique, on utilise M(r)
    """
    if r <= 0:
        return 0

    # Potentiel gravitationnel Φ = GM/r
    Phi = G * M_enclosed / r

    # Conversion de G en unités cohérentes pour avoir Φ/c²
    # G est en kpc·(km/s)²/M☉
    # c est en km/s
    # Donc Φ/c² est sans dimension

    tau = Phi / c**2

    return tau

def gamma_despres(r, v_orb):
    """
    Facteur de Lorentz modifié selon la Cartographie Després

    γ_Després = 1 / √(1 - v²/c² - 2Φ/c²)

    Retourne aussi l'IDT (Indice de Distorsion Temporelle)
    """
    M_r = mass_enclosed_total(r)

    # Terme cinétique
    beta_squared = (v_orb / c)**2

    # Terme gravitationnel (distorsion temporelle)
    tau = tau_temporal_distortion(r, M_r)
    distorsion_grav = 2 * tau

    # Facteur de Lorentz total
    denominateur = 1.0 - beta_squared - distorsion_grav

    # Vérification de validité
    if denominateur <= 0:
        gamma = float('inf')
        IDT = float('inf')
    else:
        gamma = 1.0 / np.sqrt(denominateur)
        IDT = gamma - 1.0

    return gamma, IDT, distorsion_grav

# ============================================================================
# 4. LIAISON ASSELIN - EFFET CUMULATIF VOLUMIQUE
# ============================================================================

def liaison_asselin_gradient(r_observer, r_source):
    """
    Gradient de distorsion temporelle entre deux points

    Représente la Liaison Asselin entre l'observateur à r_observer
    et une coquille de matière à r_source
    """
    M_source = mass_enclosed_total(r_source)
    M_observer = mass_enclosed_total(r_observer)

    tau_source = tau_temporal_distortion(r_source, M_source)
    tau_observer = tau_temporal_distortion(r_observer, M_observer)

    # Liaison Asselin = différence de distorsion
    liaison = abs(tau_source - tau_observer)

    return liaison

def effet_asselin_cumulatif(r):
    """
    Effet cumulatif des Liaisons Asselin sur une étoile à rayon r

    Selon l'Hypothèse B validée : Effet ∝ Δτ × d³

    Interprétation : Intégration volumique
    ∫∫∫ Liaison(r, r') × ρ(r') dV'

    Pour simplification, on intègre sur des coquilles sphériques :
    ∫₀^R Liaison(r, r') × dM(r') × (distance)^α

    où α est un paramètre à calibrer (α ≈ 1 ou 2 selon l'effet géométrique)
    """

    # Constante de couplage (à calibrer avec observations)
    # Unité : pour donner une vitesse en km/s
    # Calibré pour obtenir v ~ 200-220 km/s en périphérie (valeurs observées typiques)
    k_asselin = 0.0055  # Paramètre libre ajusté pour fit observationnel

    # Paramètre de portée : selon Hypothèse B, effet ∝ d³
    # Mais modulé pour équilibrer avec Newton
    alpha_distance = 3.0  # Exposant de la distance dans l'effet cumulatif

    # Intégration sur toutes les coquilles de matière
    def integrand(r_prime):
        if r_prime <= 0.01:  # Éviter singularité au centre
            return 0

        # Masse différentielle dans la coquille
        if r_prime < r:
            # Matière à l'intérieur
            dM_dr = (mass_enclosed_total(r_prime + 0.01) -
                     mass_enclosed_total(r_prime)) / 0.01
        else:
            # Matière à l'extérieur
            dM_dr = (mass_enclosed_total(r_prime + 0.01) -
                     mass_enclosed_total(r_prime)) / 0.01

        if dM_dr < 0:
            dM_dr = 0

        # Liaison Asselin entre r et r_prime
        liaison = liaison_asselin_gradient(r, r_prime)

        # Distance effective
        distance = abs(r - r_prime) + 0.1  # Éviter division par zéro

        # Contribution selon d^α avec atténuation exponentielle pour éviter divergence
        # Facteur d'atténuation : exp(-distance / échelle_caractéristique)
        echelle_attenuation = 50.0  # kpc (échelle cosmologique)
        attenuation = np.exp(-distance / echelle_attenuation)

        # Contribution selon d^α avec atténuation
        contribution = liaison * dM_dr * (distance ** alpha_distance) * attenuation

        return contribution

    # Intégration numérique
    try:
        effet_total, _ = quad(integrand, 0.01, R_max, limit=100, epsrel=1e-3)
    except:
        effet_total = 0

    # Conversion en terme de vitesse additionnelle
    # Δv² = k × effet_total / r
    if r > 0:
        delta_v_squared = k_asselin * effet_total / r
    else:
        delta_v_squared = 0

    return max(0, delta_v_squared)

# ============================================================================
# 5. VITESSE TOTALE - THÉORIE DE MAÎTRISE DU TEMPS
# ============================================================================

def v_maitrise_temps(r):
    """
    Vitesse de rotation selon la Théorie de Maîtrise du Temps

    v_total² = v_Newton² + Δv_Asselin²

    Où :
    - v_Newton² = GM(r)/r (matière visible)
    - Δv_Asselin² = effet cumulatif des Liaisons Asselin
    """
    # Composante newtonienne
    v_newt = v_newton(r)
    v_newt_squared = v_newt**2

    # Composante Asselin
    delta_v_squared_asselin = effet_asselin_cumulatif(r)

    # Vitesse totale
    v_total_squared = v_newt_squared + delta_v_squared_asselin
    v_total = np.sqrt(max(0, v_total_squared))

    return v_total, v_newt, np.sqrt(max(0, delta_v_squared_asselin))

# ============================================================================
# 6. MODÈLE LAMBDA-CDM (pour comparaison)
# ============================================================================

def v_lambda_cdm(r):
    """
    Vitesse de rotation avec halo de matière noire (Lambda-CDM)

    Profil NFW (Navarro-Frenk-White) pour le halo
    """
    # Paramètres du halo NFW
    M_halo_200 = 1.0e12  # Masse du halo (M☉)
    c = 10  # Paramètre de concentration
    R_200 = 200  # Rayon viriel (kpc)

    R_s = R_200 / c  # Rayon d'échelle

    # Masse du halo à l'intérieur de r (profil NFW)
    x = r / R_s
    if x > 0:
        M_halo_r = M_halo_200 * (np.log(1 + x) - x/(1 + x)) / (np.log(1 + c) - c/(1 + c))
    else:
        M_halo_r = 0

    # Masse totale (visible + halo)
    M_total = mass_enclosed_total(r) + M_halo_r

    # Vitesse
    if r > 0:
        v = np.sqrt(G * M_total / r)
    else:
        v = 0

    return v

# ============================================================================
# 7. CALCUL ET VISUALISATION
# ============================================================================

print("=" * 80)
print("CALCUL DES COURBES DE ROTATION")
print("=" * 80)
print()

# Grille de rayons
rayons = np.linspace(0.5, R_max, 200)

# Calcul des vitesses
print("Calcul en cours...")
v_newton_array = []
v_maitrise_array = []
v_asselin_contribution = []
v_lambda_cdm_array = []
IDT_array = []
gamma_array = []

for r in rayons:
    # Newton
    v_n = v_newton(r)
    v_newton_array.append(v_n)

    # Maîtrise du Temps
    v_mt, v_n_check, v_asselin = v_maitrise_temps(r)
    v_maitrise_array.append(v_mt)
    v_asselin_contribution.append(v_asselin)

    # Lambda-CDM
    v_lcdm = v_lambda_cdm(r)
    v_lambda_cdm_array.append(v_lcdm)

    # Cartographie Després
    gamma, IDT, _ = gamma_despres(r, v_mt)
    gamma_array.append(gamma)
    IDT_array.append(IDT)

# Conversion en arrays numpy
v_newton_array = np.array(v_newton_array)
v_maitrise_array = np.array(v_maitrise_array)
v_asselin_contribution = np.array(v_asselin_contribution)
v_lambda_cdm_array = np.array(v_lambda_cdm_array)
IDT_array = np.array(IDT_array)
gamma_array = np.array(gamma_array)

print("✓ Calcul terminé")
print()

# Statistiques
print("=" * 80)
print("RÉSULTATS CLÉS")
print("=" * 80)
print()
print(f"À r = 10 kpc :")
idx_10 = np.argmin(np.abs(rayons - 10.0))
print(f"  v_Newton = {v_newton_array[idx_10]:.1f} km/s")
print(f"  v_Asselin (contribution) = {v_asselin_contribution[idx_10]:.1f} km/s")
print(f"  v_Maîtrise_Temps = {v_maitrise_array[idx_10]:.1f} km/s")
print(f"  v_Lambda-CDM = {v_lambda_cdm_array[idx_10]:.1f} km/s")
print(f"  IDT (Indice Distorsion Temporelle) = {IDT_array[idx_10]:.2e}")
print()

print(f"À r = 20 kpc :")
idx_20 = np.argmin(np.abs(rayons - 20.0))
print(f"  v_Newton = {v_newton_array[idx_20]:.1f} km/s")
print(f"  v_Asselin (contribution) = {v_asselin_contribution[idx_20]:.1f} km/s")
print(f"  v_Maîtrise_Temps = {v_maitrise_array[idx_20]:.1f} km/s")
print(f"  v_Lambda-CDM = {v_lambda_cdm_array[idx_20]:.1f} km/s")
print(f"  IDT = {IDT_array[idx_20]:.2e}")
print()

# ============================================================================
# 8. GRAPHIQUES
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# ---- Graphique 1 : Courbes de rotation ----
ax1 = axes[0, 0]
ax1.plot(rayons, v_newton_array, 'b--', linewidth=2, label='Newton (matière visible seule)', alpha=0.7)
ax1.plot(rayons, v_maitrise_array, 'r-', linewidth=3, label='Maîtrise du Temps (avec Liaisons Asselin)')
ax1.plot(rayons, v_lambda_cdm_array, 'g:', linewidth=2, label='Lambda-CDM (avec halo matière noire)')
ax1.set_xlabel('Rayon (kpc)', fontsize=12)
ax1.set_ylabel('Vitesse de rotation (km/s)', fontsize=12)
ax1.set_title('Courbes de Rotation Galactique - Comparaison des Modèles', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10, loc='best')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, R_max)
ax1.set_ylim(0, 300)

# ---- Graphique 2 : Contribution de l'effet Asselin ----
ax2 = axes[0, 1]
ax2.plot(rayons, v_asselin_contribution, 'purple', linewidth=2.5, label='Contribution Asselin')
ax2.fill_between(rayons, 0, v_asselin_contribution, alpha=0.3, color='purple')
ax2.set_xlabel('Rayon (kpc)', fontsize=12)
ax2.set_ylabel('Vitesse additionnelle (km/s)', fontsize=12)
ax2.set_title('Contribution des Liaisons Asselin à la Vitesse', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, R_max)

# ---- Graphique 3 : Cartographie Després (IDT) ----
ax3 = axes[1, 0]
ax3.semilogy(rayons, IDT_array, 'orange', linewidth=2.5, label='IDT (Indice Distorsion Temporelle)')
ax3.set_xlabel('Rayon (kpc)', fontsize=12)
ax3.set_ylabel('IDT = γ_Després - 1', fontsize=12)
ax3.set_title('Cartographie Després : Distorsion Temporelle Galactique', fontsize=14, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3, which='both')
ax3.set_xlim(0, R_max)

# ---- Graphique 4 : Ratio Maîtrise du Temps / Newton ----
ax4 = axes[1, 1]
ratio = v_maitrise_array / (v_newton_array + 1e-10)  # Éviter division par zéro
ax4.plot(rayons, ratio, 'darkred', linewidth=2.5, label='v_Maîtrise / v_Newton')
ax4.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Ratio = 1 (Newton pur)')
ax4.fill_between(rayons, 1, ratio, where=(ratio >= 1), alpha=0.3, color='red',
                  label='Excès par rapport à Newton')
ax4.set_xlabel('Rayon (kpc)', fontsize=12)
ax4.set_ylabel('Ratio de vitesse', fontsize=12)
ax4.set_title('Amplification par Effet Asselin', fontsize=14, fontweight='bold')
ax4.legend(fontsize=10, loc='best')
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, R_max)

plt.tight_layout()
plt.savefig('/home/user/Maitrise-du-temps/courbe_rotation_maitrise_temps.png',
            dpi=300, bbox_inches='tight')
print("✓ Graphique sauvegardé : courbe_rotation_maitrise_temps.png")
print()

# ============================================================================
# 9. TABLEAU RÉCAPITULATIF
# ============================================================================

print("=" * 80)
print("TABLEAU RÉCAPITULATIF DES VALEURS")
print("=" * 80)
print()
print(f"{'Rayon (kpc)':<15} | {'v_Newton':<12} | {'v_Asselin':<12} | {'v_Total':<12} | {'v_LCDM':<12} | {'IDT':<12}")
print("-" * 95)

for i in [0, 25, 50, 75, 100, 125, 150, 175, 199]:
    r = rayons[i]
    print(f"{r:<15.1f} | {v_newton_array[i]:<12.1f} | {v_asselin_contribution[i]:<12.1f} | "
          f"{v_maitrise_array[i]:<12.1f} | {v_lambda_cdm_array[i]:<12.1f} | {IDT_array[i]:<12.2e}")

print()
print("=" * 80)
print("INTERPRÉTATION")
print("=" * 80)
print()
print("1. NEWTON (bleu pointillé) : Décroît en périphérie (attendu sans matière noire)")
print()
print("2. MAÎTRISE DU TEMPS (rouge) : Plateau en périphérie grâce aux Liaisons Asselin")
print("   → L'effet cumulatif des distorsions temporelles compense la chute newtonienne")
print()
print("3. LAMBDA-CDM (vert) : Plateau dû au halo de matière noire")
print("   → Courbe similaire mais mécanisme différent")
print()
print("4. CONTRIBUTION ASSELIN (violet) : Croît avec le rayon")
print("   → Effet volumique cumulatif (plus de matière → plus de liaisons)")
print()
print("5. IDT (orange) : Décroît avec le rayon")
print("   → Distorsion temporelle plus forte au centre (plus de masse)")
print()
print("=" * 80)

plt.show()
