# Guide de Soumission — Physical Review D (PRD)

**Journal :** Physical Review D — Particles, Fields, Gravitation, and Cosmology
**Éditeur :** American Physical Society (APS)
**Type :** Regular Article
**Section :** Cosmology, Dark Matter, Dark Energy / Classical General Relativity

---

## Pourquoi PRD est un Meilleur Choix que l'ApJ

| Critère | ApJ | PRD |
|---------|-----|-----|
| Accepte la physique théorique fondamentale | ❌ Non (desk-reject) | ✅ **Oui, c'est le cœur du journal** |
| Accepte cosmologie alternative à ΛCDM | Limité | ✅ Très fréquent |
| Accepte cadres unificateurs théoriques | Non | ✅ Oui |
| Reviewers théoriciens | Rare | ✅ Routinier |
| Valeur citation en cosmologie théorique | Haute | ✅ **Plus haute** |

PRD a publié :
- Gupta 2024 (CCC+TL)
- Afshordi's cuscuton et alternatives
- La plupart des papiers MOND théoriques
- Les formulations TeVeS, f(R), scalar-tensor

---

## 1. Portail de Soumission

🔗 **URL :** https://journals.aps.org/prd/authors
🔗 **Submission :** https://authors.aps.org/
🔗 **Scope :** https://journals.aps.org/prd/about

---

## 2. Compte

1. Créer un compte APS : https://journals.aps.org/
2. Associer ORCID : **0009-0009-7611-4550**
3. Affiliation : *Independent Researcher, Montréal, Québec, Canada*

---

## 3. Reframing — Adaptation du Manuscrit ApJ

Le manuscrit `docs/promotion-internationale/ARTICLE_ApJ_LATEX/ms.tex` doit être adapté pour PRD. Changements clés :

### Title
- **Avant (ApJ) :** *Temporal Distortion as a Unified Explanation for Dark Matter and Dark Energy: Validation Against Eight Independent Cosmological Datasets*
- **Après (PRD) :** *Temporal Distortion as a Unified Gravitational Framework for Dark Matter and Dark Energy: Theoretical Formulation and Observational Tests*

### Abstract Structure — Ordre PRD
1. **Théorie d'abord** : présenter |Ψ⟩ = α|t⟩ + β|t̄⟩ dès la 2e phrase
2. **Cadre GR** : insister sur la consistance avec la relativité générale
3. **Prédictions** : ensuite les formules M_eff et H(z,ρ)
4. **Validation** : les 8 tests en fin d'abstract
5. **p = 10⁻¹¹²** : dernière phrase

