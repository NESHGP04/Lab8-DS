-- Verifica las cifras del footer mediante un conteo de la lectura directa.
SELECT regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
       TRY_CAST(regexp_extract(filename, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio_archivo,
       count(*) AS filas_count
FROM read_parquet('data/raw/*/*/*.parquet', union_by_name = true, filename = true, hive_partitioning = false)
GROUP BY 1, 2 ORDER BY 2, 1;
