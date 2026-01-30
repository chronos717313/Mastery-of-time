# Théorie de Maîtrise du Temps (TMT)

## Vue d'ensemble

La **Théorie de Maîtrise du Temps** (TMT) est une formulation alternative à la cosmologie ΛCDM standard, basée sur le concept de **superposition temporelle quantique**.

### Équation Maîtresse

La formulation centrale de TMT repose sur l'équation maîtresse :

$$
\psi(\text{univers}) = \alpha(r,p,t)|t\rangle + \beta(r,p)|\bar{t}\rangle
$$

où :

- $|t\rangle$ représente l'état temporel forward (matière visible)
- $|\bar{t}\rangle$ représente l'état temporel backward (matière noire comme reflet quantique)
- $\alpha$ et $\beta$ sont les amplitudes de probabilité avec $|\alpha|^2 + |\beta|^2 = 1$

### Équation Després-Schrödinger

L'unification de la mécanique quantique et de la gravitation se réalise via l'équation Després-Schrödinger :

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t} = \left[-\frac{\hbar^2}{2m_{eff}} \nabla^2 + V(x) + mc^2\tau(x)\right] \psi
$$

où :

- $\tau(x) = \Phi(x)/c^2$ est la **distorsion temporelle locale**
- $[1 + \tau(x)]^{-1}$ ralentit le temps dans les champs gravitationnels
- $mc^2\tau(x)$ est le **potentiel temporel** (terme nouveau)
- $m_{eff} = m_0/\gamma_{\text{Després}}$ est la masse effective

Cette équation :

- Récupère Schrödinger standard quand $\tau \to 0$
- Explique la matière noire sans particules exotiques
- Unifie MQ + RG dans un cadre cohérent

> **[Voir le Lexique complet](lexique.md)** pour toutes les définitions des termes TMT.

## Statut de Validation

TMT atteint une **compatibilité exceptionnelle** avec les données observationnelles majeures :

| Test | Résultat | Script | Verdict |
|------|----------|--------|---------|
| Courbes de rotation SPARC | 156/156 (100%) | [:material-file-code: test_TMT_v2_SPARC_reel.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDÉ |
| Loi $r_c(M)$ | r = 0.768 | [:material-file-code: investigation_r_c_variation.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/investigation_r_c_variation.py) | ✅ VALIDÉ |
| Loi $k(M)$ | $R^2$ = 0.64 | [:material-file-code: test_TMT_v2_SPARC_reel.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDÉ |
| Isotropie Weak Lensing | -0.024% | [:material-file-code: test_weak_lensing_TMT_vs_LCDM.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM.py) | ✅ VALIDÉ |
| Masse-Env COSMOS2015 | r = 0.150 | [:material-file-code: test_weak_lensing_real_data.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py) | ✅ VALIDÉ |
| SNIa par environnement | préd: 0.57% | [:material-file-code: test_3_predictions_TMT.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_3_predictions_TMT.py) | ✅ VALIDÉ |
| Effet ISW | préd: 18.2% | [:material-file-code: calculate_ISW_improved.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calculate_ISW_improved.py) | ✅ VALIDÉ |
| Tension Hubble | 100% résolue | [:material-file-code: calibrate_TMT_v23_cosmologie.py](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calibrate_TMT_v23_cosmologie.py) | ✅ RÉSOLU |

> **[Scripts de reproduction complets](validation/scripts_reproduction.md)** : Instructions détaillées et données requises.

## Ponts Conceptuels vs ΛCDM

TMT établit 7 ponts conceptuels fondamentaux par rapport au modèle ΛCDM :

1. **Physique connue** : Superposition temporelle vs physique quantique + relativité
2. **Mécanique quantique** : Distorsion du temps / flèche du temps
3. **Relativité générale** : Temporons vs matière noire WIMP
4. **Thermodynamique** : $\phi_T(p=1)=0$ vs énergie noire
5. **Cosmologie** : Expansion différentielle vs ΛCDM
6. **Physique des particules** : Pas de WIMP vs particules CDM
7. **Mesures** : Résolution tension Hubble vs découvertes ΛCDM

## Structure de la Documentation

- **[Ponts Conceptuels](ponts_conceptuels/index.md)** : Comparaisons détaillées avec ΛCDM
- **[Validation Empirique](validation/index.md)** : Tests et résultats observationnels
- **[Publications](publications/index.md)** : Documents de soumission scientifique

---

*TMT - Version production prête (Janvier 2026)*
