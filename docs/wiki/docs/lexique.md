# Lexique TMT v2.4

Ce lexique définit tous les termes spécifiques à la **Théorie de Maîtrise du Temps** (TMT).

---

## Termes Fondamentaux

### $\tau(x)$ - Distorsion Temporelle

**Définition** : La distorsion temporelle locale, définie comme le rapport du potentiel gravitationnel sur le carré de la vitesse de la lumière.

$$
\tau(x) = \frac{\Phi(x)}{c^2} = \frac{GM}{rc^2} \quad \text{[sans dimension]}
$$

**Propriétés** :

| Propriété | Valeur | Signification |
|-----------|--------|---------------|
| $\tau \propto 1/r$ | Décroissance radiale | Cohérent avec métrique de Schwarzschild |
| $\tau > 0$ | Toujours positif | Temps toujours dilaté près des masses |
| $\tau \to 0$ | Quand $r \to \infty$ | Espace-temps plat loin des masses |

**Connexion avec la Relativité Générale** :

$$
g_{00} = -\left(1 + \frac{2\Phi}{c^2}\right) = -(1 + 2\tau)
$$

**Exemples numériques** :

| Lieu | $\tau$ | Effet observable |
|------|--------|------------------|
| Surface Terre | $7 \times 10^{-10}$ | Correction GPS nécessaire |
| Orbite terrestre | $1.5 \times 10^{-8}$ | Mesuré par satellites |
| Surface Soleil | $2 \times 10^{-6}$ | Redshift spectral observé |
| Étoile à neutrons | $\sim 0.2$ | Effets relativistes extrêmes |
| Horizon trou noir | $0.5$ | Limite théorique |

---

### TDI - Indice de Distorsion Temporelle

**Définition** : L'Indice de Distorsion Temporelle quantifie l'écart par rapport à l'espace-temps plat (Minkowski).

$$
\text{TDI}(r) = \gamma_{\text{Després}}(r) - 1
$$

**Interprétation** :

- TDI = 0 : Aucune distorsion (espace-temps plat)
- TDI > 0 : Distorsion temporelle significative

**Exemples** :

| Objet | TDI |
|-------|-----|
| Mercure | $3.83 \times 10^{-8}$ |
| Terre | $1.48 \times 10^{-8}$ |
| Jupiter | $2.85 \times 10^{-9}$ |
| Centre galactique | $\sim 10^{-6}$ |
| Vide cosmique | $\sim 10^{-8}$ |

---

### $\gamma_{\text{Després}}$ - Facteur de Lorentz Généralisé

**Définition** : Le facteur de Lorentz généralisé qui combine les effets cinématiques ET gravitationnels.

$$
\gamma_{\text{Després}}(r,v) = \frac{1}{\sqrt{1 - \frac{v^2}{c^2} - \frac{2\Phi}{c^2}}} = \frac{1}{\sqrt{1 - \frac{v^2}{c^2} - 2\tau}}
$$

**Composantes** :

| Terme | Origine | Effet |
|-------|---------|-------|
| $v^2/c^2$ | Relativité restreinte | Dilatation cinématique |
| $2\Phi/c^2 = 2\tau$ | Relativité générale | Dilatation gravitationnelle |

**Propriétés** :

- Valeur minimale : $\gamma_{\text{Després}} = 1$ (espace vide, loin de toute masse)
- Augmente près des objets massifs
- Intègre la 3ème loi de Kepler ($v \propto \sqrt{M/r}$)

**Validation** : Relation $2\Phi/c^2 = 2 \times v^2/c^2$ vérifiée à 0.001% de précision dans le système solaire.

---

### Équation Després-Schrödinger

**L'équation fondamentale** qui unifie mécanique quantique et gravitation :

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t} = \left[-\frac{\hbar^2}{2m_{eff}} \nabla^2 + V(x) + mc^2\tau(x)\right] \psi
$$

#### Décomposition des termes

