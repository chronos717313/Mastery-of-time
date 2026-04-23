# Stratégie de Soumission TMT — Vue d'Ensemble

**Auteur :** Pierre-Olivier Després Asselin
**ORCID :** 0009-0009-7611-4550
**Date :** Avril 2026
**Contexte :** Manuscrit ApJ desk-rejeté le 23 avril 2026 (AAS76125) — périmètre inadéquat pour la physique théorique

---

## 1. Ce qui s'est passé

| Date | Événement |
|------|-----------|
| 16-Apr-2026 | Soumission du manuscrit à ApJ (AAS76125) |
| 23-Apr-2026 | Desk rejection par Prof. Christopher Conselice |

**Motif du refus :** *"ApJ only publishes manuscripts based on the gathering, reporting and analysis of observational data and not manuscripts of a theoretical nature of fundamental physics."*

**Lecture juste :** il ne s'agit **pas** d'un refus scientifique. La théorie n'a pas été évaluée sur le fond. C'est un rejet de **scope éditorial** : l'ApJ ne publie pas de physique théorique fondamentale, même quand elle est validée par des données. Il faut viser des journaux dont le périmètre accueille explicitement la cosmologie théorique.

---

## 2. Stratégie en 4 Soumissions Parallèles

### Vue d'ensemble

| # | Journal | Type | Focus | Statut |
|---|---------|------|-------|--------|
| 1 | **MNRAS** | Article complet | Framework théorique + validation observationnelle | Paquet prêt |
| 2 | **RNAAS** | Research Note | **Résultat empirique r_c(M) SEULEMENT** (anti-scope-reject) | Paquet prêt |
| 3 | **Physical Review D** | Article complet | **Théorie** (CPT, GR, dérivations) | Paquet prêt |
| 4 | **JCAP** | Article complet | Théorie + phénoménologie + forecasts | Paquet prêt |

### Pourquoi 4 soumissions ?

L'objectif n'est **pas** la quantité mais de cibler chaque journal selon son périmètre :

- **MNRAS** accueille la cosmologie théorique appliquée aux observations → cadre complet
- **RNAAS** n'accepte que des résultats courts et observationnels → se limiter à la loi r_c(M)
- **PRD** est le journal de référence pour la physique théorique de la gravité → emphasis sur la dérivation CPT et la limite GR
- **JCAP** est le meilleur pour la phénoménologie dark-sector → emphasis sur les prédictions pour Euclid/DESI

### Règles de parallélisation

**Éthique de la publication scientifique :**
- ❌ **NE JAMAIS** soumettre le **même** manuscrit à 2 journaux en même temps (double submission — interdit)
- ✅ **IL EST PERMIS** de soumettre des manuscrits **distincts** (périmètres, titres, structures différents) qui se **citent** mutuellement comme *« companion paper »*
- ✅ Les cover letters mentionnent **explicitement** les soumissions parallèles

**Chaque manuscrit est donc distinct par son angle :**
- MNRAS → cadre + observations (orienté astronomie)
- RNAAS → 1 résultat empirique (note courte, purement observationnelle)
- PRD → théorie rigoureuse (CPT, GR, formalisme)
- JCAP → théorie + forecasts (prédictions futures)

---

## 3. Ordre Chronologique Recommandé

Pour minimiser les risques et maximiser les retours utiles :

### Phase 1 — Semaine 1 (immédiat)
**Priorité 1 :** Soumettre à **JCAP**
- Le plus compatible avec ton manuscrit actuel (cosmologie théorique)
- Délai de retour le plus rapide (4–8 mois)
- Adaptations minimes

**Priorité 2 :** Soumettre à **RNAAS**
- Manuscrit déjà prêt, court (<1500 mots)
- Va consolider le résultat empirique dans ADS
- Risque de scope-reject si mal cadré → suivre strictement le guide

### Phase 2 — Semaine 2–3
**Priorité 3 :** Soumettre à **MNRAS**
- Article complet adapté en anglais britannique
- Subscription track = gratuit
- Bon complément à JCAP (périmètres différents)

### Phase 3 — Semaine 3–4
**Priorité 4 :** Soumettre à **PRD**
- Nécessite le plus d'adaptation (CPT formel, reformulation GR)
- Le mieux pour la postérité scientifique
- Délai plus long mais prestige élevé

**Justification de l'ordre :** commencer par les cibles à plus forte probabilité et à traitement rapide (JCAP, RNAAS) pour obtenir des retours, puis étendre aux cibles plus exigeantes (MNRAS, PRD) avec les ajustements appris.

---

## 4. Structure des Paquets de Soumission

```
submissions/
├── STRATEGIE_SOUMISSION.md         ← CE DOCUMENT
├── MNRAS/
│   ├── cover_letter.tex            ← Lettre éditeur
│   └── SUBMISSION_GUIDE.md         ← Instructions pas-à-pas
├── RNAAS/
│   ├── cover_letter.tex
│   └── SUBMISSION_GUIDE.md         (avec warnings anti-scope-reject)
├── PRD/
│   ├── cover_letter.tex
│   ├── abstract_PRD.md             ← Abstract reformulé
│   └── SUBMISSION_GUIDE.md
└── JCAP/
    ├── cover_letter.tex
    └── SUBMISSION_GUIDE.md
```

