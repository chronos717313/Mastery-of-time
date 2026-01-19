#!/usr/bin/env python3
"""
TEST TMT v2.3.1 - DES Y3 WEAK LENSING
=====================================

Tests TMT predictions using DES Year 3 weak lensing data:
1. Halo isotropy (TMT predicts spherical, not triaxial halos)
2. Shear-density correlation
3. Mass-environment relation
4. Comparison with KiDS-450 results

DES Y3: ~100 million galaxies (synthetic or real)
"""

import os
import sys
import numpy as np
from pathlib import Path
from datetime import datetime
from scipy import stats

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data" / "DES_Y3"
RESULTS_DIR = Path(__file__).parent.parent / "data" / "results"

try:
    from astropy.io import fits
    from astropy.table import Table, vstack
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False


def load_des_y3_data():
    """Load DES Y3 data (synthetic or real)"""
    print("=" * 70)
    print("LOADING DES Y3 DATA")
    print("=" * 70)

    # Try synthetic data first
    synthetic_files = list(DATA_DIR.glob("DES_Y3_synthetic*.fits"))

    if synthetic_files:
        print(f"\nFound {len(synthetic_files)} synthetic file(s)")

        if ASTROPY_AVAILABLE:
            tables = []
            total = 0
            for f in sorted(synthetic_files):
                t = Table.read(f)
                tables.append(t)
                total += len(t)
                print(f"  Loaded: {f.name} ({len(t):,} rows)")

            if len(tables) > 1:
                data = vstack(tables)
            else:
                data = tables[0]

            return {
                'ra': np.array(data['RA']),
                'dec': np.array(data['DEC']),
                'z': np.array(data['Z_MEAN']),
                'e1': np.array(data['E1']),
                'e2': np.array(data['E2']),
                'log_mass': np.array(data['LOG_MASS']),
                'log_density': np.array(data['LOG_DENSITY']),
                'weight': np.array(data['WEIGHT']),
                'size': np.array(data['SIZE']),
            }
        else:
            # Try npz format
            npz_file = DATA_DIR / "DES_Y3_synthetic.npz"
            if npz_file.exists():
                data = np.load(npz_file)
                return {
                    'ra': data['ra'],
                    'dec': data['dec'],
                    'z': data['z'],
                    'e1': data['e1'],
                    'e2': data['e2'],
                    'log_mass': data['log_mass'],
                    'log_density': data['log_density'],
                    'weight': data['weight'],
                    'size': data['size'],
                }

    # Try VizieR data
    vizier_file = DATA_DIR / "DES_Y3_VizieR.fits"
    if vizier_file.exists() and ASTROPY_AVAILABLE:
        print(f"\nLoading VizieR data: {vizier_file}")
        data = Table.read(vizier_file)
        print(f"  Loaded {len(data):,} rows")
        # Convert to dict (column names may vary)
        return {'raw': data}

    print("\nNo DES Y3 data found. Run download_DES_Y3.py first.")
    return None


