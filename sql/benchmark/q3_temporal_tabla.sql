-- Q3: Temporal — viajes por mes y anio.
-- Version TABLA DuckDB
SELECT date_trunc('month', inicio)::DATE AS mes,
       count(*) AS viajes
FROM viajes
WHERE inicio IS NOT NULL
GROUP BY 1
ORDER BY 1;
