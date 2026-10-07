# Consultas de exploración y validación

Estado: SQL preparado, resultados pendientes de ejecución con los archivos Parquet del fork. El notebook `01_exploracion.ipynb` sustituirá este documento con tablas de resultados observados.

Consultar Parquet directo significa leer `data/raw/*/*/*.parquet` con DuckDB sin importar filas a `taxis.duckdb`. El footer registra número de filas y esquema; la estructura columnar permite leer sólo columnas necesarias y omitir algunos grupos según estadísticas. El glob incorpora nuevos archivos en la siguiente ejecución, pero no garantiza que todos los meses esperados estén presentes.

La fuente de cada consulta es el glob `data/raw/*/*/*.parquet`; incluye ambos servicios y todos los años presentes al momento de ejecutarla.

## 01_archivos.sql

**Objetivo:** Determinar archivos, registros según footers y grupos de filas; comparar cobertura.

**Fuente:** `data/raw/*/*/*.parquet`.

**SQL:**

```sql
-- Un registro de metadatos por archivo, no lee filas de viajes.
SELECT regexp_extract(file_name, '(yellow|green)_tripdata_', 1) AS tipo,
       TRY_CAST(regexp_extract(file_name, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio_archivo,
       count(*) AS archivos, sum(num_rows) AS filas_footer,
       sum(num_row_groups) AS grupos_filas
FROM parquet_file_metadata('data/raw/*/*/*.parquet')
GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado:** pendiente de ejecución con datos reales.

**Decisión:** confirmar las cifras y las incidencias con el notebook antes de formular conclusiones.

## 02_registros.sql

**Objetivo:** Contar registros directamente sobre Parquet; comparar con footers.

**Fuente:** `data/raw/*/*/*.parquet`.

**SQL:**

```sql
-- Verifica las cifras del footer mediante un conteo de la lectura directa.
SELECT regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
       TRY_CAST(regexp_extract(filename, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio_archivo,
       count(*) AS filas_count
FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false)
GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado:** pendiente de ejecución con datos reales.

**Decisión:** confirmar las cifras y las incidencias con el notebook antes de formular conclusiones.

## 03_columnas.sql

**Objetivo:** Contrastar columnas físicas yellow y green; justificar unión por nombre.

**Fuente:** `data/raw/*/*/*.parquet`.

**SQL:**

```sql
-- Contrasta presencia física y tipos Parquet, el nivel raíz carece de tipo.
SELECT regexp_extract(file_name, '(yellow|green)_tripdata_', 1) AS tipo,
       name AS columna, string_agg(DISTINCT type, ', ' ORDER BY type) AS tipos_parquet,
       count(DISTINCT file_name) AS archivos_con_columna
FROM parquet_schema('data/raw/*/*/*.parquet')
WHERE name <> 'schema' AND type <> 'NULL'
GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado:** pendiente de ejecución con datos reales.

**Decisión:** confirmar las cifras y las incidencias con el notebook antes de formular conclusiones.

## 04_tipos_y_muestra.sql

**Objetivo:** Ver tipos inferidos y cinco filas; revisar normalización.

**Fuente:** `data/raw/*/*/*.parquet`.

**SQL:**

```sql
-- Ejecutar las dos sentencias por separado en el notebook.
DESCRIBE SELECT * FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false);
SELECT * FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false) LIMIT 5;
```

**Resultado:** pendiente de ejecución con datos reales.

**Decisión:** confirmar las cifras y las incidencias con el notebook antes de formular conclusiones.

## 05_calidad.sql

**Objetivo:** Cuantificar nulos, fechas fuera de año, negativos y pasajeros cero; decidir investigación.

**Fuente:** `data/raw/*/*/*.parquet`.

**SQL:**

```sql
-- Requiere ejecutar antes sql/eda/00_vista.sql.
SELECT tipo, anio_archivo, count(*) AS viajes,
       count(*) FILTER (WHERE inicio IS NULL OR fin IS NULL) AS fechas_nulas,
       count(*) FILTER (WHERE inicio IS NOT NULL AND year(inicio) <> anio_archivo) AS inicio_fuera_anio,
       count(*) FILTER (WHERE fin < inicio) AS fin_antes_inicio,
       count(*) FILTER (WHERE fin > inicio + INTERVAL '24 hours') AS duracion_mayor_24h,
       count(*) FILTER (WHERE distancia_millas IS NULL) AS distancia_nula,
       count(*) FILTER (WHERE distancia_millas < 0) AS distancia_negativa,
       count(*) FILTER (WHERE distancia_millas = 0) AS distancia_cero,
       count(*) FILTER (WHERE tarifa IS NULL OR total IS NULL) AS importes_nulos,
       count(*) FILTER (WHERE tarifa < 0 OR total < 0) AS importes_negativos,
       count(*) FILTER (WHERE pasajeros IS NULL) AS pasajeros_nulos,
       count(*) FILTER (WHERE pasajeros = 0) AS pasajeros_cero,
       count(*) FILTER (WHERE tipo_pago IS NULL) AS pago_nulo
FROM viajes_b GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado:** pendiente de ejecución con datos reales.

**Decisión:** confirmar las cifras y las incidencias con el notebook antes de formular conclusiones.

## 06_validacion_anios.sql

**Objetivo:** Verificar consulta conjunta 2024 y 2026, luego 2025; repetir sin cambiar SQL.

**Fuente:** `data/raw/*/*/*.parquet`.

**SQL:**

```sql
-- Ejecutar tras descargar 2024 y repetir tras incorporar 2025.
SELECT anio_archivo, tipo, count(DISTINCT archivo) AS archivos,
       count(*) AS viajes, min(inicio) AS primera_fecha, max(inicio) AS ultima_fecha
FROM viajes_b
GROUP BY 1, 2 ORDER BY 1, 2;
```

**Resultado:** pendiente de ejecución con datos reales.

**Decisión:** confirmar las cifras y las incidencias con el notebook antes de formular conclusiones.

