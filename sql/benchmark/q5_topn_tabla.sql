-- Q5: Top-N — los 5 dias con mas viajes por anio.
-- Version TABLA DuckDB
WITH diario AS (
    SELECT anio_archivo AS anio,
           CAST(inicio AS DATE) AS dia,
           count(*) AS viajes
    FROM viajes
    WHERE inicio IS NOT NULL
    GROUP BY 1, 2
),
ranked AS (
    SELECT *, row_number() OVER (PARTITION BY anio ORDER BY viajes DESC) AS rn
    FROM diario
)
SELECT anio, dia, viajes FROM ranked WHERE rn <= 5 ORDER BY anio, rn;
