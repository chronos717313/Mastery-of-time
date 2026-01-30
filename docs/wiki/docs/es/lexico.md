# Léxico TMT v2.4

Este léxico define todos los términos específicos de la **Teoría de Dominio del Tiempo** (TMT).

---

## Términos Fundamentales

### $\tau(x)$ - Distorsión Temporal

**Definición**: La distorsión temporal local, definida como la relación del potencial gravitacional al cuadrado de la velocidad de la luz.

$$
\tau(x) = \frac{\Phi(x)}{c^2} = \frac{GM}{rc^2} \quad \text{[adimensional]}
$$

**Propiedades**:

| Propiedad | Valor | Significado |
|-----------|-------|-------------|
| $\tau \propto 1/r$ | Decaimiento radial | Consistente con métrica de Schwarzschild |
| $\tau > 0$ | Siempre positivo | Tiempo siempre dilatado cerca de masas |
| $\tau \to 0$ | Cuando $r \to \infty$ | Espacio-tiempo plano lejos de masas |

**Conexión con la Relatividad General**:

$$
g_{00} = -\left(1 + \frac{2\Phi}{c^2}\right) = -(1 + 2\tau)
$$

**Ejemplos numéricos**:

| Lugar | $\tau$ | Efecto observable |
|-------|--------|-------------------|
| Superficie Tierra | $7 \times 10^{-10}$ | Corrección GPS necesaria |
| Órbita terrestre | $1.5 \times 10^{-8}$ | Medido por satélites |
| Superficie Sol | $2 \times 10^{-6}$ | Corrimiento al rojo espectral |
| Estrella de neutrones | $\sim 0.2$ | Efectos relativistas extremos |
| Horizonte agujero negro | $0.5$ | Límite teórico |

---

### TDI - Índice de Distorsión Temporal

**Definición**: El Índice de Distorsión Temporal cuantifica la desviación del espacio-tiempo plano (Minkowski).

$$
\text{TDI}(r) = \gamma_{\text{Després}}(r) - 1
$$

**Interpretación**:

- TDI = 0: Sin distorsión (espacio-tiempo plano)
- TDI > 0: Distorsión temporal significativa

**Ejemplos**:

| Objeto | TDI |
|--------|-----|
| Mercurio | $3.83 \times 10^{-8}$ |
| Tierra | $1.48 \times 10^{-8}$ |
| Júpiter | $2.85 \times 10^{-9}$ |
| Centro galáctico | $\sim 10^{-6}$ |
| Vacío cósmico | $\sim 10^{-8}$ |

---

### $\gamma_{\text{Després}}$ - Factor de Lorentz Generalizado

**Definición**: El factor de Lorentz generalizado que combina efectos cinemáticos Y gravitacionales.

$$
\gamma_{\text{Després}}(r,v) = \frac{1}{\sqrt{1 - \frac{v^2}{c^2} - \frac{2\Phi}{c^2}}} = \frac{1}{\sqrt{1 - \frac{v^2}{c^2} - 2\tau}}
$$

**Componentes**:

| Término | Origen | Efecto |
|---------|--------|--------|
| $v^2/c^2$ | Relatividad especial | Dilatación cinemática |
| $2\Phi/c^2 = 2\tau$ | Relatividad general | Dilatación gravitacional |

**Propiedades**:

- Valor mínimo: $\gamma_{\text{Després}} = 1$ (espacio vacío, lejos de cualquier masa)
- Aumenta cerca de objetos masivos
- Integra la 3ª ley de Kepler ($v \propto \sqrt{M/r}$)

**Validación**: Relación $2\Phi/c^2 = 2 \times v^2/c^2$ verificada al 0.001% de precisión en el Sistema Solar.

---

### Ecuación Després-Schrödinger

**La ecuación fundamental** que unifica mecánica cuántica y gravitación:

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t} = \left[-\frac{\hbar^2}{2m_{eff}} \nabla^2 + V(x) + mc^2\tau(x)\right] \psi
$$

#### Descomposición de términos

