# 📥 GUIDE TÉLÉCHARGEMENT DONNÉES COSMOS/DES

**Date**: 15 Janvier 2026
**Objectif**: Obtenir les vraies données pour le test θ_halo ↔ θ_voisin
**Taille totale**: ~17 GB (COSMOS ~2 GB + DES ~15 GB)

---

## 🚀 MÉTHODE RAPIDE (RECOMMANDÉE)

### Étape 1: Créer répertoire de données

```bash
# Depuis la racine du projet
mkdir -p data/input/cosmos
mkdir -p data/input/des
cd data/input
```

---

## 📦 COSMOS FIELD DATA

### Option A: Téléchargement Direct (RECOMMANDÉ)

```bash
# Catalogue photométrique COSMOS 2020
wget -O cosmos/COSMOS2020_CLASSIC_R1_v2.1.fits \
  "https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/COSMOS2020_CLASSIC_R1_v2.1.fits.gz"

# Décompresser
gunzip cosmos/COSMOS2020_CLASSIC_R1_v2.1.fits.gz

# Shapes weak lensing
wget -O cosmos/cosmos_zphot_shapes.fits \
  "https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits"
```

**Taille**: ~2 GB total

---

### Option B: Via IRSA (Interface Web)

1. Aller sur: https://irsa.ipac.caltech.edu/Missions/cosmos.html
2. Cliquer "Catalogs" → "COSMOS2020"
3. Télécharger:
   - `COSMOS2020_CLASSIC_R1_v2.1.fits` (photometry)
   - `cosmos_zphot_shapes.fits` (weak lensing)

---

### Option C: Via astroquery (Python)

```python
from astroquery.irsa import Irsa

# Télécharger catalogue COSMOS
table = Irsa.query_region(
    "COSMOS",
    catalog='cosmos_morphology',
    spatial='Cone',
    radius=2.0  # degrés
)

# Sauvegarder
table.write('cosmos/cosmos_catalog.fits', format='fits', overwrite=True)
```

---

## 📦 DES Y3 DATA

### Option A: Téléchargement Direct (RECOMMANDÉ)

```bash
# DES Y3 Gold Catalog (positions, masses, redshifts)
wget -O des/y3_gold_2_2.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/gold-2-2/y3_gold_2_2.fits"

# DES Y3 Shear Catalog (weak lensing)
wget -O des/y3a2_metacal_v03_shear.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/shear/y3a2_metacal_v03_shear.fits"
```

**Taille**: ~15 GB total
**Temps**: ~30-60 min (selon connexion)

---

### Option B: Via DES Data Access Portal

1. Aller sur: https://des.ncsa.illinois.edu/releases/y3a2
2. Créer compte gratuit (requis)
3. Naviguer vers: **Y3 Key Catalogs** → **Gold** et **Shear**
4. Télécharger:
   - `y3_gold_2_2.fits` (~8 GB)
   - `y3a2_metacal_v03_shear.fits` (~7 GB)

---

### Option C: Via easyaccess (Outil DES)

```bash
# Installer easyaccess
pip install easyaccess

# Se connecter
easyaccess

# Dans le shell easyaccess:
> load_table y3_gold_2_2
> save_table y3_gold_2_2.fits
```

---

## 🔍 VÉRIFICATION DES DONNÉES

### Script de Vérification