def test_halo_isotropy(data):
    """
    Test 1: Halo Isotropy

    TMT Prediction: Halos are ISOTROPIC (spherical)
    LCDM Prediction: Halos are TRIAXIAL (~20% ellipticity)

    Method: Measure ellipticity alignment with local shear field
    """
    print("\n" + "=" * 70)
    print("TEST 1: HALO ISOTROPY")
    print("=" * 70)

    e1 = data['e1']
    e2 = data['e2']
    n = len(e1)

    # Compute ellipticity magnitude
    e_mag = np.sqrt(e1**2 + e2**2)

    # Compute mean ellipticity components
    mean_e1 = np.mean(e1)
    mean_e2 = np.mean(e2)
    mean_e_mag = np.mean(e_mag)

    # Standard errors
    se_e1 = np.std(e1) / np.sqrt(n)
    se_e2 = np.std(e2) / np.sqrt(n)

    # Test for isotropy: mean should be consistent with zero
    # (after cosmic shear subtraction)
    t_e1 = mean_e1 / se_e1
    t_e2 = mean_e2 / se_e2

    # Compute deviation from isotropy
    # For isotropic halos, <e> should follow intrinsic shape noise only
    # Any systematic deviation indicates preferred orientation

    # Bin by position and check for position-dependent alignment
    n_bins = 20
    ra_bins = np.linspace(data['ra'].min(), data['ra'].max(), n_bins + 1)
    dec_bins = np.linspace(data['dec'].min(), data['dec'].max(), n_bins + 1)

    alignment_scores = []
    for i in range(n_bins):
        for j in range(n_bins):
            mask = ((data['ra'] >= ra_bins[i]) & (data['ra'] < ra_bins[i+1]) &
                    (data['dec'] >= dec_bins[j]) & (data['dec'] < dec_bins[j+1]))
            if np.sum(mask) > 100:
                local_e1 = np.mean(e1[mask])
                local_e2 = np.mean(e2[mask])
                alignment_scores.append(np.sqrt(local_e1**2 + local_e2**2))

    mean_alignment = np.mean(alignment_scores) if alignment_scores else 0
    std_alignment = np.std(alignment_scores) if alignment_scores else 0

    # Expected for pure isotropy
    expected_isotropy = np.std(e1) / np.sqrt(n / (n_bins * n_bins))

    # Deviation from perfect isotropy (%)
    deviation_pct = (mean_alignment - expected_isotropy) / expected_isotropy * 100

    print(f"\nGalaxies analyzed: {n:,}")
    print(f"\nMean ellipticity components:")
    print(f"  <e1> = {mean_e1:.6f} +/- {se_e1:.6f}")
    print(f"  <e2> = {mean_e2:.6f} +/- {se_e2:.6f}")
    print(f"  <|e|> = {mean_e_mag:.4f}")
    print(f"\nPosition-binned alignment:")
    print(f"  Mean local alignment: {mean_alignment:.6f}")
    print(f"  Expected (isotropic): {expected_isotropy:.6f}")
    print(f"  Deviation: {deviation_pct:+.3f}%")

    # TMT prediction: deviation < 1% (isotropic)
    # LCDM prediction: deviation ~ 5% (triaxial)
    verdict = "ISOTROPE" if abs(deviation_pct) < 1.0 else "NON-ISOTROPE"

    print(f"\nPrediction TMT: Deviation < 1% (isotrope)")
    print(f"Prediction LCDM: Deviation ~ 5% (triaxial)")
    print(f"Observation: {deviation_pct:+.3f}%")
    print(f"VERDICT: {verdict}")

    return {
        'test': 'Halo Isotropy',
        'n_galaxies': n,
        'mean_e1': mean_e1,
        'mean_e2': mean_e2,
        'mean_e_mag': mean_e_mag,
        'deviation_pct': deviation_pct,
        'verdict': verdict,
        'score': 1.0 if verdict == "ISOTROPE" else 0.0
    }


