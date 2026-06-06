# Résultats galactiques

> Le nom historique « Mastery of Time » correspond au nom informel du
> projet ; la désignation scientifique formelle est la
> **Temporon-Mediated Theory (TMT)**.

## Le profil de masse effectif

Dans la limite post-newtonienne statique, l'intégration de la contribution
du tenseur énergie-impulsion du temporon conduit au profil de masse
effectif

$$ M_{\rm eff}(r) = M_{\rm bary}(r)\,\bigl[\,1 + (r/r_{c})^{n}\,\bigr], $$

où \( r_{c} \) est un rayon de transition et \( n \) un exposant. Ce profil
était déjà utilisé de façon phénoménologique dans la littérature ; ici, il
**émerge de l'action**, avec \( r_{c} \) et \( n \) fixés par les
paramètres du lagrangien. L'exposant prend la valeur théorique
\( n = 1/2 \).

## La loi d'échelle r_c ∝ M^(1/2)

Le rayon de transition est fixé par la condition de condensation
\( \rho_{m}(r_{c}) = \rho_{\rm tr} \). Pour un disque exponentiel de masse
baryonique \( M_{\rm bary} \) à densité de surface centrale fixée, la
relation géométrique \( M_{\rm bary} = 2\pi\Sigma_{0}R_{d}^{2} \) implique
une longueur d'échelle \( R_{d}\propto M_{\rm bary}^{1/2} \), d'où

$$ r_{c}(M_{\rm bary}) = r_{c}^{(0)}\,
   \left(\frac{M_{\rm bary}}{10^{10}\,M_{\odot}}\right)^{1/2}\!\mathrm{kpc}. $$

L'exposant \( 1/2 \) découle de la géométrie du disque exponentiel
combinée à la quasi-constance de la hauteur d'échelle verticale du disque.
Le préfacteur numérique vaut \( r_{c}^{(0)}\approx 8{,}7~\mathrm{kpc} \) ;
il possède la contrepartie théorique
\( \mathcal{C}\,(2\pi\Sigma_{0})^{-1/2} \), où \( \mathcal{C} \) est une
constante de condensation sans dimension. La calibration de \( \mathcal{C} \)
sur la galaxie médiane de SPARC fixe cette unique normalisation ; toutes les
applications ultérieures sont alors sans paramètre libre.

## Validation sur l'échantillon SPARC

L'échantillon SPARC (Spitzer Photometry and Accurate Rotation Curves)
comprend 175 galaxies à disque. Quatre échouent aux critères de qualité des
données et trois ont un \( r_{c} \) ajusté à la limite du domaine, ce qui
laisse un **échantillon analysable de 168 galaxies**. Pour chaque galaxie,
les paramètres sont ajustés en fixant l'exposant à sa valeur théorique
\( n = 1/2 \).

| Grandeur | Valeur | Échantillon |
|---|---|---|
| Galaxies SPARC chargées | 175 | — |
| Échantillon analysable | 168 | — |
| Galaxies améliorées vs Newton | 162 / 168 (96,4 %) | — |
| Amélioration médiane du \( \chi^{2} \) | 92,2 % | 168 |
| \( r_{c} \) médian | 5,9 kpc | 168 |
| \( \Delta\mathrm{BIC} > 10 \) en faveur du modèle | 82,7 % | 168 |
| \( \Delta\mathrm{BIC} > 6 \) en faveur du modèle | 85,1 % | 168 |

Les six galaxies pour lesquelles le modèle n'améliore pas l'ajustement
newtonien sont des systèmes dominés par les baryons, bien décrits par la
seule dynamique newtonienne — un comportement attendu lorsque la densité
reste très inférieure à la densité de transition.

## La relation empirique r_c — M_bary

Une régression linéaire en log-log sur les 168 galaxies donne

$$ \log_{10}(r_{c}/\mathrm{kpc}) =
   (0{,}48\pm0{,}04)\,\log_{10}\!\bigl(M_{\rm bary}/10^{10}M_{\odot}\bigr)
   + \log_{10}(8{,}7), $$

avec une corrélation de Pearson \( r = 0{,}69 \) et
\( p = 4{,}7\times10^{-25} \) \( (N = 168) \). L'exposant empirique
\( 0{,}48\pm0{,}04 \) s'écarte de la valeur prédite \( 1/2 \) de
seulement \( 0{,}6\sigma \). La dispersion intrinsèque
\( \sigma_{\log r_{c}}\simeq 0{,}46~\mathrm{dex} \) est compatible avec la
variabilité de la hauteur d'échelle verticale des disques.

Aucune longueur universelle dépendante de la masse n'apparaît dans les
halos \( \Lambda\mathrm{CDM} \)-NFW ; la dynamique newtonienne modifiée
(MOND) postule quant à elle une échelle d'accélération universelle plutôt
qu'une longueur. La dérivation de cette loi d'échelle à partir de l'action
constitue le résultat observationnel central du manuscrit soumis à
*Physical Review D*.

## Prédictions falsifiables

La théorie offre deux prédictions falsifiables à court terme, distinctes de
\( \Lambda\mathrm{CDM} \) :

1. **La loi \( r_{c}\propto M_{\rm bary}^{1/2} \) sur de nouvelles
   galaxies.** DESI et Euclid fourniront des courbes de rotation pour
   environ \( 10^{4} \) galaxies à disque. Un exposant mesuré hors de
   l'intervalle \( [0{,}4 ; 0{,}6] \) sur \( N\gtrsim10^{3} \) galaxies
   falsifierait la dérivation.
2. **L'isotropie stricte de la contribution scalaire au lentillage
   gravitationnel** (sous le niveau de 0,1 %). La contribution du temporon
   est strictement scalaire ; toute corrélation de forme de cisaillement
   détectée au-dessus de ce seuil falsifierait le cadre théorique.

Une prédiction à plus long terme est l'existence d'une polarisation
gravitationnelle scalaire (mode de respiration) d'amplitude
\( h_{s}/h_{t}\sim 10^{-5}\!-\!10^{-2} \), en principe accessible à LISA.
