"""
Test Tully-Fisher Résiduel — TMT vs ΛCDM

La relation de Tully-Fisher baryonique (BTFR): M_bary ∝ V_flat^4

Dans TMT: M_bary × [1 + k × (r_flat/r_c)^n] = V_flat^4 / (G × A_0)
  → les résidus BTFR doivent corréler avec (r_flat/r_c) et k(M)
  → PAS corréler avec des paramètres invisibles (concentration NFW, etc.)

Dans ΛCDM: les résidus corrèlent avec la concentration du halo DM
  → halo concentration = paramètre CACHÉ

Test: si TMT est correct, les résidus BTFR corrèlent avec des
      observables baryoniques (f_gas, Σ_disk, Rdisk) mais PAS avec
      des paramètres DM cachés.

Données: SPARC_Lelli2016c.mrt
"""

import numpy as np
from scipy import stats
import os

os.makedirs('data/results', exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# Charger données SPARC
# ══════════════════════════════════════════════════════════════════════════════
sparc_file = 'data/sparc/SPARC_Lelli2016c.mrt'
UPSILON = 0.5
HELIUM  = 1.33
G_SI    = 6.674e-11  # m³/kg/s²
Msun    = 1.989e30   # kg
kpc     = 3.086e19   # m
km      = 1e3        # m/s

def parse_sparc(line):
    parts = line.split()
    if len(parts) < 17:
        return None
    if not (parts[0][0].isalpha() or parts[0][0].isdigit()):
        return None
    try:
        return (parts[0], float(parts[5]), float(parts[7]), float(parts[9]),
                float(parts[10]), float(parts[11]), float(parts[12]),
                float(parts[13]), float(parts[15]),
                int(parts[17]) if len(parts) > 17 else 1)
    except (ValueError, IndexError):
        return None

rows = []
with open(sparc_file) as f:
    for line in f:
        p = parse_sparc(line)
        if p is None:
            continue
        name, inc, L36, Reff, SBeff, Rdisk, SBdisk, MHI, Vflat, Q = p
        if L36 <= 0 or Vflat <= 0 or Q == 3 or inc < 30:
            continue
        M_star = UPSILON * L36 * 1e9
        M_gas  = HELIUM  * MHI * 1e9
        M_bary = M_star + M_gas
        f_gas  = M_gas / M_bary if M_bary > 0 else 0
        Sigma  = UPSILON * SBdisk if SBdisk > 0 else np.nan
        rows.append({'name': name, 'M_bary': M_bary, 'M_star': M_star,
                     'M_gas': M_gas, 'f_gas': f_gas, 'Vflat': Vflat,
                     'Rdisk': Rdisk, 'Reff': Reff, 'SBdisk': Sigma, 'Q': Q})

print(f"Galaxies SPARC lues: {len(rows)}")

M_arr   = np.array([r['M_bary'] for r in rows])
V_arr   = np.array([r['Vflat']  for r in rows])
fg_arr  = np.array([r['f_gas']  for r in rows])
Rd_arr  = np.array([r['Rdisk']  for r in rows])
Re_arr  = np.array([r['Reff']   for r in rows])
sig_arr = np.array([r['SBdisk'] for r in rows])

valid = (M_arr > 1e7) & (V_arr > 10) & np.isfinite(np.log(M_arr))
M_v = M_arr[valid]; V_v = V_arr[valid]; fg_v = fg_arr[valid]
Rd_v = Rd_arr[valid]; sig_v = sig_arr[valid]
N = valid.sum()
print(f"Après filtres: {N}")

# ══════════════════════════════════════════════════════════════════════════════
# Ajuster la BTFR: log(M_bary) = A + 4×log(V_flat)
# ══════════════════════════════════════════════════════════════════════════════
log_M = np.log10(M_v)
log_V = np.log10(V_v)

# Ajustement libre de la pente
slope_free, inter_free, r_btfr, p_btfr, se_free = stats.linregress(log_V, log_M)

# Ajustement pente contrainte à 4 (BTFR théorique)
inter_4 = np.mean(log_M - 4.0 * log_V)

# Résidus (vs pente libre et vs pente 4)
res_free = log_M - (inter_free + slope_free * log_V)
res_4    = log_M - (inter_4    + 4.0        * log_V)

print(f"\nBTFR pente libre: {slope_free:.3f} ± {se_free:.3f}")
print(f"BTFR r = {r_btfr:.4f}, p = {p_btfr:.2e}")

# ══════════════════════════════════════════════════════════════════════════════
# Corrélations des résidus avec observables baryoniques
# ══════════════════════════════════════════════════════════════════════════════
# Variables à tester
log_fg  = np.log10(1 + fg_v)
log_Rd  = np.log10(Rd_v + 0.1)  # kpc
log_M10 = np.log10(M_v / 1e10)

# Prédiction TMT de r_c
BETA_TMT = 4.00; GAMMA_TMT = -0.49
r_c_tmt  = 2.6 * (M_v / 1e10) ** 0.56  # kpc
log_rc_Rd = np.log10(r_c_tmt / (Rd_v + 0.1))  # r_c / R_disk

# Brillance de surface (si disponible)
sig_mask = np.isfinite(sig_v) & (sig_v > 0)

correlations = [
    ('log(M_bary)',         log_M10,             res_free, 'TMT: attendu si b≠-0.5'),
    ('log(1 + f_gas)',      log_fg,               res_free, 'TMT+ΛCDM: faible effet'),
    ('log(R_disk)',         log_Rd,               res_free, 'TMT: attendu (r_c/Rd)'),
    ('log(r_c/R_disk)',     log_rc_Rd,            res_free, 'TMT: prédit positif'),
]

# ══════════════════════════════════════════════════════════════════════════════
# BTFR avec et sans correction TMT
# ══════════════════════════════════════════════════════════════════════════════
# TMT prédit M_eff = M_bary × [1 + k × (Rd/r_c)]
# donc BTFR TMT: M_bary × [1 + correction] = C × V^4
k_arr  = BETA_TMT * (M_v / 1e10) ** GAMMA_TMT
n_tmt  = 0.75
corr   = k_arr * (Rd_v / r_c_tmt) ** n_tmt
M_eff  = M_v * (1 + corr)

log_Meff = np.log10(M_eff)
slope_tmt, inter_tmt, r_tmt, p_tmt, se_tmt = stats.linregress(log_V, log_Meff)
res_tmt = log_Meff - (inter_tmt + slope_tmt * log_V)

# Dispersion des résidus (scatter BTFR)
scatter_newton = np.std(res_free)
scatter_tmt    = np.std(res_tmt)

# ══════════════════════════════════════════════════════════════════════════════
# Rapport
# ══════════════════════════════════════════════════════════════════════════════
out = []
out.append("=" * 75)
out.append("TEST TULLY-FISHER RÉSIDUEL — TMT vs ΛCDM")
out.append("Relation de Tully-Fisher baryonique: M_bary ∝ V_flat^4")
out.append("=" * 75)

out.append(f"\nÉCHANTILLON SPARC:")
out.append(f"  Galaxies valides (Q≠3, inc>30°): {N}")
out.append(f"  Gamme M_bary: [{M_v.min():.1e}, {M_v.max():.1e}] M☉")
out.append(f"  Gamme V_flat: [{V_v.min():.0f}, {V_v.max():.0f}] km/s")

out.append(f"\nBTFR AJUSTÉE (pente libre):")
out.append(f"  M_bary = 10^{inter_free:.3f} × V_flat^{slope_free:.3f}")
out.append(f"  Pearson r = {r_btfr:.4f}  (p = {p_btfr:.2e})")
out.append(f"  Pente théorique: 4.0 (MOND, TMT)")
out.append(f"  Pente mesurée:  {slope_free:.3f} ± {se_free:.3f}")
out.append(f"  Écart vs 4.0:   {(slope_free-4)/se_free:.2f}σ")

out.append(f"\nDISPERSION (scatter) DES RÉSIDUS BTFR:")
out.append(f"  Newton (M_bary):         σ = {scatter_newton:.4f} dex")
out.append(f"  TMT (M_eff = M_bary×f):  σ = {scatter_tmt:.4f} dex")
delta_scatter = (scatter_tmt - scatter_newton) / scatter_newton * 100
out.append(f"  Variation scatter TMT:   {delta_scatter:+.1f}%")
if scatter_tmt < scatter_newton:
    out.append(f"  → TMT RÉDUIT le scatter BTFR (+cohérent avec TMT)")
else:
    out.append(f"  → TMT augmente légèrement le scatter (correction r_c/Rd à affiner)")

out.append(f"\nCORRÉLATIONS DES RÉSIDUS BTFR vs OBSERVABLES:")
out.append(f"  {'Variable':<25} {'Pearson r':>10} {'p-value':>12} {'Interprétation'}")
out.append(f"  {'-'*70}")
for varname, var_arr, res_arr, interp in correlations:
    mask = np.isfinite(var_arr) & np.isfinite(res_arr)
    if mask.sum() < 10:
        continue
    r_corr, p_corr = stats.pearsonr(var_arr[mask], res_arr[mask])
    signif = "**" if p_corr < 0.01 else ("*" if p_corr < 0.05 else "")
    out.append(f"  {varname:<25} {r_corr:>+10.4f} {p_corr:>12.2e} {signif} {interp}")

# Corrélation avec brillance de surface
if sig_mask.sum() > 20:
    log_sig_v = np.log10(sig_v[sig_mask]/100)
    r_sig, p_sig = stats.pearsonr(log_sig_v, res_free[sig_mask])
    out.append(f"  {'log(Σ_disk/100)':<25} {r_sig:>+10.4f} {p_sig:>12.2e}   TMT: attendu si r_c(Σ)")

out.append(f"\nPRÉDICTIONS TMT vs ΛCDM:")
out.append(f"")
out.append(f"  TMT prédit:    résidus ∝ log(r_c/R_disk), r(résidu, Σ) ≠ 0")
out.append(f"  TMT prédit:    résidus INDÉPENDANTS de masse DM cachée")
out.append(f"  ΛCDM prédit:   résidus ∝ concentration NFW (paramètre caché)")
out.append(f"  ΛCDM prédit:   résidus ∝ histoire de merger (non observable)")
out.append(f"")
out.append(f"  → Si résidus corrèlent avec r_c/R_disk: TMT SUPPORTÉ")
out.append(f"  → Si résidus NE corrèlent PAS avec baryoniques: ΛCDM implication")

out.append(f"\nFALSIFICATION:")
out.append(f"  TMT FALSIFIÉ si |r(résidu, r_c/Rd)| < 0.05 à N > 100")
out.append(f"  TMT SUPPORTÉ si |r(résidu, r_c/Rd)| > 0.15 (p < 0.05)")

out.append(f"\nPENTE BTFR TMT (M_eff = M_bary × [1 + k×(Rd/rc)^n]):")
out.append(f"  Pente BTFR avec M_eff: {slope_tmt:.3f} ± {se_tmt:.3f}")
out.append(f"  r(M_eff, V_flat):      {r_tmt:.4f}")
out.append(f"  ΛCDM prédit pente = 4.0 exactement (pas de variation M-dépendante)")
out.append(f"  TMT prédit légère courbure pour galax. massives (k décroît avec M)")

report = "\n".join(out)
print(report)
with open('data/results/TEST_tully_fisher_residual.txt', 'w') as f:
    f.write(report)
print("\n✓ Rapport: data/results/TEST_tully_fisher_residual.txt")
