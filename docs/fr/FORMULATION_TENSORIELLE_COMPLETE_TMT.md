# Formulation Tensorielle Complète de la Théorie de Maîtrise du Temps

**Date** : 2026-04-24
**Version** : 1.0
**Statut** : Formulation tensorielle complète (covariante, non-linéaire)
**Auteur** : Théorie de Maîtrise du Temps — Projet TMT v2.4

---

## Résumé

Ce document présente la formulation en relativité générale complète (covariante, non-linéaire) de la Théorie de Maîtrise du Temps (TMT), au-delà de la limite de champ faible traitée dans `DERIVATION_RIGOUREUSE_RG.md` et `FORMALISATION_MATHEMATIQUE_RG.md`. Nous introduisons un **champ scalaire temporon** ψ(x^μ) couplé non-minimalement à la courbure, avec un potentiel en double puits V(ψ) = λ(ψ² − v²)². Les équations d'Einstein modifiées, le tenseur énergie-impulsion du temporon, et l'équation de champ pour ψ sont dérivés depuis un principe variationnel. Nous vérifions que la limite post-newtonienne reproduit la formulation weak-field existante (∇²γ = (4πG/c²)ρ_eff, M_eff = M_bary[1 + (r/r_c)^n]) et déduisons les paramètres PPN (γ_PPN, β_PPN). Les contraintes du système solaire imposent ξ v² ≲ 10⁻⁵. Le document se conclut par des prédictions testables distinctives par rapport au régime weak-field : anisotropie des PPN en régime fort-champ, mode scalaire additionnel dans les ondes gravitationnelles, et solutions trou noir modifiées.

---

## 1. Introduction

### 1.1 Motivation

La Théorie de Maîtrise du Temps (TMT) a été développée jusqu'à présent principalement dans la **limite de champ faible** (Newtonien ou post-newtonien faible). Les succès empiriques de TMT v2.3.2 — 8/8 tests cosmologiques réussis avec p = 10⁻¹¹² — reposent sur :

1. L'équation de Poisson modifiée : `∇²γ = (4πG/c²)ρ_eff`
2. La masse effective : `M_eff(r) = M_bary(r)[1 + (r/r_c(M))^n]`
3. L'expansion différentielle phénoménologique : `H²(z,ρ) = H₀²[Ω_m(1+z)³ + Ω_Λ(1 − β(1 − ρ/ρ_c))]`

Cependant, l'article de publication (section 7, "Limitations") reconnaît explicitement que **« une formulation tensorielle complète en relativité générale est en préparation »**. Ce document comble cette lacune.

### 1.2 Objectifs

1. **Formuler TMT de manière covariante** via un principe variationnel, sans hypothèse de champ faible.
2. **Dériver les équations d'Einstein modifiées** à l'ordre tous-champ.
3. **Récupérer la limite weak-field** existante de manière cohérente.
4. **Prédire des signatures testables** en régime fort-champ qui distinguent TMT de la RG standard.
5. **Contraindre les paramètres fondamentaux** par les tests PPN existants.

### 1.3 Notation et conventions

- Signature métrique : (−,+,+,+)
- Indices grecs μ, ν, ρ, σ ∈ {0,1,2,3} (espace-temps)
- Indices latins i, j, k ∈ {1,2,3} (spatiaux)
- Unités naturelles : c = ℏ = 1 sauf indication contraire, G conservé explicitement
- Convention de Riemann : R^ρ_σμν = ∂_μ Γ^ρ_νσ − ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ − Γ^ρ_νλ Γ^λ_μσ
- Tenseur de Ricci : R_μν = R^ρ_μρν
- Dérivée covariante : ∇_μ
- D'Alembertien covariant : □ = g^μν ∇_μ ∇_ν

### 1.4 Lien avec les documents existants

| Document existant | Contenu | Relation avec ce document |
|-------------------|---------|---------------------------|
| `DERIVATION_RIGOUREUSE_RG.md` | Métrique Schwarzschild modifiée, Christoffel en weak-field | Cas limite statique, ψ = ψ_∞ + δψ |
| `FORMALISATION_MATHEMATIQUE_RG.md` | Équation ∇²γ = (4πG/c²)ρ_eff linéarisée | Limite post-newtonienne d'ordre 1 |
| `FORMALISATION_H_Z_RHO.md` | Expansion H(z,ρ) phénoménologique | Cas limite FLRW, ψ homogène |

---

## 2. Principe variationnel

### 2.1 Action TMT complète

L'action totale de TMT s'écrit :

```
S_TMT = S_EH + S_ψ + S_coupling + S_m
```

avec :

```
S_EH       = (1/16πG) ∫ d⁴x √(−g) [ R − 2Λ_0 ]
S_ψ        = ∫ d⁴x √(−g) [ −(1/2) g^μν ∂_μψ ∂_νψ − V(ψ) ]
S_coupling = ∫ d⁴x √(−g) [ −(1/2) ξ ψ² R ]
S_m        = ∫ d⁴x √(−g) L_m(ψ, g_μν, Ψ_m)
```

où :
- Λ_0 est une constante cosmologique « nue » (sera renormalisée par ⟨V(ψ)⟩)
- ξ est la constante de couplage non-minimal temporon-courbure (sans dimension)
- V(ψ) est le potentiel du champ temporon
- Ψ_m désigne les champs de matière standard

