"""
Test 4 — TMT Falsifiable Prediction: β(z) scale-dependence
Prediction script for DESI BAO validation

Generates:
  1. β_eff(z) prediction curve with 1σ band
  2. Predicted ΔH/H(z) in voids vs clusters
  3. Simulated DESI measurement with noise model
  4. Fisher forecast for β_H0, z_*, α constraints

Usage: python predict_beta_scale_dependence.py
Output: data/results/TEST4_beta_scale_predictions.txt + plots
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
import os

os.makedirs('data/results', exist_ok=True)

# ── Cosmological parameters (Planck 2018) ──────────────────────────────────────
OMEGA_M  = 0.31
OMEGA_L  = 0.69

# ── TMT parameters (from dual-β first-principles derivation) ──────────────────
BETA_H0   = 0.82     # local β (SH0ES measurement, KBC void ρ/ρ_c = 0.7)
BETA_SNIA = 0.001    # integrated β (Pantheon+ LOS average)
Z_STAR    = 0.008    # transition redshift (KBC void extent ~200 Mpc → z~0.05,
                     # but rapid LOS averaging dominates below z~0.05)
ALPHA     = 1.5      # steepness of transition

# Environment density contrasts
RHO_VOID_OVER_RHO_C    = 0.5   # void: ρ/ρ_c = 0.5  → δ = -0.5
RHO_CLUSTER_OVER_RHO_C = 4.0   # cluster: ρ/ρ_c = 4.0 → δ = +3.0

# ── Helper: H²(z) in units of H₀² ────────────────────────────────────────────
def H2_norm(z, rho_over_rhoc, beta):
    """H²(z,ρ)/H₀² from TMT formula with + sign convention."""
    matter = OMEGA_M * (1 + z)**3
    de_eff = OMEGA_L * (1.0 + beta * (1.0 - rho_over_rhoc))
    return matter + de_eff

def H_norm(z, rho_over_rhoc, beta):
    return np.sqrt(H2_norm(z, rho_over_rhoc, beta))

# ── TMT β(z) model ─────────────────────────────────────────────────────────────
def beta_eff(z, beta_h0=BETA_H0, z_star=Z_STAR, alpha=ALPHA):
    """Effective β as function of redshift (first-principles TMT)."""
    return beta_h0 / (1.0 + (z / z_star) ** alpha)

def delta_H_over_H(z, rho_void=RHO_VOID_OVER_RHO_C,
                   rho_clust=RHO_CLUSTER_OVER_RHO_C, **kwargs):
    """
    Fractional difference H_void(z)/H_mean(z) - H_cluster(z)/H_mean(z)
    computed from the full TMT H(z,ρ) formula (proper ΩΛ dilution included).
    """
    b = beta_eff(z, **kwargs)
    H_mean  = H_norm(z, 1.0, b)          # ρ = ρ_c (mean universe)
    H_void  = H_norm(z, rho_void, b)
    H_clust = H_norm(z, rho_clust, b)
    return (H_void - H_clust) / H_mean   # dimensionless ratio

# ── DESI noise model ───────────────────────────────────────────────────────────
def sigma_dH(z, N_gal):
    """1σ uncertainty on ΔH/H from BAO in environment-split sample."""
    sigma_ref = 0.002    # 0.2% at N=500,000, z=0.2
    N_ref     = 500_000
    z_ref     = 0.2
    return sigma_ref * np.sqrt(N_ref / N_gal) * (1 + z) / (1 + z_ref)

# DESI DR1 approximate galaxies per environment bin
desi_bins = [
    {'z': 0.20, 'tracer': 'BGS',  'N_env': 300_000},
    {'z': 0.50, 'tracer': 'LRG',  'N_env': 400_000},
    {'z': 1.00, 'tracer': 'ELG',  'N_env': 600_000},
]

# ── 1. Prediction curve ────────────────────────────────────────────────────────
z_arr  = np.linspace(0.001, 2.5, 500)
b_arr  = beta_eff(z_arr)
dH_arr = np.array([delta_H_over_H(z) for z in z_arr]) * 100   # percent

# Uncertainty band: propagate σ(z_*) = ±0.003 and σ(α) = ±0.3
b_up  = beta_eff(z_arr, z_star=Z_STAR * 0.7, alpha=ALPHA + 0.3)
b_lo  = beta_eff(z_arr, z_star=Z_STAR * 1.4, alpha=ALPHA - 0.3)
dH_up = np.array([delta_H_over_H(z, **{'beta_h0': BETA_H0,
              'z_star': Z_STAR*0.7, 'alpha': ALPHA+0.3}) for z in z_arr]) * 100
dH_lo = np.array([delta_H_over_H(z, **{'beta_h0': BETA_H0,
              'z_star': Z_STAR*1.4, 'alpha': ALPHA-0.3}) for z in z_arr]) * 100

# ── 2. DESI simulated measurement ──────────────────────────────────────────────
rng = np.random.default_rng(7)
desi_results = []
for bin_info in desi_bins:
    z    = bin_info['z']
    pred = delta_H_over_H(z) * 100
    sig  = sigma_dH(z, bin_info['N_env']) * 100
    meas = rng.normal(pred, sig)
    sn   = pred / sig if sig > 0 else 0
    desi_results.append({
        'z': z, 'tracer': bin_info['tracer'],
        'predicted': pred, 'measured': meas,
        'sigma': sig, 'SN': sn,
        'N_env': bin_info['N_env']
    })

# ── 3. Fisher forecast ─────────────────────────────────────────────────────────
def fisher_forecast(desi_res, params0=(BETA_H0, Z_STAR, ALPHA), eps_rel=0.01):
    """3-parameter Fisher matrix: (beta_h0, z_star, alpha)."""
    b0, zs0, a0 = params0
    F = np.zeros((3, 3))
    for dr in desi_res:
        z, sig = dr['z'], dr['sigma'] / 100
        if sig == 0:
            continue
        def pred(b, zs, a):
            return delta_H_over_H(z, **{'beta_h0': b, 'z_star': zs, 'alpha': a})
        eps_b  = b0  * eps_rel
        eps_zs = zs0 * eps_rel
        eps_a  = a0  * eps_rel
        dP_db  = (pred(b0+eps_b, zs0, a0)  - pred(b0-eps_b, zs0, a0))  / (2*eps_b)
        dP_dzs = (pred(b0, zs0+eps_zs, a0) - pred(b0, zs0-eps_zs, a0)) / (2*eps_zs)
        dP_da  = (pred(b0, zs0, a0+eps_a)  - pred(b0, zs0, a0-eps_a))  / (2*eps_a)
        grad   = np.array([dP_db, dP_dzs, dP_da])
        F     += np.outer(grad, grad) / sig**2
    cov = np.linalg.inv(F)
    return cov

cov = fisher_forecast(desi_results)
sig_b0, sig_zs, sig_a = np.sqrt(np.diag(cov))

# ── 4. Save results ────────────────────────────────────────────────────────────
out = []
out.append("=" * 65)
out.append("TMT TEST 4 — β(z) SCALE-DEPENDENCE: DESI BAO PREDICTION")
out.append("=" * 65)
out.append(f"\nTMT model: β_eff(z) = β_H0 / (1 + (z/z_*)^α)")
out.append(f"  β_H0 = {BETA_H0}  (SH0ES, local KBC void z < 0.04)")
out.append(f"  z_*  = {Z_STAR}  (rapid LOS averaging transition scale)")
out.append(f"  α    = {ALPHA}  (steepness of transition)")
out.append(f"  ΔH/H(z) computed from full TMT H(z,ρ) formula (ΩΛ dilution included)\n")

out.append("─" * 65)
out.append("PREDICTED β_eff AND ΔH/H BY REDSHIFT")
out.append("  (H_void vs H_cluster, ρ_void/ρ_c=0.5, ρ_clust/ρ_c=4.0)")
out.append("─" * 65)
out.append(f"{'z':>6} {'β_eff':>10} {'ΔH/H (%)':>12}")
for z in [0.01, 0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 1.00, 1.50, 2.00]:
    b  = beta_eff(z)
    dH = delta_H_over_H(z) * 100
    out.append(f"{z:>6.2f} {b:>10.5f} {dH:>12.4f}")

out.append("\n" + "─" * 65)
out.append("DESI DR1 SIMULATED MEASUREMENTS")
out.append("─" * 65)
out.append(f"{'z':>5} {'Tracer':>6} {'N_env':>10} {'Pred (%)':>10} "
           f"{'Meas (%)':>10} {'σ (%)':>8} {'S/N':>6}")
for dr in desi_results:
    out.append(f"{dr['z']:>5.2f} {dr['tracer']:>6} {dr['N_env']:>10,} "
               f"{dr['predicted']:>10.4f} {dr['measured']:>10.4f} "
               f"{dr['sigma']:>8.4f} {dr['SN']:>6.2f}")

out.append("\n" + "─" * 65)
out.append("FISHER FORECAST — PARAMETER CONSTRAINTS (DESI DR1)")
out.append("─" * 65)
out.append(f"  σ(β_H0) = {sig_b0:.4f}  ({sig_b0/BETA_H0*100:.1f}% relative)")
out.append(f"  σ(z_*)  = {sig_zs:.5f}")
out.append(f"  σ(α)    = {sig_a:.4f}")

out.append("\n" + "─" * 65)
out.append("FALSIFICATION CRITERIA")
out.append("─" * 65)
dH_z02 = delta_H_over_H(0.2) * 100
dH_z05 = delta_H_over_H(0.5) * 100
out.append(f"  TMT predicts ΔH/H(z=0.20) = {dH_z02:.4f}%")
out.append(f"  TMT predicts ΔH/H(z=0.50) = {dH_z05:.4f}%")
out.append(f"  TMT FALSIFIED if ΔH/H(z=0.2) > 2.0% or < -0.1%")
out.append(f"  TMT FALSIFIED if β(z) shows NO monotonic decrease")
out.append(f"  TMT SUPPORTED if ΔH/H(z=0.2) in [{dH_z02*0.4:.3f}%, {dH_z02*2.0:.3f}%] at >2σ")

report = "\n".join(out)
print(report)
with open('data/results/TEST4_beta_scale_predictions.txt', 'w') as f:
    f.write(report)

# ── 5. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('TMT Test 4 — β(z) Scale-Dependence: DESI BAO Prediction', fontsize=13)

# Plot 1: β_eff(z)
ax = axes[0]
ax.fill_between(z_arr, b_lo, b_up, alpha=0.2, color='steelblue')
ax.semilogy(z_arr, b_arr, 'steelblue', lw=2.5, label=f'TMT (z_*={Z_STAR})')
ax.axhline(BETA_SNIA, color='gray', ls='--', lw=1.5, label=f'β_SNIa={BETA_SNIA}')
ax.axhline(BETA_H0, color='red', ls=':', lw=1.5, label=f'β_H0={BETA_H0}')
ax.axvline(Z_STAR, color='green', ls=':', alpha=0.5, label=f'z_*={Z_STAR}')
ax.set_xlabel('Redshift z')
ax.set_ylabel('β_eff(z)')
ax.set_title('Effective β vs redshift')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 0.5)

# Plot 2: ΔH/H prediction + DESI simulated points
ax = axes[1]
mask = z_arr < 1.6
ax.fill_between(z_arr[mask], dH_lo[mask], dH_up[mask], alpha=0.2, color='steelblue')
ax.plot(z_arr[mask], dH_arr[mask], 'steelblue', lw=2.5, label='TMT prediction')
ax.axhline(0, color='gray', ls='--', lw=1, label='ΛCDM (zero)')
colors = ['tomato', 'orange', 'purple']
for dr, col in zip(desi_results, colors):
    ax.errorbar(dr['z'], dr['measured'], yerr=dr['sigma'],
                fmt='o', color=col, ms=8, capsize=4, zorder=5,
                label=f"DESI {dr['tracer']} S/N={dr['SN']:.1f}σ")
ax.set_xlabel('Redshift z')
ax.set_ylabel('ΔH/H (%) [void − cluster]')
ax.set_title('H(z) void vs cluster offset')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# Plot 3: Constraint ellipse β_H0 vs z_*
ax = axes[2]
cov2  = cov[:2, :2]
vals, vecs = np.linalg.eigh(cov2)
from matplotlib.patches import Ellipse
for nsig, alpha_e, label in [(1, 0.4, '1σ'), (2, 0.2, '2σ')]:
    w_el = 2 * nsig * np.sqrt(vals[1])
    h_el = 2 * nsig * np.sqrt(vals[0])
    angle = np.degrees(np.arctan2(vecs[1,1], vecs[0,1]))
    e = Ellipse(xy=(BETA_H0, Z_STAR), width=w_el, height=h_el,
                angle=angle, color='steelblue', alpha=alpha_e, label=label)
    ax.add_patch(e)
ax.plot(BETA_H0, Z_STAR, 'k+', ms=12, mew=2, label='TMT true value')
ax.set_xlabel('β_H0')
ax.set_ylabel('z_* (transition redshift)')
ax.set_title(f'Fisher forecast (DESI DR1)\nσ(β_H0)={sig_b0:.3f}, σ(z_*)={sig_zs:.4f}')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('data/results/TEST4_beta_scale_predictions.png', dpi=150, bbox_inches='tight')
print("\nPlot saved: data/results/TEST4_beta_scale_predictions.png")
print("Report saved: data/results/TEST4_beta_scale_predictions.txt")

Generates:
  1. β_eff(z) prediction curve with 1σ band
  2. Predicted ΔH/H(z) in voids vs clusters
  3. Simulated DESI measurement with noise model
  4. Fisher forecast for β_H0, z_*, α constraints

Usage: python predict_beta_scale_dependence.py
Output: data/results/TEST4_beta_scale_predictions.txt + plots
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
import os

os.makedirs('data/results', exist_ok=True)

# ── TMT parameters (from dual-β first-principles derivation) ──────────────────
BETA_H0   = 0.82     # local β (SH0ES measurement)
BETA_SNIA = 0.001    # integrated β (Pantheon+)
Z_STAR    = 0.08     # transition redshift
ALPHA     = 1.5      # steepness of transition

# Environment parameters
DELTA_VOID    = -0.5   # typical void contrast
DELTA_CLUSTER = +3.0   # typical cluster contrast
DELTA_DIFF    = DELTA_CLUSTER - DELTA_VOID   # = 3.5

# ── TMT β(z) model ─────────────────────────────────────────────────────────────
def beta_eff(z, beta_h0=BETA_H0, z_star=Z_STAR, alpha=ALPHA):
    """Effective β as function of redshift (first-principles TMT)."""
    return beta_h0 / (1.0 + (z / z_star) ** alpha)

def delta_H_over_H(z, **kwargs):
    """Predicted ΔH/H = H_void/H_mean - H_cluster/H_mean."""
    b = beta_eff(z, **kwargs)
    dH_void    = b * (1.0 - (1.0 + DELTA_VOID))      # = b × |δ_void|
    dH_cluster = b * (1.0 - (1.0 + DELTA_CLUSTER))   # = -b × δ_cluster
    return dH_void - dH_cluster   # positive: voids expand faster

# ── DESI noise model ───────────────────────────────────────────────────────────
# σ(ΔH/H) from BAO peak measurement, approximate scaling
def sigma_dH(z, N_gal):
    """
    1σ uncertainty on ΔH/H from BAO in environment-split sample.
    Rough Fisher estimate: sigma proportional to 1/sqrt(N) at fixed BAO S/N per galaxy.
    """
    # Baseline: σ = 0.20% at z=0.2, N=500,000 per environment
    sigma_ref = 0.002   # 0.2%
    N_ref     = 500_000
    z_ref     = 0.2
    # Scale with N and z (higher z → fewer usable modes, larger σ)
    sigma = sigma_ref * np.sqrt(N_ref / N_gal) * (1 + z) / (1 + z_ref)
    return sigma

# DESI DR1 approximate number of galaxies per environment bin
desi_bins = [
    {'z': 0.20, 'tracer': 'BGS',  'N_env': 300_000},
    {'z': 0.50, 'tracer': 'LRG',  'N_env': 400_000},
    {'z': 1.00, 'tracer': 'ELG',  'N_env': 600_000},
]

# ── 1. Prediction curve ────────────────────────────────────────────────────────
z_arr  = np.linspace(0.001, 2.5, 500)
b_arr  = beta_eff(z_arr)
dH_arr = delta_H_over_H(z_arr) * 100   # in percent

# Uncertainty band: propagate σ(z_*) = ±0.03 and σ(α) = ±0.3
b_up = beta_eff(z_arr, z_star=Z_STAR - 0.03, alpha=ALPHA + 0.3)
b_lo = beta_eff(z_arr, z_star=Z_STAR + 0.03, alpha=ALPHA - 0.3)
dH_up = (b_up * DELTA_DIFF) * 100
dH_lo = (b_lo * DELTA_DIFF) * 100
dH_cen = (b_arr * DELTA_DIFF) * 100

# ── 2. DESI simulated measurement ──────────────────────────────────────────────
rng = np.random.default_rng(7)
desi_results = []
for bin_info in desi_bins:
    z    = bin_info['z']
    pred = delta_H_over_H(z) * 100
    sig  = sigma_dH(z, bin_info['N_env']) * 100
    meas = rng.normal(pred, sig)
    sn   = pred / sig
    desi_results.append({
        'z': z, 'tracer': bin_info['tracer'],
        'predicted': pred, 'measured': meas,
        'sigma': sig, 'SN': sn,
        'N_env': bin_info['N_env']
    })

# ── 3. Fisher forecast ─────────────────────────────────────────────────────────
def fisher_forecast(desi_res, params0=(BETA_H0, Z_STAR, ALPHA), eps=1e-4):
    """3-parameter Fisher matrix: (beta_h0, z_star, alpha)."""
    b0, zs0, a0 = params0
    F = np.zeros((3, 3))
    for dr in desi_res:
        z, sig = dr['z'], dr['sigma'] / 100
        # Partial derivatives (numerical)
        def pred(b, zs, a):
            return (b / (1 + (z/zs)**a)) * DELTA_DIFF
        dP_db  = (pred(b0+eps, zs0, a0)   - pred(b0-eps, zs0, a0))   / (2*eps)
        dP_dzs = (pred(b0, zs0+eps, a0)   - pred(b0, zs0-eps, a0))   / (2*eps)
        dP_da  = (pred(b0, zs0, a0+eps)   - pred(b0, zs0, a0-eps))   / (2*eps)
        grad   = np.array([dP_db, dP_dzs, dP_da])
        F     += np.outer(grad, grad) / sig**2
    cov = np.linalg.inv(F)
    return cov

cov = fisher_forecast(desi_results)
sig_b0, sig_zs, sig_a = np.sqrt(np.diag(cov))

# ── 4. Save results ────────────────────────────────────────────────────────────
out = []
out.append("=" * 65)
out.append("TMT TEST 4 — β(z) SCALE-DEPENDENCE: DESI BAO PREDICTION")
out.append("=" * 65)
out.append(f"\nTMT model: β_eff(z) = β_H0 / (1 + (z/z_*)^α)")
out.append(f"  β_H0 = {BETA_H0}  (SH0ES, local KBC void)")
out.append(f"  z_*  = {Z_STAR}  (transition redshift)")
out.append(f"  α    = {ALPHA}  (steepness)")
out.append(f"\nΔH/H(z) = β_eff(z) × (δ_cluster − δ_void) = β_eff × {DELTA_DIFF:.1f}\n")

out.append("─" * 65)
out.append("PREDICTED β_eff AND ΔH/H BY REDSHIFT")
out.append("─" * 65)
out.append(f"{'z':>6} {'β_eff':>8} {'ΔH/H (%)':>10}")
for z in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
    b = beta_eff(z)
    dH = b * DELTA_DIFF * 100
    out.append(f"{z:>6.2f} {b:>8.4f} {dH:>10.3f}")

out.append("\n" + "─" * 65)
out.append("DESI DR1 SIMULATED MEASUREMENTS")
out.append("─" * 65)
out.append(f"{'z':>5} {'Tracer':>6} {'N_env':>10} {'Pred (%)':>10} "
           f"{'Meas (%)':>10} {'σ (%)':>8} {'S/N':>6}")
for dr in desi_results:
    out.append(f"{dr['z']:>5.2f} {dr['tracer']:>6} {dr['N_env']:>10,} "
               f"{dr['predicted']:>10.4f} {dr['measured']:>10.4f} "
               f"{dr['sigma']:>8.4f} {dr['SN']:>6.2f}")

out.append("\n" + "─" * 65)
out.append("FISHER FORECAST — PARAMETER CONSTRAINTS (DESI DR1)")
out.append("─" * 65)
out.append(f"  σ(β_H0) = {sig_b0:.4f}  ({sig_b0/BETA_H0*100:.1f}% relative)")
out.append(f"  σ(z_*)  = {sig_zs:.4f}")
out.append(f"  σ(α)    = {sig_a:.4f}")

out.append("\n" + "─" * 65)
out.append("FALSIFICATION CRITERIA")
out.append("─" * 65)
out.append("  TMT FALSIFIED if ΔH/H(z=0.2) < -0.5% or > 2.0%")
out.append("  TMT FALSIFIED if β(z) shows NO monotonic decrease (flat)")
out.append("  TMT SUPPORTED if 0.3% < ΔH/H(z=0.2) < 1.2% at >2σ")
out.append("  TMT SUPPORTED if β(z=1.0) < 0.1 at >2σ below β(z=0.2)")

report = "\n".join(out)
print(report)
with open('data/results/TEST4_beta_scale_predictions.txt', 'w') as f:
    f.write(report)

# ── 5. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('TMT Test 4 — β(z) Scale-Dependence: DESI BAO Prediction', fontsize=13)

# Plot 1: β_eff(z)
ax = axes[0]
ax.fill_between(z_arr, b_lo, b_up, alpha=0.2, color='steelblue', label='1σ band')
ax.semilogy(z_arr, b_arr, 'steelblue', lw=2.5, label=f'TMT: β_H0={BETA_H0}')
ax.axhline(BETA_SNIA, color='gray', ls='--', lw=1.5, label=f'β_SNIa={BETA_SNIA}')
ax.axhline(BETA_H0, color='red', ls=':', lw=1.5, label=f'β_H0={BETA_H0}')
ax.set_xlabel('Redshift z')
ax.set_ylabel('β_eff(z)')
ax.set_title('Effective β vs redshift')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 2.5)

# Plot 2: ΔH/H prediction + DESI simulated points
ax = axes[1]
ax.fill_between(z_arr, dH_lo, dH_up, alpha=0.2, color='steelblue')
ax.plot(z_arr, dH_cen, 'steelblue', lw=2.5, label='TMT prediction')
ax.axhline(0, color='gray', ls='--', lw=1, label='ΛCDM (zero)')
for dr in desi_results:
    ax.errorbar(dr['z'], dr['measured'], yerr=dr['sigma'],
                fmt='o', color='tomato', ms=8, capsize=4, zorder=5,
                label=f"DESI {dr['tracer']} (S/N={dr['SN']:.1f}σ)")
ax.set_xlabel('Redshift z')
ax.set_ylabel('ΔH/H (%) [void − cluster]')
ax.set_title('H(z) void vs cluster offset')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1.5)

# Plot 3: Constraint ellipse β_H0 vs z_*
ax = axes[2]
theta = np.linspace(0, 2*np.pi, 300)
cov2  = cov[:2, :2]
vals, vecs = np.linalg.eigh(cov2)
w, h_ell  = 2*np.sqrt(vals[1]), 2*np.sqrt(vals[0])
angle     = np.degrees(np.arctan2(vecs[1,1], vecs[0,1]))
from matplotlib.patches import Ellipse
for nsig, alpha_e, label in [(1, 0.4, '1σ'), (2, 0.2, '2σ')]:
    e = Ellipse(xy=(BETA_H0, Z_STAR),
                width=nsig*w, height=nsig*h_ell, angle=angle,
                color='steelblue', alpha=alpha_e, label=label)
    ax.add_patch(e)
ax.plot(BETA_H0, Z_STAR, 'k+', ms=12, mew=2, label='TMT prediction')
ax.set_xlabel('β_H0')
ax.set_ylabel('z_*')
ax.set_title(f'Fisher forecast (DESI DR1)\nσ(β_H0)={sig_b0:.3f}, σ(z_*)={sig_zs:.3f}')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0.3, 1.4)
ax.set_ylim(0.0, 0.20)

plt.tight_layout()
plt.savefig('data/results/TEST4_beta_scale_predictions.png', dpi=150, bbox_inches='tight')
print("\nPlot saved: data/results/TEST4_beta_scale_predictions.png")
print("Report saved: data/results/TEST4_beta_scale_predictions.txt")
