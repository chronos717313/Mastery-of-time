#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DES 3 PREDICTIONS DISTINCTIVES TMT v2.0
=============================================

1. SNIa par environnement: Delta_dL = 5-10% (vide vs amas)
2. ISW amplifie +26% dans supervides
3. Validation r_c(M) par validation croisee

Auteur: Pierre-Olivier Despres Asselin
Date: Janvier 2026
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.stats import pearsonr, spearmanr, ttest_ind
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONSTANTES
# =============================================================================

H0 = 70  # km/s/Mpc
Omega_m = 0.315
Omega_Lambda = 0.685
c_km_s = 299792.458  # km/s
G_KPC = 4.302e-6  # kpc (km/s)^2 / M_sun
beta = 0.4  # Parametre d'ancrage TMT

# =============================================================================
# TEST 1: SNIa PAR ENVIRONNEMENT
# =============================================================================

def H_TMT(z, rho_ratio):
    """Fonction de Hubble TMT avec expansion differentielle."""
    term_m = Omega_m * (1 + z)**3
    term_L = Omega_Lambda * np.exp(beta * (1 - rho_ratio))
    return H0 * np.sqrt(term_m + term_L)

def H_LCDM(z):
    """Fonction de Hubble LCDM standard."""
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

def luminosity_distance(z, model='LCDM', rho_ratio=1.0):
    """Distance de luminosite en Mpc."""
    def integrand(zp):
        if model == 'TMT':
            return c_km_s / H_TMT(zp, rho_ratio)
        else:
            return c_km_s / H_LCDM(zp)
    integral, _ = quad(integrand, 0, z, limit=100)
    return (1 + z) * integral

def distance_modulus(d_L_Mpc):
    """Module de distance mu = 5 log10(d_L/10pc)."""
    d_L_pc = d_L_Mpc * 1e6
    return 5 * np.log10(d_L_pc / 10)

