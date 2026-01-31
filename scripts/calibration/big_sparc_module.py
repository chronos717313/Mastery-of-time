#!/usr/bin/env python3
"""
BIG-SPARC Module: Unified Infrastructure for Large-Scale TMT Calibration
=========================================================================

This module provides a unified interface for loading, processing, and
calibrating TMT parameters on large galaxy samples from multiple surveys:

Supported Surveys:
- SPARC (175 galaxies) - Original calibration dataset
- WALLABY DR2 (~1,800 galaxies) - ASKAP HI survey
- APERTIF DR1 (~1,740 galaxies) - WSRT HI survey
- BIG-SPARC (~4,000 galaxies) - Future unified database

Reference: TMT v2.4 Validation (January 2026)
BIG-SPARC: Haubner, Lelli et al. (2024), arXiv:2411.13329

Usage:
    from big_sparc_module import BigSPARCCalibrator

    calibrator = BigSPARCCalibrator()
    calibrator.load_all_surveys()
    results = calibrator.calibrate_k_M()
    calibrator.save_results()
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize, curve_fit
from scipy import stats
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

# Constants
G_KPC = 4.302e-6  # kpc (km/s)^2 / M_sun
C_KMS = 299792.458  # km/s

# Project directories
PROJECT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"


@dataclass
class RotationCurve:
    """Standardized rotation curve data structure."""
    name: str
    source: str
    distance: float  # Mpc
    R: np.ndarray  # kpc
    Vobs: np.ndarray  # km/s
    e_Vobs: np.ndarray  # km/s
    Vgas: np.ndarray  # km/s
    Vdisk: np.ndarray  # km/s
    Vbul: np.ndarray  # km/s
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class GalaxyResult:
    """Results from analyzing a single galaxy."""
    name: str
    source: str
    M_bary: float
    n_points: int
    chi2_newton: float
    k_opt: float
    chi2_k: float
    r_c_mass: float
    improvement_k: float
    k_free: float
    r_c_free: float
    chi2_free: float
    baryonic_valid: bool
    metadata: Dict = None


@dataclass
class CalibrationResult:
    """Results from k(M) or r_c(M) calibration."""
    parameter: str  # 'k' or 'r_c'
    a: float  # Coefficient
    b: float  # Exponent
    R2: float
    p_value: float
    n_galaxies: int
    mass_range: Tuple[float, float]
    formula: str
    comparison_sparc: str


class SurveyLoader(ABC):
    """Abstract base class for survey data loaders."""

    @abstractmethod
    def load(self, filepath: Path) -> List[RotationCurve]:
        """Load rotation curves from survey data file."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Survey name."""
        pass


class SPARCLoader(SurveyLoader):
    """Loader for original SPARC format (MRT files)."""

    @property
    def name(self) -> str:
        return "SPARC"

    def load(self, filepath: Path) -> List[RotationCurve]:
        """Load SPARC MassModels file."""
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

                    D = float(line[12:18].strip())
                    R = float(line[19:25].strip())
                    Vobs = float(line[26:32].strip())
                    e_Vobs = float(line[33:38].strip())
                    Vgas = float(line[39:45].strip())
                    Vdisk = float(line[46:52].strip())
                    Vbul = float(line[53:59].strip())

                    if name not in rotation_curves:
                        rotation_curves[name] = {
                            'R': [], 'Vobs': [], 'e_Vobs': [],
                            'Vgas': [], 'Vdisk': [], 'Vbul': [],
                            'distance': D
                        }

                    rotation_curves[name]['R'].append(R)
                    rotation_curves[name]['Vobs'].append(Vobs)
                    rotation_curves[name]['e_Vobs'].append(max(e_Vobs, 1.0))
                    rotation_curves[name]['Vgas'].append(Vgas)
                    rotation_curves[name]['Vdisk'].append(Vdisk)
                    rotation_curves[name]['Vbul'].append(Vbul)

                except (ValueError, IndexError):
                    continue

        # Convert to RotationCurve objects
        result = []
        for name, data in rotation_curves.items():
            rc = RotationCurve(
                name=name,
                source=self.name,
                distance=data['distance'],
                R=np.array(data['R']),
                Vobs=np.array(data['Vobs']),
                e_Vobs=np.array(data['e_Vobs']),
                Vgas=np.array(data['Vgas']),
                Vdisk=np.array(data['Vdisk']),
                Vbul=np.array(data['Vbul'])
            )
            result.append(rc)

        return result