| Término | Expresión | Origen | Significado |
|---------|-----------|--------|-------------|
| **Tiempo modificado** | $[1+\tau]^{-1} \partial\psi/\partial t$ | Relatividad | Tiempo propio variable |
| **Cinético modificado** | $-\hbar^2/(2m_{eff}) \nabla^2\psi$ | RG + MC | Masa efectiva gravitacional |
| **Potencial clásico** | $V(x)\psi$ | MC estándar | Electromagnético, nuclear |
| **Potencial temporal** | $mc^2\tau(x)\psi$ | **TMT nuevo!** | Energía de distorsión temporal |

#### Lado izquierdo: Evolución temporal modificada

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t}
$$

- $i\hbar$: Constante de Planck (cuántica)
- $[1 + \tau(x)]^{-1}$: **NUEVO** - El tiempo fluye más lento en campos gravitacionales
- $\partial\psi/\partial t$: Derivada temporal estándar

**Tiempo propio**: $dt_{\text{propio}} = [1 + \tau(x)] \cdot dt_{\text{cósmico}}$

#### Lado derecho: Hamiltoniano efectivo

1. **Energía cinética**: $\hat{A}_{\text{cinética}} = -\frac{\hbar^2}{2m_{eff}} \nabla^2\psi$ con $m_{eff} = m_0/\gamma_{\text{Després}}$
2. **Potencial clásico**: $\hat{A}_{\text{potencial}} = V(x)\psi$ (sin cambios)
3. **Potencial temporal**: $\hat{A}_{\text{temporal}} = mc^2\tau(x)\psi$ (nuevo término TMT)

#### Casos límite (validación)

| Límite | Condición | Resultado |
|--------|-----------|-----------|
| Espacio plano | $\tau \to 0$ | Recupera ecuación de Schrödinger estándar |
| Clásico | $\hbar \to 0$ | Recupera ecuación de Hamilton-Jacobi |
| Campo débil | $\tau \ll 1$ | Reproduce corrimiento al rojo gravitacional de Einstein |

---

### $M_{\text{Després}}$ - Masa Després

**Definición**: La masa aparente equivalente resultante de la acumulación de distorsión temporal.

$$
M_{\text{Després}} = k \times \int \left(\frac{\Phi}{c^2}\right)^2 dV = k \times \int \tau^2 \, dV
$$

**Naturaleza**: Efecto **geométrico**, NO una partícula exótica.

**Interpretación física**:

$$
M_{\text{observada}} = M_{\text{bariónica}} + M_{\text{Després}}
$$

| Modelo | Interpretación de la "materia oscura" |
|--------|---------------------------------------|
| ΛCDM | Partículas exóticas (WIMPs, axiones) |
| TMT | Efecto geométrico de distorsión temporal |

---

### $r_c(M)$ - Radio Crítico

**Definición**: El radio de transición donde las amplitudes de superposición temporal son iguales ($\alpha^2 = \beta^2 = 0.5$).

$$
r_c = 2.6 \times \left(\frac{M_{\text{bary}}}{10^{10} M_\odot}\right)^{0.56} \text{ kpc}
$$

**Significado**: Es exactamente el radio donde las curvas de rotación galáctica se vuelven planas.

**Ejemplos por tipo de galaxia**:

| Tipo | $M_{\text{bary}}$ | $r_c$ |
|------|-------------------|-------|
| Enana | $10^8 M_\odot$ | 0.4 kpc |
| Media | $10^{10} M_\odot$ | 2.6 kpc |
| Masiva | $10^{11} M_\odot$ | 9.4 kpc |

**Validación**: Correlación $r = 0.768$ en 103 galaxias SPARC.

---

### $k(M)$ - Constante de Acoplamiento

**Definición**: El coeficiente de acoplamiento entre distorsión temporal y efecto gravitacional aparente.

$$
k = 3.97 \times \left(\frac{M}{10^{10}}\right)^{-0.48}
$$

**Validación**: $R^2 = 0.64$ en 168 galaxias SPARC.

**Interpretación**: Cuanto más masiva la galaxia, más débil el acoplamiento (exponente negativo).

---

### $\alpha / \beta$ - Amplitudes de Superposición Temporal

**Estado cuántico del universo**:

$$
|\Psi\rangle = \alpha|t\rangle + \beta|\bar{t}\rangle
$$

donde:

- $|t\rangle$: estado tiempo **forward** (materia visible)
- $|\bar{t}\rangle$: estado tiempo **backward** (reflexión temporal = "materia oscura")

