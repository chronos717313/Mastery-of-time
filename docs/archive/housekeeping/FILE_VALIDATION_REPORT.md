# File Validation Report - Maitrise du Temps

**Date**: 2026-01-17
**Purpose**: Identify outdated files vs current orientation

---

## 📅 PROJECT EVOLUTION TIMELINE

### Phase 1: TMT v1.0 (Pre-December 2025)
- Simple k parameter (single value per galaxy)
- 6 galaxies calibration
- Classic gravitation approach
- Status: **SUPERSEDED**

### Phase 2: TMT v2.0 (December 2025)
- **Breakthrough**: Temporal Superposition (forward + backward time)
- Quantum-Time Unification (MT-MQ)
- Universal law k(M_bary, f_gas): R² = 0.9976
- Pedagogical guides and vulgarization
- Status: **ACTIVE**

### Phase 3: TMT v2.0 + Weak Lensing (January 2026)
- **Critical Test**: COSMOS/DES weak lensing
- 10,000+ galaxies simulation
- Signal r = 0.378 [0.357, 0.399], 35.6σ discrimination
- Zenodo package preparation
- Status: **CURRENT**

---

## 🎯 CURRENT ORIENTATION (January 2026)

### Core Focus
1. **Weak Lensing Test** - COSMOS/DES data acquisition and analysis
2. **Universal Law k** - k(M_bary, f_gas) with R²=0.9976 on 10,000+ galaxies
3. **Quantum-Time Integration** - MT-MQ unification
4. **Temporal Superposition** - Forward + backward time arrows
5. **Publication Preparation** - Zenodo package, articles EN/FR/ES

### Active Concepts
- ✅ Liaison Asselin (gravitational coupling via common time)
- ✅ Cartographie Després (temporal distortion mapping)
- ✅ Temporal Superposition (PERCÉE 2025)
- ✅ Temporons (quantum time particles)
- ✅ Universal k(M, f_gas) law
- ✅ Weak lensing halo-neighbor alignment
- ✅ Quantum-time unification (MT-MQ)

### Deprecated Concepts
- ❌ Simple k (single value per galaxy) → Replaced by k(M, f_gas)
- ❌ TMT v1.0 formulations → Replaced by v2.0 with superposition
- ❌ 6-galaxy only validation → Replaced by 10,000+ simulation
- ❌ Pure classical approach → Replaced by quantum integration

---

## 📊 FILE CLASSIFICATION

### A. CURRENT & ACTIVE (Keep in main structure)

#### Recent Work (Jan 2026)
- `zenodo_package/*` - Publication ready
- `scripts/download_cosmos_*.py` - Data acquisition (latest)
- `scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py` - Current test
- `scripts/convert_cosmos_tbl_to_fits.py` - Latest utility
- `docs/en/FINAL_SUMMARY_WEAK_LENSING_TEST_TMT.md`
- `docs/en/COSMOS_DES_DOWNLOAD_GUIDE.md`
- `docs/fr/RESUME_FINAL_TEST_WEAK_LENSING_TMT.md`

#### Core Theory (Current formulations)
- `CONCEPTS_FONDAMENTAUX.md`
- `LIAISON_ASSELIN.md`
- `CARTOGRAPHIE_DESPRES.md`
- `SUPERPOSITION_TEMPORELLE.md` - **PERCÉE 2025**
- `TEMPORONS_THEORY.md`
- `FORMULATION_MATHEMATIQUE_COMPLETE_MT.md` (if updated for v2)
- `EQUATION_SCHRODINGER_DESPRES.md`

#### Quantum-Time Unification (Dec 2025)
- `UNIFICATION_TEMPS_MECANIQUE_QUANTIQUE.md`
- `UNIFICATION_TIME_QUANTUM_MECHANICS.md`
- `RESUME_UNIFICATION_MT_MQ.md`
- `QUANTUM_TIME_MASTERY_THEORY_EN.md`
- `VULGARISATION_LOIS_FONDAMENTALES_MT_MQ.md`
- `PREDICTIONS_TESTABLES_DETAILLEES_MT_MQ.md`
- `EXPERIMENTAL_PROPOSALS_MT_MQ.md`

#### Publication Materials (Dec 2025 - Current)
- `SUBMISSION_READY.md`
- `OU_PUBLIER_MAINTENANT.md`
- `ZENODO_SUBMISSION_GUIDE.md`
- `LOI_UNIVERSELLE_k.md` (if about k(M,f_gas))
- Submission letters (EN/FR/ES)

