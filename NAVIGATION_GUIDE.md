# Guide de Navigation - Théorie de Maîtrise du Temps

**Version**: 1.0
**Date**: 2026-01-17

---

## 🎯 JE VEUX...

### Comprendre la Théorie (Grand Public)

**Démarrage rapide** (15-30 min):
1. Lisez `README.md` - Vue d'ensemble du projet
2. Lisez `docs/fr/00-vulgarisation/` - Guides pédagogiques simplifiés
3. Regardez `CONCEPT_MAP.md` - Carte conceptuelle visuelle

**Approfondissement** (2-3 heures):
1. `CONCEPTS_FONDAMENTAUX.md` - Les 3 piliers (Cartographie Després, Liaison Asselin, Masse Després)
2. `DEFINITION_MATIERE_NOIRE.md` - Qu'est-ce que la "matière noire"?
3. `DEFINITION_ENERGIE_NOIRE.md` - Qu'est-ce que l'"énergie noire"?
4. `VULGARISATION_LOIS_FONDAMENTALES_MT_MQ.md` - Liens avec physique quantique

**Questions fréquentes**:
- *Qu'est-ce qui rend TMT différent?* → `CONCEPT_MAP.md` Section "Comparaison Modèles"
- *Est-ce que ça marche vraiment?* → `STATUS.md` Section "Validation Expérimentale"
- *C'est prouvé?* → `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md`

---

### Étudier les Mathématiques (Étudiant/Chercheur)

**Prérequis**: Relativité Générale niveau L3/M1, calcul tensoriel

**Parcours recommandé** (1-2 semaines):

**Jour 1-2: Fondations**
1. `CONCEPTS_FONDAMENTAUX.md` - Intuition physique
2. `CADRE_RELATIVITE_GENERALE.md` - Cadre RG standard
3. `DERIVATION_GEODESIQUES_RG_COMPLETE.md` - Géodésiques complètes

**Jour 3-4: Formulation TMT**
4. `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md` - Formulation centrale
5. `DEFINITION_MATIERE_NOIRE.md` - Masse Després M = k·∫Φ²dV
6. `LOI_UNIVERSELLE_k.md` - Loi k(M_bary, f_gas)

**Jour 5-7: Applications**
7. `ANALYSE_COURBES_ROTATION.md` - Galaxies (NGC3198, M31, MW)
8. `MODELE_HYBRIDE_ENERGIE_NOIRE.md` - H(z,ρ) variable
9. `FORMALISATION_H_Z_RHO.md` - Paramètre Hubble local

**Jour 8-10: Validation**
10. `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md` - Tous les tests
11. `PREDICTION_TESTABLE_UNIQUE.md` - Test weak lensing
12. `COSMOS_DES_TEST_GUIDE.md` - Méthodologie test critique

**Jour 11-14: Lecture article**
13. `SCIENTIFIC_ARTICLE_TIME_MASTERY.md` (EN) ou
14. `ARTICLE_SCIENTIFIQUE_MAITRISE_TEMPS.md` (FR)

**Théories avancées** (optionnel):
- `EQUATION_SCHRODINGER_DESPRES.md` - Extension quantique
- `TEMPORONS_THEORY.md` - Quanta de temps
- `LIENS_RG_ET_ELECTROMAGNETISME.md` - Unification EM
- `RESEAU_LIGNES_ASSELIN.md` - Graphe temporel universel

---

### Reproduire les Calculs (Scientifique)

**Setup environnement** (30 min):
```bash
cd /home/chuck/dev/sources/Maitrise-du-temps
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # Si existe, sinon voir README
```

**Dépendances principales**:
- numpy, scipy, matplotlib (calculs et plots)
- astropy (données astronomiques)
- astroquery (téléchargement catalogues)

**Reproduire loi universelle k** (2-3 heures):
```bash
cd scripts
python determine_k_coupling_SPARC_full.py
# Output: k₀=0.343±0.070, α=-1.610±0.087, β=-3.585±0.852
# R²=0.9976, χ²_red=0.04
```

**Générer figures publication** (30 min):
```bash
cd scripts
python create_publication_figures.py
# Génère 4 figures dans ../data/results/
```

