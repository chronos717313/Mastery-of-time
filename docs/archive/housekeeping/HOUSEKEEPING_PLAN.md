# Plan de Réorganisation - Maîtrise du Temps

**Date**: 2026-01-17
**Branch**: `housekeeping/organize-structure`
**Objectif**: Organiser la hiérarchie des dossiers et relier les idées générales

---

## 📊 ANALYSE DE LA STRUCTURE ACTUELLE

### Problèmes Identifiés

1. **Root Directory Surchargé**
   - 109+ fichiers markdown/Python directement à la racine
   - Mélange de documents de travail, théories, et scripts
   - Difficulté de navigation et de découverte

2. **Duplication de Contenu**
   - Documents similaires en root et dans `/docs/`
   - Versions multiples de formulations mathématiques
   - Redondance entre `PUBLICATION_ZENODO/` et `zenodo_package/`

3. **Organisation Incomplète**
   - Documentation espagnole partielle (8 fichiers vs 45 FR, 14 EN)
   - Fichiers obsolètes mélangés avec documents actifs
   - Plans d'action et feuilles de route dispersés

4. **Manque de Navigation**
   - Pas d'index central reliant les concepts
   - Relations entre théories non explicites
   - Progression du projet difficile à suivre

---

## 🎯 STRUCTURE PROPOSÉE

### Niveau 1: Organisation par Phase de Projet

