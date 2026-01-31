#!/usr/bin/env python3
"""
Convert VizieR SPARC data to TMT rotation curve format.
"""

import numpy as np
from pathlib import Path
from astropy.table import Table

DATA_DIR = Path(__file__).parent.parent.parent / "data"
SPARC_DIR = DATA_DIR / "SPARC"


def convert_sparc_vizier():
    """Convert SPARC VizieR tables to TMT format."""
    print("=" * 60)
    print("Converting SPARC VizieR data to TMT format")
    print("=" * 60)

    # Load galaxy properties (Table 0)
    props_file = SPARC_DIR / "J_AJ_152_157_table0_real.fits"
    if not props_file.exists():
        print(f"File not found: {props_file}")
        return None

    props = Table.read(props_file)
    print(f"\nGalaxy properties: {len(props)} galaxies")
    print(f"Columns: {props.colnames}")

    # Load rotation curves (Table 1)
    rc_file = SPARC_DIR / "J_AJ_152_157_table1_real.fits"
    if not rc_file.exists():
        print(f"File not found: {rc_file}")
        return None

    rc_data = Table.read(rc_file)
    print(f"\nRotation curves: {len(rc_data)} data points")
    print(f"Columns: {rc_data.colnames}")

    # Create galaxy properties dictionary
    galaxy_props = {}
    for row in props:
        name = row['Name'].strip() if isinstance(row['Name'], str) else str(row['Name']).strip()
        galaxy_props[name] = {
            'distance': float(row['Dist']) if row['Dist'] else 0,
            'inclination': float(row['i']) if row['i'] else 0,
            'L36': float(row['L3.6']) if row['L3.6'] else 0,
            'Reff': float(row['Reff']) if row['Reff'] else 0
        }

    # Group rotation curve data by galaxy
    rotation_curves = {}
    for row in rc_data:
        name = row['Name'].strip() if isinstance(row['Name'], str) else str(row['Name']).strip()

        if name not in rotation_curves:
            rotation_curves[name] = {
                'R': [], 'Vobs': [], 'e_Vobs': [],
                'Vgas': [], 'Vdisk': [], 'Vbul': [],
                'distance': float(row['Dist']) if row['Dist'] else 0
            }

        # Handle potential masked/null values
        try:
            R = float(row['Rad']) if row['Rad'] else 0
            Vobs = float(row['Vobs']) if row['Vobs'] else 0
            e_Vobs = float(row['e_Vobs']) if row['e_Vobs'] else 5.0
            Vgas = float(row['Vgas']) if row['Vgas'] else 0
            Vdisk = float(row['Vdisk']) if row['Vdisk'] else 0
            Vbul = float(row['Vbul']) if 'Vbul' in row.colnames and row['Vbul'] else 0

            if R > 0 and Vobs > 0:
                rotation_curves[name]['R'].append(R)
                rotation_curves[name]['Vobs'].append(Vobs)
                rotation_curves[name]['e_Vobs'].append(max(e_Vobs, 1.0))
                rotation_curves[name]['Vgas'].append(Vgas)
                rotation_curves[name]['Vdisk'].append(Vdisk)
                rotation_curves[name]['Vbul'].append(Vbul)
        except (ValueError, TypeError):
            continue

    # Convert to arrays
    for name in rotation_curves:
        for key in ['R', 'Vobs', 'e_Vobs', 'Vgas', 'Vdisk', 'Vbul']:
            rotation_curves[name][key] = np.array(rotation_curves[name][key])

    # Filter galaxies with valid data
    valid_galaxies = {name: data for name, data in rotation_curves.items()
                      if len(data['R']) >= 5}

    print(f"\nValid galaxies with >= 5 points: {len(valid_galaxies)}")

    # Write to TMT format
    output_file = SPARC_DIR / "SPARC_VizieR_rotation_curves.txt"
    with open(output_file, 'w') as f:
        f.write("# SPARC Rotation Curves from VizieR (J/AJ/152/157)\n")
        f.write("# Reference: Lelli, McGaugh & Schombert (2016), AJ, 152, 157\n")
        f.write("# Format: Galaxy  D(Mpc)  R(kpc)  Vobs  e_Vobs  Vgas  Vdisk  Vbul\n")
        f.write("#\n")

        for name, data in valid_galaxies.items():
            for i in range(len(data['R'])):
                f.write(f"{name:20s} {data['distance']:6.1f} {data['R'][i]:8.2f} "
                       f"{data['Vobs'][i]:8.2f} {data['e_Vobs'][i]:6.2f} "
                       f"{data['Vgas'][i]:8.2f} {data['Vdisk'][i]:8.2f} {data['Vbul'][i]:8.2f}\n")

    print(f"\nSaved: {output_file}")

    # Summary statistics
    total_points = sum(len(data['R']) for data in valid_galaxies.values())
    print(f"\nSummary:")
    print(f"  Galaxies: {len(valid_galaxies)}")
    print(f"  Total data points: {total_points}")

    # Mass range
    masses = []
    for name, data in valid_galaxies.items():
        if len(data['R']) > 0 and len(data['Vdisk']) > 0:
            # Estimate M_bary from V_disk at last point
            R_last = data['R'][-1]
            V_last = np.sqrt(data['Vgas'][-1]**2 + 0.5*data['Vdisk'][-1]**2)
            if V_last > 0 and R_last > 0:
                M_est = V_last**2 * R_last / 4.302e-6  # G in kpc units
                masses.append(M_est)

    if masses:
        print(f"  Mass range: {min(masses):.2e} - {max(masses):.2e} M_sun")

    return valid_galaxies


if __name__ == "__main__":
    convert_sparc_vizier()