**Definiciones de amplitudes**:

$$
|\alpha(r)|^2 = \frac{1}{1 + (r/r_c)^n} \quad \text{(tiempo forward)}
$$

$$
|\beta(r)|^2 = \frac{(r/r_c)^n}{1 + (r/r_c)^n} \quad \text{(tiempo backward)}
$$

**Normalización cuántica**: $|\alpha|^2 + |\beta|^2 = 1$

**Perfil radial**:

| Región | $\alpha^2$ | $\beta^2$ | Interpretación |
|--------|------------|-----------|----------------|
| $r < r_c$ | > 0.5 | < 0.5 | Forward dominante |
| $r = r_c$ | 0.5 | 0.5 | **Transición crítica** |
| $r > r_c$ | < 0.5 | > 0.5 | Backward dominante (halo) |

**Masa efectiva**:

$$
M_{\text{eff}}(r) = M_{\text{visible}}(r) \times \left[1 + \frac{\beta^2(r)}{\alpha^2(r)}\right]
$$

---

### Temporones

**Definición**: Excitaciones cuánticas del campo de distorsión temporal.

**Propiedades**:

| Propiedad | Valor |
|-----------|-------|
| Masa en reposo | 0 |
| Espín | Por determinar |
| Interacción | Median la "gravedad temporal" |

**Rol**: Alternativa a las partículas WIMP para explicar los efectos gravitacionales atribuidos a la materia oscura.

---

### Enlace Asselin

**Definición**: Gradiente de distorsión temporal entre dos regiones espaciales A y B.

$$
\text{Enlace\_Asselin}(A, B) = |\tau(A) - \tau(B)| = \frac{|\Phi_A - \Phi_B|}{c^2}
$$

**Propiedades**:

| Propiedad | Descripción |
|-----------|-------------|
| **Simetría** | Enlace(A,B) = Enlace(B,A) |
| **No-localidad** | Existe incluso a grandes distancias |
| **Acumulativo** | Se suma sobre todo el volumen |

**Interpretación física**: Mide el acoplamiento temporal entre dos regiones del espacio.

---

### Cartografía Després

**Definición**: Sistema de mapeo que proporciona el factor $\gamma_{\text{Després}}$ en cualquier punto del espacio basado en la distribución de materia y campos gravitacionales.

**Aplicaciones**:

| Escala | Aplicación |
|--------|------------|
| Sistema Solar | TDI verificado al 0.001% de precisión |
| Galaxias | Predice curvas de rotación planas |
| Cosmología | Explica expansión diferencial |

---

## Tabla Resumen

| Símbolo | Nombre | Fórmula | Unidad |
|---------|--------|---------|--------|
| $\tau(x)$ | Distorsión temporal | $\Phi/c^2$ | adim. |
| TDI | Índice de distorsión | $\gamma_{\text{Després}} - 1$ | adim. |
| $\gamma_{\text{Després}}$ | Factor de Lorentz | $1/\sqrt{1-v^2/c^2-2\Phi/c^2}$ | adim. |
| $M_D$ | Masa Després | $k\int\tau^2 dV$ | $M_\odot$ |
| $r_c$ | Radio crítico | $2.6(M/10^{10})^{0.56}$ | kpc |
| $k$ | Acoplamiento | $3.97(M/10^{10})^{-0.48}$ | - |
| $\alpha, \beta$ | Amplitudes | $|\alpha|^2+|\beta|^2=1$ | adim. |

---

## Comparación ΛCDM vs TMT

| Concepto | ΛCDM | TMT |
|----------|------|-----|
| **Materia oscura** | Partículas WIMP/axiones | Efecto geométrico ($M_{\text{Després}}$) |
| **Energía oscura** | Constante cosmológica Λ | Superposición $\alpha/\beta$ en vacíos |
| **Unificación MC+RG** | Problema abierto | Ecuación Després-Schrödinger |
| **Parámetros libres** | 6 (ΛCDM estándar) | 2 ($r_c$, $n$) |
| **Detección directa** | Fracasos después de 50 años | N/A (sin partícula) |

---

[Volver al Inicio](index.md) | [Puentes Conceptuales](pontes_conceptuales/index.md) | [Validación](validacion/index.md)
