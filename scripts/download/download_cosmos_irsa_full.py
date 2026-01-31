#!/usr/bin/env python3
"""
Download COSMOS2020 Full Catalog from IRSA
==========================================
Downloads the complete COSMOS2020 catalog with stellar masses, SFR, etc.

Source: IRSA/Caltech
Reference: Weaver et al. (2022) - ApJS 258, 11

Required columns for TMT tests:
- RA, DEC (coordinates)
- z_phot (photometric redshift)
- MASS_MED (stellar mass)
- SFR_MED (star formation rate)
- lp_type (galaxy type)

Size: ~1-2 GB
Time: 10-30 minutes depending on connection
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# UTF-8 for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "COSMOS2020_full"


def log(msg):
    """Print with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")
    sys.stdout.flush()


def download_via_astroquery():
    """Download COSMOS2020 via astroquery IRSA."""
    log("=" * 60)
    log("COSMOS2020 Full Catalog Download (IRSA)")
    log("=" * 60)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check existing
    existing = list(DATA_DIR.glob("*.fits"))
    if existing:
        size_mb = existing[0].stat().st_size / (1024*1024)
        log(f"Found existing: {existing[0].name} ({size_mb:.1f} MB)")
        if size_mb > 500:  # Full catalog should be >500MB
            log("Catalog already downloaded. Delete to re-download.")
            return str(existing[0])
    
    try:
        from astroquery.ipac.irsa import Irsa
        from astropy.coordinates import SkyCoord
        from astropy import units as u
        
        # COSMOS field center
        cosmos_center = SkyCoord(ra=150.1191, dec=2.2058, unit='deg')
        
        log("")
        log("Searching IRSA for COSMOS2020 catalogs...")
        
        # List available COSMOS catalogs
        log("Available COSMOS catalogs at IRSA:")
        catalogs_to_try = [
            'cosmos2020_classic',
            'cosmos2020_farmer', 
            'cosmos_photoz',
            'cosmos2015_v1',
        ]
        
        for cat_name in catalogs_to_try:
            log(f"  Trying: {cat_name}...")
            try:
                # Test query with small radius
                test = Irsa.query_region(
                    cosmos_center,
                    catalog=cat_name,
                    radius=1 * u.arcmin,
                    spatial='Cone'
                )
                if len(test) > 0:
                    log(f"    Found! {len(test)} sources in test region")
                    log(f"    Columns: {test.colnames[:10]}...")
                    
                    # Check for required columns
                    has_mass = any('mass' in c.lower() for c in test.colnames)
                    has_z = any('z' in c.lower() for c in test.colnames)
                    log(f"    Has mass column: {has_mass}")
                    log(f"    Has redshift column: {has_z}")
                    
                    if has_mass:
                        log(f"")
                        log(f"  => Using catalog: {cat_name}")
                        return download_full_catalog(cat_name, cosmos_center)
                        
            except Exception as e:
                log(f"    Error: {str(e)[:50]}")
                continue
        
        log("")
        log("No suitable catalog found with mass column.")
        log("Trying VizieR alternative...")
        return download_via_vizier()
        
    except ImportError:
        log("astroquery not installed. Install with: pip install astroquery")
        return None
    except Exception as e:
        log(f"Error: {e}")
        return None


def download_full_catalog(cat_name, center):
    """Download full catalog from IRSA."""
    from astroquery.ipac.irsa import Irsa
    from astropy import units as u
    
    log("")
    log(f"Downloading full {cat_name} catalog...")
    log("This may take 10-30 minutes. Please wait...")
    log("")
    
    # COSMOS field is ~2 sq.deg, use 1.5 deg radius to cover it
    radius = 1.5 * u.deg
    
    start_time = time.time()
    log(f"Querying IRSA (radius={radius})...")
    
    table = Irsa.query_region(
        center,
        catalog=cat_name,
        radius=radius,
        spatial='Cone'
    )
    
    elapsed = time.time() - start_time
    log(f"Downloaded {len(table):,} sources in {elapsed:.1f}s")
    
    # Save
    output = DATA_DIR / f"{cat_name}_{len(table)}.fits"
    log(f"Saving to {output.name}...")
    table.write(str(output), format='fits', overwrite=True)
    
    size_mb = output.stat().st_size / (1024*1024)
    log(f"Saved: {size_mb:.1f} MB")
    
    # Show column info
    log("")
    log("Available columns for TMT tests:")
    mass_cols = [c for c in table.colnames if 'mass' in c.lower()]
    z_cols = [c for c in table.colnames if 'z' in c.lower() and len(c) < 15]
    sfr_cols = [c for c in table.colnames if 'sfr' in c.lower()]
    
    log(f"  Mass columns: {mass_cols[:5]}")
    log(f"  Redshift columns: {z_cols[:5]}")
    log(f"  SFR columns: {sfr_cols[:5]}")
    
    return str(output)


def download_via_vizier():
    """Fallback: Download via VizieR with more columns."""
    from astroquery.vizier import Vizier
    
    log("")
    log("Trying VizieR J/ApJS/258/11 with all columns...")
    
    # Request specific columns including mass
    columns = [
        'RAJ2000', 'DEJ2000',  # Coordinates
        'lp_zBEST', 'lp_zPDF',  # Redshifts
        'lp_mass_med', 'lp_mass_best',  # Masses
        'lp_SFR_med', 'lp_SFR_best',  # SFR
        'lp_type',  # Galaxy type
        'lp_chi2_best',  # Fit quality
    ]
    
    v = Vizier(columns=columns, row_limit=-1)
    
    log("Querying VizieR (no row limit)...")
    start_time = time.time()
    
    result = v.query_constraints(catalog='J/ApJS/258/11/classic')
    
    if result and len(result) > 0:
        table = result[0]
        elapsed = time.time() - start_time
        log(f"Downloaded {len(table):,} sources in {elapsed:.1f}s")
        
        output = DATA_DIR / f"COSMOS2020_VizieR_full_{len(table)}.fits"
        log(f"Saving to {output.name}...")
        table.write(str(output), format='fits', overwrite=True)
        
        size_mb = output.stat().st_size / (1024*1024)
        log(f"Saved: {size_mb:.1f} MB")
        log(f"Columns: {table.colnames}")
        
        return str(output)
    
    log("VizieR download failed")
    return None


def main():
    log("COSMOS2020 Full Catalog Downloader")
    log("=" * 60)
    log("")
    log("This script downloads the COSMOS2020 catalog with:")
    log("  - Stellar masses (for mass-environment correlation)")
    log("  - Photometric redshifts")
    log("  - Star formation rates")
    log("")
    
    result = download_via_astroquery()
    
    log("")
    log("=" * 60)
    if result:
        log(f"SUCCESS: {result}")
        log("")
        log("Next step: Re-run TMT COSMOS test:")
        log("  python scripts/validation/test_TMT_COSMOS2015.py")
    else:
        log("FAILED: Could not download catalog")
        log("")
        log("Manual download option:")
        log("  1. Go to: https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-scan?projshort=COSMOS")
        log("  2. Select: COSMOS2020 Classic or Farmer catalog")
        log("  3. Download as FITS")
        log(f"  4. Place in: {DATA_DIR}")
    
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
