#!/usr/bin/env python3
"""
INVESTIGATION r_c : Pourquoi 5 vs 10 vs 18 kpc?
================================================

Analyse des différentes valeurs de r_c obtenues selon les méthodes.

Conclusion préliminaire:
- r_c = 18 kpc : données SIMULÉES (obsolète)
- r_c = 5 kpc  : médiane des optimums INDIVIDUELS
- r_c = 10 kpc : optimum GLOBAL sur l'ensemble

Ce script analyse la distribution pour réconcilier ces valeurs.

Auteur: Pierre-Olivier Després Asselin
Date: Janvier 2026
"""

import numpy as np
from scipy.optimize import minimize
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Constantes
G_KPC = 4.302e-6  # kpc (km/s)² / M_sun


def load_sparc_data(data_dir):
    """Charge les données SPARC réelles."""
    models_file = data_dir / "MassModels_Lelli2016c.mrt"

    rotation_curves = {}
    with open(models_file, 'r') as f:
        for line in f:
            if line.startswith(('Title', 'Authors', 'Table', '=', '-', 'Byte', ' ', 'Note')):
                continue
            if not line.strip():
                continue
            try:
                name = line[0:11].strip()
                if not name or name in ('ID', 'Galaxy'):
                    continue
                R = float(line[19:25].strip())
                Vobs = float(line[26:32].strip())
                e_Vobs = float(line[33:38].strip())
                Vgas = float(line[39:45].strip())
                Vdisk = float(line[46:52].strip())
                Vbul = float(line[53:59].strip())

                if name not in rotation_curves:
                    rotation_curves[name] = {'R': [], 'Vobs': [], 'e_Vobs': [],
                                             'Vgas': [], 'Vdisk': [], 'Vbul': []}
                rotation_curves[name]['R'].append(R)
                rotation_curves[name]['Vobs'].append(Vobs)
                rotation_curves[name]['e_Vobs'].append(max(e_Vobs, 1.0))
                rotation_curves[name]['Vgas'].append(Vgas)
                rotation_curves[name]['Vdisk'].append(Vdisk)
                rotation_curves[name]['Vbul'].append(Vbul)
            except:
                continue

    for name in rotation_curves:
        for key in rotation_curves[name]:
            rotation_curves[name][key] = np.array(rotation_curves[name][key])

    return rotation_curves


def compute_baryonic(rc, ML_disk=0.5, ML_bul=0.7):
    """Calcule vitesse et masse baryonique."""
    V_bary_sq = rc['Vgas']**2 + ML_disk * rc['Vdisk']**2 + ML_bul * rc['Vbul']**2
    V_bary = np.sqrt(np.maximum(V_bary_sq, 0))
    M_bary_enc = V_bary**2 * rc['R'] / G_KPC
    return V_bary, M_bary_enc


def v_rotation_quantum(r, M_bary_enc, r_c, n):
    """Vitesse de rotation avec superposition quantique."""
    mult = 1.0 + (r / r_c) ** n
    M_eff = M_bary_enc * mult
    v_sq = G_KPC * M_eff / r
    return np.sqrt(np.maximum(v_sq, 0))


def chi2_galaxy(params, R, Vobs, e_Vobs, M_bary_enc):
    """Chi² pour une galaxie."""
    r_c, n = params
    if r_c <= 0 or n <= 0:
        return 1e10
    V_model = v_rotation_quantum(R, M_bary_enc, r_c, n)
    residuals = (V_model - Vobs) / e_Vobs
    return np.sum(residuals**2) / max(len(R) - 2, 1)


def optimize_individual(R, Vobs, e_Vobs, M_bary_enc):
    """Optimise r_c et n pour une galaxie individuelle."""
    best_result = None
    best_chi2 = np.inf

    for r_c_init in [2, 5, 10, 20, 40]:
        for n_init in [0.3, 0.6, 1.0, 1.5, 2.0]:
            try:
                result = minimize(
                    chi2_galaxy,
                    [r_c_init, n_init],
                    args=(R, Vobs, e_Vobs, M_bary_enc),
                    bounds=[(0.1, 200), (0.1, 5)],
                    method='L-BFGS-B'
                )
                if result.fun < best_chi2:
                    best_chi2 = result.fun
                    best_result = result
            except:
                continue

    if best_result is not None:
        return best_result.x[0], best_result.x[1], best_chi2
    return np.nan, np.nan, np.inf