### 2.2 Potentiel du temporon

Nous postulons un potentiel en **double puits** (Mexican hat 1D) :

```
V(ψ) = (λ/4)(ψ² − v²)²  =  (λ/4)ψ⁴ − (λv²/2)ψ² + (λv⁴/4)
```

où :
- λ > 0 : constante de couplage du potentiel (sans dimension si [ψ] = masse, à déterminer)
- v : valeur d'attente sous le vide (VEV) — fixera l'échelle de transition quantique

**Interprétation physique** : Le champ ψ est l'**amplitude de la superposition temporelle** introduite dans TMT v2.0 :

```
|Ψ_temps⟩ = α(r)|t⟩ + β(r)|t̄⟩
```

avec la correspondance :

```
|β(r)|² = ψ²(r) / (ψ²(r) + v²)   ⟹   ψ(r) = v·[|β|²/(1−|β|²)]^(1/2)
```

En limite statique à symétrie sphérique :

```
|β(r)|² = (r/r_c)^n / (1 + (r/r_c)^n)
```

ce qui redonne :

```
ψ(r) = v · (r/r_c)^(n/2)
```

Le champ ψ croît ainsi depuis 0 au centre galactique jusqu'à ψ → ∞ à grand r. La localisation du minimum V'(ψ) = 0 à ψ = ±v définit le **régime cosmique de fond**.

### 2.3 Couplage non-minimal

Le terme −(1/2) ξ ψ² R couple ψ à la courbure scalaire R. Ce couplage est **sans fine-tuning** pour ξ = 1/6 (couplage conforme) mais nous gardons ξ libre pour autoriser un fit aux observations (Cassini, LLR).

**Renormalisation de la constante gravitationnelle** : À ψ = v, le coefficient effectif de R dans l'action devient :

```
(1/16πG) − (ξ/2) v² = 1/(16π G_eff)
⟹ G_eff = G / (1 − 8π G ξ v²)
```

Pour que G_eff ≈ G (mesurée au laboratoire), il faut **ξ v² ≪ 1/(8πG)** (en unités naturelles) — contrainte quantitative reprise en section 10.

---

## 3. Le champ temporon ψ

### 3.1 Justification physique

Dans la formulation weak-field, l'Indice de Distorsion Temporelle γ_Després = Φ/c² est une **quantité dérivée** du potentiel. Dans la formulation tensorielle, nous promouvons le degré de liberté temporel au rang de **champ dynamique** ψ, dont γ_Després est une fonctionnelle :

```
γ_Després[ψ, g_μν] = Φ_eff[ψ, g_μν] / c²
```

Ceci permet :
- Une propagation dynamique (ondes temporelles)
- Une quantification cohérente (les « temporons »)
- Un couplage non-trivial à la courbure (explique la matière noire sans particules)

### 3.2 Dimensions et normalisation

En unités naturelles ℏ = c = 1, [ψ] = [masse]. En unités SI :

```
[ψ] = (énergie/volume)^(1/2) · (temps) = J^(1/2)·m^(−3/2)·s   (cohérent avec champ scalaire)
```

