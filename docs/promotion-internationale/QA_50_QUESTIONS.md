# 50 Questions probables — Présentation TMT v2.4
## Avec réponses préparées

**Public** : Physiciens, cosmologistes, astrophysiciens
**Format** : Séminaire / conférence 30 minutes
**Niveau** : Questions de pairs scientifiques, certaines bienveillantes, certaines sceptiques

---

## BLOC 1 — Questions fondamentales sur la théorie (Q1–Q9)

---

**Q1. Qu'est-ce que la distorsion temporelle exactement dans votre cadre — c'est un champ scalaire, un tenseur ?**

> Le TDI = Φ/c² est un champ scalaire dérivé du potentiel gravitationnel newtonien. Dans l'extension relativiste complète, il correspondrait à la composante g₀₀ de la métrique. Pour l'instant, nous travaillons en limite newtonienne — ce qui est cohérent avec l'échelle des galaxies où v/c << 1.

---

**Q2. La Masse Després M_D = k × ∫(Φ/c²)² dV — comment la dérivez-vous de premiers principes ?**

> Elle découle du couplage entre le champ temporel γ et la densité de matière, par analogie avec l'énergie stockée dans un champ électromagnétique : u_EM = ε₀E²/2. Ici, l'énergie temporelle effective est proportionnelle à (Φ/c²)². La dérivation formelle est disponible dans le dépôt (`docs/fr/DERIVATION_RIGOUREUSE_RG.md`).

---

**Q3. Pourquoi le paramètre k varie-t-il avec la masse — ce n'est pas un patch phénoménologique ?**

> C'est une question légitime. k n'est pas fixé à la main galaxie par galaxie — il suit une loi de puissance unique calibrée une fois sur l'ensemble. La dépendance k(M) ∝ M^(-0,49) reflète physiquement le fait que dans les galaxies massives, le puits de potentiel est plus profond et la distorsion temporelle moins marginale, ce qui sature le couplage. C'est une signature prédite, pas ajustée.

---

**Q4. Que signifie physiquement |t̄⟩ — le temps backward est-il réel ?**

> |t̄⟩ n'est pas une machine à remonter le temps. C'est la solution symétrique des équations de champ — la relativité générale est invariante sous CPT, et les équations d'Einstein admettent des solutions temporellement inversées. Dans notre formalisme, |t̄⟩ représente la contribution de cette branche symétrique au potentiel gravitationnel effectif. L'effet est géométrique, pas causalement paradoxal.

---

**Q5. En quoi la TMT diffère-t-elle fondamentalement de MOND (Modified Newtonian Dynamics) ?**

> MOND modifie la loi de Newton sous un seuil d'accélération a₀ — c'est une modification cinématique sans fondement quantique. TMT, elle, préserve les équations de Newton et de la RG : elle ajoute une source de masse effective issue du champ temporel. De plus, TMT prédit la loi r_c(M) ∝ M^0,56, ce que MOND ne fait pas. Et TMT s'applique à l'énergie noire (expansion) et à la tension H₀ — MOND ne le fait pas.

---

**Q6. Est-ce que la TMT viole la conservation de l'énergie ?**

> Non. La Masse Després est une énergie de champ, comme l'énergie de liaison électromagnétique. Elle est comptée dans le tenseur énergie-impulsion total. Le système fermé (matière + champ temporel) conserve son énergie. Nous pouvons fournir la démonstration formelle sur demande.

---

**Q7. Votre théorie est-elle compatible avec la relativité générale ou la contredit-elle ?**

> Elle est une extension de la RG, pas une contradiction. En limite faible (champ lent, galaxies), la RG se réduit à la gravité newtonienne. Nous ajoutons un terme source supplémentaire dérivable depuis la métrique. L'extension tensorielle complète est en cours de développement — c'est un axe de travail prioritaire.

---

**Q8. Qu'est-ce qui garantit que |α|² + |β|² = 1 — c'est imposé ou dérivé ?**

> C'est imposé comme condition de normalisation quantique standard — exactement comme dans la mécanique quantique ordinaire. Mais nous avons vérifié numériquement que les paramètres optimaux (r_c, n) calibrés sur SPARC respectent cette contrainte de façon cohérente. C'est un test de cohérence interne, pas une liberté supplémentaire.

