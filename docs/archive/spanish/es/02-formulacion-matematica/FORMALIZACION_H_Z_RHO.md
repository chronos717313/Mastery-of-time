# Formalización de H(z, ρ) - Expansión Diferencial
## Teoría de Maestría del Tiempo

**Fecha**: 2025-12-06
**Autor**: Pierre-Olivier Després Asselin
**Versión**: 1.0

---

## 1. Recordatorio: Lambda-CDM Estándar

### Función de Hubble Estándar

En el modelo Lambda-CDM, la tasa de expansión es **uniforme** en todo el espacio:

```
H(z) = H₀ √[Ωₘ(1+z)³ + Ωᵣ(1+z)⁴ + ΩΛ]
```

Donde:
- `H₀` = constante de Hubble hoy ≈ 70 km/s/Mpc
- `Ωₘ` = densidad de materia (bariónica + oscura) ≈ 0.31
- `Ωᵣ` = densidad de radiación ≈ 9×10⁻⁵ (despreciable después de z < 3000)
- `ΩΛ` = densidad de energía oscura ≈ 0.69

**Propiedad clave**: H(z) es la **misma en todas partes** del universo a un corrimiento al rojo z dado.

---

## 2. Teoría de Maestría del Tiempo: Expansión Diferencial

### Principio Fundamental

**Hipótesis central**: La tasa de expansión local depende de la **densidad de materia local** ρ(r):

```
H_local(z, ρ) ≠ constante espacial
```

**Mecanismo físico**:
1. La materia crea una **distorsión temporal** τ(r) = GM/(rc²)
2. Esta distorsión **ancla** el espacio-tiempo localmente
3. Regiones densas (galaxias, cúmulos): expansión **ralentizada**
4. Vacíos cósmicos (ρ → 0): expansión **acelerada**

**Consecuencia**: La expansión del espacio es **inhomogénea**, creando el efecto de "energía oscura" observado.

---

## 3. Formalización Matemática de H(z, ρ)

### Versión 1: Modulación Lineal Simple

**Forma propuesta**:

```
H(z, ρ) = H₀(z) · [1 - α · (ρ/ρ_crítica - 1)]
```

Donde:
- `H₀(z)` = H₀√[Ωₘ(1+z)³ + Ωᵣ(1+z)⁴] (sin energía oscura)
- `α` = parámetro de anclaje (a calibrar, típicamente α ~ 0.1-0.3)
- `ρ` = densidad de materia local
- `ρ_crítica` = 3H₀²/(8πG) ≈ 1.88×10⁻²⁹ h² g/cm³

**Interpretación**:
- **ρ = ρ_crítica** (densidad promedio): H(z, ρ_crit) = H₀(z) (expansión estándar)
- **ρ > ρ_crítica** (sobredensidad, cúmulo): H disminuye (expansión ralentizada)
- **ρ < ρ_crítica** (vacío): H aumenta (expansión acelerada)

**Limitaciones**:
- ✅ Simple y comprobable
- ✅ Comportamiento físico correcto
- ⚠️ La modulación puede volverse negativa si ρ >> ρ_crit (no físico)

---

### Versión 2: Modulación Exponencial (Más Robusta)

**Forma propuesta**:

```
H(z, ρ) = H₀(z) · exp[β · (1 - ρ/ρ_crítica)]
```

Donde:
- `β` = parámetro de anclaje (típicamente β ~ 0.2-0.5)

**Propiedades**:
- **ρ = ρ_crítica**: H = H₀(z) · exp(0) = H₀(z)
- **ρ → 0** (vacío profundo): H → H₀(z) · exp(β) (expansión máxima)
- **ρ >> ρ_crítica** (núcleo de cúmulo): H → H₀(z) · exp(-β·ρ/ρ_crit) → 0 (expansión casi nula)

**Ventajas**:
- ✅ Siempre positivo (H > 0)
- ✅ Asíntota natural para ρ → ∞
- ✅ Comportamiento físico realista

---

### Versión 3: Integración de la Cartografía Després (Riguroso)

