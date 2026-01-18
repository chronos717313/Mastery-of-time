# Carte Conceptuelle - Théorie de Maîtrise du Temps

**Version**: 1.0
**Date**: 2026-01-17

---

## 🌳 VUE D'ENSEMBLE - ARBRE CONCEPTUEL

```
                     THÉORIE DE MAÎTRISE DU TEMPS (TMT)
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
        FONDATIONS           MÉCANISMES          CONSÉQUENCES
         THÉORIQUES         PHYSIQUES          OBSERVABLES
                │                   │                   │
    ┌───────────┴──────┐   ┌───────┴────────┐  ┌───────┴────────┐
    │                  │   │                │  │                │
CARTOGRAPHIE      LIAISON    MASSE         LOI   MATIÈRE      ÉNERGIE
 DESPRÉS          ASSELIN   DESPRÉS    UNIVERSELLE  NOIRE       NOIRE
(IDT γ)         (Couplage)  (Géométrie)   k(M,f)  (Expliquée) (Expliquée)
```

---

## 🎯 CONCEPTS FONDAMENTAUX

### 1. Cartographie Després (Indice de Distortion Temporelle)

**Concept central**: Le temps s'écoule différemment selon la position dans l'univers

**Formalisation mathématique**:
```
γ_Després(r) = Facteur de Lorentz local
             = dt_local / dt_reference
             = fonction du potentiel gravitationnel Φ(r)
```

**Fichiers clés**:
- `CARTOGRAPHIE_DESPRES.md` - Définition complète
- `docs/fr/01-concepts-fondamentaux/LEXICO_MASA_Y_CARTOGRAFIA_DESPRES.md`
- `scripts/calculs/calcul_temps_local_terre.py` - Implémentation

**Relations**:
- Base de → Liaison Asselin
- Détermine → Masse Després
- Mesure → Distortion temporelle locale

---

### 2. Liaison Asselin (Gravitation par Liaison Temporelle)

**Concept central**: La gravitation est une connexion par temps commun partagé

**Principe**:
```
Deux objets sont liés gravitationnellement
↓
Parce qu'ils partagent un référentiel temporel commun
↓
La force n'est pas transmise, c'est une propriété géométrique du temps
```

**Formalisation**:
```
Liaison(A,B) = ∫∫ γ_Després(r_A, r_B) · ρ(r) dV
Réseau de liaisons = Graphe temporel de l'univers
```

**Fichiers clés**:
- `LIAISON_ASSELIN.md` - Théorie complète
- `RESEAU_LIGNES_ASSELIN.md` - Extension en réseau
- `scripts/calculs/calcul_liaisons_asselin.py` - Calculs

**Relations**:
- Utilise → Cartographie Després
- Génère → Masse Després (effet cumulatif)
- Prédit → Asymétrie des halos (test weak lensing)

---

### 3. Masse Després (Effet Géométrique)

**Concept révolutionnaire**: La "matière noire" est un effet géométrique, pas de la matière

**Formule fondamentale**:
```
M_Després = k · ∫ Φ²(r) dV

Où:
- k = facteur de couplage (dépend de M_bary et f_gas)
- Φ(r) = potentiel gravitationnel newtonien
- L'intégrale est sur tout le volume pertinent
```

**Interprétation**:
```
Matière baryonique crée potentiel Φ
       ↓
Potentiel Φ déforme temps local (γ_Després)
       ↓
Déformation cumulative = Masse Després
       ↓
Apparaît comme "matière noire" dans observations
```

**Fichiers clés**:
- `DEFINITION_MATIERE_NOIRE.md` - Définition complète (FR)
- `DARK_MATTER_DEFINITION.md` - Version anglaise
- `docs/fr/03-matiere-noire/DEFINITION_MATIERE_NOIRE.md`

**Relations**:
- Résulte de → Liaison Asselin
- Paramétrée par → Loi universelle k
- Explique → Courbes de rotation, lentilles gravitationnelles

---

### 4. Loi Universelle k (Découverte Majeure)

**Percée scientifique**: Un seul paramètre k prédit toutes les courbes de rotation

