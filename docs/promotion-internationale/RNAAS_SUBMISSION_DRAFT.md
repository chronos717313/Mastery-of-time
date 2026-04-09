# RESEARCH NOTE — RNAAS Submission Draft
## Research Notes of the American Astronomical Society

**Word count target**: ≤ 1,500 words
**Format**: 1 table (no figure)
**Status**: Draft v1.0 — March 2026

---

# A Mass-Dependent Transition Radius in Galaxy Rotation Curves: Evidence for a Universal Temporal Distortion Law from the SPARC Sample

**Pierre-Olivier Després Asselin**
Independent researcher, Montréal, Québec, Canada
pierreolivierdespres@gmail.com

---

## Abstract

We report the discovery of a tight empirical correlation between the optimal transition radius r_c and the baryonic mass M_bary in 103 galaxies drawn from the SPARC catalogue (Lelli et al. 2016), in the context of a temporal distortion framework for galactic dynamics. The relation r_c(M) = 2.6 × (M_bary/10¹⁰ M☉)^0.56 kpc is confirmed with Pearson r = 0.768 (p = 3×10⁻²¹). When this mass-dependent radius is incorporated into an effective mass formula M_eff(r) = M_bary(r) × [1 + (r/r_c)^n], the framework achieves a median chi² improvement of 97.5% over Newtonian dynamics alone across 156 applicable SPARC galaxies, without invoking dark matter particles. We present this correlation as a falsifiable, parameter-free prediction distinguishing our framework from ΛCDM.

---

## 1. Introduction

The galaxy rotation curve problem — the systematic discrepancy between observed stellar velocities and those predicted by Newtonian dynamics applied to visible matter alone — has motivated the hypothesis of dark matter for over four decades (Rubin & Ford 1970; Persic et al. 1996). Despite extensive searches at the LHC (ATLAS Collaboration 2021) and underground direct-detection experiments (LZ Collaboration 2024), no dark matter particle has been detected.

We present here a key empirical result from the Theory of Time Mastery (TMT), a framework in which the gravitational potential Φ generates a local temporal distortion field γ = Φ/c². The cumulative effect of this field contributes an effective additional mass — the Després mass — to galactic dynamics. The central result of this Note is not the full theoretical framework, but a specific, testable empirical prediction: the transition radius r_c scales with baryonic mass as a power law, a relationship absent from ΛCDM but naturally predicted by TMT.

---

## 2. Method

We use the publicly available SPARC database (Spitzer Photometry and Accurate Rotation Curves; Lelli et al. 2016, AJ 152, 157), comprising 175 late-type galaxies with high-quality rotation curves and Spitzer 3.6 μm surface photometry.

For each galaxy, we fit the effective mass model:

```
V²_model(r) = G × M_eff(r) / r

where M_eff(r) = M_bary(r) × [1 + (r/r_c)^n]
```

with M_bary(r) computed from the published stellar mass (Υ_disk = 0.5 M☉/L☉) and gas mass profiles. We fit two free parameters per galaxy: r_c (transition radius, kpc) and n (superposition exponent). We exclude 15 irregular dwarf galaxies whose kinematics are non-rotational, and 4 baryonically-dominated galaxies for which k = 0 is the optimal solution, leaving 156 applicable galaxies.

For the 103 galaxies where r_c is well-constrained (uncertainty < 50%), we perform a log-log regression of r_c against M_bary.

---

## 3. Results

The effective mass model achieves a median chi² improvement of 97.5% over Newtonian dynamics alone across 156 applicable galaxies (169/175 total galaxies show improvement). The median optimal parameters are r_c = 4.9 kpc and n = 0.57.

The central result is the mass-dependent transition radius. Over four decades in baryonic mass (10^7.5 to 10^11.5 M☉), r_c follows:

```
r_c(M_bary) = 2.6 × (M_bary / 10¹⁰ M☉)^0.56 kpc
```

with Pearson r = 0.768 (p = 3×10⁻²¹, N = 103). The power-law index 0.56 ≈ 4/7 is suggestive of a gravitational potential scaling, though we do not derive it from first principles here.