#### Scripts - Current
- `scripts/test_TMT_v2_*.py` - v2 tests
- `scripts/test_TMT_SPARC_175_galaxies.py`
- `scripts/test_TMT_10000_galaxies.py`
- `scripts/test_TMT_classique_COSMOS.py`
- `scripts/analyse_reformulation_TMT.py`

#### Documentation (Current structure)
- `docs/fr/00-vulgarisation/TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md`
- `docs/fr/theories/` - If contains current theories
- All multilingual docs (EN/FR/ES) in `docs/`

---

### B. OUTDATED - TO ARCHIVE

#### Category 1: TMT v1.0 Files (Pre-Temporal Superposition)
**Archive to**: `archive/2025-pre-superposition/`

Documents describing old formulations:
- Files explicitly about "simple k" (not k(M,f_gas))
- Pre-December 2025 formulations
- Documents mentioning only 6 galaxies (if not updated)

Candidates:
- `PHASE_1_COMPLETE.md` (Dec 7 2025 - pre-superposition)
- `PERCEE_FINALE_SUPERPOSITION.md` - Keep or archive? (check if superseded)
- `SESSION_PERCEE_ULTIME.md` - Session notes (archive as historical)
- Old calibration files referencing simple k

#### Category 2: Superseded Analysis/Results
**Archive to**: `archive/superseded-results/`

- `TRAVAIL_COMPLET_RESUME.md` - Dated "13 Décembre 2025", may be outdated
- `RESULTATS_TEST_*.md` - If superseded by newer tests
- `SYNTHESE_*.md` files - Check if superseded
- Old test results from 6-galaxy calibration

#### Category 3: Obsolete Scripts
**Archive to**: `archive/old-scripts/`

Scripts for deprecated approaches:
- `test_validation_*.py` - Old validation scripts (if v1.0)
- `test_formule*.py` - Already in archive/obsolete/
- `test_ancrage_bulbes*.py` - Bulge anchoring tests (check relevance)
- `test_reseau_*.py` - Network tests (check if v1 or v2)
- `test_d_eff_variable*.py` - Effective distance tests (check relevance)
- `test_formulations_rigoureuses_RG.py` - If superseded

Root level test scripts (should be in scripts/ anyway):
- All `test_*.py` in root directory → Archive or move to scripts/

#### Category 4: Development/Session Notes
**Archive to**: `archive/session-notes/`

- `SESSION_PERCEE_ULTIME.md`
- `PERCEE_FINALE_SUPERPOSITION.md` (session notes)
- `ETAT_ACTUEL_THEORIE.md` (if point-in-time snapshot)
- `PROGRESSION_PROJET_*.md` (progress snapshots)
- `INSTRUCTIONS_PR_MERGE.md` (dev notes)

#### Category 5: Duplicate Publication Materials
**Archive to**: `archive/publication-drafts/`

Since we have `zenodo_package/` AND `PUBLICATION_ZENODO/`:
- Keep: `zenodo_package/` (newer, Jan 2026)
- Archive: `PUBLICATION_ZENODO/` → `archive/publication-drafts/PUBLICATION_ZENODO_Dec2025/`

Individual publication files in root if duplicated:
- Root `ARTICLE_PUBLICATION_TMT.md` vs `zenodo_package/` version
- Root definition files vs `zenodo_package/` versions

---

### C. UNCERTAIN - NEEDS REVIEW

These need manual inspection to determine if current or outdated:

1. **Synthesis Documents**:
   - `SYNTHESE_COMPLETE_TESTS_QUANTITATIFS.md` - Check date and content
   - `SYNTHESE_RESULTATS_QUANTITATIFS.md` - Check if v1 or v2
   - `SYNTHESE_VOIE1_MULTI_GALAXIES.md` - Check relevance
   - `SYNTHESE_ECHELLE_GALACTIQUE.md`
   - `SYNTHESE_FORMULATION_MAXWELL.md`

2. **Results Documents**:
   - `RESULTATS_DERIVATION_RG.md` - RG derivation results (likely current)
   - `RESULTATS_TEST_COSMOS_DES.md` - Check if latest
   - `RESULTATS_MODELE_HYBRIDE_ENERGIE_NOIRE.md`
   - `RESULTATS_TEST_1000_GALAXIES.md` - v1 or v2?

