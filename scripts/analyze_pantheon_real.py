#!/usr/bin/env python3
"""
Analyse des donnees Pantheon+ reelles par environnement
Test de la prediction TMT v2.0: Delta_d_L = 5-10% (vide vs amas)

Utilise HOST_LOGMASS comme proxy de l'environnement:
- Masse elevee (>10.5) -> environnement dense (amas)
- Masse faible (<9.5) -> environnement peu dense (vide)
"""

import numpy as np
from scipy.integrate import quad
from scipy import stats
import os

# =============================================================================
# PARAMETRES
# =============================================================================
H0 = 70  # km/s/Mpc
Omega_m = 0.315
Omega_Lambda = 0.685
beta = 0.4  # parametre d'ancrage TMT
c = 299792.458  # km/s

# Seuils de classification environnement (log10(M_host/M_sun))
MASS_LOW = 9.5    # Environnement peu dense
MASS_HIGH = 10.5  # Environnement dense

# =============================================================================
# FONCTIONS COSMOLOGIQUES
# =============================================================================

def H_LCDM(z):
    """Fonction de Hubble LCDM standard."""
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def H_TMT(z, rho_ratio):
    """Fonction de Hubble TMT avec expansion differentielle."""
    term_m = Omega_m * (1 + z)**3
    term_L = Omega_Lambda * np.exp(beta * (1 - rho_ratio))
    return H0 * np.sqrt(term_m + term_L)

def d_L_LCDM(z):
    """Distance de luminosite LCDM en Mpc."""
    integrand = lambda zp: c / H_LCDM(zp)
    integral, _ = quad(integrand, 0, z)
    return (1 + z) * integral

def d_L_TMT(z, rho_ratio):
    """Distance de luminosite TMT en Mpc."""
    integrand = lambda zp: c / H_TMT(zp, rho_ratio)
    integral, _ = quad(integrand, 0, z)
    return (1 + z) * integral

def mu_from_d_L(d_L):
    """Module de distance depuis d_L en Mpc."""
    return 5 * np.log10(d_L) + 25

# =============================================================================
# LECTURE DES DONNEES
# =============================================================================

def load_pantheon_data(filepath):
    """Charge les donnees Pantheon+ depuis le fichier."""
    data = {
        'CID': [],
        'zCMB': [],
        'm_b_corr': [],
        'm_b_err': [],
        'HOST_LOGMASS': [],
        'RA': [],
        'DEC': []
    }

    with open(filepath, 'r') as f:
        header = f.readline().strip().split()

        # Trouver les indices des colonnes
        idx_cid = header.index('CID')
        idx_zcmb = header.index('zCMB')
        idx_mb = header.index('m_b_corr')
        idx_mb_err = header.index('m_b_corr_err_DIAG')
        idx_logmass = header.index('HOST_LOGMASS')
        idx_ra = header.index('RA')
        idx_dec = header.index('DEC')

        for line in f:
            parts = line.strip().split()
            if len(parts) < len(header):
                continue

            try:
                logmass = float(parts[idx_logmass])
                # Ignorer les valeurs invalides (-9 signifie pas de donnee)
                if logmass < 0:
                    continue

                data['CID'].append(parts[idx_cid])
                data['zCMB'].append(float(parts[idx_zcmb]))
                data['m_b_corr'].append(float(parts[idx_mb]))
                data['m_b_err'].append(float(parts[idx_mb_err]))
                data['HOST_LOGMASS'].append(logmass)
                data['RA'].append(float(parts[idx_ra]))
                data['DEC'].append(float(parts[idx_dec]))
            except (ValueError, IndexError):
                continue

    # Convertir en arrays numpy
    for key in data:
        if key != 'CID':
            data[key] = np.array(data[key])

    return data

# =============================================================================
# ANALYSE PAR ENVIRONNEMENT
# =============================================================================

def classify_environment(logmass):
    """Classifie l'environnement en fonction de la masse de l'hote."""
    if logmass < MASS_LOW:
        return 'vide'
    elif logmass > MASS_HIGH:
        return 'amas'
    else:
        return 'moyen'

