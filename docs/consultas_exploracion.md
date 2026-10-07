# Consultas de exploración y validación

Fuente: `data/raw/*/*/*.parquet`; archivos existentes de yellow y green. Ejecutado con DuckDB sin base persistente.

## 01_archivos.sql

**Objetivo:** Contar archivos, filas en footers y grupos por servicio y año.

**Archivos fuente:** `data/raw/*/*/*.parquet` (los presentes al ejecutar).

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

**Resultado:**

| tipo | anio_archivo | archivos | filas_footer | grupos_filas |
| --- | --- | --- | --- | --- |
| green | 2024 | 12 | 660218 | 12 |
| yellow | 2024 | 12 | 41169720 | 44 |
| green | 2025 | 12 | 591375 | 12 |
| yellow | 2025 | 12 | 48722602 | 53 |
| green | 2026 | 8 | 337114 | 8 |
| yellow | 2026 | 8 | 29703355 | 32 |

6 filas de salida; se muestran hasta 60.

**Decisión:** Comprobar cobertura y detectar faltantes. Concretar la conclusión con las cifras anteriores.

## 02_registros.sql

**Objetivo:** Contar filas a través de la lectura directa.

**Archivos fuente:** `data/raw/*/*/*.parquet` (los presentes al ejecutar).

**SQL:**

```sql
-- Verifica las cifras del footer mediante un conteo de la lectura directa.
SELECT regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
       TRY_CAST(regexp_extract(filename, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio_archivo,
       count(*) AS filas_count
FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false)
GROUP BY 1, 2 ORDER BY 2, 1;
```

**Resultado:**

| tipo | anio_archivo | filas_count |
| --- | --- | --- |
| green | 2024 | 660218 |
| yellow | 2024 | 41169720 |
| green | 2025 | 591375 |
| yellow | 2025 | 48722602 |
| green | 2026 | 337114 |
| yellow | 2026 | 29703355 |

6 filas de salida; se muestran hasta 60.

**Decisión:** Contrastar totales con footers. Concretar la conclusión con las cifras anteriores.

## 03_columnas.sql

**Objetivo:** Comparar columnas físicas y tipos por servicio.

**Archivos fuente:** `data/raw/*/*/*.parquet` (los presentes al ejecutar).

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

**Resultado:**

| tipo | columna | tipos_parquet | archivos_con_columna |
| --- | --- | --- | --- |
| yellow | Airport_fee | DOUBLE | 32 |
| green | DOLocationID | INT32 | 32 |
| yellow | DOLocationID | INT32 | 32 |
| green | PULocationID | INT32 | 32 |
| yellow | PULocationID | INT32 | 32 |
| green | RatecodeID | INT64 | 32 |
| yellow | RatecodeID | INT64 | 32 |
| green | VendorID | INT32 | 32 |
| yellow | VendorID | INT32 | 32 |
| green | cbd_congestion_fee | DOUBLE | 20 |
| yellow | cbd_congestion_fee | DOUBLE | 20 |
| green | congestion_surcharge | DOUBLE | 32 |
| yellow | congestion_surcharge | DOUBLE | 32 |
| green | ehail_fee | DOUBLE | 32 |
| green | extra | DOUBLE | 32 |
| yellow | extra | DOUBLE | 32 |
| green | fare_amount | DOUBLE | 32 |
| yellow | fare_amount | DOUBLE | 32 |
| green | improvement_surcharge | DOUBLE | 32 |
| yellow | improvement_surcharge | DOUBLE | 32 |
| green | lpep_dropoff_datetime | INT64 | 32 |
| green | lpep_pickup_datetime | INT64 | 32 |
| green | mta_tax | DOUBLE | 32 |
| yellow | mta_tax | DOUBLE | 32 |
| green | passenger_count | INT64 | 32 |
| yellow | passenger_count | INT64 | 32 |
| green | payment_type | INT64 | 32 |
| yellow | payment_type | INT64 | 32 |
| green | request_source | BYTE_ARRAY | 3 |
| yellow | request_source | BYTE_ARRAY | 3 |
| green | store_and_fwd_flag | BYTE_ARRAY | 32 |
| yellow | store_and_fwd_flag | BYTE_ARRAY | 32 |
| green | tip_amount | DOUBLE | 32 |
| yellow | tip_amount | DOUBLE | 32 |
| green | tolls_amount | DOUBLE | 32 |
| yellow | tolls_amount | DOUBLE | 32 |
| green | total_amount | DOUBLE | 32 |
| yellow | total_amount | DOUBLE | 32 |
| yellow | tpep_dropoff_datetime | INT64 | 32 |
| yellow | tpep_pickup_datetime | INT64 | 32 |
| green | trip_distance | DOUBLE | 32 |
| yellow | trip_distance | DOUBLE | 32 |
| green | trip_type | INT64 | 32 |

