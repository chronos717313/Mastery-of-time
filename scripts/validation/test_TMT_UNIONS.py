#!/usr/bin/env python3
"""
Test TMT v2.3 with UNIONS Survey Data (15M+ galaxies)
=====================================================
Large-scale weak lensing test of TMT predictions.

Key tests:
1. Isotropic halo shapes (TMT v2.0 prediction)
2. Mass-shear correlation vs TMT temporal superposition
3. Large-scale structure alignment statistics

Survey: UNIONS (Ultraviolet Near Infrared Optical Northern Survey)
- 4800 deg², ~15 million galaxies
- r-band seeing ~0.65" (ideal for weak lensing)
- Photo-z precision adequate for tomographic analysis

References:
- CFHT/CFIS: https://www.cfht.hawaii.edu/Science/CFIS/
- UNIONS: https://www.skysurvey.cc/
"""

import numpy as np
from pathlib import Path
from scipy import stats
from scipy.spatial import cKDTree
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "UNIONS"
RESULTS_DIR = Path(__file__).parent.parent / "data" / "results"

# TMT v2.3 Parameters
R_C_COEFF = 2.6  # kpc
R_C_EXPONENT = 0.56
N_SUPERPOSITION = 0.75


def load_unions_data(filepath=None):
    """
    Load UNIONS galaxy catalog.

    Returns
    -------
    astropy.table.Table or dict
    """
    if filepath is None:
        # Look for downloaded data
        fits_files = list(DATA_DIR.glob("*.fits"))
        if fits_files:
            filepath = fits_files[0]
        else:
            print(f"No data found in {DATA_DIR}")
            print("Run download_UNIONS.py first or query via TAP.")
            return None

    try:
        from astropy.table import Table
        print(f"Loading: {filepath}")
        table = Table.read(filepath)
        print(f"Loaded {len(table)} galaxies")
        return table
    except ImportError:
        print("astropy required: pip install astropy")
        return None


def compute_ellipticity_stats(e1, e2):
    """
    Compute ellipticity statistics for weak lensing.

    Parameters
    ----------
    e1, e2 : array
        Ellipticity components

    Returns
    -------
    dict with statistics
    """
    e = np.sqrt(e1**2 + e2**2)
    theta = 0.5 * np.arctan2(e2, e1) * 180 / np.pi  # Position angle

    return {
        'e_mean': np.nanmean(e),
        'e_median': np.nanmedian(e),
        'e_std': np.nanstd(e),
        'theta_mean': np.nanmean(theta),
        'theta_std': np.nanstd(theta),
        'n_galaxies': np.sum(np.isfinite(e))
    }


