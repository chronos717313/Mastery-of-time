#!/usr/bin/env python3
"""
Download KiDS-450 Weak Lensing Catalog
======================================
Public weak lensing shear catalog from KiDS DR3.

Stats:
- 14,650,348 sources
- 360.3 sq.deg effective area
- 4.14 GB total

Reference: Hildebrandt et al. (2017)
URL: https://kids.strw.leidenuniv.nl/DR3/lensing.php
"""

import os
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "KiDS450"

# KiDS-450 catalog direct download
KIDS_BASE_URL = "https://kids.strw.leidenuniv.nl/DR3/data/"
KIDS_CATALOG = "KiDS_DR3.1_ugri_shear_mask.fits"

# Alternative: ESO archive
ESO_URL = "https://www.eso.org/qi/catalogQuery/download?collection=KiDS&source="


def download_with_progress(url, dest_path):
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
        urllib.request.urlretrieve(url, dest_path, reporthook=progress)
        print("\nDownload complete!")
        return True
    except Exception as e:
        print(f"\nError: {e}")
        return False


def download_via_astroquery():
    """Download KiDS data via astroquery/ESO."""
    try:
        from astroquery.eso import Eso

        print("Connecting to ESO archive...")
        eso = Eso()

        # Search for KiDS DR3
        print("Searching for KiDS DR3.1 shear catalog...")
        # Note: This may require ESO login for some data

        return None
    except ImportError:
        print("astroquery not installed")
        return None


def download_sample_via_vizier(n_sources=100000):
    """Download a sample via VizieR."""
    try:
        from astroquery.vizier import Vizier

        print(f"Downloading {n_sources} sources from VizieR...")

        # KiDS DR3 catalog on VizieR: II/347
        v = Vizier(columns=['*'], row_limit=n_sources)
        result = v.query_constraints(catalog='II/347/kids_dr3')

        if result and len(result) > 0:
            table = result[0]
            print(f"Downloaded {len(table)} sources")

            output = DATA_DIR / f"KiDS_DR3_VizieR_{len(table)}.fits"
            table.write(str(output), format='fits', overwrite=True)
            print(f"Saved to: {output}")
            return table

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    print("=" * 60)
    print("KiDS-450 Weak Lensing Catalog Downloader")
    print("=" * 60)
    print()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Check existing files
    existing = list(DATA_DIR.glob("*.fits"))
    if existing:
        print(f"Found existing files in {DATA_DIR}:")
        for f in existing:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  {f.name}: {size_mb:.1f} MB")
        print()

    # Try VizieR first (more reliable)
    print("Attempting download via VizieR...")
    table = download_sample_via_vizier(n_sources=500000)

    if table is not None:
        print()
        print("=" * 60)
        print("Download successful!")
        print("=" * 60)
        print()
        print(f"Sources: {len(table)}")
        print(f"Columns: {len(table.colnames)}")

        # Show key columns for weak lensing
        key_cols = ['RAJ2000', 'DEJ2000', 'e1', 'e2', 'weight', 'ALPHA', 'DELTA']
        print()
        print("Key columns for weak lensing:")
        for col in key_cols:
            matches = [c for c in table.colnames if col.lower() in c.lower()]
            if matches:
                print(f"  {col}: {matches[:3]}")

    else:
        print()
        print("VizieR download failed. Manual download options:")
        print()
        print("1. Direct from KiDS website:")
        print(f"   {KIDS_BASE_URL}")
        print()
        print("2. ESO Science Archive:")
        print("   https://archive.eso.org/scienceportal/home")
        print("   Search: KiDS DR3.1")


if __name__ == "__main__":
    main()
