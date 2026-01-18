#!/usr/bin/env python3
"""
Download COSMOS2015 Catalog
===========================
Downloads the COSMOS2015 photometric redshift catalog from IAP FTP server.

Reference: Laigle et al. (2016) - ApJS 224, 24
           https://cosmos.astro.caltech.edu/page/photoz

Data: ~500,000 galaxies with 30-band photometry (UV to IR)
      Photo-z precision: σ = 0.007, catastrophic failure < 0.5%
"""

import os
import urllib.request
import gzip
import shutil
from pathlib import Path

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data" / "COSMOS2015"
FTP_BASE = "ftp://ftp.iap.fr/pub/from_users/hjmcc/COSMOS2015/"

FILES_TO_DOWNLOAD = [
    "COSMOS2015_Laigle+_v1.1.fits.gz",  # Main catalog
]

# Alternative mirrors
VIZIER_URL = "https://cdsarc.cds.unistra.fr/ftp/J/ApJS/224/24/"
ESO_URL = "https://archive.eso.org/cms/eso-archive-news/release-of-the-ultravista-cosmos2015-catalogue.html"


def download_file(url, dest_path):
    """Download file with progress indicator."""
    print(f"Downloading: {url}")
    print(f"Destination: {dest_path}")

    try:
        urllib.request.urlretrieve(url, dest_path, reporthook=progress_hook)
        print("\nDownload complete!")
        return True
    except Exception as e:
        print(f"\nError downloading: {e}")
        return False


def progress_hook(block_num, block_size, total_size):
    """Progress indicator for download."""
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, downloaded * 100 / total_size)
        mb_downloaded = downloaded / (1024 * 1024)
        mb_total = total_size / (1024 * 1024)
        print(f"\r  Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="")
    else:
        mb_downloaded = downloaded / (1024 * 1024)
        print(f"\r  Downloaded: {mb_downloaded:.1f} MB", end="")


def decompress_gz(gz_path, output_path):
    """Decompress .gz file."""
    print(f"Decompressing: {gz_path}")
    with gzip.open(gz_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Decompressed to: {output_path}")


def main():
    """Main download routine."""
    print("=" * 60)
    print("COSMOS2015 Catalog Downloader")
    print("=" * 60)
    print()

    # Create data directory
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Data directory: {DATA_DIR}")
    print()

    # Check if already downloaded
    fits_file = DATA_DIR / "COSMOS2015_Laigle+_v1.1.fits"
    if fits_file.exists():
        size_mb = fits_file.stat().st_size / (1024 * 1024)
        print(f"Catalog already exists: {fits_file}")
        print(f"Size: {size_mb:.1f} MB")
        print()
        print("To re-download, delete the file first.")
        return str(fits_file)

    # Download from FTP
    for filename in FILES_TO_DOWNLOAD:
        url = FTP_BASE + filename
        dest = DATA_DIR / filename

        if not download_file(url, dest):
            # Try IRSA mirror
            print("\nTrying IRSA mirror...")
            url = IRSA_URL + filename
            if not download_file(url, dest):
                print(f"Failed to download {filename}")
                continue

        # Decompress if .gz
        if filename.endswith('.gz'):
            output_file = DATA_DIR / filename[:-3]  # Remove .gz
            decompress_gz(dest, output_file)
            # Optionally remove .gz file
            # dest.unlink()

    print()
    print("=" * 60)
    print("Download complete!")
    print("=" * 60)
    print()
    print("Catalog contents:")
    print("  - ~500,000 galaxies")
    print("  - 30-band photometry (0.25-8 μm)")
    print("  - Photometric redshifts (σ = 0.007)")
    print("  - Stellar masses")
    print()
    print("Next step: Run test_TMT_COSMOS2015.py")

    return str(fits_file)


if __name__ == "__main__":
    main()