**Formulation**:
```
k(M_bary, f_gas) = k₀ · (M_bary / 10¹⁰ M☉)^α · (1 + f_gas)^β

Paramètres calibrés:
- k₀ = 0.343 ± 0.070  (constante de couplage fondamentale)
- α  = -1.610 ± 0.087 (k décroît avec la masse)
- β  = -3.585 ± 0.852 (k décroît avec fraction gazeuse)
```

**Performance**:
```
R² = 0.9976          (99.76% variance expliquée)
χ²_red = 0.04        (ajustement exceptionnel)
Erreur max = ±8%     (sur 6 galaxies SPARC)
Scatter réduit × 262 (99.6% réduction)
```

**Fichiers clés**:
- `LOI_UNIVERSELLE_k.md` - Dérivation et validation
- `data/results/k_asselin_calibration.txt` - Résultats calibration
- `scripts/determine_k_coupling_SPARC_full.py` - Script calibration

**Relations**:
- Paramétrise → Masse Després
- Remplace → 350+ paramètres ΛCDM
- Prédit → Courbes de rotation sans paramètres libres

---

## 🔬 FORMULATION MATHÉMATIQUE

### Hiérarchie des Équations

```
NIVEAU 1: Relativité Générale (standard)
    Gμν + Λgμν = (8πG/c⁴)Tμν
    ↓
NIVEAU 2: Métrique modifiée par IDT
    ds² = -c²(1 + 2Φ/c²)dt² + (1 - 2Φ/c²)dr²
    γ_Després = (1 - 2Φ/c²)^(-1/2)
    ↓
NIVEAU 3: Masse effective géométrique
    M_eff(r) = M_bary(r) + M_Després(r)
    M_Després = k(M_bary, f_gas) · ∫ Φ²(r) dV
    ↓
NIVEAU 4: Courbes de rotation
    v²(r) = G·M_eff(r) / r
    Prédiction sans paramètres libres
```

### Équations Clés

**1. Masse Després intégrale**
```
M_Després(r) = k · ∫₀ʳ Φ²(r') · 4πr'² dr'

Avec:
Φ(r) = -G·M_bary(r)/r  (potentiel newtonien)
```

**2. Couplage k dépendant de la galaxie**
```
k(M_bary, f_gas) = k₀ · (M_bary/10¹⁰)^(-1.61) · (1+f_gas)^(-3.59)

Physique:
- Galaxies massives → k petit → moins d'effet Després
- Galaxies riches en gaz → k petit → gaz moins couplé
```

**3. Vitesse de rotation totale**
```
v_total²(r) = v_bary²(r) + v_Després²(r)

Où:
v_bary²(r) = G·M_bary(r)/r
v_Després²(r) = G·M_Després(r)/r
```

**4. Expansion locale modifiée (énergie noire)**
```
H(z, ρ) = H₀ √[Ωₘ(1+z)³ + ΩΛ exp(β(1 - ρ/ρ_crit))]

Paramètre:
β = 0.38 ± 0.05 (calibré sur SNIa)

Physique:
- Régions denses → H plus faible (expansion ralentie)
- Vides → H plus élevé (expansion accélérée)
```

**Fichiers clés**:
- `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md` (FR)
- `COMPLETE_MATHEMATICAL_FORMULATION_MT.md` (EN)
- `CADRE_RELATIVITE_GENERALE.md` - Dérivation RG
- `DERIVATION_GEODESIQUES_RG_COMPLETE.md` - Géodésiques

---

## 🌌 EXPLICATIONS DES PHÉNOMÈNES

### Matière Noire = Géométrie

```
OBSERVATIONS                TMT EXPLICATION              FICHIERS
─────────────────────────────────────────────────────────────────
Courbes rotation plates → M_Després(r) compense   → ANALYSE_COURBES_ROTATION.md
                          décroissance M_bary

Lentilles gravit. fortes → Masse totale augmentée  → WEAK_LENSING_TEST_...
                          par M_Després

Amas galaxies (Bullet) → Séparation baryons/      → [Future work]
                         potentiel (M_Després
                         suit le potentiel)

Halos asymétriques → Alignement avec gradient    → PREDICTION_TESTABLE_UNIQUE.md
                     potentiel voisins            COSMOS_DES_TEST_GUIDE.md
                     (Liaison Asselin directionnelle)
```

### Énergie Noire = Variation Locale de H

