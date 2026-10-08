-- Q3: Temporal — viajes por mes y anio.
-- Version PARQUET
SELECT
    date_trunc('month',
        COALESCE(
            TRY_CAST(tpep_pickup_datetime AS TIMESTAMP),
            TRY_CAST(lpep_pickup_datetime AS TIMESTAMP)
        )
    )::DATE AS mes,
    count(*) AS viajes
FROM read_parquet('{glob}', union_by_name = true, filename = true, hive_partitioning = false)
WHERE COALESCE(
        TRY_CAST(tpep_pickup_datetime AS TIMESTAMP),
        TRY_CAST(lpep_pickup_datetime AS TIMESTAMP)
      ) IS NOT NULL
GROUP BY 1
ORDER BY 1;
