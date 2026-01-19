"""
CALIBRATION PRÉCISE k POUR GALAXIES ELLIPTIQUES
================================================

Objectif: Calibrer k directement sur elliptiques (sans biais)
au lieu d'appliquer un facteur correctif.

Méthode:
1. Pour chaque galaxie elliptique:
   - Calibrer k pour que σ_pred = σ_obs
2. Analyser k vs (M_bary, f_gas, R_e)
3. Déterminer si même loi k(M, f_gas) ou paramètres différents

Hypothèses à tester:
- H1: k_ell = f · k_spiral (même loi, facteur constant)
- H2: k_ell suit loi différente (k₀, α, β différents)
- H3: k_ell dépend aussi de R_e (géométrie)

Auteur: Pierre-Olivier Després Asselin
Date: 2025-12-07
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, curve_fit
from scipy.stats import pearsonr

# =============================================================================
# CONSTANTES
# =============================================================================

G = 4.302e-6  # kpc (km/s)² / M_sun
c = 299792.458  # km/s

# Loi k pour spirales (référence)
k0_spiral = 0.343
alpha_spiral = -1.610
beta_spiral = -3.585

# =============================================================================
# GÉNÉRATION GALAXIES ELLIPTIQUES
# =============================================================================

def generate_ellipticals(N=30, seed=42):
    """
    Génère galaxies elliptiques avec paramètres réalistes.
    """
    np.random.seed(seed)
    galaxies = []

    for i in range(N):
        # Masse stellaire
        log_M_stellar = np.random.uniform(10.5, 11.8)
        M_stellar = 10**log_M_stellar

        # Fraction gaz (très faible pour elliptiques)
        f_gas = 0.04 - 0.03 * (log_M_stellar - 10.5) / 1.3
        f_gas = np.clip(f_gas, 0.01, 0.05) * np.random.lognormal(0, 0.2)

        M_gas = M_stellar * f_gas
        M_bary = M_stellar + M_gas

        # Rayon effectif
        R_e = 3.0 * (M_stellar / 1e11)**0.6 * np.random.lognormal(0, 0.15)
        R_e = np.clip(R_e, 2.0, 20.0)

        # Dispersion vitesse (Faber-Jackson)
        sigma_obs = 200.0 * (M_stellar / 1e11)**0.25 * np.random.lognormal(0, 0.08)
        sigma_obs = np.clip(sigma_obs, 120, 400)

        galaxies.append({
            'id': i,
            'name': f'E{i:03d}',
            'M_stellar': M_stellar,
            'M_gas': M_gas,
            'M_bary': M_bary,
            'f_gas': f_gas,
            'R_e': R_e,
            'sigma_obs': sigma_obs
        })

    return galaxies

# =============================================================================
# MODÈLE M_DESPRÉS ELLIPTIQUES
# =============================================================================

def M_enclosed_sersic(r, M_total, R_e, n=4):
    """
    Masse enfermée profil Sérsic.
    Pour n=4 (elliptiques): approximation analytique.
    """
    if r <= 0:
        return 0
    b_n = 7.67  # Pour n=4
    x = b_n * (r / R_e)**(1/n)
    # Approximation: M(r) ~ M_total * (1 - exp(-x))
    M = M_total * (1 - np.exp(-x) * (1 + x + x**2/2))
    return M

def Phi_sersic(r, M_total, R_e):
    """Potentiel pour profil Sérsic."""
    if r <= 0.01:
        r = 0.01
    M = M_enclosed_sersic(r, M_total, R_e)
    return -G * M / r

def M_Despres_elliptical(R_max, M_bary, R_e, k):
    """
    M_D = k · ∫ Φ²(r) dV

    Intégration jusqu'à R_max (typiquement 10 R_e)
    """
    def integrand(r):
        if r <= 0:
            return 0
        Phi = Phi_sersic(r, M_bary, R_e)
        return Phi**2 * 4 * np.pi * r**2

    try:
        integral, _ = quad(integrand, 0.01, R_max, limit=200)
        return k * integral
    except:
        return 0.0

def sigma_from_M(M_total, R_e):
    """
    Dispersion vitesse depuis M_total.

    Pour elliptiques: σ² = k_virial · G M / R_e
    avec k_virial ~ 0.28 (calibré sur Faber-Jackson)

    Note: k_virial varie légèrement avec M (0.22-0.31)
    mais on utilise valeur moyenne.
    """
    k_virial = 0.28  # CORRIGÉ (était 5.0, trop élevé!)
    if R_e <= 0:
        return 0
    sigma2 = k_virial * G * M_total / R_e
    return np.sqrt(sigma2)

# =============================================================================
# CALIBRATION k POUR UNE ELLIPTIQUE
# =============================================================================

def calibrate_k_elliptical(galaxy, R_int_factor=10):
    """
    Calibre k pour qu'une elliptique reproduise σ_obs.

    Procédure:
    1. Fixer R_max = R_int_factor × R_e
    2. Chercher k tel que σ(M_bary + M_D(k)) = σ_obs

    Returns
    -------
    k : float
        Constante couplage calibrée
    success : bool
        True si calibration réussie
    """
    R_max = R_int_factor * galaxy['R_e']
    sigma_target = galaxy['sigma_obs']

    def objective(k):
        """Erreur σ_pred - σ_obs."""
        if k <= 0:
            return 1e15

        M_D = M_Despres_elliptical(R_max, galaxy['M_bary'], galaxy['R_e'], k)
        M_total = galaxy['M_bary'] + M_D
        sigma_pred = sigma_from_M(M_total, galaxy['R_e'])

        error = abs(sigma_pred - sigma_target)
        return error

    # Optimisation
    try:
        result = minimize_scalar(objective, bounds=(1e-4, 10.0), method='bounded')
        k_opt = result.x

        # Vérification qualité
        M_D = M_Despres_elliptical(R_max, galaxy['M_bary'], galaxy['R_e'], k_opt)
        M_total = galaxy['M_bary'] + M_D
        sigma_check = sigma_from_M(M_total, galaxy['R_e'])

        error_pct = abs(sigma_check - sigma_target) / sigma_target * 100

        success = (error_pct < 5.0)  # Tolérance 5%

        return k_opt, success

    except:
        return None, False

# =============================================================================
# ANALYSE PRINCIPALE
# =============================================================================

if __name__ == "__main__":

    print("=" * 80)
    print("CALIBRATION PRÉCISE k POUR GALAXIES ELLIPTIQUES")
    print("=" * 80)

    # =========================================================================
    # 1. GÉNÉRATION ÉCHANTILLON
    # =========================================================================

    print("\n### GÉNÉRATION ÉCHANTILLON ELLIPTIQUES ###\n")

    N_gal = 30
    galaxies = generate_ellipticals(N=N_gal, seed=42)

    print(f"Galaxies générées: {len(galaxies)}")
    print(f"  Masse: {min(g['M_bary'] for g in galaxies):.2e} - {max(g['M_bary'] for g in galaxies):.2e} M_sun")
    print(f"  f_gas: {min(g['f_gas'] for g in galaxies):.4f} - {max(g['f_gas'] for g in galaxies):.4f}")
    print(f"  R_e: {min(g['R_e'] for g in galaxies):.2f} - {max(g['R_e'] for g in galaxies):.2f} kpc")
    print(f"  σ: {min(g['sigma_obs'] for g in galaxies):.1f} - {max(g['sigma_obs'] for g in galaxies):.1f} km/s")

    # =========================================================================
    # 2. CALIBRATION k POUR CHAQUE GALAXIE
    # =========================================================================

    print("\n### CALIBRATION k INDIVIDUELLE ###\n")

    results = []
    for i, gal in enumerate(galaxies):
        print(f"  [{i+1:2d}/{N_gal}] {gal['name']:8s}  M={gal['M_bary']:.2e}  f_gas={gal['f_gas']:.3f}  ", end='')

        k, success = calibrate_k_elliptical(gal)

        if success:
            print(f"k={k:.4f}  ✓")
            results.append({
                'name': gal['name'],
                'M_bary': gal['M_bary'],
                'M_stellar': gal['M_stellar'],
                'M_gas': gal['M_gas'],
                'f_gas': gal['f_gas'],
                'R_e': gal['R_e'],
                'sigma_obs': gal['sigma_obs'],
                'k': k
            })
        else:
            print(f"ÉCHEC")

    N_success = len(results)
    print(f"\n✓ Calibrations réussies: {N_success}/{N_gal}")

    if N_success < 10:
        print("\n⚠ Trop peu de calibrations pour analyse fiable")
        exit()

    # =========================================================================
    # 3. STATISTIQUES k
    # =========================================================================

    k_vals = np.array([r['k'] for r in results])
    M_bary_vals = np.array([r['M_bary'] for r in results])
    f_gas_vals = np.array([r['f_gas'] for r in results])
    R_e_vals = np.array([r['R_e'] for r in results])
    M_stellar_vals = np.array([r['M_stellar'] for r in results])

    print(f"\n### STATISTIQUES k (ELLIPTIQUES) ###\n")
    print(f"  k min:     {k_vals.min():.4f}")
    print(f"  k max:     {k_vals.max():.4f}")
    print(f"  k moyen:   {k_vals.mean():.4f} ± {k_vals.std():.4f}")
    print(f"  k médian:  {np.median(k_vals):.4f}")
    print(f"  Scatter:   facteur {k_vals.max()/k_vals.min():.1f}")

    # Comparaison avec spirales
    k_spiral_typ = k0_spiral * (np.median(M_bary_vals)/1e10)**alpha_spiral * (1 + np.median(f_gas_vals))**beta_spiral
    print(f"\n  k spirale typique (même M, f_gas): {k_spiral_typ:.4f}")
    print(f"  Ratio k_ell / k_spiral:             {np.median(k_vals) / k_spiral_typ:.3f}")

    # =========================================================================
    # 4. CORRÉLATIONS
    # =========================================================================

    print(f"\n### CORRÉLATIONS k VS PARAMÈTRES ###\n")

    correlations = {}

    # k vs log(M_bary)
    r, p = pearsonr(np.log10(M_bary_vals), np.log10(k_vals))
    correlations['log_M_bary'] = (r, p)
    print(f"  k vs log(M_bary):    r = {r:+.3f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

    # k vs f_gas
    r, p = pearsonr(f_gas_vals, np.log10(k_vals))
    correlations['f_gas'] = (r, p)
    print(f"  k vs f_gas:          r = {r:+.3f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

    # k vs log(R_e)
    r, p = pearsonr(np.log10(R_e_vals), np.log10(k_vals))
    correlations['log_R_e'] = (r, p)
    print(f"  k vs log(R_e):       r = {r:+.3f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

    # Densité surfacique
    Sigma = M_bary_vals / (np.pi * R_e_vals**2)
    r, p = pearsonr(np.log10(Sigma), np.log10(k_vals))
    correlations['log_Sigma'] = (r, p)
    print(f"  k vs log(Σ):         r = {r:+.3f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

    # =========================================================================
    # 5. FITS PARAMÉTRIQUES
    # =========================================================================

    print(f"\n### FORMULATIONS k POUR ELLIPTIQUES ###\n")

    fits = {}

    # Modèle 1: k = k₀ · (M/10^10)^α
    try:
        def model_M(log_M, k0, alpha):
            return np.log10(k0) + alpha * (log_M - 10.0)

        popt, pcov = curve_fit(model_M, np.log10(M_bary_vals), np.log10(k_vals), p0=[0.1, -1.0])
        k0_M, alpha_M = popt
        err_M = np.sqrt(np.diag(pcov))

        k_pred_M = 10**model_M(np.log10(M_bary_vals), k0_M, alpha_M)
        R2_M = 1 - np.sum((k_vals - k_pred_M)**2) / np.sum((k_vals - k_vals.mean())**2)

        print(f"[1] k = k₀ · (M_bary/10¹⁰)^α")
        print(f"    k₀    = {k0_M:.4f} ± {err_M[0]:.4f}")
        print(f"    α     = {alpha_M:.4f} ± {err_M[1]:.4f}")
        print(f"    R²    = {R2_M:.4f}\n")

        fits['M_only'] = {'k0': k0_M, 'alpha': alpha_M, 'R2': R2_M, 'k_pred': k_pred_M}
    except:
        print(f"[1] Fit M_bary: ÉCHEC\n")
        fits['M_only'] = None

    # Modèle 2: k = k₀ · (M/10^10)^α · (1+f_gas)^β
    try:
        def model_comb(X, k0, alpha, beta):
            log_M, f = X
            return np.log10(k0) + alpha * (log_M - 10.0) + beta * np.log10(1 + f)

        popt, pcov = curve_fit(model_comb, [np.log10(M_bary_vals), f_gas_vals], np.log10(k_vals), p0=[0.1, -1.0, -2.0])
        k0_c, alpha_c, beta_c = popt
        err_c = np.sqrt(np.diag(pcov))

        k_pred_c = 10**model_comb([np.log10(M_bary_vals), f_gas_vals], k0_c, alpha_c, beta_c)
        R2_c = 1 - np.sum((k_vals - k_pred_c)**2) / np.sum((k_vals - k_vals.mean())**2)

        print(f"[2] k = k₀ · (M/10¹⁰)^α · (1+f_gas)^β")
        print(f"    k₀    = {k0_c:.4f} ± {err_c[0]:.4f}")
        print(f"    α     = {alpha_c:.4f} ± {err_c[1]:.4f}")
        print(f"    β     = {beta_c:.4f} ± {err_c[2]:.4f}")
        print(f"    R²    = {R2_c:.4f}\n")

        fits['combined'] = {'k0': k0_c, 'alpha': alpha_c, 'beta': beta_c, 'R2': R2_c, 'k_pred': k_pred_c}
    except:
        print(f"[2] Fit combiné: ÉCHEC\n")
        fits['combined'] = None

    # Modèle 3: k = k₀ · (M/10^10)^α · (R_e/5kpc)^γ
    try:
        def model_MR(X, k0, alpha, gamma):
            log_M, log_R = X
            return np.log10(k0) + alpha * (log_M - 10.0) + gamma * (log_R - np.log10(5.0))

        popt, pcov = curve_fit(model_MR, [np.log10(M_bary_vals), np.log10(R_e_vals)], np.log10(k_vals), p0=[0.1, -1.0, -0.5])
        k0_MR, alpha_MR, gamma_MR = popt
        err_MR = np.sqrt(np.diag(pcov))

        k_pred_MR = 10**model_MR([np.log10(M_bary_vals), np.log10(R_e_vals)], k0_MR, alpha_MR, gamma_MR)
        R2_MR = 1 - np.sum((k_vals - k_pred_MR)**2) / np.sum((k_vals - k_vals.mean())**2)

        print(f"[3] k = k₀ · (M/10¹⁰)^α · (R_e/5kpc)^γ")
        print(f"    k₀    = {k0_MR:.4f} ± {err_MR[0]:.4f}")
        print(f"    α     = {alpha_MR:.4f} ± {err_MR[1]:.4f}")
        print(f"    γ     = {gamma_MR:.4f} ± {err_MR[2]:.4f}")
        print(f"    R²    = {R2_MR:.4f}\n")

        fits['M_R'] = {'k0': k0_MR, 'alpha': alpha_MR, 'gamma': gamma_MR, 'R2': R2_MR, 'k_pred': k_pred_MR}
    except:
        print(f"[3] Fit M+R: ÉCHEC\n")
        fits['M_R'] = None

    # =========================================================================
    # 6. MEILLEUR MODÈLE
    # =========================================================================

    print("=" * 80)
    print("RÉSULTAT DÉCISIF - ELLIPTIQUES")
    print("=" * 80 + "\n")

    valid_fits = {name: fit for name, fit in fits.items() if fit is not None}
    if valid_fits:
        best_name = max(valid_fits.items(), key=lambda x: x[1]['R2'])[0]
        best = valid_fits[best_name]

        print(f"✓ MEILLEUR MODÈLE: {best_name}")
        print(f"  R² = {best['R2']:.4f} ({best['R2']*100:.1f}% variance)\n")

        if best_name == 'M_only':
            print(f"  k_ell = {best['k0']:.3f} · (M_bary/10¹⁰)^{best['alpha']:.3f}")
            print(f"\n  Comparaison spirales:")
            print(f"    k₀_spiral = {k0_spiral:.3f}  vs  k₀_ell = {best['k0']:.3f}  (ratio: {best['k0']/k0_spiral:.3f})")
            print(f"    α_spiral  = {alpha_spiral:.3f} vs  α_ell  = {best['alpha']:.3f}  (diff: {best['alpha']-alpha_spiral:+.3f})")

        elif best_name == 'combined':
            print(f"  k_ell = {best['k0']:.3f} · (M/10¹⁰)^{best['alpha']:.3f} · (1+f_gas)^{best['beta']:.3f}")
            print(f"\n  Comparaison spirales:")
            print(f"    k₀_spiral = {k0_spiral:.3f}  vs  k₀_ell = {best['k0']:.3f}  (ratio: {best['k0']/k0_spiral:.3f})")
            print(f"    α_spiral  = {alpha_spiral:.3f} vs  α_ell  = {best['alpha']:.3f}  (diff: {best['alpha']-alpha_spiral:+.3f})")
            print(f"    β_spiral  = {beta_spiral:.3f} vs  β_ell  = {best['beta']:.3f}  (diff: {best['beta']-beta_spiral:+.3f})")

        elif best_name == 'M_R':
            print(f"  k_ell = {best['k0']:.3f} · (M/10¹⁰)^{best['alpha']:.3f} · (R_e/5kpc)^{best['gamma']:.3f}")
            print(f"\n  NOUVELLE DÉPENDANCE: R_e (rayon effectif)")
            print(f"    γ = {best['gamma']:.3f} ({'négatif' if best['gamma'] < 0 else 'positif'})")

        # Scatter résiduel
        k_pred_best = best['k_pred']
        residuals = k_vals / k_pred_best
        scatter_orig = k_vals.max() / k_vals.min()
        scatter_res = residuals.max() / residuals.min()

        print(f"\n  Scatter ORIGINAL:  facteur {scatter_orig:.1f}")
        print(f"  Scatter RÉSIDUEL:  facteur {scatter_res:.1f}")
        print(f"  RÉDUCTION:         {(1 - scatter_res/scatter_orig)*100:.1f}%")

    else:
        print("⚠ AUCUN FIT VALIDE")

    # =========================================================================
    # 7. VISUALISATIONS
    # =========================================================================

    print("\n### VISUALISATIONS ###\n")

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: k vs M_bary
    ax = axes[0, 0]
    ax.loglog(M_bary_vals, k_vals, 'o', markersize=8, label='Elliptiques (calibrés)')

    if fits['M_only']:
        M_range = np.logspace(np.log10(M_bary_vals.min()), np.log10(M_bary_vals.max()), 100)
        k_fit_ell = fits['M_only']['k0'] * (M_range/1e10)**fits['M_only']['alpha']
        ax.plot(M_range, k_fit_ell, 'r-', lw=2, label=f'Fit ell: R²={fits["M_only"]["R2"]:.3f}')

        # Loi spirales pour comparaison
        k_fit_spi = k0_spiral * (M_range/1e10)**alpha_spiral * (1 + 0.02)**beta_spiral  # f_gas typ ell
        ax.plot(M_range, k_fit_spi, 'b--', lw=2, alpha=0.7, label='Loi spirales')

    ax.set_xlabel('M_bary (M☉)', fontsize=12)
    ax.set_ylabel('k', fontsize=12)
    ax.set_title('k vs Masse Baryonique (Elliptiques)', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: k vs f_gas
    ax = axes[0, 1]
    ax.semilogy(f_gas_vals, k_vals, 'o', markersize=8, label='Elliptiques')
    ax.set_xlabel('f_gas', fontsize=12)
    ax.set_ylabel('k', fontsize=12)
    ax.set_title('k vs Fraction Gazeuse', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: k_obs vs k_pred
    ax = axes[1, 0]
    if valid_fits:
        k_pred_best = valid_fits[best_name]['k_pred']
        ax.loglog(k_pred_best, k_vals, 'o', markersize=8)
        lim = [min(k_pred_best.min(), k_vals.min()), max(k_pred_best.max(), k_vals.max())]
        ax.plot(lim, lim, 'k--', lw=2, label='1:1')
        ax.set_xlabel(f'k prédit ({best_name})', fontsize=12)
        ax.set_ylabel('k calibré', fontsize=12)
        ax.set_title('Qualité Prédiction', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    # Plot 4: Distribution k
    ax = axes[1, 1]
    ax.hist(np.log10(k_vals), bins=15, alpha=0.7, edgecolor='black', color='coral')
    ax.axvline(np.log10(np.median(k_vals)), color='red', linestyle='--', lw=3,
               label=f'Médian: {np.median(k_vals):.4f}')
    ax.set_xlabel('log₁₀(k)', fontsize=12)
    ax.set_ylabel('Nombre galaxies', fontsize=12)
    ax.set_title('Distribution k (Elliptiques)', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('/home/user/Maitrise-du-temps/k_elliptiques_calibration_precise.png', dpi=150, bbox_inches='tight')
    print("  ✓ Graphiques: k_elliptiques_calibration_precise.png")

    # =========================================================================
    # 8. SAUVEGARDE RÉSULTATS
    # =========================================================================

    with open('/home/user/Maitrise-du-temps/k_elliptiques_calibration_results.txt', 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("CALIBRATION PRÉCISE k POUR GALAXIES ELLIPTIQUES\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Échantillon: {N_success} elliptiques calibrées\n\n")

        f.write("STATISTIQUES k:\n")
        f.write(f"  k min:    {k_vals.min():.4f}\n")
        f.write(f"  k max:    {k_vals.max():.4f}\n")
        f.write(f"  k moyen:  {k_vals.mean():.4f} ± {k_vals.std():.4f}\n")
        f.write(f"  k médian: {np.median(k_vals):.4f}\n")
        f.write(f"  Scatter:  facteur {k_vals.max()/k_vals.min():.1f}\n\n")

        if valid_fits:
            f.write("MEILLEUR MODÈLE: " + best_name + "\n")
            f.write(f"  R² = {best['R2']:.4f}\n\n")

            if best_name == 'combined':
                f.write(f"  k_ell = {best['k0']:.3f} · (M/10¹⁰)^{best['alpha']:.3f} · (1+f_gas)^{best['beta']:.3f}\n\n")
                f.write("COMPARAISON SPIRALES:\n")
                f.write(f"  k₀: {k0_spiral:.3f} (spiral) vs {best['k0']:.3f} (ell)  → ratio {best['k0']/k0_spiral:.3f}\n")
                f.write(f"  α:  {alpha_spiral:.3f} (spiral) vs {best['alpha']:.3f} (ell)  → diff {best['alpha']-alpha_spiral:+.3f}\n")
                f.write(f"  β:  {beta_spiral:.3f} (spiral) vs {best['beta']:.3f} (ell)  → diff {best['beta']-beta_spiral:+.3f}\n")

    print("  ✓ Résultats: k_elliptiques_calibration_results.txt\n")
    print("=" * 80)