### Structure des Sections (style PRD)
| Section | Titre suggéré |
|---------|---------------|
| I | Introduction |
| II | **Theoretical Framework** (PLUS LONG qu'ApJ) |
| III | **Temporal Superposition and CPT Symmetry** (NOUVEAU) |
| IV | **Connection to Einstein Field Equations** (NOUVEAU) |
| V | Empirical Predictions |
| VI | Observational Validation |
| VII | Discussion |
| VIII | Conclusions |

### Ajouts Requis pour PRD
1. **Dérivation rigoureuse** de l'équation de Friedmann modifiée
2. **Démonstration** que |α|² + |β|² = 1 est conservé sous évolution
3. **Discussion CPT** explicite
4. **Comparaison** avec f(R), TeVeS, MOND, scalar-tensor
5. **Limite faible champ** exposée mathématiquement
6. **Section sur les tests prochains** (Euclid, LSST, DESI)

### Ce qu'il FAUT GARDER
- Les 8 tests observationnels (preuves du modèle)
- Les p-values et significativités
- Les figures et tables
- Les références SPARC, KiDS, COSMOS, Pantheon+

### Ce qu'il FAUT AJOUTER
- Section théorique sur 3–5 pages supplémentaires
- Équations numérotées pour CHAQUE étape clé
- Limites du modèle (Section Discussion)
- Discussion explicite de la stabilité quantique

---

## 4. Format LaTeX — REVTeX 4.2

PRD exige **REVTeX 4.2** (pas AASTeX, pas MNRAS class).

```latex
\documentclass[
  aps,
  prd,
  twocolumn,
  amsmath,
  amssymb,
  superscriptaddress,
  nofootinbib
]{revtex4-2}
```

🔗 **Téléchargement :** https://journals.aps.org/revtex

### Bibliographie
PRD utilise le style `apsrev4-2.bst` :
```latex
\bibliographystyle{apsrev4-2}
\bibliography{refs}
```

---

## 5. Fichiers à Préparer

| Fichier | Source | À Faire |
|---------|--------|---------|
| **ms.tex** (manuscrit PRD) | `docs/promotion-internationale/ARTICLE_ApJ_LATEX/ms.tex` | ⚙️ Adapter + reframe théorique |
| **cover_letter.tex** | `submissions/PRD/cover_letter.tex` | ✅ Prête |
| **refs.bib** | `docs/promotion-internationale/ARTICLE_ApJ_LATEX/refs.bib` | ✅ Compatible |
| **Figures** (PDF/EPS) | À créer | ⚙️ Courbes de rotation, r_c(M), H(z,ρ) |
| **Supplemental Material** | Scripts Python | Optionnel — bon pour crédibilité |

---

## 6. Formulaire de Soumission

### Step 1 — Journal & Section
☑ **Physical Review D**
☑ Section : **Cosmology, Dark Matter, Dark Energy**
☐ (ou) Section : **Classical General Relativity**

### Step 2 — Title & Abstract
- Title (voir section 3 ci-dessus)
- Abstract : ~200 mots, théorie en ouverture

### Step 3 — PACS Codes / Subject Areas
APS utilise **Physics Subject Headings (PhySH)** :
- `Cosmology` (parent)
- `Dark matter`
- `Dark energy`
- `Cosmological perturbations`
- `Modified theories of gravity`

### Step 4 — Authors
- **Corresponding :** Pierre-Olivier Després Asselin
- **Affiliation :** Independent Researcher, Montréal, Québec, Canada
- **ORCID :** 0009-0009-7611-4550
- **Email :** pierreolivierdespres@gmail.com

### Step 5 — Reviewers (obligatoires à PRD)
Fournir **minimum 3, recommandé 5** :
1. Niayesh Afshordi (Waterloo/Perimeter) — nafshordi@uwaterloo.ca
2. James Cline (McGill) — jcline@hep.physics.mcgill.ca
3. Rajendra Gupta (Ottawa) — rgupta4@uottawa.ca
4. Levon Pogosian (SFU) — levon@sfu.ca
5. Pedro Ferreira (Oxford) — pedro.ferreira@physics.ox.ac.uk

### Step 6 — Publication Options
- **Standard** (subscription) — par défaut
- **Open Access** (CC BY 4.0) — payant ($3200 USD) — peut demander waiver
- **Recommandation :** Standard, puis waiver si accepté.

### Step 7 — Declarations
- **Conflicts of interest :** None
- **Funding :** This research received no external funding
- **Previous submissions :** *"An earlier version was submitted to The Astrophysical Journal (AAS76125); declined on scope grounds (theoretical content not within ApJ's editorial scope). Companion observationally-focussed manuscript under review at MNRAS; brief empirical note under review at RNAAS."*

### Step 8 — Upload
1. `cover_letter.pdf`
2. `ms.tex` + toutes les figures
3. `refs.bib`
4. `supplemental.pdf` (optionnel : scripts Python expliqués)

---

## 7. Timeline Attendue

| Étape | Durée |
|-------|-------|
| Accusé de réception | 1–2 jours |
| Desk review | 1–3 semaines |
| Envoi referees (typiquement 2) | 4–10 semaines |
| Première décision | 2–5 mois |
| Révisions + acceptation | 3–8 mois supplémentaires |

**Total : 5–12 mois.**

---

## 8. Checklist avant Envoi

- [ ] Manuscrit converti en REVTeX 4.2 (pas AASTeX)
- [ ] Anglais **américain** (PRD est APS, pas MNRAS)
- [ ] Théorie présentée AVANT les observations
- [ ] Connection GR explicite (Section II ou III)
- [ ] Discussion CPT rigoureuse
- [ ] Limite faible champ dérivée
- [ ] Comparaison MOND / f(R) / TeVeS dans la Discussion
- [ ] Ω_m, Ω_Λ, H_0 cohérents avec Planck 2020
- [ ] Figures en vecteur (PDF ou EPS)
- [ ] Supplemental Material citant les scripts GitHub
- [ ] 5 reviewers suggérés (PAS 3)
- [ ] Cover letter mentionne le desk-reject ApJ avec transparence

---

## 9. Contact Éditorial

**APS Editorial Office**
Email : prd@aps.org
Phone : +1 631 591 4000
Portal : https://authors.aps.org/

**Editor-in-Chief PRD :** Prof. Robert Garisto
