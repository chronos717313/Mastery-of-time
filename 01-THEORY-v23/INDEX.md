# 01 - Théorie TMT v2.3

**Version**: TMT v2.3 (Temporons)
**Date**: 18 janvier 2026

---

## Formulation Centrale

### Superposition Temporelle
```
|Ψ⟩ = α(r)|t⟩ + β(r)|t̄⟩

|α(r)|² = 1 / (1 + (r/r_c)^n)
|β(r)|² = (r/r_c)^n / (1 + (r/r_c)^n)

M_eff(r) = M_bary(r) × [1 + (r/r_c)^n]
```

### Champ de Temporons
```
Φ_T(ρ) = g_T × ln(1/ρ) × |α² - β²|

H²(z,ρ) = H₀² × [Ωₘ(1+z)³ + ΩΛ × (1 + Φ_T)]

Propriété clé: Φ_T(ρ=1) = 0 → CMB/BAO = ΛCDM
```

### Rayon Critique
```
r_c(M) = 2.6 × (M_bary/10¹⁰ M☉)^0.56 kpc
```

---

## Documents Théoriques

### Concepts Fondamentaux (docs/fr/01-concepts-fondamentaux/)

| Document | Description |
|----------|-------------|
| `CARTOGRAPHIE_DESPRES.md` | Cartographie distorsion temporelle |
| `SUPERPOSITION_TEMPORELLE.md` | Superposition forward/backward |

### Formulation Mathématique (docs/fr/02-formulation-mathematique/)

| Document | Description |
|----------|-------------|
| `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md` | Formulation complète |
| `CADRE_RELATIVITE_GENERALE.md` | Cadre RG |
| `DERIVATION_GEODESIQUES_RG_COMPLETE.md` | Géodésiques |

### Théories (docs/fr/theories/)

| Document | Description |
|----------|-------------|
| `LIAISON_ASSELIN.md` | Liaison temporelle (scalaire v2.0+) |
| `FORMULATION_MATHEMATIQUE.md` | Équations principales |

### Zenodo Package

| Document | Description |
|----------|-------------|
| `zenodo_package/TEMPORONS_THEORY.md` | Théorie temporons (EN) |
| `zenodo_package/TEMPORAL_SUPERPOSITION.md` | Superposition (EN) |
| `zenodo_package/COMPLETE_MATHEMATICAL_FORMULATION_MT.md` | Formulation (EN) |

---

## Paramètres Calibrés

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| n | 0.75 | 175 galaxies SPARC |
| g_T | 13.56 | Calibration H₀ |
| r_c coefficient | 2.6 kpc | 103 galaxies |
| r_c exposant | 0.56 | Régression |

---

## Scripts Théoriques

| Script | Fonction |
|--------|----------|
| `scripts/TMT_v23_temporons_corrige.py` | FINAL: Temporons ln(1/ρ) |
| `scripts/formulation_temps_inverse.py` | Temps inverse |

---

**Dernière mise à jour**: 2026-01-18
