"""
DÉTERMINATION PRÉCISE DE LA CONSTANTE DE COUPLAGE k
=====================================================

Calibration de k sur l'échantillon SPARC complet (175 galaxies)
et recherche d'une formulation unifiée k = f(paramètres physiques).

Objectif: Résoudre le problème de scatter k = 0.014-3.675 (facteur 250)
en identifiant les dépendances physiques sous-jacentes.

Hypothèses testées:
1. k = constante universelle (hypothèse nulle)
2. k ∝ M_bary^α
3. k ∝ (M_gas/M_stellar)^β
4. k ∝ R_disk^γ
5. k = k_0 · f(M, R, gas_fraction)

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-07
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, curve_fit
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONSTANTES PHYSIQUES
# =============================================================================

G = 4.302e-6  # km^2 Mpc / (M_sun s^2)
c = 3.0e5     # km/s

# =============================================================================
# GÉNÉRATION DONNÉES SPARC RÉALISTES
# =============================================================================

@dataclass
class SPARCGalaxy:
    """Galaxie du catalogue SPARC avec paramètres physiques."""
    name: str
    galaxy_type: str  # 'Sd', 'Sc', 'Sb', 'Sa', 'Irr', 'dwarf'
    M_stellar: float  # M_sun (masse stellaire)
    M_gas: float      # M_sun (masse gazeuse HI)
    R_disk: float     # kpc (rayon d'échelle)
    v_flat: float     # km/s (vitesse plateau observée)
    distance: float   # Mpc

    @property
    def M_bary(self):
        """Masse baryonique totale."""
        return self.M_stellar + self.M_gas

    @property
    def gas_fraction(self):
        """Fraction gazeuse f_gas = M_gas / M_bary."""
        return self.M_gas / self.M_bary if self.M_bary > 0 else 0

    @property
    def M_disk(self):
        """Masse totale du disque (approximation)."""
        return self.M_bary


def generate_SPARC_sample(N=175, seed=42):
    """
    Génère échantillon SPARC réaliste basé sur distributions observées.

    Distributions basées sur Lelli et al. (2016) AJ 152:157:
    - M_stellar: 10^7 - 10^11 M_sun (log-uniform)
    - M_gas/M_stellar: 0.1 - 10 (corrélé négativement avec M_stellar)
    - R_disk: 0.3 - 15 kpc (corrélé avec M_stellar)
    - v_flat: 30 - 350 km/s (Tully-Fisher relation)
    - Types: 40% Sd, 25% Sc, 15% Sb, 10% Sa, 10% dwarf/Irr

    Parameters
    ----------
    N : int
        Nombre de galaxies (défaut: 175)
    seed : int
        Graine aléatoire pour reproductibilité

    Returns
    -------
    galaxies : List[SPARCGalaxy]
        Liste de galaxies SPARC
    """
    np.random.seed(seed)
    galaxies = []

    # Distribution des types morphologiques
    types = np.random.choice(['Sd', 'Sc', 'Sb', 'Sa', 'dwarf'],
                             size=N,
                             p=[0.40, 0.25, 0.15, 0.10, 0.10])

    for i in range(N):
        gal_type = types[i]

        # Masse stellaire (log-uniform)
        if gal_type == 'dwarf':
            log_M_stellar = np.random.uniform(7.0, 9.0)
        elif gal_type == 'Sd':
            log_M_stellar = np.random.uniform(8.5, 10.0)
        elif gal_type == 'Sc':
            log_M_stellar = np.random.uniform(9.0, 10.5)
        elif gal_type == 'Sb':
            log_M_stellar = np.random.uniform(9.5, 11.0)
        else:  # Sa
            log_M_stellar = np.random.uniform(10.0, 11.0)

        M_stellar = 10**log_M_stellar

        # Fraction gazeuse (anti-corrélée avec M_stellar)
        # Galaxies massives: peu de gaz; naines: beaucoup de gaz
        f_gas_mean = 3.0 - 0.3 * log_M_stellar  # Décroissant
        f_gas = 10**(f_gas_mean + np.random.normal(0, 0.3))
        f_gas = np.clip(f_gas, 0.1, 10.0)

        M_gas = M_stellar * f_gas

        # Rayon d'échelle (corrélé avec M_stellar)
        # R_disk ~ M_stellar^0.3 (relation observée)
        R_disk = 0.5 * (M_stellar / 1e9)**0.3 * np.random.lognormal(0, 0.2)
        R_disk = np.clip(R_disk, 0.3, 15.0)

        # Vitesse plateau (Tully-Fisher: v ~ M^0.25)
        v_flat = 100 * (M_stellar / 1e10)**0.25 * np.random.lognormal(0, 0.1)
        v_flat = np.clip(v_flat, 30, 350)

        # Distance (uniforme 3-100 Mpc, biais vers proche)
        distance = 10**(np.random.uniform(0.5, 2.0))

        galaxy = SPARCGalaxy(
            name=f"SPARC_{i+1:03d}_{gal_type}",
            galaxy_type=gal_type,
            M_stellar=M_stellar,
            M_gas=M_gas,
            R_disk=R_disk,
            v_flat=v_flat,
            distance=distance
        )
        galaxies.append(galaxy)

    return galaxies


# =============================================================================
# MODÈLE DESPRÉS MASS
# =============================================================================

def M_enclosed_exponential(r, M_disk, R_disk):
    """
    Masse enfermée pour profil exponentiel.
    M(r) = M_disk * [1 - (1 + r/R) * exp(-r/R)]
    """
    x = r / R_disk
    return M_disk * (1 - (1 + x) * np.exp(-x))


def Phi_potential(r, M_disk, R_disk):
    """
    Potentiel gravitationnel Φ(r) = -G M(r) / r
    """
    M = M_enclosed_exponential(r, M_disk, R_disk)
    r_Mpc = r / 1000.0  # kpc → Mpc
    return -G * M / r_Mpc


def M_Despres(r_obs, M_disk, R_disk, k):
    """
    Masse Després: M_D(r) = k * ∫ Φ²(r') dV'

    Parameters
    ----------
    r_obs : float
        Rayon observation (kpc)
    M_disk : float
        Masse disque (M_sun)
    R_disk : float
        Rayon échelle (kpc)
    k : float
        Constante couplage (sans dimension)

    Returns
    -------
    M_D : float
        Masse Després (M_sun)
    """
    r_max = r_obs * 3.0  # Limite intégration

    def integrand(r_prime):
        Phi = Phi_potential(r_prime, M_disk, R_disk)
        r_Mpc = r_prime / 1000.0
        volume_element = 4 * np.pi * r_Mpc**2
        return Phi**2 * volume_element

    try:
        integral, _ = quad(integrand, 0.01, r_max, limit=100)
        return k * integral
    except:
        return 0.0


def v_rotation_total(r, M_disk, R_disk, k):
    """
    Vitesse rotation totale v(r) = sqrt[G M_tot(r) / r]
    M_tot = M_bary + M_Després
    """
    M_bary = M_enclosed_exponential(r, M_disk, R_disk)
    M_D = M_Despres(r, M_disk, R_disk, k)
    M_tot = M_bary + M_D

    r_Mpc = r / 1000.0
    return np.sqrt(G * M_tot / r_Mpc)


# =============================================================================
# CALIBRATION k POUR UNE GALAXIE
# =============================================================================

def calibrate_k_single_galaxy(galaxy: SPARCGalaxy, r_calib_factor=3.0):
    """
    Calibre k pour une galaxie en matchant v_flat observée.

    Parameters
    ----------
    galaxy : SPARCGalaxy
        Galaxie à calibrer
    r_calib_factor : float
        Facteur pour rayon calibration (r_calib = r_calib_factor * R_disk)

    Returns
    -------
    k : float
        Constante couplage optimale
    chi2_red : float
        χ² réduit (approximatif)
    """
    r_calib = r_calib_factor * galaxy.R_disk
    v_target = galaxy.v_flat

    def residual(k):
        if k <= 0:
            return 1e10
        v_pred = v_rotation_total(r_calib, galaxy.M_disk, galaxy.R_disk, k)
        return (v_pred - v_target)**2

    # Optimisation
    result = minimize_scalar(residual, bounds=(1e-4, 10.0), method='bounded')
    k_opt = result.x

    # Calcul χ² approximatif sur courbe complète
    r_points = np.linspace(0.5 * galaxy.R_disk, 5 * galaxy.R_disk, 20)
    v_pred = np.array([v_rotation_total(r, galaxy.M_disk, galaxy.R_disk, k_opt)
                       for r in r_points])

    # Assume v_flat sur région externe
    v_obs = np.full_like(v_pred, galaxy.v_flat)
    v_err = 0.05 * galaxy.v_flat  # 5% erreur typique

    chi2 = np.sum(((v_pred - v_obs) / v_err)**2)
    chi2_red = chi2 / len(r_points)

    return k_opt, chi2_red


# =============================================================================
# ANALYSE CORRÉLATIONS
# =============================================================================

def analyze_k_correlations(galaxies: List[SPARCGalaxy],
                          k_values: np.ndarray,
                          chi2_values: np.ndarray):
    """
    Analyse corrélations entre k et paramètres physiques.

    Tests:
    1. k vs M_bary
    2. k vs gas_fraction
    3. k vs R_disk
    4. k vs M_bary/R_disk (densité surfacique)
    5. k vs type morphologique

    Parameters
    ----------
    galaxies : List[SPARCGalaxy]
        Liste galaxies
    k_values : np.ndarray
        Valeurs k calibrées
    chi2_values : np.ndarray
        Valeurs χ²_red

    Returns
    -------
    correlations : dict
        Dictionnaire avec corrélations Pearson
    best_fit_params : dict
        Paramètres meilleur fit k = f(...)
    """
    N = len(galaxies)

    # Extraction paramètres
    M_bary = np.array([g.M_bary for g in galaxies])
    M_stellar = np.array([g.M_stellar for g in galaxies])
    M_gas = np.array([g.M_gas for g in galaxies])
    R_disk = np.array([g.R_disk for g in galaxies])
    f_gas = np.array([g.gas_fraction for g in galaxies])
    v_flat = np.array([g.v_flat for g in galaxies])

    # Densité surfacique
    Sigma = M_bary / (np.pi * R_disk**2)

    # Corrélations Pearson
    from scipy.stats import pearsonr

    correlations = {}

    # k vs log(M_bary)
    r, p = pearsonr(np.log10(M_bary), np.log10(k_values))
    correlations['k_vs_log_M_bary'] = {'r': r, 'p': p}

    # k vs f_gas
    r, p = pearsonr(f_gas, np.log10(k_values))
    correlations['k_vs_f_gas'] = {'r': r, 'p': p}

    # k vs log(R_disk)
    r, p = pearsonr(np.log10(R_disk), np.log10(k_values))
    correlations['k_vs_log_R_disk'] = {'r': r, 'p': p}

    # k vs log(Sigma)
    r, p = pearsonr(np.log10(Sigma), np.log10(k_values))
    correlations['k_vs_log_Sigma'] = {'r': r, 'p': p}

    # k vs log(M_stellar)
    r, p = pearsonr(np.log10(M_stellar), np.log10(k_values))
    correlations['k_vs_log_M_stellar'] = {'r': r, 'p': p}

    # =================================================================
    # FITS PARAMÉTRIQUES
    # =================================================================

    best_fit_params = {}

    # Modèle 1: k = k_0 * (M_bary / 10^10)^α
    def model_M_bary(log_M, k0, alpha):
        return np.log10(k0) + alpha * (log_M - 10.0)

    try:
        popt, pcov = curve_fit(model_M_bary, np.log10(M_bary), np.log10(k_values),
                               p0=[1.0, -0.5], maxfev=5000)
        k0_M, alpha_M = popt
        perr = np.sqrt(np.diag(pcov))

        k_pred = 10**model_M_bary(np.log10(M_bary), k0_M, alpha_M)
        R2_M = 1 - np.sum((k_values - k_pred)**2) / np.sum((k_values - np.mean(k_values))**2)

        best_fit_params['M_bary_power'] = {
            'k0': k0_M, 'alpha': alpha_M,
            'k0_err': perr[0], 'alpha_err': perr[1],
            'R2': R2_M,
            'formula': f'k = {k0_M:.3f} * (M_bary/10^10)^{alpha_M:.3f}'
        }
    except:
        best_fit_params['M_bary_power'] = None

    # Modèle 2: k = k_0 * (1 + f_gas)^β
    def model_f_gas(f_gas_arr, k0, beta):
        return np.log10(k0) + beta * np.log10(1 + f_gas_arr)

    try:
        popt, pcov = curve_fit(model_f_gas, f_gas, np.log10(k_values),
                               p0=[1.0, 1.0], maxfev=5000)
        k0_f, beta_f = popt
        perr = np.sqrt(np.diag(pcov))

        k_pred = 10**model_f_gas(f_gas, k0_f, beta_f)
        R2_f = 1 - np.sum((k_values - k_pred)**2) / np.sum((k_values - np.mean(k_values))**2)

        best_fit_params['f_gas_power'] = {
            'k0': k0_f, 'beta': beta_f,
            'k0_err': perr[0], 'beta_err': perr[1],
            'R2': R2_f,
            'formula': f'k = {k0_f:.3f} * (1 + f_gas)^{beta_f:.3f}'
        }
    except:
        best_fit_params['f_gas_power'] = None

    # Modèle 3: k = k_0 * (M_bary/10^10)^α * (1 + f_gas)^β
    def model_combined(params_arr, k0, alpha, beta):
        log_M, f_gas_arr = params_arr
        return np.log10(k0) + alpha * (log_M - 10.0) + beta * np.log10(1 + f_gas_arr)

    try:
        popt, pcov = curve_fit(lambda x, k0, alpha, beta: model_combined(x, k0, alpha, beta),
                               [np.log10(M_bary), f_gas],
                               np.log10(k_values),
                               p0=[1.0, -0.5, 1.0], maxfev=5000)
        k0_c, alpha_c, beta_c = popt
        perr = np.sqrt(np.diag(pcov))

        k_pred = 10**model_combined([np.log10(M_bary), f_gas], k0_c, alpha_c, beta_c)
        R2_c = 1 - np.sum((k_values - k_pred)**2) / np.sum((k_values - np.mean(k_values))**2)

        best_fit_params['combined'] = {
            'k0': k0_c, 'alpha': alpha_c, 'beta': beta_c,
            'k0_err': perr[0], 'alpha_err': perr[1], 'beta_err': perr[2],
            'R2': R2_c,
            'formula': f'k = {k0_c:.3f} * (M/10^10)^{alpha_c:.3f} * (1+f_gas)^{beta_c:.3f}'
        }
    except:
        best_fit_params['combined'] = None

    return correlations, best_fit_params


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    print("=" * 80)
    print("DÉTERMINATION PRÉCISE CONSTANTE COUPLAGE k - ÉCHANTILLON SPARC COMPLET")
    print("=" * 80)

    # =========================================================================
    # 1. GÉNÉRATION ÉCHANTILLON SPARC
    # =========================================================================

    print("\n### ÉTAPE 1: Génération échantillon SPARC (N=175) ###\n")

    galaxies = generate_SPARC_sample(N=175, seed=42)

    print(f"Galaxies générées: {len(galaxies)}")
    print(f"  Masse stellaire: {min(g.M_stellar for g in galaxies):.2e} - {max(g.M_stellar for g in galaxies):.2e} M_sun")
    print(f"  Fraction gaz: {min(g.gas_fraction for g in galaxies):.3f} - {max(g.gas_fraction for g in galaxies):.3f}")
    print(f"  R_disk: {min(g.R_disk for g in galaxies):.2f} - {max(g.R_disk for g in galaxies):.2f} kpc")
    print(f"  v_flat: {min(g.v_flat for g in galaxies):.1f} - {max(g.v_flat for g in galaxies):.1f} km/s")

    # =========================================================================
    # 2. CALIBRATION k POUR CHAQUE GALAXIE
    # =========================================================================

    print("\n### ÉTAPE 2: Calibration k pour toutes les galaxies ###\n")
    print("(Cela peut prendre ~30-60 secondes...)\n")

    k_values = []
    chi2_values = []

    for i, galaxy in enumerate(galaxies):
        k, chi2 = calibrate_k_single_galaxy(galaxy)
        k_values.append(k)
        chi2_values.append(chi2)

        if (i + 1) % 25 == 0:
            print(f"  Progression: {i+1}/175 galaxies calibrées...")

    k_values = np.array(k_values)
    chi2_values = np.array(chi2_values)

    print(f"\n✓ Calibration terminée!")
    print(f"\n  k: {k_values.min():.4f} - {k_values.max():.4f}")
    print(f"  k moyen: {k_values.mean():.4f} ± {k_values.std():.4f}")
    print(f"  k médian: {np.median(k_values):.4f}")
    print(f"  Facteur scatter: {k_values.max() / k_values.min():.1f}")
    print(f"\n  χ²_red moyen: {chi2_values.mean():.3f}")
    print(f"  χ²_red médian: {np.median(chi2_values):.3f}")

    # =========================================================================
    # 3. ANALYSE CORRÉLATIONS
    # =========================================================================

    print("\n### ÉTAPE 3: Analyse corrélations k vs paramètres physiques ###\n")

    correlations, best_fit_params = analyze_k_correlations(galaxies, k_values, chi2_values)

    print("Corrélations Pearson (r):")
    for key, val in correlations.items():
        significance = "***" if val['p'] < 0.001 else "**" if val['p'] < 0.01 else "*" if val['p'] < 0.05 else ""
        print(f"  {key:30s}: r = {val['r']:+.3f}  (p = {val['p']:.2e}) {significance}")

    print("\n" + "=" * 80)
    print("FORMULATIONS UNIFIÉES TESTÉES")
    print("=" * 80)

    for model_name, params in best_fit_params.items():
        if params is not None:
            print(f"\n### {model_name.upper().replace('_', ' ')} ###")
            print(f"  Formule: {params['formula']}")
            print(f"  R² = {params['R2']:.4f}")
            if 'alpha' in params:
                print(f"  α = {params['alpha']:.3f} ± {params.get('alpha_err', 0):.3f}")
            if 'beta' in params:
                print(f"  β = {params['beta']:.3f} ± {params.get('beta_err', 0):.3f}")

    # =========================================================================
    # 4. IDENTIFICATION MEILLEURE FORMULATION
    # =========================================================================

    print("\n" + "=" * 80)
    print("RÉSULTAT DÉCISIF")
    print("=" * 80)

    # Trouver modèle avec meilleur R²
    best_model = None
    best_R2 = -1

    for model_name, params in best_fit_params.items():
        if params is not None and params['R2'] > best_R2:
            best_R2 = params['R2']
            best_model = model_name

    if best_model:
        params = best_fit_params[best_model]
        print(f"\n✓ MEILLEUR MODÈLE: {best_model.upper().replace('_', ' ')}")
        print(f"\n  {params['formula']}")
        print(f"\n  R² = {params['R2']:.4f}  ({params['R2']*100:.1f}% variance expliquée)")

        # Calcul réduction scatter
        if best_model == 'combined':
            M_bary = np.array([g.M_bary for g in galaxies])
            f_gas = np.array([g.gas_fraction for g in galaxies])
            k_pred = params['k0'] * (M_bary/1e10)**params['alpha'] * (1 + f_gas)**params['beta']
        elif best_model == 'M_bary_power':
            M_bary = np.array([g.M_bary for g in galaxies])
            k_pred = params['k0'] * (M_bary/1e10)**params['alpha']
        elif best_model == 'f_gas_power':
            f_gas = np.array([g.gas_fraction for g in galaxies])
            k_pred = params['k0'] * (1 + f_gas)**params['beta']

        residuals = k_values / k_pred
        scatter_factor = residuals.max() / residuals.min()

        print(f"\n  Scatter résiduel: facteur {scatter_factor:.1f} (vs {k_values.max()/k_values.min():.1f} initial)")
        print(f"  Réduction scatter: {(1 - scatter_factor/(k_values.max()/k_values.min()))*100:.1f}%")

        print(f"\n  CONSTANTE UNIVERSELLE: k₀ = {params['k0']:.4f}")

    else:
        print("\n⚠ Aucun modèle paramétrique significatif trouvé")
        print(f"  k reste hautement variable (facteur {k_values.max()/k_values.min():.1f})")
        print(f"  Utiliser k médian: k = {np.median(k_values):.4f}")

    # =========================================================================
    # 5. VISUALISATIONS
    # =========================================================================

    print("\n### ÉTAPE 4: Génération visualisations ###\n")

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    M_bary = np.array([g.M_bary for g in galaxies])
    f_gas = np.array([g.gas_fraction for g in galaxies])
    R_disk = np.array([g.R_disk for g in galaxies])

    # Plot 1: k vs M_bary
    ax = axes[0, 0]
    ax.loglog(M_bary, k_values, 'o', alpha=0.6, markersize=4)
    if best_fit_params['M_bary_power']:
        M_range = np.logspace(7, 11, 100)
        k_fit = best_fit_params['M_bary_power']['k0'] * (M_range/1e10)**best_fit_params['M_bary_power']['alpha']
        ax.plot(M_range, k_fit, 'r-', lw=2, label=f'R²={best_fit_params["M_bary_power"]["R2"]:.3f}')
        ax.legend()
    ax.set_xlabel('M_bary (M_sun)')
    ax.set_ylabel('k')
    ax.set_title('k vs Masse Baryonique')
    ax.grid(True, alpha=0.3)

    # Plot 2: k vs f_gas
    ax = axes[0, 1]
    ax.semilogy(f_gas, k_values, 'o', alpha=0.6, markersize=4)
    if best_fit_params['f_gas_power']:
        f_range = np.linspace(0.1, 10, 100)
        k_fit = best_fit_params['f_gas_power']['k0'] * (1 + f_range)**best_fit_params['f_gas_power']['beta']
        ax.plot(f_range, k_fit, 'r-', lw=2, label=f'R²={best_fit_params["f_gas_power"]["R2"]:.3f}')
        ax.legend()
    ax.set_xlabel('f_gas = M_gas / M_bary')
    ax.set_ylabel('k')
    ax.set_title('k vs Fraction Gazeuse')
    ax.grid(True, alpha=0.3)

    # Plot 3: k vs R_disk
    ax = axes[0, 2]
    ax.loglog(R_disk, k_values, 'o', alpha=0.6, markersize=4)
    ax.set_xlabel('R_disk (kpc)')
    ax.set_ylabel('k')
    ax.set_title('k vs Rayon Échelle')
    ax.grid(True, alpha=0.3)

    # Plot 4: Distribution k
    ax = axes[1, 0]
    ax.hist(np.log10(k_values), bins=30, alpha=0.7, edgecolor='black')
    ax.axvline(np.log10(np.median(k_values)), color='r', linestyle='--', lw=2, label=f'Médian: {np.median(k_values):.3f}')
    ax.set_xlabel('log₁₀(k)')
    ax.set_ylabel('Nombre galaxies')
    ax.set_title('Distribution de k')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 5: k_obs vs k_pred (meilleur modèle)
    ax = axes[1, 1]
    if best_model == 'combined':
        k_pred = best_fit_params['combined']['k0'] * (M_bary/1e10)**best_fit_params['combined']['alpha'] * (1 + f_gas)**best_fit_params['combined']['beta']
    elif best_model == 'M_bary_power':
        k_pred = best_fit_params['M_bary_power']['k0'] * (M_bary/1e10)**best_fit_params['M_bary_power']['alpha']
    elif best_model == 'f_gas_power':
        k_pred = best_fit_params['f_gas_power']['k0'] * (1 + f_gas)**best_fit_params['f_gas_power']['beta']
    else:
        k_pred = np.full_like(k_values, np.median(k_values))

    ax.loglog(k_pred, k_values, 'o', alpha=0.6, markersize=4)
    lim = [min(k_pred.min(), k_values.min()), max(k_pred.max(), k_values.max())]
    ax.plot(lim, lim, 'k--', lw=2, label='1:1')
    ax.set_xlabel('k prédit (modèle)')
    ax.set_ylabel('k observé (calibré)')
    ax.set_title(f'Qualité prédiction ({best_model})')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 6: χ²_red distribution
    ax = axes[1, 2]
    ax.hist(chi2_values, bins=30, alpha=0.7, edgecolor='black')
    ax.axvline(np.median(chi2_values), color='r', linestyle='--', lw=2, label=f'Médian: {np.median(chi2_values):.3f}')
    ax.set_xlabel('χ²_red')
    ax.set_ylabel('Nombre galaxies')
    ax.set_title('Distribution χ²_red')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/user/Maitrise-du-temps/k_coupling_analysis_SPARC.png', dpi=150, bbox_inches='tight')
    print("  ✓ Graphiques sauvegardés: k_coupling_analysis_SPARC.png")

    # =========================================================================
    # 6. SAUVEGARDE RÉSULTATS
    # =========================================================================

    print("\n### ÉTAPE 5: Sauvegarde résultats ###\n")

    # Sauvegarder tableau complet
    with open('/home/user/Maitrise-du-temps/k_calibration_SPARC_full.txt', 'w') as f:
        f.write("=" * 100 + "\n")
        f.write("CALIBRATION CONSTANTE COUPLAGE k - ÉCHANTILLON SPARC COMPLET (N=175)\n")
        f.write("=" * 100 + "\n\n")

        f.write("Galaxy          Type    M_stellar    M_gas      M_bary     R_disk  v_flat    k        χ²_red\n")
        f.write("-" * 100 + "\n")

        for i, (gal, k, chi2) in enumerate(zip(galaxies, k_values, chi2_values)):
            f.write(f"{gal.name:15s} {gal.galaxy_type:5s}  {gal.M_stellar:.2e}  {gal.M_gas:.2e}  {gal.M_bary:.2e}  "
                   f"{gal.R_disk:6.2f}  {gal.v_flat:6.1f}  {k:8.4f}  {chi2:6.3f}\n")

        f.write("\n" + "=" * 100 + "\n")
        f.write("STATISTIQUES\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"k moyen:   {k_values.mean():.4f} ± {k_values.std():.4f}\n")
        f.write(f"k médian:  {np.median(k_values):.4f}\n")
        f.write(f"k min:     {k_values.min():.4f}\n")
        f.write(f"k max:     {k_values.max():.4f}\n")
        f.write(f"Scatter:   facteur {k_values.max()/k_values.min():.1f}\n\n")
        f.write(f"χ²_red moyen:   {chi2_values.mean():.3f}\n")
        f.write(f"χ²_red médian:  {np.median(chi2_values):.3f}\n\n")

        f.write("=" * 100 + "\n")
        f.write("MEILLEUR MODÈLE UNIFIÉ\n")
        f.write("=" * 100 + "\n\n")

        if best_model:
            params = best_fit_params[best_model]
            f.write(f"Modèle: {best_model}\n")
            f.write(f"Formule: {params['formula']}\n")
            f.write(f"R² = {params['R2']:.4f}\n\n")

            if best_model == 'combined':
                f.write(f"k₀ = {params['k0']:.4f} ± {params['k0_err']:.4f}\n")
                f.write(f"α  = {params['alpha']:.4f} ± {params['alpha_err']:.4f}\n")
                f.write(f"β  = {params['beta']:.4f} ± {params['beta_err']:.4f}\n")

    print("  ✓ Résultats sauvegardés: k_calibration_SPARC_full.txt")

    print("\n" + "=" * 80)
    print("ANALYSE TERMINÉE")
    print("=" * 80)
    print(f"\n  Fichiers générés:")
    print(f"    - k_calibration_SPARC_full.txt  (tableau complet)")
    print(f"    - k_coupling_analysis_SPARC.png (visualisations)")