**Tester weak lensing (simulation)** (1-2 heures):
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM.py
# Simulation: TMT → r=0.68, ΛCDM → r=0.02
```

**Analyser courbes rotation**:
```bash
cd scripts/calculs
python calcul_courbe_rotation_galaxie.py
# Calcule v(r) pour galaxies SPARC
```

**Tous les scripts**: Voir `04-COMPUTATION/` (après réorganisation) ou `scripts/` (actuel)

**Documentation code**:
- Chaque script a docstrings et commentaires
- Voir en-tête de fichier pour usage
- Variables notées selon convention TMT

---

### Comprendre un Concept Spécifique

#### Cartographie Després (IDT)
**Fichiers**:
- `CARTOGRAPHIE_DESPRES.md` - Définition complète
- `docs/fr/01-concepts-fondamentaux/LEXICO_MASA_Y_CARTOGRAFIA_DESPRES.md`
- `scripts/calculs/calcul_temps_local_terre.py` - Implémentation

**Équation clé**:
```
γ_Després(r) = dt_local / dt_reference
             = fonction de Φ(r)
```

#### Liaison Asselin
**Fichiers**:
- `LIAISON_ASSELIN.md` - Théorie
- `RESEAU_LIGNES_ASSELIN.md` - Extension réseau
- `scripts/calculs/calcul_liaisons_asselin.py` - Calculs

**Principe**: Gravitation = connexion temporelle commune

#### Masse Després
**Fichiers**:
- `DEFINITION_MATIERE_NOIRE.md` (FR)
- `DARK_MATTER_DEFINITION.md` (EN)
- `DEFINICION_MATERIA_OSCURA.md` (ES)

**Formule**:
```
M_Després = k · ∫ Φ²(r) dV
```

#### Loi Universelle k
**Fichiers**:
- `LOI_UNIVERSELLE_k.md` - Découverte et validation
- `data/results/k_asselin_calibration.txt` - Résultats

**Formule**:
```
k(M_bary, f_gas) = k₀ · (M_bary/10¹⁰)^α · (1+f_gas)^β
k₀ = 0.343, α = -1.610, β = -3.585
```

#### Énergie Noire (H variable)
**Fichiers**:
- `DEFINITION_ENERGIE_NOIRE.md`
- `MODELE_HYBRIDE_ENERGIE_NOIRE.md`
- `FORMALISATION_H_Z_RHO.md`

**Formule**:
```
H(z,ρ) = H₀ √[Ωₘ(1+z)³ + ΩΛ exp(β(1-ρ/ρ_crit))]
β = 0.38
```

---

### Vérifier les Résultats de Tests

#### Calibration loi k (Phase 1)
**Fichier**: `LOI_UNIVERSELLE_k.md`

**Résultats**:
- R² = 0.9976 (99.76% variance expliquée)
- χ²_red = 0.04 (ajustement exceptionnel)
- 6 galaxies: Toutes ±8% précision

**Galaxies testées**:
| Galaxie | M_bary | f_gas | k_obs | k_pred | Erreur |
|---------|--------|-------|-------|--------|--------|
| DDO154 | 3.3×10⁸ | 0.95 | 3.675 | 3.656 | -0.5% ✅ |
| NGC2403 | 3.5×10⁹ | 0.65 | 0.304 | 0.327 | +7.5% ✅ |
| NGC3198 | 8.2×10⁹ | 0.40 | 0.186 | 0.174 | -6.5% ✅ |
| NGC6503 | 1.8×10⁹ | 0.85 | 1.287 | 1.298 | +0.8% ✅ |
| NGC2841 | 1.2×10¹¹ | 0.05 | 0.026 | 0.027 | +3.8% ✅ |
| UGC2885 | 2.5×10¹¹ | 0.10 | 0.014 | 0.014 | 0.0% ✅ |

#### Courbes de Rotation
**Fichier**: `ANALYSE_COURBES_ROTATION.md`

**Résultats**: Toutes les courbes prédites sans paramètres libres
**Figures**: `data/results/figure3_rotation_curves.png`

#### Supernovae (SNIa)
**Fichier**: `RESULTATS_MODELE_HYBRIDE_ENERGIE_NOIRE.md`
**Script**: `scripts/analyze_pantheon_SNIa.py`

**Résultat**: β = 0.38 ± 0.05 (paramètre expansion)

#### Tests RG
**Fichier**: `RESULTATS_DERIVATION_RG.md`
**Script**: `scripts/tests/test_formulations_rigoureuses_RG.py`

**Résultat**: Tous tests de cohérence RG passés ✅

#### Synthèse Complète
**Fichier**: `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md`

Vue d'ensemble de tous les 8+ tests effectués

---

### Préparer une Publication

#### Articles Prêts à Soumettre
**Anglais**: `SCIENTIFIC_ARTICLE_TIME_MASTERY.md` (~8500 mots)
**Français**: `ARTICLE_SCIENTIFIQUE_MAITRISE_TEMPS.md` (~8500 mots)

**Sections**: Abstract, Introduction, Theory, Math, Results, Comparison, Predictions, Discussion, Conclusions, References

#### Figures Publication
**Localisation**: `data/results/`
- `figure1_k_vs_mass.png` (238 KB, 300 DPI)
- `figure2_k_correlation.png` (224 KB, 300 DPI)
- `figure3_rotation_curves.png` (519 KB, 300 DPI)
- `figure4_summary.png` (480 KB, 300 DPI)

**Spécifications**: `docs/en/05-publications/FIGURE_SPECIFICATIONS.md`

#### Package Zenodo
**Localisation**: `zenodo_package/` (20 fichiers) ou `PUBLICATION_ZENODO/` (31 fichiers)

**Contenu**:
- Article scientifique
- Formulation mathématique complète
- Définitions matière/énergie noires
- Prédiction testable unique
- Guide méthodologique COSMOS/DES
- Métadonnées (CITATION.cff, LICENSE, METADATA.json)

**Guide upload**: `ZENODO_SUBMISSION_GUIDE.md`

#### Soumission Journal
**Guide**: `SUBMISSION_READY.md`

**Journaux recommandés**:
1. ApJ (Astrophysical Journal) - Premier choix
2. MNRAS (Monthly Notices RAS) - Alternative
3. A&A (Astronomy & Astrophysics) - Européen

**Timeline**: 2-3 mois review après soumission

---

### Exécuter le Test Weak Lensing (Critique)

**Objectif**: Valider ou réfuter TMT définitivement

**Prédictions**:
- **TMT**: r(θ_halo, θ_voisin) > 0.50
- **ΛCDM**: r < 0.20

**Méthodologie complète**: `COSMOS_DES_TEST_GUIDE.md`

**Étapes**:

**1. Télécharger données COSMOS** (~2 GB):
```bash
cd data/input
wget https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits
# ou utiliser scripts/download_cosmos_auto.py
```

**2. Télécharger données DES** (~10 GB):
```bash
# Voir COSMOS_DES_TEST_GUIDE.md pour instructions détaillées
# ou utiliser scripts/download_cosmos_des.sh
```

**3. Exécuter analyse**:
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM.py --real-data
# Analyse θ_halo vs θ_voisin
# Calcule corrélation r
```