def analyze_by_environment(data, z_bins):
    """Analyse les residus de magnitude par environnement."""
    results = []

    for z_min, z_max in z_bins:
        # Selectionner les SNIa dans le bin de redshift
        mask = (data['zCMB'] >= z_min) & (data['zCMB'] < z_max)

        if np.sum(mask) < 10:
            continue

        z_mean = np.mean(data['zCMB'][mask])

        # Calculer le module de distance LCDM theorique
        mu_lcdm = mu_from_d_L(d_L_LCDM(z_mean))

        # Separer par environnement
        env_mask = {
            'vide': mask & (data['HOST_LOGMASS'] < MASS_LOW),
            'amas': mask & (data['HOST_LOGMASS'] > MASS_HIGH),
            'moyen': mask & (data['HOST_LOGMASS'] >= MASS_LOW) &
                          (data['HOST_LOGMASS'] <= MASS_HIGH)
        }

        result = {
            'z_min': z_min,
            'z_max': z_max,
            'z_mean': z_mean,
            'mu_lcdm': mu_lcdm
        }

        for env, emask in env_mask.items():
            n = np.sum(emask)
            if n > 0:
                m_b = data['m_b_corr'][emask]
                m_err = data['m_b_err'][emask]

                # Module de distance observe = m_b (deja corrige)
                mu_obs = m_b

                # Residu par rapport a LCDM
                residuals = mu_obs - mu_lcdm

                result[f'{env}_n'] = n
                result[f'{env}_mu_mean'] = np.mean(mu_obs)
                result[f'{env}_mu_std'] = np.std(mu_obs)
                result[f'{env}_residual'] = np.mean(residuals)
                result[f'{env}_residual_err'] = np.std(residuals) / np.sqrt(n)
            else:
                result[f'{env}_n'] = 0

        results.append(result)

    return results

