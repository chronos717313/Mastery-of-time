#!/usr/bin/env python3
"""
Download WALLABY Pilot DR2 Data
===============================
WALLABY (Widefield ASKAP L-band Legacy All-sky Blind surveY) Pilot Data Release 2.

Stats:
- ~1,800 galaxies with HI detections
- ~120+ galaxies with resolved kinematic models
- Redshift z < 0.08

Reference: Westmeier et al. (2022), PASA, 39, e058
Data: https://wallaby-survey.org/data/data-pilot-survey-dr2/
Archive: CSIRO ASKAP Science Data Archive (CASDA)

For TMT calibration: We need rotation curves from kinematic models.
"""

import os
import ssl
import urllib.request
from pathlib import Path
from typing import Optional, List
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "WALLABY_DR2"

# WALLABY DR2 URLs
WALLABY_BASE_URL = "https://wallaby-survey.org/data/"
CASDA_TAP_URL = "https://casda.csiro.au/casda_vo_tools/tap"
CADC_TAP_URL = "https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/tap"

# Direct catalog URLs (if available)
WALLABY_CATALOG_URLS = [
    "https://wallaby-survey.org/pilot/dr2/WALLABY_Pilot_DR2_catalog.fits",
    "https://casda.csiro.au/casda_vo_tools/datalink/links?ID=WALLABY_DR2"
]


def create_ssl_context():
    """Create SSL context that bypasses verification for problematic servers."""
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
        # Try with SSL bypass
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


def download_via_astroquery_cadc(n_sources: int = 2000) -> Optional[object]:
    """Download WALLABY data via CADC TAP service."""
    try:
        from astroquery.cadc import Cadc

        print(f"Connecting to CADC...")
        cadc = Cadc()

        # Query WALLABY catalog
        query = f"""
        SELECT TOP {n_sources}
            source_id, ra, dec, freq, w50, w20,
            rms, flux, snr, kin_pa, vsys, dist,
            mhi, vrot_max, vrot_err, incl, incl_err
        FROM wallaby.pilot_dr2_source
        ORDER BY snr DESC
        """

        print(f"Querying WALLABY DR2 via CADC TAP...")
        print(f"Query: {query[:100]}...")

        result = cadc.exec_sync(query)

        if result is not None and len(result) > 0:
            print(f"Downloaded {len(result)} sources")
            return result

        return None

    except ImportError:
        print("astroquery not installed. Install with: pip install astroquery")
        return None
    except Exception as e:
        print(f"CADC query error: {e}")
        return None


def download_via_pyvo(n_sources: int = 2000) -> Optional[object]:
    """Download WALLABY data via PyVO TAP service."""
    try:
        import pyvo as vo

        print("Connecting to CASDA TAP service...")
        service = vo.dal.TAPService(CASDA_TAP_URL)

        # Query for WALLABY sources with kinematic data
        query = f"""
        SELECT TOP {n_sources}
            *
        FROM ivoa.obscore
        WHERE obs_collection = 'WALLABY'
        AND dataproduct_type = 'catalog'
        """

        print(f"Querying CASDA for WALLABY data...")
        result = service.search(query)

        if result is not None and len(result) > 0:
            print(f"Found {len(result)} catalog entries")
            return result.to_table()

        return None

    except ImportError:
        print("pyvo not installed. Install with: pip install pyvo")
        return None
    except Exception as e:
        print(f"PyVO query error: {e}")
        return None


