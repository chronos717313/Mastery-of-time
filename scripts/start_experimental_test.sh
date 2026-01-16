#!/bin/bash
###############################################################################
# SCRIPT DE DÉMARRAGE - TEST EXPÉRIMENTAL FINAL TMT
###############################################################################
#
# Ce script télécharge les données COSMOS et prépare l'environnement pour
# le test décisif de weak lensing.
#
# Auteur: Pierre-Olivier Després Asselin
# Date: Décembre 2025
# Usage: bash start_experimental_test.sh
#
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "═══════════════════════════════════════════════════════════════"
echo "  TEST EXPÉRIMENTAL FINAL - THÉORIE DE MAÎTRISE DU TEMPS"
echo "═══════════════════════════════════════════════════════════════"
echo -e "${NC}"

# Vérifier répertoire
BASEDIR="/home/user/Maitrise-du-temps"
cd "$BASEDIR" || exit 1

echo -e "${YELLOW}📁 Répertoire de travail: $BASEDIR${NC}"
echo ""

###############################################################################
# PHASE 1: CRÉATION STRUCTURE RÉPERTOIRES
###############################################################################

echo -e "${BLUE}📂 Phase 1: Création structure répertoires${NC}"

mkdir -p data/input/cosmos
mkdir -p data/input/des
mkdir -p data/results/experimental
mkdir -p logs

echo -e "${GREEN}✅ Répertoires créés${NC}"
echo ""

###############################################################################
# PHASE 2: VÉRIFICATION DÉPENDANCES
###############################################################################

echo -e "${BLUE}🔧 Phase 2: Vérification dépendances Python${NC}"

# Liste packages requis
REQUIRED_PACKAGES="numpy scipy matplotlib astropy pandas"

# Vérifier chaque package
MISSING_PACKAGES=""
for pkg in $REQUIRED_PACKAGES; do
    if python3 -c "import $pkg" 2>/dev/null; then
        echo -e "${GREEN}  ✅ $pkg installé${NC}"
    else
        echo -e "${RED}  ❌ $pkg MANQUANT${NC}"
        MISSING_PACKAGES="$MISSING_PACKAGES $pkg"
    fi
done

# Installer packages manquants
if [ -n "$MISSING_PACKAGES" ]; then
    echo -e "${YELLOW}📦 Installation packages manquants:$MISSING_PACKAGES${NC}"
    pip3 install $MISSING_PACKAGES --quiet
    echo -e "${GREEN}✅ Installation complétée${NC}"
else
    echo -e "${GREEN}✅ Toutes dépendances présentes${NC}"
fi

# Packages optionnels mais recommandés
echo ""
echo -e "${YELLOW}📦 Installation packages recommandés...${NC}"
pip3 install treecorr healpy --quiet 2>/dev/null || echo -e "${YELLOW}⚠️  treecorr/healpy non installés (optionnels)${NC}"

echo ""

###############################################################################
# PHASE 3: TÉLÉCHARGEMENT DONNÉES COSMOS
###############################################################################

echo -e "${BLUE}📥 Phase 3: Téléchargement données COSMOS${NC}"

COSMOS_FILE="data/input/cosmos/cosmos_zphot_shapes.fits"

if [ -f "$COSMOS_FILE" ]; then
    echo -e "${GREEN}✅ Données COSMOS déjà téléchargées${NC}"
    FILESIZE=$(du -h "$COSMOS_FILE" | cut -f1)
    echo -e "${GREEN}   Taille: $FILESIZE${NC}"