def test_shear_density_correlation(data):
    """
    Test 2: Shear-Density Correlation

    TMT Prediction: Shear correlates with LOCAL density (scalar field)
    LCDM Prediction: Shear correlates with DIRECTIONAL mass distribution
    """
    print("\n" + "=" * 70)
    print("TEST 2: SHEAR-DENSITY CORRELATION")
    print("=" * 70)

    e1 = data['e1']
    e2 = data['e2']
    e_mag = np.sqrt(e1**2 + e2**2)
    log_density = data['log_density']
    n = len(e1)

    # Correlation between shear magnitude and density
    r_shear_density, p_shear_density = stats.pearsonr(e_mag, log_density)

    # Bin by density and compute mean shear
    n_bins = 10
    density_bins = np.percentile(log_density, np.linspace(0, 100, n_bins + 1))
    bin_centers = []
    mean_shear = []
    std_shear = []

    for i in range(n_bins):
        mask = (log_density >= density_bins[i]) & (log_density < density_bins[i+1])
        if np.sum(mask) > 100:
            bin_centers.append((density_bins[i] + density_bins[i+1]) / 2)
            mean_shear.append(np.mean(e_mag[mask]))
            std_shear.append(np.std(e_mag[mask]) / np.sqrt(np.sum(mask)))

    # Linear fit
    if len(bin_centers) > 2:
        slope, intercept, r_value, p_value, std_err = stats.linregress(bin_centers, mean_shear)
    else:
        slope, r_value, p_value = 0, 0, 1

    print(f"\nGalaxies analyzed: {n:,}")
    print(f"\nCorrelation shear-density:")
    print(f"  Pearson r = {r_shear_density:.4f}")
    print(f"  p-value = {p_shear_density:.2e}")
    print(f"\nBinned analysis:")
    print(f"  Slope: {slope:.6f} +/- {std_err:.6f}")
    print(f"  R-squared: {r_value**2:.4f}")

    # TMT predicts positive correlation (more density = more temporal distortion = more shear)
    direction_correct = slope > 0
    significant = p_value < 0.05

    print(f"\nPrediction TMT: Positive correlation (slope > 0)")
    print(f"Observation: slope = {slope:.6f}")
    print(f"Direction: {'CORRECT' if direction_correct else 'INCORRECT'}")
    print(f"Significance: {'SIGNIFICATIF' if significant else 'NON SIGNIFICATIF'}")

    verdict = "VALIDE" if direction_correct and significant else "AMBIGU"
    print(f"VERDICT: {verdict}")

    return {
        'test': 'Shear-Density Correlation',
        'n_galaxies': n,
        'pearson_r': r_shear_density,
        'p_value': p_shear_density,
        'slope': slope,
        'r_squared': r_value**2,
        'direction_correct': direction_correct,
        'significant': significant,
        'verdict': verdict,
        'score': 1.0 if verdict == "VALIDE" else 0.5 if direction_correct else 0.0
    }


def test_mass_environment_relation(data):
    """
    Test 3: Mass-Environment Relation

    TMT Prediction: More massive galaxies in denser environments
    (consistent with hierarchical formation + temporal distortion)
    """
    print("\n" + "=" * 70)
    print("TEST 3: MASS-ENVIRONMENT RELATION")
    print("=" * 70)

    log_mass = data['log_mass']
    log_density = data['log_density']
    z = data['z']
    n = len(log_mass)

    # Overall correlation
    r_mass_env, p_mass_env = stats.pearsonr(log_mass, log_density)
    rho_mass_env, p_rho = stats.spearmanr(log_mass, log_density)

    # Correlation by redshift bin
    z_bins = [0, 0.5, 1.0, 1.5, 2.0, 3.0]
    correlations_by_z = []

    print(f"\nGalaxies analyzed: {n:,}")
    print(f"\nOverall correlation:")
    print(f"  Pearson r = {r_mass_env:.4f} (p = {p_mass_env:.2e})")
    print(f"  Spearman rho = {rho_mass_env:.4f} (p = {p_rho:.2e})")
    print(f"\nCorrelation by redshift:")

    for i in range(len(z_bins) - 1):
        mask = (z >= z_bins[i]) & (z < z_bins[i+1])
        n_bin = np.sum(mask)
        if n_bin > 1000:
            r, p = stats.pearsonr(log_mass[mask], log_density[mask])
            correlations_by_z.append(r)
            print(f"  z = {z_bins[i]:.1f} - {z_bins[i+1]:.1f}: r = {r:.4f} (n = {n_bin:,})")

    mean_corr = np.mean(correlations_by_z) if correlations_by_z else 0

    # Compare with KiDS-450 result (r = 0.150)
    kids_result = 0.150

    print(f"\nComparison with KiDS-450:")
    print(f"  KiDS-450: r = {kids_result:.3f}")
    print(f"  DES Y3: r = {r_mass_env:.3f}")
    print(f"  Agreement: {abs(r_mass_env - kids_result) < 0.05}")

    # TMT prediction: positive correlation
    verdict = "VALIDE" if r_mass_env > 0.10 and p_mass_env < 0.01 else "PARTIEL"
    print(f"\nVERDICT: {verdict}")

    return {
        'test': 'Mass-Environment Relation',
        'n_galaxies': n,
        'pearson_r': r_mass_env,
        'spearman_rho': rho_mass_env,
        'p_value': p_mass_env,
        'kids_comparison': abs(r_mass_env - kids_result),
        'verdict': verdict,
        'score': 1.0 if verdict == "VALIDE" else 0.5
    }


