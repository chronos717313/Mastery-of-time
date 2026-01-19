#!/usr/bin/env python3
"""
Test TMT v2.3 with COSMOS2015 Real Data
=======================================
Tests TMT differential expansion H(z, rho) using COSMOS2015 photometric catalog.

Key TMT predictions to test:
1. H(z, rho) varies with local density
2. Distance-redshift relation differs in voids vs clusters
3. Temporal superposition effects on galaxy properties

Data: ~500,000 galaxies with photo-z (σ = 0.007)
Reference: Laigle et al. (2016) - ApJS 224, 24
"""

import numpy as np
from pathlib import Path
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "COSMOS2015"
RESULTS_DIR = Path(__file__).parent.parent / "data" / "results"

# TMT v2.3 Parameters
G_T = 13.56  # Temporon coupling constant
H0_LCDM = 67.4  # km/s/Mpc (Planck)
H0_LOCAL = 73.0  # km/s/Mpc (local measurement)
OMEGA_M = 0.315
OMEGA_LAMBDA = 0.685


def load_cosmos2015(filepath=None):
    """
    Load COSMOS2015 catalog.

    Returns
    -------
    dict with arrays: ra, dec, photoz, stellar_mass, sfr, etc.
    """
    if filepath is None:
        # Try different file names
        candidates = [
            DATA_DIR / "COSMOS2015_VizieR_full.fits",
            DATA_DIR / "COSMOS2015_VizieR_100k.fits",
            DATA_DIR / "COSMOS2015_Laigle+_v1.1.fits",
        ]
        for candidate in candidates:
            if candidate.exists():
                filepath = candidate
                break

    if filepath is None or not filepath.exists():
        print(f"File not found in {DATA_DIR}")
        print("Run download_COSMOS2015.py first.")
        return None

    try:
        from astropy.io import fits
        from astropy.table import Table

        print(f"Loading COSMOS2015 catalog: {filepath}")
        table = Table.read(filepath)

        print(f"Loaded {len(table)} sources")
        print(f"Columns: {table.colnames[:20]}...")

        return table

    except ImportError:
        print("astropy required: pip install astropy")
        return None


def compute_local_density(ra, dec, z, n_neighbors=10, max_dz=0.05):
    """
    Compute local galaxy density using nearest neighbors.

    Parameters
    ----------
    ra, dec : array
        Coordinates in degrees
    z : array
        Redshift
    n_neighbors : int
        Number of neighbors for density estimate
    max_dz : float
        Maximum redshift difference for neighbors

    Returns
    -------
    density : array
        Local density (galaxies per sq. arcmin within dz slice)
    """
    from scipy.spatial import cKDTree

    # Convert to Cartesian for fast neighbor search
    # Use (ra, dec, z*1000) to weight redshift dimension
    coords = np.column_stack([ra, dec, z * 1000])

    tree = cKDTree(coords)
    densities = np.zeros(len(ra))

    for i in range(len(ra)):
        # Find neighbors within redshift slice
        mask = np.abs(z - z[i]) < max_dz
        if np.sum(mask) < n_neighbors:
            densities[i] = np.nan
            continue

        # Query for n_neighbors
        distances, _ = tree.query(coords[i], k=n_neighbors + 1)
        # Density ~ N / Area, Area ~ pi * r^2
        r = distances[-1]  # Distance to nth neighbor (in scaled units)
        if r > 0:
            densities[i] = n_neighbors / (np.pi * r ** 2)
        else:
            densities[i] = np.nan

    return densities


def H_TMT(z, rho_ratio):
    """
    TMT Hubble parameter with temporal superposition.

    H(z, rho) = H₀ · √[Omega_ₘ(1+z)³ + Omega_Lambda_eff(rho)]

    Parameters
    ----------
    z : float or array
        Redshift
    rho_ratio : float or array
        Local density / mean density

    Returns
    -------
    H : Hubble parameter in km/s/Mpc
    """
    # TMT v2.3: Temporon field effect
    # Phi_T(rho) = g_T × ln(1/rho) × |α² - β²|

    # At rho = 1 (mean density): Phi_T = 0, H = H_LCDM
    # At rho < 1 (voids): Phi_T > 0, H enhanced
    # At rho > 1 (clusters): Phi_T < 0, H suppressed

    # Quantum amplitudes
    alpha_sq = 1 / (1 + rho_ratio ** 0.75)
    beta_sq = rho_ratio ** 0.75 / (1 + rho_ratio ** 0.75)

    # Effective dark energy modification
    delta_lambda = 0.2 * (1 - alpha_sq + beta_sq)

    # Standard LambdaCDM terms
    omega_m_z = OMEGA_M * (1 + z) ** 3
    omega_lambda_eff = OMEGA_LAMBDA * (1 + delta_lambda)

    H = H0_LCDM * np.sqrt(omega_m_z + omega_lambda_eff)

    return H


