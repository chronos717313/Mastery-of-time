#!/usr/bin/env python3
"""
Calibrate k(M) on REAL SPARC Data from VizieR
=============================================
Uses actual rotation curves from Lelli, McGaugh & Schombert (2016).

This is the definitive calibration using 171 real galaxies.
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Constants
G_KPC = 4.302e-6  # kpc (km/s)^2 / M_sun

PROJECT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"


def r_c_from_mass(M_bary):
    """TMT v2.4: r_c(M) = 2.6 x (M/10^10)^0.56 kpc"""
    return 2.6 * (M_bary / 1e10) ** 0.56


def load_rotation_curves(filepath):
    """Load rotation curves from TMT format file."""
    rotation_curves = {}

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


def V_TMT(R, M_bary_enc, k, r_c):
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


def analyze_galaxy(name, rc):
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

    # Chi2 Newton (baryons only)
    chi2_newton = chi2_reduced(V_bary, Vobs, e_Vobs, n_params=0)

    # TMT with mass-dependent r_c
    r_c_mass = r_c_from_mass(M_bary_total)

    # Optimize k
    def objective_k(k):
        if k < 0:
            return 1e10
        V_model = V_TMT(R, M_bary_enc, k, r_c_mass)
        return chi2_reduced(V_model, Vobs, e_Vobs)

    result_k = minimize_scalar(objective_k, bounds=(0.001, 100), method='bounded')
    k_opt, chi2_k = result_k.x, result_k.fun

    # Optimize both k and r_c
    def objective_both(params):
        k, r_c = params
        if k <= 0 or r_c <= 0:
            return 1e10
        V_model = V_TMT(R, M_bary_enc, k, r_c)
        return chi2_reduced(V_model, Vobs, e_Vobs, n_params=2)

    best_chi2 = np.inf
    best_params = (1.0, 5.0)

    for k_init in [0.1, 0.5, 1, 2, 5, 10]:
        for rc_init in [1, 2, 5, 10, 20]:
            try:
                result = minimize(objective_both, [k_init, rc_init],
                                bounds=[(0.001, 100), (0.1, 100)],
                                method='L-BFGS-B')
                if result.fun < best_chi2:
                    best_chi2 = result.fun
                    best_params = result.x
            except:
                continue

    k_free, r_c_free = best_params

    improvement = (chi2_newton - chi2_k) / chi2_newton * 100 if chi2_newton > 0 else 0
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
        'improvement': improvement,
        'k_free': k_free,
        'r_c_free': r_c_free,
        'chi2_free': best_chi2,
        'baryonic_valid': baryonic_valid
    }


def main():
    print("=" * 70)
    print("TMT k(M) CALIBRATION ON REAL SPARC DATA")
    print("=" * 70)
    print()

    # Load real SPARC data
    sparc_file = DATA_DIR / "SPARC" / "SPARC_VizieR_rotation_curves.txt"

    if not sparc_file.exists():
        print(f"File not found: {sparc_file}")
        print("Run convert_vizier_to_tmt.py first")
        return

    print(f"Loading: {sparc_file}")
    rotation_curves = load_rotation_curves(sparc_file)
    print(f"Loaded: {len(rotation_curves)} galaxies")

    # Analyze all galaxies
    print("\nAnalyzing galaxies...")
    results = []
    for name, rc in rotation_curves.items():
        result = analyze_galaxy(name, rc)
        if result is not None:
            results.append(result)

    print(f"Valid results: {len(results)} galaxies")

    # Performance statistics
    print("\n" + "=" * 50)
    print("PERFORMANCE STATISTICS")
    print("=" * 50)

    improvements = [r['improvement'] for r in results]
    n_improved = sum(1 for i in improvements if i > 0)
    n_baryonic = sum(1 for r in results if r['baryonic_valid'])

    print(f"\nTMT v2.4 Performance:")
    print(f"  Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)")
    print(f"  Baryonic-dominated: {n_baryonic}/{len(results)} ({100*n_baryonic/len(results):.1f}%)")
    print(f"  Median improvement: {np.median(improvements):.1f}%")
    print(f"  Mean improvement: {np.mean(improvements):.1f}%")

    # k(M) calibration
    print("\n" + "=" * 50)
    print("k(M) CALIBRATION")
    print("=" * 50)

    valid_k = [r for r in results if not r['baryonic_valid']
               and r['M_bary'] > 1e7 and 0.01 < r['k_opt'] < 100]

    M_array = np.array([r['M_bary'] for r in valid_k])
    k_array = np.array([r['k_opt'] for r in valid_k])

    log_M = np.log10(M_array / 1e10)
    log_k = np.log10(k_array)
    mask = np.isfinite(log_M) & np.isfinite(log_k)

    slope, intercept, r_value, p_value, std_err = stats.linregress(log_M[mask], log_k[mask])

    a_k = 10 ** intercept
    b_k = slope
    R2_k = r_value ** 2

    print(f"\nk(M) = {a_k:.3f} x (M/10^10)^{b_k:.3f}")
    print(f"R^2 = {R2_k:.4f}")
    print(f"p-value = {p_value:.2e}")
    print(f"Galaxies used: {np.sum(mask)}")
    print(f"Mass range: {M_array.min():.2e} - {M_array.max():.2e} M_sun")

    # r_c(M) calibration
    print("\n" + "=" * 50)
    print("r_c(M) CALIBRATION")
    print("=" * 50)

    valid_rc = [r for r in results if r['M_bary'] > 1e7 and 0.1 < r['r_c_free'] < 100]

    M_rc = np.array([r['M_bary'] for r in valid_rc])
    rc_array = np.array([r['r_c_free'] for r in valid_rc])

    log_M_rc = np.log10(M_rc / 1e10)
    log_rc = np.log10(rc_array)
    mask_rc = np.isfinite(log_M_rc) & np.isfinite(log_rc)

    slope_rc, intercept_rc, r_rc, p_rc, _ = stats.linregress(log_M_rc[mask_rc], log_rc[mask_rc])

    A_rc = 10 ** intercept_rc
    alpha_rc = slope_rc
    R2_rc = r_rc ** 2

    print(f"\nr_c(M) = {A_rc:.2f} x (M/10^10)^{alpha_rc:.2f} kpc")
    print(f"R^2 = {R2_rc:.4f}")
    print(f"Galaxies used: {np.sum(mask_rc)}")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / "TMT_REAL_SPARC_calibration.txt"

    with open(output_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("TMT k(M) CALIBRATION ON REAL SPARC DATA\n")
        f.write("=" * 70 + "\n\n")

        f.write("Data source: SPARC VizieR (J/AJ/152/157)\n")
        f.write("Reference: Lelli, McGaugh & Schombert (2016), AJ, 152, 157\n\n")

        f.write(f"Total galaxies: {len(rotation_curves)}\n")
        f.write(f"Valid galaxies: {len(results)}\n\n")

        f.write("=" * 50 + "\n")
        f.write("PERFORMANCE\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)\n")
        f.write(f"Baryonic-dominated: {n_baryonic}/{len(results)}\n")
        f.write(f"Median improvement: {np.median(improvements):.1f}%\n")
        f.write(f"Mean improvement: {np.mean(improvements):.1f}%\n\n")

        f.write("=" * 50 + "\n")
        f.write("k(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"k(M) = {a_k:.4f} x (M/10^10)^{b_k:.3f}\n")
        f.write(f"R^2 = {R2_k:.4f}\n")
        f.write(f"p-value = {p_value:.2e}\n")
        f.write(f"Galaxies: {np.sum(mask)}\n")
        f.write(f"Mass range: {M_array.min():.2e} - {M_array.max():.2e} M_sun\n\n")

        f.write("=" * 50 + "\n")
        f.write("r_c(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"r_c(M) = {A_rc:.2f} x (M/10^10)^{alpha_rc:.2f} kpc\n")
        f.write(f"R^2 = {R2_rc:.4f}\n")
        f.write(f"Galaxies: {np.sum(mask_rc)}\n\n")

        f.write("=" * 50 + "\n")
        f.write("DETAILED RESULTS\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"{'Galaxy':<15} {'M_bary':>12} {'k_opt':>8} {'r_c':>8} {'Improv':>8} {'Bary':>5}\n")
        f.write("-" * 60 + "\n")

        for r in sorted(results, key=lambda x: x['M_bary'], reverse=True):
            bary = "Yes" if r['baryonic_valid'] else "No"
            f.write(f"{r['name']:<15} {r['M_bary']:>12.2e} {r['k_opt']:>8.3f} "
                   f"{r['r_c_free']:>8.2f} {r['improvement']:>7.1f}% {bary:>5}\n")

    print(f"\nResults saved: {output_file}")

    # Generate figure
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        # k vs M
        ax1 = axes[0, 0]
        ax1.scatter(M_array, k_array, alpha=0.6, s=30, c='green', edgecolors='darkgreen', label='SPARC real')
        M_range = np.logspace(7, 12, 100)
        k_fit = a_k * (M_range / 1e10) ** b_k
        ax1.plot(M_range, k_fit, 'r-', lw=2.5, label=f'Fit: k = {a_k:.2f}(M/10^10)^{b_k:.2f}, R^2={R2_k:.3f}')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('M_bary (M_sun)', fontsize=12)
        ax1.set_ylabel('k optimal', fontsize=12)
        ax1.set_title(f'k(M) Calibration - REAL SPARC (n={len(valid_k)})', fontsize=14)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # r_c vs M
        ax2 = axes[0, 1]
        ax2.scatter(M_rc, rc_array, alpha=0.6, s=30, c='green', edgecolors='darkgreen', label='SPARC real')
        rc_fit = A_rc * (M_range / 1e10) ** alpha_rc
        ax2.plot(M_range, rc_fit, 'r-', lw=2.5, label=f'Fit: r_c = {A_rc:.2f}(M/10^10)^{alpha_rc:.2f}, R^2={R2_rc:.3f}')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('M_bary (M_sun)', fontsize=12)
        ax2.set_ylabel('r_c (kpc)', fontsize=12)
        ax2.set_title(f'r_c(M) Calibration - REAL SPARC', fontsize=14)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        # Improvement distribution
        ax3 = axes[1, 0]
        ax3.hist(improvements, bins=40, edgecolor='black', alpha=0.7, color='green')
        ax3.axvline(0, color='k', linestyle='-', lw=1)
        ax3.axvline(np.median(improvements), color='r', linestyle='--', lw=2,
                   label=f'Median = {np.median(improvements):.1f}%')
        ax3.set_xlabel('Chi^2 Improvement (%)', fontsize=12)
        ax3.set_ylabel('Number of galaxies', fontsize=12)
        ax3.set_title('TMT v2.4 Improvement Distribution', fontsize=14)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)

        # Mass distribution
        ax4 = axes[1, 1]
        all_masses = [r['M_bary'] for r in results]
        ax4.hist(np.log10(all_masses), bins=30, edgecolor='black', alpha=0.7, color='green')
        ax4.set_xlabel('log10(M_bary / M_sun)', fontsize=12)
        ax4.set_ylabel('Number of galaxies', fontsize=12)
        ax4.set_title('SPARC Mass Distribution', fontsize=14)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        fig_file = RESULTS_DIR / "TMT_REAL_SPARC_calibration.png"
        plt.savefig(fig_file, dpi=150)
        print(f"Figure saved: {fig_file}")
        plt.close()

    except ImportError:
        print("matplotlib not available")

    # Final summary
    print("\n" + "=" * 70)
    print("FINAL CALIBRATION RESULTS - REAL SPARC DATA")
    print("=" * 70)
    print()
    print(f"k(M) = {a_k:.3f} x (M/10^10)^{b_k:.3f}")
    print(f"       R^2 = {R2_k:.4f}, p = {p_value:.2e}")
    print()
    print(f"r_c(M) = {A_rc:.2f} x (M/10^10)^{alpha_rc:.2f} kpc")
    print(f"         R^2 = {R2_rc:.4f}")
    print()
    print(f"TMT v2.4 improvement: {np.median(improvements):.1f}% median")
    print(f"Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)")

    return results, (a_k, b_k, R2_k), (A_rc, alpha_rc, R2_rc)


if __name__ == "__main__":
    main()
