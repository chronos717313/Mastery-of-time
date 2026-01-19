#!/usr/bin/env python3
"""
Test TMT v2.3 with KiDS-450 Weak Lensing Data
=============================================
Large-scale test of TMT isotropy prediction.

Data: KiDS-450 shear catalog (Hildebrandt+ 2017)
- 14.6M galaxies total (1M sample here)
- 360 sq.deg effective area
- e1, e2 ellipticity measurements

TMT v2.0 Prediction: Halos are ISOTROPIC (not directional)
"""

import numpy as np
from pathlib import Path
from scipy import stats
from scipy.spatial import cKDTree
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent.parent / "data" / "KiDS450"
RESULTS_DIR = Path(__file__).parent.parent / "data" / "results"


def load_kids450():
    """Load KiDS-450 shear catalog."""
    # Find latest shear file
    files = list(DATA_DIR.glob("KiDS450_shear_*.fits"))
    if not files:
        print(f"No shear catalog found in {DATA_DIR}")
        return None

    filepath = max(files, key=lambda x: x.stat().st_size)

    try:
        from astropy.table import Table
        print(f"Loading: {filepath}")
        table = Table.read(filepath)
        print(f"Loaded {len(table)} galaxies")
        return table
    except ImportError:
        print("astropy required: pip install astropy")
        return None


def test_isotropy_kids(table, n_sample=50000, n_neighbors=10):
    """
    Test TMT v2.0: halos are ISOTROPIC.

    Method: Check if galaxy orientations align with neighbors
    - Random (isotropic): mean |cos(2*dtheta)| = 2/pi ~ 0.637
    - Aligned: mean |cos(2*dtheta)| > 0.65
    """
    print()
    print("=" * 60)
    print("TEST 1: Halo Isotropy (TMT v2.0 Key Prediction)")
    print("=" * 60)
    print()
    print("TMT v2.0: Halos are ISOTROPIC (random orientations)")
    print("LCDM (triaxial NFW): Some alignment expected")
    print()

    # Extract data
    ra = np.array(table['RAJ2000'])
    dec = np.array(table['DEJ2000'])
    e1 = np.array(table['e1'])
    e2 = np.array(table['e2'])
    weight = np.array(table['Weight'])

    # Filter valid
    mask = np.isfinite(e1) & np.isfinite(e2) & (weight > 0)
    ra, dec, e1, e2, weight = ra[mask], dec[mask], e1[mask], e2[mask], weight[mask]

    print(f"Valid galaxies: {len(ra)}")

    # Sample for speed
    if len(ra) > n_sample:
        idx = np.random.choice(len(ra), n_sample, replace=False)
        ra_s, dec_s, e1_s, e2_s = ra[idx], dec[idx], e1[idx], e2[idx]
    else:
        ra_s, dec_s, e1_s, e2_s = ra, dec, e1, e2

    print(f"Analyzing {len(ra_s)} galaxies...")

    # Build KD-tree
    coords = np.column_stack([ra_s, dec_s])
    tree = cKDTree(coords)

    # Compute alignments
    alignments = []
    for i in range(len(ra_s)):
        theta_gal = 0.5 * np.arctan2(e2_s[i], e1_s[i])

        # Find neighbors
        distances, neighbors = tree.query(coords[i], k=n_neighbors + 1)
        neighbors = neighbors[1:]  # Exclude self

        for j in neighbors:
            # Direction to neighbor
            dra = ra_s[j] - ra_s[i]
            ddec = dec_s[j] - dec_s[i]
            theta_neighbor = np.arctan2(ddec, dra)

            # Alignment
            delta = theta_gal - theta_neighbor
            alignment = np.abs(np.cos(2 * delta))
            alignments.append(alignment)

    alignments = np.array(alignments)

    # Statistics
    random_exp = 2 / np.pi  # 0.6366
    mean_align = np.mean(alignments)
    std_align = np.std(alignments) / np.sqrt(len(alignments))

    # Significance
    t_stat = (mean_align - random_exp) / std_align
    p_value = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))

    print()
    print(f"Results ({len(alignments)} pairs):")
    print(f"  Mean alignment:    {mean_align:.5f} +/- {std_align:.5f}")
    print(f"  Random expectation: {random_exp:.5f}")
    print(f"  Deviation: {(mean_align - random_exp)/random_exp * 100:.3f}%")
    print(f"  t-statistic: {t_stat:.2f}")
    print(f"  p-value: {p_value:.2e}")
    print()

    deviation = abs(mean_align - random_exp)
    if deviation < 0.005:
        verdict = "[OK] ISOTROPIC - Strong support for TMT v2.0"
    elif deviation < 0.01:
        verdict = "[OK] ~ISOTROPIC - Weak support for TMT v2.0"
    elif mean_align > random_exp:
        verdict = "[?] ALIGNED - May favor LCDM triaxial halos"
    else:
        verdict = "[?] ANTI-ALIGNED - Unexpected"

    print(f"VERDICT: {verdict}")

    return {
        'mean_alignment': mean_align,
        'std': std_align,
        'random_expectation': random_exp,
        'deviation_percent': (mean_align - random_exp)/random_exp * 100,
        't_statistic': t_stat,
        'p_value': p_value,
        'n_pairs': len(alignments),
        'verdict': verdict
    }


