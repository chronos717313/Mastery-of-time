#!/usr/bin/env python3
"""
Test TMT v2.0 avec les VRAIES données SPARC (175 galaxies)
Calibration de la loi k = a × (M/10^10)^b

Données: http://astroweb.cwru.edu/SPARC/
Référence: Lelli, McGaugh & Schombert (2016)
"""

import numpy as np
from scipy.optimize import minimize_scalar, curve_fit
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Constantes
G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
C_KMS = 299792.458  # km/s
M_SUN_NOMINAL = 1.0  # Masse solaire en unités solaires

# Paramètres TMT v2.0
R_C_DEFAULT = 18.0  # kpc - rayon critique calibré
N_DEFAULT = 1.6     # exposant calibré


def parse_sparc_table(filepath):
    """Parse SPARC_Lelli2016c.mrt - propriétés des galaxies."""
    galaxies = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Trouver la dernière ligne de séparateur
    last_sep = 0
    for i, line in enumerate(lines):
        if line.startswith('---'):
            last_sep = i

    # Parser les données - format fixe selon documentation
    # Bytes: 1-11=Galaxy, 12-13=T, 14-19=D, 27-30=Inc, 35-41=L[3.6], 62-66=Rdisk, 75-81=MHI, 87-91=Vflat, 97-99=Q
    for line in lines[last_sep + 1:]:
        if not line.strip() or len(line) < 99:
            continue
        try:
            name = line[0:11].strip()
            if not name:
                continue
            hubble_type = int(line[11:13].strip()) if line[11:13].strip().isdigit() else 0
            distance = float(line[13:19].strip()) if line[13:19].strip() else 0
            inclination = float(line[26:30].strip()) if line[26:30].strip() else 0
            L_36 = float(line[34:41].strip()) if line[34:41].strip() else 0  # 10^9 L_sun
            R_disk = float(line[61:66].strip()) if line[61:66].strip() else 0  # kpc
            M_HI = float(line[74:81].strip()) if line[74:81].strip() else 0  # 10^9 M_sun
            V_flat = float(line[86:91].strip()) if line[86:91].strip() else 0  # km/s
            quality = int(line[96:99].strip()) if line[96:99].strip().isdigit() else 2

            galaxies[name] = {
                'hubble_type': hubble_type,
                'distance': distance,
                'inclination': inclination,
                'L_36': L_36 * 1e9,  # L_sun
                'R_disk': R_disk,
                'M_HI': M_HI * 1e9,  # M_sun
                'V_flat': V_flat,
                'quality': quality
            }
        except (ValueError, IndexError) as e:
            continue

    return galaxies


def parse_mass_models(filepath):
    """Parse MassModels_Lelli2016c.mrt - courbes de rotation."""
    rotation_curves = {}

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith(('Title', 'Authors', 'Table', '=', '-', 'Byte', ' ', 'Note')):
                continue
            if not line.strip():
                continue

            try:
                name = line[0:11].strip()
                if not name or name in ('ID', 'Galaxy'):
                    continue

                D = float(line[12:18].strip())      # Mpc
                R = float(line[19:25].strip())      # kpc
                Vobs = float(line[26:32].strip())   # km/s
                e_Vobs = float(line[33:38].strip()) # km/s
                Vgas = float(line[39:45].strip())   # km/s
                Vdisk = float(line[46:52].strip())  # km/s
                Vbul = float(line[53:59].strip())   # km/s

                if name not in rotation_curves:
                    rotation_curves[name] = {
                        'R': [], 'Vobs': [], 'e_Vobs': [],
                        'Vgas': [], 'Vdisk': [], 'Vbul': [],
                        'distance': D
                    }

                rotation_curves[name]['R'].append(R)
                rotation_curves[name]['Vobs'].append(Vobs)
                rotation_curves[name]['e_Vobs'].append(max(e_Vobs, 1.0))  # Min 1 km/s
                rotation_curves[name]['Vgas'].append(Vgas)
                rotation_curves[name]['Vdisk'].append(Vdisk)
                rotation_curves[name]['Vbul'].append(Vbul)

            except (ValueError, IndexError):
                continue

    # Convertir en arrays numpy
    for name in rotation_curves:
        for key in ['R', 'Vobs', 'e_Vobs', 'Vgas', 'Vdisk', 'Vbul']:
            rotation_curves[name][key] = np.array(rotation_curves[name][key])

    return rotation_curves


