#!/usr/bin/env python3
"""
Download all required data for TMT validation
=============================================
Downloads COSMOS2015 and KiDS-450 catalogs via VizieR/IRSA.
"""

import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Data directories
BASE_DIR = Path(__file__).parent.parent.parent
COSMOS_DIR = BASE_DIR / "data" / "COSMOS2015"
KIDS_DIR = BASE_DIR / "data" / "KiDS450"

def download_cosmos2020():
    """Download COSMOS2020 catalog via VizieR (Weaver+ 2022)."""
    print("=" * 60)
    print("Downloading COSMOS2020 Catalog (Weaver+ 2022)")
    print("=" * 60)
    
    COSMOS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if already exists
    existing = list(COSMOS_DIR.glob("*COSMOS2020*.fits"))
    if existing:
        print(f"Found existing: {existing[0]}")
        size_mb = existing[0].stat().st_size / (1024*1024)
        print(f"Size: {size_mb:.1f} MB")
        return True
    
    try:
        from astroquery.vizier import Vizier
        
        # COSMOS2020 on VizieR: J/ApJS/258/11
        # Contains ~1.7 million sources with photo-z, stellar masses, etc.
        print("Querying VizieR J/ApJS/258/11 (COSMOS2020)...")
        print("This is the most complete COSMOS catalog (Weaver+ 2022)")
        print()
        
        # NO ROW LIMIT - get everything
        v = Vizier(columns=['*'], row_limit=-1)
        
        # Query full catalog (no coordinate constraint)
        print("Downloading full catalog (may take 5-10 minutes)...")
        result = v.query_constraints(catalog='J/ApJS/258/11/classic')
        
        if result and len(result) > 0:
            table = result[0]
            print(f"Downloaded: {len(table):,} galaxies")
            
            output = COSMOS_DIR / f"COSMOS2020_classic_{len(table)}.fits"
            table.write(str(output), format='fits', overwrite=True)
            print(f"Saved: {output}")
            print(f"Size: {output.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("No results, trying alternative table...")
            # Try the farmer catalog
            result = v.query_constraints(catalog='J/ApJS/258/11/farmer')
            if result and len(result) > 0:
                table = result[0]
                print(f"Downloaded: {len(table):,} galaxies (farmer)")
                output = COSMOS_DIR / f"COSMOS2020_farmer_{len(table)}.fits"
                table.write(str(output), format='fits', overwrite=True)
                print(f"Saved: {output}")
                return True
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        print("Falling back to COSMOS2015...")
        return download_cosmos2015_fallback()


def download_cosmos2015_fallback():
    """Fallback: Download COSMOS2015 if COSMOS2020 fails."""
    print()
    print("Trying COSMOS2015 (J/ApJS/224/24)...")
    
    try:
        from astroquery.vizier import Vizier
        
        v = Vizier(columns=['*'], row_limit=-1)
        result = v.query_constraints(catalog='J/ApJS/224/24/cosmos2015')
        
        if result and len(result) > 0:
            table = result[0]
            print(f"Downloaded: {len(table):,} galaxies")
            
            output = COSMOS_DIR / f"COSMOS2015_full_{len(table)}.fits"
            table.write(str(output), format='fits', overwrite=True)
            print(f"Saved: {output}")
            print(f"Size: {output.stat().st_size / (1024*1024):.1f} MB")
            return True
        return False
        
    except Exception as e:
        print(f"COSMOS2015 also failed: {e}")
        return False


def download_kids450():
    """Download KiDS-450 catalog via VizieR."""
    print()
    print("=" * 60)
    print("Downloading KiDS-450 Weak Lensing Catalog")
    print("=" * 60)
    
    KIDS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if already exists with sufficient size (>500MB expected)
    existing = list(KIDS_DIR.glob("*.fits"))
    if existing:
        size_mb = existing[0].stat().st_size / (1024*1024)
        print(f"Found existing: {existing[0]}")
        print(f"Size: {size_mb:.1f} MB")
        if size_mb > 400:  # Full catalog is ~500MB+
            return True
        else:
            print("File seems incomplete, re-downloading...")
    
    try:
        from astroquery.vizier import Vizier
        
        # KiDS DR3 on VizieR: II/347
        # Full catalog has ~14.6 million sources
        print("Querying VizieR II/347 (KiDS DR3)...")
        print("Full catalog: ~14.6 million sources")
        print()
        
        # NO ROW LIMIT - get everything
        v = Vizier(columns=['*'], row_limit=-1)
        
        print("Downloading full catalog (may take 10-20 minutes)...")
        result = v.query_constraints(catalog='II/347/kids_dr3')
        
        if result and len(result) > 0:
            table = result[0]
            print(f"Downloaded: {len(table):,} sources")
            
            # Remove old incomplete file if exists
            for old in KIDS_DIR.glob("*.fits"):
                old.unlink()
            
            output = KIDS_DIR / f"KiDS_DR3_full_{len(table)}.fits"
            table.write(str(output), format='fits', overwrite=True)
            print(f"Saved: {output}")
            print(f"Size: {output.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("No results from VizieR")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False


def download_cosmos_irsa():
    """Alternative: Download COSMOS via IRSA."""
    print()
    print("Trying IRSA alternative...")
    
    try:
        from astroquery.ipac.irsa import Irsa
        from astropy.coordinates import SkyCoord
        from astropy import units as u
        
        cosmos_center = SkyCoord(ra=150.1191, dec=2.2058, unit='deg')
        
        # Try different catalogs
        catalogs = ['cosmos2020_classic', 'cosmos_photoz', 'cosmos_morphology']
        
        for cat in catalogs:
            print(f"  Trying {cat}...")
            try:
                table = Irsa.query_region(
                    cosmos_center,
                    catalog=cat,
                    radius=2.0 * u.deg,
                    spatial='Cone'
                )
                if len(table) > 10000:
                    print(f"  Success: {len(table):,} objects")
                    output = COSMOS_DIR / f"COSMOS_IRSA_{cat}_{len(table)}.fits"
                    table.write(str(output), format='fits', overwrite=True)
                    print(f"  Saved: {output}")
                    return True
            except Exception as e:
                print(f"  Failed: {str(e)[:50]}")
                continue
        
        return False
        
    except Exception as e:
        print(f"IRSA error: {e}")
        return False


def main():
    print("TMT Data Downloader")
    print("=" * 60)
    print()
    
    # Download COSMOS2020 (or fallback to 2015)
    cosmos_ok = download_cosmos2020()
    if not cosmos_ok:
        cosmos_ok = download_cosmos_irsa()
    
    # Download KiDS-450
    kids_ok = download_kids450()
    
    # Summary
    print()
    print("=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"COSMOS2015: {'OK' if cosmos_ok else 'FAILED'}")
    print(f"KiDS-450:   {'OK' if kids_ok else 'FAILED'}")
    
    if cosmos_ok and kids_ok:
        print()
        print("All data downloaded successfully!")
        print("Run: python scripts/validation/test_complet_TMT_v232.py")
        return 0
    else:
        print()
        print("Some downloads failed. Manual download may be required:")
        if not cosmos_ok:
            print("  COSMOS2015: https://cosmos.astro.caltech.edu/page/photoz")
        if not kids_ok:
            print("  KiDS-450: https://kids.strw.leidenuniv.nl/DR3/")
        return 1


if __name__ == "__main__":
    sys.exit(main())
