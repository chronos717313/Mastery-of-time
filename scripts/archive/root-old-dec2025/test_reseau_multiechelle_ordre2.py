#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Réseau Asselin Multi-Échelle avec Ordre 2
==========================================

Date: 2025-12-05
Objectif: Tester réseau complet avec superamas et intersections IDT

AMÉLIORATION MAJEURE:
1. Inclure SUPERAMAS (masses 10^15-10^17 M☉, distances Mpc)
2. d_eff ADAPTATIF selon échelle (kpc pour galaxies, Mpc pour superamas)
3. INTERSECTIONS de lignes → points avec IDT significatif
4. RÉSEAU ORDRE 2 depuis intersections
5. Contribution IDT aux intersections au potentiel

Concept physique:
- Lignes Asselin créent structure dans espace-temps
- Aux INTERSECTIONS: distorsion temporelle renforcée
- IDT_intersection = γ_Després = renforcement non-linéaire
- Ces "nœuds" contribuent à gravitation effective
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ============================================================================
# CONSTANTES
# ============================================================================

G = 6.674e-11
c = 299792458
M_soleil = 1.989e30
kpc_to_m = 3.086e19
Mpc_to_kpc = 1000.0

# ============================================================================
# OBJETS COSMIQUES: Galaxies + Superamas
# ============================================================================

OBJETS_COSMIQUES = [
    # ===== GROUPE LOCAL (échelle kpc) =====
    {
        'nom': 'Voie Lactée',
        'type': 'galaxie',
        'M': 8.0e10 * M_soleil,
        'position': np.array([0.0, 0.0, 0.0]),
        'd_eff': 100.0  # kpc
    },
    {
        'nom': 'M31 (Andromède)',
        'type': 'galaxie',
        'M': 1.5e12 * M_soleil,
        'position': np.array([750.0, 250.0, 100.0]),
        'd_eff': 100.0
    },
    {
        'nom': 'M33 (Triangulum)',
        'type': 'galaxie',
        'M': 4.0e10 * M_soleil,
        'position': np.array([840.0, 120.0, -50.0]),
        'd_eff': 100.0
    },
    {
        'nom': 'LMC',
        'type': 'galaxie',
        'M': 1.0e10 * M_soleil,
        'position': np.array([-40.0, 30.0, -20.0]),
        'd_eff': 50.0
    },
    {
        'nom': 'SMC',
        'type': 'galaxie',
        'M': 7.0e9 * M_soleil,
        'position': np.array([-50.0, 40.0, -15.0]),
        'd_eff': 50.0
    },

    # ===== SUPERAMAS (échelle Mpc → kpc) =====
    {
        'nom': 'Amas de la Vierge',
        'type': 'superamas',
        'M': 1.2e15 * M_soleil,
        'position': np.array([16500.0, 0.0, 0.0]),  # 16.5 Mpc = 16500 kpc
        'd_eff': 5000.0  # 5 Mpc
    },
    {
        'nom': 'Superamas Hydre-Centaure',
        'type': 'superamas',
        'M': 1.0e16 * M_soleil,
        'position': np.array([50000.0, 30000.0, 10000.0]),  # ~60 Mpc
        'd_eff': 15000.0  # 15 Mpc
    },
    {
        'nom': 'Superamas Shapley',
        'type': 'superamas',
        'M': 1.0e16 * M_soleil,
        'position': np.array([200000.0, 100000.0, -50000.0]),  # ~220 Mpc
        'd_eff': 50000.0  # 50 Mpc
    },
    {
        'nom': 'Superamas Perseus-Pisces',
        'type': 'superamas',
        'M': 5.0e15 * M_soleil,
        'position': np.array([75000.0, -60000.0, 30000.0]),  # ~100 Mpc
        'd_eff': 25000.0  # 25 Mpc
    },
    {
        'nom': 'Superamas Coma',
        'type': 'superamas',
        'M': 2.0e15 * M_soleil,
        'position': np.array([100000.0, 20000.0, -15000.0]),  # ~102 Mpc
        'd_eff': 30000.0  # 30 Mpc
    }
]

# ============================================================================
# DONNÉES OBSERVATIONNELLES
# ============================================================================

r_obs_kpc = np.array([
    0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0,
    9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 18.0, 20.0,
    22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0,
    42.0, 44.0, 46.0, 48.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0,
    80.0, 85.0, 90.0, 95.0, 100.0, 110.0, 120.0, 130.0, 140.0
])

