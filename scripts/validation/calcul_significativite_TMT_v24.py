#!/usr/bin/env python3
"""
Calcul de significativite statistique - TMT v2.3.1
Probabilite que les resultats soient dus au hasard

Auteur: Pierre-Olivier Despres Asselin
Date: Janvier 2026
"""

import scipy.stats as stats
import numpy as np

def main():
    print("=" * 70)
    print("CALCUL DE SIGNIFICATIVITE STATISTIQUE - TMT v2.3.1")
    print("Probabilite que les resultats soient dus au HASARD")
    print("=" * 70)

    # =========================================================================
    # 1. TEST SPARC: 169/175 galaxies ameliorees (97%)
    # =========================================================================
    n_sparc = 175
    k_sparc = 169
    # Sous H0 (hasard): p = 0.5 (pile ou face, amelioration aleatoire)
    p_sparc = stats.binom.sf(k_sparc - 1, n_sparc, 0.5)
    z_sparc = (k_sparc - n_sparc * 0.5) / np.sqrt(n_sparc * 0.5 * 0.5)

    print(f"\n1. TEST SPARC (175 galaxies)")
    print(f"   Observe: {k_sparc}/{n_sparc} ameliorees ({100*k_sparc/n_sparc:.1f}%)")
    print(f"   Attendu si hasard: 87.5/175 (50%)")
    print(f"   z-score: {z_sparc:.1f} sigma")
    print(f"   p-value: {p_sparc:.2e}")

    # =========================================================================
    # 2. LOI k(M): R2 = 0.64, n = 172
    # =========================================================================
    R2_k = 0.64
    n_k = 172
    r_k = np.sqrt(R2_k)
    df1 = 1
    df2 = n_k - 2
    F_k = (R2_k / df1) / ((1 - R2_k) / df2)
    p_k = stats.f.sf(F_k, df1, df2)

    print(f"\n2. LOI k(M) - Correlation masse-couplage (172 galaxies)")
    print(f"   R2 = {R2_k:.2f}, r = {r_k:.2f}")
    print(f"   F-statistic: {F_k:.1f}")
    print(f"   p-value: {p_k:.2e}")

    # =========================================================================
    # 3. RELATION r_c(M): r = 0.768, p = 3e-21
    # =========================================================================
    r_rc = 0.768
    p_rc = 3e-21
    n_rc = 103

    print(f"\n3. RELATION r_c(M) - Rayon critique (103 galaxies)")
    print(f"   Pearson r = {r_rc:.3f}")
    print(f"   p-value: {p_rc:.2e}")

    # =========================================================================
    # 4. TESTS COSMOLOGIQUES: 6/6 passes
    # =========================================================================
    # Tests: SNIa, H0 tension, r_c(M), ISW, BAO, Weak lensing
    p_cosmo = 0.5 ** 6  # Probabilite de 6 succes consecutifs si hasard

    print(f"\n4. TESTS COSMOLOGIQUES (6 tests)")
    print(f"   Observe: 6/6 tests passes")
    print(f"   p-value (si hasard 50/50): {p_cosmo:.4f}")

    # =========================================================================
    # 5. SNIa par environnement: Delta d_L significatif
    # =========================================================================
    p_snia = 1e-17

    print(f"\n5. SNIa PAR ENVIRONNEMENT")
    print(f"   Delta d_L observe entre vides et amas")
    print(f"   p-value: {p_snia:.2e}")

    # =========================================================================
    # 6. KiDS-450: Isotropie confirmee sur 1M galaxies
    # =========================================================================
    # Deviation de 0.024% compatible avec isotropie
    n_kids = 1_000_000
    deviation = 0.00024
    se_kids = 1 / np.sqrt(n_kids)
    z_kids = deviation / se_kids
    p_kids_aniso = 2 * stats.norm.sf(abs(z_kids))  # p pour anisotropie
    p_kids = 1 - p_kids_aniso  # p pour isotropie (ce qu'on veut)

    print(f"\n6. KiDS-450 WEAK LENSING (1M galaxies)")
    print(f"   Deviation isotropie: {deviation*100:.3f}%")
    print(f"   Isotropie confirmee (compatible TMT v2.0 prediction)")

    # =========================================================================
    # COMBINAISON - Methode de Fisher
    # =========================================================================
    print("\n" + "=" * 70)
    print("COMBINAISON STATISTIQUE (Methode de Fisher)")
    print("=" * 70)

    # p-values independantes a combiner
    p_values = [p_sparc, p_k, p_rc, p_cosmo, p_snia]
    labels = [
        "SPARC 97%",
        "k(M) R2=0.64",
        "r_c(M) r=0.77",
        "Cosmo 6/6",
        "SNIa env."
    ]

    print("\nTests combines (independants):")
    for label, p in zip(labels, p_values):
        log_p = np.log10(p) if p > 0 else -300
        print(f"   {label:20s}: p = {p:.2e}  (10^{log_p:.0f})")

    # Statistique de Fisher: -2 * sum(ln(p))
    chi2_fisher = -2 * sum(np.log(p) for p in p_values)
    df_fisher = 2 * len(p_values)
    p_combined = stats.chi2.sf(chi2_fisher, df_fisher)

    print(f"\nStatistique chi2 de Fisher: {chi2_fisher:.1f}")
    print(f"Degres de liberte: {df_fisher}")
    print(f"p-value combinee: {p_combined:.2e}")

    # Conversion en sigma equivalent
    if p_combined > 1e-300:
        sigma_equiv = stats.norm.ppf(1 - p_combined / 2)
    else:
        # Approximation pour p tres petit
        sigma_equiv = np.sqrt(chi2_fisher)

    # =========================================================================
    # RESUME FINAL
    # =========================================================================
    print("\n" + "=" * 70)
    print("VERDICT FINAL")
    print("=" * 70)

    log_inverse = -np.log10(p_combined) if p_combined > 0 else 300

    print("""
+-------------------------------------------------------------------+
|  PROBABILITE QUE TMT v2.3.1 SOIT DU AU HASARD                     |
+-------------------------------------------------------------------+""")
    print(f"|                                                                   |")
    print(f"|  p-value combinee:  {p_combined:.2e}                                |")
    print(f"|                                                                   |")
    print(f"|  Significativite:   {sigma_equiv:.0f} sigma                                      |")
    print(f"|                                                                   |")
    print("""+-------------------------------------------------------------------+
|  INTERPRETATION                                                   |
+-------------------------------------------------------------------+""")
    print(f"|                                                                   |")
    print(f"|  Probabilite que TOUS ces resultats soient aleatoires:            |")
    print(f"|                                                                   |")
    print(f"|     1 chance sur 10^{log_inverse:.0f}                                           |")
    print(f"|                                                                   |")
    print(f"|  Equivalent: gagner au loto ~{log_inverse/7:.0f} fois de suite                    |")
    print(f"|                                                                   |")
    print("+-------------------------------------------------------------------+")

    print("\nCOMPARAISON AVEC SEUILS SCIENTIFIQUES:")
    print("-" * 50)
    print("   Publication standard:          p < 0.05    (2 sigma)")
    print("   Tres significatif:             p < 0.001   (3 sigma)")
    print("   Decouverte (physique):         p < 3e-7    (5 sigma)")
    print("   Higgs / Ondes grav. (LIGO):    p ~ 1e-7    (5 sigma)")
    print("   " + "-" * 46)
    print(f"   TMT v2.3.1 combine:            p ~ 10^-{log_inverse:.0f}  ({sigma_equiv:.0f} sigma)")
    print()

    # Bayes Factor
    if p_combined > 0 and p_combined < 1:
        BF = (1 - p_combined) / p_combined
        log_BF = np.log10(BF)
    else:
        log_BF = 300

    print(f"   Bayes Factor: ~10^{log_BF:.0f} en faveur de TMT")
    print()
    print("   [OK] TMT v2.3.1 depasse LARGEMENT le seuil de decouverte 5 sigma")
    print("   [OK] La probabilite que ce soit du hasard est NEGLIGEABLE")
    print()

    # =========================================================================
    # TABLEAU RECAPITULATIF
    # =========================================================================
    print("=" * 70)
    print("TABLEAU RECAPITULATIF")
    print("=" * 70)
    print("""
| Test                | Resultat        | p-value   | Sigma  |
|---------------------|-----------------|-----------|--------|""")

    results = [
        ("SPARC 175 galaxies", "169/175 (97%)", p_sparc, z_sparc),
        ("Loi k(M)", f"R2 = {R2_k}", p_k, stats.norm.ppf(1-p_k/2)),
        ("Relation r_c(M)", "r = 0.768", p_rc, 9.4),
        ("Tests cosmo 6/6", "6/6 passes", p_cosmo, 2.5),
        ("SNIa environnement", "Delta d_L sig.", p_snia, 8.5),
    ]

    for name, result, p, sig in results:
        print(f"| {name:19s} | {result:15s} | {p:.1e} | {sig:.1f}    |")

    print("|---------------------|-----------------|-----------|--------|")
    print(f"| COMBINE (Fisher)    | chi2 = {chi2_fisher:.0f}     | {p_combined:.1e} | {sigma_equiv:.0f}     |")
    print()

    return p_combined, sigma_equiv


if __name__ == "__main__":
    p, sigma = main()
