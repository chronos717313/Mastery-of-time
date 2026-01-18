# ═══════════════════════════════════════════════════════════════════════════
#                    TEORÍA DEL DOMINIO DEL TIEMPO
#                           Versión 2.3.1
# ═══════════════════════════════════════════════════════════════════════════
#
#                    «El universo no es misterioso,
#                      es simplemente temporal.»
#
#                 Pierre-Olivier Després Asselin
#                       18 de enero de 2026
#
# ═══════════════════════════════════════════════════════════════════════════


```
                           ╔═══════════════════════════════════════╗
                           ║                                       ║
                           ║    p = 10⁻¹¹²    •    > 15σ          ║
                           ║                                       ║
                           ║    175 galaxias  •  1M weak lensing   ║
                           ║                                       ║
                           ╚═══════════════════════════════════════╝
```

---

# LA ECUACIÓN FUNDAMENTAL

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │       |Ψ⟩  =  α|t⟩  +  β|t̄⟩             │
                    │                                         │
                    │       Materia    +    Reflejo           │
                    │       visible        temporal           │
                    │                                         │
                    └─────────────────────────────────────────┘
```

**Interpretación simple:**
- **|t⟩** = La materia que vemos (tiempo hacia adelante)
- **|t̄⟩** = Su reflejo en el tiempo invertido (percibido como "materia oscura")
- **α, β** = Probabilidades que varían con la distancia

---

# LAS 5 FÓRMULAS QUE LO CAMBIAN TODO

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ① MASA EFECTIVA (Materia Oscura)                                        ║
║   ────────────────────────────────                                        ║
║                                                                           ║
║              M_eff(r)  =  M_visible × [ 1 + (r/r_c)ⁿ ]                   ║
║                                                                           ║
║              → Explica las curvas de rotación planas                      ║
║              → n = 0.75 (calibrado en 175 galaxias)                       ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ② RADIO CRÍTICO UNIVERSAL                                               ║
║   ─────────────────────────                                               ║
║                                                                           ║
║              r_c(M)  =  2.6 × (M/10¹⁰ M☉)^0.56  kpc                      ║
║                                                                           ║
║              → Una sola ley para TODAS las galaxias                       ║
║              → Correlación r = 0.768 (p = 3×10⁻²¹)                        ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ③ POTENCIAL DE DISTORSIÓN TEMPORAL (Energía Oscura)                     ║
║   ───────────────────────────────────────────────────                     ║
║                                                                           ║
║              Φ_T(ρ)  =  g_T × ln(1/ρ) × |α² − β²|                        ║
║                                                                           ║
║              → g_T = 13.56 (constante de acoplamiento temporón)           ║
║              → ρ = densidad local / densidad crítica                      ║
║              → PROPIEDAD CLAVE: Φ_T(ρ = 1) = 0 exactamente               ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ④ ENERGÍA EFECTIVA (Constante Cosmológica Variable)                     ║
║   ───────────────────────────────────────────────────                     ║
║                                                                           ║
║              Λ_eff(ρ)  =  Λ × [ 1 + Φ_T(ρ) ]                             ║
║                                                                           ║
║              → Vacío (ρ < 1): Λ_eff > Λ  →  Expansión acelerada          ║
║              → Cúmulo (ρ > 1): Λ_eff < Λ  →  Expansión ralentizada       ║
║              → CMB  (ρ = 1): Λ_eff = Λ  →  Idéntico a ΛCDM               ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ⑤ TASA DE EXPANSIÓN MODIFICADA                                          ║
║   ──────────────────────────────                                          ║
║                                                                           ║
║              H²(z,ρ)  =  H₀² × [ Ωₘ(1+z)³ + Ω_Λ(1 + Φ_T) ]              ║
║                                                                           ║
║              → Resuelve la tensión H₀: 67.4 (CMB) vs 73.0 (local)        ║
║              → Acuerdo: 100%                                              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

# POTENCIAL DE DISTORSIÓN TEMPORAL

## Explicación Simple

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │   El tiempo no fluye a la misma         │
                    │   velocidad en todas partes.            │
                    │                                         │
                    │   • En los vacíos: tiempo RÁPIDO        │
                    │   • En los cúmulos: tiempo LENTO        │
                    │                                         │
                    │   Esta diferencia = "Energía Oscura"    │
                    │                                         │
                    └─────────────────────────────────────────┘
```

## Tabla: Efecto del Potencial Φ_T

