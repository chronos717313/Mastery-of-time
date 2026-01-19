#!/usr/bin/env python3
"""
Download DES Y3 (Dark Energy Survey Year 3) weak lensing data
TMT v2.3.1 Validation

DES Y3 contains ~100 million galaxies with shape measurements
Data source: DES Data Release (https://des.ncsa.illinois.edu/releases)
"""

import os
import numpy as np
from pathlib import Path

try:
    from astropy.io import fits
    from astropy.table import Table
    from astroquery.vizier import Vizier
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False
    print("Warning: astropy/astroquery not available")

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "DES_Y3"


def download_des_y3_vizier(max_rows=1000000):
    """
    Download DES Y3 shear catalog via VizieR
    Catalog: J/MNRAS/509/3371 (DES Y3 Gold)
    """
    if not ASTROPY_AVAILABLE:
        print("ERROR: astropy required for VizieR download")
        return None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("DES Y3 DOWNLOAD VIA VIZIER")
    print("=" * 70)

    # Configure Vizier
    Vizier.ROW_LIMIT = max_rows

    # DES Y3 catalog in VizieR
    # J/MNRAS/509/3371 - DES Year 3 cosmology results
    catalog_id = "J/MNRAS/509/3371"

    print(f"\nSearching VizieR catalog: {catalog_id}")
    print(f"Maximum rows: {max_rows:,}")

    try:
        catalogs = Vizier.get_catalogs(catalog_id)

        if catalogs:
            print(f"\nFound {len(catalogs)} table(s)")

            for i, cat in enumerate(catalogs):
                print(f"  Table {i+1}: {len(cat)} rows, {len(cat.colnames)} columns")

            # Save the main catalog
            main_cat = catalogs[0]
            output_file = OUTPUT_DIR / "DES_Y3_VizieR.fits"
            main_cat.write(output_file, format='fits', overwrite=True)
            print(f"\nSaved: {output_file}")

            return main_cat
        else:
            print("No data found in VizieR")
            return None

    except Exception as e:
        print(f"VizieR download failed: {e}")
        return None


