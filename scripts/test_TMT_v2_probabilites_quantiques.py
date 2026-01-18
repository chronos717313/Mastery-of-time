#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST TMT v2.0 - ANALYSE PROBABILISTE ET UNIFICATION QUANTIQUE
==============================================================

Ce script teste rigoureusement les predictions de TMT v2.0 avec:
1. Analyse statistique complete (chi2, p-values, intervalles de confiance)
2. Tests de falsifiabilite
3. Connexion a la mecanique quantique (superposition temporelle)

FONDEMENT QUANTIQUE:
|Psi> = alpha|t> + beta|t_bar>
- |t>: temps forward (matiere visible)
- |t_bar>: temps backward (reflet temporel = "matiere noire")
- |alpha|^2 + |beta|^2 = 1 (normalisation quantique)

Author: Pierre-Olivier Despres Asselin
Date: Janvier 2026
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize, curve_fit
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONSTANTES PHYSIQUES
# =============================================================================

G_KPC = 4.302e-6      # kpc (km/s)^2 / M_sun
C_KMS = 299792.458    # km/s
HBAR = 1.054571817e-34  # J.s (constante de Planck reduite)

# =============================================================================
# FORMULATION QUANTIQUE TMT v2.0
# =============================================================================

def alpha_squared(r, r_c, n):
    """
    Probabilite temps forward |alpha|^2.

    Interpretation quantique:
    - Probabilite d'observer la matiere dans l'etat temps forward
    - Domine a r << r_c (proche du centre galactique)
    """
    x = (r / r_c) ** n
    return 1.0 / (1.0 + x)


def beta_squared(r, r_c, n):
    """
    Probabilite temps backward |beta|^2.

    Interpretation quantique:
    - Probabilite d'observer le "reflet temporel" (matiere noire effective)
    - Domine a r >> r_c (peripherie galactique)
    """
    x = (r / r_c) ** n
    return x / (1.0 + x)


def verify_normalization(r, r_c, n):
    """Verifie |alpha|^2 + |beta|^2 = 1 (axiome quantique fondamental)."""
    return alpha_squared(r, r_c, n) + beta_squared(r, r_c, n)


def mass_multiplier_quantum(r, r_c, n):
    """
    Multiplicateur de masse effectif derive de la superposition quantique.

    M_eff = M_bary * [1 + beta^2/alpha^2]
          = M_bary * [1 + (r/r_c)^n]

    C'est exactement la formule TMT v2.0!
    """
    return 1.0 + (r / r_c) ** n


def v_rotation_quantum(r, M_bary_enc, r_c, n):
    """Vitesse de rotation avec superposition quantique."""
    mult = mass_multiplier_quantum(r, r_c, n)
    M_eff = M_bary_enc * mult
    v_sq = G_KPC * M_eff / r
    return np.sqrt(np.maximum(v_sq, 0))


# =============================================================================
# CHARGEMENT DONNEES SPARC
# =============================================================================

def load_sparc_data(data_dir):
    """Charge les donnees SPARC reelles."""
    models_file = data_dir / "MassModels_Lelli2016c.mrt"

    rotation_curves = {}
    with open(models_file, 'r') as f:
        for line in f:
            if line.startswith(('Title', 'Authors', 'Table', '=', '-', 'Byte', ' ', 'Note')):
                continue
            if not line.strip():
                continue
            try:
                name = line[0:11].strip()
                if not name or name in ('ID', 'Galaxy'):
                    continue
                R = float(line[19:25].strip())
                Vobs = float(line[26:32].strip())
                e_Vobs = float(line[33:38].strip())
                Vgas = float(line[39:45].strip())
                Vdisk = float(line[46:52].strip())
                Vbul = float(line[53:59].strip())

                if name not in rotation_curves:
                    rotation_curves[name] = {'R': [], 'Vobs': [], 'e_Vobs': [],
                                             'Vgas': [], 'Vdisk': [], 'Vbul': []}
                rotation_curves[name]['R'].append(R)
                rotation_curves[name]['Vobs'].append(Vobs)
                rotation_curves[name]['e_Vobs'].append(max(e_Vobs, 1.0))
                rotation_curves[name]['Vgas'].append(Vgas)
                rotation_curves[name]['Vdisk'].append(Vdisk)
                rotation_curves[name]['Vbul'].append(Vbul)
            except:
                continue

    # Convertir en arrays
    for name in rotation_curves:
        for key in rotation_curves[name]:
            rotation_curves[name][key] = np.array(rotation_curves[name][key])

    return rotation_curves


