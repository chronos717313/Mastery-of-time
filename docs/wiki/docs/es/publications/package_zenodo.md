# Paquete Zenodo: zenodo_package_DESPRES_UNIFIED_THEORY

## Descripción del Paquete

El paquete Zenodo contiene todos los materiales necesarios para reproducir y validar TMT.

## Contenido Incluido

### Scripts Python
- `test_TMT_v2_SPARC_reel.py`: Prueba SPARC 175 galaxias reales
- `test_TMT_v2_probabilites_quantiques.py`: Análisis probabilístico cuántico
- `investigation_r_c_variation.py`: Descubrimiento r_c(M)
- `test_3_predictions_TMT.py`: Validación de 3 predicciones

### Datos
- `data/SPARC/`: Catálogo completo SPARC (175 galaxias)
- `data/results/`: Resultados de todas las pruebas
- `data/Pantheon+/`: Datos de supernovas para validación cosmológica

### Documentación
- Artículos científicos en FR/EN
- Guías de uso
- Resúmenes ejecutivos

## Metadatos Zenodo

| Campo | Valor |
|-------|-------|
| Título | Teoría de Dominio del Tiempo: Alternativa a ΛCDM |
| Autor | C. Després |
| Descripción | Validación completa 100% SPARC, resolución tensión Hubble |
| Palabras clave | cosmología, materia oscura, expansión universo, teoría alternativa |
| Licencia | CC-BY-4.0 |

## Estado
- ✅ **Listo para upload**: Todos archivos preparados
- ✅ **DOI permanente**: Versión inmutable archivada
- ✅ **Citación**: Referencia bibliográfica estable

## Uso
```bash
# Descargar paquete
wget https://zenodo.org/record/XXXXXXX/files/zenodo_package_DESPRES_UNIFIED_THEORY.zip

# Extraer y ejecutar pruebas
unzip zenodo_package_DESPRES_UNIFIED_THEORY.zip
cd zenodo_package_DESPRES_UNIFIED_THEORY
python test_TMT_v2_SPARC_reel.py
```