```
Maitrise-du-temps/
│
├── 00-PROJECT-MANAGEMENT/           # Nouveau: Gestion du projet
│   ├── ROADMAP.md                   # Feuille de route globale
│   ├── STATUS.md                    # État actuel du projet
│   ├── NAVIGATION_GUIDE.md          # Guide de navigation
│   ├── CONCEPT_MAP.md               # Carte conceptuelle
│   ├── PLAN_ACTION.md               # Déplacé de docs/fr/communications/
│   ├── TRAVAIL_COMPLET_RESUME.md    # Déplacé de root
│   ├── OU_PUBLIER_MAINTENANT.md     # Déplacé de root
│   └── HOUSEKEEPING_PLAN.md         # Ce document
│
├── 01-THEORY/                       # Nouveau: Théories fondamentales
│   ├── core-concepts/               # Concepts de base
│   │   ├── CONCEPTS_FONDAMENTAUX.md
│   │   ├── LIAISON_ASSELIN.md
│   │   ├── CARTOGRAPHIE_DESPRES.md
│   │   ├── SUPERPOSITION_TEMPORELLE.md
│   │   └── TEMPORONS_THEORY.md
│   ├── mathematical-framework/      # Cadre mathématique
│   │   ├── FORMULATION_MATHEMATIQUE_COMPLETE_MT.md
│   │   ├── CADRE_RELATIVITE_GENERALE.md
│   │   ├── EQUATION_SCHRODINGER_DESPRES.md
│   │   └── LOI_UNIVERSELLE_k.md
│   ├── dark-matter-energy/          # Matière et énergie noires
│   │   ├── DEFINITION_MATIERE_NOIRE.md
│   │   ├── DEFINITION_ENERGIE_NOIRE.md
│   │   └── MODELE_HYBRIDE_ENERGIE_NOIRE.md
│   └── advanced-theories/           # Théories avancées
│       ├── RESEAU_LIGNES_ASSELIN.md
│       ├── DERIVATION_GEODESIQUES_RG_COMPLETE.md
│       ├── LIENS_RG_ET_ELECTROMAGNETISME.md
│       └── [autres théories]
│
├── 02-VALIDATION/                   # Nouveau: Tests et validation
│   ├── calibration/                 # Calibration des paramètres
│   │   ├── LOI_UNIVERSELLE_k.md
│   │   ├── k_asselin_calibration.txt
│   │   └── CONSTANTES_MANQUANTES.md
│   ├── test-results/                # Résultats des tests
│   │   ├── SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md
│   │   ├── RESULTATS_TEST_COSMOS_DES.md
│   │   ├── TEST_EXPERIMENTAL_FINAL.md
│   │   └── BILAN_CRITIQUE_8_TESTS.md
│   ├── analyses/                    # Analyses détaillées
│   │   ├── ANALYSE_COURBES_ROTATION.md
│   │   ├── ANALYSE_STATISTIQUE_PROBABILITES.md
│   │   ├── ANALYSE_ECHELLES_GALACTIQUES.md
│   │   └── [autres analyses]
│   └── methodology/                 # Méthodologies de test
│       ├── COSMOS_DES_TEST_GUIDE.md
│       ├── PREDICTION_TESTABLE_UNIQUE.md
│       └── OBSERVATIONS_ALIGNEMENT_HALOS.md
│
├── 03-PUBLICATION/                  # Nouveau: Publications et soumissions
│   ├── articles/                    # Articles scientifiques
│   │   ├── SCIENTIFIC_ARTICLE_TIME_MASTERY.md (EN)
│   │   ├── ARTICLE_SCIENTIFIQUE_MAITRISE_TEMPS.md (FR)
│   │   └── ARTICLE_PUBLICATION_TMT.md
│   ├── figures/                     # Figures de publication
│   │   ├── publication/             # Figures principales
│   │   │   ├── figure1_k_vs_mass.png
│   │   │   ├── figure2_k_correlation.png
│   │   │   ├── figure3_rotation_curves.png
│   │   │   └── figure4_summary.png
│   │   └── supplementary/           # Figures supplémentaires
│   │       └── [autres figures]
│   ├── zenodo/                      # Package Zenodo consolidé
│   │   ├── SCIENTIFIC_ARTICLE_TIME_MASTERY.md
│   │   ├── COMPLETE_MATHEMATICAL_FORMULATION_MT.md
│   │   ├── DARK_MATTER_DEFINITION.md
│   │   ├── DARK_ENERGY_DEFINITION.md
│   │   ├── UNIQUE_TESTABLE_PREDICTION.md
│   │   ├── METADATA.json
│   │   ├── CITATION.cff
│   │   └── LICENSE
│   └── submission-guides/           # Guides de soumission
│       ├── SUBMISSION_READY.md
│       ├── ZENODO_SUBMISSION_GUIDE.md
│       ├── ZENODO_UPLOAD_INSTRUCTIONS.md
│       └── FIGURE_SPECIFICATIONS.md
│
├── 04-COMPUTATION/                  # Nouveau: Scripts organisés
│   ├── main-scripts/                # Scripts principaux
│   │   ├── create_publication_figures.py
│   │   ├── test_weak_lensing_TMT_vs_LCDM.py
│   │   ├── analyze_pantheon_SNIa.py
│   │   └── [autres scripts principaux]
│   ├── calculations/                # Modules de calcul
│   │   ├── calcul_liaisons_asselin.py
│   │   ├── calcul_courbe_rotation_galaxie.py
│   │   ├── calcul_temps_local_terre.py
│   │   └── [autres calculs]
│   ├── tests/                       # Suite de tests
│   │   ├── test_formulations_rigoureuses_RG.py
│   │   ├── test_d_eff_variable_densite.py
│   │   └── [autres tests]
│   ├── data-acquisition/            # Acquisition de données
│   │   ├── download_cosmos_auto.py
│   │   ├── download_cosmos_simple.py
│   │   ├── download_cosmos_des.sh
│   │   └── convert_cosmos_tbl_to_fits.py
│   └── utilities/                   # Utilitaires
│       └── [scripts utilitaires]
│
├── 05-DATA/                         # Données (structure existante)
│   ├── input/
│   └── results/
│
├── docs/                            # Documentation multilingue (structure existante améliorée)
│   ├── fr/                          # Documentation française
│   │   ├── 00-vulgarisation/
│   │   ├── 01-concepts-fondamentaux/
│   │   ├── 02-formulation-mathematique/
│   │   ├── 03-matiere-noire/
│   │   ├── 04-plans-recherche/
│   │   ├── 05-publications/
│   │   ├── INDEX.md                 # Nouveau: Index de navigation
│   │   └── GLOSSAIRE.md             # Nouveau: Glossaire des termes
│   ├── en/                          # Documentation anglaise
│   │   ├── 01-core-concepts/
│   │   ├── 02-mathematical-formulation/
│   │   ├── 03-dark-matter/
│   │   ├── 04-research-plans/
│   │   ├── 05-publications/
│   │   ├── INDEX.md                 # Nouveau
│   │   └── GLOSSARY.md              # Nouveau
│   └── es/                          # Documentation espagnole
│       ├── 01-conceptos-fundamentales/
│       ├── 02-formulacion-matematica/
│       ├── 03-materia-oscura/
│       ├── 04-planes-investigacion/
│       ├── INDEX.md                 # Nouveau
│       └── GLOSARIO.md              # Nouveau
│
├── archive/                         # Archives (structure existante)
│   ├── obsolete/
│   ├── old-versions/                # Nouveau: Anciennes versions
│   └── deprecated/                  # Nouveau: Déprécié
│
└── README.md                        # README principal mis à jour
```

---

## 🔗 CARTE CONCEPTUELLE

### Hiérarchie des Idées Principales

