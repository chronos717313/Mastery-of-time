#!/usr/bin/env python3
"""
Script de téléchargement COSMOS Weak Lensing Catalog
"""

from astroquery.irsa import Irsa
from astropy import units as u
from astropy.coordinates import SkyCoord
import sys

print("📥 Téléchargement COSMOS Weak Lensing Catalog...")
print("=" * 60)

# Centre du champ COSMOS
cosmos_center = SkyCoord("10:00:28.6 +02:12:21", unit=(u.hourangle, u.deg))

try:
    # Requête catalogue weak lensing
    print("\n🔍 Requête IRSA pour catalogue COSMOS weak lensing...")
    table = Irsa.query_region(
        cosmos_center,
        catalog='cosmos_wl',  # Weak lensing catalog
        radius=2.0 * u.deg,
        spatial='Cone'
    )

    print(f"✅ Téléchargé: {len(table):,} galaxies")
    print(f"   Colonnes: {table.colnames}")

    # Sauvegarder
    output_file = '../data/input/cosmos/cosmos_zphot_shapes.fits'
    table.write(output_file, format='fits', overwrite=True)

    print(f"\n✅ Fichier sauvegardé: {output_file}")
    print(f"   Taille: {len(table):,} lignes")

except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print("\n💡 Alternatives:")
    print("   1. Essayer catalogue 'cosmos2020_classic'")
    print("   2. Télécharger manuellement depuis IRSA web interface")
    sys.exit(1)