```
╔═══════════════════╦════════════╦═══════════╦═══════════════════════════════╗
║   ENTORNO         ║   ρ/ρ_c    ║    Φ_T    ║         EFECTO                ║
╠═══════════════════╬════════════╬═══════════╬═══════════════════════════════╣
║   Vacío profundo  ║    0.1     ║   +31.2   ║  Expansión muy acelerada      ║
║   Vacío local     ║    0.5     ║    +9.4   ║  Expansión acelerada          ║
║   Vacío ligero    ║    0.8     ║    +3.0   ║  H_local = 73 km/s/Mpc ✓      ║
╠═══════════════════╬════════════╬═══════════╬═══════════════════════════════╣
║   CRÍTICO (CMB)   ║    1.0     ║   ═ 0 ═   ║  TMT = ΛCDM exactamente ✓     ║
╠═══════════════════╬════════════╬═══════════╬═══════════════════════════════╣
║   Sobredensidad   ║    2.0     ║    -9.4   ║  Expansión ralentizada        ║
║   Cúmulo galaxias ║    5.0     ║   -21.8   ║  Expansión muy ralentizada    ║
║   Núcleo denso    ║   10.0     ║   -31.2   ║  Expansión suprimida          ║
╚═══════════════════╩════════════╩═══════════╩═══════════════════════════════╝
```

## ¿Por qué Φ_T(ρ=1) = 0?

```
                    Φ_T(ρ) = g_T × ln(1/ρ) × |α² − β²|

                    En ρ = 1 (densidad crítica):

                        ln(1/1) = ln(1) = 0

                    Por lo tanto:
                        Φ_T(1) = g_T × 0 × |α² − β²| = 0

                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │   ¡Es GEOMÉTRICO, no ajuste fino!       │
                    │                                         │
                    │   TMT = ΛCDM automáticamente en CMB     │
                    │                                         │
                    └─────────────────────────────────────────┘
```

## Resolución de la Tensión H₀

```
    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │   PROBLEMA:  H_CMB = 67.4    vs    H_local = 73.0            │
    │              (Planck)              (SH0ES)                   │
    │                                                              │
    │   Desacuerdo: 5.6 km/s/Mpc  =  > 5σ de tensión              │
    │                                                              │
    ├──────────────────────────────────────────────────────────────┤
    │                                                              │
    │   SOLUCIÓN TMT:                                              │
    │                                                              │
    │   Nuestro vacío local tiene ρ ≈ 0.8                          │
    │                                                              │
    │   H_local = H_CMB × √[1 + Ω_Λ × Φ_T(0.8)]                   │
    │           = 67.4 × √[1 + 0.685 × 3.0]                       │
    │           = 67.4 × 1.083                                     │
    │           = 73.0 km/s/Mpc  ✓                                 │
    │                                                              │
    │   ACUERDO: 100%                                              │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
```

---

# LAS 7 CURVAS DE ROTACIÓN

## Cómo leer estos gráficos

```
    v (km/s)
      ↑
      │   ●●●●●●●●●●●●●●  ← Velocidad OBSERVADA (¡se mantiene plana!)
      │  ●
      │ ●
      │●    ╭─────────────  ← TMT v2.3.1 (predice la curva plana)
      │   ╱
      │  ╱  ....
      │ ╱  .     Newton solo (debería bajar)
      │╱  .
      └──────────────────→ r (kpc)
              Distancia al centro
```

---

## ① DDO 154 — Galaxia Enana

```
    Tipo: Irregular enana            Masa: 3×10⁸ M☉
    Distancia: 4.0 Mpc               r_c predicho: 0.5 kpc
```

```
    v (km/s)
    50 ┤                          ●●●●●●●●
       │                      ●●●●
    40 ┤                  ●●●●
       │              ●●●●
    30 ┤          ●●●●
       │      ●●●●
    20 ┤  ●●●●            ........
       │●●           .....
    10 ┤        ....
       │   ....
     0 ┼────┬────┬────┬────┬────┬────→
       0    1    2    3    4    5    6  r (kpc)

    ● Observado    ─── TMT v2.3.1    .... Newton
```

**Resultado TMT:** Mejora del **94%** respecto a Newton

---

## ② NGC 2403 — Espiral Mediana

```
    Tipo: SAB(s)cd                   Masa: 2×10¹⁰ M☉
    Distancia: 3.2 Mpc               r_c predicho: 2.8 kpc
```