```
THÉORIE DE MAÎTRISE DU TEMPS (TMT)
│
├─── CONCEPTS FONDAMENTAUX
│    ├── Cartographie Després (Indice de Distortion Temporelle)
│    ├── Liaison Asselin (Gravitation par liaison temporelle)
│    ├── Superposition Temporelle (Temps avant + arrière)
│    └── Temporons (Quanta de temps)
│
├─── FORMULATION MATHÉMATIQUE
│    ├── Cadre Relativité Générale
│    │   ├── Métrique de Schwarzschild modifiée
│    │   ├── Dérivation géodésiques
│    │   └── Liens avec électromagnétisme
│    ├── Masse Després: M_Després = k · ∫ Φ²(r) dV
│    ├── Loi Universelle k: k(M_bary, f_gas) = k₀·M^α·(1+f_gas)^β
│    │   ├── k₀ = 0.343 ± 0.070 (constante fondamentale)
│    │   ├── α = -1.610 ± 0.087 (exposant masse)
│    │   └── β = -3.585 ± 0.852 (exposant gaz)
│    └── Équation Schrödinger-Després
│
├─── EXPLICATIONS PHÉNOMÈNES
│    ├── Matière Noire = Effet géométrique (M_Després)
│    │   ├── Courbes de rotation galactiques
│    │   ├── Lentilles gravitationnelles
│    │   └── Amas de galaxies
│    └── Énergie Noire = Variation locale H(z,ρ)
│        ├── Modèle hybride expansion
│        ├── Paramètre β = 0.38
│        └── Effet ISW modifié
│
├─── VALIDATION EXPÉRIMENTALE
│    ├── Tests Réalisés (Phase 1 COMPLÈTE)
│    │   ├── Calibration loi k (6 galaxies SPARC)
│    │   │   └── R² = 0.9976, χ²_red = 0.04
│    │   ├── Courbes de rotation (±8% précision)
│    │   └── Supernovae synthétiques (Pantheon)
│    └── Tests Prévus (Phase 2)
│        ├── Weak Lensing COSMOS/DES (TEST DÉCISIF)
│        │   ├── Prédiction: r > 0.50 (TMT) vs r < 0.20 (ΛCDM)
│        │   └── Timeline: 6 mois
│        ├── Validation SPARC complète (175 galaxies)
│        ├── Effet ISW (Planck × BOSS voids)
│        └── Pulsars milliseconde
│
├─── COMPARAISON MODÈLES
│    ├── ΛCDM: 350+ paramètres (ajustements individuels)
│    ├── MOND: 1 paramètre universel (a₀)
│    └── TMT: 4 paramètres universels (k₀, α, β, β_DE)
│        └── Réduction facteur 100 vs ΛCDM
│
└─── PUBLICATION ET DIFFUSION
     ├── Articles scientifiques (EN/FR prêts)
     ├── Package Zenodo (DOI permanent)
     ├── Soumission ApJ/MNRAS
     └── Vulgarisation (3 langues)
```

---

## 📋 ACTIONS DE RÉORGANISATION

### Phase 1: Création de la Structure (30 min)

1. **Créer les nouveaux dossiers**
   ```bash
   mkdir -p 00-PROJECT-MANAGEMENT
   mkdir -p 01-THEORY/{core-concepts,mathematical-framework,dark-matter-energy,advanced-theories}
   mkdir -p 02-VALIDATION/{calibration,test-results,analyses,methodology}
   mkdir -p 03-PUBLICATION/{articles,figures/{publication,supplementary},zenodo,submission-guides}
   mkdir -p 04-COMPUTATION/{main-scripts,calculations,tests,data-acquisition,utilities}
   mkdir -p archive/{old-versions,deprecated}
   ```

2. **Déplacer les fichiers de gestion de projet**
   - `TRAVAIL_COMPLET_RESUME.md` → `00-PROJECT-MANAGEMENT/`
   - `OU_PUBLIER_MAINTENANT.md` → `00-PROJECT-MANAGEMENT/`
   - `docs/fr/communications/PLAN_ACTION.md` → `00-PROJECT-MANAGEMENT/`
   - `SUBMISSION_READY.md` → `03-PUBLICATION/submission-guides/`

3. **Organiser les théories**
   - Déplacer concepts fondamentaux → `01-THEORY/core-concepts/`
   - Déplacer formulations mathématiques → `01-THEORY/mathematical-framework/`
   - Déplacer définitions matière/énergie noires → `01-THEORY/dark-matter-energy/`

4. **Organiser les validations**
   - Déplacer résultats de tests → `02-VALIDATION/test-results/`
   - Déplacer analyses → `02-VALIDATION/analyses/`
   - Déplacer méthodologies → `02-VALIDATION/methodology/`

5. **Consolider les publications**
   - Fusionner `PUBLICATION_ZENODO/` et `zenodo_package/` → `03-PUBLICATION/zenodo/`
   - Déplacer figures → `03-PUBLICATION/figures/`
   - Regrouper guides de soumission → `03-PUBLICATION/submission-guides/`

