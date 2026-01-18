# Archiving Proposal - Quick Action Plan

**Date**: 2026-01-17
**Branch**: `housekeeping/organize-structure`

---

## 🎯 SUMMARY

Based on file age validation, I propose archiving files in **3 waves**:

### Wave 1: OBVIOUS (Execute Now) - 30 files
Safe to archive immediately - clearly outdated or superseded

### Wave 2: LIKELY (Needs Quick Check) - 15 files
Probably outdated, quick 30-second review per file

### Wave 3: UNCERTAIN (Needs Discussion) - 10 files
May still be relevant, need your input

---

## 📦 WAVE 1: ARCHIVE IMMEDIATELY (30 files)

### Category: Session Notes & Progress Snapshots
**Archive to**: `archive/session-notes-2025/`

```
SESSION_PERCEE_ULTIME.md (2025-12-06)
PERCEE_FINALE_SUPERPOSITION.md (2025-12-06)
ETAT_ACTUEL_THEORIE.md (2026-01-15 - snapshot, not current guide)
PROGRESSION_VISUELLE.md (2025-12-06)
REVISION_GUIDE_PEDAGOGIQUE.md (2025-12-13 - revision notes, not the guide itself)
```

**Reason**: These are historical snapshots/session notes, not reference documents

---

### Category: Duplicate Publication Materials
**Archive to**: `archive/publication-drafts-dec2025/`

```
PUBLICATION_ZENODO/* (entire folder)
```

**Reason**: `zenodo_package/` (Jan 2026) is newer and more complete

Individual duplicates in root:
```
ARTICLE_PUBLICATION_TMT.md (2025-12-07) - duplicate of zenodo version
DARK_MATTER_DEFINITION.md - multiple copies exist
DEFINICION_MATERIA_OSCURA.md - duplicate
DEFINITION_MATIERE_NOIRE.md - duplicate
```

**Action**: Keep versions in `zenodo_package/`, archive root copies

---

### Category: Old Test Scripts (Root Directory)
**Archive to**: `archive/old-scripts-root/`

All `test_*.py` files in root (not in `scripts/`):
```
test_validation_ngc3198.py
test_validation_m33.py
test_validation_m31.py
test_superposition_temporelle.py
test_reseau_multiechelle_ordre2.py
test_reseau_asselin.py
test_reseau_1000_galaxies.py
test_reformulations_k_Asselin.py
test_maximisation_amelioration.py
test_k_elliptiques_redshift.py
test_formule_simplifiee.py
test_formule_corrigee.py
test_formulations_rigoureuses_RG.py
test_formulation_maxwell.py
test_echelles_recommandees.py
test_d_eff_variable.py
test_d_eff_variable_NGC3198.py
test_approche_hybride_IDT.py
test_ancrage_bulbes_rapide.py
test_ancrage_bulbes.py
```

**Reason**: Should be in `scripts/tests/`, not root. Archive and verify duplicates.

---

### Category: Old Results from Dec 2025
**Archive to**: `archive/results-dec2025/`

```
TRAVAIL_COMPLET_RESUME.md (2025-12-13 - "TOUS LES TRAVAUX TERMINÉS")
RESULTATS_TEST_COSMOS_DES.md (2025-12-13)
DOCUMENTATION_MISE_A_JOUR_RESUME.md (2025-12-07)
```

**Reason**: Dated summaries from December, superseded by current work

---

## 📋 WAVE 2: LIKELY ARCHIVE (15 files)

### Quick Check Needed (30 sec each)

```
SYNTHESE_RESULTATS_QUANTITATIFS.md (2025-12-06)
SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md (?)
SYNTHESE_VOIE1_MULTI_GALAXIES.md (?)
SYNTHESE_ECHELLE_GALACTIQUE.md (?)
SYNTHESE_FORMULATION_MAXWELL.md (?)
PLAN_VALIDATION_PROCHAINES_GALAXIES.md (2025-12-06)
CONSTANTES_MANQUANTES.md (?)
ANALYSE_COSMOS_PREPARATION.md (2025-12-07)
PHASE_1_COMPLETE.md (?)
RESULTATS_MODELE_HYBRIDE_ENERGIE_NOIRE.md (?)
REPONSE_APPROCHE_HYBRIDE.md (?)
APPROCHE_HYBRIDE_IDT.md (?)
ANALYSE_ECHELLES_GALACTIQUES.md (?)
ANALYSE_D_EFF_VARIABLE_ECHEC.md (?)
BILAN_CRITIQUE_8_TESTS.md (?)
```