43 filas de salida; se muestran hasta 60.

**Decisión:** Identificar cambios de esquema. Concretar la conclusión con las cifras anteriores.

## 04_tipos_y_muestra.sql

**Objetivo:** Inspeccionar tipos inferidos y una muestra.

**Archivos fuente:** `data/raw/*/*/*.parquet` (los presentes al ejecutar).

**SQL:**

```sql
-- Ejecutar las dos sentencias por separado en el notebook.
DESCRIBE SELECT * FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false);
SELECT * FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false) LIMIT 5;
```

**Resultado:**

| column_name | column_type | null | key | default | extra |
| --- | --- | --- | --- | --- | --- |
| VendorID | INTEGER | YES | NULL | NULL | NULL |
| lpep_pickup_datetime | TIMESTAMP | YES | NULL | NULL | NULL |
| lpep_dropoff_datetime | TIMESTAMP | YES | NULL | NULL | NULL |
| store_and_fwd_flag | VARCHAR | YES | NULL | NULL | NULL |
| RatecodeID | BIGINT | YES | NULL | NULL | NULL |
| PULocationID | INTEGER | YES | NULL | NULL | NULL |
| DOLocationID | INTEGER | YES | NULL | NULL | NULL |
| passenger_count | BIGINT | YES | NULL | NULL | NULL |
| trip_distance | DOUBLE | YES | NULL | NULL | NULL |
| fare_amount | DOUBLE | YES | NULL | NULL | NULL |
| extra | DOUBLE | YES | NULL | NULL | NULL |
| mta_tax | DOUBLE | YES | NULL | NULL | NULL |
| tip_amount | DOUBLE | YES | NULL | NULL | NULL |
| tolls_amount | DOUBLE | YES | NULL | NULL | NULL |
| ehail_fee | DOUBLE | YES | NULL | NULL | NULL |
| improvement_surcharge | DOUBLE | YES | NULL | NULL | NULL |
| total_amount | DOUBLE | YES | NULL | NULL | NULL |
| payment_type | BIGINT | YES | NULL | NULL | NULL |
| trip_type | BIGINT | YES | NULL | NULL | NULL |
| congestion_surcharge | DOUBLE | YES | NULL | NULL | NULL |
| cbd_congestion_fee | DOUBLE | YES | NULL | NULL | NULL |
| request_source | VARCHAR | YES | NULL | NULL | NULL |
| tpep_pickup_datetime | TIMESTAMP | YES | NULL | NULL | NULL |
| tpep_dropoff_datetime | TIMESTAMP | YES | NULL | NULL | NULL |
| Airport_fee | DOUBLE | YES | NULL | NULL | NULL |
| filename | VARCHAR | YES | NULL | NULL | NULL |

26 filas de salida; se muestran hasta 60.

| VendorID | lpep_pickup_datetime | lpep_dropoff_datetime | store_and_fwd_flag | RatecodeID | PULocationID | DOLocationID | passenger_count | trip_distance | fare_amount | extra | mta_tax | tip_amount | tolls_amount | ehail_fee | improvement_surcharge | total_amount | payment_type | trip_type | congestion_surcharge | cbd_congestion_fee | request_source | tpep_pickup_datetime | tpep_dropoff_datetime | Airport_fee | filename |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2024-01-01 00:46:55 | 2024-01-01 00:58:25 | N | 1 | 236 | 239 | 1 | 1.98 | 12.8 | 1.0 | 0.5 | 3.61 | 0.0 | NULL | 1.0 | 21.66 | 1 | 1 | 2.75 | NULL | NULL | NULL | NULL | NULL | data/raw/green/2024/green_tripdata_2024-01.parquet |
| 2 | 2024-01-01 00:31:42 | 2024-01-01 00:52:34 | N | 1 | 65 | 170 | 5 | 6.54 | 30.3 | 1.0 | 0.5 | 7.11 | 0.0 | NULL | 1.0 | 42.66 | 1 | 1 | 2.75 | NULL | NULL | NULL | NULL | NULL | data/raw/green/2024/green_tripdata_2024-01.parquet |
| 2 | 2024-01-01 00:30:21 | 2024-01-01 00:49:23 | N | 1 | 74 | 262 | 1 | 3.08 | 19.8 | 1.0 | 0.5 | 3.0 | 0.0 | NULL | 1.0 | 28.05 | 1 | 1 | 2.75 | NULL | NULL | NULL | NULL | NULL | data/raw/green/2024/green_tripdata_2024-01.parquet |
| 1 | 2024-01-01 00:30:20 | 2024-01-01 00:42:12 | N | 1 | 74 | 116 | 1 | 2.4 | 14.2 | 1.0 | 1.5 | 0.0 | 0.0 | NULL | 1.0 | 16.7 | 2 | 1 | 0.0 | NULL | NULL | NULL | NULL | NULL | data/raw/green/2024/green_tripdata_2024-01.parquet |
| 2 | 2024-01-01 00:32:38 | 2024-01-01 00:43:37 | N | 1 | 74 | 243 | 1 | 5.14 | 22.6 | 1.0 | 0.5 | 6.28 | 0.0 | NULL | 1.0 | 31.38 | 1 | 1 | 0.0 | NULL | NULL | NULL | NULL | NULL | data/raw/green/2024/green_tripdata_2024-01.parquet |