```
OBSERVATIONS                TMT EXPLICATION              FICHIERS
─────────────────────────────────────────────────────────────────
Accélération expansion → H(ρ) plus élevé dans     → DEFINITION_ENERGIE_NOIRE.md
cosmique (SNIa z>0.5)    vides (β > 0)             MODELE_HYBRIDE_ENERGIE_NOIRE.md

Effet ISW (CMB) → Corrélation modifiée avec     → scripts/calculate_ISW_planck.py
                  densité locale                  RESULTATS_MODELE_HYBRIDE...

Tension H₀ → Moyenne spatiale de H(z,ρ)       → FORMALISATION_H_Z_RHO.md
              varie selon traceur                [Explains ~30% of tension]
```

---

## ✅ VALIDATION EXPÉRIMENTALE

### Phase 1: COMPLÉTÉE ✅

```
TEST                  RÉSULTAT                    FICHIER
──────────────────────────────────────────────────────────────
Calibration loi k → R² = 0.9976, χ²_red = 0.04 → LOI_UNIVERSELLE_k.md
(6 galaxies SPARC)   Toutes ±8% précision

Courbes rotation → Prédictions sans param.     → ANALYSE_COURBES_ROTATION.md
NGC3198, M31, MW    libres valident obs.        data/results/figure3...png

SNIa synthétiques → β = 0.38 ± 0.05           → analyze_pantheon_SNIa.py
(Pantheon data)     Réduit scatter 15%          RESULTATS_MODELE_...

Tests cohérence RG → Formulation rigoureuse    → test_formulations_rigoureuses_RG.py
                     passe tous tests            RESULTATS_DERIVATION_RG.md
```

### Phase 2: EN COURS / PRÉVUE ⏳

```
TEST                  STATUT      PRÉDICTION TMT        FICHIER
────────────────────────────────────────────────────────────────────
Weak Lensing       🟡 CRITIQUE  r(θ_halo, θ_voisin)   COSMOS_DES_TEST_GUIDE.md
COSMOS/DES                      > 0.50 (TMT)          test_weak_lensing_...py
                                vs < 0.20 (ΛCDM)       PREDICTION_TESTABLE_UNIQUE.md

Validation SPARC   🟢 READY     R² > 0.95 sur         PLAN_VALIDATION_...md
complet (175 gal.)              175 galaxies          [Scripts ready]

Effet ISW Planck   🟡 PLANNED   Corrélation voids     calculate_ISW_planck.py
× BOSS voids                    différente ΛCDM       [Needs real data]

Pulsars timing     🟡 FUTURE    Anomalies timing      [Not yet implemented]
milliseconde                    dans amas denses
```

**Fichier synthèse**: `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md`

---

## 📊 COMPARAISON AVEC AUTRES MODÈLES

### Tableau Comparatif

| Aspect | ΛCDM | MOND | TMT |
|--------|------|------|-----|
| **Matière noire** | Particules exotiques | Gravité modifiée | Géométrie temporelle |
| **Énergie noire** | Constante Λ | Non expliquée | H(z,ρ) variable |
| **Nombre paramètres** | 6 cosmologiques + 350+ galaxies | 1 universel (a₀) + 6 cosmo | 4 universels (k₀,α,β,β_DE) |
| **Courbes rotation** | Fit individuel NFW | Loi universelle | Loi universelle k(M,f_gas) |
| **Performance galaxies** | Bon (par construction) | Excellent | Excellent (R²=0.9976) |
| **Amas galaxies** | Excellent | Échec | À tester |
| **Lentilles fortes** | Excellent | Problématique | À tester |
| **CMB** | Parfait | Nécessite DM résiduelle | Compatible (H_eff) |
| **Falsifiabilité** | Difficile | Testée (validée) | **Test binaire weak lensing** |

**Fichiers**:
- `docs/en/05-publications/SCIENTIFIC_ARTICLE_TIME_MASTERY.md` - Section 7
- `COMPARAISON_TMT_LCDM_MOND.md` - [À créer]

---

## 🎯 PRÉDICTIONS TESTABLES

### 1. Weak Lensing - Alignement Halos (CRITIQUE)

**Prédiction TMT**:
```
Corrélation r(θ_halo, θ_voisin) > 0.50

Car:
- Liaison Asselin est directionnelle
- Halos s'alignent avec gradient potentiel voisins
- Effet géométrique, pas dynamique
```

