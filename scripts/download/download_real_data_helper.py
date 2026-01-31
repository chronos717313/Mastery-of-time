#!/usr/bin/env python3
"""
Helper Script for Downloading Real BIG-SPARC Data
=================================================

This script provides utilities to:
1. Check what data is already downloaded
2. Open browser to download pages
3. Convert downloaded data to TMT format
4. Validate data integrity

Usage:
    python download_real_data_helper.py --check
    python download_real_data_helper.py --open-wallaby
    python download_real_data_helper.py --open-apertif
    python download_real_data_helper.py --convert
"""

import argparse
import webbrowser
from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_DIR / "data"

# URLs for data download
URLS = {
    'WALLABY_CASDA': 'https://data.csiro.au/collections/casda/',
    'WALLABY_SURVEY': 'https://wallaby-survey.org/data/data-pilot-survey-dr2/',
    'APERTIF_ASTRON': 'https://www.astron.nl/telescopes/wsrt-apertif/apertif-dr1-documentation/',
    'APERTIF_ARCHIVE': 'https://hdl.handle.net/21.12136/B014022C-978B-40F6-96C6-1A3B1F4A3DB0',
    'SPARC': 'http://astroweb.cwru.edu/SPARC/',
    'BIG_SPARC_PAPER': 'https://arxiv.org/abs/2411.13329'
}


def check_data_status():
    """Check what data is currently available."""
    print("=" * 60)
    print("DATA STATUS CHECK")
    print("=" * 60)
    print()

    surveys = {
        'SPARC': DATA_DIR / 'SPARC',
        'WALLABY_DR2': DATA_DIR / 'WALLABY_DR2',
        'APERTIF_DR1': DATA_DIR / 'APERTIF_DR1',
        'BIG_SPARC': DATA_DIR / 'BIG_SPARC'
    }

    total_galaxies = 0

    for name, path in surveys.items():
        print(f"\n{name}:")
        print("-" * 40)

        if not path.exists():
            print("  [X] Directory not found")
            continue

        files = list(path.glob("*"))
        if not files:
            print("  [X] No files found")
            continue

        # Count files by type
        fits_files = list(path.glob("*.fits"))
        txt_files = list(path.glob("*.txt"))
        mrt_files = list(path.glob("*.mrt"))

        print(f"  [OK] Directory exists")
        print(f"  Files: {len(files)} total")

        if fits_files:
            print(f"    - FITS: {len(fits_files)}")
            for f in fits_files[:3]:
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"      {f.name}: {size_mb:.1f} MB")

        if txt_files:
            print(f"    - TXT: {len(txt_files)}")
            # Check for rotation curves
            rc_files = [f for f in txt_files if 'rotation' in f.name.lower()]
            if rc_files:
                # Count galaxies
                for rc_file in rc_files:
                    try:
                        with open(rc_file, 'r') as f:
                            galaxies = set()
                            for line in f:
                                if not line.startswith('#') and line.strip():
                                    parts = line.split()
                                    if parts:
                                        galaxies.add(parts[0])
                            n_gal = len(galaxies)
                            total_galaxies += n_gal
                            print(f"      {rc_file.name}: {n_gal} galaxies")
                    except:
                        pass

        if mrt_files:
            print(f"    - MRT: {len(mrt_files)}")

        # Check for synthetic vs real
        synthetic = [f for f in files if 'synthetic' in f.name.lower()]
        real = [f for f in files if 'real' in f.name.lower()]

        if synthetic:
            print(f"  [!] Contains SYNTHETIC data ({len(synthetic)} files)")
        if real:
            print(f"  [OK] Contains REAL data ({len(real)} files)")

    print()
    print("=" * 60)
    print(f"TOTAL GALAXIES WITH ROTATION CURVES: ~{total_galaxies}")
    print("=" * 60)

    # Recommendations
    print()
    print("RECOMMENDATIONS:")
    print("-" * 40)

    wallaby_real = list((DATA_DIR / 'WALLABY_DR2').glob("*real*")) if (DATA_DIR / 'WALLABY_DR2').exists() else []
    apertif_real = list((DATA_DIR / 'APERTIF_DR1').glob("*real*")) if (DATA_DIR / 'APERTIF_DR1').exists() else []

    if not wallaby_real:
        print("  1. Download WALLABY DR2 real data:")
        print(f"     python {__file__} --open-wallaby")

    if not apertif_real:
        print("  2. Download APERTIF DR1 real data:")
        print(f"     python {__file__} --open-apertif")

    if wallaby_real and apertif_real:
        print("  [OK] Real data appears to be downloaded!")
        print("  Run calibration:")
        print("     python scripts/calibration/big_sparc_module.py")


