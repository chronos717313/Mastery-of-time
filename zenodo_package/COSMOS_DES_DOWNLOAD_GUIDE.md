# 📥 COSMOS/DES DATA DOWNLOAD GUIDE

**Date**: January 15, 2026
**Objective**: Obtain real data for the θ_halo ↔ θ_neighbor test
**Total size**: ~17 GB (COSMOS ~2 GB + DES ~15 GB)

---

## 🚀 QUICK METHOD (RECOMMENDED)

### Step 1: Create data directory

```bash
# From project root
mkdir -p data/input/cosmos
mkdir -p data/input/des
cd data/input
```

---

## 📦 COSMOS FIELD DATA

### Option A: Direct Download (RECOMMENDED)

```bash
# COSMOS 2020 photometric catalog
wget -O cosmos/COSMOS2020_CLASSIC_R1_v2.1.fits \
  "https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/COSMOS2020_CLASSIC_R1_v2.1.fits.gz"

# Decompress
gunzip cosmos/COSMOS2020_CLASSIC_R1_v2.1.fits.gz

# Weak lensing shapes
wget -O cosmos/cosmos_zphot_shapes.fits \
  "https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits"
```

**Size**: ~2 GB total

---

### Option B: Via IRSA (Web Interface)

1. Go to: https://irsa.ipac.caltech.edu/Missions/cosmos.html
2. Click "Catalogs" → "COSMOS2020"
3. Download:
   - `COSMOS2020_CLASSIC_R1_v2.1.fits` (photometry)
   - `cosmos_zphot_shapes.fits` (weak lensing)

---

### Option C: Via astroquery (Python)

```python
from astroquery.irsa import Irsa

# Download COSMOS catalog
table = Irsa.query_region(
    "COSMOS",
    catalog='cosmos_morphology',
    spatial='Cone',
    radius=2.0  # degrees
)

# Save
table.write('cosmos/cosmos_catalog.fits', format='fits', overwrite=True)
```

---

## 📦 DES Y3 DATA

### Option A: Direct Download (RECOMMENDED)

```bash
# DES Y3 Gold Catalog (positions, masses, redshifts)
wget -O des/y3_gold_2_2.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/gold-2-2/y3_gold_2_2.fits"

# DES Y3 Shear Catalog (weak lensing)
wget -O des/y3a2_metacal_v03_shear.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/shear/y3a2_metacal_v03_shear.fits"
```

**Size**: ~15 GB total
**Time**: ~30-60 min (depending on connection)

---

### Option B: Via DES Data Access Portal

1. Go to: https://des.ncsa.illinois.edu/releases/y3a2
2. Create free account (required)
3. Navigate to: **Y3 Key Catalogs** → **Gold** and **Shear**
4. Download:
   - `y3_gold_2_2.fits` (~8 GB)
   - `y3a2_metacal_v03_shear.fits` (~7 GB)

---

### Option C: Via easyaccess (DES Tool)

```bash
# Install easyaccess
pip install easyaccess

# Connect
easyaccess

# In the easyaccess shell:
> load_table y3_gold_2_2
> save_table y3_gold_2_2.fits
```

---

## 🔍 DATA VERIFICATION

### Verification Script

```bash
# Create verification script
cat > verify_data.py << 'EOF'
#!/usr/bin/env python3
"""Verifies integrity of downloaded COSMOS/DES data"""

from astropy.io import fits
import os

def verify_file(filepath, expected_columns):
    """Verifies that a FITS file contains expected columns"""
    if not os.path.exists(filepath):
        print(f"❌ {filepath}: FILE MISSING")
        return False

    try:
        with fits.open(filepath) as hdul:
            data = hdul[1].data
            cols = data.columns.names

            missing = [c for c in expected_columns if c not in cols]

            print(f"✅ {os.path.basename(filepath)}:")
            print(f"   Rows: {len(data):,}")
            print(f"   Columns: {len(cols)}")

            if missing:
                print(f"   ⚠️  Missing columns: {missing}")
                return False
            else:
                print(f"   ✅ All required columns present")
                return True

    except Exception as e:
        print(f"❌ {filepath}: ERROR - {e}")
        return False

# Verify COSMOS
print("\n" + "="*60)
print("COSMOS VERIFICATION")
print("="*60)

cosmos_cols = ['RA', 'DEC', 'PHOTOZ', 'MASS_BEST', 'e1', 'e2']
verify_file('data/input/cosmos/cosmos_zphot_shapes.fits', cosmos_cols)

# Verify DES
print("\n" + "="*60)
print("DES Y3 VERIFICATION")
print("="*60)

des_gold_cols = ['RA', 'DEC', 'DNF_Z', 'SOF_PSF_MAG_CORRECTED_I']
verify_file('data/input/des/y3_gold_2_2.fits', des_gold_cols)

des_shear_cols = ['ra', 'dec', 'e_1', 'e_2', 'R11', 'R22']
verify_file('data/input/des/y3a2_metacal_v03_shear.fits', des_shear_cols)

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
EOF

# Make executable
chmod +x verify_data.py

# Run
python3 verify_data.py
```

---

## ⚡ QUICK DOWNLOAD (Automatic Script)

