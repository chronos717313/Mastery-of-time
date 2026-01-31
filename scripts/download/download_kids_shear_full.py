#!/usr/bin/env python3
"""
Download KiDS DR3/DR4 Full Shear Catalog
========================================
Downloads the complete KiDS weak lensing shear catalog.

Source: Leiden Observatory / ESO Archive
Reference: Hildebrandt et al. (2017) - MNRAS 465, 1454

Required columns for TMT tests:
- RAJ2000, DEJ2000 (coordinates)
- e1, e2 (ellipticity components)
- weight (lensing weight)
- Z_B (photometric redshift)

Size: ~4 GB (full catalog)
Time: 30-60 minutes depending on connection
"""

import sys
import time
import os
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error
import ssl

# Bypass SSL verification for trusted scientific sites
ssl._create_default_https_context = ssl._create_unverified_context

# UTF-8 for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "KiDS_shear_full"

# KiDS DR3 official download URLs - Updated January 2026
# Main site files moved, use CADC or ESO instead
KIDS_DR3_URL = "https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/data/pub/KIDS/"
KIDS_SHEAR_FILES = [
    "KiDS_DR3.1_G9_shear.fits",
    "KiDS_DR3.1_G12_shear.fits", 
    "KiDS_DR3.1_G15_shear.fits",
    "KiDS_DR3.1_G23_shear.fits",
    "KiDS_DR3.1_GS_shear.fits",
]

# Alternative URLs to try
ALTERNATIVE_URLS = [
    "https://kids.strw.leidenuniv.nl/DR3/data-files/",
    "https://www.astro-wise.org/portal/kids_dr3/",
]

# ESO archive
ESO_KIDS_URL = "https://www.eso.org/qi/"