**Action**: Quick grep for "TMT v2", "temporal superposition", "k(M,f_gas)"
- If mentions old concepts only → Archive
- If current → Keep

---

## ✅ WAVE 3: KEEP AS CURRENT (20+ files)

### Recent & Active (Jan 2026)
```
README.md (2026-01-15) ✅
FORMULATION_MATHEMATIQUE_COMPLETE_MT.md (2026-01-15) ✅
SYNTHESE_PERCEE_SUPERPOSITION.md (2026-01-15) ✅
```

### Quantum-Time Unification (Current Focus)
```
TEMPORONS_THEORY.md (2026-01-13) ✅
QUANTUM_TIME_MASTERY_THEORY_EN.md (2026-01-13) ✅
EXPERIMENTAL_PROPOSALS_MT_MQ.md (2026-01-13) ✅
UNIFICATION_TIME_QUANTUM_MECHANICS.md (2026-01-13) ✅
SCHRODINGER_DESPRES_EQUATION.md (2026-01-13) ✅
RIGOROUS_DERIVATION_GR.md (2026-01-13) ✅
DETAILED_TESTABLE_PREDICTIONS_MT_QM.md (2026-01-13) ✅
UNIFICATION_TEMPS_MECANIQUE_QUANTIQUE.md (2025-12-15) ✅
RESUME_UNIFICATION_MT_MQ.md (2025-12-15) ✅
```

### Publication Ready (Current)
```
SUBMISSION_READY.md (2025-12-10) ✅
OU_PUBLIER_MAINTENANT.md (2025-12-07) ✅
ZENODO_SUBMISSION_GUIDE.md (2025-12-07) ✅
LOI_UNIVERSELLE_k.md (2025-12-07) ✅
AAS_ABSTRACT_250_WORDS.md (2026-01-04) ✅
SUBMISSION_LETTER_UNIFICATION_MT_QM_EN.md (2025-12-19) ✅
LETTRE_SOUMISSION_UNIFICATION_MT_MQ_FR.md (2025-12-19) ✅
CARTA_SUMISION_UNIFICACION_MT_MC_ES.md (2025-12-19) ✅
```

### Core Theory (Always Current)
```
CONCEPTS_FONDAMENTAUX.md ✅
LIAISON_ASSELIN.md ✅
CARTOGRAPHIE_DESPRES.md ✅
SUPERPOSITION_TEMPORELLE.md (2025-12-06) ✅
RESEAU_LIGNES_ASSELIN.md ✅
CADRE_RELATIVITE_GENERALE.md ✅
DERIVATION_GEODESIQUES_RG_COMPLETE.md ✅
```

### Vulgarization & Analysis
```
VULGARISATION_LOIS_FONDAMENTALES_MT_MQ.md (2025-12-16) ✅
PREDICTIONS_TESTABLES_DETAILLEES_MT_MQ.md (2025-12-16) ✅
ANALYSE_STATISTIQUE_PROBABILITES.md (2025-12-18) ✅
VERIFICATIONS_NUMERIQUES.md (2025-12-13) ✅
GUIDE_CONVERSION_PDF_WORD.md (2025-12-15) ✅
```

### Foundational Math/Physics
```
FORMALISATION_H_Z_RHO.md (2025-12-06) ✅
LEXIQUE_MASSE_CARTOGRAPHIE_DESPRES.md (2025-12-06) ✅
FORMALISATION_MATHEMATIQUE_RG.md (?) ✅
EQUATION_SCHRODINGER_DESPRES.md (2025-12-17) ✅
```

### Test & Methodology (Current)
```
TEST_EXPERIMENTAL_FINAL.md (2025-12-13) ✅
```

---

## 🗂️ NEW ARCHIVE STRUCTURE

