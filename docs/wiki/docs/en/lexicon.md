# TMT Lexicon

This lexicon defines all terms specific to the **Time Mastery Theory** (TMT).

---

## Fundamental Terms

### $\tau(x)$ - Temporal Distortion

**Definition**: The local temporal distortion, defined as the ratio of gravitational potential to the square of the speed of light.

$$
\tau(x) = \frac{\Phi(x)}{c^2} = \frac{GM}{rc^2} \quad \text{[dimensionless]}
$$

**Properties**:

| Property | Value | Meaning |
|----------|-------|---------|
| $\tau \propto 1/r$ | Radial decay | Consistent with Schwarzschild metric |
| $\tau > 0$ | Always positive | Time always dilated near masses |
| $\tau \to 0$ | When $r \to \infty$ | Flat spacetime far from masses |

**Connection to General Relativity**:

$$
g_{00} = -\left(1 + \frac{2\Phi}{c^2}\right) = -(1 + 2\tau)
$$

**Numerical examples**:

| Location | $\tau$ | Observable effect |
|----------|--------|-------------------|
| Earth surface | $7 \times 10^{-10}$ | GPS correction required |
| Earth orbit | $1.5 \times 10^{-8}$ | Measured by satellites |
| Sun surface | $2 \times 10^{-6}$ | Spectral redshift observed |
| Neutron star | $\sim 0.2$ | Extreme relativistic effects |
| Black hole horizon | $0.5$ | Theoretical limit |

---

### TDI - Temporal Distortion Index

**Definition**: The Temporal Distortion Index quantifies the deviation from flat spacetime (Minkowski).

$$
\text{TDI}(r) = \gamma_{\text{Després}}(r) - 1
$$

**Interpretation**:

- TDI = 0: No distortion (flat spacetime)
- TDI > 0: Significant temporal distortion

**Examples**:

| Object | TDI |
|--------|-----|
| Mercury | $3.83 \times 10^{-8}$ |
| Earth | $1.48 \times 10^{-8}$ |
| Jupiter | $2.85 \times 10^{-9}$ |
| Galactic center | $\sim 10^{-6}$ |
| Cosmic void | $\sim 10^{-8}$ |

---

### $\gamma_{\text{Després}}$ - Generalized Lorentz Factor

**Definition**: The generalized Lorentz factor combining kinematic AND gravitational effects.

$$
\gamma_{\text{Després}}(r,v) = \frac{1}{\sqrt{1 - \frac{v^2}{c^2} - \frac{2\Phi}{c^2}}} = \frac{1}{\sqrt{1 - \frac{v^2}{c^2} - 2\tau}}
$$

**Components**:

| Term | Origin | Effect |
|------|--------|--------|
| $v^2/c^2$ | Special relativity | Kinematic dilation |
| $2\Phi/c^2 = 2\tau$ | General relativity | Gravitational dilation |

**Properties**:

- Minimum value: $\gamma_{\text{Després}} = 1$ (empty space, far from any mass)
- Increases near massive objects
- Integrates Kepler's 3rd law ($v \propto \sqrt{M/r}$)

**Validation**: Relation $2\Phi/c^2 = 2 \times v^2/c^2$ verified to 0.001% precision in the Solar System.

---

### Després-Schrödinger Equation

**The fundamental equation** unifying quantum mechanics and gravitation:

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t} = \left[-\frac{\hbar^2}{2m_{eff}} \nabla^2 + V(x) + mc^2\tau(x)\right] \psi
$$

#### Term decomposition

| Term | Expression | Origin | Meaning |
|------|------------|--------|---------|
| **Modified time** | $[1+\tau]^{-1} \partial\psi/\partial t$ | Relativity | Variable proper time |
| **Modified kinetic** | $-\hbar^2/(2m_{eff}) \nabla^2\psi$ | GR + QM | Gravitational effective mass |
| **Classical potential** | $V(x)\psi$ | Standard QM | Electromagnetic, nuclear |
| **Temporal potential** | $mc^2\tau(x)\psi$ | **TMT new!** | Temporal distortion energy |

#### Left side: Modified temporal evolution

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t}
$$

- $i\hbar$: Planck's constant (quantum)
- $[1 + \tau(x)]^{-1}$: **NEW** - Time flows more slowly in gravitational fields
- $\partial\psi/\partial t$: Standard time derivative

**Proper time**: $dt_{\text{proper}} = [1 + \tau(x)] \cdot dt_{\text{cosmic}}$

#### Right side: Effective Hamiltonian

1. **Kinetic energy**: $\hat{A}_{\text{kinetic}} = -\frac{\hbar^2}{2m_{eff}} \nabla^2\psi$ with $m_{eff} = m_0/\gamma_{\text{Després}}$
2. **Classical potential**: $\hat{A}_{\text{potential}} = V(x)\psi$ (unchanged)
3. **Temporal potential**: $\hat{A}_{\text{temporal}} = mc^2\tau(x)\psi$ (new TMT term)

#### Limiting cases (validation)

| Limit | Condition | Result |
|-------|-----------|--------|
| Flat space | $\tau \to 0$ | Recovers standard Schrödinger equation |
| Classical | $\hbar \to 0$ | Recovers Hamilton-Jacobi equation |
| Weak field | $\tau \ll 1$ | Reproduces Einstein's gravitational redshift |

---

### $M_{\text{Després}}$ - Després Mass

**Definition**: The apparent equivalent mass resulting from accumulation of temporal distortion.

$$
M_{\text{Després}} = k \times \int \left(\frac{\Phi}{c^2}\right)^2 dV = k \times \int \tau^2 \, dV
$$

**Nature**: **Geometric** effect, NOT an exotic particle.

**Physical interpretation**:

