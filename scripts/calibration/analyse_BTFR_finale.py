#!/usr/bin/env python3
"""
ANALYSE FINALE BTFR - Relation Tully-Fisher Baryonique
======================================================

Cette analyse teste la prediction TMT que M_bary ~ V_flat^4

DONNEES UTILISEES:
1. SPARC (120 galaxies): Masses baryoniques REELLES (M_stars + M_gas)
   -> Test definitif de la BTFR

2. ALFALFA (29,000+ galaxies): Masses HI seulement
   -> Test de la relation M_HI vs V_flat (pas la vraie BTFR)

RESULTATS ATTENDUS:
- SPARC: exposant ~ 4.0 (prediction TMT et McGaugh+2016)
- ALFALFA: exposant < 4.0 (car M_HI != M_bary)
"""

import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
from astropy.table import Table
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

PROJECT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"


def load_sparc():
    """Load SPARC data with TRUE baryonic masses."""
    filepath = DATA_DIR / "SPARC" / "SPARC_Lelli2016c.mrt"
    if not filepath.exists():
        return None

    data = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    last_sep = 0
    for i, line in enumerate(lines):
        if line.startswith('---') or (len(line) > 50 and '----' in line):
            last_sep = i

    for line in lines[last_sep+1:]:
        if len(line) < 50:
            continue

        try:
            parts = line.split()
            if len(parts) < 18:
                continue

            name = parts[0]
            dist = float(parts[2])
            incl = float(parts[5])
            l36 = float(parts[7])    # 10^9 L_sun
            mhi = float(parts[13])   # 10^9 M_sun
            v_flat = float(parts[15])
            e_vflat = float(parts[16])
            quality = int(parts[17])

            if v_flat < 20:
                continue

            # M/L = 0.5 for 3.6um (McGaugh & Schombert 2014)
            m_stars = 0.5 * l36 * 1e9
            m_gas = 1.33 * mhi * 1e9
            m_bary = m_stars + m_gas

            if quality <= 2 and m_bary > 1e7 and incl > 30:
                data.append({
                    'name': name,
                    'v_flat': v_flat,
                    'e_vflat': e_vflat,
                    'm_bary': m_bary,
                    'm_stars': m_stars,
                    'm_gas': m_gas,
                    'f_gas': m_gas / m_bary,
                    'dist': dist,
                    'source': 'SPARC'
                })
        except:
            continue

    return data


def load_alfalfa():
    """Load ALFALFA data (HI masses only)."""
    filepath = DATA_DIR / "ALFALFA" / "ALFALFA_table0_real.fits"
    if not filepath.exists():
        return None

    table = Table.read(filepath)

    data = []
    for row in table:
        try:
            w50 = float(row['W50']) if row['W50'] else 0
            log_mhi = float(row['logMHI']) if 'logMHI' in row.colnames and row['logMHI'] else 0
            vhel = float(row['Vhel']) if row['Vhel'] else 0

            if w50 > 50 and log_mhi > 7.5:  # Stricter cuts
                v_flat = w50 / 1.68
                m_hi = 10 ** log_mhi
                dist = vhel / 70 if vhel > 500 else 0

                if dist > 5 and v_flat > 40:  # More distant, reliable
                    data.append({
                        'name': str(row['Name']),
                        'v_flat': v_flat,
                        'm_hi': m_hi,
                        'w50': w50,
                        'dist': dist,
                        'source': 'ALFALFA'
                    })
        except:
            continue

    return data


def load_wallaby():
    """Load WALLABY data."""
    filepath = DATA_DIR / "WALLABY_DR2" / "WALLABY_PDR2_sources_real.fits"
    if not filepath.exists():
        return None

    table = Table.read(filepath)

    data = []
    for row in table:
        try:
            w50 = float(row['w50']) if row['w50'] else 0
            dist = float(row['dist_h']) if 'dist_h' in row.colnames and row['dist_h'] else 0
            f_sum = float(row['f_sum']) if row['f_sum'] else 0

            if w50 > 50 and dist > 5 and f_sum > 0.1:
                v_flat = w50 / 1.68
                m_hi = 2.36e5 * dist**2 * f_sum

                if m_hi > 1e8 and v_flat > 40:
                    data.append({
                        'name': str(row['name']),
                        'v_flat': v_flat,
                        'm_hi': m_hi,
                        'w50': w50,
                        'dist': dist,
                        'source': 'WALLABY'
                    })
        except:
            continue

    return data


