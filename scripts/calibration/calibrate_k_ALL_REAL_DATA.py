#!/usr/bin/env python3
"""
CALIBRATION k(M) SUR TOUTES LES DONNEES REELLES
================================================
- SPARC: 171 galaxies (VizieR)
- WALLABY PDR2: 236 galaxies (CASDA)

Total: ~407 galaxies réelles avec courbes de rotation
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

G_KPC = 4.302e-6  # kpc (km/s)^2 / M_sun

PROJECT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"


def r_c_from_mass(M_bary):
    """TMT v2.4: r_c(M) = 2.6 x (M/10^10)^0.56 kpc"""
    return 2.6 * (M_bary / 1e10) ** 0.56


def load_rotation_curves(filepath, source_name):
    """Load rotation curves from TMT format file."""
    rotation_curves = {}

    if not filepath.exists():
        return rotation_curves

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            parts = line.split()
            if len(parts) < 5:
                continue

            try:
                name = parts[0]
                D = float(parts[1])
                R = float(parts[2])
                Vobs = float(parts[3])
                e_Vobs = float(parts[4])
                Vgas = float(parts[5]) if len(parts) > 5 else 0
                Vdisk = float(parts[6]) if len(parts) > 6 else 0
                Vbul = float(parts[7]) if len(parts) > 7 else 0

                full_name = f"{source_name}_{name}"

                if full_name not in rotation_curves:
                    rotation_curves[full_name] = {
                        'R': [], 'Vobs': [], 'e_Vobs': [],
                        'Vgas': [], 'Vdisk': [], 'Vbul': [],
                        'distance': D, 'source': source_name
                    }

                rotation_curves[full_name]['R'].append(R)
                rotation_curves[full_name]['Vobs'].append(Vobs)
                rotation_curves[full_name]['e_Vobs'].append(max(e_Vobs, 1.0))
                rotation_curves[full_name]['Vgas'].append(Vgas)
                rotation_curves[full_name]['Vdisk'].append(Vdisk)
                rotation_curves[full_name]['Vbul'].append(Vbul)

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


def V_TMT(R, V_bary, k, r_c):
    """TMT velocity model using V_bary directly."""
    # For WALLABY data without decomposition, use V_obs as proxy for V_bary
    # and fit the dark matter contribution
    multiplier = 1.0 + k * (R / r_c)
    return V_bary * np.sqrt(multiplier)


def chi2_reduced(V_model, V_obs, e_V, n_params=1):
    """Reduced chi-squared."""
    residuals = (V_model - V_obs) / e_V
    chi2 = np.sum(residuals**2)
    dof = len(V_obs) - n_params
    return chi2 / max(dof, 1)


def estimate_M_bary(R, Vobs, has_decomposition, Vgas=None, Vdisk=None, Vbul=None):
    """Estimate baryonic mass from rotation curve."""
    if has_decomposition and Vgas is not None:
        # Use decomposition
        V_bary = compute_V_bary(Vgas, Vdisk, Vbul)
        M_bary = V_bary[-1]**2 * R[-1] / G_KPC if len(R) > 0 else 0
    else:
        # Estimate from Vobs - assume ~50% is baryonic at outer radius
        V_bary_est = Vobs * 0.5
        M_bary = V_bary_est[-1]**2 * R[-1] / G_KPC if len(R) > 0 else 0

    return max(M_bary, 1e6)


def analyze_galaxy(name, rc):
    """Analyze a single galaxy."""
    R = rc['R']
    Vobs = rc['Vobs']
    e_Vobs = rc['e_Vobs']
    source = rc.get('source', 'unknown')

    if len(R) < 3:
        return None

    # Check if we have decomposition
    has_decomposition = np.any(rc['Vdisk'] > 0) or np.any(rc['Vgas'] > 0)

    if has_decomposition:
        V_bary = compute_V_bary(rc['Vgas'], rc['Vdisk'], rc['Vbul'])
    else:
        # For WALLABY without decomposition, estimate V_bary
        V_bary = Vobs * 0.4  # Typical baryonic fraction

    M_bary = estimate_M_bary(R, Vobs, has_decomposition, rc['Vgas'], rc['Vdisk'], rc['Vbul'])

    if M_bary < 1e6:
        return None

    # Chi2 Newton (baryons only)
    chi2_newton = chi2_reduced(V_bary, Vobs, e_Vobs, n_params=0)

    # TMT with mass-dependent r_c
    r_c_mass = r_c_from_mass(M_bary)

    # Optimize k
    def objective_k(k):
        if k < 0:
            return 1e10
        V_model = V_TMT(R, V_bary, k, r_c_mass)
        return chi2_reduced(V_model, Vobs, e_Vobs)

    result = minimize_scalar(objective_k, bounds=(0.001, 100), method='bounded')
    k_opt, chi2_k = result.x, result.fun

    # Optimize both k and r_c
    def objective_both(params):
        k, r_c = params
        if k <= 0 or r_c <= 0:
            return 1e10
        V_model = V_TMT(R, V_bary, k, r_c)
        return chi2_reduced(V_model, Vobs, e_Vobs, n_params=2)

    best_chi2 = np.inf
    best_params = (1.0, 5.0)

    for k_init in [0.1, 0.5, 1, 2, 5, 10]:
        for rc_init in [1, 2, 5, 10, 20]:
            try:
                res = minimize(objective_both, [k_init, rc_init],
                             bounds=[(0.001, 100), (0.1, 100)],
                             method='L-BFGS-B')
                if res.fun < best_chi2:
                    best_chi2 = res.fun
                    best_params = res.x
            except:
                continue

    k_free, r_c_free = best_params

    improvement = (chi2_newton - chi2_k) / chi2_newton * 100 if chi2_newton > 0 else 0

    return {
        'name': name,
        'source': source,
        'M_bary': M_bary,
        'n_points': len(R),
        'R_max': R[-1],
        'V_max': np.max(Vobs),
        'chi2_newton': chi2_newton,
        'k_opt': k_opt,
        'chi2_k': chi2_k,
        'r_c_mass': r_c_mass,
        'improvement': improvement,
        'k_free': k_free,
        'r_c_free': r_c_free,
        'has_decomposition': has_decomposition
    }


def main():
    print("=" * 70)
    print("CALIBRATION k(M) - TOUTES DONNEES REELLES")
    print("=" * 70)
    print()

    # Load all real data
    all_curves = {}

    # SPARC
    sparc_file = DATA_DIR / "SPARC" / "SPARC_VizieR_rotation_curves.txt"
    if sparc_file.exists():
        sparc_curves = load_rotation_curves(sparc_file, "SPARC")
        all_curves.update(sparc_curves)
        print(f"SPARC: {len(sparc_curves)} galaxies")

    # WALLABY
    wallaby_file = DATA_DIR / "WALLABY_DR2" / "WALLABY_PDR2_rotation_curves_fixed.txt"
    if wallaby_file.exists():
        wallaby_curves = load_rotation_curves(wallaby_file, "WALLABY")
        all_curves.update(wallaby_curves)
        print(f"WALLABY: {len(wallaby_curves)} galaxies")

    print(f"\nTOTAL: {len(all_curves)} galaxies")

    # Analyze all
    print("\nAnalyzing galaxies...")
    results = []
    for name, rc in all_curves.items():
        result = analyze_galaxy(name, rc)
        if result is not None:
            results.append(result)

    print(f"Valid results: {len(results)} galaxies")

    # Statistics by source
    sparc_results = [r for r in results if r['source'] == 'SPARC']
    wallaby_results = [r for r in results if r['source'] == 'WALLABY']

    print(f"  SPARC: {len(sparc_results)}")
    print(f"  WALLABY: {len(wallaby_results)}")

    # Performance
    print("\n" + "=" * 50)
    print("PERFORMANCE")
    print("=" * 50)

    improvements = [r['improvement'] for r in results]
    n_improved = sum(1 for i in improvements if i > 0)

    print(f"\nTMT v2.4 Performance:")
    print(f"  Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)")
    print(f"  Median improvement: {np.median(improvements):.1f}%")
    print(f"  Mean improvement: {np.mean(improvements):.1f}%")

    # By source
    print(f"\n  SPARC median: {np.median([r['improvement'] for r in sparc_results]):.1f}%")
    print(f"  WALLABY median: {np.median([r['improvement'] for r in wallaby_results]):.1f}%")

    # k(M) calibration
    print("\n" + "=" * 50)
    print("k(M) CALIBRATION")
    print("=" * 50)

    valid_k = [r for r in results if r['M_bary'] > 1e7 and 0.01 < r['k_opt'] < 100]

    M_array = np.array([r['M_bary'] for r in valid_k])
    k_array = np.array([r['k_opt'] for r in valid_k])

    log_M = np.log10(M_array / 1e10)
    log_k = np.log10(k_array)
    mask = np.isfinite(log_M) & np.isfinite(log_k)

    slope, intercept, r_value, p_value, _ = stats.linregress(log_M[mask], log_k[mask])

    a_k = 10 ** intercept
    b_k = slope
    R2_k = r_value ** 2

    print(f"\nk(M) = {a_k:.3f} x (M/10^10)^{b_k:.3f}")
    print(f"R^2 = {R2_k:.4f}")
    print(f"p-value = {p_value:.2e}")
    print(f"Galaxies: {np.sum(mask)}")

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

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / "TMT_ALL_REAL_DATA_calibration.txt"

    with open(output_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("TMT k(M) CALIBRATION - ALL REAL DATA\n")
        f.write("=" * 70 + "\n\n")

        f.write("DATA SOURCES:\n")
        f.write(f"  SPARC (VizieR): {len(sparc_results)} galaxies\n")
        f.write(f"  WALLABY PDR2 (CASDA): {len(wallaby_results)} galaxies\n")
        f.write(f"  TOTAL: {len(results)} galaxies\n\n")

        f.write("=" * 50 + "\n")
        f.write("PERFORMANCE\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Galaxies improved: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)\n")
        f.write(f"Median improvement: {np.median(improvements):.1f}%\n")
        f.write(f"Mean improvement: {np.mean(improvements):.1f}%\n\n")

        f.write("By source:\n")
        f.write(f"  SPARC median: {np.median([r['improvement'] for r in sparc_results]):.1f}%\n")
        f.write(f"  WALLABY median: {np.median([r['improvement'] for r in wallaby_results]):.1f}%\n\n")

        f.write("=" * 50 + "\n")
        f.write("k(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"k(M) = {a_k:.4f} x (M/10^10)^{b_k:.3f}\n")
        f.write(f"R^2 = {R2_k:.4f}\n")
        f.write(f"p-value = {p_value:.2e}\n")
        f.write(f"Galaxies: {np.sum(mask)}\n\n")

        f.write("=" * 50 + "\n")
        f.write("r_c(M) CALIBRATION\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"r_c(M) = {A_rc:.2f} x (M/10^10)^{alpha_rc:.2f} kpc\n")
        f.write(f"R^2 = {R2_rc:.4f}\n")

    print(f"\nResults saved: {output_file}")

    # Generate figure
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        # Colors by source
        colors = ['green' if r['source'] == 'SPARC' else 'blue' for r in valid_k]

        # k vs M
        ax1 = axes[0, 0]
        ax1.scatter(M_array, k_array, alpha=0.6, s=30, c=colors, edgecolors='k', linewidth=0.5)

        M_range = np.logspace(7, 12, 100)
        k_fit = a_k * (M_range / 1e10) ** b_k
        ax1.plot(M_range, k_fit, 'r-', lw=2.5, label=f'Fit: k = {a_k:.2f}(M/10^10)^{b_k:.2f}')
        ax1.plot([], [], 'go', label='SPARC', markersize=8)
        ax1.plot([], [], 'bo', label='WALLABY', markersize=8)

        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('M_bary (M_sun)', fontsize=12)
        ax1.set_ylabel('k optimal', fontsize=12)
        ax1.set_title(f'k(M) - ALL REAL DATA (n={len(valid_k)}), R^2={R2_k:.3f}', fontsize=14)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # r_c vs M
        ax2 = axes[0, 1]
        colors_rc = ['green' if r['source'] == 'SPARC' else 'blue' for r in valid_rc]
        ax2.scatter(M_rc, rc_array, alpha=0.6, s=30, c=colors_rc, edgecolors='k', linewidth=0.5)

        rc_fit = A_rc * (M_range / 1e10) ** alpha_rc
        ax2.plot(M_range, rc_fit, 'r-', lw=2.5, label=f'Fit: r_c = {A_rc:.2f}(M/10^10)^{alpha_rc:.2f}')

        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('M_bary (M_sun)', fontsize=12)
        ax2.set_ylabel('r_c (kpc)', fontsize=12)
        ax2.set_title(f'r_c(M) - ALL REAL DATA, R^2={R2_rc:.3f}', fontsize=14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Improvement by source
        ax3 = axes[1, 0]
        sparc_impr = [r['improvement'] for r in sparc_results]
        wallaby_impr = [r['improvement'] for r in wallaby_results]

        ax3.hist(sparc_impr, bins=30, alpha=0.6, label=f'SPARC (n={len(sparc_impr)})', color='green')
        ax3.hist(wallaby_impr, bins=30, alpha=0.6, label=f'WALLABY (n={len(wallaby_impr)})', color='blue')
        ax3.axvline(np.median(improvements), color='r', linestyle='--', lw=2,
                   label=f'Combined median = {np.median(improvements):.1f}%')
        ax3.set_xlabel('Improvement (%)', fontsize=12)
        ax3.set_ylabel('Count', fontsize=12)
        ax3.set_title('TMT v2.4 Improvement by Source', fontsize=14)
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Mass distribution
        ax4 = axes[1, 1]
        sparc_mass = [np.log10(r['M_bary']) for r in sparc_results]
        wallaby_mass = [np.log10(r['M_bary']) for r in wallaby_results]

        ax4.hist(sparc_mass, bins=25, alpha=0.6, label='SPARC', color='green')
        ax4.hist(wallaby_mass, bins=25, alpha=0.6, label='WALLABY', color='blue')
        ax4.set_xlabel('log10(M_bary / M_sun)', fontsize=12)
        ax4.set_ylabel('Count', fontsize=12)
        ax4.set_title('Mass Distribution by Source', fontsize=14)
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        fig_file = RESULTS_DIR / "TMT_ALL_REAL_DATA_calibration.png"
        plt.savefig(fig_file, dpi=150)
        print(f"Figure saved: {fig_file}")
        plt.close()

    except ImportError:
        print("matplotlib not available")

    # Final summary
    print("\n" + "=" * 70)
    print("CALIBRATION FINALE - DONNEES REELLES")
    print("=" * 70)
    print()
    print(f"SPARC: {len(sparc_results)} galaxies")
    print(f"WALLABY: {len(wallaby_results)} galaxies")
    print(f"TOTAL: {len(results)} galaxies")
    print()
    print(f"k(M) = {a_k:.3f} x (M/10^10)^{b_k:.3f}, R^2 = {R2_k:.4f}")
    print(f"r_c(M) = {A_rc:.2f} x (M/10^10)^{alpha_rc:.2f}, R^2 = {R2_rc:.4f}")
    print()
    print(f"Amelioration mediane: {np.median(improvements):.1f}%")
    print(f"Galaxies ameliorees: {n_improved}/{len(results)} ({100*n_improved/len(results):.1f}%)")

    return results


if __name__ == "__main__":
    main()