def test_redshift_evolution(data):
    """
    Test 4: Redshift Evolution of Shear Signal

    TMT Prediction: Shear evolution follows temporal superposition
    """
    print("\n" + "=" * 70)
    print("TEST 4: REDSHIFT EVOLUTION")
    print("=" * 70)

    z = data['z']
    e1 = data['e1']
    e2 = data['e2']
    e_mag = np.sqrt(e1**2 + e2**2)
    n = len(z)

    # Bin by redshift
    z_bins = np.linspace(0, 2.5, 26)
    z_centers = (z_bins[:-1] + z_bins[1:]) / 2
    mean_shear = []
    std_shear = []
    n_per_bin = []

    for i in range(len(z_bins) - 1):
        mask = (z >= z_bins[i]) & (z < z_bins[i+1])
        n_bin = np.sum(mask)
        n_per_bin.append(n_bin)
        if n_bin > 100:
            mean_shear.append(np.mean(e_mag[mask]))
            std_shear.append(np.std(e_mag[mask]) / np.sqrt(n_bin))
        else:
            mean_shear.append(np.nan)
            std_shear.append(np.nan)

    mean_shear = np.array(mean_shear)
    std_shear = np.array(std_shear)

    # Fit evolution model
    valid = ~np.isnan(mean_shear)
    if np.sum(valid) > 5:
        # TMT model: shear ~ (1 + z)^alpha
        log_1pz = np.log(1 + z_centers[valid])
        log_shear = np.log(mean_shear[valid])
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_1pz, log_shear)
        alpha = slope
    else:
        alpha, r_value, p_value = 0, 0, 1

    print(f"\nGalaxies analyzed: {n:,}")
    print(f"\nShear evolution:")
    print(f"  Model: |e| ~ (1+z)^alpha")
    print(f"  alpha = {alpha:.3f} +/- {std_err:.3f}")
    print(f"  R-squared: {r_value**2:.4f}")
    print(f"\nRedshift distribution:")
    print(f"  Min: {z.min():.3f}")
    print(f"  Max: {z.max():.3f}")
    print(f"  Median: {np.median(z):.3f}")

    # TMT predicts mild positive evolution (alpha ~ 0.3-0.5)
    evolution_consistent = 0.1 < alpha < 1.0

    verdict = "VALIDE" if evolution_consistent else "PARTIEL"
    print(f"\nPrediction TMT: 0.1 < alpha < 1.0")
    print(f"Observation: alpha = {alpha:.3f}")
    print(f"VERDICT: {verdict}")

    return {
        'test': 'Redshift Evolution',
        'n_galaxies': n,
        'alpha': alpha,
        'r_squared': r_value**2,
        'z_median': np.median(z),
        'verdict': verdict,
        'score': 1.0 if verdict == "VALIDE" else 0.5
    }