```bash
# Créer script de vérification
cat > verify_data.py << 'EOF'
#!/usr/bin/env python3
"""Vérifie l'intégrité des données COSMOS/DES téléchargées"""

from astropy.io import fits
import os

def verify_file(filepath, expected_columns):
    """Vérifie qu'un fichier FITS contient les colonnes attendues"""
    if not os.path.exists(filepath):
        print(f"❌ {filepath}: FICHIER MANQUANT")
        return False

    try:
        with fits.open(filepath) as hdul:
            data = hdul[1].data
            cols = data.columns.names

            missing = [c for c in expected_columns if c not in cols]

            print(f"✅ {os.path.basename(filepath)}:")
            print(f"   Lignes: {len(data):,}")
            print(f"   Colonnes: {len(cols)}")

            if missing:
                print(f"   ⚠️  Colonnes manquantes: {missing}")
                return False
            else:
                print(f"   ✅ Toutes colonnes requises présentes")
                return True

    except Exception as e:
        print(f"❌ {filepath}: ERREUR - {e}")
        return False

# Vérifier COSMOS
print("\n" + "="*60)
print("VÉRIFICATION COSMOS")
print("="*60)

cosmos_cols = ['RA', 'DEC', 'PHOTOZ', 'MASS_BEST', 'e1', 'e2']
verify_file('data/input/cosmos/cosmos_zphot_shapes.fits', cosmos_cols)

# Vérifier DES
print("\n" + "="*60)
print("VÉRIFICATION DES Y3")
print("="*60)

des_gold_cols = ['RA', 'DEC', 'DNF_Z', 'SOF_PSF_MAG_CORRECTED_I']
verify_file('data/input/des/y3_gold_2_2.fits', des_gold_cols)

des_shear_cols = ['ra', 'dec', 'e_1', 'e_2', 'R11', 'R22']
verify_file('data/input/des/y3a2_metacal_v03_shear.fits', des_shear_cols)

print("\n" + "="*60)
print("VÉRIFICATION TERMINÉE")
print("="*60)
EOF

# Rendre exécutable
chmod +x verify_data.py

# Exécuter
python3 verify_data.py
```

---

## ⚡ TÉLÉCHARGEMENT RAPIDE (Script Automatique)

```bash
#!/bin/bash
# Script de téléchargement automatique COSMOS/DES

set -e

echo "📥 TÉLÉCHARGEMENT DONNÉES COSMOS/DES"
echo "===================================="

# Créer répertoires
mkdir -p data/input/cosmos data/input/des
cd data/input

# COSMOS
echo ""
echo "📦 Téléchargement COSMOS..."
wget -c -O cosmos/cosmos_zphot_shapes.fits.gz \
  "https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits.gz" \
  || echo "⚠️  COSMOS téléchargement échoué"

if [ -f cosmos/cosmos_zphot_shapes.fits.gz ]; then
    echo "   Décompression..."
    gunzip -f cosmos/cosmos_zphot_shapes.fits.gz
    echo "   ✅ COSMOS téléchargé (~2 GB)"
fi

# DES Y3 Gold
echo ""
echo "📦 Téléchargement DES Y3 Gold (~8 GB)..."
echo "   ⚠️  Ceci peut prendre 30-60 minutes"
wget -c -O des/y3_gold_2_2.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/gold-2-2/y3_gold_2_2.fits" \
  || echo "⚠️  DES Gold téléchargement échoué"

# DES Y3 Shear
echo ""
echo "📦 Téléchargement DES Y3 Shear (~7 GB)..."
wget -c -O des/y3a2_metacal_v03_shear.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/shear/y3a2_metacal_v03_shear.fits" \
  || echo "⚠️  DES Shear téléchargement échoué"

echo ""
echo "✅ TÉLÉCHARGEMENT TERMINÉ"
echo ""
echo "📂 Fichiers dans data/input/"
ls -lh cosmos/ des/

echo ""
echo "🔍 Exécuter verify_data.py pour vérifier intégrité"
```

**Sauvegarder comme**: `scripts/download_cosmos_des.sh`

```bash
chmod +x scripts/download_cosmos_des.sh
./scripts/download_cosmos_des.sh
```

---

## 📊 STRUCTURE DONNÉES ATTENDUE

Après téléchargement réussi:

```
data/input/
├── cosmos/
│   ├── COSMOS2020_CLASSIC_R1_v2.1.fits  (~1.5 GB)
│   └── cosmos_zphot_shapes.fits          (~500 MB)
└── des/
    ├── y3_gold_2_2.fits                  (~8 GB)
    └── y3a2_metacal_v03_shear.fits       (~7 GB)
```