v_obs_kms = np.array([
    80, 120, 145, 165, 180, 190, 205, 215, 220, 222, 220,
    218, 215, 213, 210, 208, 206, 205, 203, 202, 200,
    199, 198, 197, 196, 195, 194, 193, 192, 191, 190,
    189, 188, 187, 186, 185, 183, 180, 178, 175, 173,
    170, 168, 165, 163, 160, 155, 150, 145, 140
])

sigma_obs_kms = np.array([10.0] * len(v_obs_kms))

# ============================================================================
# MASSE VISIBLE
# ============================================================================

def masse_visible(r_kpc):
    """Masse visible Voie Lactée"""
    M_bulbe = 1.5e10 * M_soleil
    a_bulbe = 0.7
    M_bulbe_r = M_bulbe * (r_kpc**2) / ((r_kpc + a_bulbe)**2)

    M_disque = 6.0e10 * M_soleil
    R_d = 3.5
    x = r_kpc / R_d
    M_disque_r = M_disque * (1 - (1 + x) * math.exp(-x))

    M_gaz = 1.0e10 * M_soleil
    R_gaz = 7.0
    x_gaz = r_kpc / R_gaz
    M_gaz_r = M_gaz * (1 - (1 + x_gaz) * math.exp(-x_gaz))

    return M_bulbe_r + M_disque_r + M_gaz_r

# ============================================================================
# LIGNE ASSELIN ORDRE 1
# ============================================================================

class LigneAsselin:
    """Ligne Asselin entre deux objets cosmiques"""

    def __init__(self, objet_i, objet_j, ordre=1):
        """
        Args:
            objet_i, objet_j: Objets cosmiques
            ordre: 1 (objets physiques) ou 2 (intersections)
        """
        self.ordre = ordre
        self.i = objet_i
        self.j = objet_j
        self.r_i = objet_i['position']
        self.r_j = objet_j['position']

        # Distance
        self.d_ij = np.linalg.norm(self.r_j - self.r_i)

        # d_eff adaptatif (moyenne des deux objets)
        if ordre == 1:
            self.d_eff = (objet_i['d_eff'] + objet_j['d_eff']) / 2
        else:
            # Pour ordre 2, utiliser d_eff plus petit (local)
            self.d_eff = min(objet_i.get('d_eff', 100.0), objet_j.get('d_eff', 100.0))

        # Intensité Asselin
        self.intensite = self.calculer_intensite()

        # IDT (Indice Distorsion Temporelle) γ_Després
        self.gamma_IDT = self.calculer_IDT()

    def calculer_intensite(self):
        """I_ij = √(M_i·M_j) / d²_ij · exp(-d_ij/d_eff)"""
        M_i = self.i['M']
        M_j = self.j['M']

        if self.d_ij < 0.1:
            self.d_ij = 0.1

        I = math.sqrt(M_i * M_j / M_soleil**2) / (self.d_ij**2) * math.exp(-self.d_ij / self.d_eff)
        return I

    def calculer_IDT(self):
        """
        Indice de Distorsion Temporelle γ_Després

        γ = Φ/c² où Φ ≈ GM/d (potentiel moyen)
        """
        M_moy = math.sqrt(self.i['M'] * self.j['M'])
        Phi = G * M_moy / (self.d_ij * kpc_to_m)
        gamma = Phi / c**2
        return gamma

    def distance_point(self, P):
        """Distance d'un point P à la ligne"""
        u = self.r_j - self.r_i
        w = P - self.r_i

        s = np.dot(w, u) / np.dot(u, u)
        s = max(0.0, min(s, 1.0))

        P_proj = self.r_i + s * u
        d = np.linalg.norm(P - P_proj)

        return d, s

# ============================================================================
# INTERSECTIONS ET RÉSEAU ORDRE 2
# ============================================================================

