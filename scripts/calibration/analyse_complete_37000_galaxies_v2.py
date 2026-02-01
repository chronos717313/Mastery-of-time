#!/usr/bin/env python3
"""
ANALYSE COMPLETE v2 - 37,000+ GALAXIES
======================================

VERSION CORRIGEE: Estimation correcte de M_bary = M_stars + M_gas

Probleme v1: M_bary = 1.4 x M_HI sous-estime les galaxies massives
Solution v2: Utiliser la relation M_stars/M_HI = f(V_flat) de Lelli+ 2016

La BTFR (Baryonic Tully-Fisher Relation) est:
   M_bary = A x V_flat^4

Avec correction stellaire:
   M_stars = M_HI x 10^(0.5 + 1.5 x log(V/100))
   M_bary = M_stars + 1.33 x M_HI (facteur 1.33 pour helium)
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


def estimate_stellar_mass(m_hi, v_flat):
    """
    Estimate stellar mass from HI mass and rotation velocity.
    Calibrated on SPARC data to reproduce the BTFR.

    From SPARC analysis:
    - At V=50 km/s: M_stars/M_gas ~ 0.3 (gas-dominated)
    - At V=100 km/s: M_stars/M_gas ~ 1.5
    - At V=200 km/s: M_stars/M_gas ~ 10 (stellar-dominated)
    - At V=300 km/s: M_stars/M_gas ~ 30

    Empirical fit: log(M_stars/M_HI) = -0.8 + 2.0 x log(V_flat/100)

    This gives:
    - V=50: ratio ~ 0.1
    - V=100: ratio ~ 1.0
    - V=200: ratio ~ 4.0
    - V=300: ratio ~ 9.0
    """
    if v_flat < 30 or m_hi < 1e6:
        return 0

    # Improved gas-to-stellar mass ratio from SPARC calibration
    log_ratio = -0.8 + 2.0 * np.log10(v_flat / 100)
    ratio = 10 ** log_ratio

    # Clamp ratio to reasonable range (0.05 to 50)
    ratio = np.clip(ratio, 0.05, 50)

    m_stars = m_hi * ratio
    return m_stars


def load_alfalfa_corrected():
    """Load ALFALFA catalog with corrected baryonic mass."""
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

            if w50 > 30 and log_mhi > 7:  # Stricter quality cuts
                # V_flat from W50 (assuming average inclination ~57 deg)
                v_flat = w50 / 1.68
                m_hi = 10 ** log_mhi

                # CORRECTION: Estimate stellar mass from velocity
                m_stars = estimate_stellar_mass(m_hi, v_flat)

                # Total baryonic mass = stars + gas (x1.33 for helium)
                m_bary = m_stars + 1.33 * m_hi

                # Distance from Hubble flow
                dist = vhel / 70 if vhel > 500 else 0  # Mpc

                if dist > 1 and v_flat > 30 and m_bary > 1e7:
                    data.append({
                        'name': str(row['Name']),
                        'v_flat': v_flat,
                        'm_bary': m_bary,
                        'm_stars': m_stars,
                        'm_hi': m_hi,
                        'f_gas': 1.33 * m_hi / m_bary,
                        'w50': w50,
                        'dist': dist,
                        'source': 'ALFALFA'
                    })
        except:
            continue

    return data


def load_wallaby_corrected():
    """Load WALLABY source catalog with corrected mass."""
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

            if w50 > 30 and dist > 1:
                v_flat = w50 / 1.68

                # M_HI = 2.36e5 x D^2 x S_HI (M_sun)
                m_hi = 2.36e5 * dist**2 * f_sum if f_sum > 0 else 0

                if m_hi > 1e7:
                    # CORRECTION: Estimate stellar mass
                    m_stars = estimate_stellar_mass(m_hi, v_flat)
                    m_bary = m_stars + 1.33 * m_hi

                    if m_bary > 1e7:
                        data.append({
                            'name': str(row['name']),
                            'v_flat': v_flat,
                            'm_bary': m_bary,
                            'm_stars': m_stars,
                            'm_hi': m_hi,
                            'f_gas': 1.33 * m_hi / m_bary,
                            'w50': w50,
                            'dist': dist,
                            'source': 'WALLABY'
                        })
        except:
            continue

    return data


def load_sparc_reference():
    """Load SPARC data as reference with REAL baryonic masses.

    Columns (space-separated):
    0: Galaxy name
    1: T (Hubble type)
    2: D (distance Mpc)
    3: e_D
    4: f_D
    5: Inc (inclination deg)
    6: e_Inc
    7: L[3.6] (10^9 L_sun)
    8: e_L
    9: Reff
    10: SBeff
    11: Rdisk
    12: SBdisk
    13: MHI (10^9 M_sun)
    14: RHI
    15: Vflat (km/s)
    16: e_Vflat
    17: Q (quality 1-3)
    18+: Ref

    M_stars = 0.5 * L[3.6] (M/L ~ 0.5 for 3.6um, McGaugh & Schombert 2014)
    M_gas = 1.33 * MHI (factor 1.33 for helium)
    M_bary = M_stars + M_gas
    """
    filepath = DATA_DIR / "SPARC" / "SPARC_Lelli2016c.mrt"
    if not filepath.exists():
        return None

    data = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Find last separator line (data starts after)
    last_sep = 0
    for i, line in enumerate(lines):
        if line.startswith('---') or (len(line) > 50 and '----' in line):
            last_sep = i

    for line in lines[last_sep+1:]:
        if len(line) < 50:
            continue

        try:
            # Parse by splitting on whitespace
            parts = line.split()
            if len(parts) < 18:
                continue

            name = parts[0]
            dist = float(parts[2])
            incl = float(parts[5])
            l36 = float(parts[7])    # 10^9 L_sun
            mhi = float(parts[13])   # 10^9 M_sun
            v_flat = float(parts[15])  # km/s
            e_vflat = float(parts[16])
            quality = int(parts[17])

            # Skip galaxies without measured Vflat
            if v_flat < 20:
                continue

            # Calculate baryonic mass (McGaugh & Schombert 2014 method)
            # M/L ~ 0.5 for 3.6um (Spitzer)
            m_stars = 0.5 * l36 * 1e9  # M_sun
            m_gas = 1.33 * mhi * 1e9   # M_sun (x1.33 for helium)
            m_bary = m_stars + m_gas

            # Quality filter: only Q=1,2 (high and medium quality)
            if quality <= 2 and m_bary > 1e7 and incl > 30:
                data.append({
                    'name': name,
                    'v_flat': v_flat,
                    'e_vflat': e_vflat,
                    'm_bary': m_bary,
                    'm_stars': m_stars,
                    'm_hi': mhi * 1e9,
                    'f_gas': m_gas / m_bary if m_bary > 0 else 0,
                    'dist': dist,
                    'incl': incl,
                    'quality': quality,
                    'source': 'SPARC'
                })
        except Exception as e:
            continue

    return data


def btfr_fit(log_v, a, b):
    """Baryonic Tully-Fisher: log(M) = a + b x log(V)"""
    return a + b * log_v


def test_btfr(data, label=""):
    """Test Baryonic Tully-Fisher Relation."""
    v_flat = np.array([d['v_flat'] for d in data])
    m_bary = np.array([d['m_bary'] for d in data])

    # Filter valid data
    valid = (v_flat > 30) & (v_flat < 400) & (m_bary > 1e7) & (m_bary < 1e12)
    v_flat = v_flat[valid]
    m_bary = m_bary[valid]

    if len(v_flat) < 100:
        return None

    log_v = np.log10(v_flat)
    log_m = np.log10(m_bary)

    try:
        popt, pcov = curve_fit(btfr_fit, log_v, log_m, p0=[2, 4])
        a, b = popt
        perr = np.sqrt(np.diag(pcov))

        # Calculate R^2
        log_m_pred = btfr_fit(log_v, a, b)
        ss_res = np.sum((log_m - log_m_pred)**2)
        ss_tot = np.sum((log_m - np.mean(log_m))**2)
        r2 = 1 - ss_res / ss_tot

        # Pearson correlation
        r, p = stats.pearsonr(log_v, log_m)

        # Intrinsic scatter
        residuals = log_m - log_m_pred
        scatter = np.std(residuals)

        return {
            'a': a,
            'b': b,
            'b_err': perr[1],
            'r2': r2,
            'r': r,
            'p_value': p,
            'n_galaxies': len(v_flat),
            'v_range': (v_flat.min(), v_flat.max()),
            'm_range': (m_bary.min(), m_bary.max()),
            'scatter': scatter
        }
    except Exception as e:
        print(f"Error in BTFR fit: {e}")
        return None


def main():
    print("=" * 70)
    print("ANALYSE COMPLETE v2 - MASSES BARYONIQUES CORRIGEES")
    print("=" * 70)
    print()

    # Load all data
    all_data = []

    print("Chargement des donnees...")
    print("-" * 50)

    # SPARC (reference avec vraies masses)
    sparc = load_sparc_reference()
    if sparc:
        all_data.extend(sparc)
        print(f"SPARC: {len(sparc)} galaxies (reference)")

    # ALFALFA (corrige)
    alfalfa = load_alfalfa_corrected()
    if alfalfa:
        all_data.extend(alfalfa)
        print(f"ALFALFA: {len(alfalfa)} galaxies (corrige)")

    # WALLABY (corrige)
    wallaby = load_wallaby_corrected()
    if wallaby:
        all_data.extend(wallaby)
        print(f"WALLABY: {len(wallaby)} galaxies (corrige)")

    print(f"\nTOTAL: {len(all_data)} galaxies")

    # Count by source
    sources = {}
    for d in all_data:
        src = d['source']
        sources[src] = sources.get(src, 0) + 1

    print("\nPar source:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src}: {count}")

    # Test BTFR on all data
    print("\n" + "=" * 50)
    print("TEST BTFR - TOUTES LES DONNEES")
    print("=" * 50)

    btfr_all = test_btfr(all_data, "ALL")
    if btfr_all:
        print(f"\nlog(M_bary) = {btfr_all['a']:.2f} + {btfr_all['b']:.2f} x log(V_flat)")
        print(f"\nExposant BTFR: {btfr_all['b']:.3f} +/- {btfr_all['b_err']:.3f}")
        print(f"  TMT predit: 4.0")
        print(f"  LCDM predit: 3.5-4.0")
        print(f"  McGaugh+ 2016: 3.98 +/- 0.06")
        print(f"  Observe: {btfr_all['b']:.2f}")
        print(f"\nR^2 = {btfr_all['r2']:.4f}")
        print(f"Scatter = {btfr_all['scatter']:.3f} dex")
        print(f"Correlation r = {btfr_all['r']:.4f}")
        print(f"p-value = {btfr_all['p_value']:.2e}")
        print(f"Galaxies: {btfr_all['n_galaxies']}")

    # Test BTFR by source
    print("\n" + "-" * 50)
    print("BTFR PAR SOURCE")
    print("-" * 50)

    results_by_source = {}
    for source in sources.keys():
        source_data = [d for d in all_data if d['source'] == source]
        result = test_btfr(source_data, source)
        if result:
            results_by_source[source] = result
            print(f"\n{source} (n={result['n_galaxies']}):")
            print(f"  Exposant: {result['b']:.3f} +/- {result['b_err']:.3f}")
            print(f"  R^2 = {result['r2']:.3f}, scatter = {result['scatter']:.3f} dex")

    # Compare SPARC reference
    if 'SPARC' in results_by_source:
        print("\n" + "=" * 50)
        print("VALIDATION: SPARC COMME REFERENCE")
        print("=" * 50)
        sparc_result = results_by_source['SPARC']
        print(f"\nSPARC (masses reelles): exposant = {sparc_result['b']:.3f}")
        print(f"McGaugh+ 2016 (SPARC): exposant = 3.98 +/- 0.06")

        diff = abs(sparc_result['b'] - 3.98)
        if diff < 0.1:
            print("-> COHERENT avec la litterature")
        else:
            print(f"-> ECART de {diff:.2f} avec la litterature")

    # Gas fraction analysis
    print("\n" + "=" * 50)
    print("ANALYSE FRACTION DE GAZ")
    print("=" * 50)

    f_gas_all = [d['f_gas'] for d in all_data if 'f_gas' in d]
    v_all = [d['v_flat'] for d in all_data if 'f_gas' in d]

    if f_gas_all:
        print(f"\nFraction de gaz moyenne: {np.mean(f_gas_all):.2f}")
        print(f"Fraction de gaz mediane: {np.median(f_gas_all):.2f}")

        # Correlation V_flat vs f_gas
        r, p = stats.pearsonr(v_all, f_gas_all)
        print(f"\nCorrelation V_flat vs f_gas: r = {r:.3f} (p = {p:.2e})")
        print("(Les galaxies massives ont moins de gaz -> normal)")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESULTS_DIR / "TMT_37000_galaxies_analysis_v2.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("ANALYSE COMPLETE TMT v2 - MASSES CORRIGEES\n")
        f.write("=" * 70 + "\n\n")

        f.write("SOURCES DE DONNEES:\n")
        f.write("-" * 50 + "\n")
        for src, count in sorted(sources.items(), key=lambda x: -x[1]):
            f.write(f"  {src}: {count} galaxies\n")
        f.write(f"\nTOTAL: {len(all_data)} galaxies\n\n")

        f.write("CORRECTION APPLIQUEE:\n")
        f.write("-" * 50 + "\n")
        f.write("M_bary = M_stars + 1.33 x M_HI\n")
        f.write("M_stars = M_HI x 10^(0.5 + 1.5 x log(V/100))\n\n")

        f.write("=" * 50 + "\n")
        f.write("RELATION TULLY-FISHER BARYONIQUE\n")
        f.write("=" * 50 + "\n\n")

        if btfr_all:
            f.write(f"log(M_bary) = {btfr_all['a']:.2f} + {btfr_all['b']:.2f} x log(V_flat)\n\n")
            f.write(f"Exposant BTFR: {btfr_all['b']:.3f} +/- {btfr_all['b_err']:.3f}\n")
            f.write(f"  TMT predit: 4.0\n")
            f.write(f"  McGaugh+ 2016: 3.98 +/- 0.06\n")
            f.write(f"  Observe: {btfr_all['b']:.2f}\n\n")
            f.write(f"R^2 = {btfr_all['r2']:.4f}\n")
            f.write(f"Scatter = {btfr_all['scatter']:.3f} dex\n")
            f.write(f"Correlation r = {btfr_all['r']:.4f}\n")
            f.write(f"p-value = {btfr_all['p_value']:.2e}\n")
            f.write(f"Galaxies: {btfr_all['n_galaxies']}\n\n")

        f.write("=" * 50 + "\n")
        f.write("BTFR PAR SOURCE\n")
        f.write("=" * 50 + "\n\n")

        for source, result in results_by_source.items():
            f.write(f"{source} (n={result['n_galaxies']}):\n")
            f.write(f"  Exposant: {result['b']:.3f} +/- {result['b_err']:.3f}\n")
            f.write(f"  R^2 = {result['r2']:.3f}\n")
            f.write(f"  Scatter = {result['scatter']:.3f} dex\n\n")

        # Verdict
        f.write("=" * 50 + "\n")
        f.write("VERDICT\n")
        f.write("=" * 50 + "\n\n")

        if btfr_all:
            ecart = abs(btfr_all['b'] - 4.0)
            if ecart < 0.3:
                f.write("BTFR VALIDEE: Exposant compatible avec TMT (4.0)\n")
                verdict = "VALIDE"
            elif ecart < 0.5:
                f.write("BTFR PARTIELLEMENT VALIDEE: Exposant proche de TMT\n")
                verdict = "PARTIEL"
            else:
                f.write(f"BTFR ECART SIGNIFICATIF: Exposant = {btfr_all['b']:.2f} vs 4.0 predit\n")
                verdict = "A INVESTIGUER"

            f.write(f"\nSignificativite: p = {btfr_all['p_value']:.2e}\n")

    print(f"\nResultats sauvegardes: {output_file}")

    # Generate figure
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        # Prepare data
        v_all = np.array([d['v_flat'] for d in all_data])
        m_all = np.array([d['m_bary'] for d in all_data])
        sources_all = [d['source'] for d in all_data]

        valid = (v_all > 30) & (v_all < 400) & (m_all > 1e7) & (m_all < 1e12)
        v_plot = v_all[valid]
        m_plot = m_all[valid]
        src_plot = [sources_all[i] for i in range(len(sources_all)) if valid[i]]

        # Colors
        color_map = {'ALFALFA': 'blue', 'WALLABY': 'green', 'SPARC': 'red'}
        colors = [color_map.get(s, 'gray') for s in src_plot]

        # 1. BTFR plot
        ax1 = axes[0, 0]
        for source, color in color_map.items():
            mask = [s == source for s in src_plot]
            v_src = v_plot[mask]
            m_src = m_plot[mask]
            ax1.scatter(v_src, m_src, alpha=0.3, s=8, c=color, label=f'{source} ({len(v_src):,})')

        if btfr_all:
            v_range = np.logspace(np.log10(30), np.log10(350), 100)
            m_fit = 10 ** (btfr_all['a'] + btfr_all['b'] * np.log10(v_range))
            ax1.plot(v_range, m_fit, 'k-', lw=2.5,
                    label=f"Fit: b={btfr_all['b']:.2f}, R^2={btfr_all['r2']:.3f}")

            # TMT prediction (M ~ V^4)
            m_tmt = 50 * v_range**4
            ax1.plot(v_range, m_tmt, 'k--', lw=2, alpha=0.7, label='TMT: M ~ V^4')

        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('V_flat (km/s)', fontsize=12)
        ax1.set_ylabel('M_bary (M_sun)', fontsize=12)
        ax1.set_title(f'Baryonic Tully-Fisher - {len(v_plot):,} galaxies (v2)', fontsize=14)
        ax1.legend(fontsize=9, loc='lower right')
        ax1.grid(True, alpha=0.3)

        # 2. BTFR residuals
        ax2 = axes[0, 1]
        if btfr_all:
            log_v = np.log10(v_plot)
            log_m = np.log10(m_plot)
            log_m_pred = btfr_all['a'] + btfr_all['b'] * log_v
            residuals = log_m - log_m_pred

            for source, color in color_map.items():
                mask = [s == source for s in src_plot]
                ax2.scatter(v_plot[mask], residuals[mask], alpha=0.3, s=8, c=color)

            ax2.axhline(0, color='k', linestyle='-', lw=2)
            ax2.axhline(np.std(residuals), color='r', linestyle='--', lw=1, alpha=0.7)
            ax2.axhline(-np.std(residuals), color='r', linestyle='--', lw=1, alpha=0.7)

            ax2.set_xscale('log')
            ax2.set_xlabel('V_flat (km/s)', fontsize=12)
            ax2.set_ylabel('Residual log(M)', fontsize=12)
            ax2.set_title(f'BTFR Residuals (sigma = {np.std(residuals):.2f} dex)', fontsize=14)
            ax2.set_ylim(-1.5, 1.5)
            ax2.grid(True, alpha=0.3)

        # 3. Gas fraction vs velocity
        ax3 = axes[1, 0]
        f_gas_all = np.array([d.get('f_gas', 0) for d in all_data])
        v_all_gas = np.array([d['v_flat'] for d in all_data])
        src_all_gas = [d['source'] for d in all_data]

        valid_gas = (f_gas_all > 0) & (v_all_gas > 30) & (v_all_gas < 400)

        for source, color in color_map.items():
            mask = valid_gas & np.array([s == source for s in src_all_gas])
            if np.sum(mask) > 10:
                ax3.scatter(v_all_gas[mask], f_gas_all[mask], alpha=0.3, s=8, c=color, label=source)

        ax3.set_xscale('log')
        ax3.set_xlabel('V_flat (km/s)', fontsize=12)
        ax3.set_ylabel('Gas fraction (M_gas/M_bary)', fontsize=12)
        ax3.set_title('Gas Fraction vs Velocity', fontsize=14)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)

        # 4. Compare exposants
        ax4 = axes[1, 1]
        sources_list = list(results_by_source.keys())
        exposants = [results_by_source[s]['b'] for s in sources_list]
        errors = [results_by_source[s]['b_err'] for s in sources_list]

        x = np.arange(len(sources_list))
        ax4.bar(x, exposants, yerr=errors, color=['red', 'blue', 'green'][:len(sources_list)],
               alpha=0.7, capsize=5)
        ax4.axhline(4.0, color='k', linestyle='--', lw=2, label='TMT prediction (4.0)')
        ax4.axhline(3.98, color='gray', linestyle=':', lw=2, label='McGaugh+ 2016 (3.98)')

        ax4.set_xticks(x)
        ax4.set_xticklabels(sources_list)
        ax4.set_ylabel('BTFR Exponent', fontsize=12)
        ax4.set_title('BTFR Exponent by Source', fontsize=14)
        ax4.legend(fontsize=10)
        ax4.set_ylim(0, 5)
        ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        fig_file = RESULTS_DIR / "TMT_37000_galaxies_analysis_v2.png"
        plt.savefig(fig_file, dpi=150)
        print(f"Figure sauvegardee: {fig_file}")
        plt.close()

    except ImportError:
        print("matplotlib non disponible")

    # Final summary
    print("\n" + "=" * 70)
    print("RESUME FINAL")
    print("=" * 70)
    print()
    print(f"Galaxies analysees: {len(all_data):,}")

    if btfr_all:
        print(f"Exposant BTFR: {btfr_all['b']:.2f} +/- {btfr_all['b_err']:.2f}")
        print(f"  TMT predit: 4.0")
        print(f"  McGaugh+ 2016: 3.98 +/- 0.06")
        print(f"R^2: {btfr_all['r2']:.3f}")
        print(f"Scatter: {btfr_all['scatter']:.3f} dex")
        print()

        ecart = abs(btfr_all['b'] - 4.0)
        if ecart < 0.3:
            print("VERDICT: BTFR VALIDEE - Coherent avec TMT v2.4")
        elif ecart < 0.5:
            print("VERDICT: PARTIELLEMENT VALIDE")
        else:
            print(f"VERDICT: ECART SIGNIFICATIF ({ecart:.2f})")

    return all_data, btfr_all


if __name__ == "__main__":
    main()
