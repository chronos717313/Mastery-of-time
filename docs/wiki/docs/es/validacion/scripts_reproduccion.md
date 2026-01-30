# Scripts de Reproducción

Esta página proporciona todos los scripts Python necesarios para reproducir las 8 pruebas de validación de TMT v2.4.

## Requisitos Previos

### Instalación de dependencias

```bash
pip install numpy scipy matplotlib astropy
```

### Estructura de datos

```
Maitrise-du-temps/
├── data/
│   ├── sparc/
│   │   ├── SPARC_Lelli2016c.mrt
│   │   └── MassModels_Lelli2016c.mrt
│   └── Pantheon+/
│       └── Pantheon+SH0ES.dat
└── scripts/
    └── [scripts abajo]
```

---

## Tabla de Pruebas y Scripts

| Prueba | Resultado | Script | Datos |
|--------|-----------|--------|-------|
| [Curvas de rotación SPARC](#1-curvas-de-rotacion-sparc) | 156/156 (100%) | `test_TMT_v2_SPARC_reel.py` | SPARC |
| [Ley r_c(M)](#2-ley-rcm) | r = 0.768 | `investigation_r_c_variation.py` | SPARC |
| [Ley k(M)](#3-ley-km) | R² = 0.64 | `test_TMT_v2_SPARC_reel.py` | SPARC |
| [Isotropía Weak Lensing](#4-isotropia-weak-lensing) | -0.024% | `test_weak_lensing_TMT_vs_LCDM.py` | COSMOS |
| [COSMOS2015 Masa-Entorno](#5-cosmos2015-masa-entorno) | r = 0.150 | `test_weak_lensing_TMT_vs_LCDM_real_data.py` | COSMOS2015 |
| [SNIa por entorno](#6-snia-por-entorno) | pred: 0.57% | `test_3_predictions_TMT.py` | Pantheon+ |
| [Efecto ISW](#7-efecto-isw) | pred: 18.2% | `calculate_ISW_improved.py` | Planck |
| [Tensión de Hubble](#8-tension-de-hubble) | 100% resuelta | `calibrate_TMT_v23_cosmologie.py` | Planck+SH0ES |

---

## Fuentes de Datos

### SPARC (Incluido en el repositorio)

Los datos SPARC están incluidos en `data/sparc/`. Fuente original:

- **URL**: [http://astroweb.cwru.edu/SPARC/](http://astroweb.cwru.edu/SPARC/)
- **Referencia**: Lelli, McGaugh & Schombert (2016), AJ 152, 157
- **Archivos**:
    - `SPARC_Lelli2016c.mrt`: Propiedades de 175 galaxias
    - `MassModels_Lelli2016c.mrt`: Curvas de rotación

### Pantheon+ (Incluido en el repositorio)

Los datos Pantheon+ están incluidos en `data/Pantheon+/`. Fuente original:

- **URL**: [https://github.com/PantheonPlusSH0ES/DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease)
- **Referencia**: Scolnic et al. (2022), ApJ 938, 113
- **Archivo**: `Pantheon+SH0ES.dat` (1701 supernovas Tipo Ia)

### COSMOS2015 (Descarga externa)

- **URL**: [CDS VizieR](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/ApJS/224/24)
- **Referencia**: Laigle et al. (2016), ApJS 224, 24
- **Script auxiliar**: `scripts/download_cosmos_auto.py`

### Planck CMB (Datos públicos)

- **URL**: [Planck Legacy Archive](https://pla.esac.esa.int/)
- **Referencia**: Planck Collaboration (2020), A&A 641, A6

---

## Scripts Detallados

### 1. Curvas de Rotación SPARC

**Resultado**: 156/156 galaxias (100%) | **Archivo**: `test_TMT_v2_SPARC_reel.py`

Este script prueba la formulación TMT v2.0 en las 175 galaxias SPARC reales (156 retenidas después del filtrado de calidad).

**Ejecución**:
```bash
cd scripts
python test_TMT_v2_SPARC_reel.py
```

**Salida esperada**: `data/results/TMT_v2_SPARC_reel_results.txt`

??? note "Mostrar código fuente"
    ```python
    #!/usr/bin/env python3
    """
    Test TMT v2.0 con datos SPARC REALES (175 galaxias)
    Calibración de la ley k = a × (M/10^10)^b
    
    Datos: http://astroweb.cwru.edu/SPARC/
    Referencia: Lelli, McGaugh & Schombert (2016)
    """
    
    import numpy as np
    from scipy.optimize import minimize_scalar, curve_fit
    from pathlib import Path
    import warnings
    warnings.filterwarnings('ignore')
    
    # Constantes
    G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
    C_KMS = 299792.458  # km/s
    
    # Parámetros TMT v2.0
    R_C_DEFAULT = 18.0  # kpc - radio crítico calibrado
    N_DEFAULT = 1.6     # exponente calibrado
    
    # ... [Código completo disponible en GitHub]
    ```

[:material-download: Descargar script completo](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_TMT_v2_SPARC_reel.py){ .md-button }

---

### 2. Ley r_c(M)

**Resultado**: r = 0.768 (p < 10⁻²¹) | **Archivo**: `investigation_r_c_variation.py`

Este script analiza la dependencia del radio crítico r_c con la masa bariónica.

**Ejecución**:
```bash
cd scripts
python investigation_r_c_variation.py
```

**Relación descubierta**:
```
r_c(M) = 2.6 × (M_bary / 10¹⁰ M_☉)^0.56 kpc
```

??? note "Mostrar código fuente"
    ```python
    #!/usr/bin/env python3
    """
    INVESTIGACIÓN r_c: ¿Por qué 5 vs 10 vs 18 kpc?
    
    Análisis de diferentes valores de r_c obtenidos por diferentes métodos.
    Descubrimiento: ¡r_c depende de la masa bariónica!
    
    Autor: Pierre-Olivier Després Asselin
    Fecha: Enero 2026
    """
    
    import numpy as np
    from scipy.optimize import minimize
    from pathlib import Path
    
    # Constantes
    G_KPC = 4.302e-6  # kpc (km/s)² / M_sun
    
    # ... [Código completo disponible en GitHub]
    ```

[:material-download: Descargar script completo](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/investigation_r_c_variation.py){ .md-button }

---

### 3. Ley k(M)

**Resultado**: R² = 0.64 | **Archivo**: `test_TMT_v2_SPARC_reel.py`

La ley k(M) se calibra en el mismo script que las curvas de rotación.

**Ley calibrada**:
```
k = 3.97 × (M/10¹⁰)^(-0.48)
```

---

### 4. Isotropía Weak Lensing

**Resultado**: -0.024% | **Archivo**: `test_weak_lensing_TMT_vs_LCDM.py`

Este script prueba si los halos de materia oscura son isotrópicos (TMT v2.0) o alineados (TMT v1.0 refutado).

**Ejecución**:
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM.py
```

??? note "Mostrar código fuente"
    ```python
    #!/usr/bin/env python3
    """
    PRUEBA PRIMARIA: Halos Asimétricos - Predicción TMT vs ΛCDM
    
    PREDICCIÓN TMT v2.0 (ISOTRÓPICO):
      Los halos son esféricos, sin alineación preferencial.
      Correlación esperada: r ≈ 0.00 ± 0.05
    
    RESULTADO: r = -0.024% → TMT v2.0 VALIDADO (isotrópico)
    """
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import pearsonr, spearmanr
    
    # ... [Código completo disponible en GitHub]
    ```

[:material-download: Descargar script completo](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM.py){ .md-button }

---

### 5. COSMOS2015 Masa-Entorno

**Resultado**: r = 0.150 | **Archivo**: `test_weak_lensing_TMT_vs_LCDM_real_data.py`

Análisis de la correlación masa-entorno en datos reales COSMOS2015.

**Datos requeridos**: Descargar COSMOS2015 desde VizieR

**Ejecución**:
```bash
cd scripts
python test_weak_lensing_TMT_vs_LCDM_real_data.py
```

[:material-download: Descargar script completo](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_weak_lensing_TMT_vs_LCDM_real_data.py){ .md-button }

---

### 6. SNIa por Entorno

**Resultado**: pred: 0.57% | **Archivo**: `test_3_predictions_TMT.py`

Prueba de la expansión diferencial H(z,ρ) mediante supernovas Tipo Ia en diferentes entornos.

**Ejecución**:
```bash
cd scripts
python test_3_predictions_TMT.py
```

??? note "Mostrar código fuente"
    ```python
    #!/usr/bin/env python3
    """
    PRUEBA DE 3 PREDICCIONES DISTINTIVAS TMT v2.0
    
    1. SNIa por entorno: Delta_dL = 5-10% (vacío vs cúmulo)
    2. ISW amplificado +26% en supervacíos
    3. Validación r_c(M) por validación cruzada
    
    Autor: Pierre-Olivier Després Asselin
    Fecha: Enero 2026
    """
    
    import numpy as np
    from scipy.integrate import quad
    from scipy.stats import pearsonr, ttest_ind
    
    H0 = 70  # km/s/Mpc
    Omega_m = 0.315
    Omega_Lambda = 0.685
    beta = 0.4  # Parámetro TMT
    
    # ... [Código completo disponible en GitHub]
    ```

[:material-download: Descargar script completo](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/test_3_predictions_TMT.py){ .md-button }

---

### 7. Efecto ISW

**Resultado**: pred: 18.2% | **Archivo**: `calculate_ISW_improved.py`

Cálculo del efecto Sachs-Wolfe integrado (ISW) para TMT vs ΛCDM.

**Ejecución**:
```bash
cd scripts
python calculate_ISW_improved.py
```

??? note "Mostrar código fuente"
    ```python
    #!/usr/bin/env python3
    """
    Cálculo mejorado del efecto ISW (Integrated Sachs-Wolfe)
    Comparación TMT v2.0 vs LCDM
    
    El efecto ISW mide la variación del potencial gravitacional
    mientras los fotones del CMB atraviesan las estructuras:
    
    Delta_T/T = 2/c² × ∫(dΦ/dt × dl)
    """
    
    import numpy as np
    from scipy.integrate import quad, odeint
    
    H0 = 70.0          # km/s/Mpc
    Omega_m = 0.315
    Omega_Lambda = 0.685
    beta = 0.4         # Parámetro TMT
    
    # ... [Código completo disponible en GitHub]
    ```

[:material-download: Descargar script completo](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calculate_ISW_improved.py){ .md-button }

---

### 8. Tensión de Hubble

**Resultado**: 100% resuelta | **Archivo**: `calibrate_TMT_v23_cosmologie.py`

Demostración de la resolución de la tensión H₀ mediante el campo de temporones.

**Ejecución**:
```bash
cd scripts
python calibrate_TMT_v23_cosmologie.py
```

**Principio**: 
```
Φ_T(ρ=1) = 0 → CMB = ΛCDM exactamente
Φ_T(ρ<1) > 0 → H_local > H_CMB (vacío local)
```

[:material-download: Descargar script completo](https://github.com/cadespres/Maitrise-du-temps/blob/professeur_kronos/scripts/calibrate_TMT_v23_cosmologie.py){ .md-button }

---

## Ejecución Completa

Para reproducir todas las pruebas:

```bash
# Clonar repositorio
git clone https://github.com/cadespres/Maitrise-du-temps.git
cd Maitrise-du-temps

# Instalar dependencias
pip install numpy scipy matplotlib astropy

# Ejecutar pruebas principales
cd scripts
python test_TMT_v2_SPARC_reel.py          # SPARC + k(M)
python investigation_r_c_variation.py      # r_c(M)
python test_3_predictions_TMT.py           # SNIa + ISW + validación
python test_weak_lensing_TMT_vs_LCDM.py   # Weak lensing
python calculate_ISW_improved.py           # ISW detallado
python calibrate_TMT_v23_cosmologie.py     # Tensión H0
```

---

## Resultados Esperados

| Prueba | Valor Esperado | Significado |
|--------|----------------|-------------|
| SPARC | 156/156 (100%) | Todas las galaxias mejoradas vs Newton |
| r_c(M) | r = 0.768 | Fuerte correlación r_c - masa |
| k(M) | R² = 0.64 | Buen ajuste ley de potencia |
| Weak Lensing | ~0% | Halos isotrópicos confirmados |
| SNIa | <2% Δd_L | Compatible con observaciones |
| ISW | ~18% | Efecto detectable |
| H₀ | 0σ tensión | Resolución completa |

---

**Significatividad estadística global**: p = 10⁻¹¹² (>15σ) | Reducción Chi²: 81.2%

*Todos los scripts están bajo licencia MIT y pueden ser usados y modificados libremente.*
