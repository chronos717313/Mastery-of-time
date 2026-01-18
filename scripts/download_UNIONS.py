#!/usr/bin/env python3
"""
Download UNIONS Survey Data
===========================
Access UNIONS (Ultraviolet Near Infrared Optical Northern Survey) data
via the Canadian Astronomy Data Centre (CADC).

Survey: ~4800 deg², 15+ million galaxies
Bands: u, r (CFHT), i (Pan-STARRS), z (Subaru), g (WHIGS)
Ideal for: weak lensing (r-band seeing ~0.65")

References:
- https://www.cfht.hawaii.edu/Science/CFIS/
- https://www.skysurvey.cc/
"""

import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "UNIONS"

# CADC TAP service for UNIONS/CFIS
CADC_TAP_URL = "https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/tap"

# Example ADQL query for CFIS catalog
EXAMPLE_QUERY = """
SELECT TOP 1000
    ra, dec,
    mag_r, mag_u,
    photoz_mean, photoz_std,
    e1, e2,  -- ellipticity for weak lensing
    weight
FROM cfis.cfis_dr4
WHERE photoz_mean BETWEEN 0.1 AND 1.5
  AND mag_r < 24.5
"""


def setup_pyvo():
    """Check if pyvo is installed for TAP queries."""
    try:
        import pyvo
        return True
    except ImportError:
        print("pyvo not installed. Install with: pip install pyvo")
        return False


def query_unions_tap(query, max_rows=10000):
    """
    Query UNIONS data via CADC TAP service.

    Parameters
    ----------
    query : str
        ADQL query string
    max_rows : int
        Maximum rows to return

    Returns
    -------
    astropy.table.Table
        Query results
    """
    try:
        import pyvo
        from pyvo.dal import TAPService

        print(f"Connecting to CADC TAP: {CADC_TAP_URL}")
        service = TAPService(CADC_TAP_URL)

        print("Executing query...")
        print(query[:200] + "..." if len(query) > 200 else query)

        result = service.search(query, maxrec=max_rows)
        table = result.to_table()

        print(f"Retrieved {len(table)} rows")
        return table

    except Exception as e:
        print(f"Error querying TAP: {e}")
        return None


def list_available_tables():
    """List available tables in CADC TAP service."""
    try:
        import pyvo
        from pyvo.dal import TAPService

        service = TAPService(CADC_TAP_URL)

        # Query for CFIS/UNIONS tables
        query = """
        SELECT table_name, description
        FROM tap_schema.tables
        WHERE schema_name LIKE '%cfis%'
           OR schema_name LIKE '%unions%'
           OR table_name LIKE '%cfis%'
           OR table_name LIKE '%unions%'
        """

        result = service.search(query)
        return result.to_table()

    except Exception as e:
        print(f"Error: {e}")
        return None


def download_unions_sample(output_file=None, n_galaxies=100000):
    """
    Download a sample of UNIONS galaxies for TMT analysis.

    Parameters
    ----------
    output_file : str, optional
        Output FITS file path
    n_galaxies : int
        Number of galaxies to download
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if output_file is None:
        output_file = DATA_DIR / f"UNIONS_sample_{n_galaxies}.fits"

    query = f"""
    SELECT TOP {n_galaxies}
        sourceid,
        ra, dec,
        umag, rmag, imag, zmag,
        umag_err, rmag_err, imag_err, zmag_err,
        photoz_mean, photoz_std, photoz_odds,
        e1, e2, weight,
        star_flag, extended_flag
    FROM cfis.photoz
    WHERE photoz_odds > 0.8
      AND rmag < 24.5
      AND star_flag = 0
    ORDER BY rmag
    """

    table = query_unions_tap(query, max_rows=n_galaxies)

    if table is not None:
        table.write(str(output_file), format='fits', overwrite=True)
        print(f"Saved to: {output_file}")
        return table

    return None


def main():
    """Main routine."""
    print("=" * 60)
    print("UNIONS Survey Data Access")
    print("=" * 60)
    print()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not setup_pyvo():
        print()
        print("To use UNIONS data, install pyvo:")
        print("  pip install pyvo astropy")
        print()
        print("Then run this script again.")
        print()
        print("Alternative: Download pre-made catalogs from:")
        print("  https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/")
        return

    print()
    print("Checking available UNIONS/CFIS tables...")
    tables = list_available_tables()

    if tables is not None and len(tables) > 0:
        print()
        print("Available tables:")
        for row in tables:
            print(f"  - {row['table_name']}: {row['description'][:50] if row['description'] else 'N/A'}...")

    print()
    print("Example query for UNIONS weak lensing:")
    print("-" * 40)
    print(EXAMPLE_QUERY)
    print("-" * 40)
    print()
    print("To download sample data, run:")
    print("  from download_UNIONS import download_unions_sample")
    print("  download_unions_sample(n_galaxies=100000)")


if __name__ == "__main__":
    main()