**Sources du manuscrit (déjà dans le dépôt) :**
- `docs/promotion-internationale/ARTICLE_ApJ_DRAFT.md` — version ApJ (refusée)
- `docs/promotion-internationale/ARTICLE_MNRAS_DRAFT.md` — version MNRAS (adaptée)
- `docs/promotion-internationale/RNAAS_SUBMISSION_DRAFT.md` — note RNAAS
- `docs/promotion-internationale/ARTICLE_ApJ_LATEX/` — version LaTeX complète
- `docs/promotion-internationale/ARTICLE_ApJ_LATEX/refs.bib` — bibliographie partagée

---

## 5. Risques et Mitigations

| Risque | Probabilité | Mitigation |
|--------|-------------|------------|
| **RNAAS reject scope** (mêmes règles que ApJ) | Moyenne | Supprimer toute théorie ; ne présenter que la loi empirique r_c(M) ; cover letter explicite |
| **Accusation de duplication** | Faible | Titres, abstracts, structures distincts ; cover letters transparentes ; mention des soumissions parallèles |
| **Reviewer hostile (chercheur indépendant)** | Moyenne | Code ouvert, données publiques, reproductibilité |
| **Exigence de révisions majeures** | Haute | Normal — budgeter 2–3 rounds de révision par journal |
| **Manque d'affiliation institutionnelle** | Faible | ORCID établi + GitHub + Zenodo DOI suffisent |

---

## 6. Budget Prévisionnel (Coûts Publication)

| Journal | Voie standard | Open access | Waiver possible ? |
|---------|---------------|-------------|-------------------|
| MNRAS | **Gratuit** (Subscription Track) | ~3500 USD | N/A (gratuit) |
| RNAAS | ~225 USD | — | ✅ (chercheur indépendant) |
| PRD | **Gratuit** (Subscription) | ~3200 USD | ✅ sur demande |
| JCAP | **Gratuit** (Subscription) | ~2500 USD | ✅ sur demande |

**Stratégie budget :** choisir la voie subscription pour les 3 grands journaux, et demander le waiver pour RNAAS. Coût total attendu : **0 $** si les waivers sont accordés.

---

## 7. Tracking des Soumissions

Après chaque soumission, noter dans ce tableau :

| Journal | Manuscript ID | Date soumission | Statut | Dernière action |
|---------|---------------|-----------------|--------|-----------------|
| ApJ | AAS76125 | 16-Apr-2026 | ❌ Desk rejected | 23-Apr-2026 |
| MNRAS | MN-26-1174-P | 23-Apr-2026 | 🟡 Under review | 23-Apr-2026 |
| JCAP | — | — | ⏳ Bloqué (arXiv requis) | — |
| RNAAS | — | — | À soumettre | — |
| PRD | — | — | À soumettre | — |

---

## 8. Checklist Maîtresse Avant Chaque Soumission

Pour chaque soumission, vérifier :

- [ ] Manuscrit dans le bon format LaTeX (revtex/mnras/aastex/jcappub)
- [ ] Cover letter mentionne ApJ desk-reject avec transparence
- [ ] Cover letter mentionne les soumissions parallèles (si applicable)
- [ ] ORCID 0009-0009-7611-4550 partout
- [ ] Affiliation : *Independent Researcher, Montréal, Québec, Canada*
- [ ] 3–5 reviewers suggérés
- [ ] Aucun reviewer exclu
- [ ] Déclarations : no funding, no conflicts
- [ ] Data availability : GitHub + Zenodo DOI
- [ ] PDF final compilé et relu
- [ ] Tous les fichiers dans l'ordre d'upload

---

## 9. Communication Publique

**Règles pendant la période de review (~4–12 mois) :**

- ✅ **OK** : parler du projet sur le site web, GitHub, Zenodo
- ✅ **OK** : mentionner *« under review at MNRAS / JCAP / PRD »*
- ❌ **PAS OK** : annoncer publiquement *« accepted »* avant acceptation formelle
- ❌ **PAS OK** : réutiliser le communiqué de presse tel quel pendant la review
- ❌ **PAS OK** : annoncer publiquement le desk-reject ApJ (crée une image négative)

**Mise à jour recommandée du communiqué de presse :**
- Remplacer *« in cours de soumission à ApJ »* par *« soumis à JCAP, MNRAS, et Physical Review D »*
- Ne pas détailler la séquence chronologique

---

## 10. Ressources et Contacts

### Documents internes
- `docs/promotion-internationale/ARTICLE_ApJ_DRAFT.md`
- `docs/promotion-internationale/ARTICLE_MNRAS_DRAFT.md`
- `docs/promotion-internationale/RNAAS_SUBMISSION_DRAFT.md`
- `docs/promotion-internationale/ARTICLE_ApJ_LATEX/ms.tex`

### Portails de soumission
- **MNRAS :** https://mc.manuscriptcentral.com/mnras
- **RNAAS :** https://aas.msubmit.net
- **PRD :** https://authors.aps.org/
- **JCAP :** https://mc04.manuscriptcentral.com/jcap-iop

### Templates LaTeX
- **MNRAS :** https://academic.oup.com/mnras/pages/mnras_template
- **AASTeX v7 :** https://journals.aas.org/manuscript-preparation/
- **REVTeX 4.2 :** https://journals.aps.org/revtex
- **JCAP :** https://jcap.sissa.it/jcap/help/helpLoader.jsp?pgType=author

### Contact auteur
- **Email :** pierreolivierdespres@gmail.com
- **ORCID :** 0009-0009-7611-4550
- **GitHub :** https://github.com/chronos717313/Mastery-of-time
- **Zenodo DOI :** 10.5281/zenodo.18287042

---

*Document vivant — à mettre à jour après chaque soumission et chaque décision éditoriale.*