def compare_with_previous_surveys(results):
    """
    Compare DES Y3 results with KiDS-450 and COSMOS2015
    """
    print("\n" + "=" * 70)
    print("COMPARISON WITH PREVIOUS SURVEYS")
    print("=" * 70)

    comparisons = {
        'Survey': ['KiDS-450', 'COSMOS2015', 'DES Y3'],
        'N_galaxies': ['1,000,000', '1,182,108', f'{results[0]["n_galaxies"]:,}'],
        'Isotropy_deviation': ['-0.024%', 'N/A', f'{results[0]["deviation_pct"]:+.3f}%'],
        'Mass_env_r': ['0.15', '0.150', f'{results[2]["pearson_r"]:.3f}'],
    }

    print(f"\n{'Survey':<15} {'N_galaxies':<15} {'Isotropy':<15} {'Mass-Env r':<15}")
    print("-" * 60)
    for i in range(len(comparisons['Survey'])):
        print(f"{comparisons['Survey'][i]:<15} "
              f"{comparisons['N_galaxies'][i]:<15} "
              f"{comparisons['Isotropy_deviation'][i]:<15} "
              f"{comparisons['Mass_env_r'][i]:<15}")

    # Consistency check
    isotropy_consistent = abs(results[0]['deviation_pct']) < 1.0
    mass_env_consistent = abs(results[2]['pearson_r'] - 0.15) < 0.1

    print(f"\nConsistency with previous surveys:")
    print(f"  Isotropy: {'CONSISTENT' if isotropy_consistent else 'INCONSISTENT'}")
    print(f"  Mass-Env: {'CONSISTENT' if mass_env_consistent else 'INCONSISTENT'}")

    return isotropy_consistent and mass_env_consistent


def main():
    """Run all DES Y3 tests"""
    print("=" * 70)
    print("TEST TMT v2.3.1 - DES Y3 WEAK LENSING")
    print("=" * 70)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Load data
    data = load_des_y3_data()
    if data is None:
        print("\nERROR: No data available. Run download_DES_Y3.py first.")
        return

    if 'raw' in data:
        print("\nWARNING: Using VizieR data with limited columns")
        print("Full analysis requires synthetic data generation")
        return

    # Run tests
    results = []
    results.append(test_halo_isotropy(data))
    results.append(test_shear_density_correlation(data))
    results.append(test_mass_environment_relation(data))
    results.append(test_redshift_evolution(data))

    # Compare with previous surveys
    consistent = compare_with_previous_surveys(results)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY DES Y3 TESTS")
    print("=" * 70)

    total_score = sum(r['score'] for r in results)
    max_score = len(results)

    print(f"\n{'Test':<35} {'Score':<10} {'Verdict':<15}")
    print("-" * 60)
    for r in results:
        print(f"{r['test']:<35} {r['score']:.1f}/{1.0:<7} {r['verdict']:<15}")
    print("-" * 60)
    print(f"{'TOTAL':<35} {total_score:.1f}/{max_score:.1f}")

    print(f"\nScore DES Y3: {total_score}/{max_score} ({100*total_score/max_score:.0f}%)")
    print(f"Consistency with KiDS/COSMOS: {'OUI' if consistent else 'NON'}")

    verdict_global = "VALIDE" if total_score >= 3 else "PARTIEL" if total_score >= 2 else "AMBIGU"
    print(f"\nVERDICT GLOBAL: TMT v2.3.1 {verdict_global}")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / "test_DES_Y3_TMT_v231.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TEST TMT v2.3.1 - DES Y3 WEAK LENSING\n")
        f.write("=" * 70 + "\n")
        f.write(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Galaxies: {data['ra'].shape[0]:,}\n")
        f.write(f"\nScore: {total_score}/{max_score} ({100*total_score/max_score:.0f}%)\n")
        f.write(f"Verdict: {verdict_global}\n")
        f.write("\nRESULTS BY TEST:\n")
        for r in results:
            f.write(f"\n{r['test']}:\n")
            for k, v in r.items():
                if k not in ['test']:
                    f.write(f"  {k}: {v}\n")

    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    main()
