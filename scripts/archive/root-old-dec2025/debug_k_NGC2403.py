"""
DEBUG: Pourquoi NGC2403 échoue-t-il maintenant?
Test manuel avec NGC2403 qui fonctionnait avec k=0.304
"""

import numpy as np
from scipy.integrate import quad

G = 4.302e-6  # km^2 Mpc / (M_sun s^2)

# NGC2403 parameters (fonctionnait avec k=0.304, χ²_red=0.06)
M_disk = 5.3e9  # M_sun
R_disk = 1.8    # kpc
v_target = 135  # km/s
k_expected = 0.304

def M_enclosed(r, M_disk, R_disk):
    x = r / R_disk
    return M_disk * (1 - (1 + x) * np.exp(-x))

def Phi(r, M_disk, R_disk):
    M = M_enclosed(r, M_disk, R_disk)
    r_Mpc = r / 1000.0
    return -G * M / r_Mpc

def M_Despres(r_obs, M_disk, R_disk, k):
    r_max = r_obs * 3.0

    def integrand(r_prime):
        Phi_val = Phi(r_prime, M_disk, R_disk)
        r_Mpc = r_prime / 1000.0
        volume_element = 4 * np.pi * r_Mpc**2
        return Phi_val**2 * volume_element

    integral, _ = quad(integrand, 0.01, r_max, limit=200)
    return k * integral

def v_total(r, M_disk, R_disk, k):
    M_bary = M_enclosed(r, M_disk, R_disk)
    M_D = M_Despres(r, M_disk, R_disk, k)
    M_tot = M_bary + M_D
    r_Mpc = r / 1000.0
    return np.sqrt(G * M_tot / r_Mpc)

def v_bary(r, M_disk, R_disk):
    M_bary = M_enclosed(r, M_disk, R_disk)
    r_Mpc = r / 1000.0
    return np.sqrt(G * M_bary / r_Mpc)

print("="*60)
print("DEBUG NGC2403")
print("="*60)

print(f"\nParamètres:")
print(f"  M_disk  = {M_disk:.2e} M_sun")
print(f"  R_disk  = {R_disk:.1f} kpc")
print(f"  v_target = {v_target} km/s")
print(f"  k attendu = {k_expected:.3f}")

# Test à r = 5 * R_disk = 9 kpc (région plateau)
r_test = 5 * R_disk
print(f"\nTest à r = {r_test:.1f} kpc:")

# 1. Masse baryonique
M_bary_r = M_enclosed(r_test, M_disk, R_disk)
print(f"\n  M_bary({r_test:.1f} kpc) = {M_bary_r:.2e} M_sun")

# 2. Potentiel
Phi_r = Phi(r_test, M_disk, R_disk)
print(f"  Φ({r_test:.1f} kpc) = {Phi_r:.2e} km²/s²")

# 3. Vitesse baryonique seule
v_b = v_bary(r_test, M_disk, R_disk)
print(f"  v_bary({r_test:.1f} kpc) = {v_b:.1f} km/s")
print(f"  Déficit par rapport à {v_target} km/s: {v_target - v_b:.1f} km/s ({(v_target-v_b)/v_target*100:.1f}%)")

# 4. Test M_Després avec k attendu
M_D_expected = M_Despres(r_test, M_disk, R_disk, k_expected)
print(f"\n  M_Després({r_test:.1f} kpc, k={k_expected:.3f}) = {M_D_expected:.2e} M_sun")

M_tot = M_bary_r + M_D_expected
print(f"  M_total = {M_tot:.2e} M_sun")

v_tot = v_total(r_test, M_disk, R_disk, k_expected)
print(f"  v_total({r_test:.1f} kpc, k={k_expected:.3f}) = {v_tot:.1f} km/s")
print(f"  Erreur vs {v_target} km/s: {abs(v_tot - v_target):.1f} km/s ({abs(v_tot - v_target)/v_target*100:.1f}%)")

# 5. Test intégrale Φ² directement
print(f"\nTest intégrale Φ²:")

r_max = r_test * 3.0

def integrand_test(r_prime):
    Phi_val = Phi(r_prime, M_disk, R_disk)
    r_Mpc = r_prime / 1000.0
    volume = 4 * np.pi * r_Mpc**2
    return Phi_val**2 * volume

# Test sur quelques points
for r_p in [0.1, 1.0, 5.0, 10.0]:
    integ_val = integrand_test(r_p)
    print(f"  Intégrande(r={r_p:.1f} kpc) = {integ_val:.2e}")

integral_full, err = quad(integrand_test, 0.01, r_max, limit=200)
print(f"\n  Intégrale totale (0.01 → {r_max:.1f} kpc): {integral_full:.2e}")
print(f"  Erreur intégration: {err:.2e}")

# 6. Scan k pour trouver la valeur qui donne v_target
print(f"\nScan k:")
k_values = [0.01, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]

for k_test in k_values:
    v = v_total(r_test, M_disk, R_disk, k_test)
    print(f"  k = {k_test:6.2f}  →  v = {v:6.1f} km/s  (erreur: {abs(v-v_target):5.1f} km/s)")

# 7. Vérification unités
print(f"\nVérification unités:")
print(f"  G = {G:.3e} km² Mpc / (M_sun s²)")
print(f"  M = M_sun, r = Mpc → Φ = km²/s²  ✓")
print(f"  Φ² = km⁴/s⁴")
print(f"  volume = Mpc²")
print(f"  Φ² × volume = km⁴/s⁴ × Mpc²")
print(f"  k × Φ² × volume = ??? → doit donner M_sun")
print(f"\n  PROBLÈME: Les unités ne sont pas cohérentes!")
print(f"  Φ² × dV a des unités de [km⁴/s⁴ × Mpc²]")
print(f"  Pour obtenir M_sun, il faut un facteur de conversion!")

print("\n" + "="*60)
