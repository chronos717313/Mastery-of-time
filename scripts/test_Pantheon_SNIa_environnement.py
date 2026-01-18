#!/usr/bin/env python3
"""
TEST PANTHEON+ SNIa PAR ENVIRONNEMENT - TMT v2.3.1
==================================================

Test de l'expansion differentielle H(z, rho) predite par TMT.

Prediction TMT:
- Environnements peu denses (vides) -> expansion plus rapide -> SNIa apparaissent plus lointaines
- Environnements denses (amas) -> expansion plus lente -> SNIa apparaissent plus proches

Prediction LCDM:
- Pas de difference systematique entre environnements

Proxy pour la densite: HOST_LOGMASS (masse stellaire de la galaxie hote)
- Masse faible -> environnement peu dense (void-like)
- Masse elevee -> environnement dense (cluster-like)

Auteur: Pierre-Olivier Despres Asselin
Date: 18 janvier 2026
"""

import numpy as np
from scipy import stats
import os
from datetime import datetime

# Configuration
DATA_FILE = "data/Pantheon+/Pantheon+SH0ES.dat"
OUTPUT_FILE = "data/results/test_Pantheon_environnement_TMT_v231.txt"

# Seuils pour classification environnement (log M_stellar en M_sun)
MASS_LOW = 9.5    # Galaxies peu massives -> environnement peu dense
MASS_HIGH = 10.5  # Galaxies massives -> environnement dense

def load_pantheon_data(filepath):
    """Charge les donnees Pantheon+ depuis le fichier .dat"""
    print(f"Chargement de {filepath}...")

    data = {
        'CID': [],
        'zCMB': [],
        'zCMB_err': [],
        'mu': [],
        'mu_err': [],
        'host_logmass': [],
        'host_logmass_err': []
    }

    with open(filepath, 'r') as f:
        header = f.readline().strip().split()

        # Trouver les indices des colonnes
        try:
            idx_cid = header.index('CID')
            idx_zcmb = header.index('zCMB')
            idx_zcmb_err = header.index('zCMBERR')
            idx_mu = header.index('MU_SH0ES')
            idx_mu_err = header.index('MU_SH0ES_ERR_DIAG')
            idx_mass = header.index('HOST_LOGMASS')
            idx_mass_err = header.index('HOST_LOGMASS_ERR')
        except ValueError as e:
            print(f"Erreur: colonne manquante - {e}")
            return None

        for line in f:
            parts = line.strip().split()
            if len(parts) < max(idx_cid, idx_zcmb, idx_mu, idx_mass) + 1:
                continue

            try:
                zcmb = float(parts[idx_zcmb])
                mu = float(parts[idx_mu])
                mass = float(parts[idx_mass])

                # Filtrer les valeurs invalides
                if zcmb <= 0 or mu <= 0 or mass < 0 or mass == -9:
                    continue

                data['CID'].append(parts[idx_cid])
                data['zCMB'].append(zcmb)
                data['zCMB_err'].append(float(parts[idx_zcmb_err]))
                data['mu'].append(mu)
                data['mu_err'].append(float(parts[idx_mu_err]))
                data['host_logmass'].append(mass)
                data['host_logmass_err'].append(float(parts[idx_mass_err]) if parts[idx_mass_err] != '-9' else 0.1)

            except (ValueError, IndexError):
                continue

    # Convertir en arrays numpy
    for key in data:
        if key != 'CID':
            data[key] = np.array(data[key])

    print(f"  SNIa chargees: {len(data['zCMB'])}")
    return data

