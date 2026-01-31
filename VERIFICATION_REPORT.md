# Rapport de Vérification TMT v2.4
## Pre-Publication Validation Report

**Date**: 30 janvier 2026
**Auteur**: Pierre-Olivier Després Asselin
**Statut**: En cours

---

## 1. Scripts Re-exécutés

### 1.1 test_TMT_v24_SPARC.py
**Statut**: ✅ VALIDÉ

| Métrique | Attendu | Obtenu | Verdict |
|----------|---------|--------|---------|
| Galaxies analysées | 171 | 171 | ✅ |
| Galaxies exclues | 15 | 15 | ✅ |
| Galaxies applicables | 156 | 156 | ✅ |
| Score final | 156/156 (100%) | 156/156 (100%) | ✅ |
| Chi² réduction | 81.2% | 81.2% | ✅ |
| Amélioration médiane | 97.0% | 97.0% | ✅ |

### 1.2 test_complet_TMT_v232.py
**Statut**: ✅ VALIDÉ

| Test | Attendu | Obtenu | Verdict |
|------|---------|--------|---------|
| SPARC | VALIDE | VALIDE | ✅ |
| r_c(M) | VALIDE | VALIDE | ✅ |
| k(M) | VALIDE | VALIDE | ✅ |
| Weak Lensing | VALIDE | VALIDE | ✅ |
| COSMOS2015 | VALIDE | VALIDE | ✅ |
| SNIa | 0.57% préd | 0.57% préd | ✅ |
| ISW | 18.2% préd | 18.2% préd | ✅ |
| H0 | 73.0 km/s/Mpc | 73.0 km/s/Mpc | ✅ |
| **Score Total** | 8/8 (100%) | 8/8 (100%) | ✅ |

### 1.3 investigation_r_c_variation.py
**Statut**: ✅ VALIDÉ

| Métrique | Attendu | Obtenu | Verdict |
|----------|---------|--------|---------|
| Galaxies valides | 103 | 103 | ✅ |
| r_c médiane | ~5.7 kpc | 5.7 kpc | ✅ |
| r_c global | ~10.6 kpc | 10.61 kpc | ✅ |
| Corrélation Pearson r | 0.768 | 0.768 | ✅ |
| p-value | 3×10⁻²¹ | 3.05×10⁻²¹ | ✅ |
| Exposant masse | 0.56 | 0.563 | ✅ |

---

## 2. Cohérence des Paramètres

### 2.1 Paramètres TMT v2.4

| Paramètre | CLAUDE.md | Wiki | zenodo_package | Scripts | Verdict |
|-----------|-----------|------|----------------|---------|---------|
| β_SNIa | 0.001 | 0.001 | 0.001 | 0.001 | ✅ |
| β_H0 | 0.82 | 0.82 | 0.82 | 0.82 | ✅ |
| r_c coefficient | 2.6 kpc | 2.6 kpc | 2.6 kpc | 2.6 kpc | ✅ |
| r_c exponent | 0.56 | 0.56 | 0.56 | 0.56 | ✅ |
| k(M) coefficient | 4.00 | 4.0 | 4.00 | 4.0 | ✅ |
| k(M) exponent | -0.49 | -0.49 | -0.49 | -0.49 | ✅ |
| n (superposition) | 0.75 | 0.75 | 0.75 | 0.75 | ✅ |

### 2.2 Résultats de Validation

| Résultat | CLAUDE.md | Wiki | zenodo_package | Scripts | Verdict |
|----------|-----------|------|----------------|---------|---------|
| SPARC | 156/156 (100%) | 156/156 (100%) | 156/156 (100%) | 156/156 (100%) | ✅ |
| r_c correlation | r=0.768 | r=0.768 | r=0.768 | r=0.768 | ✅ |
| k(M) R² | 0.64 | 0.64 | 0.64 | 0.64 | ✅ |
| Chi² reduction | 81.2% | 81.2% | 81.2% | 81.2% | ✅ |
| SNIa predicted | +0.57% | +0.57% | +0.57% | +0.57% | ✅ |
| SNIa observed | +0.46% | +0.46% | +0.46% | - | ✅ |
| ISW predicted | +18.2% | +18.2% | +18.2% | +18.2% | ✅ |
| ISW observed | +17.9% | +17.9% | +17.9% | - | ✅ |
| H0 resolved | 73.0 | 73.0 | 73.0 | 73.0 | ✅ |

---

## 3. Scripts à Tester

### Restants à vérifier
- [ ] test_TMT_KiDS450.py (Weak Lensing)
- [ ] test_TMT_COSMOS2015.py (Mass-Environment)
- [ ] test_Pantheon_SNIa_environnement.py (SNIa)
- [ ] calculate_ISW_improved.py (ISW Effect)
- [ ] calcul_significativite_TMT_v24.py (p-value)

---

## 4. Problèmes Identifiés et Corrigés

### 4.1 Chemins de Données
**Problème**: Scripts cherchaient données dans `scripts/data/SPARC/` au lieu de `data/SPARC/`

**Scripts corrigés**:
- [x] test_TMT_v24_SPARC.py
- [x] investigation_r_c_variation.py
- [ ] Autres scripts à vérifier

**Solution**: Ajout de chemins multiples pour trouver les données SPARC

---

## 5. Prochaines Étapes

1. [ ] Terminer re-exécution des scripts restants
2. [ ] Corriger les chemins dans tous les scripts
3. [ ] Vérifier cohérence Wiki EN/ES avec FR
4. [ ] Valider que toutes les formules sont identiques
5. [ ] Créer rapport final de validation

---

## 6. Conclusion Préliminaire

**Statut actuel**: Les tests principaux (SPARC, 8 tests complets, r_c investigation) passent avec les valeurs attendues.

**Cohérence**: Tous les paramètres et résultats sont cohérents entre CLAUDE.md, wiki et zenodo_package.

**Actions requises**: Continuer la vérification des scripts secondaires et corriger les chemins de données.

---

*Rapport mis à jour: 30 janvier 2026*
