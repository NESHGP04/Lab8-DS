-- Indicador 5: Tarifa Promedio por Milla
-- Rentabilidad del viaje (ingreso por distancia) a través del tiempo.
SELECT 
    date_trunc('month', inicio)::DATE AS mes,
    tipo,
    sum(tarifa) / NULLIF(sum(distancia_millas), 0) AS tarifa_promedio_por_milla
FROM viajes
WHERE inicio IS NOT NULL 
  AND year(inicio) BETWEEN 2024 AND 2026
  AND distancia_millas > 0 
  AND tarifa > 0 
  AND tarifa < 1000 -- Remueve posibles outliers extremos
GROUP BY 1, 2
ORDER BY 1, 2;