def compute_V_bary(Vgas, Vdisk, Vbul, ML_disk=0.5, ML_bul=0.7):
    """
    Calcule la vitesse baryonique.

    V_bary² = Vgas² + ML_disk × Vdisk² + ML_bul × Vbul²

    ML_disk et ML_bul sont les rapports masse/luminosité à [3.6]
    Valeurs typiques: 0.5 pour disque, 0.7 pour bulbe (McGaugh & Schombert 2014)
    """
    V_bary_sq = Vgas**2 + ML_disk * Vdisk**2 + ML_bul * Vbul**2
    return np.sqrt(np.maximum(V_bary_sq, 0))


def compute_M_bary_enclosed(R, Vgas, Vdisk, Vbul, ML_disk=0.5, ML_bul=0.7):
    """
    Calcule la masse baryonique encerclée à partir des vitesses.

    M(<R) = V²(R) × R / G
    """
    V_bary = compute_V_bary(Vgas, Vdisk, Vbul, ML_disk, ML_bul)
    M_enc = V_bary**2 * R / G_KPC
    return M_enc


def V_TMT_v2(R, M_bary_enc, r_c=R_C_DEFAULT, n=N_DEFAULT):
    """
    Vitesse de rotation TMT v2.0 avec superposition temporelle.

    M_eff(R) = M_bary(R) × [1 + (R/r_c)^n]
    V_TMT = sqrt(G × M_eff / R)
    """
    multiplier = 1.0 + (R / r_c) ** n
    M_eff = M_bary_enc * multiplier
    V_sq = G_KPC * M_eff / R
    return np.sqrt(np.maximum(V_sq, 0))


def V_TMT_with_k(R, M_bary_enc, k, r_c=R_C_DEFAULT):
    """
    Vitesse TMT avec paramètre k direct.

    M_eff(R) = M_bary(R) × [1 + k × (R/r_c)]

    Note: Simplifié avec n=1 pour calibration de k
    """
    multiplier = 1.0 + k * (R / r_c)
    M_eff = M_bary_enc * multiplier
    V_sq = G_KPC * M_eff / R
    return np.sqrt(np.maximum(V_sq, 0))


def chi2_reduced(V_model, V_obs, e_V, n_params=1):
    """Chi² réduit."""
    residuals = (V_model - V_obs) / e_V
    chi2 = np.sum(residuals**2)
    dof = len(V_obs) - n_params
    return chi2 / max(dof, 1)


def optimize_k_for_galaxy(R, Vobs, e_Vobs, M_bary_enc, r_c=R_C_DEFAULT):
    """
    Trouve le k optimal pour une galaxie.
    """
    def objective(k):
        V_model = V_TMT_with_k(R, M_bary_enc, k, r_c)
        return chi2_reduced(V_model, Vobs, e_Vobs, n_params=1)

    # Recherche dans un large intervalle
    result = minimize_scalar(objective, bounds=(0.001, 100), method='bounded')
    return result.x, result.fun


def optimize_rc_n_for_galaxy(R, Vobs, e_Vobs, M_bary_enc):
    """
    Optimise r_c et n pour une galaxie avec formule complète.
    """
    from scipy.optimize import minimize

    def objective(params):
        r_c, n = params
        if r_c <= 0 or n <= 0:
            return 1e10
        V_model = V_TMT_v2(R, M_bary_enc, r_c, n)
        return chi2_reduced(V_model, Vobs, e_Vobs, n_params=2)

    # Plusieurs points de départ
    best_result = None
    best_chi2 = np.inf

    for r_c_init in [5, 10, 18, 30, 50]:
        for n_init in [0.5, 1.0, 1.6, 2.0]:
            try:
                result = minimize(objective, [r_c_init, n_init],
                                bounds=[(0.1, 200), (0.1, 5)],
                                method='L-BFGS-B')
                if result.fun < best_chi2:
                    best_chi2 = result.fun
                    best_result = result
            except:
                continue

    if best_result is not None:
        return best_result.x[0], best_result.x[1], best_chi2
    return R_C_DEFAULT, N_DEFAULT, np.inf


def k_law(M, a, b):
    """Loi k = a × (M/10^10)^b"""
    return a * (M / 1e10) ** b