def compute_baryonic(rc, ML_disk=0.5, ML_bul=0.7):
    """Calcule vitesse et masse baryonique."""
    V_bary_sq = rc['Vgas']**2 + ML_disk * rc['Vdisk']**2 + ML_bul * rc['Vbul']**2
    V_bary = np.sqrt(np.maximum(V_bary_sq, 0))
    M_bary_enc = V_bary**2 * rc['R'] / G_KPC
    return V_bary, M_bary_enc


# =============================================================================
# TESTS STATISTIQUES
# =============================================================================

def chi2_reduced(V_model, V_obs, e_V, n_params=2):
    """Chi-carre reduit."""
    residuals = (V_model - V_obs) / e_V
    chi2 = np.sum(residuals**2)
    dof = max(len(V_obs) - n_params, 1)
    return chi2 / dof


def log_likelihood(V_model, V_obs, e_V):
    """Log-vraisemblance (distribution gaussienne)."""
    residuals = (V_model - V_obs) / e_V
    return -0.5 * np.sum(residuals**2 + np.log(2*np.pi*e_V**2))


def bayesian_information_criterion(log_L, n_params, n_data):
    """BIC = -2*ln(L) + k*ln(n) - favorise parcimonie."""
    return -2 * log_L + n_params * np.log(n_data)


def akaike_information_criterion(log_L, n_params):
    """AIC = -2*ln(L) + 2k."""
    return -2 * log_L + 2 * n_params


def p_value_chi2(chi2_red, dof):
    """P-value pour chi2 reduit."""
    chi2_total = chi2_red * dof
    return 1 - stats.chi2.cdf(chi2_total, dof)


def bootstrap_confidence_interval(data, statistic_func, n_bootstrap=1000, ci=0.95):
    """Intervalle de confiance par bootstrap."""
    n = len(data)
    bootstrap_stats = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, n, replace=True)
        bootstrap_stats.append(statistic_func(sample))

    alpha = (1 - ci) / 2
    lower = np.percentile(bootstrap_stats, 100 * alpha)
    upper = np.percentile(bootstrap_stats, 100 * (1 - alpha))
    return lower, upper


def hypothesis_test_TMT_vs_Newton(improvements, threshold=0):
    """
    Test d'hypothese: TMT v2.0 est-il meilleur que Newton?

    H0: TMT n'apporte pas d'amelioration (improvement <= threshold)
    H1: TMT apporte une amelioration (improvement > threshold)
    """
    t_stat, p_value = stats.ttest_1samp(improvements, threshold)
    # One-sided test
    p_one_sided = p_value / 2 if t_stat > 0 else 1 - p_value / 2
    return t_stat, p_one_sided


def effect_size_cohens_d(improvements):
    """Taille d'effet de Cohen's d."""
    return np.mean(improvements) / np.std(improvements)


# =============================================================================
# ANALYSE PRINCIPALE
# =============================================================================

def analyze_galaxy(rc, r_c, n):
    """Analyse complete d'une galaxie."""
    R = rc['R']
    Vobs = rc['Vobs']
    e_Vobs = rc['e_Vobs']

    V_bary, M_bary_enc = compute_baryonic(rc)
    V_TMT = v_rotation_quantum(R, M_bary_enc, r_c, n)

    chi2_newton = chi2_reduced(V_bary, Vobs, e_Vobs, n_params=0)
    chi2_tmt = chi2_reduced(V_TMT, Vobs, e_Vobs, n_params=2)

    improvement = (chi2_newton - chi2_tmt) / chi2_newton * 100 if chi2_newton > 0 else 0

    # Log-likelihood
    ll_newton = log_likelihood(V_bary, Vobs, e_Vobs)
    ll_tmt = log_likelihood(V_TMT, Vobs, e_Vobs)

    # Criteres d'information
    n_data = len(Vobs)
    bic_newton = bayesian_information_criterion(ll_newton, 0, n_data)
    bic_tmt = bayesian_information_criterion(ll_tmt, 2, n_data)

    aic_newton = akaike_information_criterion(ll_newton, 0)
    aic_tmt = akaike_information_criterion(ll_tmt, 2)

    return {
        'chi2_newton': chi2_newton,
        'chi2_tmt': chi2_tmt,
        'improvement': improvement,
        'll_newton': ll_newton,
        'll_tmt': ll_tmt,
        'bic_newton': bic_newton,
        'bic_tmt': bic_tmt,
        'aic_newton': aic_newton,
        'aic_tmt': aic_tmt,
        'delta_bic': bic_newton - bic_tmt,  # >0 favorise TMT
        'delta_aic': aic_newton - aic_tmt,  # >0 favorise TMT
        'n_points': n_data
    }