3. **Theory Documents**:
   - `RESEAU_LIGNES_ASSELIN.md` - Network of Asselin lines (check if current)
   - `MODELE_HYBRIDE_ENERGIE_NOIRE.md` - Still relevant?
   - `CADRE_RELATIVITE_GENERALE.md` - GR framework (likely current)
   - `DERIVATION_GEODESIQUES_RG_COMPLETE.md` - GR geodesics (likely current)
   - `LIENS_RG_ET_ELECTROMAGNETISME.md` - GR-EM links (check relevance)

4. **Guides and Documentation**:
   - `DOCUMENTATION_MISE_A_JOUR_RESUME.md` - Documentation update summary
   - `CONSTANTES_MANQUANTES.md` - Missing constants (resolved?)
   - `GUIDE_CONVERSION_PDF_WORD.md` - Utility doc
   - `REVISION_GUIDE_PEDAGOGIQUE.md` - Revision notes (archive as historical)
   - `VERIFICATIONS_NUMERIQUES.md` - Numerical verifications

5. **Analysis Documents**:
   - `ANALYSE_*` files - Various analyses (check dates)
   - `APPROCHE_HYBRIDE_IDT.md` - Hybrid IDT approach
   - `PLAN_*` files - Planning documents

---

## 🗂️ PROPOSED ARCHIVE STRUCTURE

```
archive/
├── 2025-pre-superposition/           # TMT v1.0 (before temporal superposition)
│   ├── theory/
│   ├── tests/
│   ├── results/
│   └── README_ARCHIVE.md            # Explains what's here and why
│
├── superseded-results/               # Results replaced by better analysis
│   ├── 6-galaxy-calibration/
│   ├── simple-k-results/
│   └── README_ARCHIVE.md
│
├── old-scripts/                      # Deprecated scripts
│   ├── v1-tests/
│   ├── obsolete-utilities/
│   └── README_ARCHIVE.md
│
├── session-notes/                    # Development session notes
│   ├── percee-sessions/
│   ├── progress-snapshots/
│   └── README_ARCHIVE.md
│
├── publication-drafts/               # Old publication materials
│   ├── PUBLICATION_ZENODO_Dec2025/
│   ├── draft-articles/
│   └── README_ARCHIVE.md
│
└── obsolete/                         # Already existing - very old stuff
    └── (existing content)
```

---

## ✅ VALIDATION ACTIONS

### Step 1: Quick Wins (Clear Cases)
- ✅ Archive `archive/obsolete/*` content (already archived)
- ✅ Archive root `test_*.py` scripts → `archive/old-scripts/`
- ✅ Archive `PUBLICATION_ZENODO/` → `archive/publication-drafts/`
- ✅ Archive session notes (SESSION_*, PERCEE_*, ETAT_ACTUEL_*)

### Step 2: Date-Based Review
For each root `.md` file:
1. Check git log for last meaningful update
2. If before Nov 2025 AND not in "current concepts" → Archive
3. If Dec 2025 AND about v1.0 → Archive
4. If Dec 2025+ AND about current topics → Keep

### Step 3: Content-Based Review
For uncertain files:
1. Read first 20 lines
2. Check if mentions "simple k" or "6 galaxies only" → Archive
3. Check if mentions "temporal superposition" or "k(M,f_gas)" → Keep
4. Check if mentions "TMT v2" or "quantum" → Keep

### Step 4: Create README Files
For each archive folder, create `README_ARCHIVE.md`:
- What's in this archive
- Why it was archived
- When it was archived
- What replaced it (if applicable)

---

## 📋 NEXT STEPS

1. **User Review**: Get approval for this validation approach
2. **Execute Quick Wins**: Archive obvious candidates
3. **Review Uncertain**: Go through uncertain files one by one
4. **Create Archive READMEs**: Document what's archived and why
5. **Reorganize Active Files**: Apply the housekeeping plan to current files only
6. **Update Main README**: Reflect current state and archive location

---

**Questions for User:**
1. Are there specific files you know are outdated?
2. Should we keep session notes (PERCEE_*, SESSION_*) or archive them?
3. Do you want to review the uncertain files together?
4. Are TMT v1.0 materials valuable as historical record or can they be fully archived?

