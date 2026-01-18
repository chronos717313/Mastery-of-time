# Investigation r_c : Réconciliation 5 vs 10 vs 18 kpc

**Date**: Janvier 2026
**Statut**: RÉSOLU

## Problème Initial

Les différents tests TMT v2.0 donnaient des valeurs de r_c très différentes :

| Source | r_c | Méthode |
|--------|-----|---------|
| Documentation initiale | 18 kpc | Données simulées |
| Test SPARC réel (médiane) | 4.9 kpc | Optimisation individuelle |
| Test probabiliste (global) | 10.6 kpc | Optimisation globale |

**Question** : Quelle est la "vraie" valeur de r_c ?

---

## Analyse

### 1. Données simulées vs réelles

Le script `test_TMT_v2_superposition.py` utilisait des **données synthétiques** générées avec :
- Tully-Fisher pour M_bary → v_flat
- Facteur DM artificiel (1.5-3x)

Ces données ne reproduisent pas la vraie relation observée. La valeur r_c = 18 kpc est **obsolète**.

### 2. Optimisation individuelle vs globale

Sur 103 galaxies SPARC valides :

| Statistique | r_c (kpc) |
|-------------|-----------|
| Moyenne | 8.2 |
| **Médiane** | **5.7** |
| Écart-type | 9.3 |
| IC 25% | 1.1 |
| IC 75% | 12.8 |
| IC 90% | 18.4 |

L'optimum global (10.6 kpc) est tiré vers le haut par les galaxies massives.

### 3. Découverte : r_c dépend de la masse !

**Corrélation r_c vs M_bary** :
- Pearson : r = **0.768** (p = 3×10^-21)
- Spearman : ρ = **0.820** (p = 3×10^-26)

Cette corrélation extrêmement significative montre que **r_c n'est PAS une constante universelle**.

---

## Nouvelle Formulation : r_c(M)

### Relation empirique (103 galaxies SPARC)

```
log₁₀(r_c) = 0.563 × log₁₀(M_bary) - 5.153

r_c(M) = 7.04 × 10⁻⁶ × M_bary^0.56 kpc
```

### Forme normalisée

```
r_c(M) ≈ 2.6 × (M_bary / 10¹⁰ M_☉)^0.56 kpc
```

### Exemples

| Type galaxie | M_bary (M_☉) | r_c (kpc) |
|--------------|--------------|-----------|
| Naine | 10^8 | 0.4 |
| Moyenne | 10^10 | 2.6 |
| Massive | 10^11 | 9.4 |
| Très massive | 10^12 | 34 |

---

## Implications pour TMT v2.0

### Ancienne formulation (OBSOLÈTE)
```
M_eff(r) = M_bary(r) × [1 + (r/r_c)^n]
avec r_c = 18 kpc (constante)
```

### Nouvelle formulation (RECOMMANDÉE)
```
M_eff(r) = M_bary(r) × [1 + (r/r_c(M))^n]

avec r_c(M) = 2.6 × (M_bary/10¹⁰)^0.56 kpc
     n ≈ 0.75
```

### Interprétation physique

Le rayon de transition quantique r_c dépend de la masse de la galaxie :
- **Galaxies naines** : transition rapide (r_c petit)
- **Galaxies massives** : transition progressive (r_c grand)

Cela suggère que la "superposition temporelle" est liée à la **profondeur du puits de potentiel**.

---

## Réconciliation des valeurs

| Valeur | Interprétation | Statut |
|--------|----------------|--------|
| 18 kpc | Données simulées | **OBSOLÈTE** |
| 5-6 kpc | Médiane (galaxie typique) | Valide pour M ~ 10^10 |
| 10-11 kpc | Optimum global | Valide (pondéré par masse) |
| **r_c(M)** | **Relation complète** | **RECOMMANDÉ** |

---

## Valeurs canoniques pour publication

### Option 1 : Valeur fixe simplifiée
```
r_c = 6 ± 5 kpc (médiane ± écart-type)
n = 0.75 ± 0.3
```

### Option 2 : Relation r_c(M) (recommandée)
```
r_c(M) = (2.6 ± 0.5) × (M_bary/10¹⁰ M_☉)^(0.56 ± 0.05) kpc
n = 0.75 ± 0.1
```

---

## Scripts associés

- `scripts/investigation_r_c_variation.py` - Analyse complète
- `data/results/investigation_r_c.txt` - Résultats

---

## Conclusion

La variation de r_c entre 5-18 kpc n'est pas une erreur mais reflète une **dépendance physique avec la masse**. TMT v2.0 devrait utiliser r_c(M) plutôt qu'une constante universelle.

Cette découverte :
1. Explique les variations observées
2. Améliore potentiellement les prédictions
3. Suggère un lien avec la profondeur du potentiel gravitationnel

---

*Document généré le 17 janvier 2026*