| Terme | Expression | Origine | Signification |
|-------|------------|---------|---------------|
| **Temps modifié** | $[1+\tau]^{-1} \partial\psi/\partial t$ | Relativité | Temps propre variable |
| **Cinétique modifié** | $-\hbar^2/(2m_{eff}) \nabla^2\psi$ | RG + MQ | Masse effective gravitationnelle |
| **Potentiel classique** | $V(x)\psi$ | MQ standard | Électromagnétique, nucléaire |
| **Potentiel temporel** | $mc^2\tau(x)\psi$ | **TMT nouveau!** | Énergie de distorsion temporelle |

#### Côté gauche : Évolution temporelle modifiée

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t}
$$

- $i\hbar$ : Constante de Planck (quantique)
- $[1 + \tau(x)]^{-1}$ : **NOUVEAU** - Le temps s'écoule plus lentement dans les champs gravitationnels
- $\partial\psi/\partial t$ : Dérivée temporelle standard

**Temps propre** : $dt_{\text{propre}} = [1 + \tau(x)] \cdot dt_{\text{cosmique}}$

#### Côté droit : Hamiltonien effectif

1. **Énergie cinétique** : $\hat{A}_{\text{cinétique}} = -\frac{\hbar^2}{2m_{eff}} \nabla^2\psi$ avec $m_{eff} = m_0/\gamma_{\text{Després}}$
2. **Potentiel classique** : $\hat{A}_{\text{potentiel}} = V(x)\psi$ (inchangé)
3. **Potentiel temporel** : $\hat{A}_{\text{temporel}} = mc^2\tau(x)\psi$ (nouveau terme TMT)

#### Cas limites (validation)

| Limite | Condition | Résultat |
|--------|-----------|----------|
| Espace plat | $\tau \to 0$ | Récupère équation de Schrödinger standard |
| Classique | $\hbar \to 0$ | Récupère équation de Hamilton-Jacobi |
| Champ faible | $\tau \ll 1$ | Reproduit redshift gravitationnel d'Einstein |

---

### $M_{\text{Després}}$ - Masse Després

**Définition** : La masse apparente équivalente résultant de l'accumulation de la distorsion temporelle.

$$
M_{\text{Després}} = k \times \int \left(\frac{\Phi}{c^2}\right)^2 dV = k \times \int \tau^2 \, dV
$$

**Nature** : Effet **géométrique**, PAS une particule exotique.

**Interprétation physique** :

$$
M_{\text{observée}} = M_{\text{baryonique}} + M_{\text{Després}}
$$

| Modèle | Interprétation de la "matière noire" |
|--------|--------------------------------------|
| ΛCDM | Particules exotiques (WIMPs, axions) |
| TMT | Effet géométrique de distorsion temporelle |

---

### $r_c(M)$ - Rayon Critique

**Définition** : Le rayon de transition où les amplitudes de superposition temporelle sont égales ($\alpha^2 = \beta^2 = 0.5$).

$$
r_c = 2.6 \times \left(\frac{M_{\text{bary}}}{10^{10} M_\odot}\right)^{0.56} \text{ kpc}
$$

**Signification** : C'est exactement le rayon où les courbes de rotation galactiques deviennent plates.

**Exemples par type de galaxie** :

| Type | $M_{\text{bary}}$ | $r_c$ |
|------|-------------------|-------|
| Naine | $10^8 M_\odot$ | 0.4 kpc |
| Moyenne | $10^{10} M_\odot$ | 2.6 kpc |
| Massive | $10^{11} M_\odot$ | 9.4 kpc |

**Validation** : Corrélation $r = 0.768$ sur 103 galaxies SPARC.

---

### $k(M)$ - Constante de Couplage

**Définition** : Le coefficient de couplage entre distorsion temporelle et effet gravitationnel apparent.

$$
k = 3.97 \times \left(\frac{M}{10^{10}}\right)^{-0.48}
$$

**Validation** : $R^2 = 0.64$ sur 168 galaxies SPARC.

**Interprétation** : Plus la galaxie est massive, plus le couplage est faible (exposant négatif).

---

### $\alpha / \beta$ - Amplitudes de Superposition Temporelle

**État quantique de l'univers** :

$$
|\Psi\rangle = \alpha|t\rangle + \beta|\bar{t}\rangle
$$

où :

- $|t\rangle$ : état temps **forward** (matière visible)
- $|\bar{t}\rangle$ : état temps **backward** (reflet temporel = "matière noire")