else
    echo -e "${YELLOW}📥 Téléchargement COSMOS shapes catalog...${NC}"
    echo -e "${YELLOW}   (Cela peut prendre 1-2 heures selon votre connexion)${NC}"
    echo ""

    # URL COSMOS
    COSMOS_URL="https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology/cosmos_zphot_shapes.fits"

    # Télécharger avec wget (avec barre progression)
    if command -v wget &> /dev/null; then
        wget -O "$COSMOS_FILE" "$COSMOS_URL" 2>&1 | \
            grep --line-buffered "%" | \
            sed -u -e "s/^/   /"
    elif command -v curl &> /dev/null; then
        curl -# -o "$COSMOS_FILE" "$COSMOS_URL"
    else
        echo -e "${RED}❌ ERREUR: wget ou curl requis pour téléchargement${NC}"
        echo -e "${YELLOW}   Téléchargez manuellement:${NC}"
        echo -e "${YELLOW}   $COSMOS_URL${NC}"
        echo -e "${YELLOW}   Et placez dans: $COSMOS_FILE${NC}"
        exit 1
    fi

    if [ -f "$COSMOS_FILE" ]; then
        FILESIZE=$(du -h "$COSMOS_FILE" | cut -f1)
        echo -e "${GREEN}✅ Téléchargement réussi! Taille: $FILESIZE${NC}"
    else
        echo -e "${RED}❌ ERREUR: Téléchargement échoué${NC}"
        exit 1
    fi
fi

echo ""

###############################################################################
# PHASE 4: VÉRIFICATION DONNÉES
###############################################################################

echo -e "${BLUE}🔍 Phase 4: Vérification intégrité données${NC}"

# Vérifier avec Python/astropy
python3 - <<EOF
from astropy.io import fits
import sys

try:
    print("   Ouverture fichier FITS...")
    hdul = fits.open('$COSMOS_FILE')
    data = hdul[1].data

    print(f"   ✅ Fichier valide: {len(data)} galaxies")
    print(f"   📊 Colonnes disponibles: {', '.join(data.columns.names[:10])}...")

    # Vérifier colonnes requises
    required_cols = ['RA', 'DEC', 'Z_PHOT', 'e1', 'e2']
    missing = [col for col in required_cols if col not in data.columns.names]

    if missing:
        print(f"   ⚠️  Colonnes manquantes: {missing}")
        sys.exit(1)
    else:
        print(f"   ✅ Toutes colonnes requises présentes")

    hdul.close()

except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Données vérifiées et prêtes${NC}"
else
    echo -e "${RED}❌ ERREUR: Fichier corrompu ou incomplet${NC}"
    echo -e "${YELLOW}   Supprimez et relancez: rm $COSMOS_FILE${NC}"
    exit 1
fi

echo ""

###############################################################################
# PHASE 5: PRÉPARATION SCRIPT ANALYSE
###############################################################################

echo -e "${BLUE}🛠️  Phase 5: Préparation script analyse${NC}"

# Créer script Python adapté
cat > scripts/analyze_cosmos_real.py <<'PYTHON_SCRIPT'
#!/usr/bin/env python3
"""
Analyse COSMOS Réelle - Test Expérimental Final TMT
====================================================

Script adapté pour charger et analyser les vraies données COSMOS.
"""

import numpy as np
from astropy.io import fits
import sys

print("="*80)
print("ANALYSE COSMOS RÉELLE - TEST EXPÉRIMENTAL TMT")
print("="*80)
print()

# Charger données
print("📥 Chargement données COSMOS...")
try:
    hdul = fits.open('../data/input/cosmos/cosmos_zphot_shapes.fits')
    data = hdul[1].data
    print(f"✅ {len(data)} galaxies chargées")
    print()
except Exception as e:
    print(f"❌ ERREUR chargement: {e}")
    sys.exit(1)

# Extraire colonnes
print("📊 Extraction colonnes...")
RA = data['RA']
DEC = data['DEC']
z_phot = data['Z_PHOT']

# Ellipticités (noms peuvent varier)
if 'e1' in data.columns.names:
    e1 = data['e1']
    e2 = data['e2']
elif 'E1' in data.columns.names:
    e1 = data['E1']
    e2 = data['E2']
else:
    print("❌ ERREUR: Colonnes ellipticité non trouvées")
    print(f"   Colonnes disponibles: {data.columns.names}")
    sys.exit(1)

print("✅ Colonnes extraites")
print()

# Sélection échantillon
print("🔍 Sélection échantillon qualité...")

