"""
DEBUG: Pourquoi calibration k échoue pour elliptiques?
"""

import numpy as np
from scipy.integrate import quad

G = 4.302e-6  # kpc (km/s)² / M_sun

# Elliptique typique
M_bary = 1e11  # M_sun
R_e = 5.0  # kpc
sigma_obs = 250.0  # km/s (Faber-Jackson)

print("=" * 60)
print("DEBUG ELLIPTIQUE")
print("=" * 60)
print(f"\nParamètres:")
print(f"  M_bary = {M_bary:.2e} M_sun")
print(f"  R_e    = {R_e:.1f} kpc")
print(f"  σ_obs  = {sigma_obs:.1f} km/s")

# 1. Dispersion vitesse depuis M_bary seule
k_virial = 5.0
sigma_bary = np.sqrt(k_virial * G * M_bary / R_e)

print(f"\n1. σ depuis M_bary seule:")
print(f"   σ_bary = {sigma_bary:.1f} km/s")
print(f"   Déficit: {sigma_obs - sigma_bary:.1f} km/s ({(sigma_obs/sigma_bary - 1)*100:+.1f}%)")

# 2. M_dark nécessaire
# σ² ∝ M_total / R_e
# M_total = M_bary + M_dark
# σ_obs² = k_virial · G · M_total / R_e
M_total_needed = sigma_obs**2 * R_e / (k_virial * G)
M_dark_needed = M_total_needed - M_bary

print(f"\n2. Masse dark nécessaire:")
print(f"   M_total_needed = {M_total_needed:.2e} M_sun")
print(f"   M_dark_needed  = {M_dark_needed:.2e} M_sun")
print(f"   Ratio M_dark/M_bary = {M_dark_needed/M_bary:.3f}")

# 3. Potentiel Φ
def Phi_sersic_simple(r, M, R_e):
    if r <= 0.01:
        r = 0.01
    # Approximation: M(r) ~ M · (r/R_e)³ / (1 + r/R_e)³
    x = r / R_e
    M_r = M * x**3 / (1 + x)**3
    return -G * M_r / r

# Φ à R_e
Phi_at_Re = Phi_sersic_simple(R_e, M_bary, R_e)
print(f"\n3. Potentiel:")
print(f"   Φ(R_e) = {Phi_at_Re:.2e} (km/s)²")

# 4. Intégrale Φ² dV
def integrand(r):
    Phi = Phi_sersic_simple(r, M_bary, R_e)
    return Phi**2 * 4 * np.pi * r**2

R_max = 10 * R_e
integral, _ = quad(integrand, 0.01, R_max, limit=200)

print(f"\n4. Intégrale ∫ Φ² dV:")
print(f"   ∫ Φ² dV (0 → {R_max:.1f} kpc) = {integral:.2e}")

# 5. k nécessaire
k_needed = M_dark_needed / integral

print(f"\n5. k nécessaire:")
print(f"   k = M_dark / ∫Φ² dV")
print(f"   k = {k_needed:.4f}")

# 6. Test avec différents k
print(f"\n6. Test M_Després avec différents k:")

for k_test in [0.01, 0.1, 1.0, 5.0, 10.0, k_needed]:
    M_D = k_test * integral
    M_total = M_bary + M_D
    sigma_pred = np.sqrt(k_virial * G * M_total / R_e)

    print(f"   k = {k_test:7.3f}  →  M_D = {M_D:.2e}  →  σ = {sigma_pred:6.1f} km/s  (erreur: {sigma_pred - sigma_obs:+6.1f})")

print(f"\n7. Comparaison k avec spirales:")
# Loi spirales
k0_spi = 0.343
alpha_spi = -1.610
beta_spi = -3.585
f_gas_typ_ell = 0.02

k_spiral_pred = k0_spi * (M_bary/1e10)**alpha_spi * (1 + f_gas_typ_ell)**beta_spi
print(f"   k_spiral prédit (M={M_bary:.2e}, f_gas={f_gas_typ_ell}) = {k_spiral_pred:.4f}")
print(f"   k_ell nécessaire = {k_needed:.4f}")
print(f"   Ratio k_ell / k_spiral = {k_needed / k_spiral_pred:.3f}")

print("\n" + "=" * 60)
print("DIAGNOSTIC")
print("=" * 60)

if k_needed > 10:
    print(f"\n⚠ PROBLÈME: k nécessaire = {k_needed:.2f} >> 10")
    print(f"  → Intégrale ∫Φ² dV trop faible")
    print(f"  → Profil Sérsic sous-estime Φ²?")
    print(f"  → Ou k_virial = 5 trop grand?")
else:
    print(f"\n✓ k nécessaire = {k_needed:.2f} raisonnable")
    print(f"  → Calibration devrait fonctionner")

# Test k_virial différent
print(f"\n8. Sensibilité k_virial:")
for k_v in [3.0, 5.0, 7.0]:
    sigma_v = np.sqrt(k_v * G * M_bary / R_e)
    M_total_v = sigma_obs**2 * R_e / (k_v * G)
    M_dark_v = M_total_v - M_bary
    k_needed_v = M_dark_v / integral

    print(f"   k_virial = {k_v:.1f}  →  σ_bary = {sigma_v:.1f}  →  k_needed = {k_needed_v:.3f}")

print("\n" + "=" * 60)
