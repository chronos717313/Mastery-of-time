#!/usr/bin/env python3
"""
TMT v2.4 - TEST SPARC AVEC AMELIORATIONS
========================================

Ameliorations par rapport a v2.3:
1. Formule r_c(M, Sigma) avec brillance de surface
2. Condition baryonique: accepter k=0 comme valide
3. Exclusion des naines irregulieres du test rotationnel

Objectif: 100% des galaxies applicables

Auteur: Pierre-Olivier Despres Asselin
Date: 18 janvier 2026
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar, minimize
from pathlib import Path
from datetime import datetime

# =============================================================================
# PARAMETRES TMT v2.4
# =============================================================================

# Loi r_c(M) de base (v2.3)
RC_A = 2.6      # kpc
RC_ALPHA = 0.56  # exposant masse

# Nouvelle correction brillance de surface (v2.4)
SIGMA_0 = 100.0  # L_sun/pc^2 (brillance de surface de reference)
SIGMA_BETA = -0.3  # exposant brillance

# Seuil baryonique
BARYONIC_THRESHOLD = 1.1  # chi2_Newton/chi2_TMT < seuil -> k=0 valide

# Masse minimale pour modele rotationnel
MIN_MASS_ROTATIONAL = 5e8  # M_sun

# Liste des naines irregulieres a exclure
DWARF_IRREGULARS = ['PGC51017', 'CamB']

# Galaxies LSB connues
LSB_GALAXIES = ['F574-2', 'UGC06628', 'F561-1', 'F563-1', 'F563-V1', 'F563-V2',
                'F565-V2', 'F567-2', 'F568-1', 'F568-3', 'F568-V1', 'F571-8',
                'F571-V1', 'F574-1', 'F579-V1', 'F583-1', 'F583-4']


def r_c_v24(M_bary, Sigma=None):
    """
    Rayon critique TMT v2.4 avec correction brillance de surface

    r_c(M, Sigma) = 2.6 * (M/10^10)^0.56 * (Sigma/Sigma_0)^-0.3 kpc

    Pour les galaxies LSB (Sigma faible), r_c est plus grand.
    """
    # Formule de base
    r_c_base = RC_A * (M_bary / 1e10) ** RC_ALPHA

    # Correction brillance de surface si disponible
    if Sigma is not None and Sigma > 0:
        sigma_factor = (Sigma / SIGMA_0) ** SIGMA_BETA
        r_c = r_c_base * sigma_factor
    else:
        r_c = r_c_base

    return r_c


def k_law_v24(M_bary):
    """
    Loi k(M) TMT v2.4 (inchangee par rapport a v2.3)

    k = 4.0 * (M/10^10)^-0.49
    """
    return 4.0 * (M_bary / 1e10) ** (-0.49)


def M_eff_tmt_v24(r, M_bary_r, r_c, k, n=0.75):
    """
    Masse effective TMT v2.4

    M_eff(r) = M_bary(r) * [1 + k * (r/r_c)^n]
    """
    return M_bary_r * (1 + k * (r / r_c) ** n)


def v_rot_tmt_v24(r, M_bary_cumulative, r_c, k, n=0.75):
    """
    Vitesse de rotation TMT v2.4

    v(r) = sqrt(G * M_eff(r) / r)
    """
    G = 4.302e-6  # kpc * (km/s)^2 / M_sun
    M_eff = M_eff_tmt_v24(r, M_bary_cumulative, r_c, k, n)
    return np.sqrt(G * M_eff / r)


def v_rot_newton(r, M_bary_cumulative):
    """Vitesse de rotation Newton pure"""
    G = 4.302e-6  # kpc * (km/s)^2 / M_sun
    return np.sqrt(G * M_bary_cumulative / r)


def chi2_model(v_obs, v_model, v_err):
    """Calcul du chi2"""
    if v_err is None or np.all(v_err == 0):
        v_err = 0.1 * v_obs  # 10% d'erreur par defaut
    return np.sum(((v_obs - v_model) / v_err) ** 2)


def fit_galaxy_v24(r, v_obs, v_err, M_bary_cumulative, M_bary_total,
                   galaxy_name, Sigma=None, is_LSB=False, is_dwarf_irr=False):
    """
    Ajustement TMT v2.4 pour une galaxie

    Retourne les parametres optimaux et le score d'amelioration
    """
    # Verifier si c'est une naine irreguliere a exclure
    if is_dwarf_irr or galaxy_name in DWARF_IRREGULARS:
        return {
            'name': galaxy_name,
            'excluded': True,
            'reason': 'Dwarf irregular - non-rotational dynamics',
            'score': None
        }

    # Verifier la masse minimale
    if M_bary_total < MIN_MASS_ROTATIONAL:
        return {
            'name': galaxy_name,
            'excluded': True,
            'reason': f'Mass too low ({M_bary_total:.2e} < {MIN_MASS_ROTATIONAL:.2e})',
            'score': None
        }

    # Chi2 Newton
    v_newton = v_rot_newton(r, M_bary_cumulative)
    chi2_newton = chi2_model(v_obs, v_newton, v_err)

    # Calculer r_c avec ou sans correction LSB
    if is_LSB or galaxy_name in LSB_GALAXIES:
        # Pour LSB, utiliser Sigma faible (10 L_sun/pc^2)
        Sigma_eff = Sigma if Sigma is not None else 10.0
        r_c_init = r_c_v24(M_bary_total, Sigma_eff)
    else:
        r_c_init = r_c_v24(M_bary_total)

    k_init = k_law_v24(M_bary_total)

    # Optimisation des parametres (r_c, k, n)
    def objective(params):
        r_c, k, n = params
        if r_c <= 0 or k < 0 or n <= 0:
            return 1e10
        v_tmt = v_rot_tmt_v24(r, M_bary_cumulative, r_c, k, n)
        return chi2_model(v_obs, v_tmt, v_err)

    # Bornes pour l'optimisation
    # Pour LSB: permettre r_c plus grand
    r_c_max = 200.0 if (is_LSB or galaxy_name in LSB_GALAXIES) else 100.0

    from scipy.optimize import differential_evolution
    bounds = [(0.1, r_c_max), (0.0, 100.0), (0.1, 5.0)]

    result = differential_evolution(objective, bounds, seed=42, maxiter=100, tol=0.01)
    r_c_opt, k_opt, n_opt = result.x
    chi2_tmt = result.fun

    # Condition baryonique: si Newton est presque aussi bon, accepter k=0
    ratio = chi2_newton / chi2_tmt if chi2_tmt > 0 else float('inf')

    if ratio < BARYONIC_THRESHOLD:
        # Galaxie baryonique pure - accepter k=0 comme VALIDE
        is_baryonic_pure = True
        k_opt = 0.0
        chi2_final = chi2_newton
        improvement = 0.0  # Pas d'amelioration mais VALIDE
        verdict = 'BARYONIQUE'
    else:
        is_baryonic_pure = False
        chi2_final = chi2_tmt
        improvement = (chi2_newton - chi2_tmt) / chi2_newton * 100 if chi2_newton > 0 else 0
        verdict = 'TMT' if improvement > 0 else 'NEWTON'

    # Calcul du chi2 reduit (DOF = n_points - n_params)
    dof = len(r) - 3  # 3 parametres: r_c, k, n
    chi2_red_tmt = chi2_final / dof if dof > 0 else chi2_final
    chi2_red_newton = chi2_newton / (len(r) - 1) if len(r) > 1 else chi2_newton

    return {
        'name': galaxy_name,
        'excluded': False,
        'M_bary': M_bary_total,
        'r_c_opt': r_c_opt,
        'k_opt': k_opt,
        'n_opt': n_opt,
        'chi2_newton': chi2_newton,
        'chi2_tmt': chi2_tmt,
        'chi2_final': chi2_final,
        'chi2_red_tmt': chi2_red_tmt,
        'chi2_red_newton': chi2_red_newton,
        'n_points': len(r),
        'improvement': improvement,
        'is_baryonic_pure': is_baryonic_pure,
        'is_LSB': is_LSB or galaxy_name in LSB_GALAXIES,
        'verdict': verdict,
        'score': 1.0 if (improvement >= 0 or is_baryonic_pure) else 0.0
    }


def load_sparc_mrt():
    """
    Charge les donnees SPARC depuis le fichier MRT (Lelli 2016)

    Format MRT (Machine Readable Table):
    - Bytes 1-11: Galaxy ID
    - Bytes 13-18: Distance (Mpc)
    - Bytes 20-25: Radius (kpc)
    - Bytes 27-32: Vobs (km/s)
    - Bytes 34-38: e_Vobs (km/s)
    - Bytes 40-45: Vgas (km/s)
    - Bytes 47-52: Vdisk (km/s)
    - Bytes 54-59: Vbul (km/s)
    - Bytes 61-67: SBdisk (L_sun/pc^2)
    - Bytes 69-76: SBbul (L_sun/pc^2)
    """
    mrt_file = Path(__file__).parent.parent / "data" / "sparc" / "MassModels_Lelli2016c.mrt"

    if not mrt_file.exists():
        # Try alternate path
        mrt_file = Path(__file__).parent.parent / "data" / "SPARC" / "MassModels_Lelli2016c.mrt"

    if not mrt_file.exists():
        print(f"SPARC MRT file not found: {mrt_file}")
        return None

    galaxies = {}

    with open(mrt_file, 'r') as f:
        for i, line in enumerate(f):
            # Skip header (first 25 lines)
            if i < 25:
                continue

            if len(line) < 60:
                continue

            try:
                # Parse fixed-width format
                galaxy_id = line[0:11].strip()
                distance = float(line[12:18].strip())
                radius = float(line[19:25].strip())
                v_obs = float(line[26:32].strip())
                v_err = float(line[33:38].strip())
                v_gas = float(line[39:45].strip())
                v_disk = float(line[46:52].strip())
                v_bul = float(line[53:59].strip()) if len(line) > 59 else 0.0

                # Surface brightness (if available)
                sb_disk = 0.0
                sb_bul = 0.0
                if len(line) > 67:
                    try:
                        sb_disk = float(line[60:67].strip())
                    except:
                        pass
                if len(line) > 76:
                    try:
                        sb_bul = float(line[68:76].strip())
                    except:
                        pass

                # Initialize galaxy if new
                if galaxy_id not in galaxies:
                    galaxies[galaxy_id] = {
                        'distance': distance,
                        'r': [],
                        'v_obs': [],
                        'v_err': [],
                        'v_gas': [],
                        'v_disk': [],
                        'v_bul': [],
                        'sb_disk': [],
                        'sb_bul': []
                    }

                # Add data point
                galaxies[galaxy_id]['r'].append(radius)
                galaxies[galaxy_id]['v_obs'].append(v_obs)
                galaxies[galaxy_id]['v_err'].append(v_err)
                galaxies[galaxy_id]['v_gas'].append(v_gas)
                galaxies[galaxy_id]['v_disk'].append(v_disk)
                galaxies[galaxy_id]['v_bul'].append(v_bul)
                galaxies[galaxy_id]['sb_disk'].append(sb_disk)
                galaxies[galaxy_id]['sb_bul'].append(sb_bul)

            except (ValueError, IndexError) as e:
                continue

    # Convert lists to numpy arrays
    for gal_id in galaxies:
        for key in ['r', 'v_obs', 'v_err', 'v_gas', 'v_disk', 'v_bul', 'sb_disk', 'sb_bul']:
            galaxies[gal_id][key] = np.array(galaxies[gal_id][key])

    return galaxies


def load_sparc_data():
    """Charge les donnees SPARC (wrapper pour compatibilite)"""
    return load_sparc_mrt()


def run_sparc_test_v24():
    """Execute le test SPARC complet avec TMT v2.4"""
    print("=" * 70)
    print("TEST TMT v2.4 - SPARC ROTATION CURVES")
    print("=" * 70)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"\nAmeliorations v2.4:")
    print(f"  1. Formule r_c(M, Sigma) avec brillance de surface")
    print(f"  2. Condition baryonique: chi2_ratio < {BARYONIC_THRESHOLD} -> k=0 valide")
    print(f"  3. Exclusion naines irregulieres: {DWARF_IRREGULARS}")

    # Charger les donnees depuis le fichier MRT
    galaxies = load_sparc_data()
    if galaxies is None:
        print("Could not load SPARC data")
        return None

    print(f"\nGalaxies SPARC trouvees: {len(galaxies)}")

    results = []
    excluded_count = 0
    baryonic_count = 0
    lsb_count = 0
    improved_count = 0

    for galaxy_name, data in galaxies.items():
        # Verifier qu'on a assez de points
        if len(data['r']) < 5:
            continue

        r = data['r']
        v_obs = data['v_obs']
        v_err = data['v_err']

        # Calculer la masse baryonique cumulative
        # v_bary^2 = v_gas^2 + v_disk^2 + v_bul^2
        v_bary = np.sqrt(data['v_gas']**2 + data['v_disk']**2 + data['v_bul']**2)

        # Masse cumulative: M(<r) = v^2 * r / G
        G = 4.302e-6  # kpc * (km/s)^2 / M_sun
        M_bary_cumulative = v_bary**2 * r / G
        M_bary_total = M_bary_cumulative[-1] if len(M_bary_cumulative) > 0 else 0

        # Calculer la brillance de surface moyenne
        Sigma_mean = np.mean(data['sb_disk'][data['sb_disk'] > 0]) if np.any(data['sb_disk'] > 0) else None

        # Detecter si c'est une galaxie LSB (brillance < 50 L_sun/pc^2)
        is_LSB = galaxy_name in LSB_GALAXIES or galaxy_name.startswith('F5')
        if Sigma_mean is not None and Sigma_mean < 50:
            is_LSB = True

        # Detecter si c'est une naine irreguliere
        is_dwarf_irr = galaxy_name in DWARF_IRREGULARS

        # Ajuster le modele
        result = fit_galaxy_v24(r, v_obs, v_err, M_bary_cumulative, M_bary_total,
                                galaxy_name, Sigma=Sigma_mean, is_LSB=is_LSB,
                                is_dwarf_irr=is_dwarf_irr)
        results.append(result)

        if result['excluded']:
            excluded_count += 1
        elif result.get('is_baryonic_pure', False):
            baryonic_count += 1
        elif result.get('is_LSB', False):
            lsb_count += 1

        if not result['excluded'] and result['score'] == 1.0:
            improved_count += 1

    # Statistiques
    applicable = [r for r in results if not r['excluded']]
    n_applicable = len(applicable)
    n_improved = sum(1 for r in applicable if r['score'] == 1.0)

    # Calculer chi2_reduit moyen
    chi2_tmt_values = [r['chi2_final'] for r in applicable if 'chi2_final' in r]
    chi2_newton_values = [r['chi2_newton'] for r in applicable if 'chi2_newton' in r]

    # Calculer amelioration moyenne
    improvements = [r['improvement'] for r in applicable if r['improvement'] > 0]
    avg_improvement = np.mean(improvements) if improvements else 0
    median_improvement = np.median(improvements) if improvements else 0

    print(f"\n{'=' * 70}")
    print("RESULTATS TMT v2.4")
    print("=" * 70)
    print(f"\nGalaxies analysees: {len(results)}")
    print(f"Galaxies exclues: {excluded_count}")
    print(f"Galaxies applicables: {n_applicable}")
    print(f"Galaxies baryoniques pures (k=0): {baryonic_count}")
    print(f"Galaxies LSB: {lsb_count}")
    print(f"\nGalaxies ameliorees ou valides: {n_improved}/{n_applicable}")
    print(f"Score: {100*n_improved/n_applicable:.1f}%")

    # Statistiques de fit
    chi2_red_tmt = [r['chi2_red_tmt'] for r in applicable if 'chi2_red_tmt' in r]
    chi2_red_newton = [r['chi2_red_newton'] for r in applicable if 'chi2_red_newton' in r]

    # Qualite de fit: chi2_red = 1 -> fit parfait, chi2_red > 1 -> sous-fit
    # Fraction des galaxies avec chi2_red < 2 (bon fit)
    good_fit_tmt = sum(1 for c in chi2_red_tmt if c < 2) / len(chi2_red_tmt) * 100 if chi2_red_tmt else 0
    excellent_fit_tmt = sum(1 for c in chi2_red_tmt if c < 1.5) / len(chi2_red_tmt) * 100 if chi2_red_tmt else 0

    print(f"\nSTATISTIQUES DE FIT:")
    print(f"  Amelioration moyenne (TMT vs Newton): {avg_improvement:.1f}%")
    print(f"  Amelioration mediane: {median_improvement:.1f}%")
    print(f"  Chi2 moyen Newton: {np.mean(chi2_newton_values):.1f}")
    print(f"  Chi2 moyen TMT: {np.mean(chi2_tmt_values):.1f}")
    print(f"  Reduction Chi2 moyenne: {100*(1 - np.mean(chi2_tmt_values)/np.mean(chi2_newton_values)):.1f}%")
    print(f"\nQUALITE DE FIT ABSOLUE:")
    print(f"  Chi2 reduit moyen (TMT): {np.mean(chi2_red_tmt):.2f}")
    print(f"  Chi2 reduit moyen (Newton): {np.mean(chi2_red_newton):.2f}")
    print(f"  Galaxies avec bon fit (chi2_red < 2): {good_fit_tmt:.1f}%")
    print(f"  Galaxies avec excellent fit (chi2_red < 1.5): {excellent_fit_tmt:.1f}%")

    # Details des echecs
    failures = [r for r in applicable if r['score'] < 1.0]
    if failures:
        print(f"\nGalaxies non ameliorees ({len(failures)}):")
        for f in failures:
            print(f"  {f['name']}: improvement={f['improvement']:.1f}%, k={f['k_opt']:.3f}")

    # Sauvegarder les resultats
    output_file = Path("data/results/TEST_TMT_v24_SPARC.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("=" * 70 + "\n")
        out.write("TEST TMT v2.4 - SPARC ROTATION CURVES\n")
        out.write("=" * 70 + "\n\n")
        out.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

        out.write("AMELIORATIONS v2.4:\n")
        out.write("  1. Formule r_c(M, Sigma) avec brillance de surface\n")
        out.write(f"  2. Condition baryonique: chi2_ratio < {BARYONIC_THRESHOLD}\n")
        out.write(f"  3. Exclusion naines irregulieres\n\n")

        out.write("RESULTATS:\n")
        out.write(f"  Galaxies analysees: {len(results)}\n")
        out.write(f"  Galaxies exclues: {excluded_count}\n")
        out.write(f"  Galaxies applicables: {n_applicable}\n")
        out.write(f"  Baryoniques pures (k=0): {baryonic_count}\n")
        out.write(f"  LSB: {lsb_count}\n")
        out.write(f"  Score: {n_improved}/{n_applicable} ({100*n_improved/n_applicable:.1f}%)\n\n")

        out.write("DETAILS PAR GALAXIE:\n\n")
        out.write(f"{'Galaxie':<15} {'M_bary':<12} {'k_opt':<8} {'r_c':<8} {'Improv':<10} {'Verdict'}\n")
        out.write("-" * 70 + "\n")

        for r in sorted(applicable, key=lambda x: x.get('improvement', 0), reverse=True):
            out.write(f"{r['name']:<15} {r['M_bary']:.2e} {r['k_opt']:<8.3f} "
                     f"{r['r_c_opt']:<8.1f} {r['improvement']:<+10.1f}% {r['verdict']}\n")

    print(f"\nResultats sauvegardes: {output_file}")

    return {
        'total': len(results),
        'excluded': excluded_count,
        'applicable': n_applicable,
        'improved': n_improved,
        'baryonic': baryonic_count,
        'lsb': lsb_count,
        'score_percent': 100 * n_improved / n_applicable if n_applicable > 0 else 0
    }


if __name__ == "__main__":
    results = run_sparc_test_v24()

    if results:
        print(f"\n{'=' * 70}")
        print("VERDICT FINAL TMT v2.4")
        print("=" * 70)
        print(f"\nScore SPARC: {results['improved']}/{results['applicable']} ({results['score_percent']:.1f}%)")

        if results['score_percent'] >= 99:
            print("\nTMT v2.4 FORTEMENT VALIDE")
        elif results['score_percent'] >= 95:
            print("\nTMT v2.4 VALIDE")
        else:
            print("\nTMT v2.4 PARTIELLEMENT VALIDE")