**Définitions des amplitudes** :

$$
|\alpha(r)|^2 = \frac{1}{1 + (r/r_c)^n} \quad \text{(temps forward)}
$$

$$
|\beta(r)|^2 = \frac{(r/r_c)^n}{1 + (r/r_c)^n} \quad \text{(temps backward)}
$$

**Normalisation quantique** : $|\alpha|^2 + |\beta|^2 = 1$

**Profil radial** :

| Région | $\alpha^2$ | $\beta^2$ | Interprétation |
|--------|------------|-----------|----------------|
| $r < r_c$ | > 0.5 | < 0.5 | Forward dominant |
| $r = r_c$ | 0.5 | 0.5 | **Transition critique** |
| $r > r_c$ | < 0.5 | > 0.5 | Backward dominant (halo) |

**Masse effective** :

$$
M_{\text{eff}}(r) = M_{\text{visible}}(r) \times \left[1 + \frac{\beta^2(r)}{\alpha^2(r)}\right]
$$

---

### Temporons

**Définition** : Excitations quantiques du champ de distorsion temporelle.

**Propriétés** :

| Propriété | Valeur |
|-----------|--------|
| Masse au repos | 0 |
| Spin | À déterminer |
| Interaction | Médient la "gravité temporelle" |

**Rôle** : Alternative aux particules WIMP pour expliquer les effets gravitationnels attribués à la matière noire.

---

### Liaison Asselin

**Définition** : Gradient de distorsion temporelle entre deux régions spatiales A et B.

$$
\text{Liaison\_Asselin}(A, B) = |\tau(A) - \tau(B)| = \frac{|\Phi_A - \Phi_B|}{c^2}
$$

**Propriétés** :

| Propriété | Description |
|-----------|-------------|
| **Symétrie** | Liaison(A,B) = Liaison(B,A) |
| **Non-localité** | Existe même à grande distance |
| **Cumulative** | S'additionne sur le volume entier |

**Interprétation physique** : Mesure le couplage temporel entre deux régions de l'espace.

---

### Cartographie Després

**Définition** : Système de cartographie fournissant le facteur $\gamma_{\text{Després}}$ en tout point de l'espace basé sur la distribution de matière et les champs gravitationnels.

**Applications** :

| Échelle | Application |
|---------|-------------|
| Système solaire | TDI vérifié à 0.001% de précision |
| Galaxies | Prédit courbes de rotation plates |
| Cosmologie | Explique expansion différentielle |

---

## Tableau Récapitulatif

| Symbole | Nom | Formule | Unité |
|---------|-----|---------|-------|
| $\tau(x)$ | Distorsion temporelle | $\Phi/c^2$ | sans dim. |
| TDI | Indice de distorsion | $\gamma_{\text{Després}} - 1$ | sans dim. |
| $\gamma_{\text{Després}}$ | Facteur de Lorentz | $1/\sqrt{1-v^2/c^2-2\Phi/c^2}$ | sans dim. |
| $M_D$ | Masse Després | $k\int\tau^2 dV$ | $M_\odot$ |
| $r_c$ | Rayon critique | $2.6(M/10^{10})^{0.56}$ | kpc |
| $k$ | Couplage | $3.97(M/10^{10})^{-0.48}$ | - |
| $\alpha, \beta$ | Amplitudes | $|\alpha|^2+|\beta|^2=1$ | sans dim. |

---

## Comparaison ΛCDM vs TMT

| Concept | ΛCDM | TMT |
|---------|------|-----|
| **Matière noire** | Particules WIMP/axions | Effet géométrique ($M_{\text{Després}}$) |
| **Énergie noire** | Constante cosmologique Λ | Superposition $\alpha/\beta$ dans vides |
| **Unification QM+RG** | Problème ouvert | Équation Després-Schrödinger |
| **Paramètres libres** | 6 (ΛCDM standard) | 2 ($r_c$, $n$) |
| **Détection directe** | Échecs après 50 ans | N/A (pas de particule) |

---

[Retour à l'Accueil](index.md) | [Ponts Conceptuels](ponts_conceptuels/index.md) | [Validation](validation/index.md)