def trouver_intersections(lignes_ordre1, epsilon_kpc=1000.0):
    """
    Trouve intersections (quasi-intersections) des lignes Ordre 1

    Args:
        lignes_ordre1: Liste de LigneAsselin
        epsilon_kpc: Distance max pour considérer intersection (kpc)

    Returns:
        intersections: Liste de points d'intersection avec IDT
    """
    intersections = []
    N = len(lignes_ordre1)

    print(f"  Recherche d'intersections parmi {N} lignes...")
    print(f"  Critère: distance < {epsilon_kpc} kpc")

    compteur = 0
    for i in range(N):
        for j in range(i+1, N):
            L1 = lignes_ordre1[i]
            L2 = lignes_ordre1[j]

            # Distance minimale entre les deux lignes
            d_min, P_milieu = distance_ligne_ligne_3D(L1, L2)

            if d_min < epsilon_kpc:
                # Intersection détectée!
                compteur += 1

                # IDT au point d'intersection = renforcement des deux lignes
                gamma_1 = L1.gamma_IDT
                gamma_2 = L2.gamma_IDT

                # Renforcement NON-LINÉAIRE (quadratique)
                gamma_intersection = math.sqrt(gamma_1**2 + gamma_2**2)

                # Masse effective associée à l'intersection
                # M_int ∝ γ × c²/G × d_caractéristique
                d_carac = (L1.d_eff + L2.d_eff) / 2
                M_intersection = gamma_intersection * c**2 / G * d_carac * kpc_to_m

                intersection = {
                    'position': P_milieu,
                    'M': M_intersection,
                    'd_eff': d_carac,
                    'gamma_IDT': gamma_intersection,
                    'lignes_sources': [i, j],
                    'type': 'intersection'
                }

                intersections.append(intersection)

    print(f"  → {compteur} intersections trouvées")
    return intersections

def distance_ligne_ligne_3D(L1, L2):
    """
    Distance minimale entre deux lignes dans l'espace 3D

    Returns:
        d_min: Distance minimale
        P_milieu: Point milieu de la distance minimale
    """
    r1_i, r1_j = L1.r_i, L1.r_j
    r2_i, r2_j = L2.r_i, L2.r_j

    u = r1_j - r1_i
    v = r2_j - r2_i
    w = r1_i - r2_i

    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)

    denom = a*c - b*b

    if denom < 1e-10:  # Lignes parallèles
        return np.inf, None

    s1 = (b*e - c*d) / denom
    s2 = (a*e - b*d) / denom

    s1 = max(0, min(s1, 1))
    s2 = max(0, min(s2, 1))

    P1 = r1_i + s1 * u
    P2 = r2_i + s2 * v

    d_min = np.linalg.norm(P2 - P1)
    P_milieu = (P1 + P2) / 2

    return d_min, P_milieu

def creer_reseau_ordre2(intersections, lignes_ordre1):
    """
    Crée lignes Asselin Ordre 2 depuis intersections

    Args:
        intersections: Points d'intersection
        lignes_ordre1: Lignes ordre 1 (pour référence)

    Returns:
        lignes_ordre2: Liste de LigneAsselin ordre 2
    """
    lignes_ordre2 = []
    N_int = len(intersections)

    print(f"  Création réseau Ordre 2 depuis {N_int} intersections...")

    # Lignes entre intersections
    for i in range(N_int):
        for j in range(i+1, N_int):
            ligne = LigneAsselin(intersections[i], intersections[j], ordre=2)
            lignes_ordre2.append(ligne)

    print(f"  → {len(lignes_ordre2)} lignes Ordre 2 créées")
    return lignes_ordre2

# ============================================================================
# RÉSEAU COMPLET
# ============================================================================

def creer_reseau_complet(objets, epsilon_kpc=1000.0):
    """
    Crée réseau complet: Ordre 1 + Intersections + Ordre 2

    Returns:
        dict avec 'ordre1', 'intersections', 'ordre2'
    """
    print("\n" + "="*80)
    print("CRÉATION DU RÉSEAU COMPLET")
    print("="*80)

    # Ordre 1: Toutes lignes entre objets physiques
    print(f"\n1. ORDRE 1: Lignes entre {len(objets)} objets cosmiques")
    lignes_ordre1 = []
    N = len(objets)
    for i in range(N):
        for j in range(i+1, N):
            ligne = LigneAsselin(objets[i], objets[j], ordre=1)
            lignes_ordre1.append(ligne)

    print(f"  → {len(lignes_ordre1)} lignes Ordre 1 créées")

    # Statistiques
    I_max = max([L.intensite for L in lignes_ordre1])
    I_min = min([L.intensite for L in lignes_ordre1 if L.intensite > 0])
    print(f"  Intensités: [{I_min:.2e}, {I_max:.2e}]")

    # Intersections
    print(f"\n2. INTERSECTIONS (ε = {epsilon_kpc} kpc)")
    intersections = trouver_intersections(lignes_ordre1, epsilon_kpc)

    if len(intersections) == 0:
        print("  ⚠️  Aucune intersection trouvée!")
        print("  → Augmenter epsilon ou vérifier géométrie")
        return {'ordre1': lignes_ordre1, 'intersections': [], 'ordre2': []}

    # Ordre 2: Lignes entre intersections
    print(f"\n3. ORDRE 2: Réseau depuis intersections")
    lignes_ordre2 = creer_reseau_ordre2(intersections, lignes_ordre1)

    print("\n" + "="*80)
    print(f"RÉSEAU TOTAL: {len(lignes_ordre1)} Ordre 1 + {len(intersections)} Intersections + {len(lignes_ordre2)} Ordre 2")
    print("="*80 + "\n")

    return {
        'ordre1': lignes_ordre1,
        'intersections': intersections,
        'ordre2': lignes_ordre2
    }