class GenericTxtLoader(SurveyLoader):
    """Loader for generic SPARC-compatible text format."""

    def __init__(self, survey_name: str):
        self._name = survey_name

    @property
    def name(self) -> str:
        return self._name

    def load(self, filepath: Path) -> List[RotationCurve]:
        """Load rotation curves from text file."""
        rotation_curves = {}

        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue

                parts = line.split()
                if len(parts) < 8:
                    continue

                try:
                    name = parts[0]
                    D = float(parts[1])
                    R = float(parts[2])
                    Vobs = float(parts[3])
                    e_Vobs = float(parts[4])
                    Vgas = float(parts[5])
                    Vdisk = float(parts[6])
                    Vbul = float(parts[7])

                    if name not in rotation_curves:
                        rotation_curves[name] = {
                            'R': [], 'Vobs': [], 'e_Vobs': [],
                            'Vgas': [], 'Vdisk': [], 'Vbul': [],
                            'distance': D
                        }

                    rotation_curves[name]['R'].append(R)
                    rotation_curves[name]['Vobs'].append(Vobs)
                    rotation_curves[name]['e_Vobs'].append(max(e_Vobs, 1.0))
                    rotation_curves[name]['Vgas'].append(Vgas)
                    rotation_curves[name]['Vdisk'].append(Vdisk)
                    rotation_curves[name]['Vbul'].append(Vbul)

                except (ValueError, IndexError):
                    continue

        result = []
        for name, data in rotation_curves.items():
            rc = RotationCurve(
                name=name,
                source=self._name,
                distance=data['distance'],
                R=np.array(data['R']),
                Vobs=np.array(data['Vobs']),
                e_Vobs=np.array(data['e_Vobs']),
                Vgas=np.array(data['Vgas']),
                Vdisk=np.array(data['Vdisk']),
                Vbul=np.array(data['Vbul'])
            )
            result.append(rc)

        return result


class TMTModel:
    """TMT v2.4 model for rotation curve fitting."""

    @staticmethod
    def r_c_from_mass(M_bary: float) -> float:
        """TMT v2.4: r_c(M) = 2.6 x (M/10^10)^0.56 kpc"""
        return 2.6 * (M_bary / 1e10) ** 0.56

    @staticmethod
    def compute_V_bary(Vgas: np.ndarray, Vdisk: np.ndarray, Vbul: np.ndarray,
                       ML_disk: float = 0.5, ML_bul: float = 0.7) -> np.ndarray:
        """Compute baryonic velocity."""
        V_bary_sq = Vgas**2 + ML_disk * Vdisk**2 + ML_bul * Vbul**2
        return np.sqrt(np.maximum(V_bary_sq, 0))

    @staticmethod
    def compute_M_bary_enclosed(R: np.ndarray, Vgas: np.ndarray,
                                 Vdisk: np.ndarray, Vbul: np.ndarray,
                                 ML_disk: float = 0.5, ML_bul: float = 0.7) -> np.ndarray:
        """Compute enclosed baryonic mass."""
        V_bary = TMTModel.compute_V_bary(Vgas, Vdisk, Vbul, ML_disk, ML_bul)
        return V_bary**2 * R / G_KPC

    @staticmethod
    def V_TMT(R: np.ndarray, M_bary_enc: np.ndarray, k: float, r_c: float) -> np.ndarray:
        """TMT velocity model: M_eff = M_bary x [1 + k x (R/r_c)]"""
        multiplier = 1.0 + k * (R / r_c)
        M_eff = M_bary_enc * multiplier
        return np.sqrt(np.maximum(G_KPC * M_eff / R, 0))

    @staticmethod
    def chi2_reduced(V_model: np.ndarray, V_obs: np.ndarray,
                     e_V: np.ndarray, n_params: int = 1) -> float:
        """Reduced chi-squared."""
        residuals = (V_model - V_obs) / e_V
        chi2 = np.sum(residuals**2)
        dof = len(V_obs) - n_params
        return chi2 / max(dof, 1)