def test_isotropy(ra, dec, e1, e2, n_neighbors=20):
    """
    Test TMT v2.0 prediction: halos are ISOTROPIC (not directional).

    ΛCDM with triaxial NFW halos predicts some alignment.
    TMT v2.0 predicts random orientations (scalar mass contribution).

    Parameters
    ----------
    ra, dec : array
        Galaxy positions (degrees)
    e1, e2 : array
        Ellipticity components
    n_neighbors : int
        Number of neighbors for correlation

    Returns
    -------
    dict with test results
    """
    print()
    print("=" * 60)
    print("TEST 1: Halo Isotropy (TMT v2.0 Key Prediction)")
    print("=" * 60)
    print()
    print("TMT v2.0 predicts: ISOTROPIC halos (random orientations)")
    print("ΛCDM (triaxial NFW): Some directional alignment expected")
    print()

    # Build KD-tree for neighbor search
    coords = np.column_stack([ra, dec])
    tree = cKDTree(coords)

    # Compute alignment with neighbors
    n_sample = min(50000, len(ra))  # Sample for speed
    idx = np.random.choice(len(ra), n_sample, replace=False)

    alignments = []
    for i in idx:
        if not np.isfinite(e1[i]) or not np.isfinite(e2[i]):
            continue

        # Find neighbors
        distances, neighbors = tree.query(coords[i], k=n_neighbors + 1)
        neighbors = neighbors[1:]  # Exclude self

        # Galaxy orientation
        theta_i = 0.5 * np.arctan2(e2[i], e1[i])

        # Direction to neighbors
        for j in neighbors:
            if not np.isfinite(e1[j]) or not np.isfinite(e2[j]):
                continue

            # Angle to neighbor
            dra = ra[j] - ra[i]
            ddec = dec[j] - dec[i]
            theta_neighbor = np.arctan2(ddec, dra)

            # Alignment: |cos(2 * (theta_galaxy - theta_to_neighbor))|
            delta_theta = theta_i - theta_neighbor
            alignment = np.abs(np.cos(2 * delta_theta))
            alignments.append(alignment)

    alignments = np.array(alignments)

    # Random expectation: mean |cos(2θ)| = 2/π ≈ 0.637
    random_expectation = 2 / np.pi

    mean_alignment = np.mean(alignments)
    std_alignment = np.std(alignments) / np.sqrt(len(alignments))

    # Statistical test
    t_stat = (mean_alignment - random_expectation) / std_alignment
    p_value = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))

    print(f"Results ({len(alignments)} pairs analyzed):")
    print(f"  Mean alignment: {mean_alignment:.4f} ± {std_alignment:.4f}")
    print(f"  Random expectation: {random_expectation:.4f}")
    print(f"  Deviation: {(mean_alignment - random_expectation) / random_expectation * 100:.2f}%")
    print(f"  t-statistic: {t_stat:.2f}")
    print(f"  p-value: {p_value:.4f}")
    print()

    if np.abs(mean_alignment - random_expectation) < 0.02:
        verdict = "✓ ISOTROPIC - Consistent with TMT v2.0"
    elif mean_alignment > random_expectation + 0.02:
        verdict = "? ALIGNED - May favor ΛCDM triaxial halos"
    else:
        verdict = "? ANTI-ALIGNED - Unexpected"

    print(f"Verdict: {verdict}")

    return {
        'mean_alignment': mean_alignment,
        'std_alignment': std_alignment,
        'random_expectation': random_expectation,
        't_statistic': t_stat,
        'p_value': p_value,
        'n_pairs': len(alignments),
        'verdict': verdict
    }


def test_mass_shear_relation(ra, dec, e1, e2, mag, z=None):
    """
    Test TMT prediction: shear correlates with local mass.

    TMT v2.3: M_eff = M_bary × [1 + (r/r_c)^n]
    Higher mass → stronger lensing signal
    """
    print()
    print("=" * 60)
    print("TEST 2: Mass-Shear Relation")
    print("=" * 60)

    # Use magnitude as mass proxy (brighter = more massive)
    # Shear magnitude
    e = np.sqrt(e1**2 + e2**2)

    # Filter valid
    mask = np.isfinite(e) & np.isfinite(mag) & (mag > 0) & (mag < 30)
    e = e[mask]
    mag = mag[mask]

    # Bin by magnitude
    mag_bins = np.percentile(mag, [0, 25, 50, 75, 100])
    labels = ['Faint', 'Medium-Faint', 'Medium-Bright', 'Bright']

    print()
    print("Shear by magnitude bin (brighter = more massive):")
    print("-" * 50)

    results = []
    for i in range(len(mag_bins) - 1):
        bin_mask = (mag >= mag_bins[i]) & (mag < mag_bins[i + 1])
        e_bin = e[bin_mask]

        mean_e = np.mean(e_bin)
        std_e = np.std(e_bin) / np.sqrt(len(e_bin))

        print(f"  {labels[i]:15s} (mag {mag_bins[i]:.1f}-{mag_bins[i+1]:.1f}): "
              f"⟨e⟩ = {mean_e:.4f} ± {std_e:.4f} (N={len(e_bin)})")

        results.append({'label': labels[i], 'mean_e': mean_e, 'n': len(e_bin)})

    # Correlation test
    r, p = stats.spearmanr(mag, e)
    print()
    print(f"Magnitude-ellipticity correlation: r = {r:.4f}, p = {p:.2e}")

    # TMT predicts: brighter (more massive) galaxies have stronger surrounding shear
    # due to larger r_c and more temporal superposition
    if r < -0.05 and p < 0.01:
        verdict = "✓ Brighter galaxies show stronger shear - TMT consistent"
    else:
        verdict = "? No clear mass-shear trend"

    print(f"Verdict: {verdict}")

    return {
        'bins': results,
        'correlation_r': r,
        'correlation_p': p,
        'verdict': verdict
    }