# ============================================================================
# MASSE EFFECTIVE AVEC RÉSEAU COMPLET
# ============================================================================

def masse_effective_reseau_complet(r_kpc, reseau, sigma_kpc=10.0, kappa_ordre1=1e6, kappa_ordre2=1e7, kappa_int=1e8):
    """
    Masse effective avec réseau multi-niveaux + intersections IDT

    M_eff = M_vis + Contribution_Ordre1 + Contribution_Intersections + Contribution_Ordre2

    Args:
        r_kpc: Rayon galactique
        reseau: Dict avec 'ordre1', 'intersections', 'ordre2'
        sigma_kpc: Largeur gaussienne
        kappa_ordre1, kappa_ordre2, kappa_int: Facteurs de couplage

    Returns:
        M_eff en kg
    """
    M_vis = masse_visible(r_kpc)
    P = np.array([r_kpc, 0.0, 0.0])

    # Contribution Ordre 1 (galaxies + superamas)
    contrib_ordre1 = 0.0
    for ligne in reseau['ordre1']:
        d_ligne, s = ligne.distance_point(P)
        w = math.exp(-d_ligne**2 / sigma_kpc**2)
        contrib_ordre1 += w * ligne.intensite

    # Contribution Intersections (IDT renforcé!)
    contrib_intersections = 0.0
    for inter in reseau['intersections']:
        d_inter = np.linalg.norm(P - inter['position'])
        w = math.exp(-d_inter**2 / sigma_kpc**2)
        # Contribution proportionnelle à γ_IDT
        contrib_intersections += w * inter['gamma_IDT'] * 1e40  # Facteur normalization

    # Contribution Ordre 2 (lignes entre intersections)
    contrib_ordre2 = 0.0
    for ligne in reseau['ordre2']:
        d_ligne, s = ligne.distance_point(P)
        w = math.exp(-d_ligne**2 / sigma_kpc**2)
        contrib_ordre2 += w * ligne.intensite

    # Masse totale
    M_eff = (M_vis +
             kappa_ordre1 * M_soleil * contrib_ordre1 +
             kappa_int * M_soleil * contrib_intersections +
             kappa_ordre2 * M_soleil * contrib_ordre2)

    return M_eff

# ============================================================================
# VITESSE ET CHI²
# ============================================================================

def vitesse_orbitale(r_kpc, M_eff_kg):
    """v = sqrt(GM_eff/r)"""
    r_m = r_kpc * kpc_to_m
    v_ms = math.sqrt(G * M_eff_kg / r_m)
    return v_ms / 1000.0

def vitesse_orbitale_newton(r_kpc):
    """Newton (masse visible)"""
    M_vis = masse_visible(r_kpc)
    return vitesse_orbitale(r_kpc, M_vis)

def chi_carre(v_calc, v_obs, sigma_obs):
    """χ²"""
    residus = (v_calc - v_obs) / sigma_obs
    return np.sum(residus**2)

# ============================================================================
# COURBE DE ROTATION
# ============================================================================

def courbe_rotation_reseau_complet(r_array, reseau, params):
    """
    Courbe de rotation avec réseau complet

    Args:
        r_array: Rayons
        reseau: Réseau complet
        params: (sigma, kappa_1, kappa_2, kappa_int)
    """
    sigma, kappa_1, kappa_2, kappa_int = params

    v_array = []
    for r in r_array:
        M_eff = masse_effective_reseau_complet(r, reseau, sigma, kappa_1, kappa_2, kappa_int)
        v = vitesse_orbitale(r, M_eff)
        v_array.append(v)

    return np.array(v_array)

