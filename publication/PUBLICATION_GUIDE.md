# TMT v2.4 Publication Guide

**Document créé:** 30 Janvier 2026  
**Auteur:** Pierre-Olivier Després  
**Article:** Time Mastery Theory: A Scalar Temporal Distortion Model for Galaxy Rotation Curves and Cosmological Tensions

---

## Fichiers de Publication

| Fichier | Description |
|---------|-------------|
| `article_TMT_v24.tex` | Source LaTeX de l'article |
| `TMT_v24.bib` | Bibliographie (16 références) |
| `TMT_v24_Article.pdf` | PDF compilé (Overleaf) |
| `figures/` | Dossier pour les figures |

---

## Stratégie de Publication (3 Étapes)

### Étape 1: arXiv (Priorité HAUTE)

**URL:** https://arxiv.org  
**Catégorie:** `astro-ph.CO` (Cosmology and Nongalactic Astrophysics)  
**Coût:** Gratuit  
**Délai:** 1-2 jours pour modération

**Processus:**
1. Créer un compte arXiv
2. Obtenir un "endorsement" (requis pour première soumission)
3. Uploader: `article_TMT_v24.tex`, `TMT_v24.bib`, figures
4. Soumettre en catégorie `astro-ph.CO`
5. Recevoir identifiant `arXiv:2601.XXXXX`

**Avantages:**
- Visibilité immédiate dans la communauté scientifique
- DOI permanent
- Citable immédiatement
- Gratuit

**Note:** L'endorsement peut être obtenu d'un chercheur avec publications arXiv récentes en astro-ph.

---

### Étape 2: Zenodo (Même semaine qu'arXiv)

**URL:** https://zenodo.org  
**Coût:** Gratuit  
**DOI existant:** 10.5281/zenodo.18287042

**Contenu à uploader:**
- Article PDF
- Code source (scripts validation)
- Données SPARC utilisées
- Résultats de validation

**Package existant:** `zenodo_package/`

---

### Étape 3: Journal Peer-Reviewed (Après arXiv)

#### Options recommandées:

| Journal | Impact Factor | Délai Review | Coût Approx. |
|---------|---------------|--------------|--------------|
| **JCAP** | ~6 | 2-4 mois | ~$1,500 USD |
| **MNRAS** | ~5 | 2-6 mois | ~$2,000 USD |
| **A&A** | ~6 | 2-4 mois | ~€150/page |
| **Phys. Rev. D** | ~5 | 3-6 mois | ~$2,000 USD |
| **ApJ** | ~5 | 2-4 mois | ~$200/page |

#### Recommandation: **JCAP** (Journal of Cosmology and Astroparticle Physics)
- Spécialisé en cosmologie
- Bon impact factor
- Délai raisonnable
- Accepte les théories alternatives si bien documentées

---

## Résultats Clés à Mettre en Avant

| Test | Résultat | Significativité |
|------|----------|-----------------|
| SPARC Rotation Curves | 156/156 (100%) | p = 7.9×10⁻⁴³ |
| Loi r_c(M) | r = 0.768 | p = 3×10⁻²¹ |
| Loi k(M) | R² = 0.64 | p = 1.5×10⁻³⁹ |
| SNIa Environnement | +0.46% (préd: +0.57%) | Direction correcte |
| Tension H₀ | 100% résolue | H₀ = 73.0 km/s/Mpc |
| **Combiné (Fisher)** | **8/8 tests** | **p = 10⁻¹¹² (>15σ)** |

---

## Checklist Avant Soumission

### Pour arXiv:
- [ ] Compte arXiv créé
- [ ] Endorsement obtenu
- [ ] PDF compile sans erreurs
- [ ] Bibliographie complète
- [ ] Figures de haute qualité (si ajoutées)
- [ ] Abstract < 1920 caractères
- [ ] Titre clair et descriptif

### Pour Journal:
- [ ] Lettre de motivation (cover letter)
- [ ] Suggested reviewers (3-5 noms)
- [ ] Conflicts of interest déclarés
- [ ] Formatting selon guidelines du journal
- [ ] Supplementary materials préparés

---

## Contacts Utiles

### Endorsement arXiv
Pour obtenir un endorsement, contacter un chercheur actif en cosmologie:
- Professeurs en astrophysique dans universités canadiennes
- Auteurs récents sur arXiv en astro-ph.CO
- Membres de collaborations (DESI, Euclid, etc.)

### Ressources
- arXiv help: https://arxiv.org/help
- JCAP submission: https://jcap.sissa.it/
- MNRAS submission: https://academic.oup.com/mnras
- Zenodo: https://zenodo.org/deposit

---

## Timeline Suggérée

| Semaine | Action |
|---------|--------|
| **S1** | Finaliser PDF, obtenir endorsement arXiv |
| **S2** | Soumettre arXiv + Zenodo |
| **S3** | Attendre retour arXiv, préparer figures |
| **S4** | Soumettre à JCAP (si budget disponible) |
| **S5-S16** | Processus de peer review |

---

## Notes

- L'article actuel est prêt pour arXiv (format revtex4-2)
- Les figures peuvent être ajoutées pour renforcer l'article
- Le code de validation est disponible dans `scripts/validation/`
- Les données SPARC sont publiques et citées correctement

---

## Suivi

- [ ] **arXiv soumis:** ____
- [ ] **arXiv ID:** arXiv:____
- [ ] **Zenodo mis à jour:** ____
- [ ] **Journal soumis:** ____
- [ ] **Journal accepté:** ____

---

*Dernière mise à jour: 30 Janvier 2026*
