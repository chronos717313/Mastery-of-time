#!/usr/bin/env python3
"""
Recalibrate k(M) for TMT v2.3
=============================
Improve the k(M) = a*(M/10^10)^b relation using SPARC data.

Current calibration: k = 3.97 * (M/10^10)^(-0.48), R^2 = 0.37

Goals:
1. Test different functional forms
2. Include gas fraction dependence
3. Improve R^2 correlation
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

RESULTS_DIR = Path(__file__).parent.parent / "data" / "results"


def load_sparc_k_data():
    """Load k(M) calibration data from SPARC results."""
    results_file = RESULTS_DIR / "TMT_v2_SPARC_reel_results.txt"

    if not results_file.exists():
        print(f"File not found: {results_file}")
        return None, None

    masses = []
    k_values = []

    with open(results_file, 'r') as f:
        lines = f.readlines()

    # Parse the table
    in_table = False
    for line in lines:
        if 'Galaxie' in line and 'M_bary' in line:
            in_table = True
            continue
        if in_table and '---' in line:
            continue
        if in_table and line.strip():
            parts = line.split()
            if len(parts) >= 3:
                try:
                    # Parse mass (e.g., "3.64e+11")
                    mass_str = parts[1]
                    mass = float(mass_str)

                    # Parse k
                    k = float(parts[2])

                    if k > 0.001 and k < 1000:  # Filter outliers
                        masses.append(mass)
                        k_values.append(k)
                except:
                    continue

    return np.array(masses), np.array(k_values)


# Functional forms to test
def power_law(M, a, b):
    """k = a * (M/M0)^b"""
    M0 = 1e10
    return a * (M / M0) ** b


def power_law_with_floor(M, a, b, k_min):
    """k = a * (M/M0)^b + k_min"""
    M0 = 1e10
    return a * (M / M0) ** b + k_min


def broken_power_law(M, a1, b1, a2, b2, M_break):
    """Different slopes above/below M_break"""
    M0 = 1e10
    result = np.zeros_like(M)
    low = M < M_break
    high = ~low
    result[low] = a1 * (M[low] / M0) ** b1
    result[high] = a2 * (M[high] / M0) ** b2
    # Ensure continuity at M_break
    ratio = (a1 * (M_break / M0) ** b1) / (a2 * (M_break / M0) ** b2)
    result[high] *= ratio
    return result


def log_linear(M, a, b):
    """k = a + b * log10(M/M0)"""
    M0 = 1e10
    return a + b * np.log10(M / M0)


def exponential_decay(M, a, b, c):
    """k = a * exp(-b * M/M0) + c"""
    M0 = 1e10
    return a * np.exp(-b * M / M0) + c


def main():
    print("=" * 70)
    print("TMT v2.3 - Recalibration of k(M)")
    print("=" * 70)
    print()

    # Load data
    masses, k_values = load_sparc_k_data()
    if masses is None:
        return

    print(f"Data loaded: {len(masses)} galaxies")
    print(f"Mass range: {masses.min():.2e} - {masses.max():.2e} M_sun")
    print(f"k range: {k_values.min():.3f} - {k_values.max():.3f}")
    print()

    # Log transform for fitting
    log_M = np.log10(masses / 1e10)
    log_k = np.log10(k_values)

    results = {}

    # 1. Simple power law (current)
    print("-" * 50)
    print("Model 1: Power Law  k = a * (M/10^10)^b")
    print("-" * 50)
    try:
        popt, pcov = curve_fit(power_law, masses, k_values,
                               p0=[4, -0.5], maxfev=10000)
        a, b = popt
        k_pred = power_law(masses, a, b)
        r2 = 1 - np.sum((k_values - k_pred)**2) / np.sum((k_values - np.mean(k_values))**2)

        print(f"  a = {a:.4f}")
        print(f"  b = {b:.4f}")
        print(f"  R^2 = {r2:.4f}")

        results['power_law'] = {'a': a, 'b': b, 'R2': r2}
    except Exception as e:
        print(f"  Failed: {e}")

    # 2. Log-linear (equivalent to power law in log-log space)
    print()
    print("-" * 50)
    print("Model 2: Log-linear  log(k) = A + B*log(M/10^10)")
    print("-" * 50)
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_M, log_k)
    a_log = 10**intercept
    b_log = slope
    r2_log = r_value**2

    print(f"  A (intercept) = {intercept:.4f} -> a = {a_log:.4f}")
    print(f"  B (slope) = {b_log:.4f}")
    print(f"  R^2 = {r2_log:.4f}")
    print(f"  Equivalent: k = {a_log:.4f} * (M/10^10)^{b_log:.4f}")

    results['log_linear'] = {'a': a_log, 'b': b_log, 'R2': r2_log}

    # 3. Power law with floor
    print()
    print("-" * 50)
    print("Model 3: Power Law + Floor  k = a*(M/10^10)^b + k_min")
    print("-" * 50)
    try:
        popt, pcov = curve_fit(power_law_with_floor, masses, k_values,
                               p0=[4, -0.5, 0.5], maxfev=10000,
                               bounds=([0, -3, 0], [100, 0, 10]))
        a, b, k_min = popt
        k_pred = power_law_with_floor(masses, a, b, k_min)
        r2 = 1 - np.sum((k_values - k_pred)**2) / np.sum((k_values - np.mean(k_values))**2)

        print(f"  a = {a:.4f}")
        print(f"  b = {b:.4f}")
        print(f"  k_min = {k_min:.4f}")
        print(f"  R^2 = {r2:.4f}")

        results['power_law_floor'] = {'a': a, 'b': b, 'k_min': k_min, 'R2': r2}
    except Exception as e:
        print(f"  Failed: {e}")

    # 4. Separate calibration for dwarf vs massive
    print()
    print("-" * 50)
    print("Model 4: Split calibration (M < 10^10 vs M >= 10^10)")
    print("-" * 50)

    dwarf_mask = masses < 1e10
    massive_mask = ~dwarf_mask

    # Dwarf galaxies
    if np.sum(dwarf_mask) > 5:
        log_M_d = np.log10(masses[dwarf_mask] / 1e10)
        log_k_d = np.log10(k_values[dwarf_mask])
        slope_d, intercept_d, r_d, _, _ = stats.linregress(log_M_d, log_k_d)
        a_d = 10**intercept_d
        r2_d = r_d**2
        print(f"  Dwarf (N={np.sum(dwarf_mask)}):")
        print(f"    k = {a_d:.3f} * (M/10^10)^{slope_d:.3f}, R^2 = {r2_d:.3f}")

    # Massive galaxies
    if np.sum(massive_mask) > 5:
        log_M_m = np.log10(masses[massive_mask] / 1e10)
        log_k_m = np.log10(k_values[massive_mask])
        slope_m, intercept_m, r_m, _, _ = stats.linregress(log_M_m, log_k_m)
        a_m = 10**intercept_m
        r2_m = r_m**2
        print(f"  Massive (N={np.sum(massive_mask)}):")
        print(f"    k = {a_m:.3f} * (M/10^10)^{slope_m:.3f}, R^2 = {r2_m:.3f}")

        results['split'] = {
            'dwarf': {'a': a_d, 'b': slope_d, 'R2': r2_d, 'N': int(np.sum(dwarf_mask))},
            'massive': {'a': a_m, 'b': slope_m, 'R2': r2_m, 'N': int(np.sum(massive_mask))}
        }

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY - Best Calibrations")
    print("=" * 70)
    print()

    best_model = max(results.items(), key=lambda x: x[1].get('R2', 0) if 'R2' in x[1] else 0)
    print(f"Best single model: {best_model[0]}")
    print(f"  Parameters: {best_model[1]}")
    print()

    # Recommended calibration
    print("RECOMMENDED CALIBRATION for TMT v2.3:")
    print("-" * 50)

    if 'split' in results:
        print("Use split calibration:")
        print(f"  For M < 10^10 M_sun:")
        print(f"    k = {results['split']['dwarf']['a']:.3f} * (M/10^10)^{results['split']['dwarf']['b']:.3f}")
        print(f"    R^2 = {results['split']['dwarf']['R2']:.3f}")
        print()
        print(f"  For M >= 10^10 M_sun:")
        print(f"    k = {results['split']['massive']['a']:.3f} * (M/10^10)^{results['split']['massive']['b']:.3f}")
        print(f"    R^2 = {results['split']['massive']['R2']:.3f}")
    else:
        rec = results.get('log_linear', results.get('power_law'))
        print(f"  k = {rec['a']:.4f} * (M/10^10)^{rec['b']:.4f}")
        print(f"  R^2 = {rec['R2']:.4f}")

    # Save results
    output_file = RESULTS_DIR / "k_recalibration_TMT_v23.txt"
    with open(output_file, 'w') as f:
        f.write("TMT v2.3 k(M) Recalibration Results\n")
        f.write("=" * 50 + "\n\n")
        for model, params in results.items():
            f.write(f"{model}:\n")
            for k, v in params.items():
                f.write(f"  {k}: {v}\n")
            f.write("\n")

    print()
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
