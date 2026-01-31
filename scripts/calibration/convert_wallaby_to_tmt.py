#!/usr/bin/env python3
"""
Convert WALLABY PDR2 kinematic models to TMT format.
"""

import numpy as np
from astropy.table import Table
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"
WALLABY_DIR = DATA_DIR / "WALLABY_DR2"


def parse_array_string(s):
    """Parse comma-separated string to numpy array."""
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return np.array([])
    if isinstance(s, (list, np.ndarray)):
        return np.array(s)
    try:
        values = [float(x.strip()) for x in str(s).split(',') if x.strip()]
        return np.array(values)
    except:
        return np.array([])


def main():
    print("=" * 60)
    print("Converting WALLABY PDR2 to TMT format")
    print("=" * 60)

    # Load kinematic models
    kin_file = WALLABY_DIR / "WALLABY_PDR2_kinematic_real.fits"
    src_file = WALLABY_DIR / "WALLABY_PDR2_sources_real.fits"

    if not kin_file.exists():
        print(f"File not found: {kin_file}")
        return

    kin_table = Table.read(kin_file)
    print(f"\nKinematic models: {len(kin_table)} galaxies")

    # Load source catalog for additional info
    src_table = None
    if src_file.exists():
        src_table = Table.read(src_file)
        print(f"Source catalog: {len(src_table)} sources")

        # Create lookup by name
        src_lookup = {}
        for row in src_table:
            name = str(row['name']).strip()
            src_lookup[name] = row

    # Convert to rotation curves
    rotation_curves = {}
    skipped = 0

    for row in kin_table:
        name = str(row['name']).strip()

        # Parse rotation curve arrays
        rad = parse_array_string(row['rad'])
        vrot = parse_array_string(row['vrot_model'])
        e_vrot = parse_array_string(row['e_vrot_model'])

        if len(rad) < 3 or len(vrot) < 3:
            skipped += 1
            continue

        # Ensure same length
        min_len = min(len(rad), len(vrot))
        rad = rad[:min_len]
        vrot = vrot[:min_len]

        if len(e_vrot) < min_len:
            e_vrot = np.full(min_len, 10.0)  # Default error
        else:
            e_vrot = e_vrot[:min_len]

        # Get distance from source catalog
        dist = 0
        if src_table is not None and name in src_lookup:
            src_row = src_lookup[name]
            if 'dist_h' in src_row.colnames:
                dist = float(src_row['dist_h']) if src_row['dist_h'] else 0

        # Estimate distance from vsys if not available
        if dist <= 0 and 'vsys_model' in row.colnames:
            vsys = float(row['vsys_model']) if row['vsys_model'] else 0
            if vsys > 0:
                dist = vsys / 70.0  # H0 = 70 km/s/Mpc

        if dist <= 0:
            dist = 50.0  # Default distance

        # Filter valid points
        valid = (rad > 0) & (vrot > 0) & np.isfinite(rad) & np.isfinite(vrot)
        if np.sum(valid) < 3:
            skipped += 1
            continue

        rotation_curves[name] = {
            'R': rad[valid],
            'Vobs': vrot[valid],
            'e_Vobs': np.clip(e_vrot[valid], 1.0, 50.0),
            'distance': dist,
            'incl': float(row['inc_model']) if row['inc_model'] else 60.0,
            'pa': float(row['pa_model']) if row['pa_model'] else 0
        }

    print(f"\nValid rotation curves: {len(rotation_curves)}")
    print(f"Skipped: {skipped}")

    # Write to TMT format
    output_file = WALLABY_DIR / "WALLABY_PDR2_rotation_curves_real.txt"

    with open(output_file, 'w') as f:
        f.write("# WALLABY PDR2 Rotation Curves (REAL DATA)\n")
        f.write("# Source: CASDA (AS102.wallaby_pdr2_kinematic_models_v01)\n")
        f.write("# Format: Galaxy  D(Mpc)  R(kpc)  Vobs  e_Vobs  Vgas  Vdisk  Vbul\n")
        f.write("# Note: Vgas, Vdisk, Vbul set to 0 (not available in WALLABY)\n")
        f.write("#\n")

        for name, data in rotation_curves.items():
            for i in range(len(data['R'])):
                # WALLABY radii are in arcsec, convert to kpc
                # Using distance and angular size: R_kpc = R_arcsec * D_Mpc * 4.848e-6 * 1000
                R_arcsec = data['R'][i]
                R_kpc = R_arcsec * data['distance'] * 4.848e-3

                f.write(f"{name:30s} {data['distance']:8.2f} {R_kpc:10.4f} "
                       f"{data['Vobs'][i]:8.2f} {data['e_Vobs'][i]:6.2f} "
                       f"0.0 0.0 0.0\n")

    print(f"\nSaved: {output_file}")

    # Statistics
    all_R = []
    all_V = []
    for data in rotation_curves.values():
        all_R.extend(data['R'] * data['distance'] * 4.848e-3)
        all_V.extend(data['Vobs'])

    print(f"\nStatistics:")
    print(f"  Galaxies: {len(rotation_curves)}")
    print(f"  Total points: {len(all_R)}")
    print(f"  R range: {min(all_R):.2f} - {max(all_R):.2f} kpc")
    print(f"  V range: {min(all_V):.1f} - {max(all_V):.1f} km/s")

    return rotation_curves


if __name__ == "__main__":
    main()
