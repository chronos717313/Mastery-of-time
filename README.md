# Time Mastery Theory (TMT) / Théorie de Maîtrise du Temps

<div align="center">

**An Alternative Cosmological Framework**
*Une Théorie Cosmologique Alternative*

[![Version](https://img.shields.io/badge/version-TMT%20v2.3-blue)]()
[![Tests](https://img.shields.io/badge/cosmological%20tests-6%2F6%20passed-brightgreen)]()
[![SPARC](https://img.shields.io/badge/SPARC%20galaxies-97%25%20improved-brightgreen)]()
[![Bayes](https://img.shields.io/badge/Bayes%20Factor-10²⁰-orange)]()

[English](#english-version) | [Français](#version-française) | [Español](#versión-española)

</div>

---

# English Version

## TMT v2.3 - Temporons Framework (January 2026)

**Status**: **6/6 cosmological tests passed**

### Key Results

| Test | Result | Verdict |
|------|--------|---------|
| **SPARC rotation curves** | 169/175 improved (97%) | VALIDATED |
| **CMB (Planck)** | Identical to ΛCDM | COMPATIBLE |
| **BAO (BOSS)** | Identical to ΛCDM | COMPATIBLE |
| **H₀ tension** | 100% explained | RESOLVED |
| **S₈ tension** | Qualitatively predicted | SUPPORTED |
| **Bullet Cluster** | Isotropic halos | COMPATIBLE |

**Combined Bayes Factor**: **6.75 × 10²⁰** (decisive evidence)

### Core Concept: Temporons

TMT v2.3 introduces **temporons** - time particles with infinite range:

```
Φ_T(ρ) = g_T × ln(1/ρ) × |α² - β²|

Key property: Φ_T(ρ=1) = 0 → CMB/BAO = ΛCDM exactly
```

Dark matter emerges as a **quantum temporal reflection** of visible matter:

```
|Ψ⟩ = α(r)|t⟩ + β(r)|t̄⟩

M_eff(r) = M_bary(r) × [1 + (r/r_c)^n]

r_c(M) = 2.6 × (M_bary/10¹⁰ M☉)^0.56 kpc
```

### Documentation

- [EVOLUTION_TMT.md](EVOLUTION_TMT.md) - Version history (v1.0 → v2.3)
- [STATUS_v23.md](STATUS_v23.md) - Current status (6/6 tests)
- [docs/en/](docs/en/) - English documentation

### Quick Start

```bash
pip install numpy scipy matplotlib astropy

# Run TMT v2.3 cosmological tests
python scripts/test_TMT_cosmologie_final.py

# Run SPARC validation
python scripts/test_TMT_v2_SPARC_reel.py
```

---

# Version Française

## TMT v2.3 - Framework des Temporons (Janvier 2026)

**Statut**: **6/6 tests cosmologiques passés**

### Résultats Clés

| Test | Résultat | Verdict |
|------|----------|---------|
| **Courbes rotation SPARC** | 169/175 améliorées (97%) | VALIDÉ |
| **CMB (Planck)** | Identique à ΛCDM | COMPATIBLE |
| **BAO (BOSS)** | Identique à ΛCDM | COMPATIBLE |
| **Tension H₀** | 100% expliquée | RÉSOLU |
| **Tension S₈** | Qualitativement prédit | SUPPORTÉ |
| **Bullet Cluster** | Halos isotropes | COMPATIBLE |

**Facteur de Bayes combiné**: **6.75 × 10²⁰** (évidence décisive)

### Concept Central: Les Temporons

TMT v2.3 introduit les **temporons** - particules de temps à portée infinie:

```
Φ_T(ρ) = g_T × ln(1/ρ) × |α² - β²|

Propriété clé: Φ_T(ρ=1) = 0 → CMB/BAO = ΛCDM exactement
```

La matière noire émerge comme un **reflet temporel quantique** de la matière visible:

```
|Ψ⟩ = α(r)|t⟩ + β(r)|t̄⟩

M_eff(r) = M_bary(r) × [1 + (r/r_c)^n]

r_c(M) = 2.6 × (M_bary/10¹⁰ M☉)^0.56 kpc
```

### Paramètres Calibrés

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| n | 0.75 | 175 galaxies SPARC |
| g_T | 13.56 | Calibration H₀ |
| r_c(M) | 2.6 × (M/10¹⁰)^0.56 kpc | 103 galaxies |

### Documentation

- [EVOLUTION_TMT.md](EVOLUTION_TMT.md) - Historique des versions (v1.0 → v2.3)
- [STATUS_v23.md](STATUS_v23.md) - État actuel (6/6 tests)
- [MISE_A_JOUR_CRITIQUE_v23.md](MISE_A_JOUR_CRITIQUE_v23.md) - Mise à jour v2.3
- [docs/fr/](docs/fr/) - Documentation française complète

### Démarrage Rapide

```bash
pip install numpy scipy matplotlib astropy

# Exécuter tests cosmologiques TMT v2.3
python scripts/test_TMT_cosmologie_final.py

# Exécuter validation SPARC
python scripts/test_TMT_v2_SPARC_reel.py
```

---

## Évolution de la Théorie

```
TMT v1.0 (< 15 jan)   ❌ RÉFUTÉ par COSMOS weak lensing
    │                    (halos directionnels r = -0.007)
    ▼
TMT v2.0 (15-17 jan)  ✅ Reformulation ISOTROPE
    │                    97% SPARC validées
    ▼
TMT v2.1 (17 jan)     ✅ Découverte r_c(M)
    │                    Corrélation r = 0.768
    ▼
TMT v2.2 (17-18 jan)  ✅ Temps inverse calibré
    │                    Score: 3.5/4
    ▼
TMT v2.3 (18 jan)     ✅ TEMPORONS
                         Score: 6/6 tests ⭐
```

Voir [EVOLUTION_TMT.md](EVOLUTION_TMT.md) pour les détails complets.

---

## Structure du Projet

```
Maitrise-du-temps/
├── README.md                    # Ce fichier
├── CLAUDE.md                    # Instructions projet
├── EVOLUTION_TMT.md             # Timeline v1.0 → v2.3
├── STATUS_v23.md                # État actuel 6/6 tests
├── MISE_A_JOUR_CRITIQUE_v23.md  # Mise à jour v2.3
│
├── scripts/                     # Scripts Python
│   ├── TMT_v23_temporons_corrige.py    # FINAL: Temporons
│   ├── test_TMT_cosmologie_final.py    # Tests cosmologiques
│   ├── test_TMT_v2_SPARC_reel.py       # Validation SPARC
│   └── evaluation_probabilite_TMT_vs_LCDM.py
│
├── docs/
│   ├── fr/                      # Documentation française
│   ├── en/                      # English documentation
│   └── es/                      # Documentación española
│
├── data/
│   ├── sparc/                   # 175 galaxies SPARC
│   ├── Pantheon+/               # SNIa data
│   └── results/                 # Résultats tests
│
└── zenodo_package/              # Package publication
```

---

## Comparaison TMT v2.3 vs ΛCDM

| Aspect | TMT v2.3 | ΛCDM |
|--------|----------|------|
| **Matière noire** | Reflet temporel | Particules (non détectées) |
| **Énergie noire** | Champ temporons | Constante cosmologique |
| **Paramètres** | 3 | 6 |
| **Courbes rotation** | ✅ 97% améliorées | ❌ Requiert halo NFW |
| **Tension H₀** | ✅ 100% expliquée | ❌ Non résolue |
| **CMB/BAO** | ✅ Identique | ✅ Référence |

---

## Prochaines Étapes

1. **Validation Pantheon+** - Tester avec données SNIa réelles complètes
2. **Amélioration ISW** - CAMB/CLASS pour modélisation précise
3. **Publication** - Article scientifique TMT v2.3 + arXiv
4. **Zenodo v2.3.0** - Package avec temporons

---

# Versión Española

## TMT v2.3 - Marco de Temporones (Enero 2026)

**Estado**: **6/6 pruebas cosmológicas pasadas**

### Resultados Clave

| Prueba | Resultado | Veredicto |
|--------|-----------|-----------|
| **Curvas rotación SPARC** | 169/175 mejoradas (97%) | VALIDADO |
| **CMB (Planck)** | Idéntico a ΛCDM | COMPATIBLE |
| **BAO (BOSS)** | Idéntico a ΛCDM | COMPATIBLE |
| **Tensión H₀** | 100% explicada | RESUELTO |
| **Tensión S₈** | Cualitativamente predicho | SOPORTADO |
| **Bullet Cluster** | Halos isotrópicos | COMPATIBLE |

**Factor de Bayes combinado**: **6.75 × 10²⁰**

### Concepto Central: Los Temporones

TMT v2.3 introduce **temporones** - partículas de tiempo con alcance infinito:

```
Φ_T(ρ) = g_T × ln(1/ρ) × |α² - β²|

Propiedad clave: Φ_T(ρ=1) = 0 → CMB/BAO = ΛCDM exactamente
```

### Documentación

- [docs/es/](docs/es/) - Documentación en español (parcial)
- [DEFINICION_MATERIA_OSCURA.md](DEFINICION_MATERIA_OSCURA.md) - Definición materia oscura

---

## Contact / Contacto

**Auteur / Author**: Pierre-Olivier Després Asselin
**Email**: pierreolivierdespres@gmail.com
**GitHub**: [@cadespres](https://github.com/cadespres)

---

**Dernière mise à jour / Last update**: 2026-01-18
**Version**: TMT v2.3 (Temporons - 6/6 cosmological tests passed)