6. **Réorganiser les scripts**
   - `scripts/*.py` (principaux) → `04-COMPUTATION/main-scripts/`
   - `scripts/calculs/` → `04-COMPUTATION/calculations/`
   - `scripts/tests/` → `04-COMPUTATION/tests/`
   - Scripts téléchargement → `04-COMPUTATION/data-acquisition/`

### Phase 2: Création de Documents de Navigation (45 min)

1. **Créer ROADMAP.md** (feuille de route globale)
   - Vision du projet
   - Phases complétées et en cours
   - Timeline future

2. **Créer STATUS.md** (état actuel)
   - Statut par composante
   - Métrique de complétion
   - Prochaines étapes critiques

3. **Créer NAVIGATION_GUIDE.md**
   - Guide par objectif utilisateur
   - Index des documents clés
   - Chemins d'apprentissage

4. **Créer CONCEPT_MAP.md**
   - Diagramme des relations conceptuelles
   - Liens entre théories
   - Dépendances entre composantes

5. **Créer INDEX.md pour chaque langue**
   - Index alphabétique des concepts
   - Index par catégorie
   - Références croisées

6. **Créer GLOSSARY.md / GLOSSAIRE.md / GLOSARIO.md**
   - Termes techniques définis
   - Notation mathématique
   - Acronymes

### Phase 3: Mise à Jour du README (15 min)

1. **Section "Structure du Projet"**
   - Explication de l'organisation
   - Description de chaque dossier principal
   - Où trouver quoi

2. **Section "Démarrage Rapide"**
   - Pour lecteurs généraux
   - Pour chercheurs
   - Pour reproductibilité

3. **Section "Statut du Projet"**
   - Phase actuelle
   - Lien vers STATUS.md
   - Badges de statut

### Phase 4: Nettoyage et Archive (30 min)

1. **Identifier les doublons**
   - Comparer PUBLICATION_ZENODO/ vs zenodo_package/
   - Identifier les versions obsolètes
   - Marquer pour archivage

2. **Archiver les fichiers obsolètes**
   - Déplacer vers `archive/old-versions/`
   - Ajouter fichier ARCHIVE_LOG.md
   - Documenter raison d'archivage

3. **Nettoyer root directory**
   - Ne garder que: README, LICENSE, CLAUDE.md, .gitignore
   - Tout le reste déplacé dans structure organisée

---

## 🎯 BÉNÉFICES ATTENDUS

### Navigation Améliorée
- ✅ Trouvez n'importe quel concept en <30 secondes
- ✅ Comprenez les relations entre théories
- ✅ Suivez le fil logique du projet

### Maintenance Simplifiée
- ✅ Ajoutez de nouveaux documents au bon endroit
- ✅ Évitez la duplication
- ✅ Gardez la structure propre

### Collaboration Facilitée
- ✅ Nouveaux contributeurs s'orientent rapidement
- ✅ Documentation claire par langue
- ✅ Reproductibilité des résultats

### Publication Professionnelle
- ✅ Structure digne d'un projet académique
- ✅ Séparation claire travail/publication
- ✅ Archives traçables

---

## ⏱️ TIMELINE D'EXÉCUTION

| Phase | Temps Estimé | Dépendances |
|-------|-------------|-------------|
| 1. Création structure | 30 min | Aucune |
| 2. Documents navigation | 45 min | Phase 1 |
| 3. Mise à jour README | 15 min | Phases 1-2 |
| 4. Nettoyage archives | 30 min | Phase 1 |
| **TOTAL** | **2h00** | - |

---

## 🚦 NEXT STEPS

### Immédiat (Aujourd'hui)
1. ✅ Review de ce plan par l'utilisateur
2. Exécuter Phase 1 (création structure)
3. Exécuter Phase 2 (documents navigation)

### Court terme (Cette semaine)
4. Exécuter Phase 3 (README)
5. Exécuter Phase 4 (nettoyage)
6. Commit et merge de la branche housekeeping

### Moyen terme (Ce mois)
7. Compléter traductions espagnoles
8. Créer diagrammes visuels de la carte conceptuelle
9. Ajouter tutoriels vidéo/interactifs

---

## 📊 MÉTRIQUES DE SUCCÈS

- [ ] Tous les fichiers root déplacés (sauf README, LICENSE, etc.)
- [ ] Structure à 5 niveaux maximum de profondeur
- [ ] Index et glossaire disponibles en 3 langues
- [ ] Temps de navigation vers n'importe quel concept: <30s
- [ ] Aucune duplication de contenu
- [ ] Archives documentées avec raisons

---

**Créé par**: Claude Code
**Date**: 2026-01-17
**Branch**: `housekeeping/organize-structure`
**Statut**: 🟡 EN RÉVISION - Awaiting approval
