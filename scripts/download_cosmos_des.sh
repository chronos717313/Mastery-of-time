#!/bin/bash

##############################################################################
# Script de téléchargement automatique des données COSMOS et DES Y3
# Théorie de Maîtrise du Temps (TMT) - Test Weak Lensing
#
# Taille totale: ~17 GB
# Durée estimée: 1-2 heures (selon connexion)
#
# Usage: ./scripts/download_cosmos_des.sh [cosmos|des|all]
##############################################################################

set -e  # Arrêt en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Répertoire racine du projet
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/data/input"

# URLs des fichiers
COSMOS_BASE_URL="https://irsa.ipac.caltech.edu/data/COSMOS/tables/morphology"
DES_BASE_URL="https://des.ncsa.illinois.edu/releases/y3a2"

# Fichiers à télécharger
declare -A COSMOS_FILES=(
    ["cosmos_zphot_shapes.fits"]="$COSMOS_BASE_URL/cosmos_zphot_shapes.fits"
    ["COSMOS2020_CLASSIC_R1_v2.1.fits.gz"]="$COSMOS_BASE_URL/COSMOS2020_CLASSIC_R1_v2.1.fits.gz"
)

declare -A DES_FILES=(
    ["y3_gold_2_2.fits"]="$DES_BASE_URL/gold-2-2/y3_gold_2_2.fits"
    ["y3a2_metacal_v03_shear.fits"]="$DES_BASE_URL/shear/y3a2_metacal_v03_shear.fits"
)

# Tailles approximatives (en MB)
declare -A FILE_SIZES=(
    ["cosmos_zphot_shapes.fits"]=1200
    ["COSMOS2020_CLASSIC_R1_v2.1.fits.gz"]=800
    ["y3_gold_2_2.fits"]=8000
    ["y3a2_metacal_v03_shear.fits"]=7000
)

##############################################################################
# Fonctions utilitaires
##############################################################################

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Vérifier l'espace disque disponible
check_disk_space() {
    local required_mb=$1
    local target_dir=$2

    # Espace disponible en MB
    local available_mb=$(df -BM "$target_dir" | awk 'NR==2 {print $4}' | sed 's/M//')

    if [ "$available_mb" -lt "$required_mb" ]; then
        print_error "Espace disque insuffisant!"
        echo "  Requis: ${required_mb} MB"
        echo "  Disponible: ${available_mb} MB"
        return 1
    else
        print_success "Espace disque OK: ${available_mb} MB disponibles"
        return 0
    fi
}

# Télécharger un fichier avec reprise et vérification
download_file() {
    local url=$1
    local output_path=$2
    local filename=$(basename "$output_path")
    local expected_size_mb=${FILE_SIZES[$filename]:-0}

    echo ""
    print_info "Téléchargement: $filename (~${expected_size_mb} MB)"
    echo "  URL: $url"
    echo "  Destination: $output_path"

    # Si le fichier existe déjà, vérifier sa taille
    if [ -f "$output_path" ]; then
        local current_size=$(stat -f%z "$output_path" 2>/dev/null || stat -c%s "$output_path" 2>/dev/null)
        local current_size_mb=$((current_size / 1024 / 1024))

        if [ $current_size_mb -gt $((expected_size_mb - 50)) ]; then
            print_success "Fichier déjà téléchargé et complet (${current_size_mb} MB)"
            return 0
        else
            print_warning "Fichier incomplet (${current_size_mb} MB), reprise du téléchargement..."
        fi
    fi

    # Téléchargement avec reprise (-c) et barre de progression
    if wget -c --show-progress --progress=bar:force:noscroll -O "$output_path" "$url" 2>&1; then
        print_success "Téléchargement réussi: $filename"

        # Vérifier la taille finale
        local final_size=$(stat -f%z "$output_path" 2>/dev/null || stat -c%s "$output_path" 2>/dev/null)
        local final_size_mb=$((final_size / 1024 / 1024))
        echo "  Taille finale: ${final_size_mb} MB"

        return 0
    else
        print_error "Échec du téléchargement: $filename"
        return 1
    fi
}

# Décompresser les fichiers .gz
decompress_gz() {
    local gz_file=$1

    if [ -f "$gz_file" ]; then
        print_info "Décompression: $(basename "$gz_file")"
        gunzip -f "$gz_file"
        print_success "Décompression terminée"
    fi
}

##############################################################################
# Téléchargement COSMOS
##############################################################################