5 filas de salida; se muestran hasta 60.

**Decisión:** Decidir normalización de fechas y montos. Concretar la conclusión con las cifras anteriores.

## 05_calidad.sql

**Objetivo:** Cuantificar nulos, fechas incoherentes, cantidades negativas y pasajeros cero.

**Archivos fuente:** `data/raw/*/*/*.parquet` (los presentes al ejecutar).

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

**Resultado:**

| tipo | anio_archivo | viajes | fechas_nulas | inicio_fuera_anio | fin_antes_inicio | duracion_mayor_24h | distancia_nula | distancia_negativa | distancia_cero | importes_nulos | importes_negativos | pasajeros_nulos | pasajeros_cero | pago_nulo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| green | 2024 | 660218 | 0 | 20 | 2 | 0 | 0 | 0 | 34574 | 0 | 2185 | 24328 | 6793 | 24328 |
| yellow | 2024 | 41169720 | 0 | 56 | 1575 | 230 | 0 | 0 | 776305 | 0 | 733885 | 4091232 | 401354 | 0 |
| green | 2025 | 591375 | 0 | 21 | 1344 | 2 | 0 | 0 | 24438 | 0 | 1776 | 49880 | 8255 | 49880 |
| yellow | 2025 | 48722602 | 0 | 29 | 2235 | 352 | 0 | 0 | 1402958 | 0 | 2853594 | 11611894 | 260062 | 0 |
| green | 2026 | 337114 | 0 | 14 | 5 | 4 | 0 | 0 | 12212 | 0 | 1025 | 48775 | 4527 | 48775 |
| yellow | 2026 | 29703355 | 0 | 17 | 10 | 263 | 0 | 0 | 952231 | 0 | 161970 | 7716688 | 91359 | 0 |

6 filas de salida; se muestran hasta 60.

**Decisión:** Investigar incidencias sin borrar filas. Concretar la conclusión con las cifras anteriores.

## 06_validacion_anios.sql

**Objetivo:** Comprobar archivos y filas de ambos servicios por año.

**Archivos fuente:** `data/raw/*/*/*.parquet` (los presentes al ejecutar).

**SQL:**

```sql
-- Ejecutar tras descargar 2024 y repetir tras incorporar 2025.
SELECT anio_archivo, tipo, count(DISTINCT archivo) AS archivos,
       count(*) AS viajes, min(inicio) AS primera_fecha, max(inicio) AS ultima_fecha
FROM viajes_b
GROUP BY 1, 2 ORDER BY 1, 2;
```

**Resultado:**

| anio_archivo | tipo | archivos | viajes | primera_fecha | ultima_fecha |
| --- | --- | --- | --- | --- | --- |
| 2024 | green | 12 | 660218 | 2008-12-31 00:00:00 | 2025-01-01 22:21:15 |
| 2024 | yellow | 12 | 41169720 | 2002-12-31 16:46:07 | 2026-06-26 23:53:12 |
| 2025 | green | 12 | 591375 | 2008-12-31 15:13:04 | 2026-01-01 21:09:39 |
| 2025 | yellow | 12 | 48722602 | 2007-12-05 18:45:00 | 2025-12-31 23:59:59 |
| 2026 | green | 8 | 337114 | 2008-12-31 17:35:31 | 2026-08-31 23:58:28 |
| 2026 | yellow | 8 | 29703355 | 2001-01-01 09:23:58 | 2026-08-31 23:59:59 |

6 filas de salida; se muestran hasta 60.

**Decisión:** Confirmar 2024+2026 y repetir con 2025. Concretar la conclusión con las cifras anteriores.

## Consulta directa

DuckDB abre los archivos indicados por el glob sin importarlos a una tabla. El footer contiene esquema, número de filas y metadatos de grupos de filas. La lectura por columnas reduce el trabajo cuando sólo se piden algunas; las estadísticas pueden permitir omitir grupos al filtrar. `union_by_name` alinea esquemas cambiantes, pero agrega trabajo de descubrimiento. El glob incluirá archivos nuevos que cumplan la ruta al volver a ejecutar; no demuestra que la descarga esté completa.

