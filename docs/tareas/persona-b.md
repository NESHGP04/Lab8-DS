# Persona B — Exploración y análisis exploratorio

Rama: `persona-b/exploracion-eda` · 15 pts consultas directas + 15 pts análisis exploratorio.
Archivos propios: `notebooks/01_exploracion.ipynb`, `notebooks/02_eda.ipynb`, `sql/exploracion/*.sql`, `sql/eda/*.sql`, `docs/consultas_exploracion.md`, `docs/hallazgos_eda.md`, `docs/discusion_B.md`.

Fuente: SIEMPRE glob sobre Parquet (`data/raw/*/*/*.parquet`); no usa la base `.duckdb`.

### Ejercicio 3 — Consultas directas sobre Parquet
- [ ] 3.1 Cantidad de archivos
- [ ] 3.2 Cantidad de registros (`parquet_file_metadata`, `count(*)`)
- [ ] 3.3 Columnas presentes (yellow vs green)
- [ ] 3.4 Tipos de datos (`DESCRIBE`)
- [ ] 3.5 Muestra de registros
- [ ] 3.6 Problemas de calidad (nulos, fechas fuera de año, distancias/tarifas negativas, passenger_count = 0, etc.)
- [ ] 3.7 Consultas necesarias directamente sobre Parquet
- [ ] 3.8 Documentar CADA consulta: SQL, objetivo, archivos fuente, resultado, decisión (`docs/consultas_exploracion.md`)
- [ ] 3.9 Explicar qué significa consultar Parquet directo y por qué sirve con volúmenes grandes (column pruning, row groups, footer)

### Ejercicio 4 — EDA
Cubrir como mínimo: temporal, características de viajes, amarillos vs verdes, pago, distribuciones, outliers.
- [ ] 4.1 Plantear preguntas (justificadas con el dataset)
- [ ] 4.2 Construir las consultas (`sql/eda/*.sql`)
- [ ] 4.3 Documentar las consultas
- [ ] 4.4 Explicar los resultados
- [ ] 4.5 ≥ 3 hallazgos relevantes (`docs/hallazgos_eda.md`)

### Ejercicio 5 (validación)
- [ ] 5.6 Probar que se consulta 2024 + 2026 juntos
- [ ] 5.7 ¿Hay que modificar las consultas? (no, por los globs)
- [ ] 5.8 Documentar las consultas de validación

### Ejercicio 8
- [ ] 8.3 Re-ejecutar las consultas sobre 2024-2025-2026

### Ejercicio 9 (discusión)
- [ ] 9.1 Características de DuckDB más útiles
- [ ] 9.2 Ventajas y limitaciones de Parquet directo
- [ ] 9.4 Ventajas frente a cargar todo con Pandas
- [ ] 9.8 Qué se aprende con datos grandes que no se ve con datos pequeños

## Independencia
Solo necesita archivos Parquet locales (ejecuta `python scripts/download_data.py` para 2026). No depende de `taxis.duckdb` ni del tablero de C.
