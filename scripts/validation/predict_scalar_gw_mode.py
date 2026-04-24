"""
Test 5 - TMT Falsifiable Prediction: Scalar GW breathing mode
Prediction script for LISA validation

Generates:
  1. h_scalar/h_tensor vs xi*v^2 and source parameters
  2. LISA SNR prediction vs N_events stacked
  3. Sensitivity comparison: TMT prediction vs LIGO/LISA/ET curves

Usage: python predict_scalar_gw_mode.py
Output: data/results/TEST5_scalar_gw_predictions.txt + plots
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('data/results', exist_ok=True)

# ── Physical constants ─────────────────────────────────────────────────────────
G  = 6.674e-11   # m^3 kg^-1 s^-2
c  = 3e8         # m/s
M_sun = 1.989e30 # kg
Mpc   = 3.086e22 # m
pc    = 3.086e16 # m
hbar  = 1.055e-34  # J s
eV    = 1.602e-19  # J

# ── TMT parameters ─────────────────────────────────────────────────────────────
XI_V2_MIN = 1e-8   # lower bound (naturalness)
XI_V2_MAX = 1e-5   # upper bound (PPN / Cassini constraint)
M_PSI_EV  = 1e-33  # temporon mass in eV (cosmological scale: m ~ H_0/c^2)

# ── LISA noise model (simplified) ──────────────────────────────────────────────
def S_n_LISA(f):
    """LISA sky-averaged noise PSD [1/Hz], approximate."""
    f_star = 3e-3  # Hz
    S_acc  = 9e-50 * (1 + (0.4e-3/f)**2) * (1 + (f/8e-3)**4) / f**4
    S_opt  = 2.96e-45 * (1 + (f/f_star)**2)
    S_conf = 1.14e-44 * f**(-7/3) * np.exp(-f**0.138 - 0.11*f*np.sin(2.9*f))
    return S_acc + S_opt + S_conf

def h_noise_LISA(f):
    """LISA strain sensitivity [1/sqrt(Hz)]."""
    return np.sqrt(S_n_LISA(f))

# LIGO O4 approximate sensitivity
def h_noise_LIGO(f):
    return 3e-24 * np.sqrt((20/f)**4 + 1 + (f/200)**2)

# Einstein Telescope approximate
def h_noise_ET(f):
    return 3e-25 * np.sqrt((5/f)**4 + 1 + (f/500)**2)

# ── GW strain calculations ──────────────────────────────────────────────────────
def h_tensor(M_chirp_Msun, d_Mpc, f_Hz):
    """Peak tensor strain from compact binary at frequency f."""
    M  = M_chirp_Msun * M_sun
    d  = d_Mpc * Mpc
    return 4 * G * M * (np.pi * f_Hz)**(2/3) / (c**2 * d) * (G*M/c**3)**(2/3)

def h_scalar_ratio_A(xi_v2, compactness):
    """
    Channel A: strong-field coupling, h_s/h_t ~ xi_v2 * compactness
    compactness = GM/(c^2 R) ~ 0.5 for BH
    """
    return np.sqrt(xi_v2) * compactness

def h_scalar_ratio_B(xi_v2, f_Hz, m_psi_eV):
    """
    Channel B: curvature-sourced, h_s/h_t ~ xi_v2 * (f/f_compton)^2
    f_compton = m_psi c^2 / h
    """
    f_compton = m_psi_eV * eV / (hbar * 2 * np.pi)  # Hz
    if f_Hz < f_compton:
        return xi_v2 * (f_Hz / f_compton)**2
    else:
        return np.sqrt(xi_v2)  # saturates at sqrt(xi_v2)

def h_scalar_ratio(xi_v2, f_Hz, compactness, m_psi_eV=M_PSI_EV):
    """Total scalar/tensor ratio: max of channel A and B."""
    A = h_scalar_ratio_A(xi_v2, compactness)
    B = h_scalar_ratio_B(xi_v2, f_Hz, m_psi_eV)
    return max(A, B)

# ── LISA SNR model ──────────────────────────────────────────────────────────────
def snr_tensor_LISA(M_chirp_Msun, d_Mpc, T_obs=4.0):
    """Approximate integrated SNR for tensor modes with LISA."""
    f_peak = 1e-3 / (M_chirp_Msun / 1e6)   # Hz, approximate ISCO freq
    f_peak = np.clip(f_peak, 1e-4, 0.1)
    h = h_tensor(M_chirp_Msun, d_Mpc, f_peak)
    Sn = S_n_LISA(f_peak)
    return h**2 * T_obs * 365.25 * 86400 / Sn

def snr_scalar_LISA(xi_v2, M_chirp_Msun, d_Mpc, compactness=0.5, T_obs=4.0):
    """Scalar mode SNR for LISA (single event)."""
    f_peak  = 1e-3 / (M_chirp_Msun / 1e6)
    f_peak  = np.clip(f_peak, 1e-4, 0.1)
    ratio   = h_scalar_ratio(xi_v2, f_peak, compactness)
    snr_t   = snr_tensor_LISA(M_chirp_Msun, d_Mpc, T_obs)
    eta_s   = 0.3   # LISA scalar polarisation efficiency
    return ratio * np.sqrt(snr_t) * eta_s

# ── Source catalogue ────────────────────────────────────────────────────────────
sources = [
    {'name': 'SMBH 10^6 Msun @ 1 Gpc', 'M': 1e6, 'd': 1000, 'C': 0.4},
    {'name': 'SMBH 10^7 Msun @ 1 Gpc', 'M': 1e7, 'd': 1000, 'C': 0.45},
    {'name': 'SMBH 10^6 Msun @ 100 Mpc','M': 1e6, 'd': 100,  'C': 0.4},
    {'name': 'EMRI 10^6+10 @ 500 Mpc',  'M': 32,  'd': 500,  'C': 0.2},
    {'name': 'Stellar BH @ 400 Mpc',    'M': 30,  'd': 400,  'C': 0.4},
]

xi_v2_vals = np.logspace(-8, -5, 4)

# ── Report generation ──────────────────────────────────────────────────────────
out = []
out.append("=" * 72)
out.append("TMT TEST 5 — SCALAR GW BREATHING MODE: LISA PREDICTION")
out.append("=" * 72)
out.append(f"\nTMT prediction: h_scalar/h_tensor from temporon field δψ")
out.append(f"  PPN constraint: xi*v^2 < 1e-5 (Cassini)")
out.append(f"  Temporon mass : m_psi ~ {M_PSI_EV:.0e} eV (cosmological scale)")
out.append(f"\nChannel A (strong-field): h_s/h_t ~ sqrt(xi*v^2) * compactness")
out.append(f"Channel B (curvature)   : h_s/h_t ~ xi*v^2 * (f/f_compton)^2")
out.append(f"                          f_compton = m_psi*c^2/h ~ {M_PSI_EV*eV/(hbar*2*np.pi):.2e} Hz\n")

out.append("─" * 72)
out.append("h_scalar/h_tensor FOR LISA SOURCES (Channel A dominant)")
out.append("─" * 72)
header = f"{'Source':40} {'xi*v^2':>10} {'h_s/h_t':>10}"
out.append(header)
for src in sources:
    f_peak = np.clip(1e-3 / (src['M'] / 1e6), 1e-4, 0.1)
    for xv in [1e-8, 1e-5]:
        ratio = h_scalar_ratio(xv, f_peak, src['C'])
        out.append(f"{src['name']:40} {xv:>10.0e} {ratio:>10.2e}")
    out.append("")

out.append("─" * 72)
out.append("LISA SNR (single event, T_obs=4yr) — SMBH 10^6 Msun @ 1 Gpc")
out.append("─" * 72)
M_src, d_src = 1e6, 1000
snr_t = snr_tensor_LISA(M_src, d_src)
out.append(f"  Tensor SNR         : {snr_t:.1f}")
for xv in xi_v2_vals:
    snr_s = snr_scalar_LISA(xv, M_src, d_src)
    out.append(f"  xi*v^2 = {xv:.0e}: scalar SNR = {snr_s:.3f}  (5σ requires >5)")

out.append("\n" + "─" * 72)
out.append("STACKING ANALYSIS — N events for 5σ scalar detection")
out.append("─" * 72)
out.append(f"{'xi*v^2':>10} {'snr_single':>12} {'N for 5sig':>12} {'Feasible?':>12}")
for xv in xi_v2_vals:
    snr_s1 = snr_scalar_LISA(xv, M_src, d_src)
    if snr_s1 > 0:
        N_needed = (5.0 / snr_s1)**2
    else:
        N_needed = np.inf
    feasible = "YES" if N_needed < 100 else ("MARGINAL" if N_needed < 1000 else "NO")
    out.append(f"{xv:>10.0e} {snr_s1:>12.4f} {N_needed:>12.0f} {feasible:>12}")

out.append("\n" + "─" * 72)
out.append("FALSIFICATION CRITERIA")
out.append("─" * 72)
out.append("  TMT FALSIFIED if LISA stacking constrains h_s/h_t < 1e-7")
out.append("  TMT FALSIFIED if T-channel shows NO excess at SMBH merger epochs")
out.append("  TMT SUPPORTED if T-channel excess correlates with A,E at >2sigma")
out.append("  TMT SUPPORTED if h_s/h_t consistent with xi*v^2 in [1e-8, 1e-5]")
out.append("\n  CURRENT CONSTRAINTS:")
out.append("  LIGO GW170817: |h_s/h_t| < 0.03  -->  xi*v^2 < 9e-4  (weak)")
out.append("  PPN Cassini  : xi*v^2 < 1e-5  -->  h_s/h_t < 3.2e-3  (strong)")

report = "\n".join(out)
print(report)
with open('data/results/TEST5_scalar_gw_predictions.txt', 'w') as f:
    f.write(report)

# ── Plots ───────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('TMT Test 5 — Scalar GW Breathing Mode: LISA Prediction', fontsize=13)

# Plot 1: h_s/h_t vs xi*v^2
ax = axes[0]
xi_arr = np.logspace(-10, -4, 200)
for src in sources[:3]:
    f_peak = np.clip(1e-3 / (src['M'] / 1e6), 1e-4, 0.1)
    ratio_arr = [h_scalar_ratio(xv, f_peak, src['C']) for xv in xi_arr]
    ax.loglog(xi_arr, ratio_arr, lw=2, label=src['name'][:25])
ax.axhline(0.03, color='red', ls='--', lw=1.5, label='LIGO O4 limit (0.03)')
ax.axhspan(1e-5, 1e-4, alpha=0.1, color='orange', label='PPN constraint range')
ax.set_xlabel('xi * v^2 (TMT non-minimal coupling)')
ax.set_ylabel('h_scalar / h_tensor')
ax.set_title('Scalar/tensor ratio vs coupling')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# Plot 2: LISA sensitivity curves + TMT predictions
ax = axes[1]
f_arr = np.logspace(-4, 2, 500)
ax.loglog(f_arr, h_noise_LISA(f_arr), 'steelblue', lw=2.5, label='LISA')
ax.loglog(f_arr, h_noise_LIGO(f_arr), 'tomato', lw=2, ls='--', label='LIGO O4')
ax.loglog(f_arr, h_noise_ET(f_arr), 'green', lw=2, ls=':', label='ET')
# TMT scalar signal: SMBH 10^6 at 1 Gpc, xi*v^2 = 1e-5
for xv, ls, col in [(1e-5, '-', 'purple'), (1e-7, '--', 'gray')]:
    f_peak = 1e-3
    h_t = h_tensor(1e6, 1000, f_peak)
    ratio = h_scalar_ratio(xv, f_peak, 0.4)
    h_s = h_t * ratio
    ax.plot(f_peak, h_s / np.sqrt(1e-3), 's', ms=10, color=col,
            label=f'TMT scalar (xi*v^2={xv:.0e})')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Strain sensitivity (1/sqrt(Hz))')
ax.set_title('TMT scalar prediction vs detector noise')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_xlim(1e-4, 1e2)

# Plot 3: LISA SNR vs N_events
ax = axes[2]
N_arr = np.arange(1, 101)
for xv, col in [(1e-5, 'purple'), (1e-6, 'steelblue'), (1e-7, 'gray')]:
    snr1 = snr_scalar_LISA(xv, 1e6, 1000)
    snr_stack = snr1 * np.sqrt(N_arr)
    ax.plot(N_arr, snr_stack, color=col, lw=2, label=f'xi*v^2={xv:.0e}')
ax.axhline(5, color='red', ls='--', lw=2, label='5σ threshold')
ax.axhline(3, color='orange', ls=':', lw=1.5, label='3σ threshold')
ax.set_xlabel('Number of stacked SMBH merger events')
ax.set_ylabel('Scalar mode SNR')
ax.set_title('LISA stacking: SNR vs N events\n(SMBH 10^6 Msun, d=1 Gpc)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(1, 100)
ax.set_ylim(0, 15)

plt.tight_layout()
plt.savefig('data/results/TEST5_scalar_gw_predictions.png', dpi=150, bbox_inches='tight')
print("\nPlot saved: data/results/TEST5_scalar_gw_predictions.png")
print("Report saved: data/results/TEST5_scalar_gw_predictions.txt")