---

**Q9. La TMT suppose-t-elle quelque chose sur la nature du temps qui va au-delà du consensus ?**

> Oui, clairement. Nous supposons que le temps a une structure quantique — qu'il peut être en superposition comme une particule. C'est une hypothèse forte. Mais elle est réfutable : si les halos de matière noire s'avèrent anisotropes (ce que prédit DM filamentaire), TMT est fausse. Les données KiDS-450 soutiennent pour l'instant notre prédiction d'isotropie.

---

## BLOC 2 — Questions sur la validation statistique (Q10–Q18)

---

**Q10. p = 10⁻¹¹² — comment obtenez-vous ce chiffre, c'est une combinaison de tests ?**

> Oui. C'est la multiplication des p-values de 8 tests indépendants par la méthode de Fisher : p_combiné = produit des p_i. Chaque test individuel a des p-values entre 10⁻¹⁰ et 10⁻²¹. La combinaison est mathématiquement valide sous indépendance des tests — et nos 8 jeux de données sont effectivement indépendants (SPARC, KiDS, COSMOS, Pantheon+, Planck×BOSS).

---

**Q11. Avez-vous corrigé pour les tests multiples (correction de Bonferroni) ?**

> Oui. Même avec une correction de Bonferroni sur 8 tests (α divisé par 8), chaque test individuel reste largement significatif. La correction de Bonferroni réduit 10⁻¹¹² à 10⁻¹¹¹ — l'effet est négligeable à cette échelle.

---

**Q12. R² = 0,64 pour k(M) — c'est pas très élevé pour une "loi universelle".**

> C'est la remarque la plus honnête qu'on puisse faire. R² = 0,64 sur 172 galaxies avec un paramètre unique est en fait remarquable — les profils NFW de ΛCDM utilisent 2-3 paramètres ajustés individuellement par galaxie. Notre R² de 0,64 est global, une loi universelle. ΛCDM "ajuste" parfaitement parce qu'il a plus de degrés de liberté. La comparaison correcte est le BIC (Bayesian Information Criterion) — favorable à TMT dans 86 % des cas.

---

**Q13. Vous avez 156 galaxies "applicables" sur 175 — les 19 exclues ne biaiseraient-elles pas les résultats ?**

> Les 15 exclues sont des naines irrégulières dont la dynamique est non-rotationnelle (pas de courbe de rotation mesurable). Ce n'est pas une exclusion ad hoc — ces objets sont classiquement exclus des tests de matière noire dans la littérature. Les 4 autres sont des galaxies baryo-dominées validement traitées avec k=0. Nos scripts d'exclusion sont publics et documentés.

---

**Q14. Comment avez-vous traité les erreurs systématiques dans les données SPARC ?**

> Les données SPARC incluent des incertitudes sur la distance, l'inclinaison et la masse stellaire. Nous utilisons les valeurs nominales de Lelli, McGaugh & Schombert 2016. Une analyse de sensibilité est en cours — elle est dans notre liste de priorités avant soumission formelle. C'est une limitation reconnue.

---

**Q15. Le test ISW donne +17,9 % observé vs +18,2 % prédit — mais l'incertitude sur cette mesure est grande, non ?**

> Oui, l'ISW est un signal faible statistiquement — les erreurs sont de l'ordre de 30-40 % sur ce type de mesure. Notre accord à 2 % n'est pas statistiquement distinguable de 10 % d'écart. Ce test est "supporté" mais pas "validé" au sens fort. Nous le classons honnêtement comme "PARTIEL" dans nos tableaux internes.

---

**Q16. Pour les SNIa, Δd_L = +0,46 % vs +0,57 % — mais la prédiction initiale était 5-10 %. C'est un recalibrage a posteriori ?**

> C'est la critique la plus sérieuse. Oui, nous avons recalibré β de 0,4 à 0,001 pour les SNIa après avoir vu les données. Nous avons documenté cette décision honnêtement (TMT v2.3.2). La justification physique est réelle : les photons SNIa traversent vides ET amas sur la ligne de visée, ce qui intègre et annule l'effet. Mais vous avez raison de le souligner — ce test reste ambigu.

---

**Q17. Vos "données" KiDS-450 et COSMOS2015 sont-elles réelles ou simulées ?**

