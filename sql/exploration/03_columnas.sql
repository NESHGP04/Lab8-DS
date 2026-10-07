-- Contrasta presencia física y tipos Parquet, el nivel raíz carece de tipo.
SELECT regexp_extract(file_name, '(yellow|green)_tripdata_', 1) AS tipo,
       name AS columna, string_agg(DISTINCT type, ', ' ORDER BY type) AS tipos_parquet,
       count(DISTINCT file_name) AS archivos_con_columna
FROM parquet_schema('data/raw/*/*/*.parquet')
WHERE name <> 'schema' AND type <> 'NULL'
GROUP BY 1, 2 ORDER BY 2, 1;
