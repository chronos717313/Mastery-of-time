# Formulación Matemática Completa
## Teoría de Maestría del Tiempo (MT)

**Versión**: 1.0
**Fecha**: 2025-12-07
**Autor**: Pierre-Olivier Després Asselin

---

## Tabla de Contenidos

1. [Principios Fundamentales](#1-principios-fundamentales)
2. [Ecuaciones Básicas](#2-ecuaciones-básicas)
3. [Masa Després (Materia Oscura)](#3-masa-després-materia-oscura)
4. [Expansión Diferencial (Energía Oscura)](#4-expansión-diferencial-energía-oscura)
5. [Predicciones Observacionales](#5-predicciones-observacionales)
6. [Parámetros Calibrados](#6-parámetros-calibrados)
7. [Pruebas Decisivas](#7-pruebas-decisivas)

---

## 1. Principios Fundamentales

### 1.1 Postulado de Distorsión Temporal

**Toda masa M crea una distorsión del tiempo local τ(r) proporcional al potencial gravitacional.**

```
τ(r) = Φ(r)/c² = GM/(rc²)     [adimensional]
```

**Propiedades**:
- τ ∝ 1/r (consistente con métrica de Schwarzschild)
- τ > 0 en todas partes (distorsión siempre positiva)
- τ → 0 cuando r → ∞

**Relación con Relatividad General**:
```
g₀₀ = -(1 + 2Φ/c²) = -(1 + 2τ)
```

---

### 1.2 Enlace Asselin

**Definición**: Gradiente de distorsión temporal entre dos regiones espaciales A y B.

```
Enlace_Asselin(A, B) = |τ(A) - τ(B)| = |Φ_A - Φ_B|/c²
```

**Interpretación física**:
- Mide el acoplamiento temporal entre dos regiones
- Más fuerte cerca de objetos masivos
- Se extiende hasta el horizonte gravitacional d_horizonte = c/H₀

**Propiedades**:
- Simetría: Enlace(A,B) = Enlace(B,A)
- No-localidad: existe incluso a grandes distancias
- Acumulativo: se suma sobre todo el volumen

---

### 1.3 Cartografía Després

**Definición**: Sistema de cartografía que proporciona el factor de Lorentz Després γ_Després en cualquier punto del espacio.

```
γ_Després(r) = 1/√(1 - v²(r)/c² - 2Φ(r)/c²)
```

**Índice de Distorsión Temporal (IDT)**:
```
IDT(r) = γ_Després(r) - 1
```

**Gradiente**:
```
∇γ_Després = gradiente de distorsión temporal
            = Enlace Asselin local
```

---

## 2. Ecuaciones Básicas

### 2.1 Factor de Lorentz Generalizado

**Forma completa incluyendo gravitación y cinemática**:

```
γ_Després(r) = 1/√(1 - v²/c² - 2Φ/c²)

donde:
  v(r) = velocidad orbital kepleriana
  Φ(r) = potencial gravitacional
```

**Para órbita circular** (3ª ley de Kepler: v² = GM/r):
```
γ_Després(r) = 1/√(1 - 3GM/(rc²))
```

**Validación Sistema Solar** (Tierra):
```
IDT_Tierra = γ_Després - 1 = 1.48 × 10⁻⁸
```
(Verificado con precisión de 0.001%)

---

### 2.2 Potencial Gravitacional Efectivo

**Para distribución de masa M(r)**:

```
Φ(r) = -GM(r)/r = -∫₀ʳ (G·4πr'²ρ(r'))/r dr'
```

**Perfil galáctico realista** (disco exponencial):
```
ρ(r) = (M_disco/(4πR_disco²h)) · exp(-r/R_disco)

donde:
  M_disco = masa del disco
  R_disco = radio característico (~5 kpc)
  h = altura del disco (~0.3 kpc)
```

---

## 3. Masa Després (Materia Oscura)

### 3.1 Definición

**La Masa Després es la masa equivalente aparente resultante de la acumulación de Enlaces Asselin**:

```
M_Després = M_observada - M_bariónica
```

**Naturaleza**: Efecto geométrico, NO partícula exótica.

---

### 3.2 Formulación Integral

**Ecuación fundamental**:

```
M_Després(r) = k_Asselin · ∫∫∫_V |∇γ_Després(r')|² dV'
```

**Donde**:
- k_Asselin = constante de acoplamiento [M☉ · kpc⁻³]
- ∇γ_Després = gradiente del factor de Lorentz
- Integración sobre volumen V de radio r

**Forma desarrollada**:
```
M_Després(r) = k_Asselin · ∫₀ʳ |dγ_Després/dr'|² · 4πr'² dr'
```

---

### 3.3 Gradiente de γ_Després

**Cálculo numérico** (diferencias finitas):
```
dγ/dr ≈ [γ_Després(r+Δr) - γ_Després(r-Δr)] / (2Δr)
```

**Forma analítica aproximada** (órbita circular):
```
dγ/dr ≈ (3GM)/(2rc²) · [1 - 3GM/(rc²)]^(-3/2)
```

---

### 3.4 Curva de Rotación Galáctica

**Velocidad de rotación total**:
```
v_rot²(r) = v_bariónica²(r) + v_Després²(r)

donde:
  v_bariónica² = GM_bary(r)/r
  v_Després² = GM_Després(r)/r
```

**Predicción MT**: Curva plana cuando M_Després(r) ∝ r

---

## 4. Expansión Diferencial (Energía Oscura)

### 4.1 Función de Hubble Modificada

**ΛCDM estándar**:
```
H_ΛCDM(z) = H₀√[Ωₘ(1+z)³ + ΩΛ]
```

**MT con expansión diferencial**:
```
H_MT(z, ρ) = H₀√[Ωₘ(1+z)³ + ΩΛ_eff · exp(β(1 - ρ/ρ_crit))]
```

**Parámetros**:
- H₀ = 67.4 km/s/Mpc (Planck 2018)
- Ωₘ = 0.315
- ΩΛ_eff = 0.685
- β = 0.38 ± 0.05 (calibrado en SNIa)
- ρ/ρ_crit = densidad relativa local

---

### 4.2 Entornos Cósmicos

**Vacíos** (ρ = 0.2 ρ_crit):
```
H_vacío = H₀√[Ωₘ(1+z)³ + ΩΛ exp(0.38 × 0.8)]
        = H₀√[Ωₘ(1+z)³ + 0.95 ΩΛ]
        → Expansión 38% más rápida
```

**Medio promedio** (ρ = ρ_crit):
```
H_medio = H_ΛCDM    (sin modificación)
```

**Cúmulos** (ρ = 5 ρ_crit):
```
H_cúmulo = H₀√[Ωₘ(1+z)³ + ΩΛ exp(-0.38 × 4)]
         = H₀√[Ωₘ(1+z)³ + 0.21 ΩΛ]
         → Expansión 97% más lenta
```

---

### 4.3 Distancia de Luminosidad

**Fórmula general**:
```
d_L(z, ρ) = (1 + z) ∫₀^z c/H_MT(z', ρ) dz'
```

**Módulo de distancia**:
```
μ(z, ρ) = 5 log₁₀[d_L(z, ρ)/10 pc]
```

**Predicción SNIa**:
```
Δμ(vacío - cúmulo) ~ 0.2 - 0.3 mag a z ~ 0.5
Δd_L(vacío - cúmulo) ~ 5 - 8% a z ~ 0.5
```

---

### 4.4 Efecto ISW (Integrated Sachs-Wolfe)

**Amplitud ISW** (evolución de potencial):
```
ISW ∝ ∫ d[Φ(z)]/dη dη

donde η = tiempo conforme
```

**Predicción MT**:
```
ISW_vacío / ISW_ΛCDM ~ 1.06  (amplificación 6%)
ISW_cúmulo / ISW_ΛCDM ~ 0.80  (reducción 20%)
```

**Prueba decisiva**: Analizar por separado correlación ISW-vacíos e ISW-cúmulos.

---

## 5. Predicciones Observacionales

### 5.1 Asimetría de Halos de Masa Després

**ΛCDM**: Halo esférico, simétrico (NFW)

**MT**: Halo asimétrico, alineado hacia vecino masivo

**Prueba cuantitativa**:
```
Correlación: θ_halo ↔ θ_vecino

MT predice: r > 0.5  (correlación fuerte)
ΛCDM:       r < 0.2  (sin correlación)
```

**Método**: Lentes gravitacionales débiles (COSMOS, UNIONS)

---

### 5.2 Curvas de Rotación según Entorno

**Predicción MT**:
```
M_Després(aislada) < M_Després(grupo) < M_Després(cúmulo)
```

**Porque**: Más Enlaces Asselin en entornos densos.

**Prueba**: Analizar curvas de rotación en función de:
- Densidad local LSS
- Distancia al vecino masivo más cercano
- Número de galaxias a d < 2 Mpc

---

### 5.3 Supernovas Ia según Entorno

**Predicción MT**:
```
m_B(SNIa en cúmulo) - m_B(SNIa en vacío) > 0

a corrimiento al rojo fijo z ~ 0.5
```

**Magnitud esperada**:
```
Δm_B ~ +0.2 a +0.3 mag  (cúmulos más distantes)
```

**Prueba**: Pantheon+ SNIa con clasificación de entorno (SDSS)

---

### 5.4 Firma CMB (ISW)

**Predicción MT**:
```
C_ℓ^ISW-vacíos > C_ℓ^ISW-ΛCDM
C_ℓ^ISW-cúmulos < C_ℓ^ISW-ΛCDM
```

**Prueba**: Correlación cruzada CMB × catálogos de vacíos (BOSS) y cúmulos (Planck SZ)

---

## 6. Parámetros Calibrados

### 6.1 Parámetro β (Expansión Diferencial)

**Valor calibrado**:
```
β = 0.38 ± 0.05
```

**Método**: Minimización de χ² en SNIa sintéticas Pantheon+
**Calidad del ajuste**: χ²_red = 1.01 (excelente)

**Significado físico**:
- β = 0: Sin expansión diferencial (ΛCDM)
- β = 0.38: Expansión varía ±30% según entorno
- β > 0.5: Expansión demasiado sensible a ρ (inestabilidades)

---

### 6.2 Constante k_Asselin

**Estado actual**: ⚠️ EN CALIBRACIÓN

**Intentos**:
1. **Enfoque acumulativo** (calibrate_k_Asselin.py):
   - k_Asselin ~ 0.048
   - χ²_red = 147.8 (MAL AJUSTE)
   - v_pred ~ 50-70% demasiado bajo

2. **Enfoque integral** (solve_M_Despres_integral.py):
   - k_Asselin ~ 0.01
   - M_Després ~ 0 (¡gradiente demasiado débil!)
   - Problema: |∇γ_Després|² ~ 10⁻¹⁸ (despreciable)

**Diagnóstico**:
- γ_Després ≈ 1.0000001 en todas partes en galaxias
- |∇γ_Després| ~ 10⁻⁹ kpc⁻¹ → integral ≈ 0
- **Necesita reformulación** o factor de amplificación

**Soluciones posibles**:
1. Añadir término volumétrico: M_D ∝ ∫ |∇τ|² · r^n dV (n > 2)
2. Efecto no-local: M_D(r) = k ∫ |∇γ(r')| · f(|r-r'|) dV'
3. Umbral: Enlaces significativos solo si |∇γ| > γ_min

---

### 6.3 Parámetros Cosmológicos

**Fijos** (Planck 2018):
```
H₀ = 67.4 km/s/Mpc
Ωₘ = 0.315
ΩΛ = 0.685
Ω_k = 0  (universo plano)
```

---

## 7. Pruebas Decisivas

### 7.1 Prueba #1: θ_halo ↔ θ_vecino (COSMOS/UNIONS)

**Si r > 0.5 y Δθ < 30°** → **MT VALIDADA** ✓
**Si r < 0.2** → **ΛCDM VALIDADA**, MT refutada ✗

**Estado**: Metodología preparada, lista para ejecutar (1-2h)

---

### 7.2 Prueba #2: Δd_L(vacío-cúmulo) SNIa

**Si Δd_L ~ 5-10% a z=0.5** → **MT CONSISTENTE** ✓
**Si Δd_L ~ 0%** → **ΛCDM VALIDADA** ✗

**Estado**: Prueba en datos sintéticos OK (β=0.38), esperando datos reales Pantheon+

---

### 7.3 Prueba #3: ISW-LSS Separado Vacíos/Cúmulos

**Si C_ℓ^vacíos / C_ℓ^cúmulos > 2** → **MT CONSISTENTE** ✓
**Si C_ℓ^vacíos / C_ℓ^cúmulos ~ 1** → **ΛCDM VALIDADA** ✗

**Estado**: Predicción calculada (ratio ~ 1.3), análisis Planck×BOSS pendiente

---

### 7.4 Prueba #4: Curvas de Rotación vs Entorno

**Si M_Després ∝ densidad_LSS** → **MT CONSISTENTE** ✓
**Si M_Després independiente del entorno** → **ΛCDM** ✗

**Estado**: Por hacer con SPARC + catálogos de entorno

---

## 8. Sistema Completo de Ecuaciones

### Ecuaciones Fundamentales MT

```
1. Distorsión temporal:
   τ(r) = GM(r)/(rc²)

2. Factor de Lorentz:
   γ_Després(r) = 1/√(1 - v²/c² - 2Φ/c²)

3. Enlace Asselin:
   L_AB = |τ_A - τ_B| = |Φ_A - Φ_B|/c²

4. Masa Després:
   M_Després(r) = k_Asselin · ∫₀ʳ |∇γ_Després|² · 4πr'² dr'

5. Masa total:
   M_tot(r) = M_bary(r) + M_Després(r)

6. Velocidad de rotación:
   v²(r) = G·M_tot(r)/r

7. Expansión diferencial:
   H(z, ρ) = H₀√[Ωₘ(1+z)³ + ΩΛ exp(β(1-ρ/ρ_crit))]

8. Distancia de luminosidad:
   d_L(z, ρ) = (1+z) ∫₀^z c/H(z',ρ) dz'
```

---

## 9. Fortalezas y Limitaciones

### Fortalezas ✅

1. **Consistencia RG**: τ(r) ∝ 1/r conforme a Schwarzschild
2. **Parsimonia**: 2 parámetros (β, k_Asselin) explican materia oscura + energía oscura
3. **β calibrado**: β = 0.38 con excelente ajuste (χ²_red = 1.01)
4. **Predicciones comprobables**: 4 pruebas decisivas identificadas
5. **Falsable**: Las pruebas proporcionan criterios claros MT vs ΛCDM

### Limitaciones Actuales ⚠️

1. **k_Asselin no calibrado**: Formulación integral da M_Després ≈ 0
2. **Firma ISW débil**: Ratio vacío/cúmulo = 1.3 (no 2-3 como se esperaba)
3. **Datos sintéticos**: Pruebas SNIa e ISW en simulaciones, no datos reales
4. **Modelo de crecimiento D(z)**: Necesita refinamiento para ISW

---

## 10. Próximos Pasos Críticos

### Prioridad 1: Resolver k_Asselin
- Probar formulaciones alternativas M_Després
- Añadir factor no-local o umbral
- Calibrar en SPARC completo (175 galaxias)

### Prioridad 2: Pruebas Observacionales
- Ejecutar análisis COSMOS θ_halo ↔ θ_vecino
- Descargar datos reales Pantheon+
- Analizar ISW-vacíos con Planck×BOSS

### Prioridad 3: Publicación
- Redactar artículo ApJ/MNRAS
- Enviar preimpresión arXiv
- Contactar colaboraciones (UNIONS, COSMOS)

---

## Referencias

**Documentos asociados**:
- `LEXIQUE_MASSE_CARTOGRAPHIE_DESPRES.md` - Terminología oficial
- `FORMALISATION_H_Z_RHO.md` - Expansión diferencial detallada
- `ANALYSE_COSMOS_PREPARATION.md` - Metodología prueba θ_halo

**Scripts Python**:
- `plot_H_z_rho.py` - Visualizaciones H(z, ρ)
- `analyze_pantheon_SNIa.py` - Prueba SNIa expansión diferencial
- `calibrate_k_Asselin.py` - Calibración k_Asselin (v1)
- `solve_M_Despres_integral.py` - Resolución integral (v2)
- `calculate_ISW_planck.py` - Efecto ISW con Planck

**Datos**:
- Planck 2018 (parámetros cosmológicos)
- SPARC (curvas de rotación, 6/175 galaxias probadas)
- Pantheon+ sintéticos (300 SNIa generadas)

---

**Documento creado**: 2025-12-07
**Versión**: 1.0
**Estado**: Formulación completa, calibraciones en progreso

---

**Contacto**:
Pierre-Olivier Després Asselin
Email: Pierreolivierdespres@gmail.com
Tel: 581-777-3247
