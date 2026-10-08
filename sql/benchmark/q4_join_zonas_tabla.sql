-- Q4: JOIN con zonas — top 10 zonas de recogida por volumen de viajes.
-- Version TABLA DuckDB
SELECT z.Zone AS zona, z.Borough AS borough, count(*) AS viajes
FROM viajes v
JOIN zonas z ON v.zona_recogida = z.LocationID
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10;