$$
M_{\text{observed}} = M_{\text{baryonic}} + M_{\text{Després}}
$$

| Model | Interpretation of "dark matter" |
|-------|--------------------------------|
| ΛCDM | Exotic particles (WIMPs, axions) |
| TMT | Geometric effect of temporal distortion |

---

### $r_c(M)$ - Critical Radius

**Definition**: The transition radius where temporal superposition amplitudes are equal ($\alpha^2 = \beta^2 = 0.5$).

$$
r_c = 2.6 \times \left(\frac{M_{\text{bary}}}{10^{10} M_\odot}\right)^{0.56} \text{ kpc}
$$

**Meaning**: This is exactly the radius where galactic rotation curves become flat.

**Examples by galaxy type**:

| Type | $M_{\text{bary}}$ | $r_c$ |
|------|-------------------|-------|
| Dwarf | $10^8 M_\odot$ | 0.4 kpc |
| Medium | $10^{10} M_\odot$ | 2.6 kpc |
| Massive | $10^{11} M_\odot$ | 9.4 kpc |

**Validation**: Correlation $r = 0.768$ on 103 SPARC galaxies.

---

### $k(M)$ - Coupling Constant

**Definition**: The coupling coefficient between temporal distortion and apparent gravitational effect.

$$
k = 3.97 \times \left(\frac{M}{10^{10}}\right)^{-0.48}
$$

**Validation**: $R^2 = 0.64$ on 168 SPARC galaxies.

**Interpretation**: The more massive the galaxy, the weaker the coupling (negative exponent).

---

### $\alpha / \beta$ - Temporal Superposition Amplitudes

**Quantum state of the universe**:

$$
|\Psi\rangle = \alpha|t\rangle + \beta|\bar{t}\rangle
$$

where:

- $|t\rangle$: **forward** time state (visible matter)
- $|\bar{t}\rangle$: **backward** time state (temporal reflection = "dark matter")

**Amplitude definitions**:

$$
|\alpha(r)|^2 = \frac{1}{1 + (r/r_c)^n} \quad \text{(forward time)}
$$

$$
|\beta(r)|^2 = \frac{(r/r_c)^n}{1 + (r/r_c)^n} \quad \text{(backward time)}
$$

**Quantum normalization**: $|\alpha|^2 + |\beta|^2 = 1$

**Radial profile**:

| Region | $\alpha^2$ | $\beta^2$ | Interpretation |
|--------|------------|-----------|----------------|
| $r < r_c$ | > 0.5 | < 0.5 | Forward dominant |
| $r = r_c$ | 0.5 | 0.5 | **Critical transition** |
| $r > r_c$ | < 0.5 | > 0.5 | Backward dominant (halo) |

**Effective mass**:

$$
M_{\text{eff}}(r) = M_{\text{visible}}(r) \times \left[1 + \frac{\beta^2(r)}{\alpha^2(r)}\right]
$$

---

### Temporons

**Definition**: Quantum excitations of the temporal distortion field.

**Properties**:

| Property | Value |
|----------|-------|
| Rest mass | 0 |
| Spin | To be determined |
| Interaction | Mediate "temporal gravity" |

**Role**: Alternative to WIMP particles for explaining gravitational effects attributed to dark matter.

---

### Asselin Link

**Definition**: Temporal distortion gradient between two spatial regions A and B.

$$
\text{Asselin\_Link}(A, B) = |\tau(A) - \tau(B)| = \frac{|\Phi_A - \Phi_B|}{c^2}
$$

**Properties**:

| Property | Description |
|----------|-------------|
| **Symmetry** | Link(A,B) = Link(B,A) |
| **Non-locality** | Exists even at large distances |
| **Cumulative** | Adds up over entire volume |

**Physical interpretation**: Measures the temporal coupling between two regions of space.

---

### Després Mapping

**Definition**: Mapping system providing the $\gamma_{\text{Després}}$ factor at any point in space based on matter distribution and gravitational fields.

**Applications**:

| Scale | Application |
|-------|-------------|
| Solar System | TDI verified to 0.001% precision |
| Galaxies | Predicts flat rotation curves |
| Cosmology | Explains differential expansion |

---

## Summary Table

| Symbol | Name | Formula | Unit |
|--------|------|---------|------|
| $\tau(x)$ | Temporal distortion | $\Phi/c^2$ | dimensionless |
| TDI | Distortion index | $\gamma_{\text{Després}} - 1$ | dimensionless |
| $\gamma_{\text{Després}}$ | Lorentz factor | $1/\sqrt{1-v^2/c^2-2\Phi/c^2}$ | dimensionless |
| $M_D$ | Després Mass | $k\int\tau^2 dV$ | $M_\odot$ |
| $r_c$ | Critical radius | $2.6(M/10^{10})^{0.56}$ | kpc |
| $k$ | Coupling | $3.97(M/10^{10})^{-0.48}$ | - |
| $\alpha, \beta$ | Amplitudes | $|\alpha|^2+|\beta|^2=1$ | dimensionless |

---

## ΛCDM vs TMT Comparison

| Concept | ΛCDM | TMT |
|---------|------|-----|
| **Dark matter** | WIMP/axion particles | Geometric effect ($M_{\text{Després}}$) |
| **Dark energy** | Cosmological constant Λ | $\alpha/\beta$ superposition in voids |
| **QM+GR unification** | Open problem | Després-Schrödinger equation |
| **Free parameters** | 6 (standard ΛCDM) | 2 ($r_c$, $n$) |
| **Direct detection** | Failures after 50 years | N/A (no particle) |

---

[Back to Home](index.md) | [Conceptual Bridges](ponts_conceptuels/index.md) | [Validation](validation/index.md)