def calculate_expected_mu_lcdm(z, H0=70.0, Om=0.3):
    """Calcule le module de distance attendu pour LCDM"""
    c = 299792.458  # km/s

    # Integration numerique simple pour d_L
    n_steps = 1000
    z_arr = np.linspace(0, z, n_steps)
    dz = z / n_steps

    # E(z) = sqrt(Om*(1+z)^3 + (1-Om))
    E_z = np.sqrt(Om * (1 + z_arr)**3 + (1 - Om))

    # Integrale de 1/E(z)
    try:
        integral = np.trapezoid(1/E_z, z_arr)  # numpy >= 2.0
    except AttributeError:
        integral = np.trapz(1/E_z, z_arr)  # numpy < 2.0

    # Distance de luminosite (Mpc)
    d_L = (c / H0) * (1 + z) * integral

    # Module de distance
    mu = 5 * np.log10(d_L) + 25

    return mu

def analyze_by_environment(data, output):
    """Analyse les residus de distance par environnement"""

    z = data['zCMB']
    mu_obs = data['mu']
    mu_err = data['mu_err']
    mass = data['host_logmass']

    # Calculer mu attendu LCDM pour chaque SNIa
    print("\nCalcul des modules de distance LCDM attendus...")
    mu_lcdm = np.array([calculate_expected_mu_lcdm(zi) for zi in z])

    # Residus = mu_obs - mu_lcdm
    residuals = mu_obs - mu_lcdm

    # Classification par environnement
    mask_low = mass < MASS_LOW
    mask_high = mass > MASS_HIGH
    mask_mid = (mass >= MASS_LOW) & (mass <= MASS_HIGH)

    n_low = np.sum(mask_low)
    n_high = np.sum(mask_high)
    n_mid = np.sum(mask_mid)

    output.write("\n" + "="*70 + "\n")
    output.write("CLASSIFICATION PAR ENVIRONNEMENT\n")
    output.write("="*70 + "\n\n")
    output.write(f"Seuil bas (void-like):    log M < {MASS_LOW}\n")
    output.write(f"Seuil haut (cluster-like): log M > {MASS_HIGH}\n\n")
    output.write(f"SNIa en environnement peu dense (vides):  {n_low}\n")
    output.write(f"SNIa en environnement dense (amas):       {n_high}\n")
    output.write(f"SNIa en environnement intermediaire:      {n_mid}\n")
    output.write(f"Total:                                    {len(z)}\n")

    print(f"\nClassification:")
    print(f"  Vides (log M < {MASS_LOW}): {n_low}")
    print(f"  Amas (log M > {MASS_HIGH}): {n_high}")
    print(f"  Intermediaire: {n_mid}")

    if n_low < 10 or n_high < 10:
        output.write("\n*** ATTENTION: Echantillons trop petits pour analyse robuste ***\n")
        print("\n*** ATTENTION: Echantillons trop petits ***")

    # Statistiques des residus par environnement
    res_low = residuals[mask_low]
    res_high = residuals[mask_high]
    res_mid = residuals[mask_mid]

    output.write("\n" + "="*70 + "\n")
    output.write("RESIDUS DE DISTANCE PAR ENVIRONNEMENT\n")
    output.write("="*70 + "\n\n")

    output.write("Environnement peu dense (vides):\n")
    output.write(f"  N = {n_low}\n")
    output.write(f"  Residu moyen: {np.mean(res_low):.4f} mag\n")
    output.write(f"  Ecart-type:   {np.std(res_low):.4f} mag\n")
    output.write(f"  Erreur std:   {np.std(res_low)/np.sqrt(n_low):.4f} mag\n\n")

    output.write("Environnement dense (amas):\n")
    output.write(f"  N = {n_high}\n")
    output.write(f"  Residu moyen: {np.mean(res_high):.4f} mag\n")
    output.write(f"  Ecart-type:   {np.std(res_high):.4f} mag\n")
    output.write(f"  Erreur std:   {np.std(res_high)/np.sqrt(n_high):.4f} mag\n\n")

    # Difference entre environnements
    delta_mu = np.mean(res_low) - np.mean(res_high)
    delta_err = np.sqrt(np.std(res_low)**2/n_low + np.std(res_high)**2/n_high)

    output.write("="*70 + "\n")
    output.write("DIFFERENCE VIDES - AMAS\n")
    output.write("="*70 + "\n\n")
    output.write(f"Delta mu (vides - amas): {delta_mu:.4f} +/- {delta_err:.4f} mag\n")
    output.write(f"Significance:            {abs(delta_mu)/delta_err:.2f} sigma\n\n")

    # Conversion en pourcentage de distance
    # delta_mu = 5 * log10(d_L_void / d_L_cluster)
    # donc d_L_void / d_L_cluster = 10^(delta_mu/5)
    ratio = 10**(delta_mu / 5)
    delta_percent = (ratio - 1) * 100

    output.write(f"Ratio distance (vides/amas): {ratio:.4f}\n")
    output.write(f"Difference en distance:      {delta_percent:+.2f}%\n\n")

    print(f"\nResultats:")
    print(f"  Delta mu (vides - amas): {delta_mu:.4f} +/- {delta_err:.4f} mag")
    print(f"  Significance: {abs(delta_mu)/delta_err:.2f} sigma")
    print(f"  Difference distance: {delta_percent:+.2f}%")

    return delta_mu, delta_err, delta_percent, n_low, n_high

