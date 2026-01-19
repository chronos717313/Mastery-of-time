#!/usr/bin/env python3
"""
Script pour convertir et tester le fichier COSMOS .tbl
"""

from astropy.table import Table
from astropy.io import fits
import os
import sys

print("📥 Conversion fichier COSMOS .tbl → FITS")
print("=" * 60)

# Chemins possibles du fichier source
possible_paths = [
    '/home/user/Maitrise-du-temps/data/input/cosmos/cosmos_weak_lensing_shapes.fits.tbl',
    '/mnt/c/Users/PO/Downloads/cosmos_weak_lensing_shapes.fits.tbl',
    '../data/input/cosmos/cosmos_weak_lensing_shapes.fits.tbl',
    'cosmos_weak_lensing_shapes.fits.tbl'
]

source_file = None
for path in possible_paths:
    if os.path.exists(path):
        source_file = path
        print(f"✅ Fichier trouvé: {path}")
        break

if source_file is None:
    print("❌ Fichier .tbl non trouvé!")
    print("\n📋 INSTRUCTIONS:")
    print("1. Copiez le fichier depuis Windows:")
    print("   C:\\Users\\PO\\Downloads\\cosmos_weak_lensing_shapes.fits.tbl")
    print("\n2. Vers Linux:")
    print("   /home/user/Maitrise-du-temps/data/input/cosmos/")
    print("\n3. Ou placez-le dans le répertoire courant")
    sys.exit(1)

try:
    # Lire le fichier .tbl (format IPAC)
    print(f"\n📖 Lecture fichier .tbl...")
    table = Table.read(source_file, format='ipac')

    print(f"✅ Table lue: {len(table):,} lignes")
    print(f"   Colonnes ({len(table.colnames)}): {', '.join(table.colnames[:10])}...")

    # Vérifier colonnes nécessaires
    has_ra = 'ra' in table.colnames or 'RA' in table.colnames
    has_dec = 'dec' in table.colnames or 'DEC' in table.colnames
    has_gamma1 = 'gamma1' in table.colnames
    has_gamma2 = 'gamma2' in table.colnames
    has_zphot = 'zphot' in table.colnames

    print(f"\n📊 Colonnes détectées:")
    print(f"   RA: {'✅' if has_ra else '❌'}")
    print(f"   DEC: {'✅' if has_dec else '❌'}")
    print(f"   gamma1 (e1): {'✅' if has_gamma1 else '❌'}")
    print(f"   gamma2 (e2): {'✅' if has_gamma2 else '❌'}")
    print(f"   zphot: {'✅' if has_zphot else '❌'}")

    if not (has_ra and has_dec and has_gamma1 and has_gamma2):
        print("\n⚠️  Colonnes manquantes critiques!")
        print("   Colonnes disponibles:", table.colnames)
        sys.exit(1)

    # Convertir en FITS
    output_file = '../data/input/cosmos/cosmos_zphot_shapes.fits'
    print(f"\n💾 Conversion vers FITS...")
    table.write(output_file, format='fits', overwrite=True)

    print(f"✅ Fichier FITS créé: {output_file}")

    # Vérifier le fichier FITS
    print(f"\n🔍 Vérification fichier FITS...")
    with fits.open(output_file) as hdul:
        data = hdul[1].data
        print(f"✅ FITS valide: {len(data):,} galaxies")
        print(f"   Colonnes: {data.columns.names}")

    print("\n🎉 CONVERSION RÉUSSIE!")
    print("\n🚀 Prochaine étape:")
    print("   cd /home/user/Maitrise-du-temps/scripts")
    print("   python3 test_weak_lensing_TMT_vs_LCDM_real_data.py")

except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