def test_cosmic_shear_signal(e1, e2, ra, dec):
    """
    Measure cosmic shear signal (E/B mode decomposition).

    TMT predicts standard cosmic shear (B-mode ~ 0).
    """
    print()
    print("=" * 60)
    print("TEST 3: Cosmic Shear E/B Modes")
    print("=" * 60)

    # Simple E/B mode estimation via variance
    # E-mode: tangential shear around mass concentrations
    # B-mode: should be zero (systematic check)

    e = np.sqrt(e1**2 + e2**2)
    valid = np.isfinite(e)

    e1_valid = e1[valid]
    e2_valid = e2[valid]

    # Variance
    var_e1 = np.var(e1_valid)
    var_e2 = np.var(e2_valid)
    cov_e1e2 = np.cov(e1_valid, e2_valid)[0, 1]

    print(f"Ellipticity statistics ({np.sum(valid)} galaxies):")
    print(f"  Var(e1) = {var_e1:.6f}")
    print(f"  Var(e2) = {var_e2:.6f}")
    print(f"  Cov(e1,e2) = {cov_e1e2:.6f}")
    print()

    # E/B mode approximation
    # For random orientations: Var(e1) ≈ Var(e2), Cov ≈ 0
    ratio = var_e1 / var_e2 if var_e2 > 0 else np.nan

    print(f"  Var(e1)/Var(e2) = {ratio:.4f}")
    print(f"  Expected (random): 1.0")
    print()

    if 0.9 < ratio < 1.1 and np.abs(cov_e1e2) < 0.01:
        verdict = "✓ No significant B-mode - Data quality OK"
    else:
        verdict = "? Possible systematics in shear measurement"

    print(f"Verdict: {verdict}")

    return {
        'var_e1': var_e1,
        'var_e2': var_e2,
        'cov_e1e2': cov_e1e2,
        'ratio': ratio,
        'verdict': verdict
    }


def main():
    """Main test routine."""
    print("=" * 70)
    print("TMT v2.3 Test with UNIONS Survey (~15M galaxies)")
    print("=" * 70)
    print()

    # Load data
    table = load_unions_data()

    if table is None:
        print()
        print("To access UNIONS data:")
        print("  1. Install: pip install pyvo astropy")
        print("  2. Run: python scripts/download_UNIONS.py")
        print()
        print("Or query CADC TAP service directly.")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Extract columns
    try:
        ra = np.array(table['ra'])
        dec = np.array(table['dec'])
        e1 = np.array(table['e1'])
        e2 = np.array(table['e2'])
        mag = np.array(table['rmag']) if 'rmag' in table.colnames else np.array(table['mag_r'])
        z = np.array(table['photoz_mean']) if 'photoz_mean' in table.colnames else None
    except KeyError as e:
        print(f"Column not found: {e}")
        print(f"Available columns: {table.colnames}")
        return

    print(f"Data loaded: {len(ra)} galaxies")

    # Run tests
    results = {}

    # Test 1: Isotropy
    r1 = test_isotropy(ra, dec, e1, e2)
    results['isotropy'] = r1

    # Test 2: Mass-shear relation
    r2 = test_mass_shear_relation(ra, dec, e1, e2, mag, z)
    results['mass_shear'] = r2

    # Test 3: E/B modes
    r3 = test_cosmic_shear_signal(e1, e2, ra, dec)
    results['eb_modes'] = r3

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY - TMT v2.3 vs UNIONS")
    print("=" * 70)
    print()
    print("Test Results:")
    print(f"  1. Isotropy:    {results['isotropy']['verdict']}")
    print(f"  2. Mass-Shear:  {results['mass_shear']['verdict']}")
    print(f"  3. E/B Modes:   {results['eb_modes']['verdict']}")

    # Save results
    output_file = RESULTS_DIR / "TMT_UNIONS_results.txt"
    with open(output_file, 'w') as f:
        f.write("TMT v2.3 UNIONS Test Results\n")
        f.write("=" * 50 + "\n\n")
        for key, val in results.items():
            f.write(f"\n{key}:\n")
            for k, v in val.items():
                f.write(f"  {k}: {v}\n")

    print()
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