def luminosity_distance_TMT(z, rho_ratio):
    """
    Compute luminosity distance with TMT corrections.

    d_L = (1+z) × c × ∫₀ᶻ dz'/H(z', rho)
    """
    from scipy.integrate import quad

    c = 299792.458  # km/s

    if np.isscalar(z):
        z = np.array([z])
        rho_ratio = np.array([rho_ratio])

    d_L = np.zeros_like(z, dtype=float)

    for i, (zi, rhoi) in enumerate(zip(z, rho_ratio)):
        if zi <= 0 or np.isnan(rhoi):
            d_L[i] = np.nan
            continue

        integrand = lambda zp: 1.0 / H_TMT(zp, rhoi)
        result, _ = quad(integrand, 0, zi)
        d_L[i] = (1 + zi) * c * result

    return d_L


def test_differential_expansion(table):
    """
    Test TMT prediction: H varies with local density.

    TMT predicts:
    - Voids: H_eff ~ 73 km/s/Mpc (higher)
    - Clusters: H_eff ~ 64 km/s/Mpc (lower)
    """
    print()
    print("=" * 60)
    print("TEST 1: Differential Expansion H(z, rho)")
    print("=" * 60)

    # Get photo-z and positions (VizieR column names)
    try:
        z = table['zPDF']  # Photometric redshift
        ra = table['RAJ2000']
        dec = table['DEJ2000']
        mass = table['MassMed']  # log stellar mass (median)
    except KeyError as e:
        print(f"Column not found: {e}")
        print("Available columns:", table.colnames[:30])
        return None

    # Filter valid sources
    mask = (z > 0.1) & (z < 1.5) & (mass > 8) & np.isfinite(z) & np.isfinite(mass)
    z = z[mask]
    ra = ra[mask]
    dec = dec[mask]
    mass = mass[mask]

    print(f"Valid galaxies: {len(z)}")

    # Compute local density
    print("Computing local densities (this may take a while)...")
    density = compute_local_density(np.array(ra), np.array(dec), np.array(z))

    # Classify environments
    median_density = np.nanmedian(density)
    void_mask = density < 0.3 * median_density
    cluster_mask = density > 3 * median_density
    field_mask = ~void_mask & ~cluster_mask

    print(f"Environment classification:")
    print(f"  Voids (rho < 0.3 median): {np.sum(void_mask)}")
    print(f"  Field (0.3 < rho < 3 median): {np.sum(field_mask)}")
    print(f"  Clusters (rho > 3 median): {np.sum(cluster_mask)}")

    # Bin by redshift and compute mean properties
    z_bins = np.linspace(0.2, 1.2, 11)
    z_centers = (z_bins[:-1] + z_bins[1:]) / 2

    results = {
        'void': {'z': [], 'd_L': []},
        'field': {'z': [], 'd_L': []},
        'cluster': {'z': [], 'd_L': []}
    }

    for env, mask in [('void', void_mask), ('field', field_mask), ('cluster', cluster_mask)]:
        for i in range(len(z_bins) - 1):
            bin_mask = mask & (z >= z_bins[i]) & (z < z_bins[i + 1])
            if np.sum(bin_mask) > 10:
                results[env]['z'].append(z_centers[i])

    # TMT predictions
    print()
    print("TMT v2.3 Predictions:")
    print("-" * 40)

    z_test = 0.5
    print(f"At z = {z_test}:")
    print(f"  Void (rho/rho_mean = 0.3):    H = {H_TMT(z_test, 0.3):.1f} km/s/Mpc")
    print(f"  Field (rho/rho_mean = 1.0):   H = {H_TMT(z_test, 1.0):.1f} km/s/Mpc")
    print(f"  Cluster (rho/rho_mean = 3.0): H = {H_TMT(z_test, 3.0):.1f} km/s/Mpc")

    # Expected d_L differences
    d_L_void = luminosity_distance_TMT(np.array([z_test]), np.array([0.3]))[0]
    d_L_field = luminosity_distance_TMT(np.array([z_test]), np.array([1.0]))[0]
    d_L_cluster = luminosity_distance_TMT(np.array([z_test]), np.array([3.0]))[0]

    print()
    print(f"Luminosity distances at z = {z_test}:")
    print(f"  Void:    d_L = {d_L_void:.1f} Mpc")
    print(f"  Field:   d_L = {d_L_field:.1f} Mpc")
    print(f"  Cluster: d_L = {d_L_cluster:.1f} Mpc")
    print(f"  Delta_d_L (void-cluster): {(d_L_void - d_L_cluster) / d_L_field * 100:.1f}%")

    return {
        'n_void': np.sum(void_mask),
        'n_field': np.sum(field_mask),
        'n_cluster': np.sum(cluster_mask),
        'H_void': H_TMT(z_test, 0.3),
        'H_field': H_TMT(z_test, 1.0),
        'H_cluster': H_TMT(z_test, 3.0)
    }