def statistical_tests(data, output):
    """Tests statistiques detailles"""

    z = data['zCMB']
    mu_obs = data['mu']
    mass = data['host_logmass']

    # Calculer residus
    mu_lcdm = np.array([calculate_expected_mu_lcdm(zi) for zi in z])
    residuals = mu_obs - mu_lcdm

    mask_low = mass < MASS_LOW
    mask_high = mass > MASS_HIGH

    res_low = residuals[mask_low]
    res_high = residuals[mask_high]

    output.write("\n" + "="*70 + "\n")
    output.write("TESTS STATISTIQUES\n")
    output.write("="*70 + "\n\n")

    # Test t de Welch (variances inegales)
    t_stat, p_value_t = stats.ttest_ind(res_low, res_high, equal_var=False)
    output.write("Test t de Welch (variances inegales):\n")
    output.write(f"  t-statistic: {t_stat:.4f}\n")
    output.write(f"  p-value:     {p_value_t:.2e}\n\n")

    # Test de Mann-Whitney U (non-parametrique)
    u_stat, p_value_u = stats.mannwhitneyu(res_low, res_high, alternative='two-sided')
    output.write("Test de Mann-Whitney U (non-parametrique):\n")
    output.write(f"  U-statistic: {u_stat:.1f}\n")
    output.write(f"  p-value:     {p_value_u:.2e}\n\n")

    # Correlation masse-residu (sur tout l'echantillon)
    valid = (mass > 0) & (mass != -9)
    r_pearson, p_pearson = stats.pearsonr(mass[valid], residuals[valid])
    r_spearman, p_spearman = stats.spearmanr(mass[valid], residuals[valid])

    output.write("Correlation masse-residu (echantillon complet):\n")
    output.write(f"  Pearson r:  {r_pearson:.4f} (p = {p_pearson:.2e})\n")
    output.write(f"  Spearman r: {r_spearman:.4f} (p = {p_spearman:.2e})\n\n")

    print(f"\nTests statistiques:")
    print(f"  Test t de Welch: p = {p_value_t:.2e}")
    print(f"  Mann-Whitney U:  p = {p_value_u:.2e}")
    print(f"  Correlation Pearson: r = {r_pearson:.4f}, p = {p_pearson:.2e}")

    return p_value_t, p_value_u, r_pearson, p_pearson

