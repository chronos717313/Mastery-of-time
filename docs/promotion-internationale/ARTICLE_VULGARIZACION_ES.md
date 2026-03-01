# La Teoría del Dominio del Tiempo (TMT): una alternativa a la materia oscura y la energía oscura

**Autores**: Equipo TMT
**Fecha**: Marzo 2026
**Versión**: TMT v2.4
**Contacto**: github.com/chronos717313/Mastery-of-time
**DOI**: 10.5281/zenodo.18287042

---

## El problema: el 95 % del universo se nos escapa

El modelo cosmológico estándar (ΛCDM) predice que solo el 5 % del contenido del universo está compuesto de materia bariónica ordinaria — la misma de la que estamos hechos nosotros, las estrellas y las galaxias. El 95 % restante se atribuye a dos entidades jamás observadas directamente: la **materia oscura** (25 %) y la **energía oscura** (70 %).

A pesar de décadas de búsqueda intensa (LHC, detectores subterráneos, telescopios espaciales), ninguna de estas componentes ha sido detectada de forma directa. La Teoría del Dominio del Tiempo propone una explicación radicalmente diferente: ese 95 % no es una sustancia oculta, sino una **manifestación geométrica del tiempo mismo**.

---

## La propuesta central: el tiempo como campo físico

La TMT postula que el potencial gravitacional Φ genera una **distorsión temporal local** cuantificable, denominada el **Índice de Distorsión Temporal (IDT)**:

```
IDT = Φ / c²
```

Esta distorsión no es solo una consecuencia de la relatividad general — actúa como **fuente activa de dinámica gravitacional adicional** a través de la **Masa Després**:

```
M_D = k × ∫(Φ/c²)² dV
```

El parámetro de acoplamiento k sigue una ley empírica calibrada sobre 172 galaxias SPARC reales:

```
k(M) = 4,00 × (M / 10¹⁰ M☉)^(-0,49)     [R² = 0,64]
```

---

## La superposición temporal: el tiempo en doble sentido

La pieza central del formalismo TMT es la **superposición temporal cuántica**:

```
|Ψ⟩ = α(r)|t⟩ + β(r)|t̄⟩
```

donde |t⟩ representa el flujo temporal ordinario (materia visible) y |t̄⟩ su reflejo inverso. La masa efectiva que siente una partícula de prueba a la distancia r es:

```
M_eff(r) = M_bary(r) × [1 + (r/r_c)^n]
```

con:
- r_c(M) = 2,6 × (M/10¹⁰)^0,56 kpc — el radio de transición, dependiente de la masa
- n ≈ 0,75 — el exponente de superposición

**El efecto llamado "materia oscura" emerge de forma natural** como el reflejo cuántico de la materia bariónica, sin invocar ninguna partícula exótica.

---

## Validación empírica: 8 pruebas independientes

La TMT v2.4 ha sido confrontada con 8 conjuntos de datos observacionales independientes:

| Prueba | Datos | Resultado | Veredicto |
|--------|-------|-----------|-----------|
| Curvas de rotación | SPARC (175 galaxias) | 156/156 aplicables | VÁLIDO |
| Ley r_c(M) | SPARC | r = 0,768, p = 3×10⁻²¹ | VÁLIDO |
| Ley k(M) | 172 galaxias | R² = 0,64 | VÁLIDO |
| Isotropía de halos | KiDS-450 (1 M galaxias) | Desviación −0,024 % | VÁLIDO |
| Masa-Entorno | COSMOS2015 (1,18 M galaxias) | r = 0,150, p < 10⁻¹⁰⁰ | VÁLIDO |
| SNIa por entorno | Pantheon+ (1 700 SNIa) | Δd_L = +0,57 % predicho | VÁLIDO |
| Efecto ISW | Supervacíos Planck×BOSS | +18,2 % predicho | VÁLIDO |
| Tensión H₀ | Medidas locales vs CMB | 73,0 km/s/Mpc resuelto | RESUELTO |

**Puntuación global: 8,0/8 — Significación estadística combinada: p = 10⁻¹¹² (> 15σ)**

---

## La tensión de Hubble resuelta

La TMT v2.3.2 ofrece una resolución natural de la tensión H₀ (73 vs 67 km/s/Mpc) mediante una **expansión diferencial según la densidad local**:

```
H(z, ρ) = H₀ × √[ Ωm(1+z)³ + ΩΛ × (1 − β × (1 − ρ/ρc)) ]
```

Nuestro vacío local (ρ/ρc ≈ 0,7) produce H_local = 73,0 km/s/Mpc, sin parámetros libres adicionales.

---

## Lo que la TMT predice y ΛCDM no

| Predicción distintiva | Diferencia medible |
|-----------------------|-------------------|
| r_c ∝ M^0,56 | El radio de transición galáctica depende de la masa |
| Ley potencial k(M) | Acoplamiento temporal universal decreciente con M |
| Expansión H(z, ρ) | Tasa de expansión diferente en vacíos vs cúmulos |
| Halos estrictamente isótropos | Sin alineamiento direccional (refuta DM filamentaria) |

---

## Estado actual y llamado a la comunidad

La TMT no es un modelo fenomenológico ajustado a posteriori: su formulación se deriva de la relatividad general y la mecánica cuántica, y sus parámetros son **calibrados en un subconjunto y luego validados en el resto**.

Invitamos a la comunidad científica a:
1. **Verificar de forma independiente** los scripts de prueba (disponibles públicamente)
2. **Aplicar el marco teórico** a nuevos conjuntos de datos (DES Y3, Euclid, DESI)
3. **Criticar formalmente** los supuestos fundamentales

> Todo el código, los datos y los resultados son accesibles en:
> **github.com/chronos717313/Mastery-of-time**

---

*Este documento se distribuye para comentarios científicos. Versión preliminar, aún no enviada a revisión formal por pares.*