**Prédiction ΛCDM**:
```
Corrélation r < 0.20

Car:
- Halos formés par instabilités gravitationnelles
- Pas de corrélation directionnelle privilégiée
- Alignements aléatoires
```

**Critère décisif**:
- Si r > 0.50 → **TMT VALIDÉE**, ΛCDM réfutée
- Si r < 0.20 → **ΛCDM validé**, TMT réfutée

**Fichiers**:
- `PREDICTION_TESTABLE_UNIQUE.md` (FR/EN)
- `COSMOS_DES_TEST_GUIDE.md` - Méthodologie complète
- `test_weak_lensing_TMT_vs_LCDM.py` - Simulation

---

### 2. Variation H(z,ρ) locale

**Prédiction**:
```
ΔH/H ~ 8% entre vides et filaments

Mesurable avec:
- SNIa dans environnements différents
- Corrélation ISW × densité locale
```

**Fichiers**:
- `FORMALISATION_H_Z_RHO.md`
- `MODELE_HYBRIDE_ENERGIE_NOIRE.md`

---

### 3. Courbes rotation sans paramètres libres

**Prédiction**:
```
Toute galaxie SPARC prédite par k(M_bary, f_gas) seul

Validation en cours sur 175 galaxies
```

**Fichiers**:
- `LOI_UNIVERSELLE_k.md`
- `PLAN_VALIDATION_PROCHAINES_GALAXIES.md`

---

## 🗺️ CHEMINS D'APPRENTISSAGE

### Pour Débutant / Grand Public

1. **Introduction conceptuelle**
   - `docs/fr/00-vulgarisation/` - Guides pédagogiques
   - `CONCEPTS_FONDAMENTAUX.md` - Bases accessibles

2. **Comprendre le problème**
   - `DEFINITION_MATIERE_NOIRE.md` - Qu'est-ce que la matière noire?
   - `DEFINITION_ENERGIE_NOIRE.md` - Qu'est-ce que l'énergie noire?

3. **Solution TMT (simplifié)**
   - `VULGARISATION_LOIS_FONDAMENTALES_MT_MQ.md`

### Pour Étudiant / Chercheur

1. **Fondations théoriques**
   - `CONCEPTS_FONDAMENTAUX.md`
   - `LIAISON_ASSELIN.md`
   - `CARTOGRAPHIE_DESPRES.md`

2. **Mathématiques**
   - `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md`
   - `CADRE_RELATIVITE_GENERALE.md`
   - `DERIVATION_GEODESIQUES_RG_COMPLETE.md`

3. **Validation expérimentale**
   - `LOI_UNIVERSELLE_k.md`
   - `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md`
   - `COSMOS_DES_TEST_GUIDE.md`

4. **Article scientifique**
   - `SCIENTIFIC_ARTICLE_TIME_MASTERY.md` (EN)
   - `ARTICLE_SCIENTIFIQUE_MAITRISE_TEMPS.md` (FR)

### Pour Reproductibilité (Calculs)

1. **Setup environnement**
   - `README.md` - Instructions installation
   - `requirements.txt` - Dépendances Python

2. **Scripts principaux**
   - `scripts/determine_k_coupling_SPARC_full.py` - Calibration k
   - `scripts/create_publication_figures.py` - Figures
   - `scripts/test_weak_lensing_TMT_vs_LCDM.py` - Test critique

3. **Modules de calcul**
   - `scripts/calculs/calcul_courbe_rotation_galaxie.py`
   - `scripts/calculs/calcul_liaisons_asselin.py`

4. **Données**
   - `data/input/` - Données d'entrée
   - `data/results/` - Résultats et figures

---

## 🔗 GRAPHE DE DÉPENDANCES