def analyze_by_redshift_bins(data, output):
    """Analyse par tranches de redshift"""

    z = data['zCMB']
    mu_obs = data['mu']
    mass = data['host_logmass']

    mu_lcdm = np.array([calculate_expected_mu_lcdm(zi) for zi in z])
    residuals = mu_obs - mu_lcdm

    output.write("\n" + "="*70 + "\n")
    output.write("ANALYSE PAR TRANCHES DE REDSHIFT\n")
    output.write("="*70 + "\n\n")

    z_bins = [(0.01, 0.05), (0.05, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 1.0)]

    output.write(f"{'z range':<12} {'N_low':<8} {'N_high':<8} {'Delta_mu':<12} {'Signif':<10} {'Delta_%':<10}\n")
    output.write("-" * 70 + "\n")

    results_bins = []

    for z_min, z_max in z_bins:
        mask_z = (z >= z_min) & (z < z_max)
        mask_low = mask_z & (mass < MASS_LOW)
        mask_high = mask_z & (mass > MASS_HIGH)

        n_low = np.sum(mask_low)
        n_high = np.sum(mask_high)

        if n_low >= 3 and n_high >= 3:
            res_low = residuals[mask_low]
            res_high = residuals[mask_high]

            delta = np.mean(res_low) - np.mean(res_high)
            err = np.sqrt(np.std(res_low)**2/n_low + np.std(res_high)**2/n_high)
            signif = abs(delta) / err if err > 0 else 0
            delta_pct = (10**(delta/5) - 1) * 100

            output.write(f"{z_min:.2f}-{z_max:.2f}    {n_low:<8} {n_high:<8} {delta:+.4f}      {signif:.2f}sigma   {delta_pct:+.2f}%\n")
            results_bins.append((z_min, z_max, delta, signif, delta_pct))
        else:
            output.write(f"{z_min:.2f}-{z_max:.2f}    {n_low:<8} {n_high:<8} {'N/A':<12} {'N/A':<10} {'N/A':<10}\n")

    return results_bins

def compare_with_tmt_prediction(delta_percent, output):
    """Compare avec la prediction TMT"""

    output.write("\n" + "="*70 + "\n")
    output.write("COMPARAISON AVEC PREDICTIONS\n")
    output.write("="*70 + "\n\n")

    # Predictions
    tmt_prediction = (5, 10)  # TMT predit 5-10% de difference
    lcdm_prediction = 0       # LCDM predit 0%

    output.write("PREDICTIONS:\n")
    output.write(f"  TMT v2.3.1: Delta d_L = {tmt_prediction[0]}-{tmt_prediction[1]}% (vides plus lointains)\n")
    output.write(f"  LCDM:       Delta d_L = {lcdm_prediction}% (pas de difference)\n\n")

    output.write(f"OBSERVATION:\n")
    output.write(f"  Delta d_L = {delta_percent:+.2f}%\n\n")

    # Evaluation
    output.write("EVALUATION:\n")

    if delta_percent > 0:
        direction = "CORRECT (vides plus lointains)"
    else:
        direction = "INVERSE (amas plus lointains)"

    output.write(f"  Direction: {direction}\n")

    if tmt_prediction[0] <= abs(delta_percent) <= tmt_prediction[1]:
        tmt_verdict = "COMPATIBLE"
    elif abs(delta_percent) < tmt_prediction[0]:
        tmt_verdict = "TROP FAIBLE"
    else:
        tmt_verdict = "TROP FORT"

    if abs(delta_percent) < 2:
        lcdm_verdict = "COMPATIBLE"
    else:
        lcdm_verdict = "EN TENSION"

    output.write(f"  vs TMT:  {tmt_verdict}\n")
    output.write(f"  vs LCDM: {lcdm_verdict}\n")

    return tmt_verdict, lcdm_verdict