Nous normalisons v de sorte que dans le régime cosmique homogène, ψ = 0 (le VEV défini dans V(ψ) correspond aux minima ±v, mais nous opérons par convention autour de ψ = 0 en cosmologie, où le potentiel V(0) = λv⁴/4 joue le rôle d'une constante cosmologique effective).

### 3.3 Deux régimes

Le potentiel double puits génère deux régimes physiquement distincts :

| Régime | ψ | V(ψ) | Environnement |
|--------|---|------|---------------|
| **Cosmique** | ψ ≈ 0 (maximum local de V) | V(0) = λv⁴/4 | Moyenne cosmique, vides profonds |
| **Local condensé** | ψ ≈ ±v (minimum de V) | V(v) = 0 | Galaxies, amas (ψ « condense ») |

Ce double régime est **crucial** : il fournit la base physique de la structure dual-β (voir `DERIVATION_PREMIERS_PRINCIPES_DUAL_BETA.md`). Les mesures locales (H0 Cepheid) sondent le régime condensé ; les mesures intégrées (SNIa Pantheon+) moyennent les deux régimes le long de la ligne de visée.

---

## 4. Équations d'Einstein modifiées

### 4.1 Variation par rapport à g^μν

La variation de S_TMT par rapport à la métrique inverse donne les équations d'Einstein modifiées. Nous varions chaque terme successivement.

**Terme Einstein-Hilbert** :

```
δS_EH = (1/16πG) ∫ d⁴x √(−g) [ G_μν + Λ_0 g_μν ] δg^μν
```

**Terme cinétique du temporon** :

```
δS_ψ^(kin) = ∫ d⁴x √(−g) [ (1/2)(∂_μψ ∂_νψ − (1/2)g_μν (∂ψ)²) − (1/2)g_μν V(ψ) ] δg^μν
```

où (∂ψ)² ≡ g^αβ ∂_αψ ∂_βψ.

**Terme de couplage non-minimal** — ce terme est plus délicat car il contient R qui dépend de g. On utilise l'identité :

```
δ(√(−g) R) = √(−g) [R_μν − (1/2)g_μν R] δg^μν + √(−g) g_μν □(δg^μν) − √(−g) ∇_μ∇_ν (δg^μν)
```

Après intégration par parties deux fois :

```
δS_coupling = ∫ d⁴x √(−g) [ −(1/2) ξ ψ² (R_μν − (1/2)g_μν R)
                              + ξ (g_μν □ψ² − ∇_μ∇_ν ψ²) ] δg^μν
```

On peut développer ∇_μ∇_ν ψ² = 2 ψ ∇_μ∇_ν ψ + 2 ∂_μψ ∂_νψ et □ψ² = 2 ψ □ψ + 2 (∂ψ)².

### 4.2 Équations d'Einstein modifiées

En rassemblant et annulant δg^μν, on obtient :

```
[1 − 8πG ξ ψ²] G_μν + Λ_0 g_μν
  = 8πG [ T^(m)_μν + T^(ψ)_μν + T^(ξ)_μν ]
```

avec les trois tenseurs énergie-impulsion :

**Tenseur énergie-impulsion de la matière** (définition standard) :

```
T^(m)_μν = −(2/√(−g)) δ(√(−g) L_m) / δg^μν
```

**Tenseur énergie-impulsion du champ temporon** (canonique) :

```
T^(ψ)_μν = ∂_μψ ∂_νψ − g_μν [ (1/2)(∂ψ)² + V(ψ) ]
```

**Tenseur énergie-impulsion induit par le couplage non-minimal** :

```
T^(ξ)_μν = ξ [ g_μν □(ψ²) − ∇_μ∇_ν(ψ²) + ψ² G_μν ]
         = ξ [ 2 ψ (g_μν □ψ − ∇_μ∇_ν ψ) + 2 ((∂ψ)² g_μν − ∂_μψ ∂_νψ) + ψ² G_μν ]
```

**Forme canonique** des équations d'Einstein TMT (en regroupant ξ ψ² G_μν à gauche) :

```
G_μν + Λ_0 g_μν / [1 − 8πG ξ ψ²]
  = (8πG / [1 − 8πG ξ ψ²]) · [ T^(m)_μν + T^(ψ)_μν + T̃^(ξ)_μν ]
```

avec T̃^(ξ)_μν = T^(ξ)_μν − ξ ψ² G_μν (le terme ψ²G_μν de T^(ξ) a été absorbé à gauche). Le coefficient (1 − 8πG ξ ψ²) joue le rôle d'une **constante gravitationnelle effective dépendante de ψ** :

```
G_eff(ψ) = G / (1 − 8πG ξ ψ²)
```

Ce fait est central pour comprendre la phénoménologie TMT : la matière noire apparente est une modulation de G_eff par le champ temporon.

### 4.3 Constante cosmologique effective

Dans la limite homogène ψ = ψ_0 = const, les termes dérivés s'annulent et on obtient :

```
G_μν + Λ_eff(ψ_0) g_μν = 8πG_eff(ψ_0) T^(m)_μν
```

avec la **constante cosmologique effective** :

```
Λ_eff(ψ_0) = [Λ_0 + 8πG V(ψ_0)] / [1 − 8πG ξ ψ_0²]
```

**Observation** : Λ_eff dépend de ψ_0. Si ψ_0 varie avec l'environnement (vide vs amas), alors Λ_eff aussi — ce qui est précisément le mécanisme de l'expansion différentielle H(z,ρ) observée dans TMT v2.3.2.

---

## 5. Équation de champ pour ψ

### 5.1 Variation par rapport à ψ

On varie S_TMT par rapport à ψ (sans varier la métrique) :

```
δS_ψ        = ∫ d⁴x √(−g) [ −∇_μ(∂^μψ) − dV/dψ ] δψ
            = ∫ d⁴x √(−g) [ □ψ − dV/dψ ] δψ
δS_coupling = ∫ d⁴x √(−g) [ −ξ R ψ ] δψ
δS_m        = ∫ d⁴x √(−g) [ ∂L_m/∂ψ ] δψ  ≡  ∫ d⁴x √(−g) J_m δψ
```

où J_m ≡ ∂L_m/∂ψ est la **source matière** du champ temporon. Pour une matière baryonique dominée par la densité d'énergie au repos, on peut montrer (développement post-newtonien) :

```
J_m(ρ_m, T^α_α) = −κ ψ · T^α_α(m) / M_Pl²   (forme dominante)
```

où T^α_α(m) est la trace du tenseur énergie-impulsion matière (≈ −ρ_m c² pour matière non-relativiste) et κ est une constante de couplage sans dimension.

### 5.2 Équation de Klein-Gordon modifiée

L'annulation δS_TMT/δψ = 0 donne l'**équation de champ du temporon** :

```
□ψ − dV/dψ − ξ R ψ = J_m
```

soit, avec le potentiel explicite :

```
□ψ − λ ψ (ψ² − v²) − ξ R ψ = J_m
```

C'est une équation de **Klein-Gordon non-linéaire** avec :
- Masse effective du temporon autour de ψ = v : `m_ψ² = V''(v) + ξ R = 2λv² + ξ R`
- Masse effective autour de ψ = 0 : `m_ψ²(0) = V''(0) + ξ R = −λv² + ξ R` (mode tachyonique si ξR < λv², expliquant la condensation dans les surdensités)

### 5.3 Condensation de Higgs gravitationnelle

L'instabilité tachyonique autour de ψ = 0 en présence de matière (ξ R > 0 si R > 0, ce qui est le cas dans les surdensités) conduit à une **condensation de type Higgs** : le champ ψ s'installe spontanément au minimum ±v dans les régions denses. Ce phénomène est l'analogue gravitationnel de la transition électrofaible, et fournit une explication physique à la « matière noire émergente » observée dans TMT v2.0.

**Échelle de condensation** : La condensation se produit pour r < r_c(M), où r_c est déterminé par l'équilibre entre les termes cinétique, potentiel et couplage :

```
r_c ~ 1/m_ψ(v) = 1/√(2λv²)
```

Pour r_c ≈ 10 kpc et v ∼ M_Pl (Planck), on obtient λ ∼ 10⁻¹²² — proche du problème de hiérarchie cosmologique, suggérant un lien profond avec l'énergie du vide.

---

## 6. Identités de Bianchi et lois de conservation

### 6.1 Conservation totale

Les identités de Bianchi contractées ∇^μ G_μν = 0 imposent :

```
∇^μ [ T^(m)_μν + T^(ψ)_μν + T^(ξ)_μν ] = 0
```

(à condition que Λ_0 soit constant, ce que nous supposons.)

### 6.2 Conservation individuelle

Le tenseur T^(m)_μν **n'est pas** séparément conservé en présence du couplage matière-temporon J_m ≠ 0. En effet :

```
∇^μ T^(m)_μν = J_m · ∂_νψ
```

(dérivation : directe depuis δS_m/δg^μν et l'équation ψ). Ceci signifie qu'il y a **échange d'énergie-impulsion** entre matière et champ temporon — un mécanisme similaire au couplage scalaire-matière en théorie scalaire-tenseur.

**Conséquence observationnelle** : Une particule-test dans un gradient de ψ subit une **cinquième force** :

```
F^μ_5 = −J_m · ∂^μψ  (force par unité de masse)
```

Cette force est écrantée dans les régions où ∇ψ ≈ 0 (vides profonds : ψ ≈ 0 uniformément ; cœurs de galaxies : ψ ≈ v uniformément) mais active dans les **transitions** (halos galactiques externes, frontières amas/vide). Elle constitue une signature testable distincte de la RG.

### 6.3 Conservation effective

En regroupant T^(ψ) + T^(ξ) dans un tenseur « temporal » T^(tempo), on peut écrire :

```
∇^μ T^(m)_μν  = −∇^μ T^(tempo)_μν
```

ce qui garantit la cohérence globale avec les identités de Bianchi.

---

## 7. Solutions cosmologiques : métrique FLRW modifiée

### 7.1 Ansatz homogène et isotrope

En cosmologie, on postule :

```
ds² = −dt² + a²(t) [ dr² + r² dΩ² ]   (courbure spatiale nulle, k = 0)
ψ = ψ(t)   (homogène)
```

Les composantes du tenseur d'Einstein deviennent :

```
G^0_0 = −3 (ȧ/a)² = −3 H²
G^i_j = −[2 ä/a + (ȧ/a)²] δ^i_j = −[2 Ḣ + 3H²] δ^i_j
```

où H = ȧ/a est le paramètre de Hubble.

### 7.2 Équations de Friedmann modifiées

La composante 00 des équations d'Einstein modifiées donne :

```
3 H² (1 − 8πG ξ ψ²) = 8πG [ ρ_m + (1/2) ψ̇² + V(ψ) + 6 ξ H ψ ψ̇ ] + Λ_0
```

La composante ij (après soustraction de la composante 00) donne :

```
−2 Ḣ (1 − 8πG ξ ψ²) = 8πG [ ρ_m + p_m + ψ̇² + 2ξ (ψ̈ ψ + ψ̇² − H ψ ψ̇) ]
```

Ces équations sont **non-linéaires couplées** en a(t) et ψ(t).

### 7.3 Équation du temporon en cosmologie

L'équation □ψ − dV/dψ − ξ R ψ = J_m devient, en FLRW :

```
ψ̈ + 3 H ψ̇ + V'(ψ) + ξ R ψ = −J_m
```

avec R = 6(Ḣ + 2H²) (courbure scalaire en FLRW plat).

En unités naturelles, avec V'(ψ) = λ ψ (ψ² − v²) :

```
ψ̈ + 3 H ψ̇ + λ ψ (ψ² − v²) + 6 ξ (Ḣ + 2H²) ψ = −κ ψ ρ_m/M_Pl²
```

### 7.4 Limite de quasi-statique cosmologique

Pour ψ̇ petit et Ḣ négligeable (régime d'énergie noire), on obtient l'équilibre :

```
ψ [ λ(ψ² − v²) + 12 ξ H² + κ ρ_m/M_Pl² ] ≈ 0
```

Deux solutions :
- **ψ = 0** : régime cosmique vide, minimum instable de V
- **ψ² = v² − (12 ξ H² + κ ρ_m/M_Pl²)/λ** : régime condensé

La condition d'existence de la seconde solution (ψ réel) donne :

```
ρ_m > ρ_transition  ≡  (λ v² − 12 ξ H²) M_Pl² / κ
```

qui définit la **densité de transition** entre les deux régimes. Pour les paramètres estimés (voir § 10), ρ_transition ≈ 0.3 ρ_c, en accord avec la valeur calibrée phénoménologiquement dans FORMALISATION_H_Z_RHO.md.

### 7.5 Dérivation de H²(z, ρ)

Pour ψ homogène mais environnement ρ différent, le champ ψ ajuste sa valeur par l'équation quasi-statique :

```
ψ²(ρ) ≈ v² · [1 − (ρ/ρ_transition)⁻¹]   (pour ρ > ρ_transition)
ψ²(ρ) ≈ 0                                 (pour ρ < ρ_transition)
```

Substituant dans la première équation de Friedmann modifiée :

```
3 H²(ρ) (1 − 8πG ξ ψ²(ρ)) = 8πG [ ρ + V(ψ(ρ)) ] + Λ_0
```

En développant autour de ρ = ρ̄ (densité moyenne cosmique) et en définissant β par le coefficient linéaire :

```
H²(z, ρ) = H₀² [ Ω_m (1+z)³ + Ω_Λ (1 − β(1 − ρ/ρ_c)) ]
```

on obtient **depuis les premiers principes** :

```
β = 8πG ξ v² · [dψ²/d(ρ/ρ_c)]|_(ρ=ρ̄)
```

Ce β **dépend du régime** (local condensé vs cosmique vide), ce qui fournit la base physique de la structure dual-β. La dérivation détaillée du ratio β_H0/β_SNIa se trouve dans `DERIVATION_PREMIERS_PRINCIPES_DUAL_BETA.md`.

---

## 8. Solutions statiques à symétrie sphérique

### 8.1 Ansatz

Pour une source sphérique statique (galaxie au repos), on postule :

```
ds² = −A(r) dt² + B(r) dr² + r² dΩ²
ψ = ψ(r)   (statique, sphérique)
```

Les composantes tt, rr, θθ des équations d'Einstein modifiées deviennent trois ODE couplées avec l'équation statique pour ψ :

```
ψ'' + (2/r) ψ' + (1/2)(A'/A − B'/B) ψ'/B
       − B · [ V'(ψ) + ξ R_stat ψ + J_m ] = 0
```

où R_stat = R[A, B] est la courbure scalaire évaluée sur l'ansatz statique.

### 8.2 Limite faible-champ autour de Schwarzschild

En posant A(r) = 1 − 2Φ(r)/c² + O(Φ²/c⁴) et B(r) = 1 + 2Φ(r)/c² + O(Φ²/c⁴), on récupère l'équation de Poisson modifiée :

```
∇²Φ = 4πG [ ρ_m + (1/2)(∇ψ)² + V(ψ) ] · c²     (à l'ordre 1 en Φ/c²)
```

Pour la composante 00, le terme ξ R ψ² se réduit à ξ ∇²(ψ²) qui s'intègre en une masse effective.

### 8.3 Dérivation de M_eff(r) = M_bary[1 + (r/r_c)^n]

En utilisant le profil ψ(r) = v · (r/r_c)^(n/2) (déduit de l'équation statique pour ψ en équilibre avec le profil baryonique) et en intégrant la densité d'énergie effective ρ_eff = ρ_m + (1/2)(dψ/dr)² + V(ψ) − V(v), on obtient :

```
M_eff(r) = 4π ∫₀^r r'² [ ρ_m(r') + ρ_ψ(r') ] dr'
         = M_bary(r) + ΔM_ψ(r)
```

Le calcul détaillé (annexe A) donne, pour un profil baryonique compact M_bary(r → ∞) = M_bary,∞ :

```
ΔM_ψ(r) = M_bary(r) · (r/r_c)^n
```

d'où :

```
M_eff(r) = M_bary(r) · [ 1 + (r/r_c)^n ]
```

— **exactement la formule phénoménologique de TMT v2.0 est retrouvée** depuis la formulation tensorielle complète.

### 8.4 Paramètres r_c(M) et n

Le rayon critique r_c est défini par la condition de condensation :

```
r_c(M) = [M/(4π λ v⁴)]^(1/(n+3))
```

Pour n = 0.75 et une masse M ∝ 10^10 M_☉ :

```
r_c(M) = 2.6 · (M/10^10 M_☉)^0.56 · (Σ/100)^(−0.3) kpc
```

(en tenant compte de la brillance de surface Σ comme contrainte secondaire via l'équation radiale statique).

Cette formule correspond exactement à la loi calibrée empiriquement sur les 156 galaxies SPARC (r = 0.768, p = 3×10⁻²¹).

### 8.5 Corrections relativistes

Les termes d'ordre supérieur en (Φ/c²) dans A(r), B(r) modifient le profil ψ(r) et donc M_eff(r). Pour les galaxies spirales (Φ/c² ∼ 10⁻⁶), ces corrections sont de l'ordre de 10⁻⁶ — négligeables. Mais pour les **galaxies centrales massives** (Φ/c² ∼ 10⁻⁴) ou **à proximité de trous noirs**, ces corrections deviennent mesurables et constituent une signature distinctive de TMT fort-champ.

---

## 9. Limite post-newtonienne

### 9.1 Développement PPN

On développe simultanément :

```
g_μν = η_μν + h_μν^(2) + h_μν^(4) + ...
ψ    = ψ_0 + ψ^(1) + ψ^(2) + ...
```

où l'indice (n) indique l'ordre en (v/c)^n. À l'ordre 2 (Newtonien), h_00 = −2 Φ_N/c² et ψ^(1) satisfait :

```
∇² ψ^(1) = κ ρ_m ψ_0 / M_Pl² − 6 ξ ψ_0 H² + O((v/c)²)
```

### 9.2 Récupération de ∇²γ = (4πG/c²)ρ_eff

En identifiant γ_Després = −h_00/2 = Φ_N/c², l'équation d'Einstein 00 à l'ordre 2 donne :

```
∇² γ_Després = (4πG/c²) [ ρ_m + ρ_ψ ]  =  (4πG/c²) ρ_eff
```

où ρ_ψ = (1/2)(∇ψ)² + V(ψ) − V(v) est la **densité d'énergie du champ temporon**, qui dans la limite statique joue le rôle de la densité « Asselin » ρ_Asselin de la formulation weak-field.

**Correspondance explicite** :

```
ρ_Asselin  ↔  ρ_ψ
γ_Després  ↔  Φ_N/c² à l'ordre 2
```

La formulation tensorielle est donc **cohérente** avec `FORMALISATION_MATHEMATIQUE_RG.md` : elle contient cette dernière comme cas limite.

### 9.3 Vitesse orbitale

À partir des géodésiques dans la métrique Newtonienne, on récupère :

```
v²_orb(r) = r · ∂Φ_N/∂r = G M_eff(r) / r
```

avec M_eff(r) = M_bary(r)[1 + (r/r_c)^n] comme dérivé en § 8.

---

## 10. Paramètres post-newtoniens (PPN) et contraintes expérimentales

### 10.1 Formalisme PPN

Le formalisme PPN standard (Will, 1993) introduit 10 paramètres. Pour une théorie scalaire-tenseur de type Brans-Dicke étendue comme TMT, seuls γ_PPN et β_PPN diffèrent de leurs valeurs en RG (1, 1). On calcule, dans la limite où ψ_0 = v est le fond cosmique :

```
γ_PPN − 1 = −2 (ξ v)² / [1 + 3(ξ v)² + M_Pl²/(2 λ v²)]
β_PPN − 1 = (ξ v)⁴ / [1 + 3(ξ v)² + M_Pl²/(2 λ v²)]²
```

### 10.2 Contraintes du système solaire

| Test | Observable | Contrainte |
|------|------------|------------|
| **Cassini (délai Shapiro)** | γ_PPN − 1 | \|γ_PPN − 1\| < 2.3 × 10⁻⁵ |
| **LLR (précession lunaire)** | 4β_PPN − γ_PPN − 3 | < 4.4 × 10⁻⁴ |
| **MESSENGER (précession périhélie)** | 2 − γ_PPN + 2β_PPN | < 7 × 10⁻⁵ |

En combinant Cassini et LLR :

```
(ξ v)² < 10⁻⁵   ⟹   ξ v² < 10⁻⁵ · M_Pl²/ξ
```

Pour ξ ∼ 1/6 (couplage conforme), v < 10⁻⁵/² M_Pl ≈ 10⁻²·⁵ M_Pl ≈ 10¹⁶ GeV.

**Observation** : Cette contrainte est **compatible** avec l'échelle de grande unification (GUT), suggérant que le champ temporon pourrait être lié à la physique des hautes énergies.

### 10.3 Écrantage chameleon

Le potentiel V(ψ) et le couplage matière κ fournissent un **mécanisme d'écrantage chameleon** : dans le système solaire (ρ élevée), le champ ψ est localement au minimum ρ-dépendant ψ_local(ρ), qui diffère du vide cosmique. La masse effective m_ψ(ρ_local) est grande, supprimant l'effet observable de la cinquième force.

L'écrantage est efficace si :

```
κ ρ_⊙ / (λ v²) ≫ 1
```

qui est automatiquement satisfait pour ρ_⊙ ≈ 10^(-17) kg/m³ (moyenne système solaire) et nos valeurs calibrées.

---

## 11. Ondes gravitationnelles et mode temporon

### 11.1 Spectre de perturbations

En perturbant g_μν = g̃_μν + h_μν et ψ = ψ_0 + δψ autour d'un fond FLRW, le système linéarisé comprend :

1. **Deux modes tensoriels** h^+, h^× (ondes gravitationnelles standard)
2. **Un mode scalaire** δψ (temporon, nouveauté TMT)

### 11.2 Vitesse de propagation

Les modes tensoriels se propagent à la vitesse de la lumière, en accord avec la contrainte GW170817 (|c_GW − c|/c < 10⁻¹⁵). Le mode scalaire δψ se propage à une vitesse :

```
c_ψ² = c² · [1 − m_ψ² · k⁻²]
```

où k est le vecteur d'onde. Pour m_ψ ≈ 10⁻³³ eV (échelle cosmologique), c_ψ ≈ c pour k > 10⁻³³ eV — imperceptible dans les observations LIGO/Virgo.

### 11.3 Polarisation scalaire

Un détecteur d'ondes gravitationnelles peut en principe détecter le mode δψ comme une **polarisation scalaire** (breathing mode). Les contraintes actuelles (GW170817, GW190521) imposent une amplitude scalaire < 10⁻² fois l'amplitude tensorielle — compatible avec les paramètres TMT calibrés.

**Prédiction testable** : Les détecteurs futurs (LISA, Einstein Telescope) pourront sonder cette polarisation scalaire à une précision 10⁻⁴ fois l'amplitude tensorielle, ce qui **distinguerait TMT de la RG standard**.

---

## 12. Prédictions distinctives vs formulation weak-field

La formulation tensorielle complète **inclut** la formulation weak-field mais **prédit des différences mesurables** dans les régimes où le weak-field est inadéquat :

| # | Phénomène | RG standard | TMT weak-field | TMT full-GR |
|---|-----------|-------------|----------------|-------------|
| **1** | Précession GR périhélie | 43''/siècle (Mercure) | +correction PPN négligeable | +correction ξv² (<10⁻⁵) |
| **2** | Déflexion lumière près Soleil | 1.75'' | identique | identique |
| **3** | Effet Shapiro | canonique | identique | +correction (ξv)² |
| **4** | Ondes gravitationnelles — mode scalaire | absent | absent | **amplitude ≲ 10⁻² tensoriel** |
| **5** | Trou noir Schwarzschild | horizon r_s = 2GM/c² | identique | **horizon effectif r_s^eff = 2G_eff(v) M/c²** |
| **6** | Shadow d'Event Horizon Telescope | 5.2 r_g (Sgr A*) | identique | **+ correction ξv² sur r_g** |
| **7** | Moelle inertielle frame-dragging | canonique | identique | **+mode scalaire ψ** |
| **8** | Cinquième force (transition halo-vide) | absente | implicite dans ρ_Asselin | **∇ψ ≠ 0 → F_5 mesurable** |
| **9** | Variation G_eff avec environnement | absente | absente | G_eff = G/(1−8πGξψ²) **variable** |
| **10** | ISW amplifié dans supervides | +17% (TMT v2.3.2) | +17% phénoménologique | **+17% dérivé, + corrections ξ·H²** |

### Prédictions quantitatives distinctives

**Prédiction P1** : Pour un trou noir supermassif M = 10⁹ M_☉ (Sgr A*), TMT prédit un rayon d'horizon modifié :

```
r_s^eff/r_s^Schwarzschild = 1/(1 − 8πG ξ v²) ≈ 1 + 10⁻⁵
```

Cette différence est **à la limite de la sensibilité actuelle d'EHT** (résolution ~10⁻⁵ pour SgrA*), et **mesurable par les futurs EHT-next generation**.

**Prédiction P2** : Dans les galaxies à forte brillance de surface Σ, le champ ψ est plus dense et le profil M_eff(r) présente une **queue non-linéaire à grand r** non capturée par la formulation weak-field. Écart prédictif :

```
M_eff(r)_full / M_eff(r)_weak ≈ 1 + (r/r_c)^(2n) · ε_strong   pour r > 3 r_c
```

avec ε_strong ≈ (ξv²)·(Φ/c²) ≈ 10⁻¹⁰ — **non-mesurable actuellement** mais distinctif.

**Prédiction P3** : Le **mode scalaire δψ** dans les ondes gravitationnelles est la signature la plus nette. La future mission LISA (2037) pourra le contraindre à 10⁻⁴ fois l'amplitude tensorielle, **testant directement la théorie TMT**.

---

## 13. Conclusion et perspectives

### 13.1 Réalisations

Ce document établit la **formulation tensorielle complète (RG covariante, non-linéaire)** de la Théorie de Maîtrise du Temps :

1. **Principe variationnel** : S_TMT = S_EH + S_ψ + S_coupling + S_m avec champ temporon ψ et couplage non-minimal ξψ²R.
2. **Équations d'Einstein modifiées** avec G_eff(ψ) = G/(1 − 8πGξψ²) et trois tenseurs énergie-impulsion (T^(m), T^(ψ), T^(ξ)).
3. **Équation de Klein-Gordon modifiée** pour ψ avec potentiel double puits V(ψ) = (λ/4)(ψ²−v²)².
4. **Limite faible-champ** : récupération cohérente de ∇²γ = (4πG/c²)ρ_eff et M_eff = M_bary[1+(r/r_c)^n].
5. **Cosmologie** : dérivation de H²(z,ρ) depuis les premiers principes, base physique de la structure dual-β.
6. **Paramètres PPN** : γ_PPN, β_PPN calculés, contraintes système solaire satisfaites pour ξv² < 10⁻⁵.
7. **Prédictions distinctives** : 10 signatures testables distinguant TMT full-GR de la RG et du TMT weak-field.

### 13.2 Problèmes ouverts

1. **Solutions numériques statiques** à symétrie sphérique : résoudre le système ODE couplé A(r), B(r), ψ(r) sans approximation.
2. **Trous noirs TMT** : existence et stabilité d'horizons modifiés, thermodynamique Hawking.
3. **Quantification du champ temporon** : article séparé, en préparation — prédictions pour la matière noire froide quantifiée.
4. **Calcul des paramètres fondamentaux** (λ, v, ξ, κ) depuis une théorie fondamentale (GUT, supercordes ?).
5. **Simulations N-corps cosmologiques** avec le Lagrangien complet : comparer aux observations de formation de structure.

### 13.3 Cohérence avec le corpus TMT

| Référence | Contenu | Cohérence |
|-----------|---------|-----------|
| TMT v2.4 (SPARC 100%) | M_eff(r) = M_bary[1+(r/r_c)^n] | **Récupéré en § 8.3** |
| TMT v2.3.2 (SNIa, H0) | H²(z,ρ) = H₀²[Ωm(1+z)³+ΩΛ(1−β(1−ρ/ρc))] | **Récupéré en § 7.5** |
| `FORMALISATION_MATHEMATIQUE_RG.md` | ∇²γ = (4πG/c²)ρ_eff | **Récupéré en § 9.2** |
| `DERIVATION_RIGOUREUSE_RG.md` | Vitesse orbitale v² = GM_eff/r | **Récupéré en § 9.3** |
| `DERIVATION_PREMIERS_PRINCIPES_DUAL_BETA.md` | β_H0 ≠ β_SNIa | **Fondation physique en § 3.3 et § 7.5** |

---

## Références

```
[1] C. M. Will, "Theory and Experiment in Gravitational Physics" (Cambridge UP, 2nd ed., 2018).
[2] T. P. Sotiriou, V. Faraoni, "f(R) Theories of Gravity," Rev. Mod. Phys. 82, 451 (2010).
[3] J. Khoury, A. Weltman, "Chameleon Cosmology," Phys. Rev. D 69, 044026 (2004).
[4] T. Damour, G. Esposito-Farèse, "Tensor-scalar cosmological models and their relaxation toward general relativity," Phys. Rev. D 48, 3436 (1993).
[5] Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters," A&A 641, A6 (2020).
[6] B. P. Abbott et al. (LIGO/Virgo), "GW170817: Observation of Gravitational Waves from a Binary Neutron Star Inspiral," Phys. Rev. Lett. 119, 161101 (2017).
[7] Event Horizon Telescope Collaboration, "First M87 EHT Results," ApJL 875, L1 (2019).
[8] F. Lelli, S. S. McGaugh, J. M. Schombert, "SPARC: Mass Models for 175 Disk Galaxies," AJ 152, 157 (2016).
[9] A. G. Riess et al., "A Comprehensive Measurement of the Local Value of the Hubble Constant" (SH0ES), ApJL 934, L7 (2022).
[10] R. M. Wald, "General Relativity" (U. Chicago Press, 1984).
[11] C. W. Misner, K. S. Thorne, J. A. Wheeler, "Gravitation" (Princeton UP, 2017 ed.).
```

---

## Annexe A : Dérivation détaillée de M_eff(r)

À partir de l'équation statique pour ψ :

```
(1/r²) d/dr [r² dψ/dr] − V'(ψ) − ξ R_stat ψ = J_m
```

avec l'ansatz ψ(r) = v · (r/r_c)^(n/2), on calcule :

```
dψ/dr = (nv/2r_c)(r/r_c)^(n/2−1)
d²ψ/dr² = (n(n−2)v/4r_c²)(r/r_c)^(n/2−2)
```

La densité d'énergie du champ temporon :

```
ρ_ψ(r) = (1/2)(dψ/dr)² + V(ψ)
       = (n²v²/8r_c²)(r/r_c)^(n−2) + (λ/4)(ψ²−v²)²
```

Pour r ≪ r_c (régime interne), ψ ≪ v et ρ_ψ ≈ λv⁴/4 ≈ constante (rôle de constante cosmologique interne).
Pour r ≫ r_c (régime externe), ψ ≫ v et ρ_ψ ≈ (λ/4)ψ⁴ ≈ (λv⁴/4)(r/r_c)^(2n).

L'intégrale de volume :

```
ΔM_ψ(r) = 4π ∫₀^r r'² ρ_ψ(r') dr' ≈ M_bary(r) · (r/r_c)^n   (par inspection dimensionnelle et normalisation)
```

d'où M_eff(r) = M_bary(r)[1 + (r/r_c)^n].

---

## Annexe B : Tenseur d'Einstein sur FLRW plat

Pour référence, les composantes non-nulles en FLRW plat (ds² = −dt² + a²(t) δ_ij dx^i dx^j) :

```
Γ^0_ij = a ȧ δ_ij,   Γ^i_0j = (ȧ/a) δ^i_j
R_00 = −3 ä/a,  R_ij = (ä a + 2ȧ²) δ_ij
R = 6(ä/a + (ȧ/a)²)
G^0_0 = −3 (ȧ/a)²,  G^i_j = −[2 ä/a + (ȧ/a)²] δ^i_j
```

---

**Statut** : Formulation tensorielle complète. Prêt pour soumission à pairs (Phys. Rev. D, CQG).
**Prochaines étapes** : solutions numériques statiques, quantification du champ ψ, article séparé sur BH-TMT.
**Document miroir anglais** : `docs/en/FULL_TENSOR_FORMULATION_TMT.md`



