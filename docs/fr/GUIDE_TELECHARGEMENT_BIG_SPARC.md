# Guide de Téléchargement des Données BIG-SPARC

## Vue d'ensemble

Pour calibrer k(M) avec des données réelles, vous devez télécharger les courbes de rotation depuis les archives officielles.

| Survey | Galaxies | Archive | Statut |
|--------|----------|---------|--------|
| SPARC | 175 | astroweb.cwru.edu | ✅ Disponible |
| WALLABY DR2 | ~1,800 | CASDA | ✅ Disponible |
| APERTIF DR1 | ~1,740 | ASTRON | ✅ Disponible |
| BIG-SPARC | ~4,000 | À venir | ⏳ 2025-2026 |

---

## 1. WALLABY DR2 (Recommandé - Plus facile)

### Option A : Interface Web CASDA

1. **Aller sur** : https://data.csiro.au/collections/casda/

2. **Rechercher** : "WALLABY Pilot DR2"

3. **Filtrer** :
   - Collection: WALLABY
   - Data Product: Source catalog + Kinematic models

4. **Télécharger** :
   - `WALLABY_Pilot_DR2_source_catalog.fits`
   - `WALLABY_Pilot_DR2_kinematic_models.tar.gz`

5. **Placer dans** : `data/WALLABY_DR2/`

### Option B : CADC TAP (Programmable)

```python
from astroquery.cadc import Cadc

cadc = Cadc()
# Nécessite compte CADC pour accès complet
results = cadc.query_region(
    "WALLABY",
    collection="WALLABY"
)
```

### Option C : Site WALLABY Direct

1. **Aller sur** : https://wallaby-survey.org/data/data-pilot-survey-dr2/

2. **Télécharger** les fichiers kinematic models

---

## 2. APERTIF DR1

### Option A : Archive ASTRON

1. **Aller sur** : https://www.astron.nl/telescopes/wsrt-apertif/apertif-dr1-documentation/

2. **Suivre** les liens vers les données publiques

3. **Télécharger** :
   - Catalog FITS
   - HI cubes (si traitement local souhaité)

### Option B : VizieR (Partiel - 247 sources)

Déjà téléchargé automatiquement dans `data/APERTIF_DR1/APERTIF_DR1_real_catalog.fits`

### Note importante

APERTIF DR1 fournit principalement des **cubes HI bruts**, pas des courbes de rotation pré-calculées. Pour obtenir les courbes de rotation :

1. Télécharger les cubes HI
2. Traiter avec **3DBAROLO** ou **FAT**
3. Extraire v(r) pour chaque galaxie

---

## 3. Structure des Fichiers Attendus

Après téléchargement, organiser comme suit :

```
data/
├── SPARC/
│   ├── SPARC_Lelli2016c.mrt        # Propriétés galaxies
│   └── MassModels_Lelli2016c.mrt   # Courbes de rotation
│
├── WALLABY_DR2/
│   ├── WALLABY_DR2_catalog.fits    # Catalog principal
│   ├── WALLABY_DR2_kinematic.fits  # Modèles cinématiques
│   └── rotation_curves/            # Courbes individuelles
│
├── APERTIF_DR1/
│   ├── APERTIF_DR1_catalog.fits
│   └── rotation_curves/
│
└── BIG_SPARC/                      # Futur (2025-2026)
    └── BIG_SPARC_unified.fits
```

---

## 4. Format des Courbes de Rotation

Le pipeline TMT attend le format SPARC :

```
# Galaxy  D(Mpc)  R(kpc)  Vobs  e_Vobs  Vgas  Vdisk  Vbul
NGC3198   13.8    0.50    45.2   5.1    12.3   35.2   8.1
NGC3198   13.8    1.00    78.4   4.2    18.7   52.1   12.3
...
```

### Colonnes requises :
- **Galaxy** : Nom de la galaxie
- **D** : Distance en Mpc
- **R** : Rayon en kpc
- **Vobs** : Vitesse observée (km/s)
- **e_Vobs** : Erreur sur Vobs (km/s)
- **Vgas** : Contribution du gaz (km/s)
- **Vdisk** : Contribution du disque (km/s)
- **Vbul** : Contribution du bulbe (km/s)

---

## 5. Exécuter la Calibration

Une fois les données en place :

```bash
# Calibration unifiée
python scripts/calibration/big_sparc_module.py

# Ou calibration par survey
python scripts/calibration/calibrate_k_WALLABY_DR2.py
python scripts/calibration/calibrate_k_combined_WALLABY_APERTIF.py
```

---

## 6. Ressources

### Documentation officielle

| Survey | Documentation |
|--------|---------------|
| WALLABY | https://wallaby-survey.org/science/ |
| APERTIF | https://www.astron.nl/telescopes/wsrt-apertif/ |
| SPARC | http://astroweb.cwru.edu/SPARC/ |
| BIG-SPARC | https://arxiv.org/abs/2411.13329 |

### Papers de référence

- **SPARC** : Lelli, McGaugh & Schombert (2016), AJ, 152, 157
- **WALLABY** : Westmeier et al. (2022), PASA, 39, e058
- **APERTIF** : Adams et al. (2022), A&A, 667, A38
- **BIG-SPARC** : Haubner, Lelli et al. (2024), arXiv:2411.13329

---

## 7. Contact Support

Si problèmes d'accès aux données :

- **CASDA** : atnf-datasupport@csiro.au
- **ASTRON** : helpdesk@astron.nl
- **SPARC** : federico.lelli@eso.org

---

*Document généré pour TMT v2.4 - Janvier 2026*
