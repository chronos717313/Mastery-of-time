"""
Test 4 — Real-data β(z=0.2) measurement using Pantheon+ × SDSS voids
Proxy for DESI BAO void-cluster test while waiting for DESI DR1 release.

Method:
  1. Pantheon+ SNIa at 0.05 < z < 0.30 (BGS-like redshift)
  2. Cross-match with SDSS void catalogue (3D proximity in RA/DEC/z)
  3. Classify each SN as in-void vs out-of-void
  4. Compute Δμ = μ_void - μ_outside
  5. Convert to ΔH/H via dμ/dH ≈ 5/(ln10 × H)
  6. Compare to TMT prediction: ΔH/H = β_eff(z=0.2) × |δ_void|

Data:
  - Pantheon+SH0ES.dat (1701 SNIa, Scolnic+22)
  - sdss_voids.txt (1479 voids, RA/DEC/z/R_eff/δ_c)
"""

import numpy as np
from scipy import stats
import os

os.makedirs('data/results', exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# Load Pantheon+ data
# ══════════════════════════════════════════════════════════════════════════════
pantheon_file = 'data/Pantheon+/Pantheon+SH0ES.dat'

with open(pantheon_file) as f:
    header = f.readline().strip().split()

print(f"Pantheon+ columns (showing first 20): {header[:20]}")

# Try to find relevant columns
col = {name: i for i, name in enumerate(header)}
# Typical Pantheon+ columns: CID, IDSURVEY, zHD, zHDERR, zCMB, zCMBERR, zHEL,
# zHELERR, m_b_corr, m_b_corr_err_DIAG, MU_SH0ES, MU_SH0ES_ERR_DIAG, ...
# HOST_RA, HOST_DEC, ...

data = np.genfromtxt(pantheon_file, skip_header=1, dtype=None,
                     encoding='utf-8', names=header)
print(f"\nTotal SNIa entries: {len(data)}")
print(f"Available fields with RA/DEC: {[n for n in header if 'RA' in n or 'DEC' in n]}")

# Extract needed columns
z_cmb  = data['zCMB']    if 'zCMB'    in data.dtype.names else data['zHD']
mu     = data['MU_SH0ES']
mu_err = data['MU_SH0ES_ERR_DIAG']
ra_sn  = data['RA']      if 'RA'      in data.dtype.names else data['HOST_RA']
dec_sn = data['DEC']     if 'DEC'     in data.dtype.names else data['HOST_DEC']

# Filter to BGS-like redshift range
mask_z = (z_cmb > 0.05) & (z_cmb < 0.30)
z_sn    = z_cmb[mask_z]
mu_sn   = mu[mask_z]
emu_sn  = mu_err[mask_z]
ra_sn   = ra_sn[mask_z]
dec_sn  = dec_sn[mask_z]
N_sn    = len(z_sn)
print(f"SNIa in z∈[0.05, 0.30]: {N_sn}")

# ══════════════════════════════════════════════════════════════════════════════
# Load SDSS void catalogue
# ══════════════════════════════════════════════════════════════════════════════
voids = np.loadtxt('data/voids/sdss_voids.txt')
ra_v, dec_v, z_v, r_eff_v, delta_v = voids.T
print(f"SDSS voids: {len(voids)}")

# ══════════════════════════════════════════════════════════════════════════════
# Cross-match: classify each SN as in-void or outside
# ══════════════════════════════════════════════════════════════════════════════
c_km_s = 3e5  # km/s

def angular_sep_deg(ra1, dec1, ra2, dec2):
    """Haversine angular separation in degrees."""
    r1, d1, r2, d2 = map(np.radians, [ra1, dec1, ra2, dec2])
    cos_sep = (np.sin(d1)*np.sin(d2) +
               np.cos(d1)*np.cos(d2)*np.cos(r1-r2))
    return np.degrees(np.arccos(np.clip(cos_sep, -1, 1)))

# For each SN, check if it's inside any void
# Void radius R_eff is in Mpc/h → convert to angular size at void's redshift
H0 = 67.4  # km/s/Mpc
h  = 0.674
in_void        = np.zeros(N_sn, dtype=bool)
closest_delta  = np.zeros(N_sn)
closest_r      = np.full(N_sn, np.inf)

for i in range(N_sn):
    # Comoving distance to SN (Hubble-Lemaître, rough)
    D_sn  = c_km_s * z_sn[i] / H0            # Mpc
    # For each void, check 3D proximity
    for j in range(len(voids)):
        # Angular separation (degrees)
        ang = angular_sep_deg(ra_sn[i], dec_sn[i], ra_v[j], dec_v[j])
        # Tangential distance at void redshift
        D_v = c_km_s * z_v[j] / H0
        d_tang = np.radians(ang) * D_v       # Mpc (small-angle)
        # Radial distance (line-of-sight)
        d_radial = abs(D_sn - D_v)           # Mpc
        d_3d     = np.sqrt(d_tang**2 + d_radial**2)   # Mpc
        r_v_Mpc  = r_eff_v[j] / h            # R_eff in Mpc
        if d_3d < r_v_Mpc:
            in_void[i] = True
            if d_3d < closest_r[i]:
                closest_r[i]     = d_3d
                closest_delta[i] = delta_v[j]

N_void = in_void.sum()
N_out  = N_sn - N_void
print(f"\nSNIa in voids:  {N_void} ({N_void/N_sn*100:.1f}%)")
print(f"SNIa outside:   {N_out} ({N_out/N_sn*100:.1f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# Compute Δμ = μ_void - μ_outside (residuals from mean)
# ══════════════════════════════════════════════════════════════════════════════
# Subtract the z-dependent mean (cosmological expected mu)
# We use binned residuals to avoid fitting a cosmological model
def compute_mu_residuals(z, mu, emu, nbins=10):
    """Subtract smooth mean of μ(z) to get residuals."""
    z_edges = np.linspace(z.min()-1e-6, z.max()+1e-6, nbins+1)
    residuals = np.zeros_like(mu)
    for k in range(nbins):
        m = (z >= z_edges[k]) & (z < z_edges[k+1])
        if m.sum() > 5:
            wts = 1.0 / emu[m]**2
            mu_mean = np.sum(mu[m] * wts) / np.sum(wts)
            residuals[m] = mu[m] - mu_mean
    return residuals

res_mu = compute_mu_residuals(z_sn, mu_sn, emu_sn)

mu_void     = res_mu[in_void]
mu_outside  = res_mu[~in_void]
emu_void    = emu_sn[in_void]
emu_outside = emu_sn[~in_void]

delta_mu_obs = np.average(mu_void,    weights=1/emu_void**2) - \
               np.average(mu_outside, weights=1/emu_outside**2)
# Standard error of the difference
err_void    = 1.0 / np.sqrt(np.sum(1/emu_void**2))
err_outside = 1.0 / np.sqrt(np.sum(1/emu_outside**2))
sigma_dmu   = np.sqrt(err_void**2 + err_outside**2)

# Convert Δμ to ΔH/H:  μ = 5 log10(D_L) + 25,  D_L ∝ 1/H for small z
# dμ/dH = -5/(ln10 × H)  →  ΔH/H ≈ -ln10/5 × Δμ
dHH_obs      = -np.log(10)/5 * delta_mu_obs * 100   # in percent
dHH_err      = np.log(10)/5  * sigma_dmu * 100

# ══════════════════════════════════════════════════════════════════════════════
# TMT prediction
# ══════════════════════════════════════════════════════════════════════════════
BETA_H0 = 0.82
Z_STAR  = 0.008
ALPHA   = 1.5

def beta_eff(z):
    return BETA_H0 / (1 + (z/Z_STAR)**ALPHA)

# Mean redshift of void SNIa
z_mean_void = np.mean(z_sn[in_void]) if N_void > 0 else 0.2
b_pred = beta_eff(z_mean_void)

# Mean delta of voids containing SNIa
delta_void_mean = np.mean(closest_delta[in_void]) if N_void > 0 else -0.5
dHH_tmt = abs(b_pred * delta_void_mean) * 100  # percent

# ══════════════════════════════════════════════════════════════════════════════
# Report
# ══════════════════════════════════════════════════════════════════════════════
out = []
out.append("=" * 75)
out.append("TMT TEST 4 — β(z≈0.2) REAL-DATA MEASUREMENT")
out.append("Pantheon+ SNIa × SDSS void catalogue (proxy for DESI BAO)")
out.append("=" * 75)
out.append(f"\nDATA:")
out.append(f"  Pantheon+ SNIa in z∈[0.05, 0.30]:  {N_sn}")
out.append(f"  SDSS voids                      :  {len(voids)}")
out.append(f"\nCROSS-MATCH (3D proximity, d < R_eff of void):")
out.append(f"  SNIa classified in voids        :  {N_void} ({N_void/N_sn*100:.1f}%)")
out.append(f"  SNIa classified outside voids   :  {N_out} ({N_out/N_sn*100:.1f}%)")
out.append(f"  Mean z of void SNIa             :  {z_mean_void:.3f}")
out.append(f"  Mean δ_void of containing voids :  {delta_void_mean:.3f}")

out.append(f"\nMEASUREMENT:")
out.append(f"  Δμ (void − outside) = {delta_mu_obs:+.4f} ± {sigma_dmu:.4f} mag")
out.append(f"  Significance        = {delta_mu_obs/sigma_dmu:.2f}σ")
out.append(f"  ΔH/H observed       = {dHH_obs:+.3f}% ± {dHH_err:.3f}%")

out.append(f"\nTMT PREDICTION (Test 4, β_H0={BETA_H0}, z_*={Z_STAR}, α={ALPHA}):")
out.append(f"  β_eff(z={z_mean_void:.3f})      = {b_pred:.5f}")
out.append(f"  ΔH/H predicted      = {dHH_tmt:.3f}% (sign: voids expand faster)")

# ΛCDM prediction: 0
# TMT prediction: dHH_tmt
# Measured: dHH_obs ± dHH_err
# Compare residuals
out.append(f"\nCOMPARISON:")
out.append(f"  TMT    prediction  :  +{dHH_tmt:.3f}%")
out.append(f"  ΛCDM   prediction  :   0.000%")
out.append(f"  Observed           :  {dHH_obs:+.3f}% ± {dHH_err:.3f}%")

# σ against each null
chi_tmt_vs_obs  = abs(dHH_obs - dHH_tmt) / dHH_err
chi_lcdm_vs_obs = abs(dHH_obs - 0)        / dHH_err
out.append(f"\n  |Obs − TMT|  = {abs(dHH_obs - dHH_tmt):.3f}% ({chi_tmt_vs_obs:.2f}σ away from TMT)")
out.append(f"  |Obs − ΛCDM| = {abs(dHH_obs):.3f}% ({chi_lcdm_vs_obs:.2f}σ away from ΛCDM)")

# Preferred model via Bayes factor (assuming flat priors)
# Using likelihood ratio on single measurement
ll_tmt  = -0.5 * ((dHH_obs - dHH_tmt)/dHH_err)**2
ll_lcdm = -0.5 * ((dHH_obs - 0)/dHH_err)**2
log_bayes_factor = ll_tmt - ll_lcdm
out.append(f"\n  ln(BF_TMT/ΛCDM) = {log_bayes_factor:+.2f}")
if log_bayes_factor > 1:
    out.append(f"  → TMT favored")
elif log_bayes_factor < -1:
    out.append(f"  → ΛCDM favored")
else:
    out.append(f"  → Inconclusive with current statistics")

out.append(f"\nNOTE: This is a PROXY test using SNIa distance modulus.")
out.append(f"      The rigorous DESI BAO peak-shift test will have much higher S/N.")
out.append(f"      Expected improvement: factor ~10 with DESI DR1 (2026).")

report = "\n".join(out)
print(report)
with open('data/results/TEST4_beta_z02_real_data.txt', 'w') as f:
    f.write(report)
print(f"\n✓ Report saved: data/results/TEST4_beta_z02_real_data.txt")
