# Guide de Conversion - Format PDF/Word

**Document source**: `docs/fr/00-vulgarisation/TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md`

---

## 🚀 MÉTHODE 1: Script Automatique (Recommandé)

### Si vous êtes sur Linux/Mac:

```bash
# Depuis la racine du projet
./scripts/convert_to_pdf_word.sh
```

Le script va:
1. Vérifier si pandoc est installé
2. Proposer de l'installer si nécessaire
3. Créer 3 versions: PDF, DOCX, HTML

**Résultat**: Fichiers dans `docs/fr/00-vulgarisation/exports/`

---

## 🌐 MÉTHODE 2: Outils en Ligne (Sans Installation)

### Option A: Markdown to PDF Online

**Site**: https://www.markdowntopdf.com/

**Étapes**:
1. Ouvrir le fichier `TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md`
2. Copier tout le contenu (Ctrl+A, Ctrl+C)
3. Coller dans l'éditeur en ligne
4. Cliquer "Convert to PDF"
5. Télécharger le PDF

**Avantages**: ✅ Rapide, ✅ Aucune installation
**Inconvénients**: ⚠️ Mise en page basique

---

### Option B: Dillinger.io

**Site**: https://dillinger.io/

**Étapes**:
1. Aller sur https://dillinger.io/
2. Cliquer "Import from" → "Local Disk"
3. Sélectionner `TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md`
4. Prévisualiser le rendu
5. Export → "Styled HTML" ou "PDF"

**Avantages**: ✅ Prévisualisation, ✅ Bonne mise en page
**Inconvénients**: ⚠️ Export Word limité

---

### Option C: HackMD

**Site**: https://hackmd.io/

**Étapes**:
1. Créer un compte gratuit sur HackMD
2. Nouveau document
3. Coller le contenu Markdown
4. Menu → Export → PDF ou Markdown → Word (via Pandoc)

**Avantages**: ✅ Excellente mise en page, ✅ Support LaTeX
**Inconvénients**: ⚠️ Compte requis

---

## 💻 MÉTHODE 3: Éditeurs Desktop

### Option A: Typora (Payant mais excellent)

**Site**: https://typora.io/

**Prix**: ~15€ (licence à vie)

**Étapes**:
1. Installer Typora
2. Ouvrir `TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md`
3. File → Export → PDF/Word/HTML

**Avantages**: ✅ WYSIWYG, ✅ Excellente qualité, ✅ Thèmes
**Inconvénients**: ⚠️ Payant

---

### Option B: Visual Studio Code + Extensions

**Gratuit**: https://code.visualstudio.com/

**Extensions à installer**:
- Markdown PDF (yzane.markdown-pdf)
- Markdown All in One

**Étapes**:
1. Ouvrir VS Code
2. Installer extensions
3. Ouvrir le fichier .md
4. Ctrl+Shift+P → "Markdown PDF: Export (pdf)"

**Avantages**: ✅ Gratuit, ✅ Éditeur puissant
**Inconvénients**: ⚠️ Setup initial

---

### Option C: LibreOffice Writer (Gratuit)

**Site**: https://www.libreoffice.org/

**Étapes**:
1. Installer LibreOffice
2. Installer extension Markdown Writer: Pandoc
3. File → Open → Sélectionner .md
4. File → Export as PDF

**Avantages**: ✅ Gratuit, ✅ Open source
**Inconvénients**: ⚠️ Qualité moyenne

---

## 🔧 MÉTHODE 4: Pandoc en Ligne de Commande

### Installation Pandoc

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended
```

**macOS**:
```bash
brew install pandoc
brew install --cask basictex
```

**Windows**:
- Télécharger: https://pandoc.org/installing.html
- Installer MiKTeX: https://miktex.org/download

---

### Commandes de Conversion

**PDF haute qualité**:
```bash
pandoc docs/fr/00-vulgarisation/TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md \
  -o Guide_TMT_vs_LCDM.pdf \
  --pdf-engine=pdflatex \
  --toc \
  --toc-depth=2 \
  --number-sections \
  -V geometry:margin=2.5cm \
  -V fontsize=11pt \
  -V lang=fr \
  --metadata title="Théorie de Maîtrise du Temps vs ΛCDM" \
  --metadata author="Pierre-Olivier Després Asselin"