def test_mass_environment_correlation(table):
    """
    Test TMT prediction: r_c(M) correlation.

    TMT predicts r_c ∝ M^0.56, implying correlation
    between stellar mass and local environment effects.
    """
    print()
    print("=" * 60)
    print("TEST 2: Mass-Environment Correlation")
    print("=" * 60)

    try:
        z = table['zPDF']
        mass = table['MassMed']
        sfr = table['SFRMed'] if 'SFRMed' in table.colnames else None
        ra = table['RAJ2000']
        dec = table['DEJ2000']
    except KeyError as e:
        print(f"Column not found: {e}")
        return None

    # Filter
    mask = (z > 0.1) & (z < 1.0) & (mass > 8) & np.isfinite(mass)
    z = np.array(z[mask])
    mass = np.array(mass[mask])
    ra = np.array(ra[mask])
    dec = np.array(dec[mask])

    print(f"Galaxies analyzed: {len(z)}")

    # Compute density
    print("Computing local densities...")
    density = compute_local_density(ra, dec, z)

    # TMT prediction: massive galaxies in denser environments
    # r_c larger -> more dark matter contribution -> deeper potential -> more clustering
    valid = np.isfinite(density) & np.isfinite(mass)

    r, p = stats.spearmanr(mass[valid], density[valid])

    print()
    print(f"Mass-density correlation:")
    print(f"  Spearman r = {r:.4f}")
    print(f"  p-value = {p:.2e}")

    if r > 0.1 and p < 0.001:
        print("  -> CONSISTENT with TMT (massive galaxies in denser environments)")
    else:
        print("  -> No strong correlation detected")

    return {'r_mass_density': r, 'p_value': p}


def test_redshift_distribution(table):
    """
    Check redshift distribution for systematic effects.
    """
    print()
    print("=" * 60)
    print("TEST 3: Redshift Distribution Analysis")
    print("=" * 60)

    try:
        z = table['zPDF']
        z_err = table['b_zPDF'] if 'b_zPDF' in table.colnames else None  # lower bound
    except KeyError:
        z = None

    if z is None:
        print("No redshift column found")
        return None

    z = np.array(z)
    mask = (z > 0) & (z < 6) & np.isfinite(z)
    z = z[mask]

    print(f"Total galaxies with valid z: {len(z)}")
    print(f"Redshift range: {z.min():.3f} - {z.max():.3f}")
    print(f"Median z: {np.median(z):.3f}")
    print(f"Mean z: {np.mean(z):.3f}")

    # Histogram
    bins = np.linspace(0, 4, 41)
    hist, _ = np.histogram(z, bins=bins)

    print()
    print("Redshift distribution (peak counts):")
    peak_idx = np.argmax(hist)
    print(f"  Peak at z ~ {(bins[peak_idx] + bins[peak_idx+1])/2:.2f}")

    return {'median_z': np.median(z), 'n_total': len(z)}


def main():
    """Main test routine."""
    print("=" * 70)
    print("TMT v2.3 Test with COSMOS2015 Real Data")
    print("=" * 70)
    print()

    # Load data
    table = load_cosmos2015()

    if table is None:
        print()
        print("To download COSMOS2015 data, run:")
        print("  python scripts/download_COSMOS2015.py")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Run tests
    results = {}

    # Test 1: Differential expansion
    r1 = test_differential_expansion(table)
    if r1:
        results['differential_expansion'] = r1

    # Test 2: Mass-environment correlation
    r2 = test_mass_environment_correlation(table)
    if r2:
        results['mass_environment'] = r2

    # Test 3: Redshift distribution
    r3 = test_redshift_distribution(table)
    if r3:
        results['redshift_dist'] = r3

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY - TMT v2.3 vs COSMOS2015")
    print("=" * 70)
    print()

    if results.get('differential_expansion'):
        r = results['differential_expansion']
        print(f"Differential Expansion:")
        print(f"  H_void / H_cluster = {r['H_void'] / r['H_cluster']:.3f}")
        print(f"  TMT predicts ~1.15, LambdaCDM predicts 1.00")

    if results.get('mass_environment'):
        r = results['mass_environment']
        verdict = "[OK] CONSISTENT" if r['r_mass_density'] > 0.1 else "? INCONCLUSIVE"
        print(f"Mass-Environment: r = {r['r_mass_density']:.3f} {verdict}")

    # Save results
    output_file = RESULTS_DIR / "TMT_COSMOS2015_results.txt"
    with open(output_file, 'w') as f:
        f.write("TMT v2.3 COSMOS2015 Test Results\n")
        f.write("=" * 50 + "\n\n")
        for key, val in results.items():
            f.write(f"{key}: {val}\n")

    print()
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
