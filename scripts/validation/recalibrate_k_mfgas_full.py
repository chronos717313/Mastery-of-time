"""
Recalibration k(M, f_gas) — Intégralité des données SPARC

Étend la loi k(M) vers k(M, f_gas, Σ) en incluant:
  - Fraction de gaz f_gas = M_gas / M_bary
  - Brillance de surface centrale SBdisk [M_sun/pc²]
  - Rayon effectif Reff [kpc]

Données: SPARC_Lelli2016c.mrt (175 galaxies)
         + résultats k_opt individuels existants

Formule testée:
  k(M, f_gas) = a × (M_bary/10¹⁰)^b × (1 + f_gas)^c
  k(M, Σ)     = a × (M_bary/10¹⁰)^b × (Σ/100)^d
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy import stats
import os

os.makedirs('data/results', exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# Lire le catalogue SPARC principal
# ══════════════════════════════════════════════════════════════════════════════
sparc_file = 'data/sparc/SPARC_Lelli2016c.mrt'
UPSILON = 0.5   # M/L ratio [3.6 µm]
HELIUM  = 1.33  # facteur He pour M_gas

def parse_sparc_line(line):
    """Parse space-delimited SPARC line. Returns None if not a data row."""
    parts = line.split()
    if len(parts) < 17:
        return None
    # Check first token looks like a galaxy name
    if not (parts[0][0].isalpha() or parts[0][0].isdigit()):
        return None
    try:
        return {
            'name':   parts[0],
            'T':      int(parts[1]),
            'D':      float(parts[2]),
            'inc':    float(parts[5]),
            'L36':    float(parts[7]),    # 10^9 Lsun
            'Reff':   float(parts[9]),    # kpc
            'SBeff':  float(parts[10]),   # Lsun/pc²
            'Rdisk':  float(parts[11]),   # kpc
            'SBdisk': float(parts[12]),   # Lsun/pc²
            'MHI':    float(parts[13]),   # 10^9 Msun
            'RHI':    float(parts[14]),   # kpc
            'Vflat':  float(parts[15]),   # km/s
            'Q':      int(parts[17]) if len(parts) > 17 else 1,
        }
    except (ValueError, IndexError):
        return None

galaxies = {}
with open(sparc_file) as f:
    for line in f:
        row = parse_sparc_line(line)
        if row is None:
            continue
        L36 = row['L36']; Vflat = row['Vflat']
        if L36 <= 0 or Vflat <= 0:
            continue
        M_star = UPSILON * L36 * 1e9
        M_gas  = HELIUM  * row['MHI'] * 1e9
        M_bary = M_star + M_gas
        f_gas  = M_gas / M_bary if M_bary > 0 else 0.0
        Sigma_disk = UPSILON * row['SBdisk'] if row['SBdisk'] > 0 else np.nan
        galaxies[row['name']] = {
            'M_bary': M_bary, 'M_star': M_star, 'M_gas': M_gas,
            'f_gas': f_gas, 'Vflat': Vflat, 'Q': row['Q'],
            'Rdisk': row['Rdisk'], 'Reff': row['Reff'], 'SBdisk': Sigma_disk,
            'T': row['T'], 'inc': row['inc']
        }

print(f"Galaxies SPARC lues: {len(galaxies)}")

# ══════════════════════════════════════════════════════════════════════════════
# Récupérer k_opt individuel depuis résultats existants
# ══════════════════════════════════════════════════════════════════════════════
calib_file = 'data/results/TMT_REAL_SPARC_calibration.txt'
k_opt_dict = {}
with open(calib_file) as f:
    for line in f:
        # Format: "Galaxy   M_bary   k_opt   r_c   Improv  Bary"
        parts = line.split()
        if len(parts) >= 4:
            try:
                gname  = parts[0]
                M_read = float(parts[1])
                k_read = float(parts[2])
                r_read = float(parts[3])
                if gname in galaxies:
                    k_opt_dict[gname] = (k_read, r_read)
            except (ValueError, IndexError):
                continue

print(f"Galaxies avec k_opt: {len(k_opt_dict)}")

# ══════════════════════════════════════════════════════════════════════════════
# Construire tableau d'analyse
# ══════════════════════════════════════════════════════════════════════════════
data_rows = []
for name, k_opt_data in k_opt_dict.items():
    if name not in galaxies:
        continue
    g = galaxies[name]
    k_opt, r_c = k_opt_data
    if g['M_bary'] <= 0 or k_opt <= 0 or g['Q'] == 3:
        continue
    data_rows.append({
        'name': name,
        'M_bary': g['M_bary'],
        'f_gas': g['f_gas'],
        'k_opt': k_opt,
        'r_c': r_c,
        'Sigma': g['SBdisk'],
        'Rdisk': g['Rdisk'],
        'Vflat': g['Vflat'],
        'T': g['T'],
    })

N = len(data_rows)
print(f"Galaxies pour régression: {N}")

M_arr    = np.array([d['M_bary'] for d in data_rows])
fg_arr   = np.array([d['f_gas']  for d in data_rows])
k_arr    = np.array([d['k_opt']  for d in data_rows])
sig_arr  = np.array([d['Sigma']  for d in data_rows])
rc_arr   = np.array([d['r_c']    for d in data_rows])
Vf_arr   = np.array([d['Vflat'] for d in data_rows])
names    = [d['name'] for d in data_rows]

# Filtre: k_opt raisonnable (0.01 - 10), M > 1e8 Msun
valid = (k_arr > 0.01) & (k_arr < 10) & (M_arr > 1e8)
M_v   = M_arr[valid]
fg_v  = fg_arr[valid]
k_v   = k_arr[valid]
sig_v = sig_arr[valid]
Nv    = valid.sum()
print(f"Galaxies après filtre: {Nv}")

# ══════════════════════════════════════════════════════════════════════════════
# Régression 1: k(M) seul — loi puissance
# ══════════════════════════════════════════════════════════════════════════════
log_M  = np.log10(M_v / 1e10)
log_k  = np.log10(k_v)

r1, p1 = stats.pearsonr(log_M, log_k)
slope1, intercept1, _, _, se1 = stats.linregress(log_M, log_k)
a1 = 10 ** intercept1
b1 = slope1
R2_1 = r1 ** 2

# ══════════════════════════════════════════════════════════════════════════════
# Régression 2: k(M, f_gas) — puissance bivariée
# ══════════════════════════════════════════════════════════════════════════════
def log_k_model(X, log_a, b, c):
    log_M_norm, log_fg1 = X
    return log_a + b * log_M_norm + c * log_fg1

log_M_norm = np.log10(M_v / 1e10)
log_fg1    = np.log10(1 + fg_v)  # log(1 + f_gas)
X2         = (log_M_norm, log_fg1)

try:
    popt2, pcov2 = curve_fit(log_k_model, X2, log_k, p0=[0, -0.5, -1.0], maxfev=5000)
    a2 = 10 ** popt2[0]
    b2, c2 = popt2[1], popt2[2]
    log_k_pred2 = log_k_model(X2, *popt2)
    ss_res2 = np.sum((log_k - log_k_pred2)**2)
    ss_tot  = np.sum((log_k - log_k.mean())**2)
    R2_2 = 1 - ss_res2 / ss_tot
    perr2 = np.sqrt(np.diag(pcov2))
except Exception as e:
    a2, b2, c2, R2_2 = 4.0, -0.49, -0.5, 0.0
    perr2 = [0, 0, 0]
    print(f"  [Avertissement régression 2: {e}]")

# ══════════════════════════════════════════════════════════════════════════════
# Régression 3: k(M, Σ_disk) — avec brillance de surface
# ══════════════════════════════════════════════════════════════════════════════
sig_valid = ~np.isnan(sig_v) & (sig_v > 0)
M_s   = M_v[sig_valid]
k_s   = k_v[sig_valid]
sig_s = sig_v[sig_valid]
Ns    = sig_valid.sum()

log_M_s   = np.log10(M_s / 1e10)
log_k_s   = np.log10(k_s)
log_sig_s = np.log10(sig_s / 100)  # normalisé à 100 Msun/pc²

def log_k_sigma(X, log_a, b, d):
    lM, lSig = X
    return log_a + b * lM + d * lSig

try:
    popt3, pcov3 = curve_fit(log_k_sigma, (log_M_s, log_sig_s), log_k_s,
                             p0=[0.6, -0.4, -0.3], maxfev=5000)
    a3 = 10 ** popt3[0]
    b3, d3 = popt3[1], popt3[2]
    log_k_pred3 = log_k_sigma((log_M_s, log_sig_s), *popt3)
    ss_res3 = np.sum((log_k_s - log_k_pred3)**2)
    ss_tot3 = np.sum((log_k_s - log_k_s.mean())**2)
    R2_3 = 1 - ss_res3 / ss_tot3
    perr3 = np.sqrt(np.diag(pcov3))
except Exception as e:
    a3, b3, d3, R2_3 = 4.0, -0.49, -0.3, 0.0
    perr3 = [0, 0, 0]
    Ns = 0
    print(f"  [Avertissement régression 3: {e}]")

# ══════════════════════════════════════════════════════════════════════════════
# Corrélations partielles
# ══════════════════════════════════════════════════════════════════════════════
r_k_M,  p_k_M  = stats.pearsonr(log_M, log_k)
r_k_fg, p_k_fg = stats.pearsonr(np.log10(1+fg_v), log_k)
if Ns > 5:
    r_k_sig, p_k_sig = stats.pearsonr(np.log10(sig_v[sig_valid]/100), log_k[sig_valid])
else:
    r_k_sig, p_k_sig = 0, 1

# ══════════════════════════════════════════════════════════════════════════════
# Rapport
# ══════════════════════════════════════════════════════════════════════════════
out = []
out.append("=" * 75)
out.append("RECALIBRATION k(M, f_gas) — INTÉGRALITÉ DONNÉES SPARC")
out.append("=" * 75)

out.append(f"\nÉCHANTILLON:")
out.append(f"  Galaxies SPARC total       : {len(galaxies)}")
out.append(f"  Avec k_opt disponible      : {len(k_opt_dict)}")
out.append(f"  Après filtres qualité      : {Nv}")
out.append(f"  Avec Σ_disk disponible     : {Ns}")

out.append(f"\nCORRÉLATIONS PARTIELLES:")
out.append(f"  r(k, M_bary)     = {r_k_M:+.4f}  (p = {p_k_M:.2e})")
out.append(f"  r(k, f_gas)      = {r_k_fg:+.4f}  (p = {p_k_fg:.2e})")
out.append(f"  r(k, Σ_disk)     = {r_k_sig:+.4f}  (p = {p_k_sig:.2e})" if Ns > 5 else "  r(k, Σ_disk) : données insuffisantes")

out.append(f"\n{'='*55}")
out.append(f"RÉGRESSION 1 — k(M) seul [N={Nv}]")
out.append(f"{'='*55}")
out.append(f"  k = {a1:.4f} × (M/10¹⁰)^({b1:.4f})")
out.append(f"  R² = {R2_1:.4f}   r = {r1:+.4f}   p = {p1:.2e}")
out.append(f"  σ(slope) = {se1:.4f}")
out.append(f"  Comparaison v2.3 (N=172): k = 4.00 × M^(-0.49), R² = 0.64")

out.append(f"\n{'='*55}")
out.append(f"RÉGRESSION 2 — k(M, f_gas) [N={Nv}]")
out.append(f"{'='*55}")
out.append(f"  k = {a2:.4f} × (M/10¹⁰)^({b2:.4f}) × (1+f_gas)^({c2:.4f})")
out.append(f"  R² = {R2_2:.4f}")
out.append(f"  Amélioration vs Régression 1: ΔR² = {R2_2-R2_1:+.4f}")
if abs(c2) > 0.1:
    out.append(f"  → f_gas A UN EFFET SIGNIFICATIF sur k (c={c2:.3f})")
    if c2 < 0:
        out.append(f"     Galaxies gaz-riches (f_gas élevé) ont k plus FAIBLE")
    else:
        out.append(f"     Galaxies gaz-riches (f_gas élevé) ont k plus ÉLEVÉ")
else:
    out.append(f"  → Effet f_gas MARGINAL (c={c2:.3f}, faible)")

out.append(f"\n{'='*55}")
out.append(f"RÉGRESSION 3 — k(M, Σ_disk) [N={Ns}]")
out.append(f"{'='*55}")
if Ns > 10:
    out.append(f"  k = {a3:.4f} × (M/10¹⁰)^({b3:.4f}) × (Σ/100)^({d3:.4f})")
    out.append(f"  R² = {R2_3:.4f}")
    out.append(f"  Amélioration vs Régression 1: ΔR² = {R2_3-R2_1:+.4f}")
    if abs(d3) > 0.2:
        out.append(f"  → Σ_disk A UN EFFET SIGNIFICATIF (d={d3:.3f})")
    else:
        out.append(f"  → Effet Σ_disk marginal (d={d3:.3f})")
else:
    out.append(f"  [Données Σ_disk insuffisantes pour régression robuste]")

out.append(f"\nLOI RECOMMANDÉE (v2.4):")
best_R2 = max(R2_1, R2_2)
if R2_2 > R2_1 + 0.02 and abs(c2) > 0.1:
    out.append(f"  k(M, f_gas) = {a2:.3f} × (M/10¹⁰)^({b2:.3f}) × (1+f_gas)^({c2:.3f})")
    out.append(f"  R² = {R2_2:.4f}  (amélioration: +{(R2_2-R2_1)*100:.1f}% vs k(M) seul)")
else:
    out.append(f"  k(M) = {a1:.3f} × (M/10¹⁰)^({b1:.3f})")
    out.append(f"  R² = {R2_1:.4f}  (f_gas n'améliore pas significativement)")

out.append(f"\nPRÉDICTIONS k PAR TYPE:")
for label, M_val, fg_val in [
    ('Naine (10^8 M☉, f_gas=0.7)', 1e8,  0.7),
    ('Spirale (10^10 M☉, f_gas=0.2)', 1e10, 0.2),
    ('Massive (10^11 M☉, f_gas=0.05)', 1e11, 0.05),
]:
    k_pred1 = a1 * (M_val/1e10)**b1
    k_pred2 = a2 * (M_val/1e10)**b2 * (1+fg_val)**c2
    out.append(f"  {label}:")
    out.append(f"    k(M seul) = {k_pred1:.4f}")
    out.append(f"    k(M,fgas) = {k_pred2:.4f}")

report = "\n".join(out)
print(report)
with open('data/results/RECALIBRATION_k_mfgas_full.txt', 'w') as f:
    f.write(report)
print("\n✓ Rapport: data/results/RECALIBRATION_k_mfgas_full.txt")
