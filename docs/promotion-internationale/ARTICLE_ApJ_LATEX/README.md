# Article ApJ — Format LaTeX (AASTeX 6.3.1)

## Fichiers

| Fichier | Description |
|---------|-------------|
| `ms.tex` | Article principal (à compiler) |
| `refs.bib` | Bibliographie BibTeX (17 références) |
| `aastex631.cls` | Classe LaTeX AAS — **à télécharger** (voir ci-dessous) |

---

## Étape 1 — Télécharger la classe AASTeX

Télécharge le fichier `aastex631.cls` depuis le site officiel AAS :

```
https://journals.aas.org/aastexguide/
```

Clique sur **Download AASTeX** → place `aastex631.cls` dans ce même dossier.

---

## Étape 2 — Avant de compiler : ajouter ton ORCID

Ouvre `ms.tex` et remplace la ligne :
```latex
\orcid{0000-0000-0000-0000}
```
par ton vrai numéro ORCID obtenu sur https://orcid.org/register

---

## Étape 3 — Compiler le PDF

### Option A — Avec latexmk (recommandé)
```bash
latexmk -pdf ms.tex
```

### Option B — Manuellement (4 passes)
```bash
pdflatex ms.tex
bibtex ms
pdflatex ms.tex
pdflatex ms.tex
```

Le fichier `ms.pdf` est prêt pour soumission.

---

## Étape 4 — Soumission ApJ

1. Va sur : https://www.journals.aas.org/submission/
2. Crée un compte AAS (si pas déjà fait)
3. Catégorie : **Galaxies and Cosmology**
4. Téléverse `ms.tex` + `refs.bib` + `aastex631.cls`
5. Demande un waiver financier si nécessaire

---

## Overleaf (alternative en ligne — recommandé si pas de LaTeX local)

1. Va sur https://www.overleaf.com
2. **New Project → Blank Project**
3. Téléverse `ms.tex`, `refs.bib`, et `aastex631.cls`
4. Compile directement dans le navigateur
5. Télécharge le PDF pour soumission

Overleaf est **gratuit** pour usage basique et **recommandé** pour les premiers pas en LaTeX.