def test_ellipticity_distribution(table):
    """
    Test ellipticity distribution (E/B mode check).
    """
    print()
    print("=" * 60)
    print("TEST 2: Ellipticity Distribution (Systematics Check)")
    print("=" * 60)

    e1 = np.array(table['e1'])
    e2 = np.array(table['e2'])
    weight = np.array(table['Weight'])

    mask = np.isfinite(e1) & np.isfinite(e2) & (weight > 0)
    e1, e2, weight = e1[mask], e2[mask], weight[mask]

    # Statistics
    mean_e1 = np.average(e1, weights=weight)
    mean_e2 = np.average(e2, weights=weight)
    var_e1 = np.average((e1 - mean_e1)**2, weights=weight)
    var_e2 = np.average((e2 - mean_e2)**2, weights=weight)

    e = np.sqrt(e1**2 + e2**2)
    mean_e = np.average(e, weights=weight)

    print()
    print(f"Statistics ({len(e1)} galaxies, weighted):")
    print(f"  <e1> = {mean_e1:.6f} (should be ~0)")
    print(f"  <e2> = {mean_e2:.6f} (should be ~0)")
    print(f"  Var(e1) = {var_e1:.6f}")
    print(f"  Var(e2) = {var_e2:.6f}")
    print(f"  Var ratio = {var_e1/var_e2:.4f} (should be ~1)")
    print(f"  <|e|> = {mean_e:.4f}")
    print()

    # Check for systematics
    if abs(mean_e1) < 0.001 and abs(mean_e2) < 0.001:
        verdict = "[OK] No systematic bias detected"
    else:
        verdict = "[?] Possible systematic bias"

    if 0.9 < var_e1/var_e2 < 1.1:
        verdict += " | Variance ratio OK"
    else:
        verdict += " | Variance ratio suspicious"

    print(f"VERDICT: {verdict}")

    return {
        'mean_e1': mean_e1,
        'mean_e2': mean_e2,
        'var_e1': var_e1,
        'var_e2': var_e2,
        'var_ratio': var_e1/var_e2,
        'mean_e': mean_e,
        'verdict': verdict
    }


def test_redshift_dependence(table):
    """
    Test if ellipticity varies with redshift (environment proxy).
    """
    print()
    print("=" * 60)
    print("TEST 3: Redshift Dependence")
    print("=" * 60)

    z = np.array(table['zbest'])
    e1 = np.array(table['e1'])
    e2 = np.array(table['e2'])
    weight = np.array(table['Weight'])

    mask = np.isfinite(z) & np.isfinite(e1) & np.isfinite(e2) & (z > 0) & (z < 2) & (weight > 0)
    z, e1, e2, weight = z[mask], e1[mask], e2[mask], weight[mask]

    e = np.sqrt(e1**2 + e2**2)

    print(f"\nAnalyzing {len(z)} galaxies with 0 < z < 2")
    print(f"Redshift range: {z.min():.3f} - {z.max():.3f}")
    print(f"Median z: {np.median(z):.3f}")

    # Bin by redshift
    z_bins = [0, 0.3, 0.6, 0.9, 1.2, 2.0]

    print()
    print("Ellipticity by redshift bin:")
    print("-" * 50)

    results = []
    for i in range(len(z_bins) - 1):
        bin_mask = (z >= z_bins[i]) & (z < z_bins[i+1])
        if np.sum(bin_mask) < 100:
            continue

        e_bin = e[bin_mask]
        w_bin = weight[bin_mask]

        mean_e = np.average(e_bin, weights=w_bin)
        n = len(e_bin)

        print(f"  z = {z_bins[i]:.1f}-{z_bins[i+1]:.1f}: <|e|> = {mean_e:.4f} (N={n})")
        results.append({'z_min': z_bins[i], 'z_max': z_bins[i+1], 'mean_e': mean_e, 'n': n})

    # Correlation
    r, p = stats.spearmanr(z, e)
    print()
    print(f"Correlation z vs |e|: r = {r:.4f}, p = {p:.2e}")

    if abs(r) < 0.05:
        verdict = "[OK] No significant z-dependence"
    else:
        verdict = f"[?] Correlation detected (r={r:.3f})"

    print(f"VERDICT: {verdict}")

    return {
        'correlation_r': r,
        'correlation_p': p,
        'z_bins': results,
        'verdict': verdict
    }


def main():
    print("=" * 70)
    print("TMT v2.3 Test with KiDS-450 Weak Lensing Data")
    print("=" * 70)
    print()

    table = load_kids450()
    if table is None:
        print("Run download_KiDS450.py first.")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    results = {}

    # Test 1: Isotropy
    r1 = test_isotropy_kids(table)
    results['isotropy'] = r1

    # Test 2: Ellipticity distribution
    r2 = test_ellipticity_distribution(table)
    results['ellipticity'] = r2

    # Test 3: Redshift dependence
    r3 = test_redshift_dependence(table)
    results['redshift'] = r3

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY - TMT v2.3 vs KiDS-450 (1M galaxies)")
    print("=" * 70)
    print()
    print("Test Results:")
    print(f"  1. Isotropy:     {results['isotropy']['verdict']}")
    print(f"  2. Systematics:  {results['ellipticity']['verdict']}")
    print(f"  3. z-dependence: {results['redshift']['verdict']}")
    print()

    # TMT Score
    score = 0
    if 'ISOTROPIC' in results['isotropy']['verdict']:
        score += 1
    if 'OK' in results['ellipticity']['verdict']:
        score += 1
    if 'OK' in results['redshift']['verdict']:
        score += 1

    print(f"TMT v2.0 SCORE: {score}/3")
    if score >= 2:
        print("-> TMT v2.0 (isotropic halos) SUPPORTED by KiDS-450 data")
    else:
        print("-> Results inconclusive or favor LCDM")

    # Save
    output_file = RESULTS_DIR / "TMT_KiDS450_results.txt"
    with open(output_file, 'w') as f:
        f.write("TMT v2.3 KiDS-450 Test Results\n")
        f.write("=" * 50 + "\n\n")
        for key, val in results.items():
            f.write(f"\n{key}:\n")
            for k, v in val.items():
                f.write(f"  {k}: {v}\n")

    print()
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
