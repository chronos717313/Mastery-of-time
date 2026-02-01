# 🌐 Guide de Démarrage du Wiki TMT

## Démarrage Local (MkDocs)

Pour visualiser le wiki TMT localement:

```bash
# Naviguer vers le répertoire wiki
cd docs/wiki

# Démarrer le serveur MkDocs (port 8000)
py -m mkdocs serve --dev-addr=127.0.0.1:8000

# Alternative: utiliser un autre port
py -m mkdocs serve --dev-addr=127.0.0.1:8080
```

## Accès

- **URL locale**: http://127.0.0.1:8000
- **Arrêter le serveur**: `Ctrl+C`

## Prérequis

Les packages suivants doivent être installés:

```bash
py -m pip install mkdocs mkdocs-material pymdown-extensions
```

## Contenu du Wiki

Le wiki TMT contient:

### Documentation Trilingue
- **Français** (FR) - Documentation complète
- **English** (EN) - English documentation
- **Español** (ES) - Documentación en español

### Sections Principales

1. **Accueil** - Vue d'ensemble TMT v2.4
   - 8/8 tests cosmologiques validés
   - 156/156 galaxies SPARC (100%)
   - Significativité p = 10⁻¹¹² (>15σ)

2. **Lexique** - Terminologie scientifique
   - Masse Després
   - Superposition Temporelle
   - Temporons
   - Rayon critique r_c(M, Σ)

3. **Ponts Conceptuels** - Liens avec physique établie
   - Relativité générale
   - Mécanique quantique
   - Cosmologie
   - Physique des particules
   - Thermodynamique
   - Mesures et observations

4. **Validation Empirique** - Résultats des tests
   - Courbes de rotation SPARC (100%)
   - Loi r_c(M) - corrélation r=0.768
   - Loi k(M) - R²=0.64
   - Weak Lensing isotropy
   - COSMOS2015 Mass-Environment
   - SNIa par environnement
   - ISW Effect
   - Résolution tension H₀

5. **Publications** - Ressources académiques
   - Package Zenodo v2.4 (DOI: 10.5281/zenodo.18451874)
   - Article scientifique
   - Scripts de reproduction

## Structure des Fichiers

```
docs/wiki/
├── mkdocs.yml          # Configuration MkDocs
├── index.md            # Page d'accueil
├── docs/               # Contenu du wiki
│   ├── index.md        # Accueil FR
│   ├── lexique.md      # Lexique FR
│   ├── ponts_conceptuels/
│   ├── validation/
│   ├── publications/
│   ├── en/             # English version
│   └── es/             # Versión española
└── javascripts/        # MathJax configuration
```

## Thème et Fonctionnalités

- **Thème**: Material for MkDocs
- **Navigation par onglets** (FR/EN/ES)
- **Mode sombre/clair** (toggle)
- **Recherche intégrée**
- **Équations LaTeX** (MathJax)
- **Coloration syntaxique** (code)
- **Navigation breadcrumb**

## Développement

Le serveur MkDocs en mode développement (`serve`) recharge automatiquement les modifications:

1. Modifier un fichier `.md` dans `docs/wiki/docs/`
2. Sauvegarder
3. Le navigateur se recharge automatiquement

## Notes Importantes

- Le wiki est en **développement actif**
- Quelques liens internes sont en cours de correction
- Les fichiers en anglais/espagnol suivent la structure française
- Les équations utilisent la notation LaTeX standard

## Support et Contact

**Projet**: Théorie de Maîtrise du Temps (TMT)  
**Version**: TMT v2.4  
**DOI**: [10.5281/zenodo.18451874](https://doi.org/10.5281/zenodo.18451874)  
**GitHub**: [chronos717313/Mastery-of-time](https://github.com/chronos717313/Mastery-of-time)

---

**Dernière mise à jour**: 1er février 2026
