"""
Test 1 — TMT Falsifiable Prediction: r_c ∝ M^0.56
Prediction script for Euclid/DESI validation

Generates:
  1. r_c vs M_bary prediction curve with 1σ uncertainty band
  2. Monte Carlo simulated Euclid sample (N=50,000) + slope recovery
  3. TMT vs ΛCDM comparison for r_s(M_bary)
  4. Statistical power analysis

Usage: python predict_rc_mass_euclid_desi.py
Output: data/results/TEST1_rc_mass_predictions.txt + plots
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import os

# ── TMT parameters (calibrated on 103 SPARC galaxies) ─────────────────────────
RC_NORM    = 2.6      # kpc at 10^10 M_sun
RC_SLOPE   = 0.56     # exponent
RC_SCATTER = 0.25     # dex (1σ, from SPARC residuals)
N_REF_MASS = 1e10     # M_sun reference mass

# ΛCDM comparison: r_s ~ r_200 / c, c ∝ M_halo^(-0.1)
# Using baryonic mass proxy M_halo ≈ M_bary / f_bar with f_bar = 0.05
FBAR       = 0.05
RS_NORM    = 5.0      # kpc at 10^10 M_sun (baryonic), rough ΛCDM expectation
RS_SLOPE   = 0.43     # ∝ M_halo^0.43 ∝ M_bary^0.43

os.makedirs('data/results', exist_ok=True)

# ── 1. Prediction curve ────────────────────────────────────────────────────────
M_arr = np.logspace(6.5, 12, 200)  # M_sun

rc_tmt   = RC_NORM  * (M_arr / N_REF_MASS) ** RC_SLOPE
rc_upper = rc_tmt * 10 ** RC_SCATTER
rc_lower = rc_tmt * 10 ** (-RC_SCATTER)

rs_lcdm  = RS_NORM  * (M_arr / N_REF_MASS) ** RS_SLOPE
rs_upper = rs_lcdm * 2.0
rs_lower = rs_lcdm * 0.5

# ── 2. Monte Carlo Euclid sample ───────────────────────────────────────────────
N_EUCLID = 50_000
rng = np.random.default_rng(42)

# Draw galaxy masses (log-normal mass function, Schechter-like)
logM_euclid = rng.normal(loc=9.5, scale=0.9, size=N_EUCLID)
logM_euclid = np.clip(logM_euclid, 7.5, 11.8)
M_euclid    = 10 ** logM_euclid

# True r_c from TMT + scatter
logrc_true  = np.log10(RC_NORM) + RC_SLOPE * (logM_euclid - 10.0)
logrc_obs   = logrc_true + rng.normal(0, RC_SCATTER, N_EUCLID)
rc_euclid   = 10 ** logrc_obs

# Recover slope via linear regression
slope, intercept, r_val, p_val, se = stats.linregress(logM_euclid, logrc_obs)

# ── 3. Statistical power analysis ─────────────────────────────────────────────
def power_to_detect(N, slope_true=RC_SLOPE, slope_null=RS_SLOPE,
                    scatter=RC_SCATTER, logM_std=0.9):
    """Probability of rejecting ΛCDM slope given TMT is true."""
    se_slope = scatter / (np.sqrt(N) * logM_std)
    delta     = abs(slope_true - slope_null)
    t_stat    = delta / se_slope
    from scipy.stats import norm
    power = 1 - norm.cdf(1.645 - t_stat) + norm.cdf(-1.645 - t_stat)
    return power, se_slope, t_stat

N_values = [100, 500, 1000, 5000, 10000, 50000]
powers   = []
for N in N_values:
    p, se_s, t = power_to_detect(N)
    powers.append((N, p, se_s, t))

# ── 4. Prediction table by mass bin ───────────────────────────────────────────
mass_bins   = [1e7, 1e8, 1e9, 1e10, 1e11, 3e11]
bin_labels  = ['10^7', '10^8', '10^9', '10^10', '10^11', '3×10^11']
n_expected  = [2000, 5000, 15000, 20000, 8000, 1000]

# ── 5. Save results ────────────────────────────────────────────────────────────
out = []
out.append("=" * 65)
out.append("TMT TEST 1 — r_c(M) PREDICTION FOR EUCLID/DESI")
out.append("=" * 65)
out.append(f"\nTMT calibration (SPARC, N=103):")
out.append(f"  r_c = {RC_NORM} × (M_bary/10^10)^{RC_SLOPE} kpc")
out.append(f"  Pearson r = 0.768, p = 3×10^-21")
out.append(f"  Intrinsic scatter σ_lnrc = {RC_SCATTER} dex\n")

out.append("─" * 65)
out.append("PREDICTION TABLE BY MASS BIN")
out.append("─" * 65)
out.append(f"{'M_bary':>12} {'N_Euclid':>10} {'r_c TMT (kpc)':>15} "
           f"{'r_s ΛCDM (kpc)':>16}")
for mb, lb, ne in zip(mass_bins, bin_labels, n_expected):
    rc = RC_NORM * (mb / N_REF_MASS) ** RC_SLOPE
    rs = RS_NORM * (mb / N_REF_MASS) ** RS_SLOPE
    out.append(f"{lb:>12} {ne:>10} {rc:>15.3f} {rs:>16.3f}")

out.append("\n" + "─" * 65)
out.append("MONTE CARLO EUCLID RECOVERY (N=50,000)")
out.append("─" * 65)
out.append(f"  Input slope  : {RC_SLOPE:.4f}")
out.append(f"  Recovered    : {slope:.4f} ± {se:.4f}")
out.append(f"  Pearson r    : {r_val:.4f}  (p = {p_val:.2e})")
out.append(f"  Intercept    : {intercept:.4f}  (expected {np.log10(RC_NORM):.4f})")

out.append("\n" + "─" * 65)
out.append("STATISTICAL POWER ANALYSIS")
out.append("  (probability of rejecting ΛCDM slope 0.43 when TMT slope 0.56 is true)")
out.append("─" * 65)
out.append(f"{'N_galaxies':>12} {'Power':>8} {'σ_slope':>10} {'t-stat':>8}")
for N, p, se_s, t in powers:
    out.append(f"{N:>12d} {p:>8.4f} {se_s:>10.4f} {t:>8.2f}")

out.append("\n" + "─" * 65)
out.append("FALSIFICATION CRITERION")
out.append("─" * 65)
out.append("  TMT is FALSIFIED if measured slope outside [0.46, 0.66]")
out.append("  TMT is FALSIFIED if Pearson r(M_bary) < 0.3 at N > 1000")
out.append("  TMT is SUPPORTED if slope ∈ [0.50, 0.62] AND r > 0.6")

report = "\n".join(out)
print(report)

with open('data/results/TEST1_rc_mass_predictions.txt', 'w') as f:
    f.write(report)

# ── 6. Plots ───────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('TMT Test 1 — r_c ∝ M^0.56: Euclid/DESI Prediction', fontsize=13)

# Plot 1: r_c vs M (prediction curves)
ax = axes[0]
ax.fill_between(M_arr, rc_lower, rc_upper, alpha=0.25, color='steelblue', label='TMT 1σ')
ax.loglog(M_arr, rc_tmt,  color='steelblue', lw=2, label=f'TMT: slope={RC_SLOPE}')
ax.fill_between(M_arr, rs_lower, rs_upper, alpha=0.15, color='tomato')
ax.loglog(M_arr, rs_lcdm, color='tomato',    lw=2, ls='--', label=f'ΛCDM: slope={RS_SLOPE}')
ax.set_xlabel('M_bary (M_☉)')
ax.set_ylabel('r_c (kpc)')
ax.set_title('TMT vs ΛCDM prediction')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Plot 2: Monte Carlo Euclid recovery
ax = axes[1]
h = ax.hexbin(logM_euclid, logrc_obs, gridsize=50, cmap='Blues', mincnt=1)
xfit = np.linspace(7.5, 11.8, 100)
ax.plot(xfit, intercept + slope * xfit, 'r-', lw=2,
        label=f'Fit: slope={slope:.3f}±{se:.3f}')
ax.plot(xfit, np.log10(RC_NORM) + RC_SLOPE * (xfit - 10), 'k--', lw=1.5,
        label=f'True: slope={RC_SLOPE}')
plt.colorbar(h, ax=ax, label='N galaxies')
ax.set_xlabel('log M_bary (M_☉)')
ax.set_ylabel('log r_c (kpc)')
ax.set_title(f'Euclid MC recovery (N={N_EUCLID:,})\nr={r_val:.4f}, p={p_val:.2e}')
ax.legend(fontsize=8)

# Plot 3: Statistical power curve
ax = axes[2]
N_plot  = np.logspace(2, 5.5, 200)
pwr_arr = [power_to_detect(int(n))[0] for n in N_plot]
ax.semilogx(N_plot, pwr_arr, 'steelblue', lw=2)
ax.axhline(0.95, color='red', ls='--', label='95% power')
ax.axhline(0.99, color='darkred', ls=':', label='99% power')
N95 = N_plot[np.argmin(np.abs(np.array(pwr_arr) - 0.95))]
ax.axvline(N95, color='red', ls='--', alpha=0.5)
ax.text(N95 * 1.1, 0.5, f'N={int(N95):,}\nfor 95% power', fontsize=8, color='red')
ax.set_xlabel('Number of galaxies')
ax.set_ylabel('Power (prob. reject ΛCDM slope)')
ax.set_title('Statistical power: TMT vs ΛCDM')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 1.05)

plt.tight_layout()
plt.savefig('data/results/TEST1_rc_mass_predictions.png', dpi=150, bbox_inches='tight')
print("\nPlot saved: data/results/TEST1_rc_mass_predictions.png")
print("Report saved: data/results/TEST1_rc_mass_predictions.txt")