# ============================================================================
# TEST
# ============================================================================

def test_reseau_complet():
    """Test réseau multi-échelle avec ordre 2"""
    print("\n" + "="*80)
    print(" RÉSEAU ASSELIN MULTI-ÉCHELLE AVEC ORDRE 2 ".center(80))
    print("="*80)

    # Créer réseau
    reseau = creer_reseau_complet(OBJETS_COSMIQUES, epsilon_kpc=5000.0)

    # Test Newton
    print("\nTEST 1: Newton")
    print("-" * 80)
    v_newton = np.array([vitesse_orbitale_newton(r) for r in r_obs_kpc])
    chi2_newton = chi_carre(v_newton, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_newton:.2f}")

    # Test nominal
    print("\nTEST 2: Réseau complet (paramètres nominaux)")
    print("-" * 80)
    params_nominal = (10.0, 1e6, 1e7, 1e8)  # sigma, kappa_1, kappa_2, kappa_int
    v_nominal = courbe_rotation_reseau_complet(r_obs_kpc, reseau, params_nominal)
    chi2_nominal = chi_carre(v_nominal, v_obs_kms, sigma_obs_kms)
    print(f"χ² = {chi2_nominal:.2f} ({chi2_nominal/chi2_newton:.2f}× vs Newton)")

    # Optimisation
    print("\nTEST 3: Optimisation")
    print("-" * 80)
    print("Optimisation en cours (peut prendre plusieurs minutes)...")

    def objective(params_log):
        sigma, log_k1, log_k2, log_ki = params_log
        kappa_1 = 10**log_k1
        kappa_2 = 10**log_k2
        kappa_int = 10**log_ki

        try:
            v_calc = courbe_rotation_reseau_complet(r_obs_kpc, reseau,
                                                     (sigma, kappa_1, kappa_2, kappa_int))
            return chi_carre(v_calc, v_obs_kms, sigma_obs_kms)
        except:
            return 1e10

    result = minimize(objective, x0=[10.0, 6.0, 7.0, 8.0],
                     bounds=[(0.1, 100.0), (3.0, 12.0), (3.0, 12.0), (3.0, 12.0)],
                     method='L-BFGS-B', options={'maxiter': 30})

    sigma_opt, log_k1_opt, log_k2_opt, log_ki_opt = result.x
    kappa_1_opt = 10**log_k1_opt
    kappa_2_opt = 10**log_k2_opt
    kappa_int_opt = 10**log_ki_opt
    chi2_opt = result.fun

    print(f"\n  σ optimal        = {sigma_opt:.2f} kpc")
    print(f"  κ_ordre1 optimal = {kappa_1_opt:.2e}")
    print(f"  κ_ordre2 optimal = {kappa_2_opt:.2e}")
    print(f"  κ_inter optimal  = {kappa_int_opt:.2e}")
    print(f"  χ² optimal       = {chi2_opt:.2f} ({chi2_opt/chi2_newton:.2f}× vs Newton)")

    # Résultats
    print("\n" + "="*80)
    print(" RÉSULTATS FINAUX ".center(80))
    print("="*80)

    if chi2_opt < chi2_newton:
        amelioration = (1 - chi2_opt/chi2_newton) * 100
        print(f"\n🎉 SUCCÈS MAJEUR!")
        print(f"   χ² = {chi2_opt:.2f} < Newton ({chi2_newton:.2f})")
        print(f"   Amélioration: {amelioration:.1f}%")
        print(f"\n   LE RÉSEAU MULTI-ÉCHELLE AVEC ORDRE 2 FONCTIONNE!")
    else:
        print(f"\n⚠️  χ² = {chi2_opt:.2f} > Newton ({chi2_newton:.2f})")
        print(f"   Ratio: {chi2_opt/chi2_newton:.2f}×")

    print("\n" + "="*80 + "\n")

    return {
        'reseau': reseau,
        'chi2_newton': chi2_newton,
        'chi2_opt': chi2_opt,
        'params_opt': (sigma_opt, kappa_1_opt, kappa_2_opt, kappa_int_opt)
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    resultats = test_reseau_complet()