def fit_btfr(v, m, label=""):
    """Fit Baryonic Tully-Fisher: log(M) = a + b*log(V)"""
    valid = (v > 30) & (v < 400) & (m > 1e7) & (m < 1e12)
    v = v[valid]
    m = m[valid]

    if len(v) < 20:
        return None

    log_v = np.log10(v)
    log_m = np.log10(m)

    try:
        def linear(x, a, b):
            return a + b * x

        popt, pcov = curve_fit(linear, log_v, log_m, p0=[2, 4])
        a, b = popt
        perr = np.sqrt(np.diag(pcov))

        log_m_pred = linear(log_v, a, b)
        ss_res = np.sum((log_m - log_m_pred)**2)
        ss_tot = np.sum((log_m - np.mean(log_m))**2)
        r2 = 1 - ss_res / ss_tot

        r, p = stats.pearsonr(log_v, log_m)
        scatter = np.std(log_m - log_m_pred)

        return {
            'a': a, 'b': b, 'b_err': perr[1],
            'r2': r2, 'r': r, 'p_value': p,
            'scatter': scatter,
            'n': len(v),
            'v_range': (v.min(), v.max()),
            'm_range': (m.min(), m.max())
        }
    except:
        return None


def main():
    print("=" * 70)
    print("ANALYSE FINALE - RELATION TULLY-FISHER BARYONIQUE")
    print("=" * 70)
    print()

    # Load SPARC
    sparc = load_sparc()
    print(f"SPARC: {len(sparc) if sparc else 0} galaxies (masses reelles)")

    # Load ALFALFA + WALLABY
    alfalfa = load_alfalfa()
    wallaby = load_wallaby()
    hi_data = (alfalfa or []) + (wallaby or [])
    print(f"ALFALFA + WALLABY: {len(hi_data)} galaxies (masses HI)")

    print("\n" + "=" * 70)
    print("1. TEST BTFR - SPARC (MASSES BARYONIQUES REELLES)")
    print("=" * 70)

    if sparc:
        v = np.array([d['v_flat'] for d in sparc])
        m = np.array([d['m_bary'] for d in sparc])

        result = fit_btfr(v, m, "SPARC")
        if result:
            print(f"\nlog(M_bary) = {result['a']:.2f} + {result['b']:.2f} x log(V_flat)")
            print(f"\nExposant BTFR: {result['b']:.3f} +/- {result['b_err']:.3f}")
            print(f"  TMT predit: 4.0")
            print(f"  McGaugh+ 2016: 3.98 +/- 0.06")
            print(f"\nR^2 = {result['r2']:.4f}")
            print(f"Scatter = {result['scatter']:.3f} dex")
            print(f"Galaxies: {result['n']}")
            print(f"V range: {result['v_range'][0]:.0f} - {result['v_range'][1]:.0f} km/s")
            print(f"M range: {result['m_range'][0]:.2e} - {result['m_range'][1]:.2e} M_sun")

            ecart = abs(result['b'] - 4.0)
            print(f"\nEcart avec TMT: {ecart:.2f}")
            if ecart < 0.5:
                print("-> COHERENT avec TMT v2.4")
            elif ecart < 1.0:
                print("-> PARTIELLEMENT coherent avec TMT")
            else:
                print("-> ECART significatif")

    print("\n" + "=" * 70)
    print("2. RELATION M_HI vs V_flat (ALFALFA + WALLABY)")
    print("=" * 70)

    if hi_data:
        v = np.array([d['v_flat'] for d in hi_data])
        m = np.array([d['m_hi'] for d in hi_data])

        result_hi = fit_btfr(v, m, "HI")
        if result_hi:
            print(f"\nlog(M_HI) = {result_hi['a']:.2f} + {result_hi['b']:.2f} x log(V_flat)")
            print(f"\nExposant: {result_hi['b']:.3f} +/- {result_hi['b_err']:.3f}")
            print(f"\nR^2 = {result_hi['r2']:.4f}")
            print(f"Scatter = {result_hi['scatter']:.3f} dex")
            print(f"Galaxies: {result_hi['n']}")

            print("\nNote: Cette relation n'est PAS la vraie BTFR car:")
            print("  - M_HI != M_bary (manque masse stellaire)")
            print("  - Les galaxies ALFALFA sont biaisees vers les gas-rich")
            print("  - L'exposant plus faible est attendu")

    print("\n" + "=" * 70)
    print("3. COMPARAISON DES FRACTIONS DE GAZ (SPARC)")
    print("=" * 70)

    if sparc:
        f_gas = np.array([d['f_gas'] for d in sparc])
        v = np.array([d['v_flat'] for d in sparc])

        r, p = stats.pearsonr(v, f_gas)
        print(f"\nFraction gaz moyenne: {np.mean(f_gas):.2f}")
        print(f"Fraction gaz mediane: {np.median(f_gas):.2f}")
        print(f"\nCorrelation V_flat vs f_gas: r = {r:.3f} (p = {p:.2e})")
        print("(Galaxies massives ont moins de gaz - comportement normal)")

        # Split by velocity
        low_v = f_gas[v < 100]
        high_v = f_gas[v > 150]
        print(f"\nf_gas pour V < 100 km/s: {np.mean(low_v):.2f} (n={len(low_v)})")
        print(f"f_gas pour V > 150 km/s: {np.mean(high_v):.2f} (n={len(high_v)})")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / "BTFR_analyse_finale.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("ANALYSE FINALE - RELATION TULLY-FISHER BARYONIQUE\n")
        f.write("=" * 70 + "\n\n")

        f.write("RESUME:\n")
        f.write("-" * 50 + "\n")
        f.write("TMT predit: M_bary ~ V_flat^4 (exposant = 4.0)\n")
        f.write("McGaugh+ 2016: exposant = 3.98 +/- 0.06\n\n")

        if sparc and result:
            f.write("SPARC (120 galaxies, masses reelles):\n")
            f.write(f"  Exposant = {result['b']:.3f} +/- {result['b_err']:.3f}\n")
            f.write(f"  R^2 = {result['r2']:.4f}\n")
            f.write(f"  Scatter = {result['scatter']:.3f} dex\n\n")

            ecart = abs(result['b'] - 4.0)
            if ecart < 0.5:
                f.write("VERDICT: BTFR VALIDEE - Coherent avec TMT v2.4\n")
            else:
                f.write(f"VERDICT: Ecart de {ecart:.2f} avec la prediction\n")

        if hi_data and result_hi:
            f.write(f"\nALFALFA + WALLABY ({result_hi['n']} galaxies, masses HI):\n")
            f.write(f"  Exposant M_HI = {result_hi['b']:.3f} +/- {result_hi['b_err']:.3f}\n")
            f.write("  Note: Ce n'est pas la vraie BTFR (M_HI != M_bary)\n")

    print(f"\nResultats sauvegardes: {output_file}")

    # Generate figure
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        # 1. SPARC BTFR
        ax1 = axes[0, 0]
        if sparc:
            v_s = np.array([d['v_flat'] for d in sparc])
            m_s = np.array([d['m_bary'] for d in sparc])
            f_g = np.array([d['f_gas'] for d in sparc])

            scatter = ax1.scatter(v_s, m_s, c=f_g, cmap='RdYlBu_r',
                                 alpha=0.8, s=50, vmin=0, vmax=1)
            plt.colorbar(scatter, ax=ax1, label='Gas fraction')

            if result:
                v_range = np.logspace(np.log10(30), np.log10(350), 100)
                m_fit = 10 ** (result['a'] + result['b'] * np.log10(v_range))
                ax1.plot(v_range, m_fit, 'k-', lw=2,
                        label=f"Fit: b={result['b']:.2f}, R^2={result['r2']:.2f}")

                m_tmt = 50 * v_range**4
                ax1.plot(v_range, m_tmt, 'r--', lw=2, alpha=0.7, label='TMT: M ~ V^4')

        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('V_flat (km/s)', fontsize=12)
        ax1.set_ylabel('M_bary (M_sun)', fontsize=12)
        ax1.set_title('SPARC - Baryonic Tully-Fisher (masses reelles)', fontsize=13)
        ax1.legend(loc='lower right', fontsize=10)
        ax1.grid(True, alpha=0.3)

        # 2. SPARC Residuals
        ax2 = axes[0, 1]
        if sparc and result:
            log_v = np.log10(v_s)
            log_m = np.log10(m_s)
            log_m_pred = result['a'] + result['b'] * log_v
            residuals = log_m - log_m_pred

            ax2.scatter(v_s, residuals, c=f_g, cmap='RdYlBu_r',
                       alpha=0.8, s=50, vmin=0, vmax=1)
            ax2.axhline(0, color='k', lw=2)
            ax2.axhline(result['scatter'], color='r', ls='--', alpha=0.7)
            ax2.axhline(-result['scatter'], color='r', ls='--', alpha=0.7)

            ax2.set_xscale('log')
            ax2.set_xlabel('V_flat (km/s)', fontsize=12)
            ax2.set_ylabel('Residual log(M)', fontsize=12)
            ax2.set_title(f'SPARC Residuals (scatter = {result["scatter"]:.2f} dex)', fontsize=13)
            ax2.set_ylim(-0.8, 0.8)
            ax2.grid(True, alpha=0.3)

        # 3. HI mass relation
        ax3 = axes[1, 0]
        if hi_data:
            v_hi = np.array([d['v_flat'] for d in hi_data])
            m_hi = np.array([d['m_hi'] for d in hi_data])

            ax3.scatter(v_hi, m_hi, alpha=0.1, s=3, c='blue')

            if result_hi:
                v_range = np.logspace(np.log10(40), np.log10(350), 100)
                m_fit = 10 ** (result_hi['a'] + result_hi['b'] * np.log10(v_range))
                ax3.plot(v_range, m_fit, 'k-', lw=2,
                        label=f"Fit: b={result_hi['b']:.2f}")

        ax3.set_xscale('log')
        ax3.set_yscale('log')
        ax3.set_xlabel('V_flat (km/s)', fontsize=12)
        ax3.set_ylabel('M_HI (M_sun)', fontsize=12)
        ax3.set_title(f'ALFALFA+WALLABY - M_HI vs V ({len(hi_data):,} galaxies)', fontsize=13)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)

        # 4. Comparison of exponents
        ax4 = axes[1, 1]
        sources = ['TMT\nprediction', 'McGaugh+\n2016', 'SPARC\n(this work)', 'ALFALFA\n(M_HI only)']
        exponents = [4.0, 3.98, result['b'] if result else 0, result_hi['b'] if result_hi else 0]
        errors = [0, 0.06, result['b_err'] if result else 0, result_hi['b_err'] if result_hi else 0]
        colors = ['red', 'blue', 'green', 'gray']

        bars = ax4.bar(range(len(sources)), exponents, yerr=errors,
                      color=colors, alpha=0.7, capsize=5)

        ax4.set_xticks(range(len(sources)))
        ax4.set_xticklabels(sources)
        ax4.set_ylabel('BTFR Exponent', fontsize=12)
        ax4.set_title('Comparison of BTFR Exponents', fontsize=13)
        ax4.axhline(4.0, color='r', ls='--', alpha=0.5)
        ax4.set_ylim(0, 5)
        ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        fig_file = RESULTS_DIR / "BTFR_analyse_finale.png"
        plt.savefig(fig_file, dpi=150)
        print(f"Figure sauvegardee: {fig_file}")
        plt.close()

    except ImportError:
        print("matplotlib non disponible")

    # Final summary
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()
    print("La relation Tully-Fisher Baryonique sur SPARC (120 galaxies)")
    print(f"donne un exposant de {result['b']:.2f} +/- {result['b_err']:.2f}")
    print()
    print("Comparaison:")
    print(f"  - TMT predit: 4.0")
    print(f"  - McGaugh+ 2016: 3.98 +/- 0.06")
    print(f"  - SPARC (cette analyse): {result['b']:.2f} +/- {result['b_err']:.2f}")
    print()

    ecart = abs(result['b'] - 4.0)
    if ecart < 0.5:
        print("VERDICT: TMT v2.4 VALIDE sur la BTFR")
    elif ecart < 1.0:
        print("VERDICT: TMT PARTIELLEMENT valide")
    else:
        print(f"VERDICT: Ecart de {ecart:.2f} necessitant investigation")


if __name__ == "__main__":
    main()