```
archive/
│
├── session-notes-2025/
│   ├── SESSION_PERCEE_ULTIME.md
│   ├── PERCEE_FINALE_SUPERPOSITION.md
│   ├── ETAT_ACTUEL_THEORIE.md
│   ├── PROGRESSION_VISUELLE.md
│   ├── REVISION_GUIDE_PEDAGOGIQUE.md
│   └── README_ARCHIVE.md (explains these are historical session notes)
│
├── publication-drafts-dec2025/
│   ├── PUBLICATION_ZENODO/ (entire folder)
│   ├── ARTICLE_PUBLICATION_TMT.md
│   ├── DARK_MATTER_DEFINITION.md (root copy)
│   └── README_ARCHIVE.md (explains superseded by zenodo_package/)
│
├── old-scripts-root/
│   ├── test_*.py (all 20+ files from root)
│   └── README_ARCHIVE.md (explains should be in scripts/, archived for cleanup)
│
├── results-dec2025/
│   ├── TRAVAIL_COMPLET_RESUME.md
│   ├── RESULTATS_TEST_COSMOS_DES.md
│   ├── DOCUMENTATION_MISE_A_JOUR_RESUME.md
│   └── README_ARCHIVE.md (explains these are point-in-time summaries)
│
├── to-review/ (Wave 2 files temporarily)
│   ├── SYNTHESE_*.md files
│   ├── ANALYSE_*.md files
│   └── README.md (explains need quick review)
│
└── obsolete/ (already exists)
    └── (existing old files)
```

---

## 🚀 EXECUTION PLAN

### Phase 1: Safe Archives (5 minutes)
```bash
# Create archive structure
mkdir -p archive/session-notes-2025
mkdir -p archive/publication-drafts-dec2025
mkdir -p archive/old-scripts-root
mkdir -p archive/results-dec2025

# Move Wave 1 files
git mv SESSION_PERCEE_ULTIME.md archive/session-notes-2025/
git mv PERCEE_FINALE_SUPERPOSITION.md archive/session-notes-2025/
git mv ETAT_ACTUEL_THEORIE.md archive/session-notes-2025/
git mv PROGRESSION_VISUELLE.md archive/session-notes-2025/
git mv REVISION_GUIDE_PEDAGOGIQUE.md archive/session-notes-2025/

git mv PUBLICATION_ZENODO archive/publication-drafts-dec2025/
git mv ARTICLE_PUBLICATION_TMT.md archive/publication-drafts-dec2025/

git mv test_*.py archive/old-scripts-root/ 2>/dev/null || true

git mv TRAVAIL_COMPLET_RESUME.md archive/results-dec2025/
git mv RESULTATS_TEST_COSMOS_DES.md archive/results-dec2025/
git mv DOCUMENTATION_MISE_A_JOUR_RESUME.md archive/results-dec2025/

# Create README files for each archive folder
# (will create these explaining what's archived and why)
```

### Phase 2: Review Wave 2 (15 minutes)
- Quickly check each SYNTHESE_*.md and ANALYSE_*.md file
- Move to archive if outdated
- Keep if current

### Phase 3: Reorganize Active Files (30 minutes)
- Apply HOUSEKEEPING_PLAN.md to remaining current files
- Create new folder structure
- Move files to organized locations

---

## ❓ QUESTIONS FOR YOU

1. **Session Notes**: OK to archive SESSION_*, PERCEE_*, ETAT_ACTUEL_*, etc.? (They're historical snapshots, not reference docs)

2. **TRAVAIL_COMPLET_RESUME.md**: This says "TOUS LES TRAVAUX TERMINÉS" from Dec 13, 2025. Is this still accurate or superseded?

3. **Test Scripts**: OK to archive all `test_*.py` from root directory? (They should be in `scripts/` anyway)

4. **PUBLICATION_ZENODO folder**: OK to archive since `zenodo_package/` is newer?

5. **Wave 2 Files**: Should I review these with you, or proceed with automated check (grep for old vs new concepts)?

---

## 🎯 RECOMMENDATION

**Proceed with Wave 1 immediately** (30 files, clear cases), then:
- You review Wave 2 list (15 files) - 5 minutes
- I apply reorganization to remaining current files
- Total time: ~45 minutes to clean project

**Alternative**: Execute all waves automatically based on automated checks (faster but less safe)

**What's your preference?**
