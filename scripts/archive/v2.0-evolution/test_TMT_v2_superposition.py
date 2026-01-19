#!/usr/bin/env python3
"""
TEST TMT v2.0 - SUPERPOSITION TEMPORELLE
=========================================

Test de la formulation TMT v2.0 sur courbes de rotation galactiques.

Formulation:
    M_effective(r) = M_bary(r) × [1 + beta²(r)/alpha²(r)]

    alpha²(r) = 1 / (1 + (r/r_c)^n)
    beta²(r)  = (r/r_c)^n / (1 + (r/r_c)^n)

Parametres universels:
    r_c = 18 kpc (rayon critique)
    n   = 1.6   (exposant transition)

Reference: docs/fr/TMT_v2_REFORMULATION.md

Auteur: Pierre-Olivier Despres Asselin
Date: Janvier 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, minimize
from scipy.stats import pearsonr, spearmanr
from dataclasses import dataclass
from typing import List, Tuple
import os

# =============================================================================
# CONSTANTES PHYSIQUES
# =============================================================================

G_KPC = 4.302e-6  # kpc (km/s)² M_sun^-1

# =============================================================================
# PARAMETRES TMT v2.0 - SUPERPOSITION TEMPORELLE
# =============================================================================

R_C_DEFAULT = 18.0   # kpc - Rayon critique universel
N_DEFAULT = 1.6      # Exposant de transition

# =============================================================================
# STRUCTURE DONNEES
# =============================================================================

@dataclass
class Galaxy:
    """Structure de donnees pour une galaxie."""
    name: str
    M_stellar: float    # M_sun
    M_gas: float        # M_sun
    R_disk: float       # kpc (rayon d'echelle)
    v_flat: float       # km/s (vitesse plateau observee)

    # Courbe de rotation
    radii: np.ndarray   # kpc
    v_obs: np.ndarray   # km/s
    v_err: np.ndarray   # km/s

    @property
    def M_bary(self) -> float:
        return self.M_stellar + self.M_gas

    @property
    def f_gas(self) -> float:
        return self.M_gas / self.M_bary if self.M_bary > 0 else 0

# =============================================================================
# FONCTIONS TMT v2.0
# =============================================================================

def alpha_squared(r: float, r_c: float, n: float) -> float:
    """
    Coefficient alpha² de la superposition temporelle.

    alpha²(r) = 1 / (1 + (r/r_c)^n)

    Represente la fraction de l'etat |t> (temps forward).
    """
    if r_c <= 0:
        return 1.0
    x = (r / r_c) ** n
    return 1.0 / (1.0 + x)


def beta_squared(r: float, r_c: float, n: float) -> float:
    """
    Coefficient beta² de la superposition temporelle.

    beta²(r) = (r/r_c)^n / (1 + (r/r_c)^n)

    Represente la fraction de l'etat |t_bar> (temps backward).

    Note: alpha² + beta² = 1 (normalisation)
    """
    if r_c <= 0:
        return 0.0
    x = (r / r_c) ** n
    return x / (1.0 + x)


def mass_multiplier(r: float, r_c: float, n: float) -> float:
    """
    Multiplicateur de masse effectif.

    M_eff = M_bary × [1 + beta²/alpha²]
         = M_bary × [1 + (r/r_c)^n]

    A r << r_c: multiplicateur ~ 1 (Newtonien)
    A r >> r_c: multiplicateur ~ (r/r_c)^n (regime DM)
    """
    if r_c <= 0:
        return 1.0
    x = (r / r_c) ** n
    return 1.0 + x


def M_enclosed_exponential(r: float, M_disk: float, R_disk: float) -> float:
    """
    Masse baryonique enfermee pour profil exponentiel.

    M(r) = M_disk × [1 - (1 + r/R_d) × exp(-r/R_d)]
    """
    if R_disk <= 0 or r <= 0:
        return 0.0
    x = r / R_disk
    return M_disk * (1.0 - (1.0 + x) * np.exp(-x))


def v_rotation_TMT_v2(r: float, M_bary: float, R_disk: float,
                       r_c: float, n: float) -> float:
    """
    Vitesse de rotation predite par TMT v2.0.

    v²(r) = G × M_eff(r) / r

    avec M_eff = M_bary_enclosed × [1 + (r/r_c)^n]
    """
    if r < 0.1:
        r = 0.1

    # Masse baryonique enfermee
    M_bary_enc = M_enclosed_exponential(r, M_bary, R_disk)

    # Multiplicateur TMT v2.0
    mult = mass_multiplier(r, r_c, n)

    # Masse effective
    M_eff = M_bary_enc * mult

    # Vitesse circulaire
    v_squared = G_KPC * M_eff / r

    return np.sqrt(v_squared) if v_squared > 0 else 0.0


def v_rotation_Newton(r: float, M_bary: float, R_disk: float) -> float:
    """
    Vitesse de rotation Newtonienne (sans matiere noire).
    """
    if r < 0.1:
        r = 0.1

    M_bary_enc = M_enclosed_exponential(r, M_bary, R_disk)
    v_squared = G_KPC * M_bary_enc / r

    return np.sqrt(v_squared) if v_squared > 0 else 0.0

# =============================================================================
# GENERATION DONNEES SPARC REALISTES
# =============================================================================

def generate_sparc_sample(N: int = 175, seed: int = 42) -> List[Galaxy]:
    """
    Genere un echantillon realiste base sur les distributions SPARC.

    Les courbes de rotation sont generees avec une composante "matiere noire"
    qui simule ce qu'on observerait reellement.
    """
    np.random.seed(seed)
    galaxies = []

    for i in range(N):
        # Masse stellaire (log-uniform sur 3 ordres de grandeur)
        log_M_stellar = np.random.uniform(8.0, 11.0)
        M_stellar = 10**log_M_stellar

        # Fraction gazeuse (anti-correlée avec masse)
        f_gas_mean = 0.8 - 0.07 * (log_M_stellar - 8)
        f_gas = np.clip(np.random.normal(f_gas_mean, 0.15), 0.05, 0.9)
        M_gas = M_stellar * f_gas / (1 - f_gas)

        M_bary = M_stellar + M_gas

        # Rayon d'echelle (relation taille-masse)
        R_disk = 1.5 * (M_stellar / 1e10)**0.3 * np.random.lognormal(0, 0.2)
        R_disk = np.clip(R_disk, 0.5, 15.0)

        # Vitesse plateau (Tully-Fisher + contribution DM)
        # v_flat inclut la "matiere noire" observee
        v_bary_flat = 100 * (M_bary / 1e10)**0.25
        # Ajout contribution DM typique (facteur 1.5-3)
        dm_factor = np.random.uniform(1.5, 3.0)
        v_flat = v_bary_flat * np.sqrt(dm_factor)
        v_flat = np.clip(v_flat, 30, 350)

        # Generer courbe de rotation
        n_points = np.random.randint(15, 40)
        R_max = np.random.uniform(4, 8) * R_disk
        radii = np.linspace(0.5, R_max, n_points)

        # Courbe observee = Newton + "DM"
        # On simule une courbe plate a grand rayon
        v_obs = []
        for r in radii:
            v_newton = v_rotation_Newton(r, M_bary, R_disk)
            # Transition vers v_flat
            transition = 1 - np.exp(-r / (2 * R_disk))
            v = v_newton * (1 - transition) + v_flat * transition
            v_obs.append(v)

        v_obs = np.array(v_obs)
        v_err = 0.05 * v_obs + 3.0  # 5% + 3 km/s erreur typique

        # Ajouter bruit
        v_obs = v_obs + np.random.normal(0, 0.3, len(v_obs)) * v_err
        v_obs = np.clip(v_obs, 10, 400)

        galaxy = Galaxy(
            name=f"SPARC_{i+1:03d}",
            M_stellar=M_stellar,
            M_gas=M_gas,
            R_disk=R_disk,
            v_flat=v_flat,
            radii=radii,
            v_obs=v_obs,
            v_err=v_err
        )
        galaxies.append(galaxy)

    return galaxies

# =============================================================================
# TEST TMT v2.0
# =============================================================================

def fit_galaxy_TMT_v2(galaxy: Galaxy, r_c: float = R_C_DEFAULT,
                       n: float = N_DEFAULT) -> Tuple[float, float, float]:
    """
    Ajuste TMT v2.0 sur une galaxie.

    Returns:
        chi2_TMT: Chi² pour TMT v2.0
        chi2_Newton: Chi² pour Newton seul
        improvement: Amelioration relative
    """
    chi2_TMT = 0.0
    chi2_Newton = 0.0
    n_points = 0

    for r, v_obs, v_err in zip(galaxy.radii, galaxy.v_obs, galaxy.v_err):
        if v_err <= 0:
            continue

        # Prediction TMT v2.0
        v_TMT = v_rotation_TMT_v2(r, galaxy.M_bary, galaxy.R_disk, r_c, n)
        chi2_TMT += ((v_TMT - v_obs) / v_err)**2

        # Prediction Newton
        v_Newton = v_rotation_Newton(r, galaxy.M_bary, galaxy.R_disk)
        chi2_Newton += ((v_Newton - v_obs) / v_err)**2

        n_points += 1

    # Chi² reduit
    dof = max(n_points - 2, 1)  # 2 parametres: r_c, n
    chi2_red_TMT = chi2_TMT / dof
    chi2_red_Newton = chi2_Newton / dof

    # Amelioration
    if chi2_Newton > 0:
        improvement = (chi2_Newton - chi2_TMT) / chi2_Newton * 100
    else:
        improvement = 0.0

    return chi2_red_TMT, chi2_red_Newton, improvement


def optimize_parameters(galaxies: List[Galaxy]) -> Tuple[float, float, float]:
    """
    Optimise r_c et n sur l'ensemble des galaxies.
    """
    def total_chi2(params):
        r_c, n = params
        if r_c <= 0 or n <= 0:
            return 1e10

        chi2_sum = 0.0
        for gal in galaxies:
            chi2_TMT, _, _ = fit_galaxy_TMT_v2(gal, r_c, n)
            chi2_sum += chi2_TMT

        return chi2_sum

    # Optimisation
    result = minimize(
        total_chi2,
        x0=[18.0, 1.6],
        bounds=[(1.0, 50.0), (0.5, 3.0)],
        method='L-BFGS-B'
    )

    r_c_opt, n_opt = result.x
    chi2_opt = result.fun / len(galaxies)

    return r_c_opt, n_opt, chi2_opt


def test_TMT_v2(galaxies: List[Galaxy], r_c: float = R_C_DEFAULT,
                n: float = N_DEFAULT, verbose: bool = True) -> dict:
    """
    Test complet de TMT v2.0 sur l'echantillon.
    """
    N = len(galaxies)

    chi2_TMT_list = []
    chi2_Newton_list = []
    improvements = []

    if verbose:
        print("=" * 70)
        print("TEST TMT v2.0 - SUPERPOSITION TEMPORELLE")
        print("=" * 70)
        print(f"\nParametres: r_c = {r_c:.1f} kpc, n = {n:.2f}")
        print(f"Echantillon: {N} galaxies")
        print("\nProgression...")

    for i, gal in enumerate(galaxies):
        chi2_TMT, chi2_Newton, improvement = fit_galaxy_TMT_v2(gal, r_c, n)
        chi2_TMT_list.append(chi2_TMT)
        chi2_Newton_list.append(chi2_Newton)
        improvements.append(improvement)

        if verbose and (i + 1) % 25 == 0:
            print(f"  {i+1}/{N} galaxies analysees...")

    chi2_TMT_arr = np.array(chi2_TMT_list)
    chi2_Newton_arr = np.array(chi2_Newton_list)
    improvements_arr = np.array(improvements)

    # Statistiques
    chi2_TMT_mean = np.mean(chi2_TMT_arr)
    chi2_TMT_median = np.median(chi2_TMT_arr)
    chi2_Newton_mean = np.mean(chi2_Newton_arr)
    chi2_Newton_median = np.median(chi2_Newton_arr)

    improvement_mean = np.mean(improvements_arr)
    improvement_median = np.median(improvements_arr)

    # Combien de galaxies ameliorees?
    n_improved = np.sum(improvements_arr > 0)
    n_significant = np.sum(improvements_arr > 50)  # >50% amelioration

    results = {
        'N': N,
        'r_c': r_c,
        'n': n,
        'chi2_TMT_mean': chi2_TMT_mean,
        'chi2_TMT_median': chi2_TMT_median,
        'chi2_Newton_mean': chi2_Newton_mean,
        'chi2_Newton_median': chi2_Newton_median,
        'improvement_mean': improvement_mean,
        'improvement_median': improvement_median,
        'n_improved': n_improved,
        'n_significant': n_significant,
        'chi2_TMT_list': chi2_TMT_arr,
        'chi2_Newton_list': chi2_Newton_arr,
        'improvements': improvements_arr
    }

    if verbose:
        print("\n" + "=" * 70)
        print("RESULTATS")
        print("=" * 70)

        print(f"\n### Chi² reduit ###")
        print(f"  Newton seul:")
        print(f"    Moyenne: {chi2_Newton_mean:.2f}")
        print(f"    Mediane: {chi2_Newton_median:.2f}")
        print(f"  TMT v2.0:")
        print(f"    Moyenne: {chi2_TMT_mean:.2f}")
        print(f"    Mediane: {chi2_TMT_median:.2f}")

        print(f"\n### Amelioration vs Newton ###")
        print(f"  Moyenne:  {improvement_mean:.1f}%")
        print(f"  Mediane:  {improvement_median:.1f}%")
        print(f"  Galaxies ameliorees: {n_improved}/{N} ({100*n_improved/N:.0f}%)")
        print(f"  Amelioration >50%:   {n_significant}/{N} ({100*n_significant/N:.0f}%)")

        print(f"\n### Verdict ###")
        if improvement_mean > 50:
            print(f"  TMT v2.0 VALIDE: Amelioration moyenne {improvement_mean:.0f}% > 50%")
        elif improvement_mean > 20:
            print(f"  TMT v2.0 PARTIELLEMENT VALIDE: Amelioration {improvement_mean:.0f}%")
        else:
            print(f"  TMT v2.0 NON VALIDE: Amelioration {improvement_mean:.0f}% < 20%")

    return results


def plot_results(galaxies: List[Galaxy], results: dict, output_path: str):
    """
    Cree les graphiques de resultats.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. Distribution des ameliorations
    ax1 = axes[0, 0]
    ax1.hist(results['improvements'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.axvline(0, color='red', linestyle='--', linewidth=2, label='Pas amelioration')
    ax1.axvline(results['improvement_mean'], color='green', linestyle='-',
                linewidth=2, label=f'Moyenne: {results["improvement_mean"]:.1f}%')
    ax1.set_xlabel('Amelioration vs Newton (%)', fontsize=12)
    ax1.set_ylabel('Nombre de galaxies', fontsize=12)
    ax1.set_title('Distribution des Ameliorations TMT v2.0', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Chi² TMT vs Newton
    ax2 = axes[0, 1]
    ax2.scatter(results['chi2_Newton_list'], results['chi2_TMT_list'],
                alpha=0.5, s=30, c='steelblue')
    max_chi2 = max(np.max(results['chi2_Newton_list']), np.max(results['chi2_TMT_list']))
    ax2.plot([0, max_chi2], [0, max_chi2], 'r--', linewidth=2, label='TMT = Newton')
    ax2.set_xlabel('Chi2_red Newton', fontsize=12)
    ax2.set_ylabel('Chi2_red TMT v2.0', fontsize=12)
    ax2.set_title('Comparaison Chi2: TMT v2.0 vs Newton', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, min(max_chi2, 50))
    ax2.set_ylim(0, min(max_chi2, 50))

    # 3. Exemple courbe rotation
    ax3 = axes[1, 0]
    # Choisir une galaxie typique
    idx = len(galaxies) // 2
    gal = galaxies[idx]

    r_theory = np.linspace(0.5, np.max(gal.radii), 100)
    v_Newton = [v_rotation_Newton(r, gal.M_bary, gal.R_disk) for r in r_theory]
    v_TMT = [v_rotation_TMT_v2(r, gal.M_bary, gal.R_disk, results['r_c'], results['n'])
             for r in r_theory]

    ax3.errorbar(gal.radii, gal.v_obs, yerr=gal.v_err, fmt='o', markersize=6,
                 capsize=3, label='Observations', color='black', alpha=0.7)
    ax3.plot(r_theory, v_Newton, '--', linewidth=2, label='Newton seul', color='blue')
    ax3.plot(r_theory, v_TMT, '-', linewidth=2.5, label='TMT v2.0', color='red')
    ax3.set_xlabel('Rayon (kpc)', fontsize=12)
    ax3.set_ylabel('Vitesse rotation (km/s)', fontsize=12)
    ax3.set_title(f'Exemple: {gal.name}\nM_bary = {gal.M_bary:.2e} M_sun',
                  fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. Multiplicateur de masse
    ax4 = axes[1, 1]
    r_range = np.linspace(0.1, 60, 200)
    mult = [mass_multiplier(r, results['r_c'], results['n']) for r in r_range]

    ax4.plot(r_range, mult, linewidth=2.5, color='purple')
    ax4.axhline(1, color='gray', linestyle='--', alpha=0.5)
    ax4.axvline(results['r_c'], color='red', linestyle='--', linewidth=2,
                label=f'r_c = {results["r_c"]:.1f} kpc')
    ax4.set_xlabel('Rayon (kpc)', fontsize=12)
    ax4.set_ylabel('Multiplicateur M_eff/M_bary', fontsize=12)
    ax4.set_title(f'Effet Superposition Temporelle\nn = {results["n"]:.2f}',
                  fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, 60)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nGraphiques sauvegardes: {output_path}")


def save_results(results: dict, output_file: str):
    """
    Sauvegarde les resultats en fichier texte.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TEST TMT v2.0 - SUPERPOSITION TEMPORELLE\n")
        f.write("=" * 70 + "\n\n")

        f.write("## Formulation\n")
        f.write("M_eff(r) = M_bary(r) x [1 + (r/r_c)^n]\n\n")

        f.write("## Parametres\n")
        f.write(f"r_c = {results['r_c']:.2f} kpc\n")
        f.write(f"n   = {results['n']:.3f}\n\n")

        f.write("## Resultats\n")
        f.write(f"Echantillon: {results['N']} galaxies\n\n")

        f.write("Chi2 reduit:\n")
        f.write(f"  Newton: {results['chi2_Newton_mean']:.2f} (moyenne)\n")
        f.write(f"  TMT v2.0: {results['chi2_TMT_mean']:.2f} (moyenne)\n\n")

        f.write("Amelioration vs Newton:\n")
        f.write(f"  Moyenne:  {results['improvement_mean']:.1f}%\n")
        f.write(f"  Mediane:  {results['improvement_median']:.1f}%\n")
        f.write(f"  Galaxies ameliorees: {results['n_improved']}/{results['N']}\n")
        f.write(f"  Amelioration >50%:   {results['n_significant']}/{results['N']}\n\n")

        f.write("## Verdict\n")
        if results['improvement_mean'] > 50:
            f.write(f"TMT v2.0 VALIDE: Amelioration {results['improvement_mean']:.0f}%\n")
        elif results['improvement_mean'] > 20:
            f.write(f"TMT v2.0 PARTIELLEMENT VALIDE: Amelioration {results['improvement_mean']:.0f}%\n")
        else:
            f.write(f"TMT v2.0 NON VALIDE: Amelioration {results['improvement_mean']:.0f}%\n")

        f.write("\n" + "=" * 70 + "\n")

    print(f"Resultats sauvegardes: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TMT v2.0 - TEST SUPERPOSITION TEMPORELLE")
    print("Validation sur echantillon SPARC (175 galaxies)")
    print("=" * 70)

    # Etape 1: Generer donnees
    print("\n### Etape 1: Generation donnees SPARC ###\n")
    galaxies = generate_sparc_sample(N=175, seed=42)

    M_bary_range = [g.M_bary for g in galaxies]
    print(f"Echantillon: {len(galaxies)} galaxies")
    print(f"  M_bary: {min(M_bary_range):.2e} - {max(M_bary_range):.2e} M_sun")
    print(f"  f_gas:  {min(g.f_gas for g in galaxies):.3f} - {max(g.f_gas for g in galaxies):.3f}")

    # Etape 2: Test avec parametres par defaut
    print("\n### Etape 2: Test avec parametres par defaut ###\n")
    results_default = test_TMT_v2(galaxies, r_c=R_C_DEFAULT, n=N_DEFAULT, verbose=True)

    # Etape 3: Optimiser parametres
    print("\n### Etape 3: Optimisation parametres ###\n")
    print("Recherche r_c et n optimaux...")
    r_c_opt, n_opt, chi2_opt = optimize_parameters(galaxies)
    print(f"  r_c optimal = {r_c_opt:.2f} kpc")
    print(f"  n optimal   = {n_opt:.3f}")
    print(f"  Chi2 moyen  = {chi2_opt:.2f}")

    # Etape 4: Test avec parametres optimises
    print("\n### Etape 4: Test avec parametres optimises ###\n")
    results_opt = test_TMT_v2(galaxies, r_c=r_c_opt, n=n_opt, verbose=True)

    # Etape 5: Sauvegarder resultats
    print("\n### Etape 5: Sauvegarde ###\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(os.path.dirname(script_dir), 'data', 'results')
    os.makedirs(results_dir, exist_ok=True)

    plot_results(galaxies, results_opt, os.path.join(results_dir, 'TMT_v2_superposition_results.png'))
    save_results(results_opt, os.path.join(results_dir, 'TMT_v2_superposition_results.txt'))

    print("\n" + "=" * 70)
    print("TEST TERMINE")
    print("=" * 70)