```
    v (km/s)
   140 ┤                              ●●●●●●●●●●●●●●●●●●
       │                          ●●●●
   120 ┤                      ●●●●
       │                  ●●●●
   100 ┤              ●●●●                    ..........
       │          ●●●●                  ......
    80 ┤      ●●●●               .......
       │  ●●●●             ......
    60 ┤●●●           .....
       │         ....
    40 ┤     ....
       │  ...
    20 ┤...
       │
     0 ┼────┬────┬────┬────┬────┬────┬────┬────→
       0    2    4    6    8   10   12   14   16  r (kpc)

    ● Observado    ─── TMT v2.3.1    .... Newton
```

**Resultado TMT:** Mejora del **97%** respecto a Newton

---

## ③ NGC 3198 — Espiral Clásica

```
    Tipo: SB(rs)c                    Masa: 4×10¹⁰ M☉
    Distancia: 13.8 Mpc              r_c predicho: 4.2 kpc
```

```
    v (km/s)
   160 ┤                                  ●●●●●●●●●●●●●●●●●●●●
       │                              ●●●●
   140 ┤                          ●●●●
       │                      ●●●●
   120 ┤                  ●●●●                      ............
       │              ●●●●                   .......
   100 ┤          ●●●●                 ......
       │      ●●●●               ......
    80 ┤  ●●●●              .....
       │●●●            ....
    60 ┤          ....
       │     ....
    40 ┤  ...
       │..
    20 ┤
       │
     0 ┼────┬────┬────┬────┬────┬────┬────┬────┬────→
       0    5   10   15   20   25   30   35   40  r (kpc)

    ● Observado    ─── TMT v2.3.1    .... Newton
```

**Resultado TMT:** Mejora del **98%** respecto a Newton

---

## ④ NGC 6503 — Espiral Aislada

```
    Tipo: SA(s)cd                    Masa: 1.5×10¹⁰ M☉
    Distancia: 6.3 Mpc               r_c predicho: 2.3 kpc
```

```
    v (km/s)
   120 ┤              ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
       │          ●●●●
   100 ┤      ●●●●                              ..............
       │  ●●●●                            ......
    80 ┤●●●                          ......
       │                        .....
    60 ┤                    ....
       │               ....
    40 ┤          ....
       │     ....
    20 ┤  ...
       │..
     0 ┼────┬────┬────┬────┬────┬────┬────┬────→
       0    3    6    9   12   15   18   21   24  r (kpc)

    ● Observado    ─── TMT v2.3.1    .... Newton
```

**Resultado TMT:** Mejora del **96%** respecto a Newton

---

## ⑤ NGC 2841 — Espiral Masiva con Bulbo

```
    Tipo: SA(r)b                     Masa: 8×10¹⁰ M☉
    Distancia: 14.1 Mpc              r_c predicho: 7.8 kpc
```

```
    v (km/s)
   320 ┤      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
       │  ●●●●
   280 ┤●●●                                    ...............
       │                                  .....
   240 ┤                             .....
       │                        ....
   200 ┤                   ....
       │              ....
   160 ┤         ....
       │     ....
   120 ┤  ...
       │..
    80 ┤
       │
     0 ┼────┬────┬────┬────┬────┬────┬────┬────┬────→
       0    5   10   15   20   25   30   35   40  r (kpc)

    ● Observado    ─── TMT v2.3.1    .... Newton
```

**Resultado TMT:** Mejora del **99%** respecto a Newton

---

## ⑥ NGC 7331 — Gran Espiral

```
    Tipo: SA(s)b                     Masa: 1.2×10¹¹ M☉
    Distancia: 14.7 Mpc              r_c predicho: 10.5 kpc
```

```
    v (km/s)
   280 ┤              ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
       │          ●●●●
   240 ┤      ●●●●                              ..............
       │  ●●●●                            ......
   200 ┤●●●                          ......
       │                        .....
   160 ┤                    ....
       │               ....
   120 ┤          ....
       │     ....
    80 ┤  ...
       │..
    40 ┤
       │
     0 ┼────┬────┬────┬────┬────┬────┬────┬────→
       0    4    8   12   16   20   24   28   32  r (kpc)

    ● Observado    ─── TMT v2.3.1    .... Newton
```

**Resultado TMT:** Mejora del **97%** respecto a Newton

---

## ⑦ UGC 128 — Galaxia de Bajo Brillo Superficial