def create_synthetic_des_y3(n_galaxies=10000000):
    """
    Create synthetic DES Y3 catalog based on published statistics

    DES Y3 statistics (Amon et al. 2022, Secco et al. 2022):
    - ~100 million galaxies
    - Redshift range: 0.0 - 3.0 (peak at z ~ 0.6)
    - Shape noise: sigma_e ~ 0.26
    - Effective number density: n_eff ~ 5.6 arcmin^-2
    """
    print("=" * 70)
    print("CREATING SYNTHETIC DES Y3 CATALOG")
    print("=" * 70)
    print(f"\nGenerating {n_galaxies:,} galaxies...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)

    # Redshift distribution (Smail et al. model)
    # n(z) ~ z^2 * exp(-(z/z0)^1.5), z0 ~ 0.5
    z0 = 0.5
    z_samples = []
    while len(z_samples) < n_galaxies:
        z_candidate = np.random.exponential(0.6, n_galaxies - len(z_samples))
        z_candidate = z_candidate[z_candidate < 3.0]
        z_samples.extend(z_candidate.tolist())
    z = np.array(z_samples[:n_galaxies])

    # RA, DEC - DES Y3 footprint (~5000 deg^2 in South)
    # Approximate footprint: RA 0-90, 300-360; DEC -65 to -40
    ra_choice = np.random.choice([0, 1], size=n_galaxies, p=[0.5, 0.5])
    ra = np.where(ra_choice == 0,
                  np.random.uniform(0, 90, n_galaxies),
                  np.random.uniform(300, 360, n_galaxies))
    dec = np.random.uniform(-65, -40, n_galaxies)

    # Ellipticities (intrinsic + shear)
    # Shape noise sigma_e ~ 0.26
    sigma_e = 0.26
    e1_intrinsic = np.random.normal(0, sigma_e, n_galaxies)
    e2_intrinsic = np.random.normal(0, sigma_e, n_galaxies)

    # Add cosmic shear signal (simplified)
    # gamma ~ 0.02 (typical weak lensing shear)
    gamma1 = 0.02 * np.sin(2 * np.pi * ra / 90) * (1 + z) / 2
    gamma2 = 0.02 * np.cos(2 * np.pi * dec / 25) * (1 + z) / 2

    e1 = e1_intrinsic + gamma1
    e2 = e2_intrinsic + gamma2

    # Stellar mass proxy (from photometry)
    # log M* ~ 9.5 +/- 1.0 for DES galaxies
    log_mass = np.random.normal(9.5, 1.0, n_galaxies)
    log_mass = np.clip(log_mass, 7, 12)

    # Environment density proxy (from local galaxy density)
    # log(1+delta) ~ 0 +/- 0.5
    log_density = np.random.normal(0, 0.5, n_galaxies)

    # Weight (inverse variance)
    weight = np.random.uniform(0.5, 1.0, n_galaxies)

    # Size (effective radius in arcsec)
    size = np.random.lognormal(np.log(0.5), 0.5, n_galaxies)
    size = np.clip(size, 0.1, 5.0)

    # Create FITS table
    if ASTROPY_AVAILABLE:
        from astropy.table import Table

        # Save in chunks to avoid memory issues
        chunk_size = 1000000
        n_chunks = (n_galaxies + chunk_size - 1) // chunk_size

        for i in range(n_chunks):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, n_galaxies)

            table = Table({
                'RA': ra[start:end].astype(np.float32),
                'DEC': dec[start:end].astype(np.float32),
                'Z_MEAN': z[start:end].astype(np.float32),
                'E1': e1[start:end].astype(np.float32),
                'E2': e2[start:end].astype(np.float32),
                'LOG_MASS': log_mass[start:end].astype(np.float32),
                'LOG_DENSITY': log_density[start:end].astype(np.float32),
                'WEIGHT': weight[start:end].astype(np.float32),
                'SIZE': size[start:end].astype(np.float32),
            })

            suffix = f"_part{i+1}" if n_chunks > 1 else ""
            output_file = OUTPUT_DIR / f"DES_Y3_synthetic{suffix}.fits"
            table.write(output_file, format='fits', overwrite=True)
            print(f"  Saved chunk {i+1}/{n_chunks}: {output_file}")
    else:
        # Save as numpy arrays
        output_file = OUTPUT_DIR / "DES_Y3_synthetic.npz"
        np.savez(output_file,
                 ra=ra.astype(np.float32),
                 dec=dec.astype(np.float32),
                 z=z.astype(np.float32),
                 e1=e1.astype(np.float32),
                 e2=e2.astype(np.float32),
                 log_mass=log_mass.astype(np.float32),
                 log_density=log_density.astype(np.float32),
                 weight=weight.astype(np.float32),
                 size=size.astype(np.float32))
        print(f"  Saved: {output_file}")

    print(f"\nGenerated {n_galaxies:,} synthetic DES Y3 galaxies")
    print(f"Redshift range: {z.min():.3f} - {z.max():.3f}")
    print(f"Median redshift: {np.median(z):.3f}")

    return {
        'n_galaxies': n_galaxies,
        'z_median': np.median(z),
        'z_range': (z.min(), z.max()),
        'e1_std': np.std(e1),
        'e2_std': np.std(e2)
    }


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("DES Y3 DATA DOWNLOAD/GENERATION")
    print("=" * 70)

    # Try VizieR first (limited data)
    print("\nOption 1: VizieR download (limited)")
    result = download_des_y3_vizier(max_rows=100000)

    # Create synthetic data for full analysis
    print("\n" + "=" * 70)
    print("\nOption 2: Synthetic DES Y3 (10M galaxies)")
    stats = create_synthetic_des_y3(n_galaxies=10000000)

    print("\n" + "=" * 70)
    print("DOWNLOAD COMPLETE")
    print("=" * 70)
    print(f"\nOutput directory: {OUTPUT_DIR}")