download_cosmos() {
    print_header "📡 TÉLÉCHARGEMENT DONNÉES COSMOS (~2 GB)"

    # Créer le répertoire
    local cosmos_dir="$DATA_DIR/cosmos"
    mkdir -p "$cosmos_dir"

    # Vérifier l'espace disque (2.5 GB pour être sûr)
    check_disk_space 2500 "$cosmos_dir" || return 1

    local total_files=${#COSMOS_FILES[@]}
    local current=0

    # Télécharger chaque fichier
    for filename in "${!COSMOS_FILES[@]}"; do
        current=$((current + 1))
        echo ""
        echo -e "${YELLOW}[$current/$total_files]${NC}"

        download_file "${COSMOS_FILES[$filename]}" "$cosmos_dir/$filename" || {
            print_error "Échec du téléchargement COSMOS"
            return 1
        }
    done

    # Décompresser les fichiers .gz
    for file in "$cosmos_dir"/*.gz; do
        [ -f "$file" ] && decompress_gz "$file"
    done

    echo ""
    print_success "✅ COSMOS: Téléchargement terminé!"
    ls -lh "$cosmos_dir"
}

##############################################################################
# Téléchargement DES Y3
##############################################################################

download_des() {
    print_header "📡 TÉLÉCHARGEMENT DONNÉES DES Y3 (~15 GB)"

    # Créer le répertoire
    local des_dir="$DATA_DIR/des"
    mkdir -p "$des_dir"

    # Vérifier l'espace disque (16 GB pour être sûr)
    check_disk_space 16000 "$des_dir" || return 1

    print_warning "ATTENTION: Téléchargement volumineux (~15 GB)"
    print_warning "Durée estimée: 30-90 minutes selon votre connexion"
    echo ""

    local total_files=${#DES_FILES[@]}
    local current=0

    # Télécharger chaque fichier
    for filename in "${!DES_FILES[@]}"; do
        current=$((current + 1))
        echo ""
        echo -e "${YELLOW}[$current/$total_files]${NC}"

        download_file "${DES_FILES[$filename]}" "$des_dir/$filename" || {
            print_error "Échec du téléchargement DES"
            return 1
        }
    done

    echo ""
    print_success "✅ DES Y3: Téléchargement terminé!"
    ls -lh "$des_dir"
}

##############################################################################
# Vérification des données
##############################################################################

verify_data() {
    print_header "🔍 VÉRIFICATION DES DONNÉES"

    # Vérifier si Python et astropy sont disponibles
    if ! command -v python3 &> /dev/null; then
        print_warning "Python3 non trouvé, vérification basique seulement"
        return 0
    fi

    print_info "Vérification avec astropy..."

    # Créer script de vérification temporaire
    local verify_script="/tmp/verify_cosmos_des.py"
    cat > "$verify_script" << 'VERIFY_EOF'
#!/usr/bin/env python3
"""Script de vérification des données COSMOS/DES téléchargées."""

import os
import sys

try:
    from astropy.io import fits
    print("✅ astropy installé")
except ImportError:
    print("⚠️  astropy non installé - installation recommandée: pip3 install astropy")
    sys.exit(0)

def verify_fits(filepath, expected_cols=None):
    """Vérifie un fichier FITS."""
    try:
        with fits.open(filepath) as hdul:
            data = hdul[1].data
            cols = data.columns.names
            n_rows = len(data)

            print(f"  ✅ {os.path.basename(filepath)}")
            print(f"     Lignes: {n_rows:,}")
            print(f"     Colonnes: {len(cols)}")

            if expected_cols:
                missing = [c for c in expected_cols if c not in cols]
                if missing:
                    print(f"     ⚠️  Colonnes manquantes: {missing}")
                else:
                    print(f"     ✅ Toutes les colonnes requises présentes")

            return True
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

# Vérifier COSMOS
print("\n📊 COSMOS:")
cosmos_dir = "data/input/cosmos"
if os.path.exists(f"{cosmos_dir}/cosmos_zphot_shapes.fits"):
    verify_fits(f"{cosmos_dir}/cosmos_zphot_shapes.fits",
                ['RA', 'DEC', 'z_phot', 'e1', 'e2'])

if os.path.exists(f"{cosmos_dir}/COSMOS2020_CLASSIC_R1_v2.1.fits"):
    verify_fits(f"{cosmos_dir}/COSMOS2020_CLASSIC_R1_v2.1.fits",
                ['ALPHA_J2000', 'DELTA_J2000', 'lp_zPDF'])

# Vérifier DES
print("\n📊 DES Y3:")
des_dir = "data/input/des"
if os.path.exists(f"{des_dir}/y3_gold_2_2.fits"):
    verify_fits(f"{des_dir}/y3_gold_2_2.fits",
                ['RA', 'DEC', 'DNF_ZMEAN_SOF'])

if os.path.exists(f"{des_dir}/y3a2_metacal_v03_shear.fits"):
    verify_fits(f"{des_dir}/y3a2_metacal_v03_shear.fits",
                ['ra', 'dec', 'e_1', 'e_2'])

print("\n✅ Vérification terminée!")
VERIFY_EOF

    chmod +x "$verify_script"
    python3 "$verify_script"
    rm -f "$verify_script"
}

##############################################################################
# Menu principal
##############################################################################

show_usage() {
    echo "Usage: $0 [cosmos|des|all|verify]"
    echo ""
    echo "Options:"
    echo "  cosmos   - Télécharger uniquement COSMOS (~2 GB)"
    echo "  des      - Télécharger uniquement DES Y3 (~15 GB)"
    echo "  all      - Télécharger tout (défaut, ~17 GB)"
    echo "  verify   - Vérifier les données déjà téléchargées"
    echo ""
    echo "Exemples:"
    echo "  $0              # Tout télécharger"
    echo "  $0 cosmos       # COSMOS seulement"
    echo "  $0 verify       # Vérifier les données"
}

main() {
    local mode=${1:-all}

    print_header "🌌 TÉLÉCHARGEMENT DONNÉES WEAK LENSING - TMT"
    echo ""
    echo "  Projet: Théorie de Maîtrise du Temps (TMT)"
    echo "  Test: θ_halo ↔ θ_voisin (Alignement halos)"
    echo "  Destination: $DATA_DIR"
    echo ""

    case "$mode" in
        cosmos)
            download_cosmos
            verify_data
            ;;
        des)
            download_des
            verify_data
            ;;
        all)
            download_cosmos
            echo ""
            download_des
            echo ""
            verify_data
            ;;
        verify)
            verify_data
            ;;
        -h|--help|help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Option invalide: $mode"
            echo ""
            show_usage
            exit 1
            ;;
    esac

    echo ""
    print_header "✅ TÉLÉCHARGEMENT TERMINÉ"
    echo ""
    echo "📁 Structure des données:"
    tree -L 2 "$DATA_DIR" 2>/dev/null || ls -R "$DATA_DIR"
    echo ""
    echo "📊 Prochaine étape:"
    echo "   python3 scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py"
    echo ""
}

# Exécuter le script
main "$@"
