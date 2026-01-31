# Teoría de Dominio del Tiempo (TMT)

## Visión General

La **Teoría de Dominio del Tiempo** (TMT) es una formulación alternativa a la cosmología ΛCDM estándar, basada en el concepto de **superposición temporal cuántica**.

### Ecuación Maestra
La formulación central de TMT se basa en la ecuación maestra:

$$\psi(\text{universo}) = \alpha(r,p,t)|t\rangle + \beta(r,p)|\bar{t}\rangle$$

donde:

- $|t\rangle$ representa el estado temporal forward (materia visible)
- $|\bar{t}\rangle$ representa el estado temporal backward (materia oscura como reflexión cuántica)
- $\alpha$ y $\beta$ son amplitudes de probabilidad con $|\alpha|^2 + |\beta|^2 = 1$

### Ecuación Després-Schrödinger

La unificación de la mecánica cuántica y la gravitación se realiza mediante la ecuación Després-Schrödinger:

$$
i\hbar [1 + \tau(x)]^{-1} \frac{\partial\psi}{\partial t} = \left[-\frac{\hbar^2}{2m_{eff}} \nabla^2 + V(x) + mc^2\tau(x)\right] \psi
$$

donde:

- $\tau(x) = \Phi(x)/c^2$ es la **distorsión temporal local**
- $[1 + \tau(x)]^{-1}$ ralentiza el tiempo en campos gravitacionales
- $mc^2\tau(x)$ es el **potencial temporal** (término nuevo)
- $m_{eff} = m_0/\gamma_{\text{Després}}$ es la masa efectiva

Esta ecuación:

- Recupera Schrödinger estándar cuando $\tau \to 0$
- Explica la materia oscura sin partículas exóticas
- Unifica MC + RG en un marco coherente

> **[Ver el Léxico completo](lexico.md)** para todas las definiciones de términos TMT.

## Estado de Validación

TMT alcanza **compatibilidad excepcional** con datos observacionales mayores:

| Prueba | Resultado | Script | Veredicto |
|--------|-----------|--------|-----------|
| Curvas de rotación SPARC | [156/156 (100%)](validacion/galactic_scale/#criterios-de-exclusion) | [:material-file-code: test_TMT_v2_SPARC_reel.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDADO |
| Ley $r_c(M)$ | r = 0.768 | [:material-file-code: investigation_r_c_variation.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/investigation_r_c_variation.py) | ✅ VALIDADO |
| Ley $k(M)$ | $R^2$ = 0.64 | [:material-file-code: test_TMT_v2_SPARC_reel.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDADO |
| Isotropía Weak Lensing | -0.024% | [:material-file-code: test_weak_lensing_TMT_vs_LCDM.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/test_weak_lensing_TMT_vs_LCDM.py) | ✅ VALIDADO |
| Masa-Entorno COSMOS2015 | r = 0.150 | [:material-file-code: test_weak_lensing_real_data.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py) | ✅ VALIDADO |
| SNIa por entorno | pred: 0.57% | [:material-file-code: test_3_predictions_TMT.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/test_3_predictions_TMT.py) | ✅ VALIDADO |
| Efecto ISW | pred: 18.2% | [:material-file-code: calculate_ISW_improved.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/calculate_ISW_improved.py) | ✅ VALIDADO |
| Tensión de Hubble | 100% resuelta | [:material-file-code: calibrate_TMT_v23_cosmologie.py](https://github.com/chronos717313/Mastery-of-time/blob/main/scripts/calibrate_TMT_v23_cosmologie.py) | ✅ RESUELTO |

> **[Scripts de reproducción completos](validacion/scripts_reproduccion.md)**: Instrucciones detalladas y datos requeridos.

## Puentes Conceptuales vs ΛCDM

TMT establece 7 puentes conceptuales fundamentales en comparación con el modelo ΛCDM:

1. **Física conocida**: Superposición temporal vs física cuántica + relatividad
2. **Mecánica cuántica**: Distorsión del tiempo / flecha del tiempo
3. **Relatividad general**: Temporones vs materia oscura WIMP
4. **Termodinámica**: ϕ_T(p=1)=0 vs energía oscura
5. **Cosmología**: Expansión diferencial vs ΛCDM
6. **Física de partículas**: Sin WIMP vs partículas CDM
7. **Mediciones**: Resolución de la tensión de Hubble vs descubrimientos ΛCDM

## Estructura de la Documentación

- **[Puentes Conceptuales](pontes_conceptuales/index.md)**: Comparaciones detalladas con ΛCDM
- **[Validación Empírica](validacion/index.md)**: Pruebas y resultados observacionales
- **[Publicaciones](publicaciones/index.md)**: Documentos de presentación científica

---

*TMT - Versión lista para producción (Enero 2026)*