**Total**: ~17 GB

---

## 🔧 DÉPENDANCES PYTHON

```bash
# Installer packages nécessaires
pip3 install astropy numpy scipy matplotlib

# Vérifier installation
python3 -c "from astropy.io import fits; print('✅ astropy OK')"
```

---

## 📖 UTILISATION DES DONNÉES

### Charger COSMOS

```python
from astropy.io import fits

# Ouvrir catalogue COSMOS
cosmos = fits.open('data/input/cosmos/cosmos_zphot_shapes.fits')[1].data

# Extraire colonnes
RA = cosmos['RA']
DEC = cosmos['DEC']
z_phot = cosmos['PHOTOZ']
e1 = cosmos['e1']
e2 = cosmos['e2']

print(f"COSMOS: {len(RA):,} galaxies")
```

### Charger DES

```python
# Ouvrir catalogues DES
des_gold = fits.open('data/input/des/y3_gold_2_2.fits')[1].data
des_shear = fits.open('data/input/des/y3a2_metacal_v03_shear.fits')[1].data

# Extraire colonnes
RA_des = des_gold['RA']
DEC_des = des_gold['DEC']
z_des = des_gold['DNF_Z']

e1_des = des_shear['e_1']
e2_des = des_shear['e_2']

print(f"DES: {len(RA_des):,} galaxies")
```

---

## ⚠️ PROBLÈMES COURANTS

### Problème 1: Téléchargement Interrompu

```bash
# Utiliser wget avec -c (continue)
wget -c -O fichier.fits URL
```

### Problème 2: Fichier Corrompu

```bash
# Vérifier taille fichier
ls -lh data/input/cosmos/*.fits

# Si trop petit, re-télécharger
rm data/input/cosmos/cosmos_zphot_shapes.fits
wget ...
```

### Problème 3: Accès DES Refusé

- ✅ **Solution**: Créer compte gratuit sur https://des.ncsa.illinois.edu/
- Ou utiliser URLs publiques alternatives (vérifier documentation)

### Problème 4: Espace Disque Insuffisant

```bash
# Vérifier espace disponible
df -h .

# Nettoyer si nécessaire (besoin ~20 GB libres)
```

---

## 🚀 APRÈS LE TÉLÉCHARGEMENT

### 1. Vérifier Données

```bash
python3 verify_data.py
```

### 2. Adapter le Script de Test

```bash
# Modifier scripts/test_weak_lensing_TMT_vs_LCDM.py
# Remplacer section simulation par chargement données réelles
```

### 3. Exécuter Analyse Réelle

```bash
cd scripts
python3 test_weak_lensing_real_data.py
```

### 4. Timeline Attendue

- Téléchargement: **~1-2 heures** (selon connexion)
- Vérification: **~5 min**
- Adaptation script: **~2-3 heures**
- Analyse complète: **~1-2 semaines**
- **RÉSULTAT DÉCISIF**: **4-6 mois**

---

## 📞 SUPPORT

### Si problèmes avec COSMOS:
- Support IRSA: https://irsa.ipac.caltech.edu/docs/help_desk.html
- Email: help@irsa.ipac.caltech.edu

### Si problèmes avec DES:
- Documentation: https://des.ncsa.illinois.edu/releases/y3a2
- Forum: https://des-forum.ncsa.illinois.edu/

### Si problèmes avec le script:
- Issues GitHub du projet
- Email: pierreolivierdespres@gmail.com

---

## ✅ CHECKLIST AVANT ANALYSE

- [ ] Espace disque ≥ 20 GB disponible
- [ ] wget installé (`sudo apt-get install wget`)
- [ ] Python 3.8+ installé
- [ ] astropy installé (`pip install astropy`)
- [ ] Connexion internet stable
- [ ] Patience! (téléchargement ~1-2h)

---

**Prochaine étape**: Lancer `./scripts/download_cosmos_des.sh`

**Bonne chance!** 🚀
