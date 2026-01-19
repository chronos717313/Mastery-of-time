#!/usr/bin/env python3
"""
Script de téléchargement COSMOS avec plusieurs tentatives
"""

from astroquery.ipac.irsa import Irsa
from astropy import units as u
from astropy.coordinates import SkyCoord
import sys

print("📥 Téléchargement COSMOS Catalog...")
print("=" * 60)

# Centre du champ COSMOS
cosmos_center = SkyCoord("10:00:28.6 +02:12:21", unit=(u.hourangle, u.deg))

# Liste des catalogues à essayer
catalogs_to_try = [
    'cosmos2020_classic',
    'cosmos_morph',
    'cosmos_morphology',
    'cosmos_photoz',
    'fp_cosmos'
]

success = False

for catalog_name in catalogs_to_try:
    print(f"\n🔍 Tentative: {catalog_name}...")
    try:
        table = Irsa.query_region(
            cosmos_center,
            catalog=catalog_name,
            radius=2.0 * u.deg,
            spatial='Cone'
        )

        print(f"✅ Succès! Téléchargé: {len(table):,} objets")
        print(f"   Colonnes: {', '.join(table.colnames[:10])}...")

        # Vérifier si les colonnes nécessaires sont présentes
        has_ra = any(col in table.colnames for col in ['RA', 'ra', 'ALPHA_J2000'])
        has_dec = any(col in table.colnames for col in ['DEC', 'dec', 'DELTA_J2000'])
        has_shapes = any(col in table.colnames for col in ['e1', 'e2', 'gamma1', 'gamma2', 'E1', 'E2'])

        print(f"   RA/DEC: {'✅' if has_ra and has_dec else '❌'}")
        print(f"   Shapes (e1/e2): {'✅' if has_shapes else '❌'}")

        # Sauvegarder
        output_file = '../data/input/cosmos/cosmos_zphot_shapes.fits'
        table.write(output_file, format='fits', overwrite=True)

        print(f"\n✅ Fichier sauvegardé: {output_file}")
        print(f"   Catalogue: {catalog_name}")
        success = True
        break

    except Exception as e:
        print(f"   ❌ Échec: {str(e)[:100]}")
        continue

if not success:
    print("\n❌ Aucun catalogue trouvé")
    print("\n💡 Solution: Téléchargement manuel nécessaire")
    print("   1. Allez sur: https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-scan?projshort=COSMOS")
    print("   2. Cherchez: 'COSMOS Weak Lensing Source Catalog'")
    print("   3. Téléchargez le fichier FITS")
    print("   4. Placez dans: data/input/cosmos/cosmos_zphot_shapes.fits")
    sys.exit(1)
else:
    print("\n🎉 Téléchargement réussi!")