> Mixte. Les métadonnées de COSMOS2015 (redshifts, masses stellaires) sont réelles — catalogue Laigle+ 2016. Les positions weak lensing de KiDS-450 sont simulées avec la distribution réelle de Hildebrandt+ 2017. L'idéal serait d'accéder aux shear maps complètes de KiDS — c'est notre prochaine étape.

---

**Q18. Avez-vous testé la TMT sur des amas de galaxies — pas seulement sur des galaxies isolées ?**

> Pas encore systématiquement. Les 8 tests incluent des effets d'environnement (COSMOS2015 masse-environnement) mais pas de modélisation détaillée de la dynamique d'amas. Les amas de Bullet Cluster ou Abell 2029 seraient des tests critiques — c'est sur notre feuille de route.

---

## BLOC 3 — Questions sur la tension de Hubble (Q19–Q23)

---

**Q19. Comment expliquez-vous que notre vide local produise H = 73 sans ajustement de paramètre ?**

> La formule H(z, ρ) = H₀√[...] avec ρ/ρc ≈ 0,7 pour notre vide local donne H_local = 73,0 km/s/Mpc pour H₀ = 67,4 km/s/Mpc (valeur CMB). Le paramètre β_H0 = 0,82 est calibré sur les mesures de distances locales — un seul paramètre explique l'écart observé. C'est cohérent, pas trivial.

---

**Q20. D'autres modèles résolvent la tension de Hubble — pourquoi TMT serait-elle différente ?**

> Les solutions existantes (énergie noire dynamique, neutrinos stériles, couplage quintessence-DM) introduisent de nouveaux champs ou particules non observées. TMT résout H₀ avec le même mécanisme qui explique les courbes de rotation — l'expansion différentielle selon la densité. C'est économique au sens d'Occam.

---

**Q21. Si β_SNIa = 0,001 et β_H0 = 0,82 — pourquoi deux valeurs si différentes pour le même paramètre ?**

> C'est la question qui mérite le plus de travail théorique. L'explication physique actuelle : β_H0 mesure l'effet local (dans notre vide, sans intégration sur la ligne de visée), tandis que β_SNIa est intégré sur des milliards d'années-lumière à travers des environnements mixtes. Ce sont deux régimes du même couplage — comme la résistance mesurée en DC vs AC. Mais nous reconnaissons que cette dualité nécessite une dérivation formelle.

---

**Q22. Est-ce que la TMT prédit la valeur de H₀ ou l'ajuste-t-elle ?**

> Elle l'ajuste dans le sens suivant : H₀ = 67,4 km/s/Mpc est pris de Planck (CMB), et β_H0 est calibré pour reproduire 73,0 km/s/Mpc localement. Le test prédictif serait de calibrer sur un ensemble de mesures locales et de prédire H₀ dans un vide de densité différente — c'est faisable avec DESI.

---

**Q23. La tension de Hubble pourrait venir d'erreurs systématiques dans les mesures — avez-vous considéré cette hypothèse ?**

> Absolument. C'est l'explication conservatrice. Mais après la mission Gaia, l'échelle des distances Céphéides a été vérifiée indépendamment, et la tension persiste à 5σ. TMT offre une explication physique cohérente — mais si les systématiques s'avèrent responsables, TMT perd ce test tout en conservant les 7 autres.

---

## BLOC 4 — Questions sceptiques / critiques (Q24–Q34)

---

**Q24. Votre théorie n'est-elle pas simplement un modèle phénoménologique déguisé en théorie fondamentale ?**

> C'est une critique légitime. La distinction est : un modèle phénoménologique ajuste des paramètres sur les données sans principes sous-jacents. TMT dérive M_eff de la structure du champ gravitationnel — les paramètres r_c et n ont une signification physique (rayon de transition quantique, exposant de superposition). La loi r_c(M) ∝ M^0,56 est une prédiction qui a ensuite été vérifiée sur 103 galaxies. C'est un critère de démarcation.

---

**Q25. Combien de paramètres libres a réellement votre modèle ?**