def main():
    """Fonction principale"""

    print("="*70)
    print("TEST PANTHEON+ SNIa PAR ENVIRONNEMENT")
    print("TMT v2.3.1 - Expansion Differentielle H(z, rho)")
    print("="*70)

    # Verifier que le fichier existe
    if not os.path.exists(DATA_FILE):
        print(f"\nERREUR: Fichier {DATA_FILE} non trouve!")
        return

    # Creer le dossier de sortie si necessaire
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Charger les donnees
    data = load_pantheon_data(DATA_FILE)
    if data is None:
        return

    # Ouvrir le fichier de sortie
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as output:

        output.write("="*70 + "\n")
        output.write("TEST PANTHEON+ SNIa PAR ENVIRONNEMENT\n")
        output.write("TMT v2.3.1 - Expansion Differentielle H(z, rho)\n")
        output.write("="*70 + "\n\n")
        output.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        output.write(f"Fichier: {DATA_FILE}\n")
        output.write(f"SNIa total: {len(data['zCMB'])}\n")

        # Statistiques de base
        output.write("\n" + "="*70 + "\n")
        output.write("STATISTIQUES DE BASE\n")
        output.write("="*70 + "\n\n")
        output.write(f"Redshift: {np.min(data['zCMB']):.4f} - {np.max(data['zCMB']):.4f}\n")
        output.write(f"Redshift median: {np.median(data['zCMB']):.4f}\n")
        output.write(f"Host mass: {np.min(data['host_logmass']):.2f} - {np.max(data['host_logmass']):.2f}\n")
        output.write(f"Host mass median: {np.median(data['host_logmass']):.2f}\n")

        # Analyse principale
        delta_mu, delta_err, delta_percent, n_low, n_high = analyze_by_environment(data, output)

        # Tests statistiques
        p_t, p_u, r_pearson, p_pearson = statistical_tests(data, output)

        # Analyse par bins de redshift
        results_bins = analyze_by_redshift_bins(data, output)

        # Comparaison avec predictions
        tmt_verdict, lcdm_verdict = compare_with_tmt_prediction(delta_percent, output)

        # Verdict final
        output.write("\n" + "="*70 + "\n")
        output.write("VERDICT FINAL\n")
        output.write("="*70 + "\n\n")

        # Determiner le verdict
        significance = abs(delta_mu) / delta_err

        if significance >= 3:
            stat_verdict = "TRES SIGNIFICATIF (>3 sigma)"
        elif significance >= 2:
            stat_verdict = "SIGNIFICATIF (>2 sigma)"
        elif significance >= 1:
            stat_verdict = "MARGINALEMENT SIGNIFICATIF (>1 sigma)"
        else:
            stat_verdict = "NON SIGNIFICATIF (<1 sigma)"

        output.write(f"Significance statistique: {stat_verdict}\n")
        output.write(f"Compatibilite TMT:        {tmt_verdict}\n")
        output.write(f"Compatibilite LCDM:       {lcdm_verdict}\n\n")

        # Verdict global
        if delta_percent > 0 and significance >= 2:
            if tmt_verdict == "COMPATIBLE":
                global_verdict = "TMT SUPPORTE"
            else:
                global_verdict = "TMT PARTIELLEMENT SUPPORTE"
        elif abs(delta_percent) < 2 and significance < 2:
            global_verdict = "LCDM COMPATIBLE (pas de signal)"
        else:
            global_verdict = "RESULTATS AMBIGUS"

        output.write(f"VERDICT GLOBAL: {global_verdict}\n")

        # Resume
        output.write("\n" + "="*70 + "\n")
        output.write("RESUME\n")
        output.write("="*70 + "\n\n")
        output.write(f"SNIa analysees:           {len(data['zCMB'])}\n")
        output.write(f"Vides (log M < {MASS_LOW}):     {n_low}\n")
        output.write(f"Amas (log M > {MASS_HIGH}):     {n_high}\n")
        output.write(f"Delta mu:                 {delta_mu:+.4f} +/- {delta_err:.4f} mag\n")
        output.write(f"Delta distance:           {delta_percent:+.2f}%\n")
        output.write(f"Significance:             {significance:.2f} sigma\n")
        output.write(f"Test t p-value:           {p_t:.2e}\n")
        output.write(f"Correlation masse-residu: r = {r_pearson:.4f}\n")
        output.write(f"\nVERDICT: {global_verdict}\n")

        print(f"\n{'='*70}")
        print(f"VERDICT FINAL: {global_verdict}")
        print(f"{'='*70}")
        print(f"\nResultats sauvegardes dans: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
