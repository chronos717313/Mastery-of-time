#!/usr/bin/env python3
"""
Download APERTIF DR1 Data
=========================
APERTIF (APERture Tile In Focus) Data Release 1 from WSRT.

Stats:
- ~1,740 galaxies with HI detections
- 221 observations of 160 independent fields
- ~1,000 sq.deg coverage

Reference: Adams et al. (2022), A&A, 667, A38
Documentation: https://www.astron.nl/telescopes/wsrt-apertif/apertif-dr1-documentation/
Archive: ASTRON Data Archive

For TMT calibration: Need to process HI cubes to extract rotation curves.
"""

import os
import ssl
import urllib.request
from pathlib import Path
from typing import Optional, List
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "APERTIF_DR1"

# APERTIF DR1 URLs
APERTIF_DOC_URL = "https://www.astron.nl/telescopes/wsrt-apertif/apertif-dr1-documentation/"
APERTIF_TAP_URL = "https://vo.astron.nl/tap"
ASTRON_ARCHIVE_URL = "https://hdl.handle.net/21.12136/archives"

# Direct catalog URLs (if available)
APERTIF_CATALOG_URLS = [
    "https://vo.astron.nl/apertif/dr1/catalog.fits",
]


def create_ssl_context():
    """Create SSL context that bypasses verification."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def download_with_progress(url: str, dest_path: Path) -> bool:
    """Download file with progress indicator."""
    print(f"Downloading: {url}")
    print(f"Destination: {dest_path}")

    def progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            mb = downloaded / (1024 * 1024)
            total_mb = total_size / (1024 * 1024)
            print(f"\r  {percent:.1f}% ({mb:.1f}/{total_mb:.1f} MB)", end="")
        else:
            print(f"\r  {downloaded / (1024*1024):.1f} MB", end="")

    try:
        ctx = create_ssl_context()
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ctx)
        )
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, dest_path, reporthook=progress)
        print("\nDownload complete!")
        return True
    except Exception as e:
        print(f"\nError: {e}")
        return False


def download_via_pyvo(n_sources: int = 2000) -> Optional[object]:
    """Download APERTIF data via PyVO TAP service."""
    try:
        import pyvo as vo

        print("Connecting to ASTRON TAP service...")
        service = vo.dal.TAPService(APERTIF_TAP_URL)

        # Query for APERTIF DR1 sources
        query = f"""
        SELECT TOP {n_sources}
            *
        FROM apertif.dr1_continuum
        """

        print(f"Querying ASTRON for APERTIF DR1 data...")
        result = service.search(query)

        if result is not None and len(result) > 0:
            print(f"Found {len(result)} sources")
            return result.to_table()

        return None

    except ImportError:
        print("pyvo not installed. Install with: pip install pyvo")
        return None
    except Exception as e:
        print(f"PyVO query error: {e}")
        return None


def download_via_vizier(n_sources: int = 2000) -> Optional[object]:
    """Download APERTIF data via VizieR (if catalog is indexed)."""
    try:
        from astroquery.vizier import Vizier

        print(f"Searching VizieR for APERTIF catalog...")

        # APERTIF catalogs on VizieR
        v = Vizier(columns=['*'], row_limit=n_sources)

        catalog_ids = [
            'J/A+A/667/A38',  # APERTIF DR1 paper
            'J/MNRAS/*/APERTIF',
        ]

        for cat_id in catalog_ids:
            try:
                result = v.query_constraints(catalog=cat_id)
                if result and len(result) > 0:
                    table = result[0]
                    print(f"Found catalog {cat_id}: {len(table)} sources")
                    return table
            except Exception:
                continue

        print("APERTIF not found on VizieR")
        return None

    except ImportError:
        print("astroquery not installed")
        return None
    except Exception as e:
        print(f"VizieR error: {e}")
        return None


def create_synthetic_apertif_sample(n_galaxies: int = 1740) -> object:
    """
    Create synthetic APERTIF-like sample for testing pipeline.
    Uses realistic distributions from APERTIF DR1 statistics.

    APERTIF DR1 characteristics:
    - Northern hemisphere coverage
    - M_HI range: 10^7 - 10^10.5 M_sun
    - Distance range: 5 - 150 Mpc
    - Good sensitivity for LSB galaxies
    """
    import numpy as np
    from astropy.table import Table

    print(f"\nCreating synthetic APERTIF-like sample ({n_galaxies} galaxies)...")
    print("(For pipeline testing until real data is downloaded)")

    np.random.seed(123)  # Different seed from WALLABY

    # Mass distribution (log-normal, slightly different from WALLABY)
    log_M_HI = np.random.normal(9.2, 0.9, n_galaxies)
    log_M_HI = np.clip(log_M_HI, 7.0, 10.5)
    M_HI = 10 ** log_M_HI

    # Baryonic mass
    f_star = np.random.uniform(0.2, 2.5, n_galaxies)
    M_bary = M_HI * (1 + f_star)

    # Tully-Fisher
    V_flat = 45 * (M_bary / 1e9) ** 0.26
    V_flat += np.random.normal(0, 12, n_galaxies)
    V_flat = np.clip(V_flat, 25, 300)

    # Distance (Northern hemisphere selection)
    distance = np.random.exponential(35, n_galaxies) + 5
    distance = np.clip(distance, 5, 150)

    # Redshift
    z = distance * 70 / 299792.458

    # Inclination
    incl = np.random.beta(1.8, 1.3, n_galaxies) * 90
    incl = np.clip(incl, 25, 85)

    # Position angle
    pa = np.random.uniform(0, 360, n_galaxies)

    # Galaxy IDs
    gal_ids = [f"APERTIF_J{i:06d}" for i in range(n_galaxies)]

    # RA/Dec (Northern hemisphere)
    ra = np.random.uniform(0, 360, n_galaxies)
    dec = np.random.uniform(20, 70, n_galaxies)  # Northern sky

    # HI properties
    w50 = V_flat * 2 * np.sin(np.radians(incl))
    w20 = w50 * 1.15

    # SNR
    snr = 10 ** np.random.normal(1.1, 0.5, n_galaxies)
    snr = np.clip(snr, 4, 400)

    # r_eff
    r_eff = 1.8 * (M_bary / 1e10) ** 0.32
    r_eff = np.clip(r_eff, 0.4, 25)

    # Surface brightness
    mu_eff = 22.5 + 2.5 * np.log10(r_eff ** 2 / (M_bary / 1e10))

    # Quality flag
    quality = np.random.choice([1, 2, 3], n_galaxies, p=[0.25, 0.50, 0.25])

    # Has kinematic model (APERTIF has fewer resolved sources than WALLABY)
    has_kin_model = (quality <= 2) & (snr > 12) & (incl > 35) & (r_eff > 1.0)

    table = Table({
        'source_id': gal_ids,
        'ra': ra,
        'dec': dec,
        'distance': distance,
        'z': z,
        'M_HI': M_HI,
        'M_bary': M_bary,
        'V_flat': V_flat,
        'incl': incl,
        'pa': pa,
        'w50': w50,
        'w20': w20,
        'snr': snr,
        'r_eff': r_eff,
        'mu_eff': mu_eff,
        'quality': quality,
        'has_kin_model': has_kin_model
    })

    print(f"  Total galaxies: {n_galaxies}")
    print(f"  With kinematic models: {np.sum(has_kin_model)}")
    print(f"  Mass range: {M_bary.min():.2e} - {M_bary.max():.2e} M_sun")
    print(f"  V_flat range: {V_flat.min():.0f} - {V_flat.max():.0f} km/s")

    return table


def generate_synthetic_rotation_curves(catalog: object) -> dict:
    """Generate synthetic rotation curves for APERTIF galaxies."""
    import numpy as np

    print("\nGenerating synthetic rotation curves...")

    rotation_curves = {}

    kin_mask = catalog['has_kin_model']
    kin_galaxies = catalog[kin_mask]

    for row in kin_galaxies:
        gal_id = row['source_id']
        V_flat = row['V_flat']
        r_eff = row['r_eff']
        M_bary = row['M_bary']

        n_points = np.random.randint(8, 25)
        r_max = r_eff * np.random.uniform(2, 4.5)
        R = np.linspace(0.4, r_max, n_points)

        # Rotation curve shape
        r_t = r_eff * 0.45
        V_bary = V_flat * 0.65 * (2 / np.pi) * np.arctan(R / r_t)

        # Dark matter contribution
        V_DM_sq = V_flat ** 2 - V_bary ** 2
        V_DM_sq = np.maximum(V_DM_sq, 0)

        V_obs = np.sqrt(V_bary ** 2 + V_DM_sq)

        # Errors (APERTIF slightly noisier than WALLABY)
        e_V = 6 + 0.06 * V_obs + np.random.normal(0, 2.5, n_points)
        e_V = np.abs(e_V)
        e_V = np.clip(e_V, 3, 35)

        V_obs += np.random.normal(0, e_V)
        V_obs = np.maximum(V_obs, 8)

        # Component velocities
        f_gas = M_bary / (M_bary + 1.2e9)
        V_gas = V_bary * np.sqrt(f_gas * 0.55)
        V_disk = V_bary * np.sqrt(1 - f_gas * 0.55) * 0.85
        V_bul = V_bary * 0.08 * np.exp(-R / (r_eff * 0.25))

        rotation_curves[gal_id] = {
            'R': R,
            'Vobs': V_obs,
            'e_Vobs': e_V,
            'Vgas': V_gas,
            'Vdisk': V_disk,
            'Vbul': V_bul,
            'distance': row['distance'],
            'M_bary': M_bary,
            'V_flat': V_flat,
            'r_eff': r_eff,
            'incl': row['incl']
        }

    print(f"  Generated {len(rotation_curves)} rotation curves")

    return rotation_curves


def save_data(catalog: object, rotation_curves: dict, prefix: str = "APERTIF_DR1"):
    """Save catalog and rotation curves to files."""
    import numpy as np

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save catalog
    cat_file = DATA_DIR / f"{prefix}_catalog.fits"
    try:
        catalog.write(str(cat_file), format='fits', overwrite=True)
        print(f"Catalog saved: {cat_file}")
    except Exception:
        cat_file = DATA_DIR / f"{prefix}_catalog.csv"
        catalog.write(str(cat_file), format='csv', overwrite=True)
        print(f"Catalog saved: {cat_file}")

    # Save rotation curves
    rc_file = DATA_DIR / f"{prefix}_rotation_curves.txt"
    with open(rc_file, 'w') as f:
        f.write("# APERTIF DR1 Rotation Curves (SPARC-compatible format)\n")
        f.write("# Generated for TMT calibration\n")
        f.write("#\n")
        f.write("# Columns: Galaxy  D(Mpc)  R(kpc)  Vobs  e_Vobs  Vgas  Vdisk  Vbul\n")
        f.write("#\n")

        for gal_id, rc in rotation_curves.items():
            for i in range(len(rc['R'])):
                f.write(f"{gal_id:20s} {rc['distance']:6.1f} {rc['R'][i]:8.2f} "
                       f"{rc['Vobs'][i]:8.2f} {rc['e_Vobs'][i]:6.2f} "
                       f"{rc['Vgas'][i]:8.2f} {rc['Vdisk'][i]:8.2f} {rc['Vbul'][i]:8.2f}\n")

    print(f"Rotation curves saved: {rc_file}")

    # Save summary
    summary_file = DATA_DIR / f"{prefix}_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write(f"APERTIF DR1 Data Summary\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Total galaxies: {len(catalog)}\n")
        f.write(f"With rotation curves: {len(rotation_curves)}\n\n")

        f.write("Mass distribution:\n")
        masses = catalog['M_bary']
        f.write(f"  Min: {np.min(masses):.2e} M_sun\n")
        f.write(f"  Max: {np.max(masses):.2e} M_sun\n")
        f.write(f"  Median: {np.median(masses):.2e} M_sun\n\n")

        f.write("Velocity distribution:\n")
        vels = catalog['V_flat']
        f.write(f"  Min: {np.min(vels):.0f} km/s\n")
        f.write(f"  Max: {np.max(vels):.0f} km/s\n")
        f.write(f"  Median: {np.median(vels):.0f} km/s\n")

    print(f"Summary saved: {summary_file}")

    return cat_file, rc_file


def main():
    print("=" * 70)
    print("APERTIF DR1 Data Downloader")
    print("=" * 70)
    print()
    print("Data source: ASTRON Data Archive")
    print("URL: https://www.astron.nl/telescopes/wsrt-apertif/apertif-dr1-documentation/")
    print()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Check existing files
    existing = list(DATA_DIR.glob("*"))
    if existing:
        print(f"Found existing files in {DATA_DIR}:")
        for f in existing:
            if f.is_file():
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  {f.name}: {size_mb:.1f} MB")
        print()

    catalog = None

    # Try different download methods
    print("-" * 50)
    print("Method 1: PyVO/ASTRON TAP")
    print("-" * 50)
    catalog = download_via_pyvo(n_sources=2000)

    if catalog is None:
        print()
        print("-" * 50)
        print("Method 2: VizieR")
        print("-" * 50)
        catalog = download_via_vizier(n_sources=2000)

    if catalog is None:
        print()
        print("-" * 50)
        print("Creating Synthetic Sample for Pipeline Testing")
        print("-" * 50)
        print()

        catalog = create_synthetic_apertif_sample(n_galaxies=1740)
        rotation_curves = generate_synthetic_rotation_curves(catalog)

        cat_file, rc_file = save_data(catalog, rotation_curves,
                                       prefix="APERTIF_DR1_synthetic")

        print()
        print("=" * 70)
        print("SYNTHETIC DATA CREATED")
        print("=" * 70)
        print()
        print("Files created:")
        print(f"  Catalog: {cat_file}")
        print(f"  Rotation curves: {rc_file}")
        print()
        print("NOTE: This is synthetic data for pipeline testing.")
        print("For real APERTIF data, access ASTRON archives at:")
        print("  https://www.astron.nl/telescopes/wsrt-apertif/apertif-dr1-documentation/")

    else:
        print()
        print("=" * 70)
        print("REAL DATA DOWNLOADED")
        print("=" * 70)
        print(f"Galaxies: {len(catalog)}")

        output = DATA_DIR / "APERTIF_DR1_real_catalog.fits"
        try:
            catalog.write(str(output), format='fits', overwrite=True)
            print(f"Saved: {output}")
        except Exception:
            output = DATA_DIR / "APERTIF_DR1_real_catalog.csv"
            catalog.write(str(output), format='csv', overwrite=True)
            print(f"Saved: {output}")

    return catalog


if __name__ == "__main__":
    main()