```bash
#!/bin/bash
# Automatic COSMOS/DES download script

set -e

echo "📥 DOWNLOADING COSMOS/DES DATA"
echo "===================================="

# Create directories
mkdir -p data/input/cosmos data/input/des
cd data/input

# COSMOS
echo ""
echo "📦 Downloading COSMOS..."
wget -c -O cosmos/cosmos_zphot_shapes.fits.gz \
  "https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits.gz" \
  || echo "⚠️  COSMOS download failed"

if [ -f cosmos/cosmos_zphot_shapes.fits.gz ]; then
    echo "   Decompressing..."
    gunzip -f cosmos/cosmos_zphot_shapes.fits.gz
    echo "   ✅ COSMOS downloaded (~2 GB)"
fi

# DES Y3 Gold
echo ""
echo "📦 Downloading DES Y3 Gold (~8 GB)..."
echo "   ⚠️  This may take 30-60 minutes"
wget -c -O des/y3_gold_2_2.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/gold-2-2/y3_gold_2_2.fits" \
  || echo "⚠️  DES Gold download failed"

# DES Y3 Shear
echo ""
echo "📦 Downloading DES Y3 Shear (~7 GB)..."
wget -c -O des/y3a2_metacal_v03_shear.fits \
  "https://des.ncsa.illinois.edu/releases/y3a2/shear/y3a2_metacal_v03_shear.fits" \
  || echo "⚠️  DES Shear download failed"

echo ""
echo "✅ DOWNLOAD COMPLETE"
echo ""
echo "📂 Files in data/input/"
ls -lh cosmos/ des/

echo ""
echo "🔍 Run verify_data.py to verify integrity"
```

**Save as**: `scripts/download_cosmos_des.sh`

```bash
chmod +x scripts/download_cosmos_des.sh
./scripts/download_cosmos_des.sh
```

---

## 📊 EXPECTED DATA STRUCTURE

After successful download:

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

## 🔧 PYTHON DEPENDENCIES

```bash
# Install required packages
pip3 install astropy numpy scipy matplotlib

# Verify installation
python3 -c "from astropy.io import fits; print('✅ astropy OK')"
```

---

## 📖 DATA USAGE

### Load COSMOS

```python
from astropy.io import fits

# Open COSMOS catalog
cosmos = fits.open('data/input/cosmos/cosmos_zphot_shapes.fits')[1].data

# Extract columns
RA = cosmos['RA']
DEC = cosmos['DEC']
z_phot = cosmos['PHOTOZ']
e1 = cosmos['e1']
e2 = cosmos['e2']

print(f"COSMOS: {len(RA):,} galaxies")
```

### Load DES

```python
# Open DES catalogs
des_gold = fits.open('data/input/des/y3_gold_2_2.fits')[1].data
des_shear = fits.open('data/input/des/y3a2_metacal_v03_shear.fits')[1].data

# Extract columns
RA_des = des_gold['RA']
DEC_des = des_gold['DEC']
z_des = des_gold['DNF_Z']

e1_des = des_shear['e_1']
e2_des = des_shear['e_2']

print(f"DES: {len(RA_des):,} galaxies")
```

---

## ⚠️ COMMON PROBLEMS

### Problem 1: Interrupted Download

```bash
# Use wget with -c (continue)
wget -c -O file.fits URL
```

### Problem 2: Corrupted File

```bash
# Check file size
ls -lh data/input/cosmos/*.fits

# If too small, re-download
rm data/input/cosmos/cosmos_zphot_shapes.fits
wget ...
```

### Problem 3: DES Access Denied

- ✅ **Solution**: Create free account at https://des.ncsa.illinois.edu/
- Or use alternative public URLs (check documentation)

### Problem 4: Insufficient Disk Space

```bash
# Check available space
df -h .

# Clean if necessary (need ~20 GB free)
```

---

## 🚀 AFTER DOWNLOAD

### 1. Verify Data

```bash
python3 verify_data.py
```

### 2. Adapt Test Script

```bash
# Modify scripts/test_weak_lensing_TMT_vs_LCDM.py
# Replace simulation section with real data loading
```

### 3. Run Real Analysis

```bash
cd scripts
python3 test_weak_lensing_real_data.py
```

### 4. Expected Timeline

- Download: **~1-2 hours** (depending on connection)
- Verification: **~5 min**
- Script adaptation: **~2-3 hours**
- Complete analysis: **~1-2 weeks**
- **DECISIVE RESULT**: **4-6 months**

---

## 📞 SUPPORT

### If problems with COSMOS:
- IRSA Support: https://irsa.ipac.caltech.edu/docs/help_desk.html
- Email: help@irsa.ipac.caltech.edu

### If problems with DES:
- Documentation: https://des.ncsa.illinois.edu/releases/y3a2
- Forum: https://des-forum.ncsa.illinois.edu/

### If problems with script:
- Project GitHub issues
- Email: pierreolivierdespres@gmail.com

---

## ✅ CHECKLIST BEFORE ANALYSIS

- [ ] Disk space ≥ 20 GB available
- [ ] wget installed (`sudo apt-get install wget`)
- [ ] Python 3.8+ installed
- [ ] astropy installed (`pip install astropy`)
- [ ] Stable internet connection
- [ ] Patience! (download ~1-2h)

---

**Next step**: Run `./scripts/download_cosmos_des.sh`

**Good luck!** 🚀
