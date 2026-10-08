-- Q1: Agregacion simple — total de viajes y promedio de monto por tipo y anio.
-- Version TABLA DuckDB
SELECT tipo, anio_archivo AS anio,
       count(*)                AS viajes,
       round(avg(total), 2)    AS total_promedio
FROM viajes
GROUP BY 1, 2
ORDER BY 2, 1;