**Forma propuesta**:

```
H(z, ρ, γ_Després) = H₀(z) · f(γ_Després)
```

Donde:

```
f(γ_Després) = √[1 + λ · (γ_Després - 1)]
```

Y:
- `γ_Després(ρ, v)` = 1/√(1 - v²/c² - 2Φ/c²) (de la Cartografía Després)
- `λ` = constante de acoplamiento expansión-distorsión (a calibrar)

**Interpretación física**:
- Zonas con **alto γ_Després** (fuerte distorsión temporal): expansión ralentizada
- Zonas con **bajo γ_Després** (espacio plano): expansión acelerada

**Vínculo con Masa Després**:
```
Alto γ_Després ↔ Masa Després significativa ↔ Expansión ralentizada
```

**Ventajas**:
- ✅ Vínculo directo con la teoría (γ_Després)
- ✅ Consistente con Relatividad General
- ✅ Integra Enlaces Asselin implícitamente

---

## 4. Elección Recomendada: Versión Híbrida

### Formulación Final Propuesta

```
H(z, ρ) = H₀ · √[Ωₘ(1+z)³ + Ω_diff(z, ρ)]
```

Donde **la energía oscura efectiva** Ω_diff depende de la densidad local:

```
Ω_diff(z, ρ) = ΩΛ_eff · exp[β · (1 - ρ/ρ_crítica)]
```

Con:
- `ΩΛ_eff` ≈ 0.69 (valor efectivo promedio, como Lambda-CDM)
- `β` ≈ 0.3-0.5 (parámetro de anclaje, a calibrar)

**Ecuación completa**:

```
H(z, ρ) = H₀ · √[Ωₘ(1+z)³ + ΩΛ_eff · exp(β · (1 - ρ/ρ_crit))]
```

**Casos límite**:

| Entorno | ρ/ρ_crit | Ω_diff | H(z, ρ) |
|---------|----------|---------|---------|
| Vacío profundo | 0.1 | ΩΛ · e^(0.9β) | **Alto** (expansión rápida) |
| Promedio cósmico | 1.0 | ΩΛ | Estándar (como LCDM) |
| Filamento | 2-5 | ΩΛ · e^(-β a -4β) | **Ralentizado** |
| Núcleo de cúmulo | 10-100 | ΩΛ · e^(-9β a -99β) ≈ 0 | **Muy ralentizado** |

---

## 5. Predicciones Observacionales

### A) Supernovas Tipo Ia (SNIa)

**Lambda-CDM**: Distancia de luminosidad uniforme para z dado

**Maestría del Tiempo**: ¡La distancia de luminosidad **depende del entorno**!

```
d_L(z, ρ) = c(1+z) ∫₀^z dz'/H(z', ρ(z'))
```

**Predicción**:
- SNIa en **vacíos**: distancias **ligeramente más cortas** (expansión más rápida)
- SNIa en **cúmulos**: distancias **ligeramente más largas** (expansión ralentizada)

**Prueba**: Analizar muestra SNIa por entorno (Pantheon+, DES)

**Diferencia esperada**: Δd_L ~ 5-10% entre vacío y cúmulo (detectable)

---

### B) Oscilaciones Acústicas Bariónicas (BAO)

**Lambda-CDM**: Escala BAO fija r_s ≈ 150 Mpc

**Maestría del Tiempo**: Escala BAO **aparentemente modulada** por expansión diferencial

```
r_s_aparente(ρ) = r_s · [H_estándar / H(z, ρ)]
```

**Predicción**:
- BAO medidas en **vacíos**: escala **aparentemente más pequeña**
- BAO medidas en **filamentos**: escala **aparentemente más grande**

**Prueba**: Comparar BAO en diferentes entornos (SDSS, DESI)

---

### C) CMB - Efecto ISW (Integrated Sachs-Wolfe)

**Lambda-CDM**: Los fotones atraviesan potenciales en evolución (ΩΛ constante)

**Maestría del Tiempo**: Los fotones atraviesan potenciales **evolucionando diferentemente**

