-- Un registro de metadatos por archivo, no lee filas de viajes.
SELECT regexp_extract(file_name, '(yellow|green)_tripdata_', 1) AS tipo,
       TRY_CAST(regexp_extract(file_name, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio_archivo,
       count(*) AS archivos, sum(num_rows) AS filas_footer,
       sum(num_row_groups) AS grupos_filas
FROM parquet_file_metadata('data/raw/*/*/*.parquet')
GROUP BY 1, 2 ORDER BY 2, 1;