def download_via_vizier(n_sources: int = 2000) -> Optional[object]:
    """Download WALLABY data via VizieR (if catalog is indexed)."""
    try:
        from astroquery.vizier import Vizier

        print(f"Searching VizieR for WALLABY catalog...")

        # WALLABY catalogs on VizieR
        # J/PASA/39/e058 - WALLABY pilot survey
        v = Vizier(columns=['*'], row_limit=n_sources)

        # Try different catalog references
        catalog_ids = [
            'J/PASA/39/e058',  # Main WALLABY pilot survey
            'J/MNRAS/*/WALLABY',  # Any MNRAS WALLABY
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

        print("WALLABY not found on VizieR")
        return None

    except ImportError:
        print("astroquery not installed")
        return None
    except Exception as e:
        print(f"VizieR error: {e}")
        return None


def download_kinematic_models() -> Optional[Path]:
    """
    Download WALLABY kinematic models (FAT/3DBAROLO outputs).
    These contain rotation curves needed for TMT calibration.
    """
    print("\n" + "=" * 60)
    print("Downloading WALLABY Kinematic Models")
    print("=" * 60)

    # URLs for kinematic model data
    kinematic_urls = [
        "https://wallaby-survey.org/pilot/dr2/kinematic_models.tar.gz",
        "https://casda.csiro.au/wallaby/pilot_dr2_kinematic.fits",
    ]

    for url in kinematic_urls:
        dest = DATA_DIR / url.split('/')[-1]
        if download_with_progress(url, dest):
            return dest

    print("Direct download failed. Manual download required from:")
    print("  https://wallaby-survey.org/data/data-pilot-survey-dr2/")
    return None


def create_synthetic_wallaby_sample(n_galaxies: int = 1800) -> object:
    """
    Create synthetic WALLABY-like sample for testing pipeline.
    Uses realistic mass/velocity distributions from WALLABY DR2 statistics.

    WALLABY DR2 statistics (from literature):
    - M_HI range: 10^7 - 10^11 M_sun
    - V_rot range: 30 - 300 km/s
    - Distance range: 5 - 200 Mpc
    - Redshift: z < 0.08
    """
    import numpy as np
    from astropy.table import Table

    print(f"\nCreating synthetic WALLABY-like sample ({n_galaxies} galaxies)...")
    print("(For pipeline testing until real data is downloaded)")

    np.random.seed(42)

    # Mass distribution (log-normal, peaked around 10^9.5 M_sun)
    log_M_HI = np.random.normal(9.5, 0.8, n_galaxies)
    log_M_HI = np.clip(log_M_HI, 7.0, 11.0)
    M_HI = 10 ** log_M_HI

    # Baryonic mass (M_bary ~ 1.4 * M_HI for gas-dominated, more for stellar-dominated)
    f_star = np.random.uniform(0.3, 3.0, n_galaxies)  # M_star / M_HI ratio
    M_bary = M_HI * (1 + f_star)

    # Tully-Fisher: V_flat ~ M_bary^0.25
    V_flat = 50 * (M_bary / 1e9) ** 0.25
    V_flat += np.random.normal(0, 10, n_galaxies)  # scatter
    V_flat = np.clip(V_flat, 30, 350)

    # Distance (selection effects favor nearby)
    distance = np.random.exponential(40, n_galaxies) + 5
    distance = np.clip(distance, 5, 200)

    # Redshift from distance (H0 = 70)
    z = distance * 70 / 299792.458

    # Inclination (random, with detection bias toward edge-on)
    incl = np.random.beta(2, 1.5, n_galaxies) * 90  # favors higher inclinations
    incl = np.clip(incl, 30, 85)  # exclude face-on and extreme edge-on

    # Position angle (random)
    pa = np.random.uniform(0, 360, n_galaxies)

    # Galaxy IDs
    gal_ids = [f"WALLABY_J{i:06d}" for i in range(n_galaxies)]

    # RA/Dec (random sky positions in WALLABY footprint)
    ra = np.random.uniform(0, 360, n_galaxies)
    dec = np.random.uniform(-90, 30, n_galaxies)  # Southern sky

    # HI properties
    w50 = V_flat * 2 * np.sin(np.radians(incl))  # Line width at 50%
    w20 = w50 * 1.2  # Line width at 20%

    # SNR (log-normal distribution)
    snr = 10 ** np.random.normal(1.2, 0.4, n_galaxies)
    snr = np.clip(snr, 5, 500)

    # r_eff (effective radius, correlates with mass)
    r_eff = 2.0 * (M_bary / 1e10) ** 0.3  # kpc
    r_eff = np.clip(r_eff, 0.5, 30)

    # Surface brightness (related to r_eff and luminosity)
    mu_eff = 22 + 2.5 * np.log10(r_eff ** 2 / (M_bary / 1e10))  # mag/arcsec^2

    # Quality flag (1=excellent, 2=good, 3=fair)
    quality = np.random.choice([1, 2, 3], n_galaxies, p=[0.3, 0.5, 0.2])

    # Has kinematic model flag
    has_kin_model = (quality <= 2) & (snr > 15) & (incl > 40)

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
    """
    Generate synthetic rotation curves for galaxies with kinematic models.
    Uses realistic profiles based on WALLABY/SPARC statistics.
    """
    import numpy as np

    print("\nGenerating synthetic rotation curves...")

    rotation_curves = {}

    # Only generate for galaxies with kinematic models
    kin_mask = catalog['has_kin_model']
    kin_galaxies = catalog[kin_mask]

    for row in kin_galaxies:
        gal_id = row['source_id']
        V_flat = row['V_flat']
        r_eff = row['r_eff']
        M_bary = row['M_bary']

        # Number of radial points (depends on quality)
        n_points = np.random.randint(10, 30)

        # Radial extent (1-5 effective radii)
        r_max = r_eff * np.random.uniform(2, 5)
        R = np.linspace(0.5, r_max, n_points)

        # Rotation curve shape (arctangent profile)
        # V(R) = V_flat * (2/pi) * arctan(R / r_t)
        r_t = r_eff * 0.5  # turnover radius
        V_bary = V_flat * 0.7 * (2 / np.pi) * np.arctan(R / r_t)

        # Add "dark matter" contribution (this is what TMT should explain)
        # V_obs^2 = V_bary^2 + V_DM^2
        # For flat rotation curve: V_DM^2 ~ V_flat^2 - V_bary^2
        V_DM_sq = V_flat ** 2 - V_bary ** 2
        V_DM_sq = np.maximum(V_DM_sq, 0)

        V_obs = np.sqrt(V_bary ** 2 + V_DM_sq)

        # Add realistic errors
        e_V = 5 + 0.05 * V_obs + np.random.normal(0, 2, n_points)
        e_V = np.abs(e_V)
        e_V = np.clip(e_V, 2, 30)

        # Add scatter to observations
        V_obs += np.random.normal(0, e_V)
        V_obs = np.maximum(V_obs, 10)

        # Component velocities (for TMT analysis)
        # V_gas (HI contribution)
        f_gas = M_bary / (M_bary + 1e9)  # gas fraction proxy
        V_gas = V_bary * np.sqrt(f_gas * 0.5)

        # V_disk (stellar disk)
        V_disk = V_bary * np.sqrt(1 - f_gas * 0.5) * 0.9

        # V_bul (bulge, small for late-types)
        V_bul = V_bary * 0.1 * np.exp(-R / (r_eff * 0.3))

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


def save_data(catalog: object, rotation_curves: dict, prefix: str = "WALLABY_DR2"):
    """Save catalog and rotation curves to files."""
    import numpy as np

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save catalog
    cat_file = DATA_DIR / f"{prefix}_catalog.fits"
    try:
        catalog.write(str(cat_file), format='fits', overwrite=True)
        print(f"Catalog saved: {cat_file}")
    except Exception as e:
        # Fallback to CSV
        cat_file = DATA_DIR / f"{prefix}_catalog.csv"
        catalog.write(str(cat_file), format='csv', overwrite=True)
        print(f"Catalog saved: {cat_file}")

    # Save rotation curves in SPARC-compatible format
    rc_file = DATA_DIR / f"{prefix}_rotation_curves.txt"
    with open(rc_file, 'w') as f:
        f.write("# WALLABY DR2 Rotation Curves (SPARC-compatible format)\n")
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
        f.write(f"WALLABY DR2 Data Summary\n")
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
    print("WALLABY Pilot DR2 Data Downloader")
    print("=" * 70)
    print()
    print("Data source: CSIRO ASKAP Science Data Archive (CASDA)")
    print("URL: https://wallaby-survey.org/data/data-pilot-survey-dr2/")
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
    print("Method 1: CADC TAP Service")
    print("-" * 50)
    catalog = download_via_astroquery_cadc(n_sources=2000)

    if catalog is None:
        print()
        print("-" * 50)
        print("Method 2: VizieR")
        print("-" * 50)
        catalog = download_via_vizier(n_sources=2000)

    if catalog is None:
        print()
        print("-" * 50)
        print("Method 3: PyVO/CASDA TAP")
        print("-" * 50)
        catalog = download_via_pyvo(n_sources=2000)

    if catalog is None:
        print()
        print("-" * 50)
        print("Creating Synthetic Sample for Pipeline Testing")
        print("-" * 50)
        print()
        print("Real data download failed. Creating synthetic WALLABY-like sample")
        print("to test the TMT calibration pipeline.")
        print()

        catalog = create_synthetic_wallaby_sample(n_galaxies=1800)
        rotation_curves = generate_synthetic_rotation_curves(catalog)

        cat_file, rc_file = save_data(catalog, rotation_curves,
                                       prefix="WALLABY_DR2_synthetic")

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
        print("For real calibration, download actual WALLABY DR2 data from:")
        print("  https://wallaby-survey.org/data/data-pilot-survey-dr2/")
        print()
        print("Or use CASDA directly:")
        print("  https://data.csiro.au/collections/casda/")

    else:
        print()
        print("=" * 70)
        print("REAL DATA DOWNLOADED")
        print("=" * 70)
        print()
        print(f"Galaxies: {len(catalog)}")
        print(f"Columns: {catalog.colnames if hasattr(catalog, 'colnames') else 'N/A'}")

        # Save real data
        output = DATA_DIR / "WALLABY_DR2_real_catalog.fits"
        try:
            catalog.write(str(output), format='fits', overwrite=True)
            print(f"Saved: {output}")
        except Exception as e:
            output = DATA_DIR / "WALLABY_DR2_real_catalog.csv"
            catalog.write(str(output), format='csv', overwrite=True)
            print(f"Saved: {output}")

    return catalog


if __name__ == "__main__":
    main()
