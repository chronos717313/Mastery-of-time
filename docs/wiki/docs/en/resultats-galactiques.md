# Galactic results

> The historical name "Mastery of Time" reflects the project's informal
> name; the formal scientific designation is the
> **Temporon-Mediated Theory (TMT)**.

## The effective mass profile

In the static post-Newtonian limit, integrating the temporon
stress-energy contribution yields the effective mass profile

$$ M_{\rm eff}(r) = M_{\rm bary}(r)\,\bigl[\,1 + (r/r_{c})^{n}\,\bigr], $$

where \( r_{c} \) is a transition radius and \( n \) an exponent. This
profile had already been used phenomenologically in the literature; here it
**emerges from the action**, with \( r_{c} \) and \( n \) fixed by the
Lagrangian parameters. The exponent takes the theoretical value
\( n = 1/2 \).

## The scaling law r_c ∝ M^(1/2)

The transition radius is fixed by the condensation condition
\( \rho_{m}(r_{c}) = \rho_{\rm tr} \). For an exponential disk of baryonic
mass \( M_{\rm bary} \) at fixed central surface density, the geometric
relation \( M_{\rm bary} = 2\pi\Sigma_{0}R_{d}^{2} \) implies a scale
length \( R_{d}\propto M_{\rm bary}^{1/2} \), hence

$$ r_{c}(M_{\rm bary}) = r_{c}^{(0)}\,
   \left(\frac{M_{\rm bary}}{10^{10}\,M_{\odot}}\right)^{1/2}\!\mathrm{kpc}. $$

The exponent \( 1/2 \) follows from the exponential-disk geometry combined
with the near-constancy of the disk vertical scale height. The numerical
prefactor is \( r_{c}^{(0)}\approx 8.7~\mathrm{kpc} \); it has the
theoretical counterpart \( \mathcal{C}\,(2\pi\Sigma_{0})^{-1/2} \), where
\( \mathcal{C} \) is a dimensionless condensation constant. Calibrating
\( \mathcal{C} \) on the SPARC median galaxy fixes this single
normalisation; all subsequent applications are then parameter-free.

## Validation against the SPARC sample

The SPARC sample (Spitzer Photometry and Accurate Rotation Curves)
comprises 175 disk galaxies. Four fail the data-quality cuts and three have
a fitted \( r_{c} \) at the prior boundary, leaving an **analysable sample
of 168 galaxies**. For each galaxy, the parameters are fitted with the
exponent fixed at its theoretical value \( n = 1/2 \).

| Quantity | Value | Sample |
|---|---|---|
| SPARC galaxies loaded | 175 | — |
| Analysable sample | 168 | — |
| Galaxies improved over Newton | 162 / 168 (96.4%) | — |
| Median \( \chi^{2} \) improvement | 92.2% | 168 |
| Median \( r_{c} \) | 5.9 kpc | 168 |
| \( \Delta\mathrm{BIC} > 10 \) in favour | 82.7% | 168 |
| \( \Delta\mathrm{BIC} > 6 \) in favour | 85.1% | 168 |

The six galaxies for which the model does not improve over the Newtonian
fit are baryon-dominated systems well described by Newtonian dynamics
alone — the expected behaviour when the density stays well below the
transition density.

## The empirical r_c — M_bary relation

A log-log linear regression on the 168 galaxies gives

$$ \log_{10}(r_{c}/\mathrm{kpc}) =
   (0.48\pm0.04)\,\log_{10}\!\bigl(M_{\rm bary}/10^{10}M_{\odot}\bigr)
   + \log_{10}(8.7), $$

with a Pearson correlation \( r = 0.69 \) and
\( p = 4.7\times10^{-25} \) \( (N = 168) \). The empirical exponent
\( 0.48\pm0.04 \) deviates from the predicted value \( 1/2 \) by only
\( 0.6\sigma \). The intrinsic scatter
\( \sigma_{\log r_{c}}\simeq 0.46~\mathrm{dex} \) is consistent with the
variability of the disk vertical scale height.

No universal mass-dependent length appears in \( \Lambda\mathrm{CDM} \)-NFW
haloes; modified Newtonian dynamics (MOND), for its part, postulates a
universal acceleration scale rather than a length. Deriving this scaling
law from the action is the central observational result of the manuscript
submitted to *Physical Review D*.

## Falsifiable predictions

The theory offers two near-term falsifiable predictions, distinct from
\( \Lambda\mathrm{CDM} \):

1. **The law \( r_{c}\propto M_{\rm bary}^{1/2} \) on newly observed
   galaxies.** DESI and Euclid will provide rotation curves for about
   \( 10^{4} \) disk galaxies. A measured exponent outside the range
   \( [0.4, 0.6] \) on \( N\gtrsim10^{3} \) galaxies would falsify the
   derivation.
2. **Strict isotropy of the scalar lensing contribution** (below the 0.1%
   level). The temporon contribution is strictly scalar; any shear-shape
   correlation detected above this threshold would falsify the framework.

A longer-term prediction is the existence of a scalar (breathing)
gravitational-wave polarisation of amplitude
\( h_{s}/h_{t}\sim 10^{-5}\!-\!10^{-2} \), in principle accessible to LISA.
