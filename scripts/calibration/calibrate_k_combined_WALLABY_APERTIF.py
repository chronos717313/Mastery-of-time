#!/usr/bin/env python3
"""
Combined k(M) Calibration: WALLABY DR2 + APERTIF DR1
====================================================
Combine WALLABY (~1,800 galaxies) and APERTIF (~1,740 galaxies) for
improved k(M) calibration with ~3,500 total galaxies.

Current calibration (SPARC, 172 galaxies):
    k = 4.00 x (M/10^10)^(-0.49), R^2 = 0.64

Goal: 20x more galaxies -> better statistics, improved R^2

TMT v2.4 formulation:
    M_eff(r) = M_bary(r) x [1 + k x (r/r_c)]
    r_c(M) = 2.6 x (M/10^10)^0.56 kpc
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Constants
G_KPC = 4.302e-6  # kpc (km/s)^2 / M_sun

# Directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = PROJECT_DIR / "data"
WALLABY_DIR = DATA_DIR / "WALLABY_DR2"
APERTIF_DIR = DATA_DIR / "APERTIF_DR1"
RESULTS_DIR = DATA_DIR / "results"


def r_c_from_mass(M_bary):
    """TMT v2.4: r_c(M) = 2.6 x (M/10^10)^0.56 kpc"""
    return 2.6 * (M_bary / 1e10) ** 0.56


def load_rotation_curves(filepath: Path) -> dict:
    """Load rotation curves from SPARC-compatible format."""
    rotation_curves = {}

    if not filepath.exists():
        return rotation_curves

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            parts = line.split()
            if len(parts) < 8:
                continue

            try:
                name = parts[0]
                D = float(parts[1])
                R = float(parts[2])
                Vobs = float(parts[3])
                e_Vobs = float(parts[4])
                Vgas = float(parts[5])
                Vdisk = float(parts[6])
                Vbul = float(parts[7])

                if name not in rotation_curves:
                    rotation_curves[name] = {
                        'R': [], 'Vobs': [], 'e_Vobs': [],
                        'Vgas': [], 'Vdisk': [], 'Vbul': [],
                        'distance': D
                    }

                rotation_curves[name]['R'].append(R)
                rotation_curves[name]['Vobs'].append(Vobs)
                rotation_curves[name]['e_Vobs'].append(max(e_Vobs, 1.0))
                rotation_curves[name]['Vgas'].append(Vgas)
                rotation_curves[name]['Vdisk'].append(Vdisk)
                rotation_curves[name]['Vbul'].append(Vbul)

            except (ValueError, IndexError):
                continue

    for name in rotation_curves:
        for key in ['R', 'Vobs', 'e_Vobs', 'Vgas', 'Vdisk', 'Vbul']:
            rotation_curves[name][key] = np.array(rotation_curves[name][key])

    return rotation_curves


def compute_V_bary(Vgas, Vdisk, Vbul, ML_disk=0.5, ML_bul=0.7):
    """Compute baryonic velocity."""
    V_bary_sq = Vgas**2 + ML_disk * Vdisk**2 + ML_bul * Vbul**2
    return np.sqrt(np.maximum(V_bary_sq, 0))


def compute_M_bary_enclosed(R, Vgas, Vdisk, Vbul, ML_disk=0.5, ML_bul=0.7):
    """Compute enclosed baryonic mass."""
    V_bary = compute_V_bary(Vgas, Vdisk, Vbul, ML_disk, ML_bul)
    return V_bary**2 * R / G_KPC


def V_TMT_with_k(R, M_bary_enc, k, r_c):
    """TMT velocity model."""
    multiplier = 1.0 + k * (R / r_c)
    M_eff = M_bary_enc * multiplier
    return np.sqrt(np.maximum(G_KPC * M_eff / R, 0))


def chi2_reduced(V_model, V_obs, e_V, n_params=1):
    """Reduced chi-squared."""
    residuals = (V_model - V_obs) / e_V
    chi2 = np.sum(residuals**2)
    dof = len(V_obs) - n_params
    return chi2 / max(dof, 1)


def optimize_k_for_galaxy(R, Vobs, e_Vobs, M_bary_enc, r_c):
    """Find optimal k for a galaxy."""
    def objective(k):
        if k < 0:
            return 1e10
        V_model = V_TMT_with_k(R, M_bary_enc, k, r_c)
        return chi2_reduced(V_model, Vobs, e_Vobs, n_params=1)

    result = minimize_scalar(objective, bounds=(0.001, 100), method='bounded')
    return result.x, result.fun


def optimize_k_rc_for_galaxy(R, Vobs, e_Vobs, M_bary_enc):
    """Optimize both k and r_c."""
    def objective(params):
        k, r_c = params
        if k <= 0 or r_c <= 0:
            return 1e10
        V_model = V_TMT_with_k(R, M_bary_enc, k, r_c)
        return chi2_reduced(V_model, Vobs, e_Vobs, n_params=2)

    best_result = None
    best_chi2 = np.inf

    for k_init in [0.5, 1, 2, 5]:
        for rc_init in [1, 3, 5, 10]:
            try:
                result = minimize(objective, [k_init, rc_init],
                                bounds=[(0.01, 100), (0.1, 100)],
                                method='L-BFGS-B')
                if result.fun < best_chi2:
                    best_chi2 = result.fun
                    best_result = result
            except:
                continue

    if best_result is not None:
        return best_result.x[0], best_result.x[1], best_chi2
    return 1.0, 5.0, np.inf


def analyze_galaxy(name: str, rc: dict, source: str) -> dict:
    """Analyze a single galaxy."""
    R = rc['R']
    Vobs = rc['Vobs']
    e_Vobs = rc['e_Vobs']

    if len(R) < 5:
        return None

    V_bary = compute_V_bary(rc['Vgas'], rc['Vdisk'], rc['Vbul'])
    M_bary_enc = compute_M_bary_enclosed(R, rc['Vgas'], rc['Vdisk'], rc['Vbul'])

    M_bary_total = M_bary_enc[-1] if len(M_bary_enc) > 0 else 0

    if M_bary_total < 1e6:
        return None

    chi2_newton = chi2_reduced(V_bary, Vobs, e_Vobs, n_params=0)
    r_c_mass = r_c_from_mass(M_bary_total)
    k_opt, chi2_k = optimize_k_for_galaxy(R, Vobs, e_Vobs, M_bary_enc, r_c_mass)
    k_free, r_c_free, chi2_free = optimize_k_rc_for_galaxy(R, Vobs, e_Vobs, M_bary_enc)

    improvement_k = (chi2_newton - chi2_k) / chi2_newton * 100 if chi2_newton > 0 else 0
    baryonic_valid = chi2_newton / chi2_k < 1.1 if chi2_k > 0 else False

    return {
        'name': name,
        'source': source,
        'M_bary': M_bary_total,
        'n_points': len(R),
        'chi2_newton': chi2_newton,
        'k_opt': k_opt,
        'chi2_k': chi2_k,
        'r_c_mass': r_c_mass,
        'improvement_k': improvement_k,
        'k_free': k_free,
        'r_c_free': r_c_free,
        'chi2_free': chi2_free,
        'baryonic_valid': baryonic_valid
    }


def k_law(M, a, b):
    """k = a x (M/10^10)^b"""
    return a * (M / 1e10) ** b


def calibrate_relations(results: list) -> tuple:
    """Calibrate k(M) and r_c(M) relations."""
    # Filter valid results
    valid = [r for r in results if r is not None
             and r['M_bary'] > 1e7
             and 0.01 < r['k_opt'] < 100
             and not r['baryonic_valid']]

    if len(valid) < 20:
        return {'error': 'Not enough data'}, {'error': 'Not enough data'}

    M_array = np.array([r['M_bary'] for r in valid])
    k_array = np.array([r['k_opt'] for r in valid])
    rc_array = np.array([r['r_c_free'] for r in valid])

    # k(M) calibration
    log_M = np.log10(M_array / 1e10)
    log_k = np.log10(k_array)
    mask_k = np.isfinite(log_M) & np.isfinite(log_k)

    slope_k, intercept_k, r_k, p_k, _ = stats.linregress(log_M[mask_k], log_k[mask_k])
    a_k = 10 ** intercept_k
    b_k = slope_k
    r2_k = r_k ** 2

    k_calib = {
        'a': a_k, 'b': b_k, 'R2': r2_k, 'p_value': p_k,
        'n_galaxies': np.sum(mask_k),
        'mass_range': (M_array.min(), M_array.max())
    }

    # r_c(M) calibration
    log_rc = np.log10(rc_array)
    mask_rc = np.isfinite(log_M) & np.isfinite(log_rc) & (rc_array > 0.1) & (rc_array < 100)

    slope_rc, intercept_rc, r_rc, p_rc, _ = stats.linregress(log_M[mask_rc], log_rc[mask_rc])
    A_rc = 10 ** intercept_rc
    alpha_rc = slope_rc
    r2_rc = r_rc ** 2

    rc_calib = {
        'A': A_rc, 'alpha': alpha_rc, 'R2': r2_rc, 'p_value': p_rc,
        'n_galaxies': np.sum(mask_rc)
    }

    return k_calib, rc_calib


def main():
    print("=" * 70)
    print("COMBINED k(M) CALIBRATION: WALLABY DR2 + APERTIF DR1")
    print("=" * 70)
    print()

    # Load WALLABY data
    wallaby_files = list(WALLABY_DIR.glob("*rotation_curves*.txt"))
    apertif_files = list(APERTIF_DIR.glob("*rotation_curves*.txt"))

    if not wallaby_files and not apertif_files:
        print("No rotation curve files found!")
        print("Run download_WALLABY_DR2.py and download_APERTIF_DR1.py first.")
        return

    all_rotation_curves = {}

    # Load WALLABY
    if wallaby_files:
        print(f"Loading WALLABY: {wallaby_files[0]}")
        wallaby_rc = load_rotation_curves(wallaby_files[0])
        print(f"  Loaded {len(wallaby_rc)} galaxies")
        for name, rc in wallaby_rc.items():
            all_rotation_curves[f"WALLABY_{name}"] = {**rc, 'source': 'WALLABY'}

    # Load APERTIF
    if apertif_files:
        print(f"Loading APERTIF: {apertif_files[0]}")
        apertif_rc = load_rotation_curves(apertif_files[0])
        print(f"  Loaded {len(apertif_rc)} galaxies")
        for name, rc in apertif_rc.items():
            all_rotation_curves[f"APERTIF_{name}"] = {**rc, 'source': 'APERTIF'}

    print(f"\nTotal combined: {len(all_rotation_curves)} galaxies")

    # Analyze all galaxies
    print()
    print("-" * 50)
    print("Analyzing galaxies...")
    print("-" * 50)

    results = []
    for i, (name, rc) in enumerate(all_rotation_curves.items()):
        source = rc.pop('source', 'unknown')
        result = analyze_galaxy(name, rc, source)
        if result is not None:
            results.append(result)

        if (i + 1) % 200 == 0:
            print(f"  Processed {i + 1}/{len(all_rotation_curves)} galaxies...")

    print(f"\nValid galaxies: {len(results)}")

    # Statistics by source
    wallaby_results = [r for r in results if r['source'] == 'WALLABY']
    apertif_results = [r for r in results if r['source'] == 'APERTIF']

    print(f"  WALLABY: {len(wallaby_results)}")
    print(f"  APERTIF: {len(apertif_results)}")

    # Performance statistics
    print()
    print("-" * 50)
    print("Performance Statistics")
    print("-" * 50)

    improvements = [r['improvement_k'] for r in results]
    n_improved = sum(1 for i in improvements if i > 0)
    n_baryonic = sum(1 for r in results if r['baryonic_valid'])

    print(f"\nCombined TMT v2.4 performance:")
    print(f"  Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)")
    print(f"  Baryonic-dominated: {n_baryonic}/{len(results)} ({100*n_baryonic/len(results):.1f}%)")
    print(f"  Median improvement: {np.median(improvements):.1f}%")
    print(f"  Mean improvement: {np.mean(improvements):.1f}%")

    # Calibrate relations
    print()
    print("-" * 50)
    print("Combined Calibration")
    print("-" * 50)

    k_calib, rc_calib = calibrate_relations(results)

    if 'error' not in k_calib:
        print(f"\nk(M) = {k_calib['a']:.4f} x (M/10^10)^{k_calib['b']:.3f}")
        print(f"R^2 = {k_calib['R2']:.4f}")
        print(f"Galaxies: {k_calib['n_galaxies']}")

        print(f"\nComparison with SPARC:")
        print(f"  SPARC (172 gal):   k = 4.00 x (M/10^10)^(-0.49), R^2 = 0.64")
        print(f"  Combined ({k_calib['n_galaxies']} gal): k = {k_calib['a']:.2f} x (M/10^10)^({k_calib['b']:.2f}), R^2 = {k_calib['R2']:.2f}")

    if 'error' not in rc_calib:
        print(f"\nr_c(M) = {rc_calib['A']:.2f} x (M/10^10)^{rc_calib['alpha']:.2f} kpc")
        print(f"R^2 = {rc_calib['R2']:.4f}")

        print(f"\nComparison:")
        print(f"  SPARC: r_c = 2.6 x (M/10^10)^0.56 kpc, R^2 = 0.768")
        print(f"  Combined: r_c = {rc_calib['A']:.2f} x (M/10^10)^{rc_calib['alpha']:.2f}, R^2 = {rc_calib['R2']:.3f}")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / "TMT_combined_WALLABY_APERTIF_calibration.txt"

    with open(output_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("COMBINED k(M) CALIBRATION: WALLABY DR2 + APERTIF DR1\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Total galaxies: {len(all_rotation_curves)}\n")
        f.write(f"Valid galaxies: {len(results)}\n")
        f.write(f"  WALLABY: {len(wallaby_results)}\n")
        f.write(f"  APERTIF: {len(apertif_results)}\n\n")

        f.write("=" * 50 + "\n")
        f.write("PERFORMANCE\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)\n")
        f.write(f"Median improvement: {np.median(improvements):.1f}%\n\n")

        f.write("=" * 50 + "\n")
        f.write("k(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        if 'error' not in k_calib:
            f.write(f"k = {k_calib['a']:.4f} x (M/10^10)^{k_calib['b']:.3f}\n")
            f.write(f"R^2 = {k_calib['R2']:.4f}\n")
            f.write(f"Galaxies: {k_calib['n_galaxies']}\n\n")

            f.write("Comparison with SPARC (172 galaxies):\n")
            f.write("  SPARC: k = 4.00 x (M/10^10)^(-0.49), R^2 = 0.64\n")
            f.write(f"  Combined: k = {k_calib['a']:.2f} x (M/10^10)^({k_calib['b']:.2f}), R^2 = {k_calib['R2']:.2f}\n\n")

            improvement_factor = k_calib['n_galaxies'] / 172
            f.write(f"Statistical improvement: {improvement_factor:.0f}x more galaxies\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write("r_c(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        if 'error' not in rc_calib:
            f.write(f"r_c = {rc_calib['A']:.2f} x (M/10^10)^{rc_calib['alpha']:.2f} kpc\n")
            f.write(f"R^2 = {rc_calib['R2']:.4f}\n")

    print(f"\nResults saved: {output_file}")

    # Generate plot
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        valid_results = [r for r in results if not r['baryonic_valid']]
        M_plot = np.array([r['M_bary'] for r in valid_results])
        k_plot = np.array([r['k_opt'] for r in valid_results])
        sources = [r['source'] for r in valid_results]

        # Colors by source
        colors = ['blue' if s == 'WALLABY' else 'orange' for s in sources]

        # 1. k vs M_bary
        ax1 = axes[0, 0]
        ax1.scatter(M_plot, k_plot, alpha=0.3, s=8, c=colors)

        if 'error' not in k_calib:
            M_range = np.logspace(7, 12, 100)
            k_model = k_law(M_range, k_calib['a'], k_calib['b'])
            ax1.plot(M_range, k_model, 'r-', lw=2.5,
                    label=f"Combined: k = {k_calib['a']:.2f}(M/10^10)^{k_calib['b']:.2f}")
            k_sparc = k_law(M_range, 4.00, -0.49)
            ax1.plot(M_range, k_sparc, 'g--', lw=2, alpha=0.7,
                    label="SPARC: k = 4.00(M/10^10)^(-0.49)")

        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('M_bary (M_sun)', fontsize=12)
        ax1.set_ylabel('k optimal', fontsize=12)
        ax1.set_title(f'k(M) Calibration - Combined (n={len(valid_results)})', fontsize=14)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. r_c vs M_bary
        ax2 = axes[0, 1]
        rc_plot = np.array([r['r_c_free'] for r in valid_results])
        ax2.scatter(M_plot, rc_plot, alpha=0.3, s=8, c=colors)

        if 'error' not in rc_calib:
            M_range = np.logspace(7, 12, 100)
            rc_model = rc_calib['A'] * (M_range / 1e10) ** rc_calib['alpha']
            ax2.plot(M_range, rc_model, 'r-', lw=2.5,
                    label=f"Combined: r_c = {rc_calib['A']:.2f}(M/10^10)^{rc_calib['alpha']:.2f}")
            rc_sparc = 2.6 * (M_range / 1e10) ** 0.56
            ax2.plot(M_range, rc_sparc, 'g--', lw=2, alpha=0.7,
                    label="SPARC: r_c = 2.6(M/10^10)^0.56")

        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('M_bary (M_sun)', fontsize=12)
        ax2.set_ylabel('r_c (kpc)', fontsize=12)
        ax2.set_title('r_c(M) Calibration', fontsize=14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Improvement distribution by source
        ax3 = axes[1, 0]
        impr_wallaby = [r['improvement_k'] for r in results if r['source'] == 'WALLABY']
        impr_apertif = [r['improvement_k'] for r in results if r['source'] == 'APERTIF']

        ax3.hist(impr_wallaby, bins=40, alpha=0.6, label=f'WALLABY (n={len(impr_wallaby)})', color='blue')
        ax3.hist(impr_apertif, bins=40, alpha=0.6, label=f'APERTIF (n={len(impr_apertif)})', color='orange')
        ax3.axvline(0, color='k', linestyle='-', lw=1)
        ax3.axvline(np.median(improvements), color='r', linestyle='--', lw=2,
                   label=f'Combined median = {np.median(improvements):.1f}%')
        ax3.set_xlabel('Improvement (%)', fontsize=12)
        ax3.set_ylabel('Number of galaxies', fontsize=12)
        ax3.set_title('TMT v2.4 Improvement by Survey', fontsize=14)
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. Mass distribution by source
        ax4 = axes[1, 1]
        mass_wallaby = [r['M_bary'] for r in results if r['source'] == 'WALLABY']
        mass_apertif = [r['M_bary'] for r in results if r['source'] == 'APERTIF']

        ax4.hist(np.log10(mass_wallaby), bins=40, alpha=0.6, label='WALLABY', color='blue')
        ax4.hist(np.log10(mass_apertif), bins=40, alpha=0.6, label='APERTIF', color='orange')
        ax4.set_xlabel('log10(M_bary / M_sun)', fontsize=12)
        ax4.set_ylabel('Number of galaxies', fontsize=12)
        ax4.set_title('Mass Distribution by Survey', fontsize=14)
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        fig_file = RESULTS_DIR / "TMT_combined_WALLABY_APERTIF_calibration.png"
        plt.savefig(fig_file, dpi=150)
        print(f"Figure saved: {fig_file}")
        plt.close()

    except ImportError:
        print("matplotlib not available")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY - COMBINED CALIBRATION")
    print("=" * 70)
    print()

    if 'error' not in k_calib:
        print(f"k(M) = {k_calib['a']:.3f} x (M/10^10)^{k_calib['b']:.3f}")
        print(f"R^2 = {k_calib['R2']:.3f}")
        print(f"Total galaxies: {k_calib['n_galaxies']} ({k_calib['n_galaxies']/172:.0f}x SPARC)")
        print()
        print(f"TMT v2.4 improvement: {np.median(improvements):.1f}% median")

    return results, k_calib, rc_calib


if __name__ == "__main__":
    main()