def open_download_page(survey: str):
    """Open browser to download page."""
    url_key = f"{survey.upper()}_CASDA" if survey.upper() == 'WALLABY' else f"{survey.upper()}_ASTRON"

    if url_key not in URLS:
        # Try alternate keys
        for key in URLS:
            if survey.upper() in key:
                url_key = key
                break

    if url_key in URLS:
        url = URLS[url_key]
        print(f"Opening: {url}")
        webbrowser.open(url)

        print()
        print("DOWNLOAD INSTRUCTIONS:")
        print("-" * 40)

        if 'WALLABY' in survey.upper():
            print("""
1. Search for "WALLABY Pilot DR2"
2. Download:
   - Source catalog (FITS)
   - Kinematic models (if available)
3. Place files in: data/WALLABY_DR2/
4. Run: python scripts/download/download_real_data_helper.py --convert
            """)
        elif 'APERTIF' in survey.upper():
            print("""
1. Navigate to APERTIF DR1 data products
2. Download:
   - HI source catalog
   - Kinematic products (if available)
3. Place files in: data/APERTIF_DR1/
4. Run: python scripts/download/download_real_data_helper.py --convert
            """)
    else:
        print(f"Unknown survey: {survey}")
        print(f"Available: {list(URLS.keys())}")


def convert_downloaded_data():
    """Convert downloaded FITS/VOTable to TMT format."""
    print("=" * 60)
    print("DATA CONVERSION")
    print("=" * 60)
    print()

    try:
        from astropy.table import Table
        from astropy.io import fits
    except ImportError:
        print("ERROR: astropy required for conversion")
        print("Install with: pip install astropy")
        return

    # Check for new FITS files to convert
    for survey_dir in [DATA_DIR / 'WALLABY_DR2', DATA_DIR / 'APERTIF_DR1']:
        if not survey_dir.exists():
            continue

        fits_files = list(survey_dir.glob("*.fits"))
        for fits_file in fits_files:
            if 'synthetic' in fits_file.name.lower():
                continue

            print(f"\nProcessing: {fits_file.name}")

            try:
                table = Table.read(fits_file)
                print(f"  Columns: {table.colnames[:10]}...")
                print(f"  Rows: {len(table)}")

                # Check for kinematic columns
                kin_cols = ['vrot', 'v_rot', 'velocity', 'vsys', 'w50']
                found_kin = [c for c in table.colnames if any(k in c.lower() for k in kin_cols)]

                if found_kin:
                    print(f"  [OK] Kinematic columns found: {found_kin}")
                else:
                    print(f"  [!] No kinematic columns - may need processing")

            except Exception as e:
                print(f"  ERROR: {e}")

    print()
    print("NOTE: Full conversion to rotation curves requires kinematic models.")
    print("If only source catalogs available, use synthetic data for now.")


def main():
    parser = argparse.ArgumentParser(
        description="Helper for downloading real BIG-SPARC data"
    )
    parser.add_argument('--check', action='store_true',
                       help='Check current data status')
    parser.add_argument('--open-wallaby', action='store_true',
                       help='Open WALLABY download page')
    parser.add_argument('--open-apertif', action='store_true',
                       help='Open APERTIF download page')
    parser.add_argument('--open-sparc', action='store_true',
                       help='Open SPARC download page')
    parser.add_argument('--convert', action='store_true',
                       help='Convert downloaded FITS to TMT format')

    args = parser.parse_args()

    if args.check:
        check_data_status()
    elif args.open_wallaby:
        open_download_page('WALLABY')
    elif args.open_apertif:
        open_download_page('APERTIF')
    elif args.open_sparc:
        open_download_page('SPARC')
    elif args.convert:
        convert_downloaded_data()
    else:
        # Default: show status
        check_data_status()


if __name__ == "__main__":
    main()
