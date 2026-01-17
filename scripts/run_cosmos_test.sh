#!/bin/bash

echo "🔬 TEST WEAK LENSING TMT - COSMOS RÉEL"
echo "======================================"

# Vérifier si fichier .tbl existe
TBL_FILE="../data/input/cosmos/cosmos_weak_lensing_shapes.fits.tbl"

if [ ! -f "$TBL_FILE" ]; then
    echo ""
    echo "❌ Fichier .tbl non trouvé!"
    echo ""
    echo "📋 INSTRUCTIONS:"
    echo "1. Ouvrez l'Explorateur Windows"
    echo "2. Allez dans: \\\\wsl\$\\Ubuntu\\home\\user\\Maitrise-du-temps\\data\\input\\cosmos"
    echo "3. Copiez-y le fichier: C:\\Users\\PO\\Downloads\\cosmos_weak_lensing_shapes.fits.tbl"
    echo "4. Relancez ce script"
    exit 1
fi

echo ""
echo "✅ Fichier .tbl trouvé!"
ls -lh "$TBL_FILE"

# Convertir
echo ""
echo "📝 Étape 1: Conversion .tbl → FITS..."
python3 convert_cosmos_tbl_to_fits.py

if [ $? -ne 0 ]; then
    echo "❌ Conversion échouée"
    exit 1
fi

# Lancer test
echo ""
echo "🚀 Étape 2: Exécution test weak lensing..."
python3 test_weak_lensing_TMT_vs_LCDM_real_data.py

echo ""
echo "✅ TEST TERMINÉ!"