```

**Word (DOCX)**:
```bash
pandoc docs/fr/00-vulgarisation/TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md \
  -o Guide_TMT_vs_LCDM.docx \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --metadata title="Théorie de Maîtrise du Temps vs ΛCDM"
```

**HTML standalone**:
```bash
pandoc docs/fr/00-vulgarisation/TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md \
  -o Guide_TMT_vs_LCDM.html \
  --standalone \
  --toc \
  --mathjax \
  --css=https://latex.now.sh/style.css
```

---

## 📋 COMPARAISON DES MÉTHODES

| Méthode | Difficulté | Qualité PDF | Qualité Word | Temps | Gratuit |
|---------|-----------|-------------|--------------|-------|---------|
| **Script auto** | ⭐ Facile | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 2 min | ✅ |
| **Markdown to PDF** | ⭐ Facile | ⭐⭐⭐ | ❌ | 1 min | ✅ |
| **Dillinger** | ⭐ Facile | ⭐⭐⭐⭐ | ⭐⭐ | 3 min | ✅ |
| **HackMD** | ⭐⭐ Moyen | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 5 min | ✅ |
| **Typora** | ⭐ Facile | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 1 min | ❌ |
| **VS Code** | ⭐⭐ Moyen | ⭐⭐⭐⭐ | ⭐⭐⭐ | 5 min | ✅ |
| **LibreOffice** | ⭐⭐ Moyen | ⭐⭐⭐ | ⭐⭐⭐ | 5 min | ✅ |
| **Pandoc CLI** | ⭐⭐⭐ Avancé | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 3 min | ✅ |

---

## 💡 RECOMMANDATIONS

### Pour une utilisation immédiate:
👉 **Méthode 2A ou 2B** (en ligne, 1-3 min)

### Pour la meilleure qualité:
👉 **Méthode 1** (script automatique) ou **Méthode 4** (Pandoc)

### Pour édition Word ultérieure:
👉 **Typora** ou **Pandoc → DOCX**

---

## ⚠️ NOTES IMPORTANTES

### Formules mathématiques
Les formules comme `Φ²/c⁴` peuvent ne pas s'afficher correctement selon la méthode:
- ✅ **Bien rendu**: Pandoc, Typora, HackMD
- ⚠️ **Peut nécessiter ajustements**: Outils en ligne basiques

### Tableaux
Les tableaux complexes sont bien gérés par:
- ✅ Pandoc
- ✅ Typora
- ⚠️ Peut être déformé dans convertisseurs basiques

### Schémas ASCII
Les schémas comme le réseau Asselin sont mieux rendus avec:
- ✅ Police monospace (Courier, Consolas)
- ✅ Pandoc avec options de formatage
- ⚠️ Peuvent être déformés dans Word (ajuster manuellement)

---

## 🆘 BESOIN D'AIDE?

Si aucune méthode ne fonctionne, vous pouvez:

1. **Demander une conversion manuelle**:
   - Envoyer le .md à un service de conversion
   - Utiliser Google Docs (Import → Markdown)

2. **Version HTML puis Impression PDF**:
   ```bash
   # Le script crée aussi un HTML
   # Ouvrir dans navigateur → Imprimer → Enregistrer PDF
   ```

3. **Copier-coller dans Word**:
   - Ouvrir le .md dans éditeur texte
   - Copier tout
   - Coller dans Word
   - Appliquer styles manuellement

---

## ✅ CHECKLIST POST-CONVERSION

Après conversion, vérifier:

- [ ] Table des matières générée correctement
- [ ] Glossaire lisible (page 1)
- [ ] Formules mathématiques correctes (Φ, c², etc.)
- [ ] Tableaux bien alignés
- [ ] Schémas ASCII en police monospace
- [ ] Numérotation des sections
- [ ] Références croisées (§4, §5, etc.) cliquables
- [ ] Métadonnées (auteur, date, titre)
- [ ] 13 pages environ

---

**Bonne conversion!** 🚀

Pour toute question: pierreolivierdespres@gmail.com