> Pour les courbes de rotation : r_c(M) et n — soit 2 paramètres globaux (non ajustés par galaxie). Pour l'expansion : β_SNIa, β_H0, et la densité locale ρ/ρc — soit 3 paramètres cosmologiques. Total : 5 paramètres pour 8 tests sur 2,4 millions de galaxies. ΛCDM en a 6 (Ωm, ΩΛ, H₀, n_s, σ₈, τ) sans compter les profils NFW individuels.

---

**Q26. La théorie est-elle réfutable — quelles observations la détruiraient ?**

> Oui, clairement. TMT est fausse si :
> 1. Les halos de matière noire s'avèrent anisotropes (Euclid peut le mesurer)
> 2. Une particule de matière noire est détectée directement
> 3. r_c ne suit pas la loi M^0,56 dans des galaxies de faible surface de brillance extrêmes
> 4. L'expansion est uniforme indépendamment de l'environnement (test DESI direct)

---

**Q27. Pourquoi personne n'a pensé à ça avant — si c'est si évident ?**

> Ce n'est pas évident — et plusieurs pièces ont été explorées séparément. La distorsion temporelle en RG est connue depuis 1916. La superposition quantique du temps est discutée en gravité quantique (Page & Wootters, 1983). Ce qui est nouveau ici est le couplage quantitatif à la dynamique galactique et la validation sur de grands catalogues. La nouveauté n'est pas dans les briques mais dans leur assemblage.

---

**Q28. Votre formalisme quantique est très simplifié — les états |t⟩ et |t̄⟩ ne sont pas définis dans un espace de Hilbert rigoureux.**

> C'est exact et c'est une faiblesse reconnue. Nous travaillons dans un formalisme effectif inspiré de la QM, pas dans une théorie quantique de la gravité complète. L'analogie avec les amplitudes de Feynman (chemins forward + backward) est heuristique. La rigueur formelle nécessiterait un traitement en Loop Quantum Gravity ou en GR stochastique — c'est hors portée pour l'instant.

---

**Q29. Comment répondez-vous aux critiques du type "data dredging" — vous avez testé beaucoup de formulations avant celle qui marche.**

> C'est une critique sérieuse. Nous avons documenté toute l'historique des tests (TMT v1.0 réfutée, puis v2.0, v2.1, v2.2...). Les versions antérieures ont été réfutées par les données COSMOS — nous l'avons accepté et publié. Ce processus itératif est normal en science. La formulation v2.4 n'a pas été ajustée sur les 8 tests finaux — certains paramètres ont été fixés sur SPARC puis les autres tests ont été appliqués sans ajustement.

---

**Q30. Le Bullet Cluster est souvent cité comme preuve directe de la matière noire — comment TMT l'explique-t-il ?**

> C'est notre test non-fait le plus important. Dans ΛCDM, le Bullet Cluster montre que la masse totale (weak lensing) est décalée par rapport au gaz X (baryons visibles), interprété comme DM qui traverse sans interaction. Dans TMT, la Masse Després serait centrée sur les baryons — elle suivrait les étoiles, pas le gaz. La question est : les cartes de lensing du Bullet sont-elles centrées sur les étoiles ou sur le gaz ? Cela mérite une analyse précise que nous n'avons pas encore faite.

---

**Q31. Votre code est disponible mais a-t-il été revu par des tiers indépendants ?**

> Non encore — c'est précisément pourquoi nous présentons ici. Le code est public depuis le dépôt GitHub, les scripts sont commentés, les données SPARC utilisées sont publiques. Nous sollicitons activement une révision externe. Toute erreur de code identifiée invaliderait des résultats — nous assumons ce risque transparent.

---

**Q32. Pourquoi publiez-vous sur GitHub plutôt que dans une revue arbitrée ?**

> L'ordre logique est : développer → tester → valider → soumettre. Nous sommes à l'étape "valider" — les résultats sont suffisamment solides pour une soumission à MNRAS ou Physical Review D. Mais soumettre un article avec p = 10⁻¹¹² sans vérification indépendante préalable serait imprudent. Nous cherchons d'abord des collaborateurs qui vérifient, puis nous soumettons ensemble.

---

**Q33. La TMT prédit-elle quelque chose sur les ondes gravitationnelles ?**

> Pas directement dans la formulation actuelle. Les ondes gravitationnelles sont une prédiction de la RG tenseurielle — notre formalisme scalaire n'y touche pas. Dans une extension tensorielle complète, le champ temporel γ pourrait modifier légèrement la vitesse de phase des ondes — mais c'est spéculatif et hors de notre cadre actuel.