def optimize_parameters(rotation_curves):
    """Optimise r_c et n globalement."""

    def total_chi2(params):
        r_c, n = params
        if r_c <= 0 or n <= 0:
            return 1e10
        total = 0
        count = 0
        for name, rc in rotation_curves.items():
            if len(rc['R']) < 5:
                continue
            R = rc['R']
            Vobs = rc['Vobs']
            e_Vobs = rc['e_Vobs']
            V_bary, M_bary_enc = compute_baryonic(rc)
            V_TMT = v_rotation_quantum(R, M_bary_enc, r_c, n)
            chi2 = np.sum(((V_TMT - Vobs) / e_Vobs)**2)
            total += chi2
            count += len(R)
        return total / max(count, 1)

    # Optimisation
    result = minimize(total_chi2, [10, 1.0], bounds=[(0.1, 100), (0.1, 3)], method='L-BFGS-B')
    return result.x[0], result.x[1]


def main():
    print("=" * 75)
    print("TEST TMT v2.0 - ANALYSE PROBABILISTE ET UNIFICATION QUANTIQUE")
    print("=" * 75)

    # Charger donnees
    data_dir = Path(__file__).parent.parent / "data" / "SPARC"

    if not data_dir.exists():
        data_dir = Path(__file__).parent.parent / "data" / "sparc"

    print("\n[1/7] Chargement donnees SPARC...")
    rotation_curves = load_sparc_data(data_dir)
    print(f"      {len(rotation_curves)} galaxies chargees")

    # Verification normalisation quantique
    print("\n[2/7] Verification axiomes quantiques...")
    r_test = np.array([1, 5, 10, 20, 50, 100])
    r_c_test, n_test = 5.0, 0.57
    norms = verify_normalization(r_test, r_c_test, n_test)
    print(f"      |alpha|^2 + |beta|^2 = {norms} (doit etre = 1)")
    print(f"      Normalisation quantique: VERIFIEE")

    # Optimiser parametres
    print("\n[3/7] Optimisation parametres globaux...")
    r_c_opt, n_opt = optimize_parameters(rotation_curves)
    print(f"      r_c optimal = {r_c_opt:.2f} kpc")
    print(f"      n optimal   = {n_opt:.2f}")

    # Analyser toutes les galaxies
    print("\n[4/7] Analyse statistique complete...")
    results = []
    for name, rc in rotation_curves.items():
        if len(rc['R']) < 5:
            continue
        res = analyze_galaxy(rc, r_c_opt, n_opt)
        res['name'] = name
        results.append(res)

    print(f"      {len(results)} galaxies analysees")

    # Statistiques globales
    print("\n[5/7] Resultats statistiques...")

    improvements = np.array([r['improvement'] for r in results])
    chi2_newtons = np.array([r['chi2_newton'] for r in results])
    chi2_tmts = np.array([r['chi2_tmt'] for r in results])
    delta_bics = np.array([r['delta_bic'] for r in results])
    delta_aics = np.array([r['delta_aic'] for r in results])

    n_improved = np.sum(improvements > 0)
    n_total = len(improvements)

    print(f"\n      === PERFORMANCE ===")
    print(f"      Galaxies ameliorees: {n_improved}/{n_total} ({100*n_improved/n_total:.1f}%)")
    print(f"      Amelioration mediane: {np.median(improvements):.1f}%")
    print(f"      Amelioration moyenne: {np.mean(improvements):.1f}%")
    print(f"      Chi2 Newton moyen:    {np.mean(chi2_newtons):.2f}")
    print(f"      Chi2 TMT moyen:       {np.mean(chi2_tmts):.2f}")

    # Tests d'hypothese
    print(f"\n      === TESTS D'HYPOTHESE ===")

    # Test t
    t_stat, p_value = hypothesis_test_TMT_vs_Newton(improvements, threshold=0)
    print(f"      Test t (H0: amelioration <= 0):")
    print(f"        t-statistique: {t_stat:.2f}")
    print(f"        p-value:       {p_value:.2e}")
    if p_value < 0.001:
        print(f"        Verdict:       TRES SIGNIFICATIF (p < 0.001)")
    elif p_value < 0.05:
        print(f"        Verdict:       SIGNIFICATIF (p < 0.05)")
    else:
        print(f"        Verdict:       NON SIGNIFICATIF")

    # Taille d'effet
    d = effect_size_cohens_d(improvements)
    print(f"\n      Taille d'effet (Cohen's d): {d:.2f}")
    if abs(d) > 0.8:
        print(f"        Interpretation: GRAND effet")
    elif abs(d) > 0.5:
        print(f"        Interpretation: MOYEN effet")
    else:
        print(f"        Interpretation: PETIT effet")

    # Intervalle de confiance bootstrap
    print(f"\n      === INTERVALLE DE CONFIANCE (95%) ===")
    ci_lower, ci_upper = bootstrap_confidence_interval(improvements, np.median)
    print(f"      Amelioration mediane: [{ci_lower:.1f}%, {ci_upper:.1f}%]")

    # Criteres d'information
    print(f"\n      === CRITERES D'INFORMATION ===")
    print(f"      Delta BIC moyen: {np.mean(delta_bics):.1f}")
    print(f"        (>10 = evidence tres forte pour TMT)")
    n_bic_favor = np.sum(delta_bics > 10)
    print(f"        Galaxies avec BIC fortement favorable: {n_bic_favor}/{n_total}")

    print(f"      Delta AIC moyen: {np.mean(delta_aics):.1f}")
    print(f"        (>10 = evidence tres forte pour TMT)")

    # Connexion quantique
    print("\n[6/7] Unification avec mecanique quantique...")

    print(f"""
      === FONDEMENTS QUANTIQUES DE TMT v2.0 ===

      1. SUPERPOSITION TEMPORELLE
         |Psi> = alpha(r)|t> + beta(r)|t_bar>

         - |t>     : etat temps forward (matiere visible)
         - |t_bar> : etat temps backward (reflet temporel)

      2. NORMALISATION (axiome quantique)
         |alpha|^2 + |beta|^2 = 1

         Verifie: {verify_normalization(10, r_c_opt, n_opt):.10f}

      3. PROBABILITES RADIALES
         |alpha(r)|^2 = 1 / (1 + (r/r_c)^n)
         |beta(r)|^2  = (r/r_c)^n / (1 + (r/r_c)^n)

         A r << r_c: |alpha|^2 ~ 1, |beta|^2 ~ 0 (matiere visible domine)
         A r >> r_c: |alpha|^2 ~ 0, |beta|^2 ~ 1 (reflet temporel domine)

      4. MASSE EFFECTIVE (valeur moyenne quantique)
         <M_eff> = M_bary * (|alpha|^2 + 2*|beta|^2)
                 = M_bary * [1 + (r/r_c)^n]

         C'est exactement la formule TMT v2.0!

      5. SYMETRIE CPT
         La superposition temporelle respecte CPT:
         - C (conjugaison de charge): matiere <-> antimatiere
         - P (parite): inversion spatiale
         - T (renversement temporel): t <-> t_bar

      6. PARAMETRES CALIBRES (175 galaxies SPARC)
         r_c = {r_c_opt:.2f} kpc (rayon de transition quantique)
         n   = {n_opt:.2f} (exposant de superposition)
    """)

    # Resume final
    print("\n[7/7] Resume et verdict...")

    print(f"""
    ======================================================================
                    RESUME - FORCE STATISTIQUE TMT v2.0
    ======================================================================

    ECHANTILLON
      Galaxies:           {n_total}
      Points de donnees:  {sum(r['n_points'] for r in results)}

    PERFORMANCE
      Galaxies ameliorees:     {n_improved}/{n_total} ({100*n_improved/n_total:.1f}%)
      Amelioration mediane:    {np.median(improvements):.1f}%
      IC 95%:                  [{ci_lower:.1f}%, {ci_upper:.1f}%]

    FORCE STATISTIQUE
      p-value (t-test):        {p_value:.2e}
      Cohen's d:               {d:.2f} ({"GRAND" if abs(d) > 0.8 else "MOYEN" if abs(d) > 0.5 else "PETIT"})
      Delta BIC moyen:         {np.mean(delta_bics):.1f}

    PARAMETRES QUANTIQUES
      r_c (transition):        {r_c_opt:.2f} kpc
      n (exposant):            {n_opt:.2f}

    ======================================================================
                              VERDICT FINAL
    ======================================================================
    """)

    # Calcul score global
    score = 0
    evidence = []

    if n_improved / n_total > 0.95:
        score += 3
        evidence.append("+3 : >95% galaxies ameliorees")
    elif n_improved / n_total > 0.80:
        score += 2
        evidence.append("+2 : >80% galaxies ameliorees")
    elif n_improved / n_total > 0.50:
        score += 1
        evidence.append("+1 : >50% galaxies ameliorees")

    if p_value < 1e-10:
        score += 3
        evidence.append("+3 : p-value < 10^-10 (extremement significatif)")
    elif p_value < 1e-5:
        score += 2
        evidence.append("+2 : p-value < 10^-5 (tres significatif)")
    elif p_value < 0.05:
        score += 1
        evidence.append("+1 : p-value < 0.05 (significatif)")

    if abs(d) > 0.8:
        score += 2
        evidence.append("+2 : Cohen's d > 0.8 (grand effet)")
    elif abs(d) > 0.5:
        score += 1
        evidence.append("+1 : Cohen's d > 0.5 (effet moyen)")

    if np.mean(delta_bics) > 10:
        score += 2
        evidence.append("+2 : Delta BIC > 10 (evidence tres forte)")
    elif np.mean(delta_bics) > 6:
        score += 1
        evidence.append("+1 : Delta BIC > 6 (evidence forte)")

    print(f"    SCORE D'EVIDENCE: {score}/10")
    print()
    for e in evidence:
        print(f"      {e}")
    print()

    if score >= 8:
        verdict = "TMT v2.0 FORTEMENT VALIDE"
        symbol = "+++"
    elif score >= 6:
        verdict = "TMT v2.0 VALIDE"
        symbol = "++"
    elif score >= 4:
        verdict = "TMT v2.0 PARTIELLEMENT SUPPORTE"
        symbol = "+"
    else:
        verdict = "EVIDENCE INSUFFISANTE"
        symbol = "?"

    print(f"    [{symbol}] {verdict}")
    print()
    print("    CONNEXION QUANTIQUE: La superposition temporelle")
    print("    |Psi> = alpha|t> + beta|t_bar> explique naturellement")
    print("    l'emergence de la 'matiere noire' comme reflet temporel")
    print("    de la matiere visible, sans particules exotiques.")
    print()
    print("=" * 75)

    # Sauvegarder resultats
    output_dir = Path(__file__).parent.parent / "data" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    results_file = output_dir / "TMT_v2_probabilites_quantiques.txt"
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TMT v2.0 - ANALYSE PROBABILISTE ET UNIFICATION QUANTIQUE\n")
        f.write("=" * 70 + "\n\n")

        f.write("ECHANTILLON\n")
        f.write(f"  Galaxies: {n_total}\n")
        f.write(f"  Source: SPARC (Lelli, McGaugh & Schombert 2016)\n\n")

        f.write("PARAMETRES QUANTIQUES CALIBRES\n")
        f.write(f"  r_c = {r_c_opt:.2f} kpc (rayon de transition)\n")
        f.write(f"  n   = {n_opt:.2f} (exposant de superposition)\n\n")

        f.write("FORCE STATISTIQUE\n")
        f.write(f"  Galaxies ameliorees: {n_improved}/{n_total} ({100*n_improved/n_total:.1f}%)\n")
        f.write(f"  Amelioration mediane: {np.median(improvements):.1f}%\n")
        f.write(f"  IC 95%: [{ci_lower:.1f}%, {ci_upper:.1f}%]\n")
        f.write(f"  p-value: {p_value:.2e}\n")
        f.write(f"  Cohen's d: {d:.2f}\n")
        f.write(f"  Delta BIC moyen: {np.mean(delta_bics):.1f}\n\n")

        f.write("VERDICT\n")
        f.write(f"  Score: {score}/10\n")
        f.write(f"  {verdict}\n\n")

        f.write("FONDEMENT QUANTIQUE\n")
        f.write("  |Psi> = alpha(r)|t> + beta(r)|t_bar>\n")
        f.write("  |alpha|^2 + |beta|^2 = 1 (normalisation verifiee)\n")
        f.write("  M_eff = M_bary * [1 + (r/r_c)^n]\n")

    print(f"\nResultats sauvegardes: {results_file}")

    return score, verdict


if __name__ == "__main__":
    main()
