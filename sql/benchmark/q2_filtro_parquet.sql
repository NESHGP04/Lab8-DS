-- Q2: Filtro — viajes largos (> 10 millas), promedio de tarifa por tipo.
-- Version PARQUET
SELECT
    regexp_extract(filename, '(yellow|green)_tripdata_', 1) AS tipo,
    count(*)                                          AS viajes_largos,
    round(avg(TRY_CAST(fare_amount AS DOUBLE)), 2)    AS tarifa_promedio
FROM read_parquet('{glob}', union_by_name = true, filename = true, hive_partitioning = false)
WHERE TRY_CAST(trip_distance AS DOUBLE) > 10
GROUP BY 1
ORDER BY 1;