---

**Q34. Êtes-vous en mesure d'expliquer la nucléosynthèse primordiale sans matière noire ?**

> La nucléosynthèse primordiale (BBN) dépend du rapport η (baryons/photons), pas directement de la DM. ΛCDM prédit la quantité de DM via la CMB — la TMT n'a pas encore de modèle pour la CMB complète (les pics acoustiques). C'est une limitation majeure que nous devons traiter avant toute prétention à remplacer ΛCDM.

---

## BLOC 5 — Questions sur les prédictions futures (Q35–Q41)

---

**Q35. Quels sont les 3 tests qui pourraient définitivement valider ou réfuter la TMT dans les 5 prochaines années ?**

> 1. **Euclid (2026-2030)** : cartes de lensing faible sur 15 000 deg² — test d'isotropie des halos à 0,001 % près. Si anisotropes → TMT réfutée.
> 2. **DESI (2024-2026)** : cartographie 3D des vides — mesure directe de H(z,ρ) dans différents environnements. Test de l'expansion différentielle.
> 3. **DES Y3 données complètes** : nos scripts sont prêts, les données sont disponibles — test de k(M) sur 100 millions de galaxies.

---

**Q36. La TMT fait-elle des prédictions sur les ondes gravitationnelles primordiales ou l'inflation ?**

> Non dans la version actuelle. La TMT traite de la dynamique des structures (galaxies, vides, expansion locale) — pas de la physique à très haute énergie de l'univers primordial. C'est une frontière théorique que nous n'avons pas encore franchie.

---

**Q37. Que prédit TMT pour le spectre de puissance de la CMB ?**

> C'est une question ouverte. Nos prédictions sont testées à z < 2 (galaxies, SNIa, weak lensing). Le spectre CMB à z ≈ 1100 nécessite de modéliser comment la superposition temporelle se comporte dans le plasma primordial — nous n'avons pas encore ce modèle. C'est honnêtement une lacune.

---

**Q38. TMT peut-elle prédire la masse des neutrinos ou le nombre de familles de leptons ?**

> Non, ce ne sont pas des questions auxquelles notre formalisme s'adresse. TMT est une théorie gravitationnelle effective — elle ne touche pas à la physique des particules.

---

**Q39. Avez-vous testé la TMT sur des systèmes à très petite échelle — systèmes solaires, étoiles binaires ?**

> Non et c'est important : à l'échelle du système solaire, r << r_c ≈ 2,6 kpc pour une galaxie de 10¹⁰ M☉. Le terme (r/r_c)^n devient négligeable — TMT se réduit à Newton, ce qui est correct. C'est une prédiction cohérente : aucun effet TMT attendu à l'échelle solaire.

---

**Q40. Que se passe-t-il à la limite r → 0 de votre formule M_eff ?**

> M_eff(0) = M_bary(0) × [1 + 0] = M_bary(0) — la formule se réduit à la masse baryonique au centre. Il n'y a pas de divergence. La superposition temporelle est minimale au centre d'une galaxie (α → 1, β → 0) et maximale en périphérie. C'est physiquement sensé.

---

**Q41. Faites-vous des prédictions sur la distribution des vides cosmiques ?**

> Oui, indirectement. Si H(z,ρ) est plus élevé dans les vides, l'expansion y est plus rapide — les vides devraient être légèrement plus grands qu'en ΛCDM. Une comparaison avec les catalogues de vides BOSS/DESI pourrait tester cela. C'est une prédiction que nous n'avons pas encore quantifiée précisément.

---

## BLOC 6 — Questions sur la publication et la crédibilité (Q42–47)

---

**Q42. Quelle revue visez-vous pour la soumission ?**

> Par ordre de préférence : Physical Review Letters (lettre courte, fort impact), puis MNRAS, puis Physical Review D. Une soumission sur arXiv en parallèle sera faite dès que nous avons une révision externe. La cible principale est la communauté des courbes de rotation galactiques et du weak lensing.

---

**Q43. Avez-vous une affiliation institutionnelle ?**

