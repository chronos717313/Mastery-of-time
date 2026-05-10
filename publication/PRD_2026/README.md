# Tensor Modification of Time (TMT) — PRD 2026 Submission

This directory contains the complete submission package for the manuscript:

> **Galactic rotation curves from a scalar-tensor theory with double-well potential: derivation of the transition-radius scaling $r_c \propto M_{\rm bary}^{1/2}$**
>
> Pierre-Olivier Després Asselin (Independent Researcher, Montréal)
> Submitted to *Physical Review D*, May 2026
> ORCID: [0009-0009-7611-4550](https://orcid.org/0009-0009-7611-4550)

## Scope

This manuscript is deliberately restricted to the **galactic and post-Newtonian regimes**. Cosmological consequences of the same action (Hubble tension, CMB acoustic peaks) are deferred to a separate companion paper currently in preparation.

## Contents

| Path | Description |
|---|---|
| `article_prd.tex` | Main manuscript (RevTeX 4.2, 749 lines) |
| `cover_letter_PRD.tex` | Cover letter to PRD editors |
| `refs_prd.bib` | Bibliography (32 entries, all verified via NASA ADS) |
| `figures/figure_rotation_curves_v24_PRD.png` | Fig. 1 — six representative SPARC rotation curves |
| `figures/figure_rc_M_scatter_REAL.png` | Supplementary scatter $r_c$ vs $M_{\rm bary}$ |
| `scripts/generate_rotation_curves_v24_PRD.py` | Reproduces Fig. 1 |
| `scripts/generate_rc_M_scatter_REAL.py` | Reproduces the scatter on real SPARC data |
| `scripts/derive_dual_beta_factors.py` | First-principles estimate of dual-β factors (preliminary, deferred to companion paper) |
| `audit/SPARC_REAL_ANALYSIS_LOG.md` | Audit trail: input parameters, output statistics, reproduction commands |
| `audit/DUAL_BETA_AUDIT.md` | Notes on the dual-β derivation; deferred items for the companion paper |

## Reproducibility

All numerical claims in the manuscript are reproducible from the public SPARC catalogue (Lelli, McGaugh & Schombert 2016) using the calibration script `big_sparc_module.py` from the parent repository.

```bash
# From the repository root:
ln -sf sparc data/SPARC                   # workaround for case-sensitive path
python3 scripts/calibration/big_sparc_module.py  # SPARC fit
python3 publication/PRD_2026/scripts/generate_rotation_curves_v24_PRD.py
python3 publication/PRD_2026/scripts/generate_rc_M_scatter_REAL.py
```

Expected output: `r_c = 8.70 × (M/10^10)^0.48 kpc`, Pearson $r = 0.69$, $p = 4.7 \times 10^{-25}$, $N = 168$ galaxies.

## Key results (verified end-to-end)

- Empirical relation: $r_c \propto M_{\rm bary}^{0.48 \pm 0.04}$ on 168 SPARC galaxies
- Empirical exponent deviates from theoretical 1/2 by **only 0.6σ**
- Median χ² improvement over Newtonian baseline: **92.2 %** in **96.4 %** of the sample
- ΔBIC > 10 favouring temperon: **82.7 %** of the sample
- Solar-system PPN tests satisfied for $\xi v^2 < 10^{-5} M_{\rm Pl}^2$

## License

Code and data: **CC BY 4.0** (Creative Commons Attribution).
Manuscript text: copyright Pierre-Olivier Després Asselin, 2026.

## Citation

Once published, please cite both the article and the Zenodo deposit:

```
Després Asselin, P.-O. (2026)
"Galactic rotation curves from a scalar-tensor theory with double-well
 potential: derivation of the transition-radius scaling
 r_c ∝ M_bary^(1/2)"
Physical Review D, [in review]
arXiv: [link when posted]
Zenodo DOI: 10.5281/zenodo.18287042 (latest version)
```

## Companion papers in preparation

1. **Cosmological implications** — late-time density-dependent expansion, recombination behaviour, Boltzmann implementation
2. **Bullet Cluster analysis** — density-dependent matter coupling κ(ρ) for merging clusters
3. **Quantum-foundational interpretations** — connections between the temperon scalar field and quantum mechanics (Foundations of Physics)

## Contact

Pierre-Olivier Després Asselin
[pierreolivierdespres@gmail.com](mailto:pierreolivierdespres@gmail.com)
ORCID: 0009-0009-7611-4550
