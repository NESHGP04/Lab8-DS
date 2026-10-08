-- Indicador 3: Distribución de Recogidas por Distrito (Borough)
-- Top distritos de origen por tipo de taxi.
SELECT 
    z.Borough AS distrito,
    v.tipo,
    count(*) AS total_viajes
FROM viajes v
JOIN zonas z ON v.zona_recogida = z.LocationID
WHERE z.Borough != 'Unknown'
GROUP BY 1, 2
ORDER BY 3 DESC;
