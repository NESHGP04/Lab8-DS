# División de tareas – Lab 8 DuckDB (equipo de 3)

Reparto pensado para que **cada persona trabaje en archivos propios** (sin
conflictos de merge) y **no dependa de entregables de las otras**. Lo único
compartido es un contrato de rutas (abajo), que ya está fijado y no cambia.

## Contrato compartido (no se negocia, ya está definido)

| Elemento | Valor |
|---|---|
| Archivos Parquet | `data/raw/<yellow\|green>/<año>/<tipo>_tripdata_<año>-<mes>.parquet` |
| Patrón de lectura (todos los años/tipos) | `data/raw/*/*/*.parquet` (dentro del contenedor: `/workspace/data/raw/...`) |
| Patrón por tipo / año | `data/raw/yellow/*/*.parquet`, `data/raw/*/2026/*.parquet` |
| Base materializada (Ej. 6) | `data/processed/taxis.duckdb` (tabla `viajes`) |
| Tabla de zonas | `data/raw/zonas/taxi_zone_lookup.csv` |
| Datos de partida | Cada quien ejecuta `python scripts/download_data.py` (el script de la base ya funciona para 2026), así que nadie espera a otra persona. |

Como todas las consultas usan *globs*, el código de B y C sirve igual con 2026,
2024+2026 o 2024+2025+2026: **no hay que reescribirlo** cuando A incorpora más años.

Un `.duckdb` admite un solo escritor: **B y C usan bases/archivos distintos**
(`data/processed/taxis.duckdb` solo lo escribe C; B consulta Parquet directo).

---

## Persona A — Infraestructura, datos y reproducibilidad (≈ 30 pts + discusión)

| Ejercicio | Qué hace |
|---|---|
| **1** (todo) | Fork, `docker compose up`, verificar JupyterLab (8888) y Metabase (3000), herramientas disponibles, explicar importancia del ambiente reproducible |
| **2** (todo) | Modificar `scripts/download_data.py`, documentar cambios, verificar completitud |
| **5.1–5.5, 5.9** | Parametrizar el script por años (`--years 2024 2026`), re-ejecutar sin re-descargar |
| **8.1–8.2** | Agregar 2025, verificar que no se re-descargan archivos |
| **9.5, 9.6, 9.7** | Discusión: incorporar datos con cambios mínimos, automatización en producción, decisiones de reproducibilidad |
| Cierre | README completo (secciones "Cómo levantar / descargar / ejecutar / benchmarks / resultados"), `.gitignore`, revisión final del historial git |

**Archivos propios:** `scripts/download_data.py`, `scripts/verify_data.py`,
`README.md`, `docs/ambiente.md`, `docs/descarga.md`, `docs/discusion_A.md`.
**Rama:** `persona-a/infra-datos`
**Pasaporte (Fase 1, 15 pts) es 100 % de esta persona** → debe estar listo primero.

## Persona B — Exploración y análisis exploratorio (≈ 30 pts + discusión)

| Ejercicio | Qué hace |
|---|---|
| **3** (todo) | Consultas directas sobre Parquet: nº de archivos, registros, columnas, tipos, muestra, calidad de datos; documentar cada consulta (SQL, objetivo, fuente, resultado, decisión); explicar qué es consultar Parquet directo |
| **4** (todo) | Preguntas analíticas: temporal, características, amarillos vs verdes, pago, distribuciones, outliers; ≥ 3 hallazgos |
| **5.6–5.8** | Verificar con DuckDB que 2024+2026 se consultan juntos; ¿hay que modificar las consultas?; documentar validación |
| **8.3** | Comprobar que las consultas siguen funcionando con 2024+2025+2026 |
| **9.1, 9.2, 9.4, 9.8** | Discusión: características útiles de DuckDB, ventajas/limitaciones de Parquet directo, DuckDB vs Pandas, aprendizajes con datos grandes |

**Archivos propios:** `notebooks/01_exploracion.ipynb`, `notebooks/02_eda.ipynb`,
`sql/exploracion/*.sql`, `sql/eda/*.sql`, `docs/consultas_exploracion.md`,
`docs/hallazgos_eda.md`, `docs/discusion_B.md`.
**Rama:** `persona-b/exploracion-eda`

## Persona C — Benchmark, indicadores y tablero (≈ 30 pts + discusión)

| Ejercicio | Qué hace |
|---|---|
| **6** (todo) | Tabla materializada en DuckDB, benchmark Parquet vs tabla con distintos volúmenes (1 mes, 3 meses, año, todo), tabla de tiempos, análisis, cuándo usar cada estrategia |
| **7** (todo) | ≥ 10 preguntas, ≥ 6 indicadores con SQL + visualización en Metabase + interpretación; tablero |
| **8.4–8.7** | Actualizar indicadores/tablero con 2024-2026, evolución temporal, ≥ 3 patrones, documentar consultas |
| **9.3** | Discusión: ventajas/limitaciones de tablas materializadas |

**Archivos propios:** `scripts/benchmark.py`, `scripts/build_duckdb.py`,
`notebooks/03_benchmark.ipynb`, `notebooks/04_indicadores.ipynb`,
`sql/benchmark/*.sql`, `sql/indicadores/*.sql`, `docs/benchmark.md`,
`docs/indicadores.md`, `dashboard/` (capturas/export del tablero),
`docs/discusion_C.md`.
**Rama:** `persona-c/benchmark-tablero`

---

## Balance

| | Fase 1 | Fase 2 (rúbrica) | Total aprox. |
|---|---|---|---|
| **A** | 15 (Ej. 1-2) | 10 (incorporación incremental) + 5 (reproducibilidad) | **30** |
| **B** | – | 15 (consultas directas) + 15 (EDA) | **30** |
| **C** | – | 15 (benchmark) + 15 (indicadores) + 10 (análisis completo, con 8.4–8.7) | **40** |

C tiene más puntos pero A además integra el README y B carga la mayor parte de
la discusión (Ej. 9: 4 de 8 preguntas); en carga de trabajo real es ≈ 33 % cada uno.
Si prefieren equilibrar los puntos, la **discusión 8.5–8.6** (patrones 2024-2026)
puede pasar de C a B sin romper ninguna dependencia.

## Flujo de trabajo en git

1. Cada persona crea su rama (`persona-x/...`) desde `main` y hace commits frecuentes y descriptivos (el historial se evalúa).
2. Como los archivos propios no se solapan, los merges a `main` son triviales. Único archivo con posible conflicto: `README.md` → **solo A lo edita**; B y C le pasan su párrafo "cómo ejecutar" en `docs/` y A lo integra.
3. Nunca se hace commit de `data/raw/**` ni `data/processed/**` (ya ignorados en `.gitignore`).