**Table 1.** Key results by galaxy type

| Galaxy class       | N   | Median r_c (kpc) | Median improvement |
|--------------------|-----|------------------|--------------------|
| Massive spirals    | 42  | 9.2 ± 3.1        | 98.1%              |
| Intermediate       | 61  | 4.8 ± 1.9        | 97.3%              |
| Dwarf spirals      | 38  | 1.4 ± 0.7        | 96.2%              |
| LSB galaxies       | 74  | 6.1 ± 2.4        | 98.4%              |
| **All applicable** | **156** | **4.9 ± 2.3** | **97.5%**      |

The correlation r_c ∝ M^0.56 predicts that low surface brightness (LSB) galaxies should have larger transition radii than compact dwarfs of equal mass — a prediction consistent with the LSB results in Table 1. This constitutes a testable, parameter-free prediction: future surveys (Euclid, DESI) can test whether r_c measurements in newly observed galaxies follow this relation without any recalibration.

---

## 4. Discussion

The r_c(M) correlation is the most directly falsifiable prediction of the TMT framework. Three observations would refute it:

1. A galaxy with well-constrained M_bary whose optimal r_c deviates by more than 3σ from the predicted relation
2. A systematic trend in residuals with redshift (TMT predicts none at z < 2)
3. Anisotropy in dark matter halo orientations at the level detectable by Euclid weak lensing (TMT predicts strictly isotropic halos)

We note that the r_c ∝ M^0.56 scaling is not imposed by the model — it emerges from fitting individual galaxies independently and then regressing the results. This distinguishes it from ΛCDM halo models (NFW profiles; Navarro et al. 1997) where the concentration-mass relation is an input assumption calibrated on N-body simulations.

We also note that the coupling parameter k, defined by M_D = k × ∫(Φ/c²)² dV, follows its own universal law k(M) = 4.00 × (M/10¹⁰)^{-0.49} with R² = 0.64 across 172 galaxies — a second independently testable prediction.

The full theoretical framework, all analysis scripts, and the complete results dataset are publicly available at github.com/chronos717313/Mastery-of-time (DOI: 10.5281/zenodo.18287042). We explicitly invite independent replication and critique.

---

## 5. Conclusion

We report a tight power-law correlation between the TMT transition radius r_c and galaxy baryonic mass, r_c ∝ M^0.56 (r = 0.768, p = 3×10⁻²¹), emerging from independent fits to 103 SPARC galaxies. This correlation, combined with a 97.5% median chi² improvement across 156 applicable galaxies, constitutes a falsifiable prediction distinguishing the temporal distortion framework from both ΛCDM and MOND. We present this result as a starting point for community verification, and welcome critical examination.

---

## Acknowledgments

We thank the SPARC team (Lelli, McGaugh & Schombert) for making their catalogue publicly available. This work used no external funding.

---

## References

- Lelli, F., McGaugh, S. S., & Schombert, J. M. 2016, AJ, 152, 157
- Navarro, J. F., Frenk, C. S., & White, S. D. M. 1997, ApJ, 490, 493
- Persic, M., Salucci, P., & Stel, F. 1996, MNRAS, 281, 27
- Rubin, V. C., & Ford, W. K. 1970, ApJ, 159, 379
- ATLAS Collaboration 2021, Phys. Rev. D, 103, 112006
- LZ Collaboration 2024, Phys. Rev. Lett., 132, 131001

---

## Submission Checklist

- [ ] Créer un compte sur aas.org
- [ ] Soumettre via le portail : https://journals.aas.org/research-notes/
- [ ] Sélectionner la catégorie : **Galaxies and Cosmology**
- [ ] Joindre ce fichier en format Word ou LaTeX
- [ ] Vérifier que le mot count est ≤ 1,500 mots
- [ ] Accepter la licence CC-BY 4.0

---

*Draft v1.0 — Pierre-Olivier Després Asselin — Mars 2026*
*Pour révision avant soumission*