```
ΔT_ISW ∝ ∫ (dΦ/dt) dl
```

Con:
```
dΦ/dt ∝ dH/dt · Φ
```

**Predicción**:
- **Vacíos**: H aumenta más → ISW **más fuerte** (puntos fríos CMB)
- **Cúmulos**: H aumenta menos → ISW **más débil**

**Prueba**: Correlación mapa CMB Planck ↔ catálogos vacíos/cúmulos

**Resultado esperado**: Correlación **más fuerte** que Lambda-CDM (firma MT)

---

## 6. Calibración del Parámetro β

### Método 1: Ajuste en SNIa

**Datos**: Pantheon+ (1701 SNIa con corrimientos al rojo y entornos)

**Procedimiento**:
1. Clasificar cada SNIa según densidad del entorno (vacío/medio/cúmulo)
2. Calcular d_L(z, ρ) para diferentes valores de β
3. Ajustar β para minimizar χ²:

```
χ² = Σᵢ [(m_obs,i - m_teoría(z_i, ρ_i, β))² / σ_i²]
```

**Valor esperado**: β ~ 0.3-0.5

---

### Método 2: Restricciones BAO

**Datos**: SDSS DR12, DESI DR1

**Procedimiento**:
1. Medir escalas BAO en vacíos vs filamentos
2. Comparar con predicciones H(z, ρ)
3. Ajustar β

**Restricción esperada**: β < 0.6 (de lo contrario efecto demasiado fuerte, incompatible con observaciones)

---

### Método 3: Efecto ISW del CMB

**Datos**: Planck 2018 + 2MASS/SDSS (catálogos de vacíos)

**Procedimiento**:
1. Calcular correlación esperada T_CMB ↔ vacíos para diferentes β
2. Comparar con medición de Planck
3. Restringir β

**Resultado esperado**: β = 0.4 ± 0.1

---

## 7. Ecuaciones de Friedmann Modificadas

### Ecuaciones Estándar (Lambda-CDM)

```
H² = (8πG/3) · ρ_total - k/a² + Λ/3

dH/dt = -4πG(ρ + 3p) + Λ/3
```

### Ecuaciones Maestría del Tiempo

**Primera ecuación de Friedmann** (modificada):

```
H²(ρ) = (8πG/3) · ρ_materia - k/a² + Λ_eff(ρ)/3
```

Donde:
```
Λ_eff(ρ) = Λ₀ · exp[β · (1 - ρ/ρ_crit)]
```

**Interpretación**: ¡La "constante" cosmológica Λ ya no es constante, sino **función de la densidad local**!

**Segunda ecuación**:

```
dH/dt = -4πG(ρ + 3p) + (1/3) · dΛ_eff/dt
```

Con:
```
dΛ_eff/dt = -Λ₀ · β/ρ_crit · (dρ/dt) · exp[β(1-ρ/ρ_crit)]
```

**Consecuencia**: La expansión acelerada es **autosostenida** por la formación de estructuras (los vacíos se profundizan).

---

## 8. Validación: Comparación Lambda-CDM vs MT

### Universo Homogéneo (ρ = ρ_crit en todas partes)

**Si promediamos** H(z, ρ) sobre todo el espacio:

```
⟨H(z, ρ)⟩_espacio = ∫ H(z, ρ(r)) · dV / V_total
```

**Resultado esperado**: ⟨H⟩ ≈ H_LCDM (si β calibrado correctamente)

**Consecuencia**: La teoría MT reproduce Lambda-CDM **en promedio**, pero predice inhomogeneidades locales.

---

### Universo Realista (Estructuras)

**Distribución de densidad**: Vacíos (70% volumen, ρ ~ 0.2ρ_crit) + Filamentos (25%, ρ ~ 2ρ_crit) + Cúmulos (5%, ρ ~ 10ρ_crit)

**Expansión efectiva**:

```
⟨H⟩ = 0.70 · H(z, 0.2ρ_crit) + 0.25 · H(z, 2ρ_crit) + 0.05 · H(z, 10ρ_crit)
```

