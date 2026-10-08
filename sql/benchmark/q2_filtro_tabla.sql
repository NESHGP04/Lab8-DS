-- Q2: Filtro — viajes largos (> 10 millas), promedio de tarifa por tipo.
-- Version TABLA DuckDB
SELECT tipo,
       count(*)                AS viajes_largos,
       round(avg(tarifa), 2)   AS tarifa_promedio
FROM viajes
WHERE distancia_millas > 10
GROUP BY 1
ORDER BY 1;
