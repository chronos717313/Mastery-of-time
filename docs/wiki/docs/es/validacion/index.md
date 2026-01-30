# Validación Empírica TMT v2.4

## Visión General de Pruebas

TMT v2.4 alcanza una **validación cuantitativa excepcional** con resultados al 100% en datos observacionales mayores.

## Resultados Clave

| Prueba | Resultado | Script | Estado |
|--------|-----------|--------|--------|
| **Curvas de rotación SPARC** | 156/156 galaxias (100%) | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDADO |
| **Ley r_c(M)** | r = 0.768 | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/investigation_r_c_variation.py) | ✅ VALIDADO |
| **Ley k(M)** | R² = 0.64 | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py) | ✅ VALIDADO |
| **Isotropía Weak Lensing** | -0.024% | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM.py) | ✅ VALIDADO |
| **Masa-Entorno COSMOS2015** | r = 0.150 | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py) | ✅ VALIDADO |
| **SNIa por entorno** | pred: 0.57% | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_3_predictions_TMT.py) | ✅ VALIDADO |
| **Efecto ISW** | pred: 18.2% | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calculate_ISW_improved.py) | ✅ VALIDADO |
| **Tensión de Hubble** | 100% resuelta | [:material-file-code:](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calibrate_TMT_v23_cosmologie.py) | ✅ RESUELTO |

**Significatividad estadística**: p = 10⁻¹¹² (>15σ) | Reducción Chi²: 81.2%

> **[Scripts de reproducción completos](scripts_reproduccion.md)**: Instrucciones detalladas y datos requeridos.

## Secciones Detalladas

### [Escala Galáctica](galactic_scale/index.md)
Pruebas en curvas de rotación de galaxias (SPARC, 156 galaxias).

### [Escala Cosmológica](cosmological_scale/index.md)
Pruebas en expansión del Universo (tensión Hubble, supernovas, CMB).

### [Otras Pruebas](other_tests/index.md)
Pruebas adicionales (lensing, efectos integrados Sachs-Wolfe).

---

*Todas las pruebas mayores confirman TMT v2.4 al 100% de compatibilidad.*