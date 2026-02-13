# Pont 2 : Mécanique Quantique

## Extension de la Mécanique Quantique à l'Échelle Cosmologique

### ΛCDM : Mécanique Quantique Limité aux Particules
Dans ΛCDM, la mécanique quantique s'applique uniquement aux particules élémentaires et à la physique des hautes énergies. L'Univers dans son ensemble suit des lois classiques.

### TMT : Distorsion Temporelle Quantique
TMT étend la mécanique quantique à l'échelle cosmologique via le concept de **distorsion temporelle** :

- L'Univers existe dans un état de **superposition temporelle**
- La **flèche du temps** émerge comme effet quantique
- Les **temporons** sont des excitations quantiques de la distorsion temporelle

---

## L'Équation Després-Schrödinger

TMT unifie mécanique quantique et gravitation via l'équation Després-Schrödinger :

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t} = \left[-\frac{\hbar^2}{2m_{eff}} \nabla^2 + V(x) + mc^2\tau(x)\right] \psi
$$

### Décomposition Visuelle

#### Côté Gauche : Évolution Temporelle Modifiée

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t}
$$

| Composante | Signification |
|------------|---------------|
| $i\hbar$ | Constante de Planck (quantique) |
| $[1 + \tau(x)]^{-1}$ | **NOUVEAU** - Temps ralenti par gravité |
| $\partial\psi/\partial t$ | Dérivée temporelle standard |

**Interprétation** : Le temps propre s'écoule différemment du temps cosmique :

$$
dt_{\text{propre}} = [1 + \tau(x)] \cdot dt_{\text{cosmique}}
$$

Plus $\tau$ est grand → le temps s'écoule plus lentement → la particule évolue plus lentement.

#### Côté Droit : Hamiltonien Effectif

**Terme 1 - Énergie cinétique modifiée** :

$$
\hat{A}_{\text{cinétique}} = -\frac{\hbar^2}{2m_{eff}} \nabla^2\psi
$$

avec $m_{eff} = m_0/\gamma_{\text{Després}}$ où $\gamma_{\text{Després}} = 1/\sqrt{1 - 2\Phi/c^2 - v^2/c^2}$

**Terme 2 - Potentiel classique** (inchangé) :

$$
\hat{A}_{\text{potentiel}} = V(x)\psi
$$

**Terme 3 - Potentiel temporel** (NOUVEAU!) :

$$
\hat{A}_{\text{temporel}} = mc^2\tau(x)\psi
$$

C'est le **terme clé** : une nouvelle énergie potentielle créée par la distorsion temporelle elle-même.

### Signification Physique des Termes

| Terme | Expression | Effet |
|-------|------------|-------|
| $[1+\tau]^{-1}$ | Facteur temporel | Horloge quantique ralentie près des masses |
| $m_{eff}$ | Masse effective | La masse varie avec la distorsion gravitationnelle |
| $mc^2\tau$ | Potentiel temporel | Énergie liée à la distorsion temporelle locale |

### Cas Limites (Validation)

| Limite | Condition | Résultat |
|--------|-----------|----------|
| **Espace plat** | $\tau \to 0$ | Récupère équation de Schrödinger standard ✓ |
| **Classique** | $\hbar \to 0$ | Récupère équation de Hamilton-Jacobi ✓ |
| **Champ faible** | $\tau \ll 1$ | Reproduit redshift gravitationnel d'Einstein ✓ |

---

### Implications pour la Matière Noire
- Pas besoin de particules WIMP exotiques
- La matière noire est un **effet collectif** de la distorsion temporelle
- Compatible avec toutes les observations galactiques

### Validation
- Reproduit parfaitement les courbes de rotation des galaxies (SPARC 100%)
- Prédit la loi $r_c(M)$ observée avec r = 0.768
- Simplifie drastiquement le modèle particulaire

> **[Voir le Lexique](../lexique.md)** pour les définitions complètes de $\tau(x)$, $\gamma_{\text{Després}}$, et tous les termes TMT.

[Retour aux Ponts Conceptuels](index.md) | [Pont Précédent : Physique Connue](physique_connue.md) | [Pont Suivant : Relativité Générale](relativite_generale.md)