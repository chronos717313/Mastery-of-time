# Package Zenodo : zenodo_package_DESPRES_UNIFIED_THEORY

## Description du Package

Le package Zenodo contient tous les matériaux nécessaires pour reproduire et valider TMT v2.4.

## Contenu Inclus

### Scripts Python
- `test_TMT_v2_SPARC_reel.py` : Test SPARC 175 galaxies réelles
- `test_TMT_v2_probabilites_quantiques.py` : Analyse probabiliste quantique
- `investigation_r_c_variation.py` : Découverte r_c(M)
- `test_3_predictions_TMT.py` : Validation des 3 prédictions

### Données
- `data/SPARC/` : Catalogue complet SPARC (175 galaxies)
- `data/results/` : Résultats de tous les tests
- `data/Pantheon+/` : Données supernovae pour validation cosmologique

### Documentation
- Articles scientifiques en FR/EN
- Guides d'utilisation
- Résumés exécutifs

## Métadonnées Zenodo

| Champ | Valeur |
|-------|--------|
| Titre | Théorie de Maîtrise du Temps v2.4 : Alternative à ΛCDM |
| Auteur | C. Després |
| Description | Validation complète 100% SPARC, résolution tension Hubble |
| Mots-clés | cosmologie, matière noire, expansion univers, théorie alternative |
| Licence | CC-BY-4.0 |

## Statut
- ✅ **Prêt pour upload** : Tous fichiers préparés
- ✅ **DOI permanent** : Version immutable archivée
- ✅ **Citation** : Référence bibliographique stable

## Utilisation
```bash
# Télécharger le package
wget https://zenodo.org/record/XXXXXXX/files/zenodo_package_DESPRES_UNIFIED_THEORY.zip

# Extraire et exécuter tests
unzip zenodo_package_DESPRES_UNIFIED_THEORY.zip
cd zenodo_package_DESPRES_UNIFIED_THEORY
python test_TMT_v2_SPARC_reel.py
```