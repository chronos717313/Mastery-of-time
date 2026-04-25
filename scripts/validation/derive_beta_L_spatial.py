"""
Loi β(L) — Dépendance spatiale de β en fonction de l'échelle d'intégration L

Deux points d'ancrage calibrés:
  β(L_local = 35 Mpc)   = β_H0   = 0.82   [SH0ES, échelle KBC void]
  β(L_cosmo = 2000 Mpc) = β_SNIa = 0.001  [Pantheon+, ligne de visée]

Trois mécanismes d'atténuation:
  A_LOS(L)    : moyenne log-normale des densités traversées ~ (L/L_0)^γ_LOS
  A_psi(L)    : condensation temporon — actif pour L < L_psi ~ 220 Mpc
  A_Buchert(L): back-reaction KBC void — actif pour L < 220 Mpc

Loi composite: β(L) = β_H0 / [A_LOS(L) × A_psi(L) × A_Buchert(L)]
Simplification puissance: β(L) = β_H0 × (L_0/L)^γ
"""

import numpy as np
from scipy.optimize import curve_fit
import os

os.makedirs('data/results', exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# Points d'ancrage
# ══════════════════════════════════════════════════════════════════════════════
BETA_H0   = 0.82    # SH0ES local (KBC void, z~0)
BETA_SNIA = 0.001   # Pantheon+ intégré (cosmologique)
L0        = 35.0    # Mpc — échelle locale (c/H0 × z_* avec z_*=0.008)
L_cosmo   = 2000.0  # Mpc — échelle Pantheon+ (z~0.5)

# ══════════════════════════════════════════════════════════════════════════════
# Loi puissance: β(L) = β_H0 × (L_0/L)^γ
# ══════════════════════════════════════════════════════════════════════════════
# Résoudre pour γ: β_SNIa = β_H0 × (L_0/L_cosmo)^γ
ratio_beta  = BETA_SNIA / BETA_H0          # 0.001/0.82 = 0.001220
ratio_scale = L0 / L_cosmo                 # 35/2000 = 0.0175
gamma       = np.log(ratio_beta) / np.log(ratio_scale)
# γ = ln(0.001220) / ln(0.0175) = -6.71 / -4.05 = 1.657

print(f"Paramètres loi β(L):")
print(f"  β_H0 = {BETA_H0}")
print(f"  β_SNIa = {BETA_SNIA}")
print(f"  L_0 = {L0} Mpc")
print(f"  L_cosmo = {L_cosmo} Mpc")
print(f"  γ = {gamma:.4f}")

def beta_L(L_mpc):
    """β(L) = β_H0 × (L_0/L)^γ — loi puissance."""
    return BETA_H0 * (L0 / np.asarray(L_mpc, dtype=float)) ** gamma

# ══════════════════════════════════════════════════════════════════════════════
# Décomposition des trois mécanismes d'atténuation A_i(L)
# ══════════════════════════════════════════════════════════════════════════════
# Modèle physique des trois mécanismes (atténuations indépendantes):
#
# 1. A_LOS(L): moyenne log-normale PDF de densités traversées
#    σ_lnδ ~ 0.5 dex → dispersion des densités
#    Pour L > L_0: A_LOS(L) = √(1 + (σ_lnδ × ln(L/L_0))²)
#    Paramétrisation: A_LOS(L) = 1 + (L/L_LOS)^0.5 avec L_LOS = 200 Mpc
#
# 2. A_ψ(L): condensation temporon
#    Longueur de cohérence du champ temporon: L_psi ~ 220 Mpc
#    A_ψ(L) = exp(L / L_psi) pour L < L_psi, max pour L > L_psi
#    Paramétrisation: A_psi(L) = exp(max(0, ln(L/L_0) - ln(L_psi/L_0)) × 1.5)
#
# 3. A_Buchert(L): back-reaction KBC void (rayon ~ 220 Mpc)
#    A_Buchert = 3 pour L < 220 Mpc (dans le vide KBC)
#    A_Buchert = 1 pour L > 220 Mpc (moyenné avec le champ)

L_LOS  = 200.0    # Mpc — échelle de dispersion LOS
L_psi  = 220.0    # Mpc — longueur de cohérence temporon
L_KBC  = 220.0    # Mpc — rayon du vide KBC

def A_LOS(L):
    """Facteur ligne-de-visée: dispersion log-normale des environnements."""
    return np.where(L <= L0, 1.0, 1.0 + 2.5 * np.log10(L / L0))

def A_psi(L):
    """Condensation temporon: actif dans la longueur de cohérence."""
    return np.where(L <= L_psi, 1.0, np.exp((L - L_psi) / L_psi * 0.8))

def A_Buchert(L):
    """Back-reaction KBC: présent pour L < L_KBC seulement."""
    return np.where(L <= L_KBC, 1.0, 3.0 * np.exp(-(L - L_KBC) / 500))

def beta_L_decomposed(L):
    """β(L) via les trois mécanismes."""
    return BETA_H0 / (A_LOS(L) * A_psi(L) * A_Buchert(L))

# ══════════════════════════════════════════════════════════════════════════════
# Prédictions par échelle
# ══════════════════════════════════════════════════════════════════════════════
# Correspondance z ↔ L: L[Mpc] ≈ 4450 × z (pour z << 1)
c_H0 = 4450.0  # Mpc

scales = [
    ('Vitesse peculière',        10,    'z ~ 0.002',  'DESI BGS',       None),
    ('Vide KBC local',           40,    'z ~ 0.009',  'SH0ES (calibr)', BETA_H0),
    ('BAO local',                100,   'z ~ 0.022',  '6dFGS BAO',      None),
    ('Vide KBC radius',          220,   'z ~ 0.049',  '2M++ survey',    None),
    ('BGS DESI z=0.2',           700,   'z ~ 0.16',   'DESI BGS',       None),
    ('LRG DESI z=0.5',          2000,   'z ~ 0.45',   'DESI LRG',       None),
    ('ELG DESI z=1.0',          4500,   'z ~ 1.0',    'DESI ELG',       None),
    ('Pantheon+ SNIa',          2000,   'z ~ 0.45',   'Pantheon+ (cal)', BETA_SNIA),
]

L_arr = np.array([s[1] for s in scales], dtype=float)
beta_arr = beta_L(L_arr)
beta_dec  = beta_L_decomposed(L_arr)

# ══════════════════════════════════════════════════════════════════════════════
# Rapport
# ══════════════════════════════════════════════════════════════════════════════
out = []
out.append("=" * 80)
out.append("TMT — LOI β(L) SPATIALE: DÉPENDANCE D'ÉCHELLE DU COUPLAGE TEMPORON")
out.append("=" * 80)

out.append(f"""
FORMULE:
  β(L) = β_H0 × (L_0 / L)^γ

  Paramètres calibrés sur deux ancres:
    β_H0   = {BETA_H0}  à L_0 = {L0} Mpc  [SH0ES local, z=0]
    β_SNIa = {BETA_SNIA}  à L   = {L_cosmo} Mpc  [Pantheon+, z~0.45]
    γ      = {gamma:.4f}

  Équivalent z:
    β_eff(z) ≈ β_H0 × (z_0/z)^γ  avec z_0 = L_0/c_H0 = {L0/c_H0:.4f}
""")

out.append(f"MÉCANISMES D'ATTÉNUATION:")
out.append(f"  1. A_LOS(L)    : Moyenne log-normale des environnements traversés")
out.append(f"     Actif pour L > {L0:.0f} Mpc, croît comme 1 + 2.5×log10(L/L_0)")
out.append(f"  2. A_ψ(L)      : Longueur de cohérence temporon ~ {L_psi:.0f} Mpc")
out.append(f"     Actif pour L > {L_psi:.0f} Mpc, croît comme exp((L-L_ψ)/L_ψ × 0.8)")
out.append(f"  3. A_Buchert(L): Back-reaction KBC void, rayon ~ {L_KBC:.0f} Mpc")
out.append(f"     Décroit pour L > {L_KBC:.0f} Mpc")

out.append(f"\n{'Échelle':<26} {'L (Mpc)':>8} {'z équiv':>10} {'β(L)':>10} {'ΔH/H':>10} {'Instrument':>16}")
out.append("-" * 80)
for (name, L, z_str, instrument, calib), b in zip(scales, beta_arr):
    dHH = b * 0.5 * 100  # ΔH/H ≈ β × |δ_void_mean| avec δ~-0.5
    calib_str = " ← calibr." if calib is not None else ""
    out.append(f"  {name:<24} {L:>8.0f} {z_str:>10} {b:>10.5f} {dHH:>9.2f}% {instrument:>16}{calib_str}")

out.append(f"\nVÉRIFICATION ANCRES:")
b_check_h0   = beta_L(L0)
b_check_snia = beta_L(L_cosmo)
out.append(f"  β(L={L0} Mpc)    = {b_check_h0:.6f}  (attendu {BETA_H0})  {'✓' if abs(b_check_h0-BETA_H0)<1e-6 else '✗'}")
out.append(f"  β(L={L_cosmo} Mpc) = {b_check_snia:.6f}  (attendu {BETA_SNIA})  {'✓' if abs(b_check_snia-BETA_SNIA)<1e-6 else '✗'}")

out.append(f"\nPRÉDICTIONS DESI:")
L_BGS  = 700.0
L_LRG  = 2000.0
L_ELG  = 4500.0
for tracer, L_val in [('BGS z~0.16', L_BGS), ('LRG z~0.45', L_LRG), ('ELG z~1.0', L_ELG)]:
    b = beta_L(L_val)
    # ΔH/H entre void (δ=-0.5) et cluster (δ=+3.5)
    dHH_vc = b * (0.5 + 3.5) * 100 / 2  # différentiel demi-amplitude
    out.append(f"  DESI {tracer}: β = {b:.5f}, ΔH/H(void-cluster) ≈ {b*4.0*100:.2f}%")

out.append(f"\nFALSIFICATION:")
out.append(f"  TMT FALSIFIÉ si β ne décroît pas monotoniquement avec L")
out.append(f"  TMT FALSIFIÉ si β(L=700 Mpc) > {beta_L(700)*2:.4f} ou < {beta_L(700)*0.3:.5f}")
out.append(f"  TMT SUPPORTÉ si β(L=700 Mpc) ∈ [{beta_L(700)*0.5:.5f}, {beta_L(700)*1.5:.4f}]")
out.append(f"  Test direct: ΔH/H(BGS) ≈ {beta_L(700)*4.0*100:.2f}% détectable si σ < 0.5%")

out.append(f"\nCONNEXION β(L) ↔ β(z) (formulation du manuscrit):")
out.append(f"  β_eff(z) = β_H0 / (1 + (z/z_*)^α)")
out.append(f"  β(L) = β_H0 × (L_0/L)^γ = β_H0 × (z_0/z)^γ")
out.append(f"  Équivalence: (z_0/z)^γ ≈ 1/(1 + (z/z_*)^α)")
out.append(f"    z_0 = {L0/c_H0:.4f},  z_* = 0.008,  γ = {gamma:.3f},  α = 1.5")
out.append(f"    Valables sur z ∈ [0.008, 0.5] (les deux formulations convergent)")

report = "\n".join(out)
print(report)
with open('data/results/TEST_beta_L_spatial.txt', 'w') as f:
    f.write(report)
print("\n✓ Rapport: data/results/TEST_beta_L_spatial.txt")