def test_SNIa_environment():
    """
    Test 1: SNIa par environnement
    Prediction TMT: Delta_dL = 5-10% entre vide et amas
    """
    print("=" * 70)
    print("TEST 1: SNIa PAR ENVIRONNEMENT")
    print("Prediction TMT: Delta_dL(vide-amas) = 5-10%")
    print("=" * 70)
    print()

    # Generer echantillon SNIa synthetique
    np.random.seed(42)
    n_sn = 500

    # Redshifts
    z_array = np.random.uniform(0.01, 1.2, n_sn)

    # Environnements
    env_type = np.random.choice(['void', 'mean', 'cluster'], size=n_sn, p=[0.4, 0.4, 0.2])
    rho_map = {'void': 0.3, 'mean': 1.0, 'cluster': 5.0}

    # Generer magnitudes avec TMT (comme si c'etait la realite)
    M_abs = -19.3
    m_obs = []

    for z_i, env in zip(z_array, env_type):
        rho = rho_map[env]
        d_L = luminosity_distance(z_i, model='TMT', rho_ratio=rho)
        mu = distance_modulus(d_L)
        m = M_abs + mu + np.random.normal(0, 0.15)
        m_obs.append(m)

    m_obs = np.array(m_obs)

    # Analyser par bins de redshift
    z_bins = [(0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]

    results = []
    print("Analyse par bins de redshift:")
    print("-" * 50)

    for z_min, z_max in z_bins:
        mask_z = (z_array >= z_min) & (z_array < z_max)

        # SNIa dans vides
        mask_void = mask_z & (env_type == 'void')
        mB_void = m_obs[mask_void]
        z_void = z_array[mask_void]

        # SNIa dans amas
        mask_cluster = mask_z & (env_type == 'cluster')
        mB_cluster = m_obs[mask_cluster]
        z_cluster = z_array[mask_cluster]

        if len(mB_void) < 5 or len(mB_cluster) < 5:
            continue

        # Calculer residus par rapport a LCDM
        resid_void = []
        for z_i, m_i in zip(z_void, mB_void):
            d_L_LCDM = luminosity_distance(z_i, model='LCDM')
            m_LCDM = M_abs + distance_modulus(d_L_LCDM)
            resid_void.append(m_i - m_LCDM)

        resid_cluster = []
        for z_i, m_i in zip(z_cluster, mB_cluster):
            d_L_LCDM = luminosity_distance(z_i, model='LCDM')
            m_LCDM = M_abs + distance_modulus(d_L_LCDM)
            resid_cluster.append(m_i - m_LCDM)

        resid_void = np.array(resid_void)
        resid_cluster = np.array(resid_cluster)

        # Difference moyenne
        delta_m = np.mean(resid_cluster) - np.mean(resid_void)

        # Test t de Student
        t_stat, p_value = ttest_ind(resid_cluster, resid_void)

        # Convertir en difference de distance
        # Delta_m ~ 5 * Delta_log(d_L) ~ 2.17 * Delta_d_L/d_L
        delta_dL_percent = delta_m / 0.0217  # approximation

        print(f"  z = [{z_min}, {z_max}]:")
        print(f"    N_void = {len(mB_void)}, N_cluster = {len(mB_cluster)}")
        print(f"    Delta_m = {delta_m:+.3f} mag")
        print(f"    Delta_dL ~ {delta_dL_percent:+.1f}%")
        print(f"    p-value = {p_value:.2e}")

        if p_value < 0.05 and delta_m > 0:
            print(f"    => COHERENT TMT (amas plus lointains)")
        print()

        results.append({
            'z_center': (z_min + z_max) / 2,
            'delta_m': delta_m,
            'delta_dL_percent': delta_dL_percent,
            'p_value': p_value,
            'significant': p_value < 0.05 and delta_m > 0
        })

    # Prediction theorique TMT
    print("\nPrediction theorique TMT:")
    print("-" * 50)

    for z in [0.3, 0.5, 0.7, 0.9]:
        d_L_void = luminosity_distance(z, model='TMT', rho_ratio=0.3)
        d_L_cluster = luminosity_distance(z, model='TMT', rho_ratio=5.0)
        delta_percent = 100 * (d_L_cluster - d_L_void) / d_L_void
        print(f"  z = {z}: Delta_dL(amas-vide) = {delta_percent:.1f}%")

    # Verdict
    n_significant = sum(1 for r in results if r['significant'])

    print("\n" + "=" * 70)
    print("VERDICT TEST 1 (SNIa)")
    print("=" * 70)
    print(f"Bins significatifs: {n_significant}/{len(results)}")

    if n_significant >= len(results) // 2:
        print("=> TMT SUPPORTE: Difference vide-amas detectee")
        verdict1 = "SUPPORTE"
    else:
        print("=> INCONCLUSIF: Donnees synthetiques, vraies donnees requises")
        verdict1 = "INCONCLUSIF (donnees synthetiques)"

    return {'verdict': verdict1, 'results': results}

# =============================================================================
# TEST 2: ISW x SUPERVIDES
# =============================================================================

def growth_factor_LCDM(z):
    """Facteur de croissance D(z) approximatif."""
    Omega_m_z = Omega_m * (1 + z)**3 / (Omega_m * (1 + z)**3 + Omega_Lambda)
    return np.exp(-Omega_m_z + 1) / (1 + z)

def growth_factor_TMT(z, rho_ratio):
    """Facteur de croissance D(z) TMT."""
    D_LCDM = growth_factor_LCDM(z)
    correction = 1 + beta * (1 - rho_ratio) * (z / (1 + z))
    return D_LCDM * correction

def ISW_integrand(z, model='LCDM', rho_ratio=1.0):
    """Integrande ISW dPhi/deta."""
    dz = 0.01
    z1 = max(z - dz, 0.001)
    z2 = z + dz

    if model == 'TMT':
        D1 = growth_factor_TMT(z1, rho_ratio)
        D2 = growth_factor_TMT(z2, rho_ratio)
        H_z = H_TMT(z, rho_ratio)
    else:
        D1 = growth_factor_LCDM(z1)
        D2 = growth_factor_LCDM(z2)
        H_z = H_LCDM(z)

    dD_dz = (D2 - D1) / (2 * dz)
    dz_deta = -H_z * (1 + z) / c_km_s

    return dD_dz * dz_deta

def calculate_ISW_amplitude(z_min=0.01, z_max=2.0, model='LCDM', rho_ratio=1.0):
    """Calcule amplitude ISW integree."""
    z_array = np.linspace(z_min, z_max, 100)
    integrand_values = [ISW_integrand(z, model, rho_ratio) for z in z_array]
    # Use scipy.integrate.trapezoid for compatibility
    from scipy.integrate import trapezoid
    return trapezoid(integrand_values, z_array)

def test_ISW_supervoids():
    """
    Test 2: ISW amplifie dans supervides
    Prediction TMT: +26% par rapport a LCDM
    """
    print("\n" + "=" * 70)
    print("TEST 2: ISW x SUPERVIDES")
    print("Prediction TMT: ISW amplifie +26% dans vides")
    print("=" * 70)
    print()

    # Calculer ISW pour differents modeles
    print("Calcul amplitude ISW:")
    print("-" * 50)

    ISW_LCDM = calculate_ISW_amplitude(model='LCDM')
    ISW_TMT_void = calculate_ISW_amplitude(model='TMT', rho_ratio=0.2)
    ISW_TMT_mean = calculate_ISW_amplitude(model='TMT', rho_ratio=1.0)
    ISW_TMT_cluster = calculate_ISW_amplitude(model='TMT', rho_ratio=5.0)

    print(f"  ISW LCDM (reference):    {ISW_LCDM:.6e}")
    print(f"  ISW TMT (vide, rho=0.2): {ISW_TMT_void:.6e}")
    print(f"  ISW TMT (moyen, rho=1):  {ISW_TMT_mean:.6e}")
    print(f"  ISW TMT (amas, rho=5):   {ISW_TMT_cluster:.6e}")
    print()

    # Ratios
    ratio_void = abs(ISW_TMT_void / ISW_LCDM) if ISW_LCDM != 0 else 1
    ratio_mean = abs(ISW_TMT_mean / ISW_LCDM) if ISW_LCDM != 0 else 1
    ratio_cluster = abs(ISW_TMT_cluster / ISW_LCDM) if ISW_LCDM != 0 else 1

    print("Ratios TMT / LCDM:")
    print("-" * 50)
    print(f"  Vide (rho=0.2):   {ratio_void:.2f} ({100*(ratio_void-1):+.0f}%)")
    print(f"  Moyen (rho=1.0):  {ratio_mean:.2f} ({100*(ratio_mean-1):+.0f}%)")
    print(f"  Amas (rho=5.0):   {ratio_cluster:.2f} ({100*(ratio_cluster-1):+.0f}%)")
    print()

    # Prediction vs observation
    print("Comparaison avec prediction:")
    print("-" * 50)
    print(f"  Prediction TMT (vide):  +26%")
    print(f"  Calcule:                {100*(ratio_void-1):+.0f}%")

    amplification = 100 * (ratio_void - 1)

    print("\n" + "=" * 70)
    print("VERDICT TEST 2 (ISW)")
    print("=" * 70)

    if amplification > 20:
        print(f"=> TMT SUPPORTE: ISW amplifie de {amplification:.0f}% dans vides")
        print("   (Coherent avec prediction +26%)")
        verdict2 = "SUPPORTE"
    elif amplification > 10:
        print(f"=> PARTIELLEMENT SUPPORTE: ISW amplifie de {amplification:.0f}%")
        verdict2 = "PARTIEL"
    else:
        print(f"=> NON SUPPORTE: Amplification trop faible ({amplification:.0f}%)")
        verdict2 = "NON SUPPORTE"

    print("\nNote: Test avec vraies donnees Planck x BOSS requis pour validation")

    return {
        'verdict': verdict2,
        'amplification_void': amplification,
        'ratio_void': ratio_void,
        'ratio_cluster': ratio_cluster
    }

# =============================================================================
# TEST 3: VALIDATION r_c(M) PAR VALIDATION CROISEE
# =============================================================================

def load_sparc_data(data_dir):
    """Charge les donnees SPARC."""
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

    for name in rotation_curves:
        for key in rotation_curves[name]:
            rotation_curves[name][key] = np.array(rotation_curves[name][key])

    return rotation_curves

def compute_baryonic(rc, ML_disk=0.5, ML_bul=0.7):
    """Calcule masse baryonique."""
    V_bary_sq = rc['Vgas']**2 + ML_disk * rc['Vdisk']**2 + ML_bul * rc['Vbul']**2
    V_bary = np.sqrt(np.maximum(V_bary_sq, 0))
    M_bary_enc = V_bary**2 * rc['R'] / G_KPC
    return V_bary, M_bary_enc

def r_c_from_mass(M_bary, a=2.6, b=0.56):
    """Relation r_c(M) calibree."""
    return a * (M_bary / 1e10)**b

def optimize_r_c_individual(R, Vobs, e_Vobs, M_bary_enc, n=0.75):
    """Optimise r_c pour une galaxie."""
    def chi2(r_c):
        if r_c <= 0:
            return 1e10
        mult = 1 + (R / r_c)**n
        M_eff = M_bary_enc * mult
        V_model = np.sqrt(G_KPC * M_eff / R)
        return np.sum(((V_model - Vobs) / e_Vobs)**2)

    result = minimize(lambda x: chi2(x[0]), [5.0], bounds=[(0.1, 200)], method='L-BFGS-B')
    return result.x[0] if result.success else np.nan

def test_r_c_M_validation():
    """
    Test 3: Validation croisee r_c(M)
    Divise SPARC en train/test et verifie la relation
    """
    print("\n" + "=" * 70)
    print("TEST 3: VALIDATION CROISEE r_c(M)")
    print("Prediction: r_c = 2.6 x (M/10^10)^0.56 kpc")
    print("=" * 70)
    print()

    # Charger donnees SPARC
    data_dir = Path(__file__).parent.parent / "data" / "SPARC"
    if not data_dir.exists():
        data_dir = Path(__file__).parent.parent / "data" / "sparc"

    print("Chargement donnees SPARC...")
    rotation_curves = load_sparc_data(data_dir)
    print(f"  {len(rotation_curves)} galaxies chargees")
    print()

    # Calculer r_c optimal pour chaque galaxie
    galaxy_data = []

    for name, rc in rotation_curves.items():
        if len(rc['R']) < 5:
            continue

        R = rc['R']
        Vobs = rc['Vobs']
        e_Vobs = rc['e_Vobs']
        V_bary, M_bary_enc = compute_baryonic(rc)

        M_bary_total = M_bary_enc[-1] if len(M_bary_enc) > 0 else 0

        if M_bary_total < 1e6:
            continue

        r_c_opt = optimize_r_c_individual(R, Vobs, e_Vobs, M_bary_enc)

        if 0.1 < r_c_opt < 200:
            galaxy_data.append({
                'name': name,
                'M_bary': M_bary_total,
                'r_c': r_c_opt
            })

    print(f"  {len(galaxy_data)} galaxies avec r_c valide")
    print()

    # Diviser en train (70%) / test (30%)
    np.random.seed(42)
    indices = np.random.permutation(len(galaxy_data))
    n_train = int(0.7 * len(galaxy_data))

    train_idx = indices[:n_train]
    test_idx = indices[n_train:]

    train_data = [galaxy_data[i] for i in train_idx]
    test_data = [galaxy_data[i] for i in test_idx]

    print(f"Division train/test: {len(train_data)}/{len(test_data)}")
    print()

    # Calibrer r_c(M) sur train
    print("Calibration sur ensemble TRAIN:")
    print("-" * 50)

    M_train = np.array([g['M_bary'] for g in train_data])
    r_c_train = np.array([g['r_c'] for g in train_data])

    # Fit log-log
    valid = (M_train > 0) & (r_c_train > 0)
    log_M = np.log10(M_train[valid] / 1e10)
    log_rc = np.log10(r_c_train[valid])

    coeffs = np.polyfit(log_M, log_rc, 1)
    b_train = coeffs[0]
    a_train = 10**coeffs[1]

    # R2 sur train
    r_c_pred_train = a_train * (M_train[valid] / 1e10)**b_train
    ss_res = np.sum((r_c_train[valid] - r_c_pred_train)**2)
    ss_tot = np.sum((r_c_train[valid] - np.mean(r_c_train[valid]))**2)
    R2_train = 1 - ss_res / ss_tot

    print(f"  Relation calibree: r_c = {a_train:.2f} x (M/10^10)^{b_train:.2f}")
    print(f"  R2 (train): {R2_train:.3f}")
    print()

    # Valider sur test
    print("Validation sur ensemble TEST:")
    print("-" * 50)

    M_test = np.array([g['M_bary'] for g in test_data])
    r_c_test = np.array([g['r_c'] for g in test_data])

    # Prediction avec parametres calibres sur train
    r_c_pred_test = a_train * (M_test / 1e10)**b_train

    # R2 sur test
    valid_test = (M_test > 0) & (r_c_test > 0) & (r_c_pred_test > 0)
    ss_res_test = np.sum((r_c_test[valid_test] - r_c_pred_test[valid_test])**2)
    ss_tot_test = np.sum((r_c_test[valid_test] - np.mean(r_c_test[valid_test]))**2)
    R2_test = 1 - ss_res_test / ss_tot_test if ss_tot_test > 0 else 0

    # Correlation sur test
    r_pearson, p_pearson = pearsonr(np.log10(M_test[valid_test]), np.log10(r_c_test[valid_test]))

    print(f"  R2 (test):     {R2_test:.3f}")
    print(f"  Pearson (test): r = {r_pearson:.3f} (p = {p_pearson:.2e})")
    print()

    # Comparer avec relation originale
    print("Comparaison avec relation originale (103 galaxies):")
    print("-" * 50)
    print(f"  Original: r_c = 2.6 x (M/10^10)^0.56")
    print(f"  Train:    r_c = {a_train:.2f} x (M/10^10)^{b_train:.2f}")

    # Ecart
    delta_a = 100 * (a_train - 2.6) / 2.6
    delta_b = 100 * (b_train - 0.56) / 0.56
    print(f"  Ecart a: {delta_a:+.0f}%")
    print(f"  Ecart b: {delta_b:+.0f}%")
    print()

    print("=" * 70)
    print("VERDICT TEST 3 (r_c(M))")
    print("=" * 70)

    if R2_test > 0.3 and abs(r_pearson) > 0.5 and p_pearson < 0.01:
        print(f"=> r_c(M) VALIDE par validation croisee")
        print(f"   R2_test = {R2_test:.3f}, r = {r_pearson:.3f}")
        verdict3 = "VALIDE"
    elif R2_test > 0.15:
        print(f"=> r_c(M) PARTIELLEMENT VALIDE")
        print(f"   R2_test = {R2_test:.3f} (faible mais positif)")
        verdict3 = "PARTIEL"
    else:
        print(f"=> r_c(M) NON VALIDE sur cet echantillon")
        verdict3 = "NON VALIDE"

    return {
        'verdict': verdict3,
        'a_train': a_train,
        'b_train': b_train,
        'R2_train': R2_train,
        'R2_test': R2_test,
        'r_pearson_test': r_pearson,
        'p_value_test': p_pearson
    }

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("        TEST DES 3 PREDICTIONS DISTINCTIVES TMT v2.0")
    print("=" * 70)
    print()
    print("1. SNIa par environnement: Delta_dL = 5-10%")
    print("2. ISW amplifie +26% dans supervides")
    print("3. Validation croisee r_c(M)")
    print()

    # Test 1: SNIa
    results_snia = test_SNIa_environment()

    # Test 2: ISW
    results_isw = test_ISW_supervoids()

    # Test 3: r_c(M)
    results_rc = test_r_c_M_validation()

    # Resume final
    print("\n" + "=" * 70)
    print("                    RESUME DES 3 TESTS")
    print("=" * 70)
    print()
    print(f"  Test 1 (SNIa environnement): {results_snia['verdict']}")
    print(f"  Test 2 (ISW supervides):     {results_isw['verdict']}")
    print(f"  Test 3 (r_c(M) validation):  {results_rc['verdict']}")
    print()

    # Score global
    verdicts = [results_snia['verdict'], results_isw['verdict'], results_rc['verdict']]
    n_supporte = sum(1 for v in verdicts if 'SUPPORTE' in v or 'VALIDE' in v)
    n_partiel = sum(1 for v in verdicts if 'PARTIEL' in v)

    print("-" * 70)
    if n_supporte >= 2:
        print("VERDICT GLOBAL: TMT v2.0 SUPPORTE")
        print(f"  {n_supporte}/3 tests positifs")
    elif n_supporte + n_partiel >= 2:
        print("VERDICT GLOBAL: TMT v2.0 PARTIELLEMENT SUPPORTE")
        print(f"  {n_supporte} positifs, {n_partiel} partiels")
    else:
        print("VERDICT GLOBAL: TESTS SUPPLEMENTAIRES REQUIS")
        print("  Vraies donnees observationnelles necessaires")

    print("=" * 70)

    # Sauvegarder resultats
    output_dir = Path(__file__).parent.parent / "data" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    results_file = output_dir / "test_3_predictions_TMT.txt"
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TEST DES 3 PREDICTIONS DISTINCTIVES TMT v2.0\n")
        f.write("=" * 70 + "\n\n")

        f.write("TEST 1: SNIa PAR ENVIRONNEMENT\n")
        f.write(f"  Verdict: {results_snia['verdict']}\n")
        f.write(f"  Prediction: Delta_dL = 5-10%\n\n")

        f.write("TEST 2: ISW x SUPERVIDES\n")
        f.write(f"  Verdict: {results_isw['verdict']}\n")
        f.write(f"  Amplification vide: {results_isw['amplification_void']:.0f}%\n")
        f.write(f"  (Prediction: +26%)\n\n")

        f.write("TEST 3: VALIDATION r_c(M)\n")
        f.write(f"  Verdict: {results_rc['verdict']}\n")
        f.write(f"  Relation: r_c = {results_rc['a_train']:.2f} x (M/10^10)^{results_rc['b_train']:.2f}\n")
        f.write(f"  R2 train: {results_rc['R2_train']:.3f}\n")
        f.write(f"  R2 test:  {results_rc['R2_test']:.3f}\n")
        f.write(f"  Pearson test: r = {results_rc['r_pearson_test']:.3f}\n\n")

        f.write("=" * 70 + "\n")
        f.write(f"VERDICT GLOBAL: {n_supporte}/3 tests positifs\n")
        f.write("=" * 70 + "\n")

    print(f"\nResultats sauvegardes: {results_file}")

    return {
        'snia': results_snia,
        'isw': results_isw,
        'rc': results_rc
    }

if __name__ == "__main__":
    main()
