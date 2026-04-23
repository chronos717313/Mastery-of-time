# Guide de Soumission — RNAAS

**Journal :** Research Notes of the American Astronomical Society
**Éditeur :** AAS (American Astronomical Society)
**Type :** Research Note (court, ≤ 1500 mots, 1 figure OU 1 table)
**Review :** Léger (editor-only, pas de peer-review formel)

---

## ⚠️ Point Critique — Éviter le Desk Rejection ApJ

**Contexte :** Ton manuscrit ApJ (AAS76125) a été desk-rejeté le 23 avril 2026 par Prof. Conselice avec le motif : *"ApJ only publishes manuscripts based on the gathering, reporting and analysis of observational data and not manuscripts of a theoretical nature of fundamental physics."*

**RNAAS est géré par la MÊME AAS**, donc la même règle s'applique. Pour éviter un second rejet :

### ✅ À FAIRE dans la Research Note :
- Se concentrer UNIQUEMENT sur la loi empirique **r_c(M) = 2,6 × M^0,56**
- Présenter la découverte comme une **observation empirique** sur SPARC
- Mentionner le cadre théorique UNE SEULE FOIS, en arrière-plan
- Citer *« a phenomenological effective-mass formula »* sans développer
- Laisser la théorie complète pour MNRAS / JCAP / PRD

### ❌ À NE PAS FAIRE :
- Présenter |Ψ⟩ = α|t⟩ + β|t̄⟩ (superposition quantique)
- Parler de « time mastery », « temporal superposition », etc.
- Introduire Před-/Després-mass, Temporons, champs hypothétiques
- Prétendre expliquer à la fois matière noire ET énergie noire
- Mentionner les 8 tests cosmologiques

La draft actuelle `RNAAS_SUBMISSION_DRAFT.md` est DÉJÀ bien cadrée — garde-la telle quelle.

---

## 1. Portail de Soumission

🔗 **URL :** https://aas.msubmit.net
🔗 **Instructions :** https://journals.aas.org/research-notes/
🔗 **Author guide :** https://journals.aas.org/manuscript-preparation/

---

## 2. Compte

1. Utiliser le **MÊME COMPTE** que pour l'ApJ (manuscrit AAS76125)
2. ORCID déjà associé : **0009-0009-7611-4550**
3. Affiliation : *Independent Researcher, Montréal, Québec, Canada*

---

## 3. Format — Contraintes Strictes

| Élément | Limite |
|---------|--------|
| **Mots** | ≤ 1 500 |
| **Figures** | 1 MAXIMUM |
| **Tables** | 1 MAXIMUM |
| **Total figures + tables** | ≤ 1 (exclusif) ou ≤ 2 (total) selon version |
| **Références** | Jusqu'à ~10 |
| **Sections** | Format libre (pas de sections formelles) |
| **Abstract** | Court (~100 mots) |

La draft actuelle respecte déjà ces limites.

---

## 4. Fichiers à Préparer

| Fichier | Source | Statut |
|---------|--------|--------|
| **Research Note** | `docs/promotion-internationale/RNAAS_SUBMISSION_DRAFT.md` | ✅ Convertir en LaTeX AASTeX v7 |
| **Cover letter** | `submissions/RNAAS/cover_letter.tex` | ✅ Prête |
| **Table** | Tableau par type de galaxie (déjà dans la draft) | ✅ Intégré |

**Template LaTeX :** https://journals.aas.org/manuscript-preparation/
*(télécharger `aastex7.cls` + template)*

---

## 5. Formulaire de Soumission

### Step 1 — Manuscript Type
☑ **Research Note**
(NE PAS choisir : Article, Letter, Erratum)

### Step 2 — Title, Authors, Abstract
- **Title :** *A Mass-Dependent Transition Radius in Galaxy Rotation Curves: Evidence for a Universal Scaling Law from the SPARC Sample*
- **Short title :** *Mass-Dependent r_c in SPARC Galaxies*
- **Abstract :** copier depuis `RNAAS_SUBMISSION_DRAFT.md` (~130 mots)

### Step 3 — Keywords (AAS UAT — Unified Astronomy Thesaurus)
Choisir parmi les mots officiels :
- `Galaxy kinematics (602)`
- `Galaxy rotation curves (619)`
- `Scaling relations (2031)`
- `Dark matter (353)`
- `Spiral galaxies (1560)`

### Step 4 — Authors & Affiliations
- **Corresponding :** Pierre-Olivier Després Asselin
- **Affiliation :** Independent Researcher, Montréal, Québec, Canada
- **ORCID :** 0009-0009-7611-4550
- **Email :** pierreolivierdespres@gmail.com

### Step 5 — Reviewers
RNAAS n'exige **pas** de reviewers suggérés (editor-only review).
Laisser le champ vide ou ignorer.

### Step 6 — Publication Charges
☑ **Request AAS Publication Support Fund waiver**
*(chercheur indépendant sans financement institutionnel)*

### Step 7 — Declarations
- **Conflicts of interest :** None
- **Funding :** This research received no external funding
- **Data availability :** All data used are the publicly available SPARC catalogue (Lelli et al. 2016). Analysis scripts at https://github.com/chronos717313/Mastery-of-time (DOI: 10.5281/zenodo.18287042)

### Step 8 — Upload
1. `cover_letter.pdf`
2. `research_note.tex` (AASTeX v7 format)
3. `refs.bib` (court — ~8 références seulement)

---

## 6. Particularités RNAAS

| Élément | Règle |
|---------|-------|
| **Ton** | Concis, factuel, observationnel |
| **Revue par pairs** | NON (editor-only) |
| **Citations futures** | Oui, indexée ADS + DOI assigné |
| **Coût** | ~225 USD (waiver possible pour chercheurs indépendants) |
| **Délai décision** | 2–4 semaines typiquement |

---

## 7. Checklist de Relecture avant Envoi

Avant le `Submit` final :

- [ ] Aucune mention de « time mastery » ou « temporal superposition »
- [ ] Aucune équation |Ψ⟩ = α|t⟩ + β|t̄⟩
- [ ] Le mot « theory » utilisé ≤ 2 fois dans tout le texte
- [ ] Accent observationnel : « We report an empirical correlation... »
- [ ] Les 15σ et les 8 tests ne sont PAS mentionnés
- [ ] La formule M_eff(r) = M_bary(r) × [1 + (r/r_c)^n] présentée comme « phenomenological »
- [ ] La loi k(M) peut être mentionnée brièvement (second résultat empirique)
- [ ] Citation du cadre théorique complet : *« see companion paper (Després Asselin, MNRAS, submitted) »*
- [ ] ≤ 1500 mots total
- [ ] ≤ 1 figure ou 1 table
- [ ] Cover letter mentionne explicitement que le framework théorique est dans une soumission séparée

---

## 8. Timeline Attendue

| Étape | Durée |
|-------|-------|
| Accusé de réception | 1 jour |
| Decision éditoriale | 2–4 semaines |
| Correction mineure | 1 semaine |
| Publication en ligne | 1–2 semaines après acceptation |

**Total : ~4–8 semaines.**

---

## 9. Contact Éditorial

**RNAAS Editorial Office**
Email : rnaas@aas.org
Portal : https://aas.msubmit.net