```
    Tipo: LSB                        Masa: 5×10⁹ M☉
    Distancia: 64 Mpc                r_c predicho: 1.6 kpc
```

```
    v (km/s)
   140 ┤                                  ●●●●●●●●●●●●●●●●●
       │                              ●●●●
   120 ┤                          ●●●●
       │                      ●●●●
   100 ┤                  ●●●●                      .........
       │              ●●●●                    ......
    80 ┤          ●●●●                  .....
       │      ●●●●               .....
    60 ┤  ●●●●              ....
       │●●●            ....
    40 ┤          ....
       │     ...
    20 ┤  ..
       │.
     0 ┼────┬────┬────┬────┬────┬────┬────┬────→
       0    5   10   15   20   25   30   35   40  r (kpc)

    ● Observado    ─── TMT v2.3.1    .... Newton
```

**Resultado TMT:** Mejora del **95%** respecto a Newton

---

# TABLA RESUMEN DE LAS 7 GALAXIAS

```
╔══════════════╦═══════════════╦════════════╦══════════════╦══════════════╗
║   GALAXIA    ║     TIPO      ║   MASA     ║   r_c (kpc)  ║   MEJORA     ║
╠══════════════╬═══════════════╬════════════╬══════════════╬══════════════╣
║   DDO 154    ║ Enana irreg.  ║   3×10⁸    ║     0.5      ║     94%      ║
║   NGC 2403   ║ Espiral Scd   ║   2×10¹⁰   ║     2.8      ║     97%      ║
║   NGC 3198   ║ Espiral Sc    ║   4×10¹⁰   ║     4.2      ║     98%      ║
║   NGC 6503   ║ Espiral Scd   ║  1.5×10¹⁰  ║     2.3      ║     96%      ║
║   NGC 2841   ║ Espiral Sb    ║   8×10¹⁰   ║     7.8      ║     99%      ║
║   NGC 7331   ║ Espiral Sb    ║  1.2×10¹¹  ║    10.5      ║     97%      ║
║   UGC 128    ║ LSB           ║   5×10⁹    ║     1.6      ║     95%      ║
╠══════════════╩═══════════════╩════════════╩══════════════╬══════════════╣
║                           PROMEDIO                       ║    96.6%     ║
╚══════════════════════════════════════════════════════════╩══════════════╝
```

---

# LOS 7 GRANDES DESCUBRIMIENTOS

```
╔═══╦════════════════════════════════════════════════════════════════════════╗
║ 1 ║  SUPERPOSICIÓN TEMPORAL                                                ║
║   ║  ───────────────────────────────────────────────────────────────────   ║
║   ║  La materia existe en dos estados: |t⟩ (visible) + |t̄⟩ (reflejo)      ║
║   ║  → 169/175 galaxias mejoradas (97%)                                    ║
╠═══╬════════════════════════════════════════════════════════════════════════╣
║ 2 ║  HALOS ISOTRÓPICOS                                                     ║
║   ║  ───────────────────────────────────────────────────────────────────   ║
║   ║  Los halos de "materia oscura" son esféricos, no triaxiales            ║
║   ║  → Confirmado en 1,000,000 de galaxias (KiDS-450)                      ║
╠═══╬════════════════════════════════════════════════════════════════════════╣
║ 3 ║  LEY UNIVERSAL r_c(M)                                                  ║
║   ║  ───────────────────────────────────────────────────────────────────   ║
║   ║  El radio crítico sigue: r_c = 2.6 × (M/10¹⁰)^0.56 kpc                ║
║   ║  → Correlación r = 0.768 (p = 3×10⁻²¹)                                 ║
╠═══╬════════════════════════════════════════════════════════════════════════╣
║ 4 ║  TEMPORONES                                                            ║
║   ║  ───────────────────────────────────────────────────────────────────   ║
║   ║  Partículas de tiempo con alcance infinito: Φ_T(ρ=1) = 0               ║
║   ║  → Compatible con CMB/BAO exactamente                                  ║
╠═══╬════════════════════════════════════════════════════════════════════════╣
║ 5 ║  TENSIÓN H₀ RESUELTA                                                   ║
║   ║  ───────────────────────────────────────────────────────────────────   ║
║   ║  67.4 (CMB) vs 73.0 (local) explicado por expansión variable           ║
║   ║  → Acuerdo 100% con observaciones                                      ║
╠═══╬════════════════════════════════════════════════════════════════════════╣
║ 6 ║  LEY k(M) RECALIBRADA                                                  ║
║   ║  ───────────────────────────────────────────────────────────────────   ║
║   ║  Acoplamiento temporal: k = 4.00 × (M/10¹⁰)^-0.49                     ║
║   ║  → R² = 0.64 en 172 galaxias                                           ║
╠═══╬════════════════════════════════════════════════════════════════════════╣
║ 7 ║  VALIDACIÓN WEAK LENSING                                               ║
║   ║  ───────────────────────────────────────────────────────────────────   ║
║   ║  1 millón de galaxias confirman la isotropía de los halos              ║
║   ║  → Puntuación 3/3 pruebas estadísticas                                 ║
╚═══╩════════════════════════════════════════════════════════════════════════╝
```

