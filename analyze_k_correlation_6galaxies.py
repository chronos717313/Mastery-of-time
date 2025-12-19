"""
ANALYSE CORRÉLATIONS k - 6 GALAXIES SPARC VALIDÉES
===================================================

Analyse des 6 galaxies avec k calibrés (formulation Φ² · r⁰):
- NGC2403: k=0.304
- NGC3198: k=0.186
- NGC6503: k=1.287
- DDO154:  k=3.675
- UGC2885: k=0.014
- NGC2841: k=0.026

Objectif: Trouver k = f(M_bary, f_gas, R_disk, ...)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.optimize import curve_fit

# Données des 6 galaxies
galaxies = {
    'NGC2403': {'M_stellar': 3.5e9, 'M_gas': 1.8e9, 'k': 0.304, 'R_disk': 1.8},
    'NGC3198': {'M_stellar': 6.2e9, 'M_gas': 2.1e9, 'k': 0.186, 'R_disk': 2.5},
    'NGC6503': {'M_stellar': 1.8e9, 'M_gas': 8e8, 'k': 1.287, 'R_disk': 1.2},
    'DDO154':  {'M_stellar': 1.5e8, 'M_gas': 5e8, 'k': 3.675, 'R_disk': 0.5},
    'UGC2885': {'M_stellar': 5.0e10, 'M_gas': 8e9, 'k': 0.014, 'R_disk': 12.0},
    'NGC2841': {'M_stellar': 3.8e10, 'M_gas': 3.2e9, 'k': 0.026, 'R_disk': 9.5},
}

# Extraction paramètres
names = list(galaxies.keys())
k_vals = np.array([galaxies[name]['k'] for name in names])
M_stellar = np.array([galaxies[name]['M_stellar'] for name in names])
M_gas = np.array([galaxies[name]['M_gas'] for name in names])
M_bary = M_stellar + M_gas
f_gas = M_gas / M_bary
R_disk = np.array([galaxies[name]['R_disk'] for name in names])

# Autres quantités dérivées
Sigma_bary = M_bary / (np.pi * R_disk**2)  # Densité surfacique (M_sun/kpc²)

print("=" * 80)
print("ANALYSE CORRÉLATIONS k - 6 GALAXIES SPARC")
print("=" * 80)

print("\n### DONNÉES ###\n")
print(f"{'Galaxy':<10s}  {'M_bary':>12s}  {'f_gas':>6s}  {'R_disk':>7s}  {'Σ_bary':>12s}  {'k':>8s}")
print("-" * 80)
for name in names:
    g = galaxies[name]
    M_b = g['M_stellar'] + g['M_gas']
    f_g = g['M_gas'] / M_b
    Sig = M_b / (np.pi * g['R_disk']**2)
    print(f"{name:<10s}  {M_b:>12.2e}  {f_g:>6.3f}  {g['R_disk']:>7.2f}  {Sig:>12.2e}  {g['k']:>8.4f}")

print(f"\n{'Moyenne':<10s}  {M_bary.mean():>12.2e}  {f_gas.mean():>6.3f}  {R_disk.mean():>7.2f}  {Sigma_bary.mean():>12.2e}  {k_vals.mean():>8.4f}")

# ==============================================================================
# CORRÉLATIONS
# ==============================================================================

print("\n" + "=" * 80)
print("CORRÉLATIONS PEARSON")
print("=" * 80 + "\n")

correlations = {}

# 1. k vs log(M_bary)
r, p = pearsonr(np.log10(M_bary), np.log10(k_vals))
correlations['log_M_bary'] = (r, p)
print(f"  k vs log(M_bary):    r = {r:+.4f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

# 2. k vs f_gas
r, p = pearsonr(f_gas, np.log10(k_vals))
correlations['f_gas'] = (r, p)
print(f"  k vs f_gas:          r = {r:+.4f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

# 3. k vs log(R_disk)
r, p = pearsonr(np.log10(R_disk), np.log10(k_vals))
correlations['log_R_disk'] = (r, p)
print(f"  k vs log(R_disk):    r = {r:+.4f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

# 4. k vs log(Σ_bary)
r, p = pearsonr(np.log10(Sigma_bary), np.log10(k_vals))
correlations['log_Sigma'] = (r, p)
print(f"  k vs log(Σ):         r = {r:+.4f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

# 5. k vs log(M_stellar)
r, p = pearsonr(np.log10(M_stellar), np.log10(k_vals))
correlations['log_M_stellar'] = (r, p)
print(f"  k vs log(M_stellar): r = {r:+.4f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

# 6. k vs log(M_gas)
r, p = pearsonr(np.log10(M_gas), np.log10(k_vals))
correlations['log_M_gas'] = (r, p)
print(f"  k vs log(M_gas):     r = {r:+.4f}  (p = {p:.4f})  {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'NS'}")

# Trouver meilleure corrélation
best_corr = max(correlations.items(), key=lambda x: abs(x[1][0]))
print(f"\n  → MEILLEURE CORRÉLATION: {best_corr[0]} (r = {best_corr[1][0]:+.4f}, p = {best_corr[1][1]:.4f})")

# ==============================================================================
# FITS PARAMÉTRIQUES
# ==============================================================================

print("\n" + "=" * 80)
print("FITS PARAMÉTRIQUES")
print("=" * 80 + "\n")

results = {}

# Modèle 1: k = k_0 * (M_bary / 10^10)^α
try:
    def model_M(log_M, k0, alpha):
        return np.log10(k0) + alpha * (log_M - 10.0)

    popt, pcov = curve_fit(model_M, np.log10(M_bary), np.log10(k_vals), p0=[1.0, -0.5])
    k0_M, alpha_M = popt
    err_M = np.sqrt(np.diag(pcov))

    k_pred_M = 10**model_M(np.log10(M_bary), k0_M, alpha_M)
    R2_M = 1 - np.sum((k_vals - k_pred_M)**2) / np.sum((k_vals - k_vals.mean())**2)

    print(f"[1] k = k₀ · (M_bary / 10¹⁰ M☉)^α")
    print(f"    k₀    = {k0_M:.4f} ± {err_M[0]:.4f}")
    print(f"    α     = {alpha_M:.4f} ± {err_M[1]:.4f}")
    print(f"    R²    = {R2_M:.4f}")
    print(f"    Formule: k = {k0_M:.3f} · (M_bary/10¹⁰)^{alpha_M:.3f}\n")

    results['M_bary'] = {'k0': k0_M, 'alpha': alpha_M, 'R2': R2_M, 'k_pred': k_pred_M}
except Exception as e:
    print(f"[1] k vs M_bary: ÉCHEC ({e})\n")
    results['M_bary'] = None

# Modèle 2: k = k_0 * (1 + f_gas)^β
try:
    def model_f(f, k0, beta):
        return np.log10(k0) + beta * np.log10(1 + f)

    popt, pcov = curve_fit(model_f, f_gas, np.log10(k_vals), p0=[1.0, 1.0])
    k0_f, beta_f = popt
    err_f = np.sqrt(np.diag(pcov))

    k_pred_f = 10**model_f(f_gas, k0_f, beta_f)
    R2_f = 1 - np.sum((k_vals - k_pred_f)**2) / np.sum((k_vals - k_vals.mean())**2)

    print(f"[2] k = k₀ · (1 + f_gas)^β")
    print(f"    k₀    = {k0_f:.4f} ± {err_f[0]:.4f}")
    print(f"    β     = {beta_f:.4f} ± {err_f[1]:.4f}")
    print(f"    R²    = {R2_f:.4f}")
    print(f"    Formule: k = {k0_f:.3f} · (1 + f_gas)^{beta_f:.3f}\n")

    results['f_gas'] = {'k0': k0_f, 'beta': beta_f, 'R2': R2_f, 'k_pred': k_pred_f}
except Exception as e:
    print(f"[2] k vs f_gas: ÉCHEC ({e})\n")
    results['f_gas'] = None

# Modèle 3: k = k_0 * (M/10^10)^α * (1+f_gas)^β
try:
    def model_comb(X, k0, alpha, beta):
        log_M, f = X
        return np.log10(k0) + alpha * (log_M - 10.0) + beta * np.log10(1 + f)

    popt, pcov = curve_fit(model_comb, [np.log10(M_bary), f_gas], np.log10(k_vals), p0=[1.0, -0.5, 1.0])
    k0_c, alpha_c, beta_c = popt
    err_c = np.sqrt(np.diag(pcov))

    k_pred_c = 10**model_comb([np.log10(M_bary), f_gas], k0_c, alpha_c, beta_c)
    R2_c = 1 - np.sum((k_vals - k_pred_c)**2) / np.sum((k_vals - k_vals.mean())**2)

    print(f"[3] k = k₀ · (M_bary/10¹⁰)^α · (1+f_gas)^β")
    print(f"    k₀    = {k0_c:.4f} ± {err_c[0]:.4f}")
    print(f"    α     = {alpha_c:.4f} ± {err_c[1]:.4f}")
    print(f"    β     = {beta_c:.4f} ± {err_c[2]:.4f}")
    print(f"    R²    = {R2_c:.4f}")
    print(f"    Formule: k = {k0_c:.3f} · (M/10¹⁰)^{alpha_c:.3f} · (1+f_gas)^{beta_c:.3f}\n")

    results['combined'] = {'k0': k0_c, 'alpha': alpha_c, 'beta': beta_c, 'R2': R2_c, 'k_pred': k_pred_c}
except Exception as e:
    print(f"[3] k vs M+f_gas: ÉCHEC ({e})\n")
    results['combined'] = None

# Modèle 4: k = k_0 * (R_disk / 1 kpc)^γ
try:
    def model_R(log_R, k0, gamma):
        return np.log10(k0) + gamma * log_R

    popt, pcov = curve_fit(model_R, np.log10(R_disk), np.log10(k_vals), p0=[1.0, -1.0])
    k0_R, gamma_R = popt
    err_R = np.sqrt(np.diag(pcov))

    k_pred_R = 10**model_R(np.log10(R_disk), k0_R, gamma_R)
    R2_R = 1 - np.sum((k_vals - k_pred_R)**2) / np.sum((k_vals - k_vals.mean())**2)

    print(f"[4] k = k₀ · (R_disk / 1 kpc)^γ")
    print(f"    k₀    = {k0_R:.4f} ± {err_R[0]:.4f}")
    print(f"    γ     = {gamma_R:.4f} ± {err_R[1]:.4f}")
    print(f"    R²    = {R2_R:.4f}")
    print(f"    Formule: k = {k0_R:.3f} · (R_disk/1kpc)^{gamma_R:.3f}\n")

    results['R_disk'] = {'k0': k0_R, 'gamma': gamma_R, 'R2': R2_R, 'k_pred': k_pred_R}
except Exception as e:
    print(f"[4] k vs R_disk: ÉCHEC ({e})\n")
    results['R_disk'] = None

# ==============================================================================
# RÉSULTAT DÉCISIF
# ==============================================================================

print("=" * 80)
print("RÉSULTAT DÉCISIF")
print("=" * 80 + "\n")

# Trouver meilleur modèle
valid_results = {name: res for name, res in results.items() if res is not None}
if valid_results:
    best_name = max(valid_results.items(), key=lambda x: x[1]['R2'])[0]
    best = valid_results[best_name]

    print(f"✓ MEILLEUR MODÈLE: {best_name}")
    print(f"  R² = {best['R2']:.4f} ({best['R2']*100:.1f}% variance expliquée)\n")

    if best_name == 'M_bary':
        print(f"  k = {best['k0']:.3f} · (M_bary / 10¹⁰ M☉)^{best['alpha']:.3f}")
        print(f"\n  CONSTANTE: k₀ = {best['k0']:.4f}")
        print(f"  EXPOSANT:  α  = {best['alpha']:.4f}")
        if abs(best['alpha']) < 0.1:
            print(f"\n  → k QUASI-CONSTANT (|α| < 0.1)")
            print(f"  → Utiliser k ≈ {best['k0']:.2f} pour toutes galaxies")
        elif best['alpha'] < 0:
            print(f"\n  → k DÉCROÎT avec M_bary (α < 0)")
            print(f"  → Galaxies naines: k élevé, géantes: k faible")
        else:
            print(f"\n  → k CROÎT avec M_bary (α > 0)")

    elif best_name == 'f_gas':
        print(f"  k = {best['k0']:.3f} · (1 + f_gas)^{best['beta']:.3f}")
        print(f"\n  CONSTANTE: k₀ = {best['k0']:.4f}")
        print(f"  EXPOSANT:  β  = {best['beta']:.4f}")

    elif best_name == 'R_disk':
        print(f"  k = {best['k0']:.3f} · (R_disk / 1 kpc)^{best['gamma']:.3f}")
        print(f"\n  CONSTANTE: k₀ = {best['k0']:.4f}")
        print(f"  EXPOSANT:  γ  = {best['gamma']:.4f}")

    elif best_name == 'combined':
        print(f"  k = {best['k0']:.3f} · (M/10¹⁰)^{best['alpha']:.3f} · (1+f_gas)^{best['beta']:.3f}")
        print(f"\n  CONSTANTE: k₀ = {best['k0']:.4f}")
        print(f"  α (masse): {best['alpha']:.4f}")
        print(f"  β (gaz):   {best['beta']:.4f}")

    # Scatter
    k_pred_best = best['k_pred']
    residuals = k_vals / k_pred_best
    scatter_orig = k_vals.max() / k_vals.min()
    scatter_res = residuals.max() / residuals.min()

    print(f"\n  Scatter ORIGINAL:  facteur {scatter_orig:.1f}")
    print(f"  Scatter RÉSIDUEL:  facteur {scatter_res:.1f}")
    print(f"  RÉDUCTION SCATTER: {(1 - scatter_res/scatter_orig)*100:.1f}%")

else:
    print("⚠ AUCUN FIT VALIDE")
    print(f"  Utiliser k médian: k = {np.median(k_vals):.3f}")

# ==============================================================================
# VISUALISATIONS
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: k vs M_bary
ax = axes[0, 0]
ax.loglog(M_bary, k_vals, 'o', markersize=10, label='Données')
if results['M_bary']:
    M_range = np.logspace(np.log10(M_bary.min()), np.log10(M_bary.max()), 100)
    k_fit = results['M_bary']['k0'] * (M_range/1e10)**results['M_bary']['alpha']
    ax.plot(M_range, k_fit, 'r-', lw=2, label=f'R²={results["M_bary"]["R2"]:.3f}')
for i, name in enumerate(names):
    ax.annotate(name, (M_bary[i], k_vals[i]), fontsize=8, ha='left')
ax.set_xlabel('M_bary (M☉)', fontsize=12)
ax.set_ylabel('k', fontsize=12)
ax.set_title('k vs Masse Baryonique', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: k vs f_gas
ax = axes[0, 1]
ax.semilogy(f_gas, k_vals, 'o', markersize=10, label='Données')
if results['f_gas']:
    f_range = np.linspace(f_gas.min(), f_gas.max(), 100)
    k_fit = results['f_gas']['k0'] * (1 + f_range)**results['f_gas']['beta']
    ax.plot(f_range, k_fit, 'r-', lw=2, label=f'R²={results["f_gas"]["R2"]:.3f}')
for i, name in enumerate(names):
    ax.annotate(name, (f_gas[i], k_vals[i]), fontsize=8, ha='left')
ax.set_xlabel('f_gas = M_gas / M_bary', fontsize=12)
ax.set_ylabel('k', fontsize=12)
ax.set_title('k vs Fraction Gazeuse', fontsize=13, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: k_pred vs k_obs
ax = axes[1, 0]
if valid_results:
    k_pred_best = valid_results[best_name]['k_pred']
    ax.loglog(k_pred_best, k_vals, 'o', markersize=10)
    lim = [min(k_pred_best.min(), k_vals.min()), max(k_pred_best.max(), k_vals.max())]
    ax.plot(lim, lim, 'k--', lw=2, label='1:1')
    for i, name in enumerate(names):
        ax.annotate(name, (k_pred_best[i], k_vals[i]), fontsize=8, ha='left')
    ax.set_xlabel(f'k prédit ({best_name})', fontsize=12)
    ax.set_ylabel('k observé', fontsize=12)
    ax.set_title(f'Prédiction vs Observation', fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

# Plot 4: Distribution k
ax = axes[1, 1]
ax.bar(names, k_vals, alpha=0.7, edgecolor='black')
ax.axhline(k_vals.mean(), color='red', linestyle='--', lw=2, label=f'Moyenne: {k_vals.mean():.3f}')
ax.set_ylabel('k', fontsize=12)
ax.set_title('Distribution k par galaxie', fontsize=13, fontweight='bold')
ax.set_yscale('log')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('/home/user/Maitrise-du-temps/k_correlation_6galaxies.png', dpi=150, bbox_inches='tight')
print(f"\n  ✓ Graphiques sauvegardés: k_correlation_6galaxies.png\n")
print("=" * 80)
