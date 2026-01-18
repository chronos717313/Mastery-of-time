# 04 - Scripts TMT v2.3

**Version**: TMT v2.3 (Temporons)
**Date**: 18 janvier 2026

---

## Scripts Principaux TMT v2.3

| Script | Fonction | Taille |
|--------|----------|--------|
| `TMT_v23_temporons_corrige.py` | **FINAL**: Temporons ln(1/ρ) | 15.3 KB |
| `TMT_v23_temporons.py` | Temporons (1-ρ) | 15.7 KB |
| `calibrate_TMT_v23_local.py` | Calibration locale | 15.1 KB |
| `calibrate_TMT_v23_cosmologie.py` | Calibration CMB/BAO | 14.0 KB |

---

## Tests Cosmologiques

| Script | Fonction | Taille |
|--------|----------|--------|
| `test_TMT_cosmologie_final.py` | **FINAL**: 6 tests | 13.7 KB |
| `test_TMT_cosmologie_complete.py` | Tests complets | 19.8 KB |
| `test_TMT_cosmologie_v2.py` | Tests v2 | 17.8 KB |

---

## Validation SPARC

| Script | Fonction |
|--------|----------|
| `test_TMT_v2_SPARC_reel.py` | 175 galaxies réelles |
| `test_TMT_v2_superposition.py` | Superposition temporelle |
| `test_TMT_v2_probabilites_quantiques.py` | Probabilités quantiques |
| `investigation_r_c_variation.py` | Investigation r_c(M) |

---

## Prédictions et Analyses

| Script | Fonction |
|--------|----------|
| `test_3_predictions_TMT.py` | 3 prédictions distinctives |
| `test_3_predictions_complete.py` | Prédictions complètes |
| `evaluation_probabilite_TMT_vs_LCDM.py` | Facteurs Bayes |
| `analyse_comparative_realiste_TMT_LCDM.py` | Comparaison réaliste |

---

## Calibrations

| Script | Fonction |
|--------|----------|
| `calibrate_beta_expansion.py` | Calibration β expansion |
| `formulation_temps_inverse.py` | Temps inverse |
| `test_TMT_v21_calibrated.py` | TMT v2.1 |
| `test_TMT_v22_final.py` | TMT v2.2 |

---

## Scripts Utilitaires

| Script | Fonction |
|--------|----------|
| `create_publication_figures.py` | Génère figures |
| `determine_k_coupling_SPARC_full.py` | Calibration k |
| `analyze_pantheon_SNIa.py` | Analyse SNIa |

---

## Données

### SPARC (data/sparc/)
- 175 fichiers `.mrt` (galaxies SPARC)

### Pantheon+ (data/Pantheon+/)
- Données SNIa réelles

### Résultats (data/results/)
- `TMT_v23_final_corrige.txt`
- `TMT_v23_temporons.txt`
- `TMT_v2_SPARC_reel_results.txt`
- `evaluation_probabilite_TMT_LCDM.txt`

---

## Exécution

```bash
# Tests cosmologiques TMT v2.3
python scripts/test_TMT_cosmologie_final.py

# Validation SPARC
python scripts/test_TMT_v2_SPARC_reel.py

# Évaluation probabiliste
python scripts/evaluation_probabilite_TMT_vs_LCDM.py

# Temporons (FINAL)
python scripts/TMT_v23_temporons_corrige.py
```

---

## Dépendances

```bash
pip install numpy scipy matplotlib astropy
```

---

**Dernière mise à jour**: 2026-01-18
