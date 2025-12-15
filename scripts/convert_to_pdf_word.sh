#!/bin/bash
# Script de conversion Markdown → PDF/Word
# Guide pédagogique TMT vs ΛCDM

set -e

INPUT_FILE="docs/fr/00-vulgarisation/TMT_vs_LCDM_GUIDE_PEDAGOGIQUE.md"
OUTPUT_DIR="docs/fr/00-vulgarisation/exports"
BASENAME="TMT_vs_LCDM_Guide_Pedagogique"

# Créer répertoire de sortie
mkdir -p "$OUTPUT_DIR"

echo "🔄 Conversion du guide pédagogique TMT vs ΛCDM..."
echo ""

# Fonction pour installer pandoc si nécessaire
install_pandoc() {
    echo "📦 Installation de pandoc..."

    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
    elif command -v yum &> /dev/null; then
        sudo yum install -y pandoc texlive
    elif command -v brew &> /dev/null; then
        brew install pandoc
        brew install --cask mactex-no-gui
    else
        echo "❌ Gestionnaire de paquets non supporté"
        echo "   Installez pandoc manuellement: https://pandoc.org/installing.html"
        exit 1
    fi
}

# Vérifier si pandoc est installé
if ! command -v pandoc &> /dev/null; then
    echo "⚠️  pandoc n'est pas installé"
    read -p "   Voulez-vous l'installer? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        install_pandoc
    else
        echo "❌ Conversion annulée (pandoc requis)"
        echo ""
        echo "📌 ALTERNATIVES:"
        echo "   1. Convertisseur en ligne: https://www.markdowntopdf.com/"
        echo "   2. Dillinger.io: https://dillinger.io/ (exporter PDF/Word)"
        echo "   3. Typora: https://typora.io/ (éditeur avec export)"
        exit 1
    fi
fi

echo "✅ pandoc détecté: $(pandoc --version | head -1)"
echo ""

# Conversion en PDF avec LaTeX
echo "📄 Conversion en PDF..."
pandoc "$INPUT_FILE" \
    -o "$OUTPUT_DIR/${BASENAME}.pdf" \
    --pdf-engine=pdflatex \
    --toc \
    --toc-depth=2 \
    --number-sections \
    -V geometry:margin=2.5cm \
    -V fontsize=11pt \
    -V documentclass=article \
    -V lang=fr \
    -V mainfont="DejaVu Serif" \
    --highlight-style=tango \
    --metadata title="Théorie de Maîtrise du Temps vs ΛCDM" \
    --metadata author="Pierre-Olivier Després Asselin" \
    --metadata date="Décembre 2025" \
    2>&1 || {
        echo "⚠️  Conversion PDF échouée (possiblement LaTeX non installé)"
        echo "   Essai avec méthode alternative..."

        # Méthode alternative sans LaTeX
        pandoc "$INPUT_FILE" \
            -o "$OUTPUT_DIR/${BASENAME}.html" \
            --standalone \
            --toc \
            --toc-depth=2 \
            --css=https://latex.now.sh/style.css \
            --metadata title="Théorie de Maîtrise du Temps vs ΛCDM"

        echo "✅ HTML créé: $OUTPUT_DIR/${BASENAME}.html"
        echo "   Ouvrez dans un navigateur et imprimez en PDF"
    }

if [ -f "$OUTPUT_DIR/${BASENAME}.pdf" ]; then
    echo "✅ PDF créé: $OUTPUT_DIR/${BASENAME}.pdf"
    echo "   Taille: $(du -h "$OUTPUT_DIR/${BASENAME}.pdf" | cut -f1)"
fi

# Conversion en Word (.docx)
echo ""
echo "📝 Conversion en Word (DOCX)..."
pandoc "$INPUT_FILE" \
    -o "$OUTPUT_DIR/${BASENAME}.docx" \
    --toc \
    --toc-depth=2 \
    --number-sections \
    --reference-doc=reference.docx \
    --metadata title="Théorie de Maîtrise du Temps vs ΛCDM" \
    --metadata author="Pierre-Olivier Després Asselin" \
    2>&1 || {
        # Sans document de référence
        pandoc "$INPUT_FILE" \
            -o "$OUTPUT_DIR/${BASENAME}.docx" \
            --toc \
            --toc-depth=2 \
            --metadata title="Théorie de Maîtrise du Temps vs ΛCDM"
    }

if [ -f "$OUTPUT_DIR/${BASENAME}.docx" ]; then
    echo "✅ Word créé: $OUTPUT_DIR/${BASENAME}.docx"
    echo "   Taille: $(du -h "$OUTPUT_DIR/${BASENAME}.docx" | cut -f1)"
fi

# Conversion en HTML (standalone)
echo ""
echo "🌐 Conversion en HTML..."
pandoc "$INPUT_FILE" \
    -o "$OUTPUT_DIR/${BASENAME}.html" \
    --standalone \
    --toc \
    --toc-depth=2 \
    --number-sections \
    --css=https://latex.now.sh/style.css \
    --mathjax \
    --metadata title="Théorie de Maîtrise du Temps vs ΛCDM" \
    --metadata author="Pierre-Olivier Després Asselin"

if [ -f "$OUTPUT_DIR/${BASENAME}.html" ]; then
    echo "✅ HTML créé: $OUTPUT_DIR/${BASENAME}.html"
    echo "   Taille: $(du -h "$OUTPUT_DIR/${BASENAME}.html" | cut -f1)"
fi

# Résumé
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ CONVERSION TERMINÉE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📂 Fichiers créés dans: $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR/" | grep -E "\.(pdf|docx|html)$" || echo "Aucun fichier généré"
echo ""
echo "📌 NOTES:"
echo "   - PDF: Prêt pour impression et distribution"
echo "   - DOCX: Éditable dans Microsoft Word / LibreOffice"
echo "   - HTML: Ouvrir dans navigateur web"
echo ""
echo "🚀 Le guide pédagogique TMT est prêt!"