def test_TMT_prediction(results):
    """Teste la prediction TMT: Delta_m(vide - amas)."""
    print("\n" + "="*70)
    print("TEST PREDICTION TMT: DIFFERENCE VIDE VS AMAS")
    print("="*70)
    print("\nPrediction TMT: Les SNIa dans les vides devraient apparaitre")
    print("PLUS PROCHES (magnitude plus faible) que dans les amas.")
    print("Delta_mu attendu (amas - vide) = +0.1 a +0.2 mag (5-10% en distance)")
    print()

    significant_count = 0
    total_count = 0
    delta_mu_list = []

    print(f"{'Bin z':<12} {'N_vide':<8} {'N_amas':<8} {'Delta_mu':<12} {'Sigma':<8} {'Verdict'}")
    print("-"*70)

    for r in results:
        if r.get('vide_n', 0) > 5 and r.get('amas_n', 0) > 5:
            total_count += 1

            # Delta_mu = mu(amas) - mu(vide)
            # Positif = amas plus loin (comme predit par TMT)
            delta_mu = r['amas_residual'] - r['vide_residual']

            # Erreur combinee
            err_combined = np.sqrt(r['vide_residual_err']**2 + r['amas_residual_err']**2)
            sigma = delta_mu / err_combined if err_combined > 0 else 0

            delta_mu_list.append(delta_mu)

            verdict = ""
            if sigma > 2:
                verdict = "AMAS > VIDE **"
                significant_count += 1
            elif sigma < -2:
                verdict = "VIDE > AMAS !!"
            else:
                verdict = "non significatif"

            z_label = f"{r['z_min']:.2f}-{r['z_max']:.2f}"
            print(f"{z_label:<12} {r['vide_n']:<8} {r['amas_n']:<8} {delta_mu:+.4f} mag  {sigma:+.2f}   {verdict}")

    print("-"*70)

    if delta_mu_list:
        mean_delta = np.mean(delta_mu_list)
        std_delta = np.std(delta_mu_list)

        print(f"\nDelta_mu moyen (amas - vide): {mean_delta:+.4f} +/- {std_delta:.4f} mag")

        # Test t pour voir si significativement different de 0
        if len(delta_mu_list) > 1:
            t_stat, p_value = stats.ttest_1samp(delta_mu_list, 0)
            print(f"Test t: t = {t_stat:.2f}, p = {p_value:.4e}")

        # Conversion en difference de distance
        delta_dL_percent = 100 * (10**(mean_delta/5) - 1)
        print(f"=> Difference en distance: {delta_dL_percent:+.1f}%")

        print(f"\nBins significatifs (>2 sigma): {significant_count}/{total_count}")

        # Verdict
        print("\n" + "="*70)
        print("VERDICT:")
        if mean_delta > 0.05 and significant_count >= total_count/2:
            print("  => TMT SUPPORTE: Les SNIa dans amas sont systematiquement")
            print("     plus lointains que dans les vides")
            return "SUPPORTE"
        elif mean_delta < -0.05:
            print("  => TMT REFUTE: Tendance opposee observee")
            return "REFUTE"
        else:
            print("  => INCONCLUSIF: Pas de difference significative detectee")
            return "INCONCLUSIF"

    return "DONNEES_INSUFFISANTES"

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("ANALYSE PANTHEON+ PAR ENVIRONNEMENT - TEST TMT v2.0")
    print("="*70)

    # Chemin des donnees
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "Pantheon+", "Pantheon+SH0ES.dat")

    print(f"\nChargement des donnees: {data_path}")
    data = load_pantheon_data(data_path)

    n_total = len(data['CID'])
    print(f"SNIa chargees: {n_total}")
    print(f"SNIa avec HOST_LOGMASS valide: {len(data['zCMB'])}")

    # Distribution des environnements
    n_vide = np.sum(data['HOST_LOGMASS'] < MASS_LOW)
    n_amas = np.sum(data['HOST_LOGMASS'] > MASS_HIGH)
    n_moyen = np.sum((data['HOST_LOGMASS'] >= MASS_LOW) & (data['HOST_LOGMASS'] <= MASS_HIGH))

    print(f"\nDistribution des environnements:")
    print(f"  Vides (log M < {MASS_LOW}): {n_vide}")
    print(f"  Moyen ({MASS_LOW} <= log M <= {MASS_HIGH}): {n_moyen}")
    print(f"  Amas (log M > {MASS_HIGH}): {n_amas}")

    # Distribution en redshift
    print(f"\nDistribution en redshift:")
    print(f"  z min: {np.min(data['zCMB']):.4f}")
    print(f"  z max: {np.max(data['zCMB']):.4f}")
    print(f"  z median: {np.median(data['zCMB']):.4f}")

    # Definir les bins de redshift
    z_bins = [
        (0.01, 0.03),   # Tres local
        (0.03, 0.05),   # Local
        (0.05, 0.10),   # Proche
        (0.10, 0.20),   # Intermediaire
        (0.20, 0.40),   # Lointain
        (0.40, 0.70),   # Tres lointain
        (0.70, 1.00),   # Extreme
        (1.00, 2.30),   # Ultra-lointain
    ]

    # Analyse par environnement
    print("\n" + "="*70)
    print("ANALYSE PAR BIN DE REDSHIFT ET ENVIRONNEMENT")
    print("="*70)

    results = analyze_by_environment(data, z_bins)

    print(f"\n{'Bin z':<12} {'z_mean':<8} {'N_vide':<8} {'N_moyen':<8} {'N_amas':<8}")
    print("-"*60)
    for r in results:
        z_label = f"{r['z_min']:.2f}-{r['z_max']:.2f}"
        n_vide = r.get('vide_n', 0)
        n_moyen = r.get('moyen_n', 0)
        n_amas = r.get('amas_n', 0)
        print(f"{z_label:<12} {r['z_mean']:.4f}   {n_vide:<8} {n_moyen:<8} {n_amas:<8}")

    # Test de la prediction TMT
    verdict = test_TMT_prediction(results)

    # Comparaison avec prediction theorique TMT
    print("\n" + "="*70)
    print("COMPARAISON AVEC PREDICTION THEORIQUE TMT")
    print("="*70)

    print("\nPrediction TMT v2.0 pour z = 0.5:")

    # Calcul theorique
    z_test = 0.5
    rho_vide = 0.3    # Vide: 30% de la densite critique
    rho_amas = 5.0    # Amas: 5x la densite critique

    d_L_void = d_L_TMT(z_test, rho_vide)
    d_L_cluster = d_L_TMT(z_test, rho_amas)
    d_L_lcdm = d_L_LCDM(z_test)

    mu_void = mu_from_d_L(d_L_void)
    mu_cluster = mu_from_d_L(d_L_cluster)
    mu_lcdm_val = mu_from_d_L(d_L_lcdm)

    delta_mu_pred = mu_cluster - mu_void
    delta_dL_pred = 100 * (d_L_cluster - d_L_void) / d_L_void

    print(f"  d_L(vide):  {d_L_void:.1f} Mpc  (mu = {mu_void:.2f})")
    print(f"  d_L(amas):  {d_L_cluster:.1f} Mpc  (mu = {mu_cluster:.2f})")
    print(f"  d_L(LCDM):  {d_L_lcdm:.1f} Mpc  (mu = {mu_lcdm_val:.2f})")
    print(f"\n  Delta_mu theorique (amas - vide): {delta_mu_pred:+.4f} mag")
    print(f"  Delta_dL theorique: {delta_dL_pred:+.1f}%")

    # Sauvegarder les resultats
    results_dir = os.path.join(script_dir, "..", "data", "results")
    os.makedirs(results_dir, exist_ok=True)
    results_path = os.path.join(results_dir, "pantheon_environment_analysis.txt")

    with open(results_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("ANALYSE PANTHEON+ PAR ENVIRONNEMENT - RESULTATS\n")
        f.write("="*70 + "\n\n")
        f.write(f"SNIa analysees: {len(data['zCMB'])}\n")
        f.write(f"Vides (log M < {MASS_LOW}): {n_vide}\n")
        f.write(f"Amas (log M > {MASS_HIGH}): {n_amas}\n\n")
        f.write(f"Verdict: {verdict}\n")

    print(f"\nResultats sauvegardes: {results_path}")
    print("\n" + "="*70)
    print(f"VERDICT FINAL: {verdict}")
    print("="*70)