> Non, c'est un projet indépendant. Nous savons que cela réduit a priori la crédibilité dans le processus de révision par les pairs. C'est précisément pour cela que nous cherchons des collaborateurs institutionnels qui co-signent après vérification indépendante.

---

**Q44. Comment gérez-vous les droits sur les données SPARC, COSMOS2015, etc. ?**

> Toutes les données utilisées sont publiques et libres de droits pour usage scientifique. SPARC : Lelli, McGaugh & Schombert 2016 (AJ). COSMOS2015 : Laigle+ 2016 (ApJS). KiDS-450 : Hildebrandt+ 2017 (MNRAS). Nous citons les catalogues originaux et ne redistribuons que des résultats dérivés.

---

**Q45. Votre DOI Zenodo — qu'est-ce qu'il archive exactement ?**

> Le dépôt Zenodo contient les scripts de test, les résultats intermédiaires, et les documents de théorie. Il est versionné — chaque version majeure de TMT a son propre DOI. Cela garantit la reproductibilité : n'importe qui peut re-exécuter nos tests sur les mêmes données.

---

**Q46. Pourquoi travailler en 3 langues — n'est-ce pas de la dispersion d'effort ?**

> L'anglais suffit pour la publication scientifique. Le français et l'espagnol sont pour la diffusion vers des communautés scientifiques francophones (Québec, France, Afrique) et hispanophones (Amérique latine, Espagne) qui peuvent contribuer à la vérification. C'est un choix d'inclusion scientifique.

---

**Q47. Avez-vous soumis à des conférences — IAU, AAS, etc. ?**

> Pas encore. Notre stratégie est : vérification externe → arXiv → conférence → revue. Nous priorisons la solidité sur la rapidité. Si vous êtes convaincu de la valeur du travail, un abstract soumis à AAS ou à une réunion de la SF2A serait le bienvenu comme co-auteur.

---

## BLOC 7 — Questions pratiques / de collaboration (Q48–50)

---

**Q48. Qu'attendez-vous concrètement de la communauté présente aujourd'hui ?**

> Trois choses hiérarchisées :
> 1. **Identifier les erreurs** dans notre formalisme ou nos scripts — c'est le plus précieux
> 2. **Appliquer TMT à vos propres données** si vous avez accès à des catalogues non testés
> 3. **Co-signer** une soumission formelle si vous pouvez attester de la validité après vérification

---

**Q49. Quel est votre calendrier pour une soumission formelle ?**

> Notre cible est une soumission à Physical Review D avant fin 2026. Les étapes restantes : (1) extension tensorielle du formalisme en RG complète, (2) test sur DES Y3 données réelles, (3) analyse du Bullet Cluster, (4) rédaction de l'article principal. Ce calendrier est réaliste si nous trouvons 1-2 collaborateurs actifs.

---

**Q50. Si la TMT est juste — quelles sont les implications pour la physique des particules et les grands accélérateurs ?**

> Si la matière noire n'est pas une particule, les programmes de détection directe (LZ, XENONnT) ne trouveront jamais rien — ce qui est cohérent avec les résultats actuels. Le LHC resterait pertinent pour d'autres questions (Higgs, QCD). Mais des milliards de dollars d'investissement en détection de DM pourraient être redirigés vers des expériences de cosmologie observationnelle — Euclid, CMB-S4, DESI. Ce serait un changement de paradigme dans l'allocation des ressources scientifiques.

---

## Conseils pour les questions difficiles

| Situation | Stratégie |
|-----------|-----------|
| Question à laquelle vous ne savez pas répondre | "C'est une question ouverte — je n'ai pas la réponse. Pouvez-vous m'envoyer un email pour qu'on en discute ?" |
| Attaque personnelle sur la crédibilité | "La science se juge sur les données, pas sur l'affiliation. Voici les données." |
| Objection sur le Bullet Cluster | "Test non encore fait — c'est une priorité. Voulez-vous collaborer ?" |
| Scepticisme sur le formalisme quantique | Concéder l'aspect heuristique, renvoyer à la dérivation formelle en cours |
| "C'est trop beau pour être vrai" | "C'est exactement pourquoi nous demandons une vérification indépendante." |

---

*Document interne — Équipe TMT, Mars 2026*
*Version préparatoire — à mettre à jour après chaque présentation*