def main():
    print("=" * 70)
    print("TEST TMT v2.0 - DONNÉES SPARC RÉELLES (175 galaxies)")
    print("=" * 70)

    # Chemins des fichiers
    data_dir = Path(__file__).parent.parent / "data" / "SPARC"
    table_file = data_dir / "SPARC_Lelli2016c.mrt"
    models_file = data_dir / "MassModels_Lelli2016c.mrt"

    # Charger les données
    print("\n[1/5] Chargement des données SPARC...")
    galaxies_props = parse_sparc_table(table_file)
    rotation_curves = parse_mass_models(models_file)

    print(f"      Propriétés: {len(galaxies_props)} galaxies")
    print(f"      Courbes de rotation: {len(rotation_curves)} galaxies")

    # Analyser chaque galaxie
    print("\n[2/5] Analyse des courbes de rotation...")

    results = []
    ML_disk = 0.5  # Rapport M/L typique pour disque à [3.6]
    ML_bul = 0.7   # Rapport M/L typique pour bulbe

    for name, rc in rotation_curves.items():
        R = rc['R']
        Vobs = rc['Vobs']
        e_Vobs = rc['e_Vobs']

        # Calcul vitesse et masse baryonique
        V_bary = compute_V_bary(rc['Vgas'], rc['Vdisk'], rc['Vbul'], ML_disk, ML_bul)
        M_bary_enc = compute_M_bary_enclosed(R, rc['Vgas'], rc['Vdisk'], rc['Vbul'], ML_disk, ML_bul)

        # Masse baryonique totale (au dernier rayon)
        M_bary_total = M_bary_enc[-1] if len(M_bary_enc) > 0 else 0

        # Chi² Newton (baryons seuls)
        chi2_newton = chi2_reduced(V_bary, Vobs, e_Vobs, n_params=0)

        # Optimiser k
        k_opt, chi2_k = optimize_k_for_galaxy(R, Vobs, e_Vobs, M_bary_enc)

        # Optimiser r_c et n (formule complète)
        r_c_opt, n_opt, chi2_full = optimize_rc_n_for_galaxy(R, Vobs, e_Vobs, M_bary_enc)

        # Amélioration
        improvement_k = (chi2_newton - chi2_k) / chi2_newton * 100 if chi2_newton > 0 else 0
        improvement_full = (chi2_newton - chi2_full) / chi2_newton * 100 if chi2_newton > 0 else 0

        # Propriétés de la galaxie
        props = galaxies_props.get(name, {})

        results.append({
            'name': name,
            'M_bary': M_bary_total,
            'L_36': props.get('L_36', 0),
            'M_HI': props.get('M_HI', 0),
            'V_flat': props.get('V_flat', 0),
            'R_disk': props.get('R_disk', 0),
            'quality': props.get('quality', 3),
            'n_points': len(R),
            'R_max': R[-1] if len(R) > 0 else 0,
            'chi2_newton': chi2_newton,
            'k_opt': k_opt,
            'chi2_k': chi2_k,
            'improvement_k': improvement_k,
            'r_c_opt': r_c_opt,
            'n_opt': n_opt,
            'chi2_full': chi2_full,
            'improvement_full': improvement_full
        })

    print(f"      {len(results)} galaxies analysées")

    # Filtrer les résultats valides
    valid_results = [r for r in results if r['M_bary'] > 0 and r['k_opt'] > 0.001 and r['k_opt'] < 100]
    print(f"      {len(valid_results)} galaxies avec k valide")

    # Statistiques globales
    print("\n[3/5] Statistiques globales...")

    improvements_k = [r['improvement_k'] for r in valid_results]
    improvements_full = [r['improvement_full'] for r in valid_results]

    n_improved_k = sum(1 for i in improvements_k if i > 0)
    n_improved_full = sum(1 for i in improvements_full if i > 0)

    print(f"\n      TMT v2.0 avec k optimisé:")
    print(f"        Amélioration moyenne: {np.mean(improvements_k):.1f}%")
    print(f"        Amélioration médiane: {np.median(improvements_k):.1f}%")
    print(f"        Galaxies améliorées: {n_improved_k}/{len(valid_results)} ({100*n_improved_k/len(valid_results):.0f}%)")

    print(f"\n      TMT v2.0 avec r_c, n optimisés:")
    print(f"        Amélioration moyenne: {np.mean(improvements_full):.1f}%")
    print(f"        Amélioration médiane: {np.median(improvements_full):.1f}%")
    print(f"        Galaxies améliorées: {n_improved_full}/{len(valid_results)} ({100*n_improved_full/len(valid_results):.0f}%)")

    # Calibration de la loi k(M)
    print("\n[4/5] Calibration de la loi k = a × (M/10^10)^b...")

    # Utiliser toutes les galaxies avec k et M_bary valides
    high_quality = [r for r in valid_results if r['M_bary'] > 1e6 and r['k_opt'] > 0.01 and r['k_opt'] < 50]
    print(f"      {len(high_quality)} galaxies avec k et M_bary valides")

    if len(high_quality) >= 10:
        M_array = np.array([r['M_bary'] for r in high_quality])
        k_array = np.array([r['k_opt'] for r in high_quality])

        # Fit en log-log
        log_M = np.log10(M_array / 1e10)
        log_k = np.log10(k_array)

        # Régression linéaire en log-log
        valid_mask = np.isfinite(log_M) & np.isfinite(log_k)
        if np.sum(valid_mask) >= 5:
            coeffs = np.polyfit(log_M[valid_mask], log_k[valid_mask], 1)
            b_fit = coeffs[0]
            a_fit = 10 ** coeffs[1]

            # R² du fit
            k_pred = k_law(M_array[valid_mask], a_fit, b_fit)
            ss_res = np.sum((k_array[valid_mask] - k_pred) ** 2)
            ss_tot = np.sum((k_array[valid_mask] - np.mean(k_array[valid_mask])) ** 2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

            print(f"\n      Loi calibrée (n={len(high_quality)} galaxies haute qualité):")
            print(f"        k = {a_fit:.4f} × (M/10^10)^{b_fit:.3f}")
            print(f"        R² = {r_squared:.4f}")
            print(f"\n      Comparaison avec calibration originale:")
            print(f"        Original: k = 0.343 × (M/10^10)^(-1.610)")
            print(f"        Nouveau:  k = {a_fit:.3f} × (M/10^10)^({b_fit:.3f})")
        else:
            print("      Pas assez de données valides pour le fit")
            a_fit, b_fit, r_squared = 0.343, -1.61, 0
    else:
        print(f"      Seulement {len(high_quality)} galaxies haute qualité - fit non fiable")
        a_fit, b_fit, r_squared = 0.343, -1.61, 0

    # Distribution de r_c et n optimaux
    print("\n[5/5] Distribution des paramètres optimaux...")

    r_c_values = [r['r_c_opt'] for r in valid_results if 0.1 < r['r_c_opt'] < 200]
    n_values = [r['n_opt'] for r in valid_results if 0.1 < r['n_opt'] < 5]

    print(f"\n      r_c optimal:")
    print(f"        Moyenne: {np.mean(r_c_values):.1f} kpc")
    print(f"        Médiane: {np.median(r_c_values):.1f} kpc")
    print(f"        Écart-type: {np.std(r_c_values):.1f} kpc")

    print(f"\n      n optimal:")
    print(f"        Moyenne: {np.mean(n_values):.2f}")
    print(f"        Médiane: {np.median(n_values):.2f}")
    print(f"        Écart-type: {np.std(n_values):.2f}")

    # Résumé final
    print("\n" + "=" * 70)
    print("RÉSUMÉ - TMT v2.0 sur SPARC réel")
    print("=" * 70)

    print(f"\nÉchantillon: {len(valid_results)} galaxies SPARC")
    print(f"\nPerformance TMT v2.0:")
    print(f"  - Amélioration médiane: {np.median(improvements_full):.1f}%")
    print(f"  - Galaxies améliorées: {n_improved_full}/{len(valid_results)} ({100*n_improved_full/len(valid_results):.0f}%)")

    print(f"\nLoi universelle calibrée:")
    print(f"  k = {a_fit:.4f} × (M/10^10)^{b_fit:.3f}")
    print(f"  R² = {r_squared:.4f}")

    print(f"\nParamètres optimaux moyens:")
    print(f"  r_c = {np.median(r_c_values):.1f} kpc (attendu: 18 kpc)")
    print(f"  n   = {np.median(n_values):.2f} (attendu: 1.6)")

    # Sauvegarder les résultats
    output_dir = Path(__file__).parent.parent / "data" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    results_file = output_dir / "TMT_v2_SPARC_reel_results.txt"
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("TMT v2.0 - TEST SUR DONNÉES SPARC RÉELLES\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Échantillon: {len(valid_results)} galaxies\n\n")

        f.write("Loi calibrée:\n")
        f.write(f"  k = {a_fit:.4f} × (M/10^10)^{b_fit:.3f}\n")
        f.write(f"  R² = {r_squared:.4f}\n\n")

        f.write("Paramètres optimaux:\n")
        f.write(f"  r_c médian = {np.median(r_c_values):.1f} kpc\n")
        f.write(f"  n médian   = {np.median(n_values):.2f}\n\n")

        f.write("Performance:\n")
        f.write(f"  Amélioration médiane: {np.median(improvements_full):.1f}%\n")
        f.write(f"  Galaxies améliorées: {n_improved_full}/{len(valid_results)}\n\n")

        f.write("=" * 70 + "\n")
        f.write("DÉTAILS PAR GALAXIE\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"{'Galaxie':<12} {'M_bary':>12} {'k_opt':>8} {'r_c':>8} {'n':>6} {'Improv':>8}\n")
        f.write("-" * 60 + "\n")

        for r in sorted(valid_results, key=lambda x: x['M_bary'], reverse=True):
            f.write(f"{r['name']:<12} {r['M_bary']:>12.2e} {r['k_opt']:>8.3f} "
                   f"{r['r_c_opt']:>8.1f} {r['n_opt']:>6.2f} {r['improvement_full']:>7.1f}%\n")

    print(f"\nRésultats sauvegardés: {results_file}")

    # Graphique
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # 1. k vs M_bary
        ax1 = axes[0, 0]
        M_plot = np.array([r['M_bary'] for r in valid_results])
        k_plot = np.array([r['k_opt'] for r in valid_results])
        ax1.scatter(M_plot, k_plot, alpha=0.5, s=20)

        if a_fit > 0:
            M_range = np.logspace(7, 12, 100)
            k_model = k_law(M_range, a_fit, b_fit)
            ax1.plot(M_range, k_model, 'r-', lw=2,
                    label=f'k = {a_fit:.3f}×(M/10¹⁰)^{b_fit:.2f}')
            ax1.legend()

        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('M_bary (M☉)')
        ax1.set_ylabel('k optimal')
        ax1.set_title('Loi k(M) - Calibration SPARC')
        ax1.grid(True, alpha=0.3)

        # 2. Distribution r_c
        ax2 = axes[0, 1]
        ax2.hist(r_c_values, bins=30, edgecolor='black', alpha=0.7)
        ax2.axvline(18, color='r', linestyle='--', label='r_c = 18 kpc (calibré)')
        ax2.axvline(np.median(r_c_values), color='g', linestyle='-',
                   label=f'Médiane = {np.median(r_c_values):.1f} kpc')
        ax2.set_xlabel('r_c optimal (kpc)')
        ax2.set_ylabel('Nombre de galaxies')
        ax2.set_title('Distribution de r_c')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Distribution n
        ax3 = axes[1, 0]
        ax3.hist(n_values, bins=30, edgecolor='black', alpha=0.7)
        ax3.axvline(1.6, color='r', linestyle='--', label='n = 1.6 (calibré)')
        ax3.axvline(np.median(n_values), color='g', linestyle='-',
                   label=f'Médiane = {np.median(n_values):.2f}')
        ax3.set_xlabel('n optimal')
        ax3.set_ylabel('Nombre de galaxies')
        ax3.set_title('Distribution de n')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. Amélioration vs M_bary
        ax4 = axes[1, 1]
        impr_plot = [r['improvement_full'] for r in valid_results]
        ax4.scatter(M_plot, impr_plot, alpha=0.5, s=20)
        ax4.axhline(0, color='k', linestyle='-', lw=0.5)
        ax4.axhline(np.median(impr_plot), color='r', linestyle='--',
                   label=f'Médiane = {np.median(impr_plot):.1f}%')
        ax4.set_xscale('log')
        ax4.set_xlabel('M_bary (M☉)')
        ax4.set_ylabel('Amélioration χ² (%)')
        ax4.set_title('Amélioration TMT v2.0 vs Newton')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        fig_file = output_dir / "TMT_v2_SPARC_reel_results.png"
        plt.savefig(fig_file, dpi=150)
        print(f"Graphique sauvegardé: {fig_file}")
        plt.close()

    except ImportError:
        print("matplotlib non disponible - pas de graphique")

    return a_fit, b_fit, r_squared


if __name__ == "__main__":
    main()