**4. Interpréter résultats**:
- Si r > 0.50: **TMT VALIDÉE** ✅
- Si 0.20 < r < 0.50: Incertain, refaire avec plus de données
- Si r < 0.20: **TMT RÉFUTÉE** ❌

**Timeline**: 1 semaine téléchargement + 1-2 heures analyse

---

### Contribuer au Projet

#### Structure Actuelle (Avant Housekeeping)
```
Maitrise-du-temps/
├── docs/          # Documentation organisée (FR/EN/ES)
├── scripts/       # Code Python
├── data/          # Données et résultats
├── figures/       # Figures générées
├── archive/       # Archives
└── [109+ fichiers root]  # À réorganiser
```

#### Structure Proposée (Après Housekeeping)
Voir `HOUSEKEEPING_PLAN.md` pour détails complets

```
Maitrise-du-temps/
├── 00-PROJECT-MANAGEMENT/  # Gestion projet
├── 01-THEORY/             # Théories
├── 02-VALIDATION/         # Tests et résultats
├── 03-PUBLICATION/        # Articles et figures
├── 04-COMPUTATION/        # Scripts organisés
├── 05-DATA/               # Données
├── docs/                  # Docs multilingues
└── archive/               # Archives
```

#### Workflow Contribution
1. Fork/clone le repository
2. Créer branche feature: `git checkout -b feature/nom-feature`
3. Faire modifications
4. Tester (scripts, cohérence docs)
5. Commit avec message descriptif
6. Push et créer pull request
7. Review et merge

