# Internal Review Notes

## Pending Validation Tests

### S8 Tension (σ8 Tension)

**Status**: Predicted qualitatively, NOT quantitatively validated

**Background**:
- S8 = σ8 × √(Ωm/0.3) measures structure growth amplitude
- Current tension: Planck CMB (S8 = 0.832 ± 0.013) vs Weak Lensing (S8 = 0.759 ± 0.024) = ~2.7σ

**TMT Prediction**:
TMT predicts the S8 tension as a **signature** of the theory:
- CMB measures S8 at cosmological scale (ρ ~ ρ_crit) → standard growth
- Weak lensing measures S8 in/around halos (ρ > ρ_crit) → modified growth due to temporal superposition

The "S8 tension" could be a TMT signature, not an anomaly.

**Code Reference**: `scripts/deprecated/test_TMT_cosmologie_complete.py` (lines 304-363)

**Action Required**:
1. Develop quantitative S8 prediction with TMT formalism
2. Compare with latest KiDS-1000, DES Y3, HSC data
3. If validated, add to main validation table as 9th test

**Priority**: Medium - qualitative prediction exists, needs rigorous testing

---

*Last updated: January 2026*