mask_quality = (
    (z_phot > 0.2) & (z_phot < 0.8) &
    (np.isfinite(e1)) & (np.isfinite(e2)) &
    (np.abs(e1) < 1) & (np.abs(e2) < 1)  # Ellipticités physiques
)

N_selected = np.sum(mask_quality)
print(f"✅ {N_selected} galaxies sélectionnées ({100*N_selected/len(data):.1f}%)")
print()

# Statistiques
print("📈 Statistiques échantillon:")
print(f"   Redshift: {np.median(z_phot[mask_quality]):.2f} (médian)")
print(f"   RA range: {RA[mask_quality].min():.2f} - {RA[mask_quality].max():.2f} deg")
print(f"   DEC range: {DEC[mask_quality].min():.2f} - {DEC[mask_quality].max():.2f} deg")
print(f"   Ellipticité: {np.std(e1[mask_quality]):.3f} (σ)")
print()

# Message suivant
print("="*80)
print("✅ DONNÉES CHARGÉES ET PRÊTES POUR ANALYSE")
print("="*80)
print()
print("🎯 Prochaine étape:")
print("   Modifier test_weak_lensing_TMT_vs_LCDM.py pour utiliser ces données")
print("   Voir: TEST_EXPERIMENTAL_FINAL.md (Phase 3)")
print()

hdul.close()
PYTHON_SCRIPT

chmod +x scripts/analyze_cosmos_real.py

echo -e "${GREEN}✅ Script préparé: scripts/analyze_cosmos_real.py${NC}"
echo ""

###############################################################################
# PHASE 6: TEST RAPIDE
###############################################################################

echo -e "${BLUE}🧪 Phase 6: Test rapide chargement données${NC}"

python3 scripts/analyze_cosmos_real.py 2>&1 | tee logs/cosmos_load_test.log

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Test réussi!${NC}"
else
    echo ""
    echo -e "${RED}❌ Test échoué - voir logs/cosmos_load_test.log${NC}"
    exit 1
fi

echo ""

###############################################################################
# RÉSUMÉ FINAL
###############################################################################

echo -e "${GREEN}"
echo "═══════════════════════════════════════════════════════════════"
echo "  ✅ ENVIRONNEMENT PRÊT POUR TEST EXPÉRIMENTAL FINAL"
echo "═══════════════════════════════════════════════════════════════"
echo -e "${NC}"

echo -e "${YELLOW}📋 PROCHAINES ÉTAPES:${NC}"
echo ""
echo -e "${BLUE}1. Vérifier résultats test:${NC}"
echo "   cat logs/cosmos_load_test.log"
echo ""
echo -e "${BLUE}2. Adapter script analyse principale:${NC}"
echo "   Éditer: scripts/test_weak_lensing_TMT_vs_LCDM.py"
echo "   Voir guide: TEST_EXPERIMENTAL_FINAL.md (Phase 3)"
echo ""
echo -e "${BLUE}3. Exécuter analyse complète:${NC}"
echo "   cd scripts"
echo "   python3 test_weak_lensing_TMT_vs_LCDM.py --real"
echo ""
echo -e "${BLUE}4. Timeline:${NC}"
echo "   • Adaptation script: 1-2 jours"
echo "   • Analyse corrélation: 2-3 semaines"
echo "   • Tests systématiques: 2-3 semaines"
echo "   • Résultat DÉCISIF: 4-6 mois"
echo ""
echo -e "${YELLOW}🎯 CRITÈRE DÉCISION:${NC}"
echo -e "${GREEN}   • Si r > 0.50 → TMT VALIDÉE ✅${NC}"
echo -e "${RED}   • Si r < 0.20 → TMT RÉFUTÉE ❌${NC}"
echo ""
echo -e "${BLUE}📚 Documentation complète:${NC}"
echo "   • TEST_EXPERIMENTAL_FINAL.md (guide détaillé)"
echo "   • COSMOS_DES_TEST_GUIDE.md (méthodologie)"
echo "   • RESULTATS_TEST_COSMOS_DES.md (résultats simulation)"
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Le test qui changera tout est maintenant entre vos mains.${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