#### Standards
- **Code**: Python 3.8+, PEP8, docstrings
- **Documentation**: Markdown, FR/EN (ES si possible)
- **Figures**: PNG 300 DPI minimum
- **Références**: Format APA ou journal target

---

### Traduire en Espagnol

**Statut actuel**: 8 fichiers traduits / ~53 total

**Fichiers prioritaires à traduire**:
1. Articles scientifiques (EN → ES)
2. Formulation mathématique complète
3. Analyses et résultats de tests
4. Guides méthodologiques

**Fichiers déjà traduits** (`docs/es/`):
- Concepts fondamentaux (2 fichiers)
- Formulation mathématique (2 fichiers)
- Matière noire (1 fichier)
- Plans recherche (1 fichier)
- Définitions (2 fichiers)

**Workflow traduction**:
1. Copier fichier FR ou EN
2. Traduire contenu (préserver structure Markdown)
3. Adapter exemples si nécessaire
4. Placer dans `docs/es/[catégorie]/`
5. Ajouter au glossaire ES
6. Commit: `git commit -m "🌐 Traduction ES: [nom fichier]"`

**Outils recommandés**:
- DeepL pour traduction initiale (meilleur que Google)
- Review manuelle pour termes techniques
- Glossaire TMT pour cohérence terminologie

---

### Obtenir de l'Aide

#### Documentation Projet
- `README.md` - Vue d'ensemble
- `STATUS.md` - État actuel et métriques
- `CONCEPT_MAP.md` - Relations conceptuelles
- **CE FICHIER** (`NAVIGATION_GUIDE.md`) - Navigation

#### Questions Théoriques
- Chercher dans `CONCEPT_MAP.md` - Index concepts
- Lire formulation: `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md`
- Consulter glossaire (à créer)

#### Questions Code
- Lire docstrings dans scripts Python
- Voir exemples d'usage en haut de chaque script
- Consulter `scripts/tests/` pour exemples

#### Questions Publication
- `SUBMISSION_READY.md` - Checklist soumission
- `ZENODO_SUBMISSION_GUIDE.md` - Upload Zenodo
- `OU_PUBLIER_MAINTENANT.md` - Options publication

#### Contact
**Chercheur principal**: Pierre-Olivier Després Asselin
**Email**: pierreolivierdespres@gmail.com

---

## 📚 INDEX ALPHABÉTIQUE DES FICHIERS CLÉS

### A-C
- `ANALYSE_COURBES_ROTATION.md` - Validation courbes rotation
- `ANALYSE_STATISTIQUE_PROBABILITES.md` - Tests statistiques
- `APPROCHE_HYBRIDE_IDT.md` - Approche hybride IDT
- `ARTICLE_SCIENTIFIQUE_MAITRISE_TEMPS.md` - Article FR
- `CADRE_RELATIVITE_GENERALE.md` - Cadre RG
- `CARTOGRAPHIE_DESPRES.md` - Indice distortion temporelle
- `CONCEPT_MAP.md` - Carte conceptuelle (CE FICHIER)
- `CONCEPTS_FONDAMENTAUX.md` - Fondations théoriques
- `COSMOS_DES_TEST_GUIDE.md` - Guide test weak lensing

