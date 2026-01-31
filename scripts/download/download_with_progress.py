#!/usr/bin/env python3
"""
Download COSMOS2020 and KiDS with progress logging
===================================================
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
COSMOS_DIR = BASE_DIR / "data" / "COSMOS2020"
KIDS_DIR = BASE_DIR / "data" / "KiDS450"


def log(msg):
    """Print with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")
    sys.stdout.flush()


def download_cosmos2020_chunked():
    """Download COSMOS2020 in chunks with progress."""
    log("=" * 60)
    log("COSMOS2020 Download (Weaver+ 2022)")
    log("=" * 60)
    
    COSMOS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check existing
    existing = list(COSMOS_DIR.glob("*.fits"))
    if existing:
        size_mb = existing[0].stat().st_size / (1024*1024)
        log(f"Found existing: {existing[0].name} ({size_mb:.1f} MB)")
        if size_mb > 400:
            return True
    
    try:
        from astroquery.vizier import Vizier
        
        log("Querying VizieR J/ApJS/258/11 (COSMOS2020 classic)...")
        log("Expected: ~966,000 galaxies")
        log("")
        
        # Download in chunks
        chunk_size = 100000
        all_tables = []
        offset = 0
        
        while True:
            log(f"  Downloading rows {offset:,} - {offset + chunk_size:,}...")
            start = time.time()
            
            v = Vizier(columns=['*'], row_limit=chunk_size)
            # Use ROW to paginate
            result = v.query_constraints(
                catalog='J/ApJS/258/11/classic',
                # Constraint to paginate - use ID range if available
            )
            
            if not result or len(result) == 0:
                break
                
            table = result[0]
            elapsed = time.time() - start
            log(f"    Got {len(table):,} rows in {elapsed:.1f}s")
            
            all_tables.append(table)
            
            if len(table) < chunk_size:
                log("  Reached end of catalog")
                break
            
            offset += chunk_size
            
            # VizieR doesn't support true pagination easily, so break after first chunk
            # and try full download
            break
        
        # If chunking didn't work, try full download
        if len(all_tables) == 1:
            log("")
            log("Attempting full catalog download (no row limit)...")
            log("This may take 5-15 minutes. Please wait...")
            
            v = Vizier(columns=['*'], row_limit=-1)
            start = time.time()
            
            result = v.query_constraints(catalog='J/ApJS/258/11/classic')
            
            if result and len(result) > 0:
                table = result[0]
                elapsed = time.time() - start
                log(f"Downloaded {len(table):,} galaxies in {elapsed:.1f}s")
                
                output = COSMOS_DIR / f"COSMOS2020_classic_{len(table)}.fits"
                log(f"Saving to {output.name}...")
                table.write(str(output), format='fits', overwrite=True)
                
                size_mb = output.stat().st_size / (1024*1024)
                log(f"Saved: {size_mb:.1f} MB")
                return True
        
        return False
        
    except Exception as e:
        log(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def download_kids_chunked():
    """Download KiDS DR3 with progress."""
    log("")
    log("=" * 60)
    log("KiDS DR3 Download (Hildebrandt+ 2017)")
    log("=" * 60)
    
    KIDS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check existing
    existing = list(KIDS_DIR.glob("*.fits"))
    if existing:
        size_mb = existing[0].stat().st_size / (1024*1024)
        log(f"Found existing: {existing[0].name} ({size_mb:.1f} MB)")
        if size_mb > 100:
            return True
    
    try:
        from astroquery.vizier import Vizier
        
        log("Querying VizieR II/347 (KiDS DR3)...")
        log("Expected: ~14.6M sources (may be limited by VizieR)")
        log("")
        
        # Try with reasonable limit first
        log("Attempting download (up to 5M rows)...")
        log("This may take 10-20 minutes. Please wait...")
        
        v = Vizier(columns=['RAJ2000', 'DEJ2000', 'e1', 'e2', 'weight', 'Z_B'], 
                   row_limit=5000000)
        start = time.time()
        
        result = v.query_constraints(catalog='II/347/kids_dr3')
        
        if result and len(result) > 0:
            table = result[0]
            elapsed = time.time() - start
            log(f"Downloaded {len(table):,} sources in {elapsed:.1f}s")
            
            # Remove old files
            for old in KIDS_DIR.glob("*.fits"):
                old.unlink()
            
            output = KIDS_DIR / f"KiDS_DR3_{len(table)}.fits"
            log(f"Saving to {output.name}...")
            table.write(str(output), format='fits', overwrite=True)
            
            size_mb = output.stat().st_size / (1024*1024)
            log(f"Saved: {size_mb:.1f} MB")
            return True
        else:
            log("No data returned from VizieR")
            return False
        
    except Exception as e:
        log(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    log("TMT Data Downloader (with progress)")
    log("=" * 60)
    log("")
    
    # Kill any stuck downloads - start fresh
    cosmos_ok = download_cosmos2020_chunked()
    kids_ok = download_kids_chunked()
    
    log("")
    log("=" * 60)
    log("SUMMARY")
    log("=" * 60)
    log(f"COSMOS2020: {'OK' if cosmos_ok else 'FAILED'}")
    log(f"KiDS DR3:   {'OK' if kids_ok else 'FAILED'}")
    
    if cosmos_ok and kids_ok:
        log("")
        log("All downloads complete!")
        log("Run: python scripts/validation/test_complet_TMT_v232.py")
        return 0
    else:
        log("")
        log("Some downloads failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