def main():
    print("=" * 75)
    print("INVESTIGATION r_c : Pourquoi 5 vs 10 vs 18 kpc?")
    print("=" * 75)

    # Charger données
    data_dir = Path(__file__).parent.parent / "data" / "SPARC"
    print("\n[1/4] Chargement données SPARC réelles...")
    rotation_curves = load_sparc_data(data_dir)
    print(f"      {len(rotation_curves)} galaxies chargées")

    # Optimisation individuelle
    print("\n[2/4] Optimisation INDIVIDUELLE de r_c et n...")

    r_c_individuals = []
    n_individuals = []
    galaxy_data = []

    for i, (name, rc) in enumerate(rotation_curves.items()):
        if len(rc['R']) < 5:
            continue

        R = rc['R']
        Vobs = rc['Vobs']
        e_Vobs = rc['e_Vobs']
        V_bary, M_bary_enc = compute_baryonic(rc)

        r_c_opt, n_opt, chi2_opt = optimize_individual(R, Vobs, e_Vobs, M_bary_enc)

        if 0.1 < r_c_opt < 200 and 0.1 < n_opt < 5:
            r_c_individuals.append(r_c_opt)
            n_individuals.append(n_opt)
            galaxy_data.append({
                'name': name,
                'r_c': r_c_opt,
                'n': n_opt,
                'chi2': chi2_opt,
                'R_max': R[-1],
                'M_bary': M_bary_enc[-1]
            })

        if (i + 1) % 30 == 0:
            print(f"      {i+1}/{len(rotation_curves)} galaxies...")

    r_c_individuals = np.array(r_c_individuals)
    n_individuals = np.array(n_individuals)

    print(f"\n      {len(r_c_individuals)} galaxies avec paramètres valides")

    # Statistiques distribution r_c
    print("\n[3/4] Distribution de r_c individuel...")

    percentiles = [10, 25, 50, 75, 90]
    print("\n      Percentiles r_c:")
    for p in percentiles:
        val = np.percentile(r_c_individuals, p)
        print(f"        {p}%: {val:.1f} kpc")

    print(f"\n      Statistiques r_c:")
    print(f"        Moyenne:     {np.mean(r_c_individuals):.1f} kpc")
    print(f"        Médiane:     {np.median(r_c_individuals):.1f} kpc")
    print(f"        Écart-type:  {np.std(r_c_individuals):.1f} kpc")
    print(f"        Min:         {np.min(r_c_individuals):.1f} kpc")
    print(f"        Max:         {np.max(r_c_individuals):.1f} kpc")

    # Optimisation globale
    print("\n[4/4] Optimisation GLOBALE de r_c et n...")

    def total_chi2(params):
        r_c, n = params
        if r_c <= 0 or n <= 0:
            return 1e10
        total = 0
        count = 0
        for name, rc in rotation_curves.items():
            if len(rc['R']) < 5:
                continue
            R = rc['R']
            Vobs = rc['Vobs']
            e_Vobs = rc['e_Vobs']
            V_bary, M_bary_enc = compute_baryonic(rc)
            V_model = v_rotation_quantum(R, M_bary_enc, r_c, n)
            chi2 = np.sum(((V_model - Vobs) / e_Vobs)**2)
            total += chi2
            count += len(R)
        return total / max(count, 1)

    result = minimize(total_chi2, [10, 1.0], bounds=[(0.1, 100), (0.1, 3)], method='L-BFGS-B')
    r_c_global, n_global = result.x

    print(f"\n      r_c GLOBAL = {r_c_global:.2f} kpc")
    print(f"      n GLOBAL   = {n_global:.2f}")

    # Résumé et interprétation
    print("\n" + "=" * 75)
    print("RÉCONCILIATION DES VALEURS r_c")
    print("=" * 75)

    print(f"""
    ================================================================
                      RECONCILIATION r_c
    ================================================================

    Valeur    | Source                  | Statut
    ----------|-------------------------|---------------------------
    18 kpc    | Donnees SIMULEES        | [X] OBSOLETE
    ~5 kpc    | MEDIANE individuelle    | [OK] Valeur TYPIQUE
    ~10 kpc   | Optimum GLOBAL          | [OK] Valeur MOYENNE ponderee

    ================================================================
                          EXPLICATION
    ================================================================

    La distribution de r_c est ASYMETRIQUE avec une longue queue
    vers les grandes valeurs.

    - La MEDIANE (~5 kpc) represente la galaxie "typique"
    - L'optimum GLOBAL (~10 kpc) est tire vers le haut par les
      galaxies massives qui contribuent plus au chi2 total

    Les deux valeurs sont VALIDES pour des usages differents:

    * r_c = 5 kpc  -> galaxies individuelles (mediane)
    * r_c = 10 kpc -> modele global (meilleur fit d'ensemble)

    ================================================================
                        RECOMMANDATION
    ================================================================

    VALEUR CANONIQUE:  r_c = {np.median(r_c_individuals):.0f} - {r_c_global:.0f} kpc

    Pour publications:
    - Mediane: {np.median(r_c_individuals):.1f} kpc (IC 25-75%: [{np.percentile(r_c_individuals, 25):.1f}, {np.percentile(r_c_individuals, 75):.1f}] kpc)
    - Globale: {r_c_global:.1f} kpc

    ABANDONNER la valeur 18 kpc (basee sur donnees simulees)

    ================================================================
    """)

    # Corrélation r_c avec propriétés
    print("\n[BONUS] Corrélation r_c avec propriétés galactiques...")

    M_bary_array = np.array([g['M_bary'] for g in galaxy_data])
    R_max_array = np.array([g['R_max'] for g in galaxy_data])
    r_c_array = np.array([g['r_c'] for g in galaxy_data])

    # Corrélation r_c vs M_bary
    from scipy.stats import pearsonr, spearmanr

    valid = (M_bary_array > 0) & (r_c_array > 0)
    if np.sum(valid) > 10:
        r_pearson, p_pearson = pearsonr(np.log10(M_bary_array[valid]), np.log10(r_c_array[valid]))
        r_spearman, p_spearman = spearmanr(M_bary_array[valid], r_c_array[valid])

        print(f"\n      r_c vs log(M_bary):")
        print(f"        Pearson:  r = {r_pearson:.3f} (p = {p_pearson:.2e})")
        print(f"        Spearman: rho = {r_spearman:.3f} (p = {p_spearman:.2e})")

        if abs(r_pearson) > 0.3 and p_pearson < 0.01:
            print(f"\n      => r_c DEPEND de la masse!")
            print(f"      => Suggere r_c(M) plutot qu'un r_c universel")

            # Fit r_c(M)
            log_M = np.log10(M_bary_array[valid])
            log_rc = np.log10(r_c_array[valid])
            coeffs = np.polyfit(log_M, log_rc, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            print(f"\n      Relation empirique:")
            print(f"        log(r_c) = {slope:.3f} * log(M_bary) + {intercept:.3f}")
            print(f"        r_c = {10**intercept:.2e} * (M_bary)^{slope:.2f}")

    # Corrélation r_c vs R_max
    valid2 = (R_max_array > 0) & (r_c_array > 0)
    if np.sum(valid2) > 10:
        r_pearson2, p_pearson2 = pearsonr(R_max_array[valid2], r_c_array[valid2])
        print(f"\n      r_c vs R_max:")
        print(f"        Pearson: r = {r_pearson2:.3f} (p = {p_pearson2:.2e})")

    # Sauvegarder résultats
    output_dir = Path(__file__).parent.parent / "data" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    results_file = output_dir / "investigation_r_c.txt"
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("INVESTIGATION r_c : RÉCONCILIATION DES VALEURS\n")
        f.write("=" * 70 + "\n\n")

        f.write("VALEURS OBSERVÉES\n")
        f.write(f"  - Données simulées:    18 kpc (OBSOLÈTE)\n")
        f.write(f"  - Médiane individuelle: {np.median(r_c_individuals):.1f} kpc\n")
        f.write(f"  - Optimum global:       {r_c_global:.1f} kpc\n\n")

        f.write("STATISTIQUES DISTRIBUTION r_c\n")
        f.write(f"  Moyenne:    {np.mean(r_c_individuals):.1f} kpc\n")
        f.write(f"  Médiane:    {np.median(r_c_individuals):.1f} kpc\n")
        f.write(f"  Écart-type: {np.std(r_c_individuals):.1f} kpc\n")
        f.write(f"  IC 25-75%:  [{np.percentile(r_c_individuals, 25):.1f}, {np.percentile(r_c_individuals, 75):.1f}] kpc\n\n")

        f.write("CONCLUSION\n")
        f.write(f"  Valeur canonique: {np.median(r_c_individuals):.0f} - {r_c_global:.0f} kpc\n")
        f.write(f"  Abandonner 18 kpc (données simulées)\n")

    print(f"\nRésultats sauvegardés: {results_file}")

    return {
        'r_c_median': np.median(r_c_individuals),
        'r_c_global': r_c_global,
        'r_c_mean': np.mean(r_c_individuals),
        'r_c_std': np.std(r_c_individuals),
        'n_global': n_global
    }


if __name__ == "__main__":
    main()
