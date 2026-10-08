-- Q1: Agregacion simple — total de viajes y promedio de monto por tipo y anio.
-- Version PARQUET
SELECT
    regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
    TRY_CAST(regexp_extract(filename, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio,
    count(*)                                        AS viajes,
    round(avg(TRY_CAST(total_amount AS DOUBLE)), 2) AS total_promedio
FROM read_parquet('{glob}', union_by_name = true, filename = true, hive_partitioning = false)
GROUP BY 1, 2
ORDER BY 2, 1;