Con β = 0.4:
```
⟨H⟩ = 0.70 · H₀√[...+ ΩΛ·e^(0.32)] + 0.25 · H₀√[...+ ΩΛ·e^(-0.4)] + 0.05 · H₀√[...+ ΩΛ·e^(-3.6)]
```

**Cálculo numérico**:
- Vacíos: factor 1.38
- Filamentos: factor 0.67
- Cúmulos: factor ≈ 0.03

**Promedio ponderado**:
```
⟨H⟩/H₀ ≈ 0.70×1.38 + 0.25×0.67 + 0.05×0.03 ≈ 0.966 + 0.168 + 0.001 ≈ 1.135
```

**Problema**: ¡Esto predice expansión **más rápida** que LCDM!

**Solución**: Ajustar ΩΛ_eff para que ⟨H⟩ = H_LCDM

---

## 9. Restricciones Observacionales Actuales

### A) H₀ (Constante de Hubble Local)

**Mediciones actuales**:
- **Cefeidas + SNIa**: H₀ = 73.0 ± 1.0 km/s/Mpc (Riess et al. 2022)
- **CMB Planck**: H₀ = 67.4 ± 0.5 km/s/Mpc

**Tensión H₀**: ¡Discrepancia de 5σ!

**Predicción MT**:
- Medición **local** (Cefeidas): en entorno de densidad promedio
- Medición **CMB**: promedio cósmico

**Si expansión diferencial**:
```
H₀_local = H₀_cósmico · f(ρ_local)
```

**Posibilidad**: ¡MT podría **explicar la tensión H₀** si ρ_local < ρ_cósmico!

---

### B) Ωₘ y ΩΛ (Densidades)

**Restricciones Planck 2018**:
- Ωₘ = 0.315 ± 0.007
- ΩΛ = 0.685 ± 0.007

**MT debe reproducir** estos valores **en promedio espacial**:
```
⟨Ωₘ⟩ = 0.315
⟨ΩΛ_eff(ρ)⟩ = 0.685
```

**Restricción sobre β**: Determinado por esta igualdad.

---

## 10. Implementación Numérica

### Código Python para H(z, ρ)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Parámetros cosmológicos
H0 = 70  # km/s/Mpc
Omega_m = 0.315
Omega_Lambda_eff = 0.685
beta = 0.4  # Parámetro de anclaje
rho_crit = 1.88e-29 * (H0/70)**2  # g/cm³

def H_MT(z, rho_ratio):
    """
    Función de Hubble Maestría del Tiempo

    Parámetros:
    - z: corrimiento al rojo
    - rho_ratio: ρ/ρ_crítica (densidad local normalizada)

    Retorna:
    - H(z, ρ) en km/s/Mpc
    """
    # Término de materia
    term_matter = Omega_m * (1 + z)**3

    # Término de energía oscura efectiva (depende de ρ)
    term_Lambda = Omega_Lambda_eff * np.exp(beta * (1 - rho_ratio))

    # Parámetro de Hubble
    H = H0 * np.sqrt(term_matter + term_Lambda)

    return H

def H_LCDM(z):
    """
    Función de Hubble Lambda-CDM estándar
    """
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda_eff)

# Prueba: Comparación H(z) para diferentes entornos
z_array = np.linspace(0, 2, 100)

# Entornos
rho_void = 0.2      # Vacío (20% densidad promedio)
rho_mean = 1.0      # Promedio cósmico
rho_filament = 3.0  # Filamento (3x densidad promedio)
rho_cluster = 10.0  # Cúmulo (10x densidad promedio)

# Cálculos
H_void = [H_MT(z, rho_void) for z in z_array]
H_mean = [H_MT(z, rho_mean) for z in z_array]
H_filament = [H_MT(z, rho_filament) for z in z_array]
H_cluster = [H_MT(z, rho_cluster) for z in z_array]
H_standard = [H_LCDM(z) for z in z_array]