### D-F
- `DARK_MATTER_DEFINITION.md` - Définition matière noire (EN)
- `DEFINITION_ENERGIE_NOIRE.md` - Définition énergie noire
- `DEFINITION_MATIERE_NOIRE.md` - Définition matière noire (FR)
- `DERIVATION_GEODESIQUES_RG_COMPLETE.md` - Géodésiques RG
- `EQUATION_SCHRODINGER_DESPRES.md` - Extension quantique
- `FORMALISATION_H_Z_RHO.md` - Paramètre Hubble local
- `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md` - Formulation complète

### H-M
- `HOUSEKEEPING_PLAN.md` - Plan réorganisation
- `LIAISON_ASSELIN.md` - Gravitation par liaison temporelle
- `LIENS_RG_ET_ELECTROMAGNETISME.md` - Unification EM
- `LOI_UNIVERSELLE_k.md` - Loi k(M,f_gas) - PERCÉE MAJEURE
- `MODELE_HYBRIDE_ENERGIE_NOIRE.md` - Modèle H(z,ρ)

### N-S
- `NAVIGATION_GUIDE.md` - CE FICHIER
- `OU_PUBLIER_MAINTENANT.md` - Options publication
- `PREDICTION_TESTABLE_UNIQUE.md` - Test weak lensing
- `README.md` - Vue d'ensemble projet
- `RESEAU_LIGNES_ASSELIN.md` - Graphe temporel
- `RESULTATS_DERIVATION_RG.md` - Résultats dérivation RG
- `SCIENTIFIC_ARTICLE_TIME_MASTERY.md` - Article EN
- `STATUS.md` - État projet
- `SUBMISSION_READY.md` - Checklist soumission
- `SUPERPOSITION_TEMPORELLE.md` - Temps avant+arrière
- `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md` - Synthèse tests

### T-Z
- `TEMPORONS_THEORY.md` - Quanta de temps
- `TRAVAIL_COMPLET_RESUME.md` - Résumé travail complet
- `VULGARISATION_LOIS_FONDAMENTALES_MT_MQ.md` - Vulgarisation
- `ZENODO_SUBMISSION_GUIDE.md` - Guide upload Zenodo

---

## 🗺️ RACCOURCIS PAR OBJECTIF

| Je veux... | Fichier(s) |
|------------|------------|
| **Comprendre TMT en 30 min** | `README.md` + `CONCEPT_MAP.md` |
| **Lire l'article** | `SCIENTIFIC_ARTICLE_TIME_MASTERY.md` (EN/FR) |
| **Voir les résultats** | `STATUS.md` + `LOI_UNIVERSELLE_k.md` |
| **Reproduire calculs** | `scripts/` + ce guide section "Reproduire" |
| **Publier maintenant** | `SUBMISSION_READY.md` + `ZENODO_SUBMISSION_GUIDE.md` |
| **Test critique** | `COSMOS_DES_TEST_GUIDE.md` |
| **Math rigoureuse** | `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md` |
| **Comparer ΛCDM/MOND/TMT** | `SCIENTIFIC_ARTICLE_...` Section 7 |
| **Contribuer** | `HOUSEKEEPING_PLAN.md` + workflow ci-dessus |
| **Traduire ES** | Section "Traduire" ci-dessus |

---

## 📞 SUPPORT ET COMMUNAUTÉ

### Ressources Projet
- **Repository**: [GitHub - Maitrise-du-temps]
- **Documentation**: `docs/` (FR/EN/ES)
- **Issues**: [GitHub Issues]
- **Discussions**: [GitHub Discussions]

### Références Externes
- **SPARC Database**: http://astroweb.cwru.edu/SPARC/
- **Pantheon SNIa**: https://pantheonplussh0es.github.io/
- **COSMOS**: https://cosmos.astro.caltech.edu/
- **DES**: https://www.darkenergysurvey.org/

### Publications Connexes
- Planck Collaboration 2018 (ΛCDM parameters)
- McGaugh et al. 2016 (SPARC)
- Riess et al. 2022 (H₀ tension)
- Milgrom 1983 (MOND)

---

**Créé**: 2026-01-17
**Auteur**: Claude Code (Housekeeping)
**Version**: 1.0
**Statut**: 🟢 Actif

**Besoin d'aide? Commencez par `README.md` puis revenez ici!**
