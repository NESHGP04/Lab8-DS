# Persona C — Benchmark, indicadores y tablero

Rama: `persona-c/benchmark-tablero` · 15 pts benchmark + 15 pts indicadores + parte de los 10 pts de análisis completo.
Archivos propios: `scripts/benchmark.py`, `scripts/build_duckdb.py`, `notebooks/03_benchmark.ipynb`, `notebooks/04_indicadores.ipynb`, `sql/benchmark/*.sql`, `sql/indicadores/*.sql`, `docs/benchmark.md`, `docs/indicadores.md`, `dashboard/`, `docs/discusion_C.md`.

Es la única persona que **escribe** `data/processed/taxis.duckdb`. Metabase lo abre en solo lectura.

### Ejercicio 6 — Parquet vs tablas DuckDB
- [ ] 6.1 Consultar Parquet directo
- [ ] 6.2 Crear tabla `viajes` en `taxis.duckdb` desde los años descargados
- [ ] 6.3 Elegir consultas representativas (agregación, filtro, join con zonas, top-N…)
- [ ] 6.4 Ejecutar cada consulta sobre Parquet y sobre la tabla
- [ ] 6.5 Registrar tiempos (varias repeticiones, mediana)
- [ ] 6.6 Repetir con distintos volúmenes (1 mes, 3 meses, 1 año, todo)
- [ ] 6.7 Tabla de resultados (`docs/benchmark.md`)
- [ ] 6.8 Documentar las consultas (`sql/benchmark/*.sql`)
- [ ] 6.9 Analizar las diferencias
- [ ] 6.10 ¿Cuándo Parquet directo y cuándo materializar?

### Ejercicio 7 — Indicadores y tablero
- [ ] 7.1 ≥ 10 preguntas de análisis
- [ ] 7.2 Diseñar ≥ 6 indicadores
- [ ] 7.3 Consultas SQL por indicador (`sql/indicadores/*.sql`)
- [ ] 7.4 Visualizaciones en Metabase (+ matplotlib en `04_indicadores.ipynb` como respaldo)
- [ ] 7.5 Tablero conjunto (evidencia en `dashboard/`)
- [ ] 7.6 Justificar cada indicador
- [ ] 7.7 Documentar consultas (`docs/indicadores.md`)
- [ ] 7.8 Interpretar resultados y hallazgos

### Ejercicio 8 — 2024, 2025 y 2026
- [ ] 8.4 Actualizar indicadores y visualizaciones con los 3 años
- [ ] 8.5 Evolución de los indicadores en el tiempo
- [ ] 8.6 ≥ 3 cambios/patrones entre 2024, 2025 y 2026
- [ ] 8.7 Documentar las consultas

### Ejercicio 9
- [ ] 9.3 Ventajas y limitaciones de las tablas materializadas

## Independencia
Solo necesita Parquet locales (los mismos globs). Trabaja con 2026 desde el día 1; cuando A incorpore más años basta con volver a correr `build_duckdb.py` y `benchmark.py`.
