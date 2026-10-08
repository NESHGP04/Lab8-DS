-- Q5: Top-N — los 5 dias con mas viajes por anio.
-- Version PARQUET
WITH diario AS (
    SELECT
        TRY_CAST(regexp_extract(filename, '(20[0-9]{2})-[0-9]{2}\.parquet$', 1) AS INTEGER) AS anio,
        CAST(COALESCE(
            TRY_CAST(tpep_pickup_datetime AS TIMESTAMP),
            TRY_CAST(lpep_pickup_datetime AS TIMESTAMP)
        ) AS DATE) AS dia,
        count(*) AS viajes
    FROM read_parquet('{glob}', union_by_name = true, filename = true, hive_partitioning = false)
    WHERE COALESCE(
            TRY_CAST(tpep_pickup_datetime AS TIMESTAMP),
            TRY_CAST(lpep_pickup_datetime AS TIMESTAMP)
          ) IS NOT NULL
    GROUP BY 1, 2
),
ranked AS (
    SELECT *, row_number() OVER (PARTITION BY anio ORDER BY viajes DESC) AS rn
    FROM diario
)
SELECT anio, dia, viajes FROM ranked WHERE rn <= 5 ORDER BY anio, rn;