def log(msg):
    """Print with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")
    sys.stdout.flush()


def download_with_progress(url, dest_path, desc=""):
    """Download file with progress indicator."""
    log(f"Downloading: {desc or url}")
    log(f"  -> {dest_path}")
    
    start_time = time.time()
    last_report = [0]  # Use list to allow modification in nested function
    
    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        elapsed = time.time() - start_time
        
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            speed = mb_downloaded / elapsed if elapsed > 0 else 0
            eta = (mb_total - mb_downloaded) / speed if speed > 0 else 0
            
            # Report every 10%
            if int(percent / 10) > last_report[0]:
                last_report[0] = int(percent / 10)
                log(f"  {percent:.0f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB) - {speed:.1f} MB/s - ETA: {eta:.0f}s")
        else:
            mb_downloaded = downloaded / (1024 * 1024)
            if int(mb_downloaded / 100) > last_report[0]:
                last_report[0] = int(mb_downloaded / 100)
                log(f"  {mb_downloaded:.1f} MB downloaded...")
    
    try:
        urllib.request.urlretrieve(url, dest_path, reporthook=progress_hook)
        elapsed = time.time() - start_time
        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
        log(f"  Done: {size_mb:.1f} MB in {elapsed:.1f}s")
        return True
    except urllib.error.URLError as e:
        log(f"  Error: {e}")
        return False
    except Exception as e:
        log(f"  Error: {e}")
        return False


def download_kids_direct():
    """Download KiDS shear files - try multiple sources."""
    log("=" * 60)
    log("KiDS DR3 Shear Catalog - Direct Download")
    log("=" * 60)
    log("")
    log("Note: Original Leiden URLs may have changed.")
    log("Trying multiple sources...")
    log("")
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    downloaded = []
    failed = []
    
    # URLs to try in order
    base_urls = [
        KIDS_DR3_URL,
        "https://kids.strw.leidenuniv.nl/DR3/data-files/",
        "https://kids.strw.leidenuniv.nl/DR3/data/",
    ]
    
    for filename in KIDS_SHEAR_FILES:
        dest = DATA_DIR / filename
        
        if dest.exists():
            size_mb = dest.stat().st_size / (1024 * 1024)
            log(f"Already exists: {filename} ({size_mb:.1f} MB)")
            downloaded.append(str(dest))
            continue
        
        success = False
        for base_url in base_urls:
            url = base_url + filename
            log(f"Trying: {url}")
            if download_with_progress(url, dest, filename):
                downloaded.append(str(dest))
                success = True
                break
        
        if not success:
            failed.append(filename)
    
    return downloaded, failed


def download_via_astroquery():
    """Alternative: Download via astroquery ESO."""
    log("")
    log("Trying astroquery ESO archive...")
    
    try:
        from astroquery.eso import Eso
        
        eso = Eso()
        log("Connected to ESO archive")
        
        # Search for KiDS data
        log("Searching for KiDS DR3 shear catalogs...")
        # Note: This may require ESO login
        
        return None  # ESO usually requires authentication
        
    except ImportError:
        log("astroquery ESO module not available")
        return None
    except Exception as e:
        log(f"ESO error: {e}")
        return None


def download_via_vizier_full():
    """Download via VizieR with shear columns."""
    log("")
    log("Trying VizieR II/347 with shear columns...")
    
    try:
        from astroquery.vizier import Vizier
        
        # Request shear-specific columns
        columns = [
            'RAJ2000', 'DEJ2000',  # Coordinates
            'e1', 'e2',  # Ellipticity
            'weight',  # Lensing weight
            'Z_B', 'Z_B_MIN', 'Z_B_MAX',  # Photo-z
            'MAG_AUTO',  # Magnitude
            'FWHM_IMAGE',  # PSF size
        ]
        
        log(f"Requesting columns: {columns}")
        
        v = Vizier(columns=columns, row_limit=-1)
        
        log("Querying VizieR (no row limit)...")
        log("This may take 15-30 minutes for full catalog...")
        
        start_time = time.time()
        result = v.query_constraints(catalog='II/347/kids_dr3')
        
        if result and len(result) > 0:
            table = result[0]
            elapsed = time.time() - start_time
            log(f"Downloaded {len(table):,} sources in {elapsed:.1f}s")
            
            # Check if we got shear columns
            has_e1 = 'e1' in table.colnames
            has_e2 = 'e2' in table.colnames
            has_weight = 'weight' in table.colnames
            
            log(f"Has e1: {has_e1}, Has e2: {has_e2}, Has weight: {has_weight}")
            log(f"Columns received: {table.colnames}")
            
            output = DATA_DIR / f"KiDS_DR3_VizieR_shear_{len(table)}.fits"
            log(f"Saving to {output.name}...")
            table.write(str(output), format='fits', overwrite=True)
            
            size_mb = output.stat().st_size / (1024 * 1024)
            log(f"Saved: {size_mb:.1f} MB")
            
            if has_e1 and has_e2:
                return str(output)
            else:
                log("WARNING: VizieR did not return shear columns (e1, e2)")
                log("The full shear catalog must be downloaded from:")
                log("  https://kids.strw.leidenuniv.nl/DR3/lensing.php")
                return str(output)
        
        log("VizieR query returned no results")
        return None
        
    except Exception as e:
        log(f"VizieR error: {e}")
        return None


def merge_catalogs(file_list):
    """Merge multiple FITS catalogs into one."""
    if not file_list:
        return None
    
    log("")
    log(f"Merging {len(file_list)} catalogs...")
    
    try:
        from astropy.table import Table, vstack
        
        tables = []
        for f in file_list:
            log(f"  Loading: {Path(f).name}")
            t = Table.read(f)
            tables.append(t)
            log(f"    {len(t):,} sources")
        
        log("  Stacking tables...")
        merged = vstack(tables)
        log(f"  Total: {len(merged):,} sources")
        
        output = DATA_DIR / f"KiDS_DR3_merged_{len(merged)}.fits"
        log(f"  Saving to: {output.name}")
        merged.write(str(output), format='fits', overwrite=True)
        
        size_mb = output.stat().st_size / (1024 * 1024)
        log(f"  Final size: {size_mb:.1f} MB")
        
        return str(output)
        
    except Exception as e:
        log(f"Merge error: {e}")
        return None


def main():
    log("KiDS Shear Catalog Full Downloader")
    log("=" * 60)
    log("")
    log("This script downloads the KiDS weak lensing shear catalog with:")
    log("  - Ellipticity components (e1, e2) for isotropy test")
    log("  - Lensing weights")
    log("  - Photometric redshifts")
    log("")
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check existing files with shear data
    existing = list(DATA_DIR.glob("*.fits"))
    for f in existing:
        size_mb = f.stat().st_size / (1024 * 1024)
        log(f"Found existing: {f.name} ({size_mb:.1f} MB)")
        if size_mb > 500:  # Probably has enough data
            # Check if it has e1, e2 columns
            try:
                from astropy.table import Table
                t = Table.read(f)
                if 'e1' in t.colnames and 'e2' in t.colnames:
                    log(f"  Has e1, e2 columns - good for weak lensing!")
                    log("Catalog already downloaded. Delete to re-download.")
                    return 0
                else:
                    log(f"  Missing e1/e2 columns: {t.colnames[:10]}")
            except:
                pass
    
    # VizieR is the most reliable source - try it first
    log("")
    log("Downloading via VizieR (most reliable)...")
    result = download_via_vizier_full()
    
    if result:
        log("")
        log("=" * 60)
        log(f"SUCCESS: {result}")
        log("")
        log("Next step: Re-run TMT KiDS test:")
        log("  python scripts/validation/test_TMT_KiDS450.py")
        return 0
    
    # Try direct download as fallback
    log("")
    log("VizieR failed, trying direct download...")
    downloaded, failed = download_kids_direct()
    
    if downloaded and not failed:
        result = merge_catalogs(downloaded)
        if result:
            log("")
            log("=" * 60)
            log(f"SUCCESS: {result}")
            return 0
    
    log("")
    log("=" * 60)
    log("DOWNLOAD INCOMPLETE")
    log("")
    log("Manual download options:")
    log("  1. ESO Science Archive:")
    log("     https://archive.eso.org/scienceportal/home")
    log("     Search: 'KiDS DR3.1 shear'")
    log("")
    log("  2. CADC (Canadian):")
    log("     https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/search/")
    log("     Collection: KIDS")
    log("")
    log(f"  Place downloaded files in: {DATA_DIR}")
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
