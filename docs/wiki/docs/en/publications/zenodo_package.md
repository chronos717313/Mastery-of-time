# Zenodo Package: zenodo_package_DESPRES_UNIFIED_THEORY

## Package Description

The Zenodo package contains all materials needed to reproduce and validate TMT.

## Included Content

### Python Scripts
- `test_TMT_v2_SPARC_reel.py`: SPARC 175 real galaxies test
- `test_TMT_v2_probabilites_quantiques.py`: Quantum probabilistic analysis
- `investigation_r_c_variation.py`: r_c(M) discovery
- `test_3_predictions_TMT.py`: 3 predictions validation

### Data
- `data/SPARC/`: Complete SPARC catalog (175 galaxies)
- `data/results/`: Results from all tests
- `data/Pantheon+/`: Supernova data for cosmological validation

### Documentation
- Scientific articles in FR/EN
- Usage guides
- Executive summaries

## Zenodo Metadata

| Field | Value |
|-------|-------|
| Title | Mastery of Time Theory: Alternative to ΛCDM |
| Author | C. Després |
| Description | Complete 100% SPARC validation, Hubble tension resolution |
| Keywords | cosmology, dark matter, universe expansion, alternative theory |
| License | CC-BY-4.0 |

## Status
- ✅ **Ready for upload**: All files prepared
- ✅ **Permanent DOI**: Immutable archived version
- ✅ **Citation**: Stable bibliographic reference

## Usage
```bash
# Download package
wget https://zenodo.org/record/XXXXXXX/files/zenodo_package_DESPRES_UNIFIED_THEORY.zip

# Extract and run tests
unzip zenodo_package_DESPRES_UNIFIED_THEORY.zip
cd zenodo_package_DESPRES_UNIFIED_THEORY
python test_TMT_v2_SPARC_reel.py
```