class BigSPARCCalibrator:
    """
    Main calibrator class for BIG-SPARC unified analysis.

    This class handles:
    - Loading data from multiple surveys
    - Analyzing rotation curves with TMT v2.4
    - Calibrating k(M) and r_c(M) relations
    - Generating reports and figures
    """

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or DATA_DIR
        self.rotation_curves: List[RotationCurve] = []
        self.results: List[GalaxyResult] = []
        self.k_calibration: CalibrationResult = None
        self.rc_calibration: CalibrationResult = None

        # Survey loaders
        self.loaders = {
            'SPARC': SPARCLoader(),
            'WALLABY': GenericTxtLoader('WALLABY'),
            'APERTIF': GenericTxtLoader('APERTIF'),
            'BIG-SPARC': GenericTxtLoader('BIG-SPARC')
        }

    def load_survey(self, survey: str, filepath: Path = None) -> int:
        """Load a single survey."""
        if filepath is None:
            # Auto-detect filepath
            survey_dirs = {
                'SPARC': self.data_dir / 'SPARC',
                'WALLABY': self.data_dir / 'WALLABY_DR2',
                'APERTIF': self.data_dir / 'APERTIF_DR1',
                'BIG-SPARC': self.data_dir / 'BIG_SPARC'
            }

            search_dir = survey_dirs.get(survey, self.data_dir)

            # Find rotation curve file
            patterns = ['*rotation_curves*.txt', '*MassModels*.mrt', '*.txt']
            for pattern in patterns:
                files = list(search_dir.glob(pattern))
                if files:
                    filepath = files[0]
                    break

        if filepath is None or not filepath.exists():
            print(f"No data file found for {survey}")
            return 0

        loader = self.loaders.get(survey, GenericTxtLoader(survey))
        new_curves = loader.load(filepath)

        self.rotation_curves.extend(new_curves)
        return len(new_curves)

    def load_all_surveys(self) -> Dict[str, int]:
        """Load all available surveys."""
        counts = {}

        for survey in ['SPARC', 'WALLABY', 'APERTIF', 'BIG-SPARC']:
            count = self.load_survey(survey)
            if count > 0:
                counts[survey] = count
                print(f"Loaded {survey}: {count} galaxies")

        print(f"\nTotal: {len(self.rotation_curves)} galaxies")
        return counts

    def analyze_galaxy(self, rc: RotationCurve) -> Optional[GalaxyResult]:
        """Analyze a single galaxy with TMT v2.4."""
        if len(rc.R) < 5:
            return None

        model = TMTModel()

        V_bary = model.compute_V_bary(rc.Vgas, rc.Vdisk, rc.Vbul)
        M_bary_enc = model.compute_M_bary_enclosed(rc.R, rc.Vgas, rc.Vdisk, rc.Vbul)

        M_bary_total = M_bary_enc[-1] if len(M_bary_enc) > 0 else 0

        if M_bary_total < 1e6:
            return None

        # Chi2 Newton
        chi2_newton = model.chi2_reduced(V_bary, rc.Vobs, rc.e_Vobs, n_params=0)

        # TMT with mass-dependent r_c
        r_c_mass = model.r_c_from_mass(M_bary_total)

        # Optimize k
        def objective_k(k):
            if k < 0:
                return 1e10
            V_model = model.V_TMT(rc.R, M_bary_enc, k, r_c_mass)
            return model.chi2_reduced(V_model, rc.Vobs, rc.e_Vobs)

        result_k = minimize_scalar(objective_k, bounds=(0.001, 100), method='bounded')
        k_opt, chi2_k = result_k.x, result_k.fun

        # Optimize both k and r_c
        def objective_both(params):
            k, r_c = params
            if k <= 0 or r_c <= 0:
                return 1e10
            V_model = model.V_TMT(rc.R, M_bary_enc, k, r_c)
            return model.chi2_reduced(V_model, rc.Vobs, rc.e_Vobs, n_params=2)

        best_chi2 = np.inf
        best_params = (1.0, 5.0)

        for k_init in [0.5, 1, 2, 5]:
            for rc_init in [1, 3, 5, 10]:
                try:
                    result = minimize(objective_both, [k_init, rc_init],
                                    bounds=[(0.01, 100), (0.1, 100)],
                                    method='L-BFGS-B')
                    if result.fun < best_chi2:
                        best_chi2 = result.fun
                        best_params = result.x
                except:
                    continue

        k_free, r_c_free = best_params
        chi2_free = best_chi2

        improvement_k = (chi2_newton - chi2_k) / chi2_newton * 100 if chi2_newton > 0 else 0
        baryonic_valid = chi2_newton / chi2_k < 1.1 if chi2_k > 0 else False

        return GalaxyResult(
            name=rc.name,
            source=rc.source,
            M_bary=M_bary_total,
            n_points=len(rc.R),
            chi2_newton=chi2_newton,
            k_opt=k_opt,
            chi2_k=chi2_k,
            r_c_mass=r_c_mass,
            improvement_k=improvement_k,
            k_free=k_free,
            r_c_free=r_c_free,
            chi2_free=chi2_free,
            baryonic_valid=baryonic_valid
        )

    def analyze_all(self, verbose: bool = True) -> List[GalaxyResult]:
        """Analyze all loaded galaxies."""
        self.results = []

        for i, rc in enumerate(self.rotation_curves):
            result = self.analyze_galaxy(rc)
            if result is not None:
                self.results.append(result)

            if verbose and (i + 1) % 200 == 0:
                print(f"  Processed {i + 1}/{len(self.rotation_curves)} galaxies...")

        if verbose:
            print(f"\nValid galaxies: {len(self.results)}")

        return self.results

    def calibrate_k_M(self) -> CalibrationResult:
        """Calibrate k(M) relation."""
        valid = [r for r in self.results
                 if r.M_bary > 1e7
                 and 0.01 < r.k_opt < 100
                 and not r.baryonic_valid]

        if len(valid) < 20:
            return None

        M_array = np.array([r.M_bary for r in valid])
        k_array = np.array([r.k_opt for r in valid])

        log_M = np.log10(M_array / 1e10)
        log_k = np.log10(k_array)
        mask = np.isfinite(log_M) & np.isfinite(log_k)

        slope, intercept, r_value, p_value, _ = stats.linregress(log_M[mask], log_k[mask])

        a = 10 ** intercept
        b = slope
        R2 = r_value ** 2

        self.k_calibration = CalibrationResult(
            parameter='k',
            a=a,
            b=b,
            R2=R2,
            p_value=p_value,
            n_galaxies=np.sum(mask),
            mass_range=(M_array.min(), M_array.max()),
            formula=f"k = {a:.3f} x (M/10^10)^{b:.3f}",
            comparison_sparc="SPARC: k = 4.00 x (M/10^10)^(-0.49), R^2 = 0.64"
        )

        return self.k_calibration

    def calibrate_r_c_M(self) -> CalibrationResult:
        """Calibrate r_c(M) relation."""
        valid = [r for r in self.results
                 if r.M_bary > 1e7
                 and 0.1 < r.r_c_free < 100]

        if len(valid) < 20:
            return None

        M_array = np.array([r.M_bary for r in valid])
        rc_array = np.array([r.r_c_free for r in valid])

        log_M = np.log10(M_array / 1e10)
        log_rc = np.log10(rc_array)
        mask = np.isfinite(log_M) & np.isfinite(log_rc)

        slope, intercept, r_value, p_value, _ = stats.linregress(log_M[mask], log_rc[mask])

        A = 10 ** intercept
        alpha = slope
        R2 = r_value ** 2

        self.rc_calibration = CalibrationResult(
            parameter='r_c',
            a=A,
            b=alpha,
            R2=R2,
            p_value=p_value,
            n_galaxies=np.sum(mask),
            mass_range=(M_array.min(), M_array.max()),
            formula=f"r_c = {A:.2f} x (M/10^10)^{alpha:.2f} kpc",
            comparison_sparc="SPARC: r_c = 2.6 x (M/10^10)^0.56 kpc, R^2 = 0.768"
        )

        return self.rc_calibration

    def get_statistics(self) -> Dict[str, Any]:
        """Get summary statistics."""
        if not self.results:
            return {}

        improvements = [r.improvement_k for r in self.results]
        n_improved = sum(1 for i in improvements if i > 0)
        n_baryonic = sum(1 for r in self.results if r.baryonic_valid)

        sources = {}
        for r in self.results:
            sources[r.source] = sources.get(r.source, 0) + 1

        return {
            'total_galaxies': len(self.results),
            'sources': sources,
            'n_improved': n_improved,
            'n_baryonic': n_baryonic,
            'improvement_median': np.median(improvements),
            'improvement_mean': np.mean(improvements),
            'improvement_std': np.std(improvements)
        }

    def save_results(self, output_dir: Path = None) -> Path:
        """Save calibration results to file."""
        output_dir = output_dir or RESULTS_DIR
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "TMT_BIG_SPARC_calibration.txt"

        stats = self.get_statistics()

        with open(output_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("BIG-SPARC UNIFIED TMT CALIBRATION\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Total galaxies: {stats.get('total_galaxies', 0)}\n")
            f.write(f"Sources: {stats.get('sources', {})}\n\n")

            f.write("=" * 50 + "\n")
            f.write("PERFORMANCE\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"Galaxies improved: {stats.get('n_improved', 0)}/{stats.get('total_galaxies', 0)}\n")
            f.write(f"Median improvement: {stats.get('improvement_median', 0):.1f}%\n\n")

            if self.k_calibration:
                f.write("=" * 50 + "\n")
                f.write("k(M) CALIBRATION\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"{self.k_calibration.formula}\n")
                f.write(f"R^2 = {self.k_calibration.R2:.4f}\n")
                f.write(f"Galaxies: {self.k_calibration.n_galaxies}\n")
                f.write(f"Comparison: {self.k_calibration.comparison_sparc}\n\n")

            if self.rc_calibration:
                f.write("=" * 50 + "\n")
                f.write("r_c(M) CALIBRATION\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"{self.rc_calibration.formula}\n")
                f.write(f"R^2 = {self.rc_calibration.R2:.4f}\n")
                f.write(f"Comparison: {self.rc_calibration.comparison_sparc}\n")

        print(f"Results saved: {output_file}")
        return output_file

    def generate_figure(self, output_dir: Path = None) -> Optional[Path]:
        """Generate calibration figure."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not available")
            return None

        output_dir = output_dir or RESULTS_DIR

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        valid = [r for r in self.results if not r.baryonic_valid]
        M_plot = np.array([r.M_bary for r in valid])
        k_plot = np.array([r.k_opt for r in valid])
        rc_plot = np.array([r.r_c_free for r in valid])
        sources = [r.source for r in valid]

        # Color by source
        color_map = {'SPARC': 'green', 'WALLABY': 'blue', 'APERTIF': 'orange', 'BIG-SPARC': 'red'}
        colors = [color_map.get(s, 'gray') for s in sources]

        # k vs M
        ax1 = axes[0, 0]
        ax1.scatter(M_plot, k_plot, alpha=0.3, s=8, c=colors)
        if self.k_calibration:
            M_range = np.logspace(7, 12, 100)
            k_model = self.k_calibration.a * (M_range / 1e10) ** self.k_calibration.b
            ax1.plot(M_range, k_model, 'r-', lw=2.5, label=self.k_calibration.formula)
            k_sparc = 4.00 * (M_range / 1e10) ** (-0.49)
            ax1.plot(M_range, k_sparc, 'g--', lw=2, alpha=0.7, label='SPARC')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('M_bary (M_sun)')
        ax1.set_ylabel('k optimal')
        ax1.set_title(f'k(M) Calibration (n={len(valid)})')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # r_c vs M
        ax2 = axes[0, 1]
        ax2.scatter(M_plot, rc_plot, alpha=0.3, s=8, c=colors)
        if self.rc_calibration:
            rc_model = self.rc_calibration.a * (M_range / 1e10) ** self.rc_calibration.b
            ax2.plot(M_range, rc_model, 'r-', lw=2.5, label=self.rc_calibration.formula)
            rc_sparc = 2.6 * (M_range / 1e10) ** 0.56
            ax2.plot(M_range, rc_sparc, 'g--', lw=2, alpha=0.7, label='SPARC')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('M_bary (M_sun)')
        ax2.set_ylabel('r_c (kpc)')
        ax2.set_title('r_c(M) Calibration')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Improvement histogram
        ax3 = axes[1, 0]
        improvements = [r.improvement_k for r in self.results]
        ax3.hist(improvements, bins=50, edgecolor='black', alpha=0.7)
        ax3.axvline(np.median(improvements), color='r', linestyle='--', lw=2,
                   label=f'Median = {np.median(improvements):.1f}%')
        ax3.set_xlabel('Improvement (%)')
        ax3.set_ylabel('Count')
        ax3.set_title('TMT v2.4 Improvement Distribution')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Mass distribution by source
        ax4 = axes[1, 1]
        for source in set(sources):
            masses = [r.M_bary for r in self.results if r.source == source]
            ax4.hist(np.log10(masses), bins=30, alpha=0.5, label=source)
        ax4.set_xlabel('log10(M_bary / M_sun)')
        ax4.set_ylabel('Count')
        ax4.set_title('Mass Distribution by Survey')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        fig_file = output_dir / "TMT_BIG_SPARC_calibration.png"
        plt.savefig(fig_file, dpi=150)
        plt.close()

        print(f"Figure saved: {fig_file}")
        return fig_file


def main():
    """Main execution function."""
    print("=" * 70)
    print("BIG-SPARC MODULE - TMT UNIFIED CALIBRATION")
    print("=" * 70)
    print()

    calibrator = BigSPARCCalibrator()

    # Load all surveys
    print("Loading surveys...")
    counts = calibrator.load_all_surveys()

    if not calibrator.rotation_curves:
        print("No data loaded!")
        return

    # Analyze
    print("\nAnalyzing galaxies...")
    calibrator.analyze_all()

    # Calibrate
    print("\nCalibrating k(M)...")
    k_result = calibrator.calibrate_k_M()
    if k_result:
        print(f"  {k_result.formula}")
        print(f"  R^2 = {k_result.R2:.4f}")

    print("\nCalibrating r_c(M)...")
    rc_result = calibrator.calibrate_r_c_M()
    if rc_result:
        print(f"  {rc_result.formula}")
        print(f"  R^2 = {rc_result.R2:.4f}")

    # Statistics
    stats = calibrator.get_statistics()
    print(f"\nStatistics:")
    print(f"  Galaxies improved: {stats['n_improved']}/{stats['total_galaxies']}")
    print(f"  Median improvement: {stats['improvement_median']:.1f}%")

    # Save
    calibrator.save_results()
    calibrator.generate_figure()

    print("\n" + "=" * 70)
    print("BIG-SPARC CALIBRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
