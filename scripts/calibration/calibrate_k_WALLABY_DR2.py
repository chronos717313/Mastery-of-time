#!/usr/bin/env python3
"""
Calibrate k(M) on WALLABY DR2 Data
==================================
Re-calibrate TMT k(M) relation using WALLABY DR2 (~1800 galaxies).

Current calibration (SPARC, 172 galaxies):
    k = 4.00 × (M/10^10)^(-0.49), R² = 0.64

Goal: Improve calibration with 10× more galaxies.

TMT v2.4 formulation:
    M_eff(r) = M_bary(r) × [1 + k × (r/r_c)]
    r_c(M) = 2.6 × (M/10^10)^0.56 kpc

Reference: TMT v2.4 Validation (January 2026)
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize, curve_fit
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Constants
G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
C_KMS = 299792.458  # km/s

# Data directories
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = PROJECT_DIR / "data"
WALLABY_DIR = DATA_DIR / "WALLABY_DR2"
RESULTS_DIR = DATA_DIR / "results"


def r_c_from_mass(M_bary):
    """
    TMT v2.4: Critical radius depends on baryonic mass.
    r_c(M) = 2.6 × (M/10^10)^0.56 kpc
    """
    return 2.6 * (M_bary / 1e10) ** 0.56


def load_wallaby_rotation_curves(filepath: Path) -> dict:
    """
    Load WALLABY rotation curves from SPARC-compatible format.

    Format: Galaxy  D(Mpc)  R(kpc)  Vobs  e_Vobs  Vgas  Vdisk  Vbul
    """
    rotation_curves = {}

    if not filepath.exists():
        print(f"File not found: {filepath}")
        return rotation_curves

    with open(filepath, 'r') as f:
        for line in f:
            # Skip comments and headers
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

    # Convert to numpy arrays
    for name in rotation_curves:
        for key in ['R', 'Vobs', 'e_Vobs', 'Vgas', 'Vdisk', 'Vbul']:
            rotation_curves[name][key] = np.array(rotation_curves[name][key])

    return rotation_curves


def compute_V_bary(Vgas, Vdisk, Vbul, ML_disk=0.5, ML_bul=0.7):
    """
    Compute baryonic velocity contribution.
    V_bary² = Vgas² + ML_disk × Vdisk² + ML_bul × Vbul²
    """
    V_bary_sq = Vgas**2 + ML_disk * Vdisk**2 + ML_bul * Vbul**2
    return np.sqrt(np.maximum(V_bary_sq, 0))


def compute_M_bary_enclosed(R, Vgas, Vdisk, Vbul, ML_disk=0.5, ML_bul=0.7):
    """
    Compute enclosed baryonic mass from velocities.
    M(<R) = V²(R) × R / G
    """
    V_bary = compute_V_bary(Vgas, Vdisk, Vbul, ML_disk, ML_bul)
    M_enc = V_bary**2 * R / G_KPC
    return M_enc


def V_TMT_with_k(R, M_bary_enc, k, r_c):
    """
    TMT velocity with k parameter.
    M_eff(R) = M_bary(R) × [1 + k × (R/r_c)]
    V_TMT = sqrt(G × M_eff / R)
    """
    multiplier = 1.0 + k * (R / r_c)
    M_eff = M_bary_enc * multiplier
    V_sq = G_KPC * M_eff / R
    return np.sqrt(np.maximum(V_sq, 0))


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
    """Optimize both k and r_c for a galaxy."""
    def objective(params):
        k, r_c = params
        if k <= 0 or r_c <= 0:
            return 1e10
        V_model = V_TMT_with_k(R, M_bary_enc, k, r_c)
        return chi2_reduced(V_model, Vobs, e_Vobs, n_params=2)

    best_result = None
    best_chi2 = np.inf

    for k_init in [0.5, 1, 2, 5, 10]:
        for rc_init in [1, 3, 5, 10, 20]:
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


def k_law(M, a, b):
    """k = a × (M/10^10)^b"""
    return a * (M / 1e10) ** b


def analyze_galaxy(name: str, rc: dict, ML_disk=0.5, ML_bul=0.7) -> dict:
    """Analyze a single galaxy and return results."""
    R = rc['R']
    Vobs = rc['Vobs']
    e_Vobs = rc['e_Vobs']

    if len(R) < 5:
        return None

    # Compute baryonic quantities
    V_bary = compute_V_bary(rc['Vgas'], rc['Vdisk'], rc['Vbul'], ML_disk, ML_bul)
    M_bary_enc = compute_M_bary_enclosed(R, rc['Vgas'], rc['Vdisk'], rc['Vbul'],
                                          ML_disk, ML_bul)

    M_bary_total = M_bary_enc[-1] if len(M_bary_enc) > 0 else 0

    if M_bary_total < 1e6:  # Too low mass
        return None

    # Chi² Newton
    chi2_newton = chi2_reduced(V_bary, Vobs, e_Vobs, n_params=0)

    # TMT r_c from mass relation
    r_c_mass = r_c_from_mass(M_bary_total)

    # Optimize k with mass-dependent r_c
    k_opt, chi2_k = optimize_k_for_galaxy(R, Vobs, e_Vobs, M_bary_enc, r_c_mass)

    # Optimize both k and r_c freely
    k_free, r_c_free, chi2_free = optimize_k_rc_for_galaxy(R, Vobs, e_Vobs, M_bary_enc)

    # Improvement
    improvement_k = (chi2_newton - chi2_k) / chi2_newton * 100 if chi2_newton > 0 else 0
    improvement_free = (chi2_newton - chi2_free) / chi2_newton * 100 if chi2_newton > 0 else 0

    # Check if baryonic-only is valid (TMT v2.4 condition)
    baryonic_valid = chi2_newton / chi2_k < 1.1 if chi2_k > 0 else False

    return {
        'name': name,
        'M_bary': M_bary_total,
        'n_points': len(R),
        'R_max': R[-1],
        'chi2_newton': chi2_newton,
        'k_opt': k_opt,
        'chi2_k': chi2_k,
        'r_c_mass': r_c_mass,
        'improvement_k': improvement_k,
        'k_free': k_free,
        'r_c_free': r_c_free,
        'chi2_free': chi2_free,
        'improvement_free': improvement_free,
        'baryonic_valid': baryonic_valid
    }


def calibrate_k_M_relation(results: list) -> dict:
    """Calibrate k(M) relation from results."""
    # Filter valid results
    valid = [r for r in results if r is not None
             and r['M_bary'] > 1e7
             and 0.01 < r['k_opt'] < 100
             and not r['baryonic_valid']]  # Exclude baryonic-dominated galaxies

    if len(valid) < 10:
        return {'error': 'Not enough valid galaxies'}

    M_array = np.array([r['M_bary'] for r in valid])
    k_array = np.array([r['k_opt'] for r in valid])

    # Log-log regression
    log_M = np.log10(M_array / 1e10)
    log_k = np.log10(k_array)

    valid_mask = np.isfinite(log_M) & np.isfinite(log_k)

    if np.sum(valid_mask) < 10:
        return {'error': 'Not enough valid data points'}

    # Linear regression in log-log space
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        log_M[valid_mask], log_k[valid_mask]
    )

    a_fit = 10 ** intercept
    b_fit = slope
    r_squared = r_value ** 2

    # Predict and calculate residuals
    k_pred = k_law(M_array[valid_mask], a_fit, b_fit)
    residuals = k_array[valid_mask] - k_pred
    rms_residual = np.sqrt(np.mean(residuals ** 2))

    return {
        'a': a_fit,
        'b': b_fit,
        'R2': r_squared,
        'p_value': p_value,
        'std_err': std_err,
        'rms_residual': rms_residual,
        'n_galaxies': np.sum(valid_mask),
        'mass_range': (M_array.min(), M_array.max()),
        'k_range': (k_array.min(), k_array.max())
    }


def calibrate_r_c_M_relation(results: list) -> dict:
    """Calibrate r_c(M) relation from free-fit results."""
    valid = [r for r in results if r is not None
             and r['M_bary'] > 1e7
             and 0.1 < r['r_c_free'] < 100]

    if len(valid) < 10:
        return {'error': 'Not enough valid galaxies'}

    M_array = np.array([r['M_bary'] for r in valid])
    r_c_array = np.array([r['r_c_free'] for r in valid])

    # Log-log regression: r_c = A × (M/10^10)^alpha
    log_M = np.log10(M_array / 1e10)
    log_rc = np.log10(r_c_array)

    valid_mask = np.isfinite(log_M) & np.isfinite(log_rc)

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        log_M[valid_mask], log_rc[valid_mask]
    )

    A_fit = 10 ** intercept
    alpha_fit = slope
    r_squared = r_value ** 2

    return {
        'A': A_fit,
        'alpha': alpha_fit,
        'R2': r_squared,
        'p_value': p_value,
        'n_galaxies': np.sum(valid_mask),
        'formula': f"r_c = {A_fit:.2f} × (M/10^10)^{alpha_fit:.2f} kpc"
    }


def main():
    print("=" * 70)
    print("TMT k(M) CALIBRATION ON WALLABY DR2")
    print("=" * 70)
    print()

    # Find rotation curve file
    rc_files = list(WALLABY_DIR.glob("*rotation_curves*.txt"))

    if not rc_files:
        print(f"No rotation curve files found in {WALLABY_DIR}")
        print("Run download_WALLABY_DR2.py first to generate data.")
        return

    rc_file = rc_files[0]
    print(f"Loading: {rc_file}")

    # Load data
    rotation_curves = load_wallaby_rotation_curves(rc_file)
    print(f"Loaded {len(rotation_curves)} galaxies")

    if len(rotation_curves) < 10:
        print("Not enough galaxies for calibration")
        return

    # Analyze each galaxy
    print()
    print("-" * 50)
    print("Analyzing galaxies...")
    print("-" * 50)

    results = []
    for i, (name, rc) in enumerate(rotation_curves.items()):
        result = analyze_galaxy(name, rc)
        if result is not None:
            results.append(result)

        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(rotation_curves)} galaxies...")

    print(f"\nValid galaxies: {len(results)}")

    # Statistics
    print()
    print("-" * 50)
    print("Performance Statistics")
    print("-" * 50)

    improvements = [r['improvement_k'] for r in results]
    n_improved = sum(1 for i in improvements if i > 0)
    n_baryonic = sum(1 for r in results if r['baryonic_valid'])

    print(f"\nTMT v2.4 with mass-dependent r_c:")
    print(f"  Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)")
    print(f"  Baryonic-dominated (k~0): {n_baryonic}/{len(results)} ({100*n_baryonic/len(results):.1f}%)")
    print(f"  Median improvement: {np.median(improvements):.1f}%")
    print(f"  Mean improvement: {np.mean(improvements):.1f}%")

    # Calibrate k(M)
    print()
    print("-" * 50)
    print("k(M) Calibration")
    print("-" * 50)

    k_calib = calibrate_k_M_relation(results)

    if 'error' in k_calib:
        print(f"  Error: {k_calib['error']}")
    else:
        print(f"\n  k = {k_calib['a']:.4f} × (M/10^10)^{k_calib['b']:.3f}")
        print(f"  R² = {k_calib['R2']:.4f}")
        print(f"  p-value = {k_calib['p_value']:.2e}")
        print(f"  Galaxies used: {k_calib['n_galaxies']}")
        print(f"  Mass range: {k_calib['mass_range'][0]:.2e} - {k_calib['mass_range'][1]:.2e} M_sun")

        print(f"\n  Comparison with SPARC calibration:")
        print(f"    SPARC (172 gal): k = 4.00 × (M/10^10)^(-0.49), R² = 0.64")
        print(f"    WALLABY ({k_calib['n_galaxies']} gal): k = {k_calib['a']:.2f} × (M/10^10)^({k_calib['b']:.2f}), R² = {k_calib['R2']:.2f}")

    # Calibrate r_c(M)
    print()
    print("-" * 50)
    print("r_c(M) Calibration")
    print("-" * 50)

    rc_calib = calibrate_r_c_M_relation(results)

    if 'error' in rc_calib:
        print(f"  Error: {rc_calib['error']}")
    else:
        print(f"\n  {rc_calib['formula']}")
        print(f"  R² = {rc_calib['R2']:.4f}")
        print(f"  Galaxies used: {rc_calib['n_galaxies']}")

        print(f"\n  Comparison with SPARC calibration:")
        print(f"    SPARC: r_c = 2.6 × (M/10^10)^0.56 kpc, R² = 0.768")
        print(f"    WALLABY: {rc_calib['formula']}, R² = {rc_calib['R2']:.3f}")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / "TMT_WALLABY_DR2_calibration.txt"

    with open(output_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("TMT k(M) CALIBRATION ON WALLABY DR2\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Data source: {rc_file}\n")
        f.write(f"Total galaxies: {len(rotation_curves)}\n")
        f.write(f"Valid galaxies: {len(results)}\n\n")

        f.write("=" * 50 + "\n")
        f.write("PERFORMANCE\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)\n")
        f.write(f"Baryonic-dominated: {n_baryonic}/{len(results)} ({100*n_baryonic/len(results):.1f}%)\n")
        f.write(f"Median improvement: {np.median(improvements):.1f}%\n")
        f.write(f"Mean improvement: {np.mean(improvements):.1f}%\n\n")

        f.write("=" * 50 + "\n")
        f.write("k(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        if 'error' not in k_calib:
            f.write(f"k = {k_calib['a']:.4f} × (M/10^10)^{k_calib['b']:.3f}\n")
            f.write(f"R² = {k_calib['R2']:.4f}\n")
            f.write(f"p-value = {k_calib['p_value']:.2e}\n")
            f.write(f"Galaxies: {k_calib['n_galaxies']}\n\n")

            f.write("Comparison:\n")
            f.write("  SPARC (172 gal): k = 4.00 × (M/10^10)^(-0.49), R² = 0.64\n")
            f.write(f"  WALLABY ({k_calib['n_galaxies']} gal): k = {k_calib['a']:.2f} × (M/10^10)^({k_calib['b']:.2f}), R² = {k_calib['R2']:.2f}\n\n")

        f.write("=" * 50 + "\n")
        f.write("r_c(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        if 'error' not in rc_calib:
            f.write(f"{rc_calib['formula']}\n")
            f.write(f"R² = {rc_calib['R2']:.4f}\n")
            f.write(f"Galaxies: {rc_calib['n_galaxies']}\n\n")

            f.write("Comparison:\n")
            f.write("  SPARC: r_c = 2.6 × (M/10^10)^0.56 kpc, R² = 0.768\n")
            f.write(f"  WALLABY: {rc_calib['formula']}, R² = {rc_calib['R2']:.3f}\n\n")

        f.write("=" * 50 + "\n")
        f.write("DETAILED RESULTS\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"{'Galaxy':<25} {'M_bary':>12} {'k_opt':>8} {'r_c':>8} {'Improv':>8}\n")
        f.write("-" * 65 + "\n")

        for r in sorted(results, key=lambda x: x['M_bary'], reverse=True):
            f.write(f"{r['name']:<25} {r['M_bary']:>12.2e} {r['k_opt']:>8.3f} "
                   f"{r['r_c_mass']:>8.2f} {r['improvement_k']:>7.1f}%\n")

    print()
    print(f"Results saved: {output_file}")

    # Generate plot if matplotlib available
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        # Filter for plotting
        plot_results = [r for r in results if not r['baryonic_valid']]
        M_plot = np.array([r['M_bary'] for r in plot_results])
        k_plot = np.array([r['k_opt'] for r in plot_results])
        rc_plot = np.array([r['r_c_free'] for r in plot_results])
        impr_plot = np.array([r['improvement_k'] for r in plot_results])

        # 1. k vs M_bary
        ax1 = axes[0, 0]
        ax1.scatter(M_plot, k_plot, alpha=0.3, s=10, c='blue')

        if 'error' not in k_calib:
            M_range = np.logspace(7, 12, 100)
            k_model = k_law(M_range, k_calib['a'], k_calib['b'])
            ax1.plot(M_range, k_model, 'r-', lw=2,
                    label=f"WALLABY: k = {k_calib['a']:.2f}×(M/10¹⁰)^{k_calib['b']:.2f}")

            # SPARC for comparison
            k_sparc = k_law(M_range, 4.00, -0.49)
            ax1.plot(M_range, k_sparc, 'g--', lw=2, alpha=0.7,
                    label="SPARC: k = 4.00×(M/10¹⁰)^(-0.49)")

        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('M_bary (M☉)', fontsize=12)
        ax1.set_ylabel('k optimal', fontsize=12)
        ax1.set_title(f'k(M) Calibration - WALLABY DR2 (n={len(plot_results)})', fontsize=14)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. r_c vs M_bary
        ax2 = axes[0, 1]
        ax2.scatter(M_plot, rc_plot, alpha=0.3, s=10, c='blue')

        if 'error' not in rc_calib:
            M_range = np.logspace(7, 12, 100)
            rc_model = rc_calib['A'] * (M_range / 1e10) ** rc_calib['alpha']
            ax2.plot(M_range, rc_model, 'r-', lw=2,
                    label=f"WALLABY: r_c = {rc_calib['A']:.2f}×(M/10¹⁰)^{rc_calib['alpha']:.2f}")

            # SPARC for comparison
            rc_sparc = 2.6 * (M_range / 1e10) ** 0.56
            ax2.plot(M_range, rc_sparc, 'g--', lw=2, alpha=0.7,
                    label="SPARC: r_c = 2.6×(M/10¹⁰)^0.56")

        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('M_bary (M☉)', fontsize=12)
        ax2.set_ylabel('r_c (kpc)', fontsize=12)
        ax2.set_title('r_c(M) Calibration', fontsize=14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Improvement distribution
        ax3 = axes[1, 0]
        ax3.hist(impr_plot, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        ax3.axvline(0, color='k', linestyle='-', lw=1)
        ax3.axvline(np.median(impr_plot), color='r', linestyle='--', lw=2,
                   label=f'Median = {np.median(impr_plot):.1f}%')
        ax3.set_xlabel('χ² Improvement (%)', fontsize=12)
        ax3.set_ylabel('Number of galaxies', fontsize=12)
        ax3.set_title('TMT v2.4 Improvement Distribution', fontsize=14)
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. Improvement vs Mass
        ax4 = axes[1, 1]
        ax4.scatter(M_plot, impr_plot, alpha=0.3, s=10, c='blue')
        ax4.axhline(0, color='k', linestyle='-', lw=1)
        ax4.axhline(np.median(impr_plot), color='r', linestyle='--', lw=2,
                   label=f'Median = {np.median(impr_plot):.1f}%')
        ax4.set_xscale('log')
        ax4.set_xlabel('M_bary (M☉)', fontsize=12)
        ax4.set_ylabel('χ² Improvement (%)', fontsize=12)
        ax4.set_title('Improvement vs Baryonic Mass', fontsize=14)
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        fig_file = RESULTS_DIR / "TMT_WALLABY_DR2_calibration.png"
        plt.savefig(fig_file, dpi=150)
        print(f"Figure saved: {fig_file}")
        plt.close()

    except ImportError:
        print("matplotlib not available - no plot generated")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()

    if 'error' not in k_calib:
        print(f"k(M) = {k_calib['a']:.3f} × (M/10^10)^{k_calib['b']:.3f}")
        print(f"R² = {k_calib['R2']:.3f} (SPARC: 0.64)")
        print(f"Galaxies: {k_calib['n_galaxies']} (SPARC: 172)")
        print()

        # Statistical significance
        improvement_factor = k_calib['n_galaxies'] / 172
        print(f"Statistical improvement: {improvement_factor:.1f}× more galaxies")

        if k_calib['R2'] > 0.64:
            print("[OK] R^2 IMPROVED compared to SPARC")
        else:
            print("[!] R^2 lower than SPARC (may need data quality filtering)")

    return results, k_calib, rc_calib


if __name__ == "__main__":
    main()