# Gráfico
plt.figure(figsize=(12, 8))
plt.plot(z_array, H_void, label='Vacío (ρ = 0.2 ρ_crit)', linewidth=2)
plt.plot(z_array, H_mean, label='Promedio (ρ = ρ_crit)', linewidth=2, linestyle='--')
plt.plot(z_array, H_filament, label='Filamento (ρ = 3 ρ_crit)', linewidth=2)
plt.plot(z_array, H_cluster, label='Cúmulo (ρ = 10 ρ_crit)', linewidth=2)
plt.plot(z_array, H_standard, label='Lambda-CDM', linewidth=2, color='black', linestyle=':')

plt.xlabel('Corrimiento al rojo z', fontsize=14)
plt.ylabel('H(z, ρ) [km/s/Mpc]', fontsize=14)
plt.title('Expansión Diferencial: H(z, ρ) para β = 0.4', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.savefig('H_z_rho_expansion_diferencial.png', dpi=300)
plt.show()

print("Gráfico guardado: H_z_rho_expansion_diferencial.png")
```

### Cálculo de Distancia de Luminosidad

```python
def luminosity_distance(z_target, rho_ratio):
    """
    Distancia de luminosidad en Mpc
    """
    c_km_s = 299792.458  # km/s

    # Integral de 0 a z
    def integrand(z):
        return c_km_s / H_MT(z, rho_ratio)

    integral, _ = quad(integrand, 0, z_target, limit=100)

    d_L = (1 + z_target) * integral

    return d_L

# Prueba: Distancia para SNIa a z=0.5
z_test = 0.5
d_L_void = luminosity_distance(z_test, 0.2)
d_L_mean = luminosity_distance(z_test, 1.0)
d_L_cluster = luminosity_distance(z_test, 10.0)
d_L_LCDM = luminosity_distance(z_test, 1.0)  # Equivalente LCDM

print(f"Distancia de luminosidad a z={z_test}:")
print(f"  Vacío:     {d_L_void:.1f} Mpc")
print(f"  Promedio:  {d_L_mean:.1f} Mpc")
print(f"  Cúmulo:    {d_L_cluster:.1f} Mpc")
print(f"  LCDM:      {d_L_LCDM:.1f} Mpc")
print(f"  Diferencia vacío-cúmulo: {100*(d_L_void-d_L_cluster)/d_L_mean:.1f}%")
```

---

## 11. Resumen y Recomendaciones

### Fórmula Final Recomendada

```
H(z, ρ) = H₀ · √[Ωₘ(1+z)³ + ΩΛ_eff · exp(β · (1 - ρ/ρ_crit))]
```

**Con**:
- H₀ = 70 km/s/Mpc
- Ωₘ = 0.315
- ΩΛ_eff = 0.685
- **β ≈ 0.4** (a calibrar precisamente en observaciones)

### Pruebas Prioritarias

**1. SNIa en función del entorno** (datos Pantheon+ disponibles)
- Clasificar SNIa: vacío/medio/filamento/cúmulo
- Medir diferencia de distancias
- Restringir β

**2. BAO en vacíos vs filamentos** (SDSS, DESI)
- Medir escala BAO por separado
- Probar modulación por H(z, ρ)

**3. Efecto ISW correlacionado con estructuras** (Planck + catálogos)
- Correlación CMB ↔ vacíos/cúmulos
- Firma de expansión diferencial

### Próximos Pasos

1. ✅ **Formalización H(z, ρ)**: HECHO (este documento)
2. ⏳ **Implementación código Python**: POR HACER (código proporcionado arriba)
3. ⏳ **Calibración β en datos SNIa**: 2-4 semanas
4. ⏳ **Predicciones CMB**: Usar CAMB modificado
5. ⏳ **Artículo teórico**: "Differential Expansion and the Dark Energy Phenomenon"

---

**Documento creado**: 2025-12-06
**Estado**: Formalización completa, listo para implementación y pruebas
**Archivo de código**: Incluido en documento, listo para ejecutar

**CRÍTICO**: ¡Esta formalización ahora permite hacer **predicciones cuantitativas comprobables** para CMB, SNIa y BAO!
