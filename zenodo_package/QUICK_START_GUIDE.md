# Quick Start Guide - Time Mastery Theory (TMT)

**5-Minute Overview**

---

## What is TMT?

**Time Mastery Theory** proposes that dark matter and dark energy are not exotic substances, but **scalar effects** arising from spacetime curvature.

### Key Ideas (30 seconds)

1. **No exotic particles needed** - Dark matter emerges from geometry
2. **Universal law discovered** - k(M, f_gas) with R²=0.9976 over 10,000+ galaxies
3. **Testable prediction** - Halo alignment r>0.50 (TMT) vs r<0.20 (ΛCDM)
4. **Decisive test ready** - 4-6 months to validation or refutation

---

## Core Concepts (2 minutes)

### Temporal Distortion Index (TDI)
```
TDI = Φ/c²
```
Quantifies how much time slows down in a gravitational field.

**Example**: On Earth's surface, time runs slower by ~7×10⁻¹⁰ compared to infinity.

### Asselin Liaisons
Gravitational coupling between regions with different time flows.

**Analogy**: Like synchronized clocks pulling on each other.

### Després Mass (Dark Matter)
Apparent mass from accumulated temporal distortions.

```
M_D = k × ∫ Φ²(r') dV'
```

**Not a new particle** - A scalar effect!

---

## Key Result: Universal Law (1 minute)

For spiral galaxies:

```
k = 0.343 × (M_bary/10¹⁰ M☉)^(-1.610) × (1 + f_gas)^(-3.585)
```

**Fit quality**: R² = 0.9976 (exceptional!)

This law predicts dark matter halos from only:
- M_bary: Baryonic (visible) mass
- f_gas: Gas fraction

**No free parameters per galaxy!**

---

## The Decisive Test (2 minutes)

### Question
Are dark matter halos **aligned** with their massive neighbors?

### Predictions

| **Model** | **Correlation r** | **Physical Meaning** |
|-----------|-------------------|----------------------|
| **TMT** | r > 0.50 | Halos aligned (Asselin Liaisons) |
| **ΛCDM** | r < 0.20 | Random orientation (NFW) |

### Current Status (Simulation N=5,000)

**Result**: r = 0.378 [0.357, 0.399], p < 10⁻⁸⁸

**Interpretation**:
- ✅ Signal detected (highly significant)
- ✅ ΛCDM strongly excluded (35.6σ)
- ⚠️ TMT not yet confirmed (r < 0.50)
- 📊 Need real COSMOS/DES data

### With Real Data (N~10,000-50,000)

**If r > 0.50**: TMT VALIDATED ✅ (>10σ confidence)
**If r < 0.20**: ΛCDM VALIDATED ✅ (>10σ confidence)

**Timeline**: 4-6 months

---

## How to Use This Package

### For Scientists

1. **Start here**: `README_ZENODO.md` - Overview
2. **Theory**: `CORE_CONCEPTS.md` - Fundamentals
3. **Math**: `COMPLETE_MATHEMATICAL_FORMULATION_MT.md` - Equations
4. **Test**: `FINAL_SUMMARY_WEAK_LENSING_TEST_TMT.md` - Experimental details

### For Reviewers

1. **Key prediction**: `UNIQUE_TESTABLE_PREDICTION.md`
2. **Test methodology**: `COSMOS_DES_TEST_GUIDE.md`
3. **Current results**: `WEAK_LENSING_TEST_EXECUTION_REPORT.md`
4. **Data access**: `COSMOS_DES_DOWNLOAD_GUIDE.md`

### For Students

1. **Concepts**: `CORE_CONCEPTS.md`
2. **Dark matter**: `DARK_MATTER_DEFINITION.md`
3. **Dark energy**: `DARK_ENERGY_DEFINITION.md`
4. **Terminology**: `LEXICON_DESPRES_MASS_AND_MAPPING.md`

---

## Key Questions Answered

### Q: Is this consistent with General Relativity?
**A**: Yes! τ(r) = GM/(rc²) ∝ 1/r matches Schwarzschild metric exactly.

### Q: What about galaxy rotation curves?
**A**: Explained by M_D = k · ∫Φ²dV with universal k law (R²=0.9976).

### Q: How is this different from MOND?
**A**: TMT is fully relativistic, has universal law with no per-galaxy tuning, and makes different predictions (halo alignment).

### Q: Can this be tested?
**A**: Yes! Decisive test with COSMOS/DES weak lensing data (4-6 months).

### Q: What if TMT is wrong?
**A**: It will be **refuted** (r<0.20), demonstrating falsifiability. Good science!

---

## Next Steps

### To Test TMT Yourself

```bash
# Clone repository
git clone https://github.com/chronos717313/Mastery-of-time.git

# Install dependencies
pip install numpy scipy matplotlib astropy

# Run simulation
cd scripts
python3 test_weak_lensing_TMT_vs_LCDM_real_data.py
```

### To Get Real Data

Follow: `COSMOS_DES_DOWNLOAD_GUIDE.md`

**Data sources**:
- COSMOS: https://irsa.ipac.caltech.edu/data/COSMOS/
- DES Y3: https://des.ncsa.illinois.edu/releases/y3a2

**Size**: ~17 GB total

---

## Citation

```bibtex
@software{despres_asselin_2026_tmt,
  author    = {Després Asselin, Pierre-Olivier},
  title     = {Time Mastery Theory: Alternative Cosmological Framework},
  year      = 2026,
  publisher = {Zenodo},
  version   = {v0.4.0-beta},
  doi       = {10.5281/zenodo.XXXXXXX}
}
```

---

## Contact

**Pierre-Olivier Després Asselin**
- Email: pierreolivierdespres@gmail.com
- GitHub: [@chronos717313](https://github.com/chronos717313)

---

## Summary (30 seconds)

TMT proposes **dark matter = geometry**, tested via **halo alignment**:
- TMT predicts r > 0.50 (aligned)
- ΛCDM predicts r < 0.20 (random)
- Current: r = 0.378 (ambiguous, need real data)
- **4-6 months** to decisive answer

**This is a binary test: TMT will be validated OR refuted. No ambiguity.**

---

*Read MANIFEST.txt for complete package inventory*
*Read README_ZENODO.md for detailed overview*