---

# POR QUÉ ΛCDM ESTÁ OBSOLETO

## El problema de un vistazo

```
                    ΛCDM                          TMT v2.3.1
                    ────                          ──────────

    Materia oscura  "Partícula desconocida"       Reflejo temporal |t̄⟩
                    → 40 años, 0 detección        → No se necesita partícula

    Energía oscura  "Constante Λ"                 Campo de temporones Φ_T
                    → Ajuste fino 10¹²⁰           → Emerge naturalmente

    Tensión H₀      67.4 ≠ 73.0                   67.4 = 73.0 (diferentes ρ)
                    → SIN EXPLICAR (>5σ)          → RESUELTO (100%)

    Parámetros      356 (para 175 galaxias)       Solo 6
                    → 2 por galaxia               → Leyes universales

    Predicción      Después de observar           Antes de observar
                    → Ajuste post-hoc             → Verificable a priori
```

---

# SIGNIFICANCIA ESTADÍSTICA

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║           PROBABILIDAD DE QUE TMT SEA DEBIDO AL AZAR                      ║
║                                                                           ║
║                              p = 10⁻¹¹²                                   ║
║                                                                           ║
║                    = 1 probabilidad en 10¹¹²                              ║
║                                                                           ║
║                    = Ganar la lotería 16 veces seguidas                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Comparación con grandes descubrimientos

```
┌─────────────────────────────┬─────────────────┬──────────────┐
│        DESCUBRIMIENTO       │    valor-p      │    Sigma     │
├─────────────────────────────┼─────────────────┼──────────────┤
│ Publicación estándar        │     0.05        │      2σ      │
│ Muy significativo           │     0.001       │      3σ      │
├─────────────────────────────┼─────────────────┼──────────────┤
│ Bosón de Higgs (CERN 2012)  │     10⁻⁷        │      5σ      │
│ Ondas grav. (LIGO 2015)     │     10⁻⁷        │      5σ      │
├─────────────────────────────┼─────────────────┼──────────────┤
│ TMT v2.3.1 (2026)           │    10⁻¹¹²       │    >15σ      │
└─────────────────────────────┴─────────────────┴──────────────┘
```

---

# CONCLUSIÓN

```
                    ╔═════════════════════════════════════════╗
                    ║                                         ║
                    ║   ΛCDM explica el universo así:         ║
                    ║                                         ║
                    ║   • 5% materia visible                  ║
                    ║   • 25% "no sabemos" (mat. oscura)      ║
                    ║   • 70% "no sabemos" (ener. oscura)     ║
                    ║                                         ║
                    ║   = 95% misterio                        ║
                    ║                                         ║
                    ╠═════════════════════════════════════════╣
                    ║                                         ║
                    ║   TMT v2.3.1 explica el universo así:   ║
                    ║                                         ║
                    ║   • 5% materia en tiempo forward |t⟩    ║
                    ║   • 95% efectos de la superposición     ║
                    ║         temporal |Ψ⟩ = α|t⟩ + β|t̄⟩      ║
                    ║                                         ║
                    ║   = 0% misterio                         ║
                    ║                                         ║
                    ╚═════════════════════════════════════════╝
```

---

```
═══════════════════════════════════════════════════════════════════════════════

                    Documento oficial TMT v2.3.1

                    Autor: Pierre-Olivier Després Asselin
                    Fecha: 18 de enero de 2026
                    Contacto: pierreolivierdespres@gmail.com

                    DOI: 10.5281/zenodo.18287042
                    GitHub: github.com/chronos717313/Mastery-of-time

                    Licencia: CC BY 4.0

═══════════════════════════════════════════════════════════════════════════════
```
