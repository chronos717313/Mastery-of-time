# TMT v2.4 Website Update - Progress Report

**Date**: 2026-02-01
**Objective**: Harmonize all formulas with TMT v2.4 validated parameters

---

## COMPLETED TASKS

### 1. Rotation Curves Generation Script
- **File**: `scripts/tools/generate_rotation_curves_v24.py`
- **Status**: CREATED
- **Features**:
  - Generates publication-quality figures with 3 curves (TMT black, Kepler yellow, k blue)
  - Uses 6 representative SPARC galaxies (DDO154, NGC6503, NGC2403, NGC3198, F563-1, UGC2885)
  - Outputs PNG 300 DPI to all 3 language image folders
  - Includes complete references and TMT v2.4 parameters

### 2. French Rotation Curves Page
- **File**: `docs/wiki/docs/validation/courbes_rotation/index.md`
- **Status**: REWRITTEN with TMT v2.4 parameters
- **Content**:
  - k(M) = 4.00 x (M/10^10)^(-0.49), R² = 0.64
  - r_c(M,Σ) = 2.6 x (M/10^10)^0.56 x (Σ/100)^-0.3 kpc
  - Score: 156/156 (100%)
  - Complete references (SPARC, theoretical, Zenodo)
  - Mathematical derivations

### 3. English Galactic Scale Page
- **File**: `docs/wiki/docs/en/validation/galactic_scale/index.md`
- **Status**: REWRITTEN with TMT v2.4 parameters
- **Content**: Same as French, translated to English

### 4. Spanish Galactic Scale Page
- **File**: `docs/wiki/docs/es/validacion/galactic_scale/index.md`
- **Status**: REWRITTEN with TMT v2.4 parameters
- **Content**: Same as French, translated to Spanish

### 5. Reproduction Script
- **File**: `scripts/reproduce_TMT_v24.py`
- **Status**: CREATED
- **Features**:
  - Downloads SPARC data from VizieR (--download flag)
  - Applies TMT v2.4 filters (baryonic threshold, LSB correction, irregular exclusion)
  - Calculates k and r_c for each galaxy
  - Generates validation report
  - Outputs expected: 156/156 (100%), R²=0.64, r=0.768

### 6. Scripts Reproduction Documentation
- **File**: `docs/wiki/docs/validation/scripts_reproduction.md`
- **Status**: UPDATED with TMT v2.4
- **Content**:
  - New script table with correct parameters
  - Complete data sources with DOIs
  - Step-by-step reproduction instructions
  - Bibliography references

### 7. Figure Generation
- **Status**: EXECUTED
- **Output files created**:
  - `docs/wiki/docs/validation/courbes_rotation/images/figure_rotation_curves_v24.png`
  - `docs/wiki/docs/en/validation/galactic_scale/images/figure_rotation_curves_v24.png`
  - `docs/wiki/docs/es/validacion/galactic_scale/images/figure_rotation_curves_v24.png`

---

## REMAINING TASKS

### 1. Verify Generated Images - DONE
- All 3 PNG files created successfully:
  - `docs/wiki/docs/validation/courbes_rotation/images/figure_rotation_curves_v24.png`
  - `docs/wiki/docs/en/validation/galactic_scale/images/figure_rotation_curves_v24.png`
  - `docs/wiki/docs/es/validacion/galactic_scale/images/figure_rotation_curves_v24.png`

### 2. Update Image References - DONE
- Pages already reference the new filename `figure_rotation_curves_v24.png`

### 3. Test MkDocs Build - OPTIONAL
```bash
cd docs/wiki
mkdocs serve
```

### 4. Check Other Pages - DONE
- `docs/wiki/docs/index.md` - Already has correct TMT v2.4 values
- `docs/wiki/docs/validation/index.md` - Already correct
- No outdated parameters found (searched for 0.9894, 6.10, 402/407, 98.8%)

### 5. Git Commit (when user requests)
```bash
git add scripts/tools/generate_rotation_curves_v24.py
git add scripts/reproduce_TMT_v24.py
git add docs/wiki/docs/validation/courbes_rotation/index.md
git add docs/wiki/docs/en/validation/galactic_scale/index.md
git add docs/wiki/docs/es/validacion/galactic_scale/index.md
git add docs/wiki/docs/validation/scripts_reproduction.md
git add docs/wiki/docs/validation/courbes_rotation/images/figure_rotation_curves_v24.png
git add docs/wiki/docs/en/validation/galactic_scale/images/figure_rotation_curves_v24.png
git add docs/wiki/docs/es/validacion/galactic_scale/images/figure_rotation_curves_v24.png
```

---

## TMT v2.4 PARAMETERS REFERENCE

| Parameter | Formula | Value |
|-----------|---------|-------|
| k(M) | 4.00 x (M/10^10)^(-0.49) | R² = 0.64 |
| r_c(M,Σ) | 2.6 x (M/10^10)^0.56 x (Σ/100)^-0.3 kpc | r = 0.768 |
| n | 0.5 | fixed |
| Baryonic threshold | chi2_Newton/chi2_TMT < 1.1 | 27 galaxies |
| Score | 156/156 | 100% |
| Significance | p = 10^-112 | >15 sigma |

---

## FILES MODIFIED/CREATED

| File | Action |
|------|--------|
| `scripts/tools/generate_rotation_curves_v24.py` | NEW |
| `scripts/reproduce_TMT_v24.py` | NEW |
| `docs/wiki/docs/validation/courbes_rotation/index.md` | REWRITTEN |
| `docs/wiki/docs/en/validation/galactic_scale/index.md` | REWRITTEN |
| `docs/wiki/docs/es/validacion/galactic_scale/index.md` | REWRITTEN |
| `docs/wiki/docs/validation/scripts_reproduction.md` | UPDATED |
| `docs/wiki/docs/*/images/figure_rotation_curves_v24.png` | GENERATED |