```
CONCEPTS FONDAMENTAUX
    │
    ├─ Cartographie Després
    │       ├─→ Liaison Asselin
    │       │       ├─→ Masse Després
    │       │       │       └─→ Loi Universelle k
    │       │       │               └─→ Courbes Rotation
    │       │       │
    │       │       └─→ Prédiction Weak Lensing
    │       │
    │       └─→ H(z,ρ) variable
    │               └─→ Énergie Noire expliquée
    │
    └─ Relativité Générale (standard)
            └─→ Métrique Schwarzschild
                    └─→ Géodésiques
                            └─→ Équation Schrödinger-Després

VALIDATION
    │
    ├─ Phase 1 (COMPLÈTE)
    │   ├─ Calibration k (6 galaxies)
    │   ├─ Courbes rotation
    │   ├─ SNIa synthétiques
    │   └─ Tests cohérence RG
    │
    └─ Phase 2 (EN COURS)
        ├─ Weak Lensing COSMOS/DES ★ CRITIQUE ★
        ├─ SPARC complet (175 galaxies)
        ├─ Effet ISW
        └─ Pulsars
```

---

## 📚 INDEX DES FICHIERS CLÉS

### Théorie (Root Level + docs/)

| Concept | Fichier Principal | Fichiers Associés |
|---------|-------------------|-------------------|
| **Cartographie Després** | `CARTOGRAPHIE_DESPRES.md` | `calcul_temps_local_terre.py` |
| **Liaison Asselin** | `LIAISON_ASSELIN.md` | `RESEAU_LIGNES_ASSELIN.md`, `calcul_liaisons_asselin.py` |
| **Masse Després** | `DEFINITION_MATIERE_NOIRE.md` | `DARK_MATTER_DEFINITION.md` (EN) |
| **Loi Universelle k** | `LOI_UNIVERSELLE_k.md` | `determine_k_coupling_SPARC_full.py` |
| **Énergie Noire** | `DEFINITION_ENERGIE_NOIRE.md` | `MODELE_HYBRIDE_ENERGIE_NOIRE.md` |
| **Formulation Math** | `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md` | `CADRE_RELATIVITE_GENERALE.md` |

### Validation et Tests

| Test | Fichier Résultats | Script Associé |
|------|-------------------|----------------|
| **Calibration k** | `LOI_UNIVERSELLE_k.md` | `determine_k_coupling_SPARC_full.py` |
| **Courbes rotation** | `ANALYSE_COURBES_ROTATION.md` | `calcul_courbe_rotation_galaxie.py` |
| **Weak Lensing** | `RESULTATS_TEST_COSMOS_DES.md` | `test_weak_lensing_TMT_vs_LCDM.py` |
| **SNIa** | `RESULTATS_MODELE_HYBRIDE_...` | `analyze_pantheon_SNIa.py` |
| **Synthèse tests** | `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md` | - |

### Publication

| Document | Langue | Fichier |
|----------|--------|---------|
| **Article scientifique** | EN | `SCIENTIFIC_ARTICLE_TIME_MASTERY.md` |
| **Article scientifique** | FR | `ARTICLE_SCIENTIFIQUE_MAITRISE_TEMPS.md` |
| **Prédiction testable** | EN/FR | `UNIQUE_TESTABLE_PREDICTION.md` / `PREDICTION_TESTABLE_UNIQUE.md` |
| **Guide soumission** | FR | `SUBMISSION_READY.md`, `ZENODO_SUBMISSION_GUIDE.md` |

---

## 🎓 GLOSSAIRE RAPIDE

| Terme | Définition | Fichier Détails |
|-------|------------|-----------------|
| **γ_Després** | Facteur Lorentz local (IDT) | `CARTOGRAPHIE_DESPRES.md` |
| **k** | Facteur couplage temporel | `LOI_UNIVERSELLE_k.md` |
| **M_Després** | Masse géométrique (≈ matière noire) | `DEFINITION_MATIERE_NOIRE.md` |
| **Liaison Asselin** | Couplage gravitationnel temporel | `LIAISON_ASSELIN.md` |
| **H(z,ρ)** | Paramètre Hubble local | `FORMALISATION_H_Z_RHO.md` |
| **IDT** | Indice de Distortion Temporelle | `APPROCHE_HYBRIDE_IDT.md` |
| **SPARC** | Catalog de courbes rotation | `LOI_UNIVERSELLE_k.md` |
| **Weak Lensing** | Lentilles gravitationnelles faibles | `COSMOS_DES_TEST_GUIDE.md` |

---

**Dernière mise à jour**: 2026-01-17
**Maintenu par**: Projet TMT
**Statut**: 🟢 Actif et à jour
