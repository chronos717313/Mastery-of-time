# Guide de Soumission — JCAP

**Journal :** Journal of Cosmology and Astroparticle Physics
**Éditeur :** IOP Publishing / SISSA (Scuola Internazionale Superiore di Studi Avanzati)
**Impact factor :** ~6.8 (2024) — **le plus haut en cosmologie théorique**
**Type :** Regular article

---

## Pourquoi JCAP est un Candidat Idéal

| Critère | JCAP |
|---------|------|
| Accepte la cosmologie théorique | ✅ Cœur du journal |
| Accepte dark matter / dark energy alternatives | ✅ Routinier |
| Accepte « phenomenological dark-sector models » | ✅ Une catégorie éditoriale dédiée |
| Délai review | Plus rapide que PRD (souvent 2–3 mois) |
| Open access | Gratuit en voie subscription + open access facultatif |
| Impact communauté théorique | Très élevé — beaucoup de citations |

JCAP publie fréquemment des alternatives à ΛCDM, des modèles de gravité modifiée (f(R), DHOST, scalar-tensor), et la résolution de la tension H₀.

---

## 1. Portail de Soumission

🔗 **URL :** https://jcap.sissa.it/
🔗 **Submission :** https://mc04.manuscriptcentral.com/jcap-iop
🔗 **Author guide :** https://iopscience.iop.org/journal/1475-7516

---

## 2. Compte

1. Créer un compte IOP ScholarOne Manuscripts
2. Associer ORCID : **0009-0009-7611-4550**
3. Affiliation : *Independent Researcher, Montréal, Québec, Canada*

---

## 3. Reframing pour JCAP

Le manuscrit PRD fonctionne bien pour JCAP avec des ajustements mineurs. Différences clés :

### Ton
- **PRD** : ton théorique rigoureux (dérivations détaillées)
- **JCAP** : équilibre théorie + phénoménologie + observations

### Structure JCAP Typique
| Section | Titre |
|---------|-------|
| 1 | Introduction |
| 2 | Theoretical framework |
| 3 | Phenomenological predictions |
| 4 | Observational tests |
| 5 | Discussion and forecasts |
| 6 | Conclusions |

### Adaptations vs. version PRD
1. **Plus d'accent sur les prédictions pour Euclid / LSST / DESI** (JCAP apprécie le contenu prédictif pour surveys futurs)
2. **Moins de formalisme CPT** — 1 paragraphe au lieu d'une section entière
3. **Ajouter un forecast** : nombre de galaxies Euclid requis pour un test décisif
4. **Fisher matrix** ou analyse MCMC optionnelle mais appréciée

### Title Proposé pour JCAP
*A Temporal-Distortion Framework for the Dark Sector: Unified Treatment of Galactic Dynamics, the Hubble Tension, and Weak Lensing Isotropy*

---

## 4. Format LaTeX — JCAP Template

JCAP utilise une classe LaTeX dédiée `jcappub.cls` :

```latex
\documentclass[a4paper,11pt]{article}
\usepackage{jcappub}
```

🔗 **Template :** https://jcap.sissa.it/jcap/help/helpLoader.jsp?pgType=author

### Bibliographie
Style JCAP : `JHEP.bst` (même style que JHEP)
```latex
\bibliographystyle{JHEP}
\bibliography{refs}
```

---

## 5. Fichiers à Préparer

| Fichier | Source | À Faire |
|---------|--------|---------|
| **ms.tex** (JCAP format) | Version PRD + adaptations | ⚙️ Reformater |
| **cover_letter.tex** | `submissions/JCAP/cover_letter.tex` | ✅ Prête |
| **refs.bib** | `docs/promotion-internationale/ARTICLE_ApJ_LATEX/refs.bib` | ✅ Compatible |
| **Figures** (PDF) | À créer | ⚙️ Rotation curves, r_c(M), H(z,ρ) |

---

## 6. Formulaire de Soumission

### Step 1 — Journal & Category
☑ **JCAP**
☑ Subject category : **Alternatives to dark matter (or general dark matter models)**
☑ Or : **Dark energy theory**

### Step 2 — Article Type
☑ **Article** (pas Letter, pas Erratum)

### Step 3 — Title & Abstract
- Title : voir ci-dessus
- Abstract ≈ 200–250 mots

### Step 4 — Keywords (JCAP free-text, choose 4–6)
- dark matter theory
- dark energy theory
- modified gravity
- rotation curves of galaxies
- weak gravitational lensing
- Hubble tension

### Step 5 — Authors
- **Corresponding :** Pierre-Olivier Després Asselin
- **Affiliation :** Independent Researcher, Montréal, Québec, Canada
- **ORCID :** 0009-0009-7611-4550
- **Email :** pierreolivierdespres@gmail.com

### Step 6 — Reviewers (minimum 3 recommandé)
1. Niayesh Afshordi — nafshordi@uwaterloo.ca
2. Levon Pogosian — levon@sfu.ca
3. Rajendra Gupta — rgupta4@uottawa.ca
4. Alessandra Silvestri — silvestri@lorentz.leidenuniv.nl
5. Pedro Ferreira — pedro.ferreira@physics.ox.ac.uk

### Step 7 — Publication Option
- **Subscription** (standard, gratuit pour l'auteur) ← par défaut
- **Open Access** (APC ~$2500) — peut demander waiver

### Step 8 — Declarations
- **Conflicts :** None
- **Funding :** No external funding
- **Data availability :** Public (GitHub + Zenodo DOI)
- **Previous submissions :** *"An earlier version was submitted to The Astrophysical Journal (AAS76125) and declined on scope grounds (theoretical content not within ApJ's editorial policy). Companion observationally focussed manuscript under review at MNRAS; brief empirical research note under review at RNAAS; theoretical companion in preparation for PRD."*

### Step 9 — Upload
1. `cover_letter.pdf`
2. `ms.tex` + figures
3. `refs.bib`
4. Supplemental materials (optionnel)

---

## 7. Timeline JCAP

| Étape | Durée |
|-------|-------|
| Accusé de réception | 1 jour |
| Desk review | 1–2 semaines |
| Envoi referees | 2–6 semaines |
| Première décision | 2–4 mois |
| Révisions + acceptation | 2–6 mois |

**Total : 4–8 mois** (plus rapide que PRD).

---

## 8. Checklist avant Envoi JCAP

- [ ] Manuscrit en LaTeX classe `jcappub`
- [ ] Anglais britannique OU américain (JCAP accepte les deux — rester cohérent)
- [ ] Section Theoretical framework + Phenomenology distinctes
- [ ] Prédictions pour Euclid / LSST / DESI explicitement quantifiées
- [ ] Comparaison avec MOND, f(R), CCC+TL dans Discussion
- [ ] 5 reviewers suggérés
- [ ] Figures en PDF (vecteur)
- [ ] Citations JCAP récentes (au moins 3 papers JCAP 2023–2025)

---

## 9. Contact Éditorial

**JCAP Editorial Office**
Email : jcap-eo@sissa.it
Portal : https://mc04.manuscriptcentral.com/jcap-iop
Web : https://jcap.sissa.it/
